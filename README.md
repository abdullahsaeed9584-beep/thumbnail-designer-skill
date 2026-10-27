# Thumbnail Designer — a Claude skill

A senior-art-director skill for Claude Code / Claude.ai that designs, critiques, A/B tests,
resizes and batch-produces **premium** thumbnails and cover images — and actually renders them,
rather than only describing them.

Built for YouTube, Shorts/Reels/TikTok, Instagram, Facebook, LinkedIn, X, podcast covers and
blog/OG images. Handles topic-only briefs, video titles, personal photos under a strict
identity-preservation protocol, reference thumbnails, brand kits, Urdu/RTL headlines,
background replacement, cinematic grading, and CTR-focused critique.

## Why this one is different

- **It renders.** Seven production HTML/CSS layouts plus a Python compositing pipeline —
  background depth, contact shadow, rim light, colour match, gradient type, grain finish.
- **It proves its work.** Every build runs the four tests a thumbnail has to survive:
  mobile 168 px, grayscale, squint, and a mock feed row beside competitors.
- **It scores itself.** A 10-axis scorecard with a shipping threshold, so "looks fine" is not
  the standard.
- **It refuses to fake things.** No face reshaping or regeneration, no fabricated data, no
  clickbait that the video doesn't pay off, no claiming an edit it didn't execute.

## Install

**As a Claude Code plugin (recommended)**

```bash
/plugin marketplace add <your-github-user>/thumbnail-designer-skill
/plugin install thumbnail-designer
```

**As a plain skill** — copy the skill folder into your skills directory:

```bash
# user-level (all projects)
cp -r skills/thumbnail-designer ~/.claude/skills/
# or project-level
cp -r skills/thumbnail-designer .claude/skills/
```

**On Claude.ai** — upload `skills/thumbnail-designer/` as a custom skill.

## First run

```bash
python -m pip install pillow numpy          # required
python -m pip install opencv-python rembg   # optional: better cut-outs
python skills/thumbnail-designer/scripts/fetch_fonts.py --all
python skills/thumbnail-designer/scripts/render_html.py --check
```

Then just ask:

> Make a YouTube thumbnail for "Why Most People Never Become Rich"

> Here's my photo — finance thumbnail, dark navy and gold

> Why is the CTR on this thumbnail low? *(attach it)*

> 3 A/B variants for this title

> Resize this for Shorts, Instagram and LinkedIn

## What's inside

```
skills/thumbnail-designer/
├── SKILL.md                  entry point: workflow, routing, hard rules
├── references/
│   ├── premium-standard.md   the quality bar — read on every build
│   ├── render-pipeline.md    the 10-layer build order and the commands
│   ├── composition-type.md   composition, typography, graphics, Urdu/RTL
│   ├── retouch-color.md      grading, cut-outs, lighting, compositing
│   ├── hooks.md              headline formulas and what's banned
│   ├── scorecard.md          10 axes × 0-4, ship at ≥32/40
│   ├── identity-protocol.md  mandatory face/hair preservation rules
│   ├── cases.md              19 input/intent routes
│   ├── niche-guide.md        visual vocabulary per niche
│   ├── platform-specs.md     sizes, safe zones, file limits
│   ├── qa-export.md          QA checklist and deliverables
│   └── tools-fallback.md     tier detection and honesty rules
├── scripts/
│   ├── render_html.py        HTML template → PNG (headless Chromium)
│   ├── composite.py          subject + bg: shadow, rim light, colour match
│   ├── finish.py             clarity, vignette, grain, sharpen, size cap
│   ├── thumb_test.py         the four proof tests + contact sheet
│   ├── contrast_check.py     WCAG contrast vs real pixels
│   ├── safe_zone_overlay.py  margin / duration-badge overlay
│   ├── resize.py             focal-aware multi-platform re-crop
│   └── fetch_fonts.py        licence-safe Google Fonts
├── assets/
│   ├── templates/            7 production layouts + base.css
│   ├── brand-kits/           per-client style systems
│   └── fonts/                OFL fonts land here
└── evals/test-prompts.md     25 regression prompts
```

## Pipeline at a glance

```bash
# 1. headline + layout
python scripts/render_html.py assets/templates/person-led.html work/raw.png \
  --var HEADLINE="IT'S" --var KEYWORD="OVER" --var SUBJECT="work/cut.png" \
  --var BG="work/bg.jpg" --var ACCENT="#00E5FF"

# 2. or composite photographically
python scripts/composite.py work/bg.jpg work/cut.png work/raw.png \
  --pos right --bg-blur 22 --shadow 0.55 --rim "#00E5FF" --match 0.3 \
  --text-layer work/text.png

# 3. master and export under the platform limit
python scripts/finish.py work/raw.png out/final.jpg --preset cinematic --max-bytes 2000000

# 4. prove it
python scripts/thumb_test.py out/final.jpg --competitors comp1.jpg comp2.jpg
```

## Non-negotiables

Identity is never generated — a person's face and hair come from their original pixels, with
no reshaping, smoothing or generative inpainting. Nothing is fabricated: no invented stats,
prices, quotes, screenshots or endorsements. Nothing is claimed that wasn't executed. Fonts
are licence-safe. Honesty is a hard gate on the scorecard, not a style preference.

## Contributing

A bad output means a missing rule. Add it to the matching file in `references/`, not to
`SKILL.md` (which stays under ~150 lines), then re-run `evals/test-prompts.md`.

## Licence

MIT — see [LICENSE](LICENSE). Bundled fonts are OFL and fetched at setup, not vendored.
