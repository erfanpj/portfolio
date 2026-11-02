"""Build .docx, .md and .pdf for every CV in cv_content.DOCS plus the cover letter.
Usage: python build_cvs.py OUTDIR [doc keys...]"""
import sys, subprocess
from pathlib import Path
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT, WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.shared import Mm, Pt, RGBColor
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cv_content as C

ACCENT = "7A4E12"; INK = "1E2124"; MUTED = "50565A"; LINK = "1F4E6B"
def base_doc(title):
    d = Document(); d.core_properties.title = title; d.core_properties.author = C.NAME
    s = d.sections[0]; s.page_width, s.page_height = Mm(210), Mm(297)
    s.top_margin = s.bottom_margin = Mm(13); s.left_margin = s.right_margin = Mm(16); s.footer_distance = Mm(7)
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10); st.font.color.rgb = RGBColor.from_string(INK)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    pf = st.paragraph_format; pf.space_before = Pt(0); pf.space_after = Pt(2); pf.line_spacing = 1.07
    lb = d.styles["List Bullet"]; lb.font.name = "Calibri"; lb.font.size = Pt(10)
    lb.paragraph_format.space_after = Pt(1.5); lb.paragraph_format.line_spacing = 1.05
    return d
def run(p, text, bold=False, size=None, color=None, italic=False):
    r = p.add_run(text); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    if color: r.font.color.rgb = RGBColor.from_string(color)
    return r
def hyperlink(p, label, url, size=None):
    rel = p.part.relate_to(url, RT.HYPERLINK, is_external=True)
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), rel)
    r = OxmlElement("w:r"); pr = OxmlElement("w:rPr")
    c = OxmlElement("w:color"); c.set(qn("w:val"), LINK); pr.append(c)
    if size:
        sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(size*2))); pr.append(sz)
    r.append(pr); t = OxmlElement("w:t"); t.text = label; t.set(qn("xml:space"), "preserve"); r.append(t); h.append(r); p._p.append(h)
def bottom_border(p, color="B9B2A8"):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); e = OxmlElement("w:bottom")
    for k, v in [("val","single"),("sz","4"),("space","1"),("color",color)]: e.set(qn("w:"+k), v)
    b.append(e); pPr.append(b)
def para(d, space_before=0, space_after=2, keep=False, align=None):
    p = d.add_paragraph(); f = p.paragraph_format; f.space_before = Pt(space_before); f.space_after = Pt(space_after); f.keep_with_next = keep
    if align is not None: p.alignment = align
    return p
def right_tab(p, d):
    sec = d.sections[0]; width = sec.page_width - sec.left_margin - sec.right_margin
    p.paragraph_format.tab_stops.add_tab_stop(width, WD_TAB_ALIGNMENT.RIGHT)

def header(d, md, tagline, phone):
    p = para(d, space_after=0); run(p, C.NAME, True, 20, INK)
    p = para(d, space_after=3); run(p, tagline, True, 11, ACCENT)
    items = [C.LOCATION] + ([C.PHONE] if phone else []) + [C.EMAIL]
    p = para(d, space_after=0)
    for i, it in enumerate(items):
        if i: run(p, "  |  ", size=9.5, color=MUTED)
        if it == C.EMAIL: hyperlink(p, it, "mailto:" + it, 9.5)
        else: run(p, it, size=9.5)
    p = para(d, space_after=4)
    for i, (label, url) in enumerate(C.LINKS):
        if i: run(p, "  |  ", size=9.5, color=MUTED)
        hyperlink(p, label, url, 9.5)
    bottom_border(p, ACCENT)
    md += [f"# {C.NAME}", f"**{tagline}**", "", " | ".join(items) + "  ", " | ".join(l for l, _ in C.LINKS), ""]

def render(d, md, blocks):
    for b in blocks:
        k = b[0]
        if k == "h":
            p = para(d, space_before=7, space_after=2, keep=True); run(p, b[1].upper(), True, 10.5, ACCENT); bottom_border(p)
            md += ["", f"## {b[1]}", ""]
        elif k == "role":
            _, title, org, dates = b
            p = para(d, space_before=3, space_after=1, keep=True); right_tab(p, d)
            run(p, title, True, 10.3); run(p, "  ·  " + org, size=10, color=MUTED); run(p, "\t" + dates, size=9.5, color=MUTED)
            md += [f"**{title}** · {org} | {dates}  "]
        elif k == "proj":
            _, title, kind, label, url = b
            p = para(d, space_before=3, space_after=1, keep=True)
            run(p, title, True, 10.3); run(p, "  ·  " + kind, italic=True, size=9.5, color=MUTED)
            if url: run(p, "  ·  ", size=9.5, color=MUTED); hyperlink(p, label, url, 9.5)
            md += [f"**{title}** · *{kind}*" + (f" | {label}" if url else "") + "  "]
        elif k == "b":
            p = d.add_paragraph(style="List Bullet"); p.paragraph_format.left_indent = Mm(4.5); p.paragraph_format.first_line_indent = Mm(-3.5)
            run(p, b[1]); md += [f"- {b[1]}"]
        elif k == "p":
            p = para(d, space_after=2); run(p, b[1]); md += [b[1], ""]
        elif k == "kv":
            p = para(d, space_after=1.5); run(p, b[1] + ": ", True); run(p, b[2]); md += [f"**{b[1]}:** {b[2]}  "]

def footer(d):
    f = d.sections[0].footer.paragraphs[0]; f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run(f, C.NAME + "  ·  page ", size=8, color=MUTED)
    fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE"); f._p.append(fld)

def to_pdf(docx, outdir):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(outdir), str(docx)], check=True, capture_output=True)

def build_cv(key, out):
    spec = C.DOCS[key]; d = base_doc(f"{C.NAME} | CV"); md = []
    header(d, md, spec["tagline"], spec["phone"]); render(d, md, spec["blocks"]); footer(d)
    stem = out / spec["file"]; d.save(str(stem) + ".docx"); Path(str(stem) + ".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    to_pdf(str(stem) + ".docx", out); return stem

def build_cover(out):
    spec = C.COVER; d = base_doc(f"{C.NAME} | Cover letter"); md = []
    d.sections[0].left_margin = d.sections[0].right_margin = Mm(22); d.sections[0].top_margin = Mm(16)
    header(d, md, "Applied AI & ML engineer", True)
    for i, t in enumerate(spec["paragraphs"]):
        p = para(d, space_before=4 if i else 8, space_after=4)
        lines = t.split("\n")
        for j, ln in enumerate(lines):
            r = run(p, ln, bold=(ln.startswith("Application:")), size=10.5)
            if j < len(lines) - 1: r.add_break()
        md += [t.replace("\n", "  \n"), ""]
    stem = out / spec["file"]; d.save(str(stem) + ".docx"); Path(str(stem) + ".md").write_text("\n".join(md), encoding="utf-8")
    to_pdf(str(stem) + ".docx", out); return stem

if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    keys = sys.argv[2:] or [k for k in C.DOCS if k != "Public_site"] + ["cover"]
    for k in keys:
        stem = build_cover(out) if k == "cover" else build_cv(k, out)
        pages = subprocess.run(["pdfinfo", str(stem) + ".pdf"], capture_output=True, text=True).stdout
        print(k, stem.name, [l for l in pages.splitlines() if l.startswith("Pages")])
