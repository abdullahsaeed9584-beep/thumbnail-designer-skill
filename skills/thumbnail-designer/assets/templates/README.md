# Templates

Production HTML/CSS layouts rendered to PNG by `scripts/render_html.py`. All share `base.css`,
which holds the design tokens and the layer stack from `references/render-pipeline.md`.

`creator-impact.html` additionally loads **`impact.css`**, which carries the loud creator
register - heavy stroke plus hard 3D extrude, saturated grounds, sunburst/halftone/grid
textures and props. See `references/style-registers.md`; never mix the two registers.

| File | Use | Size |
|---|---|---|
| `creator-impact.html` | **high-impact creator register**: stacked stroked/extruded type, saturated ground, props | 1280x720 |
| `person-led.html` | face-led 16:9, hook upper-left, subject right, text masked behind subject | 1280x720 |
| `text-hero.html` | no subject photo, or the words are the idea | 1280x720 |
| `product-led.html` | hero object or a single data indicator on a studio sweep | 1280x720 |
| `comparison.html` | real before/after or A vs B, diagonal split, warm vs cool | 1280x720 |
| `urdu-rtl.html` | Urdu/Nastaliq, mirrored Z-pattern, descender room | 1280x720 |
| `vertical-cover.html` | Shorts / Reels / TikTok | 1080x1920 |
| `scene.html` | **the dense premium build**: real environment photo, detailed light source, subject masked into the scene | any |
| `insight.html` | **Premium Insight register**: light source in frame, mono subject, refined type, annotation | any |
| `photo-split.html` | **real photograph, full bleed one side, type the other** - no cut-out needed | any |
| `showcase.html` | **any offer/product/service**: hook left, device right. `DEVICE=browser\|player\|screen\|none` - `screen` drops in YOUR OWN image | any |
| `text-layer.html` | headline only, transparent - for the `composite.py --text-layer` route | 1280x720 |

## Tokens (override with `--var`)
`ACCENT` the single accent colour - `BG` background image path - `SUBJECT` cut-out PNG -
`HEADLINE` + `KEYWORD` (keyword gets the accent) - `SUBHEAD` small kicker line -
`PHOTO` + `SIDE`/`SPLIT`/`FOCUS`/`GRADE` and `GLOW`/`GLOW_SHAPE`/`GLOW_POS`/`GLOW_SIZE`/`GLOW_STRENGTH` for photo-split - `BADGE` corner label - `LOGO` brand mark - `KICKER` label line - `CHIPS` (split on ` - `) - `DEVICE` + `SCREEN` for showcase - `ALIGN`, `LEFT_IMG`, `RIGHT_IMG`, `LEFT_LABEL`, `RIGHT_LABEL` per template.
Unused placeholders render as nothing, and empty nodes are removed by the inline script.

## Example
```
python scripts/render_html.py assets/templates/person-led.html work/raw.png \
  --var HEADLINE="IT'S" --var KEYWORD="OVER" --var SUBHEAD="nobody saw this coming" \
  --var SUBJECT="work/cut.png" --var BG="work/bg.jpg" --var ACCENT="#00E5FF"
python scripts/finish.py work/raw.png out/final.jpg --preset cinematic --max-bytes 2000000
python scripts/thumb_test.py out/final.jpg
```

## Checking a layout
Add `show-guides` to the `.stage` class to draw the 4% margin and the duration-badge keep-out,
render, look, then remove it before exporting.

## House rules
Edit a copy, not the original, when a client needs a variant - and save the client's token
values to `assets/brand-kits/<client>.md`. Keep the layer order in `base.css` intact: it is
the render pipeline, and reordering it is what makes composites look pasted.

## Using a real photograph

`photo-split.html` is the reliable route. It bleeds the photo across one side and dissolves it
into the type side with a gradient scrim that tracks `SPLIT`, so there is no mask, no halo and
no hair matting. `GLOW` adds a screen-blend backlight behind the subject - a halo **ring** by
default, because a filled disc washes the face out under screen blend.

```
render_html.py photo-split.html out.png --size 1280x720   --var PHOTO="work/me.jpg" --var KICKER="FITNESS" --var HEADLINE="30 DAYS"   --var KEYWORD="NO EXCUSES" --var ACCENT="#00E5FF" --var GLOW="#00E5FF"   --var GRADE="cool" --var SPLIT=64 --var FOCUS="54% 30%" --var GLOW_POS="72% 36%"
```

Dark-background portraits blend best. A licence is not a model release - see
`references/identity-protocol.md` before using anyone else's face.
