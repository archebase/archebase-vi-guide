"""Validate all 46 page-level records for the official VI Guide."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'references' / 'guide-pages'
INDEX = ROOT / 'assets' / 'guide-page-index.json'
EXPECTED_SHA = '80680405ee05512878f5ecadc50cf32975d5a5d18c81b1ea17bcc8ad681493cb'
FRONTMATTER = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)


def parse_frontmatter(path: Path) -> dict[str, str]:
    match = FRONTMATTER.match(path.read_text(encoding='utf-8'))
    if not match:
        raise ValueError('missing YAML frontmatter')
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        cleaned = value.strip()
        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
            cleaned = cleaned[1:-1]
        data[key.strip()] = cleaned
    return data


def main() -> int:
    failures: list[str] = []
    files = sorted(PAGES.glob('page-*.md')) if PAGES.is_dir() else []
    if len(files) != 46:
        failures.append(f'expected 46 page records, found {len(files)}')

    seen: set[int] = set()
    for path in files:
        match = re.fullmatch(r'page-(\d{3})\.md', path.name)
        if not match:
            failures.append(f'invalid page filename: {path.name}')
            continue
        page = int(match.group(1))
        if page in seen:
            failures.append(f'duplicate page record: {page}')
        seen.add(page)
        try:
            fm = parse_frontmatter(path)
        except Exception as exc:
            failures.append(f'{path.name}: {exc}')
            continue
        if fm.get('page') != str(page):
            failures.append(f'{path.name}: frontmatter page={fm.get("page")!r}')
        if fm.get('source_sha256') != EXPECTED_SHA:
            failures.append(f'{path.name}: source_sha256 does not match official Guide')
        for key in ('title', 'group', 'source', 'evidence_type', 'confidence', 'modes', 'routes', 'human_review_required'):
            if key not in fm:
                failures.append(f'{path.name}: missing frontmatter field {key}')
        body = path.read_text(encoding='utf-8')
        for heading in ('## Visible elements', '## Rule extracted', '## Applies to', '## Do not infer', '## Review'):
            if heading not in body:
                failures.append(f'{path.name}: missing section {heading}')
        if fm.get('evidence_type') == 'visual_board_only' and fm.get('human_review_required') != 'true':
            failures.append(f'{path.name}: visual_board_only must require human review')
        if fm.get('evidence_type') in {'visual_inference', 'visual_board_only'} and fm.get('confidence') == 'high':
            failures.append(f'{path.name}: visual inference cannot be high confidence without explicit evidence')

    expected = set(range(1, 47))
    if seen != expected:
        failures.append(f'page coverage mismatch: missing={sorted(expected-seen)} extra={sorted(seen-expected)}')

    if INDEX.is_file():
        index = json.loads(INDEX.read_text(encoding='utf-8'))
        if index.get('pages') != 46:
            failures.append('guide-page-index.json pages must be 46')
        if index.get('page_records') != 'references/guide-pages/page-{page:03d}.md':
            failures.append('guide-page-index.json page_records pointer is missing or wrong')
    else:
        failures.append('missing guide-page-index.json')

    if failures:
        for failure in failures:
            print(f'FAIL {failure}')
        return 1
    print('PASS 46 page records: complete coverage, source hash, evidence boundaries and mode/route metadata')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
