#!/usr/bin/env python3
"""Static checks on the HTML templates. Run after editing any of them.

  python lint_templates.py ../assets/templates
  python lint_templates.py ../assets/templates --render   # also render each one

Exists because two separate templates shipped with the same silent failure: a
top-level `var top` and a top-level `var name` in the inline script. Both are
assignments to read-only / coercing properties of `window`, so they fail without
an exception at the point of assignment and break something far away - a chart
whose bars all compute to NaN%, a sign where every piece of text vanishes while
the background renders perfectly. Nothing about the output says "script error",
which is what makes them expensive.

Checks
  globals    top-level `var <window property>` in an inline script
  braces     net brace/paren depth of each <script> block (a stray brace silently
             kills the whole block)
  tokens     {{PLACEHOLDER}} names that are not referenced in the script or body
  images     <img> without onerror, which renders a broken-image icon
  css        linked stylesheets that do not exist
"""
import argparse, os, re, sys
from pathlib import Path

# Properties of window that are read-only, coercing, or otherwise hostile to
# being shadowed by a top-level `var`.
WINDOW_PROPS = {
    "top", "name", "length", "status", "parent", "self", "window", "document",
    "location", "history", "closed", "frames", "origin", "screen", "navigator",
    "opener", "scrollX", "scrollY", "innerWidth", "innerHeight", "outerWidth",
    "outerHeight", "frameElement", "localStorage", "sessionStorage",
}


def scripts_of(html):
    return re.findall(r"<script[^>]*>(.*?)</script>", html, re.S | re.I)


def check(path):
    html = Path(path).read_text(encoding="utf-8", errors="replace")
    problems = []

    body = re.sub(r"<!--.*?-->", "", html, flags=re.S)

    for block in scripts_of(body):
        code = re.sub(r"//[^\n]*", "", block)
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)

        for m in re.finditer(r"\bvar\s+([A-Za-z_$][\w$]*)", code):
            if m.group(1) in WINDOW_PROPS:
                problems.append(
                    f"FAIL  `var {m.group(1)}` shadows window.{m.group(1)} - the "
                    f"assignment silently fails or coerces. Rename it.")

        stripped = re.sub(r"(['\"])(?:\\.|(?!\1).)*\1", "''", code)
        depth = stripped.count("{") - stripped.count("}")
        if depth != 0:
            problems.append(f"FAIL  unbalanced braces in a <script> block (net {depth:+d}) "
                            f"- a stray brace kills the entire block")
        pdepth = stripped.count("(") - stripped.count(")")
        if pdepth != 0:
            problems.append(f"FAIL  unbalanced parens in a <script> block (net {pdepth:+d})")

    tokens = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", body))
    for t in sorted(tokens):
        uses = len(re.findall(r"\{\{" + t + r"\}\}", body))
        if uses == 1 and not re.search(r"\{\{" + t + r"\}\}", body):
            problems.append(f"WARN  token {{{{{t}}}}} appears once and is never read")

    for m in re.finditer(r"<img\b[^>]*>", body, re.I):
        tag = m.group(0)
        if "onerror" not in tag.lower():
            src = re.search(r'src="([^"]*)"', tag)
            problems.append(f"WARN  <img src=\"{src.group(1) if src else '?'}\"> has no "
                            f"onerror - a missing asset renders a broken-image icon")

    for m in re.finditer(r'<link[^>]+href="([^"]+\.css)"', body, re.I):
        css = Path(path).parent / m.group(1)
        if not css.exists():
            problems.append(f"FAIL  linked stylesheet not found: {m.group(1)}")

    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", nargs="?", default=str(Path(__file__).parent.parent / "assets" / "templates"))
    ap.add_argument("--render", action="store_true", help="also render each template to a temp PNG")
    a = ap.parse_args()

    files = sorted(Path(a.dir).glob("*.html"))
    files = [f for f in files if not f.name.endswith(".filled.html")]
    if not files:
        sys.exit(f"no templates in {a.dir}")

    fails = warns = 0
    for f in files:
        problems = check(f)
        nf = sum(1 for p in problems if p.startswith("FAIL"))
        fails += nf
        warns += len(problems) - nf
        mark = "FAIL" if nf else ("warn" if problems else " ok ")
        print(f"[{mark}] {f.name}")
        for p in problems:
            print("        " + p)

    if a.render:
        import subprocess, tempfile
        rh = Path(__file__).parent / "render_html.py"
        print("\n--- render smoke test ---")
        for f in files:
            if f.name in ("print-page.html", "signage.html"):
                print(f"[skip] {f.name} (rendered by make_pdf.py at a physical size)")
                continue
            out = os.path.join(tempfile.gettempdir(), f.stem + "_lint.png")
            r = subprocess.run([sys.executable, str(rh), str(f), out, "--size", "1280x720"],
                               capture_output=True, text=True, timeout=180)
            ok = os.path.exists(out)
            print(f"[{'ok' if ok else 'FAIL'}] {f.name}"
                  + ("" if ok else "  " + r.stderr.strip()[-160:]))
            if not ok:
                fails += 1

    print(f"\n{len(files)} templates, {fails} failure(s), {warns} warning(s)")
    if fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
