# The Premium Standard

The quality bar for every build. Numbers are defaults, not dogma — but if you deviate, you must be able to say why.

## 0. The one-sentence test
Before touching pixels, finish this sentence: **"This thumbnail makes someone feel ___ and wonder ___ within 3 seconds."**
If you can't, the concept isn't ready. One thumbnail = one idea (curiosity, emotion, or result). It complements the title; it never repeats it.

## 1. The Rule of 3 — never more than three core elements
1. **Main subject** (person or object)
2. **Short text hook** (2-5 words)
3. **Story-driven background**
Everything else is support. A fourth competing element is clutter, not value.

## 2. Visual hierarchy & eye flow
- Eye path must be deliberate: **subject → text → detail**. Nothing else gets attention.
- Default western layout: **hook top-left / upper-third, subject right** (natural Z-pattern). Mirror it for RTL (Urdu) audiences: hook on the right.
- Rule of thirds or a strong deliberate centre. Focal point on an intersection, not dead centre by accident.
- Real negative space around the headline. Crowding reads as cheap.
- **Three depth layers always**: foreground / midground / background. A flat two-layer design looks pasted.

## 3. Safe zones
- ≥4% clear margin on every edge.
- **YouTube: keep the bottom-right 12% × 12% completely clear** (duration badge).
- Vertical formats: nothing important in the top 10%, bottom 20%, or right 15% (action rail).
- Grid previews may re-crop to 1:1 / 3:4 / 4:5 — the focal point survives a centre crop.

## 4. Subject
- Face: close, large (**≥35% of canvas height**), one strong unambiguous emotion.
- Eyes toward camera, or toward the text/object you want read next. **Bright catchlights in the eyes** — a dead eye kills the whole frame.
- Cutout: clean edge, smooth but not mushy, **no halo**, no colour spill from the old background. See `identity-protocol.md`.
- Product: high-res, sharp, flattering angle, recognisable at 168 px.

## 5. Lighting, blending, realism
- **Rim light / edge glow**: bright highlight along the subject's edge, keyed to the background light source (neon cyan, electric blue, gold, red). This is the single biggest "pro vs amateur" tell. Gradient *behind* the mask edge — never a painted outline over hair strands.
- **One key light direction across every element.** Conflicting shadows read as fake instantly.
- **Ambient occlusion**: a dark contact shadow directly under/behind the subject and objects so they sit in the scene; plus a soft cast shadow. Grounded, not floating, not pasted.
- **Colour match**: pull foreground skin tones and shadows toward the environment with curves/levels/colour balance. Unmatched black points are why composites look wrong.

## 6. Depth of field (the 3D cinematic look)
- Background blur **15-30%** (Gaussian or lens blur) to push subject and text forward. Never blur the face or the headline.
- **Foreground depth**: slightly out-of-focus elements at the extreme frame edges — sparks, smoke, particles, cash, glowing shards, bokeh. 1-2 only, at low opacity.
- **Vignette**: darken the four corners **8-15%** to drive the eye to the focal point.

## 7. Typography
- **2-4 words. 5 absolute maximum.** Never the video title verbatim.
- Heavy sans-serif: Anton, Bebas Neue, Montserrat Black/ExtraBold, Poppins ExtraBold, Archivo Black, Oswald, Inter Black. (Impact/Gilroy/Akira only if licensed.)
- **Max 2 fonts. Exactly 1 highlighted keyword** — accent colour or scale, not both plus a box.
- Modern styling: **subtle vertical gradient fill** (silver→white, gold→yellow) + soft drop shadow + a dark glow behind the glyphs. Prefer this over a harsh black stroke; use a stroke only when contrast genuinely demands it.
- **Mask the text slightly behind the subject** (text layer under subject layer) for real depth.
- Contrast ≥4.5:1 against the actual pixels behind it (not the nominal background) — verify with `contrast_check.py --box`.
- Max 2 text effects total. Never distort, stretch or arch type to fit.

## 8. Colour
- **2-3 colours + 1 accent.** That's the whole palette.
- High subject/background separation. Complementary pairs that work: blue/orange, purple/yellow, teal/red, yellow/black (warning, mystery), red vs green (comparison).
- **Controlled saturation**: boost on the focal point (face, arrow, hero object); hold the background slightly desaturated. Never global saturation slam.
- Natural skin tone is non-negotiable. Brand colours exact when a kit exists.

## 9. Graphic cues
- Arrows, rings, underlines, badges, icons: **max 2-3, and only to direct attention or add information.**
- One icon style throughout — all flat or all 3D, never mixed.
- Glowing arrows, circles around a detail, blurred "secret" objects, split-screen before/after: use to open a curiosity gap, not to decorate.
- Logos and badges clean, aligned, unmodified, secondary to the message.

## 10. Final mastering
Merge visible layers, then one finishing pass (`scripts/finish.py`):
- Texture / local contrast **+10 to +20**
- Clarity and a final **unsharp mask** — face and text stay crisp
- **Monochromatic grain 2-3%** to bind every layer into one photographic image
- Edge cleanup, layer colour match, no clipped highlights or crushed blacks
This is what turns "a composite" into "a cinematic poster".

## 11. The proof tests — run them, don't imagine them
`python scripts/thumb_test.py out.jpg` renders all four:
1. **Mobile (~168 px)** — is the subject, the emotion and the hook still legible?
2. **Grayscale** — does it hold up on luminance alone? If not, your contrast is colour-dependent and will fail.
3. **Squint / blur** — is there exactly one focal point?
4. **Feed mock** — does it stand out beside neighbours, or blend in?
Plus: compare against real competitor thumbnails in the niche. Ship 2 variants and A/B when the user can.

## 12. Never ship
Too much text · more than 3 colours · low-res or upscaled-mush source · clickbait the video doesn't deliver · crowded layout · tiny type · weak contrast · over-saturation · cheap uniform outer glow · fake lens flares · HDR halo look · particle spam · plastic skin · misaligned or unevenly padded elements · drop shadows with no light source · a style that doesn't match the rest of the channel.
