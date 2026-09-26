"""
composite_frame.py — build a device-frame mockup from a real screenshot using
pure HTML/CSS, rendered out via Playwright. No AI image generation involved,
so the real screenshot inside the frame is always pixel-accurate.

Covers 4 of the 5 styles in references/mockup-style-patterns.md:
  - flat-browser-frame
  - angled-3d-perspective  (CSS 3D transform, not a photo)
  - multi-device-collage   (desktop + mobile frames arranged together)
  - dark-portfolio-shot    (single frame, dark background, soft glow)

The 5th style, device-in-hand-lifestyle, needs a real/AI-generated photo
background and isn't a good fit for pure CSS — see perspective_composite.py
and the "Photoreal styles" section of mockup-style-patterns.md for that one.

Usage:
  python3 composite_frame.py flat-browser-frame --screenshot desktop.png --output out.png --width 1400
  python3 composite_frame.py angled-3d-perspective --screenshot mobile.png --output out.png --device mobile
  python3 composite_frame.py multi-device-collage --screenshot desktop.png --screenshot2 mobile.png --output out.png
  python3 composite_frame.py dark-portfolio-shot --screenshot desktop.png --output out.png --accent "#FF9500"
"""

import argparse
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright


def _img_data_uri(path):
    data = Path(path).read_bytes()
    ext = Path(path).suffix.lstrip(".").lower()
    mime = "image/png" if ext == "png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def build_html(style, screenshot, screenshot2=None, device="desktop", accent="#FF9500"):
    img = _img_data_uri(screenshot)
    img2 = _img_data_uri(screenshot2) if screenshot2 else None

    if style == "flat-browser-frame":
        chrome = "" if device == "mobile" else """
          <div class="browser-bar">
            <div class="dots"><span></span><span></span><span></span></div>
            <div class="addr"></div>
          </div>
        """
        radius = "28px" if device == "mobile" else "12px"
        return f"""
        <html><head><style>
          body {{ margin:0; background:#eef0f3; display:flex; align-items:center; justify-content:center; height:100vh; }}
          .frame {{ border-radius:{radius}; overflow:hidden; box-shadow:0 30px 80px rgba(0,0,0,0.25); background:#fff; }}
          .browser-bar {{ height:34px; background:#e7e7ea; display:flex; align-items:center; padding:0 12px; gap:10px; }}
          .dots span {{ display:inline-block; width:10px; height:10px; border-radius:50%; background:#c9c9cf; margin-right:6px; }}
          .addr {{ flex:1; height:18px; background:#fff; border-radius:6px; margin-left:8px; }}
          img {{ display:block; width:100%; }}
        </style></head><body>
          <div class="frame">{chrome}<img src="{img}"></div>
        </body></html>
        """

    if style == "angled-3d-perspective":
        return f"""
        <html><head><style>
          body {{ margin:0; background:radial-gradient(circle at 30% 20%, #2a2a35, #0d0d12); display:flex; align-items:center; justify-content:center; height:100vh; }}
          .stage {{ perspective:1800px; }}
          .frame {{ border-radius:14px; overflow:hidden; box-shadow:0 60px 120px rgba(0,0,0,0.55);
                     transform: rotateY(-18deg) rotateX(4deg) rotate(-1deg); background:#fff; }}
          img {{ display:block; width:900px; }}
        </style></head><body>
          <div class="stage"><div class="frame"><img src="{img}"></div></div>
        </body></html>
        """

    if style == "multi-device-collage":
        img2_html = f'<img src="{img2}">' if img2 else ""
        return f"""
        <html><head><style>
          body {{ margin:0; background:#f4f5f7; display:flex; align-items:flex-end; justify-content:center;
                   height:100vh; gap:-60px; }}
          .desktop {{ border-radius:10px; overflow:hidden; box-shadow:0 30px 70px rgba(0,0,0,0.2); width:900px; z-index:1; }}
          .mobile {{ border-radius:26px; overflow:hidden; box-shadow:0 30px 70px rgba(0,0,0,0.28); width:260px;
                      margin-left:-90px; margin-bottom:-30px; z-index:2; border:6px solid #111; }}
          img {{ display:block; width:100%; }}
        </style></head><body>
          <div class="desktop"><img src="{img}"></div>
          <div class="mobile">{img2_html}</div>
        </body></html>
        """

    if style == "dark-portfolio-shot":
        radius = "26px" if device == "mobile" else "14px"
        return f"""
        <html><head><style>
          body {{ margin:0; background:#0a0a0d; display:flex; align-items:center; justify-content:center; height:100vh; position:relative; }}
          .glow {{ position:absolute; width:600px; height:600px; background:radial-gradient(circle, {accent}33, transparent 70%);
                    filter:blur(40px); }}
          .frame {{ position:relative; border-radius:{radius}; overflow:hidden; box-shadow:0 40px 100px rgba(0,0,0,0.6); background:#111; }}
          img {{ display:block; width:900px; }}
        </style></head><body>
          <div class="glow"></div>
          <div class="frame"><img src="{img}"></div>
        </body></html>
        """

    raise ValueError(f"Unknown CSS-buildable style: {style}. device-in-hand-lifestyle needs perspective_composite.py instead.")


def render(html, output, width=1600, height=1200):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
        page.set_content(html)
        page.wait_for_timeout(300)
        page.screenshot(path=output)
        browser.close()
    print(f"Saved: {output}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("style", choices=[
        "flat-browser-frame", "angled-3d-perspective", "multi-device-collage", "dark-portfolio-shot",
    ])
    ap.add_argument("--screenshot", required=True, help="primary screenshot (desktop, or mobile if --device mobile)")
    ap.add_argument("--screenshot2", help="second screenshot, only used by multi-device-collage (the mobile shot)")
    ap.add_argument("--output", required=True)
    ap.add_argument("--device", default="desktop", choices=["desktop", "mobile"])
    ap.add_argument("--accent", default="#FF9500", help="glow/accent color, used by dark-portfolio-shot")
    ap.add_argument("--canvas-width", type=int, default=1600)
    ap.add_argument("--canvas-height", type=int, default=1200)
    args = ap.parse_args()

    html = build_html(args.style, args.screenshot, args.screenshot2, args.device, args.accent)
    render(html, args.output, args.canvas_width, args.canvas_height)
