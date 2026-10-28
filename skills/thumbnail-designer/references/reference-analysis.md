# Reference Analysis — reading what the user actually meant

A reference image is an instruction the user could not put into words. The job is to work
out *which* instruction it is, because "like this" means something different every time:
sometimes the layout, sometimes only the mood, sometimes the exact shade of one colour.

Guessing wrong wastes the whole build. One sentence stating what you read it as costs
nothing and lets the user correct you immediately.

---

## 1. Read the image in this order

Work down. Earlier items are structural and survive any change of subject; later ones are
surface and are often the only thing the user actually wants.

1. **Format** — ratio, orientation, where it was meant to be seen
2. **Composition** — where the subject sits, the division of the frame, the eye path
3. **Scale** — how much of the frame the subject occupies; headroom; crop point
4. **Depth** — how many planes, what is sharp, what is blurred
5. **Light** — direction, hardness, colour temperature, where the source is
6. **Palette** — the two or three structural colours and the one accent
7. **Treatment** — grade, grain, saturation, contrast curve
8. **Type** — face, weight, case, size relative to frame, position, hierarchy, effects
9. **Graphics** — shapes, rules, badges, arrows, their weight and restraint
10. **Mood** — what the whole thing is trying to make you feel

Write the read as a short list, not an essay. Three lines is usually enough.

---

## 2. Decide the role of each element

For everything you listed, pick exactly one:

| Role | Meaning |
|---|---|
| **Preserve** | reproduce closely — the user asked for this specifically |
| **Recreate** | same structure, our own content |
| **Replace** | the reference has it, ours will differ |
| **Inspire** | take the principle, not the execution |
| **Ignore** | present in the reference, irrelevant to the brief |

The default for an unqualified "make it like this" is: **composition, light and palette
recreate; subject, text and brand replace; everything else inspire.** That reading is
nearly always right, and stating it gives the user one obvious place to push back.

**"Exact match"** means mirror layout, scale, palette, light and type treatment. It never
means copy the reference's logo, watermark, photography, illustration or any other
proprietary asset — those are Replace, always.

---

## 3. Several references at once

Do not average them. Averaging four references produces something that resembles none of
them and has no structure at all.

Assign each reference a **job**, then say so:

> "Taking the layout from the first, the lighting and palette from the third, and the
> type treatment from the fourth. The second reads as mood only."

If two references conflict on the same element — one centred, one hard left — that is one
of the few cases worth a question, because no assumption makes the other reference useful.

When the user supplies **both a reference and a photo of a person**, the roles are fixed
and not negotiable: **the photo is identity truth, the reference is design direction
only.** Adapt the layout to the pose that exists. Never bend a pose, a face or a body to
match a reference. See `cases.md §E` and `identity-protocol.md`.

---

## 4. What must not change

Elements the user supplied are evidence, not raw material. Unless they explicitly ask:

- **Faces and hair** — `identity-protocol.md`, mandatory
- **Logos and brand assets** — no stretching, recolouring, redrawing
- **Product shape, colour and branding** — `commerce.md`
- **Supplied wording, numbers, prices, phone numbers, addresses** — character for
  character, verified on the rendered pixels
- **Anything they named as "keep this"** — including things that look like mistakes.
  Ask once if it looks like an error; do not silently fix it.

---

## 5. When the reference cannot be matched

Say which part and why, then offer the nearest honest route. Common cases:

- The reference used a **studio photograph** we do not have → use the user's own photo, or
  real stock (`fetch_stock.py`), and accept a different composition.
- The reference used a **cut-out subject with perfect hair edges** → use `photo-split.html`
  or `scene.html`, which need no cutout at all.
- The reference used a **licensed typeface** → name the closest licence-safe face and say
  it is a substitute.
- The reference used **generative imagery** → there is no image model here.
- The reference's subject is a **real person who is not the user** → licence is not a
  model release; refuse the commercial use, not the whole job.

---

## 6. Competitor and style analysis

When the user supplies a set to analyse rather than to copy (`cases.md §O`): report the
common palettes, layouts, text length, face usage and recurring devices — then the gap
worth exploiting. The deliverable is differentiation, not conformity. Never reproduce
branded assets from the set.

---

## 7. Checks

- [ ] Stated in one line what you read the reference as asking for
- [ ] Every supplied reference has a named job; none was silently averaged in
- [ ] Nothing proprietary copied — logos, watermarks, photographs, illustrations
- [ ] Supplied faces, products, logos and wording unchanged
- [ ] Compared the finished build against the reference **and** against the source photo
- [ ] Named anything you could not match, and what you did instead

Related: `cases.md §D–F`, `identity-protocol.md`, `style-registers.md`, `commerce.md`.
