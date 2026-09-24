#!/usr/bin/env python3
"""Build news and coverage with the Python standard library; retain existing pages."""
from pathlib import Path
from html import escape as esc
from datetime import date, datetime, timezone
from email.utils import format_datetime
import json, re, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://sayonpramanik.github.io'
TEMPLATE = (ROOT / 'templates/page.html').read_text()

def link(url, label):
    if not (url.startswith('/') and not url.startswith('//') or url.startswith('https://')):
        raise ValueError('Only local paths or HTTPS links are supported')
    return f'<a href="{esc(url, quote=True)}">{esc(label)}</a>'

def render(path, title, description, body, schema, article=False):
    html = TEMPLATE
    for key, value in {'TITLE':esc(title), 'DESCRIPTION':esc(description, quote=True), 'URL':SITE+path, 'BODY':body,
                       'STRUCTURED_DATA':'<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org', **schema},ensure_ascii=False).replace('<','\\u003c')+'</script>'}.items():
        html = html.replace('{{'+key+'}}', value)
    section = '/media/' if path.startswith('/media/') else '/news/'
    html = html.replace(f'<a href="{section}">',f'<a href="{section}" aria-current="page">',1)
    if article:
        html = html.replace('property="og:type" content="website"','property="og:type" content="article"')
    dest = ROOT / path.strip('/') / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)

def row(post):
    return f'<a class="note-row" href="/news/{post["slug"]}/"><time datetime="{post["date"]}">{date.fromisoformat(post["date"]).strftime("%d %B %Y")}</time><div><p class="section-index">{esc(post["category"])}</p><h3>{esc(post["title"])}</h3><p>{esc(post["summary"])}</p></div><span aria-hidden="true">↗</span></a>'

def main():
    posts = json.loads((ROOT/'content/news.json').read_text())
    seen = set()
    for p in posts:
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', p['slug']), 'Invalid slug'
        assert p['slug'] not in seen, 'Duplicate slug'
        seen.add(p['slug'])
        assert date.fromisoformat(p['date']) <= date.today(), 'Future publication date'
        for tag, text in p['body']:
            assert tag in ('p', 'h2'), 'Unsupported body element'
        for url, label in p.get('sources', []) + p.get('related', []): link(url, label)
    posts.sort(key=lambda p:p['date'],reverse=True)
    for p in posts:
        path = '/news/'+p['slug']+'/'
        body = '<article><header class="article-header"><a class="back-link" href="/news/">← News &amp; Updates</a>'
        body += f'<div class="article-meta"><span>{esc(p["category"])}</span><time datetime="{p["date"]}">{date.fromisoformat(p["date"]).strftime("%d %B %Y")}</time></div><h1>{esc(p["title"])}</h1></header><div class="article-body">'
        body += ''.join(f'<{tag}>{esc(text)}</{tag}>' for tag,text in p['body'])
        for heading, key in [('Sources','sources'),('Related reading','related')]:
            if p.get(key): body += '<h2>'+heading+'</h2><ul>'+''.join('<li>'+link(*x)+'</li>' for x in p[key])+'</ul>'
        body += '</div></article>'
        schema = {'@type':'BlogPosting','headline':p['title'],'description':p['summary'],'url':SITE+path,'mainEntityOfPage':SITE+path,'datePublished':p['date'],'dateModified':p.get('modified',p['date']),'author':{'@type':'Person','name':'Sayon Pramanik','url':SITE+'/about/'},'image':SITE+'/og.png','isPartOf':{'@type':'Blog','url':SITE+'/news/','name':'News & Updates'}}
        if p.get('sources'): schema['citation']=[x[0] for x in p['sources']]
        render(path,p['title'],p['summary'],body,schema,True)
    rows = ''.join(row(p) for p in posts)
    body = '<header class="page-intro"><p class="section-index">News &amp; Updates</p><h1>Notes from an evolving research practice.</h1><p class="intro-copy">Research reflections, academic updates and selected news on urban form, collective movement and public life.</p><div class="section-links"><a class="text-link" href="/field-notes/">Explore Field Notes →</a><a class="text-link" href="/media/">Media &amp; Coverage →</a><a class="text-link" href="/news/feed.xml">Subscribe via RSS →</a></div></header><section class="content-section"><div class="notes-list">'+rows+'</div></section>'
    render('/news/','News & Updates','Research reflections and academic updates from Sayon Pramanik, The Bartlett, UCL.',body,{'@type':'Blog','name':'News & Updates','url':SITE+'/news/','blogPost':[{'@type':'BlogPosting','headline':p['title'],'url':SITE+'/news/'+p['slug']+'/'} for p in posts]})
    media = json.loads((ROOT/'content/media.json').read_text())
    body = '<header class="page-intro"><p class="section-index">Media &amp; Coverage</p><h1>Work and achievements in the public record.</h1><p class="intro-copy">Selected newspaper coverage and institutional references, with links to the original sources.</p></header><section class="content-section publication-list">'
    for m in media:
        date.fromisoformat(m['verified'])
        body += f'<article class="publication" id="{esc(m["id"])}"><span class="section-index">{esc(m["category"])}</span><div><p class="project-meta">{esc(m["publisher"])}<br>{esc(m["date_label"])}</p><h2>{esc(m["title"])}</h2><p>{esc(m["summary"])}</p><p class="source-link">{link(m["url"],m["source_label"]+" ↗")}</p></div></article>'
    body += '</section><section class="content-section"><p>For research outputs, see '+link('/publications/','Publications')+'. For recent writing and activity, see '+link('/news/','News & Updates')+'.</p></section>'
    render('/media/','Media & Coverage','Selected newspaper coverage and institutional references to Sayon Pramanik’s work and achievements.',body,{'@type':'CollectionPage','name':'Media & Coverage','url':SITE+'/media/','mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'item':{'@type':'CreativeWork','name':m['title'],'url':m['url'],'publisher':{'@type':'Organization','name':m['publisher']}}} for i,m in enumerate(media)]}})
    preview = '<section class="section"><div class="section-heading"><div><p class="section-index">05 / News &amp; Updates</p><h2>Recent notes &amp; news</h2></div><a class="text-link" href="/news/">All updates →</a></div><div class="notes-list">'+''.join(row(p) for p in posts[:3])+'</div><p>'+link('/media/','Media & Coverage →')+'</p></section>'
    hp = ROOT/'index.html'
    hp.write_text(re.sub(r'<!-- NEWS_PREVIEW_START -->.*?<!-- NEWS_PREVIEW_END -->','<!-- NEWS_PREVIEW_START -->'+preview+'<!-- NEWS_PREVIEW_END -->',hp.read_text(),flags=re.S))
    rss = ET.Element('rss',version='2.0'); channel=ET.SubElement(rss,'channel')
    for k,v in [('title','Sayon Pramanik — News & Updates'),('link',SITE+'/news/'),('description','Research reflections and academic updates on urban form, collective movement and public life.')]: ET.SubElement(channel,k).text=v
    for p in posts:
        item=ET.SubElement(channel,'item')
        for k,v in [('title',p['title']),('link',SITE+'/news/'+p['slug']+'/'),('guid',SITE+'/news/'+p['slug']+'/'),('description',p['summary']),('pubDate',format_datetime(datetime.fromisoformat(p['date']).replace(tzinfo=timezone.utc),usegmt=True))]: ET.SubElement(item,k).text=v
    ET.ElementTree(rss).write(ROOT/'news/feed.xml',encoding='utf-8',xml_declaration=True)
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
    tree=ET.parse(ROOT/'sitemap.xml'); root=tree.getroot(); existing={n.text for n in root.iter('{'+ns+'}loc')}
    for path in ['/news/','/media/']+['/news/'+p['slug']+'/' for p in posts]:
        if SITE+path not in existing: ET.SubElement(ET.SubElement(root,'{'+ns+'}url'),'{'+ns+'}loc').text=SITE+path
    tree.write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    (ROOT/'sitemap.txt').write_text('\n'.join(n.text for n in root.iter('{'+ns+'}loc'))+'\n')
    print(f'Built {len(posts)} updates and {len(media)} verified coverage entries.')

if __name__ == '__main__': main()
