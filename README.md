# ArcheBase VI Guide Skill

An agent skill that encodes the ArcheBase Visual Identity (VI) system: logo resolution, color and type rules, page-level evidence from the official VI Guide, per-channel composition playbooks, review rubric, and release gates.

It is built as a **3-layer progressive-disclosure system** rather than a static manual, so an agent can load only the rules a given task needs.

| Layer | Contents | Role |
|---|---|---|
| 1 | `SKILL.md` | Triggers, source hierarchy, route selection, compiler, release gates, output contract |
| 2 | `references/` | Guide page evidence, logo resolver, visual grammar, route playbooks, review rubric, release procedures |
| 3 | `templates/`, `checklists/`, `tokens/`, `assets/`, `scripts/` | Fillable records, semantic tokens, approved asset manifest, deterministic validators |

## When the skill triggers

Any ArcheBase-branded design or review work: PPTX/deck/BP/film, website or product UI, social and press material, video or event screens, image prompts and sourcing, Logo/font/color/template operations, and brand review.

For `.pptx` / `.potx` work, load this skill **together with** the shared `pptx` skill — that skill owns PowerPoint construction, OOXML, native charts, rendering and technical validation, while this one owns visual direction, source evidence, asset choice and brand QA.

## Routes

`deck` · `web-ui` · `social` · `video-event` · `image` · `review`

Each route has a playbook in `references/` and a matching checklist in `checklists/`.

## Install

Copy or symlink the repository into your agent's skills directory. For example:

```sh
git clone https://github.com/archebase/archebase-vi-guide.git
ln -s "$PWD/archebase-vi-guide" ~/.agents/skills/archebase-vi-guide
```

## Bundled assets

The logo bundle is synced to the official delivery `智域基石 Logo V2` (2026-09-22) and is included so the skill works offline.

| Directory | Use for |
|---|---|
| `assets/logos/svg/` | Source of truth for geometry and color |
| `assets/logos/png/` | Raster delivery for web, social, office and deck export |
| `assets/logos/png-hires/` | App icon, avatar, favicon and large-format icon use |

Asset filenames follow the official brand naming pattern `{color}_{lettering}_{orientation}_{form}` and are kept in their original Chinese form on purpose — renaming them would break the link to the source delivery. See `assets/logo-manifest.json` for the inventory and `references/logo-asset-resolver.md` for the resolution procedure.

The SVGs are the **editable vector master** — open them directly in Illustrator, Figma or Inkscape; no `.ai` is supplied and none is needed. Being editable is about using the master, not altering it: the bundled assets are **immutable**, and `scripts/validate_asset_integrity.py` pins every one by SHA-256 so CI fails if a byte changes. A changed mark is a new official delivery, never a local edit.

### Renderer warning

The gradient logo SVGs use multiple stops with `stop-opacity`. ImageMagick's internal SVG renderer renders them incorrectly — output is darker and parts of the mark are flattened. Use `rsvg-convert` (librsvg) or a browser engine, never `magick file.svg`. The simplest correct path is to use the bundled PNG directly.

```sh
rsvg-convert assets/logos/svg/<name>.svg -o /tmp/render.png
magick compare -metric RMSE /tmp/render.png assets/logos/png/<name>.png null:   # expect 0
```

`scripts/render_logo.sh` performs this render-and-verify step.

## Validators

```sh
python3 scripts/validate_logo_bundle.py     # SVG/PNG pair and bundle integrity
python3 scripts/validate_asset_integrity.py # SHA-256 pins: brand assets unmodified
python3 scripts/validate_tokens.py          # tokens against the approved Guide color set
python3 scripts/validate_asset_reference.py # manifest vs bundle; dangling/legacy references
python3 scripts/check_release_report.py     # release report completeness
python3 scripts/check_doc_links.py          # markdown and reference-index link integrity
```

All are deterministic, read-only, and exit non-zero on failure. They run in CI on every push and pull request via [`.github/workflows/validate.yml`](.github/workflows/validate.yml).

To additionally re-render every SVG and compare it against the bundled PNG bit-for-bit (requires `librsvg` and ImageMagick):

```sh
scripts/render_logo.sh --verify-all
```

## Source hierarchy

1. Current approved asset package and explicit brand-owner decisions.
2. The official 46-page `智域基石vi基础.pdf`.
3. The interpretations in `references/`, each citing Guide pages.
4. Temporary heuristics, always labeled `待确认`.

On conflict, stop and record the conflict. Never average conflicting brand values.

## License and brand assets

The skill instructions are published so ArcheBase teams and their agents can apply the brand system consistently. The logo files and the VI Guide are **proprietary brand assets of ArcheBase** and are not licensed for redistribution or reuse outside ArcheBase-branded work. See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md).

Do not redraw, trace, recolor, skew, stretch, add effects to, or regenerate the official marks.
