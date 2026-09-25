# Logo asset resolver

Source folder: `https://archebase.feishu.cn/drive/folder/MBewfd14ll34N0dJINNcQnQqn4c`
Current delivery: `智域基石 Logo V2` (synced 2026-09-22). See `assets/logo-manifest.json` for inventory, naming pattern and verification record.

## Bundled asset directories

| Directory | Use for |
|---|---|
| `assets/logos/svg/` | Source of truth for geometry and color, and the editable vector master |
| `assets/logos/png/` | Raster delivery for web, social, office and deck export |
| `assets/logos/png-hires/` | App icon, avatar, favicon and large-format icon use |

The `svg/` files are the **editable vector master**, not a web-only export. Open them directly in Illustrator, Figma or Inkscape — **no `.ai` file is needed or supplied**, and the absence of one is not a gap to fill. All 25 are pure vector: `<path>` geometry, real `<linearGradient>` defs, a `viewBox`, no embedded raster and no external references.

The wordmark is outlined, so the SVGs contain no live `<text>`, which is standard for a logo and keeps rendering identical across tools.

"Editable" means the vector master can be opened, measured, placed and exported from directly — it does **not** authorise altering the mark. The bundled assets are **immutable**: never redraw, trace, recolor, skew, stretch, add effects to, or regenerate them, and never hand-edit a file to invent a variant. `scripts/validate_asset_integrity.py` pins every asset by SHA-256 and fails CI if one changes. If the mark itself must change, that is a new official delivery — see `references/asset-governance.md`.

Each SVG has a matching PNG at the same native size in `assets/logos/png/`. All 25 pairs verified at RMSE 0 on 2026-09-22.

## Current generation — required

`智域基石 Logo V2` is the **correct and current** generation (brand-owner decision, 2026-09-25; recorded in `assets/logo-manifest.json` under `approved_generation`). Resolve only against the bundled assets, which are a byte-for-byte copy of that delivery.

Never resolve to a superseded generation:

| Superseded | What it is |
|---|---|
| V1 naming (`白色_*` / `蓝色_*`, no 纯色/渐变 split) | The previous generation; shipped as `智域基石 Logo`, `智域基石 Logo V1 2` |
| The 2026-07-29 raw export (`正常logo 1–10/a–h`, `单色logo 1–5`) | Unreviewed export of the same marks; not the reviewed delivery |
| Pre-V2 drafts (`20260321logo*`, `20260325logo-黑白彩色`, `成图logo-*`, `LOGO.ai`, `LOGO排版00.ai`) | Historical drafts |

A filename from a superseded generation is **not** a missing variant to reconstruct. If a needed variant appears absent, mark it `待确认` and ask the brand owner — do not rebuild it from an older name or an older file.

## Resolution procedure

1. Use the bundled `assets/logos/` directories first. Read-only list the Feishu folder only when the needed variant is missing or a newer export must be confirmed.
2. Prefer current `svg` for the source; use the bundled `png` for raster output and `jpg` only for preview/reference.
3. Treat `old_png` and `old_ai` as legacy until owner confirms otherwise.
4. Resolve by background (light/dark/image/mono), lockup (graphic/wordmark/combination), language (Chinese/English/bilingual), and orientation (horizontal/vertical/square/square-to-circle).
   For a circular display surface or any placement that may be circularly cropped, use the supplied `方圆通用` variant—not the ordinary `方形` variant—because it includes the approved circular safe area. The current bundled circular-safe asset is `蓝色纯色_无文字_方圆通用_图形标.svg` (with matching PNG/PNG-hires); do not create a circular crop from `方形` by scaling or masking.
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
