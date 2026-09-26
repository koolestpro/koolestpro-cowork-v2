#!/usr/bin/env python3
"""Assemble the Bebemoss CRO Fix content pack.

Reuses the approved Material Kitchen content pack's <style> and <script>
blocks byte for byte (region swap, same approach the Tips builder uses),
and writes fresh Section 01-04 markup for Bebemoss.

Every raster image is base64 embedded so html2canvas downloads work from
file:// without tainting the canvas.
"""
import base64
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CF = os.path.join(ROOT, "outputs", "cro-fixes")
REF = os.path.join(CF, "materialkitchen_homepage-above-the-fold_content.html")
OUT = os.path.join(CF, "bebemoss_toys-collection_content.html")

SLUG = "bebemoss_toys-collection"


def b64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def grab(html, start_tag, end_tag):
    i = html.index(start_tag)
    j = html.index(end_tag, i) + len(end_tag)
    return html[i:j]


ref = open(REF, encoding="utf-8").read()
STYLE = grab(ref, "<style>", "</style>")
SCRIPT = ref[ref.rindex("<script>"):ref.rindex("</script>") + len("</script>")]

# The reference script already declares POST_BRAND/POST_SLUG/POST_TYPE/POST_FOLDER,
# TOTAL and sendToPipeline(). Re-declaring them in a second <script> would throw
# "already been declared" and kill that whole block, so retarget them in place
# instead of appending a duplicate.
_SUBS = [
    ("const POST_BRAND  = 'Material Kitchen';",
     "const POST_BRAND  = 'Bebemoss';"),
    ("const POST_SLUG   = 'materialkitchen_homepage-above-the-fold';",
     "const POST_SLUG   = 'bebemoss_toys-collection';"),
    ("const TOTAL = 6;", "const TOTAL = 7;"),
    ("title:'Material Kitchen homepage: the proof, price and trust were all below the scroll',",
     "title:'Bebemoss soft toys collection: the mission paragraph was the whole first screen',"),
    ("'✓ Exported — open ridwan_content_system_updated.html and sync.'",
     "'Exported. Open ridwan_content_system_updated.html and sync.'"),
]
for old, new in _SUBS:
    if old not in SCRIPT:
        raise SystemExit("Reference script changed, substitution not found:\n  " + old)
    SCRIPT = SCRIPT.replace(old, new)

# --- Bebemoss palette overrides layered after the reusable stylesheet ---
BRAND_CSS = """
<style>
/* Bebemoss brand overrides */
#ba-graphic{background:#151312}
#anno-graphic{background:#FCF8F5}
.ba-title{font-family:'Syne',sans-serif;font-weight:800;font-size:54px;top:52px;line-height:1.1}
.an-title{font-family:'Syne',sans-serif;font-weight:800;font-size:50px;top:48px;line-height:1.1;color:#151312}
.ba-glow{background:radial-gradient(circle,rgba(193,115,95,0.24),transparent 70%)}
.an-cap{color:#1F3D33;font-size:26px}
.an-cap b{color:#C1735F}
.an-img{left:370px;top:200px;width:340px}
.an-arrows{left:0;top:0;width:1080px;height:1080px}
.s-li:before{background:#C1735F}
.dot.active{background:#C1735F}
</style>
"""

BEFORE = b64(os.path.join(CF, "_bebemoss_before_raw.png"))
AFTER = b64(os.path.join(CF, "_bebemoss_after_raw.png"))
ARROWS = b64(os.path.join(CF, "_bebemoss_arrows.png"))

# ---------------------------------------------------------------- section 01
# ph-img is 300px wide (390 CSS capture -> scale 0.7692), top 322.
S = 300 / 390.0
BA_TOP = 322
AFTER_LEFT = 660


def ba_y(page_y):
    return round(BA_TOP + page_y * S)


# three pins = the three real fixes, split across both sides of the AFTER image
BA_PINS = [
    ("left", 186, "1"),   # filter + sort row
    ("right", 405, "2"),  # first product row, name + price at the fold
    ("right", 814, "3"),  # save pill moved clear
]

pin_html = []
for side, py, num in BA_PINS:
    y = ba_y(py)
    if side == "left":
        pin_html.append(
            f'<div class="lead" style="left:{AFTER_LEFT - 25}px;top:{y}px;width:25px"></div>'
            f'<div class="pin" style="left:{AFTER_LEFT - 59}px;top:{y - 17}px">{num}</div>'
        )
    else:
        r = AFTER_LEFT + 300
        pin_html.append(
            f'<div class="lead" style="left:{r}px;top:{y}px;width:25px"></div>'
            f'<div class="pin" style="left:{r + 25}px;top:{y - 17}px">{num}</div>'
        )

SECTION_01 = f"""
<!-- SECTION 01 BEFORE/AFTER -->
<div class="section-label">01 - Before / After</div>
<div class="section-divider"></div>
<div class="wrap">
<div id="ba-graphic" class="sqg">
  <div class="ba-glow" style="top:-120px;right:-120px"></div>
  <div class="ba-glow" style="bottom:-160px;left:-140px"></div>
  <div class="ba-title">The mission ate the<br>whole first screen.</div>
  <div class="ba-credit">bebemoss.com - soft toys collection, mobile. CRO teardown by @koolestpro</div>
  <div class="ph-label" style="left:170px;color:rgba(255,255,255,0.45)">Before</div>
  <div class="ph-label" style="left:{AFTER_LEFT + 52}px;color:#E8A98F">After</div>
  <img class="ph-img" style="left:120px" src="{BEFORE}" alt="before">
  <img class="ph-img" style="left:{AFTER_LEFT}px" src="{AFTER}" alt="after">
  {''.join(pin_html)}
</div>
</div>
"""

# ---------------------------------------------------------------- section 02
CAPS_LEFT = [
    (262, "1", "Collection finally has a name"),
    (388, "3", "Six ranges, now tappable"),
    (552, "5", "Name and price at the fold"),
    (745, "7", "Four toys before any scroll"),
]
CAPS_RIGHT = [
    (222, "6", "Header and breadcrumb kept"),
    (318, "2", "Mission down to one line"),
    (445, "4", "Sort by price, new"),
    (905, "8", "Save pill clear of the text"),
]

caps = []
for top, n, txt in CAPS_LEFT:
    caps.append(
        f'<div class="an-cap" style="left:10px;width:322px;text-align:right;top:{top}px">'
        f'<b>{n}</b>{txt}</div>'
    )
for top, n, txt in CAPS_RIGHT:
    caps.append(
        f'<div class="an-cap" style="left:748px;width:322px;text-align:left;top:{top}px">'
        f'<b>{n}</b>{txt}</div>'
    )

SECTION_02 = f"""
<!-- SECTION 02 ANNOTATION -->
<div class="section-label">02 - The rebuilt fold, annotated</div>
<div class="section-divider"></div>
<div class="wrap">
<div id="anno-graphic" class="sqg">
  <div class="an-title">What I moved, kept<br>and what I cut.</div>
  <img class="an-img" src="{AFTER}" alt="after annotated">
  <img class="an-arrows" src="{ARROWS}" alt="">
  {''.join(caps)}
</div>
</div>
"""

# ---------------------------------------------------------------- section 03
TOTAL = 7


def slide(n, accent, blob_rgba, eyebrow, headline, body="", items=None,
          cover=False, cta=False):
    items = items or []
    num = f"{n:02d}"
    blob_pos = "top:-60px;right:-60px" if n % 2 else "bottom:-40px;left:-50px"
    parts = [
        '<div class="slide">',
        '<div class="dotgrid"></div>',
        f'<div class="accentbar" style="background:{accent}"></div>',
        f'<div class="blob" style="width:250px;height:250px;'
        f'background:radial-gradient(circle,{blob_rgba},transparent 70%);{blob_pos}"></div>',
    ]
    if cover:
        parts.append('<div class="s-num" style="color:rgba(255,255,255,0.04);'
                     'font-size:120px;right:30px;top:20px">01</div>')
        parts.append(f'<span class="eyebrow">{eyebrow}</span>')
        parts.append(f'<div style="margin-top:120px" class="s-h">{headline}</div>')
    else:
        parts.append(f'<div class="s-num" style="color:{blob_rgba}">{num}</div>')
        parts.append(
            f'<div style="font-family:\'DM Mono\';font-size:12px;letter-spacing:2px;'
            f'text-transform:uppercase;color:{accent};margin-bottom:14px">{eyebrow}</div>')
        parts.append(f'<div class="s-h">{headline}</div>')
    parts.append(f'<div class="s-rule" style="background:{accent}"></div>')
    if body:
        parts.append(f'<div class="s-b">{body}</div>')
    for it in items:
        parts.append(f'<div class="s-li">{it}</div>')
    if cover:
        parts.append('<div style="position:absolute;bottom:56px;left:44px;'
                     'font-family:\'DM Mono\',monospace;font-size:13px;color:#C1735F">SWIPE &rarr;</div>')
    if cta:
        parts.append(
            '<div style="position:absolute;bottom:74px;left:44px;display:flex;'
            'align-items:center;gap:14px">'
            '<div style="width:64px;height:64px;border-radius:50%;overflow:hidden;'
            'border:2px solid rgba(193,115,95,0.5);flex-shrink:0">'
            '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2" '
            'style="width:100%;height:100%;object-fit:cover;object-position:center top" '
            'onerror="this.style.display=\'none\'"></div>'
            '<div style="font-family:\'DM Mono\',monospace;font-size:12px;'
            'color:rgba(255,255,255,0.55);line-height:1.6">Ridwan Adekunle<br>'
            '<span style="color:#C1735F">CRO for eCommerce</span></div></div>')
    parts.append(f'<div class="scount">{n} / {TOTAL}</div><div class="shandle">@koolestpro</div>')
    if n < TOTAL:
        parts.append('<div class="swb" onclick="goTo(current+1)">&rsaquo;</div>')
    parts.append('</div>')
    return "\n".join(parts)


SLIDES = [
    slide(1, "linear-gradient(90deg,#C1735F,#1F3D33)", "rgba(193,115,95,0.25)",
          "CRO teardown",
          "Beautiful story.<br>It's also the entire<br>first screen.",
          body="Bebemoss soft toys collection, on mobile.",
          cover=True),
    slide(2, "#3b82f6", "rgba(59,130,246,0.16)",
          "The problem",
          "519px of story.<br>844px of screen.<br>No toys.",
          body="The page opens with five sentences about the mission. "
               "That block is 519px tall on a phone. The screen is 844.<br><br>"
               "The first toy creeps in at the bottom edge with its name and price cut off."),
    slide(3, "#eab308", "rgba(234,179,8,0.14)",
          "Why it costs sales",
          "They already<br>decided they<br>want toys.",
          body="Someone who taps \"Soft Toys\" has made that choice already.<br><br>"
               "The first screen answers a question they did not ask."),
    slide(4, "#ef4444", "rgba(239,68,68,0.14)",
          "Second problem",
          "A discount tab<br>parked on the<br>prices.",
          body="A pink \"Save 10%\" tab sits docked bottom left. The page runs 8,200px "
               "and it rides the whole way down.<br><br>"
               "On my screen it covered a toy's name and its price."),
    slide(5, "#a855f7", "rgba(168,85,247,0.14)",
          "Third problem",
          "48 toys.<br>No filter.<br>No sort.",
          body="Bebemoss names its own ranges in its own copy. Safari, Ocean, "
               "Woodland, Garden Life, Dreams.<br><br>"
               "None of it is something you can tap."),
    slide(6, "#22c55e", "rgba(34,197,94,0.14)",
          "The fix",
          "Same photos.<br>Same prices.<br>I moved the toys up.",
          items=[
              "Mission cut to one line, story link kept",
              "Five ranges become filter chips",
              "A price sort next to them",
              "Grid starts at the fold, four toys visible",
              "Save pill shrunk, moved clear of card text",
          ]),
    slide(7, "linear-gradient(90deg,#C1735F,#1F3D33)", "rgba(193,115,95,0.2)",
          "Your turn",
          "Your collection<br>page probably<br>does this too.",
          body="If the first screen of yours is copy instead of product, "
               "send me the link. I will tell you what I would move.",
          cta=True),
]

SECTION_03 = f"""
<!-- SECTION 03 CAROUSEL -->
<div class="section-label">03 - Carousel</div>
<div class="section-divider"></div>
<div class="lk-frame">
  <div class="lk-header">
    <div class="lk-av"><img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" onerror="this.style.display='none'"></div>
    <div class="lk-meta"><b>Ridwan Adekunle</b><span>CRO for eCommerce &middot; @koolestpro</span></div>
  </div>
  <div id="viewport">
    <div id="track">
{chr(10).join(SLIDES)}
    </div>
  </div>
  <div id="dots"></div>
  <div id="pager"></div>
</div>

<div id="download-panel">
  <button onclick="dlSlide(current)">Download this slide</button>
  <button onclick="dlAll()">Download all slides</button>
  <button onclick="dlPDF()">Download PDF</button>
  <button onclick="dlFixed('ba-graphic')">Download Before/After</button>
  <button onclick="dlFixed('anno-graphic')">Download Annotated</button>
  <div id="download-status" aria-live="polite"></div>
</div>
"""

# ---------------------------------------------------------------- section 04
LINKEDIN = """Bebemoss makes handmade toys. Every one crocheted by a woman artisan, a lot of them refugees. I like the brand, which is exactly why the collection page bothered me.

It opens with five sentences about the mission. On a phone that block is 519px tall and the screen is 844, so the whole first screen is copy. The first toy creeps in at the bottom edge with its name and price still cut off.

Nobody taps "Soft Toys" to read a mission statement. They tap it to see toys.

Two other things while I was in there.

A pink "Save 10%" tab is docked to the bottom left. The page runs 8,200px and that tab rides the whole way down. On my screen it sat right on top of a toy's name and price.

And there are 48 products with no filter and no sort. Bebemoss already names its ranges in its own copy, Safari, Ocean, Woodland, Garden Life, Dreams. None of that is something a shopper can tap.

So I rebuilt the top of the page. Same photos, same prices, same brand.

- Mission down to one line, with a "Read our story" link for anyone who wants the rest
- Those five ranges as filter chips, price sort sitting next to them
- Grid starts at the fold, four toys with names and prices before you scroll
- Save pill shrunk and moved bottom right, clear of the card text

The story still sells. It just sells better standing next to the toys instead of in front of them.

If your collection page opens with a paragraph, go look at it on your phone right now.

Ridwan

#ecommerce #cro #shopify #dtc #conversionrateoptimization"""

INSTAGRAM = """This toy brand's story is beautiful. It's also the entire first screen.

Bebemoss sells handmade crochet toys. Their collection page opens with five sentences about the mission. On a phone that paragraph is 519px tall, the screen is 844, so you scroll past all of it before you see a single toy.

Two more things I found:
A pink "Save 10%" tab docked bottom left, riding the full 8,200px scroll, sitting on top of a toy's name and price.
48 products with no filter and no sort, even though the brand names its own ranges in its own copy.

I rebuilt the top. Same photos, same prices:
Mission to one line, story link kept
Five ranges as filter chips
Price sort added
Grid starts at the fold
Save pill moved clear of the text

Save this if your collection page opens with a paragraph.

@koolestpro
#ecommerce #cro #shopify #dtc #collectionpage"""

HOOKS = """1. This toy brand's story is beautiful. It's also the entire first screen.

2. 519px of mission statement. 844px of screen. Zero toys.

3. Nobody taps "Soft Toys" to read a mission statement.

4. Their discount popup has been sitting on a product's price this whole time.

5. 48 products, no filter, no sort, and the brand already named its own ranges."""

X_ANGLES = """ANGLE A:
Bebemoss sells handmade crochet toys. Lovely brand.

Their collection page opens with a 519px mission paragraph on an 844px screen.

You scroll past the whole first screen before you see a toy.

ANGLE B:
Found a "Save 10%" tab docked to the bottom left of a collection page.

The page is 8,200px long. The tab rides the whole way down.

It was sitting on top of a product's name and price.

ANGLE C:
48 products. No filter. No sort.

The brand names its own ranges in its own copy: Safari, Ocean, Woodland, Garden Life, Dreams.

None of it is tappable. The taxonomy exists, it just never made it onto the page."""

X_THREAD = """1/ Bebemoss makes handmade crochet toys, each one made by a woman artisan.

Good brand. Their collection page still buries the toys. Quick teardown.

2/ The page opens with five sentences about the mission.

That block is 519px tall. A phone screen is 844.

So the entire first screen is copy.

3/ The first toy only reaches the bottom edge, with its name and price still cut off.

Someone who tapped "Soft Toys" already decided they want toys. The first screen answers a question they did not ask.

4/ Second thing: a pink "Save 10%" tab docked bottom left.

The page runs 8,200px and the tab rides all of it. On my screen it covered a toy's name and its price.

5/ Third: 48 products, no filter, no sort.

Bebemoss names its ranges in its own copy. Safari, Ocean, Woodland, Garden Life, Dreams. None of it is tappable.

6/ Rebuild, same photos and same prices:

Mission to one line with a story link. Five ranges as filter chips. Price sort. Grid starts at the fold. Save pill moved clear of the card text.

7/ The story still sells. It sells better standing next to the toys than in front of them.

If your collection page opens with a paragraph, open it on your phone."""

TABS = [
    ("tab-linkedin", "LinkedIn", LINKEDIN, True),
    ("tab-ig", "Instagram", INSTAGRAM, False),
    ("tab-hook", "Hook Variations", HOOKS, False),
    ("tab-twitter-angles", "Twitter Angles", X_ANGLES, False),
    ("tab-twitter-thread", "Twitter Thread", X_THREAD, False),
]

btns = "".join(
    f'<button class="tab-btn{" active" if act else ""}" '
    f'onclick="openTab(this,\'{tid}\')">{label}</button>'
    for tid, label, _, act in TABS
)
panels = "".join(
    f'<div id="{tid}" class="tab-panel{" active" if act else ""}">\n<pre>{txt}</pre>\n'
    f'<button onclick="copyText(\'{tid}\')">Copy</button>\n</div>\n'
    for tid, _, txt, act in TABS
)

SECTION_04 = f"""
<!-- SECTION 04 POST COPY -->
<div class="section-label">04 - Post copy</div>
<div class="section-divider"></div>
<div class="tabs-wrap">
  <div class="tab-buttons">{btns}</div>
  {panels}
</div>
"""

# ---------------------------------------------------------------- pipeline
PIPELINE = """
<div style="max-width:600px;margin:0 auto;padding:40px 20px 60px;">
<div style="background:#0a0a0a;border:1px solid rgba(255,149,0,0.2);border-radius:12px;padding:24px;">
  <div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;margin-bottom:8px;">Content Pipeline</div>
  <div style="font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.45);line-height:1.7;margin-bottom:18px;">Export this post to the content system. Downloads a <code>.json</code> file. Open <code>ridwan_content_system_updated.html</code> and sync to register it.</div>
  <button onclick="sendToPipeline()" style="background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;font-family:'Syne',sans-serif;font-weight:700;font-size:13px;padding:12px 28px;border:none;border-radius:8px;cursor:pointer;letter-spacing:0.5px;">Send to Content Pipeline &rarr;</button>
  <div id="pipeline-status" style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.35);margin-top:12px;min-height:16px;"></div>
</div>
</div>
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Bebemoss - CRO Fix Content Pack</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Caveat:wght@500;600;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
{STYLE}
{BRAND_CSS}
</head>
<body>
{SECTION_01}
{SECTION_02}
{SECTION_03}
{SECTION_04}
{PIPELINE}
{SCRIPT}
</body>
</html>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)

opens = HTML.count("<div")
closes = HTML.count("</div>")
print(f"Wrote {OUT} ({len(HTML):,} chars)")
print(f"div balance: {opens} open / {closes} close -> {'OK' if opens == closes else 'MISMATCH'}")
print("em dashes:", HTML.count("—"))
