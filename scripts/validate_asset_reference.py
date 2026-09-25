"""Validate ArcheBase asset references.

Two modes:

1. Bundle integrity (default) — compares ``assets/logo-manifest.json`` against
   the files actually present, and checks that every SVG source has a matching
   PNG raster delivery.

2. Record scan (``--records``) — checks a deliverable record (a decision record,
   brief or release report) for logo references that are missing from the
   bundle, that point at a legacy ``old_*`` asset, or that describe recreating
   the mark instead of placing the supplied file.

Read-only and deterministic. Exits non-zero on any failure.

Usage:
    python3 scripts/validate_asset_reference.py
    python3 scripts/validate_asset_reference.py --records path/to/record.md ...
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'assets' / 'logo-manifest.json'

# Manifest inventory key -> directory under assets/logos/
INVENTORY_DIRS = {
    'svg': 'svg',
    'png': 'png',
    'png_hires': 'png-hires',
}

ASSET_REF = re.compile(r'assets/logos/[^\s`\'"()\[\],;]+\.(?:svg|png|jpg|jpeg|ai)', re.I)

# Wording that describes recreating the mark rather than placing the supplied file.
RECREATION = re.compile(
    r'\b(redraw|re-draw|retrace|re-trace|trace|recolor|recolour|recreate|re-create|'
    r'regenerate|re-generate|rebuild the logo|stretch|skew|distort|recolour)\b',
    re.I,
)

# Lines that prohibit an action are rules, not violations.
PROHIBITION = re.compile(r'\b(never|do not|don\'t|must not|may not|no)\b', re.I)

LEGACY = re.compile(r'\bold[_-]', re.I)

failures: list[str] = []


def check_bundle() -> None:
    if not MANIFEST.is_file():
        failures.append(f'missing manifest: {MANIFEST.relative_to(ROOT)}')
        return

    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    inventory = manifest.get('inventory', {})
    logo_root = ROOT / 'assets' / 'logos'

    for key, dirname in INVENTORY_DIRS.items():
        path = logo_root / dirname
        if not path.is_dir():
            failures.append(f'missing asset directory: assets/logos/{dirname}')
            continue
        actual = sorted(p for p in path.iterdir() if p.is_file())
        expected = inventory.get(key)
        if expected is None:
            failures.append(f'manifest inventory is missing key: {key}')
        elif expected != len(actual):
            failures.append(
                f'inventory mismatch for {key}: manifest says {expected}, '
                f'assets/logos/{dirname} contains {len(actual)}'
            )
        for p in actual:
            if p.stat().st_size == 0:
                failures.append(f'empty asset: {p.relative_to(ROOT)}')

    svg_dir = logo_root / 'svg'
    png_dir = logo_root / 'png'
    if svg_dir.is_dir() and png_dir.is_dir():
        svg_stems = {p.stem for p in svg_dir.iterdir() if p.is_file()}
        png_stems = {p.stem for p in png_dir.iterdir() if p.is_file()}
        for stem in sorted(svg_stems - png_stems):
            failures.append(f'SVG without matching PNG raster delivery: {stem}.svg')
        for stem in sorted(png_stems - svg_stems):
            failures.append(f'PNG without matching SVG source: {stem}.png')

        pairs = manifest.get('verified', {}).get('svg_vs_png_pairs')
        if pairs is not None and pairs != len(svg_stems):
            failures.append(
                f'verified.svg_vs_png_pairs says {pairs}, '
                f'but the bundle holds {len(svg_stems)} SVG sources'
            )

    if not failures:
        print(
            f'PASS bundle integrity: {inventory.get("svg")} SVG, '
            f'{inventory.get("png")} PNG, {inventory.get("png_hires")} png-hires'
        )


def check_record(path: Path) -> None:
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except OSError as exc:
        failures.append(f'cannot read record {path}: {exc}')
        return

    before = len(failures)
    seen = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        for ref in ASSET_REF.findall(line):
            seen += 1
            target = ROOT / ref
            if not target.is_file():
                failures.append(f'{path}:{lineno} dangling asset reference: {ref}')
            if LEGACY.search(Path(ref).name):
                failures.append(
                    f'{path}:{lineno} references a legacy asset: {ref} '
                    f'(use a current asset or record the owner exception)'
                )
        if RECREATION.search(line) and not PROHIBITION.search(line):
            failures.append(
                f'{path}:{lineno} describes recreating the mark rather than '
                f'placing the supplied file: {line.strip()[:120]}'
            )

    status = 'FAIL' if len(failures) > before else 'OK'
    print(f'{status} {path}: {seen} logo reference(s) scanned')


def main(argv: list[str]) -> int:
    if '--records' in argv:
        idx = argv.index('--records')
        targets = argv[idx + 1:]
        if not targets:
            print('FAIL --records requires at least one file or directory')
            return 2
        files: list[Path] = []
        for t in targets:
            p = Path(t)
            if p.is_dir():
                files.extend(sorted(q for q in p.rglob('*.md') if q.is_file()))
            elif p.is_file():
                files.append(p)
            else:
                failures.append(f'no such record: {t}')
        for f in files:
            if 'references' in f.parts or 'checklists' in f.parts:
                continue  # rules documents, not deliverable records
            check_record(f)
    else:
        check_bundle()

    if failures:
        for f in failures:
            print(f'FAIL {f}')
        return 1

    print('PASS asset references')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
