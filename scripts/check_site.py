#!/usr/bin/env python3
"""Check generated local assets, page links and fragment targets, including subpath builds."""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

root = Path(sys.argv[1] if len(sys.argv)>1 else 'public').resolve()
prefix = sys.argv[2].rstrip('/') if len(sys.argv)>2 else ''
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.path=path; self.refs=[]; self.ids=set(); self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if d.get('id'): self.ids.add(d['id'])
        for attr in ('href','src'):
            if d.get(attr): self.refs.append(d[attr])

pages={p:Page(p) for p in root.rglob('*.html')}
errors=[]
for file,page in pages.items():
    for ref in page.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc: continue
        path=unquote(u.path)
        if path.startswith('/'):
            if prefix and not (path==prefix or path.startswith(prefix+'/')):
                errors.append(f'{file.relative_to(root)}: missing base path in {ref}');continue
            target=root/path.removeprefix(prefix).lstrip('/')
        else: target=file.parent/path if path else file
        if target.is_dir(): target=target/'index.html'
        if not target.exists(): errors.append(f'{file.relative_to(root)}: missing {ref}');continue
        if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f'{file.relative_to(root)}: missing fragment {ref}')
if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'OK: {len(pages)} HTML pages; all local links, assets and fragments exist (base path: {prefix or "/"}).')
