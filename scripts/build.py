#!/usr/bin/env python3
"""Generate site/ from apps/*.yaml manifests and templates/.

Usage:  python scripts/build.py
Needs:  pyyaml, jinja2   (pip install pyyaml jinja2)

Run after adding or editing a manifest. Commit the regenerated site/ together
with the manifest — Vercel serves site/ as-is (vercel.json rootDirectory), so
no build step runs on deploy.
"""
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is required: pip install pyyaml")
try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:
    sys.exit("jinja2 is required: pip install jinja2")

ROOT = Path(__file__).resolve().parent.parent
APPS_DIR = ROOT / "apps"
ASSETS_DIR = ROOT / "assets"
SITE_DIR = ROOT / "site"
TEMPLATES_DIR = ROOT / "templates"

REQUIRED = ("slug", "name", "tagline", "problem", "status")
STATUSES = ("live", "beta", "prototype")


def load_manifests():
    apps = []
    for path in sorted(APPS_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        missing = [f for f in REQUIRED if not data.get(f)]
        if missing:
            sys.exit(f"{path.name}: missing required field(s): {', '.join(missing)}")
        if data["status"] not in STATUSES:
            sys.exit(f'{path.name}: status must be one of {list(STATUSES)}, got {data["status"]!r}')
        if data.get("slug") != path.stem:
            print(f"  warn: {path.name} has slug {data['slug']!r}; using filename stem as slug")
            data["slug"] = path.stem

        base = ASSETS_DIR / data["slug"]
        assets = data.get("assets") or {}
        for key in ("video_full", "video_short", "cover"):
            f = assets.get(key)
            if f and not (base / f).is_file():
                print(f"  warn: {path.name}: assets.{key} -> missing file {base / f}")

        shots = []
        for s in assets.get("screenshots") or []:
            p = base / "screenshots" / s
            if p.is_file():
                shots.append(f"/assets/{data['slug']}/screenshots/{s}")
            else:
                print(f"  warn: {path.name}: missing screenshot {p}")

        video_short = assets.get("video_short")
        cover = assets.get("cover")
        data["_shots"] = shots
        data["_video"] = f"/assets/{data['slug']}/{video_short}" if (video_short and (base / video_short).is_file()) else None
        data["_cover"] = f"/assets/{data['slug']}/{cover}" if (cover and (base / cover).is_file()) else None

        # normalize optional fields for the templates
        data.setdefault("stack", [])
        links = dict(data.get("links") or {})
        for k in ("github", "huggingface", "demo"):
            links[k] = links.get(k) or None
        data["links"] = links
        data["metrics"] = data.get("metrics") or None
        data["launched"] = data.get("launched") or None
        apps.append(data)
    return apps


def copy_assets(apps):
    for app in apps:
        src = ASSETS_DIR / app["slug"]
        if not src.is_dir():
            continue
        dst = SITE_DIR / "assets" / app["slug"]
        for f in sorted(src.rglob("*")):
            if f.is_file():
                out = dst / f.relative_to(src)
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, out)


def clean_site():
    if SITE_DIR.exists():
        for child in SITE_DIR.iterdir():
            if child.name == ".gitkeep":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    SITE_DIR.mkdir(parents=True, exist_ok=True)


def main():
    apps = load_manifests()
    clean_site()
    copy_assets(apps)

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), undefined=StrictUndefined, autoescape=True)
    (SITE_DIR / "index.html").write_text(env.get_template("index.html").render(apps=apps), encoding="utf-8")
    for app in apps:
        out_dir = SITE_DIR / app["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(env.get_template("app.html").render(app=app), encoding="utf-8")

    print(f"built {len(apps)} app page(s): " + (", ".join(a["slug"] for a in apps) or "(none)"))


if __name__ == "__main__":
    main()
