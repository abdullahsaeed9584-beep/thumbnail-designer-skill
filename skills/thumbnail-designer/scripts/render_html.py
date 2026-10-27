#!/usr/bin/env python3
"""Render an HTML thumbnail template to PNG via headless Chromium.

  python render_html.py template.html out.png --var HEADLINE="IT'S OVER" --var ACCENT="#00E5FF"
  python render_html.py text.html text.png --transparent --size 1280x720
  python render_html.py --check          # report which render backends exist

{{NAME}} placeholders are replaced by --var NAME=value; unused ones become "".
Asset paths in --var are rewritten to absolute file:// URLs so the page can load them.
Tries Playwright first, then any Chrome/Chromium/Edge binary found on the system.
"""
import argparse, os, shutil, subprocess, sys, tempfile
from pathlib import Path

# Tokens that must never render empty: an empty CSS custom property is valid but
# poisons every color-mix()/gradient that depends on it.
DEFAULTS = {
    "ACCENT": "#00E5FF",
    "INK": "#FFFFFF",
    "BASE": "#0B0E14",
    "ALIGN": "left",
}

CHROME_NAMES = [
    "chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome",
    "msedge", "microsoft-edge",
]
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]


def find_chrome():
    for n in CHROME_NAMES:
        p = shutil.which(n)
        if p:
            return p
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    return None


def have_playwright():
    try:
        import playwright.sync_api  # noqa: F401
        return True
    except Exception:
        return False


ASSET_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif",
             ".ttf", ".otf", ".woff", ".woff2"}


def as_url(v):
    """Turn a local ASSET path into a file:// URL; leave anything else alone.

    The extension check is load-bearing. Without it any value that happens to match a
    file or folder name gets rewritten - and on Windows the match is case-insensitive,
    so a headline word like "WORK" next to a work/ directory silently renders as
    file:///C:/.../work inside the thumbnail.
    """
    if not v or "://" in v or v.startswith("#") or v.startswith("data:"):
        return v
    if Path(v).suffix.lower() not in ASSET_EXT:
        return v
    p = Path(v)
    return p.resolve().as_uri() if p.exists() else v


def fill(html, variables):
    import re
    for k, v in variables.items():
        html = html.replace("{{%s}}" % k, as_url(v))
    return re.sub(r"\{\{[A-Z0-9_]+\}\}", "", html)   # drop unused placeholders


def shoot_playwright(html_path, out, w, h, transparent, wait):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg.goto(Path(html_path).resolve().as_uri())
        try:
            pg.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass
        pg.wait_for_timeout(wait)
        pg.screenshot(path=out, omit_background=transparent)
        b.close()


def shoot_chrome(binary, html_path, out, w, h, transparent, wait):
    cmd = [
        binary, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-color-profile=srgb", "--font-render-hinting=none",
        f"--virtual-time-budget={max(wait, 1500)}",
        f"--window-size={w},{h}", f"--screenshot={os.path.abspath(out)}",
    ]
    if transparent:
        cmd.append("--default-background-color=00000000")
    cmd.append(Path(html_path).resolve().as_uri())
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not os.path.exists(out):
        sys.exit(f"chrome screenshot failed:\n{r.stderr[-1500:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template", nargs="?")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--var", action="append", default=[], metavar="NAME=VALUE")
    ap.add_argument("--size", default="1280x720")
    ap.add_argument("--transparent", action="store_true", help="omit page background (for text/overlay layers)")
    ap.add_argument("--wait", type=int, default=600, help="ms to wait for fonts/images")
    ap.add_argument("--keep-html", action="store_true", help="keep the filled HTML next to --out for debugging")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    chrome, pw = find_chrome(), have_playwright()
    if a.check:
        print(f"playwright: {'yes' if pw else 'no'}")
        print(f"chrome/chromium: {chrome or 'not found'}")
        print("ok" if (pw or chrome) else "NO BACKEND - render type with Pillow and say so in the note")
        return
    if not a.template or not a.out:
        sys.exit("usage: render_html.py template.html out.png [--var K=V ...]  |  --check")
    if not (pw or chrome):
        sys.exit("no headless browser found. Run with --check, or render type via Pillow and disclose it.")

    w, h = (int(v) for v in a.size.lower().split("x"))
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
    # write beside the template so relative css/font paths still resolve
    if a.keep_html:
        tmp = Path(a.template).with_suffix(".filled.html")
    else:
        fd, name = tempfile.mkstemp(suffix=".html", dir=str(Path(a.template).parent))
        os.close(fd)          # Windows keeps the file locked while the fd is open
        tmp = Path(name)
    tmp.write_text(html, encoding="utf-8")
    try:
        if pw:
            shoot_playwright(str(tmp), a.out, w, h, a.transparent, a.wait)
        else:
            shoot_chrome(chrome, str(tmp), a.out, w, h, a.transparent, a.wait)
    finally:
        if not a.keep_html:
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass
    print(f"{a.out}  {w}x{h}  via {'playwright' if pw else os.path.basename(chrome)}")


if __name__ == "__main__":
    main()
