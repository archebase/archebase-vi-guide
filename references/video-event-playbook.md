# Video and event-screen playbook

Load with `references/visual-grammar.md`, `references/logo-asset-resolver.md` and `references/guide-page-evidence.md`.

This playbook owns brand composition for video, film and large-format event screens. It does not own editing, encoding or playback hardware.

## 1. Brief

Fill `templates/brief.md`. A video or event brief must add:

- the playback surface and its native resolution,
- the **viewing distance** and the realistic worst-case distance,
- the aspect ratio and the safe area for the venue,
- the frame/scene inventory: one row per scene with its single primary judgment,
- whether audio carries part of the message, and whether captions are required.

Viewing distance is the controlling input for every size decision. An asset that works on a laptop fails on a 12-metre LED wall and vice versa; do not reuse one for the other without re-checking.

## 2. Evidence to inspect

| Guide pages | What to take from them |
|---|---|
| 37–46 | Application boards: composition, image treatment and scale. Inspect rendered pages. |
| 6–21 | Type specimens and language pairing — relevant when on-screen type is or contains the Identity. |
| 22–25 | Identity placement, clear space, orientation and combination restrictions. |
| 29–32 | Color and neutral values. |

Record one `templates/page-inspection-record.md` per page used.

## 3. Legibility and safe area

- Size on-screen type and the mark for the **worst-case** viewing distance in the brief, not the best seat.
- Keep the mark and all critical text inside the venue safe area. Projection, LED processing and overscan can each crop differently; record the value used and its source.
- Check contrast on the actual screen or a calibrated preview. A color that reads well on a monitor can disappear on a bright stage LED.
- Do not place the mark on a moving or high-detail passage. Choose the variant through the resolver rather than adding an outline or shadow to force contrast.
- State the conclusion before the metadata, and keep no more than three hierarchy levels per scene.

## 4. Motion

- Motion must explain the claim, not decorate it. Justified: data flow, process step, transformation, camera move that reveals real evidence.
- Remove random node animation, glow, particle fields, decorative wipes and unrelated transition families.
- Give any text that carries a claim enough hold time to be read at the briefed distance. Do not animate a headline in while the previous one is still on screen.
- Keep the mark static or at least stable. An animated or morphing logo is a recreation of the mark and is not permitted.

## 5. Audio and captions

- If a claim is carried by audio, it also needs a visual carrier so the message survives a muted screen.
- Captions and lower-thirds inherit the same typography and color discipline as the rest of the asset.
- Do not overlay text on a passage so detailed that it becomes unreadable; change the edit instead.

## 6. QA before release

- Review at the actual playback surface or the closest available equivalent, at the briefed distance.
- Watch the full piece once at speed and once frame-stepped over every text-bearing moment.
- Check crop on every aspect ratio in scope, including the venue's.
- Check audio levels against the venue spec, if one exists.
- Run `checklists/video-event.md`, then the four gates in `references/release-gates.md`.

## 待确认

- Venue safe areas and minimum on-screen type sizes are not in the Guide; record the source of whatever value is used.
- Logo clear space and minimum size at large format.
- Whether the mark may animate at all, and if so which approved motion exists.
- Whether `WISDOM BUILDS INTELLIGENCE` or `Powered by` may appear in motion graphics, and at what scale.
