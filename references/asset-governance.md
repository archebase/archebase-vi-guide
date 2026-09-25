# Asset governance

Load when creating, updating, approving or auditing any official ArcheBase brand asset, or when a deliverable's asset provenance is in question.

This reference governs the *assets themselves*: identity files, type files, color definitions and the records that describe them. Composition and channel decisions belong to the route playbooks.

## 1. Source hierarchy

1. The current approved asset package and explicit brand-owner decisions.
2. The official 46-page `智域基石vi基础.pdf`.
3. Layer 2 interpretations citing Guide pages.
4. Temporary heuristics, always labeled `待确认`.

On conflict, **stop and record the conflict**. Never average conflicting brand values, and never pick the more convenient one. Route the conflict to the brand owner with both values and their sources.

## 2. Roles

| Role | Owns |
|---|---|
| Brand owner | Approving new assets, variant changes, legacy retirement, and any exception |
| Asset maintainer | Keeping `assets/logo-manifest.json` and the bundle in sync with the approved source |
| Designer | Selecting and placing assets through `references/logo-asset-resolver.md` |
| Reviewer | Confirming the delivered artifact used the approved asset, unmodified |

An asset change with no recorded owner approval is not current, regardless of how it got into the bundle.

## 3. What every asset record must contain

For each bundled asset family, the manifest records:

- filename and extension,
- asset family: color, lettering, orientation, form, and any delivery suffix,
- source directory and the remote reference or token,
- source modified time,
- legacy status,
- verification result.

`assets/logo-manifest.json` is that record. `references/guide-source-manifest.md` records the Guide and folder provenance. `EXPORT-METADATA.json` records the skill bundle identity and changelog.

Never store credentials, OAuth codes, access tokens or private authorization URLs in the skill or its records.

## 4. Inventory integrity

The bundle's counts and the manifest's counts must agree, and every SVG must have a matching PNG at the same native size.

```sh
python3 scripts/validate_logo_bundle.py      # pairs, empty files, alpha sanity
python3 scripts/validate_asset_reference.py  # manifest vs bundle, dangling and legacy references
python3 scripts/validate_asset_integrity.py  # SHA-256 pins: assets unmodified
```

Run all three before and after any change to `assets/`. All are deterministic and read-only. `scripts/render_logo.sh --verify-all` additionally re-renders every SVG and compares it against the bundled PNG at native size.

A count mismatch between the manifest and the bundle is a record defect: fix the record, not the count, unless a file actually moved.

## 5. Brand assets are immutable

**A bundled brand asset is never edited.** Not to fix a curve, not to adjust a gradient, not to add a variant, not to "improve" an export. The asset is the official mark as the brand owner issued it. `scripts/validate_asset_integrity.py` pins every file by SHA-256 and fails CI on any modification, addition or deletion, so this is enforced rather than merely asked for.

Being the editable vector master is about *using* the SVG — measuring it, placing it, exporting approved derivatives from it — not about altering the mark.

When the mark genuinely must change, the asset is not updated; it is **replaced by a new official delivery**:

1. The brand owner issues a new delivery. Record who approved it and when.
2. Re-sync the affected assets wholesale from that delivery. Do not hand-edit a file to reconcile the two.
3. Keep the official filenames. Do not rename assets to a local convention — the names are the contract with the delivery.
4. Add both the SVG source and its matching PNG so the pair check stays green. Generate the PNG through `scripts/render_logo.sh`, never through ImageMagick's internal SVG renderer.
5. Update `assets/logo-manifest.json`: inventory, verification record, dates, `source_delivery`, and any new `known_gaps`.
6. Run every validator, then `scripts/render_logo.sh --verify-all`.
7. Regenerate the pins as part of the same change: `python3 scripts/validate_asset_integrity.py --write`. This step *is* the recorded act of accepting the delivery — never run it to silence a failure caused by an edit.
8. Increment the skill version and add a changelog entry in `EXPORT-METADATA.json`.

## 5a. Re-verifying the bundle against the delivery

Before trusting the bundle, before a large brand deliverable, or whenever the source folder may have moved on, compare the two directly. This is read-only on the delivery.

1. Locate the delivery folder from the approved `source_folder` URL. `source_local_path` is optional audit metadata and may be null in the portable skill; never require a machine-specific Downloads path.
2. Compare every bundled asset against its counterpart with SHA-256 — not size or timestamps.
3. Run `scripts/render_logo.sh --verify-all` to confirm every SVG still renders to its bundled PNG bit-for-bit.
4. Record the outcome in the manifest's `verified.reverified` block: date, method, result.

Compare against the delivery's own layout, which differs from the bundled layout. See `source_layout` in the manifest:

| Delivery | Bundled |
|---|---|
| `svg/*.svg` (25) | `assets/logos/svg/` |
| `svg/*.png` (9) | `assets/logos/png-hires/` |
| `png/*.png` (24) | `assets/logos/png/` — plus one extra, see below |
| `jpg/*.jpg` (23) | not bundled; preview only |

The delivery's `svg/` folder mixes SVG sources with PNG exports, and its `png/` folder holds 24 files while the bundle's `assets/logos/png/` holds 25. The extra file is `蓝色纯色_无文字_方圆通用_图形标.png`, copied from the delivery's `svg/` folder so that every SVG has a same-size raster beside it and the pair check stays green. Expect this asymmetry; do not "fix" it by deleting the file or by moving the delivery's files around.

## 6. Renderer rule

The gradient SVGs use multiple stops with `stop-opacity`. **ImageMagick's internal SVG renderer renders them incorrectly** — output is darker and parts of the mark are flattened, which has previously made the mark look wrong or "missing" in composed layouts.

- Never produce logo raster output with `magick file.svg` or `convert file.svg`.
- Use `rsvg-convert` (librsvg) or another spec-complete renderer.
- Simplest correct path: use the bundled PNG directly.
- After any SVG render, verify against the bundled PNG before placing it.

An asset rasterized with a renderer that does not match the approved asset blocks release.

## 7. Legacy assets and superseded generations

Files marked `old_*` are legacy. They may not be used in new work and may only be used in an existing artifact when the brand owner approves the exception in writing, recorded in the decision record. Retirement of a legacy asset is a brand-owner decision.

Whole generations can also be superseded, which matters more than any single file. The brand owner confirmed on 2026-09-25 that **`智域基石 Logo V2` is the correct version**; the manifest records this under `approved_generation`, including the superseded set. In short:

- the V1 generation (naming with no 纯色/渐变 split — `白色_*` / `蓝色_*`),
- the 2026-07-29 unreviewed raw export (`正常logo 1–10/a–h`, `单色logo 1–5`),
- pre-V2 drafts (`20260321logo*`, `20260325logo-黑白彩色`, `成图logo-*`, `LOGO.ai`, `LOGO排版00.ai`).

A superseded generation stays out of the bundle. Do not add it as `old_*` "for completeness": mixing generations is what makes a resolver ambiguous, because the older names look like plausible variants of the newer set. If an older file is genuinely needed for an existing artifact, keep it outside the bundle and record the exception.

An absent variant is a `待确认` item for the brand owner, never a gap to improvise from an older generation.

## 8. Approvals and blocking conditions

Block publication when any of these is unresolved:

- an invented, redrawn or incorrect mark,
- a mark rasterized with a renderer that does not match the approved asset,
- missing asset rights,
- a missing or unapproved asset variant,
- use of a name other than the approved public `ArcheBase` in current work, or an unapproved lockup/domain naming change,
- an unapproved color or type rule,
- missing source for a material metric,
- a manifest or bundle integrity failure.

Record each open item with its owner and its release impact. An item with no owner is not merely open — it is unassigned, and the release stays blocked.
