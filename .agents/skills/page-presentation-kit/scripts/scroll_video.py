"""
scroll_video.py — record an eased, smooth scroll-through of a page as video.

Reuses the same Playwright/Chromium setup as screenshot.py (same ARM64 sandbox
workaround applies — see playwright-setup.md before first use).

Records a .webm via Playwright's native video capture, then (if ffmpeg is
available) converts to .mp4 and applies a couple of light polish passes
(fps normalize, optional fade in/out). Silent output — no audio track. If you
want narration/music, run text-to-speech / sound-effects separately and mux
the result onto this video afterward; this script deliberately stays a single
job (reliable scroll capture) rather than trying to own the whole audio chain.

Usage:
  python3 scroll_video.py "https://example.com" out.mp4
  python3 scroll_video.py "/path/to/page.html" out.mp4 --file
  python3 scroll_video.py "https://example.com" out.mp4 --width 1440 --height 900 --duration 8
  python3 scroll_video.py "https://example.com" out.mp4 --width 390 --height 844 --duration 6 --clean
"""

import sys
import os
import argparse
import shutil
import subprocess
import tempfile
from playwright.sync_api import sync_playwright

DISMISS_LABELS = [
    "Accept", "Accept All", "Accept all cookies", "I Agree", "I agree",
    "Got it", "OK", "Allow all", "Allow All", "Agree", "Close",
    "No thanks", "Dismiss", "Continue", "X",
]

HIDE_CSS = """
[class*="cookie" i], [id*="cookie" i],
[class*="consent" i], [id*="consent" i],
[class*="newsletter-popup" i], [class*="modal-overlay" i],
[class*="popup" i][class*="overlay" i] {
  display: none !important;
}
"""


def dismiss_popups(page):
    for label in DISMISS_LABELS:
        try:
            btn = page.get_by_role("button", name=label, exact=False).first
            if btn.is_visible(timeout=800):
                btn.click(timeout=800)
                page.wait_for_timeout(400)
                return True
        except Exception:
            continue
    return False


def record(target, output, width=390, height=844, is_file=False,
           duration=6.0, clean=False, fps=30):
    tmp_video_dir = tempfile.mkdtemp(prefix="ppk_video_")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=2,
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

        if clean:
            dismiss_popups(page)
            page.add_style_tag(content=HIDE_CSS)
            page.wait_for_timeout(300)

        # Total scrollable distance
        total_height = page.evaluate("document.body.scrollHeight") or height
        scroll_distance = max(total_height - height, 0)

        if scroll_distance <= 0:
            # Nothing to scroll (short page) — just hold on the hero for the
            # full duration so the output is still a usable clip.
            page.wait_for_timeout(int(duration * 1000))
        else:
            # Eased scroll: ease-in-out over `duration` seconds, driven from
            # inside the page so it's frame-accurate rather than relying on
            # our own sleep loop's timing.
            page.evaluate(
                """
                ([distance, ms]) => {
                  return new Promise(resolve => {
                    const start = performance.now();
                    function ease(t) { return t < 0.5 ? 2*t*t : 1 - Math.pow(-2*t+2, 2)/2; }
                    function step(now) {
                      const elapsed = now - start;
                      const t = Math.min(elapsed / ms, 1);
                      window.scrollTo(0, distance * ease(t));
                      if (t < 1) requestAnimationFrame(step);
                      else resolve();
                    }
                    requestAnimationFrame(step);
                  });
                }
                """,
                [scroll_distance, duration * 1000],
            )
            page.wait_for_timeout(400)  # settle on last frame before closing

        video_path = page.video.path() if page.video else None
        context.close()
        browser.close()

    if not video_path or not os.path.exists(video_path):
        print("Failed to capture video — no output from Playwright.")
        sys.exit(1)

    if shutil.which("ffmpeg"):
        # Normalize fps and encode to mp4 (H.264) for broad compatibility
        # (Playwright's raw output is .webm/VP8).
        cmd = [
            "ffmpeg", "-y", "-i", video_path,
            "-r", str(fps),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output,
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Saved (converted to mp4): {output}")
    else:
        # No ffmpeg available — hand back the raw webm instead of failing.
        fallback = output.rsplit(".", 1)[0] + ".webm"
        shutil.move(video_path, fallback)
        print(f"ffmpeg not found — saved raw capture instead: {fallback}")
        print("Install ffmpeg and rerun to get a proper .mp4.")

    shutil.rmtree(tmp_video_dir, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("output")
    ap.add_argument("--file", action="store_true", help="target is a local HTML file, not a URL")
    ap.add_argument("--clean", action="store_true", help="dismiss/hide cookie & popup overlays before capture")
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    ap.add_argument("--duration", type=float, default=6.0, help="seconds to spend scrolling top to bottom")
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()
    record(args.target, args.output, width=args.width, height=args.height,
           is_file=args.file, duration=args.duration, clean=args.clean, fps=args.fps)
