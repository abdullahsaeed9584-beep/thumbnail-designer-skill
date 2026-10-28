#!/usr/bin/env python3
"""The proof sheet. Renders the four tests a premium thumbnail must survive.

  python thumb_test.py out.jpg
  python thumb_test.py out.jpg --outdir work/tests --competitors a.jpg b.jpg

Writes (and you must LOOK at each one):
  *_01_mobile.png   ~168 px wide, upscaled nearest  -> is the idea still readable?
  *_02_gray.png     grayscale                       -> does contrast hold without colour?
  *_03_squint.png   heavy blur                      -> is there exactly ONE focal point?
  *_04_feed.png     mock feed row beside neighbours -> does it stand out?
  *_sheet.png       all of the above on one canvas
Exit code 1 if a measurable check fails (ratio, pixel size, file size, flat contrast).
"""
import argparse
import os
import sys
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from scratch import proof_dir, proof_path

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    sys.exit("needs Pillow:  python -m pip install pillow")

MOBILE_W = 168           # YouTube mobile feed thumbnail width, roughly
SPEC = {
    "16:9": (1280, 720, 2_000_000),
    "9:16": (1080, 1920, None),
    "4:5": (1080, 1350, None),
    # 1000 is the marketplace floor (Amazon/eBay/Daraz listing images), NOT the
    # podcast floor. A 1:1 canvas is a listing at least as often as it is a podcast
    # cover, and failing a perfectly valid 1200x1200 listing trains people to ignore
    # the checker. The podcast minimum is handled as a note below instead.
    "1:1": (1000, 1000, None),
    # Fiverr gig images are 1280x769, not 16:9 - without this entry a correct
    # gig image is reported as "not a clean platform ratio".
    "1280:769": (1280, 769, None),
}


def nearest_ratio(w, h):
    r = w / h
    best, diff = None, 9e9
    for name in SPEC:
        a, b = name.split(":")
        d = abs(r - int(a) / int(b))
        if d < diff:
            best, diff = name, d
    return best, diff


def up(img, factor=4):
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)


def mobile(img):
    h = max(1, round(MOBILE_W * img.height / img.width))
    return img.resize((MOBILE_W, h), Image.LANCZOS)


def label(img, text):
    out = Image.new("RGB", (img.width, img.height + 26), (18, 18, 20))
    out.paste(img.convert("RGB"), (0, 26))
    ImageDraw.Draw(out).text((8, 7), text, fill=(235, 235, 240))
    return out


def feed_mock(img, competitors):
    """A row of 3 thumbnails as a viewer sees them, ours in the middle."""
    tw, th = 320, 180
    cells = []
    for c in competitors[:2]:
        try:
            cells.append(Image.open(c).convert("RGB").resize((tw, th), Image.LANCZOS))
        except Exception:
            cells.append(None)
    while len(cells) < 2:
        cells.append(None)
    placeholder = Image.new("RGB", (tw, th), (52, 52, 58))
    d = ImageDraw.Draw(placeholder)
    d.text((10, th // 2 - 6), "(no competitor supplied)", fill=(140, 140, 150))
    cells = [c if c is not None else placeholder.copy() for c in cells]

    mine = img.convert("RGB").resize((tw, th), Image.LANCZOS)
    gap, pad = 16, 20
    row = [cells[0], mine, cells[1]]
    canvas = Image.new("RGB", (pad * 2 + tw * 3 + gap * 2, pad * 2 + th + 34), (15, 15, 17))
    dr = ImageDraw.Draw(canvas)
    for i, cell in enumerate(row):
        x = pad + i * (tw + gap)
        canvas.paste(cell, (x, pad))
        dr.rectangle([x + tw - 54, pad + th - 22, x + tw - 6, pad + th - 6], fill=(0, 0, 0))
        dr.text((x + tw - 48, pad + th - 20), "12:34", fill=(255, 255, 255))
        dr.text((x, pad + th + 8), "Video title goes here" if i != 1 else ">> YOURS <<",
                fill=(200, 200, 210) if i != 1 else (90, 220, 255))
    return canvas


def contrast_spread(img):
    """Luminance spread of the grayscale version - a flat image reads as mush at 168 px."""
    g = img.convert("L")
    hist = g.histogram()
    total = sum(hist) or 1
    acc, lo, hi = 0, 0, 255
    for v, n in enumerate(hist):
        acc += n
        if acc >= total * 0.02:
            lo = v
            break
    acc = 0
    for v in range(255, -1, -1):
        acc += hist[v]
        if acc >= total * 0.02:
            hi = v
            break
    return hi - lo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--outdir", default=None,
                    help="default: a temp proof folder, not the image's own directory")
    ap.add_argument("--here", action="store_true",
                    help="write the four proofs beside the source image")
    ap.add_argument("--competitors", nargs="*", default=[])
    ap.add_argument("--max-bytes", type=int, default=0, help="0 = infer from ratio")
    a = ap.parse_args()

    img = Image.open(a.image)
    base = os.path.splitext(os.path.basename(a.image))[0]
    # Five PNGs per run. Next to the artwork that is clutter; in a temp folder
    # it is still openable, which is all a proof needs to be.
    outdir = a.outdir or (os.path.dirname(os.path.abspath(a.image))
                          if a.here else str(proof_dir(a.image)))
    os.makedirs(outdir, exist_ok=True)
    p = lambda suffix: os.path.join(outdir, f"{base}_{suffix}.png")

    small = mobile(img)
    t1 = up(small)
    t1.save(p("01_mobile"))
    t2 = up(small.convert("L"))
    t2.save(p("02_gray"))
    t3 = img.convert("RGB").resize((640, max(1, round(640 * img.height / img.width))), Image.LANCZOS) \
            .filter(ImageFilter.GaussianBlur(9))
    t3.save(p("03_squint"))
    t4 = feed_mock(img, a.competitors)
    t4.save(p("04_feed"))

    panels = [label(t1, f"1. MOBILE {MOBILE_W}px - idea readable?"),
              label(t2, "2. GRAYSCALE - contrast without colour?"),
              label(t3, "3. SQUINT - one focal point?"),
              label(t4, "4. FEED - does it stand out?")]
    sw = max(x.width for x in panels)
    sh = sum(x.height for x in panels) + 12 * (len(panels) - 1)
    sheet = Image.new("RGB", (sw, sh), (18, 18, 20))
    y = 0
    for x in panels:
        sheet.paste(x, ((sw - x.width) // 2, y))
        y += x.height + 12
    sheet.save(p("sheet"))

    ratio, diff = nearest_ratio(img.width, img.height)
    spec_w, spec_h, spec_bytes = SPEC[ratio]
    size = os.path.getsize(a.image)
    limit = a.max_bytes or spec_bytes
    spread = contrast_spread(img)

    fails = []
    if diff > 0.02:
        fails.append(f"aspect {img.width}x{img.height} is not a clean platform ratio (nearest {ratio})")
    if img.width < spec_w or img.height < spec_h:
        fails.append(f"below spec size: {img.width}x{img.height} < {spec_w}x{spec_h}")
    if limit and size > limit:
        fails.append(f"file {size/1024/1024:.2f} MB exceeds the {limit/1024/1024:.2f} MB limit")
    notes = []
    if ratio == "1:1" and img.width < 1400:
        notes.append(f"{img.width}x{img.height} is fine for a marketplace listing but below "
                     f"the 1400 minimum for a podcast cover (3000 recommended)")
    if spread < 110:
        fails.append(f"luminance spread only {spread}/255 - too flat, will mush at {MOBILE_W}px")

    print(f"wrote 4 tests + {p('sheet')}")
    print(f"ratio {ratio} | {img.width}x{img.height} | {size/1024:.0f} KB | luminance spread {spread}/255")
    for n in notes:
        print(f"note: {n}")
    if fails:
        print("\nFAIL:")
        for f in fails:
            print("  - " + f)
        print("\nFix these, then re-run. Also OPEN the four images above - the human checks "
              "(focal point, emotion, standout) cannot be automated.")
        sys.exit(1)
    print("\nMeasurable checks pass. Now OPEN the four images - focal point, emotion and "
          "standout are judged by eye, then score with references/scorecard.md.")


if __name__ == "__main__":
    main()
