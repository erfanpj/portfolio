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

## Portfolio analytics

The [GA4 property for erfanpj.com](https://analytics.google.com/analytics/web/#/a414339311p561967861/reports/intelligenthome) uses web stream `G-WHZYD0QJF8`. The site loads the Google tag on its production domain only after the visitor allows analytics. The footer’s **Privacy & analytics** control can change that choice. Enhanced measurement is off in the stream. The site counts page views, CV download clicks and project opens; it omits form entries, query strings and fragments.

Run `node tools/check_analytics.cjs` to check consent, event selection and withdrawal. With `--real-tag` the check loads Google’s public library and intercepts its collection requests locally.

In Explorations, break down `select_content` by **Content ID** for the project and **Content type** for a demo or a case study.

## Release

The Pages workflow publishes `site/` from main. Verify the custom-domain HTTPS response, assets, real CAPTCHA challenge and reviewed PDF at the final address. An inbox delivery test is separate from a successful build and must use synthetic data.
