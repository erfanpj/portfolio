"""Build the public CV (no phone number) for erfanpj.com from tools/cv_content.py.

    python tools/build_cv.py

Writes cv/Erfan-Pirjahandideh-CV.docx, a plain-text copy, and the PDF (LibreOffice) into site/.
The private master CV and the role variants are built with tools/build_cvs.py from the same source."""
import shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
tmp = ROOT / "cv" / "_build"
subprocess.run([sys.executable, str(ROOT / "tools" / "build_cvs.py"), str(tmp), "Public_site"], check=True)
shutil.copy(tmp / "Erfan-Pirjahandideh-CV.docx", ROOT / "cv")
shutil.copy(tmp / "Erfan-Pirjahandideh-CV.pdf", ROOT / "site")
md = (tmp / "Erfan-Pirjahandideh-CV.md").read_text(encoding="utf-8")
txt = "\n".join(l.replace("**", "").removeprefix("## ").removeprefix("# ").replace("- ", "• ", 1 if l.startswith("- ") else 0).rstrip() for l in md.splitlines())
(ROOT / "cv" / "Erfan-Pirjahandideh-CV.txt").write_text(txt + "\n", encoding="utf-8")
shutil.rmtree(tmp)
