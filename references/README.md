# ArcheBase VI System references

Load only the references needed for the current route.

## Core references — load for all visual asset work

| Reference | When to load |
|---|---|
| `modes.md` | **Always, before applying route guidance**; choose strict/guided/creative/off and preserve channel latitude |
| `guide-page-evidence.md` | Any task needing VI Guide page interpretation; pair with `assets/guide-evidence.json` for verified numeric/color/font evidence |
| `logo-asset-resolver.md` | Any task placing or reviewing Logo/assets |
| `visual-grammar.md` | Any visual design or review |
| `release-gates.md` | Any deliverable approaching review/release |

## Route playbooks — load the one matching the route

| Route | Playbook |
|---|---|
| `deck` | `deck-playbook.md` (also load the shared `pptx` skill) |
| `web-ui` | `web-ui-playbook.md` |
| `social` | `social-playbook.md` |
| `video-event` | `video-event-playbook.md` |
| `image` | `image-generation-playbook.md` |
| `review` | `review-rubric.md` |

## Supporting references

| Reference | When to load |
|---|---|
| `architecture.md` | Changing the skill's own structure or layer responsibilities |
| `asset-governance.md` | Asset ownership, version, hash, approval or retirement work |
| `guide-source-manifest.md` | Confirming where the Guide and logo sources came from |

## Layer 3 execution files

| File | Purpose |
|---|---|
| `templates/brief.md` | Per-task brief; fill before designing |
| `templates/page-inspection-record.md` | One record per Guide page inspected |
| `templates/decision-record.md` | Choices, rationale, source page, approver |
| `templates/release-report.md` | The four release gates and the verdict |
| `checklists/*.md` | Route-specific execution gates |
| `tokens/archebase.tokens.json` | Semantic colors, Guide ratio/neutral evidence and type tokens |
| `assets/logo-manifest.json` | Logo inventory, naming rules, verification and known gaps |
| `assets/logo-checksums.json` | SHA-256 pins making the brand assets immutable |
| `assets/guide-page-index.json` | Guide page-group map and source hash |
| `assets/guide-evidence.json` | Verified page-level numeric and visual evidence register |
| `scripts/validate_logo_bundle.py` | SVG/PNG pair and bundle integrity |
| `scripts/validate_asset_integrity.py` | Pinned-asset check: fails if any brand asset changed |
| `scripts/validate_guide_evidence.py` | Evidence register and optional official PDF hash/page-count check |
| `scripts/validate_modes.py` | Opt-in mode, hard-boundary and mode-aware gate contract |
| `scripts/validate_tokens.py` | Token file against the approved Guide color set |
| `scripts/validate_asset_reference.py` | Manifest vs bundle, dangling and legacy references |
| `scripts/check_release_report.py` | Release report completeness |
| `scripts/check_doc_links.py` | Markdown and reference-index link integrity |
| `scripts/render_logo.sh` | Render an SVG and verify it against the bundled PNG |
| `evals/evals.json` | Representative prompts for skill regression evaluation |

## Version status

The `deck` and `review` routes have the most worked-out guidance. The other four playbooks were derived from the same Guide evidence, token set and release gates but have not yet been exercised on a full production deliverable. Treat their route-specific specifics as `待确认` until a real artifact confirms them.
