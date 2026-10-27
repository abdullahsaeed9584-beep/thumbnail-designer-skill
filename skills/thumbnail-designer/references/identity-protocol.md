# Identity & Hair Preservation (mandatory when a person's photo is used)

Original photo = authoritative source of identity.

## Preserve
Face shape/geometry, eyes/eyelids/brows/spacing, nose, lips/teeth/smile, ears, jaw/chin/cheeks, skin texture + marks, beard/stubble boundaries, hairstyle/hairline/parting/direction, visible strands + flyaways, neck/body/pose/clothing (unless user asks otherwise).

## Forbidden
Face swap · generative face restoration · reshaping · eye/nose/jaw edits · artificial smoothing · beauty filters · regenerating or redesigning hair · generative inpaint/outpaint on face/hair · forcing pose to match a reference via generation.

## Method
1. Copy original to `work/original.*`; never modify.
2. Non-destructive: separate layers (PNG/RGBA), masks, adjustments applied to copies.
3. Use original pixels for subject. Background/graphics built separately, composited behind.
4. Light/color changes selective, protect face + hair detail.
5. Cutout: Tier 1 → try existing alpha (user PNG) first; else `rembg`/OpenCV only if installable (network is limited: pip works, model download may not). Inspect edges at 300% zoom. If hair edge is poor: (a) ask for pre-cut PNG / plain-background photo, (b) keep original background and design around it, (c) feather edge + disclose limitation. Never "fix" hair by painting/generating.
6. Rim light: soft gradient behind the mask edge, never painted outlines over strands.
7. Compare original vs final side by side (crop face, same scale). Reject any change.

## Edge checklist
Halos (white/dark) · jagged outline · missing flyaways · over-smooth hair boundary · color spill from old background · ears/hairline/beard/glasses/fingers · hard mask transition.

## Claims
Say "original pixels used, no generative edits on face/hair" only if true for the method used. Never promise "every strand guaranteed" without verification. If expression is wrong for the concept → ask for another photo, don't synthesize.

## Skin tone requests
Restrained, realistic tonal correction only; keep texture; no identity change.

## Multiple people
Same protocol per person. Don't combine people/scenes to imply an event that didn't happen.

## Third-party and stock faces (not the user's own photo)

A licence is not a model release. CC0, public-domain and Unsplash-style terms grant
**copyright** permission; they almost never grant the right to use an identifiable person's
likeness to advertise something.

**Never put a stranger's face on a commercial offer** - a gig image, a service ad, a product
page, a course sales thumbnail. It implies that person provides or endorses the thing, and a
buyer reasonably assumes that is who they are hiring. That is a false depiction under this
skill's honesty rules, whatever the image licence says.

Order of preference whenever a face is wanted:
1. **The user's own photo.** Free, legally clean, and it converts better - people hire people.
2. A person who has given the user explicit permission, or a properly model-released library
   the user pays for and names.
3. No face. A strong object, device, type-hero or illustration beats a borrowed face.

Also never acceptable: a real public figure implying endorsement, an AI-generated face passed
off as the seller or a customer, or a face swapped onto another body.

If the user asks for a stock face anyway, say once why it is a problem, offer the three options
above, and build the layout so their own photo drops straight in.
