<div align="center">

![Thumbnail Designer](docs/banner.png)

**A senior-art-director skill for Claude that designs, renders, critiques, A/B tests and
batch-produces premium thumbnails — and proves the result before shipping it.**

[![License: MIT](https://img.shields.io/badge/license-MIT-0B0E14?style=flat-square)](LICENSE)
![Skill](https://img.shields.io/badge/type-agent%20skill-2563EB?style=flat-square)
![Templates](https://img.shields.io/badge/templates-7-16A34A?style=flat-square)
![Scripts](https://img.shields.io/badge/scripts-8-0891B2?style=flat-square)
![Platforms](https://img.shields.io/badge/platforms-12-F2A20C?style=flat-square)

</div>

---

## Quick Start

**Fastest path — any agent, one command.** The open
[skills CLI](https://github.com/vercel-labs/skills) installs into Claude Code, Cursor, Codex,
Copilot, Cline and more. Requires Node.js 22.20+:

```bash
# install into the current project (it prompts for the agent)
npx skills add abdullahsaeed9584-beep/thumbnail-designer-skill

# or straight into Claude Code, available across all projects
npx skills add abdullahsaeed9584-beep/thumbnail-designer-skill --skill thumbnail-designer -a claude-code -g

# try it once without installing
npx skills use abdullahsaeed9584-beep/thumbnail-designer-skill@thumbnail-designer
```

**As a Claude Code plugin** — this repo ships a marketplace manifest:

```bash
/plugin marketplace add abdullahsaeed9584-beep/thumbnail-designer-skill
/plugin install thumbnail-designer
```

**Manual copy** — works everywhere, nothing to trust:

```bash
git clone https://github.com/abdullahsaeed9584-beep/thumbnail-designer-skill
cp -r thumbnail-designer-skill/skills/thumbnail-designer ~/.claude/skills/     # all projects
cp -r thumbnail-designer-skill/skills/thumbnail-designer .claude/skills/       # this repo only
```

**On Claude.ai** — upload `skills/thumbnail-designer/` as a custom skill.

### Then set up the renderer

```bash
python -m pip install pillow numpy          # required
python -m pip install opencv-python rembg   # optional: better cut-outs
python ~/.claude/skills/thumbnail-designer/scripts/fetch_fonts.py --all
python ~/.claude/skills/thumbnail-designer/scripts/render_html.py --check
```

---

## What it makes

![Example thumbnails](docs/examples.png)

<sub>Rendered by the skill itself — no photo input, no image generation. The banner above was
made the same way.</sub>

```
Make a YouTube thumbnail for "Why Most People Never Become Rich"
Here's my photo — finance thumbnail, dark navy and gold
Why is the CTR on this thumbnail low?          (attach it)
3 A/B variants for this title
Resize this for Shorts, Instagram and LinkedIn
Urdu headline: امیر کیسے بنیں
```

---

## The pipeline

```
   CONCEPT         BUILD           LIGHT            TYPE           PROVE          SHIP
 ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
 │  Hook    │   │   BG     │   │   Rim    │   │ Headline │   │  Mobile  │   │  Export  │
 │  Layout  │──▶│ Subject  │──▶│  Shadow  │──▶│ Keyword  │──▶│   Gray   │──▶│  Score   │
 │  Palette │   │  Depth   │   │  Match   │   │   Cues   │   │  Squint  │   │ Deliver  │
 └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
   hooks.md      composite.py   composite.py   render_html    thumb_test      finish.py
   premium-       templates/     base.css        .py             .py         scorecard.md
   standard.md
```

Ten layers, built in order — background, depth, subject, contact shadow, rim light, colour
match, headline, cues, foreground depth, finish. Reordering them is what makes a composite look
pasted on.

---

## Why this one is different

**It renders.** Seven production HTML/CSS layouts plus a Python compositing pipeline —
background depth, contact shadow, rim light, colour match, gradient type, grain finish. Most
thumbnail "skills" only produce a brief.

**It proves its work.** Every build runs the four tests a thumbnail has to survive:

![Proof tests](docs/proof-sheet.png)

Plus a mock feed row beside competitors. `thumb_test.py` exits non-zero on a bad ratio, pixel
size, file weight or flat luminance — so a failing thumbnail can't quietly ship.

**It scores itself.** A 10-axis scorecard with a ship threshold of 32/40, and honesty as a hard
gate — not "looks fine to me".

**It refuses to fake things.** No face reshaping or regeneration, no fabricated data, no
clickbait the video doesn't pay off, and no claiming an edit it didn't actually execute.

---

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
│   ├── contrast_check.py     WCAG contrast vs the real pixels behind the text
│   ├── safe_zone_overlay.py  margin / duration-badge overlay
│   ├── resize.py             focal-aware multi-platform re-crop
│   └── fetch_fonts.py        licence-safe Google Fonts
├── assets/
│   ├── templates/            7 production layouts + base.css
│   ├── brand-kits/           per-client style systems
│   └── fonts/                OFL fonts land here
└── evals/test-prompts.md     25 regression prompts
```

---

## Pipeline by hand

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

---

## Templates

| File | Use | Size |
|---|---|---|
| `person-led.html` | face-led, hook upper-left, subject right, text masked behind subject | 1280×720 |
| `text-hero.html` | no subject photo, or the words are the idea | 1280×720 |
| `product-led.html` | hero object or a single data indicator on a studio sweep | 1280×720 |
| `comparison.html` | real before/after or A vs B, diagonal split, warm vs cool | 1280×720 |
| `urdu-rtl.html` | Urdu/Nastaliq, mirrored Z-pattern, descender room | 1280×720 |
| `vertical-cover.html` | Shorts / Reels / TikTok | 1080×1920 |
| `text-layer.html` | headline only, transparent — for the compositing route | 1280×720 |

---

## Non-negotiables

Identity is never generated — a person's face and hair come from their original pixels, with no
reshaping, smoothing or generative inpainting. Nothing is fabricated: no invented stats, prices,
quotes, screenshots or endorsements. Nothing is claimed that wasn't executed. Fonts are
licence-safe. Honesty is a hard gate on the scorecard, not a style preference.

## Contributing

A bad output means a missing rule. Add it to the matching file in `references/`, not to
`SKILL.md` (which stays under ~150 lines), then re-run `evals/test-prompts.md`.

## Licence

MIT — see [LICENSE](LICENSE). Fonts are OFL and fetched at setup, not vendored.
