#!/usr/bin/env python3
"""Download licence-safe display fonts (Google Fonts, OFL) into assets/fonts/.

  python fetch_fonts.py --all
  python fetch_fonts.py anton bebas montserrat
  python fetch_fonts.py --urdu
  python fetch_fonts.py --list

Everything here is Open Font Licence - free for commercial thumbnails.
Paid faces (Impact, Gilroy, Akira, Jameel Noori Nastaleeq) are NOT fetched;
use them only if the user owns a licence.
"""
import argparse
import os
import sys
import urllib.error
import urllib.request

RAW = "https://raw.githubusercontent.com/google/fonts/main"

FONTS = {
    # key: (path on google/fonts, filename)
    "anton":        (f"{RAW}/ofl/anton/Anton-Regular.ttf", "Anton-Regular.ttf"),
    "bebas":        (f"{RAW}/ofl/bebasneue/BebasNeue-Regular.ttf", "BebasNeue-Regular.ttf"),
    "archivo":      (f"{RAW}/ofl/archivoblack/ArchivoBlack-Regular.ttf", "ArchivoBlack-Regular.ttf"),
    "montserrat":   (f"{RAW}/ofl/montserrat/Montserrat%5Bwght%5D.ttf", "Montserrat-Variable.ttf"),
    "poppins":      (f"{RAW}/ofl/poppins/Poppins-ExtraBold.ttf", "Poppins-ExtraBold.ttf"),
    "poppins-black": (f"{RAW}/ofl/poppins/Poppins-Black.ttf", "Poppins-Black.ttf"),
    "oswald":       (f"{RAW}/ofl/oswald/Oswald%5Bwght%5D.ttf", "Oswald-Variable.ttf"),
    "inter":        (f"{RAW}/ofl/inter/Inter%5Bopsz,wght%5D.ttf", "Inter-Variable.ttf"),
    "teko":         (f"{RAW}/ofl/teko/Teko%5Bwght%5D.ttf", "Teko-Variable.ttf"),
    "barlow":       (f"{RAW}/ofl/barlowcondensed/BarlowCondensed-ExtraBold.ttf", "BarlowCondensed-ExtraBold.ttf"),
    # Urdu / Arabic script
    "nastaliq":     (f"{RAW}/ofl/notonastaliqurdu/NotoNastaliqUrdu%5Bwght%5D.ttf", "NotoNastaliqUrdu-Variable.ttf"),
    "naskh":        (f"{RAW}/ofl/notonaskharabic/NotoNaskhArabic%5Bwght%5D.ttf", "NotoNaskhArabic-Variable.ttf"),
    "lateef":       (f"{RAW}/ofl/lateef/Lateef%5Bwght%5D.ttf", "Lateef-Variable.ttf"),
}
URDU = ["nastaliq", "naskh", "lateef"]
LATIN = [k for k in FONTS if k not in URDU]


def dest_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(here), "assets", "fonts")


def fetch(key, outdir, force=False):
    url, name = FONTS[key]
    path = os.path.join(outdir, name)
    if os.path.exists(path) and not force:
        print(f"  = {name} (already present)")
        return True
    req = urllib.request.Request(url, headers={"User-Agent": "thumbnail-designer-skill"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"  x {name}: {e}")
        return False
    if len(data) < 2000:
        print(f"  x {name}: suspiciously small response, skipped")
        return False
    with open(path, "wb") as f:
        f.write(data)
    print(f"  + {name}  ({len(data)/1024:.0f} KB)")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fonts", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--urdu", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if a.list:
        print("latin:", " ".join(sorted(LATIN)))
        print("urdu/arabic:", " ".join(URDU))
        return

    keys = list(FONTS) if a.all else (URDU if a.urdu else a.fonts)
    if not keys:
        sys.exit("name fonts, or use --all / --urdu / --list")
    unknown = [k for k in keys if k not in FONTS]
    if unknown:
        sys.exit(f"unknown: {', '.join(unknown)} (see --list)")

    outdir = dest_dir()
    os.makedirs(outdir, exist_ok=True)
    print(f"-> {outdir}")
    ok = sum(fetch(k, outdir, a.force) for k in keys)
    print(f"\n{ok}/{len(keys)} available.")
    if ok < len(keys):
        print("Network may be restricted. Fall back to fonts already installed on the system, "
              "or ask the user to supply the TTF - and say which face was actually used.")


if __name__ == "__main__":
    main()
