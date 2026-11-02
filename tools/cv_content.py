"""Public CV content for erfanpj.com (no phone number). Private role variants live outside this repo. Facts come from Erfan's own CVs on Drive
(FINAL_v3 master, DRAFT_v2, Applied ML & Brain Research CV), the repo READMEs and the live site.
Placeholders in [[DOUBLE_BRACKETS]] must be filled by Erfan before sending."""
NAME = "Erfan Pirjahandideh"
PHONE = ""  # the public CV never shows a phone number
EMAIL = "erfan@erfanpj.com"
LOCATION = "Darmstadt, Germany"
LINKS = [("https://erfanpj.com", "https://erfanpj.com/"),
         ("https://github.com/erfanpj", "https://github.com/erfanpj"),
         ("https://www.linkedin.com/in/erfan-pirjahandideh/", "https://www.linkedin.com/in/erfan-pirjahandideh/")]
GRAD = "[[MSC_GRAD_DATE]]"

# ---------------- reusable blocks ----------------
EDU_MSC = ("role", "M.Sc. Artificial Intelligence and Machine Learning", "TU Darmstadt, Germany", "2024 – present")
EDU_MSC_NOTE = ("p", f"In progress; expected graduation {GRAD}.")
EDU_REST_FULL = [
    ("role", "AI master’s studies", "Islamic Azad University, Iran", "2015 – 2019"),
    ("p", "20 credits completed; no thesis; degree not completed."),
    ("role", "B.Sc. Software Engineering", "Islamic Azad University, Iran", "2009 – 2013"),
    ("role", "Associate Degree in Software Engineering", "Islamic Azad University, Iran", "2006 – 2009"),
]
EDU_REST_SHORT = [
    ("role", "B.Sc. and Associate Degree in Software Engineering", "Islamic Azad University, Iran", "2006 – 2013"),
    ("p", "Earlier AI master’s coursework: 20 credits, no degree awarded."),
]

FRAUNHOFER_ROLE = ("role", "Computer Vision & AI Research Assistant", "Fraunhofer IGD, Darmstadt, Germany", "Feb 2026 – present")
FH = {
 "wacv": "Work on attribute-driven identity synthesis; paper in preparation, target venue WACV 2027 (ongoing research, no published results yet).",
 "pipe": "Build reproducible generative-model and biometric-evaluation pipelines with Python, PyTorch, CUDA, Hugging Face Diffusers and Datasets, Stable Diffusion 1.5 with a pretrained CelebA-HQ LoRA, InsightFace and ONNX Runtime.",
 "align": "Analyse captions, construct controlled prompts, perform ArcFace-style face alignment and extract 512-dimensional ElasticFace/ElasticCos iResNet100 embeddings.",
 "eval": "Evaluate generated identities with EER and FMR/FNMR; completed individual-attribute and age-pair experiments, with attribute-combination work ongoing.",
 "slurm": "Run GPU experiments through Slurm on A100 infrastructure.",
 "prune": "Contribute to CR-FIQA × DiffProb face-recognition data pruning through quality scoring, identity-wise selection and SHA-256 dataset-integrity checks.",
 "train": "Completed one iResNet50 + CosFace training run on a 75% CASIA-WebFace subset (368,660 images, 10,572 identities) on two A100 GPUs.",
 "dental": "Produced data-collection forms, checklists and review workflows for a dental data-acquisition project (completed and reviewed).",
 "short": "Build reproducible image-synthesis and biometric-evaluation pipelines (PyTorch, CUDA, Stable Diffusion + LoRA, face alignment, 512-d embeddings, EER/FMR/FNMR) and run them on A100 GPUs through Slurm.",
}

NAK_ROLE = ("role", "QA Team & Project Lead | Senior Developer Expert", "NAK (MCI project, telecommunications), Tehran, Iran", "2022 – 2024")
NAK = ["Led the implementation of a monitoring system covering more than 30 services for the mobile operator MCI (Hamrah-e Aval).",
       "Built a Chrome ticketing extension (jQuery, HTML, CSS) that reduced ticket-resolution time by 25%.",
       "Built Python and Groovy tools and Power BI dashboards to automate workflows and report on operations and project status."]
BEHSA_ROLE = ("role", "Service Desk & Service Management Team Leader", "Behsa (MCI project, telecommunications), Tehran, Iran", "2018 – 2022")
BEHSA = ["Set up and led a seven-person service desk handling more than 2,000 tickets a month; integrated MCI ticketing with Jira.",
         "Introduced ITIL-aligned workflows that improved response times by 40%; coordinated incident and request resolution against SLAs."]
AHS_ROLE = ("role", "First Technical Support & Helpdesk Engineer", "AHS (MTN project, telecommunications), Tehran, Iran", "2016 – 2018")
AHS = ["Automated daily management reports for senior management and the CIO, improving report accuracy by 30%.",
       "Built Chrome extensions and service-desk dashboards that reduced manual workload by 20%; built Telegram bots for automated report updates."]
TELECOM_SHORT_ROLE = ("role", "Telecommunications IT, about eight years", "NAK, Behsa (MCI projects) and AHS (MTN project), Tehran, Iran", "2016 – 2024")
TELECOM_SHORT = ["Led a seven-person service desk (2,000+ tickets a month) and the monitoring rollout for 30+ services; integrated MCI ticketing with Jira.",
                 "Cut ticket-resolution time by 25% with a Chrome ticketing extension and improved response times by 40% with ITIL-aligned workflows.",
                 "Automated management reporting (30% more accurate) and built dashboards that reduced manual service-desk work by 20%."]
FREELANCE_ROLE = ("role", "Freelance Software Developer & Web Designer", "Independent", "2005 – present")
FREELANCE = ["Build web applications, responsive websites, dashboards and workflow automations with PHP, WordPress, Joomla, JavaScript and Python, using AI-assisted development (Cursor, ChatGPT/Codex)."]
EARLIER = [("role", ".NET Programmer", "Charkheh Dadehaye Sabz, Iran", "2011 – 2012"),
           ("b", "Implemented CMS and CLM functionality with ASP.NET, C#, jQuery and MVC."),
           ("role", "Robot Programmer", "Islamic Azad University Robotics Team", "2008 – 2010"),
           ("b", "Programmed robotic systems in C++; Student of the Year recognition, 2010."),
           ("role", "University student job", "Mentoring", "until Apr 2026"),
           ("b", "Mentored a new student.")]

P = {
 "brain": [("proj", "Brain Signals Lab — EEG motor imagery", "Completed evaluation · public data", "github.com/erfanpj/brain-signals-lab", "https://github.com/erfanpj/brain-signals-lab"),
   ("b", "Tested whether imagined left- vs right-fist movement can be decoded from the EEG of people the model has never seen: public PhysioNet data, 50 participants, 2,245 trials, five participant-held-out folds; band and settings chosen on training participants only."),
   ("b", "CSP + LDA reached 61.8% mean accuracy vs a 50.4% majority-class baseline (participant median 57.8%); a reduced EEGNet reached 53.9%. A static viewer shows every participant’s result. Engineering result on one public dataset, not a clinical or neuroscience claim.")],
 "opsdesk": [("proj", "OpsDesk AI — human-approved support automation", "Local prototype · browser demo is a simulation", "github.com/erfanpj/opsdesk-ai", "https://github.com/erfanpj/opsdesk-ai"),
   ("b", "Built a local support desk: retrieval over a handbook (keyword, BM25, dense, hybrid), structured proposals from a small local LLM, explicit human approval and mock execution."),
   ("b", "Approval is invalidated when a proposal changes; execution is idempotent per approval id; every step is written to a hash-chained audit log. A FastAPI review UI and an MCP adapter share the same service."),
   ("b", "On 60 held-out fictional tickets the rules baseline produced 37/60 fully correct proposals vs 25/60 for the local model, so I kept rules as the default.")],
 "opsdesk_short": [("proj", "OpsDesk AI — human-approved support automation", "Local prototype", "github.com/erfanpj/opsdesk-ai", "https://github.com/erfanpj/opsdesk-ai"),
   ("b", "Local retrieval + small local LLM proposals + explicit human approval + idempotent mock execution with an audit log, FastAPI review UI and MCP adapter. Rules 37/60 vs local model 25/60 on 60 held-out fictional tickets.")],
 "reach": [("proj", "Reachboard — Django workflow showcase", "Fictional data · browser demo is a simulation", "github.com/erfanpj/reachboard-showcase", "https://github.com/erfanpj/reachboard-showcase"),
   ("b", "Django campaign workflow with server-authoritative pricing, ownership checks, CSRF-protected checkout, explicit state transitions, audit history and idempotent submission (a repeated submit adds no duplicate history).")],
 "breast": [("proj", "Breast cancer classifier comparison", "Completed evaluation · public dataset", "github.com/erfanpj/Breast_Cancer_Project", "https://github.com/erfanpj/Breast_Cancer_Project"),
   ("b", "Rebuilt an earlier analysis with leakage-safe pipelines, nested cross-validation and a held-out test set scored once; automated tests check that no fit sees a test row."),
   ("b", "Tuned MLP F1 0.950 vs 0.951 for plain logistic regression on 143 held-out samples, so the simpler model is just as good. Not a clinical tool.")],
 "alz": [("proj", "Exploratory Alzheimer’s data analysis in Julia", "Descriptive analysis · synthetic data", "github.com/erfanpj/exploratory_alzheimers", "https://github.com/erfanpj/exploratory_alzheimers"),
   ("b", "Descriptive analysis of a synthetic dataset (2,149 records) with validation against the data card, recorded cleaning counts, provenance notes, 95% intervals and 49 tests. Results describe the data generator; no clinical claims.")],
 "dash": [("proj", "Personal planning dashboard", "Ongoing personal project", None, None),
   ("b", "Build and iterate on a planning dashboard with task and schedule views and action-state tracking (JavaScript interface, Python utilities, Node.js/API components, Git).")],
}

SK = {
 "ai": ("Applied AI & automation", "LLM-assisted workflows, retrieval (keyword, BM25, dense, hybrid), local LLMs, MCP, human-in-the-loop approval, audit logging, FastAPI; AI-assisted development with Cursor and ChatGPT/Codex. Currently learning AI agents, LLM evaluation and workflow-automation platforms."),
 "ml": ("ML & computer vision", "PyTorch, CUDA, OpenCV, scikit-learn, Hugging Face Diffusers and Datasets, Stable Diffusion, LoRA, InsightFace, ArcFace, ElasticFace, CosFace, CR-FIQA, ONNX Runtime."),
 "eeg": ("EEG & signals", "MNE, band-pass filtering, CSP, LDA, EEGNet, participant-held-out cross-validation."),
 "eval": ("Evaluation & research engineering", "Held-out and nested cross-validation, simple baselines, EER and FMR/FNMR, bootstrap intervals, reproducible pipelines, identity-wise data selection, dataset-integrity checks, experiment documentation."),
 "sw": ("Software & infrastructure", "Python, Julia, SQL, JavaScript, PHP, Groovy; Django, Celery, Laravel, PostgreSQL, MySQL, APIs; Git, Linux, Docker, Slurm, A100 GPUs, Playwright, Power BI."),
 "proc": ("Process & delivery", "ITIL, Jira, SCSM, SLA/OLA, QA and software testing, workflow automation, stakeholder coordination, team leadership."),
}
PUB = ("p", "Co-author, “Personality Recognition from Text Based on Deep Learning with Recurrent Neural Network.” 5th International Conference on Fundamental Research in Computer Engineering and Information Technology, 2017.")
AWARDS = ("p", "MTN CEO Special Award for Innovation, April 2018. Student of the Year, Islamic Azad University Robotics Team, 2010.")
CERTS = ("p", "ISTQB software-testing training and DevOps Foundation (2021); Python Foundation and ITIL Foundation (2017); Microsoft .NET, SQL Server and MCITP certifications (2012).")
LANG = ("p", "English: advanced (working language) · Farsi: native · German: A1")
OPEN_TO = "Open to applied AI, AI automation, AI enablement and ML engineering roles, and a master’s thesis (brain and neurotech preferred). Berlin, Frankfurt or remote EU; based in Germany."

def skills(keys): return [("kv", SK[k][0], SK[k][1]) for k in keys]

# ---------------- documents ----------------
DOCS = {}
DOCS["Public_site"] = dict(
 file="Erfan-Pirjahandideh-CV", tagline="Applied AI & ML engineer · Computer vision research", phone=False,
 blocks=[
  ("h", "Profile"),
  ("p", f"I’m a Computer Vision & AI Research Assistant at Fraunhofer IGD and an M.Sc. student in Artificial Intelligence and Machine Learning at TU Darmstadt (expected graduation {GRAD}). Before that I spent about eight years in telecom IT, leading a service desk and automating support work: 25% faster ticket resolution and 40% faster response times. I build things people can check: held-out evaluations, simple baselines and human approval before automated actions."),
  ("p", OPEN_TO),
  ("h", "Research experience"), FRAUNHOFER_ROLE,
  ("b", FH["wacv"]),
  ("b", "Build reproducible image-synthesis and evaluation pipelines with Python, PyTorch, CUDA and Stable Diffusion. Align faces, extract 512-dimensional embeddings and compare biometric error rates (EER, FMR/FNMR) across controlled experiments."),
  ("b", "Run experiments on A100 GPUs with Slurm; apply quality scoring and identity-wise selection, verify dataset integrity and document evaluation procedures."),
  ("h", "Selected projects"), *P["brain"], *P["opsdesk"], *P["reach"], *P["breast"], *P["alz"],
  ("p", "I used AI coding assistants on these independent projects; each README states what is fictional, local-only or simulated."),
  ("h", "Professional experience"), NAK_ROLE, *[("b", x) for x in NAK[:2]], BEHSA_ROLE, *[("b", x) for x in BEHSA], AHS_ROLE, *[("b", x) for x in AHS],
  FREELANCE_ROLE, *[("b", x) for x in FREELANCE],
  ("h", "Skills"), *skills(["ai","ml","eval","sw","proc"]),
  ("h", "Education"), EDU_MSC, EDU_MSC_NOTE, *EDU_REST_SHORT,
  ("h", "Additional"), ("kv", "Publication", PUB[1]), ("kv", "Award", "MTN CEO Special Award for Innovation, April 2018."),
  ("kv", "Training", "ISTQB software testing, DevOps Foundation (2021); ITIL Foundation, Python Foundation (2017)."),
  ("kv", "Languages", "English: advanced · Farsi: native · German: A1"),
 ])
