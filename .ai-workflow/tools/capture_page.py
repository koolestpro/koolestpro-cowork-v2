#!/usr/bin/env python3
"""capture_page.py - Lovable / Figma Make capture handoff (2026-09-13).

The rebuild quality bar lives in Lovable and Figma Make (see
docs/system/rebuild-tooling-and-quality.md). This is the one step that connects a
finished page back into this pipeline: give it a published URL (or a local export
from a Lovable repo), and it returns the exact screenshots the mockup, carousel
and recap builders expect.

It produces, per brand:
  <brand>-mobile.png    390x844 @2  -> 780x1688  (above the fold; the phone screen)
  <brand>-full.png      full page @2             (tall shot for strips / mobile-strip)
  <brand>-desktop.png   1440x900 @2              (only with --device desktop/both)

Same mobile viewport and device_scale_factor as the rest of the pipeline, and
reduced motion, so the capture drops straight into build_device_still.py without
resizing or re-capturing.

Usage (run with the project venv that has Playwright):
  python3 capture_page.py --url https://my-app.lovable.app --brand getfit
  python3 capture_page.py --url https://my-app.lovable.app --brand getfit --device both --full
  python3 capture_page.py --file /path/to/dist/index.html --brand getfit --full

Output dir default: outputs/cro-fixes/_capture/<brand>/
Prints a JSON summary (paths + the pipeline fields) so the next step can consume it.
"""
import argparse
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Playwright not found. Install it in this venv: pip install playwright && "
             "playwright install chromium (see .ai-workflow/tools/README.md).")

# Reuse screenshot.py's popup handling so behavior matches the existing tool.
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from screenshot import dismiss_popups, HIDE_CSS
except Exception:  # keep the tool usable even if screenshot.py moves
    def dismiss_popups(page):
        return False
    HIDE_CSS = ""

ROOT = Path(__file__).resolve().parents[2]
MOBILE = {"width": 390, "height": 844}
DESKTOP = {"width": 1440, "height": 900}


def _load(page, target, is_file):
    if is_file:
        page.goto(f"file://{target}", wait_until="load", timeout=45000)
    else:
        try:
            page.goto(target, wait_until="networkidle", timeout=12000)
        except Exception:
            page.goto(target, wait_until="load", timeout=45000)
    page.wait_for_timeout(1500)


def _shoot(browser, target, is_file, viewport, out_path, full_page, clean):
    page = browser.new_page(viewport=viewport, device_scale_factor=2,
                            reduced_motion="reduce")
    try:
        _load(page, target, is_file)
        if clean:
            dismiss_popups(page)
            if HIDE_CSS:
                page.add_style_tag(content=HIDE_CSS)
            page.wait_for_timeout(300)
        page.screenshot(path=str(out_path), full_page=full_page)
    finally:
        page.close()
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="published URL (Lovable publish, Figma Make share, live site)")
    src.add_argument("--file", help="local HTML file (e.g. a Lovable repo export build)")
    ap.add_argument("--brand", required=True, help="brand/slug used to name the files")
    ap.add_argument("--out", help="output dir (default outputs/cro-fixes/_capture/<brand>/)")
    ap.add_argument("--device", default="both", choices=["mobile", "desktop", "both"])
    ap.add_argument("--full", action="store_true", help="also capture the full mobile page (tall)")
    ap.add_argument("--no-clean", action="store_true", help="skip popup dismissal / overlay hiding")
    args = ap.parse_args()

    out_dir = Path(args.out) if args.out else ROOT / "outputs" / "cro-fixes" / "_capture" / args.brand
    out_dir.mkdir(parents=True, exist_ok=True)
    target = args.file or args.url
    is_file = bool(args.file)
    clean = not args.no_clean
    assets = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        try:
            if args.device in ("mobile", "both"):
                assets["mobile"] = str(_shoot(
                    browser, target, is_file, MOBILE,
                    out_dir / f"{args.brand}-mobile.png", False, clean))
                if args.full:
                    assets["full"] = str(_shoot(
                        browser, target, is_file, MOBILE,
                        out_dir / f"{args.brand}-full.png", True, clean))
            if args.device in ("desktop", "both"):
                assets["desktop"] = str(_shoot(
                    browser, target, is_file, DESKTOP,
                    out_dir / f"{args.brand}-desktop.png", False, clean))
        finally:
            browser.close()

    for k, v in assets.items():
        print(f"Saved: {v}")
    summary = {
        "brand": args.brand,
        "source": target,
        "source_type": "file" if is_file else "url",
        "status": "Created",
        "assets": assets,
        "next": "feed the mobile shot into build_device_still.py / carousel / recap builders",
    }
    print("CAPTURE_SUMMARY " + json.dumps(summary))


if __name__ == "__main__":
    main()
