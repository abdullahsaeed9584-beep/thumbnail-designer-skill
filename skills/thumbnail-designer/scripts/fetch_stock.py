#!/usr/bin/env python3
"""Fetch REAL photographs for a thumbnail - the fix for designs that look synthetic.

  python fetch_stock.py "video editing workstation" --count 4 --out work/stock
  python fetch_stock.py "city skyline night" --count 3 --min-width 1600 --landscape
  python fetch_stock.py "office desk" --any-license        # wider pool, needs attribution

Sources, tried in order until one answers. No API key needed for either:
  1. Openverse (openverse.org) - aggregates Flickr, Wikimedia, Nappy, Rawpixel. Best
     licence metadata and the best search.
  2. Wikimedia Commons, reached through the en.wikipedia.org API - public domain and
     Creative Commons photographs, with full attribution metadata.

One source being down is the normal case, not the exceptional one: Openverse was
unreachable from the machine this was last tested on while Wikimedia answered fine.
A single-source fetcher simply fails there, which is why there are two.

LICENSING - this matters, read it:
  * Default is CC0 + Public Domain Mark ONLY. Those need no attribution and are safe for
    commercial work, which is what a thumbnail needs.
  * --any-license widens the pool to CC-BY / CC-BY-SA etc. Those REQUIRE visible credit and
    some require share-alike. A thumbnail has nowhere to put credit, so only use them when
    the user says they will credit elsewhere.
  * Every download writes ATTRIBUTION.md with title, creator, licence and source URL. Keep it.
  * Openly licensed does NOT mean model- or property-released, and it does not clear
    trademarks or logos. For a face, a brand, or a product shot, use the user's own asset.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import re

API = "https://api.openverse.org/v1/images/"
UA = {"User-Agent": "thumbnail-designer-skill/1.0 (+https://github.com/)"}
SAFE = "cc0,pdm"          # no attribution required, commercial use OK


def search(query, count, license_filter, min_width, orientation, timeout):
    params = {"q": query, "page_size": max(count * 4, 20)}
    if license_filter:
        params["license"] = license_filter
    if orientation:
        params["aspect_ratio"] = orientation
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read()[:200].decode(errors="replace")
        sys.exit(f"Openverse HTTP {e.code}: {body}\n"
                 f"(anonymous use is rate limited - wait a minute and retry)")
    except Exception as e:
        sys.exit(f"Openverse unreachable: {e}\n"
                 f"Fall back to an asset the user supplies, and say so in the note.")

    out = []
    for r in data.get("results", []):
        w = r.get("width") or 0
        if w and w < min_width:
            continue
        if not r.get("url"):
            continue
        out.append(r)
        if len(out) >= count:
            break
    return out, data.get("result_count", 0)


WIKI_API = "https://en.wikipedia.org/w/api.php"
# Wikimedia's user-agent policy rejects generic agents with HTTP 429. It wants a
# named client and a contact URL, so this request does not reuse the UA above.
WIKI_UA = {"User-Agent": "thumbnail-designer-skill/1.8 "
                         "(https://github.com/abdullahsaeed9584-beep/thumbnail-designer-skill) "
                         "python-urllib"}


def strip_html(v):
    return re.sub(r"<[^>]+>", "", v or "").strip()


def search_wikimedia(query, count, min_width, timeout):
    """Commons search via the en.wikipedia API, normalised to Openverse's shape.

    ns 6 is the File namespace. iiurlwidth gives a scaled thumbnail URL, which is what
    we want: the originals are routinely 40 MP scans nobody needs for a design.
    """
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrlimit": max(count * 5, 20), "gsrnamespace": 6,
        "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
        "iiurlwidth": 2000,
    }
    url = WIKI_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=WIKI_UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode())

    pages = (data.get("query") or {}).get("pages") or {}
    out = []
    for pg in pages.values():
        ii = (pg.get("imageinfo") or [{}])[0]
        if not ii:
            continue
        if (ii.get("mime") or "") not in ("image/jpeg", "image/png", "image/webp"):
            continue
        w = ii.get("width") or 0
        if w and w < min_width:
            continue
        em = ii.get("extmetadata") or {}
        lic = strip_html((em.get("LicenseShortName") or {}).get("value")) or "unknown"
        out.append({
            "url": ii.get("thumburl") or ii.get("url"),
            "width": ii.get("width"), "height": ii.get("height"),
            "title": strip_html((em.get("ObjectName") or {}).get("value"))
                     or pg.get("title", "").replace("File:", ""),
            "creator": strip_html((em.get("Artist") or {}).get("value")) or "unknown",
            "license": lic,
            "license_version": "",
            "foreign_landing_url": "https://commons.wikimedia.org/wiki/"
                                   + urllib.parse.quote(pg.get("title", "")),
            "_source": "Wikimedia Commons",
        })
        if len(out) >= count:
            break
    return out, len(pages)


def search_all(query, count, license_filter, min_width, orientation, timeout):
    """Try each backend; only give up when every one has failed."""
    problems = []
    try:
        res, total = search(query, count, license_filter, min_width, orientation, timeout)
        if res:
            for r in res:
                r.setdefault("_source", "Openverse")
            return res, total, "Openverse", problems
        problems.append("Openverse returned no usable result")
    except SystemExit as e:
        problems.append(str(e).splitlines()[0])
    except Exception as e:
        problems.append(f"Openverse: {e}")

    try:
        res, total = search_wikimedia(query, count, min_width, timeout)
        if res:
            return res, total, "Wikimedia Commons", problems
        problems.append("Wikimedia returned no usable result")
    except Exception as e:
        problems.append(f"Wikimedia: {e}")

    return [], 0, None, problems


def download(rec, outdir, index, timeout):
    url = rec["url"]
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp"):
        ext = ".jpg"
    path = os.path.join(outdir, f"{index:02d}{ext}")
    hdr = WIKI_UA if "wikimedia.org" in url or "wikipedia.org" in url else UA
    req = urllib.request.Request(url, headers=hdr)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
    except Exception as e:
        print(f"  x {url[:60]}: {e}")
        return None
    if len(data) < 8000:
        print(f"  x {url[:60]}: too small, skipped")
        return None
    with open(path, "wb") as f:
        f.write(data)
    print(f"  + {path}  {len(data)/1024:.0f} KB  "
          f"{rec.get('width')}x{rec.get('height')}  [{rec.get('license', '?').upper()}]")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--count", type=int, default=3)
    ap.add_argument("--out", default="work/stock")
    ap.add_argument("--min-width", type=int, default=1200)
    ap.add_argument("--landscape", action="store_true", help="prefer wide images")
    ap.add_argument("--portrait", action="store_true", help="prefer tall images")
    ap.add_argument("--any-license", action="store_true",
                    help="widen past CC0/PDM - results then REQUIRE visible attribution")
    ap.add_argument("--timeout", type=int, default=45)
    a = ap.parse_args()

    people = ("face", "man", "woman", "person", "people", "portrait", "model", "guy",
              "girl", "boy", "businessman", "businesswoman", "entrepreneur", "selfie")
    if any(w in a.query.lower().split() or w in a.query.lower() for w in people):
        print()
        print("!! This query is about PEOPLE. An open licence is NOT a model release.")
        print("   Do not put a stranger's face on a commercial offer (gig, ad, product,")
        print("   course) - it implies they endorse it. Use the user's own photo.")
        print("   See references/identity-protocol.md.")
        print()

    orientation = "wide" if a.landscape else ("tall" if a.portrait else None)
    lic = None if a.any_license else SAFE

    results, total, used, problems = search_all(
        a.query, a.count, lic, a.min_width, orientation, a.timeout)
    for note in problems:
        print(f"  .. {note}")
    if not results:
        sys.exit(f"No usable results for {a.query!r} from any source.\n"
                 f"Try a simpler query, lower --min-width, or --any-license.\n"
                 f"Otherwise fall back to an asset the user supplies - and say so.")

    os.makedirs(a.out, exist_ok=True)
    print(f"{len(results)} of {total} matches via {used} -> {a.out}")
    if used != "Openverse":
        print("  NOTE: this is the fallback source. Licences here are often CC-BY or "
              "CC-BY-SA, which REQUIRE visible credit - check ATTRIBUTION.md per image.")
    rows, paths = [], []
    for i, rec in enumerate(results, 1):
        p = download(rec, a.out, i, a.timeout)
        if p:
            paths.append(p)
            rows.append((os.path.basename(p), rec))

    if not paths:
        sys.exit("Nothing downloaded. Use a user-supplied asset instead.")

    att = os.path.join(a.out, "ATTRIBUTION.md")
    with open(att, "w", encoding="utf-8") as f:
        f.write(f"# Image attribution\n\nQuery: `{a.query}`\nSearched via: {used}\n\n")
        if a.any_license:
            f.write("**These are NOT all CC0.** Any CC-BY / CC-BY-SA item below must be "
                    "credited visibly wherever the thumbnail is published.\n\n")
        for name, rec in rows:
            f.write(f"## {name}\n"
                    f"- Title: {rec.get('title') or 'untitled'}\n"
                    f"- Creator: {rec.get('creator') or 'unknown'}\n"
                    f"- Licence: {(rec.get('license') or '?').upper()} "
                    f"{rec.get('license_version') or ''}\n"
                    f"- Via: {rec.get('_source') or used}\n"
                    f"- Source: {rec.get('foreign_landing_url') or rec.get('url')}\n\n")
    print(f"\nwrote {att} - keep it, and look at every image before using it.")
    print("Openly licensed is not model- or property-released and does not clear brands.")


if __name__ == "__main__":
    main()
