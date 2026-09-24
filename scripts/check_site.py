"""Check generated metadata, internal links, feeds and navigation using stdlib."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.links=[];self.ids=set();self.canon=[];self.h1=0;self.ld=False;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='link' and a.get('rel')=='canonical':self.canon.append(a['href'])
        if tag=='script':self.ld=a.get('type')=='application/ld+json'
    def handle_data(self,data):
        if self.ld:json.loads(data)
    def handle_endtag(self,tag):
        if tag=='script':self.ld=False
pages={p:Page(p.read_text()) for p in ROOT.rglob('*.html') if 'templates' not in p.parts}
errors=[]
for p,page in pages.items():
    if 'site-footer' not in p.read_text():continue
    assert page.h1==1,(p,'h1')
    assert len(page.canon)==1,(p,'canonical')
    assert '/news/' in page.links and '/media/' in page.links,p
    assert 'Maintained with assistance from AI agents.' in p.read_text(),p
    for url in page.links:
        u=urlsplit(url)
        if u.scheme or u.netloc:continue
        dest=ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else p.parent/unquote(u.path)
        if not u.path:dest=p
        if dest.is_dir():dest=dest/'index.html'
        if not dest.exists():errors.append((str(p.relative_to(ROOT)),url,'missing path'))
        elif u.fragment and dest in pages and unquote(u.fragment) not in pages[dest].ids:errors.append((str(p.relative_to(ROOT)),url,'missing anchor'))
for name in ['sitemap.xml','feed.xml','news/feed.xml']:ET.parse(ROOT/name)
assert not errors,errors
print(f'Passed: {len(pages)} HTML pages; internal links and anchors; JSON-LD; RSS and sitemaps; navigation and footer.')
