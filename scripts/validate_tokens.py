"""Validate the ArcheBase semantic token and Guide-evidence records.

Enforces the contract documented in ``references/architecture.md``: reject
colors outside the approved token set unless explicitly declared as
``待确认``, reject malformed hex values, and keep the explicit numeric
relationships from Guide pp.28 and pp.30-32 synchronized with the token file.

The approved set and numeric expectations are independently duplicated here
from ``references/guide-page-evidence.md`` and ``assets/guide-evidence.json``
so that the token file cannot silently become its own authority.

Read-only and deterministic. Exits non-zero on any failure.

Usage:
    python3 scripts/validate_tokens.py [tokens/archebase.tokens.json]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / 'tokens' / 'archebase.tokens.json'
EVIDENCE = ROOT / 'assets' / 'guide-evidence.json'

# Approved by the Guide. See references/guide-page-evidence.md (p.29, pp.30-32).
APPROVED = {
    'AB_BLUE_1': '#0032FF',
    'AB_BLUE_2': '#7172FA',
    'AB_BLUE_3': '#619AFD',
    'AB_BLUE_4': '#46CFFF',
    'AB_CHARCOAL': '#1E2124',
}
RATIO = {
    'AB_BLUE_1': 50,
    'AB_BLUE_2': 25,
    'AB_BLUE_3': 10,
    'AB_BLUE_4': 5,
}
HEX = re.compile(r'^#[0-9A-Fa-f]{6}$')
STALE_UNCONFIRMED = {
    'p28_ratio_roles',
    'exact neutral mappings',
}
REQUIRED_UNCONFIRMED = {
    'p28_semantic_role_names_and_per_component_allocation',
    'neutral_compositing_and_component_role_mapping',
}


def main(argv: list[str]) -> int:
    path = Path(argv[0]) if argv else DEFAULT
    if not path.is_file():
        print(f'FAIL no such token file: {path}')
        return 2

    data = json.loads(path.read_text(encoding='utf-8'))
    colors = data.get('colors')
    if not isinstance(colors, dict) or not colors:
        print('FAIL token file has no "colors" map')
        return 1

    failures: list[str] = []
    unconfirmed = set(data.get('unconfirmed') or [])

    for name, value in colors.items():
        if not isinstance(value, str) or not HEX.match(value):
            failures.append(f'malformed hex for {name}: {value!r}')
            continue
        approved = APPROVED.get(name)
        if approved is None:
            if name not in unconfirmed:
                failures.append(
                    f'unapproved color token {name}={value}; add it to the approved '
                    f'Guide set or declare it in "unconfirmed" as 待确认'
                )
        elif value.upper() != approved:
            failures.append(
                f'{name} is {value}, but the Guide documents {approved}; '
                f'do not change an approved value without an owner decision'
            )

    for name, value in APPROVED.items():
        if name not in colors:
            failures.append(f'approved token missing from the token file: {name} ({value})')

    ratio = data.get('color_ratio') or {}
    mapping = ratio.get('mapping_percent') if isinstance(ratio, dict) else None
    if mapping != RATIO:
        failures.append(f'color_ratio.mapping_percent must be {RATIO}, got {mapping!r}')
    if not isinstance(ratio, dict) or ratio.get('source_page') != 28:
        failures.append('color_ratio.source_page must be 28')
    if not isinstance(ratio, dict) or ratio.get('labeled_percent_total') != 90:
        failures.append('color_ratio.labeled_percent_total must be 90')
    if not isinstance(ratio, dict) or ratio.get('unmapped_percent') != 10:
        failures.append('color_ratio.unmapped_percent must be 10')

    neutral = data.get('neutral_levels') or {}
    if neutral.get('source_pages') != [30, 31, 32]:
        failures.append('neutral_levels.source_pages must be [30, 31, 32]')
    if neutral.get('background_percent') != [100, 5]:
        failures.append('neutral_levels.background_percent must be [100, 5]')
    if neutral.get('text_percent') != [100, 70, 50]:
        failures.append('neutral_levels.text_percent must be [100, 70, 50]')

    if STALE_UNCONFIRMED & unconfirmed:
        failures.append(f'stale unconfirmed entries remain: {sorted(STALE_UNCONFIRMED & unconfirmed)}')
    if not REQUIRED_UNCONFIRMED <= unconfirmed:
        failures.append(
            f'missing remaining evidence-boundary entries: {sorted(REQUIRED_UNCONFIRMED - unconfirmed)}'
        )

    if not EVIDENCE.is_file():
        failures.append(f'missing evidence register: {EVIDENCE.relative_to(ROOT)}')
    else:
        evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))
        evidence_ratio = next(
            (item for item in evidence.get('evidence', []) if item.get('id') == 'color.ratio'),
            None,
        )
        if evidence_ratio is None:
            failures.append('evidence register is missing color.ratio')
        else:
            evidence_map = {
                item.get('token'): item.get('percent')
                for item in evidence_ratio.get('mapping', [])
            }
            if evidence_map != RATIO:
                failures.append(f'evidence color ratio must be {RATIO}, got {evidence_map!r}')

    if failures:
        for failure in failures:
            print(f'FAIL {failure}')
        return 1

    print(
        f'PASS semantic tokens: {len(colors)} colors, '
        f'Guide ratio 50/25/10/5, neutral levels 100/70/50 and background 100/5 verified, '
        f'{len(unconfirmed)} open 待确认 item(s)'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
