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
