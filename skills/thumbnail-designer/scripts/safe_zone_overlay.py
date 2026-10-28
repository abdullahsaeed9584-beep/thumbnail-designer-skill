#!/usr/bin/env python3
"""Draw safe-zone overlay on a thumbnail for visual QA.
  python safe_zone_overlay.py thumb.jpg [--platform yt|vertical|square] [--out overlay.png]
Red = avoid zone, cyan = 4% margin, white = rule-of-thirds."""
import argparse
from PIL import Image, ImageDraw
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from scratch import proof_dir, proof_path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--platform", default="yt",
                    choices=["yt", "vertical", "square", "ytbanner"])
    ap.add_argument("--out")
    ap.add_argument("--here", action="store_true",
                    help="write beside the source instead of the temp proof folder")
    a = ap.parse_args()
    img = Image.open(a.input).convert("RGBA")
    W, H = img.size
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    m = 0.04
    d.rectangle([W*m, H*m, W*(1-m), H*(1-m)], outline=(0, 255, 255, 230), width=max(2, W//400))
    for i in (1, 2):
        d.line([W*i/3, 0, W*i/3, H], fill=(255, 255, 255, 140), width=2)
        d.line([0, H*i/3, W, H*i/3], fill=(255, 255, 255, 140), width=2)
    red = (255, 0, 0, 90)
    if a.platform == "yt":
        d.rectangle([W*0.88, H*0.88, W, H], fill=red)      # timestamp badge
    elif a.platform == "vertical":
        d.rectangle([0, 0, W, H*0.10], fill=red)           # top UI
        d.rectangle([0, H*0.80, W, H], fill=red)           # caption/buttons
        d.rectangle([W*0.85, 0, W, H], fill=red)           # right action rail
    elif a.platform == "ytbanner":
        # A channel banner is uploaded at 2560x1440 but almost nobody ever sees that
        # rectangle. Mobile shows the centre 1546x423; TV shows the whole 2560x1440;
        # desktop shows roughly 2560x423. So everything that must be read - the name,
        # the logo, the one line of copy - lives inside the centre 1546x423, and the
        # rest is scenery that gets cropped away. The green box is that safe area.
        sw, sh = 1546 / 2560, 423 / 1440
        x0, y0 = W * (1 - sw) / 2, H * (1 - sh) / 2
        x1, y1 = W * (1 + sw) / 2, H * (1 + sh) / 2
        d.rectangle([0, 0, W, y0], fill=red)               # cropped on mobile
        d.rectangle([0, y1, W, H], fill=red)
        d.rectangle([0, y0, x0, y1], fill=red)
        d.rectangle([x1, y0, W, y1], fill=red)
        d.rectangle([x0, y0, x1, y1], outline=(0, 255, 120, 255), width=max(3, W // 500))
        # desktop strip: full width, same height band
        d.rectangle([0, y0, W, y1], outline=(255, 210, 0, 200), width=max(2, W // 900))
    # Proofs are evidence for whoever is doing the work, not deliverables.
    # Writing them beside the artwork is how a delivery folder fills up.
    out = a.out or proof_path(a.input, "_safezone.png", here=a.here)
    Image.alpha_composite(img, ov).convert("RGB").save(out)
    print(out)

if __name__ == "__main__":
    main()
