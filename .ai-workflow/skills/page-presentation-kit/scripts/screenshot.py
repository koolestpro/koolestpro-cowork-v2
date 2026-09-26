import sys
import argparse
from playwright.sync_api import sync_playwright

DISMISS_LABELS = [
    "Accept", "Accept All", "Accept all cookies", "I Agree", "I agree",
    "Got it", "OK", "Allow all", "Allow All", "Agree", "Close",
    "No thanks", "Dismiss", "Continue", "X",
]

HIDE_CSS = """
[class*="cookie" i], [id*="cookie" i],
[class*="consent" i], [id*="consent" i],
[class*="newsletter-popup" i], [class*="modal-overlay" i],
[class*="popup" i][class*="overlay" i] {
  display: none !important;
}
"""

def dismiss_popups(page):
    for label in DISMISS_LABELS:
        try:
            btn = page.get_by_role("button", name=label, exact=False).first
            if btn.is_visible(timeout=800):
                btn.click(timeout=800)
                page.wait_for_timeout(400)
                return True
        except Exception:
            continue
    return False

def screenshot(target, output, width=390, height=844, is_file=False,
               full_page=False, clean=False):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
        if is_file:
            page.goto(f"file://{target}")
        else:
            try:
                page.goto(target, wait_until="networkidle", timeout=12000)
            except Exception:
                page.goto(target, wait_until="load", timeout=30000)
        page.wait_for_timeout(1500)

        if clean:
            dismiss_popups(page)
            page.add_style_tag(content=HIDE_CSS)
            page.wait_for_timeout(300)

        page.screenshot(path=output, full_page=full_page)
        browser.close()
        print(f"Saved: {output}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("output")
    ap.add_argument("--file", action="store_true", help="target is a local HTML file, not a URL")
    ap.add_argument("--clean", action="store_true", help="dismiss/hide cookie & popup overlays before capture")
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    ap.add_argument("--full-page", action="store_true")
    args = ap.parse_args()
    screenshot(args.target, args.output, width=args.width, height=args.height,
               is_file=args.file, full_page=args.full_page, clean=args.clean)
