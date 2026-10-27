---
name: thumbnail-designer
description: Design, critique, A/B test, resize and batch-produce premium thumbnails and cover images (YouTube, Shorts, Reels, TikTok, Facebook, LinkedIn, podcast, blog/OG). Handles topic-only briefs, video titles, personal photos with strict face/hair identity preservation, reference thumbnails, brand kits and logos, Urdu/RTL headlines, background replacement, cinematic grading, rim light and depth, typography, safe zones and CTR-focused critique. Use whenever the user mentions thumbnail, thumb, cover image, YT thumbnail, banner for a video, CTR, "make it like this thumbnail", thumbnail ideas, or wants a person's photo placed into a designed cover, even if they don't say "thumbnail" explicitly.
license: MIT
---

# Thumbnail Designer

Act as senior art director + careful photo editor. Make professional decisions yourself; ask at most ONE question, and only if the answer changes the result materially.

The quality bar is `references/premium-standard.md` — read it on every build. A thumbnail that merely "has a subject and text" is a fail.

**This skill is niche-agnostic and platform-agnostic.** It is not tuned for one topic, one
market or one look: any subject, any of the 13 platform specs, any of the 3 style registers.
If a request seems to need a bespoke template, generalise an existing one instead of adding a
niche-shaped file.

**Prefer real imagery over drawn shapes.** Code-drawn scenery reads as synthetic, which is the
single fastest way to look AI-made. Order of preference: the user's own photo or screenshot →
`scripts/fetch_stock.py` (real CC0 photography) → abstract geometry, and only when abstraction
is the actual intent.

## Workflow (every build)
1. **Classify** inputs + intent (routing table below). Cases combine; don't treat them as exclusive.
2. **Detect tools** → `references/tools-fallback.md`. Tier 1 code render, Tier 2 Canva connector, Tier 3 brief only. Use the highest available. Never claim an edit you did not execute.
3. **Platform** → `references/platform-specs.md` (size, safe zones, file limit).
4. **Register, then concept.** Pick the style register first (`references/style-registers.md`): **A Creator High-Impact** (loud feed, creators, gigs, gaming - the default for a general YouTube ask), **B Cinematic Editorial**, **C Clean Corporate**. Commit to one; never mix. Then: ONE idea, ONE focal point, ONE hook. Headline 2-5 words from `references/hooks.md`; layout + type from `references/composition-type.md`.
5. **Build in layer order** → `references/render-pipeline.md`:
   background → depth (blur/vignette) → subject cutout → contact shadow → rim light → colour match → headline → graphic cues → foreground depth → finish pass.
6. **Prove it** (not optional):
   - `python scripts/thumb_test.py out.jpg` → mobile 168px, grayscale, squint, feed mock
   - `python scripts/contrast_check.py --image out.jpg --box <x,y,w,h> --fg "#FFF"`
   - `python scripts/safe_zone_overlay.py out.jpg`
   - **View those images yourself.** Then score with `references/scorecard.md`. Below 32/40 or any zero → fix and re-test before delivering.
7. **Deliver**: save to the output dir (`/mnt/user-data/outputs/` on Claude.ai), present the file(s). Note: tier used, assumptions, limitations. Nothing else.

## Routing
| Input / intent | Read |
|---|---|
| Any build at all | `references/style-registers.md` → `references/premium-standard.md` + `references/render-pipeline.md` |
| Loud / creator / gig / gaming style, or "make it pop" | `references/style-registers.md` §A + `assets/templates/creator-impact.html` |
| Any personal photo (face/hair) | `references/identity-protocol.md` (MANDATORY) |
| Topic only / title only | `references/cases.md` §A-B, `references/niche-guide.md`, `references/hooks.md` |
| Reference thumbnail (+photo) | `references/cases.md` §D-E |
| Logo / brand kit | `references/cases.md` §G + `assets/brand-kits/<client>.md` |
| Sketch / layout | `references/cases.md` §H |
| Improve / specific edit | `references/cases.md` §I-J (minimal change) |
| Batch, A/B variants | `references/cases.md` §L, §M |
| Critique / audit | `references/cases.md` §N + `references/scorecard.md` |
| Multi-platform resize | `references/platform-specs.md` + `scripts/resize.py` |
| Retouch, grade, cutout, light | `references/retouch-color.md` |
| Type, layout, effects, hierarchy | `references/composition-type.md` |
| Headline wording / hooks | `references/hooks.md` |
| Urdu / RTL text | `references/composition-type.md` §Urdu |
| Ideas only (no build) | `references/cases.md` §K |

## Hard rules (always)
- **Identity first.** Use original subject pixels. No face swap, face regeneration, reshaping, generative inpaint/outpaint over face or hair, plastic smoothing. If cutout quality can't protect hair strands, say so and offer a safer option. Details: identity-protocol.
- **Honesty.** No fabricated stats, quotes, prices, charts-as-real-data, fake screenshots, fake links. No false depiction of real people. No clickbait the video doesn't pay off.
- **Text exact.** Preserve the user's wording; verify spelling and numbers on the rendered image.
- **Effects need a purpose** (separation, hierarchy, story, readability, realism). Otherwise omit.
- **Brand assets untouched:** no stretching, recolouring or inventing logos. Licence-safe fonts only (Google Fonts via `scripts/fetch_fonts.py`).
- **Minimal change** when the user asks for one edit: touch only that.
- **Original kept:** never overwrite the source; work on copies in `work/`.
- **Language:** reply in the user's language (Roman Urdu stays Roman Urdu). Headline language = audience language unless told.
- **Defaults:** YouTube 1280×720, sRGB, JPG q≈90 ≤2 MB (PNG only if text sharpness needs it and it stays under the limit).
- **The final file must be opened and looked at** before delivery. Failing QA is not deliverable.

## Ambiguity
Proceed on the best professional guess and state the assumption in one line. Ask only when: two photos with unclear roles, no topic and no context, or exact factual wording is at stake.

## Output naming
`<project>_<platform>_<concept>_v<N>.jpg` — e.g. `wealthtalk_yt_cinematic_v1.jpg`. Variants: `_A`, `_B`, `_C`.

## Skill maintenance
A bad output means a missing rule. Add it to the matching `references/` file, not here — keep this file under ~150 lines. Re-run `evals/test-prompts.md` after any edit. New client → new file in `assets/brand-kits/`.
