"""Check every bilingual atlas page has a direct personal-home navigation link."""
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.styles=[]; self.current=None; self.navs=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='nav': self.navs.append(attrs.get('id'))
        if tag=='a': self.current={'attrs':attrs,'text':'','nav':self.navs[-1] if self.navs else None}
        if tag=='link' and attrs.get('rel')=='stylesheet': self.styles.append(attrs.get('href'))
    def handle_data(self, text):
        if self.current is not None: self.current['text']+=text
    def handle_endtag(self, tag):
        if tag=='a' and self.current is not None: self.links.append(self.current);self.current=None
        if tag=='nav' and self.navs: self.navs.pop()

pages=sorted(ROOT.glob('*.html'))
assert pages, 'No atlas pages found'
for path in pages:
    zh=path.name.endswith('.zh.html');page=Page();page.feed(path.read_text())
    home=[x for x in page.links if 'atlas-home-link' in x['attrs'].get('class','').split()]
    assert len(home)==1, (path.name,'Expected one explicit personal-home link')
    link=home[0]
    assert link['nav']=='atlas-langbar', (path.name,'Home link must be in the top navigation')
    assert link['attrs']['href']==('https://shundazhang.github.io/index.zh.html' if zh else 'https://shundazhang.github.io/')
    assert link['text']==('返回个人主页' if zh else 'Personal home')
    assert 'home-navigation.css' in page.styles
    assert (ROOT/'home-navigation.css').is_file()
    languages=[x['attrs'].get('data-atlas-lang') for x in page.links if x['attrs'].get('data-atlas-lang')]
    assert sorted(languages)==['en','zh'], (path.name,'Language selection must be preserved')
print(f'PASS · {len(pages)} pages · direct personal-home links, localized destinations, top placement, styles and language switches')
