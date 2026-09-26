from PIL import Image, ImageDraw, ImageFont
import math

ASSETS = "outputs/cro-fixes/caraway/_assets/"
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(FONT_DIR+name, size)
    except Exception:
        return ImageFont.load_default()

BG = (10,10,10)
ACCENT = (255,149,0)
WHITE = (255,255,255)

# ---------- BA-GRAPHIC (1:1, 1200x1200) ----------
W = H = 1200
canvas = Image.new("RGB", (W,H), BG)
draw = ImageDraw.Draw(canvas)

# top accent bar
draw.rectangle([0,0,W,10], fill=ACCENT)

# PAGE-TYPE LABEL (added 2026-09-07, Ridwan's standing instruction) — every before/after
# and annotated graphic must state what kind of page this is, visibly, not just in notes.
def draw_page_type_badge(d, x, y, text="PRODUCT PAGE (PDP)", fg=ACCENT, bg=(30,30,30)):
    pad_x, pad_y = 16, 8
    bbox = d.textbbox((0,0), text, font=font(18,True))
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    d.rounded_rectangle([x, y, x+tw+pad_x*2, y+th+pad_y*2+4], radius=6, fill=bg, outline=fg, width=2)
    d.text((x+pad_x, y+pad_y-2), text, font=font(18,True), fill=fg)
    return tw+pad_x*2

draw_page_type_badge(draw, 60, 22)

# headline — scope specific to this audit's real finding
headline = "Price & Proof, Reconnected"
sub = "Same fry pan. The decision now happens in one glance, not three."
draw.text((60,70), headline, font=font(56,True), fill=WHITE)
draw.text((60,138), sub, font=font(24), fill=(255,255,255,160))

# labels
draw.text((60,208), "BEFORE", font=font(20,True), fill=(255,255,255,120))
draw.text((640,208), "AFTER", font=font(20,True), fill=ACCENT)

before = Image.open(ASSETS+"before_popup3.png").convert("RGB")
after = Image.open(ASSETS+"after_raw.png").convert("RGB")

col_w, col_h = 430, 900
before_r = before.resize((col_w, int(col_w*before.height/before.width)))
after_r = after.resize((col_w, int(col_w*after.height/after.width)))
before_r = before_r.crop((0,0,col_w,min(col_h,before_r.height)))
after_r = after_r.crop((0,0,col_w,min(col_h,after_r.height)))

by = 248
bx = 50
ax = 640
# rounded-rect frames
def paste_framed(img, x, y):
    frame = Image.new("RGB", (img.width+8, img.height+8), (40,40,40))
    frame.paste(img, (4,4))
    canvas.paste(frame, (x-4, y-4))

paste_framed(before_r, bx, by)
paste_framed(after_r, ax, by)

# numbered pins on the AFTER image, split left/right, for the 3 real fixes
pin_pts = [
    (ax-2, by+160, "1", "left"),      # price directly under title
    (ax+col_w+2, by+205, "2", "right"), # rating renders inline w/ stars+count
    (ax+col_w+2, by+520, "3", "right"), # hero image now visible above the fold
]

def draw_pin(x, y, label, side):
    r = 22
    leader_len = 30
    if side == "left":
        lx = x - leader_len
        draw.line([(lx,y),(x,y)], fill=ACCENT, width=3)
        cx = lx
    else:
        lx = x + leader_len
        draw.line([(x,y),(lx,y)], fill=ACCENT, width=3)
        cx = lx
    draw.ellipse([cx-r,y-r,cx+r,y+r], fill=ACCENT)
    bbox = draw.textbbox((0,0), label, font=font(24,True))
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text((cx-tw/2, y-th/2-4), label, font=font(24,True), fill=(20,20,20))

for (x,y,label,side) in pin_pts:
    draw_pin(x,y,label,side)

canvas.save(ASSETS+"ba-graphic.png")
print("ba-graphic saved", canvas.size)

# ---------- ANNO-GRAPHIC (1:1, 1200x1200) — arrows pre-rasterized in-image ----------
canvas2 = Image.new("RGB", (W,H), (247,245,239))
draw2 = ImageDraw.Draw(canvas2)
draw2.rectangle([0,0,W,10], fill=ACCENT)

draw_page_type_badge(draw2, 60, 22, fg=(21,19,18), bg=(247,245,239))

headline2 = "What Actually Changed, Named"
draw2.text((60,70), headline2, font=font(54,True), fill=(21,19,18))
draw2.text((60,136), "Three real fixes on the same product page.", font=font(24), fill=(90,88,80))

after_big_w = 430
after_big = after.resize((after_big_w, int(after_big_w*after.height/after.width)))
ax2, ay2 = (W-after_big_w)//2, 250
canvas2.paste(after_big, (ax2, ay2))

# annotation targets, mapped from the 390-wide screenshot to the after_big_w-wide render
scale = after_big_w/390
def mapx(px): return ax2 + int(px*scale)
def mapy(py): return ay2 + int(py*scale)

def draw_curved_arrow(start, end, color=ACCENT, width=5):
    x0,y0 = start
    x2,y2 = end
    mx, my = (x0+x2)/2, y0 + (y2-y0)*0.15
    pts = []
    steps = 30
    for i in range(steps+1):
        t = i/steps
        xt = (1-t)**2*x0 + 2*(1-t)*t*mx + t**2*x2
        yt = (1-t)**2*y0 + 2*(1-t)*t*my + t**2*y2
        pts.append((xt,yt))
    draw2.line(pts, fill=color, width=width, joint="curve")
    (ex,ey) = pts[-1]
    (px,py) = pts[-3]
    ang = math.atan2(ey-py, ex-px)
    ah = 15
    a1 = (ex - ah*math.cos(ang-0.4), ey - ah*math.sin(ang-0.4))
    a2 = (ex - ah*math.cos(ang+0.4), ey - ah*math.sin(ang+0.4))
    draw2.polygon([ (ex,ey), a1, a2 ], fill=color)

def wrap_text(text, w=18):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        test = (cur+" "+wd).strip()
        if len(test) > w:
            lines.append(cur); cur = wd
        else:
            cur = test
    if cur: lines.append(cur)
    return lines

def label_block(x, y, text, align="left"):
    lines = wrap_text(text)
    for i, ln in enumerate(lines):
        bbox = draw2.textbbox((0,0), ln, font=font(21,True))
        lw = bbox[2]-bbox[0]
        lx = x if align=="left" else x-lw
        draw2.text((lx, y+i*27), ln, font=font(21,True), fill=(21,19,18))
    return len(lines)*27

# left-margin labels (logo, price) with arrows pointing right into the image
label_block(50, 250, "Real logo, pulled directly from their own site", align="left")
draw_curved_arrow((300, 275), (mapx(70), mapy(45)))

label_block(50, 430, "Price sits directly under the title now", align="left")
draw_curved_arrow((300, 452), (mapx(20), mapy(225)))

# right-margin labels (reviews, photo) with arrows pointing left into the image
label_block(870, 340, "Stars + review count", align="left")
draw_curved_arrow((865, 362), (mapx(410), mapy(260)))

label_block(870, 640, "Product photo fills the first screen", align="left")
draw_curved_arrow((865, 662), (mapx(410), mapy(480)))

canvas2.save(ASSETS+"anno-graphic.png")
print("anno-graphic saved", canvas2.size)
