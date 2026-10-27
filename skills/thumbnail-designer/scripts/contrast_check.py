#!/usr/bin/env python3
"""WCAG contrast + mobile-size preview.
  python contrast_check.py --fg "#FFFFFF" --bg "#111111"
  python contrast_check.py --image t.jpg --box 60,400,700,200 --fg "#FFFFFF"   # text box vs real pixels
  python contrast_check.py --image t.jpg --preview                             # writes t_preview168.png (+ grayscale)

--box measures the headline colour against the pixels BEHIND it. On a finished thumbnail the
glyphs are themselves in the box, so pixels close to --fg are excluded by default (they are the
text, not the backdrop); pass --include-text to measure every pixel instead.
Target: >= 4.5 (large headline text >= 3.0 minimum)."""
import argparse
from PIL import Image

def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lum(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def verdict(r):
    return "PASS" if r >= 4.5 else ("OK for large text only" if r >= 3 else "FAIL")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fg"); ap.add_argument("--bg")
    ap.add_argument("--image"); ap.add_argument("--box", help="x,y,w,h text region")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--include-text", action="store_true",
                    help="measure every pixel in --box, glyphs included")
    a = ap.parse_args()

    if a.fg and a.bg:
        r = ratio(hex_rgb(a.fg), hex_rgb(a.bg))
        print(f"contrast {r:.2f}:1  {verdict(r)}")
    if a.image and a.box and a.fg:
        x, y, w, h = (int(v) for v in a.box.split(","))
        region = Image.open(a.image).convert("RGB").crop((x, y, x + w, y + h))
        b = region.tobytes()
        px = list(zip(b[0::3], b[1::3], b[2::3]))
        fgl = hex_rgb(a.fg)
        all_ratios = [ratio(fgl, p) for p in px]
        if a.include_text:
            kept = all_ratios
        else:
            # Drop pixels that are essentially the text itself (near-zero contrast with fg).
            kept = [r for r in all_ratios if r >= 1.6]
            share = 100 * (1 - len(kept) / max(1, len(all_ratios)))
            print(f"excluded {share:.0f}% of the box as glyph pixels "
                  f"(--include-text to keep them)")
        if not kept:
            print("text vs bg pixels: the whole box is the text colour - widen the box or "
                  "sample the background before the text layer is composited")
        else:
            kept.sort()
            worst = kept[int(len(kept) * 0.05)]   # 5th percentile = the bad spots
            med = kept[len(kept) // 2]
            print(f"text vs bg pixels: median {med:.2f}:1, worst-5% {worst:.2f}:1  {verdict(worst)}")
    if a.image and a.preview:
        img = Image.open(a.image).convert("RGB")
        base = a.image.rsplit(".", 1)[0]
        small = img.resize((168, round(168 * img.height / img.width)), Image.LANCZOS)
        small.resize((small.width * 4, small.height * 4), Image.NEAREST).save(base + "_preview168.png")
        small.convert("L").resize((small.width * 4, small.height * 4), Image.NEAREST).save(base + "_preview168_gray.png")
        print(f"wrote {base}_preview168.png and _gray.png (view them: is the idea + headline readable?)")

if __name__ == "__main__":
    main()
