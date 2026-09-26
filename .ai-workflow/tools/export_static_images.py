#!/usr/bin/env python3
"""
export_static_images.py — headless static-image export for koolestpro content.html files.

Replaces the manual "open in a browser, click every download button" step.
Drives the REAL export pipeline already embedded in the content.html (the same
captureFixed()/captureSlide() functions the on-page download buttons call), so
whatever ships here is byte-identical to what a human clicking the buttons would get.
No native page.screenshot() is used for the actual captures — see
.ai-workflow/project-constitution.md ("verify against the ACTUAL html2canvas
output") for why that distinction matters.

Usage:
    export LD_LIBRARY_PATH=/tmp/pw_libs/extracted/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH
    python3 export_static_images.py <content.html> <output_dir>

Run .ai-workflow/tools/bootstrap_env.sh first (source it) to guarantee the
LD_LIBRARY_PATH / chromium install are in place — this script does not do
its own environment setup, it assumes a working Playwright chromium.

Output:
    <output_dir>/ba-graphic.png          (if #ba-graphic exists in the file)
    <output_dir>/anno-graphic.png        (if #anno-graphic exists)
    <output_dir>/slide-1.png .. slide-N.png   (if a carousel with TOTAL slides exists)
    <output_dir>/captions.txt            (every .tab-panel's <pre> text, labeled)
    <output_dir>/manifest.json           (what was exported, sizes, source file, timestamp)
"""
import sys
import os
import re
import json
import base64
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright


def log(msg):
    print(f"[export] {msg}", flush=True)


def save_data_url(data_url: str, out_path: str) -> int:
    b64 = data_url.split(",", 1)[1]
    raw = base64.b64decode(b64)
    with open(out_path, "wb") as f:
        f.write(raw)
    return len(raw)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    content_path = os.path.abspath(sys.argv[1])
    out_dir = os.path.abspath(sys.argv[2])
    os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(content_path):
        log(f"ERROR: {content_path} does not exist")
        sys.exit(1)

    raw_html = open(content_path, encoding="utf-8", errors="ignore").read()

    def find_const(name):
        m = re.search(rf"const {name}\s*=\s*'([^']*)'", raw_html)
        return m.group(1) if m else None

    post_brand = find_const("POST_BRAND")
    post_slug = find_const("POST_SLUG")
    post_type = find_const("POST_TYPE")

    manifest = {
        "sourceFile": content_path,
        "exportedAt": datetime.now(timezone.utc).isoformat(),
        "postBrand": post_brand,
        "postSlug": post_slug,
        "postType": post_type,
        "files": {},
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chromium")
        page = browser.new_page(viewport={"width": 1400, "height": 1200})
        page.goto(f"file://{content_path}", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)

        # ── fixed-id graphics (before/after, annotation) ──
        for gid, fname in [("ba-graphic", "ba-graphic.png"), ("anno-graphic", "anno-graphic.png")]:
            exists = page.evaluate(f"() => !!document.getElementById('{gid}')")
            if not exists:
                log(f"skip {gid} — not present in this file")
                continue
            if not page.evaluate("() => typeof captureFixed === 'function'"):
                log(f"skip {gid} — captureFixed() not defined in this file")
                continue
            log(f"capturing #{gid} ...")
            data_url = page.evaluate(f"async () => {{ const c = await captureFixed('{gid}'); return c.toDataURL('image/png'); }}")
            out_path = os.path.join(out_dir, fname)
            size = save_data_url(data_url, out_path)
            manifest["files"][gid] = {"path": out_path, "bytes": size}
            log(f"  -> {out_path} ({size:,} bytes)")

        # ── carousel slides (if this file has one) ──
        has_carousel = page.evaluate("() => typeof captureSlide === 'function' && typeof TOTAL !== 'undefined'")
        if has_carousel:
            total = page.evaluate("() => TOTAL")
            log(f"capturing {total} carousel slides ...")
            for i in range(total):
                data_url = page.evaluate(f"async () => {{ const c = await captureSlide({i}); return c.toDataURL('image/png'); }}")
                fname = f"slide-{i + 1}.png"
                out_path = os.path.join(out_dir, fname)
                size = save_data_url(data_url, out_path)
                manifest["files"][f"slide-{i + 1}"] = {"path": out_path, "bytes": size}
                log(f"  -> {out_path} ({size:,} bytes)")
        else:
            log("skip carousel — captureSlide()/TOTAL not present in this file")

        # ── captions (post copy tabs) ──
        captions = page.evaluate("""
            () => Array.from(document.querySelectorAll('.tab-panel')).map(el => ({
                id: el.id,
                text: (el.querySelector('pre') ? el.querySelector('pre').innerText : el.innerText).trim()
            }))
        """)
        browser.close()

    if captions:
        cap_path = os.path.join(out_dir, "captions.txt")
        with open(cap_path, "w", encoding="utf-8") as f:
            for c in captions:
                f.write(f"===== {c['id']} =====\n{c['text']}\n\n")
        manifest["files"]["captions"] = {"path": cap_path}
        log(f"  -> {cap_path} ({len(captions)} tabs)")

    manifest_path = os.path.join(out_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    log(f"manifest -> {manifest_path}")
    log("done.")


if __name__ == "__main__":
    main()
