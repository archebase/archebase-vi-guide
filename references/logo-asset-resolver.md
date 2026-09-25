# Logo asset resolver

Source folder: `https://archebase.feishu.cn/drive/folder/MBewfd14ll34N0dJINNcQnQqn4c`
Current delivery: `智域基石 Logo V2` (synced 2026-09-22). See `assets/logo-manifest.json` for inventory, naming pattern and verification record.

## Bundled asset directories

| Directory | Use for |
|---|---|
| `assets/logos/svg/` | Source of truth for geometry and color |
| `assets/logos/png/` | Raster delivery for web, social, office and deck export |
| `assets/logos/png-hires/` | App icon, avatar, favicon and large-format icon use |

Each SVG has a matching PNG at the same native size in `assets/logos/png/`. All 24 pairs verified at RMSE 0 on 2026-09-22.

## Resolution procedure

1. Use the bundled `assets/logos/` directories first. Read-only list the Feishu folder only when the needed variant is missing or a newer export must be confirmed.
2. Prefer current `svg` for the source; use the bundled `png` for raster output and `jpg` only for preview/reference.
3. Treat `old_png` and `old_ai` as legacy until owner confirms otherwise.
4. Resolve by background (light/dark/image/mono), lockup (graphic/wordmark/combination), language (Chinese/English/bilingual), and orientation (horizontal/vertical/square).
5. Record filename, extension, source directory, remote token/reference, modified time, and legacy status in the decision record and manifest.
6. Insert the supplied original file; never redraw, trace, recolor, skew, stretch, add effects, or generate a replacement.
7. Check clear space, minimum size, contrast and crop against Guide pp.22–25 or approved asset notes. If unavailable, mark `待确认`.

## Rendering rule — required

The gradient logo SVGs use multiple stops with `stop-opacity`. **ImageMagick's internal SVG renderer renders them incorrectly** — the output is visibly darker and parts of the mark are flattened. This has previously caused the logo to look wrong or "missing" in composed layouts.

- Do **not** produce logo raster output with `magick file.svg` / `convert file.svg`.
- Use `rsvg-convert` (librsvg), or another spec-complete renderer such as a browser engine.
- Simplest correct path: **use the bundled PNG directly** instead of converting the SVG at all.
- After any SVG render, verify against the bundled PNG before placing it:

```sh
rsvg-convert assets/logos/svg/<name>.svg -o /tmp/render.png
magick compare -metric RMSE /tmp/render.png assets/logos/png/<name>.png null:   # expect 0
```

`scripts/render_logo.sh` performs this render-and-verify step.

Representative current SVG families include `蓝色渐变_英文_横版_组合标.svg`, `蓝色渐变_中英文_横版_组合标.svg`, `蓝色渐变_无文字_方形_图形标.svg`, `白色渐变_英文_横版_组合标.svg`, `白色纯色_无文字_方形_图形标.svg`, `黑色_中英文_横版_组合标.svg`, and `蓝色纯色_无文字_方形_图形标.svg`. Always live-resolve rather than relying on this example list.

Naming pattern: `{color}_{lettering}_{orientation}_{form}`.
