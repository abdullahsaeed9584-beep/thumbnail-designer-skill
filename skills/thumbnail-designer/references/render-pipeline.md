# Render Pipeline (Tier 1)

How a premium thumbnail is actually produced in code. Build in this order — each step depends on the one before.

## Setup (once)
```bash
python -m pip install --quiet pillow numpy            # core, always
python -m pip install --quiet opencv-python rembg     # optional: better cutout
python scripts/fetch_fonts.py --all                   # licence-safe Google Fonts into assets/fonts/
```
Headless Chromium (Playwright, `chrome`, `chromium`, or Edge) gives the best typography and is required for Urdu/Nastaliq. `scripts/render_html.py --check` reports what's available.

## The 10 layers

| # | Layer | How |
|---|---|---|
| 1 | **Background** | user photo, or CSS gradient/geometry/texture. Never competes with the subject. |
| 2 | **Background depth** | Gaussian blur 15-30% + desaturate ~15% + vignette 8-15%. `finish.py --vignette` or CSS `filter`. |
| 3 | **Subject cutout** | existing alpha > `rembg` > GrabCut. Inspect edges at 300%. `composite.py --subject` |
| 4 | **Contact + cast shadow** | blurred, offset alpha multiplied under the subject. `composite.py --shadow` |
| 5 | **Rim light** | coloured blurred alpha offset behind the subject edge, keyed to the bg light. `composite.py --rim "#00E5FF"` |
| 6 | **Colour match** | pull subject black point/temperature toward the background. `composite.py --match` |
| 7 | **Headline** | HTML/CSS → transparent PNG → composite. `render_html.py` |
| 8 | **Graphic cues** | ≤3 arrows/rings/badges, one style, aligned. |
| 9 | **Foreground depth** | 1-2 blurred particle/bokeh elements at the extreme edges, low opacity. |
| 10 | **Finish** | `finish.py --clarity 15 --grain 2.5 --vignette 10 --sharpen` |

**Text goes under the subject layer** when you want the masked-behind-subject depth effect: render 7 before compositing 3.

## Two routes

**A. HTML/CSS (preferred).** Compose the whole 1280×720 frame as one HTML page from `assets/templates/`, substitute placeholders, screenshot it, then run `finish.py`. Best type control, real gradients, blend modes, `backdrop-filter`. Mandatory for Urdu.
```bash
python scripts/render_html.py assets/templates/person-led.html out.png \
  --var HEADLINE="IT'S OVER" --var ACCENT="#00E5FF" --var SUBJECT="work/cut.png" --var BG="work/bg.jpg"
python scripts/finish.py out.png final.jpg --clarity 15 --grain 2.5 --vignette 10 --sharpen --max-bytes 2000000
```

**B. Pillow/OpenCV.** For photographic compositing, masks and batch work. Use `composite.py` for layers 3-6, then `render_html.py` for the headline PNG, then `finish.py`.

Mixing is normal: backgrounds and compositing in Python, type in HTML.

## Placeholders in templates
`{{HEADLINE}}` `{{KEYWORD}}` `{{SUBHEAD}}` `{{SUBJECT}}` `{{BG}}` `{{ACCENT}}` `{{INK}}` `{{BASE}}` `{{LOGO}}` `{{BADGE}}` — any `--var NAME=value` replaces `{{NAME}}`. Unused placeholders render empty, not as literal braces.

## Honesty
State the tier and the route in the delivery note. If Chromium is unavailable, say the type was rendered with Pillow and may be less refined. If the cutout came from GrabCut, say the hair edge is approximate. Never claim a layer you didn't build.
