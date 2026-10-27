#!/usr/bin/env python3
"""Draw safe-zone overlay on a thumbnail for visual QA.
  python safe_zone_overlay.py thumb.jpg [--platform yt|vertical|square] [--out overlay.png]
Red = avoid zone, cyan = 4% margin, white = rule-of-thirds."""
import argparse
from PIL import Image, ImageDraw

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--platform", default="yt", choices=["yt", "vertical", "square"])
    ap.add_argument("--out")
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
    out = a.out or a.input.rsplit(".", 1)[0] + "_safezone.png"
    Image.alpha_composite(img, ov).convert("RGB").save(out)
    print(out)

if __name__ == "__main__":
    main()
