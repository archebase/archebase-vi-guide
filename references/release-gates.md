# Release gates

The gates are mode-aware. The purpose is to protect the organization without making every creative artifact behave like a formal identity system.

## Asset gate

In every non-off mode: official current Logo and correct variant when a Logo is used; no generated or modified Logo; image, face, customer and third-party rights. In `strict`, also check clear space/minimum size and approved font/license/weight. In `guided`/`creative`, a decision not to show the Logo is acceptable when the artifact is not claiming to be an official lockup.

## Design gate

In `strict`: one clear judgment; evidence dominates; approved tokens used semantically; actual-size readability; no overflow, low contrast, random decoration or generic AI wallpaper. In `guided`/`creative`: check readability and channel fit, but treat composition, crop, pacing, texture, campaign colors and platform-native style as adjustable; record intentional departures instead of blocking them.

## Claims/Rights gate

Every non-off mode: names, claims, metrics, units, time, sample and sources checked; no unsupported customer/product claims, confidential data, unlicensed media, or generated Logo/text. This gate is hard in every mode because it protects people, rights and factual integrity.

## Export/QA gate

Render at the actual channel size/distance/crop and inspect the result. In `strict`, run the full route checklist and technical/accessibility checks. In `guided`/`creative`, check the channel-specific risks and document accepted departures; do not claim strict VI compliance.

## Mode verdicts

- `strict`: unresolved asset, type, color-role, naming, claims/rights or export issues can block external release.
- `guided`: hard-boundary failures block; soft visual deviations become findings with owner/impact.
- `creative`: hard-boundary failures block; deliberate platform-native departures may pass after human review.
- `off`: do not issue a VI release verdict; return `VI guidance not applied`.

Verdict must be `可发布`, `修复后复审`, `阻塞，待确认`, or (only for `off`) `VI guidance not applied`.
