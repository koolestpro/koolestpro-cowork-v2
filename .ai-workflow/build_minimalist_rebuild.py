#!/usr/bin/env python3
"""Build the Minimalist Niacinamide 10% Face Serum CRO rebuild (the "after" page).

Weekly CRO Fix, 2026-09-27. Fallback flow (Claude authors the page directly from
outputs/cro-fixes/minimalist_niacinamide-10-serum-pdp_build-brief.md) because no page
builder credits were usable this run (see the facts file's "builder" note).

The #1 finding: on a 390x844 phone the first screen is only the product photo. The
name starts at y=813, price at y=1576, Add to Cart at y=1870. This page puts the whole
decision on the first screen: outcome headline + name on a hero that blends with the
real studio photo, real rating (3.9, 1,480 reviews), price with MRP, benefit chips,
size pills, ONE Add to Cart, and a trust row under it.

Every number is from the live page / policies on 2026-09-27. Real logo PNG and real
Proxima Nova webfont files from the brand's own CDN are embedded as data URIs.
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "minimalist" / "_assets"
OUT = ROOT / "outputs" / "cro-fixes" / "minimalist_niacinamide-10-serum-pdp_rebuild.html"


def uri(p: pathlib.Path) -> str:
    mime = {".png": "image/png", ".woff2": "font/woff2", ".jpg": "image/jpeg"}[p.suffix]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def icon(name: str, size: int = 18, color: str = "currentColor") -> str:
    svg = (A / "icons" / f"ic_{name}.svg").read_text()
    return (svg.replace('width="1em"', f'width="{size}"')
               .replace('height="1em"', f'height="{size}"')
               .replace('fill="currentColor"', f'fill="{color}"')
               .replace("<svg ", '<svg aria-hidden="true" style="display:block;flex-shrink:0" ', 1))


def stars(size: int, pct: float) -> str:
    row = "".join(icon("star", size) for _ in range(5))
    return (f'<span class="stars" style="width:{size*5}px;height:{size}px">'
            f'<span class="s-off">{row}</span>'
            f'<span class="s-on" style="width:{pct:.0f}%">{row}</span></span>')


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Niacinamide 10% Face Serum | Minimalist (CRO rebuild concept by @koolestpro)</title>
<!-- Unofficial concept rebuild by @koolestpro. Minimalist is not a client. All facts from the live page, 2026-09-27. -->
<style>
@font-face{font-family:'PN';src:url(__FONT_R__) format('woff2');font-weight:400;font-display:block;}
@font-face{font-family:'PN';src:url(__FONT_B__) format('woff2');font-weight:700;font-display:block;}
:root{--ink:#111;--muted:#5d6468;--line:#e3e6e8;--plinth:#E5E9EA;--orange:#FB6900;--gold:#1a1a1a;}
*{margin:0;padding:0;box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{font-family:'PN','Helvetica Neue',Arial,sans-serif;color:var(--ink);background:#fff;width:100%;max-width:430px;margin:0 auto;}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important;}}
.offer{height:30px;background:var(--orange);color:#fff;font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:6px;letter-spacing:.2px;}
.offer code{font-family:inherit;font-weight:400;opacity:.92;}
header{height:50px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;border-bottom:1px solid var(--line);}
header .l,header .r{display:flex;gap:14px;align-items:center;width:64px;}
header .r{justify-content:flex-end;}
header img{height:20px;display:block;}
.hero{position:relative;background:var(--plinth);height:352px;overflow:hidden;}
.hero .shot{position:absolute;right:-6px;bottom:-6px;height:360px;width:auto;display:block;}
.hero .txt{position:absolute;left:16px;top:18px;width:200px;z-index:2;}
.pill{display:inline-flex;align-items:center;height:22px;padding:0 9px;border-radius:11px;background:#111;color:#fff;font-size:11px;font-weight:700;letter-spacing:.4px;}
.hero h1{font-size:31px;line-height:1.04;font-weight:700;letter-spacing:-.6px;margin-top:12px;}
.hero .name{margin-top:12px;font-size:15px;font-weight:700;line-height:1.25;}
.hero .sub{font-size:13px;color:var(--muted);line-height:1.35;margin-top:4px;max-width:190px;}
.hero .usage{position:absolute;left:16px;bottom:16px;display:flex;gap:6px;z-index:2;}
.tag{display:inline-flex;align-items:center;gap:5px;height:26px;padding:0 10px;border-radius:13px;background:rgba(255,255,255,.78);font-size:12px;font-weight:700;color:#222;}
.buy{padding:12px 16px 0;}
.row1{display:flex;align-items:center;justify-content:space-between;}
.rating{display:flex;align-items:center;gap:7px;font-size:14px;}
.rating b{font-weight:700;}
.rating a{color:var(--ink);text-decoration:underline;text-underline-offset:2px;}
.stars{position:relative;display:inline-block;}
.stars .s-off,.stars .s-on{position:absolute;left:0;top:0;display:flex;white-space:nowrap;overflow:hidden;height:100%;}
.stars .s-off{color:#d5d9dc;width:100%;}
.stars .s-on{color:#111;}
.stock{font-size:12px;color:#1c7c43;font-weight:700;display:flex;align-items:center;gap:5px;}
.stock i{width:7px;height:7px;border-radius:50%;background:#1fa35a;display:inline-block;}
.price{display:flex;align-items:baseline;gap:9px;margin-top:9px;}
.price .now{font-size:30px;font-weight:700;letter-spacing:-.5px;}
.price .mrp{font-size:15px;color:var(--muted);}
.price .mrp s{text-decoration-thickness:1px;}
.price .off{font-size:12px;font-weight:700;background:#E8F6EE;color:#1c7c43;border-radius:5px;padding:3px 7px;align-self:center;}
.price .tax{font-size:11px;color:var(--muted);margin-left:auto;align-self:center;}
.chips{display:grid;grid-template-columns:1fr 1fr;gap:6px 10px;margin-top:11px;}
.chip{display:flex;align-items:center;gap:6px;font-size:13px;color:#222;}
.chip svg{color:#1c7c43;}
.sizes{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:13px;}
.size{border:1.5px solid var(--line);border-radius:10px;height:46px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:14px;font-weight:700;line-height:1.1;}
.size span{font-size:11px;font-weight:400;color:var(--muted);margin-top:2px;}
.size.on{border-color:#111;background:#111;color:#fff;}
.size.on span{color:#cfd3d5;}
.cta{margin-top:12px;height:54px;border-radius:12px;background:#111;color:#fff;border:0;width:100%;font:700 17px 'PN',Arial,sans-serif;display:flex;align-items:center;justify-content:center;gap:10px;letter-spacing:.2px;}
.cta .sep{width:1px;height:18px;background:rgba(255,255,255,.35);}
.trust{display:grid;grid-template-columns:repeat(3,1fr);margin-top:10px;border-top:1px solid var(--line);padding-top:10px;}
.trust div{word-spacing:3px;display:flex;flex-direction:column;align-items:center;text-align:center;font-size:11.5px;line-height:1.25;color:#333;gap:4px;}
.trust div+div{border-left:1px solid var(--line);}
/* below the fold */
section{padding:28px 16px 0;}
h2{font-size:20px;font-weight:700;letter-spacing:-.3px;margin-bottom:12px;}
.quote{background:#F6F7F8;border-radius:14px;padding:16px;font-size:15px;line-height:1.5;}
.quote .who{margin-top:10px;font-size:13px;color:var(--muted);display:flex;align-items:center;gap:8px;}
.offers{display:flex;gap:10px;overflow:hidden;}
.ocard{flex:0 0 72%;border:1.5px dashed #c9ced1;border-radius:12px;padding:12px 14px;}
.ocard b{display:block;font-size:13px;letter-spacing:.6px;}
.ocard p{font-size:14px;margin-top:4px;line-height:1.35;}
.ing{display:grid;gap:10px;}
.ing div{border:1px solid var(--line);border-radius:12px;padding:12px 14px;}
.ing b{font-size:15px;}
.ing p{font-size:14px;color:#333;margin-top:3px;line-height:1.4;}
.use{display:flex;gap:10px;}
.use div{flex:1;border:1px solid var(--line);border-radius:12px;padding:12px;display:flex;align-items:center;gap:10px;font-size:14px;}
.dist{display:grid;gap:6px;margin-top:12px;}
.dist div{display:grid;grid-template-columns:20px 1fr 40px;align-items:center;gap:8px;font-size:13px;}
.bar{height:7px;border-radius:4px;background:#eceff1;position:relative;overflow:hidden;}
.bar i{position:absolute;left:0;top:0;bottom:0;background:#111;border-radius:4px;}
.acc{border-top:1px solid var(--line);}
.acc div{display:flex;justify-content:space-between;align-items:center;height:52px;border-bottom:1px solid var(--line);font-size:15px;font-weight:700;}
footer{margin-top:32px;background:#111;color:#bfc4c7;font-size:12px;padding:22px 16px 90px;line-height:1.6;}
.sticky{position:fixed;left:50%;transform:translate(-50%,110%);bottom:0;width:100%;max-width:430px;background:#fff;border-top:1px solid var(--line);padding:10px 16px;display:flex;align-items:center;gap:12px;transition:transform .2s;z-index:10;}
.sticky.show{transform:translate(-50%,0);}
.sticky .p{font-size:17px;font-weight:700;}
.sticky .p small{display:block;font-size:11px;font-weight:400;color:var(--muted);}
.sticky button{flex:1;height:46px;border-radius:10px;background:#111;color:#fff;border:0;font:700 15px 'PN',Arial,sans-serif;}
</style>
</head>
<body>

<div class="offer">Buy 2, Get 3rd Free <code>&middot; B2G3RDFREE</code></div>
<header>
  <div class="l">__I_MENU__ __I_SEARCH__</div>
  <img src="__LOGO__" alt="Minimalist">
  <div class="r">__I_HEART__ __I_CART__</div>
</header>

<!-- FIRST SCREEN: the whole decision -->
<div class="hero">
  <img class="shot" src="__HERO__" alt="Minimalist Niacinamide 10% Face Serum, 30ml bottle">
  <div class="txt">
    <span class="pill">BEST SELLER</span>
    <h1>Control oil.<br>Refine pores.<br>Even out tone.</h1>
    <div class="name">Niacinamide 10%<br>Face Serum</div>
    <div class="sub">with Matmarine + Zinc, for oily and acne-prone skin</div>
  </div>
  <div class="usage"><span class="tag">__I_SUN__ AM</span><span class="tag">__I_NIGHT__ PM</span><span class="tag">Everyday</span></div>
</div>

<div class="buy">
  <div class="row1">
    <div class="rating">__STARS__ <b>3.9</b> <a href="#reviews">1,480 reviews</a></div>
    <div class="stock"><i></i>In stock</div>
  </div>
  <div class="price"><span class="now">&#8377;539</span><span class="mrp">MRP <s>&#8377;599</s></span><span class="off">10% OFF</span><span class="tax">incl. all taxes</span></div>
  <div class="chips">
    <div class="chip">__I_CHECK__ Fragrance free</div>
    <div class="chip">__I_CHECK__ Non-comedogenic</div>
    <div class="chip">__I_CHECK__ Pregnancy-safe</div>
    <div class="chip">__I_CHECK__ Derm patch-tested</div>
  </div>
  <div class="sizes">
    <div class="size">10ml<span>&#8377;237</span></div>
    <div class="size">20ml<span>&#8377;499</span></div>
    <div class="size on">30ml<span>&#8377;539</span></div>
    <div class="size">60ml<span>&#8377;899</span></div>
  </div>
  <button class="cta" id="main-cta">__I_CART_W__ Add to Cart <span class="sep"></span> &#8377;539</button>
  <div class="trust">
    <div>__I_TRUCK__Ships in<br>48 hours</div>
    <div>__I_CASH__Cash on<br>Delivery</div>
    <div>__I_BOX__7-day<br>replacement</div>
  </div>
</div>

<!-- BELOW THE FOLD -->
<section>
  <div class="quote">
    <div style="color:#b9bfc2">__I_QUOTE__</div>
    "I've been using it for past 3-4 months. I'm on my 2nd bottle. I had uneven skin tone, acne scar marks and now it's almost gone."
    <div class="who">Charu S., quoted on the product page</div>
  </div>
</section>

<section>
  <h2>Offers on this serum</h2>
  <div class="offers">
    <div class="ocard"><b>B2G3RDFREE</b><p>Buy 2, get the 3rd product free</p></div>
    <div class="ocard"><b>ATC10</b><p>Extra 10% off on orders above &#8377;599</p></div>
  </div>
</section>

<section>
  <h2>What makes it work</h2>
  <div class="ing">
    <div><b>Niacinamide 10% (Vitamin B3)</b><p>Reduces the skin's sebum level, improves the barrier and evens skin tone.</p></div>
    <div><b>Matmarine</b><p>A marine biotech extract that helps regulate oiliness and reduces sebum and the look of pores.</p></div>
    <div><b>Zinc</b><p>Balances sebum activity and reduces inflammation, with no sticky residue.</p></div>
  </div>
</section>

<section>
  <h2>Is it right for me?</h2>
  <div class="ing">
    <div><b>Made for</b><p>Acne marks, acne-prone and oily skin. Age 16+.</p></div>
    <div><b>Pregnancy and lactation</b><p>Safe, per Minimalist's product page.</p></div>
    <div><b>Tested</b><p>Evaluated for safety through patch testing under a dermatologist's supervision. Fragrance free, essential oil free, non-comedogenic, pH 5.5 - 6.5.</p></div>
  </div>
</section>

<section>
  <h2>How to use</h2>
  <div class="use"><div>__I_SUN__ Morning</div><div>__I_NIGHT__ Night</div></div>
  <p style="font-size:14px;color:#333;margin-top:10px;line-height:1.45">Apply 2-3 drops after cleansing and toning. Let it absorb fully before the next step. Every day, AM and PM.</p>
</section>

<section id="reviews">
  <h2>Customer reviews</h2>
  <div class="rating" style="font-size:15px">__STARS__ <b>3.9</b>&nbsp;based on 1,480 reviews</div>
  <div class="dist">
    <div>5<span class="bar"><i style="width:55.5%"></i></span><span>822</span></div>
    <div>4<span class="bar"><i style="width:15.7%"></i></span><span>232</span></div>
    <div>3<span class="bar"><i style="width:9.9%"></i></span><span>147</span></div>
    <div>2<span class="bar"><i style="width:5.8%"></i></span><span>86</span></div>
    <div>1<span class="bar"><i style="width:13%"></i></span><span>193</span></div>
  </div>
</section>

<section>
  <div class="acc">
    <div>Full ingredient list __I_CHEV__</div>
    <div>Shipping &amp; returns __I_CHEV__</div>
  </div>
</section>

<footer>
  Ships within 48 working hours. Delivery in 2 to 10 days (about 3 days in Delhi, Mumbai, Kolkata and Bangalore). Cash on Delivery adds &#8377;70. Replacement for damaged, wrong or expired products within 7 days of delivery.<br><br>
  Concept rebuild by @koolestpro. Not affiliated with Minimalist.
</footer>

<div class="sticky" id="sticky"><div class="p">&#8377;539<small>30ml</small></div><button>Add to Cart</button></div>

<script>
// Sticky ATC appears only after the main CTA has scrolled out of view (never in the first viewport).
(function(){
  var cta=document.getElementById('main-cta'), st=document.getElementById('sticky');
  if(!('IntersectionObserver' in window)) return;
  new IntersectionObserver(function(e){
    var past=!e[0].isIntersecting && e[0].boundingClientRect.top<0;
    st.classList.toggle('show',past);
  }).observe(cta);
})();
</script>
</body>
</html>
"""


def main() -> None:
    rep = {
        "__FONT_R__": uri(A / "ProximaNovaA-Regular.woff2"),
        "__FONT_B__": uri(A / "ProximaNovaA-Bold.woff2"),
        "__LOGO__": uri(A / "logo.png"),
        "__HERO__": uri(A / "hero_plinth.png"),
        "__I_MENU__": icon("menu", 24),
        "__I_SEARCH__": icon("magnify", 22),
        "__I_HEART__": icon("heart-outline", 22),
        "__I_CART__": icon("cart-outline", 23),
        "__I_CART_W__": icon("cart-outline", 20, "#fff"),
        "__I_SUN__": icon("weather-sunny", 16),
        "__I_NIGHT__": icon("weather-night", 15),
        "__I_CHECK__": icon("check-circle-outline", 16, "#1c7c43"),
        "__I_TRUCK__": icon("truck-fast-outline", 22),
        "__I_CASH__": icon("cash", 22),
        "__I_BOX__": icon("package-variant-closed-check", 22),
        "__I_QUOTE__": icon("format-quote-open", 26),
        "__I_CHEV__": icon("chevron-down", 22),
        "__STARS__": stars(16, 3.9 / 5 * 100),
    }
    html = HTML
    for k, v in rep.items():
        html = html.replace(k, v)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({len(html):,} chars)")


if __name__ == "__main__":
    main()
