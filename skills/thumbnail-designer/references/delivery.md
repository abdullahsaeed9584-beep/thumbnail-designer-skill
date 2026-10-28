# Delivery — what actually lands in the user's folder

A design job is judged on the finished files. Everything else — concepts, proofs,
overlays, contact sheets, frame dumps, intermediate exports — is working material.
It belongs in the temp proof folder, and it stays there.

---

## 1. The default delivery

**One file per thing the user asked for.** Nothing else.

| Asked for | Deliver | Not this |
|---|---|---|
| A thumbnail | one JPG at the platform size | the 4 proof images, the raw PNG, 3 variants |
| A logo | one SVG + one PNG | 6 lockup files, a contact sheet, every export size |
| A logo *and* banner | logo SVG, logo PNG, banner PNG | a `png/` tree, proofs, white + dark of everything |
| A flyer | one print-ready PDF | the PDF, the proof raster and the filled HTML |
| An animated logo | one MP4 | the MP4, the GIF, the frame sequence and a filmstrip |

Then 1–3 lines: what it is, where it is, and any limitation worth knowing.

**Give more only when asked.** "Show me the concepts", "I need the source", "give me
every size", "both colourways" — those are requests. Absent them, assume not.

---

## 2. Where working files go

`scripts/scratch.py` resolves a temp folder per project. `thumb_test.py`,
`safe_zone_overlay.py`, `svg_check.py --sheet` and `make_pdf.py --proof` all route
there by default; `--here` overrides when proofs are genuinely wanted beside the art.

```
python scripts/scratch.py            # where the proofs are
python scripts/scratch.py --clean    # remove them after a successful delivery
```

Clean up at the end of a successful job. **Never delete anything outside that temp
folder** — not the user's source photos, not earlier versions, not the project's own
assets. If an old deliverable is being replaced, replace that file; do not sweep the
directory.

---

## 3. Explore privately, ship once

Three genuinely different directions is good practice, and it is an *internal* step.
Build them into one contact sheet in the temp folder, look at it, pick one, and
develop that one properly. The user sees the winner.

This is a real quality lever, not a formality: the first idea is usually the obvious
one, and the obvious one is what makes a logo look like a template. But exploring
costs nothing only if the exploration stays out of the delivery.

If the user asks to see the directions, show the single contact sheet — not three
finished sets.

---

## 4. Naming

Name files for what they are, from the user's point of view:

```
stayfit-logo.svg        not  stayfit-logo-horizontal-white-v3.svg
stayfit-logo.png        not  png/stayfit-mark-solid_800.png
stayfit-banner.png      not  stayfit-banner-final-2560x1440-v2.png
```

No version numbers in a delivered filename unless the user versions things that way.
No size in the name unless two sizes are being delivered. No `final`, no `v2`.

---

## 5. Before you write the summary

- [ ] Does the output folder contain **only** the files asked for?
- [ ] Any proof, overlay, contact sheet or frame left behind? Move or delete it.
- [ ] Any duplicate of the same artefact in two formats nobody requested?
- [ ] Any folder created for a single intermediate step? Flatten it.
- [ ] Temp folder cleaned, and nothing outside it touched?
- [ ] Does every path in the summary exist, and open?

Related: `deliverables.md` (which artefact a brief needs), `qa-export.md` (the checks
themselves), `scripts/scratch.py`.
