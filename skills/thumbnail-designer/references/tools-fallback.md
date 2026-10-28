# Tool Tiers & Honesty

Detect once per task; state the tier and the route in the one-line delivery note.

## Tier 1: Code render (default wherever bash + Python exist)
- **Setup:** `python -m pip install --quiet pillow numpy` (add `opencv-python rembg` if the network allows), then `python scripts/fetch_fonts.py --all`.
- **Type + full layouts:** HTML/CSS to headless Chromium via `scripts/render_html.py` (check availability with `--check`). Best typography, real gradients, blend modes. Mandatory for Urdu/Nastaliq.
- **Photographic compositing:** `scripts/composite.py` - background depth, contact shadow, rim light, colour match.
- **Mastering:** `scripts/finish.py` - clarity, vignette, grain, sharpen, size-capped export.
- **Proof:** `scripts/thumb_test.py`, `scripts/contrast_check.py`, `scripts/safe_zone_overlay.py`, `scripts/resize.py`.
- **Print pages:** `scripts/make_pdf.py` - HTML to a PDF whose page box is trim + bleed, with crop marks. It reads the `/MediaBox` back out and fails on a mismatch, and `--proof` writes a raster to look at. sRGB only; CMYK and ICC are prepress.
- **Vector / logos:** author the SVG by hand; `scripts/text_to_paths.py` converts a wordmark to real outlines (needs `fonttools`); `scripts/svg_check.py` validates structure, refuses an embedded raster or a missing viewBox, and renders a scale + one-colour contact sheet.
- **Packaging:** `scripts/dieline.py` generates a dimensioned straight-tuck-end carton dieline as SVG (cut / crease / safe / bleed, barcode keepline). For layout only - the converter's die wins.
- **Decks:** `scripts/make_deck.py` builds a multi-page PDF plus slide PNGs from a JSON spec, and refuses an unsourced statistic or chart. **Not** a .pptx; nothing here can write one.
- **Template hygiene:** `scripts/lint_templates.py` after editing any template - it catches unbalanced braces, missing `onerror`, and the `var top` / `var name` class of bug that fails silently and breaks something far away.
- **Motion:** `scripts/animate.py` renders an animated HTML design frame by frame and encodes MP4 / WebM / GIF with ffmpeg (`--frames-only` works without it). No audio, no AE/Lottie project, no 3D, no footage editing.
- **Cutout:** existing alpha, else `rembg` (if the model downloads), else GrabCut (rough - disclose it).
- **Cannot do:** PSD, AI, INDD, Figma, .pptx, CMYK/ICC output, audio, generative imagery, Photoshop-grade hair matting. Say so plainly and offer the alternative in `deliverables.md`.
- No headless browser? Render type with Pillow and state that it is less refined.

## Tier 2: Canva connector
If Canva tools are present: `generate-image` for backgrounds and objects only (**never a face**), `create-design`, `export-design`, brand kits. Always verify the exported result and re-read the rendered text for exactness. Run the Tier 1 proof scripts on the export when bash is also available.

## Tier 3: Brief + prompts (no execution tools)
Deliver: concept, layout spec with px coordinates, palette hex values, font names, headline, per-element image-generation prompts, and a numbered build order for Canva/Photoshop/Figma. Label it clearly **"not executed"**.

## Always
Don't pretend a tool exists. Don't claim an edit, an export or a verification you didn't perform. For an unsupported request, state the limit and offer the closest reliable alternative.
**Optional dependencies, and what to do without them:** `fonttools` (wordmark outlining - without it say the lettering is still live text), `ffmpeg` (video encode - without it deliver a PNG frame sequence), `rembg` (cutouts - without it use `photo-split.html` or `scene.html`, which need none). Check before claiming, never after.

Match tool to task: pixel preservation needs masks and layers - exact text needs an HTML/code render - colour needs controlled code adjustments - illustration needs a generation tool (non-face only) - batch needs scripts.
