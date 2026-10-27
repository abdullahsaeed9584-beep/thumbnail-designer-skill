# QA + Export

Verify what applies - and actually open the images. Nothing here may be assumed.

## Automated
```
python scripts/thumb_test.py out.jpg --competitors comp1.jpg comp2.jpg
python scripts/contrast_check.py --image out.jpg --box 60,400,700,200 --fg "#FFFFFF"
python scripts/safe_zone_overlay.py out.jpg --platform yt
```
`thumb_test.py` exits 1 on a hard failure (ratio, pixel size, file size, flat luminance). Fix, then re-run.

## By eye (cannot be automated - open the files)
**IDENTITY** - face geometry and proportions unchanged - eyes/nose/lips/ears/jaw intact - hairstyle, hairline and flyaway strands intact - no regeneration - no smoothing. Compare a face crop against the original at the same scale.
**IMAGE** - exposure - contrast - natural skin - controlled saturation - no destructive sharpening - no clipping, banding or colour casts.
**COMPOSITING** - clean edges, no halos - perspective - one light direction - realistic contact and cast shadow - rim light keyed to the background - natural blend.
**DESIGN** - one focal point - clear hierarchy - negative space - balance - purposeful graphics - no clutter - three depth layers.
**TYPE** - spelling - numbers - readable at 168 px - appropriate face - spacing - no distortion - safe margins - (Urdu) shaping, joins and RTL order correct.
**EXPORT** - ratio - pixel size - format - sRGB - under the platform file limit - the file actually opens.
**HONESTY** - no fabricated data or claims - matches the video - limitations disclosed.

## Score before shipping
`references/scorecard.md` - 10 axes, 0-4 each. **Ship at 32/40 or above, with no axis at 0**, and the honesty axis never at 0. Below that: fix and re-test. If something is unfixable in the current tier, say so plainly rather than shipping it quietly.

## Deliverables
1. Final image(s), presented.
2. The original kept separately and unmodified.
3. Editable source where the tool supports it - PSD is not producible in Tier 1; offer the layered PNGs plus the HTML/script that generated it.
4. Font and asset list, licence-safe.
5. A 1-3 line note: tier used, assumptions made, limitations.
Never invent a download link or claim an editable file that doesn't exist.
