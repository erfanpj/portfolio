# Erfan Pirjahandideh · Evidence Portfolio

Static portfolio and two-page CV for [erfanpj.com](https://erfanpj.com/). GitHub Pages serves only `site/`. The original artwork is adapted for the visitor’s viewport. The contact form is first-party HTML on the same page; the [Google Apps Script mailer](contact/README.md) handles human verification and delivers to the owner.

- [Design decision and interaction contract](DESIGN.md)
- [Editable CV](cv/Erfan-Pirjahandideh-CV.docx), [plain text](cv/Erfan-Pirjahandideh-CV.txt), and [public PDF](site/Erfan-Pirjahandideh-CV.pdf)
- [Image credits](site/assets/ATTRIBUTION.md)

## Preview and verify

```powershell
python -m http.server 8791 --bind 127.0.0.1 --directory site
node tools/test_contact.cjs
node tools/smoke_release.cjs
python tools/link_audit.py
```

The browser check requires Playwright and Chromium; set `PLAYWRIGHT_MODULE` or `CHROME_BIN` to select local installations. It checks the whole hero at 12 viewport sizes, 144 × 90 previews, motion preferences, navigation, published PDF bytes and form states. The simulated transport never sends mail. Personal data is not included in release evidence.

Edit the public site in `site/`. The original direction boards and original one-off builders document the first release; they are not inputs for regenerating the current public HTML. Update `tools/build_cv.py` when CV facts change, export the Word master to PDF, check both pages, and update the expected PDF fingerprint in the smoke check.

## Release

The Pages workflow publishes `site/` from main. Verify the custom-domain HTTPS response, assets, real CAPTCHA challenge and reviewed PDF at the final address. An inbox delivery test is separate from a successful build and must use synthetic data.
