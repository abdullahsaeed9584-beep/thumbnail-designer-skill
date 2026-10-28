#!/usr/bin/env python3
"""Validate a logo SVG and prove it survives the things a logo has to survive.

  python svg_check.py logo.svg --sheet logo_proof.png --png-out dist/

A logo is not finished because it looks good at 1000px on a white artboard. It has
to hold at 16px in a browser tab, work as one flat colour on an invoice, knock out
to white on a dark background, and scale without a raster edge. This checks all of
that and writes a contact sheet to LOOK at - the eye check is still yours.

Checks
  structure   parses, has a viewBox (without one it does not scale), sane aspect
  vector      no embedded raster, no filters that force rasterisation on export
  text        <text> elements still live = the file depends on a font being present
  scale       renders at 16/32/64/128/512 px
  monochrome  solid black, knockout white, and greyscale renders

Exit 1 on a structural failure, so it can gate a delivery.
"""
import argparse, os, re, sys, tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render_html import find_chrome, have_playwright  # noqa: E402
from scratch import proof_path  # noqa: E402

SVG_NS = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"
SIZES = [16, 32, 64, 128, 512]


def localname(tag):
    return tag.split("}", 1)[-1]


def inspect(path):
    issues, notes = [], []
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        return None, [f"FAIL  not well-formed XML: {e}"], [], None

    if localname(root.tag) != "svg":
        issues.append("FAIL  root element is not <svg>")

    vb = root.get("viewBox")
    if not vb:
        issues.append("FAIL  no viewBox - the file cannot scale cleanly; add one")
        ratio = None
    else:
        try:
            _, _, vw, vh = [float(v) for v in re.split(r"[ ,]+", vb.strip())]
            ratio = vw / vh if vh else None
            notes.append(f"      viewBox {vb.strip()}  ({vw:g} x {vh:g}, ratio {ratio:.3f})")
        except Exception:
            issues.append(f"FAIL  viewBox is not four numbers: {vb!r}")
            ratio = None

    w, h = root.get("width"), root.get("height")
    if w and h and re.fullmatch(r"\d+(\.\d+)?(px)?", w or "") and re.fullmatch(r"\d+(\.\d+)?(px)?", h or ""):
        notes.append(f"      intrinsic size {w} x {h}")

    kinds = {}
    texts, rasters, filters = 0, 0, 0
    for el in root.iter():
        n = localname(el.tag)
        kinds[n] = kinds.get(n, 0) + 1
        if n == "text" or n == "tspan":
            texts += 1
        if n == "image":
            href = el.get("href") or el.get(XLINK) or ""
            rasters += 1
            notes.append(f"      <image> -> {href[:60]}")
        if n in ("filter", "feGaussianBlur", "feDropShadow"):
            filters += 1

    if rasters:
        issues.append(f"FAIL  {rasters} embedded raster <image> element(s) - this is not a vector logo")
    if texts:
        issues.append(f"WARN  {texts} live <text>/<tspan> element(s) - the logo will change shape "
                      f"on any machine without that font. Convert lettering to paths.")
    if filters:
        issues.append(f"WARN  {filters} filter element(s) - these rasterise in most print RIPs "
                      f"and in EPS export. Keep a flat fallback version.")
    if ratio is not None and (ratio > 8 or ratio < 0.125):
        issues.append(f"WARN  extreme aspect ratio {ratio:.2f} - check it still reads in a square avatar crop")

    shapes = sum(kinds.get(k, 0) for k in ("path", "circle", "rect", "ellipse", "polygon", "polyline", "line"))
    notes.append("      elements: " + ", ".join(f"{k}x{v}" for k, v in sorted(kinds.items())))
    notes.append(f"      {shapes} drawable shape(s), {os.path.getsize(path)} bytes")
    return root, issues, notes, ratio


SHEET = """<!doctype html>
<html><head><meta charset="utf-8"><style>
  body {{ margin:0; background:#FFFFFF; font:12px/1.4 system-ui,sans-serif; color:#333; }}
  .row {{ display:flex; align-items:flex-end; gap:28px; padding:26px 30px; }}
  .row + .row {{ border-top:1px solid #E6E8EC; }}
  .cell {{ text-align:center; }}
  .cell span {{ display:block; margin-top:8px; color:#8A8F98; font-size:11px; }}
  .box {{ display:flex; align-items:center; justify-content:center; }}
  .dark {{ background:#11161D; }}
  h2 {{ margin:0; padding:18px 30px 0; font-size:12px; letter-spacing:.14em;
        text-transform:uppercase; color:#8A8F98; }}
  img {{ display:block; }}
  .black img {{ filter: brightness(0) saturate(100%); }}
  .white img {{ filter: brightness(0) invert(1); }}
  .grey  img {{ filter: grayscale(1); }}
</style></head><body>
<h2>Scale — does it survive 16px?</h2>
<div class="row">{scale}</div>
<h2>One colour — solid black, knockout white, greyscale</h2>
<div class="row">{mono}</div>
</body></html>"""


def build_sheet(svg_path, out_png, pw, chrome, ratio=None):
    url = Path(svg_path).resolve().as_uri()
    # Size by the LONGER side. A horizontal lockup constrained by height renders
    # several thousand pixels wide and the sheet becomes unreadable - which is
    # exactly the shape most logo deliveries are.
    dim = "width" if (ratio or 1) > 1.5 else "height"
    mono_px = 300 if dim == "width" else 96
    scale = "".join(
        f'<div class="cell"><div class="box"><img src="{url}" {dim}="{s}"></div>'
        f'<span>{s}px</span></div>' for s in SIZES)
    mono = (
        f'<div class="cell"><div class="box"><img src="{url}" {dim}="{mono_px}"></div><span>colour</span></div>'
        f'<div class="cell black"><div class="box"><img src="{url}" {dim}="{mono_px}"></div><span>solid black</span></div>'
        f'<div class="cell white"><div class="box dark" style="padding:14px"><img src="{url}" {dim}="{mono_px}"></div>'
        f'<span>knockout white</span></div>'
        f'<div class="cell grey"><div class="box"><img src="{url}" {dim}="{mono_px}"></div><span>greyscale</span></div>')
    html = SHEET.format(scale=scale, mono=mono)

    fd, name = tempfile.mkstemp(suffix=".html")
    os.close(fd)
    tmp = Path(name)
    tmp.write_text(html, encoding="utf-8")
    try:
        if pw:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b = p.chromium.launch(args=["--force-color-profile=srgb"])
                pg = b.new_page(viewport={"width": 1000, "height": 520},
                                device_scale_factor=2)
                pg.goto(tmp.resolve().as_uri())
                pg.wait_for_timeout(500)
                pg.screenshot(path=out_png, full_page=True)
                b.close()
        else:
            import subprocess
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--force-color-profile=srgb", "--virtual-time-budget=3000",
                            "--window-size=1000,520", f"--screenshot={os.path.abspath(out_png)}",
                            tmp.resolve().as_uri()], capture_output=True, timeout=120)
    finally:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
    return os.path.exists(out_png)


def export_pngs(svg_path, outdir, sizes, pw, chrome):
    """Transparent PNG exports at the sizes an identity pack actually ships."""
    os.makedirs(outdir, exist_ok=True)
    url = Path(svg_path).resolve().as_uri()
    stem = Path(svg_path).stem
    written = []
    for s in sizes:
        page = (f'<!doctype html><html><head><meta charset="utf-8"><style>'
                f'html,body{{margin:0;background:transparent;}}'
                f'img{{display:block;width:{s}px;}}</style></head>'
                f'<body><img src="{url}"></body></html>')
        fd, name = tempfile.mkstemp(suffix=".html")
        os.close(fd)
        tmp = Path(name)
        tmp.write_text(page, encoding="utf-8")
        dest = os.path.join(outdir, f"{stem}_{s}.png")
        try:
            if pw:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    b = p.chromium.launch()
                    pg = b.new_page(viewport={"width": s, "height": s})
                    pg.goto(tmp.resolve().as_uri())
                    pg.wait_for_timeout(250)
                    el = pg.query_selector("img")
                    el.screenshot(path=dest, omit_background=True)
                    b.close()
            else:
                import subprocess
                subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                                "--default-background-color=00000000",
                                "--virtual-time-budget=2000", f"--window-size={s},{s}",
                                f"--screenshot={os.path.abspath(dest)}",
                                tmp.resolve().as_uri()], capture_output=True, timeout=120)
        finally:
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass
        if os.path.exists(dest):
            written.append(dest)
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg")
    ap.add_argument("--sheet", nargs="?", const="AUTO",
                    help="scale + one-colour contact sheet; bare flag = temp proof folder")
    ap.add_argument("--png-out", help="also export transparent PNGs into this directory")
    ap.add_argument("--png-sizes", default="64,256,1024")
    a = ap.parse_args()

    if not os.path.exists(a.svg):
        sys.exit(f"no such file: {a.svg}")

    root, issues, notes, ratio = inspect(a.svg)
    print(f"{a.svg}")
    for n in notes:
        print(n)
    fails = [i for i in issues if i.startswith("FAIL")]
    for i in issues:
        print("  " + i)
    if not issues:
        print("  OK    structure, vector purity and type all clean")

    if a.sheet == "AUTO":
        a.sheet = proof_path(a.svg, "_proof.png")
    pw, chrome = have_playwright(), find_chrome()
    if (a.sheet or a.png_out) and not (pw or chrome):
        print("  WARN  no headless browser - cannot rasterise. Do not claim PNG exports.")
    else:
        if a.sheet and build_sheet(a.svg, a.sheet, pw, chrome, ratio):
            print(f"  sheet {a.sheet}  - OPEN IT AND LOOK: 16px legibility and the "
                  f"one-colour versions are eye calls, not script calls")
        if a.png_out:
            sizes = [int(s) for s in a.png_sizes.split(",") if s.strip()]
            w = export_pngs(a.svg, a.png_out, sizes, pw, chrome)
            for f in w:
                print(f"  png   {f}")

    if fails:
        sys.exit(f"{len(fails)} structural failure(s) - not deliverable as a logo")


if __name__ == "__main__":
    main()
