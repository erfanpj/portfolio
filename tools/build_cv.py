"""Build the master CV and its plain-text equivalent from the same copy."""
from pathlib import Path
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.shared import Mm, Pt, RGBColor

import sys
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "cv"
OUT.mkdir(parents=True, exist_ok=True)
STEM = "Erfan-Pirjahandideh-CV"
d = Document()
d.core_properties.title = "Erfan Pirjahandideh | Curriculum vitae"
d.core_properties.author = "Erfan Pirjahandideh"
d.core_properties.subject = "Applied machine learning, computer vision and software engineering"
sec = d.sections[0]
sec.page_width, sec.page_height = Mm(210), Mm(297)
sec.top_margin, sec.bottom_margin = Mm(17), Mm(16)
sec.left_margin, sec.right_margin = Mm(20), Mm(20)
sec.footer_distance = Mm(8)
styles = d.styles
def style(name, size, color="202324", bold=False, before=0, after=0, leading=1.12, keep=False):
    st = styles[name] if name in styles else styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    st.font.name = "Calibri"; st.font.size = Pt(size)
    st.font.color.rgb = RGBColor.from_string(color); st.font.bold = bold
    pf = st.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after); pf.line_spacing = leading
    pf.keep_with_next = keep; pf.widow_control = True
    return st
style("Normal", 11,after=3)
style("Title", 28, "121415", True, after=1, keep=True)
style("Discipline", 14, "503E22", True, after=4, keep=True)
style("Contact", 10.5, after=1)
style("Heading 1", 14, "28251F", True, before=9, after=3, keep=True)
style("Heading 2", 11.8, "242424", True, before=5, after=1, keep=True)
style("Continuation", 13, "503E22", True, after=6, keep=True)
style("RoleDate", 10, "454B4D", False, after=2, keep=True)
style("Detail", 10.9, after=3)
style("Foot", 9, "525759")
for nm in ["Title","Heading 1","Heading 2"]:
    pr=styles[nm]._element.get_or_add_pPr()
    for child in list(pr):
        if child.tag == qn("w:pBdr"): pr.remove(child)
source=[]
def line(text, sty="Detail"):
    source.append(text)
    return d.add_paragraph(text, sty)
def headed(key, body):
    p=d.add_paragraph(style="Detail");p.add_run(key+"  ").bold=True;p.add_run(body)
    source.append(key+"  "+body)
def hyperlink(par, label, url):
    rel=par.part.relate_to(url,RT.HYPERLINK,is_external=True)
    h=OxmlElement("w:hyperlink");h.set(qn("r:id"),rel)
    r=OxmlElement("w:r");props=OxmlElement("w:rPr")
    for tag,val in [("color","294F5A"),("u","single")]:
        e=OxmlElement("w:"+tag);e.set(qn("w:val"),val);props.append(e)
    r.append(props);t=OxmlElement("w:t");t.text=label;r.append(t);h.append(r);par._p.append(h)
def links(items):
    p=d.add_paragraph(style="Contact")
    for i,(label,url) in enumerate(items):
        if i:p.add_run("   |   ")
        if url: hyperlink(p,label,url)
        else:p.add_run(label)
    source.append("  |  ".join(label+(f" ({url})" if url and not url.startswith("mailto:") else "") for label,url in items))
def project(name, url, body):
    p=d.add_paragraph(style="Heading 2");p.add_run(name+"   ");hyperlink(p,"Demo",url)
    source.append(name+" — "+url);line(body)

line("Erfan Pirjahandideh","Title")
line("Computer vision and applied machine learning","Discipline")
links([("Darmstadt, Germany",None),("erfanpj@gmail.com","mailto:erfanpj@gmail.com")])
links([("erfanpj.com","https://erfanpj.com/"),("GitHub","https://github.com/erfanpj"),("LinkedIn","https://www.linkedin.com/in/erfan-pirjahandideh")])
line("Professional profile","Heading 1")
line("Computer vision and AI research assistant at Fraunhofer IGD with eight years of experience in telecommunications IT. My work spans image synthesis, biometric evaluation, service monitoring and software development. My academic background includes artificial intelligence and machine learning studies at TU Darmstadt.")
line("How I work","Heading 1")
line("I start by finding the question behind a failure. I build the smallest useful comparison, test it against a baseline and share enough detail for someone else to challenge the result. That habit connects how I troubleshoot services with how I evaluate models.")
line("Technical skills","Heading 1")
headed("Computer vision and generative models.","Python, PyTorch, CUDA, OpenCV, Hugging Face Diffusers and Datasets; Stable Diffusion, pretrained LoRA, face alignment and biometric embeddings.")
headed("Evaluation and reproducibility.","Participant-held-out testing, simple baselines, EER and FMR/FNMR, experiment logging, identity-wise sampling and dataset integrity. Git, Linux, Docker and Slurm.")
headed("Software and service operations.","Django, APIs, PostgreSQL, PHP, Laravel and JavaScript. Service monitoring, Jira integration, workflow automation, testing and technical documentation.")
line("Selected achievements","Heading 1")
headed("Innovation recognition.","Received the MTN CEO Special Award for Innovation in April 2018.")
headed("Service leadership.","Led a seven-person service desk handling more than 2,000 tickets a month at Behsa. Led the implementation of monitoring for more than 30 services at NAK.")
line("Research experience","Heading 1")
line("Computer Vision and AI Research Assistant","Heading 2")
line("Fraunhofer IGD, Darmstadt, Germany  |  February 2026–present","RoleDate")
line("Build reproducible image-synthesis and evaluation pipelines with Python, PyTorch, CUDA and Stable Diffusion. Align faces, extract 512-dimensional embeddings and compare biometric error rates across controlled experiments.")
line("Run experiments on A100 GPUs with Slurm. Apply quality scoring and identity-wise selection; verify dataset integrity and document evaluation procedures. Developed forms and review checklists for dental data acquisition.")
d.add_page_break(); source.append("\n")
line("Erfan Pirjahandideh","Continuation")
line("Engineering and operations experience","Heading 1")
line("Telecommunications IT","Heading 2")
line("NAK and Behsa, MCCI projects; AHS, MTN project  |  2016–2024","RoleDate")
headed("NAK.","Led service-monitoring implementation and developed a Chrome extension for handling tickets.")
headed("Behsa.","Led the service desk, integrated MCI ticketing with Jira and implemented ITIL-aligned workflows.")
headed("AHS.","Automated management reporting and developed ticketing extensions and service-desk dashboards.")
line("Freelance software development and web design","Heading 2")
line("Independent  |  2005–present","RoleDate")
line("Develop responsive websites and applications using PHP, WordPress, Joomla and JavaScript. Use AI coding tools for implementation, debugging and documentation.")
line("Education","Heading 1")
line("Artificial intelligence and machine learning studies","Heading 2")
line("Technical University of Darmstadt (TU Darmstadt), Germany","RoleDate")
line("Software engineering and earlier AI studies","Heading 2")
line("Islamic Azad University","RoleDate")
line("B.Sc. and Associate Degree in Software Engineering. Earlier postgraduate study in AI: 20 credits.")
line("Research publication","Heading 1")
line("Co-author, “Personality Recognition from Text Based on Deep Learning with Recurrent Neural Network.” 5th International Conference on Fundamental Research in Computer Engineering and Information Technology, 2017.")
line("Professional training","Heading 1")
line("ISTQB software testing and DevOps Foundation (2021); Python Foundation and ITIL Foundation (2017).")
line("Languages","Heading 1")
line("Farsi: native   |   English: advanced   |   German: A1")
line("Independent work","Heading 1")
line("Selected examples include an EEG evaluation viewer, a support workflow and a Django campaign application. Demos and case notes, including the scope of AI coding assistance, are available in my portfolio.")
links([("View selected projects","https://erfanpj.com/#work")])
f=sec.footer.paragraphs[0];f.style="Foot";f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
f.add_run("Erfan Pirjahandideh   /   ")
field=OxmlElement("w:fldSimple");field.set(qn("w:instr"),"PAGE");f._p.append(field)
d.save(OUT/(STEM+".docx"))
(OUT/(STEM+".txt")).write_text("\n".join(source)+"\n",encoding="utf-8")
