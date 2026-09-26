#!/usr/bin/env python3
"""
Playwright request routing for this sandbox's blocked CDNs.

Why this exists (discovered 2026-08-21): this workspace's network allowlist does
NOT reach cdnjs.cloudflare.com or fonts.googleapis.com. Every generated carousel
HTML loads html2canvas + jsPDF from cdnjs via blocking <script src> tags in
<head>, so a Playwright `page.goto()` against one of those files never even
reaches DOMContentLoaded — it hangs until timeout. Google Fonts CSS is blocked
the same way, which would silently render every export in a fallback typeface
and make a visual QA pass meaningless.

Fix: intercept those requests and fulfil them from locally cached copies in
offline_assets/ (fetched from unpkg/jsdelivr, which ARE reachable). The HTML
files themselves are left untouched — they keep their cdnjs/Google Fonts URLs,
which work normally on Ridwan's own machine. This is a test-harness concern only.

Usage:
    from sandbox_cdn_route import install_routes      # sync API
    install_routes(page)

    from sandbox_cdn_route import install_routes_async  # async API
    await install_routes_async(page)
"""
import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'offline_assets')
FONTS = os.path.join(ASSETS, 'fonts')

FONT_CSS = """
@font-face{font-family:'Syne';font-style:normal;font-weight:400;font-display:block;src:url(https://cdn.jsdelivr.net/npm/@fontsource/syne@5.0.0/files/syne-latin-400-normal.woff2) format('woff2');}
@font-face{font-family:'Syne';font-style:normal;font-weight:500;font-display:block;src:url(https://cdn.jsdelivr.net/npm/@fontsource/syne@5.0.0/files/syne-latin-500-normal.woff2) format('woff2');}
@font-face{font-family:'Syne';font-style:normal;font-weight:600;font-display:block;src:url(https://cdn.jsdelivr.net/npm/@fontsource/syne@5.0.0/files/syne-latin-600-normal.woff2) format('woff2');}
@font-face{font-family:'Syne';font-style:normal;font-weight:700;font-display:block;src:url(https://cdn.jsdelivr.net/npm/@fontsource/syne@5.0.0/files/syne-latin-700-normal.woff2) format('woff2');}
@font-face{font-family:'Syne';font-style:normal;font-weight:800;font-display:block;src:url(https://cdn.jsdelivr.net/npm/@fontsource/syne@5.0.0/files/syne-latin-800-normal.woff2) format('woff2');}
@font-face{font-family:'DM Mono';font-style:normal;font-weight:300;font-display:block;src:url(https://cdn.jsdelivr.net/npm/@fontsource/dm-mono@5.0.0/files/dm-mono-latin-300-normal.woff2) format('woff2');}
@font-face{font-family:'DM Mono';font-style:normal;font-weight:400;font-display:block;src:url(https://cdn.jsdelivr.net/npm/@fontsource/dm-mono@5.0.0/files/dm-mono-latin-400-normal.woff2) format('woff2');}
@font-face{font-family:'DM Mono';font-style:normal;font-weight:500;font-display:block;src:url(https://cdn.jsdelivr.net/npm/@fontsource/dm-mono@5.0.0/files/dm-mono-latin-500-normal.woff2) format('woff2');}
@font-face{font-family:'DM Mono';font-style:italic;font-weight:300;font-display:block;src:url(https://cdn.jsdelivr.net/npm/@fontsource/dm-mono@5.0.0/files/dm-mono-latin-300-italic.woff2) format('woff2');}
@font-face{font-family:'DM Mono';font-style:italic;font-weight:400;font-display:block;src:url(https://cdn.jsdelivr.net/npm/@fontsource/dm-mono@5.0.0/files/dm-mono-latin-400-italic.woff2) format('woff2');}
"""

_JS_MAP = {
    'html2canvas': 'html2canvas.min.js',
    'jspdf': 'jspdf.umd.min.js',
}


def _local_js(url):
    for key, fname in _JS_MAP.items():
        if key in url:
            path = os.path.join(ASSETS, fname)
            if os.path.exists(path):
                return open(path, 'rb').read()
    return None


def _local_font(url):
    name = url.rsplit('/', 1)[-1].split('?')[0]
    path = os.path.join(FONTS, name)
    return open(path, 'rb').read() if os.path.exists(path) else None


def install_routes(page):
    """Sync Playwright: serve blocked CDN assets from the local cache."""
    def handle(route):
        url = route.request.url
        if 'cdnjs.cloudflare.com' in url:
            body = _local_js(url)
            if body is not None:
                return route.fulfill(status=200, content_type='application/javascript',
                                     body=body)
            return route.fulfill(status=200, content_type='application/javascript', body=b'')
        if 'fonts.googleapis.com' in url:
            return route.fulfill(status=200, content_type='text/css', body=FONT_CSS)
        if 'jsdelivr.net' in url and url.endswith('.woff2'):
            body = _local_font(url)
            if body is not None:
                return route.fulfill(status=200, content_type='font/woff2', body=body)
        return route.continue_()

    page.route('**/*', handle)


async def install_routes_async(page):
    """Async Playwright: same behaviour as install_routes."""
    async def handle(route):
        url = route.request.url
        if 'cdnjs.cloudflare.com' in url:
            body = _local_js(url)
            if body is not None:
                return await route.fulfill(status=200, content_type='application/javascript',
                                           body=body)
            return await route.fulfill(status=200, content_type='application/javascript', body=b'')
        if 'fonts.googleapis.com' in url:
            return await route.fulfill(status=200, content_type='text/css', body=FONT_CSS)
        if 'jsdelivr.net' in url and url.endswith('.woff2'):
            body = _local_font(url)
            if body is not None:
                return await route.fulfill(status=200, content_type='font/woff2', body=body)
        return await route.continue_()

    await page.route('**/*', handle)
