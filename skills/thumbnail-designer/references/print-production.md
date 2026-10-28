# Print Production — paper, packaging and signage

Screen work forgives. Print does not: there is no undo after 5,000 copies, and the
guillotine has a tolerance of about a millimetre either way. Everything in this file
exists because of that tolerance.

---

## 1. The three boxes, always

| Box | What it is | Rule |
|---|---|---|
| **Bleed** | artwork beyond the cut | **3 mm** per edge (5 mm for large format). Background art must actually reach it |
| **Trim** | where the knife lands | the finished size the client asked for |
| **Safe** | inside the trim | **5 mm** minimum. Nothing that matters — type, logos, faces, borders — outside it |

Two failures cause most reprints: artwork that stops at the trim (leaving a white sliver
down one edge), and type sitting 2 mm from the trim (trimmed off on some of the run).

**A full-bleed border is a trap.** A frame 4 mm from the edge will look 2 mm on one side
and 6 mm on the other. Either bleed it off or move it well inside.

```
python scripts/make_pdf.py assets/templates/print-page.html out.pdf \
  --trim A5 --bleed 3 --marks --proof out_proof.png --var HEADLINE="..."
```

`make_pdf.py` reads the `/MediaBox` back out of the finished PDF and fails if it is not
trim + bleed. `--proof` writes a raster to look at, because a PDF that nobody opened is
not a checked deliverable. Turn guides on with `--var GUIDES=1` for your own proof and
**never** in the file that goes to the printer.

---

## 2. Resolution and colour

- **300 DPI at final size.** A 1000px photo cannot fill an A4 page; at 300 DPI A4 needs
  2480×3508. Check the source image before planning the layout around it.
- **Large format is the exception.** A banner read from 3 m away is fine at 100–150 DPI;
  a billboard at 20–30. Designing a 6 m banner at 300 DPI produces a file nobody can open.
- **Design in sRGB; conversion is prepress.** `make_pdf.py` emits sRGB. Say so in the
  delivery note and let the printer convert with their own profile for their own stock.
- **Saturated RGB shifts.** Bright cyan, vivid green and neon orange have no CMYK
  equivalent and will come back duller. If the brand depends on one of those, warn the
  user and suggest a spot colour.
- **Rich black for large areas** (roughly C40 M30 Y30 K100 — the printer will specify);
  plain K100 for body text, or small type ends up fringed by misregistration.
- **Hairlines vanish.** Keep rules at 0.25 pt / 0.1 mm minimum.

---

## 3. Common pieces

| Piece | Trim | Notes |
|---|---|---|
| Business card | 85×55 mm (EU) / 88.9×50.8 mm (US) | 3 mm bleed; keep type 5 mm in; rounded corners need 5 mm safe |
| Flyer / leaflet | A5 148×210, A6 105×148, DL 99×210 | DL is the one that fits a standard envelope |
| Poster | A3 297×420, A2 420×594, A1, A0 | read at distance: one message, huge type |
| Brochure (bi-fold A4) | 420×297 landscape | design as spreads, not pages; allow 1 mm creep |
| Tri-fold (A4 landscape) | panels are **not** equal: the folded-in panel is ~2 mm narrower | get the panel widths from the printer |
| Menu | A4 / A5, often laminated | laminate darkens by roughly 5–10%; avoid near-black backgrounds |
| Certificate | A4 landscape or portrait | leave a signature line and space for a seal; never fake a seal |
| Invitation | A6, 148×148 sq | check it fits an available envelope before finalising |

`make_pdf.py --sizes` lists the named trims it knows; any `WxH` in mm also works.

---

## 4. Packaging

Packaging is engineering with artwork on it. Get the structure right first.

```
python scripts/dieline.py --l 60 --w 35 --h 140 --out work/box.svg
```

Generates a straight-tuck-end carton: cut (magenta), crease (cyan dashed), safe (green)
and bleed, with panel labels and an EAN-13 keepline at 100% magnification.

**Non-negotiables**

- **The converter's die wins.** Send them the generated dieline, then rebuild the artwork
  on the die they return. Ours is for layout and conversation, never for plate-making.
- **Design across the creases, not up to them.** Keep type and logos 4 mm clear of every
  crease — a fold through a word is unreadable and unfixable.
- **Know which panel is which.** Front faces the shelf. Back takes the barcode and the
  legal copy. Sides take ingredients or specs. The glue flap is never seen — put nothing
  on it.
- **Barcode:** EAN-13 at 100% is 37.29×25.93 mm. Never below 80%. Light background, dark
  bars, 2 mm quiet zone each side. Never invent a barcode number.
- **Legal copy is the client's.** Ingredients, weights, warnings, recycling marks,
  addresses and any certification logo come from them, verbatim. Never generate them, and
  never place a certification mark the client has not confirmed they hold.
- **Material changes colour.** Kraft board shifts everything warm; uncoated stock mutes
  by 10–15%. Ask what the stock is.

---

## 5. Signage, shutters, vehicles and large format

Different physics: distance, angle, weather and the fact that someone has to fix it to
something.

**The distance rule:** roughly **25 mm of cap height per 3 m of reading distance**. A
shop sign read from 15 m needs letters about 125 mm tall. Work out the height first, then
see how many words fit — not the other way round.

- **Contrast beats colour.** Dark on light or light on dark. Mid-tone on mid-tone is
  invisible at distance and in rain.
- **Three to five words.** A shopfront is not a brochure. Name, trade, one phone number.
- **Shop shutters:** the surface is corrugated. Horizontal ribs chop fine detail and thin
  horizontal strokes, so use heavy weights and keep critical detail off the rib lines.
  Allow for the fact that the shutter rolls up — the top third is often not visible when
  the shop is open.
- **Vehicles:** door handles, fuel caps, wheel arches and window lines eat artwork. Get
  the vehicle template from the wrap fitter. Keep the phone number on the rear and the
  sides, not the bonnet.
- **Safe margins are bigger:** 50 mm minimum on a banner, because of hems and eyelets.
- **Supplied details are sacred.** Phone numbers, addresses, prices and opening hours are
  copied character by character from the user and checked against the rendered pixels.
  A wrong digit on a sign is a wrong digit for years. See `composition-type.md`.

**Urdu / Arabic signage** is the common case here and has its own failure mode: the
script must *shape and join*. Build it in HTML with a real Nastaliq or Naskh face
(`assets/templates/urdu-rtl.html`), never by placing letters individually. Check the
joins and the right-to-left order on the rendered image, and keep Latin numerals and the
phone number in the direction the user wrote them. Details in `composition-type.md §Urdu`.

---

## 6. Hand-over checklist

- [ ] PDF page = trim + bleed, **measured** (`make_pdf.py` prints the MediaBox)
- [ ] Artwork actually runs into the bleed on every edge it should
- [ ] Nothing live outside the safe area; nothing important near a crease or fold
- [ ] Images 300 DPI at final size (or justified lower for large format)
- [ ] Proof raster opened and read, including every phone number and price
- [ ] Guides and dielines on a separate layer or switched off
- [ ] Note states: sRGB, bleed used, safe margin, fonts, and that CMYK/ICC is prepress
- [ ] Told the user what you could **not** verify — stock, laminate, the converter's die

Related: `deliverables.md`, `platform-specs.md`, `composition-type.md`, `qa-export.md`.
