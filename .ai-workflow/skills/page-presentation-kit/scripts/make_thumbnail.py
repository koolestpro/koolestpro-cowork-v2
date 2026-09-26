#!/usr/bin/env python3
"""
make_thumbnail.py — V2 distribution pipeline, Step 3 (Template Showcase only).

Turn a finished device-mockup cover (the cover.png this project already
produces) into a scroll-stopping VIDEO THUMBNAIL in Ridwan's Instagram-grid
style: near-black background, brand orange->purple radial glow, the device
composition, a bold headline, small diamond accents, and a bottom tagline.

Headlines are ROTATED from a fixed template set (per the V2 plan) with the
brand/category slotted in — not freshly authored each run. Pass --headline to
override, or --brand/--category to fill a rotated template.

Compositing is mechanical (PIL). Brand/headline SELECTION is Claude's job in the
content-brief phase — this script just renders what it's told.

Sizes per platform (native video-thumbnail targets):
    linkedin / twitter -> 1280x720  (16:9)
    instagram          -> 1080x1350 (4:5, feed-safe portrait)
    instagram-reel     -> 1080x1920 (9:16)

Fonts: uses Syne if a path is given (--font) or found; otherwise falls back to
DejaVu Sans Bold (present in this sandbox). For production parity install Syne
and pass --font. Emoji render best with a color-emoji font installed; without
one, emoji in a headline may render as a box — keep emoji optional.

Usage:
    python3 make_thumbnail.py --cover COVER.png --out THUMB.png
        [--platform linkedin|twitter|instagram|instagram-reel]
        [--headline "Shopify Store Redesign that Converts"]
        [--brand KURA] [--category "Product Page"] [--tagline "@koolestpro"]
        [--font /path/to/Syne-Bold.ttf]
"""

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ── brand system ──
BG = (8, 8, 8)
ORANGE = (255, 149, 0)
PURPLE = (123, 47, 190)
PINK = (224, 64, 160)
WHITE = (255, 255, 255)
MUTED = (170, 170, 175)

SIZES = {
    "linkedin": (1280, 720),
    "twitter": (1280, 720),
    "instagram": (1080, 1350),
    "instagram-reel": (1080, 1920),
}

# Rotated headline templates — {brand}/{category} slotted in.
HEADLINE_TEMPLATES = [
    "{brand} Store Redesign that Converts",
    "5 {category} Fixes That Bring More Sales",
    "5 {category} Fixes That Build Trust",
    "How I Built {brand} From Nothing",
    "{brand}: A Full Brand Build, Start to Finish",
]

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/local/lib/python3.10/dist-packages/matplotlib/mpl-data/fonts/ttf/DejaVuSans-Bold.ttf",
]
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def load_font(path, size):
    for cand in ([path] if path else []) + FONT_CANDIDATES:
        if cand and os.path.exists(cand):
            try:
                return ImageFont.truetype(cand, size)
            except Exception:
                continue
    return ImageFont.load_default()


def radial_glow(size, center, color, radius, alpha=120):
    """A soft radial brand glow blob (matches the project's glow system)."""
    w, h = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = center
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
              fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(radius // 2))


def wrap_text(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        test = (cur + " " + wd).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def make(cover_path, out_path, platform, headline, tagline, font_path):
    W, H = SIZES.get(platform, SIZES["linkedin"])
    img = Image.new("RGB", (W, H), BG)

    # brand glows: orange top-left, purple bottom-right
    base = img.convert("RGBA")
    base.alpha_composite(radial_glow((W, H), (int(W * 0.18), int(H * 0.20)), ORANGE, int(W * 0.42), 90))
    base.alpha_composite(radial_glow((W, H), (int(W * 0.86), int(H * 0.82)), PURPLE, int(W * 0.46), 90))
    img = base.convert("RGB")
    draw = ImageDraw.Draw(img)

    # device cover, scaled to ~62% width, placed in the upper region
    if cover_path and os.path.exists(cover_path):
        cover = Image.open(cover_path).convert("RGBA")
        target_w = int(W * (0.72 if platform.startswith("instagram") else 0.60))
        scale = target_w / cover.width
        cover = cover.resize((target_w, int(cover.height * scale)), Image.LANCZOS)
        # cap height so it never collides with the headline band
        max_h = int(H * (0.52 if platform.startswith("instagram") else 0.60))
        if cover.height > max_h:
            s2 = max_h / cover.height
            cover = cover.resize((int(cover.width * s2), max_h), Image.LANCZOS)
        cx = (W - cover.width) // 2
        cy = int(H * (0.10 if platform.startswith("instagram") else 0.08))
        img.paste(cover, (cx, cy), cover)
        draw = ImageDraw.Draw(img)

    # headline band (bottom third)
    hl_font_size = int(W * (0.062 if platform.startswith("instagram") else 0.058))
    hl_font = load_font(font_path, hl_font_size)
    max_text_w = int(W * 0.86)
    lines = wrap_text(draw, headline, hl_font, max_text_w)
    line_h = int(hl_font_size * 1.16)
    block_h = line_h * len(lines)
    y0 = int(H * (0.70 if platform.startswith("instagram") else 0.66))

    # small diamond accents flanking the headline start
    def diamond(cx, cy, r, color):
        draw.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=color)

    acc_y = y0 - int(hl_font_size * 0.55)
    diamond(int(W * 0.09), acc_y, int(W * 0.010), ORANGE)
    diamond(int(W * 0.09) + int(W * 0.028), acc_y, int(W * 0.008), PINK)
    diamond(int(W * 0.09) + int(W * 0.052), acc_y, int(W * 0.006), PURPLE)

    y = y0
    for ln in lines:
        draw.text((int(W * 0.08), y), ln, font=hl_font, fill=WHITE)
        y += line_h

    # accent rule under the headline
    rule_y = y + int(hl_font_size * 0.20)
    draw.rectangle([int(W * 0.08), rule_y, int(W * 0.08) + int(W * 0.16), rule_y + max(3, int(H * 0.006))],
                   fill=ORANGE)

    # tagline (mono, muted) bottom-left
    tag_font = load_font(FONT_MONO, int(W * 0.024))
    draw.text((int(W * 0.08), int(H * 0.94)), tagline, font=tag_font, fill=MUTED)

    img.save(out_path, "PNG")
    return W, H, len(lines)


def main():
    ap = argparse.ArgumentParser(description="Composite a Template Showcase video thumbnail.")
    ap.add_argument("--cover", required=True, help="device-mockup cover.png to feature")
    ap.add_argument("--out", required=True)
    ap.add_argument("--platform", default="linkedin", choices=list(SIZES.keys()))
    ap.add_argument("--headline", default=None)
    ap.add_argument("--brand", default="")
    ap.add_argument("--category", default="Product Page")
    ap.add_argument("--template-index", type=int, default=0,
                    help="which HEADLINE_TEMPLATES entry to use when --headline not given")
    ap.add_argument("--tagline", default="@koolestpro")
    ap.add_argument("--font", default=None, help="path to Syne-Bold.ttf for brand parity")
    args = ap.parse_args()

    headline = args.headline
    if not headline:
        tmpl = HEADLINE_TEMPLATES[args.template_index % len(HEADLINE_TEMPLATES)]
        headline = tmpl.format(brand=args.brand or "This Brand", category=args.category)

    w, h, nlines = make(args.cover, args.out, args.platform, headline, args.tagline, args.font)
    print(f"[thumbnail] {args.platform} {w}x{h} | headline={headline!r} ({nlines} line(s))")
    print(f"[thumbnail] -> {args.out}")
    if not (args.font and os.path.exists(args.font)):
        print("[thumbnail] note: Syne not supplied — used DejaVu Sans Bold fallback. Pass --font Syne-Bold.ttf for brand parity.")


if __name__ == "__main__":
    main()
