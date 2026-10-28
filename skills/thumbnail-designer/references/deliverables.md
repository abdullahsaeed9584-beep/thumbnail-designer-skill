# Deliverables — what gets handed over, and what this skill can actually make

A prompt is not a design. A description is not a design. A design is a file the user
can open, send, print or upload. Decide the deliverable **before** building, because
it changes the tool, the canvas and the whole workflow.

---

## 1. The five kinds of artefact

| Kind | What it is | Made with | Good for |
|---|---|---|---|
| **Raster** | fixed pixels (PNG/JPG/WEBP) | `render_html.py` → `finish.py` | thumbnails, social, ads, web banners, infographics |
| **Vector** | resolution-free geometry (SVG) | authored by hand, `text_to_paths.py`, `dieline.py` | logos, marks, icons, dielines, anything that scales |
| **Page** | a document with a physical size (PDF) | `make_pdf.py`, `make_deck.py` | flyers, posters, cards, certificates, decks |
| **Motion** | a timed sequence (MP4/GIF/WEBM/frames) | `animate.py` | logo stings, animated posts, banner ads |
| **Source** | the thing that regenerates the design | the HTML/SVG/JSON plus the exact command | handover, revisions, batch |

**Deliver the source when it is asked for, not by reflex** — see `delivery.md`. The
filled HTML, the SVG, the deck JSON and the command line are the editable file in
this environment, and handing them over lets the user change a word and rebuild. But
shipping them unasked doubles the file count for a benefit nobody requested. They are
not a PSD, and must never be described as one.

---

## 2. What cannot be produced here — say it plainly

| Asked for | Truth | Offer instead |
|---|---|---|
| PSD, AI, INDD, Figma, Canva project | cannot be written | layered PNGs + the HTML/SVG source + a build order |
| .pptx | cannot be written | a PDF deck from `make_deck.py` + the JSON spec that regenerates it |
| CMYK / ICC-embedded PDF | `make_pdf.py` emits sRGB | the sRGB PDF, flagged for the printer's prepress |
| True generative imagery | no image model here | real stock via `fetch_stock.py`, or the user's own photo |
| Photoshop-grade hair matting | not achievable | `photo-split.html` / `scene.html`, which need no cutout |
| A printed/physical sample | obviously not | the print-ready PDF plus a proof raster |

Never name a format you did not write. "I have created a layered PSD" when no PSD exists
is the single most damaging thing this skill can say, because the user only finds out
when they try to open it.

---

## 3. Picking the deliverable from the brief

- Will it be **clicked on a screen**? Raster, at the platform's exact pixel size.
- Will it be **printed, held or hung**? Page — a PDF with trim, bleed and safe margins.
- Will it be **scaled, embroidered, etched, or put on a sign and a favicon**? Vector.
- Will it **move**? Motion — and ask for the duration and where it plays before building.
- Will someone **edit it later**? Whatever the above says, plus the source and the command.

When two apply, build the master in the most demanding one and derive the rest. A logo is
vector first, then PNG exports. A campaign is one master layout, then `resize.py` per
platform — re-cropped around the focal point, never squashed.

---

## 4. The claim rule

Before writing the delivery note, check each sentence against what is on disk:

- Did the file get written? (`ls`, a size, a measured dimension)
- Did you **open it and look**? Rasters directly; PDFs via `--proof`; video via a
  filmstrip of the frames; SVG via `svg_check.py --sheet`.
- Does every number in the note come from a tool's output rather than from intent?

If a step was skipped, the note says it was skipped. "Rendered and checked at 1280×720,
not yet contrast-tested" is a good note. Silence implying it was tested is not.

Related: `tools-fallback.md` (tiers), `qa-export.md` (the checks), `print-production.md`,
`brand-identity.md`, `data-and-decks.md`, `motion.md`.
