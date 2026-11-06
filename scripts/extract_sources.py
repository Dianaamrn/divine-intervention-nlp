"""Extract the local research PDFs; preserve one-based PDF page locators."""
import json
import sys
import logging
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding='utf-8')
logging.getLogger('pypdf').setLevel(logging.ERROR)
CACHE = ROOT / 'research' / 'source_text'
CACHE.mkdir(parents=True, exist_ok=True)
SOURCES = [
    ('burkert_1985', 'Greek Religion', 'Walter Burkert', 1985),
    ('sissa_detienne_2000', 'The Daily Life of the Greek Gods', 'Giulia Sissa and Marcel Detienne', 2000),
    ('bremmer_erskine_2010', 'The Gods of Ancient Greece', 'Jan N. Bremmer and Andrew Erskine (editors)', 2010),
]
registry = []
for source_id, title, author, year in SOURCES:
    matches = list((ROOT / 'sources').glob(title + '*.pdf'))
    if len(matches) != 1:
        raise ValueError(f'Expected one PDF for {title}, found {len(matches)}')
    path = matches[0]
    cache_path = CACHE / f'{source_id}.json'
    if cache_path.exists():
        pages = json.loads(cache_path.read_text(encoding='utf-8'))
    else:
        reader = PdfReader(path)
        pages = [{'pdf_page': i + 1, 'text': page.extract_text() or ''} for i, page in enumerate(reader.pages)]
        cache_path.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
    registry.append({'id': source_id, 'title': title, 'author_or_editors': author,
                     'bibliographic_year_from_draft': year, 'path': path.relative_to(ROOT).as_posix(),
                     'pdf_pages': len(pages), 'locator_note': 'pdf_page is one-based; printed pages must be checked separately.'})
    print(source_id, len(pages), 'pages;', sum(bool(p['text'].strip()) for p in pages), 'with extractable text')
    for p in pages[:12]:
        if any(k in p['text'].lower() for k in ['contents', 'copyright', 'first published']):
            print('PDF PAGE', p['pdf_page'], p['text'][:6500])
(ROOT / 'research' / 'sources.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
