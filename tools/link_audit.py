"""Check the actual public destinations plus local file, PDF and fragment targets."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]/"site"
PROJECTS={"brain-signals-lab","opsdesk-ai","reachboard-showcase","recall-studio","commonnest-showcase"}
LINKEDIN="https://www.linkedin.com/in/erfan-pirjahandideh"
EXTERNAL={LINKEDIN,"https://github.com/erfanpj","https://erfanpj.github.io/brain-signals-lab/viewer/"}|{f"https://github.com/erfanpj/{p}" for p in PROJECTS}|{f"https://erfanpj.github.io/{p}/" for p in PROJECTS}


class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.links=set();self.assets=set();self.duplicate=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:self.duplicate.add(a["id"])
            self.ids.add(a["id"])
        if tag=="a" and a.get("href"):self.links.add(a["href"])
        if tag in {"img","script"} and a.get("src"):self.assets.add(a["src"])
        if tag=="image" and a.get("href"):self.assets.add(a["href"])
        if tag=="link" and a.get("rel") in {"stylesheet","icon"} and a.get("href"):self.assets.add(a["href"])


def probe(href):
    for method in ("HEAD","GET"):
        try:
            req=Request(href,method=method,headers={"User-Agent":"Portfolio-link-check/1.0"})
            with urlopen(req,timeout=14) as res:
                return (href,res.status,"ok" if 200<=res.status<400 else "failed")
        except HTTPError as e:
            if method=="HEAD" and e.code in (403,405,501):continue
            if href==LINKEDIN and e.code in (403,429,999):return href,e.code,"blocks automated requests"
            return href,e.code,"failed"
        except (OSError,URLError) as e:return href,str(e),"failed"


def main():
    p=Page();p.feed((ROOT/"index.html").read_text(encoding="utf-8"));issues=[f"duplicate id #{x}" for x in p.duplicate];public=set()
    for href in sorted(p.links|p.assets):
        u=urlsplit(href)
        if u.scheme=="https" and href in EXTERNAL:public.add(href)
        elif href=="mailto:erfanpj@gmail.com":pass
        elif u.scheme or u.netloc:issues.append(f"unrecognized destination: {href}")
        elif not u.path and u.fragment:
            if unquote(u.fragment) not in p.ids:issues.append(f"missing fragment {href}")
        else:
            asset=(ROOT/unquote(u.path)).resolve()
            if not asset.is_relative_to(ROOT) or not asset.is_file():issues.append(f"missing file {href}")
    ok=0;limited=[]
    with ThreadPoolExecutor(max_workers=6) as pool:
        for href,status,result in pool.map(probe,sorted(public)):
            if result=="ok":ok+=1
            elif result=="failed":issues.append(f"{href} — {status}")
            else:limited.append(f"{href} — HTTP {status}, {result}")
    for item in limited:print("LIMIT:",item)
    for item in issues:print("FAIL:",item)
    print(f"{ok}/{len(public)} public URLs returned HTTP success; {len(limited)} access-limited; {len(issues)} errors. Checked local destinations and fragment IDs.")
    return int(bool(issues))


if __name__=="__main__":raise SystemExit(main())
