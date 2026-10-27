#!/usr/bin/env python3
"""Final mastering pass - the 'cinematic poster' finish.

  python finish.py in.png out.jpg --clarity 15 --grain 2.5 --vignette 10 --sharpen
  python finish.py in.png out.jpg --preset cinematic --max-bytes 2000000
  python finish.py in.png out.jpg --protect 420,90,440,520      # keep this box (face/text) crisp

Order: clarity (local contrast) -> contrast/saturation -> vignette -> grain -> sharpen -> export.
Everything is restrained on purpose; defaults sit inside the premium standard's ranges.
"""
import argparse, os, sys

try:
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
    sys.exit("needs Pillow:  python -m pip install pillow")
try:
    import numpy as np
except ImportError:
    np = None

PRESETS = {
    # clarity, contrast, saturation, vignette, grain, sharpen
    "cinematic":  dict(clarity=18, contrast=1.08, saturation=1.04, vignette=12, grain=2.5, sharpen=True),
    "clean":      dict(clarity=8,  contrast=1.04, saturation=1.02, vignette=6,  grain=1.2, sharpen=True),
    "punchy":     dict(clarity=20, contrast=1.12, saturation=1.10, vignette=10, grain=2.0, sharpen=True),
    "documentary":dict(clarity=14, contrast=1.06, saturation=0.96, vignette=15, grain=3.0, sharpen=True),
    "none":       dict(clarity=0,  contrast=1.0,  saturation=1.0,  vignette=0,  grain=0,   sharpen=False),
}


def clarity(img, amount):
    """Local contrast (Camera Raw 'Texture'/'Clarity'): unsharp at a large radius."""
    if amount <= 0:
        return img
    return img.filter(ImageFilter.UnsharpMask(radius=max(3, img.width // 120),
                                              percent=int(amount * 5), threshold=3))


def vignette(img, percent):
    if percent <= 0:
        return img
    strength = percent / 100.0
    W, H = img.size
    if np is not None:
        yy, xx = np.mgrid[0:H, 0:W]
        cx, cy = W / 2, H / 2
        r = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2) / 1.4142
        mask = np.clip(1.0 - strength * np.clip((r - 0.45) / 0.55, 0, 1) ** 1.6, 0, 1)
        a = np.asarray(img, dtype=np.float32)
        a[..., :3] *= mask[..., None]
        return Image.fromarray(np.clip(a, 0, 255).astype("uint8"), img.mode)
    # Pillow-only fallback: radial gradient via a scaled ellipse
    from PIL import ImageDraw
    m = Image.new("L", (W // 4, H // 4), 0)
    ImageDraw.Draw(m).ellipse([-W // 16, -H // 16, W // 4 + W // 16, H // 4 + H // 16], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(W // 40)).resize((W, H), Image.LANCZOS)
    dark = Image.new(img.mode, (W, H), (0, 0, 0) if img.mode == "RGB" else (0, 0, 0, 255))
    return Image.composite(img, Image.blend(img, dark, strength), m)


def grain(img, percent):
    """Monochromatic film grain - binds composited layers into one photographic image."""
    if percent <= 0 or np is None:
        return img
    a = np.asarray(img, dtype=np.float32)
    rng = np.random.default_rng(7)
    n = rng.normal(0, percent * 2.55, (img.height, img.width, 1))
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255)
    return Image.fromarray(a.astype("uint8"), img.mode)


def parse_box(s):
    x, y, w, h = (int(v) for v in s.split(","))
    return (x, y, x + w, y + h)


def save(img, path, max_bytes):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        img = img.convert("RGB")
        q = 92
        while True:
            img.save(path, "JPEG", quality=q, optimize=True, subsampling=0)
            size = os.path.getsize(path)
            if not max_bytes or size <= max_bytes or q <= 60:
                return q, size
            q -= 4
    img.save(path)
    return None, os.path.getsize(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--preset", choices=list(PRESETS), help="start from a preset, then override")
    ap.add_argument("--clarity", type=float); ap.add_argument("--contrast", type=float)
    ap.add_argument("--saturation", type=float); ap.add_argument("--vignette", type=float)
    ap.add_argument("--grain", type=float); ap.add_argument("--sharpen", action="store_true")
    ap.add_argument("--protect", help="x,y,w,h kept pristine (face / headline)")
    ap.add_argument("--max-bytes", type=int, default=0)
    a = ap.parse_args()

    cfg = dict(PRESETS[a.preset]) if a.preset else dict(PRESETS["clean"])
    for k in ("clarity", "contrast", "saturation", "vignette", "grain"):
        if getattr(a, k) is not None:
            cfg[k] = getattr(a, k)
    if a.sharpen:
        cfg["sharpen"] = True

    src = Image.open(a.input)
    img = src.convert("RGBA" if src.mode in ("RGBA", "LA", "P") and a.output.lower().endswith(".png") else "RGB")
    keep = img.crop(parse_box(a.protect)) if a.protect else None

    img = clarity(img, cfg["clarity"])
    if cfg["contrast"] != 1.0:
        img = ImageEnhance.Contrast(img).enhance(cfg["contrast"])
    if cfg["saturation"] != 1.0:
        img = ImageEnhance.Color(img).enhance(cfg["saturation"])
    img = vignette(img, cfg["vignette"])
    img = grain(img, cfg["grain"])
    if cfg["sharpen"]:
        img = img.filter(ImageFilter.UnsharpMask(radius=1.1, percent=95, threshold=3))
    if keep is not None:
        box = parse_box(a.protect)
        soft = ImageEnhance.Contrast(clarity(keep, cfg["clarity"] * 0.4)).enhance(1.0)
        img.paste(soft, box[:2])

    q, size = save(img, a.output, a.max_bytes)
    note = f"q={q} " if q else ""
    print(f"{a.output}  {img.width}x{img.height}  {note}{size/1024:.0f} KB  "
          f"[clarity {cfg['clarity']} contrast {cfg['contrast']} sat {cfg['saturation']} "
          f"vignette {cfg['vignette']}% grain {cfg['grain']}%]")
    if np is None:
        print("note: numpy missing - grain skipped, vignette used the fallback path")


if __name__ == "__main__":
    main()
