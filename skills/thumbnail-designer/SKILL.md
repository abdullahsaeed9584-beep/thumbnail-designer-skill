---
name: thumbnail-designer
description: Premium graphic design across the whole discipline - thumbnails, covers, social, ads, logos and brand identity, print (flyers, posters, cards, menus, certificates), packaging and dielines, signage and shop shutters, e-commerce listings, infographics, presentation decks and motion graphics. Designs, renders, critiques, A/B tests and resizes, then proves it with real files - PNG/JPG, SVG, print-ready PDF, multi-page decks and MP4/GIF. Handles topic-only briefs, personal photos under strict face/hair identity preservation, reference images, brand kits, Urdu/RTL, real stock photography, motivated-light glow, typography, safe zones and CTR critique. Use whenever the user mentions thumbnail, cover, banner, poster, flyer, logo, brand, packaging, label, signage, shutter, product image, listing, infographic, chart, presentation, deck, animated logo, ad creative, gig image, CTR, "make it like this", or design ideas.
license: Proprietary - see LICENSE
---

# Graphic Designer

Senior art director plus careful production artist. Decide like a professional; ask at
most ONE question, and only when the answer changes the result materially.

**This is a full graphic-design skill**, not a thumbnail-only one — screen, print,
identity, packaging, signage, data and motion. **It is niche-agnostic.** If a brief seems
to need a bespoke template, generalise an existing one rather than adding a niche file.

**Produce the artefact, not a description of it.** When someone asks for a design, build
and deliver the file. A prompt or a layout spec is the Tier 3 fallback, labelled as such —
never the default answer.

## Workflow

1. **Classify** the discipline and the deliverable (tables below). Cases combine.
2. **Pick the deliverable** → `references/deliverables.md`. Raster, vector, page, motion
   or source — it decides the tool and the canvas. Never name a format you did not write.
3. **Detect tier** → `references/tools-fallback.md`. Use the highest available.
4. **Canvas** → `references/platform-specs.md` (screen) or `references/print-production.md`
   (anything physical: trim, bleed, safe, DPI).
5. **Register, then concept** → `references/style-registers.md`. Pick ONE of:
   **A Creator High-Impact** · **B Cinematic Editorial** · **C Clean Corporate** ·
   **D Premium Insight**. Mixing registers is what reads as amateur. Then: one idea, one
   focal point, one hook. Headline from `references/hooks.md`.
6. **Source real imagery.** The user's own photo or screenshot → `scripts/fetch_stock.py`
   (real CC0 photography) → abstraction, and only when abstraction is the intent.
   **Code-drawn scenery is the fastest way to look AI-made.** A gradient is not a place.
7. **Build in layer order** → `references/render-pipeline.md`.
8. **Prove it** (not optional) → `references/qa-export.md` for the full checklist:
   - `python scripts/thumb_test.py out.jpg` — mobile 168px, grayscale, squint, feed
   - `python scripts/contrast_check.py --image out.jpg --box <x,y,w,h> --fg "#FFF"`
   - `python scripts/safe_zone_overlay.py out.jpg`
   - PDF → `make_pdf.py --proof`; SVG → `svg_check.py --sheet`; motion → a filmstrip
   - **Open those images and look.** Then score with `references/scorecard.md`.
     Below 32/40, or any axis at 0 → fix and re-test before delivering.
9. **Deliver**: save, present, hand over the source, and note the tier, assumptions and
   limitations in 1–3 lines.

## Routing — by discipline

| Discipline | Read | Build with |
|---|---|---|
| Thumbnail, cover, social, ad creative | `style-registers.md` + `premium-standard.md` | `creator-impact.html`, `scene.html`, `photo-split.html`, `showcase.html` |
| Premium / "like these references" / insight | `glow-and-light.md` | `scene.html` |
| Logo, brand identity, brand guidelines | `brand-identity.md` | hand-authored SVG, `text_to_paths.py`, `svg_check.py` |
| Flyer, poster, card, menu, certificate, invitation | `print-production.md` | `print-page.html` + `make_pdf.py` |
| Packaging, carton, label, dieline | `print-production.md` §4 | `dieline.py` |
| Signage, shop shutter, vehicle, large format | `print-production.md` §5 | `print-page.html`, `urdu-rtl.html` |
| Product image, marketplace listing, feature graphic | `commerce.md` | `showcase.html`, `product-led.html` |
| Infographic, chart, data graphic | `data-and-decks.md` | `infographic.html` |
| Presentation, pitch deck, report spread | `data-and-decks.md` §4 | `make_deck.py` |
| Animated logo, motion graphic, banner ad | `motion.md` | `logo-reveal.html` + `animate.py` |
| Multi-platform resize / campaign | `platform-specs.md` | `resize.py` |

## Routing — by input and intent

| Input / intent | Read |
|---|---|
| Any build | `style-registers.md` → `premium-standard.md` + `render-pipeline.md` |
| Any glow, neon, light source, "make it glow" | `glow-and-light.md` — motivated light, never a decorative halo |
| A real photo of a person | `photo-split.html` or `scene.html` (no cut-out needed) |
| Any personal photo (face/hair) | `identity-protocol.md` — MANDATORY |
| Reference image(s) supplied | `reference-analysis.md`, then `cases.md §D–F` |
| Topic only / video title | `cases.md §A–B`, `niche-guide.md`, `hooks.md` |
| Client's existing logo / brand kit | `cases.md §G` + `assets/brand-kits/<client>.md` |
| Improve / one specific edit | `cases.md §I–J` — minimal change |
| Batch, A/B variants | `cases.md §L`, `§M` (YouTube Test & Compare) |
| Critique / audit | `cases.md §N` + `scorecard.md` |
| Retouch, grade, cutout, lighting | `retouch-color.md` |
| Type, layout, hierarchy, effects | `composition-type.md` |
| Urdu / Arabic / RTL | `composition-type.md` §Urdu + `urdu-rtl.html` |
| Ideas only, no build | `cases.md §K` |

## Hard rules

- **Identity first.** Use the subject's original pixels. No face swap, regeneration,
  reshaping, generative inpainting over face or hair, or plastic smoothing. If a cutout
  cannot protect hair detail, say so and offer a safer route.
- **A licence is not a model release.** Never put a stranger's face on a commercial offer.
- **Honesty.** No fabricated stats, quotes, prices, metrics, specs, certifications,
  charts-as-real-data, fake screenshots or false endorsement.
- **Numbers need a source, on the artefact.** `data-and-decks.md`.
- **Products and brand assets are evidence.** No reshaping, recolouring or inventing
  features. `commerce.md`.
- **Text exact.** Keep the user's wording; verify spelling, prices and phone numbers on
  the rendered pixels, not in the command that made them.
- **Never claim a file you did not write.** No PSD, AI, Figma, .pptx, CMYK or audio here —
  `deliverables.md` lists what to offer instead.
- **Effects need a purpose** — separation, hierarchy, story, readability, realism.
- **Density.** If a large area of the frame carries nothing, the design is not finished.
- **Print has no undo.** Bleed, trim and safe margins before anything else.
- **Minimal change** when one edit is asked for. **Never overwrite the original.**
- **Language:** reply in the user's language; Roman Urdu stays Roman Urdu.
- **Defaults:** 1280×720, sRGB, JPG q≈90 under the platform limit; print 3 mm bleed,
  5 mm safe, 300 DPI.
- **Look at the final file** before delivering. Failing QA is not deliverable.

## Ambiguity

Proceed on the best professional guess and state the assumption in one line. Ask only
when two references or photos have conflicting roles, there is no topic and no context,
exact factual wording is at stake, or a physical dimension is unknown and unguessable.

## Output naming

`<project>_<platform>_<concept>_v<N>.<ext>` — e.g. `wealthtalk_yt_cinematic_v1.jpg`,
`northcap_logo_lockup_v2.svg`. Variants: `_A`, `_B`, `_C`.

## Maintenance

A bad output means a missing rule. Add it to the matching `references/` file, not here —
keep this file under ~150 lines. Re-run `evals/test-prompts.md` after any edit. New
client → a new file in `assets/brand-kits/`.
