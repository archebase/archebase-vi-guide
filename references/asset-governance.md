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
python3 scripts/validate_logo_bundle.py     # pairs, empty files, alpha sanity
python3 scripts/validate_asset_reference.py # manifest vs bundle, dangling and legacy references
```

Run both before and after any change to `assets/`. Both are deterministic and read-only. `scripts/render_logo.sh --verify-all` additionally re-renders every SVG and compares it against the bundled PNG at native size.

A count mismatch between the manifest and the bundle is a record defect: fix the record, not the count, unless a file actually moved.

## 5. Adding or updating an asset

1. Confirm the change is approved by the brand owner and record who approved it and when.
2. Export from the approved source. Do not re-export an asset by re-rendering a lossy copy.
3. Keep the official filename. Do not rename assets to a local convention — the names are the contract with the source delivery.
4. Add both the SVG source and the matching PNG so the pair check stays green.
5. Update `assets/logo-manifest.json`: inventory, verification record, date, and any new `known_gaps`.
6. Run both validators and `scripts/render_logo.sh --verify-all`.
7. Increment the skill version and add a changelog entry in `EXPORT-METADATA.json`.

## 6. Renderer rule

The gradient SVGs use multiple stops with `stop-opacity`. **ImageMagick's internal SVG renderer renders them incorrectly** — output is darker and parts of the mark are flattened, which has previously made the mark look wrong or "missing" in composed layouts.

- Never produce logo raster output with `magick file.svg` or `convert file.svg`.
- Use `rsvg-convert` (librsvg) or another spec-complete renderer.
- Simplest correct path: use the bundled PNG directly.
- After any SVG render, verify against the bundled PNG before placing it.

An asset rasterized with a renderer that does not match the approved asset blocks release.

## 7. Legacy assets

Files marked `old_*` are legacy. They may not be used in new work and may only be used in an existing artifact when the brand owner approves the exception in writing, recorded in the decision record. Retirement of a legacy asset is a brand-owner decision.

## 8. Approvals and blocking conditions

Block publication when any of these is unresolved:

- an invented, redrawn or incorrect mark,
- a mark rasterized with a renderer that does not match the approved asset,
- missing asset rights,
- a missing or unapproved asset variant,
- an unresolved `ArcheBase` / `ArchBase` / `ARCHBASE` naming question,
- an unapproved color or type rule,
- missing source for a material metric,
- a manifest or bundle integrity failure.

Record each open item with its owner and its release impact. An item with no owner is not merely open — it is unassigned, and the release stays blocked.
