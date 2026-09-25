# InkPost / WeChat article playbook

Load this playbook for Markdown articles laid out or corrected in InkPost for an ArcheBase-owned WeChat channel. Load it with `visual-grammar.md`, `modes.md`, `assets/guide-evidence.json`, `tokens/archebase.tokens.json` and `checklists/inkpost-wechat.md`.

This playbook owns article hierarchy, CSS token mapping and export QA. InkPost owns Markdown parsing, CSS inlining, image processing and clipboard export.

## 1. Mode and brief

Default to `guided`. Use `strict` when the article needs formal VI sign-off or is being prepared as an official company release.

Record:

- article path, audience and one-sentence takeaway;
- mode, WeChat destination and preview width;
- whether the task is a new article, layout correction or CSS import/export;
- claims, metrics, images, logos and naming that require approval.

One article has one primary audience judgment. Put the conclusion before explanatory metadata where the narrative permits.

## 2. Theme source

The tracked InkPost preset is `src/shared/presets/archebase-wechat-safe.ts` in the InkPost repository. Its preset id is `preset-archebase-wechat-safe`.

The local InkPost app may persist user-created themes separately. Those are user state, not a brand source of truth:

- do not copy a user's complete local store into a repository;
- do not overwrite a user-created theme unless the user asks to synchronize it;
- compare the CSS that will be exported, not just a source preset, before release;
- when a local theme and tracked preset differ, state the source and the difference.

## 3. Article grammar

- Use one `h1` article title; `h2` and `h3` establish the only meaningful section hierarchy. Do not add decorative headings.
- Keep body copy neutral. `#0032FF` is structural emphasis; colored prose should not become the body texture.
- Use one dominant neutral field, one structural blue and at most one meaningful highlight per module.
- Use `::: block-1`, `::: block-2`, `::: block-3`, `::: info`, `::: tip`, `::: warning` and `::: danger` only for semantic callouts. Reuse the same callout for the same meaning inside an article.
- Images must carry evidence or narrative. Preserve aspect ratio and inspect the real WeChat crop.
- Do not use a Logo as a CSS decoration. If an approved logo is needed, resolve the supplied V2 asset separately through `logo-asset-resolver.md`; do not regenerate, recolor or rasterize it through ImageMagick.

## 4. WeChat-safe CSS mapping

The following are **channel mappings**, not newly approved semantic roles in the VI Guide:

| Article role | Mapping | Evidence / boundary |
| --- | --- | --- |
| Structural heading and link | `#0032FF` | `color.ratio`, p.28 |
| Secondary hierarchy and quotation edge | `#7172FA` | `color.ratio`, p.28 |
| Secondary annotation / warning edge | `#619AFD` | `color.ratio`, p.28 |
| Controlled highlight / heading edge | `#46CFFF` | `color.ratio`, p.28 |
| Body copy and technical field | `#1E2124` | `neutral.background`, `neutral.text`, pp.30–32 |
| Light surface | `#FFFFFF`, plus named blue tints in the tracked preset | white is a channel surface; exact neutral compositing remains `待确认` |

Use 思源黑体 / Source Han Sans SC as the preferred Chinese stack, with installed-system fallbacks. WeChat cannot guarantee font embedding. Poppins is the Latin family shown in the Guide, but exact production files, CSS weights and license remain `待确认`.

Do not interpret the p.28 50/25/10/5 labels as component-level CSS quotas. The remaining 10% is unassigned. Do not introduce orange as a brand CTA or status color.

Keep CSS compatible with InkPost's WeChat scanner: avoid flex/grid, fixed/sticky positioning, animation, transforms, filters, masks, columns and vertical writing mode. Do not rely on gradients for ordinary article layout.

## 5. Preflight

Run the deterministic CSS validator against the exact CSS being exported:

```sh
python3 scripts/validate_inkpost_css.py path/to/theme.css
```
It rejects unsafe WeChat layout properties, prohibited orange declarations, gradient dependency and saturated colors outside the approved article palette. It accepts only the approved VI colors plus explicitly listed light blue channel tints, so do not use it to bless a campaign-specific `creative` extension.

Then render the actual Markdown with InkPost and inspect the preview at its target width. Check heading wrapping, paragraphs, callouts, code, tables, images and all first-screen content. A scanner pass is not visual QA.

## 待确认

- p.28 semantic roles and per-component allocation;
- exact alpha/compositing values for `#1E2124` and its light surfaces;
- production font files, weights and licensing;
- logo clear space and minimum size in a WeChat article;
- `ArcheBase` / `ArchBase` / `ARCHBASE` naming approval;
- naming/role mapping for a warning or error state.
