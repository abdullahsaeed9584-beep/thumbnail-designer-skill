# QA + Export

Verify what applies - and actually open the images. Nothing here may be assumed.

## Automated
```
python scripts/thumb_test.py out.jpg --competitors comp1.jpg comp2.jpg
python scripts/contrast_check.py --image out.jpg --box 60,400,700,200 --fg "#FFFFFF"
python scripts/safe_zone_overlay.py out.jpg --platform yt
```
`thumb_test.py` exits 1 on a hard failure (ratio, pixel size, file size, flat luminance). Fix, then re-run.

**Per deliverable** - a raster check proves nothing about a PDF or a video:
```
python scripts/make_pdf.py ... --proof out_proof.png   # measures /MediaBox, fails on mismatch
python scripts/svg_check.py logo.svg --sheet proof.png # structure + 16px + one-colour sheet
python scripts/make_deck.py deck.json --pdf deck.pdf   # compares page count to slide count
python scripts/animate.py ... --frames-dir frames/     # then build a filmstrip and watch it
```
Each of these writes something to LOOK at, because none of them can be judged from a measurement.

## By eye (cannot be automated - open the files)
**IDENTITY** - face geometry and proportions unchanged - eyes/nose/lips/ears/jaw intact - hairstyle, hairline and flyaway strands intact - no regeneration - no smoothing. Compare a face crop against the original at the same scale.
**IMAGE** - exposure - contrast - natural skin - controlled saturation - no destructive sharpening - no clipping, banding or colour casts.
**COMPOSITING** - clean edges, no halos - perspective - one light direction - realistic contact and cast shadow - rim light keyed to the background - natural blend.
**DESIGN** - one focal point - clear hierarchy - negative space - balance - purposeful graphics - no clutter - three depth layers.
**TYPE** - spelling - numbers - readable at 168 px - appropriate face - spacing - no distortion - safe margins - (Urdu) shaping, joins and RTL order correct.
**EXPORT** - ratio - pixel size - format - sRGB - under the platform file limit - the file actually opens.
**PRINT** (if physical) - page = trim + bleed - art runs into the bleed - nothing live outside safe - nothing near a crease - 300 DPI at final size - guides off - prepress limits stated.
**VECTOR** (if a logo) - viewBox present - no embedded raster - lettering outlined - legible at 16px - black, knockout and greyscale versions all still read.
**MOTION** (if animated) - watched a filmstrip, not one frame - contrast holds at every moment - eased, not linear - ends on a hold - duration/size/fps quoted from the probe.
**DATA** (if it carries numbers) - every figure traceable to the user or a named source - the source is ON the artefact - axis starts at zero - units present.
**HONESTY** - no fabricated data or claims - matches the video - limitations disclosed.

## Score before shipping
`references/scorecard.md` - 10 axes, 0-4 each. **Ship at 32/40 or above, with no axis at 0**, and the honesty axis never at 0. Below that: fix and re-test. If something is unfixable in the current tier, say so plainly rather than shipping it quietly.

## Deliverables
1. Final image(s), presented.
2. The original kept separately and unmodified.
3. The source that regenerates it - the filled HTML, the SVG, the deck JSON, and the exact command. PSD/AI/Figma/.pptx are not producible here; offer this instead and say so. See `deliverables.md`.
4. Font and asset list, licence-safe.
5. A 1-3 line note: tier used, assumptions made, limitations.
Never invent a download link or claim an editable file that doesn't exist.
