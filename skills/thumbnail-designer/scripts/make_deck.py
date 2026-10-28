#!/usr/bin/env python3
"""Build a presentation from a JSON slide spec: one multi-page PDF plus slide PNGs.

  python make_deck.py deck.json --pdf deck.pdf --png-dir slides/
  python make_deck.py --example > deck.json

Slide spec (a JSON object):
  {"title": "...", "subtitle": "...", "accent": "#2563EB", "footer": "Acme - 2026",
   "slides": [
     {"layout": "title",   "kicker": "Series A", "title": "...", "sub": "..."},
     {"layout": "bullets", "title": "...", "bullets": ["...", "..."], "note": "..."},
     {"layout": "stat",    "stat": "42%", "title": "...", "sub": "...", "source": "..."},
     {"layout": "two",     "title": "...", "left": ["..."], "right": ["..."],
                           "left_head": "Now", "right_head": "After"},
     {"layout": "bars",    "title": "...", "series": [["Q1", 12], ["Q2", 31]],
                           "unit": "k", "source": "Company data, 2026"},
     {"layout": "quote",   "quote": "...", "attrib": "..."},
     {"layout": "section", "title": "..."}
   ]}

Why a PDF and not a .pptx: nothing in this environment can write a genuine
PowerPoint file. A PDF deck presents and prints correctly everywhere and is an
honest deliverable; a .pptx that was never created is not. If the user needs an
editable .pptx, say so plainly and hand over the PDF plus this JSON, which
regenerates the deck - see references/data-and-decks.md.

Numbers come from the spec and are never invented. A `bars` slide without a
`source` is refused, because an unsourced chart in a deck is a claim.
"""
import argparse, html, json, os, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render_html import find_chrome, have_playwright  # noqa: E402

# PowerPoint / Keynote 16:9 at its real physical size.
SLIDE_W_MM, SLIDE_H_MM = 338.667, 190.5

CSS = """
@page { size: {w}mm {h}mm; margin: 0; }
* { margin:0; padding:0; box-sizing:border-box; }
html, body { background:#FFF; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.slide {
  position:relative; width:{w}mm; height:{h}mm; overflow:hidden;
  background:#FFFFFF; color:#101722;
  font-family:'Inter','Montserrat',system-ui,sans-serif;
  padding: 18mm 22mm 15mm; display:flex; flex-direction:column;
  page-break-after: always; break-after: page;
}
.slide:last-child { page-break-after: auto; break-after: auto; }
.slide.dark { background:#0C1220; color:#FFFFFF; }
.kicker { font-size:4mm; font-weight:800; letter-spacing:.22em; text-transform:uppercase;
          color:var(--accent); margin-bottom:6mm; }
h1 { font-size:17mm; font-weight:800; line-height:1.04; letter-spacing:-.025em; }
h2 { font-size:11mm; font-weight:800; line-height:1.08; letter-spacing:-.02em; margin-bottom:9mm; }
.sub { font-size:6mm; font-weight:500; line-height:1.35; opacity:.72; margin-top:6mm; }
ul { list-style:none; display:flex; flex-direction:column; gap:5.5mm; }
li { font-size:6.2mm; line-height:1.3; padding-left:9mm; position:relative; }
li::before { content:""; position:absolute; left:0; top:2.4mm; width:4mm; height:1.4mm;
             border-radius:.7mm; background:var(--accent); }
.note { margin-top:auto; font-size:3.6mm; opacity:.55; }
.stat { font-size:46mm; font-weight:800; letter-spacing:-.04em; line-height:.92;
        color:var(--accent); }
.cols { display:flex; gap:14mm; flex:1; }
.col { flex:1; display:flex; flex-direction:column; gap:4.5mm; }
.colhead { font-size:4.4mm; font-weight:800; letter-spacing:.14em; text-transform:uppercase;
           padding-bottom:3mm; border-bottom:.6mm solid var(--accent); }
.quote { font-size:11mm; font-weight:600; line-height:1.22; letter-spacing:-.015em; }
.attrib { margin-top:8mm; font-size:4.6mm; font-weight:700; opacity:.6; }
.rule { width:26mm; height:1.6mm; background:var(--accent); border-radius:.8mm; margin-top:8mm; }
.src { margin-top:5mm; font-size:3.4mm; opacity:.55; }
.foot { position:absolute; left:22mm; right:22mm; bottom:7mm; display:flex;
        justify-content:space-between; font-size:3.4mm; opacity:.45; }
.chart { flex:1; display:flex; align-items:flex-end; gap:5mm; padding:6mm 0 0; }
.bar { flex:1; display:flex; flex-direction:column; justify-content:flex-end;
       align-items:center; gap:2.5mm; height:100%; }
.bar .fill { width:100%; background:var(--accent); border-radius:1mm 1mm 0 0; }
.bar .val { font-size:4.4mm; font-weight:800; }
.bar .lab { font-size:4mm; opacity:.65; }
.section-wrap { flex:1; display:flex; align-items:center; }
"""


def esc(s):
    return html.escape(str(s), quote=False)


def render_slide(s, idx, total, deck):
    layout = s.get("layout", "bullets")
    dark = s.get("dark", layout in ("title", "section", "quote"))
    out = [f'<section class="slide{" dark" if dark else ""}">']

    if layout == "title":
        if s.get("kicker"):
            out.append(f'<div class="kicker">{esc(s["kicker"])}</div>')
        out.append('<div class="section-wrap"><div>')
        out.append(f'<h1>{esc(s.get("title", ""))}</h1>')
        out.append('<div class="rule"></div>')
        if s.get("sub"):
            out.append(f'<div class="sub">{esc(s["sub"])}</div>')
        out.append("</div></div>")

    elif layout == "section":
        out.append('<div class="section-wrap"><div>')
        out.append(f'<div class="kicker">{esc(s.get("kicker", f"{idx:02d}"))}</div>')
        out.append(f'<h1>{esc(s.get("title", ""))}</h1><div class="rule"></div>')
        out.append("</div></div>")

    elif layout == "stat":
        out.append(f'<h2>{esc(s.get("title", ""))}</h2>')
        out.append(f'<div class="stat">{esc(s.get("stat", ""))}</div>')
        if s.get("sub"):
            out.append(f'<div class="sub">{esc(s["sub"])}</div>')
        if s.get("source"):
            out.append(f'<div class="src">Source: {esc(s["source"])}</div>')

    elif layout == "two":
        out.append(f'<h2>{esc(s.get("title", ""))}</h2><div class="cols">')
        for side, head in (("left", "left_head"), ("right", "right_head")):
            out.append('<div class="col">')
            if s.get(head):
                out.append(f'<div class="colhead">{esc(s[head])}</div>')
            out.append("<ul>" + "".join(f"<li>{esc(b)}</li>" for b in s.get(side, [])) + "</ul>")
            out.append("</div>")
        out.append("</div>")

    elif layout == "bars":
        series = s.get("series", [])
        vals = [float(v) for _, v in series] or [1.0]
        top = max(vals) or 1.0
        out.append(f'<h2>{esc(s.get("title", ""))}</h2><div class="chart">')
        unit = s.get("unit", "")
        for lab, val in series:
            pct = max(2.0, float(val) / top * 100.0)
            out.append(f'<div class="bar"><div class="val">{esc(val)}{esc(unit)}</div>'
                       f'<div class="fill" style="height:{pct:.1f}%"></div>'
                       f'<div class="lab">{esc(lab)}</div></div>')
        out.append("</div>")
        out.append(f'<div class="src">Source: {esc(s["source"])}</div>')

    elif layout == "quote":
        out.append('<div class="section-wrap"><div>')
        out.append(f'<div class="quote">“{esc(s.get("quote", ""))}”</div>')
        if s.get("attrib"):
            out.append(f'<div class="attrib">{esc(s["attrib"])}</div>')
        out.append("</div></div>")

    else:  # bullets
        out.append(f'<h2>{esc(s.get("title", ""))}</h2>')
        out.append("<ul>" + "".join(f"<li>{esc(b)}</li>" for b in s.get("bullets", [])) + "</ul>")
        if s.get("note"):
            out.append(f'<div class="note">{esc(s["note"])}</div>')

    if layout not in ("title",):
        out.append(f'<div class="foot"><span>{esc(deck.get("footer", ""))}</span>'
                   f'<span>{idx} / {total}</span></div>')
    out.append("</section>")
    return "\n".join(out)


def build_html(deck):
    slides = deck.get("slides", [])
    accent = deck.get("accent", "#2563EB")
    body = "\n".join(render_slide(s, i + 1, len(slides), deck) for i, s in enumerate(slides))
    css = CSS.replace("{w}", f"{SLIDE_W_MM:.3f}").replace("{h}", f"{SLIDE_H_MM:.3f}")
    return (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<title>{esc(deck.get("title", "Deck"))}</title>'
            f'<style>:root{{--accent:{accent};}}{css}</style></head><body>{body}</body></html>')


def validate(deck):
    problems = []
    for i, s in enumerate(deck.get("slides", []), 1):
        if s.get("layout") == "bars":
            if not s.get("source"):
                problems.append(f"slide {i}: a chart with no 'source' - an unsourced number "
                                f"in a deck is a claim. Add the source or drop the chart.")
            if not s.get("series"):
                problems.append(f"slide {i}: 'bars' with no series")
        if s.get("layout") == "stat" and not s.get("source"):
            problems.append(f"slide {i}: headline statistic with no 'source'")
        n = len(s.get("bullets", []))
        if n > 6:
            problems.append(f"slide {i}: {n} bullets - past about six nobody reads them; split the slide")
        for b in s.get("bullets", []):
            if len(str(b).split()) > 18:
                problems.append(f"slide {i}: a bullet of {len(str(b).split())} words is a paragraph")
    return problems


EXAMPLE = {
    "title": "Northcap - Series A", "accent": "#2563EB", "footer": "Northcap - confidential",
    "slides": [
        {"layout": "title", "kicker": "Series A", "title": "Advice that compounds",
         "sub": "Northcap - February 2026"},
        {"layout": "bullets", "title": "The problem",
         "bullets": ["Advice is priced per hour, not per outcome",
                     "Nobody under 40 will pay it", "So they get none at all"]},
        {"layout": "stat", "stat": "68%", "title": "of under-40s have never taken advice",
         "sub": "and the gap widens every year", "source": "replace with your real source"},
        {"layout": "bars", "title": "Revenue", "unit": "k",
         "series": [["Q1", 12], ["Q2", 31], ["Q3", 44], ["Q4", 71]],
         "source": "replace with your real source"},
        {"layout": "quote", "quote": "I did not know where to start, so I did nothing.",
         "attrib": "User interview, n=40"},
    ],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", nargs="?", help="deck JSON")
    ap.add_argument("--pdf")
    ap.add_argument("--png-dir")
    ap.add_argument("--example", action="store_true", help="print a starter spec and exit")
    ap.add_argument("--keep-html")
    a = ap.parse_args()

    if a.example:
        print(json.dumps(EXAMPLE, indent=2))
        return
    if not a.spec:
        sys.exit("usage: make_deck.py deck.json --pdf deck.pdf [--png-dir slides/]")

    deck = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    slides = deck.get("slides", [])
    if not slides:
        sys.exit("no slides in the spec")

    problems = validate(deck)
    html_doc = build_html(deck)

    tmp = Path(a.keep_html) if a.keep_html else None
    if tmp is None:
        fd, name = tempfile.mkstemp(suffix=".html")
        os.close(fd)
        tmp = Path(name)
    tmp.write_text(html_doc, encoding="utf-8")

    pw, chrome = have_playwright(), find_chrome()
    if not (pw or chrome):
        sys.exit("no headless browser - cannot build the deck.")

    try:
        if a.pdf:
            if pw:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    b = p.chromium.launch(args=["--force-color-profile=srgb"])
                    pg = b.new_page()
                    pg.goto(tmp.resolve().as_uri())
                    pg.wait_for_timeout(500)
                    pg.pdf(path=a.pdf, width=f"{SLIDE_W_MM}mm", height=f"{SLIDE_H_MM}mm",
                           print_background=True, prefer_css_page_size=True,
                           margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
                    b.close()
            else:
                subprocess.run([chrome, "--headless=new", "--disable-gpu",
                                "--no-pdf-header-footer", "--virtual-time-budget=5000",
                                f"--print-to-pdf={os.path.abspath(a.pdf)}",
                                tmp.resolve().as_uri()], capture_output=True, timeout=180)
            import re
            data = Path(a.pdf).read_bytes()
            pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
            print(f"{a.pdf}  {os.path.getsize(a.pdf) / 1024:.0f} KB  {pages} page(s)")
            if pages != len(slides):
                print(f"  MISMATCH: {len(slides)} slides in the spec but {pages} pages in the PDF")

        if a.png_dir and pw:
            os.makedirs(a.png_dir, exist_ok=True)
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b = p.chromium.launch(args=["--force-color-profile=srgb"])
                pg = b.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1.5)
                pg.goto(tmp.resolve().as_uri())
                pg.wait_for_timeout(400)
                for i, el in enumerate(pg.query_selector_all(".slide"), 1):
                    el.screenshot(path=os.path.join(a.png_dir, f"slide_{i:02d}.png"))
                b.close()
            print(f"  {len(slides)} slide PNGs in {a.png_dir}")
        elif a.png_dir:
            print("  slide PNGs need Playwright - skipped")
    finally:
        if not a.keep_html:
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass

    print(f"  {len(slides)} slides, accent {deck.get('accent', '#2563EB')}")
    if problems:
        print("  REVIEW:")
        for p_ in problems:
            print("    - " + p_)
    else:
        print("  content checks: clean")
    print("  This is a PDF deck, not a .pptx. Do not describe it as an editable PowerPoint.")


if __name__ == "__main__":
    main()
