# Style Registers

A thumbnail is not one aesthetic. Pick the register from the audience and the niche, then
follow its craft rules. Mixing registers is what makes work look amateur - commit to one.

| Register | Reads as | Use for |
|---|---|---|
| **A. Creator High-Impact** | loud, saturated, maximum stopping power | YouTube creators, gigs/services, gaming, reactions, finance hype, tutorials, most of the open feed |
| **B. Cinematic Editorial** | restrained, moody, expensive | documentary, long-form, business, tech, premium brands, interviews |
| **C. Clean Corporate** | calm, trustworthy, legible | B2B, SaaS, education, medical, LinkedIn, course platforms |
| **D. Premium Insight** | expensive, analytical, cinematic | the top tier of creator work: finance, psychology, business breakdowns, documentaries, case studies, premium ads and posters |

Default for a general YouTube creator request is **A**. Default for a brand, agency or B2B
request is **B** or **C**. When the user supplies reference thumbnails, match their register.

---

## A. Creator High-Impact — the recipe

This is the dominant look in YouTube search and the gig marketplaces. It is a real craft with
specific rules, not "just make it loud".

### Type (the single biggest tell)
- **2-3 stacked lines, each with a different role**: small label line → hero word → accent word.
- **Per-line colour roles**: white for the neutral line, one saturated accent (yellow `#FFD400`,
  red `#FF2A2A`, orange gradient) for the payload word. Never colour every line.
- **Heavy outline**: black stroke 8-16px with `paint-order: stroke fill` so the stroke sits
  behind the glyph. A second thin white stroke outside the black reads as a sticker.
- **3D extrude**: stacked offset shadows in a darker shade of the fill, 6-16px down, hard edges
  (no blur). This is what separates the look from flat type.
- **One line rotated** -2° to -4°, or set on an angled colour bar. One, not all.
- Condensed ultra-heavy faces: Anton, Archivo Black, Bebas Neue, Poppins Black.
- Still **3-5 words total**. Loud does not mean long.

### Background
- Saturated field, not a photo: red, purple→pink, cyan→blue, yellow→orange.
- One texture on top: **sunburst rays**, **halftone dots**, or a **perspective grid**.
- Heavy corner vignette so the centre pops.
- Optional bokeh sparkles at the edges.

### Subject
- Cut-out person at one side, **high contrast, hard white or coloured rim light**, hard drop
  shadow plus a coloured glow pad behind them.
- Expression is big and unambiguous: shock, delight, disbelief.
- **Pointing or gesturing toward the text** is the signature move - it hands the eye to the hook.
- Identity rules still apply in full (`identity-protocol.md`). Loud styling never licenses
  reshaping a face.

### Props
- 2-4 only: play buttons, growth arrows, coins/cash, badges, subscribe buttons, emoji.
- Rotate each 6-15°, give each a hard shadow, scatter them to the edges and corners.
- One style throughout - all 3D or all flat.
- They point at or frame the subject and hook. Never fill empty space with them.

### Colour
- 2 dominant + 1 accent, pushed to high saturation. Complementary pairs: red/cyan,
  purple/yellow, blue/orange, green/magenta.
- Subject stays colour-correct - the background carries the saturation, not skin.

### What this register still does NOT do
- Fabricated performance numbers presented as real: fake CTR figures, fake view counts, fake
  analytics screenshots, fake earnings. A seller's own offer claim ("I design thumbnails") is
  theirs to make; invented data is not.
- Emoji spam, four-plus competing colours, blurry upscaled cut-outs, text over the face,
  anything in the duration-badge corner, or a promise the video does not pay off.
- Loud is a style. Dishonest is a defect.

Template: `assets/templates/creator-impact.html`.

---

## D. Premium Insight - the recipe

The look of the best-paid creator design. Three things define it, and all three must be present:

1. **A light source inside the frame.** A glowing candlestick, waveform, screen, orb or sign -
   and its colour lands on the subject, the background and the headline. Never a decorative
   halo with no source.
2. **Selective desaturation.** People and background pushed to black and white; the only
   saturated colour in the frame is the source and its spill. This is what makes the accent hit.
3. **Refined mixed-case type.** "One Big Gap", "Rhythmic Variability" - heavy neo-grotesque at
   600-800 weight, silver gradient, soft shadow, set behind the subject. **No stroke, no 3D
   extrude** - that is register A, and mixing the two looks cheap.

Plus, sparingly: a thin white hand-drawn arrow from claim to proof, a red hand-drawn ellipse
round the key word, small white or red pill labels. Two marks maximum.

Full doctrine and build order: `glow-and-light.md`.  Templates: `insight.html`, and
`photo-split.html` with `GLOW`.


## B. Cinematic Editorial — the recipe
Dark base, one restrained accent, blurred photographic or gradient background, rim light keyed
to the key light, contact shadow, 15-30% depth-of-field, silver or gold gradient type with a
soft dark glow instead of a hard stroke, 2-3% grain. Negative space is the point.
Templates: `person-led.html`, `text-hero.html`, `service-device.html`.
Full detail: `premium-standard.md`.

## C. Clean Corporate — the recipe
Light or single-colour ground, generous margins, one photograph or device, no texture, no glow,
type in a single weight pair with one accent colour, flat geometric shapes for structure, and a
logo given real clearance. Legibility and trust over drama.
Templates: `product-led.html`, `comparison.html`, `service-device.html` with a light `--base`.

---

## Choosing, in one line
Loud feed, creator, gig, gaming, reaction, hype → **A**.
Insight, analysis, comparison, "how this really works", premium brand -> **D**.
Brand, documentary, long-form, premium service → **B**.
B2B, education, medical, enterprise → **C**.
Reference supplied → whatever the reference is. Ask only if the references are mixed.
