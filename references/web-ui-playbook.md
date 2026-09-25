# Web / product UI playbook

Load with `references/visual-grammar.md`, `references/logo-asset-resolver.md` and `references/guide-page-evidence.md`.

This playbook owns brand composition for screens and components. It does not own front-end architecture, component library choices or framework conventions.

## 1. Brief

Fill `templates/brief.md` before designing. A web brief must add:

- the exact viewport widths and heights being judged,
- the screen inventory: one row per screen with its single primary judgment,
- the interaction states in scope (see §5),
- light/dark mode support, if any.

One screen has one primary audience judgment. If a screen tries to make two arguments, split it.

## 2. Evidence to inspect

| Guide pages | What to take from them |
|---|---|
| 37–46 | Application boards: composition, grid, whitespace and scale. Inspect rendered pages; OCR alone is not evidence. |
| 22–25 | Primary and auxiliary identity: clear space, minimum size, orientation and combination restrictions. |
| 29 | Main color values (`#0032FF`, `#7172FA`, `#619AFD`, `#46CFFF`). |
| 30–32 | `#1E2124` neutral levels and their role mapping. |
| 28 | The `25% / 50% / 10% / 5%` ratio diagram — **role mapping is unresolved**, see §4. |

Record one `templates/page-inspection-record.md` per page used. A visual inference may not become an official rule without approval.

## 3. Hierarchy and composition

- State the conclusion before the metadata. A user should get the judgment from the first screenful.
- Keep no more than three hierarchy levels.
- Use one dominant field, one structural blue, and at most one meaningful highlight.
- Let evidence dominate decoration. Data flow, connected nodes, labeled modules, system boundaries and real physical-world imagery are allowed only when they explain the claim.

Remove random node graphs, circuit wallpaper, glow, rainbow palettes, 3D charts, decorative gradients, filler stripes and unrelated icon families.

## 4. Tokens

Map every color to a semantic role from `tokens/archebase.tokens.json`. Do not introduce a color that is not in the token file.

`AB_CHARCOAL` `#1E2124` is the technical dark field and neutral text color. Its exact opacity levels per role are **待确认** — do not present an invented scale as the approved one.

The p.28 ratio roles are **待确认**. Until the brand owner confirms the mapping, do not claim a specific 25/50/10/5 usage split in a deliverable; record it as an open approval in the release report.

Do not introduce orange as a CTA or status color. The Guide text does not confirm that system.

## 5. Required states

A component or screen is not complete until each state has a defined treatment. Cover at minimum:

default · hover · active · focus-visible · disabled · error · empty · loading

Where the Guide or an approved component library is silent on a state's visual treatment, mark it **待确认** rather than inventing one, and list it as an unresolved approval.

## 6. Logo and favicon

1. Resolve the variant through `references/logo-asset-resolver.md` by background, lockup, language and orientation.
2. Use the SVG for web rendering. Never rasterize the gradient SVGs with ImageMagick's internal renderer.
3. Use `assets/logos/png-hires/` for favicon, app icon and avatar. These are opaque `白底` or transparent variants — do not substitute one for the other. See the `known_gaps` in `assets/logo-manifest.json`.
4. Check clear space and minimum size against Guide pp.22–25. If unavailable, mark **待确认**.
5. Never redraw, trace, recolor, skew, stretch, add effects to, or regenerate the mark.

## 7. QA before release

- Render at the actual viewport sizes in the brief, then inspect the rendered output visually — not the source markup.
- Check overflow, wrapping, truncation, contrast and focus visibility.
- Check every crop and every breakpoint in scope.
- Check that dark mode (if in scope) still places the mark against an approved background.
- Run `checklists/web-ui.md`, then the four gates in `references/release-gates.md`.

## 待确认

- p.28 ratio role mapping.
- `#1E2124` neutral opacity levels per role.
- Logo clear space and minimum size in pixels.
- Font license and approved weights for web embedding.
- `ArcheBase` / `ArchBase` / `ARCHBASE` naming in UI copy.
- Color conversion for screens vs print.
- The rule selecting 方形 vs 方圆通用 orientation.
