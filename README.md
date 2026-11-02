# Portfolio index

Static recruiter-facing index for **`erfanpj/portfolio`** → `https://erfanpj.github.io/portfolio/`.

## Pages artifact

GitHub Actions deploys **`site/`** only (HTML, CSS, screenshots, attribution). QA scripts and review captures stay outside that folder.

## Local preview (`/portfolio/` base path)

```powershell
mkdir review-root\portfolio -Force
cmd /c mklink /J review-root\portfolio site
python -m http.server 8791 --directory review-root
```

Open http://127.0.0.1:8791/portfolio/

## Checks (local)

```powershell
python tools/link_audit.py
node tools/capture_review.mjs
```
