#!/usr/bin/env python3
"""Email comparison images for the FleeMoto outreach hook (2026-11-01): live page vs concept redesign,
both 390 wide, labelled "Your page today" / "Concept redesign". First screen + full mobile page."""
import pathlib
from PIL import Image, ImageDraw, ImageFont
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs/cro-fixes/fleemoto/_assets"; P = ROOT / "outputs/cro-fixes/fleemoto_supermoto-wheels-pdp_presentation"
F = A / "fonts/inter-latin.woff2"
def font(sz):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        try: return ImageFont.truetype(f, sz)
        except Exception: pass
    return ImageFont.load_default()
def pair(a, b, out, maxh=None):
    L, R = [Image.open(p).convert("RGB") for p in (a, b)]
    L = L.resize((390, round(L.height * 390 / L.width))); R = R.resize((390, round(R.height * 390 / R.width)))
    h = max(L.height, R.height) if not maxh else maxh
    W = 390 * 2 + 60; c = Image.new("RGB", (W, h + 70), "#f3f3f3"); d = ImageDraw.Draw(c)
    c.paste(L, (20, 56)); c.paste(R, (430, 56))
    for x, t, col in ((20, "Your page today", "#555555"), (430, "Concept redesign", "#0d0d0d")):
        d.text((x, 18), t, fill=col, font=font(22))
    c.save(out, optimize=True); print(out, c.size)
pair(A / "before_raw.png", A / "after_raw.png", P / "fleemoto-compare.png")
pair(A / "before_full.png", A / "after_raw_full.png", P / "fleemoto-compare-full.png")
