#!/usr/bin/env python3
"""Build the Topicals homepage CRO rebuild (the "after" first screen) + hero variants.

Weekly CRO Fix, 2026-10-18. Fallback flow: Claude authors the page directly from
outputs/cro-fixes/topicals_homepage-hero_build-brief.md (unattended run, no page builder driven).

#1 finding (live page, 390x844, 2026-10-18): screen one is a full-screen "Try your luck /
Scratch here" game. Close it and the hero is a giant TOPICALS wordmark over a face photo, the
headline is a one-kit promo ("Bright Eyes & Slick Lips") at 668px, and a "Scratch to win" pill
sits on top of the only "Shop now" button. "Skincare for flare-ups" (what Topicals sells) only
exists in the browser tab title, and not one star rating appears anywhere on the homepage,
while the products carry 4.8 to 4.9 stars from hundreds of reviews each.

Every number below is from the live site (JSON-LD aggregateRating + homepage cards) on
2026-10-18. Real logo (header inline SVG, rasterized), real fonts (Chalet, Chalet Bold, ITC
Garamond Cond Italic from their Oxygen CDN), real packshots (background removed) and real
photos from their CDNs, all embedded as data URIs.

Usage: python3 build_topicals_rebuild.py            -> full rebuild (variant C hero, Ridwan's pick 2026-10-18)
       python3 build_topicals_rebuild.py --variants -> 4 hero variant pages in _variants/
"""
import base64, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "topicals" / "_assets"
OUT = ROOT / "outputs" / "cro-fixes" / "topicals_homepage-hero_rebuild.html"
VOUT = ROOT / "outputs" / "cro-fixes" / "topicals" / "_variants"


def uri(p: pathlib.Path) -> str:
    mime = {".png": "image/png", ".woff2": "font/woff2", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".webp": "image/webp"}[p.suffix]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def icon(name, size=16, color="currentColor"):
    svg = (A / "icons" / f"ic_{name}.svg").read_text()
    return (svg.replace('width="1em"', f'width="{size}"').replace('height="1em"', f'height="{size}"')
               .replace('fill="currentColor"', f'fill="{color}"')
               .replace("<svg ", '<svg aria-hidden="true" style="display:block;flex-shrink:0" ', 1))


def stars(size=12, color="#1a1a1a"):
    return '<span class="stars">' + "".join(icon("star", size, color) for _ in range(5)) + "</span>"


CSS = """
@font-face{font-family:'Chalet';src:url(__F_CH__) format('woff2');font-weight:400;font-display:block;}
@font-face{font-family:'Chalet';src:url(__F_CHB__) format('woff2');font-weight:700;font-display:block;}
@font-face{font-family:'GaramondCI';src:url(__F_GAR__) format('woff2');font-style:italic;font-display:block;}
:root{--ink:#111;--red:#EF4A4F;--pink:#F9D3D8;--blush:#FDEDEF;--soft:#5d5557;--line:#E8DCDD;}
*{margin:0;padding:0;box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{font-family:'Chalet',system-ui,sans-serif;color:var(--ink);background:#fff;width:100%;max-width:430px;margin:0 auto;}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important;}}
.offer{height:32px;background:var(--ink);color:#fff;display:flex;align-items:center;justify-content:center;gap:7px;font-size:12px;letter-spacing:.1px;}
.offer b{font-weight:700;color:#FFB9C1;}
header{height:52px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;background:#fff;border-bottom:1px solid #f1e8e9;}
header img.logo{height:17px;display:block;}
header .cart{display:flex;align-items:center;gap:4px;font-size:13px;}
.stars{display:inline-flex;gap:1px;}
.hero{position:relative;overflow:hidden;}
.tag{position:absolute;z-index:3;background:#fff;border-radius:14px;padding:5px 10px 6px;font-size:11px;line-height:1.15;box-shadow:0 6px 16px rgba(120,40,50,.16);white-space:nowrap;}
.tag b{display:block;font-weight:700;font-size:12.5px;}
.stack{padding:14px 16px 0;text-align:center;}
.proof{display:flex;align-items:center;justify-content:center;gap:6px;font-size:12.5px;color:#3a3334;}
.proof u{text-underline-offset:2px;}
h1{font-weight:700;font-size:33px;line-height:1.02;letter-spacing:-.6px;margin-top:8px;}
h1 em{font-family:'GaramondCI',serif;font-style:italic;font-weight:400;font-size:39px;color:var(--red);letter-spacing:-.4px;}
.sub{font-size:14px;line-height:1.35;color:var(--soft);margin:8px auto 0;max-width:330px;}
.cta{margin:14px 0 0;height:52px;width:100%;border:0;border-radius:4px;background:var(--red);color:#fff;font-family:'Chalet',sans-serif;font-weight:700;font-size:15px;letter-spacing:.3px;display:flex;align-items:center;justify-content:center;gap:8px;}
.pills{display:flex;gap:6px;justify-content:center;margin-top:11px;flex-wrap:nowrap;}
.pills span{border:1px solid var(--line);border-radius:999px;padding:6px 10px;font-size:12px;white-space:nowrap;}
.trust{display:flex;justify-content:center;gap:12px;margin-top:11px;font-size:11px;color:var(--soft);}
.trust span{display:flex;align-items:center;gap:4px;white-space:nowrap;}
.sec{padding:30px 16px 0;}
.sec h2{font-weight:700;font-size:22px;letter-spacing:-.3px;display:flex;justify-content:space-between;align-items:baseline;}
.sec h2 em{font-family:'GaramondCI',serif;font-weight:400;font-size:26px;color:var(--red);}
.sec h2 a{font-size:13px;font-weight:400;color:var(--ink);}
.rail{display:flex;gap:10px;overflow:hidden;margin-top:14px;}
.card{flex:0 0 172px;}
.card .ph{height:200px;background:#F4F4F4;border-radius:6px;position:relative;display:flex;align-items:center;justify-content:center;}
.card .ph img{max-width:80%;max-height:84%;object-fit:contain;}
.card .badge{position:absolute;top:8px;left:8px;background:var(--red);color:#fff;font-size:10px;font-weight:700;padding:3px 6px;border-radius:3px;}
.card h3{font-size:14px;font-weight:700;margin-top:8px;}
.card .for{font-size:12px;color:var(--soft);margin-top:2px;}
.card .rv{display:flex;align-items:center;gap:4px;font-size:11.5px;margin-top:5px;}
.card .pr{font-size:14px;font-weight:700;margin-top:4px;}
.card .pr s{color:#9a9192;font-weight:400;margin-left:4px;}
.concern{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px;}
.concern div{background:var(--blush);border-radius:8px;height:118px;padding:12px;position:relative;overflow:hidden;}
.concern b{font-size:15px;display:block;max-width:104px;line-height:1.15;}
.concern small{font-size:11.5px;color:var(--soft);display:block;max-width:96px;margin-top:3px;}
.concern img{position:absolute;right:12px;bottom:10px;height:92px;}
.values{margin:30px 16px 0;padding:20px;background:var(--ink);color:#fff;border-radius:8px;}
.values h2{font-size:21px;line-height:1.15;}
.values h2 em{font-family:'GaramondCI',serif;font-weight:400;font-size:25px;color:#FFB9C1;}
.values li{list-style:none;display:flex;gap:8px;align-items:center;font-size:13px;margin-top:10px;}
footer{padding:30px 16px 40px;font-size:11px;color:#8a8283;text-align:center;}
"""

HEAD = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Topicals | Skincare for flare-ups (CRO rebuild concept by @koolestpro)</title>
<!-- Unofficial concept rebuild by @koolestpro. Topicals is not a client. All facts from the live site, 2026-10-18. -->
<style>__CSS____EXTRA__</style></head><body>
<div class="offer">__GIFT__ Bright Eyes + Slick Lips Kit: <b>$45 value, now $30</b></div>
<header>__MENU__<img class="logo" src="__LOGO__" alt="Topicals"><span class="cart">__BAG__ 0</span></header>
"""

STACK = """<div class="stack">
  <div class="proof">__STARS__ <b>4.9</b> <u>from 882 Faded Serum reviews</u></div>
  <h1>Skincare for flare-ups.<br><em>Made fun.</em></h1>
  <p class="sub">For dark spots, dry patches, dark circles and rough skin. Vegan and cruelty free.</p>
  <button class="cta">Shop best sellers __ARROW__</button>
  <div class="pills"><span>Dark spots</span><span>Dry skin</span><span>Under eyes</span><span>Body</span></div>
  <div class="trust"><span>__TRUCK__ Free shipping $50+</span><span>__FLASK__ Science-backed</span><span>__LEAF__ Vegan</span></div>
</div>"""

# --- hero families -------------------------------------------------------------
HERO_A = """<div class="hero" style="height:318px;background:linear-gradient(180deg,#FDEDEF 0%,#F9D3D8 100%);">
  <div style="position:absolute;left:50%;bottom:22px;transform:translateX(-50%);width:330px;height:26px;border-radius:50%;background:rgba(170,70,85,.16);filter:blur(6px);"></div>
  <img src="__C_DSK__" style="position:absolute;left:226px;top:74px;height:170px;transform:rotate(4deg);">
  <img src="__C_LB__" style="position:absolute;left:62px;top:40px;height:236px;transform:rotate(-7deg);">
  <img src="__C_SL__" style="position:absolute;left:198px;top:96px;height:190px;transform:rotate(5deg);">
  <img src="__C_SER__" style="position:absolute;left:142px;top:30px;height:262px;">
  <img src="__C_EYE__" style="position:absolute;left:12px;top:190px;height:96px;transform:rotate(-12deg);">
  <div class="tag" style="left:10px;top:18px;"><b>Like Butter</b>dry, eczema-prone skin</div>
  <div class="tag" style="left:150px;top:6px;"><b>Faded Serum</b>dark spots</div>
  <div class="tag" style="right:10px;top:40px;"><b>Dark Spot Kit</b>new, save $16</div>
  <div class="tag" style="right:12px;top:244px;"><b>Slather</b>body texture</div>
  <div class="tag" style="left:16px;top:270px;"><b>Eye Masks</b>dark circles</div>
</div>"""

HERO_B = """<div class="hero" style="height:330px;">
  <img src="__P_EYES__" style="position:absolute;left:0;top:-150px;width:390px;height:740px;object-fit:cover;">
  <div class="tag" style="left:14px;top:150px;"><b>Faded Eye Masks</b>dark circles, 4.8 stars</div>
  <div class="tag" style="right:12px;top:262px;"><b>Slick Salve</b>new shades in the $30 kit</div>
</div>"""

HERO_C = """<div class="hero" style="height:612px;background:#4a0d12;">
  <img src="__P_KIT__" style="position:absolute;left:0;top:-40px;width:390px;height:740px;object-fit:cover;">
  __TAG_C__
  <div style="position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(180deg,rgba(40,6,10,0) 0%,rgba(40,6,10,.82) 45%,rgba(30,4,8,.96) 100%);"></div>
  <div class="stack" style="position:absolute;left:0;right:0;bottom:22px;color:#fff;">
    <div class="proof" style="color:#fff">__STARS_W__ <b>4.9</b> <u>from 882 Faded Serum reviews</u></div>
    <h1 style="color:#fff">Skincare for flare-ups.<br><em style="color:#FFB9C1">Made fun.</em></h1>
    <p class="sub" style="color:#f1dcdd">For dark spots, dry patches, dark circles and rough skin. Vegan and cruelty free.</p>
    <button class="cta">Shop best sellers __ARROW__</button>
    <div class="pills"><span style="border-color:rgba(255,255,255,.4)">Dark spots</span><span style="border-color:rgba(255,255,255,.4)">Dry skin</span><span style="border-color:rgba(255,255,255,.4)">Under eyes</span><span style="border-color:rgba(255,255,255,.4)">Body</span></div>
    __TRUST_C__
  </div>
</div>"""

HERO_D_TOP = """<div class="stack" style="padding-top:20px;background:var(--blush);padding-bottom:18px;">
  <h1 style="margin-top:0">Skincare for flare-ups.<br><em>Made fun.</em></h1>
  <p class="sub">For dark spots, dry patches, dark circles and rough skin. Vegan and cruelty free.</p>
  <div class="proof" style="margin-top:9px">__STARS__ <b>4.9</b> <u>from 882 Faded Serum reviews</u></div>
  <button class="cta">Shop best sellers __ARROW__</button>
</div>
<div class="concern" style="padding:12px 16px 0;margin-top:0;">
  <div><b>Dark spots</b><small>Faded Serum</small><img src="__C_SER__"></div>
  <div><b>Dry skin</b><small>Like Butter</small><img src="__C_LB__"></div>
  <div><b>Under eyes</b><small>Eye Masks</small><img src="__C_EYE__" style="height:58px"></div>
  <div><b>Body</b><small>Slather</small><img src="__C_SL__"></div>
</div>"""

BELOW = """
<section class="sec"><h2><span>You make skin <em>look good.</em></span><a href="#">Shop all</a></h2>
  <div class="rail">
    <div class="card"><div class="ph"><span class="badge">SAVE $15</span><img src="__C_KIT__" style="max-width:92%"></div><h3>Bright Eyes &amp; Slick Lips Kit</h3><div class="for">Lip balms + under eye patches</div><div class="rv">__STARS_S__ 5.0 (129)</div><div class="pr">$30<s>$45</s></div></div>
    <div class="card"><div class="ph"><span class="badge">SAVE $16</span><img src="__C_DSK__"></div><h3>Faded Dark Spot Kit</h3><div class="for">Dark spots + uneven texture</div><div class="rv">__STARS_S__ 4.8 (401)</div><div class="pr">$28<s>$44</s></div></div>
    <div class="card"><div class="ph"><img src="__C_LB__"></div><h3>Like Butter Moisturizer</h3><div class="for">Dry, eczema-prone skin</div><div class="rv">__STARS_S__ 4.9 (719)</div><div class="pr">$34</div></div>
  </div>
</section>
<section class="sec"><h2><span>Shop by <em>flare-up</em></span></h2>
  <div class="concern">
    <div><b>Dark spots</b><small>Faded Serum, 4.9 (882)</small><img src="__C_SER__"></div>
    <div><b>Dry, eczema-prone</b><small>Like Butter, 4.9 (719)</small><img src="__C_LB__"></div>
    <div><b>Dark circles</b><small>Eye Masks, 4.8 (721)</small><img src="__C_EYE__" style="height:58px"></div>
    <div><b>Body texture</b><small>Slather, 4.8 (676)</small><img src="__C_SL__"></div>
  </div>
</section>
<div class="values"><h2>A new take on the <em>ointment aisle.</em></h2><ul>
  <li>__FLASK_W__ Science-backed formulas &amp; quality active ingredients</li>
  <li>__SPARK_W__ Skin shade and condition inclusivity</li>
  <li>__LEAF_W__ Vegan &amp; cruelty free products</li></ul></div>
<footer>Unofficial concept rebuild by @koolestpro. Topicals is not a client.<br>All products, prices and ratings from mytopicals.com, Oct 18 2026.</footer>
"""


TRUST_ON = {"c": True}


def fill(html):
    rep = {
        "__CSS__": CSS, "__EXTRA__": "",
        "__F_CH__": uri(A / "fonts" / "Chalet.woff2"), "__F_CHB__": uri(A / "fonts" / "ChaletBold.woff2"),
        "__F_GAR__": uri(A / "fonts" / "GaramondCondIta.woff2"),
        "__LOGO__": uri(A / "logo.png"),
        "__C_SER__": uri(A / "cut_serum_tube.webp"), "__C_LB__": uri(A / "cut_card_lb.webp"),
        "__C_SL__": uri(A / "cut_card_sl.webp"), "__C_EYE__": uri(A / "cut_card_eye.webp"),
        "__C_DSK__": uri(A / "cut_card_dsk.webp"), "__C_KIT__": uri(A / "cut_card_kit.webp"),
        "__P_EYES__": uri(A / "hero_eyes.webp"), "__P_KIT__": uri(A / "kit_life.webp"),
        "__STARS__": stars(12), "__STARS_W__": stars(12, "#fff"), "__STARS_S__": stars(10),
        "__ARROW__": icon("arrow", 17, "#fff"), "__GIFT__": icon("gift", 14, "#FFB9C1"),
        "__MENU__": icon("menu", 22), "__BAG__": icon("bag", 20),
        "__TRUCK__": icon("truck", 13, "#5d5557"), "__FLASK__": icon("flask", 13, "#5d5557"), "__LEAF__": icon("leaf", 13, "#5d5557"),
        "__TRUST_C__": TRUST_C if TRUST_ON["c"] else "", "__TAG_C__": TAG_C if TRUST_ON["c"] else "",
        "__TRUCK_W__": icon("truck", 13, "#f1dcdd"), "__FLASK_W2__": icon("flask", 13, "#f1dcdd"), "__LEAF_W2__": icon("leaf", 13, "#f1dcdd"),
        "__FLASK_W__": icon("flask", 17, "#FFB9C1"), "__SPARK_W__": icon("sparkle", 17, "#FFB9C1"), "__LEAF_W__": icon("leaf", 17, "#FFB9C1"),
    }
    for _ in range(2):
        for k, v in rep.items():
            html = html.replace(k, v)
    # 2026-10-18: images are embedded as WebP at display size (~350KB page instead of 1.9MB)
    # so the file previews in chat and opens anywhere with no outside files.
    return html


TRUST_C = '<div class="trust" style="color:#f1dcdd"><span>__TRUCK_W__ Free shipping $50+</span><span>__FLASK_W2__ Science-backed</span><span>__LEAF_W2__ Vegan</span></div>'
TAG_C = '<div class="tag" style="right:12px;top:118px;"><b>Faded Dark Spot Kit</b>new, $28 (was $44)</div>'


def page(hero_block, stack=True, below=True):
    body = HEAD + hero_block + (STACK if stack else "") + (BELOW if below else "") + "</body></html>"
    return fill(body)


def main():
    if "--variants" in sys.argv:
        VOUT.mkdir(parents=True, exist_ok=True)
        for k, (h, st) in {"v1": (HERO_A, True), "v2": (HERO_B, True), "v3": (HERO_C, False), "v4": (HERO_D_TOP, False)}.items():
            (VOUT / f"{k}.html").write_text(page(h, st, True), encoding="utf-8"); print("wrote", k)
        return
    # Ridwan picked C on 2026-10-18 (full-bleed product + scrim); A is kept as the A/B challenger.
    OUT.write_text(page(HERO_C, False, True), encoding="utf-8"); print("wrote", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
