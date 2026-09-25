# Web / UI checklist

- [ ] `templates/brief.md` filled with viewport sizes and a screen inventory
- [ ] One primary judgment per screen; conclusion stated before metadata
- [ ] Every color mapped to a semantic token; no color outside the token file
- [ ] p.28 labels recorded correctly: AB_BLUE_1 50%, AB_BLUE_2 25%, AB_BLUE_3 10%, AB_BLUE_4 5% (90% labelled; remaining 10% unassigned)
- [ ] Ratio is not incorrectly treated as a per-component allocation; unresolved semantic roles and the unassigned 10% are recorded as `待确认`
- [ ] No orange introduced as a CTA or status color
- [ ] Required states covered: default, hover, active, focus-visible, disabled, error, empty, loading
- [ ] Logo variant resolved through the resolver; SVG for web, `png-hires` for icon/avatar/favicon
- [ ] `白底` and transparent `png-hires` variants not substituted for one another
- [ ] Clear space and minimum size checked, or marked `待确认`
- [ ] Rendered at real viewport sizes and inspected; overflow, wrap, truncation, contrast and focus checked
- [ ] Dark mode checked if in scope
