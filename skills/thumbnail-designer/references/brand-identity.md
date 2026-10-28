# Brand Identity — logos, marks, systems

A thumbnail is judged in a feed. A logo is judged at 16px on a browser tab, embroidered
on a shirt, etched on glass, faxed in black and white, and on a billboard — often by the
same client in the same week. Design for the worst of those, not the best.

Routing note: `cases.md §G` is about **using a logo the client already has**. This file
is about **designing one**.

---

## 1. Before drawing anything

Four answers, from the user or inferred and stated:

1. **Name as written.** Exact spelling, capitalisation, any ampersand or accent.
2. **What the business actually does**, in one sentence of plain language.
3. **Who it has to beat.** A logo that looks like its three nearest competitors has failed
   at the one job that is purely functional: being told apart.
4. **Where it will live first.** A shopfront, an app icon, a van, a document footer.
   That decides whether the mark or the wordmark leads.

Do not ask about colour or font. Decide those, and say why in one line.

---

## 2. The forms, and when each is right

| Form | Use when | Risk |
|---|---|---|
| **Wordmark** (name only) | the name is short, distinctive, and must be read | nothing to use as an avatar |
| **Lettermark** (initials) | the name is long or generic | initials collide; check them |
| **Mark + wordmark lockup** | the default for most businesses | two things to get right |
| **Pictorial mark** | the thing is literal and ownable (a bird, a key) | cliché; search before committing |
| **Abstract mark** | the business is a service or a concept | meaningless unless the form is strong |
| **Emblem** (type inside a shape) | heritage, badges, food, trades | unreadable small; always needs a simplified variant |

---

## 3. Construction rules that decide whether it survives

**Build the mark as geometry, not as decoration.** Draw it on a grid of circles and
straight lines with a consistent corner radius and stroke weight. A mark made of
arbitrary curves cannot be redrawn, scaled or explained.

**Use a counter-shape, not two tones.** A two-colour mark collapses into a silhouette the
moment it is printed in one colour, embroidered, or engraved. Cut the shape *out* of the
container with `fill-rule="evenodd"` on a single path. Then the one-colour version is the
same path, and there is exactly one fill to change for any brand colour. This is the
single highest-leverage decision in the file.

**One path if you can.** Fewer elements means fewer things to go wrong in export, in
embroidery digitising and in a sign-maker's cutter.

**No gradients, no shadows, no filters in the master.** They rasterise in print RIPs and
in EPS export, and they are invisible at 16px. If the brand wants a gradient version,
that is a *variant* built from the flat master, never the other way round.

**Optical sizing in a lockup.** Set the mark at roughly 1.4–1.6× the cap height of the
type. Matching them mathematically makes the mark look undersized, because all-caps type
has no ascender or descender filling the measure.

**Clear space** is defined in terms of the logo itself — typically the mark's corner
radius or the width of one letter — so it scales with the logo instead of being a number
that stops making sense.

---

## 4. Type in a logo must be outlined

A logo delivered with live `<text>` is not a logo. Open it on a machine without the font
and the letterforms silently change — usually to Times — and nobody notices until it is
printed.

```
python scripts/text_to_paths.py --text "NORTHCAP" \
  --font assets/fonts/Montserrat-Variable.ttf --weight 800 \
  --tracking 0.04 --fill "#0E2A47" --out work/wordmark.svg
```

- **Instance variable fonts** at the weight you mean. Without `--weight` you get the
  default instance — usually Regular — and a wordmark that is quietly too light.
- The script applies advance widths and uniform tracking but **not GPOS kerning pairs**.
  Look at the result; fix specific pairs with `--kern "AV:-0.04"`.
- Licence: check the font permits use in a trademark. OFL fonts generally allow it;
  some commercial licences do not. Say which font was used, every time.

---

## 5. Prove it before calling it finished

```
python scripts/svg_check.py work/logo.svg --sheet work/proof.png --png-out dist/
```

`svg_check.py` fails the file for: not parsing, no `viewBox` (it cannot scale), or an
embedded raster (then it is not a vector logo). It warns for live text, for filters, and
for an extreme aspect ratio. Then it renders a contact sheet — **open it and look**:

- [ ] Legible at **16px**? If only the lockup fails, that is fine and expected — it is
      why the mark exists as a separate asset. If the *mark* fails, redraw it.
- [ ] **Solid black** version still reads as the same mark?
- [ ] **Knockout white** on dark still reads?
- [ ] **Greyscale** holds its contrast?
- [ ] Does it look like anyone else's? Say so if it does.

---

## 6. The identity pack

A logo delivery is a set, not a file:

1. `logo-lockup.svg` — horizontal, master
2. `logo-stacked.svg` — for square and narrow spaces
3. `logo-mark.svg` — the mark alone, for avatars and app icons
4. One-colour black and white versions (or a documented filter, if the mark is a knockout)
5. PNG exports at 64 / 256 / 1024 with transparency (`svg_check.py --png-out`)
6. Colour values: HEX, and the RGB/CMYK caveat from `print-production.md`
7. Typeface names, weights and where to get them
8. Clear space and minimum size, stated as a rule not a number
9. Misuse list: do not stretch, recolour, rotate, add effects, or put it on a busy photo

Save the system to `assets/brand-kits/<client>.md` so later work inherits it.

---

## 7. Hard lines

- **Never redraw a trademark** that belongs to someone else, or produce a logo that
  imitates an existing brand's mark closely enough to be mistaken for it.
- **Never claim a trademark search has been done.** Say that one is the user's next step.
- Do not invent a registration symbol. ® means registered; use it only if the user says so.
- A monogram built from someone's real initials is fine; a logo built from a real
  person's face or signature needs their permission — see `identity-protocol.md`.

Related: `deliverables.md`, `composition-type.md`, `print-production.md`, `motion.md`
(animated logo), `cases.md §G` (using a supplied logo).
