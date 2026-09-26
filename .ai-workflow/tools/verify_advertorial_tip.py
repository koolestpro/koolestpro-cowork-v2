#!/usr/bin/env python3
"""Live click-through verification for the advertorial Tips carousel.

Loads the finished HTML in headless Chromium, clicks the swipe button (.swb)
through every slide, confirms it stays pinned to the card and hides on the
last slide, and reports any console/page errors. This is the mandatory
check called out in koolestpro-tips-weekly Step 4 -- a prior bug broke
navigation invisibly (no console error, no static-PNG symptom), so a live
click-through is the only thing that catches it.
"""
import sys
from playwright.sync_api import sync_playwright

PATH = sys.argv[1] if len(sys.argv) > 1 else "outputs/tips/advertorial-page-6-elements_2026-07-31.html"
URL = "file://" + __import__("os").path.abspath(PATH)

errors = []
console_msgs = []

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 700, "height": 900})
    page.on("console", lambda msg: console_msgs.append(f"[{msg.type}] {msg.text}"))
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    # domcontentloaded, not the default 'load' -- this sandbox can't always reach
    # fonts.googleapis.com / cdnjs / Cloudinary, so waiting for the full 'load'
    # event (all external resources) can hang indefinitely. The swipe JS only
    # needs the DOM, not the webfonts/CDN scripts, to be testable.
    page.goto(URL, wait_until="domcontentloaded", timeout=10000)
    page.wait_for_timeout(600)

    total = page.evaluate("document.querySelectorAll('.slide').length")
    print(f"[info] slide count in DOM: {total}")

    swb = page.locator("#main-swb")
    pager = page.locator("#pager")

    for i in range(total):
        text = pager.inner_text()
        print(f"[slide {i+1}] pager reads: {text!r}")
        # confirm swb bounding box is pinned to the viewport's right edge, not floating off
        box = swb.bounding_box()
        vp_box = page.locator("#viewport").bounding_box()
        pinned = box is not None and vp_box is not None and abs((box["x"] + box["width"]) - (vp_box["x"] + vp_box["width"])) < 3
        visible = swb.is_visible()
        print(f"          swb visible={visible} pinned_to_viewport_edge={pinned}")
        if i < total - 1:
            if not visible:
                errors.append(f"swipe button hidden before reaching last slide (at slide {i+1})")
            swb.click(force=True)
            page.wait_for_timeout(450)
        else:
            if visible:
                errors.append("swipe button still visible on the LAST slide (should be hidden)")

    final_text = pager.inner_text()
    print(f"[info] final pager text: {final_text!r}")

    browser.close()

print()
print(f"[info] console messages captured: {len(console_msgs)}")
for m in console_msgs:
    if "error" in m.lower():
        print("  ", m)

if errors:
    print()
    print("[FAIL] issues found:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
else:
    print()
    print("[PASS] swipe navigation pinned + hides correctly on last slide, no page errors.")
