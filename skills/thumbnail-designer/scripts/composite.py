#!/usr/bin/env python3
"""Composite a cut-out subject onto a background with premium lighting.

  python composite.py bg.jpg subject.png out.png \
      --pos right --scale 0.95 --bg-blur 22 --bg-desat 15 \
      --shadow 0.55 --rim "#00E5FF" --rim-width 6 --match 0.35

Builds, in order: bg depth -> cast/contact shadow -> rim light -> colour match -> subject.
The subject's own pixels are never regenerated; only exposure/temperature are nudged
(see references/identity-protocol.md). Face and hair detail stay untouched.
"""
import argparse
import sys

try:
    from PIL import Image, ImageEnhance, ImageFilter, ImageChops
except ImportError:
    sys.exit("needs Pillow:  python -m pip install pillow")
try:
    import numpy as np
except ImportError:
    np = None


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cover(img, W, H, fx=0.5, fy=0.5):
    sw, sh = img.size
    s = max(W / sw, H / sh)
    img = img.resize((round(sw * s), round(sh * s)), Image.LANCZOS)
    nw, nh = img.size
    left = min(max(round(fx * nw - W / 2), 0), nw - W)
    top = min(max(round(fy * nh - H / 2), 0), nh - H)
    return img.crop((left, top, left + W, top + H))


def place(canvas_size, subj, where, scale, dx, dy):
    W, H = canvas_size
    target_h = int(H * scale)
    s = target_h / subj.height
    subj = subj.resize((max(1, round(subj.width * s)), target_h), Image.LANCZOS)
    anchors = {"left": 0.26, "center": 0.5, "right": 0.74}
    cx = anchors.get(where, 0.74) * W
    x = round(cx - subj.width / 2) + dx
    y = H - subj.height + dy          # feet at the bottom edge
    return subj, (x, y)


def shadow_layer(size, subj, pos, opacity, blur, offset):
    """Soft cast shadow + tighter dark contact shadow = ambient occlusion."""
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    alpha = subj.split()[-1]
    passes = (
        (blur, opacity * 0.65, offset),
        (max(2, blur // 4), opacity, (offset[0] // 3, max(2, offset[1] // 3))),
    )
    for b, o, off in passes:
        sh = Image.new("RGBA", size, (0, 0, 0, 0))
        tint = Image.new("RGBA", subj.size, (0, 0, 0, 255))
        tint.putalpha(alpha.point(lambda v, o=o: int(v * o)))
        sh.paste(tint, (pos[0] + off[0], pos[1] + off[1]), tint)
        lay = Image.alpha_composite(lay, sh.filter(ImageFilter.GaussianBlur(b)))
    return lay


def rim_layer(size, subj, pos, colour, width, strength, direction):
    """Coloured glow behind the mask edge - never painted over hair strands."""
    alpha = subj.split()[-1]
    grow = alpha.filter(ImageFilter.MaxFilter(max(3, width * 2 + 1)))
    edge = ImageChops.subtract(grow, alpha)
    edge = edge.filter(ImageFilter.GaussianBlur(max(1.0, width * 0.55)))
    edge = edge.point(lambda v: int(min(255, v * strength)))
    tint = Image.new("RGBA", subj.size, colour + (255,))
    tint.putalpha(edge)
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    offsets = {"left": (-width, -width), "right": (width, -width),
               "top": (0, -width * 2), "back": (0, 0)}
    ox, oy = offsets.get(direction, (width, -width))
    lay.paste(tint, (pos[0] + ox, pos[1] + oy), tint)
    return lay


def colour_match(subj, bg, amount):
    """Pull the subject's mean colour toward the background's - kills the pasted look.
    Global, gentle, texture-preserving: no pixel is regenerated."""
    if amount <= 0 or np is None:
        return subj
    a = np.asarray(subj, dtype=np.float32)
    rgb, al = a[..., :3], a[..., 3:4]
    m = al[..., 0] > 32
    if not m.any():
        return subj
    b = np.asarray(bg.convert("RGB"), dtype=np.float32)
    delta = b.reshape(-1, 3).mean(0) - rgb[m].mean(0)
    rgb = np.clip(rgb + delta * amount * (al / 255.0), 0, 255)
    return Image.fromarray(np.concatenate([rgb, al], -1).astype("uint8"), "RGBA")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("background")
    ap.add_argument("subject")
    ap.add_argument("output")
    ap.add_argument("--size", default="1280x720")
    ap.add_argument("--pos", default="right", choices=["left", "center", "right"])
    ap.add_argument("--scale", type=float, default=0.95,
                    help="subject height as a fraction of the canvas")
    ap.add_argument("--dx", type=int, default=0)
    ap.add_argument("--dy", type=int, default=0)
    ap.add_argument("--bg-focus", default="0.5,0.5")
    ap.add_argument("--bg-blur", type=float, default=20, help="px of background blur")
    ap.add_argument("--bg-desat", type=float, default=12, help="percent")
    ap.add_argument("--bg-darken", type=float, default=0, help="percent")
    ap.add_argument("--shadow", type=float, default=0.55, help="0-1 opacity, 0 = off")
    ap.add_argument("--shadow-blur", type=int, default=28)
    ap.add_argument("--shadow-offset", default="18,16")
    ap.add_argument("--rim", help="hex colour, e.g. #00E5FF")
    ap.add_argument("--rim-width", type=int, default=6)
    ap.add_argument("--rim-strength", type=float, default=1.3)
    ap.add_argument("--rim-dir", default="right", choices=["left", "right", "top", "back"])
    ap.add_argument("--match", type=float, default=0.3,
                    help="0-1 colour match toward the background")
    ap.add_argument("--text-layer",
                    help="transparent PNG composited UNDER the subject (masked-behind depth)")
    ap.add_argument("--over-layer",
                    help="transparent PNG composited OVER everything (cues, foreground bokeh)")
    a = ap.parse_args()

    W, H = (int(v) for v in a.size.lower().split("x"))
    fx, fy = (float(v) for v in a.bg_focus.split(","))

    bg = cover(Image.open(a.background).convert("RGB"), W, H, fx, fy)
    if a.bg_blur > 0:
        bg = bg.filter(ImageFilter.GaussianBlur(a.bg_blur))
    if a.bg_desat:
        bg = ImageEnhance.Color(bg).enhance(max(0.0, 1 - a.bg_desat / 100))
    if a.bg_darken:
        bg = ImageEnhance.Brightness(bg).enhance(max(0.0, 1 - a.bg_darken / 100))
    canvas = bg.convert("RGBA")

    subj = Image.open(a.subject).convert("RGBA")
    if subj.split()[-1].getextrema()[0] == 255:
        print("warning: subject PNG has no transparency - cut it out first "
              "(existing alpha / rembg)")
    subj, pos = place((W, H), subj, a.pos, a.scale, a.dx, a.dy)

    if a.text_layer:
        tl = Image.open(a.text_layer).convert("RGBA")
        if tl.size != (W, H):
            tl = tl.resize((W, H), Image.LANCZOS)
        canvas = Image.alpha_composite(canvas, tl)

    if a.shadow > 0:
        off = tuple(int(v) for v in a.shadow_offset.split(","))
        canvas = Image.alpha_composite(
            canvas, shadow_layer((W, H), subj, pos, a.shadow, a.shadow_blur, off))
    if a.rim:
        canvas = Image.alpha_composite(
            canvas, rim_layer((W, H), subj, pos, hex_rgb(a.rim),
                              a.rim_width, a.rim_strength, a.rim_dir))

    subj = colour_match(subj, bg, a.match)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.paste(subj, pos, subj)
    canvas = Image.alpha_composite(canvas, layer)

    if a.over_layer:
        ol = Image.open(a.over_layer).convert("RGBA")
        if ol.size != (W, H):
            ol = ol.resize((W, H), Image.LANCZOS)
        canvas = Image.alpha_composite(canvas, ol)

    out = canvas if a.output.lower().endswith(".png") else canvas.convert("RGB")
    out.save(a.output)
    print("{}  {}x{}  subject@{} scale={} bg_blur={} shadow={} rim={} match={}".format(
        a.output, W, H, pos, a.scale, a.bg_blur, a.shadow, a.rim or "none", a.match))
    print("next: python finish.py {} final.jpg --preset cinematic --max-bytes 2000000".format(a.output))
    if np is None:
        print("note: numpy missing - colour match skipped")


if __name__ == "__main__":
    main()
