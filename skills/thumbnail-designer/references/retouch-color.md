# Retouch, Colour, Cutout, Lighting, Compositing

## Retouch (natural, selective)
Exposure, white balance, highlight/shadow recovery, colour-cast removal, honest skin-tone correction, dust and spot cleanup, background distraction cleanup, noise reduction, mild sharpening. Blemish or object removal only when asked. Keep pores, lines and texture. Never: plastic skin, heavy clarity on faces, skin whitening, oversharpened edges, beauty filters.

## Grade
Evaluate the image first, then choose levers: exposure, contrast curve, white balance, highlights/shadows, black point, vibrance (over saturation), selective hue, split tone, subject/background separation, subtle vignette, local dodge and burn, restrained bloom. Protect skin tones. No clipped highlights, no crushed blacks, no neon overdose.

**Controlled saturation:** lift saturation on the focal point (face, arrow, hero object) and hold the background 10-20% *down*. A global saturation boost is the fastest way to look cheap.

Palette starters (not rules): finance navy/charcoal/gold - tech cool blue/cyan - fitness high-contrast + one bold accent - real estate clean white/blue/warm - documentary cinematic shadows - education clean and high-clarity - urgency controlled red/orange.
Complementary pairs that hold at 168 px: blue/orange - purple/yellow - teal/red - yellow/black - red vs green (comparison only).

## Cutout
Order of preference: existing alpha from a user PNG, then `rembg` (if the model downloads), then OpenCV GrabCut (rough; warn about hair). Inspect the edge at 300%. Never paint or generate hair to "fix" it - see `identity-protocol.md`.
Edge decontamination: erode the mask 1 px, feather 1-2 px, shift edge colour toward the new background tone.

## Lighting
- **One key direction for every element.** Conflicting shadows are the number one fake tell.
- **Rim light** is the premium signature: a coloured, blurred glow *behind* the mask edge, keyed to the background light source. `composite.py --rim "#00E5FF" --rim-width 6 --rim-dir right`. Never a painted outline over strands.
- **Ambient occlusion:** a tight, dark contact shadow where the subject meets the ground or backdrop, plus a wider soft cast shadow offset along the light direction. `composite.py --shadow 0.55 --shadow-blur 28`.
- Fill light to keep shadow detail; falloff so the background darkens away from the key.
- No blown highlights on the face.

## Background
Supports the subject, never competes. Match perspective, scale, light direction, colour temperature and depth. Options: gradient, studio sweep, cinematic scene, geometric, texture, themed location. Generated or stock backgrounds always go *behind* the protected subject, never over it.
Depth recipe: blur 15-30%, desaturate ~12%, darken corners 8-15% (`composite.py --bg-blur 22 --bg-desat 12`).

## Compositing
Foreground / midground / background. Match scale, perspective, colour and black point; integrate the shadow; blend the edge; set the focus hierarchy. **Colour match** pulls the subject's mean toward the background (`composite.py --match 0.3`) - this is what kills the pasted-on look.

## Code recipes (Pillow / numpy / OpenCV)
- Contrast: `ImageEnhance.Contrast` in small steps (1.05-1.15) or a LUT curve.
- Local contrast / texture: `ImageFilter.UnsharpMask(radius=width//120, percent=clarity*5)`.
- Vignette: radial gradient multiply, max 15%.
- Subject/bg separation: slight blur + darken + desaturate on the background, warm/cool contrast between the two.
- Soft shadow: blur the alpha, offset, multiply under the subject.
- Grain: monochromatic gaussian noise at 2-3% - the final cohesion step.
`scripts/finish.py` implements all of the above; prefer it to hand-rolling.
