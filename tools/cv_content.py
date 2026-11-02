"""Shared CV content and the public website CV (no phone number) for erfanpj.com.
Facts come from Erfan's own earlier CVs on Drive (FINAL_v3 master, DRAFT_v2, Applied ML & Brain Research CV),
the project READMEs and the live site. Private role variants and the cover letter live in cv_private.py,
which is not part of the public repository."""
NAME = "Erfan Pirjahandideh"
PHONE = ""  # the public CV never shows a phone number; cv_private.py sets it for application CVs
EMAIL = "erfan@erfanpj.com"
LOCATION = "Darmstadt, Germany"
LINKS = [("Portfolio", "erfanpj.com", "https://erfanpj.com/"),
         ("GitHub", "github.com/erfanpj", "https://github.com/erfanpj"),
         ("LinkedIn", "linkedin.com/in/erfan-pirjahandideh", "https://www.linkedin.com/in/erfan-pirjahandideh/")]
GRAD = "2027"
AVAILABILITY = "Available for full-time roles now; start date flexible. Open to relocating to Berlin."

# ---------------- education ----------------
EDU_MSC = ("role", "M.Sc. Artificial Intelligence and Machine Learning", "TU Darmstadt, Germany", "2024 – present")
EDU_MSC_NOTE = ("p", f"In progress; expected graduation {GRAD}.")
EDU_REST_FULL = [
    ("role", "AI master’s studies", "Islamic Azad University, Iran", "2015 – 2019"),
    ("p", "20 credits completed; no thesis; degree not awarded."),
    ("role", "B.Sc. Software Engineering", "Islamic Azad University, Iran", "2009 – 2013"),
    ("role", "Associate Degree in Software Engineering", "Islamic Azad University, Iran", "2006 – 2009"),
]
EDU_REST_SHORT = [
    ("role", "B.Sc. and Associate Degree in Software Engineering", "Islamic Azad University, Iran", "2006 – 2013"),
    ("p", "Earlier AI master’s coursework: 20 credits completed; degree not awarded."),
]

# ---------------- Fraunhofer: generic only, no project-specific study details ----------------
FRAUNHOFER_ROLE = ("role", "Computer Vision & AI Research Assistant", "Fraunhofer IGD, Darmstadt, Germany", "Feb 2026 – present")
FH_GENERIC = "Contribute to image-synthesis and biometric-evaluation experiments in an ongoing research project, with an emphasis on reproducible pipelines, controlled comparisons and documented evaluation."
FH_PUBLIC_TOOLS = "Work with Python, PyTorch and GPU computing through Slurm; document evaluation methods and their limits."

# ---------------- telecom (client names as in Erfan's earlier CVs: MCCI and MTN) ----------------
NAK_ROLE = ("role", "QA Team & Project Lead | Senior Developer Expert", "NAK (MCCI project, telecommunications), Tehran, Iran", "2022 – 2024")
NAK = ["Led the implementation of a monitoring system covering more than 30 services.",
       "Developed a Chrome ticketing extension (jQuery, HTML, CSS) that reduced ticket-resolution time by 25%.",
       "Built Python and Groovy tools and Power BI dashboards to automate workflows and report on operations and project status."]
BEHSA_ROLE = ("role", "Service Desk & Service Management Team Leader", "Behsa (MCCI project, telecommunications), Tehran, Iran", "2018 – 2022")
BEHSA = ["Set up and led a seven-person service desk handling more than 2,000 tickets a month; integrated the MCCI ticketing system with Jira.",
         "Introduced ITIL-aligned workflows that improved response times by 40%; coordinated incident and request resolution against SLAs."]
AHS_ROLE = ("role", "First Technical Support & Helpdesk Engineer", "AHS (MTN Irancell project, telecommunications), Tehran, Iran", "2016 – 2018")
AHS = ["Automated daily management reports used by senior management and the CIO, improving report accuracy by 30%.",
       "Built Chrome extensions and service-desk dashboards that reduced manual workload by 20%; built Telegram bots for automated report updates."]
TELECOM_SHORT_ROLE = ("role", "Telecommunications IT", "NAK and Behsa (MCCI projects), AHS (MTN Irancell project), Tehran, Iran", "2016 – 2024")
TELECOM_SHORT = ["Led a seven-person service desk (2,000+ tickets a month) and the monitoring rollout for 30+ services; integrated ticketing with Jira.",
                 "Reduced ticket-resolution time by 25% with a Chrome ticketing extension and improved response times by 40% with ITIL-aligned workflows.",
                 "Automated management reporting (30% more accurate) and built dashboards that reduced manual service-desk work by 20%."]
FREELANCE_ROLE = ("role", "Freelance Software Developer & Web Designer", "Independent", "2005 – present")
FREELANCE = ["Build web applications, responsive websites, dashboards and workflow automations with PHP, WordPress, Joomla, JavaScript and Python, using AI-assisted development (Cursor, ChatGPT/Codex)."]
EARLIER = [("role", ".NET Programmer", "Charkheh Dadehaye Sabz, Iran", "2011 – 2012"),
           ("b", "Implemented CMS and CLM functionality with ASP.NET, C#, jQuery and MVC."),
           ("role", "Robot Programmer", "Islamic Azad University Robotics Team", "2008 – 2010"),
           ("b", "Programmed robotic systems in C++; Student of the Year recognition, 2010."),
           ("role", "University student job", "Mentoring", "until Apr 2026"),
           ("b", "Mentored a new student.")]

# ---------------- projects (each linked to its repository) ----------------
def proj(title, kind, repo): return ("proj", title, kind, f"github.com/erfanpj/{repo}", f"https://github.com/erfanpj/{repo}")
P = {
 "brain": [proj("Brain Signals Lab — EEG motor imagery", "Completed evaluation · Public dataset", "brain-signals-lab"),
   ("b", "Tested EEG classification of imagined left- vs right-fist movement on public PhysioNet data: 50 participants, 2,245 usable trials, five participant-held-out folds; band and settings chosen on training participants only."),
   ("b", "CSP + LDA reached 61.8% mean accuracy versus a 50.4% majority-class baseline (participant median 57.8%); a reduced EEGNet variant reached 53.9%. Results apply to this evaluated dataset subset, not to EEG decoding in general.")],
 "brain_short": [proj("Brain Signals Lab — EEG evaluation", "Completed evaluation · Public dataset", "brain-signals-lab"),
   ("b", "Participant-held-out EEG evaluation (50 participants, 2,245 trials, five folds): CSP + LDA 61.8% mean accuracy versus a 50.4% majority-class baseline.")],
 "opsdesk": [proj("OpsDesk AI — human-reviewed support automation", "Local prototype · Browser simulation", "opsdesk-ai"),
   ("b", "Built a local support-assistance workflow: handbook retrieval (keyword, BM25, dense, hybrid), proposals from a small local language model, human approval and mock actions."),
   ("b", "Editing a proposal cancels its approval; mock execution is idempotent per approval; every step is written to a hash-chained audit log. A FastAPI review UI and an MCP adapter share the same service."),
   ("b", "On 60 held-out fictional tickets, rules produced 37 fully correct proposals versus 25 from the local model, so I kept the rules as the default.")],
 "opsdesk_short": [proj("OpsDesk AI — human-reviewed support automation", "Local prototype", "opsdesk-ai"),
   ("b", "Local retrieval and language-model proposals with human approval, idempotent mock actions and an audit log. Rules 37/60 versus local model 25/60 on held-out fictional tickets.")],
 "reach_line": [proj("Reachboard — Django Workflow Showcase", "Fictional-data application · Browser simulation available", "reachboard-showcase"),
   ("b", "Django workflow demonstration with server-side pricing, ownership checks, controlled state changes and an audit history; repeated submissions do not create duplicate history entries.")],
 "breast": [proj("Breast Cancer Classifier Comparison", "Completed evaluation · Public benchmark · Not a clinical tool", "Breast_Cancer_Project"),
   ("b", "Reworked an earlier ML exercise to prevent data leakage and separate model selection (nested cross-validation) from final testing; automated tests check that no fit sees a test row."),
   ("b", "On 143 held-out samples, a tuned MLP achieved 0.950 F1 and an untuned logistic-regression baseline 0.951; the more complex model offered no clear advantage on this split.")],
 "breast_short": [proj("Breast Cancer Classifier Comparison", "Completed evaluation · Not a clinical tool", "Breast_Cancer_Project"),
   ("b", "Leakage-aware rework with nested cross-validation; on 143 held-out samples a tuned MLP (F1 0.950) matched an untuned logistic-regression baseline (0.951).")],
 "alz": [proj("Exploratory Alzheimer’s Data Analysis — Julia", "Educational analysis · Synthetic data", "exploratory_alzheimers"),
   ("b", "Reproducible descriptive-analysis workflow with validation, summary tables and 49 automated tests on 2,149 synthetic records. The data does not represent real patients; the results are not medical findings.")],
}
AI_NOTE = ("p", "I used AI coding assistants on these independent projects; each README states what is fictional, local-only or simulated.")

SK = {
 "ai": ("Applied AI & automation", "LLM-assisted workflows, retrieval (keyword, BM25, dense, hybrid), local language models, MCP, human-in-the-loop approval, audit logging, FastAPI; AI-assisted development with Cursor and ChatGPT/Codex."),
 "ml_public": ("ML & computer vision", "Python, PyTorch, CUDA, OpenCV, scikit-learn, Hugging Face Diffusers, biometric evaluation (EER, FMR/FNMR)."),
 "eeg": ("EEG & signals", "MNE, band-pass filtering, CSP, LDA, EEGNet, participant-held-out cross-validation."),
 "eval": ("Evaluation & research engineering", "Held-out and nested cross-validation, simple baselines, reproducible pipelines, dataset-integrity checks, experiment documentation."),
 "sw_public": ("Software & infrastructure", "Python, Julia, SQL, JavaScript, PHP, Groovy; Django, Celery, Laravel, PostgreSQL, MySQL, APIs; Git, Linux, Docker, Slurm, Playwright, Power BI."),
 "proc": ("Process & delivery", "ITIL, Jira, SCSM, SLA/OLA, QA and software testing, workflow automation, stakeholder coordination, team leadership."),
}
def skills(keys): return [("kv", SK[k][0], SK[k][1]) for k in keys]
PUB = "Co-author, “Personality Recognition from Text Based on Deep Learning with Recurrent Neural Network.” 5th International Conference on Fundamental Research in Computer Engineering and Information Technology, 2017."
AWARD = "CEO Special Award for Innovation, MTN, April 2018."
TRAINING = "ISTQB software-testing training and DevOps Foundation (2021); Python Foundation and ITIL Foundation (2017)."
LANGS = "Persian/Farsi — Native | English — Advanced | German — A1"

DOCS = {}
DOCS["Public_site"] = dict(
 file="Erfan-Pirjahandideh-CV", title="Applied AI & Computer Vision", phone=False,
 blocks=[
  ("h", "Profile"),
  ("p", f"Applied AI and automation practitioner with current computer vision research experience at Fraunhofer IGD and ongoing M.Sc. studies in Artificial Intelligence and Machine Learning at TU Darmstadt (expected {GRAD}). Previously spent eight years in telecommunications IT, building operational tools, improving service workflows and leading technical teams. Independent projects demonstrate held-out ML evaluation, simple baselines, human-reviewed automation and reproducible experiments."),
  ("p", "Looking for applied AI, AI automation and ML engineering roles, or a master’s thesis in brain research or neurotechnology. Available now for full-time roles. Based in Darmstadt; open to Berlin, Frankfurt and remote roles based in Germany."),
  ("h", "Research & Professional Experience"), FRAUNHOFER_ROLE, ("b", FH_GENERIC), ("b", FH_PUBLIC_TOOLS),
  NAK_ROLE, *[("b", x) for x in NAK[:2]], BEHSA_ROLE, *[("b", x) for x in BEHSA], AHS_ROLE, *[("b", x) for x in AHS],
  FREELANCE_ROLE, *[("b", x) for x in FREELANCE],
  ("h", "Selected Independent Projects"), *P["brain"], *P["opsdesk"], *P["breast_short"], *P["alz"], *P["reach_line"], AI_NOTE,
  ("h", "Education"), EDU_MSC, EDU_MSC_NOTE, *EDU_REST_SHORT,
  ("h", "Technical Skills"), *skills(["ai", "ml_public", "eval", "sw_public", "proc"]),
  ("h", "Publication & Award"), ("p", PUB), ("p", AWARD),
  ("h", "Languages"), ("p", LANGS),
 ])
COVER = None
