"""
scroll_video_raw.py — same capture logic as scroll_video.py but stops after
Playwright's own .webm capture, WITHOUT the ffmpeg-to-mp4 conversion step.

Added 2026-07-31: on this sandbox, doing capture + convert in a single call
was hitting the ~44s hard bash-call ceiling right at the edge (26s scroll +
launch/settle overhead + ffmpeg encode), producing a truncated mp4 with a
missing moov atom. Splitting the two steps into separate calls (this script,
then a plain ffmpeg convert call) keeps each step comfortably inside budget.

FIXED 2026-07-31 (same day, after Ridwan reviewed the first halos_pdp-01 run):
the original version drove the scroll with a single in-page requestAnimationFrame
loop timed against performance.now() ("finish moving distance*ease(t) over
`duration` seconds, driven by the page's own rAF ticks"). On this sandbox that
self-timed loop is NOT robust — recording a video (especially a big desktop
viewport at device_scale_factor=2, i.e. 3200x1932 real pixels per frame) loads
the renderer's main thread heavily, and when that thread stalls, the in-page
rAF callback doesn't fire for a real stretch of wall-clock time. Confirmed by
extracting frames across the halos_pdp-01 laptop.mp4 timeline: identical hero
content was still on screen at both t=10s AND t=20s (a 10s dead stall), then a
completely different section appeared at t=29s with no visible transition —
a classic "stuck, then the rAF finally fires once and sees elapsed >> ms, so it
jumps t straight to 1" pattern. This is why the desktop/laptop capture was the
worst offender: it's the highest-pixel-count recording, so most likely to
starve its own paint/JS thread.

Fix: stop trusting the page's own animation frame timing entirely. Scroll is
now driven from OUTSIDE the page, in fixed discrete steps, each an explicit
`page.evaluate(scrollTo(...))` followed by our own `page.wait_for_timeout(...)`.
Playwright's wait_for_timeout blocks on the Python/CDP side, not on the page's
main thread being free to run a callback — so even if the renderer briefly
stalls on a heavy frame, our next step still lands at the right scroll
position once we resume, rather than depending on the page waking itself up.
Eased easing curve is now precomputed per-step in Python before the loop, not
recomputed by an in-page function.

Also switched device_scale_factor from 2 to 1 for video capture specifically
(not for the still-image capture scripts, where retina sharpness still
matters and there's no continuous animation to stall) — this roughly quarters
the pixel volume the renderer has to composite and encode per frame, which
directly reduces how likely a stall is in the first place. frame_video.py
already scales whatever resolution the raw clip is down to fit the bezel's
screen rect via an ffmpeg scale filter, so this has no visible quality cost in
the final framed video.

Usage:
  python3 scroll_video_raw.py "/path/to/page.html" out.webm --file \
      --width 1600 --height 966 --duration 26
  python3 scroll_video_raw.py "/path/to/page.html" out.webm --file \
      --width 1600 --height 966 --duration 26 --steps 45
"""

import argparse
import os
import shutil
import sys
import tempfile
from playwright.sync_api import sync_playwright


def ease(t):
    return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2


def record(target, output, width, height, is_file, duration, steps=48, end_hold_ms=900):
    tmp_video_dir = tempfile.mkdtemp(prefix="ppk_video_")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
            record_video_dir=tmp_video_dir,
            record_video_size={"width": width, "height": height},
        )
        page = context.new_page()

        if is_file:
            page.goto(f"file://{target}")
        else:
            try:
                page.goto(target, wait_until="networkidle", timeout=12000)
            except Exception:
                page.goto(target, wait_until="load", timeout=30000)
        page.wait_for_timeout(1200)

        total_height = page.evaluate("document.body.scrollHeight") or height
        scroll_distance = max(total_height - height, 0)

        if scroll_distance <= 0:
            page.wait_for_timeout(int(duration * 1000))
        else:
            # Reserve end_hold_ms at the end so the last frame genuinely
            # sits at the bottom for a beat, rather than the clip cutting
            # off the instant it arrives.
            scroll_ms = max(duration * 1000 - end_hold_ms, 1000)
            step_ms = scroll_ms / steps
            for i in range(steps + 1):
                t = i / steps
                y = scroll_distance * ease(t)
                page.evaluate(f"window.scrollTo(0, {y})")
                page.wait_for_timeout(step_ms)
            # Explicit final snap to the true bottom — guards against any
            # rounding short of the exact bottom pixel over the stepped loop.
            page.evaluate(f"window.scrollTo(0, {scroll_distance})")
            page.wait_for_timeout(end_hold_ms)

        video_path = page.video.path() if page.video else None
        context.close()
        browser.close()

    if not video_path or not os.path.exists(video_path):
        print("Failed to capture video — no output from Playwright.")
        sys.exit(1)

    shutil.move(video_path, output)
    shutil.rmtree(tmp_video_dir, ignore_errors=True)
    print(f"Saved raw webm: {output}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("output")
    ap.add_argument("--file", action="store_true")
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    ap.add_argument("--duration", type=float, default=6.0)
    ap.add_argument("--steps", type=int, default=48,
                     help="number of discrete scroll steps across the animation — more is "
                          "smoother but each step costs a small wait_for_timeout overhead")
    args = ap.parse_args()
    record(args.target, args.output, args.width, args.height, args.file, args.duration, args.steps)
