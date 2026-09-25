#!/usr/bin/env bash
# Render an ArcheBase logo SVG to PNG and verify it against the bundled raster.
#
# The gradient logo SVGs use multiple stops with stop-opacity. ImageMagick's
# internal SVG renderer mangles them, so this script requires rsvg-convert and
# refuses to fall back to `magick file.svg`.
#
# Usage:
#   scripts/render_logo.sh <name-without-extension> [width] [output.png]
#   scripts/render_logo.sh --verify-all
#
# Example:
#   scripts/render_logo.sh 白色渐变_英文_横版_组合标 1524 /tmp/logo.png

set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
svg_dir="$here/assets/logos/svg"
png_dir="$here/assets/logos/png"

command -v rsvg-convert >/dev/null 2>&1 || {
  echo "FAIL rsvg-convert not found. Install librsvg (brew install librsvg)." >&2
  echo "Do NOT substitute 'magick file.svg' - it renders these logos incorrectly." >&2
  exit 1
}

rmse() { # $1 rendered, $2 reference
  magick compare -metric RMSE "$1" "$2" null: 2>&1 || true
}

if [ "${1:-}" = "--verify-all" ]; then
  fail=0
  count=0
  for svg in "$svg_dir"/*.svg; do
    name="$(basename "$svg" .svg)"
    ref="$png_dir/$name.png"
    [ -f "$ref" ] || { echo "SKIP $name (no bundled PNG)"; continue; }
    out="$(mktemp -t archebase_logo_XXXX).png"
    # Render at the bundled PNG's native size so the comparison is meaningful.
    size="$(magick identify -format '%wx%h' "$ref")"
    rsvg-convert -w "${size%x*}" -h "${size#*x}" "$svg" -o "$out"
    result="$(rmse "$out" "$ref")"
    case "$result" in
      0*|"0 (0)") count=$((count + 1)) ;;
      *) echo "MISMATCH $name -> RMSE $result"; fail=1 ;;
    esac
    rm -f "$out"
  done
  [ "$fail" -eq 0 ] || exit 1
  echo "PASS $count SVG renders match the bundled PNG bit-for-bit"
  exit 0
fi

name="${1:?usage: render_logo.sh <name-without-extension> [width] [output.png]}"
width="${2:-}"
out="${3:-${name}.png}"
svg="$svg_dir/$name.svg"
ref="$png_dir/$name.png"

[ -f "$svg" ] || { echo "FAIL no such SVG: $svg" >&2; exit 1; }

if [ -n "$width" ]; then
  rsvg-convert -w "$width" "$svg" -o "$out"
else
  rsvg-convert "$svg" -o "$out"
fi
echo "rendered $out"

if [ -f "$ref" ]; then
  result="$(rmse "$out" "$ref")"
  case "$result" in
    0*|"0 (0)") echo "verified against bundled PNG: RMSE 0" ;;
    *) echo "NOTE differs from bundled PNG (RMSE $result) - expected if you requested a different width" ;;
  esac
fi
