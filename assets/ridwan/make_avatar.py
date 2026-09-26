"""
Koolestpro — Avatar Generator
Creates circular brand avatars from raw photos.
Usage: python3 make_avatar.py photo-main.jpg
Output: avatar-circle.jpg (1080×1080, circular crop, orange→purple gradient border)
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFilter
import math

def make_circular_avatar(input_path: str, output_path: str, size: int = 1080, border: int = 24):
    """
    Crop photo to circle, add brand gradient border, save on black background.
    Brand gradient: #FF9500 (orange) → #E040A0 (pink) → #7B2FBE (purple)
    """
    img = Image.open(input_path).convert("RGBA")

    # Square-crop centered on face (top-biased: focus on upper 60% of image)
    w, h = img.size
    sq = min(w, h)
    left = (w - sq) // 2
    top = max(0, int(h * 0.08))          # shift up slightly to capture face
    top = min(top, h - sq)
    img = img.crop((left, top, left + sq, top + sq))
    img = img.resize((size, size), Image.LANCZOS)

    # Create circular mask (inner photo area, inset by border width)
    inner = size - border * 2
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([border, border, border + inner - 1, border + inner - 1], fill=255)

    # Black background
    result = Image.new("RGBA", (size, size), (0, 0, 0, 255))

    # Paste photo with circular mask
    result.paste(img, (0, 0), mask)

    # Draw gradient border ring
    border_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(border_img)

    # Brand colours
    c1 = (255, 149, 0)    # #FF9500 orange
    c2 = (224, 64, 160)   # #E040A0 pink
    c3 = (123, 47, 190)   # #7B2FBE purple

    cx = cy = size / 2
    r_outer = size / 2
    r_inner = r_outer - border

    STEPS = 720
    for i in range(STEPS):
        angle = (i / STEPS) * 2 * math.pi - math.pi / 2   # start at top

        # Map angle to gradient position (0 → 1)
        t = (angle + math.pi / 2) / (2 * math.pi) % 1.0

        # Lerp through 3 stops: 0 = orange, 0.5 = pink, 1.0 = purple
        if t < 0.5:
            s = t * 2
            r = int(c1[0] + s * (c2[0] - c1[0]))
            g = int(c1[1] + s * (c2[1] - c1[1]))
            b = int(c1[2] + s * (c2[2] - c1[2]))
        else:
            s = (t - 0.5) * 2
            r = int(c2[0] + s * (c3[0] - c2[0]))
            g = int(c2[1] + s * (c3[1] - c2[1]))
            b = int(c2[2] + s * (c3[2] - c2[2]))

        color = (r, g, b, 255)

        # Draw a short arc segment as a line
        x1 = cx + r_outer * math.cos(angle)
        y1 = cy + r_outer * math.sin(angle)
        x2 = cx + r_inner * math.cos(angle)
        y2 = cy + r_inner * math.sin(angle)
        bdraw.line([(x1, y1), (x2, y2)], fill=color, width=2)

    # Slight anti-alias blur on the border only
    border_img = border_img.filter(ImageFilter.GaussianBlur(radius=0.8))
    result = Image.alpha_composite(result, border_img)

    # Save as JPEG on black bg
    final = Image.new("RGB", (size, size), (0, 0, 0))
    final.paste(result, mask=result.split()[3])
    final.save(output_path, "JPEG", quality=95)
    print(f"✅ Saved: {output_path} ({size}×{size}px)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 make_avatar.py <input_photo.jpg> [output_name.jpg]")
        print("Example: python3 make_avatar.py photo-main.jpg avatar-circle.jpg")
        sys.exit(1)

    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "avatar-circle.jpg"

    if not out.endswith(".jpg"):
        out += ".jpg"

    make_circular_avatar(inp, out)
