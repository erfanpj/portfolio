# Portfolio index (static)

Recruiter-facing static site for **published** portfolio projects only. Intended destination: **`erfanpj/portfolio`** on GitHub Pages at `https://erfanpj.github.io/portfolio/`.

## Local preview (base path)

Pages serves this repository root under `/portfolio/`. Preview the same layout:

```powershell
cd path\to\parent
mkdir review-root -Force
cmd /c mklink /J review-root\portfolio path\to\portfolio-index
python -m http.server 8791 --directory review-root
```

Open http://127.0.0.1:8791/portfolio/

## Checks

```powershell
python tools/link_audit.py
node tools/capture_review.mjs
```

## Scope

- Live links: Brain Signals Lab viewer and OpsDesk fixture only.
- Screenshots: see `assets/ATTRIBUTION.md`.
- No backend, secrets, or unpublished project cards.

## AI assistance

Copy aligns with upstream project READMEs; this index was drafted with AI coding assistants and awaits editorial review before publish.
