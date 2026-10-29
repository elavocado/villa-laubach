# Structure and hosting

A static website with no backend, database or JavaScript package manager. Python generates HTML and converts photographs to WebP. CSS and JavaScript are copied from `src`.

| Path | Purpose |
| --- | --- |
| scripts/build.py | Templates, bilingual copy and image generation |
| scripts/check.py | Page, language, heading, link and photo checks |
| src/ | Editable CSS and browser JavaScript |
| assets/photos/property/ | Selected property originals with descriptive filenames |
| assets/photos/region/ | Selected regional originals with descriptive filenames |
| content/photos.json | Original filenames, categories and bilingual descriptions |
| content/regional-photo-licenses.json | Regional credits and licences |
| dist/ | Generated output, intentionally tracked for buildless Sites deployment |
| .openai/hosting.json | Existing Sites project identity; no credentials |
| docs/research/ | Curated research snapshots |

Edit sources and rebuild. The root `build.py` is a compatibility wrapper. The complete research archive is included under `research/`; it is not needed to build and is not included in the Pages artifact.

Serve `dist` as the web root. BASE_PATH prefixes local URLs for GitHub Pages; SITE_ORIGIN sets canonical and social-image URLs. The current hosting manifest preserves the existing private Sites preview. GitHub Actions checks pull requests and deploys main to GitHub Pages.

The planner prepares text in the browser and links to Airbnb. It has no email recipient, availability service or booking backend.
