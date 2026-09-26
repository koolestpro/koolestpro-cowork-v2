"""
build_mosaic.py — capture a page's ENTIRE scroll length at desktop viewport
width and tile it into a 2-per-row grid mosaic.

Fixes two confirmed bugs from the first real run
(outputs/templates/kura_hp-01_2026-07-13/kura_hp-01-full-mosaic.png):

  1. Blank navy panels: the page uses scroll-triggered reveal animations
     (GSAP / IntersectionObserver fade-ins). A single naive full_page
     screenshot captures those sections in their PRE-reveal (often blank or
     near-blank) state, because the browser never actually scrolled them
     into view. Fix: scroll incrementally top-to-bottom first (same idea as
     scroll_video.py's capture, just stepped instead of eased/continuous),
     waiting after each step so one-shot reveal animations fire and settle,
     THEN take the full-page screenshot from a browser that has already
     "seen" every section once.

  2. Blind fixed-height slicing: cutting the page into N equal-height bands
     ignores where the real section boundaries are, so a cut can land mid-
     section or entirely inside a large blank transition zone. Fix: scan
     row-wise pixel variance (a cheap proxy for "is there content here")
     and place cuts at local minima near each evenly-spaced target instead
     of blindly at the target itself, then merge any resulting band whose
     average content density is still below threshold into its neighbor.

Usage:
  python3 build_mosaic.py "/path/to/page.html" out.png --file --width 1440
  python3 build_mosaic.py "https://example.com" out.png --width 1440 --cols 2
"""

import argparse
import subprocess
import sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright


def capture_full_page(target, width, is_file, clean=False, step_frac=0.85, settle_ms=550):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": width, "height": 1000}, device_scale_factor=1)
        page = context.new_page()

        if is_file:
            page.goto(f"file://{target}")
        else:
            try:
                page.goto(target, wait_until="networkidle", timeout=12000)
            except Exception:
                page.goto(target, wait_until="load", timeout=30000)
        page.wait_for_timeout(1200)

        if clean:
            HIDE_CSS = """
            [class*="cookie" i], [id*="cookie" i],
            [class*="consent" i], [id*="consent" i] { display:none !important; }
            """
            page.add_style_tag(content=HIDE_CSS)

        total_height = page.evaluate("document.body.scrollHeight")
        viewport_height = 1000
        step = int(viewport_height * step_frac)

        # Pass 1: walk the whole page top -> bottom so one-shot reveal
        # animations (IntersectionObserver / GSAP ScrollTrigger) fire.
        y = 0
        while y < total_height:
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(settle_ms)
            y += step
        page.evaluate(f"window.scrollTo(0, {total_height})")
        page.wait_for_timeout(settle_ms)

        # Recheck height (lazy content / infinite sections can grow it) then
        # settle back at the top for a clean full-page capture.
        total_height = page.evaluate("document.body.scrollHeight") or total_height
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(400)

        png_bytes = page.screenshot(full_page=True)
        context.close()
        browser.close()
    return png_bytes


def content_density_profile(img_arr, smooth=15):
    """Row-wise std-dev of grayscale intensity, smoothed. Low value = blank/
    near-uniform row (background color, empty transition space)."""
    gray = img_arr.mean(axis=2)
    row_std = gray.std(axis=1)
    kernel = np.ones(smooth) / smooth
    smoothed = np.convolve(row_std, kernel, mode="same")
    return smoothed


def choose_cut_points(profile, n_tiles, search_frac=0.18):
    h = len(profile)
    target_step = h / n_tiles
    cuts = [0]
    for i in range(1, n_tiles):
        target = int(i * target_step)
        window = int(target_step * search_frac)
        lo, hi = max(target - window, cuts[-1] + 1), min(target + window, h - 1)
        if lo >= hi:
            cuts.append(target)
            continue
        local = profile[lo:hi]
        best = lo + int(np.argmin(local))
        cuts.append(best)
    cuts.append(h)
    return cuts


def excise_dead_zones(img, profile, min_run=140, density_ratio=0.22, pad=24):
    """Splice out sustained near-uniform vertical runs before tiling at all.

    Full-page screenshots can't represent scroll-scrubbed / pinned
    ScrollTrigger sections correctly (their visual state is a function of
    live scroll position, not something that stays "revealed" once you've
    scrolled past it) — those sections often bake out as a long flat-color
    dead zone in a static capture. Rather than showing that as its own
    boring tile (or diluting a content tile by merging blank space into
    it), cut those runs out of the image entirely before slicing, the same
    way you'd trim dead air out of a video. `pad` keeps a small buffer of
    the on either side so a cut doesn't slice flush against real content.
    """
    page_avg = profile.mean()
    threshold = page_avg * density_ratio
    below = profile < threshold

    runs = []
    start = None
    for i, is_dead in enumerate(below):
        if is_dead and start is None:
            start = i
        elif not is_dead and start is not None:
            if i - start >= min_run:
                runs.append((start, i))
            start = None
    if start is not None and len(below) - start >= min_run:
        runs.append((start, len(below)))

    if not runs:
        return img, []

    w, h = img.size
    keep_ranges = []
    prev_end = 0
    for s, e in runs:
        s2, e2 = max(s + pad, prev_end), min(e - pad, h)
        if s2 > prev_end:
            keep_ranges.append((prev_end, s2))
        prev_end = max(e2, prev_end)
    if prev_end < h:
        keep_ranges.append((prev_end, h))

    strips = [img.crop((0, a, w, b)) for a, b in keep_ranges if b > a]
    spliced = Image.new("RGB", (w, sum(s.height for s in strips)))
    y = 0
    for s in strips:
        spliced.paste(s, (0, y))
        y += s.height
    return spliced, runs


def build_mosaic(png_bytes, out_path, cols=2, tile_pad=14, canvas_pad=24, bg=(8, 8, 10)):
    img = Image.open(__import__("io").BytesIO(png_bytes)).convert("RGB")
    arr = np.asarray(img)
    profile = content_density_profile(arr)

    img, dead_runs = excise_dead_zones(img, profile)
    if dead_runs:
        print(f"Excised {len(dead_runs)} dead zone(s) totaling "
              f"{sum(e - s for s, e in dead_runs)}px (likely scroll-pinned/scrubbed "
              f"sections that only render correctly at a live scroll position).")

    arr = np.asarray(img)
    h, w = arr.shape[:2]
    profile = content_density_profile(arr)

    target_tile_h = w * 0.62
    n_tiles = max(6, min(10, round(h / target_tile_h)))
    if n_tiles % cols != 0:
        n_tiles += cols - (n_tiles % cols)

    cuts = choose_cut_points(profile, n_tiles)

    tiles = [img.crop((0, cuts[i], w, cuts[i + 1])) for i in range(len(cuts) - 1)]
    # pad tile count up to a multiple of cols by splitting the tallest tile
    while len(tiles) % cols != 0:
        idx = max(range(len(tiles)), key=lambda i: tiles[i].height)
        t = tiles.pop(idx)
        half = t.height // 2
        tiles.insert(idx, t.crop((0, 0, t.width, half)))
        tiles.insert(idx + 1, t.crop((0, half, t.width, t.height)))

    rows = len(tiles) // cols
    tile_w = w
    row_heights = [max(tiles[r * cols + c].height for c in range(cols)) for r in range(rows)]
    canvas_w = cols * tile_w + (cols + 1) * tile_pad + 2 * canvas_pad
    canvas_h = sum(row_heights) + (rows + 1) * tile_pad + 2 * canvas_pad

    canvas = Image.new("RGB", (canvas_w, canvas_h), bg)
    y = canvas_pad + tile_pad
    for r in range(rows):
        x = canvas_pad + tile_pad
        for c in range(cols):
            t = tiles[r * cols + c]
            canvas.paste(t, (x, y))
            x += tile_w + tile_pad
        y += row_heights[r] + tile_pad

    canvas.save(out_path)
    print(f"Saved: {out_path} ({canvas_w}x{canvas_h}, {len(tiles)} tiles, {rows} rows x {cols} cols)")
    return len(tiles), rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("output")
    ap.add_argument("--file", action="store_true")
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--cols", type=int, default=2)
    args = ap.parse_args()

    png_bytes = capture_full_page(args.target, args.width, args.file, args.clean)
    build_mosaic(png_bytes, args.output, cols=args.cols)
