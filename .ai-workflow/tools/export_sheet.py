#!/usr/bin/env python3
"""Export a single-sheet graphic (annotated graphic, variants board) through the page's
OWN captureSheet() (html2canvas, scale 2), not a browser screenshot.

Usage: python3 .ai-workflow/tools/export_sheet.py <page.html> <out.png> [--offline]
--offline serves html2canvas/fonts from offline_assets via sandbox_cdn_route.py (only for
sandboxes that block cdnjs/Google Fonts; note its font CSS has no Caveat, so the
clear-bg annotated graphic must be exported WITHOUT --offline to keep the marker font).
"""
import asyncio, base64, os, sys
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.async_api import async_playwright


async def main(h, o, offline):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1700, "height": 1200})
        if offline:
            from sandbox_cdn_route import install_routes_async
            await install_routes_async(pg)
        await pg.goto(Path(h).resolve().as_uri(), wait_until="domcontentloaded")
        await pg.wait_for_function("typeof captureSheet==='function'")
        await pg.wait_for_timeout(3000)
        d = await pg.evaluate("captureSheet().then(c=>c.toDataURL('image/png'))")
        Path(o).parent.mkdir(parents=True, exist_ok=True)
        Path(o).write_bytes(base64.b64decode(d.split(',')[1]))
        print("wrote", o)
        await b.close()

if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    asyncio.run(main(args[0], args[1], "--offline" in sys.argv))
