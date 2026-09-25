"""Verify that the bundled brand assets are unmodified.

The brand assets are immutable by policy. This makes that true by mechanism:
every file under ``assets/logos/`` is pinned by SHA-256 in
``assets/logo-checksums.json``, and any modification, addition or deletion
fails.

Editing a brand asset is never a legitimate way to change it. The only
sanctioned path is a **re-sync**: the brand owner issues a new official
delivery, and the bundle is replaced wholesale from it, with the checksum
record regenerated in the same change. Regenerating the record is the recorded
act of accepting that delivery, which is why it is an explicit flag rather
than the default.

Read-only by default. Exits non-zero on any failure.

Usage:
    python3 scripts/validate_asset_integrity.py
    python3 scripts/validate_asset_integrity.py --write
"""

from __future__ import annotations

import hashlib
import json
import posixpath
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets' / 'logos'
RECORD = ROOT / 'assets' / 'logo-checksums.json'

failures: list[str] = []


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def current_files() -> dict[str, str]:
    if not ASSETS.is_dir():
        return {}
    return {
        posixpath.join(p.parent.relative_to(ASSETS).as_posix(), p.name): digest(p)
        for p in sorted(ASSETS.rglob('*'))
        if p.is_file()
    }


def write_record(files: dict[str, str]) -> None:
    RECORD.write_text(
        json.dumps(
            {
                'algorithm': 'sha256',
                'record': 'Pins every bundled brand asset. Brand assets are immutable: do not edit them. A changed, added or missing file fails CI. Regenerate only as part of an approved re-sync from a new official delivery.',
                'files': dict(sorted(files.items())),
            },
            ensure_ascii=False,
            indent=2,
        )
        + '\n',
        encoding='utf-8',
    )
    print(f'WROTE {RECORD.relative_to(ROOT)} with {len(files)} asset hash(es)')


def main(argv: list[str]) -> int:
    files = current_files()

    if '--write' in argv:
        if not files:
            print(f'FAIL no assets found under {ASSETS.relative_to(ROOT)}')
            return 1
        write_record(files)
        return 0

    if not RECORD.is_file():
        print(f'FAIL missing checksum record: {RECORD.relative_to(ROOT)}')
        print('     create it with: python3 scripts/validate_asset_integrity.py --write')
        return 1

    recorded = json.loads(RECORD.read_text(encoding='utf-8')).get('files', {})

    for name in sorted(set(recorded) - set(files)):
        failures.append(f'brand asset is missing (was pinned): assets/logos/{name}')
    for name in sorted(set(files) - set(recorded)):
        failures.append(
            f'unpinned brand asset added: assets/logos/{name} '
            f'(assets are immutable; a new delivery needs an approved re-sync)'
        )
    for name in sorted(set(files) & set(recorded)):
        if files[name] != recorded[name]:
            failures.append(
                f'brand asset was modified: assets/logos/{name}\n'
                f'         pinned {recorded[name]}\n'
                f'         actual {files[name]}'
            )

    if failures:
        for f in failures:
            print(f'FAIL {f}')
        print('\nBrand assets are immutable. To accept a new official delivery, get brand-owner')
        print('approval, re-sync the bundle, then regenerate the record with --write in the same change.')
        return 1

    print(f'PASS {len(files)} brand asset(s) match the pinned SHA-256 record — unmodified')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
