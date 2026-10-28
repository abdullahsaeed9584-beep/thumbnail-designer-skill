#!/usr/bin/env python3
"""Generate a straight-tuck-end carton dieline as a dimensioned SVG.

  python dieline.py --l 60 --w 35 --h 140 --out box.svg
  python dieline.py --l 60 --w 35 --h 140 --out box.svg --artwork front.png

L = front panel width, W = depth, H = height, all in millimetres - the order a
printer asks for them in. Everything else (flap depths, glue flap, tuck curve,
dust flaps) is derived with the usual rules of thumb and printed in the report so
the numbers can be checked against a real converter's spec.

Layers, by colour, which is the convention every packaging printer reads:
  magenta solid   CUT      the knife
  cyan dashed     CREASE   the fold
  green dashed    SAFE     keep live matter inside this
  grey dashed     BLEED    art must run out to here

This produces a dieline to DESIGN INTO and to show a printer. It is NOT a
substitute for the converter's own die: before anything is printed, send them
this file and build the final artwork on the die THEY return. Say that when you
deliver it - see references/print-production.md.
"""
import argparse, sys
from pathlib import Path

MM = 1.0


def build(L, W, H, glue, bleed, safe, tuck=None, dust=None):
    tuck = W - 2 if tuck is None else tuck      # tuck flap slightly under depth so it slides in
    dust = round(W * 0.82, 1) if dust is None else dust
    tuck = max(tuck, 8)

    # Panels left to right: glue | back | side | front | side
    xs = []
    x = 0.0
    for wdt in (glue, L, W, L, W):
        xs.append((x, wdt))
        x += wdt
    flat_w = x
    body_top = max(tuck, dust)
    flat_h = body_top + H + body_top

    gx, back, sideA, front, sideB = xs
    y0 = body_top              # top of the body
    y1 = body_top + H          # bottom of the body

    cut, crease = [], []

    def line(store, x1, y1_, x2, y2):
        store.append((x1, y1_, x2, y2))

    # --- body outline ------------------------------------------------------
    # left edge of the glue flap is angled, which is what lets the flap seat
    # inside the carton without a visible step.
    taper = min(4.0, glue * 0.45)
    cut += [(gx[0] + taper, y0, gx[0] + glue, y0)]        # glue top
    cut += [(gx[0] + taper, y1, gx[0] + glue, y1)]        # glue bottom
    cut += [(gx[0] + taper, y0, gx[0], y0 + taper)]       # top taper
    cut += [(gx[0], y0 + taper, gx[0], y1 - taper)]       # glue outer edge
    cut += [(gx[0], y1 - taper, gx[0] + taper, y1)]       # bottom taper
    cut += [(flat_w, y0, flat_w, y1)]                      # far right edge

    # --- top flaps ---------------------------------------------------------
    # dust flaps on the two side panels, tuck on the back panel
    for (px, pw) in (sideA, sideB):
        inset = 1.0
        cut += [(px + inset, y0 - dust, px + pw - inset, y0 - dust)]
        cut += [(px + inset, y0 - dust, px, y0)]
        cut += [(px + pw - inset, y0 - dust, px + pw, y0)]
        crease += [(px, y0, px + pw, y0)]

    tx, tw = back
    cut += [(tx, y0, tx, y0 - tuck + 3), (tx, y0 - tuck + 3, tx + 3, y0 - tuck)]
    cut += [(tx + 3, y0 - tuck, tx + tw - 3, y0 - tuck)]
    cut += [(tx + tw - 3, y0 - tuck, tx + tw, y0 - tuck + 3), (tx + tw, y0 - tuck + 3, tx + tw, y0)]
    crease += [(tx, y0, tx + tw, y0)]

    # --- bottom flaps: tuck on the front, dust on the sides ----------------
    for (px, pw) in (sideA, sideB):
        inset = 1.0
        cut += [(px + inset, y1 + dust, px + pw - inset, y1 + dust)]
        cut += [(px + inset, y1 + dust, px, y1)]
        cut += [(px + pw - inset, y1 + dust, px + pw, y1)]
        crease += [(px, y1, px + pw, y1)]

    fx, fw = front
    cut += [(fx, y1, fx, y1 + tuck - 3), (fx, y1 + tuck - 3, fx + 3, y1 + tuck)]
    cut += [(fx + 3, y1 + tuck, fx + fw - 3, y1 + tuck)]
    cut += [(fx + fw - 3, y1 + tuck, fx + fw, y1 + tuck - 3), (fx + fw, y1 + tuck - 3, fx + fw, y1)]
    crease += [(fx, y1, fx + fw, y1)]

    # A straight tuck end closes the top with a tuck off the BACK and dust flaps off
    # the SIDES, which leaves the front panel's top edge carrying no flap at all -
    # and the back panel's bottom edge likewise. Those edges are knife, not crease.
    # Leaving them out is how a dieline reaches a converter with an open box on it.
    cut += [(front[0], y0, front[0] + front[1], y0)]
    cut += [(back[0], y1, back[0] + back[1], y1)]

    # --- vertical creases between panels -----------------------------------
    for (px, pw) in xs[:-1]:
        crease += [(px + pw, y0, px + pw, y1)]
    crease += [(gx[0] + glue, y0, gx[0] + glue, y1)]

    panels = {
        "glue flap": gx, "back": back, "side": sideA, "front": front, "side ": sideB,
    }
    return dict(cut=cut, crease=crease, xs=xs, flat_w=flat_w, flat_h=flat_h,
                y0=y0, y1=y1, tuck=tuck, dust=dust, panels=panels,
                front=front, back=back, sideA=sideA, sideB=sideB)


def svg(d, L, W, H, bleed, safe, artwork=None):
    pad = 14.0
    vb_w, vb_h = d["flat_w"] + pad * 2, d["flat_h"] + pad * 2
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{vb_w:.2f}mm" '
             f'height="{vb_h:.2f}mm" viewBox="0 0 {vb_w:.2f} {vb_h:.2f}">')
    o.append(f'<!-- Straight tuck end carton. L {L} x W {W} x H {H} mm. '
             f'Flat {d["flat_w"]:.1f} x {d["flat_h"]:.1f} mm. '
             f'CUT magenta, CREASE cyan dashed, SAFE green, BLEED grey. '
             f'Check against the converter die before printing. -->')
    o.append('<rect width="100%" height="100%" fill="#FFFFFF"/>')
    o.append(f'<g transform="translate({pad:.2f},{pad:.2f})">')

    if artwork:
        fx, fw = d["front"]
        o.append(f'<image href="{artwork}" x="{fx:.2f}" y="{d["y0"]:.2f}" '
                 f'width="{fw:.2f}" height="{H:.2f}" preserveAspectRatio="xMidYMid slice"/>')

    # bleed box
    o.append(f'<rect x="{-bleed:.2f}" y="{-bleed:.2f}" '
             f'width="{d["flat_w"] + 2 * bleed:.2f}" height="{d["flat_h"] + 2 * bleed:.2f}" '
             f'fill="none" stroke="#9AA0A8" stroke-width="0.25" stroke-dasharray="2 2"/>')
    o.append(f'<text x="{-bleed:.2f}" y="{-bleed - 1.5:.2f}" font-family="sans-serif" '
             f'font-size="3" fill="#9AA0A8">BLEED {bleed}mm — artwork must run to here</text>')

    o.append('<g stroke="#00AEEF" stroke-width="0.3" stroke-dasharray="3 2" fill="none">')
    for x1, y1, x2, y2 in d["crease"]:
        o.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/>')
    o.append('</g>')

    o.append('<g stroke="#FF00AA" stroke-width="0.4" fill="none" stroke-linecap="round">')
    for x1, y1, x2, y2 in d["cut"]:
        o.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/>')
    o.append('</g>')

    # safe area inside each body panel
    o.append('<g stroke="#2FB457" stroke-width="0.25" stroke-dasharray="1.5 1.5" fill="none">')
    for (px, pw) in d["xs"][1:]:
        o.append(f'<rect x="{px + safe:.2f}" y="{d["y0"] + safe:.2f}" '
                 f'width="{pw - 2 * safe:.2f}" height="{H - 2 * safe:.2f}"/>')
    o.append('</g>')

    # barcode keepline, bottom of the back panel - where a retailer expects it
    bx, bw = d["back"]
    bc_w, bc_h = 37.29, 25.93          # EAN-13 at 100% magnification
    if bw - 2 * safe >= bc_w and H - 2 * safe >= bc_h:
        o.append(f'<rect x="{bx + safe + 2:.2f}" y="{d["y1"] - safe - bc_h - 2:.2f}" '
                 f'width="{bc_w}" height="{bc_h}" fill="none" stroke="#2FB457" '
                 f'stroke-width="0.3"/>')
        o.append(f'<text x="{bx + safe + 3.5:.2f}" y="{d["y1"] - safe - bc_h + 2.6:.2f}" '
                 f'font-family="sans-serif" font-size="2.2" fill="#2FB457">EAN-13 100%</text>')
        o.append(f'<text x="{bx + safe + 3.5:.2f}" y="{d["y1"] - safe - bc_h + 5.4:.2f}" '
                 f'font-family="sans-serif" font-size="2.2" fill="#2FB457">2mm quiet zone</text>')
        barcode_note = "placed on the back panel"
    else:
        barcode_note = ("DOES NOT FIT at 100% on the back panel - reduce magnification "
                        "to no less than 80% or move it to a larger panel")

    # panel labels
    o.append('<g font-family="sans-serif" font-size="3.4" fill="#5A6472" '
             'text-anchor="middle">')
    names = ["GLUE", "BACK", "SIDE", "FRONT", "SIDE"]
    for name, (px, pw) in zip(names, d["xs"]):
        o.append(f'<text x="{px + pw / 2:.2f}" y="{d["y0"] + H / 2:.2f}">{name}</text>')
        o.append(f'<text x="{px + pw / 2:.2f}" y="{d["y0"] + H / 2 + 4.6:.2f}" '
                 f'font-size="2.6">{pw:.0f}mm</text>')
    o.append('</g>')

    # dimension rule along the bottom
    yb = d["flat_h"] + 6
    o.append(f'<g stroke="#5A6472" stroke-width="0.2" font-family="sans-serif" font-size="2.8" fill="#5A6472">')
    o.append(f'<line x1="0" y1="{yb:.2f}" x2="{d["flat_w"]:.2f}" y2="{yb:.2f}"/>')
    o.append(f'<text x="{d["flat_w"] / 2:.2f}" y="{yb + 4:.2f}" text-anchor="middle" '
             f'stroke="none">flat {d["flat_w"]:.1f} x {d["flat_h"]:.1f} mm '
             f'(+{bleed}mm bleed all round)</text>')
    o.append('</g>')

    o.append('</g></svg>')
    return "\n".join(o), barcode_note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--l", type=float, required=True, help="front panel width, mm")
    ap.add_argument("--w", type=float, required=True, help="depth, mm")
    ap.add_argument("--h", type=float, required=True, help="height, mm")
    ap.add_argument("--out", required=True)
    ap.add_argument("--glue", type=float, default=15.0, help="glue flap width, mm")
    ap.add_argument("--bleed", type=float, default=3.0)
    ap.add_argument("--safe", type=float, default=4.0)
    ap.add_argument("--tuck", type=float, default=None, help="tuck flap depth, mm")
    ap.add_argument("--dust", type=float, default=None, help="dust flap depth, mm")
    ap.add_argument("--artwork", default=None, help="image to drop onto the front panel as a placement proof")
    a = ap.parse_args()

    for n, v in (("L", a.l), ("W", a.w), ("H", a.h)):
        if v <= 0:
            sys.exit(f"{n} must be positive")
    if a.w > a.l * 3:
        print(f"note: depth {a.w} is large relative to width {a.l} - check this is intended")

    d = build(a.l, a.w, a.h, a.glue, a.bleed, a.safe, a.tuck, a.dust)
    body, barcode_note = svg(d, a.l, a.w, a.h, a.bleed, a.safe, a.artwork)
    Path(a.out).write_text(body, encoding="utf-8")

    vol = a.l * a.w * a.h / 1000.0
    print(f"{a.out}")
    print(f"  carton      L {a.l} x W {a.w} x H {a.h} mm   ({vol:.0f} ml internal, nominal)")
    print(f"  flat sheet  {d['flat_w']:.1f} x {d['flat_h']:.1f} mm")
    print(f"  with bleed  {d['flat_w'] + 2 * a.bleed:.1f} x {d['flat_h'] + 2 * a.bleed:.1f} mm")
    print(f"  glue flap   {a.glue} mm   tuck {d['tuck']:.1f} mm   dust flaps {d['dust']:.1f} mm")
    print(f"  safe        {a.safe} mm inside every panel edge and every crease")
    print(f"  barcode     {barcode_note}")
    print()
    print("  Panels left to right: GLUE | BACK | SIDE | FRONT | SIDE")
    print("  Top tuck folds off the BACK panel, bottom tuck off the FRONT panel.")
    print("  This is a generated dieline for layout. Send it to the converter and")
    print("  rebuild the artwork on the die they return before anything is printed.")


if __name__ == "__main__":
    main()
