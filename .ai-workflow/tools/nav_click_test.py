#!/usr/bin/env python3
"""
Live navigation click-through test for a Tips carousel HTML file.

Drives the real page with Playwright, clicks the swipe button through every
slide, and asserts:
  - the pager advances one slide per click
  - the track transform matches -idx*540 (slide never orphans/misaligns)
  - the swipe button stays pinned to the card's right edge (within the viewport)
  - the swipe button hides on the last slide
  - zero console errors / page errors

Usage: python3 nav_click_test.py outputs/tips/<file>.html
"""
import sys, os, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from sandbox_cdn_route import install_routes

path = pathlib.Path(sys.argv[1]).resolve()
errors = []

with sync_playwright() as p:
    b = p.chromium.launch(args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 1280, 'height': 1000})
    pg.on('console', lambda m: errors.append(f'console.{m.type}: {m.text}')
          if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
    install_routes(pg)
    # wait_until='load' hangs in this sandbox (external font/CDN requests never
    # settle) — same workaround export_tip_slides.py already uses.
    pg.goto(path.as_uri(), wait_until='domcontentloaded', timeout=20000)
    pg.wait_for_timeout(3500)

    total = pg.evaluate('TOTAL')
    print(f'TOTAL slides reported by page JS: {total}')
    vp_box = pg.locator('#viewport').bounding_box()

    for i in range(total):
        pager = pg.locator('#pager').inner_text()
        transform = pg.evaluate("document.getElementById('track').style.transform")
        swb = pg.locator('#main-swb')
        display = pg.evaluate("document.getElementById('main-swb').style.display")
        box = swb.bounding_box() if display != 'none' else None

        # pager text format varies by generator ("Slide 1 of 7" vs "1 / 7"),
        # so assert on the numbers present rather than an exact string.
        digits = [int(d) for d in __import__('re').findall(r'\d+', pager)]
        if digits[:2] != [i + 1, total]:
            errors.append(f'slide {i+1}: pager reads "{pager}", expected slide {i+1} of {total}')
        # slide 0 has no inline transform until the first goTo() fires, which is
        # correct (the track sits at its natural x=0 position).
        expect_tx = ['', 'translateX(0px)', 'translateX(-0px)'] if i == 0 \
            else [f'translateX(-{i * 540}px)']
        if transform.replace(' ', '') not in [e.replace(' ', '') for e in expect_tx]:
            errors.append(f'slide {i+1}: transform "{transform}", expected "{expect_tx[-1]}"')

        if i == total - 1:
            if display != 'none':
                errors.append(f'slide {i+1}: swipe button NOT hidden on last slide')
            print(f'  slide {i+1}: pager OK · transform OK · swb hidden={display == "none"}')
        else:
            if box is None:
                errors.append(f'slide {i+1}: swipe button missing before last slide')
            else:
                right_gap = (vp_box['x'] + vp_box['width']) - (box['x'] + box['width'])
                if abs(right_gap) > 2:
                    errors.append(
                        f'slide {i+1}: swipe button not pinned to card right edge '
                        f'(gap {right_gap:.1f}px)')
                vert = box['y'] + box['height'] / 2 - (vp_box['y'] + vp_box['height'] / 2)
                if abs(vert) > 3:
                    errors.append(f'slide {i+1}: swipe button not vertically centred ({vert:.1f}px)')
                print(f'  slide {i+1}: pager OK · transform OK · swb pinned '
                      f'(right gap {right_gap:.1f}px)')
                swb.click()
                pg.wait_for_timeout(500)

    b.close()

if errors:
    print('\nFAILED:')
    for e in errors:
        print('  -', e)
    sys.exit(1)
print('\nnav click-through: PASS (no console/page errors)')
