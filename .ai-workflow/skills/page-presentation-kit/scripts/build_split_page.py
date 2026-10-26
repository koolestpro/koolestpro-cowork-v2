"""
build_split_page.py — capture a page's ENTIRE scroll length at desktop
viewport width and lay it out as TWO side-by-side columns instead of a grid
mosaic.

REPLACES build_mosaic.py's grid-tiling output (2026-07-29, Ridwan's call —
"I do not want it"). The grid mosaic chopped the page into many small equal
tiles arranged 2-per-row, which fragmented sections and (per the 2026-07-13
fix) still needed dead-zone excision to avoid blank panels. Ridwan wants
something much simpler and closer to a real "read the whole page" reference:
the full page, split into exactly two tall columns placed side by side, each
column showing complete sections wherever possible, continuing top-to-bottom
from column 1 into column 2 (reference: a real 2-column export he shared
2026-07-29, where column 1 covers the page from the hero down through the
first several sections, and column 2 continues from there to the footer).

Keeps two things from build_mosaic.py that are still genuinely necessary,
they just aren't the part Ridwan objected to:
  1. Walk-the-page-first capture, so scroll-triggered reveal animations
     (GSAP / IntersectionObserver fades) have already fired before the
     full-page screenshot is taken — a naive one-shot full_page screenshot
     catches those sections still hidden/blank.
  2. Dead-zone excision — splice out sustained near-uniform vertical runs
     (the static-screenshot artifact of scroll-pinned/scrubbed sections)
     before splitting, same reasoning as before: a static image can't
     represent a section whose visual state is a function of live scroll
     position, so showing it as a long blank strip is worse than cutting it.

What's DIFFERENT from build_mosaic.py: exactly ONE split point (not many),
chosen near the vertical midpoint but snapped to the nearest low-content-
density gap (a real seam between sections) so neither column cuts a section
in half — this is what "not necessarily split into two 50%" means in
practice. The two columns are simply placed side by side, both read normally
top-to-bottom (col 1 finishes where col 2 picks up), not mirrored/flipped.

Usage:
  python3 build_split_page.py "/path/to/page.html" out.png --file --width 1440
  python3 build_split_page.py "https://example.com" out.png --width 1440
"""

import argparse
import io
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright


def _wire_vendor(page, vendor_dir):
    """Serve JS libraries and web fonts from local files instead of their CDNs.

    Added 2026-08-28 after a capture silently lost content: cdnjs hung inside
    Chromium (while still reachable by curl), GSAP never loaded, the page's
    motion layer bailed out, and the animated stat counters rendered as
    "0 0 0 0" in the finished asset. Nothing errored — the capture just quietly
    published a page that looked broken. Point this at a directory holding
    gsap.min.js / ScrollTrigger.min.js / lenis.min.js and a fonts.css of
    data-URI @font-face rules to make a capture deterministic.
    """
    import os

    def route(r, req):
        name = req.url.split("?")[0].split("/")[-1]
        local = os.path.join(vendor_dir, name)
        if os.path.exists(local):
            ctype = "text/css" if name.endswith(".css") else "application/javascript"
            r.fulfill(status=200, content_type=ctype, body=open(local, "rb").read())
        elif "fonts.googleapis.com" in req.url:
            fc = os.path.join(vendor_dir, "fonts.css")
            r.fulfill(status=200, content_type="text/css",
                      body=open(fc, "rb").read() if os.path.exists(fc) else b"")
        elif "fonts.gstatic.com" in req.url:
            r.fulfill(status=200, content_type="text/css", body=b"")
        else:
            r.continue_()

    for pat in ("**/gsap.min.js", "**/ScrollTrigger.min.js", "**/lenis.min.js",
                "**fonts.googleapis.com**", "**fonts.gstatic.com**"):
        page.route(pat, route)


def capture_full_page(target, width, is_file, clean=False, step_frac=0.85, settle_ms=550,
                       vendor_dir=None):
    with sync_playwright() as p:
        # A full-page screenshot of a long page is one very large bitmap, and
        # Chromium stages it through /dev/shm. This sandbox gives /dev/shm only
        # 512MB, which crashed the renderer outright on a 10,000px page
        # (2026-08-28, Meridian). --disable-dev-shm-usage moves that staging to
        # /tmp and fixes it.
        browser = p.chromium.launch(args=["--disable-dev-shm-usage"])
        context = browser.new_context(viewport={"width": width, "height": 1000}, device_scale_factor=1)
        page = context.new_page()
        if vendor_dir:
            _wire_vendor(page, vendor_dir)

        # A page's third-party assets must not be able to hang the capture.
        # `page.goto()` defaults to wait_until="load", and a Google Fonts
        # stylesheet that never resolves (seen live 2026-08-28 — reachable by
        # curl, hung inside Chromium) blocks that event forever. Every path
        # here degrades to "domcontentloaded" plus a settle wait instead of
        # raising, then a longer settle covers whatever was still in flight.
        url = f"file://{target}" if is_file else target
        try:
            page.goto(url, wait_until="networkidle", timeout=12000)
        except Exception:
            try:
                page.goto(url, wait_until="load", timeout=15000)
            except Exception:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(2400)

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

        total_height = page.evaluate("document.body.scrollHeight") or total_height
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(400)

        # Prepare the page for a *document* capture rather than a viewport one.
        #
        # 1. Kill ScrollTriggers, preserving current state. `full_page=True`
        #    resizes the viewport to the whole document, which fires
        #    ScrollTrigger's resize handler and can revert tweens that already
        #    finished during the walk above. Seen live 2026-08-28: animated
        #    stat counters that had counted up correctly rendered as "0 0 0 0"
        #    in the final image, making the captured site look broken.
        #
        # 2. Hide everything `position: fixed`. Fixed elements are viewport
        #    chrome, not document content — floating buttons, cart drawers
        #    parked off-canvas, toasts, watermarks, transition curtains. The
        #    2026-07-31 fix turned these static, which dropped them into the
        #    flow: an off-canvas cart drawer and a floating WhatsApp button
        #    both appeared mid-document in the 2026-08-28 Lumora capture.
        #
        # 3. Turn `position: sticky` static. Sticky elements *are* document
        #    content and would otherwise be painted on every stitched tile,
        #    which is the original 2026-07-31 duplicated-header bug.
        page.evaluate("""
            if (window.ScrollTrigger && ScrollTrigger.getAll) {
                ScrollTrigger.getAll().forEach(t => { try { t.kill(false); } catch (e) {} });
            }
            document.querySelectorAll('*').forEach(el => {
                const pos = getComputedStyle(el).position;
                if (pos === 'fixed') {
                    el.style.setProperty('display', 'none', 'important');
                } else if (pos === 'sticky') {
                    el.style.setProperty('position', 'static', 'important');
                }
            });
            // Defensive: anything the reveal system left invisible would read
            // as a blank band in the capture.
            document.querySelectorAll('[data-reveal],[data-split]').forEach(el => {
                el.style.setProperty('opacity', '1', 'important');
                el.style.setProperty('transform', 'none', 'important');
            });
            // Counters animate from 0 via ScrollTrigger. If the motion library
            // never loaded, or its trigger never fired, they sit at "0" and the
            // captured page looks broken. The final value is declared on the
            // element, so fill it in directly rather than depending on whether
            // an animation got to run.
            document.querySelectorAll('[data-count]').forEach(el => {
                const v = el.getAttribute('data-count');
                const suffix = el.getAttribute('data-suffix') || '';
                if (v !== null) el.textContent = Math.round(parseFloat(v)) + suffix;
            });
        """)
        page.wait_for_timeout(350)

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


def ink_rows(img_arr, delta=38, min_px=3, spread=10):
    """Rows that carry ANY real ink (text, icons), however small.

    FIXED 2026-10-17 (moult_hp-01 run, Tier 1 QA): the std-dev profile alone
    let a thin 11px eyebrow label ("ONE BRUSH. EVERY COAT.") read as dead
    space, so excision sliced it in half. A row counts as inked when at least
    `min_px` pixels differ from that row's median by more than `delta`, and
    the flag is spread +/- `spread` rows so letter gaps don't break it up."""
    gray = img_arr.mean(axis=2)
    med = np.median(gray, axis=1, keepdims=True)
    ink = (np.abs(gray - med) > delta).sum(axis=1) >= min_px
    if spread:
        k = np.ones(2 * spread + 1)
        ink = np.convolve(ink.astype(float), k, mode="same") > 0
    return ink


def excise_dead_zones(img, profile, min_run=140, density_ratio=0.22, pad=24):
    """Splice out sustained near-uniform vertical runs before splitting at
    all — see module docstring. Same logic as build_mosaic.py."""
    page_avg = profile.mean()
    threshold = page_avg * density_ratio
    below = (profile < threshold) & ~ink_rows(np.asarray(img))

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


def _section_seam(img_arr, lo, hi, target, window, band=24, min_diff=28.0,
                  max_imbalance=0.22):
    """Row index where the page background switches colour (a section
    boundary), nearest the midpoint and within `max_imbalance` of it. Both
    sides of the seam must be ink-free for `band` rows so the cut never
    touches text."""
    ink = ink_rows(img_arr, spread=0)
    gray = img_arr.mean(axis=2)
    edge_mean = np.concatenate([gray[:, :40], gray[:, -40:]], axis=1).mean(axis=1)
    h = len(edge_mean)
    best = None
    for y in range(max(lo, band), min(hi, h - band)):
        a = edge_mean[y - band:y].mean()
        b = edge_mean[y:y + band].mean()
        if abs(a - b) < min_diff:
            continue
        if abs(edge_mean[y - 1] - edge_mean[y]) < min_diff * 0.6:
            continue
        if ink[y - 6:y + 6].any():
            continue
        if abs(y - target) > max_imbalance * h:
            continue
        if best is None or abs(y - target) < abs(best - target):
            best = y
    return best


def choose_split_point(profile, search_frac=0.32, gap_ratio=0.40, proximity_weight=0.5,
                       min_gap_run=40, img_arr=None):
    """Find ONE cut point near the vertical midpoint, snapped to a real
    section gap (a run of low content density = whitespace/background
    between sections) rather than a rigid half point — this is what "not
    necessarily split into two 50%" means in practice.

    First pass: look for actual low-density RUNS (not just a single-row
    minimum, which can land right at the noisy edge of a run and produce a
    wildly uneven split) within the search window, and pick whichever run's
    CENTER sits closest to the true midpoint. This keeps the two columns
    reasonably balanced in height while still snapping to a genuine seam
    instead of cutting through content.

    Fallback (no clear gap found): a distance-penalized minimum — low
    density is good, but weighted against how far it sits from center, so
    an extreme low point way out at the edge of the window can't win purely
    on density alone."""
    h = len(profile)
    target = h // 2
    window = int(h * search_frac)
    lo, hi = max(target - window, 1), min(target + window, h - 1)

    # ADDED 2026-10-17 (moult_hp-01 run): prefer a real SECTION SEAM, a row
    # where the background colour changes between two sections, over a gap
    # inside a section. The old run-centre logic cut the MOULT homepage just
    # under a section heading, orphaning "Made for the Pets You Actually
    # Have." at the foot of column 1 while its cards opened column 2.
    if img_arr is not None:
        # ADDED 2026-10-24 (moult_pdp-01 run): the strict pass alone cut the
        # MOULT PDP at 67% (col1 5151px vs col2 2545px) because only the one
        # dark section change cleared min_diff=28; the cream/beige seams near
        # the middle are subtler. Try balanced seams first (strict, then
        # subtle), and only accept a lopsided strict seam as a last resort.
        for md, imb in ((28.0, 0.10), (7.0, 0.10), (28.0, 0.22)):
            seam = _section_seam(img_arr, lo, hi, target, window, min_diff=md,
                                 max_imbalance=imb)
            if seam is not None:
                return seam

    page_avg = profile.mean()
    threshold = page_avg * gap_ratio
    below = profile < threshold

    runs = []
    start = None
    for i in range(lo, hi):
        if below[i] and start is None:
            start = i
        elif not below[i] and start is not None:
            runs.append((start, i))
            start = None
    if start is not None:
        runs.append((start, hi))

    # FIXED 2026-08-23 (halos_lp-01 run, Tier 1 QA): a run of ANY length used
    # to qualify as a "section gap", so a 1-2px band of near-uniform pixels
    # INSIDE a section (e.g. the flat background strip running between two
    # lines of text in a card grid) could win purely by sitting closest to
    # the midpoint — which is exactly how that run's first cut landed
    # mid-way through a 3-across feature-card row. A genuine seam between
    # sections is a *sustained* band of whitespace, so require one.
    runs = [r for r in runs if r[1] - r[0] >= min_gap_run]

    if runs:
        best_run = min(runs, key=lambda r: abs((r[0] + r[1]) // 2 - target))
        return (best_run[0] + best_run[1]) // 2

    local = profile[lo:hi]
    norm = local / (local.max() + 1e-6)
    idxs = np.arange(lo, hi)
    dist_penalty = np.abs(idxs - target) / max(window, 1)
    score = norm + proximity_weight * dist_penalty
    best = lo + int(np.argmin(score))
    return best


def build_split_page(png_bytes, out_path, width, pad=110, gap=48, bg=(238, 238, 240)):
    # FIXED 2026-07-31: Ridwan reviewed the first halos_pdp-01 run and expected
    # visible whitespace framing left/right of the two columns — the old
    # pad=28 (about 2% of a 1440px-wide column) read as edge-to-edge with
    # near-zero margin once the column's own near-white page background sat
    # right up against a similarly light canvas bg. pad is now ~4x larger and
    # the inter-column gap is wider too, so the two-column composition reads
    # as a deliberately framed image, not a raw crop.
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
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

    cut = choose_split_point(profile, img_arr=arr)
    col1 = img.crop((0, 0, w, cut))
    col2 = img.crop((0, cut, w, h))

    col_h = max(col1.height, col2.height)
    canvas_w = 2 * width + gap + 2 * pad
    canvas_h = col_h + 2 * pad

    canvas = Image.new("RGB", (canvas_w, canvas_h), bg)
    canvas.paste(col1, (pad, pad))
    canvas.paste(col2, (pad + width + gap, pad))

    canvas.save(out_path)
    print(f"Saved: {out_path} ({canvas_w}x{canvas_h}) — "
          f"col1 {col1.height}px, col2 {col2.height}px, split at y={cut} of {h}")
    return col1.height, col2.height


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("output")
    ap.add_argument("--file", action="store_true")
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--vendor-dir", help="serve gsap/lenis/fonts from here instead of their CDNs, so a CDN stall cannot silently strip motion from the capture")
    args = ap.parse_args()

    png_bytes = capture_full_page(args.target, args.width, args.file, args.clean,
                                  vendor_dir=args.vendor_dir)
    build_split_page(png_bytes, args.output, width=args.width)
