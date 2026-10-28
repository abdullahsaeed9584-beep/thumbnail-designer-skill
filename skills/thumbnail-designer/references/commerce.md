# Commerce — product images, listings and marketplace graphics

The rules here are not aesthetic. A listing image that breaks a marketplace's spec gets
suppressed, and a listing image that flatters the product gets returns. Both cost the
user money, so both are correctness problems.

---

## 1. The product is evidence, not raw material

**Never alter what the buyer is paying for.** No reshaping, no slimming a bottle, no
deepening a colour, no removing a seam or a logo, no adding a feature that is not there,
no compositing in an accessory that is not in the box. Colour correction to match the
real item is right; colour *enhancement* past it is misrepresentation.

If the supplied photo is too poor to sell from, say so and ask for a better one. A bad
photo honestly presented beats a good photo of something the buyer will not receive.

Never invent specifications, dimensions, materials, certifications, compatibility,
ratings, review counts, "bestseller" badges or before/after results. Everything written
on a listing graphic comes from the user.

---

## 2. Marketplace specs

Platforms change these. Verify against the platform's current help page when a listing
depends on an exact number — and say that you did or did not.

| Platform | Main image | Notes |
|---|---|---|
| Amazon | ≥1000 px longest side (1600+ recommended for zoom), JPG/PNG | **Main image: pure white background (RGB 255,255,255), product filling ~85% of frame, no text, no logos, no props, no borders.** Secondary images may have lifestyle, text and infographics |
| eBay | ≥500 px, 1600 recommended | no added text or borders on the primary image |
| Etsy | 2000×2000 recommended, square | first image is cropped square in search |
| Shopify / own store | 2048×2048 square | consistent crop and padding across the catalogue matters more than any single shot |
| Daraz / Jumia / regional | typically 1000×1000, white background | check the local spec; they diverge |
| Google Shopping | ≥800 px | no promotional text or watermarks in the feed image |

**The rule behind the rules:** the *first* image is the product on white, alone. Everything
persuasive — callouts, lifestyle, comparisons, sizing — goes in images two onward.

---

## 3. The image set that actually sells

1. **Hero** — product on white, correct proportions, square, consistent padding
2. **Scale** — next to something everyone knows, or with real dimensions labelled
3. **Detail** — the material, the stitching, the port, the thing the photos usually hide
4. **In use** — a real context, lit consistently with the hero
5. **What's in the box** — flat lay, counted, honest
6. **Feature callouts** — three to five, each pointing at a visible part of the product
7. **Comparison / sizing chart** — only with the user's real numbers

Keep one lighting direction and one background treatment across the whole set. An
inconsistent set reads as drop-shipped.

---

## 4. Callout graphics without lying

- Point the line at the actual feature in the actual photograph. A callout floating
  beside the product is decoration.
- Two to four words per callout. "Machine washable", not a sentence.
- Use the product's own colours for the accent so the graphics belong to the picture.
- **Icons must be literal.** A shield for "waterproof" means nothing; say waterproof.
- If a claim needs a qualifier ("tested to IP67"), include the qualifier or drop the claim.

Build with `showcase.html` (general product/feature layout) or `photo-split.html` when a
real photograph carries one side. `product-led.html` for a single hero object.

---

## 5. Sale, bundle and promo graphics

- A discount figure is arithmetic the user supplies. Never calculate a percentage from
  invented prices, and never show a struck-through "was" price the user has not confirmed.
- Urgency language ("ends tonight") is the user's claim, not yours. If it is not true it
  is a consumer-protection problem, not a design choice.
- Keep the price legible at thumbnail scale — listing grids render small.
- Regional pricing: keep the currency and formatting the user used. Rs. 2,499 is not
  $2,499 and the separator convention differs by market.

---

## 6. Checks before handing over

- [ ] Main image: white background, no text, no logo, no border, correct fill ratio
- [ ] Minimum pixel size met for the named platform, square where required
- [ ] Product shape, colour and branding unaltered — compare against the original crop
- [ ] Every number, size, material and claim traceable to something the user supplied
- [ ] Set is visually consistent — one light direction, one background family
- [ ] Legible in a search grid (`thumb_test.py` works for this: it is the same problem)
- [ ] Text re-read on the rendered pixels, not in the command that made it

Related: `niche-guide.md` (e-commerce row), `deliverables.md`, `platform-specs.md`,
`print-production.md` (packaging and labels), `qa-export.md`.
