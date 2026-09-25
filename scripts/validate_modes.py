"""Validate the opt-in mode contract for the ArcheBase VI skill."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODES = ROOT / 'references' / 'modes.md'
BRIEF = ROOT / 'templates' / 'brief.md'
DECISION = ROOT / 'templates' / 'decision-record.md'
REPORT = ROOT / 'templates' / 'release-report.md'
GATES = ROOT / 'references' / 'release-gates.md'

REQUIRED_MODES = ('strict', 'guided', 'creative', 'off')
REQUIRED_HARD_BOUNDARIES = (
    'Logo',
    'rights',
    'claims',
    'Human approval',
)


def main() -> int:
    failures: list[str] = []
    text = MODES.read_text(encoding='utf-8')
    for mode in REQUIRED_MODES:
        if f'| `{mode}` |' not in text:
            failures.append(f'modes.md missing mode table row: {mode}')
    if 'not a mandatory visual police layer' not in text:
        failures.append('modes.md must explicitly define the skill as opt-in')
    if 'creative' not in text or 'platform-native' not in text:
        failures.append('modes.md must preserve platform-native creative latitude')
    for phrase in REQUIRED_HARD_BOUNDARIES:
        if phrase not in text:
            failures.append(f'modes.md missing hard-boundary concept: {phrase}')
    for path in (BRIEF, DECISION, REPORT):
        content = path.read_text(encoding='utf-8')
        if 'Mode:' not in content:
            failures.append(f'{path.relative_to(ROOT)} missing Mode field')
    gate_text = GATES.read_text(encoding='utf-8')
    for mode in REQUIRED_MODES:
        if f'`{mode}`' not in gate_text:
            failures.append(f'release-gates.md missing mode behavior: {mode}')
    if failures:
        for failure in failures:
            print(f'FAIL {failure}')
        return 1
    print('PASS opt-in modes: strict/guided/creative/off, hard boundaries, templates and mode-aware gates')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
