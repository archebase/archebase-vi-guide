---
name: archebase-vi-guide
version: 3.1.3
description: "Use for any ArcheBase-branded design or review. This is a 3-layer VI system: SKILL.md orchestrates progressive disclosure; references contain route/page/domain rules; templates, manifests, tokens, checklists and validators make execution repeatable. Use with the shared pptx skill for PowerPoint work."
license: Proprietary. Do not redistribute brand assets.
---

# ArcheBase VI Guide System

This skill is the orchestration layer for ArcheBase brand work. It is deliberately not a static manual. It selects the smallest relevant domain reference, uses approved assets, compiles content into a design route, renders and checks the result, and stops at explicit approval gates.

## Trigger

Use for any ArcheBase-branded PPTX/deck/BP/film, website/product UI, social or press material, video/event screen, image prompt/source, Logo/font/color/template operation, or brand review.

If `.pptx` or `.potx` is involved, load this skill **and** the shared `pptx` skill. The `pptx` skill owns PowerPoint construction, OOXML, native charts, rendering and technical validation. This skill owns ArcheBase visual direction, source evidence, asset choice and brand QA.

## Three-layer design

- **Layer 1 — this `SKILL.md`:** triggers, source hierarchy, route selection, progressive disclosure, high-level compiler, mandatory release gates and output contract.
- **Layer 2 — `references/`:** page evidence, logo resolution, visual grammar, route playbooks, review rubric, governance and release procedures. Load only what the task needs.
- **Layer 3 — `templates/`, `checklists/`, `tokens/`, `assets/`, `scripts/`:** fillable records, semantic tokens, approved asset manifest and deterministic validators. These make execution repeatable.

Do not treat Layer 3 records as official rules unless their source and approval fields are complete.

## Source hierarchy

1. Current approved asset package and explicit brand-owner decisions.
2. Official 46-page `智域基石vi基础.pdf`.
3. Layer 2 interpretations citing Guide pages.
4. Temporary heuristics, always labeled `待确认`.

On conflict, stop and record the conflict. Never average conflicting brand values.

## Progressive disclosure

1. Load this file.
2. Select route: `deck`, `web-ui`, `social`, `video-event`, `image`, or `review`.
3. Load `references/guide-page-evidence.md` and `references/logo-asset-resolver.md` for all visual asset work.
4. Load the selected route playbook.
5. Load the relevant template, checklist and token/manifest files.
6. Build, render, inspect, validate and run release gates.
7. Return only relevant evidence, decisions, QA, approvals and verdict.

## Logo assets

Bundled and synced to `智域基石 Logo V2` (2026-09-22):

| Directory | Use for |
|---|---|
| `assets/logos/svg/` | Source of truth for geometry and color |
| `assets/logos/png/` | Raster delivery for web, social, office and decks |
| `assets/logos/png-hires/` | App icon, avatar, favicon, large format |

Every SVG has a matching same-size PNG; all pairs verified at RMSE 0. Prefer the bundled PNG for raster output.

**Renderer warning:** the gradient logo SVGs use multiple stops with `stop-opacity`. ImageMagick's internal SVG renderer renders them incorrectly — output is darker and parts of the mark are flattened, which has caused the Logo to look wrong or "missing" in composed layouts. Use `rsvg-convert` (librsvg) or a browser engine, never `magick file.svg`. `scripts/render_logo.sh` renders and verifies; `scripts/validate_logo_bundle.py` checks the bundle.

## Brand constitution

- One artifact/page/frame has one primary audience judgment.
- Evidence, product UI, real physical-world data, system/process structure and verifiable claims outrank decoration.
- The visual language should feel reliable, ordered and infrastructure-grade, not generic “AI futuristic”.
- Official Logo/font/color assets are immutable; never redraw, regenerate or silently replace them.
- Unknowns are `待确认`, not an invitation to invent precision.
- No external publication before asset, design, claims/rights and export/QA gates pass human review.

## Compiler

Before design, fill `templates/brief.md`. Then:

1. Extract the one-sentence takeaway.
2. Identify evidence and claims; distinguish fact, inference and proposal.
3. Inspect relevant Guide pages and create page records.
4. Resolve official assets using the resolver and record the selected file.
5. Choose a composition recipe and semantic tokens.
6. Build with the route playbook and relevant specialist skill.
7. Render at the actual channel size/distance/crop.
8. Run route checklist, validators and four release gates.
9. Record unresolved approvals, owner and release impact.
10. Return a single verdict: `可发布`, `修复后复审`, or `阻塞，待确认`.

## Mandatory blocking conditions

Block publication when any of these is unresolved: invented/incorrect Logo, Logo rasterized with a renderer that does not match the approved asset, missing asset rights, uncertain public claim or customer data, unresolved `ArcheBase`/`ArchBase`/`ARCHBASE` naming, unapproved color/type rule, unreadable or overflowing output, missing source for material metrics, or failed technical/visual QA.

## Output contract

Every use returns:

1. Route and brief.
2. Page/frame inventory or review scope.
3. Selected assets/tokens and source pages.
4. Decisions and assumptions.
5. Build/review result.
6. Asset/design/claims-rights/export-QA results.
7. Unresolved approvals with owner and impact.
8. One release verdict.

## References

See `references/README.md` for the route map. Do not load every reference by default.
