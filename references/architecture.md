# ArcheBase VI Guide System — 3-Layer Architecture

## Why this skill needs more than one file

A single `SKILL.md` is the entrypoint, not the entire knowledge system. The `pptx` skill has 55 files because it separates trigger/routing guidance, operational playbooks, reusable scripts, validators, references, and examples. The VI system now follows the same architecture:

- **Layer 1 — SKILL.md / orchestration:** short trigger contract, source hierarchy, decision tree, progressive disclosure, routing, mandatory gates, and output contract.
- **Layer 2 — references / domain knowledge:** page-by-page evidence, logo resolver, visual grammar, channel playbooks, review rubric, asset governance, and QA procedures. Load only the reference needed by the route.
- **Layer 3 — assets/scripts/templates / execution tools:** approved asset manifests, token files, decision-record templates, inspection worksheets, route checklists, and optional automation. These support repeatable execution without bloating the trigger file.

The three layers are intentionally different: the first decides *what to load*, the second explains *how to decide*, and the third helps *execute and verify*.

## Layer 1: SKILL.md responsibilities

The primary file should remain compact and operational. It must contain:

1. When to trigger, including all ArcheBase-branded artifacts.
2. Source hierarchy and conflict policy.
3. Route selection: `deck`, `web-ui`, `social`, `video-event`, `image`, `review`.
4. The minimum brand constitution: official assets immutable, evidence before decoration, one primary judgment, unknowns are `待确认`, human approval before release.
5. Progressive-disclosure instructions pointing to Layer 2 references.
6. The high-level compiler: brief → inspect → plan → build → render → gates → verdict.
7. The output contract and release verdicts.

It must not become a 50-page dump. If a task needs detail, load a reference file.

## Layer 2: reference routing table

| Need | Reference to load | Output |
|---|---|---|
| Understand official pages | `references/guide-page-evidence.md` | page-level inspection records and confidence |
| Select a Logo | `references/logo-asset-resolver.md` | asset filename/type/background/lockup/language/orientation |
| Establish colors/type/layout | `references/visual-grammar.md` | semantic tokens and composition decisions |
| Build a PPTX | `references/deck-playbook.md` then shared `pptx` skill | slide inventory, build plan, QA plan |
| Build web/UI | `references/web-ui-playbook.md` | responsive hierarchy and component states |
| Make social/press material | `references/social-playbook.md` | first-frame/crop/copy/rights checks |
| Make video/event material | `references/video-event-playbook.md` | viewing-distance, safe-area, motion checks |
| Generate images | `references/image-generation-playbook.md` | no-logo prompt, provenance and rights checks |
| Review an artifact | `references/review-rubric.md` | severity findings, score, verdict |
| Govern assets and updates | `references/asset-governance.md` | version/hash/owner/approval record |
| Validate a delivery | `references/release-gates.md` | four-gate pass/fail/待确认 report |

## Layer 3: execution support

Layer 3 should contain executable or fillable support files, not more prose:

- `assets/guide-page-index.json`: page-group routing for the official Guide, with the source hash and evidence-register pointer.
- `assets/guide-evidence.json`: compact, verified page-level evidence for numeric/color/font claims; preserves `do_not_infer` boundaries without embedding the large PDF.
- `assets/logo-manifest.json`: generated from a read-only listing of the approved Drive folder; records current filename, extension, asset family, source directory, token/reference, modified time, and legacy status. Never stores credentials.
- `tokens/archebase.tokens.json`: semantic colors, explicit p.28 ratio and p.30–32 neutral evidence, type families, logo policy, and remaining `待确认` implementation fields.
- `templates/brief.md`: mode/route/audience/dimensions/judgment/evidence/assets/risk.
- `templates/page-inspection-record.md`: page, visible elements, extracted rule, evidence type, applies-to, do-not-infer, confidence, reviewer/date.
- `templates/decision-record.md`: question, options, choice, rationale, source page, assumptions, reversible boundary, approver.
- `templates/release-report.md`: four gates, findings, owner, impact, verdict.
- `checklists/deck.md`, `checklists/web-ui.md`, `checklists/social.md`, `checklists/video-event.md`, `checklists/image.md`: compact route-specific execution gates.
- `scripts/validate_tokens.py`: rejects colors outside the approved token set and checks the explicit Guide ratio/neutral evidence.
- `scripts/validate_guide_evidence.py`: verifies the compact evidence register and, when a local PDF is supplied, its page count and SHA-256.
- `scripts/validate_modes.py`: verifies the opt-in mode contract, hard boundaries, templates and mode-aware gates.
- `scripts/validate_asset_reference.py`: rejects missing/non-current/logo recreation references and flags legacy assets.
- `scripts/check_release_report.py`: ensures every deliverable has source pages, QA status, unresolved owner, and verdict.
- `evals/evals.json`: representative route prompts and verifiable expectations for regression evaluation.

Scripts must be deterministic, read-only by default, and fail closed for brand-sensitive errors.

## Progressive disclosure contract

Use this order:

1. Load `SKILL.md`.
2. Select the route.
3. Load exactly the route playbook and any evidence/asset reference needed.
4. Load templates/checklists before producing the artifact.
5. Run validators and release gates after rendering.
6. Return only the relevant decisions, QA, sources, and unresolved approvals.

Do not load all references for a simple request. Do not skip the references for a high-risk public artifact.

## What belongs where

| Content | Layer |
|---|---|
| “Use this skill for ArcheBase-branded work” | 1 |
| “For PPTX also load `pptx`” | 1 |
| Exact interpretation of Guide page 28 | 2 |
| Logo filename and token mapping | 2 + 3 manifest |
| Four color tokens | 2 + 3 token file |
| How to render/validate PPTX | shared `pptx` skill |
| A page inspection form | 3 template |
| Brand release blocker | 1 + 2 release-gates |
| Current owner/hash/date | 3 manifest / governance record |

## Change management

A change to Layer 1 affects routing and may be breaking. A change to Layer 2 affects design decisions and must cite Guide pages. A change to Layer 3 affects execution and must add a regression test. Increment the system version when any layer changes, preserve the prior manifest, and verify every bound agent still has both `pptx` and `archebase-vi-guide`.
