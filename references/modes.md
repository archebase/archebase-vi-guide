# VI guidance modes

The skill is an opt-in collaborator, not a mandatory visual police layer. Choose a mode before applying route guidance. If the user has not specified one, infer the least restrictive mode that still serves the request and state the choice briefly.

## Modes

| Mode | Use when | What the skill does | What it does not do |
|---|---|---|---|
| `strict` | Official brand system work, website, investor/partner deck, formal company material, or the user explicitly asks for VI compliance | Applies the full Guide evidence, approved asset rules, route checklist and release gates | Does not invent missing rules; unresolved official questions still go to `待确认` |
| `guided` | Normal ArcheBase work where the user wants recognizable brand coherence but has not requested strict conformance | Recommends assets, palette, type, hierarchy and QA; flags deviations and suggests fixes | Does not block a creative choice merely because it departs from a soft visual preference |
| `creative` | Social, campaign, event, editorial, recruiting, or experimental work where platform-native style and creative authorship matter | Protects identity, rights, claims, privacy and asset provenance while allowing deliberate stylistic departure | Does not force the p.28 ratio, a fixed layout grammar, a fixed number of hierarchy levels, or generic brand decoration |
| `off` | The user explicitly says not to apply ArcheBase VI guidance, or the work is not intended to be ArcheBase-branded | Stays out of visual direction and reports only ordinary task results | Does not silently claim brand compliance or approve official brand use |

## Hard boundaries in every non-off mode

These are not style preferences and are never relaxed:

- Never redraw, generate, distort, recolor, or silently modify an official Logo. If a Logo is used, resolve and place the supplied V2 asset.
- Never generate a Logo or wordmark inside an AI-generated image. Place the approved asset afterwards when the selected mode calls for one.
- Do not publish unlicensed imagery, faces, customer material, third-party marks or confidential data.
- Do not present an unsupported customer claim, metric or product capability as fact.
- Do not imply that a creative artifact passed strict VI approval when it was produced in `guided` or `creative` mode.
- Human approval remains required for external publication; the mode changes the kind of review, not the ownership of the decision.

## Creative latitude

In `guided` and `creative` modes, the following may intentionally depart from the Guide when the channel or audience benefits:

- composition, crop, pacing, motion, texture, illustration style and visual metaphor;
- platform-native type scale and caption treatment;
- campaign-specific color extension, provided it is not presented as an official token or system color;
- playful, editorial or culturally specific art direction;
- a decision not to show the Logo, when the asset is not claiming to be an official lockup or formal company identity.

Record an intentional departure only when it affects review or future reuse. Use `templates/decision-record.md` with `Mode: guided | creative`, `Departure`, `Why the channel benefits`, and `Owner`.

## Mode selection algorithm

1. Honor an explicit user mode.
2. If the user says "official", "on-brand", "follow the VI Guide", "strict brand compliance", or the artifact is a formal external company asset, use `strict`.
3. If the user asks for a social, campaign, event, editorial or experimental artifact and does not ask for strict compliance, use `creative` or offer it as the recommended mode.
4. Otherwise use `guided` for ArcheBase-branded work.
5. If the user says not to apply the brand guide, use `off`; do not keep applying soft style rules after that choice.

Always state the selected mode in the brief and final report. A mode can be changed mid-task; record the change and re-run only the gates affected by the new mode.

## Gate behavior by mode

- `strict`: unresolved asset, type, color-role, naming, claims/rights or export issues can block release.
- `guided`: hard-boundary failures block; soft visual deviations become findings with severity and an owner, not automatic blockers.
- `creative`: hard-boundary failures block; intentional visual departures are accepted when recorded and reviewed for channel fit.
- `off`: do not issue a VI release verdict. Return `VI guidance not applied` and avoid implying approval.
