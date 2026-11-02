"""Verify portfolio index links resolve and stay on the approved public set."""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "site" / "index.html"

ALLOWED_PREFIXES = (
    "https://erfanpj.github.io/brain-signals-lab/",
    "https://github.com/erfanpj/brain-signals-lab",
    "https://erfanpj.github.io/opsdesk-ai/",
    "https://github.com/erfanpj/opsdesk-ai",
    "https://erfanpj.github.io/reachboard-showcase/",
    "https://github.com/erfanpj/reachboard-showcase",
    "https://erfanpj.github.io/recall-studio/",
    "https://github.com/erfanpj/recall-studio",
    "https://erfanpj.github.io/commonnest-showcase/",
    "https://github.com/erfanpj/commonnest-showcase",
    "https://github.com/erfanpj",
    "https://www.linkedin.com/in/erfan-pirjahandideh",
)

INTERNAL = re.compile(
    r"^(#|assets/|styles\.css|hero\.js|Erfan-Pirjahandideh-CV\.pdf|mailto:erfanpj@gmail.com)"
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        for key, val in attrs:
            if key == "href" and val:
                self.hrefs.append(val)


def main() -> int:
    html = INDEX.read_text(encoding="utf-8")
    parser = LinkParser()
    parser.feed(html)
    problems: list[str] = []
    checked: set[str] = set()
    for href in parser.hrefs:
        if INTERNAL.match(href):
            continue
        if href.startswith("mailto:"):
            if href != "mailto:erfanpj@gmail.com":
                problems.append(f"unexpected mailto: {href}")
            continue
        if not href.startswith("http"):
            problems.append(f"unexpected relative external pattern: {href}")
            continue
        if not any(href.startswith(p) for p in ALLOWED_PREFIXES):
            problems.append(f"href not on allowlist: {href}")
            continue
        if href in checked:
            continue
        checked.add(href)
        headers = {"User-Agent": "portfolio-link-audit/1.0"}
        req = urllib.request.Request(href, method="HEAD", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                if resp.status >= 400:
                    problems.append(f"{href} -> HTTP {resp.status}")
        except urllib.error.HTTPError as exc:
            if exc.code in (405, 403, 501):
                get = urllib.request.Request(href, headers=headers)
                try:
                    with urllib.request.urlopen(get, timeout=20) as resp:
                        if resp.status >= 400:
                            problems.append(f"{href} -> HTTP {resp.status}")
                except urllib.error.HTTPError as get_exc:
                    if get_exc.code == 999 and "linkedin.com" in href:
                        continue
                    problems.append(f"{href} -> HTTP {get_exc.code}")
            elif exc.code == 999 and "linkedin.com" in href:
                continue
            else:
                problems.append(f"{href} -> HTTP {exc.code}")
        except Exception as exc:  # noqa: BLE001
            if "linkedin.com" in href:
                continue
            problems.append(f"{href} -> {exc}")
    if problems:
        print("LINK AUDIT FAIL")
        for line in problems:
            print(line)
        return 1
    print(f"LINK AUDIT OK ({len(checked)} unique https targets checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
