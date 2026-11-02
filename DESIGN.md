# Erfan Pirjahandideh · Evidence Portfolio

**Decision, 2 November 2026.** Erfan chose direction A after reviewing complete desktop and phone designs. The audience is a researcher, engineer or hiring manager trying to understand how Erfan thinks and whether his work supports the skills he describes. The first useful action should be possible without finishing an animation.

| Direction shown | First substantial section | How a visitor reads the work |
| --- | --- | --- |
| A · Evidence Portfolio (selected) | Skills linked to proof | Follow a capability to an actual project, baseline, result and limitation. |
| B · Research Index | Projects, with an index alongside | Browse the experiments first, then consult the skills and career record. |
| C · Working Notebook | One question and a six-step account | Read the method chronologically before browsing other examples. |

Keep the dark Hero 14 header, Erfan’s illustrated portrait, layered cutaway, amber cone, neuron diagram and laptop stickers. Below it, warm paper, ruled rows and large headings make the work readable. Each of the three main project rows pairs an original screenshot with a question and a result. The two smaller demos appear separately. The PDF carries the full employment and education record.

The [selected layout](design/approved-a.html) owns the composition. The [resolved motion reference](design/hero-motion-reference.html) owns the illustration geometry and timing. Semantic colors and page type are in `site/styles.css`; responsive navigation, focus treatment, and caption contrast are in `site/refinements.css`. The inherited vector illustration has its own drawing palette. The same artwork is re-composed for phones from the original paths and bitmap assets, without cropping the desktop screenshot.

**Interactions.** A sticky masthead provides direct section jumps. On phones Menu opens a native dialog. Each case-study link opens a labeled dialog with a close action, Escape and focus return. The visible pause button stops the 20-second motion; a system request for reduced motion shows its final static state. The four illustrated chemistry motifs describe personal feelings, stay readable through the sequence and provide notes on tap or keyboard input. Nothing requires completing the animation.

**Evidence and references.** The supplied CV and the public repositories are authoritative for personal and project claims. This is an English, left-to-right static site; there are no account, payment, form submission or destructive states. The [W3C dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) informs focus containment and return. [Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) informs motion controls; [Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) informs captions and labels. These are interaction references, not sources of portfolio content or visual branding.
