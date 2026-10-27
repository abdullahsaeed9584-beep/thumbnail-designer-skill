# Tool Tiers & Honesty

Detect once per task; state the tier and the route in the one-line delivery note.

## Tier 1: Code render (default wherever bash + Python exist)
- **Setup:** `python -m pip install --quiet pillow numpy` (add `opencv-python rembg` if the network allows), then `python scripts/fetch_fonts.py --all`.
- **Type + full layouts:** HTML/CSS to headless Chromium via `scripts/render_html.py` (check availability with `--check`). Best typography, real gradients, blend modes. Mandatory for Urdu/Nastaliq.
- **Photographic compositing:** `scripts/composite.py` - background depth, contact shadow, rim light, colour match.
- **Mastering:** `scripts/finish.py` - clarity, vignette, grain, sharpen, size-capped export.
- **Proof:** `scripts/thumb_test.py`, `scripts/contrast_check.py`, `scripts/safe_zone_overlay.py`, `scripts/resize.py`.
- **Cutout:** existing alpha, else `rembg` (if the model downloads), else GrabCut (rough - disclose it).
- **Cannot do:** PSD, true generative imagery, Photoshop-grade hair matting. Say so plainly.
- No headless browser? Render type with Pillow and state that it is less refined.

## Tier 2: Canva connector
If Canva tools are present: `generate-image` for backgrounds and objects only (**never a face**), `create-design`, `export-design`, brand kits. Always verify the exported result and re-read the rendered text for exactness. Run the Tier 1 proof scripts on the export when bash is also available.

## Tier 3: Brief + prompts (no execution tools)
Deliver: concept, layout spec with px coordinates, palette hex values, font names, headline, per-element image-generation prompts, and a numbered build order for Canva/Photoshop/Figma. Label it clearly **"not executed"**.

## Always
Don't pretend a tool exists. Don't claim an edit, an export or a verification you didn't perform. For an unsupported request, state the limit and offer the closest reliable alternative.
Match tool to task: pixel preservation needs masks and layers - exact text needs an HTML/code render - colour needs controlled code adjustments - illustration needs a generation tool (non-face only) - batch needs scripts.
