# Villa Laubach

German and English website for a former schoolhouse in Laubach, Eifel. Includes the house story, 25 gallery photos, excursions, credits and a local enquiry planner. No advertised prices.

[GitHub Pages preview](https://elavocado.github.io/villa-laubach/) · [GitHub repository](https://github.com/elavocado/villa-laubach)

## Setup

Use Python 3.13, from this directory:

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/check.py
python -m http.server 8310 --directory dist
```

Open http://localhost:8310/de/ or http://localhost:8310/en/. Stop with Ctrl+C. No sibling photo or research folders are needed.

## Editing

- Templates and bilingual copy: scripts/build.py
- Styles and interactions: src/style.css and src/site.js
- Original photos: assets/photos/
- Photo provenance and licences: content/
- Generated, deployable output: dist/ (rebuild instead of editing manually)

## Handoff

- [Structure and hosting](docs/architecture.md)
- [GitHub handoff](docs/github-handoff.md)
- [Launch checklist](docs/launch-checklist.md)
- [Complete research archive](research/START-HERE-FINAL.md)
- [Curated research handoff](docs/research/README.md)

Preview content: operator details and property photo rights need confirmation before public launch. The planner creates a local draft for Airbnb; it does not send messages or reserve dates. Regional photos retain their individual licences. No blanket open-source licence is assigned.

## Deployment

Pushes to main build, validate and deploy to GitHub Pages automatically. The workflow sets BASE_PATH=/villa-laubach and SITE_ORIGIN=https://elavocado.github.io/villa-laubach. Local and Sites builds keep their existing defaults. Pages is publicly accessible; preview labels and noindex remain until launch details are finalized.

## Full research archive

The `research/` directory contains all 128 archived source files: findings, drafts, captured source pages, historical PDFs and extracts, photos, image credits and Booking references. Start with [the final research index](research/START-HERE-FINAL.md). The visual research board can be opened locally after cloning. Only `dist/` is uploaded to GitHub Pages; archive files are available in the repository. Inclusion does not grant a new licence to third-party materials.
