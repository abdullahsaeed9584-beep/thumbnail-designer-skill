#!/usr/bin/env python3
"""Convert a word into real SVG outlines, so a wordmark stops depending on a font.

  python text_to_paths.py --text "NORTHCAP" --font ../assets/fonts/Montserrat-Variable.ttf \
      --weight 800 --tracking 0.06 --out wordmark.svg --fill "#0E2A47"

A logo that ships as <text> is not a logo: open it anywhere the font is missing and
the letterforms silently change. Every identity delivery converts lettering to
curves. This does that conversion - genuine glyph outlines pulled from the font
file, not a traced screenshot - and reports what it did.

Needs fontTools:  python -m pip install fonttools
Variable fonts are instanced at --weight first, otherwise you get the default
instance (usually Regular) and a wordmark that is quietly too light.

Kerning note: this applies the font's advance widths and a uniform --tracking.
It does NOT apply GPOS kerning pairs, so pairs like AV or To may need a nudge.
Check the result by eye and use --kern "AV:-0.04" to correct specific pairs.
"""
import argparse, sys
from pathlib import Path


def load_font(path, weight, width):
    from fontTools.ttLib import TTFont
    font = TTFont(path)
    axes = {}
    if "fvar" in font:
        axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in font["fvar"].axes}
    if axes and (weight is not None or width is not None):
        from fontTools.varLib import instancer
        loc = {}
        if weight is not None and "wght" in axes:
            lo, _, hi = axes["wght"]
            loc["wght"] = max(lo, min(hi, weight))
        if width is not None and "wdth" in axes:
            lo, _, hi = axes["wdth"]
            loc["wdth"] = max(lo, min(hi, width))
        if loc:
            font = instancer.instantiateVariableFont(font, loc, inplace=False)
            return font, axes, loc
    return font, axes, {}


def outlines(font, text, tracking, kern_pairs):
    from fontTools.pens.svgPathPen import SVGPathPen
    upem = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]

    parts, x, missing = [], 0.0, []
    prev = None
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            missing.append(ch)
            x += upem * 0.3
            prev = None
            continue
        if prev is not None:
            pair = prev + ch
            x += kern_pairs.get(pair, 0.0) * upem
        pen = SVGPathPen(glyphset)
        glyphset[gname].draw(pen)
        d = pen.getCommands()
        if d:
            parts.append(f'<path transform="translate({x:.1f} 0)" d="{d}"/>')
        adv = hmtx[gname][0]
        x += adv + tracking * upem
        prev = ch
    if text:
        x -= tracking * upem          # no tracking after the final glyph
    return parts, x, upem, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--font", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--weight", type=float, default=None, help="variable-font wght axis, e.g. 800")
    ap.add_argument("--width", type=float, default=None, help="variable-font wdth axis")
    ap.add_argument("--tracking", type=float, default=0.0, help="letter-spacing in em, e.g. 0.06")
    ap.add_argument("--kern", action="append", default=[], metavar="AV:-0.04",
                    help="manual kern for one pair, in em; repeatable")
    ap.add_argument("--fill", default="#000000")
    ap.add_argument("--height", type=float, default=100.0, help="output viewBox height")
    a = ap.parse_args()

    try:
        import fontTools  # noqa: F401
    except ImportError:
        sys.exit("fontTools is not installed - run: python -m pip install fonttools\n"
                 "Until then do NOT claim the lettering is outlined.")

    if not Path(a.font).exists():
        sys.exit(f"font not found: {a.font}  (run fetch_fonts.py first)")

    kern_pairs = {}
    for k in a.kern:
        if ":" not in k:
            sys.exit(f"--kern wants PAIR:EM, got {k!r}")
        pair, val = k.rsplit(":", 1)
        kern_pairs[pair] = float(val)

    font, axes, loc = load_font(a.font, a.weight, a.width)
    parts, advance, upem, missing = outlines(font, a.text, a.tracking, kern_pairs)
    if not parts:
        sys.exit("no glyphs were drawn - check the text and the font")

    # Measure the real ink, not the em box: a wordmark is aligned on its outlines.
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.svgPathPen import SVGPathPen  # noqa: F401
    cmap = font.getBestCmap()
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]
    minx = miny = 1e9
    maxx = maxy = -1e9
    x = 0.0
    prev = None
    for ch in a.text:
        g = cmap.get(ord(ch))
        if g is None:
            x += upem * 0.3
            prev = None
            continue
        if prev is not None:
            x += kern_pairs.get(prev + ch, 0.0) * upem
        bp = BoundsPen(glyphset)
        glyphset[g].draw(bp)
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            minx = min(minx, x + x0); maxx = max(maxx, x + x1)
            miny = min(miny, y0);     maxy = max(maxy, y1)
        x += hmtx[g][0] + a.tracking * upem
        prev = ch

    ink_w, ink_h = maxx - minx, maxy - miny
    scale = a.height / ink_h
    out_w = ink_w * scale

    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {out_w:.2f} {a.height:.2f}" '
        f'width="{out_w:.2f}" height="{a.height:.2f}" role="img" aria-label="{a.text}">',
        f'<!-- "{a.text}" as outlines from {Path(a.font).name}'
        + (f', instanced at {loc}' if loc else '')
        + f', tracking {a.tracking}em. No live text: this file does not need the font. -->',
        f'<g fill="{a.fill}" fill-rule="nonzero" '
        f'transform="translate({-minx * scale:.2f} {maxy * scale:.2f}) scale({scale:.6f} {-scale:.6f})">',
    ]
    body += parts
    body += ["</g>", "</svg>"]
    Path(a.out).write_text("\n".join(body), encoding="utf-8")

    print(f"{a.out}")
    print(f"  text        {a.text!r}  ({len(parts)} glyph outline(s))")
    print(f"  font        {Path(a.font).name}  upem {upem}")
    if axes:
        print(f"  axes        {', '.join(axes)}" + (f"  instanced at {loc}" if loc
              else "  NOT INSTANCED - you are getting the default instance"))
    print(f"  tracking    {a.tracking} em" + (f"  manual kerns {kern_pairs}" if kern_pairs else ""))
    print(f"  ink box     {ink_w:.0f} x {ink_h:.0f} units -> {out_w:.1f} x {a.height:.1f}")
    if missing:
        print(f"  MISSING     no glyph for {missing!r} in this font - fix before delivering")
    print("  GPOS kerning is not applied. Look at the result and correct pairs with --kern.")


if __name__ == "__main__":
    main()
