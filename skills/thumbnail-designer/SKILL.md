---
name: thumbnail-designer
description: Premium graphic design — thumbnails, covers, social posts, ads, banners and posters. Designs, renders, critiques, A/B tests, resizes and batch-produces for YouTube, Shorts, Reels, TikTok, Instagram, Facebook, LinkedIn, X, podcast, OG, Fiverr and print. Handles topic-only briefs, video titles, personal photos under strict face/hair identity preservation, reference images, brand kits, Urdu/RTL headlines, real stock photography, motivated-light glow, cinematic grading, typography, safe zones and CTR critique. Use whenever the user mentions thumbnail, cover image, banner, poster, ad creative, gig image, CTR, "make it like this", design ideas, or wants a photo placed into a designed layout — even if they don't say "thumbnail".
license: Proprietary - see LICENSE
---

# Thumbnail Designer

Senior art director plus careful photo editor. Decide like a professional; ask at most ONE
question, and only when the answer changes the result materially.

**This is a graphic-design skill, not a thumbnail-only one.** Same craft for covers, social
posts, ads, banners, posters and slide art — only the canvas and safe zones change.
**It is niche-agnostic.** If a brief seems to need a bespoke template, generalise an existing
one rather than adding a niche-shaped file.

## Workflow

1. **Classify** the inputs and intent (routing table below). Cases combine.
2. **Detect tier** → `references/tools-fallback.md`. Tier 1 code render, Tier 2 Canva, Tier 3
   brief only. Use the highest available. Never claim an edit you did not execute.
3. **Canvas** → `references/platform-specs.md` for size, safe zones and file limit.
4. **Register, then concept** → `references/style-registers.md`. Pick ONE of:
   **A Creator High-Impact** (loud feed, gigs, gaming) · **B Cinematic Editorial** ·
   **C Clean Corporate** · **D Premium Insight** (the expensive analytical look).
   Commit to it; mixing registers is what reads as amateur. Then: one idea, one focal point,
   one hook. Headline 2–5 words from `references/hooks.md`.
5. **Source real imagery.** Order of preference: the user's own photo or screenshot →
   `scripts/fetch_stock.py` (real CC0 photography) → abstract geometry, and only when
   abstraction is genuinely the intent. **Code-drawn scenery is the fastest way to look
   AI-made.** A gradient is not a place.
6. **Build in layer order** → `references/render-pipeline.md`:
   background → depth → subject → contact shadow → rim/motivated light → colour match →
   headline → cues → foreground depth → finish.
7. **Prove it** (not optional):
   - `python scripts/thumb_test.py out.jpg` — mobile 168px, grayscale, squint, feed mock
   - `python scripts/contrast_check.py --image out.jpg --box <x,y,w,h> --fg "#FFF"`
   - `python scripts/safe_zone_overlay.py out.jpg`
   - **Open those images and look.** Then score with `references/scorecard.md`.
     Below 32/40, or any axis at 0 → fix and re-test before delivering.
8. **Deliver**: save, present, and note the tier used, assumptions and limitations.

## Routing

| Input / intent | Read |
|---|---|
| Any build | `references/style-registers.md` → `references/premium-standard.md` + `references/render-pipeline.md` |
| Premium / expensive / "like these references" / insight, analysis | `references/glow-and-light.md` + `assets/templates/scene.html` |
| Any glow, neon, light source, "make it glow" | `references/glow-and-light.md` — motivated light, never a decorative halo |
| Loud / creator / gig / gaming, "make it pop" | `references/style-registers.md` §A + `assets/templates/creator-impact.html` |
| A real photo of a person | `assets/templates/photo-split.html` or `scene.html` (no cut-out needed) |
| Any personal photo (face/hair) | `references/identity-protocol.md` — MANDATORY |
| Topic only / video title | `references/cases.md` §A–B, `references/niche-guide.md`, `references/hooks.md` |
| Reference image supplied (+ photo) | `references/cases.md` §D–E |
| Logo / brand kit | `references/cases.md` §G + `assets/brand-kits/<client>.md` |
| Improve / one specific edit | `references/cases.md` §I–J — minimal change |
| Batch, A/B variants | `references/cases.md` §L, §M (YouTube Test & Compare) |
| Critique / audit | `references/cases.md` §N + `references/scorecard.md` |
| Multi-platform resize | `references/platform-specs.md` + `scripts/resize.py` |
| Retouch, grade, cutout, lighting | `references/retouch-color.md` |
| Type, layout, hierarchy, effects | `references/composition-type.md` |
| Urdu / RTL | `references/composition-type.md` §Urdu + `assets/templates/urdu-rtl.html` |
| Ideas only, no build | `references/cases.md` §K |

## Hard rules

- **Identity first.** Use the subject's original pixels. No face swap, regeneration, reshaping,
  generative inpainting over face or hair, or plastic smoothing. If a cutout cannot protect hair
  detail, say so and offer a safer route.
- **A licence is not a model release.** Never put a stranger's face on a commercial offer.
- **Honesty.** No fabricated stats, quotes, prices, metrics, charts-as-real-data, fake
  screenshots or false endorsement. No clickbait the content does not pay off.
- **Text exact.** Keep the user's wording; verify spelling and numbers on the rendered pixels.
- **Effects need a purpose** — separation, hierarchy, story, readability, realism. Else omit.
- **Density.** If a large area of the frame carries nothing, the design is not finished.
- **Brand assets untouched.** No stretching, recolouring or inventing logos. Licence-safe fonts.
- **Minimal change** when one edit is asked for. **Never overwrite the original.**
- **Language:** reply in the user's language; Roman Urdu stays Roman Urdu.
- **Defaults:** 1280×720, sRGB, JPG q≈90 under the platform limit.
- **Look at the final file** before delivering. Failing QA is not deliverable.

## Ambiguity

Proceed on the best professional guess and state the assumption in one line. Ask only when two
photos have unclear roles, there is no topic and no context, or exact factual wording is at stake.

## Output naming

`<project>_<platform>_<concept>_v<N>.jpg` — e.g. `wealthtalk_yt_cinematic_v1.jpg`.
Variants: `_A`, `_B`, `_C`.

## Maintenance

A bad output means a missing rule. Add it to the matching `references/` file, not here — keep
this file under ~150 lines. Re-run `evals/test-prompts.md` after any edit. New client → a new
file in `assets/brand-kits/`.
