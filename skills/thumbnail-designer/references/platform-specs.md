# Platform Specs

Platforms change - verify current values if a job depends on an exact number.

| Platform | Size (px) | Ratio | `resize.py` preset | Notes |
|---|---|---|---|---|
| YouTube thumbnail | 1280x720 (min width 640) | 16:9 | `yt` | JPG/PNG/GIF/WEBP, max 2 MB. Duration badge bottom-right. Test at ~168x94 |
| YouTube 1080 | 1920x1080 | 16:9 | `yt_hd` | Same rules, more headroom for type |
| Shorts / Reels / TikTok cover | 1080x1920 | 9:16 | `vertical` | Keep key content in the centre ~1080x1350. UI covers the bottom ~20% and the right rail; grids may crop to 1:1, 3:4 or 4:5 |
| Instagram feed | 1080x1350 | 4:5 | `ig_feed` | Profile grid crops to centre square - keep the focal point middle |
| Facebook link/post | 1200x630 | 1.91:1 | `fb_link` | Keep text away from the edges |
| Facebook page cover | 820x312 (mobile-safe centre ~640x312) | ~2.63:1 | `fb_cover` | Mobile crops the sides hard |
| LinkedIn post/link | 1200x627 | 1.91:1 | `linkedin` | Clean, text-light, professional |
| X / Twitter post | 1200x675 | 16:9 | `x_post` | Timeline crops tall images |
| Blog / OG image | 1200x630 | 1.91:1 | `og` | Title must read in a small link preview |
| Fiverr gig image | 1280x769 (min 712x430, max 4000x2416) | ~1.665:1 | `fiverr` | Fiverr's own recommendation, 72 DPI, landscape. Up to 3 images per gig. NOT 16:9 - a 1280x720 export gets letterboxed or cropped |
| Podcast cover | 3000x3000 (min 1400) | 1:1 | `podcast` | Must read at 150x150 |
| Course cover | 1280x720 or 1920x1080 | 16:9 | `yt` / `yt_hd` | Follow the host platform's own rule |

## Safe zones
- General: 4% clear margin minimum on every edge.
- YouTube: keep the bottom-right 12% w x 12% h clear (duration badge).
- Vertical: nothing important in the top 10%, bottom 20%, or right 15%.
- Square/podcast: assume a centre crop and small display.
- Fiverr: the search grid shows the image around 300px wide with the seller block beneath it, so keep type large but don't fear a support line the way a 168px YouTube thumbnail must.
Check visually: `python scripts/safe_zone_overlay.py out.jpg --platform yt|vertical|square`.

## Multi-platform resize
Never just squash. Re-crop around the focal point (`scripts/resize.py --focus 0.68,0.42`), re-balance the text size for the new canvas, and re-check safe zones. If the crop breaks the composition, rebuild the layout for that ratio instead - a 16:9 design forced into 9:16 always looks wrong.

## File rules
sRGB. JPG at q~90, stepping down until it fits the limit (`finish.py --max-bytes`). PNG only when text sharpness demands it and the file still fits. Name per `SKILL.md`.

## Beyond thumbnails - general design canvases

The craft is the same; only the canvas and safe zones change.

| Use | Size (px) | Notes |
|---|---|---|
| Instagram post / carousel | 1080x1350 (4:5) or 1080x1080 | Grid crops to square - keep the focal point centred |
| Instagram / Facebook story | 1080x1920 | Top 10% and bottom 20% are UI |
| YouTube channel banner | 2560x1440, safe area 1546x423 | Everything that matters inside the safe area |
| X / Twitter header | 1500x500 | Avatar overlaps the lower left |
| LinkedIn banner | 1584x396 | Avatar overlaps the left |
| Display ad (MPU / leaderboard) | 300x250 / 728x90 / 160x600 | Tiny - one message, huge type, no fine detail |
| Presentation slide | 1920x1080 | Readable from the back of a room: body text 24pt+ |
| Poster, print | A4 2480x3508, A3 3508x4961 at 300 DPI | Add 3mm bleed if it goes to a printer; CMYK conversion is the printer's job, design in sRGB |
| Flyer, print | A5 1748x2480 at 300 DPI | As above |
| Album / book cover | 3000x3000 | Must read at 150x150 |
| Email header | 1200x400 | Many clients block images - never put the only message in the image |

For print, work at 300 DPI, keep text away from the trim edge by at least 5mm, and remember
that saturated RGB cyans and greens will shift when converted. Deliver a PDF or a 300 DPI PNG
and say which colour space it is in.
