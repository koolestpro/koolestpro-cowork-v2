#!/usr/bin/env python3
"""Export a Tips carousel's slides using the page's OWN html2canvas capture path.

Drives headless Chromium against a finished outputs/tips/*.html file and calls the
file's real dlSlide(i) function, intercepting each download. Output is byte-identical
to clicking the on-page download buttons — NOT a generic browser screenshot, which
renders gradients and blur differently than html2canvas does.

Setup: see .ai-workflow/tools/README.md (ARM64 Playwright recipe).
Requires LD_LIBRARY_PATH to include the extracted libXdamage dir.

Usage:
  python3 export_tip_slides.py outputs/tips/<file>.html outputs/tips/<assets-dir>/
"""
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.async_api import async_playwright
from sandbox_cdn_route import install_routes_async


async def main(html_path: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        page = await browser.new_page(viewport={"width": 1200, "height": 1000})
        # ROOT CAUSE of the 2026-07-31 "goto hangs" note below, found 2026-08-21:
        # this sandbox's network allowlist does NOT reach cdnjs.cloudflare.com or
        # fonts.googleapis.com (curl to both hangs; unpkg/jsdelivr/Cloudinary are
        # fine). The blocking <script src> tags for html2canvas/jsPDF therefore
        # stall the parser and DOMContentLoaded never fires. Worse, the blocked
        # Google Fonts CSS would silently render every export in a fallback
        # typeface, which makes a visual QA pass meaningless. install_routes_async
        # serves all three from a local cache so captures match the real thing.
        await install_routes_async(page)
        # wait_until='load' can still hang on other remote assets, and
        # 'domcontentloaded' is enough: dlSlide is defined by a normal
        # (non-deferred) inline <script> that runs synchronously during parse, so
        # it exists by the time domcontentloaded fires, and the explicit
        # wait_for_function below still guards against timing races.
        await page.goto(html_path.resolve().as_uri(), wait_until="domcontentloaded", timeout=15000)
        await page.wait_for_function("typeof dlSlide === 'function'")
        # let webfonts + cloudinary avatar settle before any capture
        await page.wait_for_timeout(3500)

        total = await page.evaluate("TOTAL")
        print(f"{total} slides detected")

        for i in range(total):
            async with page.expect_download(timeout=60000) as dl_info:
                await page.evaluate(f"dlSlide({i})")
            download = await dl_info.value
            dest = out_dir / f"slide{i + 1}.png"
            await download.save_as(dest)
            print(f"  wrote {dest.name}")

        await browser.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    asyncio.run(main(Path(sys.argv[1]), Path(sys.argv[2])))
