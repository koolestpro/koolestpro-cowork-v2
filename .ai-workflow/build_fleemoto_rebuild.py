#!/usr/bin/env python3
"""Build the FleeMoto supermoto wheel set PRODUCT PAGE (PDP) CRO rebuild + 4 hero variants (2026-11-01).

Weekly CRO Fix, unattended run. Fallback flow: Claude authors the page from
outputs/cro-fixes/fleemoto_supermoto-wheels-pdp_build-brief.md (no page builder driven unattended).
#1 finding (live page, 390x844): price at y=903 and Add to cart at y=895, below the 844px screen;
the fit list ("compatibility") at y=1093 under the buy buttons; the 2-week pre-order note under the
buttons too. Facts: outputs/cro-fixes/fleemoto_supermoto-wheels-pdp_facts.json. No reviews, ratings,
warranty or shipping promises are shown because the store shows none.
Logo: the live header is text only ("FleeMoto", Inter 600), carried over as-is (no logo file exists).

Usage: python3 build_fleemoto_rebuild.py             -> full page (variant A)
       python3 build_fleemoto_rebuild.py --variants  -> 4 first-screen variants in fleemoto/_variants/
"""
import base64, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs/cro-fixes/fleemoto/_assets"
OUT = ROOT / "outputs/cro-fixes/fleemoto_supermoto-wheels-pdp_rebuild.html"
VOUT = ROOT / "outputs/cro-fixes/fleemoto/_variants"
CONTACT = "https://fleemoto.shop/pages/contact"

def uri(p):
    p = pathlib.Path(p)
    mime = {".png": "image/png", ".woff2": "font/woff2", ".jpg": "image/jpeg", ".webp": "image/webp"}[p.suffix]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

def ic(name, size=18, color="currentColor"):
    s = (A / "icons" / f"ic_{name}.svg").read_text()
    s = s.replace('width="1em"', f'width="{size}"').replace('height="1em"', f'height="{size}"').replace('fill="currentColor"', f'fill="{color}"')
    return s.replace("<svg ", '<svg aria-hidden="true" style="display:block;flex-shrink:0" ', 1)

TITLE = "17/14 Chrome Super Moto Wheels Set for Yozma in 10 / Tuttio / Valintinsu"
BIKES = ["Yozma in 10", "Valintinsu EM5", "Tuttio"]
XS = json.loads((A / "xs/xs.json").read_text())

CSS = """
@font-face{font-family:'Inter';src:url(__FONT__) format('woff2');font-weight:100 900;font-display:block;}
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
body{font-family:'Inter',system-ui,sans-serif;color:#0d0d0d;background:#fff;-webkit-font-smoothing:antialiased;max-width:480px;margin:0 auto;}
a{color:inherit;}
.ann{background:#0d0d0d;color:#fff;font-size:12px;font-weight:500;height:32px;display:flex;align-items:center;justify-content:center;gap:7px;letter-spacing:.2px;}
.hdr{height:52px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;border-bottom:1px solid #eee;}
.hdr .l,.hdr .r{display:flex;gap:16px;align-items:center;width:72px;}.hdr .r{justify-content:flex-end;}
.logo{font-weight:600;font-size:17px;letter-spacing:-.2px;}
.crumb{font-size:12px;color:#777;padding:10px 16px 0;}
.plinth{position:relative;margin:8px 16px 0;height:262px;border-radius:18px;overflow:hidden;background:radial-gradient(120% 90% at 50% 38%,#3a3b3f 0%,#18191b 58%,#0b0b0c 100%);}
.plinth .floor{position:absolute;left:12%;right:12%;bottom:26px;height:22px;border-radius:50%;background:radial-gradient(closest-side,rgba(0,0,0,.65),transparent);}
.plinth img{position:absolute;left:50%;top:50%;transform:translate(-50%,-52%);width:82%;height:86%;object-fit:contain;}
.plinth .count{position:absolute;right:12px;bottom:12px;background:rgba(255,255,255,.14);color:#fff;font-size:11px;font-weight:600;padding:4px 9px;border-radius:20px;}
.plinth .tag{position:absolute;left:12px;top:12px;background:#fff;color:#0d0d0d;font-size:11px;font-weight:700;padding:5px 10px;border-radius:20px;letter-spacing:.3px;}
.info{padding:14px 16px 0;}
h1{font-size:22px;line-height:1.18;font-weight:800;letter-spacing:-.4px;}
.sub{font-size:14px;color:#555;margin-top:6px;line-height:1.35;}
.pr{display:flex;align-items:center;gap:10px;margin-top:12px;}
.price{font-size:26px;font-weight:800;letter-spacing:-.5px;}
.po{font-size:12px;font-weight:600;background:#f1f1f1;border-radius:20px;padding:5px 10px;display:flex;align-items:center;gap:5px;}
.fit{margin-top:12px;border:1.5px solid #0d0d0d;border-radius:14px;padding:11px 12px;}
.fit .h{font-size:13px;font-weight:700;display:flex;justify-content:space-between;align-items:center;}
.fit .h a{font-weight:500;color:#555;font-size:12px;}
.bikes{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;}
.bike{display:flex;align-items:center;gap:5px;font-size:13px;font-weight:600;background:#f4f4f4;border-radius:9px;padding:6px 9px;}
.cta{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;height:54px;margin-top:12px;background:#0d0d0d;color:#fff;border:0;border-radius:14px;font:700 16px 'Inter',sans-serif;letter-spacing:-.1px;cursor:pointer;}
.trust{display:flex;justify-content:space-between;gap:6px;margin-top:10px;font-size:11px;color:#444;font-weight:500;}
.trust div{display:flex;align-items:center;gap:4px;}
section{padding:36px 16px 0;}
section h2{font-size:22px;font-weight:800;letter-spacing:-.4px;line-height:1.15;}
section .lead{font-size:14px;color:#555;margin-top:6px;line-height:1.45;}
.fitcards{display:grid;gap:8px;margin-top:14px;}
.fc{display:flex;align-items:center;gap:12px;border:1px solid #e6e6e6;border-radius:14px;padding:14px;}
.fc b{font-size:16px;display:block;}.fc span{font-size:12px;color:#666;}
.fc .ok{margin-left:auto;}
.ask{display:flex;align-items:center;gap:10px;background:#f4f4f4;border-radius:14px;padding:14px;margin-top:8px;font-size:13px;line-height:1.4;}
.ask a{font-weight:700;}
.photos{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px;}
.photos figure{border-radius:14px;overflow:hidden;background:#111;aspect-ratio:3/4;}
.photos img{width:100%;height:100%;object-fit:cover;display:block;}
.photos figcaption{font-size:12px;color:#666;margin-top:6px;}
.spec{margin-top:14px;display:grid;grid-template-columns:120px 1fr;gap:12px;align-items:center;}
.spec .pic{background:#f4f4f4;border-radius:14px;aspect-ratio:1;display:flex;align-items:center;justify-content:center;}
.spec .pic img{width:88%;height:88%;object-fit:contain;}
.rows div{display:flex;justify-content:space-between;font-size:14px;padding:9px 0;border-bottom:1px solid #eee;}.rows div span{color:#666;}
.steps{margin-top:14px;display:grid;gap:10px;}
.step{display:flex;gap:12px;align-items:flex-start;}
.step .n{width:30px;height:30px;border-radius:50%;background:#0d0d0d;color:#fff;font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step b{font-size:15px;display:block;}.step p{font-size:13px;color:#555;margin-top:2px;line-height:1.4;}
details{border-bottom:1px solid #e6e6e6;padding:14px 0;}
summary{list-style:none;font-weight:700;font-size:15px;display:flex;justify-content:space-between;cursor:pointer;}
summary::-webkit-details-marker{display:none;}
details p{font-size:14px;color:#555;margin-top:8px;line-height:1.45;}
.xs{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px;}
.xs .im{background:#f4f4f4;border-radius:12px;aspect-ratio:1;overflow:hidden;display:flex;align-items:center;justify-content:center;}
.xs img{width:100%;height:100%;object-fit:contain;}
.xs .t{font-size:13px;margin-top:6px;line-height:1.3;}.xs .p{font-size:13px;font-weight:700;margin-top:2px;}
.news{margin:40px 16px 0;background:#0d0d0d;color:#fff;border-radius:18px;padding:22px 18px;}
.news b{font-size:18px;display:block;line-height:1.25;}
.news .f{display:flex;margin-top:14px;background:#fff;border-radius:12px;overflow:hidden;}
.news input{flex:1;border:0;padding:13px;font:14px 'Inter';}
.news button{border:0;background:#fff;padding:0 14px;font-weight:700;}
footer{padding:26px 16px 110px;font-size:12px;color:#777;display:flex;justify-content:space-between;}
.sticky{position:fixed;left:0;right:0;bottom:0;max-width:480px;margin:0 auto;background:#fff;border-top:1px solid #e6e6e6;padding:10px 16px 14px;display:flex;align-items:center;gap:12px;transform:translateY(110%);transition:transform .25s;z-index:20;}
.sticky.on{transform:none;}
.sticky .m{font-size:12px;color:#555;line-height:1.3;}.sticky .m b{display:block;color:#0d0d0d;font-size:15px;}
.sticky .cta{margin:0;height:46px;flex:1;font-size:15px;}
"""

def head(title):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="robots" content="noindex,nofollow">
<style>{CSS.replace('__FONT__', uri(A / 'fonts/inter-latin.woff2'))}</style></head><body>"""

def chrome():
    return f"""<div class="ann">{ic('clock-outline',14,'#fff')}Pre-orders ship 2 weeks after order</div>
<header class="hdr"><div class="l">{ic('menu',22)}{ic('magnify',21)}</div><div class="logo">FleeMoto</div><div class="r">{ic('account-outline',22)}{ic('cart-outline',22)}</div></header>"""

def bikes():
    return "".join(f'<div class="bike">{ic("check-circle",15,"#1a7f37")}{b}</div>' for b in BIKES)

def buyblock(sub=True, fit=True):
    s = f"""<div class="info"><h1>{TITLE}</h1>""" + ("""<p class="sub">Chrome super moto wheels, sold as a set.</p>""" if sub else "") + f"""
<div class="pr"><div class="price">$319.99</div><div class="po">{ic('calendar-check',14)}Pre-order</div></div>"""
    if fit:
        s += f"""<div class="fit"><div class="h">Fits these bikes<a href="{CONTACT}">Not sure? Ask us</a></div><div class="bikes">{bikes()}</div></div>"""
    s += f"""<button class="cta" id="buy">Pre-order &middot; $319.99</button>
<div class="trust"><div>{ic('truck-fast-outline',15)}Ships 2 weeks after order</div><div>{ic('shield-lock-outline',15)}Shop Pay checkout</div></div></div>"""
    return s

def hero_A():
    return f"""<div class="crumb">Home / Shop all / Wheels</div>
<div class="plinth"><div class="tag">17/14 &middot; CHROME</div><div class="floor"></div><img src="{uri(A/'cut/pair.webp')}" alt="FleeMoto 17/14 chrome super moto wheel set"><div class="count">1 / 4 photos</div></div>
{buyblock()}"""

def hero_B():  # on-bike photo, full bleed, text on scrim
    return f"""<div style="position:relative;height:430px;overflow:hidden;background:#111;">
<img src="{uri(A/'photo/sunset.webp')}" style="width:100%;height:100%;object-fit:cover;object-position:50% 40%;display:block;">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 35%,rgba(0,0,0,.85) 100%);"></div>
<div style="position:absolute;left:16px;right:16px;bottom:16px;color:#fff;"><h1 style="font-size:21px;">{TITLE}</h1>
<div class="pr"><div class="price">$319.99</div><div class="po" style="background:rgba(255,255,255,.18);">{ic('calendar-check',14,'#fff')}Pre-order</div></div></div></div>
<div class="info"><div class="fit"><div class="h">Fits these bikes<a href="{CONTACT}">Not sure? Ask us</a></div><div class="bikes">{bikes()}</div></div>
<button class="cta">Pre-order &middot; $319.99</button><div class="trust"><div>{ic('truck-fast-outline',15)}Ships 2 weeks after order</div><div>{ic('shield-lock-outline',15)}Shop Pay checkout</div></div></div>"""

def hero_C():  # fitment first
    pills = "".join(f'<div class="bike" style="background:#0d0d0d;color:#fff;">{ic("motorbike",15,"#fff")}{b}</div>' for b in BIKES)
    return f"""<div style="background:#f4f4f4;padding:14px 16px;"><div style="font-size:13px;font-weight:700;">Which bike do you ride?</div><div class="bikes">{pills}</div>
<div style="font-size:12px;color:#555;margin-top:8px;">This set fits all three. Something else? <a href="{CONTACT}" style="font-weight:700;">Ask us</a></div></div>
<div class="plinth" style="height:200px;margin-top:12px;"><div class="floor"></div><img src="{uri(A/'cut/pair.webp')}"></div>
{buyblock(sub=False, fit=False)}"""

def hero_D():  # photo grid
    g = "".join(f'<div style="border-radius:10px;overflow:hidden;background:{bg};height:150px;display:flex;align-items:center;justify-content:center;"><img src="{uri(src)}" style="width:100%;height:100%;object-fit:{fit};"></div>'
                for src, fit, bg in [(A/'photo/wall.webp','cover','#111'),(A/'cut/pair.webp','contain','#f4f4f4'),(A/'photo/sunset.webp','cover','#111'),(A/'cut/single.webp','contain','#f4f4f4')])
    return f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:10px 16px 0;">{g}</div>
<div class="info"><h1 style="font-size:20px;">{TITLE}</h1><div class="pr"><div class="price">$319.99</div><div class="po">{ic('calendar-check',14)}Pre-order</div></div>
<div class="fit"><div class="h">Fits these bikes</div><div class="bikes">{bikes()}</div></div><button class="cta">Pre-order &middot; $319.99</button></div>"""

def below():
    fc = "".join(f'<div class="fc">{ic("motorbike",28)}<div><b>{b}</b><span>Listed by FleeMoto as compatible</span></div><div class="ok">{ic("check-circle",24,"#1a7f37")}</div></div>' for b in BIKES)
    xs = "".join(f'<div><div class="im"><img src="{uri(A/x["img"])}" alt="{x["title"]}"></div><div class="t">{x["title"]}</div><div class="p">${x["price"]}</div></div>' for x in XS)
    faq = [("Which bikes does this set fit?", "FleeMoto lists the Yozma in 10, the Valintinsu EM5 and the Tuttio. If you ride something else, message us before you order."),
           ("When will it ship?", "This is a pre-order. Pre-orders ship 2 weeks after you order."),
           ("What size are the wheels?", "17/14 inch, in chrome, sold as a set. The last two photos show the pair."),
           ("How do I pay?", "Checkout takes Shop Pay, plus the other payment options shown at checkout."),
           ("Can I ask a question first?", "Yes. Use the contact page and FleeMoto will get back to you.")]
    fq = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}{ic("chevron-down",20)}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faq))
    return f"""
<section id="fit"><h2>Check your bike first</h2><p class="lead">Wheels only help if they bolt on. These are the bikes FleeMoto lists for this set.</p>
<div class="fitcards">{fc}</div><div class="ask">{ic('email-outline',22)}<div>Riding a different model? <a href="{CONTACT}">Send us a message</a> before you pre-order.</div></div></section>
<section><h2>On the bike</h2><p class="lead">The set fitted, from FleeMoto's own photos.</p>
<div class="photos"><div><figure><img src="{uri(A/'photo/wall.webp')}" alt="Wheel set fitted, daylight"></figure><figcaption>Daylight</figcaption></div><div><figure><img src="{uri(A/'photo/sunset.webp')}" alt="Wheel set fitted, dusk"></figure><figcaption>Dusk</figcaption></div></div></section>
<section><h2>What you get</h2>
<div class="spec"><div class="pic"><img src="{uri(A/'cut/single.webp')}" alt="Single wheel"></div><div class="rows"><div><span>Size</span>17/14 inch</div><div><span>Finish</span>Chrome</div><div><span>Style</span>Super moto</div><div><span>Sold as</span>A set</div></div></div></section>
<section><h2>How the pre-order works</h2><div class="steps">
<div class="step"><div class="n">1</div><div><b>Check the fit</b><p>Yozma in 10, Valintinsu EM5 or Tuttio. Ask us if you're unsure.</p></div></div>
<div class="step"><div class="n">2</div><div><b>Place your pre-order</b><p>$319.99, paid at checkout with Shop Pay or another option.</p></div></div>
<div class="step"><div class="n">3</div><div><b>It ships in 2 weeks</b><p>Pre-orders ship 2 weeks after your order.</p></div></div></div></section>
<section><h2>Questions</h2><div style="margin-top:6px;">{fq}</div></section>
<section><h2>Finish the build</h2><p class="lead">More parts from FleeMoto.</p><div class="xs">{xs}</div></section>
<div class="news"><b>Get exclusive deals and early access to new products.</b><div class="f"><input placeholder="Email address" aria-label="Email address"><button aria-label="Subscribe">&rarr;</button></div></div>
<footer><span>&copy; 2026 FleeMoto</span><span>Terms and Policies</span></footer>
<div class="sticky" id="sticky"><div class="m"><b>$319.99</b>Pre-order &middot; ships in 2 weeks</div><button class="cta">Pre-order</button></div>
<script>(function(){{var b=document.getElementById('buy'),s=document.getElementById('sticky');if(!b||!s)return;
function u(){{var r=b.getBoundingClientRect();s.classList.toggle('on',r.bottom<0);}}addEventListener('scroll',u,{{passive:true}});u();}})();</script>"""

def main():
    if "--variants" in sys.argv:
        VOUT.mkdir(parents=True, exist_ok=True)
        for i, fn in enumerate([hero_A, hero_B, hero_C, hero_D], 1):
            (VOUT / f"v{i}.html").write_text(head(f"FleeMoto PDP variant {i}") + chrome() + fn() + "</body></html>", encoding="utf-8")
            print("variant", i)
        return
    html = head(f"{TITLE} | FleeMoto (concept redesign by @koolestpro)") + chrome() + hero_A() + below() + "</body></html>"
    OUT.write_text(html, encoding="utf-8"); print("wrote", OUT, f"{len(html)/1024:.0f} KB")

if __name__ == "__main__":
    main()
