#!/usr/bin/env python3
"""Smart-crop + resize a thumbnail to platform presets.
Usage: python resize.py in.jpg --presets yt,ig_feed,fb_link --out outdir [--focus 0.5,0.4]
       python resize.py in.jpg --presets all --focus 0.68,0.42
--focus = focal point as fractions (x,y) so the crop keeps the subject.
JPG output is re-encoded until it fits the preset max size (if any).
Always re-check safe zones after a re-crop: safe_zone_overlay.py."""
import argparse, os, sys
from PIL import Image

PRESETS = {  # name: (w, h, max_bytes or None)
    "yt": (1280, 720, 2_000_000),
    "yt_hd": (1920, 1080, 2_000_000),
    "vertical": (1080, 1920, None),
    "shorts": (1080, 1920, None),
    "ig_feed": (1080, 1350, None),
    "ig_square": (1080, 1080, None),
    "fb_link": (1200, 630, None),
    "fb_cover": (820, 312, None),
    "linkedin": (1200, 627, None),
    "x_post": (1200, 675, None),
    "og": (1200, 630, None),
    "podcast": (3000, 3000, None),
}
ALL = "yt,vertical,ig_feed,fb_link,linkedin,og"

def cover_crop(img, w, h, fx, fy):
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = min(max(round(fx * nw - w / 2), 0), nw - w)
    top = min(max(round(fy * nh - h / 2), 0), nh - h)
    return img.crop((left, top, left + w, top + h))

def save(img, path, max_bytes):
    img = img.convert("RGB")
    q = 92
    while True:
        img.save(path, "JPEG", quality=q, optimize=True)
        if not max_bytes or os.path.getsize(path) <= max_bytes or q <= 60:
            return q, os.path.getsize(path)
        q -= 4

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--presets", default="yt", help='comma list, or "all" for the common set')
    ap.add_argument("--out", default="resized")
    ap.add_argument("--focus", default="0.5,0.5")
    a = ap.parse_args()
    fx, fy = (float(v) for v in a.focus.split(","))
    os.makedirs(a.out, exist_ok=True)
    img = Image.open(a.input)
    base = os.path.splitext(os.path.basename(a.input))[0]
    names = ALL.split(",") if a.presets == "all" else a.presets.split(",")
    for name in names:
        if name not in PRESETS:
            sys.exit(f"unknown preset {name}; options: {', '.join(PRESETS)}")
        w, h, mb = PRESETS[name]
        out = os.path.join(a.out, f"{base}_{name}.jpg")
        q, size = save(cover_crop(img, w, h, fx, fy), out, mb)
        print(f"{out}  {w}x{h}  q={q}  {size/1024:.0f} KB")

if __name__ == "__main__":
    main()
