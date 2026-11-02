# Erfan Pirjahandideh · Evidence Portfolio

Static portfolio and public CV for **erfanpj.com**. The source also supports the GitHub Pages project path `/portfolio/`. Only `site/` is served; it does not need Node, a database, remote fonts, or a build service.

- `site/index.html` — complete homepage, project cases, local artwork, evidence and contact.
- `site/Erfan-Pirjahandideh-CV.pdf` — two-page public CV.
- [Design record](DESIGN.md) — selected direction, original assets and interaction contract.
- [Image credits](site/assets/ATTRIBUTION.md) — public project screenshot sources and font licences.

## Preview and verify

```powershell
python -m http.server 8791 --bind 127.0.0.1 --directory site
python tools/link_audit.py
```

Preview at <http://127.0.0.1:8791/>. The audit checks internal files and fragments, then probes the public destinations. LinkedIn may reject automated requests; the audit reports that limit separately. Use `node tools/capture_review.mjs` on Windows for screenshots at the Pages base path.

With Playwright and Chromium available, `node tools/smoke_release.cjs` serves the site at both URL bases and checks 320–1440px widths, keyboard controls, focus return, motion, project evidence, local media and the hash of the public PDF. Optional environment variables `PLAYWRIGHT_MODULE` and `CHROME_BIN` can select an existing local installation.

The public HTML is committed explicitly. To reproduce it after a change to the generator, run `python tools/build_evidence_site.py`. Its input is the public design handoff in `design/`, and it reuses the original vector artwork for the phone layout. The interaction code and responsive refinements are maintained in `site/`.

## Release

The existing GitHub Pages workflow deploys `site/` from `main`. Publish reviewed source through the normal repository process. The GitHub Pages custom-domain setting and the registrar's website records are separate from pushing a review branch. Verify the apex over HTTPS, the projects, and the same PDF bytes at the final address before declaring a release live.
