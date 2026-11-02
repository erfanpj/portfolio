"""One-shot builder: transform design/approved-a.html into site/ production files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "design" / "approved-a.html"
SITE = ROOT / "site"

EXTRA_CSS = """
.skip-link{position:absolute;left:-9999px;top:0;background:var(--amber);color:var(--night);padding:10px 16px;z-index:99;font-weight:600}
.skip-link:focus{left:12px;top:12px}
.hero-controls{position:absolute;z-index:5;right:80px;top:26px;display:flex;gap:10px;align-items:center}
.hero-play{min-height:44px;padding:10px 16px;border-radius:10px;border:1px solid var(--light);background:rgba(28,26,33,.85);color:var(--light);font:600 14px 'Familjen Grotesk',sans-serif;cursor:pointer}
.hero-play:focus-visible{outline:2px solid var(--amber);outline-offset:3px}
.illustration-note{font-size:13px;color:var(--muted);margin:12px 0 0;max-width:52ch;line-height:1.45}
.menu-toggle{display:none;min-width:44px;min-height:44px;border:1px solid var(--muted);border-radius:8px;background:transparent;color:var(--light);cursor:pointer;font-size:20px}
.mobile-nav-panel{display:none}
.mobileSceneWrap{position:relative;margin-top:14px}
.mobileBeam{position:absolute;left:16%;top:6%;width:68%;height:38%;pointer-events:none;opacity:.5;z-index:2}
.mobileBeam svg{width:100%;height:100%}
.mobileStepGrid{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px;margin:16px 0 0;padding:0;list-style:none}
.mobileStepGrid li{font-size:13px;line-height:1.35;color:var(--light);border-top:1px solid var(--darkline);padding-top:10px}
.mobileStepGrid li b{color:var(--amber);font-weight:600;display:block;margin-bottom:2px}
.mobileChem{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
.mobileChem button{min-height:48px;border-radius:10px;border:1px solid #4A4652;background:#1C1A21;color:var(--light);text-align:left;padding:10px 12px;font:600 13px/1.25 'Familjen Grotesk',sans-serif;cursor:pointer}
.mobileChem button[aria-pressed=true]{border-color:var(--amber);box-shadow:0 0 16px rgba(242,165,65,.35)}
.mobileChem button span{display:block;font:400 11px/1.3 'DM Sans',sans-serif;color:var(--muted);margin-top:4px}
.mobileChemLabel{font-size:12px;color:var(--muted);margin-top:12px;line-height:1.4}
.supporting .skillrow h3{font-size:24px}
.dialog-links{display:flex;flex-wrap:wrap;gap:16px;margin-top:18px}
.dialog-links a.ref,.dialog-links a.repo{font-weight:600;font-size:15px}
.dialog-links a.repo{text-decoration:underline;text-underline-offset:4px}
dialog dl{margin:16px 0 0;display:grid;gap:12px}
dialog dt{font-weight:650;font-size:14px;color:var(--brown)}
dialog dd{margin:0;font-size:15px;line-height:1.45;color:var(--text)}
.ai-disclosure{font-size:16px;color:var(--text);max-width:70ch;margin:0}
@media(max-width:870px){
  .hero-controls{display:none}
  .menu-toggle{display:inline-flex;align-items:center;justify-content:center}
  .mobileHero header .desktop-nav{display:none}
  .mobile-nav-panel{position:fixed;inset:0;background:rgba(11,10,14,.78);z-index:40}
  .mobile-nav-panel[hidden]{display:none!important}
  .mobile-nav-panel:not([hidden]){display:block}
  .mobile-nav-panel .sheet{position:absolute;right:0;top:0;bottom:0;width:min(320px,88vw);background:var(--night);padding:24px 22px;border-left:1px solid var(--darkline)}
  .mobile-nav-panel a{display:block;padding:14px 0;border-top:1px solid var(--darkline);color:var(--light);font-size:16px}
  .mobile-nav-panel .close-sheet{margin-bottom:12px;min-height:44px;width:100%;border:1px solid var(--muted);background:transparent;color:var(--light);border-radius:8px;cursor:pointer}
}
@media(max-width:600px){.mobileStepGrid{font-size:12px}}
"""


def extract_css(html: str) -> str:
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    if not m:
        raise SystemExit("no style block")
    css = m.group(1)
    return css.replace("../site/assets/", "assets/")


def extract_hero_inner(html: str) -> str:
    start = html.find('<div class="heroFrame">')
    end = html.find("</div></div><div class=\"mobileHero\">")
    if start < 0 or end < 0:
        raise SystemExit("hero frame markers missing")
    block = html[start:end]
    block = block.replace("../site/assets/", "assets/")
    block = block.replace("../site/Erfan-Pirjahandideh-CV.pdf", "Erfan-Pirjahandideh-CV.pdf")
    block = block.replace('class="designstill"', 'class="hero-scene" id="hero-scene"')
    block = block.replace(
        '<div class="hlab off A lon3"',
        '<p class="hlab off A lon3 illustration-note" style="width:560px;left:780px;top:848px;text-align:center;opacity:.72!important">Illustrated process motifs only — not biological or clinical claims.</p>\n<div class="hlab off A lon3"',
    )
    return block


def main() -> None:
    html = APPROVED.read_text(encoding="utf-8")
    css = extract_css(html)
    fonts = (
        '@font-face{font-family:"Familjen Grotesk";src:url("assets/FamiljenGrotesk.ttf") format("truetype");font-weight:400 700;font-display:swap}\n'
        '@font-face{font-family:"DM Sans";src:url("assets/dm-sans.woff2") format("woff2");font-weight:100 900;font-display:swap}\n'
    )
    (SITE / "styles.css").write_text(fonts + css + EXTRA_CSS, encoding="utf-8")

    hero = extract_hero_inner(html)
    # chemistry tooltips: illustration disclaimer
    hero = hero.replace(
        'aria-label="Dopamine: motivation: do it again"',
        'aria-label="Illustration: dopamine motif — motivation to repeat"',
    )
    hero = hero.replace(
        'aria-label="Serotonin: calm satisfaction"',
        'aria-label="Illustration: serotonin motif — calm satisfaction"',
    )
    hero = hero.replace(
        'aria-label="Oxytocin: trust &amp; togetherness"',
        'aria-label="Illustration: oxytocin motif — trust and togetherness"',
    )
    hero = hero.replace(
        'aria-label="Endorphins: feel-good lift"',
        'aria-label="Illustration: endorphin motif — feel-good lift"',
    )

    index_path = SITE / "index.html"
    index_path.write_text(build_index(hero), encoding="utf-8")
    print("Wrote", index_path, "and styles.css")


def build_index(hero_block: str) -> str:
    # hero_block ends with closing divs for designstill; inject play control after header in hero
    hero_block = hero_block.replace(
        "</header>\n<div class=\"top\"",
        '</header>\n<div class="hero-controls"><button type="button" class="hero-play" id="hero-play" aria-pressed="false" aria-controls="hero-scene">Pause scene</button></div>\n<div class="top"',
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Erfan Pirjahandideh — Evidence Portfolio</title>
  <meta name="description" content="Applied ML and computer vision projects with saved evaluation evidence, live demos, and case notes.">
  <meta property="og:title" content="Erfan Pirjahandideh — Evidence Portfolio">
  <meta property="og:description" content="Follow one idea from question to inspectable result — Brain Signals Lab, OpsDesk, Reachboard, and more.">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="styles.css">
</head>
<body class="field">
<a class="skip-link" href="#skills">Skip to content</a>
<main id="home">
{hero_block}</div></div>

<div class="mobileHero" id="mobile-hero">
  <header>
    <a href="#home">Erfan Pirjahandideh<span>.</span></a>
    <div style="display:flex;gap:10px;align-items:center">
      <button type="button" class="hero-play" id="mobile-hero-play" aria-pressed="false" aria-controls="mobile-hero">Pause</button>
      <button type="button" class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="mobile-nav">Menu</button>
    </div>
    <nav class="desktop-nav" aria-label="Main">
      <a href="#approach">Approach</a>
      <a href="#work">Work</a>
      <a href="#contact">Contact</a>
    </nav>
  </header>
  <div class="mobile-nav-panel" id="mobile-nav" hidden>
    <div class="sheet" role="dialog" aria-modal="true" aria-label="Site menu">
      <button type="button" class="close-sheet" id="menu-close">Close menu</button>
      <a href="#approach">Approach</a>
      <a href="#work">Work</a>
      <a href="#supporting">More demos</a>
      <a href="#log">Progress log</a>
      <a href="#cv">CV</a>
      <a href="#contact">Contact</a>
      <a href="Erfan-Pirjahandideh-CV.pdf">Download CV (PDF)</a>
    </div>
  </div>
  <p class="mfocus">AI · machine learning · brain exploration</p>
  <h1>Every good idea starts as a <em>small signal.</em></h1>
  <p>I'm Erfan. I research computer vision at Fraunhofer IGD and study AI at TU Darmstadt. Follow one question from noticing to sharing.</p>
  <div class="mact">
    <a href="#approach">Follow the signal</a>
    <a href="Erfan-Pirjahandideh-CV.pdf">Download CV</a>
  </div>
  <div class="mobileSceneWrap">
    <svg class="mobileBeam" viewBox="0 0 400 120" aria-hidden="true"><defs><linearGradient id="mbg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F2A541" stop-opacity=".35"/><stop offset="1" stop-color="#F2A541" stop-opacity=".05"/></linearGradient></defs><path d="M20,100 L180,60 L380,20 L370,8 L170,52 L10,92 Z" fill="url(#mbg)"/><path d="M20,100 L180,60 L380,20" fill="none" stroke="#F2A541" stroke-width="1.2" opacity=".55"/></svg>
    <div class="mobileVisual">
      <img class="person" src="assets/portrait-scene.png" alt="Illustrated portrait with laptop and brain cutaway aligned to the signal beam">
      <img class="zoom" src="assets/neuron-scene.png" alt="Illustration of the six-stage process with labels outside the circle">
    </div>
  </div>
  <ol class="mobileStepGrid" aria-label="Six-step process">
    <li><b>01 Notice</b>Look for what the average hides.</li>
    <li><b>02 Make sense</b>Turn symptoms into a question.</li>
    <li><b>03 Decide</b>Pick one comparison you can defend.</li>
    <li><b>04 Build</b>Make the decision inspectable.</li>
    <li><b>05 Test &amp; improve</b>Read what the average missed.</li>
    <li><b>06 Enjoy together</b>Share so others can question it.</li>
  </ol>
  <p class="mobileChemLabel">Process illustration only — not a biological or clinical claim:</p>
  <div class="mobileChem" role="group" aria-label="Illustrated chemistry motifs">
    <button type="button" data-chem="dopamine" aria-pressed="false">Dopamine<span>Illustration · motivation motif</span></button>
    <button type="button" data-chem="serotonin" aria-pressed="false">Serotonin<span>Illustration · calm satisfaction motif</span></button>
    <button type="button" data-chem="oxytocin" aria-pressed="false">Oxytocin<span>Illustration · trust motif</span></button>
    <button type="button" data-chem="endorphins" aria-pressed="false">Endorphins<span>Illustration · feel-good motif</span></button>
  </div>
  <p class="illustration-note">Tap a motif to highlight it in the storyboard. These icons explain the hero narrative, not brain chemistry in real life.</p>
</div>

<aside class="glance"><div class="wrap"><div><small>Based in</small>Darmstadt, Germany</div><div><small>Focus</small>Applied ML &amp; computer vision</div><div><small>Background</small>Eight years in telecom IT</div></div></aside>

<section id="skills" class="band skills"><div class="wrap"><div class="sec-intro"><h2>Skills you can trace.</h2><p>Each skill links to a project or role where I used it.</p></div>
<div class="skillrow"><h3>Model evaluation</h3><div><strong>Design a comparison I can trust.</strong><p>Participant-held-out splits, simple baselines and error analysis.</p></div><a class="ref" href="https://erfanpj.github.io/brain-signals-lab/viewer/">Brain Signals Lab ↗</a></div>
<div class="skillrow"><h3>Computer vision</h3><div><strong>Keep the experiment reproducible.</strong><p>Python, PyTorch, CUDA, face alignment and biometric evaluation.</p></div><a class="ref" href="#cv">Fraunhofer IGD ↗</a></div>
<div class="skillrow"><h3>Software delivery</h3><div><strong>Build for the second attempt.</strong><p>Django, APIs, SQL, approval workflows, testing and service operations.</p></div><a class="ref" href="https://erfanpj.github.io/reachboard-showcase/">Reachboard ↗</a></div>
</div></section>

<section id="work" class="band work"><div class="wrap"><div class="sec-intro"><h2>Selected work.</h2><p>Three independent projects. Each starts with a question and ends with something you can inspect.</p></div>
<article class="project p0"><div class="plate"><figure><img src="assets/brain-viewer-evaluation.png" width="960" height="540" alt="Saved evaluation on public PhysioNet data."><figcaption>Saved evaluation on public PhysioNet data (<a href="assets/ATTRIBUTION.md">source</a>).</figcaption></figure></div><div class="projtext"><span class="projecttype">Machine learning · EEG</span><h3>Brain Signals Lab</h3><p class="question">Does the model work for someone it has never seen?</p><p>I held out whole participants, not random trials. Across five folds and 50 people, CSP + LDA averaged 61.8% accuracy against a 50.4% most-frequent-class baseline. The participant median was 57.8%.</p><div class="links"><a class="ref" href="https://erfanpj.github.io/brain-signals-lab/viewer/">Open the EEG viewer ↗</a><a class="case" href="#case-0">Case study</a></div></div></article>
<article class="project p1"><div class="plate"><figure><img src="assets/opsdesk-fixture-simulation-mobile.png" width="390" height="844" alt="Fictional support ticket; simulated receipt."><figcaption>Fictional support ticket; simulated receipt (<a href="assets/ATTRIBUTION.md">source</a>).</figcaption></figure></div><div class="projtext"><span class="projecttype">Applied AI · workflow design</span><h3>OpsDesk</h3><p class="question">When should a support assistant stop and ask?</p><p>I made a changed draft expire its previous approval. On 60 held-out fictional tickets, rules made 37 fully correct proposals and the local model made 25. The demo simulates actions.</p><div class="links"><a class="ref" href="https://erfanpj.github.io/opsdesk-ai/">Try the approval flow ↗</a><a class="case" href="#case-1">Case study</a></div></div></article>
<article class="project p2"><div class="plate"><figure><img src="assets/reachboard-static-draft-75-desktop.png" width="1280" height="720" alt="Browser fixture with a fictional campaign draft."><figcaption>Public static fixture at draft — 75 RB credits (<a href="assets/ATTRIBUTION.md">source</a>).</figcaption></figure></div><div class="projtext"><span class="projecttype">Software engineering · Django</span><h3>Reachboard</h3><p class="question">What happens when someone submits a campaign twice?</p><p>I fixed the quote at submission, scoped drafts to each advertiser, and made retries leave the audit history unchanged. The public browser fixture uses fictional prices and placements.</p><div class="links"><a class="ref" href="https://erfanpj.github.io/reachboard-showcase/">Explore the campaign demo ↗</a><a class="case" href="#case-2">Case study</a></div></div></article>
</div></section>

<section id="supporting" class="band supporting"><div class="wrap"><div class="sec-intro"><h2>Supporting demos.</h2><p>Smaller public experiments outside the three main highlights.</p></div>
<div class="skillrow"><h3>Recall Studio</h3><div><strong>Train/test splits when rows repeat the same participant.</strong><p>Interactive lesson on leakage when IDs repeat across rows.</p></div><a class="ref" href="https://erfanpj.github.io/recall-studio/">Live demo ↗</a></div>
<div class="skillrow"><h3>Commonnest</h3><div><strong>Fictional household week planning.</strong><p>Tasks, meals, and a shopping list saved in the browser only.</p></div><a class="ref" href="https://erfanpj.github.io/commonnest-showcase/">Live demo ↗</a></div>
</div></section>

<section id="approach" class="band approach"><div class="wrap"><div class="sec-intro"><h2>How I work.</h2><p>One example, from the first observation to a result someone else can explore.</p></div>
<ol class="steps"><li><b>01</b><div><h3>Notice</h3><em>Look for the part that is easy to overlook.</em><p>The EEG average hid how differently the model performed across people.</p></div></li>
<li><b>02</b><div><h3>Make sense</h3><em>Find the question behind the symptom.</em><p>Would the model work on someone whose data it had never seen?</p></div></li>
<li><b>03</b><div><h3>Decide</h3><em>Choose one useful comparison.</em><p>Hold out whole participants and keep a most-frequent-class baseline.</p></div></li>
<li><b>04</b><div><h3>Build</h3><em>Make the decision inspectable.</em><p>Put the five folds, participant scores and saved outputs into a viewer.</p></div></li>
<li><b>05</b><div><h3>Test &amp; improve</h3><em>Look for what the average missed.</em><p>The participant median was 57.8%. Some people scored below chance.</p></div></li>
<li><b>06</b><div><h3>Enjoy it together</h3><em>Share the result so others can question it.</em><p>Anyone can open the viewer, sort the scores and explore the differences.</p></div></li></ol>
</div></section>

<section id="cv" class="band history"><div class="wrap"><div class="sec-intro"><h2>Experience &amp; education.</h2></div><div class="timeline">
<div><time>Feb 2026–present</time><div><h3>Computer Vision and AI Research Assistant</h3><p>Fraunhofer IGD · Darmstadt. Reproducible identity synthesis, face alignment and biometric evaluation on GPU infrastructure.</p></div></div>
<div><time>2024–present</time><div><h3>M.Sc. Artificial Intelligence and Machine Learning</h3><p>TU Darmstadt · In progress, expected in the first half of 2027.</p></div></div>
<div><time>2016–2024</time><div><h3>Telecommunications IT</h3><p>NAK, Behsa and AHS. Service monitoring, ticketing integration, team leadership and reporting automation.</p></div></div>
<div><time>2005–present</time><div><h3>Freelance software development and web design</h3><p>Web applications, responsive websites and workflow automation.</p></div></div>
</div><a class="cvbtn" href="Erfan-Pirjahandideh-CV.pdf">Download my CV <span>PDF · 2 pages</span></a>
<p class="ai-disclosure" style="margin-top:28px">I used AI coding assistants on these independent portfolio projects; each repository README describes scope, local-only pieces, and what the public demo does not run.</p>
</div></section>

<section id="log" class="band log"><div class="wrap"><div class="sec-intro"><h2>Progress log.</h2></div><div class="logs">
<p><time>31 Oct 2026</time><span>Released the EEG evaluation viewer with saved fold and participant results.</span></p>
<p><time>01 Nov 2026</time><span>Released OpsDesk's fictional approval demo with the rules and model comparison.</span></p>
<p><time>02 Nov 2026</time><span>Added Recall Studio and Commonnest as supporting demos in the portfolio index.</span></p>
<p><time>02 Nov 2026</time><span>Shipped the Evidence Portfolio layout for erfanpj.com with animated hero and case-study dialogs.</span></p>
</div></div></section>
</main>

<footer id="contact"><div class="wrap"><h2>Let's compare notes.</h2><p>Have a computer vision problem, a model to evaluate, or a workflow that keeps breaking? I'd like to hear about it.</p>
<a class="email" href="mailto:erfanpj@gmail.com">erfanpj@gmail.com ↗</a>
<div class="footline"><span>Erfan Pirjahandideh · Darmstadt · Independent projects are my own work.</span><div><a href="https://github.com/erfanpj">GitHub ↗</a> <a href="https://www.linkedin.com/in/erfan-pirjahandideh">LinkedIn ↗</a> <a href="#home">Top ↑</a></div></div>
</div></footer>

<dialog id="case-0" aria-labelledby="case-title-0"><form method="dialog"><button class="closecase" type="submit">Close ×</button></form>
<h2 id="case-title-0">Brain Signals Lab</h2>
<h3>Does the model work for someone it has never seen?</h3>
<dl>
<dt>Erfan's choice</dt><dd>Participant-held-out cross-validation on public PhysioNet motor imagery — five folds, 50 people, CSP + LDA.</dd>
<dt>Baseline / failure mode</dt><dd>Most-frequent-class label at 50.4%; random trial splits would inflate scores when the same person appears in train and test.</dd>
<dt>Result</dt><dd>Mean accuracy 61.8%; participant median 57.8%. Saved reports in the static viewer — no retraining in the browser.</dd>
<dt>Limits</dt><dd>One public dataset; engineering comparison only, not clinical or neuroscience evidence.</dd>
</dl>
<div class="dialog-links"><a class="ref" href="https://erfanpj.github.io/brain-signals-lab/viewer/">Public viewer ↗</a><a class="repo" href="https://github.com/erfanpj/brain-signals-lab">Source repository ↗</a></div>
</dialog>

<dialog id="case-1" aria-labelledby="case-title-1"><form method="dialog"><button class="closecase" type="submit">Close ×</button></form>
<h2 id="case-title-1">OpsDesk</h2>
<h3>When should a support assistant stop and ask?</h3>
<dl>
<dt>Erfan's choice</dt><dd>Expire approval when a ticket draft changes; require explicit re-approval before simulated execution.</dd>
<dt>Baseline / failure mode</dt><dd>Rules-only proposals vs a local model on 60 held-out fictional tickets — neither is production support software.</dd>
<dt>Result</dt><dd>Rules: 37/60 fully correct proposals; local model: 25/60. Duplicate execution requests return the first receipt.</dd>
<dt>Limits</dt><dd>Browser fixture simulates the workflow; the Python service runs locally. No real tickets or customer systems.</dd>
</dl>
<div class="dialog-links"><a class="ref" href="https://erfanpj.github.io/opsdesk-ai/">Public demo ↗</a><a class="repo" href="https://github.com/erfanpj/opsdesk-ai">Source repository ↗</a></div>
</dialog>

<dialog id="case-2" aria-labelledby="case-title-2"><form method="dialog"><button class="closecase" type="submit">Close ×</button></form>
<h2 id="case-title-2">Reachboard</h2>
<h3>What happens when someone submits a campaign twice?</h3>
<dl>
<dt>Erfan's choice</dt><dd>Fix quotes at submission, scope drafts per advertiser, and keep audit history unchanged on retries.</dd>
<dt>Baseline / failure mode</dt><dd>Client-side totals and anonymous drafts — easy to double-submit or lose ownership context.</dd>
<dt>Result</dt><dd>Django backend enforces ownership and locked totals; public static fixture shows fictional placements at draft (75 RB credits).</dd>
<dt>Limits</dt><dd>The GitHub Pages demo is a browser simulation. The Django app is separate and local; the fixture does not run that backend.</dd>
</dl>
<div class="dialog-links"><a class="ref" href="https://erfanpj.github.io/reachboard-showcase/">Public demo ↗</a><a class="repo" href="https://github.com/erfanpj/reachboard-showcase">Source repository ↗</a></div>
</dialog>

<script src="hero.js" defer></script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
