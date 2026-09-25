"""Validate the ArcheBase semantic token file.

Enforces the contract documented in ``references/architecture.md``: reject
colors outside the approved token set unless they are explicitly declared as
``待确认``, and reject malformed hex values.

The approved set is the independent expectation taken from the Guide evidence
(``references/guide-page-evidence.md``): four blues from p.29 and the neutral
from pp.30-32. It is intentionally duplicated here so that the token file
cannot silently become its own authority.

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

# Approved by the Guide. See references/guide-page-evidence.md (p.29, pp.30-32).
APPROVED = {
    'AB_BLUE_1': '#0032FF',
    'AB_BLUE_2': '#7172FA',
    'AB_BLUE_3': '#619AFD',
    'AB_BLUE_4': '#46CFFF',
    'AB_CHARCOAL': '#1E2124',
}

HEX = re.compile(r'^#[0-9A-Fa-f]{6}$')

failures: list[str] = []


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

    unconfirmed = data.get('unconfirmed') or []

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

    if failures:
        for f in failures:
            print(f'FAIL {f}')
        return 1

    print(
        f'PASS semantic tokens: {len(colors)} colors, '
        f'{len(APPROVED)} matching the approved Guide set, '
        f'{len(unconfirmed)} open 待确认 item(s)'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
