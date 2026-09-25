"""Validate the compact evidence register for the official VI Guide.

The official 46-page PDF is intentionally not bundled. This validator checks
that the shipped evidence register is internally complete and that its numeric
claims cannot drift from the approved token set. With ``--pdf`` it additionally
checks the page count and SHA-256 of a local source PDF using PyMuPDF.

Usage:
    python3 scripts/validate_guide_evidence.py
    python3 scripts/validate_guide_evidence.py --pdf /path/to/智域基石vi基础.pdf
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / 'assets' / 'guide-evidence.json'
TOKENS = ROOT / 'tokens' / 'archebase.tokens.json'
HEX = re.compile(r'^#[0-9A-Fa-f]{6}$')


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf', type=Path, help='optional local official PDF to verify')
    args = parser.parse_args(argv)
    failures: list[str] = []

    if not EVIDENCE.is_file():
        print(f'FAIL missing evidence register: {EVIDENCE.relative_to(ROOT)}')
        return 1
    data = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    source = data.get('source', {})
    if source.get('pages') != 46:
        fail(f'source.pages must be 46, got {source.get("pages")!r}', failures)
    if source.get('local_verified_path') is not None:
        fail('source.local_verified_path must remain null for portability', failures)
    if not source.get('display_name') or not source.get('source_filename'):
        fail('source.display_name and source.source_filename are required', failures)
    if not isinstance(source.get('sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', source['sha256']):
        fail('source.sha256 must be a 64-character lowercase SHA-256 digest', failures)

    token_data = json.loads(TOKENS.read_text(encoding='utf-8'))
    colors = token_data.get('colors', {})
    evidence = data.get('evidence', [])
    ids = [item.get('id') for item in evidence]
    if len(ids) != len(set(ids)):
        fail('evidence ids must be unique', failures)
    for item in evidence:
        pages = item.get('pages', [])
        if not pages or any(not isinstance(p, int) or p < 1 or p > 46 for p in pages):
            fail(f'invalid pages for evidence {item.get("id")!r}', failures)
        if not item.get('status') or not item.get('do_not_infer'):
            fail(f'evidence {item.get("id")!r} needs status and do_not_infer', failures)

    ratio = next((item for item in evidence if item.get('id') == 'color.ratio'), None)
    if ratio is None:
        fail('missing color.ratio evidence', failures)
    else:
        mapping = ratio.get('mapping', [])
        expected = {
            'AB_BLUE_1': ('#0032FF', 50),
            'AB_BLUE_2': ('#7172FA', 25),
            'AB_BLUE_3': ('#619AFD', 10),
            'AB_BLUE_4': ('#46CFFF', 5),
        }
        if sum(item.get('percent', 0) for item in mapping) != 90:
            fail('color.ratio labeled mapping must sum to 90; the remaining 10 is intentionally unassigned', failures)
        if ratio.get('labeled_percent_total') != 90 or ratio.get('unmapped_percent') != 10:
            fail('color.ratio must record labeled_percent_total=90 and unmapped_percent=10', failures)
        if not ratio.get('unmapped_role'):
            fail('color.ratio must explain that the remaining 10% is not assigned by the Guide', failures)
        for token, (hex_value, percent) in expected.items():
            found = next((item for item in mapping if item.get('token') == token), None)
            if found is None:
                fail(f'color.ratio missing {token}', failures)
            else:
                if found.get('hex') != hex_value or found.get('percent') != percent:
                    fail(f'color.ratio mismatch for {token}: {found}', failures)
                if colors.get(token) != hex_value:
                    fail(f'color.ratio {token} disagrees with tokens: {colors.get(token)!r}', failures)

    neutral_background = next((item for item in evidence if item.get('id') == 'neutral.background'), None)
    neutral_text = next((item for item in evidence if item.get('id') == 'neutral.text'), None)
    if neutral_background is None or neutral_background.get('background_levels_percent') != [100, 5]:
        fail('neutral.background must record [100, 5] percent levels', failures)
    if neutral_text is None or neutral_text.get('text_levels_percent') != [100, 70, 50]:
        fail('neutral.text must record [100, 70, 50] percent levels', failures)
    if colors.get('AB_CHARCOAL') != '#1E2124':
        fail('AB_CHARCOAL must remain #1E2124', failures)

    if args.pdf:
        if not args.pdf.is_file():
            fail(f'PDF does not exist: {args.pdf}', failures)
        else:
            try:
                import fitz  # type: ignore
                doc = fitz.open(args.pdf)
                if doc.page_count != source['pages']:
                    fail(f'PDF page count {doc.page_count} != {source["pages"]}', failures)
                actual_hash = sha256(args.pdf)
                if actual_hash != source['sha256']:
                    fail(f'PDF SHA-256 {actual_hash} != evidence register {source["sha256"]}', failures)
            except ImportError:
                fail('PyMuPDF (fitz) is required when --pdf is supplied', failures)

    if failures:
        for item in failures:
            print(f'FAIL {item}')
        return 1
    print(f'PASS Guide evidence: {len(evidence)} evidence records; source pages=46')
    if args.pdf:
        print(f'PASS PDF source: {args.pdf} matches page count and SHA-256')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
