"""
scroll_video_frames.py: frame-by-frame scroll capture. The DEFAULT video
capturer for Template Showcase runs since 2026-10-10.

WHY (Ridwan, 2026-10-10, on halos_li-02 laptop.mp4): "the laptop of this
website build is not smooth and it didn't scroll naturally". Root cause, found
in scroll_video_raw.py: it records the browser live while jumping the page in
48 discrete scrollTo() steps. On a 6,000px+ desktop page that is a ~125px jump
every ~0.5s, which reads as a stutter, not a scroll. Raising the step count
does not fix it, because live recording also drops frames under load.

HOW THIS ONE WORKS: it never records live. It walks the page once (so lazy
images and reveal animations have fired), then for every output frame it sets
an exact scroll position and takes a screenshot, and finally encodes the
frames at a fixed frame rate with ffmpeg. Every frame is a deliberate,
evenly-spaced position, so motion is smooth by construction and immune to
renderer stalls. It also has no blank lead-in: frame 1 is the rendered hero
and the page is already moving (Ridwan's second note: videos must start
immediately, not on an empty device screen).

Easing is mostly linear with soft ends (no long slow ramp at the start).

Usage:
  python3 scroll_video_frames.py "/abs/page.html" raw_desktop.mp4 --file \
      --width 1600 --height 966 --duration 24 --fps 30
  python3 scroll_video_frames.py "/abs/page.html" raw_mobile.mp4 --file \
      --width 390 --height 855 --duration 24 --fps 30

The output is a raw clip; frame it with frame_video.py exactly like before.
Budget: roughly 40-80ms per frame. If a single call would exceed the ~178s
sandbox ceiling, use --chunk/--chunks to capture in parts, then the last call
(with --encode-only) stitches them.
"""

import argparse
import glob
import os
import subprocess
import sys
import tempfile

from playwright.sync_api import sync_playwright


def ease(t, soft=0.12):
    """Linear in the middle, short smooth ramps at each end (soft = fraction
    of the timeline spent ramping on each side)."""
    if t <= 0:
        return 0.0
    if t >= 1:
        return 1.0
    # constant-velocity profile with quadratic ramps; total area normalised to 1
    v = 1.0 / (1.0 - soft)
    if t < soft:
        return v * t * t / (2 * soft)
    if t > 1 - soft:
        r = 1 - t
        return 1 - v * r * r / (2 * soft)
    return v * (t - soft / 2)


def capture(target, frames_dir, width, height, is_file, duration, fps,
            chunk=0, chunks=1, end_hold=0.8):
    total = int(round(duration * fps))
    hold = int(round(end_hold * fps))
    moving = max(total - hold, 2)
    lo = total * chunk // chunks
    hi = total * (chunk + 1) // chunks
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-dev-shm-usage"])
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        page.goto(f"file://{target}" if is_file else target, wait_until="load")
        page.wait_for_timeout(1200)
        # walk once so lazy images + one-shot reveal animations are already fired
        h = page.evaluate("document.documentElement.scrollHeight")
        y = 0
        while y < h:
            page.evaluate(f"window.scrollTo(0,{y})")
            page.wait_for_timeout(180)
            y += int(height * 0.8)
        page.evaluate("document.documentElement.style.scrollBehavior='auto'")
        page.add_style_tag(content="*{scroll-behavior:auto!important}")
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(900)
        dist = max(page.evaluate("document.documentElement.scrollHeight") - height, 0)
        for i in range(lo, hi):
            t = min(i / (moving - 1), 1.0)
            page.evaluate(f"window.scrollTo(0,{round(dist * ease(t))})")
            page.wait_for_timeout(16)
            page.screenshot(path=os.path.join(frames_dir, f"f{i:05d}.jpg"), type="jpeg", quality=92)
        browser.close()
    return total, dist


def encode(frames_dir, output, fps):
    n = len(glob.glob(os.path.join(frames_dir, "f*.jpg")))
    cmd = ["ffmpeg", "-y", "-v", "error", "-framerate", str(fps),
           "-i", os.path.join(frames_dir, "f%05d.jpg"),
           "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", output]
    subprocess.run(cmd, check=True)
    print(f"Saved raw clip: {output} ({n} frames @ {fps}fps = {n / fps:.1f}s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("output")
    ap.add_argument("--file", action="store_true")
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    ap.add_argument("--duration", type=float, default=24.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--frames-dir", help="keep frames here (needed for chunked runs)")
    ap.add_argument("--chunk", type=int, default=0)
    ap.add_argument("--chunks", type=int, default=1)
    ap.add_argument("--encode-only", action="store_true")
    a = ap.parse_args()
    fd = a.frames_dir or tempfile.mkdtemp(prefix="svf_")
    os.makedirs(fd, exist_ok=True)
    if not a.encode_only:
        total, dist = capture(a.target, fd, a.width, a.height, a.file, a.duration, a.fps, a.chunk, a.chunks)
        print(f"chunk {a.chunk + 1}/{a.chunks} captured ({total} frames total, scroll distance {dist}px)")
    if a.encode_only or a.chunks == 1:
        encode(fd, a.output, a.fps)
