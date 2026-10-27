# Case Routing

Cases combine - don't treat them as exclusive. Every build also obeys `premium-standard.md`, `render-pipeline.md` and `scorecard.md`.

## A. Topic only
Understand the audience, pick the strongest honest visual concept, write the headline (`hooks.md`), choose subject/composition/palette, build background and supporting elements, set type, add only purposeful effects. Don't ask about fonts, colours or shadows - decide.

## B. Video title given
Extract the subject and the claim, find the strongest visual reading, write a headline that *complements* the title (keep the user's wording if it is already short and strong), one focal point, one curiosity gap, never misrepresent the video.

## C. Personal photo
Read `identity-protocol.md` first. Judge photo suitability, decide keep or replace background, design the background and graphics independently, apply selective light and colour, position per composition, keep the headline off the face, then compare face and hair against the original. Wrong expression for the concept? Ask for another photo - never synthesise one.

## D. Reference thumbnail
Analyse: composition, subject scale and placement, background, palette, light direction, type and hierarchy, graphics, depth, mood. "Exact match" means mirror the layout and style closely. "Inspired by" means an original composition using the same principles. Never copy logos, watermarks or proprietary assets.

## E. Photo + reference (high priority)
The photo is identity truth; the reference is design direction only. Map composition, palette, type and background structure, then adapt to the photo's real pose and proportions. Preserve face and hair, build the background independently, verify against both inputs. Never bend a pose or body through generation.

## F. Multiple photos
Infer roles (main, secondary, product, background, reference, before/after, evidence). Unclear *and* material to the result? Ask ONE question. Preserve every person's identity. Never imply an event that didn't happen.

## G. Logo / brand kit
Keep logo proportions and appearance exactly. Use the brand colours and fonts (load `assets/brand-kits/<client>.md`). The logo is secondary to the message unless told otherwise. No stretching, no recolouring. Keep consistency across related thumbnails.

## H. Sketch / layout supplied
Treat it as a composition guide: keep subject position, text location, relative sizes, flow, key objects and empty space. Improve alignment, spacing, balance, lighting and finish.

## I. Improve an existing thumbnail
Diagnose first with `scorecard.md` (hierarchy, contrast, readability, grade, isolation, shadows, clutter, balance, source quality). Keep what works. Fix only the weaknesses - and say what you changed.

## J. One specific edit
Minimal change. Protect everything unaffected: a background-only edit must not touch the face, clothes or text.

## K. Ideas only (no build)
Give 3 genuinely different concepts. Per concept: name - visual idea - focal subject - headline - composition - palette - background - type direction - essential effects - why it fits. Draw directions from: clean editorial, cinematic portrait, bold high-contrast, product/object, data viz, minimalist premium, documentary, text-hero, reference-inspired. If the user actually asked for a finished thumbnail, EXECUTE the strongest one.

## L. Batch
Build a shared style system first (palette, type, layout grid, logo spot), then vary concept, focal point and headline per title. Preserve identity in every output. Export separately with proper names and verify each one. Near-duplicates are a fail.

## M. A/B variants (the one exception to "no near-duplicates")
Default 3 variants, each varying exactly ONE major lever: (A) headline hook, (B) focal point/composition, (C) colour/mood. Same underlying truth about the video. State in one line what differs and the hypothesis. Never claim which will win.

## N. Critique / audit
Run `scorecard.md` in full: 10 axes, 0-4, one line of evidence each. Then the top 3 fixes ordered by impact, what to keep, and an offer to rebuild. Run `thumb_test.py`, `contrast_check.py --preview` and `safe_zone_overlay.py` on any image supplied, and look at the results.

## O. Competitor / niche style analysis
Analyse only images or sources the user supplies. Output: common palettes, layouts, text length, face usage, recurring patterns, and the gaps worth exploiting to differentiate. Never copy branded assets.

## P. Client brief intake (agency use)
Collect only what's missing: platform, title/topic, audience, target emotion, mandatory text, brand kit, assets. Save a new client style to `assets/brand-kits/<client>.md` only if the user asks.

## Q. Image-generation prompts (Canva / Midjourney / Photoshop)
Provide a prompt per element (background, objects) and **never for the protected face**. Include subject, style, light, palette, composition, negative space reserved for text, aspect ratio, and negatives. State clearly that these are prompts, not executed edits.

## R. Vertical cover (Shorts / Reels / TikTok)
9:16, but the grid crops it. Keep the focal point and the hook inside the centre 1080x1350, nothing important in the top 10%, bottom 20% or right 15%. Fewer words than a 16:9 thumbnail - 2-3. Re-check with `safe_zone_overlay.py --platform vertical`.

## S. Channel style system
When the user wants consistency across a channel, define once and save to `assets/brand-kits/<channel>.md`: palette + accent, type pair and treatment, subject treatment (cutout style, rim colour), background family, logo/badge placement, grain and grade preset. Every later thumbnail inherits it; only the concept changes.
