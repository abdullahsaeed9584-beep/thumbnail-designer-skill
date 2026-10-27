# Composition, Typography, Graphics, Finish

Quality bar: `premium-standard.md`. Wording: `hooks.md`. This file is the craft detail.

## Composition
One idea, one focal point. Rule of thirds or a deliberate strong centre. Face large and clear when person-led. Gaze toward the text or the object you want read second. Real negative space for the headline. Never crowd.

**Eye-flow default (LTR):** hook upper-left, subject right — the natural Z-path. **Mirror it for Urdu/RTL:** hook on the right, subject left. Reading order and visual order must agree.

**Three depth layers, always:** background (scene) / midground (subject) / foreground (one or two blurred edge elements). Two layers looks pasted.

Keep key content out of the YouTube duration badge zone (bottom-right ~12% w × 12% h) and ≥4% from every edge.

**Layout picks**
- person-led — face ≥35% of canvas height, one clear emotion, catchlights in the eyes
- product-led — recognisable at 168 px, flattering angle, one callout maximum
- data — ONE chart or indicator, big; no tiny numbers; never pass illustration as real data
- comparison — balanced two parts, clear divider, legible labels, red vs green or warm vs cool
- transformation — real before/after, or clearly labelled as illustrative
- story/mystery — focal object + 1-2 clues, heavier vignette, withheld information
- text-hero — no subject available: type *is* the subject, 2-3 words at huge scale, one accent
- none dominant — pick the clearest concept; don't auto-insert a person

## Headline
3-5 words max, 2-4 ideal. Complements the title, never repeats it. Curiosity, claim or contrast — honest. User wording is final; "no text" means a text-free design. Verify spelling and numbers on the rendered pixels. Never invent stats, quotes or prices. Patterns: `hooks.md`.

## Typography
- One main face, one optional secondary. Max 2 fonts total.
- Licence-safe display faces (`scripts/fetch_fonts.py`): Anton, Bebas Neue, Archivo Black, Montserrat ExtraBold/Black, Poppins ExtraBold, Oswald, Teko, Barlow Condensed ExtraBold, Inter Black. Impact / Gilroy Heavy / Akira Expanded only with a licence.
- **Exactly one highlighted keyword** — accent colour *or* larger scale, not both plus a box.
- **Modern styling:** subtle vertical gradient fill (silver→white `#FFFFFF`→`#BFC7D2`, gold→yellow `#FFD76E`→`#F2A20C`), soft drop shadow, and a dark glow behind the glyphs for separation. Prefer this to a hard black stroke; add a stroke only when contrast genuinely requires it.
- **Depth trick:** place the text layer *under* the subject layer so the subject masks a corner of it (`composite.py --text-layer`). Reads as one photograph, not an overlay.
- Contrast ≥4.5:1 against the real pixels behind the glyphs — `contrast_check.py --box`, not a guess.
- Tight tracking on heavy caps (-1% to -3%), line-height 0.92-1.0 for stacked display lines.
- Max 2 text effects. Never distort, stretch, skew or arch type to fit — resize the type or cut a word.

## Urdu / RTL
- Fonts: Noto Nastaliq Urdu, Noto Naskh Arabic, Lateef (`fetch_fonts.py --urdu`). Jameel Noori Nastaleeq only if the user holds a licence.
- **Safest route:** HTML/CSS in headless Chromium (`direction: rtl; font-family: 'Noto Nastaliq Urdu'`) → transparent PNG → composite. `render_html.py --transparent`.
- PIL route: `arabic_reshaper` + `python-bidi`, `ImageFont` with RAQM layout if available.
- Nastaliq needs line-height ≥1.8 and real descender room — it drops diagonally; a tight box clips it.
- 2-3 words maximum: the script is detailed and dies first at 168 px.
- Check on the rendered image: joins, ligatures, word order, dots and diacritics not clipped, and bidi order where Urdu mixes with English or digits.

## Graphic cues
Arrows, rings, underlines, badges, icons, charts, panels, callouts, number markers: **max 2-3**, and only if they direct attention or add information. One style throughout — all flat or all 3D, never mixed. Align to the layout grid; even padding. No random stickers. Logos exact and secondary to the message.

## Finish (restraint)
Depth of field, subtle grain, vignette, bloom, haze, radial light, local contrast — see `retouch-color.md` and `scripts/finish.py`. The face and the headline always stay sharp. No fake lens flares, no HDR halos, no particle spam, no uniform outer glow on everything.

## Honest clickability
One clear idea · focal contrast · emotion relevant to the actual video · a visual question or conflict · image and headline working as one sentence. No guaranteed-CTR claims, no misleading imagery. Retention beats clicks: a thumbnail that oversells costs more than it earns.
