# Templates

Production HTML/CSS layouts rendered to PNG by `scripts/render_html.py`. All share `base.css`,
which holds the design tokens and the layer stack from `references/render-pipeline.md`.

| File | Use | Size |
|---|---|---|
| `person-led.html` | face-led 16:9, hook upper-left, subject right, text masked behind subject | 1280x720 |
| `text-hero.html` | no subject photo, or the words are the idea | 1280x720 |
| `product-led.html` | hero object or a single data indicator on a studio sweep | 1280x720 |
| `comparison.html` | real before/after or A vs B, diagonal split, warm vs cool | 1280x720 |
| `urdu-rtl.html` | Urdu/Nastaliq, mirrored Z-pattern, descender room | 1280x720 |
| `service-device.html` | agency/service offer: hook left, tilted device right, abstract UI | 1280x720 |
| `vertical-cover.html` | Shorts / Reels / TikTok | 1080x1920 |
| `text-layer.html` | headline only, transparent - for the `composite.py --text-layer` route | 1280x720 |

## Tokens (override with `--var`)
`ACCENT` the single accent colour - `BG` background image path - `SUBJECT` cut-out PNG -
`HEADLINE` + `KEYWORD` (keyword gets the accent) - `SUBHEAD` small kicker line -
`BADGE` corner label - `LOGO` brand mark - `KICKER` service label - `STRAP` support line - `ALIGN`, `LEFT_IMG`, `RIGHT_IMG`, `LEFT_LABEL`, `RIGHT_LABEL` per template.
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
