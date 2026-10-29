"""Validate generated pages, local links and image sources."""
from pathlib import Path
from html.parser import HTMLParser
import json, os

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
BASE_PATH='/' + os.environ.get('BASE_PATH','').strip('/') if os.environ.get('BASE_PATH','').strip('/') else ''


class PageCheck(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.lang, self.headings = path, None, 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'html':
            self.lang = d.get('lang')
        if tag == 'h1':
            self.headings += 1
        for key in ('src', 'href'):
            value = d.get(key, '').split('#')[0].split('?')[0]
            if BASE_PATH and value.startswith(BASE_PATH + '/'):
                value=value[len(BASE_PATH):]
            if value.startswith('/') and not value.startswith('//'):
                assert (DIST / value.lstrip('/')).exists(), f'{self.path}: missing {value}'


pages = list(DIST.glob('*/*.html'))
assert len(pages) == 18, f'Expected 18 pages, found {len(pages)}'
for page in pages:
    check = PageCheck(page)
    check.feed(page.read_text(encoding='utf-8'))
    assert check.lang == page.parent.name, f'Incorrect language: {page}'
    assert check.headings == 1, f'Expected one h1: {page}'
for photo in json.loads((ROOT / 'content/photos.json').read_text(encoding='utf-8')):
    assert (ROOT / photo['file']).is_file(), photo['file']
    assert (DIST / 'assets' / (photo['id'] + '.webp')).is_file(), photo['id']
print(f'Passed: {len(pages)} bilingual pages, local links and image sources/output.')
