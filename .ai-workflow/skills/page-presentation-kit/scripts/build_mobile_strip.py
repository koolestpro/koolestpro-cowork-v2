"""
build_mobile_strip.py — capture a page's ENTIRE scroll length at MOBILE
viewport width and lay it out as N side-by-side columns, so the whole page
reads at a glance as one wide image.

WHY THIS EXISTS (2026-09-02, Ridwan's call). A QA contact sheet built during
the halos-li-02 listicle build — the full mobile page sliced into 6 columns
placed side by side — turned out to read better as a shareable asset than
anything already in the kit: "I love this image, add it to outputs and preview
in the future." It is now a registered Template Showcase asset
(`{slug}-mobile-strip.png`, key `TS-{BRAND}-MOBILESTRIP`) and gets its own X
post. See koolestpro-cowork-v2/CLAUDE.md.

HOW IT DIFFERS FROM ITS TWO NEIGHBOURS, both of which stay as they are:
  - build_split_page.py  — DESKTOP width, exactly TWO columns, light neutral
    background, meant as a straightforward "read the whole page" reference.
  - build_device_still.py — device bezels, a few phones at chosen scroll
    depths, brand background. A styled hero asset, not the whole page.
  - this script          — MOBILE width, MANY columns, the entire page end to
    end with nothing omitted. The appeal is density: you see every section of
    a responsive build in one frame.

Shares build_split_page.py's capture and analysis rather than reimplementing
them, so fixes to the sticky-header / fixed-element / reveal-animation
handling land in both. Two things are added on top:

  1. TILE-STITCH FALLBACK. `full_page=True` crashes the renderer outright on
     some image-heavy pages in this sandbox even with --disable-dev-shm-usage
     (reproduced on halos-li-02, 2026-09-02: the crash lands partway down the
     page, not at the screenshot call). When the one-shot capture dies, this
     falls back to scrolling and stitching viewport tiles, which has never
     crashed. Same pixels, slower.

  2. N-COLUMN SEAM SNAPPING. build_split_page picks ONE cut snapped to a real
     section gap. This generalizes that to N-1 cuts so no column boundary
     slices through the middle of a section.

TWO MODES (--mode, default `post`):

  post (DEFAULT, 2026-09-19)  The deliverable. A fixed standard post canvas
    that the content fills completely: 1080x1350 by default, `--size
    square|story|landscape` for the others. At most 5 columns, and the real
    count is the largest the page can actually fill, because a column the page
    cannot fill is dead space at the bottom. Covering the whole canvas outranks
    showing every section, so the tail of a long page is simply not in the post.
    Ridwan's correction: "it should be made in a format I can post on social, it
    should always take the full page, no empty space should be visual especially
    on the lower parts... as long as it covers the whole space, we can leave any
    missing part, max of 5 columns... and we must use a standard post dimension."

  contact-sheet  The original behaviour, kept for QA. The whole page in exactly
    --columns columns at native mobile width, canvas sized to whatever that comes
    to. Ragged column bottoms are filled with each column's own edge colour, but
    the result is not a postable shape, which is why it is no longer the default.

SPACING (post mode, 2026-09-19). A 12px gap sits BETWEEN columns, never around
the outside. Ridwan: "I think we should give them a little gap inbetween to
create distinctions." Without it a dark column running straight into a cream one
reads as one continuous page rather than three views of it. The gap is a
separator, not a frame, so the canvas is still covered edge to edge and the
no-dead-space rule is untouched. `--gap` / `--gap-color` override it.
Contact-sheet mode stays fully flush (gap=0). Neither is the preview.png spacing
rule (generous outer margins, thin inner gaps) — that one is about a few
floating phone mockups and does not apply here.

Usage:
  python3 build_mobile_strip.py "/path/to/page.html" out.png --file
  python3 build_mobile_strip.py "https://example.com" out.png --size square
  python3 build_mobile_strip.py "/path/to/page.html" qa.png --file \\
      --mode contact-sheet --columns 6
"""

import argparse
import io
# QUALITY NOTE (2026-09-19, Ridwan's feedback on the kura_pdp-02 run): the
# reference/gold-standard output for "post" mode is
# outputs/templates/halos_pp-01_.../halos-pp-01-mobile-strip.png (3 columns,
# 1080x1350, canvas fully covered, tight and dense — "goes out well"). On a
# very long page (e.g. kura_pdp-02, ~11,494px tall at 390 width) the
# max-columns-that-fill-the-canvas logic can settle on just 2 columns at a
# low scale, which reads sparser and is "not ideal" per Ridwan. When a run
# produces only 2 columns, sanity-check whether a taller/narrower crop or a
# different --max-columns would land closer to the halos-pp-01 density
# before treating the output as final — don't just accept whatever column
# count the script picks on a long page without a look.

import os
import sys

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_split_page import (  # noqa: E402
    capture_full_page,
    content_density_profile,
    excise_dead_zones,
)

REVEAL_JS = """() => {
  document.querySelectorAll('.fade-in,.fade-up,[data-reveal],[data-split]').forEach(el => {
    el.classList.add('visible','in-view','is-visible');
    el.style.setProperty('opacity', '1', 'important');
    el.style.setProperty('transform', 'none', 'important');
  });
  document.querySelectorAll('*').forEach(el => {
    const pos = getComputedStyle(el).position;
    if (pos === 'fixed') el.style.setProperty('display', 'none', 'important');
    else if (pos === 'sticky') el.style.setProperty('position', 'static', 'important');
  });
}"""


def capture_tiled(target, width, is_file, height=844, settle_ms=380, attempts=6):
    """Scroll-and-stitch fallback for pages whose full_page capture crashes.

    Tiles already captured survive across attempts, so a crash partway down
    costs only the remaining tiles rather than restarting the whole page.
    """
    url = f"file://{target}" if is_file else target
    tiles, total = {}, None

    for attempt in range(1, attempts + 1):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    args=["--disable-dev-shm-usage", "--disable-gpu", "--no-sandbox"])
                page = browser.new_page(viewport={"width": width, "height": height},
                                        device_scale_factor=1)
                try:
                    page.goto(url, wait_until="load", timeout=15000)
                except Exception:
                    page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(1200)
                page.add_style_tag(content="*,*::before,*::after{"
                                           "animation:none !important;transition:none !important}")
                page.evaluate(REVEAL_JS)
                total = page.evaluate("document.documentElement.scrollHeight")

                y = 0
                while y < total:
                    if y in tiles:
                        y += height
                        continue
                    page.evaluate(f"window.scrollTo(0,{y})")
                    page.wait_for_timeout(settle_ms)   # let lazy images decode
                    page.evaluate(REVEAL_JS)
                    page.wait_for_timeout(160)
                    tiles[y] = (page.evaluate("window.scrollY"),
                                page.screenshot(full_page=False))
                    y += height

                broken = page.evaluate("""() => [...document.images]
                    .filter(i => !i.complete || i.naturalWidth === 0)
                    .map(i => i.getAttribute('src'))""")
                if broken:
                    print(f"WARNING: {len(broken)} image(s) still unloaded: {broken}")
                browser.close()
            break
        except Exception as exc:
            print(f"  tiled capture attempt {attempt}: {type(exc).__name__} "
                  f"after {len(tiles)} tiles, retrying", flush=True)
    else:
        raise RuntimeError(f"tiled capture failed after {attempts} attempts")

    canvas = Image.new("RGB", (width, total), "white")
    for _, (real_y, png) in sorted(tiles.items()):
        tile = Image.open(io.BytesIO(png)).convert("RGB")
        canvas.paste(tile, (0, min(real_y, total - tile.height)))
    buf = io.BytesIO()
    canvas.save(buf, format="PNG")
    return buf.getvalue()


def capture(target, width, is_file, clean=False):
    """One-shot capture, falling back to tiles if the renderer dies."""
    try:
        png = capture_full_page(target, width, is_file, clean=clean)
        print("Captured via full_page screenshot.")
    except Exception as exc:
        print(f"full_page capture failed ({type(exc).__name__}); "
              f"falling back to tile stitching.")
        png = capture_tiled(target, width, is_file)
    return _crop_to_width(png, width)


def _crop_to_width(png, width):
    """2026-09-30: Playwright's full_page mode can capture wider than the real
    viewport on pages with will-change carousels even when the page is not
    actually scrolling sideways (moult-pdp-01: 1170px+ wide, content in the left
    390px). plan_post_columns derives scale from the image width, so a wide
    capture shrank the columns to ~40% and left the canvas mostly blank. Crop to
    the true mobile width before anything downstream measures it."""
    img = Image.open(io.BytesIO(png))
    if img.width <= width:
        return png
    print(f"Capture was {img.width}px wide; cropping to {width}px.")
    buf = io.BytesIO()
    img.convert("RGB").crop((0, 0, width, img.height)).save(buf, format="PNG")
    return buf.getvalue()


def choose_split_points(profile, n_cols, search_frac=0.10, gap_ratio=0.40, min_gap_run=30):
    """Pick n_cols-1 cuts, each snapped to a genuine section seam.

    Generalizes build_split_page.choose_split_point to N cuts. Each nominal
    boundary (h*i/n) is snapped to the centre of the nearest sustained
    low-density run inside a window around it. A run must be at least
    min_gap_run tall to qualify — the 2026-08-23 halos_lp-01 lesson: a 1-2px
    flat band *inside* a section otherwise wins on proximity alone and the cut
    lands mid-content. Falls back to the nominal position when no real seam is
    available, which is correct: an even cut beats a bad snap.
    """
    h = len(profile)
    window = max(int(h * search_frac), 1)
    threshold = profile.mean() * gap_ratio
    below = profile < threshold

    cuts, prev = [], 0
    for i in range(1, n_cols):
        target = h * i // n_cols
        lo, hi = max(target - window, prev + 1), min(target + window, h - 1)

        runs, start = [], None
        for j in range(lo, hi):
            if below[j] and start is None:
                start = j
            elif not below[j] and start is not None:
                runs.append((start, j))
                start = None
        if start is not None:
            runs.append((start, hi))
        runs = [r for r in runs if r[1] - r[0] >= min_gap_run]

        if runs:
            best = min(runs, key=lambda r: abs((r[0] + r[1]) // 2 - target))
            cut = (best[0] + best[1]) // 2
        else:
            cut = target
        cuts.append(cut)
        prev = cut
    return cuts


# Ridwan, 2026-09-19: "I think we should give them a little gap inbetween to
# create distinctions." A hairline between columns, not a frame: gaps sit
# BETWEEN columns only, never around the outside, so the canvas still reads as
# fully covered. 12px at 1080 wide is about 1.1% of the width, enough to
# separate a dark column from a cream one without looking like a grid.
POST_GAP = 12
POST_GAP_COLOR = (255, 255, 255)

POST_SIZES = {
    "portrait":  (1080, 1350),   # 4:5 — LinkedIn / Instagram feed, the default
    "square":    (1080, 1080),   # 1:1
    "story":     (1080, 1920),   # 9:16 — stories / reels covers
    "landscape": (1200, 675),    # 16:9 — X
}


def post_column_widths(canvas_w, n, gap):
    """Integer column widths that, with the gaps, sum to exactly canvas_w."""
    usable = canvas_w - (n - 1) * gap
    base, extra = divmod(usable, n)
    return [base + (1 if i < extra else 0) for i in range(n)]


def plan_post_columns(page_h, page_w, canvas_w, canvas_h, max_columns=5, gap=0):
    """Largest column count (<= max_columns) that the page can FILL completely.

    Column width is (canvas_w - gaps)/n, so the scale is forced, and each column
    therefore shows canvas_h/scale page pixels. Pick the biggest n whose demand
    the page can actually meet. Fewer columns on a short page is the whole
    point: a column the page cannot fill is empty space at the bottom, which is
    the one thing this asset must never have.
    """
    for n in range(max_columns, 0, -1):
        col_w = post_column_widths(canvas_w, n, gap)[0]
        col_page_h = canvas_h * page_w / col_w
        if n * col_page_h <= page_h:
            return n, col_page_h
    col_w = post_column_widths(canvas_w, 1, gap)[0]
    return 1, canvas_h * page_w / col_w


def choose_post_starts(profile, n_cols, col_page_h, page_h,
                       search_frac=0.06, gap_ratio=0.40, min_gap_run=24):
    """Column start offsets, nudged FORWARD onto real section seams.

    Unlike the contact-sheet mode, columns here are a fixed height and the page
    is longer than the canvas needs, so there is slack to spend. Each start is
    pushed forward (never back) to the next genuine low-density seam, which
    skips a little content rather than slicing a section in half. Total forward
    movement is capped by the slack so the final column still lands inside the
    page.
    """
    slack = page_h - n_cols * col_page_h
    window = max(int(col_page_h * search_frac), 1)
    threshold = profile.mean() * gap_ratio
    below = profile < threshold

    starts, spent = [0], 0.0
    for i in range(1, n_cols):
        nominal = starts[-1] + col_page_h
        budget = min(window, slack - spent)
        lo, hi = int(nominal), int(min(nominal + budget, page_h - col_page_h))

        chosen = nominal
        if hi > lo:
            run_start = None
            for j in range(lo, hi):
                if below[j] and run_start is None:
                    run_start = j
                elif not below[j] and run_start is not None:
                    if j - run_start >= min_gap_run:
                        chosen = (run_start + j) / 2
                        break
                    run_start = None
            else:
                if run_start is not None and hi - run_start >= min_gap_run:
                    chosen = (run_start + hi) / 2
        spent += chosen - nominal
        starts.append(chosen)
    return starts


def build_post(png_bytes, out_path, size="portrait", max_columns=5,
               gap=POST_GAP, gap_color=POST_GAP_COLOR, excise=True, max_bytes=None):
    """Lay the mobile page out as a postable image at a standard post size.

    Ridwan, 2026-09-19: "it should be made in a format I can post on social, it
    should always take the full page, no empty space should be visual especially
    on the lower parts... max of 5 columns, but it should cover the whole space
    and we must use a standard post dimension."

    So the canvas is fixed and the content bends to it, which is the opposite of
    the contact-sheet mode below (where the page was fixed and the canvas bent
    to it, leaving ragged column bottoms). Covering the whole canvas matters more
    than showing every section, so the tail of a long page is simply not in the
    post.
    """
    canvas_w, canvas_h = POST_SIZES[size] if isinstance(size, str) else size
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")

    if excise:
        profile = content_density_profile(np.asarray(img))
        img, dead = excise_dead_zones(img, profile)
        if dead:
            print(f"Excised {len(dead)} dead zone(s) totaling "
                  f"{sum(e - s for s, e in dead)}px.")

    page_w, page_h = img.size
    n, col_page_h = plan_post_columns(page_h, page_w, canvas_w, canvas_h,
                                      max_columns, gap)
    starts = choose_post_starts(content_density_profile(np.asarray(img)),
                                n, col_page_h, page_h)

    # widths + gaps sum to exactly canvas_w, and the gaps are strictly between
    # columns, so nothing shows at the outer edges
    widths = post_column_widths(canvas_w, n, gap)

    canvas = Image.new("RGB", (canvas_w, canvas_h), gap_color)
    x = 0
    for i, cw in enumerate(widths):
        top = int(round(starts[i]))
        bottom = min(int(round(starts[i] + col_page_h)), page_h)
        col = img.crop((0, top, page_w, bottom)).resize((cw, canvas_h), Image.LANCZOS)
        canvas.paste(col, (x, 0))
        x += cw + gap

    canvas.save(out_path)
    sz = os.path.getsize(out_path)
    shown = n * col_page_h
    print(f"Saved: {out_path} ({canvas_w}x{canvas_h}, {sz / 1024:.0f}KB) — "
          f"{n} columns at {size}, {gap}px gaps, each column showing "
          f"{col_page_h:.0f}px of page ({shown / page_h:.0%} of the page, "
          f"scale {widths[0] / page_w:.2f}), canvas fully covered.")

    if max_bytes and sz > max_bytes:
        stem, _ = os.path.splitext(out_path)
        alt = f"{stem}-x.jpg"
        canvas.save(alt, "JPEG", quality=88, optimize=True, progressive=True)
        print(f"Also wrote {alt} ({os.path.getsize(alt) / 1024:.0f}KB).")
    return canvas.size


def build_strip(png_bytes, out_path, columns=6, pad=0, gap=0,
                bg=(255, 255, 255), excise=True, max_bytes=None):
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")

    if excise:
        profile = content_density_profile(np.asarray(img))
        img, dead = excise_dead_zones(img, profile)
        if dead:
            print(f"Excised {len(dead)} dead zone(s) totaling "
                  f"{sum(e - s for s, e in dead)}px.")

    arr = np.asarray(img)
    h, w = arr.shape[:2]
    cuts = choose_split_points(content_density_profile(arr), columns)

    bounds = [0] + cuts + [h]
    cols = [img.crop((0, bounds[i], w, bounds[i + 1])) for i in range(columns)]
    cols = [c for c in cols if c.height > 0]

    col_h = max(c.height for c in cols)
    canvas_w = len(cols) * w + (len(cols) - 1) * gap + 2 * pad
    canvas = Image.new("RGB", (canvas_w, col_h + 2 * pad), bg)
    for i, c in enumerate(cols):
        x = pad + i * (w + gap)
        # Snapping cuts to section seams means columns end at different
        # heights, which would otherwise leave a hard white rectangle under
        # every short column and make the strip read as unfinished. Extend
        # each short column with the average colour of its own bottom edge
        # so it reads as that column's background running on. Same
        # edge-sampling idea as status_bar_util's notch fill.
        if c.height < col_h:
            edge = np.asarray(c.crop((0, c.height - 8, w, c.height))).reshape(-1, 3)
            fill = tuple(int(v) for v in edge.mean(axis=0))
            canvas.paste(Image.new("RGB", (w, col_h - c.height), fill),
                         (x, pad + c.height))
        canvas.paste(c, (x, pad))

    canvas.save(out_path)
    size = os.path.getsize(out_path)
    print(f"Saved: {out_path} ({canvas.width}x{canvas.height}, "
          f"{size / 1024:.0f}KB) — {len(cols)} columns, "
          f"heights {[c.height for c in cols]}")

    # X caps uploads at 5MB and Make's fetch module has choked well below that
    # (the 2026-08-01 combined-showcase incident, see CLAUDE.md). Emit a
    # compressed sibling rather than overwriting the full-resolution asset.
    if max_bytes and size > max_bytes:
        stem, _ = os.path.splitext(out_path)
        alt = f"{stem}-x.jpg"
        scale = 1.0
        while scale > 0.3:
            small = canvas.resize((round(canvas.width * scale),
                                   round(canvas.height * scale)), Image.LANCZOS)
            small.save(alt, "JPEG", quality=88, optimize=True, progressive=True)
            if os.path.getsize(alt) <= max_bytes:
                break
            scale -= 0.12
        print(f"Also wrote {alt} ({os.path.getsize(alt) / 1024:.0f}KB) — "
              f"point X/Make rows at this one, not the full-resolution PNG.")
    return canvas.size


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("output")
    ap.add_argument("--file", action="store_true", help="target is a local path, not a URL")
    ap.add_argument("--clean", action="store_true", help="hide cookie/consent banners")
    ap.add_argument("--width", type=int, default=390, help="mobile viewport width")
    ap.add_argument("--mode", choices=["post", "contact-sheet"], default="post",
                    help="post: fixed standard post canvas, fully covered (default). "
                         "contact-sheet: the original ragged-bottom QA sheet.")
    ap.add_argument("--size", choices=sorted(POST_SIZES), default="portrait",
                    help="post canvas size (post mode only)")
    ap.add_argument("--max-columns", type=int, default=5,
                    help="ceiling on columns in post mode; the real count is the "
                         "largest that the page can fill")
    ap.add_argument("--columns", type=int, default=6,
                    help="exact column count (contact-sheet mode only)")
    ap.add_argument("--pad", type=int, default=0, help="outer margin (default flush)")
    ap.add_argument("--gap", type=int, default=None,
                    help=f"gap between columns. Post mode defaults to {POST_GAP}px "
                         f"(the separator Ridwan asked for, 2026-09-19); "
                         f"contact-sheet mode defaults to 0.")
    ap.add_argument("--gap-color", default="ffffff",
                    help="colour of the between-column gaps in post mode")
    ap.add_argument("--bg", default="ffffff")
    ap.add_argument("--no-excise", action="store_true",
                    help="keep blank runs instead of splicing them out")
    ap.add_argument("--max-bytes", type=int, default=4_000_000,
                    help="emit a compressed -x.jpg sibling above this size")
    a = ap.parse_args()

    target = os.path.abspath(a.target) if a.file else a.target
    hexcol = lambda s: tuple(int(s.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    png = capture(target, a.width, a.file, clean=a.clean)
    if a.mode == "post":
        build_post(png, a.output, size=a.size, max_columns=a.max_columns,
                   gap=POST_GAP if a.gap is None else a.gap,
                   gap_color=hexcol(a.gap_color),
                   excise=not a.no_excise, max_bytes=a.max_bytes)
    else:
        build_strip(png, a.output, columns=a.columns, pad=a.pad,
                    gap=0 if a.gap is None else a.gap,
                    bg=tuple(int(a.bg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)),
                    excise=not a.no_excise, max_bytes=a.max_bytes)
