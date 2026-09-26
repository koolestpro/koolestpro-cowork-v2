#!/usr/bin/env python3
"""
build_tapro_graphics.py — builds ba-graphic.png and anno-graphic.png for the
TAPro Cards CRO Fix post, fully pre-rendered via PIL (no html2canvas, no live
SVG, no canvas-tainting risk). The finished PNGs get embedded as flat base64
<img> tags inside id="ba-graphic"/"anno-graphic" divs in the content.html, so
captureFixed() still works (html2canvas on a div containing one <img> is
trivially safe) while sidestepping every documented html2canvas/SVG bug.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_DIR = "/tmp/fonts"
SYNE = f"{FONT_DIR}/Syne.ttf"
DMMONO_R = f"{FONT_DIR}/DMMono-Regular.ttf"
DMMONO_M = f"{FONT_DIR}/DMMono-Medium.ttf"
CAVEAT = f"{FONT_DIR}/Caveat.ttf"

OUT_DIR = "/sessions/trusting-admiring-bardeen/mnt/koolestpro-cowork-v2/outputs/cro-fixes/tapro"
BEFORE_RAW = f"{OUT_DIR}/tapro_before_raw.png"
AFTER_RAW = f"{OUT_DIR}/tapro_after_raw.png"

CROP_H = 1716  # raw px — updated 2026-09-01 for the above-the-fold rebuild layout
DISPLAY_W = 390
DISPLAY_H = 858  # 1716 * 0.5


def syne(size, weight=800):
    f = ImageFont.truetype(SYNE, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def load_cropped(path):
    im = Image.open(path).convert("RGB")
    im = im.crop((0, 0, im.width, min(CROP_H, im.height)))
    im = im.resize((DISPLAY_W, int(im.height * DISPLAY_W / im.width)), Image.LANCZOS)
    return im


def glow(size, color, blur):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((0, 0, size[0], size[1]), fill=color)
    return layer.filter(ImageFilter.GaussianBlur(blur))


def rounded_rect(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


def center_text(draw, xy_center, text, font, fill, max_width=None):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = xy_center[0] - w / 2 - bbox[0]
    y = xy_center[1] - h / 2 - bbox[1]
    draw.text((x, y), text, font=font, fill=fill)
    return w, h


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] > max_width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


# ══════════════════════════════════════════════════════════════
# BA-GRAPHIC — before/after, dark, 1080x1080, pins on AFTER only
# ══════════════════════════════════════════════════════════════
def build_ba_graphic():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), (10, 10, 10))

    # glow blobs
    g1 = glow((420, 420), (255, 149, 0, 90), 60)
    canvas.paste(Image.alpha_composite(Image.new("RGBA", g1.size, (10, 10, 10, 255)), g1).convert("RGB"), (-160, -160))
    g2 = glow((420, 420), (123, 47, 190, 90), 60)
    canvas.paste(Image.alpha_composite(Image.new("RGBA", g2.size, (10, 10, 10, 255)), g2).convert("RGB"), (W - 260, -160))

    d = ImageDraw.Draw(canvas)

    # headline
    head_font = syne(46, 800)
    sub_font = ImageFont.truetype(DMMONO_R, 16)
    center_text(d, (W / 2, 62), "PRICE. PROOF. ONE CTA.", head_font, (255, 255, 255))
    center_text(d, (W / 2, 112), "NOW ABOVE THE FOLD.", head_font, (255, 255, 255))
    center_text(d, (W / 2, 160), "TAPRO CARDS: HOMEPAGE FIRST SCREEN, BEFORE VS. AFTER", sub_font, (255, 255, 255, 140))

    label_font = syne(17, 800)
    IMG_TOP = 214
    before_x = 50
    after_x = 570

    before_im = load_cropped(BEFORE_RAW)
    after_im = load_cropped(AFTER_RAW)

    center_text(d, (before_x + DISPLAY_W / 2, 196), "BEFORE", label_font, (255, 255, 255))
    center_text(d, (after_x + DISPLAY_W / 2, 196), "AFTER", label_font, (255, 149, 0))

    # rounded-corner paste via mask, with a backing card + soft shadow so the
    # phone reads as a distinct panel instead of blending into the black
    # canvas (the after-panel especially, since its own UI is near-black too)
    def paste_with_backing(im, pos, radius=14):
        pad = 14
        card_box = (pos[0] - pad, pos[1] - pad, pos[0] + im.width + pad, pos[1] + im.height + pad)

        # soft drop shadow behind the card
        shadow = Image.new("RGBA", (card_box[2] - card_box[0] + 60, card_box[3] - card_box[1] + 60), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle((30, 34, shadow.width - 30, shadow.height - 26), radius=radius + pad, fill=(0, 0, 0, 160))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18))
        canvas.paste(Image.alpha_composite(Image.new("RGBA", shadow.size, (10, 10, 10, 255)).crop((0, 0, shadow.width, shadow.height)), shadow).convert("RGB"),
                     (card_box[0] - 30, card_box[1] - 30))

        # lighter backing card + thin border so the panel separates from the pure-black canvas
        card = Image.new("RGBA", (card_box[2] - card_box[0], card_box[3] - card_box[1]), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, card.width - 1, card.height - 1), radius=radius + pad, fill=(26, 26, 26, 255), outline=(255, 255, 255, 46), width=2)
        canvas.paste(card, (card_box[0], card_box[1]), card)

        mask = Image.new("L", im.size, 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle((0, 0, im.width, im.height), radius=radius, fill=255)
        canvas.paste(im, pos, mask)

    paste_with_backing(before_im, (before_x, IMG_TOP))
    paste_with_backing(after_im, (after_x, IMG_TOP))

    # pins on AFTER image, split both sides
    def raw_to_canvas_y(raw_y):
        return IMG_TOP + raw_y * (DISPLAY_W / 780)

    pins = [
        (1, "left", 504.3, "Real price + rating\nabove the fold"),
        (2, "right", 643.3, "Trust proof pulled up\n(15,500+ businesses)"),
        (3, "left", 1064.3, "Real product, background\nremoved, uncropped"),
        (4, "right", 1557.3, "CTA now points at\none specific product"),
    ]

    pin_font = syne(16, 800)
    num_font = ImageFont.truetype(DMMONO_R, 12)
    left_zone_x = after_x - 70
    right_zone_x = after_x + DISPLAY_W + 70
    left_pin_cx = after_x - 35
    right_pin_cx = after_x + DISPLAY_W + 35

    for num, side, raw_y, label in pins:
        cy = raw_to_canvas_y(raw_y)
        pin_cx = left_pin_cx if side == "left" else right_pin_cx
        edge_x = after_x if side == "left" else after_x + DISPLAY_W
        # leader line
        d.line([(pin_cx + (16 if side == "left" else -16), cy), (edge_x, cy)], fill=(255, 149, 0), width=3)
        # pin circle
        r = 22
        d.ellipse((pin_cx - r, cy - r, pin_cx + r, cy + r), fill=(255, 149, 0))
        center_text(d, (pin_cx, cy - 1), str(num), num_font, (10, 10, 10))

    canvas.save(f"{OUT_DIR}/ba-graphic.png")
    print("saved ba-graphic.png", canvas.size)


# ══════════════════════════════════════════════════════════════
# ANNO-GRAPHIC — annotated changes, light bg, curved arrows
# ══════════════════════════════════════════════════════════════
def cubic_bezier(p0, p1, p2, p3, n=48):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def draw_arrow(d, start, c1, c2, end, color=(21, 19, 18), width=3):
    """Cubic bezier arrow. c1 gives the start-side personality (vary this
    freely for different curve shapes). c2 MUST stay close to `end`'s x/y
    (within ~10px) so the final approach into the endpoint is nearly flat —
    this is what keeps the arrowhead pointing cleanly into the target
    instead of up/down at a weird angle."""
    pts = cubic_bezier(start, c1, c2, end, n=48)
    d.line(pts, fill=color, width=width, joint="curve")
    tx, ty = pts[-1][0] - pts[-4][0], pts[-1][1] - pts[-4][1]
    ang = math.atan2(ty, tx)
    ah = 12
    p0 = end
    p1 = (end[0] - ah * math.cos(ang - math.radians(22)), end[1] - ah * math.sin(ang - math.radians(22)))
    p2 = (end[0] - ah * math.cos(ang + math.radians(22)), end[1] - ah * math.sin(ang + math.radians(22)))
    d.polygon([p0, p1, p2], fill=color)


def build_anno_graphic():
    W = 1090
    IMG_TOP = 264
    DISPLAY_H_LOCAL = DISPLAY_H
    H = IMG_TOP + DISPLAY_H_LOCAL + 100
    canvas = Image.new("RGB", (W, H), (241, 239, 233))
    d = ImageDraw.Draw(canvas)

    head_font = syne(44, 800)
    sub_font = ImageFont.truetype(DMMONO_R, 15)

    lines = wrap_text(d, "NO PRICE. NO RATING. NO PRODUCT. NOT ON SCREEN ONE.", head_font, 820)
    y = 56
    for ln in lines:
        center_text(d, (W / 2, y), ln, head_font, (21, 19, 18))
        y += 54
    center_text(d, (W / 2, y + 10), "TAPRO CARDS: 8 THINGS ABOUT THE REBUILT HOMEPAGE", sub_font, (21, 19, 18))

    after_im = load_cropped(AFTER_RAW)
    img_x = (W - DISPLAY_W) / 2
    mask = Image.new("L", after_im.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, after_im.width, after_im.height), radius=14, fill=255)
    canvas.paste(after_im, (int(img_x), IMG_TOP), mask)

    def raw_to_canvas_y(raw_y):
        return IMG_TOP + raw_y * (DISPLAY_W / 780)

    # 8 points: (side, raw_y, target_x_on_edge, caption, curve_style)
    points = [
        ("left", 35, "One thin line,\nnot two"),
        ("right", 152, "No duplicate\nsearch icon"),
        ("left", 302, "Says what it\nactually does"),
        ("left", 504.3, "$34.95,\nreal price"),
        ("right", 504.3, "4.9 stars,\n1,125 reviews"),
        ("right", 643.3, "15,500+ real\nbusinesses"),
        ("left", 1064.3, "Real product,\nbackground removed"),
        ("right", 1557.3, "One clear\nnext step"),
    ]

    cap_font = ImageFont.truetype(CAVEAT, 26)
    left_edge = img_x
    right_edge = img_x + DISPLAY_W
    ARROW_GAP = 130  # horizontal span the arrow actually travels, clear of both caption text and image content
    # a few different start-side curve personalities, cycled for visual variety
    curve_variants = [-46, 34, -30, 50, -40, 28, -50, 38]

    for i, (side, raw_y, caption) in enumerate(points):
        cy = raw_to_canvas_y(raw_y)
        capt_lines = caption.split("\n")
        variety = curve_variants[i % len(curve_variants)]
        if side == "left":
            cap_right_x = left_edge - ARROW_GAP - 28   # caption block ends here, well clear of the arrow
            arrow_start_x = left_edge - ARROW_GAP
            arrow_end_x = left_edge + 6                # nudged just inside the image edge, touching real content
            start = (arrow_start_x, cy + variety * 0.6)
            c1 = (arrow_start_x + 34, cy + variety)      # start-side personality — free to vary
            c2 = (arrow_end_x - 8, cy)                   # end-side — pinned close to end so approach stays flat
            end = (arrow_end_x, cy)
            draw_arrow(d, start, c1, c2, end)
            ty = cy - (len(capt_lines) * 15)
            for cl in capt_lines:
                bbox = d.textbbox((0, 0), cl, font=cap_font)
                cw = bbox[2] - bbox[0]
                d.text((cap_right_x - cw, ty), cl, font=cap_font, fill=(21, 19, 18))
                ty += 30
        else:
            cap_left_x = right_edge + ARROW_GAP + 28
            arrow_start_x = right_edge + ARROW_GAP
            arrow_end_x = right_edge - 6
            start = (arrow_start_x, cy + variety * 0.6)
            c1 = (arrow_start_x - 34, cy + variety)
            c2 = (arrow_end_x + 8, cy)
            end = (arrow_end_x, cy)
            draw_arrow(d, start, c1, c2, end)
            ty = cy - (len(capt_lines) * 15)
            for cl in capt_lines:
                d.text((cap_left_x, ty), cl, font=cap_font, fill=(21, 19, 18))
                ty += 30

    canvas.save(f"{OUT_DIR}/anno-graphic.png")
    print("saved anno-graphic.png", canvas.size)


if __name__ == "__main__":
    build_ba_graphic()
    build_anno_graphic()
