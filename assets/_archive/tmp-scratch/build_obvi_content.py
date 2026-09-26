#!/usr/bin/env python3
"""Build outputs/cro-fixes/obvi_homepage-hero_content.html (Skill E content pack).

Follows .ai-workflow/project-constitution.md:
  - 1:1 square #ba-graphic / #anno-graphic, 1080x1080
  - headline 52-60px Syne, solid color only (no gradient text anywhere)
  - every raster image base64-embedded (file:// canvas tainting)
  - arrow overlay pre-rasterized to PNG (live <svg> vanishes in html2canvas)
  - pins on the AFTER image only, split both sides, leaders extend into the UI
  - carousel 540x680 portrait, scale:2, chrome hidden via visibility:hidden
"""
import base64
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CRO = os.path.join(ROOT, "outputs", "cro-fixes")
TMP = os.path.join(ROOT, ".ai-workflow", "tmp")

POST_SLUG = "obvi_homepage-hero"
OUT = os.path.join(CRO, POST_SLUG + "_content.html")
TITLE = "Obvi's homepage headline announces inventory, not a reason to buy"

INK = "#151312"
PINK = "#E0399B"
PURPLE = "#4B2E9E"
LIGHT = "#FDF3FA"
TOTAL = 6


def b64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


BEFORE = b64(os.path.join(CRO, "_obvi_before_raw.png"))
AFTER = b64(os.path.join(CRO, "_obvi_after_raw.png"))
ARROWS = b64(os.path.join(TMP, "_obvi_arrows.png"))

# ---------------------------------------------------------------- annotations
# canvas coords; must match .ai-workflow/tmp/build_obvi_arrows.py POINTS
ANNOS = [
    (343, "L", 1, "Their own hero photo, untouched"),
    (438, "R", 2, "Stock news demoted to a pill"),
    (500, "L", 3, "Headline names the outcome now"),
    (603, "R", 4, "One sentence, now four scannable lines"),
    (671, "L", 5, "The 800,000 proof given real weight"),
    (711, "R", 6, "Button carries the actual offer"),
    (800, "L", 7, "Real best seller, real price, real reviews"),
    (892, "R", 8, "Widget moved clear of every button"),
]

# ba-graphic pins: real fixes only, split both sides.
# after image: left 660, top 322, width 300 (scale 300/390 = 0.7692)
BA_PINS = [
    (590, "L", 1),   # headline
    (695, "R", 2),   # benefit lines
    (791, "L", 3),   # offer CTA
    (869, "R", 4),   # real price + reviews
]


def anno_caps():
    out = []
    for y, side, n, text in ANNOS:
        top = y - 20
        if side == "L":
            out.append(
                f'  <div class="an-cap" style="left:10px;width:315px;text-align:right;top:{top}px">'
                f'<b>{n}</b>{text}</div>'
            )
        else:
            out.append(
                f'  <div class="an-cap" style="left:755px;width:315px;text-align:left;top:{top}px">'
                f'<b>{n}</b>{text}</div>'
            )
    return "\n".join(out)


def ba_pins():
    out = []
    for y, side, n in BA_PINS:
        if side == "L":
            out.append(
                f'  <div class="lead" style="left:635px;top:{y}px;width:25px"></div>'
                f'<div class="pin" style="left:599px;top:{y-18}px">{n}</div>'
            )
        else:
            out.append(
                f'  <div class="lead" style="left:960px;top:{y}px;width:25px"></div>'
                f'<div class="pin" style="left:985px;top:{y-18}px">{n}</div>'
            )
    return "\n".join(out)


# -------------------------------------------------------------------- captions
LINKEDIN = """Obvi has over 800,000 customers and a best seller sitting at 1,489 reviews.

The biggest words on their mobile homepage say "BACK IN STOCK."

That is a warehouse update. It only lands for someone who already tried to buy and got told no. Everyone else, which on a homepage fed by paid social is nearly everyone, reads the largest text on the screen and learns nothing about what the product does.

The part that would actually sell is right underneath at 13px, welded into one 40 word sentence. Metabolism, cravings, weight loss, hair, skin and nails, all in a single breath. Four real reasons to buy and not one of them scannable.

Then there is the bit I had to zoom in on to believe. The accessibility widget renders on top of the bottom left corner of the SHOP NOW button. Tap a little low and you get a settings panel instead of the store.

So I rebuilt the top of the page. Same pink, same purple, same wordmark, same product photo.

Headline states the outcome, using Obvi's own line from further down their page.
"Back in stock" moved to a small pill where it still works for returning buyers.
The paragraph became four benefit lines you can read in a second.
The 800,000 customer proof got weight instead of grey 11px type.
One primary button carrying the real offer, quiz demoted to a link under it.
The real best seller pulled up with its real price of $29.74 and its real 1,489 reviews.
Widget moved clear of every tap target.

Nothing was redesigned. The brand was already doing its job. The hero was just spending its biggest slot announcing inventory.

Quick test for your own homepage. If the headline would still make sense written on a warehouse whiteboard, it is not selling.

Ridwan

Prices, review counts and certifications shown are Obvi's own, read off the live site. Statements about supplements have not been evaluated by the FDA."""

IG = """800,000 customers. And the biggest words on the homepage say BACK IN STOCK.

That is a warehouse update, not a reason to buy. If you have never heard of Obvi, the largest text on the screen tells you nothing about what the product does.

The real value prop sits under it at 13px, four benefits welded into one 40 word sentence. And the accessibility widget renders on top of the corner of the SHOP NOW button.

I rebuilt the hero. Same pink, same purple, same product photo:

Headline that names the outcome
Stock news demoted to a small pill
Four scannable benefit lines instead of a paragraph
The 800,000 proof given real weight
One button carrying the real offer
Real best seller at its real price with its real review count
Widget moved clear of every button

Your headline is your most expensive real estate. Do not spend it on inventory news.

Save this if your homepage looks fine and still is not selling.

@koolestpro
#ecommerce #cro #shopify #dtc #conversionrateoptimization

Prices and review counts shown are Obvi's own. Statements about supplements have not been evaluated by the FDA."""

HOOKS = """1. Their homepage's biggest words announce inventory. Not a single reason to buy.

2. 800,000 customers, and the headline still says BACK IN STOCK.

3. The accessibility widget is sitting on top of their SHOP NOW button. Nobody noticed.

4. Your headline is the most expensive real estate you own. Stop spending it on stock updates.

5. If your homepage headline would make sense on a warehouse whiteboard, it is not selling."""

X_ANGLES = """ANGLE A:
Obvi's mobile homepage headline is "BACK IN STOCK."

That is a warehouse update, not a reason to buy.

The actual value prop sits under it at 13px, four benefits welded into one sentence.

ANGLE B:
Found this on a supplement brand with 800,000+ customers.

Their accessibility widget renders on top of the bottom corner of the primary SHOP NOW button.

Tap a little low and you get a settings panel instead of the store.

ANGLE C:
Quick test for your homepage.

If the headline would still make sense written on a warehouse whiteboard, it is not selling.

"Back in stock" is a warehouse sentence."""

X_THREAD = """1/ Obvi has 800,000+ customers and a best seller with 1,489 reviews.

The biggest text on their mobile homepage says "BACK IN STOCK." Quick teardown.

2/ "Back in stock" only lands for someone who already tried to buy and got told no.

Everyone else learns nothing about what the product actually does.

3/ The real value prop is right under it at 13px. Metabolism, cravings, weight loss, hair, skin and nails, all in one 40 word sentence.

Four reasons to buy. None of them scannable.

4/ Then the accessibility widget renders on top of the bottom left corner of the SHOP NOW button.

Tap low, get a settings panel instead of the store.

5/ Two CTAs sit side by side at the same weight, and the secondary one is physically bigger than the primary. Neither wins.

6/ Rebuild, same brand. Outcome headline, four scannable benefit lines, proof given weight, one primary button with the real offer, real best seller at $29.74 with 1,489 reviews, widget moved clear.

7/ Nothing was redesigned. The brand was fine. The hero was just spending its biggest slot announcing inventory.

Ridwan, @koolestpro"""


def slide(n, body):
    return body


SLIDES = f"""
      <!-- SLIDE 1 COVER -->
      <div class="slide">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:linear-gradient(90deg,{PINK},{PURPLE})"></div>
        <div class="blob" style="width:260px;height:260px;background:radial-gradient(circle,rgba(224,57,155,0.25),transparent 70%);top:-60px;right:-60px"></div>
        <div class="s-num" style="color:rgba(255,255,255,0.04);font-size:120px;right:30px;top:20px">01</div>
        <span class="eyebrow">CRO teardown</span>
        <div style="margin-top:120px" class="s-h">800,000 customers.<br>And the headline still<br>says "back in stock."</div>
        <div class="s-rule" style="background:{PINK}"></div>
        <div class="s-b">A look at Obvi's mobile hero, and the version that actually sells.</div>
        <div style="position:absolute;bottom:56px;left:44px;font-family:'DM Mono',monospace;font-size:13px;color:{PINK}">SWIPE &rarr;</div>
        <div class="scount">1 / {TOTAL}</div><div class="shandle">@koolestpro</div>
        <div class="swb" onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 2 PROBLEM -->
      <div class="slide">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:#3b82f6"></div>
        <div class="blob" style="width:240px;height:240px;background:radial-gradient(circle,rgba(59,130,246,0.18),transparent 70%);bottom:-40px;left:-50px"></div>
        <div class="s-num" style="color:rgba(59,130,246,0.1)">02</div>
        <div style="font-family:'DM Mono';font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#3b82f6;margin-bottom:14px">The problem</div>
        <div class="s-h">The biggest text<br>on the page is<br>a stock update.</div>
        <div class="s-rule" style="background:#3b82f6"></div>
        <div class="s-b">"BACK IN STOCK" at 30px. It only lands for someone who already tried to buy and got told no.<br><br>Everyone else reads the largest text on the screen and still has no idea what the product does.</div>
        <div class="scount">2 / {TOTAL}</div><div class="shandle">@koolestpro</div>
        <div class="swb" onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 3 DIAGNOSIS -->
      <div class="slide">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:#eab308"></div>
        <div class="blob" style="width:240px;height:240px;background:radial-gradient(circle,rgba(234,179,8,0.14),transparent 70%);top:-40px;right:-40px"></div>
        <div class="s-num" style="color:rgba(234,179,8,0.1)">03</div>
        <div style="font-family:'DM Mono';font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#eab308;margin-bottom:14px">Why it costs sales</div>
        <div class="s-h">The good stuff is<br>there. It is just<br>set at 13px.</div>
        <div class="s-rule" style="background:#eab308"></div>
        <div class="s-b">Metabolism, cravings, weight loss, hair, skin and nails, all welded into one 40 word sentence under the headline.<br><br>Four real reasons to buy, and not one of them scannable on a phone.</div>
        <div class="scount">3 / {TOTAL}</div><div class="shandle">@koolestpro</div>
        <div class="swb" onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 4 FIX -->
      <div class="slide">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:#22c55e"></div>
        <div class="blob" style="width:240px;height:240px;background:radial-gradient(circle,rgba(34,197,94,0.14),transparent 70%);bottom:-40px;right:-40px"></div>
        <div class="s-num" style="color:rgba(34,197,94,0.1)">04</div>
        <div style="font-family:'DM Mono';font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#22c55e;margin-bottom:14px">The fix</div>
        <div class="s-h" style="font-size:30px">Same brand. I just<br>gave the hero a job.</div>
        <div class="s-rule" style="background:#22c55e"></div>
        <div class="s-li">Headline names the outcome, in Obvi's own words</div>
        <div class="s-li">Stock news demoted to a small pill</div>
        <div class="s-li">One sentence split into four scannable lines</div>
        <div class="s-li">Real best seller: $29.74, 1,489 reviews, 30% off</div>
        <div class="s-li">Accessibility widget moved off the SHOP NOW button</div>
        <div class="scount">4 / {TOTAL}</div><div class="shandle">@koolestpro</div>
        <div class="swb" onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 5 RESULT -->
      <div class="slide">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:linear-gradient(90deg,{PINK},{PURPLE})"></div>
        <div class="blob" style="width:260px;height:260px;background:radial-gradient(circle,rgba(224,57,155,0.2),transparent 70%);top:-50px;left:-50px"></div>
        <div class="s-num" style="color:rgba(255,255,255,0.05)">05</div>
        <div style="font-family:'DM Mono';font-size:12px;letter-spacing:2px;text-transform:uppercase;color:{PINK};margin-bottom:14px">The result</div>
        <div class="s-h" style="font-size:30px">None of this is new.<br>It was all already<br>on the page.</div>
        <div class="s-rule" style="background:{PINK}"></div>
        <div class="s-b">Same pink. Same purple. Same product photo. Every price, review count and claim is Obvi's own.<br><br>The hero just stopped announcing inventory and started answering "why should I buy this."</div>
        <div class="scount">5 / {TOTAL}</div><div class="shandle">@koolestpro</div>
        <div class="swb" onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 6 CTA -->
      <div class="slide" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:linear-gradient(90deg,{PINK},{PURPLE})"></div>
        <div class="blob" style="width:300px;height:300px;background:radial-gradient(circle,rgba(224,57,155,0.22),transparent 70%);top:40px;left:50%;transform:translateX(-50%)"></div>
        <div style="width:180px;height:180px;border-radius:50%;overflow:hidden;border:2px solid rgba(224,57,155,0.5);margin:0 auto 22px;position:relative;z-index:2">
          <img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2" style="width:100%;height:100%;object-fit:cover;object-position:center top" onerror="this.style.display='none'">
        </div>
        <div class="s-h" style="font-size:28px;position:relative;z-index:2">Is your headline<br>doing any selling?</div>
        <div class="s-b" style="margin-top:14px;text-align:center">I rebuild above-the-fold sections so the first screen answers the buyer's question instead of the warehouse's.</div>
        <div style="margin-top:22px;background:linear-gradient(90deg,{PINK},{PURPLE});color:#fff;font-family:'Syne';font-weight:700;font-size:14px;padding:12px 26px;border-radius:999px;position:relative;z-index:2">Follow @koolestpro</div>
        <div class="scount">6 / {TOTAL}</div><div class="shandle">@koolestpro</div>
      </div>
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Obvi · CRO Fix content pack</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=Caveat:wght@600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0e0e0e;color:#fff;font-family:'DM Mono',monospace;padding:40px 20px 80px}}
.section-label{{max-width:1080px;margin:40px auto 14px;font-family:'DM Mono',monospace;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#FF9500}}
.section-divider{{max-width:1080px;margin:0 auto 24px;height:1px;background:rgba(255,255,255,0.08)}}
.wrap{{max-width:1080px;margin:0 auto;overflow-x:auto}}

/* ===== SQUARE GRAPHICS ===== */
.sqg{{width:1080px;height:1080px;position:relative;overflow:hidden;flex-shrink:0}}
#ba-graphic{{background:{INK}}}
.ba-title{{position:absolute;top:56px;left:70px;right:70px;font-family:'Syne',sans-serif;font-weight:800;font-size:54px;line-height:1.1;color:#fff;letter-spacing:-1px}}
.ba-credit{{position:absolute;top:214px;left:70px;font-family:'DM Mono',monospace;font-size:16px;color:rgba(255,255,255,0.5)}}
.ba-glow{{position:absolute;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(224,57,155,0.24),transparent 70%);filter:blur(70px);pointer-events:none}}
.ph-label{{position:absolute;top:284px;font-family:'DM Mono',monospace;font-size:15px;letter-spacing:3px;text-transform:uppercase}}
.ph-img{{position:absolute;top:322px;width:300px;border-radius:6px;display:block;box-shadow:0 18px 50px rgba(0,0,0,0.55)}}
.pin{{position:absolute;width:36px;height:36px;border-radius:50%;background:#fff;color:{PURPLE};font-family:'DM Mono',monospace;font-weight:500;font-size:19px;text-align:center;line-height:36px;box-shadow:0 3px 10px rgba(0,0,0,0.4)}}
.lead{{position:absolute;height:2px;background:rgba(255,255,255,0.75)}}

#anno-graphic{{background:{LIGHT}}}
.an-title{{position:absolute;top:52px;left:64px;right:64px;font-family:'Syne',sans-serif;font-weight:800;font-size:46px;line-height:1.12;color:{INK};letter-spacing:-1px}}
.an-img{{position:absolute;left:370px;top:180px;width:340px;border-radius:8px;display:block;box-shadow:0 16px 44px rgba(0,0,0,0.18)}}
.an-arrows{{position:absolute;left:0;top:0;width:1080px;height:1080px;pointer-events:none}}
.an-cap{{position:absolute;font-family:'Caveat',cursive;font-weight:600;font-size:27px;color:{PURPLE};line-height:1.05}}
.an-cap b{{font-family:'DM Mono',monospace;font-weight:500;font-size:19px;color:{PINK};margin-right:5px}}

/* ===== CAROUSEL ===== */
.lk-frame{{max-width:588px;margin:0 auto;background:#1a1a1a;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,0.08)}}
.lk-header{{display:flex;align-items:flex-start;gap:10px;padding:14px 16px 10px}}
.lk-av{{width:42px;height:42px;border-radius:50%;overflow:hidden;flex-shrink:0}}
.lk-meta b{{font-family:'Syne',sans-serif;font-size:14px}}
.lk-meta span{{display:block;font-size:11px;color:rgba(255,255,255,0.4)}}
#viewport{{width:540px;height:680px;overflow:hidden;position:relative;cursor:grab;margin:0 auto;background:#080808}}
#track{{display:flex;transition:transform 0.32s cubic-bezier(0.4,0,0.2,1);will-change:transform}}
.slide{{width:540px;height:680px;flex-shrink:0;position:relative;overflow:hidden;background:#080808;padding:52px 44px}}
.dotgrid{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.02) 1px,transparent 1px);background-size:24px 24px;pointer-events:none}}
.blob{{position:absolute;border-radius:50%;filter:blur(70px);pointer-events:none}}
.accentbar{{position:absolute;top:0;left:0;right:0;height:3px}}
.scount{{position:absolute;bottom:20px;left:24px;font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.2)}}
.shandle{{position:absolute;bottom:20px;right:24px;font-family:'DM Mono',monospace;font-size:9px;color:rgba(255,255,255,0.15)}}
.swb{{position:absolute;right:0;top:50%;transform:translateY(-50%);width:32px;height:80px;display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,0.35);font-size:22px;cursor:pointer;z-index:20;background:linear-gradient(to right,transparent,rgba(0,0,0,0.25));user-select:none}}
.eyebrow{{display:inline-block;font-family:'DM Mono',monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;border:1px solid rgba(255,255,255,0.2);border-radius:999px;color:rgba(255,255,255,0.6)}}
.s-num{{position:absolute;right:28px;top:24px;font-family:'Syne',sans-serif;font-weight:800;font-size:80px}}
.s-h{{font-family:'Syne',sans-serif;font-weight:800;font-size:34px;line-height:1.12;color:#fff;position:relative;z-index:2}}
.s-rule{{height:2px;width:44px;margin:16px 0;border-radius:2px}}
.s-b{{font-family:'DM Mono',monospace;font-size:15px;line-height:1.7;color:rgba(255,255,255,0.5);position:relative;z-index:2}}
.s-li{{font-family:'DM Mono',monospace;font-size:15px;line-height:1.55;color:rgba(255,255,255,0.72);margin:10px 0;padding-left:20px;position:relative}}
.s-li:before{{content:"";position:absolute;left:0;top:9px;width:8px;height:8px;border-radius:2px;background:{PINK}}}
#dots{{display:flex;justify-content:center;gap:6px;padding:12px 0}}
.dot{{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,0.18);cursor:pointer;transition:all 0.2s}}
.dot.active{{background:#FF9500;width:20px;border-radius:3px}}
#pager{{text-align:center;font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.28);padding-bottom:8px}}
#download-panel{{max-width:588px;margin:22px auto 0;display:flex;flex-wrap:wrap;gap:8px;justify-content:center}}
#download-panel button{{background:#161616;color:#eee;border:1px solid rgba(255,255,255,0.14);border-radius:8px;padding:9px 14px;font-family:'DM Mono',monospace;font-size:11px;cursor:pointer}}
#download-status{{width:100%;text-align:center;font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.4);margin-top:6px;min-height:14px}}

/* ===== TABS ===== */
.tabs-wrap{{max-width:640px;margin:0 auto}}
.tab-buttons{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}}
.tab-btn{{background:#161616;color:rgba(255,255,255,0.6);border:1px solid rgba(255,255,255,0.12);border-radius:8px;padding:8px 13px;font-family:'DM Mono',monospace;font-size:11px;cursor:pointer}}
.tab-btn.active{{background:#FF9500;color:#111;border-color:#FF9500}}
.tab-panel{{display:none;background:#111;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:18px}}
.tab-panel.active{{display:block}}
.tab-panel pre{{white-space:pre-wrap;font-family:'DM Mono',monospace;font-size:13px;line-height:1.7;color:rgba(255,255,255,0.82)}}
.tab-panel button{{margin-top:12px;background:{PURPLE};color:#fff;border:none;border-radius:8px;padding:8px 16px;font-family:'Syne',sans-serif;font-weight:700;font-size:12px;cursor:pointer}}
</style>
</head>
<body>

<!-- SECTION 01 BEFORE/AFTER -->
<div class="section-label">01 · Before / After</div>
<div class="section-divider"></div>
<div class="wrap">
<div id="ba-graphic" class="sqg">
  <div class="ba-glow" style="top:-120px;right:-120px"></div>
  <div class="ba-glow" style="bottom:-160px;left:-140px"></div>
  <div class="ba-title">Their biggest headline<br>announces inventory.</div>
  <div class="ba-credit">myobvi.com · homepage, mobile · CRO teardown by @koolestpro</div>
  <div class="ph-label" style="left:170px;color:rgba(255,255,255,0.45)">Before</div>
  <div class="ph-label" style="left:712px;color:{PINK}">After</div>
  <img class="ph-img" style="left:120px" src="{BEFORE}" alt="before">
  <img class="ph-img" style="left:660px" src="{AFTER}" alt="after">
{ba_pins()}
</div>
</div>

<!-- SECTION 02 ANNOTATION -->
<div class="section-label">02 · Above the fold, annotated</div>
<div class="section-divider"></div>
<div class="wrap">
<div id="anno-graphic" class="sqg">
  <div class="an-title">Eight fixes on one screen.<br>The brand never changed.</div>
  <img class="an-img" src="{AFTER}" alt="after annotated">
  <img class="an-arrows" src="{ARROWS}" alt="">
{anno_caps()}
</div>
</div>

<!-- SECTION 03 CAROUSEL -->
<div class="section-label">03 · Carousel</div>
<div class="section-divider"></div>
<div class="lk-frame">
  <div class="lk-header">
    <div class="lk-av"><img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" onerror="this.style.display='none'"></div>
    <div class="lk-meta"><b>Ridwan Adekunle</b><span>CRO for eCommerce · @koolestpro</span></div>
  </div>
  <div id="viewport">
    <div id="track">
{SLIDES}
    </div>
    <div class="swb" id="main-swb" onclick="goTo(current+1)">&rsaquo;</div>
  </div>
  <div id="dots"></div>
  <div id="pager">Slide 1 of {TOTAL}</div>
</div>

<div id="download-panel">
  <button onclick="dlSlide(current)">Download current slide</button>
  <button onclick="dlAll()">Download all slides</button>
  <button onclick="dlPDF()">Download PDF</button>
  <button onclick="dlFixed('ba-graphic')">Download Before/After</button>
  <button onclick="dlFixed('anno-graphic')">Download Annotated</button>
  <div id="download-status" aria-live="polite"></div>
</div>

<!-- SECTION 04 POST COPY -->
<div class="section-label">04 · Post copy</div>
<div class="section-divider"></div>
<div class="tabs-wrap">
  <div class="tab-buttons">
    <button class="tab-btn active" onclick="openTab(this,'tab-linkedin')">LinkedIn</button>
    <button class="tab-btn" onclick="openTab(this,'tab-ig')">Instagram</button>
    <button class="tab-btn" onclick="openTab(this,'tab-hook')">Hook Variations</button>
    <button class="tab-btn" onclick="openTab(this,'tab-twitter-angles')">Twitter Angles</button>
    <button class="tab-btn" onclick="openTab(this,'tab-twitter-thread')">Twitter Thread</button>
  </div>

  <div id="tab-linkedin" class="tab-panel active">
<pre>{LINKEDIN}</pre>
    <button onclick="copyText('tab-linkedin')">Copy</button>
  </div>

  <div id="tab-ig" class="tab-panel">
<pre>{IG}</pre>
    <button onclick="copyText('tab-ig')">Copy</button>
  </div>

  <div id="tab-hook" class="tab-panel">
<pre>{HOOKS}</pre>
    <button onclick="copyText('tab-hook')">Copy</button>
  </div>

  <div id="tab-twitter-angles" class="tab-panel">
<pre>{X_ANGLES}</pre>
    <button onclick="copyText('tab-twitter-angles')">Copy</button>
  </div>

  <div id="tab-twitter-thread" class="tab-panel">
<pre>{X_THREAD}</pre>
    <button onclick="copyText('tab-twitter-thread')">Copy</button>
  </div>
</div>

<!-- PIPELINE EXPORT -->
<div style="max-width:600px;margin:40px auto 0;padding:0 20px 60px">
<div style="background:#0a0a0a;border:1px solid rgba(255,149,0,0.2);border-radius:12px;padding:24px">
  <div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;margin-bottom:8px">Content Pipeline</div>
  <div style="font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.45);line-height:1.7;margin-bottom:18px">Export this post to the content system. Downloads a <code>.json</code> file, then open <code>ridwan_content_system_updated.html</code> and sync to register it.</div>
  <button onclick="sendToPipeline()" style="background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;font-family:'Syne',sans-serif;font-weight:700;font-size:13px;padding:12px 28px;border:none;border-radius:8px;cursor:pointer;letter-spacing:0.5px">Send to Content Pipeline &rarr;</button>
  <div id="pipeline-status" style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.35);margin-top:12px;min-height:16px"></div>
</div>
</div>

<script>
const POST_BRAND  = 'Obvi';
const POST_SLUG   = '{POST_SLUG}';
const POST_TYPE   = 'CRO Fix';
const POST_FOLDER = 'outputs/cro-fixes/' + POST_SLUG + '_content.html';
const TOTAL = {TOTAL};

// carousel
const track = document.getElementById('track');
const slides = Array.from(document.querySelectorAll('.slide'));
const dotsWrap = document.getElementById('dots');
const pager = document.getElementById('pager');
let current = 0;
slides.forEach((_,i)=>{{const d=document.createElement('div');d.className='dot'+(i===0?' active':'');d.onclick=()=>goTo(i);dotsWrap.appendChild(d);}});
function goTo(i){{current=Math.max(0,Math.min(TOTAL-1,i));track.style.transform=`translateX(-${{current*540}}px)`;document.querySelectorAll('.dot').forEach((d,j)=>d.classList.toggle('active',j===current));pager.textContent=`Slide ${{current+1}} of ${{TOTAL}}`;const sw=document.getElementById('main-swb');if(sw)sw.style.display=(current>=TOTAL-1)?'none':'flex';}}

async function waitForSlideAssets(el){{
  if(document.fonts&&document.fonts.ready)await document.fonts.ready;
  const images=Array.from(el.querySelectorAll('img'));
  await Promise.all(images.map(img=>{{
    if(img.complete&&img.naturalWidth>0)return Promise.resolve();
    if(img.decode)return img.decode().catch(()=>{{}});
    return new Promise(r=>{{img.onload=r;img.onerror=r;}});
  }}));
}}
async function captureSlide(idx){{
  const slide=slides[idx];
  if(!slide)throw new Error(`Slide ${{idx+1}} was not found.`);
  const toHide=document.querySelectorAll('[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap');
  toHide.forEach(el=>el.style.visibility='hidden');
  const prevT=track.style.transform,prevTr=track.style.transition;
  track.style.transform=`translateX(-${{idx*540}}px)`;track.style.transition='none';
  try{{
    await waitForSlideAssets(slide);
    await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
    return await html2canvas(slide,{{scale:2,useCORS:true,allowTaint:true,backgroundColor:'#080808',logging:false}});
  }}finally{{track.style.transform=prevT;track.style.transition=prevTr;toHide.forEach(el=>el.style.visibility='');}}
}}
async function captureFixed(id){{
  const el=document.getElementById(id);
  if(!el)throw new Error(id+' not found');
  const toHide=document.querySelectorAll('[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap');
  toHide.forEach(e=>e.style.visibility='hidden');
  try{{
    await waitForSlideAssets(el);
    await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
    return await html2canvas(el,{{scale:2,useCORS:true,allowTaint:true,backgroundColor:null,logging:false}});
  }}finally{{toHide.forEach(e=>e.style.visibility='');}}
}}
function setDownloadStatus(m){{const s=document.getElementById('download-status');if(s)s.textContent=m||'';}}
async function dlSlide(idx){{try{{setDownloadStatus(`Preparing slide ${{idx+1}}...`);const c=await captureSlide(idx);const a=document.createElement('a');a.href=c.toDataURL('image/png');a.download=`koolestpro_${{POST_SLUG}}_slide${{idx+1}}.png`;a.click();setDownloadStatus(`Slide ${{idx+1}} downloaded.`);}}catch(e){{console.error(e);setDownloadStatus(`Slide ${{idx+1}} failed: ${{e.message}}`);}}}}
async function dlAll(){{for(let i=0;i<TOTAL;i++){{await dlSlide(i);await new Promise(r=>setTimeout(r,300));}}}}
async function dlFixed(id){{try{{setDownloadStatus(`Preparing ${{id}}...`);const c=await captureFixed(id);const a=document.createElement('a');a.href=c.toDataURL('image/png');a.download=`koolestpro_${{POST_SLUG}}_${{id}}.png`;a.click();setDownloadStatus(`${{id}} downloaded.`);}}catch(e){{console.error(e);setDownloadStatus(`${{id}} failed: ${{e.message}}`);}}}}
async function dlPDF(){{try{{if(!window.jspdf||!window.jspdf.jsPDF)throw new Error('PDF library did not load.');const {{jsPDF}}=window.jspdf;const pdf=new jsPDF({{orientation:'portrait',unit:'px',format:[540,680],compress:true}});for(let i=0;i<TOTAL;i++){{setDownloadStatus(`Adding slide ${{i+1}} of ${{TOTAL}} to PDF...`);const c=await captureSlide(i);if(i>0)pdf.addPage([540,680],'portrait');pdf.addImage(c.toDataURL('image/jpeg',0.92),'JPEG',0,0,540,680);}}setDownloadStatus('Saving PDF...');pdf.save(`koolestpro_${{POST_SLUG}}.pdf`);setDownloadStatus('PDF downloaded.');}}catch(e){{console.error(e);setDownloadStatus(`PDF failed: ${{e.message}}`);}}}}

// tabs
function openTab(el,id){{document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));el.classList.add('active');document.getElementById(id).classList.add('active');}}
function copyText(id){{const text=document.getElementById(id).querySelector('pre').innerText;navigator.clipboard.writeText(text).then(()=>{{const btn=document.querySelector(`[onclick="copyText('${{id}}')"]`);if(btn){{btn.textContent='Copied!';setTimeout(()=>btn.textContent='Copy',1800);}}}});}}

// pipeline
function sendToPipeline(){{
  const now=new Date();
  const dateStr=now.toISOString().slice(0,10).replace(/-/g,'');
  const data={{
    id:POST_TYPE.toLowerCase().replace(' ','-')+'-'+POST_SLUG+'-'+dateStr,
    type:POST_TYPE,
    title:{TITLE!r},
    slug:POST_SLUG,
    status:'Created',
    day:'',
    created:now.toISOString(),
    folder:POST_FOLDER,
    week:'Week of '+now.toLocaleDateString('en-US',{{month:'long',day:'numeric'}}),
    month:now.toLocaleDateString('en-US',{{month:'long',year:'numeric'}}),
    monthSlug:now.toISOString().slice(0,7)
  }};
  console.log('EXPORT_POST_JSON',JSON.stringify(data));
  const blob=new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=POST_SLUG+'_pipeline.json';document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(a.href);
  const s=document.getElementById('pipeline-status');if(s)s.textContent='Exported. Open ridwan_content_system_updated.html and sync.';
}}
goTo(0);
</script>
</body>
</html>
"""

with open(OUT, "w") as f:
    f.write(HTML)

opens = HTML.count("<div")
closes = HTML.count("</div>")
print("wrote", OUT, len(HTML), "chars")
print("div balance:", opens, closes, "OK" if opens == closes else "MISMATCH")
assert "&mdash;" not in HTML, "em dash entity found"
bad = [s for s in (LINKEDIN, IG, HOOKS, X_ANGLES, X_THREAD) if "—" in s]
print("em dashes in captions:", len(bad))
