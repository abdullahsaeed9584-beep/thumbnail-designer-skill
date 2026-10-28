# Glow, Light and the Premium Insight Look

The single biggest gap between a competent composite and a top-tier one is **where the light
comes from**. Amateur work adds a glow *behind* the subject as decoration. Premium work puts a
**light source inside the frame** and lets it spill onto everything.

---

## 1. Motivated glow (the core technique)

**Rule: every glow must have a visible source in the picture.**

A glowing candlestick, a waveform, a laptop screen, a phone, a neon sign, a ring light, a
portal. The viewer can point at what is emitting the light. Then that light behaves physically:

| It must touch | How |
|---|---|
| **The subject** | The side facing the source is tinted and brightened in the source's hue. Hands nearest it glow most. |
| **The background** | A soft pool of the same hue, falling off with distance (inverse square - fast at first, then slow). |
| **The type** | The headline nearest the source picks up a rim or a wash of it. A glow behind one word only. |
| **The air** | Light haze/bloom between source and camera. |

**Build order**
1. Place the source object. Give it a **three-stop core**: near-white centre → saturated hue →
   transparent. A flat single-colour shape never reads as emitting.
2. `blur` a copy of the source shape behind itself at 2-4x size for the bloom.
3. Add the spill onto the subject: a soft-light or screen layer in the source hue, masked to the
   side of the subject that faces the source.
4. Darken everything *away* from the source. Contrast is what sells brightness - you cannot make
   something look bright without making its surroundings dark.

**The decorative-halo mistake:** a ring or disc floating behind someone's head with no source.
It reads as a sticker. If there is no source object, there should be no coloured glow - use a
plain rim light from the key instead.

---

## 2. Selective desaturation (what makes the colour hit)

Look at any premium analysis thumbnail: the people are **black and white or near-mono**, and the
only saturated colour in the frame is the glowing element.

- Subject and background: desaturate 70-100%, keep strong local contrast and detail.
- Light source and its spill: full saturation.
- Result: the eye is physically unable to look anywhere else.

Use this whenever the message is an insight, a comparison or a data point. Keep full colour only
when the subject's own colour *is* the story (food, product, travel, fashion).

**Two-source variant:** two subjects facing each other, each lit by a different hue (blue vs
orange, blue vs red), with a thin bright seam between them. Instant comparison framing.

---

## 3. Premium type treatment

This tier does **not** use the heavy stroke-and-extrude of the creator register. It uses:

- **Mixed case, not all caps.** "One Big Gap", "Rhythmic Variability", "Kill vs. Scale",
  "Steve's Fluency". Caps are reserved for one short shouted word.
- Heavy neo-grotesque or geometric sans at **600-800 weight** - Inter Display, Montserrat,
  Poppins, Archivo. Not Anton, not Impact.
- **Silver gradient fill** (white → #B9C0CB) with a soft dark drop shadow. No black stroke.
- **Tight tracking** (-2% to -4%) and line-height 0.95-1.05.
- **Set behind the subject** so the subject masks part of it - the type lives in the scene.
- One word carries the accent: a glow, a coloured bar behind it, or the source's hue.

---

## 4. The annotation layer

The "analyst marking up evidence" layer. Used sparingly it signals insight; overused it is noise.

- **Thin white curved arrow** with a soft drop shadow, pointing from the claim to the proof.
  Hand-drawn feel, tapered, 4-8px, never a clip-art arrow.
- **Hand-drawn red ellipse** circling the key number or word. Slightly irregular, open-ended.
- **Red or yellow underline** under one word, drawn like a marker stroke.
- **Small pill labels** - white or red rounded rect, 1-3 words, for naming a part of the picture.
- Maximum **two** annotation marks per thumbnail.

---

## 5. Props that carry words

Physical objects holding the message beat floating text: a blindfold reading THEORY, a held
book, a clipboard checklist, a phone screen, a sign. The word becomes part of the scene, which
is both more believable and more memorable.

---

## 6. Stylised data, never fake data

Charts, candlesticks and waveforms in this register are **illustrations**: oversized, glowing,
simplified, obviously stylised. That is honest - nobody reads them as a real screenshot.

What stays banned: a realistic-looking analytics screenshot, dashboard or balance with invented
numbers, or any chart captioned as the creator's actual results when it is not. Stylised and
unlabelled is fine; realistic and fabricated is not. See `niche-guide.md`.

---

## 7. Density - the mistake that makes all of the above look cheap

Every rule above can be followed exactly and still produce something empty: one portrait, one
glowing shape, and a large field of black. Austere is not premium.

The expensive-looking references are **dense**. A real place behind the subject - a studio, a
blackboard, a trading floor, a street. Real objects with real texture. A light source that is
a *meaningful thing* (a candlestick chart, an equaliser, a screen), never a featureless bar.

- **Put a real environment photograph behind everything.** A gradient is not a place. Blur it
  8-12px and dim it to 0.7-0.85 - dim it further and the room becomes a smear, which defeats
  the point.
- **Keep colour.** Desaturate the subject 20-40%, not 95%. Pushing to full mono only works when
  there is a strong scene and a vivid source to carry the frame; on a plain portrait it just
  drains the picture.
- **Give the source structure.** 16 candlesticks with wicks, 30 equaliser bars, a plotted line -
  many elements, not one rectangle. Detail is what makes it read as an object rather than a UI
  chrome element.
- **Blend the subject with a mask**, feathering its own edge into the scene. An overlaid dark
  band is not a blend; it is a dark band.
- If a large area carries nothing, the design is not finished.
- **The subject has to belong to the scene.** A sunlit outdoor portrait dropped into a dark
  club reads as fake instantly, however good the glow is - the light direction and colour
  temperature give it away. Match them, or pick a different photo. `DIM` and `MONO` can pull a
  bright studio portrait down into a dark room, but they cannot move the sun.
- **Give the source enough weight.** A 2-3px plotted line is a squiggle at thumbnail scale,
  not a light source. Stroke it at 6px+ with a double drop-shadow, or use candlesticks or
  bars where structure does the work.

Template: `scene.html`.

## Checklist for this look

- [ ] Can I point at the thing emitting the light?
- [ ] Does its colour appear on the subject, the background AND the type?
- [ ] Is everything away from the source actually dark?
- [ ] Is the subject desaturated so the accent is the only colour?
- [ ] Is the headline mixed case, silver, soft-shadowed - and masked behind the subject?
- [ ] Two annotation marks at most?
- [ ] Is any data stylised rather than pretending to be a real screenshot?
- [ ] Is there a real PLACE behind the subject, not a gradient?
- [ ] Does the source have structure - many elements, not one shape?
- [ ] Is any large area of the frame carrying nothing?
