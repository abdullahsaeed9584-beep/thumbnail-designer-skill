# Changelog

## 1.0.0 - 2026-10-27

First release.

### Added
- **Render pipeline.** The skill now builds, not just briefs: `render_html.py` (HTML/CSS to PNG
  via headless Chromium), `composite.py` (background depth, contact shadow, rim light, colour
  match), `finish.py` (clarity, vignette, grain, sharpen, size-capped export).
- **7 production templates** plus `base.css` holding the design tokens and the layer stack:
  person-led, text-hero, product-led, comparison, urdu-rtl, vertical-cover, text-layer.
- **`references/premium-standard.md`** - the quality bar: rule of 3, Z-pattern eye flow, three
  depth layers, rim light, ambient occlusion, depth of field, gradient type fills, controlled
  saturation, final mastering numbers, and the never-ship list.
- **`references/hooks.md`** - 10 headline formulas, title-pairing table, banned patterns.
- **`references/scorecard.md`** - 10 axes x 0-4 with a ship threshold of 32/40 and honesty as a
  hard gate.
- **`references/render-pipeline.md`** - the 10-layer build order with the exact commands.
- **`scripts/thumb_test.py`** - the four proof tests (mobile 168 px, grayscale, squint, feed
  mock) on one contact sheet, with measurable pass/fail on ratio, size, file weight and
  luminance spread.
- **`scripts/fetch_fonts.py`** - licence-safe OFL font fetcher, including the Urdu faces.
- Case routes R (vertical covers) and S (channel style systems).
- `yt_hd`, `shorts`, `ig_square`, `x_post` resize presets and a `--presets all` shortcut.
- Expanded evals: 25 prompts covering premium craft, traps and degraded environments.
- Packaged as an installable Claude Code plugin, with a marketplace manifest.

### Changed
- `SKILL.md` workflow now mandates the proof tests and the scorecard before delivery.
- Typography guidance rewritten around gradient fills and text-masked-behind-subject depth
  rather than hard black strokes.
- Lighting and compositing guidance given concrete numbers and script flags.
- Brand kit template expanded into a full per-client style system.

### Fixed
- `contrast_check.py --box` no longer reports a false FAIL on a finished thumbnail: glyph
  pixels are excluded by default so the headline is measured against the backdrop behind it
  (`--include-text` restores the old behaviour).
- `render_html.py` closes the temp file descriptor before deleting it (Windows file lock).
- Unsupplied colour tokens now fall back to sane defaults - an empty CSS custom property is
  valid but silently breaks every `color-mix()` and gradient that reads it.
- `vertical-cover.html` keeps the headline clear of the subject's face.
- Every template image drops itself when its asset is missing, instead of leaving a broken
  image icon in the render.
- Urdu headlines start at 158px: Nastaliq reads far smaller than Latin at the same point size,
  so the old 104px default had no presence at thumbnail scale.
- `product-led.html`'s callout ring is opt-in (`--var RING=1`) instead of landing on the
  subject by default, where it read as an accidental halo.

### Docs
- Hero banner, example gallery and proof-test strip in `docs/`, all rendered by the skill's own
  renderer rather than mocked up elsewhere.
- Install paths for the `skills` CLI (`npx skills add`), the Claude Code plugin marketplace, and
  manual copy; plus an ASCII diagram of the six-stage pipeline.

## 1.1.0 - 2026-10-27

### Added
- `service-device.html` - eighth layout, for agency and freelance service offers: service
  kicker and hook upper-left, tilted browser/device right, faint technical grid, rim light on
  the device edge. The device content is a deliberately abstract wireframe, never a screenshot
  of real results and never invented metrics.
- Its optional `STRAP` support line is OFF by default: at 168px any line under roughly 30px
  source size turns to mush, which `thumb_test.py` caught on the first build with it enabled.

## 1.2.0 - 2026-10-27

Researched how high-performing thumbnails are actually built - the YouTube search/gig-marketplace
register, plus current practice guidance - and taught the skill the look it was missing.

### Added
- **`references/style-registers.md`** - three registers (Creator High-Impact, Cinematic Editorial,
  Clean Corporate), when each applies, and the full craft recipe for each. The skill now picks a
  register BEFORE concepting, and commits to it.
- **`assets/templates/impact.css`** - the loud creator type system: heavy black stroke with
  `paint-order: stroke fill`, hard 3D extrude per colour role, angled sticker bars, saturated
  grounds, sunburst / halftone / perspective-grid textures, hard-lit cut-out treatment, and
  props (play button, growth arrow, coin, badge, subscribe pill).
- **`assets/templates/creator-impact.html`** - ninth layout. Stacked tri-line hook, kicker
  sticker, 2-4 rotated props, subject right. With no cut-out supplied it automatically
  rebalances to a centred type-hero rather than leaving half the frame dead.
- Verified at 168px: all three sample builds stay fully legible, which is the point of the
  register.

### Changed
- `SKILL.md` workflow step 4 is now "Register, then concept", with routing for loud/creator asks.
- **`cases.md` §M rewritten around YouTube's Test & Compare**, which resolves by **watch time
  share, not CTR**; outcomes are Winner / Preferred / None, results take a few days to two weeks,
  and the report is in the Reach tab. Variants must be visually diverse or the test cannot
  resolve. This is why an overselling thumbnail can win the click and still lose the test.
- The register explicitly still refuses fabricated performance numbers - fake CTR figures, view
  counts or analytics screenshots - which are common in that market. Loud is a style; dishonest
  is a defect.

## 1.3.0 - 2026-10-27

Course-correction release. The skill had started growing templates shaped around whatever the
last example happened to be, and its artwork was drawn in CSS - which is exactly why output
read as synthetic.

### Added
- **`scripts/fetch_stock.py`** - real CC0 / public-domain photography from Openverse, no API
  key. Writes `ATTRIBUTION.md` for every download, defaults to licences that need no credit,
  and warns that open licensing is not a model, property or trademark release.
- **`assets/templates/showcase.html`** - one niche-agnostic layout replacing `service-device`
  and `gig-video`. `DEVICE=browser|player|screen|none`; `screen` composites the user's OWN
  image inside the rim-lit tilted frame. Works at any canvas size and auto-centres as a type
  hero when no device is used.
- Fiverr gig spec (1280x769, min 712x430, max 4000x2416) in `platform-specs.md`, a `fiverr`
  preset in `resize.py`, and its ratio in `thumb_test.py` - without that entry a correct gig
  image was reported as "not a clean platform ratio".

### Changed
- `SKILL.md` now states the skill is niche- and platform-agnostic, and sets the imagery order
  of preference: user's own asset, then real stock, then abstraction.
- Removed `service-device.html` and `gig-video.html`; both were the same pattern shaped around
  one example each. Use `showcase.html`.

### Fixed
- **`render_html.py` silently turned ordinary words into file:// URLs.** Any `--var` value
  matching an existing file or folder was rewritten as a path, and on Windows the match is
  case-insensitive - so a headline word like WORK beside a `work/` directory rendered as
  `file:///C:/.../work` inside the thumbnail. Conversion now requires an asset extension.

## 1.4.0 - 2026-10-27

### Added
- **`assets/templates/photo-split.html`** - a real photograph full-bleed on one side, type on
  the other, joined by a gradient scrim. No cut-out, so no mask, no halo and no hair matting.
  This is the practical way to use real photography when `rembg` is unavailable (its model is
  a 1 GB download) or the background is busy. `SIDE`, `SPLIT`, `FOCUS`, `GRADE`
  (teal-orange / cool / warm / none) and an opt-in `SEAM`.

### Changed
- The accent seam is opt-in and the scrim feather is longer. A hard line at the join advertised
  the composite as two pasted halves instead of reading as one photograph.

## 1.5.0 - 2026-10-27

### Added
- **Backlight glow in `photo-split.html`** - `GLOW`, `GLOW_SHAPE`, `GLOW_POS`, `GLOW_SIZE`,
  `GLOW_STRENGTH`. Screen blend, because the photo is full-bleed rather than cut out, so a
  layer underneath would be invisible. Default shape is a halo **ring**: a filled disc centred
  on the head washes the face out under screen blend, which is the mistake the first pass made.
- `docs/style-photo-split.png` - three real-photo examples across fitness, business and podcast
  niches, two layout directions, three palettes, all from the one template.

### Changed
- README restructured: the output gallery now sits at the top under "What it makes" instead of
  being buried near the licence.

### Fixed
- **The scrim fade now tracks `SPLIT`.** With fixed gradient stops a wide photo ended inside
  open frame and showed its straight edge, while a narrow one got scrimmed into mud. The stops
  are computed from the split position.

## 1.6.0 - 2026-10-28

Studied a set of top-tier reference thumbnails and taught the skill the technique that
separates them from competent work.

### Added
- **`references/glow-and-light.md`** - the motivated-light doctrine. Every glow must have a
  visible source in the frame, and its colour must land on the subject, the background and the
  type. Plus selective desaturation, the premium mixed-case type treatment, the annotation
  layer, props that carry words, and stylised-not-fake data.
- **Register D, Premium Insight** in `style-registers.md`.
- **`assets/templates/premium.css`** - light sources (bar / wave / orb) with a three-stop
  emissive core and a blurred bloom, local spill, source-centred falloff, mono treatment,
  silver mixed-case headline, hand-drawn SVG annotation, pill labels.
- **`assets/templates/insight.html`** - tenth layout, the register D build.
- **General design canvases** in `platform-specs.md`: Instagram, stories, channel banners, X
  and LinkedIn headers, display ads, slides, A4/A3 posters, flyers, covers, email headers,
  with print notes. The skill is explicitly a graphic-design skill now, not a thumbnail-only one.

### Fixed
- Spill and bloom were sized at 3.4x the source and applied frame-wide, which flooded the
  whole canvas and stopped the source reading as a source. Both are now capped and local, and
  the spill leans toward the subject so motivated light actually lands on the person.
- The insight headline could overrun the pill label; the column now reserves that band.

## 1.6.1 - 2026-10-28

### Added
- `DIM` on `insight.html`. A portrait shot on a light background sits brighter than the design
  base, so its straight edge shows through the scrim; `DIM` drops it to meet the design.
- `docs/showcase.png` - the README now leads with Premium Insight work across health, finance
  and psychology, replacing the earlier gallery.

### Changed
- The insight type column narrowed to 42%. A multi-word `LIT` with `LIT_STYLE=bar` wrapped into
  a slab so large it covered the light source behind it; the template now says to keep a bar
  accent to one word.

## 1.7.0 - 2026-10-28

The premium register was producing austere, empty work: one portrait, one glowing bar and a
large field of black. Technically compliant with its own doctrine, and visually cheap.

### Added
- **`glow-and-light.md` section 7, Density.** A real environment photograph behind everything
  (a gradient is not a place), colour kept rather than crushed, a light source with real
  structure, and the subject blended with a mask. If a large area carries nothing, it is not
  finished.
- **`assets/templates/scene.html`** - eleventh layout and the dense build: environment photo,
  `VIZ` light object (16 candlesticks with wicks / 30 equaliser bars / a plotted line), subject
  feathered into the scene with a CSS mask, colour preserved.

### Fixed
- Environment dimming defaulted so dark the room became a smear - the exact failure the
  template exists to prevent. Defaults are now blur 9px, brightness 0.78.
- The subject edge was being hidden under an overlaid dark band rather than blended; the photo
  now feathers its own edge with `mask-image`.
- `MONO` defaulted near 1.0, draining the picture. The useful range in a scene is 0.2-0.4.

## 1.7.1 - 2026-10-28

Audit and packaging pass.

### Changed
- **`SKILL.md` rewritten** as a proper entry point: workflow in 8 numbered steps with the
  register choice and real-imagery sourcing promoted into the flow, a routing table that leads
  with the premium and glow paths, and the hard rules tightened. 96 lines, every path verified
  to resolve.

### Fixed
- Two dead references to `service-device.html` in `style-registers.md`, left behind when that
  template was folded into `showcase.html`.
- README claimed 11 templates; there are 12.

### Verified
- All 9 scripts compile and their CLIs load.
- Every `references/`, `scripts/`, `assets/` and `evals/` path cited in `SKILL.md` exists.
- Every cross-reference between files in `references/` resolves.
- Every template referenced in the docs is present, and every present template is documented.
- Every README image link resolves.
- Distributable is 1.71 MB.

## 1.7.2 - 2026-10-28

### Changed
- **Showcase rebuilt with `scene.html`.** The gallery still led with three `insight.html`
  builds - the austere, empty version of the premium look. Replaced with music, markets and DJ
  builds that have a real place behind the subject and a structured light source.
- Dropped `docs/style-premium-insight.png`; the register D section now points at the showcase
  rather than carrying a second, weaker gallery.

### Fixed
- `VIZ=line` stroked at 2.6px, which reads as a squiggle rather than a light source. Now 6px
  with a double drop-shadow and a wider viewport.

### Added
- Two rules to `glow-and-light.md` section 7, both from errors made building the gallery: the
  subject must belong to the scene (a sunlit portrait in a dark club gives itself away through
  light direction and colour temperature), and the light source needs enough visual weight.

## 1.7.3 - 2026-10-28

### Changed
- **Licence: MIT replaced with a proprietary all-rights-reserved licence.** MIT was the wrong
  choice for a product that is sold - it grants every buyer the right to redistribute and
  resell the skill. The new `LICENSE` permits reading, evaluating and licensed use, and
  withholds redistribution, resale and derivative products. Output images stay the user's own.
  The repository remains public: readable source is not an open-source grant, and the licence
  says so explicitly.
- `plugin.json` now declares `"SEE LICENSE IN LICENSE"`; `SKILL.md` frontmatter declares
  `Proprietary - see LICENSE`; the README badge and licence section match.
- Third-party terms called out separately: fonts stay OFL, and stock photography keeps the
  licence and model-release terms of its source.
