#!/usr/bin/env python3
"""
Build the Gainful CRO Fix content pack.

Two stages:
  1. Pre-rasterise the annotation arrow overlay to a transparent PNG.
     (A live <svg> renders fine natively but html2canvas silently drops the
     paths — see project-constitution.md. Never ship the SVG live.)
  2. Emit outputs/cro-fixes/gainful_customize-your-protein_content.html with
     every raster image base64-embedded (file:// canvas-tainting guard).

Usage:
  python3 .ai-workflow/tools/build_gainful_content.py
"""
import base64
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CRO = ROOT / "outputs" / "cro-fixes"

BEFORE = CRO / "_gainful_before_raw.png"
AFTER = CRO / "_gainful_after_raw.png"
ARROWS_HTML = CRO / "_gainful_arrows.html"
ARROWS_PNG = CRO / "_gainful_arrows.png"
OUT = CRO / "gainful_customize-your-protein_content.html"

# ── annotation geometry ──────────────────────────────────────────────
# #anno-graphic is 1080x1080. .an-img sits at left:370 top:230 width:340.
# The after screenshot is 390x844 CSS, so scale = 340/390 = 0.8718 and the
# image occupies y 230..966. Top was moved from 180 to 230 so the headline
# (two lines at 46px) clears caption 1 instead of colliding with it.
IMG_L, IMG_T, IMG_W = 370, 230, 340
SCALE = IMG_W / 390.0
IMG_R = IMG_L + IMG_W

# (n, side, arrow_y, caption_top, caption_html)
# arrow_y = IMG_T + (element's CSS y in the 390x844 after frame * SCALE)
POINTS = [
    (1, "L", 245, 205, "Two competing 25% offers became one"),
    (2, "R", 359, 320, "The bare review count is a real link now"),
    (3, "L", 418, 378, "The inputs finally say what they produce"),
    (4, "R", 644, 604, "Price became the anchor, with a per serving read"),
    (5, "L", 875, 858, "Subscribe is a real choice now"),
    (6, "R", 914, 874, "An add to cart, and cancel or skip anytime"),
]

# Start-side control points are varied for personality; the END-side control
# point is always within ~10px of the endpoint's y and close to its x, which
# is what keeps every arrowhead approaching flat instead of pointing up/down.
CURVE_START_DX = {1: (18, -24), 2: (-20, -30), 3: (22, -32),
                  4: (-22, 32), 5: (20, 34), 6: (-20, 26)}


def build_arrows_svg() -> str:
    paths = []
    for n, side, y, _ctop, _cap in POINTS:
        dx, dy = CURVE_START_DX[n]
        if side == "L":
            x0, x1 = 335, IMG_L + 20          # end 20px INSIDE the image
            c1x, c1y = x0 + dx, y + dy
            c2x, c2y = x1 - 18, y + (3 if dy > 0 else -3)
        else:
            x0, x1 = 745, IMG_R - 20
            c1x, c1y = x0 + dx, y + dy
            c2x, c2y = x1 + 18, y + (3 if dy > 0 else -3)
        paths.append(
            f'<path d="M{x0},{y} C{c1x},{c1y} {c2x},{c2y} {x1},{y}" '
            f'fill="none" stroke="#2B2A28" stroke-width="2.4" '
            f'marker-end="url(#ah)"/>'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" '
        'viewBox="0 0 1080 1080">'
        '<defs><marker id="ah" viewBox="0 0 9 9" refX="8" refY="4.5" '
        'markerWidth="5.5" markerHeight="5.5" orient="auto">'
        '<path d="M0,0 L9,4.5 L0,9 Z" fill="#2B2A28"/></marker></defs>'
        + "".join(paths) +
        "</svg>"
    )


def rasterise_arrows():
    ARROWS_HTML.write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<style>*{margin:0;padding:0}html,body{background:transparent}</style>"
        "</head><body>" + build_arrows_svg() + "</body></html>",
        encoding="utf-8",
    )
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1080},
                        device_scale_factor=2)
        pg.goto(f"file://{ARROWS_HTML}")
        pg.wait_for_timeout(600)
        pg.locator("svg").screenshot(path=str(ARROWS_PNG), omit_background=True)
        b.close()
    print(f"arrows -> {ARROWS_PNG}")


def b64(path: pathlib.Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


# ── captions (already humanised — see gainful-social-content.md) ─────
LINKEDIN = """Gainful asks you four questions before it gives you one reason to trust it.

Their protein customizer is a good idea. Pick a dietary preference, pick a goal, get a formula matched to it. On mobile it opens with two different 25% discounts stacked on top of each other, one for subscribing and one for a new customer code, and nothing on the page tells you whether they stack or which one you should take.

Then it asks for four decisions. Dietary preference. Primary goal. Serving size. Flavour packets.

And it never offers you a way to buy.

I searched every button and link on that page. There is no add to cart. No buy button. No checkout. The only call to action anywhere is Take The Quiz, sitting 3,693 pixels down, and it sends you into a different funnel than the one you were already halfway through.

The words guarantee, money back, cancel anytime and risk free do not appear on the page either. That last one matters, because the loudest thing on the screen is asking you to start a subscription.

So I rebuilt the top of it. Same type, same warm grey, same black pills, same photography.

One promo strip instead of two, and the subscribe offer moved down to the buy area where it is an actual choice.
Price given its own line at 29px with a per serving figure under it, because on a configurator the price is the running total.
A sticky bar carrying the live price and an add to cart, so the endpoint is visible from the first tap.
Cancel or skip anytime, sitting right where the subscription is being asked for.
The review count turned into a link you can actually check.
One line above the two selectors naming what they produce.

Nothing invented. Every number is Gainful's own, read off the live page: $31.47, 14 servings, 20g protein, 100 calories, 6 ingredients, 2,123 ratings.

If your page asks the shopper to do work, it owes them somewhere to put it.

Ridwan

The review quote in the rebuild is an illustrative placeholder, labelled as such in the file, not a real Gainful customer."""

INSTAGRAM = """Gainful asks you four questions before it gives you one reason to trust it.

Dietary preference. Primary goal. Serving size. Flavour packets.

Then nothing. No add to cart anywhere on the page. I checked every button and link on it. The only CTA is Take The Quiz, 3,693 pixels down, and it routes you into a different funnel.

No guarantee either. No cancel anytime. On a page whose top bar is selling a subscription.

So I rebuilt the top of it, same brand, nothing redesigned:

One promo strip instead of two competing 25% offers
Price as an anchor with a per serving read
A sticky add to cart carrying the live price
Cancel or skip anytime, next to the subscribe offer
The review count as a real link

Every number is theirs. $31.47, 14 servings, 20g protein, 2,123 ratings.

If your page asks the shopper to do work, give them somewhere to put it.

#ecommerce #shopify #cro #conversionrateoptimization #dtc #uxdesign"""

HOOKS = """1. Gainful asks you four questions before it gives you one reason to trust it.

2. I searched every button on this page for an add to cart. There isn't one.

3. Their protein customizer has no way to buy the protein.

4. Two 25% discounts stacked on top of each other, and nothing says which one you get.

5. The page asks for four decisions and offers you nowhere to put them.

6. A subscription offer with no cancellation terms anywhere on the page.

7. The only CTA on this page sits 3,693 pixels down and sends you somewhere else."""

X_ANGLES = """ANGLE 1: the missing button

Gainful's protein customizer asks for 4 decisions.

Dietary preference. Goal. Serving size. Flavour packets.

Then gives you nowhere to buy.

I searched every button and link on the page. There is no add to cart on it.

---

ANGLE 2: the two offers

Two 25% discounts stacked at the top of the page.

One for subscribing. One for a new customer code.

Nothing tells you whether they stack, or which one is the better deal.

Ambiguity at the offer level is the expensive kind. It hits every visitor before they see the product.

---

ANGLE 3: the missing safety net

The words guarantee, money back, cancel anytime and risk free appear nowhere on Gainful's customizer page.

The loudest thing on the screen is asking you to start a subscription.

Asking for a recurring commitment without stating the exit terms suppresses the take rate you were trying to raise."""

X_THREAD = """1/ Gainful asks you four questions before it gives you one reason to trust it.

Their protein customizer, on mobile. A teardown.

2/ It opens with two different 25% offers stacked on top of each other.

One for subscribing. One for a new customer code.

Nothing says whether they stack or which one you should take.

3/ Then it asks for four decisions.

Dietary preference. Primary goal. Serving size. Flavour packets.

4/ And it never offers you a way to buy.

I searched every button and link on the page. No add to cart. No buy button. No checkout.

5/ The only CTA anywhere is Take The Quiz, 3,693 pixels down.

It sends you into a different funnel than the one you were already halfway through.

6/ Guarantee. Money back. Cancel anytime. Risk free.

None of those words appear on the page.

The loudest thing on the screen is selling a subscription.

7/ So I rebuilt the top. Same type, same warm grey, same black pills.

One promo strip. Price as an anchor with a per serving read. A sticky add to cart. Cancel or skip anytime.

8/ Every number is Gainful's own, read off the live page.

$31.47. 14 servings. 20g protein. 100 calories. 6 ingredients. 2,123 ratings.

9/ If your page asks the shopper to do work, it owes them somewhere to put it."""


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    for f in (BEFORE, AFTER):
        if not f.exists():
            sys.exit(f"missing {f}")
    rasterise_arrows()

    before_b64, after_b64, arrows_b64 = b64(BEFORE), b64(AFTER), b64(ARROWS_PNG)

    caps = "\n".join(
        '  <div class="an-cap" style="{pos};top:{t}px"><b>{n}</b>{txt}</div>'.format(
            pos=("left:10px;width:315px;text-align:right"
                 if side == "L" else "left:755px;width:315px;text-align:left"),
            t=ctop, n=n, txt=cap)
        for n, side, _y, ctop, cap in POINTS
    )

    html = TEMPLATE.format(
        before=before_b64, after=after_b64, arrows=arrows_b64, caps=caps,
        linkedin=esc(LINKEDIN), instagram=esc(INSTAGRAM), hooks=esc(HOOKS),
        xangles=esc(X_ANGLES), xthread=esc(X_THREAD),
    )
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT}  ({len(html):,} chars)")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Gainful · CRO Fix content pack</title>
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
#ba-graphic{{background:#151312}}
.ba-title{{position:absolute;top:56px;left:70px;right:70px;font-family:'Syne',sans-serif;font-weight:800;font-size:54px;line-height:1.1;color:#fff;letter-spacing:-1px}}
.ba-credit{{position:absolute;top:230px;left:70px;font-family:'DM Mono',monospace;font-size:16px;color:rgba(255,255,255,0.5)}}
.ba-glow{{position:absolute;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(223,242,101,0.20),transparent 70%);filter:blur(70px);pointer-events:none}}
.ph-label{{position:absolute;top:284px;font-family:'DM Mono',monospace;font-size:15px;letter-spacing:3px;text-transform:uppercase}}
.ph-img{{position:absolute;top:322px;width:300px;border-radius:6px;display:block;box-shadow:0 18px 50px rgba(0,0,0,0.55)}}
.pin{{position:absolute;width:36px;height:36px;border-radius:50%;background:#DFF265;color:#2B2A28;font-family:'DM Mono',monospace;font-weight:500;font-size:19px;text-align:center;line-height:36px;box-shadow:0 3px 10px rgba(0,0,0,0.4)}}
.lead{{position:absolute;height:2px;background:rgba(223,242,101,0.85)}}

#anno-graphic{{background:#F4F3EF}}
.an-title{{position:absolute;top:52px;left:64px;right:64px;font-family:'Syne',sans-serif;font-weight:800;font-size:46px;line-height:1.12;color:#151312;letter-spacing:-1px}}
.an-img{{position:absolute;left:370px;top:230px;width:340px;border-radius:8px;display:block;box-shadow:0 16px 44px rgba(0,0,0,0.18)}}
.an-arrows{{position:absolute;left:0;top:0;width:1080px;height:1080px;pointer-events:none}}
.an-cap{{position:absolute;font-family:'Caveat',cursive;font-weight:600;font-size:27px;color:#2B2A28;line-height:1.05}}
.an-cap b{{font-family:'DM Mono',monospace;font-weight:500;font-size:19px;color:#7A8C0E;margin-right:5px}}

/* ===== CAROUSEL ===== */
.lk-frame{{max-width:588px;margin:0 auto;background:#1a1a1a;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,0.08)}}
.lk-header{{display:flex;align-items:flex-start;gap:10px;padding:14px 16px 10px}}
.lk-av{{width:42px;height:42px;border-radius:50%;overflow:hidden;flex-shrink:0}}
.lk-meta b{{font-family:'Syne',sans-serif;font-size:14px}}
.lk-meta span{{display:block;font-size:11px;color:rgba(255,255,255,0.4)}}
#viewport{{width:540px;height:680px;overflow:hidden;position:relative;cursor:grab;margin:0 auto;background:#080808}}
#track{{display:flex;transition:transform 0.32s cubic-bezier(0.4,0,0.2,1);will-change:transform}}
.slide{{width:540px;height:680px;flex-shrink:0;position:relative;overflow:hidden;background:#080808;padding:52px 44px}}
.slide.fill{{display:flex;flex-direction:column;justify-content:center;align-items:flex-start}}
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
.s-li:before{{content:"";position:absolute;left:0;top:9px;width:8px;height:8px;border-radius:2px;background:#DFF265}}
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
.tab-panel button{{margin-top:12px;background:#2B2A28;color:#fff;border:none;border-radius:8px;padding:8px 16px;font-family:'Syne',sans-serif;font-weight:700;font-size:12px;cursor:pointer}}
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
  <div class="ba-title">Four decisions asked.<br>Nowhere to put them.</div>
  <div class="ba-credit">gainful.com · protein customizer, mobile · CRO teardown by @koolestpro</div>
  <div class="ph-label" style="left:170px;color:rgba(255,255,255,0.45)">Before</div>
  <div class="ph-label" style="left:712px;color:#DFF265">After</div>
  <img class="ph-img" style="left:120px" src="{before}" alt="before">
  <img class="ph-img" style="left:660px" src="{after}" alt="after">
  <div class="lead" style="left:635px;top:335px;width:25px"></div><div class="pin" style="left:599px;top:317px">1</div>
  <div class="lead" style="left:635px;top:687px;width:25px"></div><div class="pin" style="left:599px;top:669px">2</div>
  <div class="lead" style="left:960px;top:926px;width:25px"></div><div class="pin" style="left:985px;top:908px">3</div>
</div>
</div>

<!-- SECTION 02 ANNOTATION -->
<div class="section-label">02 · Above the fold, annotated</div>
<div class="section-divider"></div>
<div class="wrap">
<div id="anno-graphic" class="sqg">
  <div class="an-title">The configurator was fine.<br>Everything else wasn't.</div>
  <img class="an-img" src="{after}" alt="after annotated">
  <img class="an-arrows" src="{arrows}" alt="">
{caps}
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

      <!-- SLIDE 1 COVER -->
      <div class="slide fill">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:linear-gradient(90deg,#DFF265,#7A8C0E)"></div>
        <div class="blob" style="width:260px;height:260px;background:radial-gradient(circle,rgba(223,242,101,0.22),transparent 70%);top:-60px;right:-60px"></div>
        <div class="s-num" style="color:rgba(255,255,255,0.04);font-size:120px;right:30px;top:20px">01</div>
        <span class="eyebrow" style="flex-shrink:0">CRO teardown</span>
        <div class="s-h" style="margin-top:26px">Four questions.<br>Then no way<br>to buy it.</div>
        <div class="s-rule" style="background:#DFF265"></div>
        <div class="s-b">A look at Gainful's protein customizer on mobile, and the version that lets you finish.</div>
        <div style="position:absolute;bottom:56px;left:44px;font-family:'DM Mono',monospace;font-size:13px;color:#DFF265">SWIPE &rarr;</div>
        <div class="scount">1 / 6</div><div class="shandle">@koolestpro</div>
        <div class="swb" onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 2 PROBLEM -->
      <div class="slide fill">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:#3b82f6"></div>
        <div class="blob" style="width:240px;height:240px;background:radial-gradient(circle,rgba(59,130,246,0.18),transparent 70%);bottom:-40px;left:-50px"></div>
        <div class="s-num" style="color:rgba(59,130,246,0.1)">02</div>
        <div style="font-family:'DM Mono';font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#3b82f6;margin-bottom:14px">The problem</div>
        <div class="s-h">There is no add<br>to cart anywhere<br>on the page.</div>
        <div class="s-rule" style="background:#3b82f6"></div>
        <div class="s-b">I scanned every button and link on it. No add to cart, no buy button, no checkout.<br><br>The only CTA is Take The Quiz, 3,693 pixels down, and it routes you into a different funnel.</div>
        <div class="scount">2 / 6</div><div class="shandle">@koolestpro</div>
        <div class="swb" onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 3 DIAGNOSIS -->
      <div class="slide fill">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:#eab308"></div>
        <div class="blob" style="width:240px;height:240px;background:radial-gradient(circle,rgba(234,179,8,0.14),transparent 70%);top:-40px;right:-40px"></div>
        <div class="s-num" style="color:rgba(234,179,8,0.1)">03</div>
        <div style="font-family:'DM Mono';font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#eab308;margin-bottom:14px">Why it costs sales</div>
        <div class="s-h">It opens with two<br>different 25%<br>offers at once.</div>
        <div class="s-rule" style="background:#eab308"></div>
        <div class="s-b">One for subscribing, one for a new customer code. Nothing says whether they stack.<br><br>Then it asks for four decisions and gives you nowhere to put them.</div>
        <div class="scount">3 / 6</div><div class="shandle">@koolestpro</div>
        <div class="swb" onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 4 FIX -->
      <div class="slide fill">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:#22c55e"></div>
        <div class="blob" style="width:240px;height:240px;background:radial-gradient(circle,rgba(34,197,94,0.14),transparent 70%);bottom:-40px;right:-40px"></div>
        <div class="s-num" style="color:rgba(34,197,94,0.1)">04</div>
        <div style="font-family:'DM Mono';font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#22c55e;margin-bottom:14px">The fix</div>
        <div class="s-h" style="font-size:30px">Same brand. I just<br>gave it an ending.</div>
        <div class="s-rule" style="background:#22c55e"></div>
        <div class="s-li">A sticky bar with the live price and an add to cart</div>
        <div class="s-li">One promo strip, subscribe moved to the buy area</div>
        <div class="s-li">Price at 29px with a per serving read under it</div>
        <div class="s-li">Cancel or skip anytime, next to the subscribe offer</div>
        <div class="s-li">The 2,123 review count turned into a real link</div>
        <div class="scount">4 / 6</div><div class="shandle">@koolestpro</div>
        <div class="swb" onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 5 RESULT -->
      <div class="slide fill">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:linear-gradient(90deg,#DFF265,#7A8C0E)"></div>
        <div class="blob" style="width:260px;height:260px;background:radial-gradient(circle,rgba(223,242,101,0.18),transparent 70%);top:-50px;left:-50px"></div>
        <div class="s-num" style="color:rgba(255,255,255,0.05)">05</div>
        <div style="font-family:'DM Mono';font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#DFF265;margin-bottom:14px">The result</div>
        <div class="s-h" style="font-size:30px">Nothing here was<br>redesigned. It was<br>reordered.</div>
        <div class="s-rule" style="background:#DFF265"></div>
        <div class="s-b">Same warm grey, same type, same black pills, same tub photo. Every number is Gainful's own.<br><br>$31.47. 14 servings. 20g protein. 100 calories. 6 ingredients. 2,123 ratings.</div>
        <div class="scount">5 / 6</div><div class="shandle">@koolestpro</div>
        <div class="swb" onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 6 CTA -->
      <div class="slide" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:linear-gradient(90deg,#DFF265,#7A8C0E)"></div>
        <div class="blob" style="width:300px;height:300px;background:radial-gradient(circle,rgba(223,242,101,0.20),transparent 70%);top:40px;left:50%;transform:translateX(-50%)"></div>
        <div style="width:180px;height:180px;border-radius:50%;overflow:hidden;border:2px solid rgba(223,242,101,0.5);margin:0 auto 22px;position:relative;z-index:2">
          <img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2" style="width:100%;height:100%;object-fit:cover;object-position:center top" onerror="this.style.display='none'">
        </div>
        <div class="s-h" style="font-size:28px;position:relative;z-index:2">Can a shopper finish<br>on your page?</div>
        <div class="s-b" style="margin-top:14px;text-align:center">I rebuild product and configurator pages so the work a shopper does actually leads somewhere.</div>
        <div style="margin-top:22px;background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;font-family:'Syne';font-weight:700;font-size:14px;padding:12px 26px;border-radius:999px;position:relative;z-index:2">Follow @koolestpro</div>
        <div class="scount">6 / 6</div><div class="shandle">@koolestpro</div>
      </div>

    </div>
    <div class="swb" id="main-swb" onclick="goTo(current+1)">&rsaquo;</div>
  </div>
  <div id="dots"></div>
  <div id="pager">Slide 1 of 6</div>
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
<pre>{linkedin}</pre>
    <button onclick="copyText('tab-linkedin')">Copy</button>
  </div>

  <div id="tab-ig" class="tab-panel">
<pre>{instagram}</pre>
    <button onclick="copyText('tab-ig')">Copy</button>
  </div>

  <div id="tab-hook" class="tab-panel">
<pre>{hooks}</pre>
    <button onclick="copyText('tab-hook')">Copy</button>
  </div>

  <div id="tab-twitter-angles" class="tab-panel">
<pre>{xangles}</pre>
    <button onclick="copyText('tab-twitter-angles')">Copy</button>
  </div>

  <div id="tab-twitter-thread" class="tab-panel">
<pre>{xthread}</pre>
    <button onclick="copyText('tab-twitter-thread')">Copy</button>
  </div>
</div>

<!-- PIPELINE EXPORT -->
<div style="max-width:600px;margin:0 auto;padding:40px 20px 60px">
<div style="background:#0a0a0a;border:1px solid rgba(255,149,0,0.2);border-radius:12px;padding:24px;margin-bottom:16px">
  <div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;margin-bottom:8px">Content Pipeline</div>
  <div style="font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.45);line-height:1.7;margin-bottom:18px">Export this post to the content system. Downloads a <code>.json</code> file. Open <code>ridwan_content_system_updated.html</code> and sync to register it.</div>
  <button onclick="sendToPipeline()" style="background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;font-family:'Syne',sans-serif;font-weight:700;font-size:13px;padding:12px 28px;border:none;border-radius:8px;cursor:pointer;letter-spacing:0.5px">Send to Content Pipeline &rarr;</button>
  <div id="pipeline-status" style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.35);margin-top:12px;min-height:16px"></div>
</div>
</div>

<script>
const POST_BRAND  = 'Gainful';
const POST_SLUG   = 'gainful_customize-your-protein';
const POST_TYPE   = 'CRO Fix';
const POST_FOLDER = 'outputs/cro-fixes/' + POST_SLUG + '_content.html';
const TOTAL = 6;

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

function openTab(el,id){{document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));el.classList.add('active');document.getElementById(id).classList.add('active');}}
function copyText(id){{const text=document.getElementById(id).querySelector('pre').innerText;navigator.clipboard.writeText(text).then(()=>{{const btn=document.querySelector(`[onclick="copyText('${{id}}')"]`);if(btn){{btn.textContent='Copied!';setTimeout(()=>btn.textContent='Copy',1800);}}}});}}

function sendToPipeline(){{
  const now=new Date();
  const dateStr=now.toISOString().slice(0,10).replace(/-/g,'');
  const data={{
    id:POST_TYPE.toLowerCase().replace(' ','-')+'-'+POST_SLUG+'-'+dateStr,
    type:POST_TYPE,
    title:"Gainful's protein customizer has no add to cart on it",
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

if __name__ == "__main__":
    main()
