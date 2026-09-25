"""Validate the bundled ArcheBase logo asset package.

Checks the SVG source set, the raster delivery set, filename agreement between
them, and that no zero-byte asset slipped in.

Usage:
    python3 scripts/validate_logo_bundle.py [assets/logos]
"""

from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'assets/logos')
failures = []

svg_dir = root / 'svg'
png_dir = root / 'png'


def check_dir(path: Path, label: str, minimum: int) -> list[Path]:
    if not path.is_dir():
        failures.append(f'missing directory: {path}')
        return []
    files = sorted(p for p in path.iterdir() if p.is_file())
    if not files:
        failures.append(f'no {label} assets in {path}')
        return []
    if len(files) < minimum:
        failures.append(f'expected at least {minimum} {label} assets, found {len(files)}')
    for p in files:
        if p.stat().st_size == 0:
            failures.append(f'empty asset: {p}')
    return files


svgs = check_dir(svg_dir, 'SVG', 5)
pngs = check_dir(png_dir, 'PNG', 5)

for p in svgs:
    if not p.read_text(encoding='utf-8', errors='ignore').lstrip().startswith('<'):
        failures.append(f'not an SVG document: {p}')

svg_stems = {p.stem for p in svgs}
png_stems = {p.stem for p in pngs}

for stem in sorted(svg_stems - png_stems):
    failures.append(f'SVG without matching PNG raster delivery: {stem}.svg')
for stem in sorted(png_stems - svg_stems):
    failures.append(f'PNG without matching SVG source: {stem}.png')

# Optional: flag raster delivered by ImageMagick's known-bad SVG renderer.
for p in pngs:
    try:
        from PIL import Image
    except ImportError:
        break
    with Image.open(p) as im:
        if im.mode not in ('RGBA', 'LA', 'P'):
            failures.append(f'PNG lacks usable alpha channel: {p.name} (mode {im.mode})')
        if im.getchannel('A').getextrema() == (255, 255):
            failures.append(f'PNG has fully opaque alpha; check renderer: {p.name}')

if failures:
    for f in failures:
        print(f'FAIL {f}')
    raise SystemExit(1)

print(f'PASS {len(svgs)} SVG source assets, {len(pngs)} matching PNG raster assets')
print('NOTE rasterize SVGs with rsvg-convert (librsvg), never ImageMagick\'s internal SVG renderer.')
