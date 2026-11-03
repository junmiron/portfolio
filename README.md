# Portfolio site

Public portfolio of AI apps I build and ship. One page per app, generated from YAML manifests — the repo is the single source of truth for every app fact (name, links, assets, metrics).

## Layout

```
portfolio/
├── apps/<slug>.yaml        # one manifest per app (schema in apps/README.md)
├── assets/<slug>/          # screenshots/, demo.mp4 (raw), short.mp4, cover.jpg
├── templates/              # Jinja2 templates: base.html, index.html, app.html
├── scripts/build.py        # generates site/ from manifests + templates
├── site/                   # generated output — committed; Vercel serves this as-is
└── vercel.json             # rootDirectory: "site" (no build step on deploy)
```

## Adding or updating an app

1. Write or edit `apps/<slug>.yaml` (schema + example in [apps/README.md](apps/README.md)).
2. Put media under `assets/<slug>/`.
3. Run `python scripts/build.py` (needs `pyyaml` and `jinja2`).
4. Commit the manifest, assets **and** regenerated `site/`, push to `main`.

Vercel has a git-connected project on this repo (`rootDirectory: site`), so every push to `main` auto-deploys. After each deploy, read back the live URL and confirm the page renders (title, links, media) before calling it done.

Rules: never hand-edit pages in `site/` without updating the manifest; never overwrite `demo.mp4` (raw recording) — edits write to new files; metrics are real numbers only, unknowns ship as `{{your number}}`.
