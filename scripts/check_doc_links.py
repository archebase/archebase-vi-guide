"""Check that file paths referenced in the skill's markdown actually exist.

Guards against the regression where `references/README.md` listed playbooks that
were never written, and where `references/architecture.md` documented a script
that did not exist.

Also asserts that every file in `references/` is reachable from
`references/README.md`, so a new reference cannot be added silently.

Read-only and deterministic. Exits non-zero on any failure.

Usage:
    python3 scripts/check_doc_links.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Backticked paths carrying an explicit directory prefix.
PREFIXED = re.compile(
    r'`((?:references|checklists|templates|scripts|tokens|assets|\.github)/[^`\s]+?\.'
    r'(?:md|py|sh|json|yml|svg|png))`'
)

# Backticked bare filenames such as `guide-page-evidence.md`.
BARE = re.compile(r'`([A-Za-z0-9._\u4e00-\u9fff-]+\.(?:md|py|sh|json|yml))`')

BACKTICK = re.compile(r'`([^`]+)`')

SKIP_DIRS = {'.git', '.github', 'node_modules', '__pycache__'}

# Files referenced by name that live at the repository root.
ROOT_DOCS = {'README.md', 'SKILL.md', 'NOTICE.md', 'LICENSE', 'EXPORT-METADATA.json'}

failures: list[str] = []


def markdown_files() -> list[Path]:
    return sorted(
        p for p in ROOT.rglob('*.md') if not any(part in SKIP_DIRS for part in p.parts)
    )


def resolves(doc: Path, ref: str) -> bool:
    if '*' in ref:
        return True  # glob example such as `checklists/*.md`
    return (ROOT / ref).is_file() or (doc.parent / ref).is_file()


def check_links() -> int:
    checked = 0
    for doc in markdown_files():
        text = doc.read_text(encoding='utf-8', errors='ignore')
        refs = set(PREFIXED.findall(text)) | set(BARE.findall(text))
        for ref in sorted(refs):
            if ref in ROOT_DOCS:
                continue
            checked += 1
            if not resolves(doc, ref):
                failures.append(f'{doc.relative_to(ROOT)} references a missing file: {ref}')
    return checked


def check_reference_index() -> None:
    ref_dir = ROOT / 'references'
    index = ref_dir / 'README.md'
    if not index.is_file():
        failures.append('references/README.md is missing')
        return

    tokens = {t.strip() for t in BACKTICK.findall(index.read_text(encoding='utf-8'))}
    names = {Path(t).name for t in tokens}

    for f in sorted(ref_dir.glob('*.md')):
        if f.name == 'README.md':
            continue
        if f.name not in names:
            failures.append(
                f'references/{f.name} exists but is not listed in references/README.md'
            )


def main() -> int:
    checked = check_links()
    check_reference_index()

    if failures:
        for f in failures:
            print(f'FAIL {f}')
        return 1

    print(f'PASS doc links: {checked} referenced path(s) resolve, references/ index complete')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
