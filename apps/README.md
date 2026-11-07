# App manifests

One YAML file per app: `apps/<slug>.yaml`. The site is generated from these files by `scripts/build.py` — never hand-edit pages in `site/`; change the manifest, rebuild, commit both.

## Schema

```yaml
slug: my-app            # must match the filename; used for URLs and asset paths
name: My App
tagline: One-line value proposition
problem: What it solves and for whom
stack: [Python, FastAPI, LLM-X]
status: live | beta | prototype
links:
  github: https://github.com/<user>/<repo>
  huggingface: https://huggingface.co/spaces/<user>/<space>   # or /models/...
  demo: https://<app>.vercel.app                               # if deployed
assets:
  screenshots: [1.png, 2.png]    # stored in assets/<slug>/screenshots/
  video_full: demo.mp4           # raw recording; never overwritten by edits
  video_short: short.mp4         # post-ready clip (4:5 or 9:16, H.264 + AAC)
  cover: cover.jpg               # thumbnail for the site card and LinkedIn posts
metrics: "one concrete, true number"    # optional; never invented
launched: YYYY-MM-DD
intro: Optional lead paragraph under the tagline (1-3 sentences)
tldr:                                    # optional; short labeled summary bullets
  - label: "What"
    text: "One sentence"
sections:                                # optional; question-form headed blocks, rendered in order
  - title: "What is it?"
    body: "One or two paragraphs"
takeaways:                               # optional; closing bullet list
  - "One sentence"
```

Required fields: `slug`, `name`, `tagline`, `problem`, `status`. Everything else is optional. If a field you want to show is missing or stale, ask the user (or read the app's repo README) — do not guess. Unknown numbers ship as `{{your number}}` in copy; they are never invented.

## Filled example

```yaml
slug: invoice-ocr
name: Invoice OCR
tagline: Turn scanned invoices into structured data in seconds
problem: Small businesses waste hours keying invoice fields by hand; this extracts line items, totals and vendor details from photos or PDFs.
stack: [Python, FastAPI, LLM]
status: beta
links:
  github: https://github.com/junmiron/invoice-ocr
  huggingface: https://huggingface.co/spaces/junmiron/invoice-ocr
  demo: https://invoice-ocr.vercel.app
assets:
  screenshots: [1.png, 2.png]
  video_full: demo.mp4
  video_short: short.mp4
  cover: cover.jpg
metrics: "98.2% field accuracy on a 500-invoice test set"
launched: 2026-11-03
```

## Adding an app (checklist)

1. Write `apps/<slug>.yaml`.
2. Put media in `assets/<slug>/` (`screenshots/`, `demo.mp4`, `short.mp4`, `cover.jpg`).
3. Run `python scripts/build.py` (needs pyyaml + jinja2).
4. Commit manifest + assets + regenerated `site/`, push to `main`. Vercel auto-deploys; verify the live page renders title, links and media before calling it done.
