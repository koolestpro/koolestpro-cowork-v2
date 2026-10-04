#!/usr/bin/env python3
"""Build the Fly By Jing Original Sichuan Chili Crisp CRO rebuild (the "after" page).

Weekly CRO Fix, 2026-10-04. Fallback flow: Claude authors the page directly from
outputs/cro-fixes/flybyjing_chili-crisp-pdp_build-brief.md (no page builder was driven
in this unattended run; see the run summary).

#1 finding (live page, 390x844, 2026-10-04): screen one is the jar, the product name,
bare stars and a 50-word paragraph. The pack picker starts at y=1017, the price ($30,
which is the default 2-pack, never shown per jar) at y=1146 and Add to Cart at
y=1357. The 4.9 rating number sits about 5,750px down. On first load a full-screen
"UNLOCK 20% OFF" quiz covers the page.

This page puts the decision on screen one: an outcome headline on the real lifestyle
photo, the heat level in the brand's own words, 4.9 stars + 2,459 reviews + 97% would
recommend, a pack picker that shows the per-jar price, ONE Add to Cart and a shipping
row under it. Every number is from the live page / product JSON on 2026-10-04. Real
logo (rasterized from the brand's own SVG), real fonts (JeanLuc, Publico) and real
product photos from the brand's CDN are embedded as data URIs.
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "flybyjing" / "_assets"
OUT = ROOT / "outputs" / "cro-fixes" / "flybyjing_chili-crisp-pdp_rebuild.html"


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
<title>Original Sichuan Chili Crisp | Fly By Jing (CRO rebuild concept by @koolestpro)</title>
<!-- Unofficial concept rebuild by @koolestpro. Fly By Jing is not a client. All facts from the live page, 2026-10-04. -->
<style>
@font-face{font-family:'JL';src:url(__F_JL__) format('woff');font-weight:400;font-display:block;}
@font-face{font-family:'PB';src:url(__F_PR__) format('woff');font-weight:400;font-display:block;}
@font-face{font-family:'PB';src:url(__F_PM__) format('woff');font-weight:700;font-display:block;}
:root{--red:#AB2328;--deep:#7E1A1D;--yellow:#FFF000;--ink:#111;--cream:#FFF6E8;}
*{margin:0;padding:0;box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{font-family:'PB',Georgia,serif;color:#fff;background:var(--red);width:100%;max-width:430px;margin:0 auto;}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important;}}
.jl{font-family:'JL','Arial Narrow',sans-serif;text-transform:uppercase;letter-spacing:.3px;}
.offer{height:30px;background:#000;color:var(--yellow);font-size:12px;display:flex;align-items:center;justify-content:center;gap:8px;}
.offer b{font-family:'JL',sans-serif;font-weight:400;font-size:14px;letter-spacing:.4px;}
header{height:52px;display:flex;align-items:center;justify-content:space-between;padding:0 14px;background:var(--red);}
header img{height:22px;display:block;}
header .cart{background:#fff;color:#000;border-radius:16px;height:30px;padding:0 13px;display:flex;align-items:center;font-family:'JL',sans-serif;font-size:15px;}
.hero{position:relative;height:308px;overflow:hidden;background:linear-gradient(180deg,#D3061F 0%,#E2361A 45%,#F25200 100%);}
.hero .shot{position:absolute;right:-58px;top:-12px;width:324px;height:324px;display:block;}
.hero .fade{position:absolute;left:0;top:0;bottom:0;width:205px;background:linear-gradient(90deg,rgba(211,6,31,.92) 0%,rgba(214,20,28,.78) 62%,rgba(214,20,28,0) 100%);}
.hero .txt{position:absolute;left:16px;top:16px;width:196px;z-index:2;}
.pill{display:inline-flex;align-items:center;height:22px;padding:0 9px;border-radius:11px;background:var(--yellow);color:#000;font-family:'JL',sans-serif;font-size:13px;letter-spacing:.5px;}
.hero h1{font-family:'JL',sans-serif;font-weight:400;font-size:40px;line-height:.92;margin-top:11px;text-transform:uppercase;letter-spacing:.2px;text-shadow:0 2px 10px rgba(80,0,0,.25);}
.hero h1 span{color:var(--yellow);}
.hero .name{margin-top:12px;font-size:15px;font-weight:700;line-height:1.2;}
.hero .sub{font-size:12.5px;line-height:1.35;margin-top:3px;opacity:.95;}
.heat{position:absolute;left:16px;bottom:14px;z-index:2;display:flex;align-items:center;gap:7px;background:rgba(0,0,0,.72);border-radius:14px;padding:6px 11px 6px 8px;font-size:12.5px;line-height:1.2;max-width:250px;}
.heat svg{color:var(--yellow);}
.buy{padding:12px 16px 0;}
.row1{display:flex;align-items:center;gap:8px;font-size:14px;flex-wrap:nowrap;}
.stars{display:inline-flex;gap:1px;}
.row1 b{font-weight:700;}
.row1 a{color:#fff;text-decoration:underline;text-underline-offset:2px;}
.row1 .rec{margin-left:auto;font-size:12px;background:rgba(0,0,0,.25);border-radius:10px;padding:3px 8px;white-space:nowrap;}
.packs-h{display:flex;justify-content:space-between;align-items:baseline;margin-top:13px;font-size:13px;}
.packs-h span{opacity:.85;}
.packs{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:7px;}
.pk{border:1.5px solid rgba(255,255,255,.75);border-radius:12px;height:62px;display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.1;}
.pk .q{font-family:'JL',sans-serif;font-size:17px;}
.pk .p{font-size:13px;font-weight:700;margin-top:2px;}
.pk .e{font-size:10.5px;opacity:.9;margin-top:2px;}
.pk.on{background:#fff;color:#000;border-color:#fff;}
.price{display:flex;align-items:center;gap:10px;margin-top:12px;}
.price .now{font-family:'JL',sans-serif;font-size:38px;line-height:1;}
.price .what{font-size:13px;line-height:1.25;}
.price .club{margin-left:auto;border:1.5px dashed var(--yellow);color:var(--yellow);border-radius:10px;padding:5px 9px;font-size:11.5px;line-height:1.25;text-align:right;}
.price .club b{font-size:14px;}
.cta{margin-top:11px;height:56px;border-radius:28px;background:var(--yellow);color:#000;border:0;width:100%;font-family:'JL',sans-serif;font-size:22px;letter-spacing:.4px;display:flex;align-items:center;justify-content:center;gap:12px;}
.cta .sep{width:2px;height:20px;background:rgba(0,0,0,.35);}
.trust{display:grid;grid-template-columns:repeat(3,1fr);margin-top:12px;border-top:1px solid rgba(255,255,255,.28);padding-top:10px;}
.trust div{display:flex;flex-direction:column;align-items:center;text-align:center;font-size:11.5px;line-height:1.25;gap:4px;}
.trust div+div{border-left:1px solid rgba(255,255,255,.28);}
.trust svg{color:var(--yellow);}
section{padding:30px 16px 0;}
h2 .num{font-family:'PB',serif;font-weight:700;font-size:25px;text-transform:none;}
h2{font-family:'JL',sans-serif;font-weight:400;font-size:28px;line-height:1;text-transform:uppercase;margin-bottom:12px;}
.uses{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.uses figure{border-radius:14px;overflow:hidden;background:var(--deep);}
.uses img{width:100%;aspect-ratio:1/1;display:block;object-fit:cover;}
.uses figcaption{font-size:13px;padding:8px 10px;}
.quote{background:var(--deep);border-radius:14px;padding:16px;font-size:15px;line-height:1.5;margin-bottom:10px;}
.quote .who{margin-top:8px;font-size:12.5px;opacity:.85;}
.quote svg{color:var(--yellow);margin-bottom:4px;}
.ing{display:grid;gap:10px;}
.ing div{border:1px solid rgba(255,255,255,.3);border-radius:12px;padding:12px 14px;}
.ing b{font-family:'JL',sans-serif;font-weight:400;font-size:18px;letter-spacing:.3px;}
.ing p{font-size:14px;margin-top:3px;line-height:1.4;opacity:.95;}
.acc div{display:flex;justify-content:space-between;align-items:center;height:52px;border-bottom:1px solid rgba(255,255,255,.28);font-family:'JL',sans-serif;font-size:18px;}
footer{margin-top:32px;background:#000;color:#cfcfcf;font-size:12px;padding:22px 16px 92px;line-height:1.6;}
.sticky{position:fixed;left:50%;transform:translate(-50%,110%);bottom:0;width:100%;max-width:430px;background:var(--deep);padding:10px 16px;display:flex;align-items:center;gap:12px;transition:transform .2s;z-index:10;}
.sticky.show{transform:translate(-50%,0);}
.sticky .p{font-family:'JL',sans-serif;font-size:22px;line-height:1;}
.sticky .p small{display:block;font-family:'PB',serif;font-size:11px;opacity:.85;}
.sticky button{flex:1;height:48px;border-radius:24px;background:var(--yellow);color:#000;border:0;font-family:'JL',sans-serif;font-size:19px;}
</style>
</head>
<body>

<div class="offer"><b>FREE SHIPPING OVER $75</b>&middot; club members save 20%</div>
<header>
  <span>__I_MENU__</span>
  <img src="__LOGO__" alt="Fly By Jing">
  <span class="cart">CART</span>
</header>

<!-- FIRST SCREEN: the whole decision -->
<div class="hero">
  <img class="shot" src="__HERO__" alt="A jar of Original Sichuan Chili Crisp with a spoonful lifted out">
  <div class="fade"></div>
  <div class="txt">
    <span class="pill">#1 BEST SELLER</span>
    <h1>Crunchy.<br>Numbing.<br><span>Goes on<br>everything.</span></h1>
    <div class="name">Original Sichuan Chili Crisp</div>
    <div class="sub">6oz jars &middot; vegan &middot; sugar free</div>
  </div>
  <div class="heat">__I_CHILI__ <span><b>Heat:</b> intensely flavorful, not off-the-charts spicy</span></div>
</div>

<div class="buy">
  <div class="row1">__STARS__ <b>4.9</b> <a href="#reviews">2,459 reviews</a><span class="rec">97% recommend</span></div>
  <div class="packs-h"><b>Pick your pack</b><span>6oz jars</span></div>
  <div class="packs">
    <div class="pk on"><span class="q">2 jars</span><span class="p">$30</span><span class="e">$15 / jar</span></div>
    <div class="pk"><span class="q">3 jars</span><span class="p">$42.75</span><span class="e">$14.25 / jar</span></div>
    <div class="pk"><span class="q">4 jars</span><span class="p">$54</span><span class="e">$13.50 / jar</span></div>
    <div class="pk"><span class="q">16oz</span><span class="p">$32</span><span class="e">1 big jar</span></div>
  </div>
  <div class="price"><span class="now">$30</span><span class="what">for 2 jars<br>$15 a jar</span><span class="club">Club members<br><b>$24</b> (save 20%)</span></div>
  <button class="cta" id="main-cta">ADD 2 JARS TO CART <span class="sep"></span> $30</button>
  <div class="trust">
    <div>__I_CLOCK__Ships in<br>48-72 hours</div>
    <div>__I_TRUCK__Free shipping<br>over $75</div>
    <div>__I_LEAF__No artificial flavors<br>or preservatives</div>
  </div>
</div>

<!-- BELOW THE FOLD -->
<section>
  <h2>Use it on everything. Yes, even that.</h2>
  <div class="uses">
    <figure><img src="__USE1__" alt="Pizza slice with chili crisp"><figcaption>Pizza</figcaption></figure>
    <figure><img src="__USE2__" alt="Salmon rice bowl with chili crisp"><figcaption>Rice bowls</figcaption></figure>
  </div>
</section>

<section id="reviews">
  <h2>Rated <span class="num">4.9</span> by <span class="num">2,459</span> reviewers</h2>
  <div class="quote">__I_QUOTE__"I put it on everything because it enhances everything."<div class="who">Christina R., verified buyer</div></div>
  <div class="quote">__I_QUOTE__"Good on all types of food. If you haven't tried it you're missing something!"<div class="who">Joyce H., verified buyer</div></div>
</section>

<section>
  <h2>What we're made of</h2>
  <div class="ing">
    <div><b>Erjingtiao chili</b><p>Fragrant and flavorful, a staple in Sichuan cuisine. Grown in Guizhou.</p></div>
    <div><b>Tribute pepper</b><p>The rarest Sichuan peppercorn, hand-harvested in the Qingxi mountains once a year. Brings the tongue-tingling spice.</p></div>
    <div><b>Sichuan caiziyou</b><p>Cold-pressed, non-GMO rapeseed oil with an amber hue and a nutty flavor.</p></div>
  </div>
</section>

<section>
  <div class="acc">
    <div>Ingredients __I_CHEV__</div>
    <div>Nutrition facts __I_CHEV__</div>
    <div>Shipping __I_CHEV__</div>
  </div>
</section>

<footer>
  Orders ship from a fulfillment partner within 48 to 72 hours via DHL/USPS, FedEx or UPS. Standard transit is 3-7 business days depending on your region. Contains soy and sesame.<br><br>
  Concept rebuild by @koolestpro. Not affiliated with Fly By Jing.
</footer>

<div class="sticky" id="sticky"><div class="p">$30<small>2 jars</small></div><button>ADD TO CART</button></div>

<script>
// Sticky ATC appears only after the main CTA has scrolled out of view (never on screen one).
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
        "__F_JL__": uri(A / "JeanLuc.woff"),
        "__F_PR__": uri(A / "PublicoRoman.woff"),
        "__F_PM__": uri(A / "PublicoMedium.woff"),
        "__LOGO__": uri(A / "logo.png"),
        "__HERO__": uri(A / "hero_photo.jpg"),
        "__USE1__": uri(A / "lifestyle-2.jpg"),
        "__USE2__": uri(A / "lifestyle-3.jpg"),
        "__I_MENU__": icon("menu", 28, "#fff"),
        "__I_CHILI__": icon("fire", 18),
        "__I_CLOCK__": icon("clock-fast", 22),
        "__I_TRUCK__": icon("truck-fast-outline", 22),
        "__I_LEAF__": icon("leaf", 21),
        "__I_QUOTE__": icon("format-quote-open", 24),
        "__I_CHEV__": icon("chevron-down", 24, "#fff"),
        "__STARS__": stars(15, "#FFF000"),
    }
    html = HTML
    for k, v in rep.items():
        html = html.replace(k, v)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars)")


if __name__ == "__main__":
    main()
