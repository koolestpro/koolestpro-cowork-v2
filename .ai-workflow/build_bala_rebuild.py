#!/usr/bin/env python3
"""Build the Bala homepage CRO rebuild (the "after" first screen).

Weekly CRO Fix, 2026-10-11. Fallback flow: Claude authors the page directly from
outputs/cro-fixes/bala_bangles-homepage_build-brief.md (no page builder was driven in this
unattended run; see the run summary).

#1 finding (live page, 390x844, 2026-10-11): screen one is a hairline slogan ("FITNESS, BUT
MAKE IT CUTE"), a 10%-off-bundles line and an outline SHOP BUNDLES button. It never says what
Bala sells. Bala Bangles, the product the company is named after (4.9 stars, 1,865 reviews,
$55/$65/$79 a pair), first appears 3,431px down and its rating at 3,894px.

Revision 3 (same day, Ridwan: "do not narrow the hero", research first): first screen is now
variant V1 from references-for-posts/homepage-hero-research-2026-10-11/bala-variants/ (range
flatlay + product labels, centered short stack, one CTA, category pills, press strip).

Revision 2 (same day, Ridwan: "looks like a PDP"): the weight picker, per-pair prices and
"Shop Bala Bangles from $55" buy box are gone from screen one. It now reads as a homepage:
hero that names what the brand sells with one CTA + "Shop all", a shop-by row, and a
best-sellers rail across the range (Bangles, Wavy Roller, Pilates Method, Ab Roller).

This page names the product in Bala's own voice on their own wrist-bangle photo, puts the
4.9 rating, the weight picker with real per-pair prices, ONE filled CTA and a reasons row on
screen one. Every number is from the live page / product JSON on 2026-10-11. Real logo (the
header's inline SVG, rasterized), real fonts (Iskry, Diatype) and real photos from Bala's CDN
are embedded as data URIs.
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "bala" / "_assets"
OUT = ROOT / "outputs" / "cro-fixes" / "bala_bangles-homepage_rebuild.html"


def uri(p: pathlib.Path) -> str:
    mime = {".png": "image/png", ".woff": "font/woff", ".jpg": "image/jpeg"}[p.suffix]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def icon(name: str, size: int = 18, color: str = "currentColor") -> str:
    svg = (A / "icons" / f"ic_{name}.svg").read_text()
    return (svg.replace('width="1em"', f'width="{size}"')
               .replace('height="1em"', f'height="{size}"')
               .replace('fill="currentColor"', f'fill="{color}"')
               .replace("<svg ", '<svg aria-hidden="true" style="display:block;flex-shrink:0" ', 1))


def stars(size: int, color: str) -> str:
    return '<span class="stars">' + "".join(icon("star", size, color) for _ in range(5)) + "</span>"


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bala | Weights &amp; activewear (CRO rebuild concept by @koolestpro)</title>
<!-- Unofficial concept rebuild by @koolestpro. Bala is not a client. All facts from the live site, 2026-10-11. -->
<style>
@font-face{font-family:'Iskry';src:url(__F_ISB__) format('woff');font-weight:700;font-display:block;}
@font-face{font-family:'Iskry';src:url(__F_ISR__) format('woff');font-weight:400;font-display:block;}
@font-face{font-family:'Diatype';src:url(__F_DIA__) format('woff');font-weight:400;font-display:block;}
:root{--ink:#1C1A1B;--blush:#F3E9EA;--pink:#F2C4CB;--rose:#E89AA8;--soft:#6E6467;--line:#E6D8DA;}
*{margin:0;padding:0;box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{font-family:'Diatype',system-ui,sans-serif;color:var(--ink);background:#fff;width:100%;max-width:430px;margin:0 auto;}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important;}}
.offer{height:30px;background:linear-gradient(90deg,#F4C6D0,#FBB8B5);display:flex;align-items:center;justify-content:center;gap:8px;font-size:12px;letter-spacing:.2px;}
.offer b{font-family:'Iskry',sans-serif;font-weight:700;}
header{height:52px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;background:#fff;}
header img{height:27px;display:block;}
header .cart{width:32px;height:32px;border:1.5px solid var(--ink);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;}
.hero{position:relative;height:404px;background:#FBEBEE;overflow:hidden;}
.hero img.kit{position:absolute;left:50%;top:8px;transform:translateX(-50%);width:310px;height:388px;display:block;}
.tag{position:absolute;z-index:2;background:#fff;border-radius:16px;padding:6px 11px;font-size:11.5px;line-height:1.2;box-shadow:0 6px 16px rgba(160,70,90,.16);text-align:center;}
.tag b{display:block;font-family:'Iskry',sans-serif;font-weight:700;font-size:13px;}
.stars{display:inline-flex;gap:1px;}
.stack{padding:14px 16px 0;text-align:center;}
.proofline{display:flex;align-items:center;justify-content:center;gap:6px;font-size:12.5px;color:#3d3739;}
.proofline b{font-family:'Iskry',sans-serif;font-weight:700;color:var(--ink);}
.proofline a{color:#3d3739;}
.stack h1{font-family:'Iskry',sans-serif;font-weight:700;font-size:31px;line-height:1.06;letter-spacing:-.6px;-webkit-text-stroke:.7px currentColor;margin-top:8px;}
.stack h1 span{color:#C9566E;}
.stack .sub{margin-top:8px;font-size:14px;line-height:1.4;color:#3d3739;}
.cta{margin-top:14px;width:100%;height:54px;border-radius:27px;background:var(--ink);color:#fff;border:0;font-family:'Iskry',sans-serif;font-weight:700;font-size:16px;letter-spacing:.8px;text-transform:uppercase;display:flex;align-items:center;justify-content:center;gap:10px;}
.cats{display:flex;justify-content:center;gap:7px;margin-top:14px;}
.cats span{height:32px;padding:0 12px;border:1.5px solid var(--line);border-radius:16px;display:flex;align-items:center;font-size:12.5px;white-space:nowrap;}
.press{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:14px;}
.press .lab{white-space:nowrap;font-size:10.5px;letter-spacing:1.4px;text-transform:uppercase;color:var(--soft);}
.press img{display:block;opacity:.85;}
.rail-h{display:flex;justify-content:space-between;align-items:baseline;padding:14px 16px 0;}
.rail-h b{font-family:'Iskry',sans-serif;font-weight:700;font-size:19px;}
.rail-h a{font-size:13px;color:var(--ink);}
.rail{display:flex;gap:10px;padding:9px 16px 0;overflow:hidden;}
.card{flex:0 0 146px;}
.card .im{position:relative;width:146px;height:166px;border-radius:14px;overflow:hidden;background:#FFF1F1;}
.card .im img{width:100%;height:100%;object-fit:contain;display:block;}
.card .bdg{position:absolute;left:8px;top:8px;background:var(--ink);color:#fff;font-family:'Iskry',sans-serif;font-weight:700;font-size:9.5px;letter-spacing:.8px;border-radius:8px;padding:3px 7px;}
.card .bdg.new{background:#C9566E;}
.card .nm{font-size:13.5px;margin-top:7px;line-height:1.2;}
.card .pr{font-size:13px;margin-top:2px;color:#3d3739;display:flex;align-items:center;gap:5px;}
.card .pr b{font-family:'Diatype',sans-serif;font-weight:400;color:var(--ink);}
.card .pr .st{display:inline-flex;align-items:center;gap:2px;font-size:11.5px;color:var(--soft);}
.strip{display:flex;justify-content:space-between;margin:14px 16px 0;padding-top:10px;border-top:1px solid var(--line);font-size:11.5px;color:#3d3739;}
.strip div{display:flex;align-items:center;gap:5px;}
.strip svg{color:#C9566E;}
section{padding:28px 16px 0;}
h2{font-family:'Iskry',sans-serif;font-weight:700;font-size:26px;line-height:1.05;letter-spacing:-.3px;margin-bottom:12px;}
.uses{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.uses figure{border-radius:14px;overflow:hidden;background:var(--blush);}
.uses img{width:100%;aspect-ratio:4/5;display:block;object-fit:cover;}
.uses figcaption{font-size:13px;padding:8px 10px;}
.quote{background:var(--blush);border-radius:14px;padding:16px;font-size:15px;line-height:1.5;margin-bottom:10px;}
.quote .who{margin-top:8px;font-size:12.5px;color:var(--soft);}
.quote svg{color:#C9566E;margin-bottom:4px;}
.bundle{background:var(--ink);color:#fff;border-radius:16px;padding:18px;display:flex;justify-content:space-between;align-items:center;gap:12px;}
.bundle b{font-family:'Iskry',sans-serif;font-weight:700;font-size:20px;display:block;}
.bundle span{font-size:13px;opacity:.85;}
.bundle a{color:#fff;border:1.5px solid #fff;border-radius:20px;padding:8px 14px;font-size:13px;text-decoration:none;white-space:nowrap;}
footer{margin-top:32px;background:var(--blush);color:#5a5254;font-size:12px;padding:22px 16px 92px;line-height:1.6;}
.sticky{position:fixed;left:50%;transform:translate(-50%,110%);bottom:0;width:100%;max-width:430px;background:#fff;border-top:1px solid var(--line);padding:10px 16px;display:flex;align-items:center;gap:12px;transition:transform .2s;z-index:10;}
.sticky.show{transform:translate(-50%,0);}
.sticky .p{font-family:'Iskry',sans-serif;font-weight:700;font-size:18px;line-height:1;}
.sticky .p small{display:block;font-family:'Diatype',sans-serif;font-weight:400;font-size:11px;color:var(--soft);}
.sticky button{flex:1;height:48px;border-radius:24px;background:var(--ink);color:#fff;border:0;font-family:'Iskry',sans-serif;font-weight:700;font-size:15px;letter-spacing:.6px;}
</style>
</head>
<body>

<div class="offer"><b>Save 10%</b> when you bundle &middot; HSA/FSA eligible</div>
<header>
  <span>__I_MENU__</span>
  <img src="__LOGO__" alt="Bala">
  <span class="cart">0</span>
</header>

<!-- FIRST SCREEN: the range in one picture, then a short centered stack (research: references-for-posts/homepage-hero-research-2026-10-11) -->
<div class="hero">
  <img class="kit" src="__KIT__" alt="Bala Bangles, Bala Bra, Flared Legging and Everyday Sweatshirt in Blush">
  <div class="tag" style="left:12px;top:22px;"><b>Bala Bangles</b>1&ndash;3 lb, wrists or ankles</div>
  <div class="tag" style="right:12px;top:62px;"><b>Bala Bra</b>matching sets</div>
  <div class="tag" style="right:12px;top:262px;"><b>Flared Legging</b></div>
  <div class="tag" style="left:12px;top:318px;"><b>Everyday Sweatshirt</b></div>
</div>
<div class="stack">
  <div class="proofline">__STARS__ <b>4.9</b> <a href="#reviews">from 1,865 Bala Bangles reviews</a></div>
  <h1>Weights &amp; activewear,<br><span>but make it cute.</span></h1>
  <div class="sub">Wearable weights, Pilates props and matching sets.</div>
  <button class="cta" id="main-cta">Shop best sellers __I_ARROW__</button>
  <div class="cats"><span>Weights</span><span>Pilates props</span><span>Activewear</span><span>Bundles</span></div>
  <div class="press"><span class="lab">As seen in</span><img src="__P_WSJ__" style="height:13px" alt="The Wall Street Journal"><img src="__P_GOOP__" style="height:15px" alt="goop"><img src="__P_GLAM__" style="height:13px" alt="Glamour"></div>
</div>

<!-- BELOW THE FOLD -->
<section style="padding-top:22px;"></section>
<div class="rail-h"><b>Best sellers</b><a href="#">See all</a></div>
<div class="rail">
  <div class="card"><div class="im"><img src="__C_BANGLES__" alt="Bala Bangles"><span class="bdg">BEST SELLER</span></div><div class="nm">Bala Bangles</div><div class="pr"><b>from $55</b><span class="st">__STAR1__ 4.9</span></div></div>
  <div class="card"><div class="im"><img src="__C_WAVY__" alt="The Wavy Roller"><span class="bdg new">NEW</span></div><div class="nm">The Wavy Roller</div><div class="pr"><b>$39</b></div></div>
  <div class="card"><div class="im"><img src="__C_PILATES__" alt="The Bala Pilates Method"><span class="bdg new">NEW</span></div><div class="nm">The Bala Pilates Method</div><div class="pr"><b>from $99</b></div></div>
  <div class="card"><div class="im"><img src="__C_AB__" alt="The Ab Roller"><span class="bdg new">NEW</span></div><div class="nm">The Ab Roller</div><div class="pr"><b>$99</b></div></div>
</div>

<div class="strip"><div>__I_PAY__HSA/FSA eligible</div><div>__I_CARD__Klarna &amp; Shop Pay</div><div>__I_PAIR__Bangles sold in pairs</div></div>

<section>
  <h2>Wear them your way</h2>
  <div class="uses">
    <figure><img src="__USE1__" alt="Bala Bangles in their carry case"><figcaption>Pair + carry case</figcaption></figure>
    <figure><img src="__USE2__" alt="Bala apparel and Pilates mat"><figcaption>Walks, Pilates, barre</figcaption></figure>
  </div>
</section>

<section id="reviews">
  <h2>Bala Bangles: 4.9 stars from 1,865 reviews</h2>
  <div class="quote">__I_QUOTE__"I thought they would feel heavy but they don't."<div class="who">Rochell J., verified buyer</div></div>
  <div class="quote">__I_QUOTE__"Adds resistance when walking, using the stairs and during my workout."<div class="who">Megan C., verified buyer</div></div>
</section>

<section id="bundle">
  <div class="bundle"><div><b>Bundle &amp; save 10%</b><span>Pair your Bangles with your favorite Bala props.</span></div><a href="#">Shop bundles</a></div>
</section>

<footer>
  Bala Bangles: steel wrapped in soft silicone, patented design. Adjustable strap fits 5.5"&ndash;11". 1, 2 and 3 lb, sold in pairs. Shipping calculated at checkout.<br><br>
  Concept rebuild by @koolestpro. Not affiliated with Bala.
</footer>

<div class="sticky" id="sticky"><div class="p">Bala<small>weights, props &amp; sets</small></div><button>SHOP BEST SELLERS</button></div>

<script>
// Sticky CTA appears only after the main CTA has scrolled out of view (never on screen one).
(function(){
  var cta=document.getElementById('main-cta'), st=document.getElementById('sticky');
  if(!('IntersectionObserver' in window)) return;
  new IntersectionObserver(function(e){
    st.classList.toggle('show', !e[0].isIntersecting && e[0].boundingClientRect.top<0);
  }).observe(cta);
})();
</script>
</body>
</html>
"""


def main() -> None:
    rep = {
        "__F_ISB__": uri(A / "Iskry-Bold.woff"),
        "__F_ISR__": uri(A / "Iskry-Regular.woff"),
        "__F_DIA__": uri(A / "Diatype-Regular.woff"),
        "__LOGO__": uri(A / "logo.png"),
        "__HERO__": uri(A / "hero_wrist.jpg"),
        "__USE1__": uri(A / "case_blush.jpg"),
        "__USE2__": uri(A / "lifestyle_mat.jpg"),
        "__I_MENU__": icon("menu", 28, "#1C1A1B"),
        "__I_PAIR__": icon("package-variant-closed", 15),
        "__I_CARD__": icon("credit-card-check-outline", 15),
        "__I_ARROW__": icon("arrow-right", 18, "#fff"),
        "__I_WEIGHT__": icon("weight-pound", 15),
        "__I_YOGA__": icon("yoga", 15),
        "__I_TAG__": icon("tag-outline", 15),
        "__STAR1__": icon("star", 12, "#1C1A1B"),
        "__C_BANGLES__": uri(A / "bangles_render.jpg"),
        "__C_WAVY__": uri(A / "card_wavy.jpg"),
        "__C_PILATES__": uri(A / "card_pilates.jpg"),
        "__C_AB__": uri(A / "card_abroller.jpg"),
                "__I_PAY__": icon("hospital-box-outline", 15),
        "__I_QUOTE__": icon("format-quote-open", 24),
        "__STARS__": stars(12, "#1C1A1B"),
        "__KIT__": uri(A / "kit_studio_street.jpg"),
        "__P_WSJ__": uri(A / "press_wsj.png"),
        "__P_GOOP__": uri(A / "press_goop.png"),
        "__P_GLAM__": uri(A / "press_glamour.png"),
    }
    html = HTML
    for k, v in rep.items():
        html = html.replace(k, v)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars)")


if __name__ == "__main__":
    main()
