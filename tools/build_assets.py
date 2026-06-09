#!/usr/bin/env python3
"""
Regenerate the inlined offline assets in army-builder.html.

The app embeds its fonts (Google Fonts: Bebas Neue + Barlow) and a subset of
Font Awesome 6 *solid* icons directly in the HTML, inside:

    <style id="offline-assets"> ... </style>

This keeps the app a single self-contained file that renders fully offline and
from file:// (no CDN, no service worker). Run this script to rebuild that block
after adding new icons or bumping font/FA versions.

Requirements:  pip install fonttools brotli      (needs network to fetch assets)
Usage:         python3 tools/build_assets.py
"""
import re, sys, subprocess, base64, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / "army-builder.html"
FA_VERSION = "6.7.2"
FA_CSS_URL   = f"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/{FA_VERSION}/css/all.min.css"
FA_WOFF2_URL = f"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/{FA_VERSION}/webfonts/fa-solid-900.woff2"
GF_URL = ("https://fonts.googleapis.com/css2?family=Bebas+Neue&"
          "family=Barlow:wght@400;500;600;700&display=swap")
CHROME = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
GF_SUBSETS = ("latin", "latin-ext")   # latin-ext covers accented names

def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": CHROME})
    data = urllib.request.urlopen(req, timeout=30).read()
    return data if binary else data.decode()

def main():
    src = HTML.read_text(encoding="utf-8")
    # collect icon names from the app source WITHOUT the existing inlined block
    app = re.sub(r'<style id="offline-assets">.*?</style>', "", src, flags=re.S)
    names = set(re.findall(r'fa-([a-z0-9]+(?:-[a-z0-9]+)*)', app))
    names -= {"solid","regular","brands","2x","3x","4x","5x","lg","sm","xs","fw","spin",
              "pulse","stack","stack-1x","stack-2x","li","border","pull-left","pull-right",
              "spin-pulse","beat","fade","flip","flip-horizontal","flip-vertical","flip-both",
              "rotate-90","rotate-180","rotate-270","rotate-by","inverse","layers"}
    # bare names rendered via fa-${...} that the literal scan misses
    names |= {"table-columns","list","rotate","plus","bolt","chess-pawn","chess-rook",
              "earth-americas","flag","gear","star","users","shield","gem","robot","virus","hand-fist"}

    fa_css = fetch(FA_CSS_URL)
    cp = {}
    for m in re.finditer(r'([.\w,\s-]+?)\{--fa:"\\([0-9a-f]+)"', fa_css):
        for nm in re.findall(r'\.fa-([a-z0-9-]+)', m.group(1)):
            cp.setdefault(nm, m.group(2))
    used = {n: cp[n] for n in sorted(names) if n in cp}
    missing = [n for n in sorted(names) if n not in cp]
    if missing:
        print("ERROR: unresolved icon names:", ", ".join(missing), file=sys.stderr)
        sys.exit(1)
    print(f"icons: {len(used)} resolved")

    # subset the solid font to just the used glyphs
    woff2 = ROOT / "tools" / ".fa-solid-900.woff2"
    woff2.write_bytes(fetch(FA_WOFF2_URL, binary=True))
    sub = ROOT / "tools" / ".fa-subset.woff2"
    unicodes = ",".join("U+"+c for c in sorted(set(used.values())))
    subprocess.run(["pyftsubset", str(woff2), f"--unicodes={unicodes}", "--flavor=woff2",
                    f"--output-file={sub}", "--no-hinting", "--desubroutinize"], check=True)
    fa_b64 = base64.b64encode(sub.read_bytes()).decode()
    woff2.unlink(); sub.unlink()
    print(f"FA subset: {len(fa_b64)//1024} KB base64")
    icon_rules = "".join(f'.fa-{n}::before{{content:"\\{c}"}}' for n, c in sorted(used.items()))
    fa_block = (
        "@font-face{font-family:'Font Awesome 6 Free';font-style:normal;font-weight:900;"
        f"font-display:block;src:url(data:font/woff2;base64,{fa_b64}) format('woff2')}}"
        ".fa-solid,.fas{font-family:'Font Awesome 6 Free';font-weight:900}"
        ".fa,.fas,.fa-solid{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;"
        "display:inline-block;font-style:normal;font-variant:normal;line-height:1;text-rendering:auto}"
        + icon_rules)

    # embed Google Fonts (latin + latin-ext) as data URIs
    gf = fetch(GF_URL)
    kept = []
    for label, block in re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})', gf):
        if label not in GF_SUBSETS:
            continue
        u = re.search(r'url\((https://[^)]+\.woff2)\)', block)
        if not u:
            continue
        data = fetch(u.group(1), binary=True)
        b64 = base64.b64encode(data).decode()
        kept.append(re.sub(r'\s+', ' ', block.replace(u.group(1), f"data:font/woff2;base64,{b64}")))
    print(f"Google Fonts: {len(kept)} faces embedded")

    inline = ("/* Inlined offline assets: Google Fonts (Bebas Neue, Barlow) + Font Awesome 6 "
              "solid subset. Regenerate with tools/build_assets.py */" + "".join(kept) + fa_block)

    pattern = r'<style id="offline-assets">.*?</style>'
    if not re.search(pattern, src, flags=re.S):
        print('ERROR: <style id="offline-assets"> block not found', file=sys.stderr); sys.exit(1)
    # lambda replacement => the CSS (incl. its backslash escapes) is inserted literally
    new = re.sub(pattern, lambda m: '<style id="offline-assets">' + inline + '</style>',
                 src, count=1, flags=re.S)
    HTML.write_text(new, encoding="utf-8")
    print(f"{HTML.name}: no change (assets already up to date)" if new == src
          else f"updated {HTML.name}: {len(src)} -> {len(new)} bytes")

if __name__ == "__main__":
    main()
