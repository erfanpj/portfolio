# ErfanPJ.com · approved Evidence Portfolio

On 2 November 2026 Erfan selected **A — Evidence Portfolio** after viewing the full desktop and phone design options. This project belongs to his personal website. The design reference is in this directory; only the contents of `site/` are deployed by the existing Pages workflow. Do not publish working files, unrelated CVs or private project evidence.

## What to build

- Retain the original Hero 14 identity. Use the supplied transparent portrait, actual layered cutaway, laptop with stickers, amber tapered cone, six numbered steps and the neuron scene. `hero-motion-reference.html` contains the resolved vector geometry, sequence and animation CSS; it has no Claude runtime or private asset URLs. Keep the wordmark/nav and featured headline. Supply an obvious pause/play control, keyboard support and a legible reduced-motion end state. Identify the chemistry motif as an illustration of the process, not a scientific or clinical assertion; avoid deterministic mood claims.
- Below the hero use the **A** warm-paper skills index, real screenshot-led project rows, six-step EEG example, work/education, dated release log and contact. Preserve the readable typography, ruled rows, colors and generous spacing in `approved-a.html`. The header can become sticky if its height does not obscure section anchors. Avoid an automatic scroll or gated walkthrough.
- On phones build one responsive scene with portrait and cutaway physically aligned, the beam connected to the neuron view, and labels outside the circle. Keep all six stages reachable as a two-column list, with four accessible chemistry controls, navigation with a working Contact link, and a pause control. Do not use the cropped desktop scene fragments in the reference as the mobile implementation.
- Supply useful native case-study dialogs with each question, Erfan’s choice, baseline or failure mode, result and limits, plus the public demo and repository links. Return focus to the opener on close; handle Escape and keyboard navigation. Keep source and demo clearly distinct for OpsDesk and Reachboard. Include the two secondary public demos, Recall Studio and Commonnest, outside the three main highlights.
- Use the actual two-page PDF in `site/Erfan-Pirjahandideh-CV.pdf`. Public contact: erfanpj@gmail.com, https://github.com/erfanpj and https://www.linkedin.com/in/erfan-pirjahandideh. Do not assume availability, expose a telephone number or imply Fraunhofer sponsored the independent projects. Preserve existing source/screenshot attribution and font licenses. No proprietary code or private screenshots.

## Evidence to preserve

| Project | Evidence, limits and destination |
|---|---|
| Brain Signals Lab | Public PhysioNet motor imagery; 50 participants, five participant-held-out folds, mean accuracy 61.8% vs 50.4% most-frequent-class baseline, participant median 57.8%. One dataset, saved results. [Viewer](https://erfanpj.github.io/brain-signals-lab/viewer/) · [Repository](https://github.com/erfanpj/brain-signals-lab) |
| OpsDesk | 60 held-out fictional tickets: rules 37/60 fully correct proposals, local model 25/60. Editing a draft invalidates its approval. Static browser simulation vs local service. [Demo](https://erfanpj.github.io/opsdesk-ai/) · [Repository](https://github.com/erfanpj/opsdesk-ai) |
| Reachboard | Django ownership checks, fixed quotes and retries that leave audit history unchanged. Public browser fixture uses fictional placements and prices. [Demo](https://erfanpj.github.io/reachboard-showcase/) · [Repository](https://github.com/erfanpj/reachboard-showcase) |

Progress log: 31 Oct 2026, EEG viewer; 1 Nov 2026, OpsDesk approval demo; 2 Nov 2026, Recall Studio and Commonnest added to the portfolio index. Include short AI coding assistance credit for the independent work. Education/experience must match the supplied public CV.

## Release criteria

Build on an isolated branch. Preserve the existing site and live links until a reviewed release is ready; no force push. The deployed site must work at either `/portfolio/` or a domain root with relative asset paths. Check 320, 375, 768 and 1440 CSS px; keyboard, menu, focus return, reduced motion, animated/responsive hero, actual PDF, links, licenses, titles and social/SEO metadata. Run the repository’s link audit and a browser smoke test against the actual release, verify the HTTPS response and final asset bytes. The domain target is **erfanpj.com**. A working GitHub Pages default URL is not proof of a custom-domain deployment. Changes to the external DNS/host require evidence of the right site route; do not infer access from repository permissions.
