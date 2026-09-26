"""
capture_scroll_depth.py — capture a screenshot at a specific scroll depth
(hero / mid / footer / any fraction) after walking the whole page top-to-
bottom first, so scroll-triggered reveal animations (GSAP/IntersectionObserver)
have already fired before the screenshot is taken. Used to source the 2-3
genuinely-different screenshots build_device_still.py's `preview` mode needs,
and the single hero screenshots `cover` mode needs.

Usage:
  python3 capture_scroll_depth.py "/path/to/page.html" out.png --file \
      --width 390 --height 844 --frac 0.0
  python3 capture_scroll_depth.py "/path/to/page.html" out.png --file \
      --width 1600 --height 966 --frac 0.5
"""

import argparse
from playwright.sync_api import sync_playwright


def capture(target, output, width, height, is_file, frac, settle_ms=550, step_frac=0.85):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=2)
        page = context.new_page()

        if is_file:
            page.goto(f"file://{target}")
        else:
            try:
                page.goto(target, wait_until="networkidle", timeout=12000)
            except Exception:
                page.goto(target, wait_until="load", timeout=30000)
        page.wait_for_timeout(1200)

        total_height = page.evaluate("document.body.scrollHeight")
        step = int(height * step_frac)

        # Walk top -> bottom first so one-shot reveal animations fire.
        y = 0
        while y < total_height:
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(settle_ms)
            y += step
        page.evaluate(f"window.scrollTo(0, {total_height})")
        page.wait_for_timeout(settle_ms)

        total_height = page.evaluate("document.body.scrollHeight") or total_height
        target_y = max(0, min(total_height - height, int((total_height - height) * frac)))
        page.evaluate(f"window.scrollTo(0, {target_y})")
        page.wait_for_timeout(700)

        page.screenshot(path=output)
        context.close()
        browser.close()
        print(f"Saved: {output} (scroll_y={target_y} of {total_height - height})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("output")
    ap.add_argument("--file", action="store_true")
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    ap.add_argument("--frac", type=float, default=0.0, help="0.0=hero/top, 0.5=mid, 1.0=footer/bottom")
    args = ap.parse_args()
    capture(args.target, args.output, args.width, args.height, args.file, args.frac)
