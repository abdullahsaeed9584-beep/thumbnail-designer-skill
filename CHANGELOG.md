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
