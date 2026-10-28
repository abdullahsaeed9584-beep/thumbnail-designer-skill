#!/usr/bin/env python3
"""Render an animated HTML design to MP4 / GIF / WebM / PNG frames.

  python animate.py ../assets/templates/logo-reveal.html out.mp4 \
      --size 1920x1080 --duration 2.4 --fps 30 --gif out.gif \
      --var WORDMARK="work/lockup.svg" --var ACCENT="#0E2A47"

How the seeking works: the page is NOT recorded in real time. Every frame, the
Web Animations API is used to pause every running animation and set its
currentTime to the exact frame time. That means a slow render still produces
perfectly even timing, and staggered delays stay correct because each animation
keeps its own timeline. Record in real time and you get dropped frames and jitter.

Requirements
  headless Chromium (Playwright preferred - it keeps one browser open for all
  frames instead of launching one per frame)
  ffmpeg on PATH for any video output; --frames-only works without it

Animations in the template must use `animation-fill-mode: both` (or `fill: both`),
otherwise they snap back to the un-animated state once their time has passed and
the tail of the clip renders wrong.
"""
import argparse, os, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render_html import fill, find_chrome, have_playwright, DEFAULTS  # noqa: E402

SEEK = """(t) => {
  document.getAnimations().forEach(a => { try { a.pause(); a.currentTime = t; } catch (e) {} });
}"""


def have_ffmpeg():
    return shutil.which("ffmpeg")


def render_frames(html_path, outdir, w, h, duration, fps, pw, chrome):
    n = max(1, int(round(duration * fps)))
    os.makedirs(outdir, exist_ok=True)
    url = Path(html_path).resolve().as_uri()
    if pw:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--force-color-profile=srgb",
                                        "--font-render-hinting=none"])
            pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            pg.goto(url)
            try:
                pg.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            pg.wait_for_timeout(400)
            for i in range(n):
                t_ms = (i / fps) * 1000.0
                pg.evaluate(SEEK, t_ms)
                pg.screenshot(path=os.path.join(outdir, f"f{i:05d}.png"))
            b.close()
        return n
    # Chrome CLI fallback: one process per frame, and no way to drive the Web
    # Animations API, so the seek is done with a URL fragment the template reads.
    for i in range(n):
        t = i / fps
        dest = os.path.join(outdir, f"f{i:05d}.png")
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-color-profile=srgb", "--virtual-time-budget=2000",
                        f"--window-size={w},{h}", f"--screenshot={os.path.abspath(dest)}",
                        url + f"#t={t:.4f}"], capture_output=True, timeout=120)
    return n


def encode(frames, out, fps, kind):
    pat = os.path.join(frames, "f%05d.png")
    if kind == "gif":
        pal = os.path.join(frames, "palette.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(fps), "-i", pat,
                        "-vf", "palettegen=stats_mode=diff", pal], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(fps), "-i", pat,
                        "-i", pal, "-lavfi", "paletteuse=dither=bayer:bayer_scale=3",
                        "-loop", "0", out], check=True)
    elif kind == "webm":
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(fps), "-i", pat,
                        "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-crf", "28",
                        "-b:v", "0", out], check=True)
    else:
        # yuv420p + even dimensions, or half the players in the world refuse it
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(fps), "-i", pat,
                        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                        "-pix_fmt", "yuv420p",
                        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                        "-movflags", "+faststart", out], check=True)


def probe(path):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=width,height,nb_frames,avg_frame_rate",
                            "-show_entries", "format=duration", "-of", "default=nw=1",
                            path], capture_output=True, text=True, timeout=30)
        return r.stdout.strip()
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template")
    ap.add_argument("out", nargs="?", help="output video (.mp4 / .webm / .gif); omit with --frames-only")
    ap.add_argument("--var", action="append", default=[], metavar="NAME=VALUE")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--duration", type=float, default=3.0, help="seconds")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--gif", help="also write a GIF here")
    ap.add_argument("--frames-only", action="store_true", help="keep PNG frames, no encode")
    ap.add_argument("--frames-dir", help="where to put frames (default: a temp dir)")
    a = ap.parse_args()

    pw, chrome = have_playwright(), find_chrome()
    if not (pw or chrome):
        sys.exit("no headless browser - cannot render frames. Do not claim an animation.")
    if not a.frames_only and not have_ffmpeg():
        sys.exit("ffmpeg not found. Use --frames-only and deliver the frame sequence, "
                 "or install ffmpeg. Do not claim a video file you cannot produce.")
    if not a.frames_only and not a.out:
        sys.exit("give an output file, or use --frames-only")

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
    fd, name = tempfile.mkstemp(suffix=".html", dir=str(Path(a.template).parent))
    os.close(fd)
    tmp = Path(name)
    tmp.write_text(html, encoding="utf-8")

    frames_dir = a.frames_dir or tempfile.mkdtemp(prefix="frames_")
    try:
        n = render_frames(str(tmp), frames_dir, w, h, a.duration, a.fps, pw, chrome)
        print(f"  {n} frames at {w}x{h}, {a.fps} fps ({a.duration}s)")
        if not pw:
            print("  NOTE: rendered via the Chrome CLI fallback - CSS animations cannot be")
            print("  seeked there, so the template must animate from the #t= fragment.")
        if a.frames_only:
            print(f"  frames {frames_dir}")
            return
        kind = Path(a.out).suffix.lower().lstrip(".")
        encode(frames_dir, a.out, a.fps, "gif" if kind == "gif" else kind)
        print(f"  {a.out}  {os.path.getsize(a.out) / 1024:.0f} KB")
        info = probe(a.out)
        if info:
            print("  " + info.replace("\n", "  "))
        if a.gif:
            encode(frames_dir, a.gif, a.fps, "gif")
            print(f"  {a.gif}  {os.path.getsize(a.gif) / 1024:.0f} KB")
        print("  OPEN IT AND WATCH IT. Timing and easing are eye calls.")
    finally:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
        if not a.frames_dir and not a.frames_only:
            shutil.rmtree(frames_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
