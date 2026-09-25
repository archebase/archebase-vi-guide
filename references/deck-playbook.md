# Deck playbook

Load with the shared `pptx` skill. Keep responsibilities separate: this playbook decides brand composition; `pptx` owns OOXML and file mechanics.

1. Fill `templates/brief.md` and create slide inventory: number, purpose, one judgment, evidence, recipe, background, logo asset, open approval.
2. Classify slides as system statement, evidence-led, transformation flow, comparison, or image-led.
3. Use 16:9 unless specified; vary layouts; every slide needs meaningful evidence or structure.
4. Use the Guide's explicit color evidence when choosing the overall palette: `AB_BLUE_1` 50%, `AB_BLUE_2` 25%, `AB_BLUE_3` 10%, `AB_BLUE_4` 5% (90% labelled total, p.28–29). The remaining 10% is not assigned in the Guide; do not turn the ratio into a per-slide component allocation without a separate decision.
5. Select current SVG logo through the resolver; use PNG only when raster output requires it.
6. Use native charts where PowerPoint supports them. Titles state conclusions; include units, time, sample and source.
7. Run the shared `pptx` content QA, validator, rendered visual QA and thumbnail grid. Fix overflow, overlap, low contrast and repetitive layouts.
8. Report technical file QA separately from brand QA. Unconfirmed logo geometry, type sizing, semantic color-role allocation, or naming blocks release.
