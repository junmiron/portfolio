# App manifests

One YAML file per app: `apps/<slug>.yaml`. The site is generated from these files by `scripts/build.py` — never hand-edit pages in `site/`; change the manifest, rebuild, commit both.

## Schema

```yaml
slug: my-app            # must match the filename; used for URLs and asset paths
name: My App
tagline: One-line value proposition
problem: What it solves and for whom
stack: [Python, FastAPI, LLM-X]
featured: true                         # optional; highlight one project on the home page
status: live | beta | technical preview | prototype
links:
  github: https://github.com/<user>/<repo>
  huggingface: https://huggingface.co/spaces/<user>/<space>   # or /models/...
  demo: https://<app>.vercel.app                               # if deployed
  contact: https://www.linkedin.com/in/<user>/                 # CTA link
assets:
  screenshots: [1.png, 2.png]    # stored in assets/<slug>/screenshots/
  video_full: demo.mp4           # raw recording; never overwritten by edits
  video_short: short.mp4         # post-ready clip (4:5 or 9:16, H.264 + AAC)
  cover: cover.jpg               # thumbnail for the site card and LinkedIn posts
  videos:                        # optional; replaces video_short for multi-clip demos
    - file: overview.mp4
      label: "Plain-language overview"
      note: "Optional audience-facing one-liner"
      cover: cover-overview.jpg
      captions: overview.vtt
sample:                                  # optional; real output from an actual run
  note: "One line: what the sample is"
  quote: "One real line from the output (e.g. a question asked)"
  diagram: diagram.png             # rendered output image, shown inline
  downloads: [a.pdf, b.html, c.md] # files in assets/<slug>/sample/, linked for download
tldr:                                    # optional; 4-6 labeled bullets, same order every app:
  - label: "What"                  #   What / You get / Why it's different / Runs on / Stack / Status
    text: "One sentence"
sections:                                # optional; "How it works" — question-form sub-headings
  - title: "How does it work?"
    body: "One or two paragraphs"
limitations:                             # optional; honest limits, replaces any "takeaways"
  - "One sentence"
glossary:                                # optional; one-line explains of jargon for non-specialists
  - term: "AutoGen"
    def: "One sentence a non-specialist can follow"
next_steps: "One line showing the project is alive"
intro: "Outcome-first lead paragraph (1-3 sentences), under the tagline"
context: "One line: thesis / personal project / client work, plus your role"
metrics: "one concrete, true number"    # optional; never invented
launched: YYYY-MM-DD
```

## Page structure (standard, all apps)

1. Title, one-line outcome (tagline), status badge
2. Intro (outcome first, not architecture) + context line
3. Links: code, demo, contact
4. Demo: labeled video(s) and screenshots, high on the page
5. TL;DR: 4-6 bullets, same order every app
6. Problem: one or two human sentences, not a copy of the intro
7. How it works: the technical detail, for engineers
8. Stack
9. Sample output: real run, inline diagram + downloads
10. Limitations (honest), then Next steps (one line, shows the project is alive)

Homepage cards can set `featured: true` to highlight an intentional first project. The featured card uses the first screenshot and up to three stack tags; maintain one featured project until more real app manifests exist.
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
