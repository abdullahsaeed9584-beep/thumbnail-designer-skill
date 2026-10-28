#!/usr/bin/env python3
"""Render an HTML design to a print-ready PDF at an exact physical page size.

  python make_pdf.py flyer.html flyer.pdf --trim A5 --bleed 3 --marks \
      --var HEADLINE="Grand Opening" --var ACCENT="#C8102E"

  python make_pdf.py card.html card.pdf --trim 85x55 --bleed 3 --marks
  python make_pdf.py --sizes           # list the named trim sizes

Why this exists: a 300 DPI PNG is an image of a document, not a document. A printer
needs a PDF whose page box is the trim plus bleed, with the artwork actually running
into the bleed. This builds that, then MEASURES the result - it reads the /MediaBox
back out of the finished PDF and fails if it is not the size that was asked for, so
"print-ready" is a verified claim rather than a hopeful one.

What it does NOT do: convert to CMYK, embed an ICC profile, or flatten transparency.
Those are prepress steps. Say so when you deliver - see references/print-production.md.
"""
import argparse, os, re, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render_html import fill, find_chrome, have_playwright, DEFAULTS  # noqa: E402
from scratch import proof_path  # noqa: E402

MM_PER_IN = 25.4
PT_PER_IN = 72.0

# Trim sizes in mm, width x height (portrait). Use --landscape to swap.
SIZES = {
    "A3": (297, 420), "A4": (210, 297), "A5": (148, 210), "A6": (105, 148),
    "DL": (99, 210), "LETTER": (215.9, 279.4), "TABLOID": (279.4, 431.8),
    "CARD": (85, 55),          # ISO/European business card
    "CARD_US": (88.9, 50.8),   # US business card, 3.5 x 2 in
    "POSTER_A2": (420, 594), "POSTER_A1": (594, 841), "POSTER_A0": (841, 1189),
    "SQUARE_210": (210, 210),
}


def parse_trim(s, landscape):
    key = s.strip().upper()
    if key in SIZES:
        w, h = SIZES[key]
    else:
        m = re.fullmatch(r"\s*([\d.]+)\s*[xX*]\s*([\d.]+)\s*(mm)?\s*", s)
        if not m:
            sys.exit(f"unknown trim size {s!r}. Use --sizes to list names, or WxH in mm.")
        w, h = float(m.group(1)), float(m.group(2))
    # --landscape means "wider than tall", not "swap whatever I was given". An
    # explicit 3000x2000 is already landscape; swapping it produced a portrait
    # page and silently ignored the orientation the caller actually stated.
    if landscape and h > w:
        w, h = h, w
    return w, h


def media_box_mm(pdf_path):
    """Read the first /MediaBox out of a PDF and return it in mm.

    Deliberately crude: no PDF library is assumed to be installed, and the box is
    plain ASCII in the page dictionary of every PDF Chromium emits.
    """
    data = Path(pdf_path).read_bytes()
    m = re.search(rb"/MediaBox\s*\[\s*([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s*\]", data)
    if not m:
        return None
    x0, y0, x1, y1 = (float(v) for v in m.groups())
    return ((x1 - x0) / PT_PER_IN * MM_PER_IN, (y1 - y0) / PT_PER_IN * MM_PER_IN)


def page_css(page_w, page_h, trim_w, trim_h, bleed, safe, marks):
    """CSS the template does not have to carry itself.

    The page box is trim+bleed. The artwork is positioned so that 0,0 of the design
    is the top-left of the BLEED, which is what a printer expects to receive.
    """
    css = f"""
    @page {{ size: {page_w:.3f}mm {page_h:.3f}mm; margin: 0; }}
    html, body {{ margin: 0; padding: 0; background: #FFFFFF; }}
    body {{ width: {page_w:.3f}mm; height: {page_h:.3f}mm; }}
    .stage, .page {{
      position: relative;
      width: {page_w:.3f}mm; height: {page_h:.3f}mm;
      overflow: hidden;
    }}
    :root {{
      --bleed: {bleed:.3f}mm; --safe: {safe:.3f}mm;
      --trim-w: {trim_w:.3f}mm; --trim-h: {trim_h:.3f}mm;
      --page-w: {page_w:.3f}mm; --page-h: {page_h:.3f}mm;
    }}
    """
    if marks and bleed > 0:
        # Crop marks sit in the bleed margin, offset so they never touch the trim.
        off = min(bleed, 3.0)
        length = max(bleed * 1.6, 4.0)
        css += f"""
    .cropmarks {{ position: absolute; inset: 0; pointer-events: none; z-index: 9999; }}
    .cropmarks i {{ position: absolute; background: #000; }}
    .cropmarks .h {{ height: 0.25mm; width: {length:.3f}mm; }}
    .cropmarks .v {{ width: 0.25mm; height: {length:.3f}mm; }}
    """
    return css


def marks_html(page_w, page_h, trim_w, trim_h, bleed):
    if bleed <= 0:
        return ""
    l, t = bleed, bleed
    r, b = bleed + trim_w, bleed + trim_h
    gap = min(bleed * 0.35, 1.0)
    parts = []
    for x, y, cls, dx, dy in (
        (l, t, "h", -(bleed), 0), (l, t, "v", 0, -(bleed)),
        (r, t, "h", gap, 0),      (r, t, "v", 0, -(bleed)),
        (l, b, "h", -(bleed), 0), (l, b, "v", 0, gap),
        (r, b, "h", gap, 0),      (r, b, "v", 0, gap),
    ):
        parts.append(
            f'<i class="{cls}" style="left:{x + dx:.3f}mm;top:{y + dy:.3f}mm"></i>')
    return '<div class="cropmarks">' + "".join(parts) + "</div>"


def pdf_playwright(html_path, out, page_w, page_h):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--force-color-profile=srgb"])
        pg = b.new_page()
        pg.goto(Path(html_path).resolve().as_uri())
        try:
            pg.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass
        pg.wait_for_timeout(500)
        pg.pdf(path=out, width=f"{page_w:.3f}mm", height=f"{page_h:.3f}mm",
               print_background=True, margin={"top": "0", "bottom": "0",
                                              "left": "0", "right": "0"},
               prefer_css_page_size=True)
        b.close()


def proof_png(html_path, out_png, page_w, page_h, dpi, pw, chrome):
    """A lookable raster of the same page.

    A PDF cannot be opened and judged by eye without a PDF rasteriser, and the QA
    rule in this skill is to LOOK at what is being delivered. So every PDF gets a
    proof image at the same geometry. The proof is for inspection only - the PDF
    is the deliverable, and the proof must never be sent to a printer in its place.
    """
    # The page is laid out in millimetres, and CSS resolves mm at a fixed 96 DPI.
    # So the viewport must be the page's CSS-pixel size and the DPI must come from
    # the device scale factor. Sizing the viewport in output pixels instead leaves
    # the design sitting small in the corner of a larger canvas.
    css_w = max(1, int(round(page_w / MM_PER_IN * 96)))
    css_h = max(1, int(round(page_h / MM_PER_IN * 96)))
    scale = dpi / 96.0
    px_w, px_h = int(round(css_w * scale)), int(round(css_h * scale))
    if pw:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--force-color-profile=srgb"])
            pg = b.new_page(viewport={"width": css_w, "height": css_h},
                            device_scale_factor=scale)
            pg.goto(Path(html_path).resolve().as_uri())
            try:
                pg.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            pg.wait_for_timeout(400)
            pg.screenshot(path=out_png)
            b.close()
    else:
        cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--force-color-profile=srgb", "--virtual-time-budget=3000",
               f"--force-device-scale-factor={scale}",
               f"--window-size={css_w},{css_h}",
               f"--screenshot={os.path.abspath(out_png)}",
               Path(html_path).resolve().as_uri()]
        subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    return (px_w, px_h) if os.path.exists(out_png) else None


def pdf_chrome(binary, html_path, out):
    cmd = [binary, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           "--force-color-profile=srgb", "--virtual-time-budget=4000",
           f"--print-to-pdf={os.path.abspath(out)}",
           Path(html_path).resolve().as_uri()]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not os.path.exists(out):
        sys.exit(f"chrome print-to-pdf failed:\n{r.stderr[-1500:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template", nargs="?")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--var", action="append", default=[], metavar="NAME=VALUE")
    ap.add_argument("--trim", default="A5", help="A4, A5, CARD, LETTER ... or 210x297 (mm)")
    ap.add_argument("--landscape", action="store_true")
    ap.add_argument("--bleed", type=float, default=3.0, help="mm per edge (0 for none)")
    ap.add_argument("--safe", type=float, default=5.0, help="mm clear of trim for type")
    ap.add_argument("--marks", action="store_true", help="draw crop marks in the bleed")
    ap.add_argument("--proof", nargs="?", const="AUTO", metavar="PNG",
                    help="lookable raster proof; bare flag = temp proof folder")
    ap.add_argument("--proof-dpi", type=int, default=150)
    ap.add_argument("--keep-html", action="store_true")
    ap.add_argument("--sizes", action="store_true")
    a = ap.parse_args()

    if a.sizes:
        for k, (w, h) in SIZES.items():
            print(f"  {k:<12} {w} x {h} mm")
        return
    if not a.template or not a.out:
        sys.exit("usage: make_pdf.py design.html out.pdf --trim A5 --bleed 3 [--marks]")

    chrome, pw = find_chrome(), have_playwright()
    if not (pw or chrome):
        sys.exit("no headless browser found - cannot produce a PDF. Say so; do not claim one.")

    if a.proof == "AUTO":
        a.proof = proof_path(a.out, "_proof.png")
    trim_w, trim_h = parse_trim(a.trim, a.landscape)
    page_w, page_h = trim_w + 2 * a.bleed, trim_h + 2 * a.bleed

    variables = {}
    for item in a.var:
        if "=" not in item:
            sys.exit(f"--var needs NAME=VALUE, got {item!r}")
        k, v = item.split("=", 1)
        variables[k.strip()] = v
    for k, v in DEFAULTS.items():
        if not variables.get(k, "").strip():
            variables[k] = v

    html = fill(Path(a.template).read_text(encoding="utf-8"), variables)
    inject = ("<style>" + page_css(page_w, page_h, trim_w, trim_h, a.bleed, a.safe, a.marks)
              + "</style>")
    if "</head>" in html:
        html = html.replace("</head>", inject + "</head>", 1)
    else:
        html = inject + html
    if a.marks:
        mk = marks_html(page_w, page_h, trim_w, trim_h, a.bleed)
        html = html.replace("</body>", mk + "</body>", 1) if "</body>" in html else html + mk

    if a.keep_html:
        tmp = Path(a.template).with_suffix(".filled.html")
    else:
        fd, name = tempfile.mkstemp(suffix=".html", dir=str(Path(a.template).parent))
        os.close(fd)
        tmp = Path(name)
    tmp.write_text(html, encoding="utf-8")
    try:
        if pw:
            pdf_playwright(str(tmp), a.out, page_w, page_h)
        else:
            pdf_chrome(chrome, str(tmp), a.out)
        proof_size = None
        if a.proof:
            proof_size = proof_png(str(tmp), a.proof, page_w, page_h, a.proof_dpi, pw, chrome)
    finally:
        if not a.keep_html:
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass

    got = media_box_mm(a.out)
    size_kb = os.path.getsize(a.out) / 1024
    print(f"{a.out}  {size_kb:.0f} KB")
    print(f"  trim   {trim_w} x {trim_h} mm")
    print(f"  bleed  {a.bleed} mm per edge -> page {page_w:.1f} x {page_h:.1f} mm")
    print(f"  safe   {a.safe} mm inside trim")
    if got is None:
        print("  MediaBox: could not be read - VERIFY THE PDF BY HAND before delivering")
        sys.exit(1)
    dw, dh = abs(got[0] - page_w), abs(got[1] - page_h)
    print(f"  MediaBox measured: {got[0]:.1f} x {got[1]:.1f} mm", end="  ")
    if max(dw, dh) > 0.6:
        print("MISMATCH")
        sys.exit("FAIL: the PDF page is not the requested size. Do not call this print-ready.")
    print("OK")
    if a.proof:
        if proof_size:
            print(f"  proof  {a.proof}  {proof_size[0]}x{proof_size[1]} px @ {a.proof_dpi} DPI "
                  f"- OPEN IT AND LOOK. Inspection copy only, not the deliverable.")
        else:
            print("  proof: FAILED to render - inspect the PDF by hand instead")
    print("  colour: sRGB. CMYK conversion, ICC embedding and flattening are prepress -")
    print("  state that in the delivery note.")


if __name__ == "__main__":
    main()
