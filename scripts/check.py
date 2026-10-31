#!/usr/bin/env python3
"""Validate generated URLs, bilingual alternates, assets and unique identifiers."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build import ROUTES, ORIGIN
PUBLIC = ROOT / "public"
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]; self.links=[]; self.lang=None; self.h1=0; self.canonical=[]; self.alternates={}
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if "id" in a: self.ids.append(a["id"])
        if tag=="html": self.lang=a.get("lang")
        if tag=="h1": self.h1+=1
        if tag=="a" and a.get("href"): self.links.append(a["href"])
        if tag in ["script","img"] and a.get("src"): self.links.append(a["src"])
        if tag=="link" and a.get("rel") in ["stylesheet","icon"]: self.links.append(a["href"])
        if tag=="link" and a.get("rel")=="canonical": self.canonical.append(a["href"])
        if tag=="link" and a.get("rel")=="alternate": self.alternates[a["hreflang"]]=a["href"]
pages={}
for key, langs in ROUTES.items():
    for lang,url in langs.items():
        file=PUBLIC / url.strip("/") / "index.html"
        p=Page();p.feed(file.read_text())
        assert p.lang==lang, file
        assert p.h1==1, file
        assert len(p.ids)==len(set(p.ids)), ("duplicate IDs",file)
        assert p.canonical==[ORIGIN+url], file
        assert p.alternates["es"]==ORIGIN+ROUTES[key]["es"], file
        assert p.alternates["en"]==ORIGIN+ROUTES[key]["en"], file
        assert p.alternates["x-default"]==ORIGIN+ROUTES[key]["es"], file
        pages[url]=p
for url,p in pages.items():
    for href in p.links:
        parsed=urlparse(href)
        if parsed.scheme or parsed.netloc: continue
        target=unquote(parsed.path) or url
        if target in pages:
            if parsed.fragment: assert unquote(parsed.fragment) in pages[target].ids, (url,href)
        else: assert (PUBLIC / target.lstrip("/")).is_file(), (url,href)
assert (PUBLIC/"404.html").is_file()
for name in ["social.png","social-en.png"]:
    assert (PUBLIC/name).read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), name
assert "ilustrativ" not in (PUBLIC/"index.html").read_text().lower()
assert "illustrative" not in (PUBLIC/"en/index.html").read_text().lower()
print("PASS: generated pages, both languages, canonical/hreflang, internal links, images, unique IDs.")
