#!/usr/bin/env python3
"""Bala homepage hero: four design directions on real Bala assets (2026-10-11, r3).

Built after the hero research in references-for-posts/homepage-hero-research-2026-10-11/
(Ridwan's 8 references + live captures + Baymard/Instant). Each variant is one family from that
research, so the choice is made by looking at them side by side, not by guessing.

  v1  Range flatlay + floating product labels, centered stack below (Serenova / Tofu Go)
  v2  Lifestyle photo top + press sticker, benefit chips (SWT / S'noods)
  v3  Full-bleed lifestyle photo, centered text on a scrim (Majco Greens)
  v4  Text first, range band below (Carnivore Snax / Ion Layer)

Every fact is from shopbala.com on 2026-10-11: 4.9 stars from 1,865 reviews (Bala Bangles),
Bangles 1-3 lb from $55, press logos from their own "As seen on" strip (WSJ, goop, Glamour),
"Save 10% when you bundle", HSA/FSA eligible (footer + PDP), photos from their CDN.
Output: outputs/cro-fixes/bala/_variants/v{1..4}.html (+ screenshots via the board script).
"""
import base64, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "bala" / "_assets"
OUT = ROOT / "outputs" / "cro-fixes" / "bala" / "_variants"


def uri(name):
    p = A / name
    mime = {".png": "image/png", ".woff": "font/woff", ".jpg": "image/jpeg"}[p.suffix]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def icon(name, size=16, color="currentColor"):
    svg = (A / "icons" / f"ic_{name}.svg").read_text()
    return (svg.replace('width="1em"', f'width="{size}"').replace('height="1em"', f'height="{size}"')
               .replace('fill="currentColor"', f'fill="{color}"')
               .replace("<svg ", '<svg aria-hidden="true" style="display:block;flex-shrink:0" ', 1))


def stars(size, color):
    return '<span class="stars">' + "".join(icon("star", size, color) for _ in range(5)) + "</span>"


BASE_CSS = """
@font-face{font-family:'Iskry';src:url(__F_ISB__) format('woff');font-weight:700;font-display:block;}
@font-face{font-family:'Diatype';src:url(__F_DIA__) format('woff');font-weight:400;font-display:block;}
:root{--ink:#1C1A1B;--blush:#FBEBEE;--rose:#C9566E;--soft:#6E6467;--line:#E9DADD;}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Diatype',system-ui,sans-serif;color:var(--ink);background:#fff;width:390px;margin:0 auto;}
.offer{height:30px;background:linear-gradient(90deg,#F4C6D0,#FBB8B5);display:flex;align-items:center;justify-content:center;gap:6px;font-size:12px;}
.offer b{font-family:'Iskry',sans-serif;font-weight:700;}
header{height:52px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;background:#fff;position:relative;z-index:5;}
header img{height:26px;display:block;}
header .cart{width:30px;height:30px;border:1.5px solid var(--ink);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;}
.stars{display:inline-flex;gap:1px;}
.proofline{display:flex;align-items:center;justify-content:center;gap:6px;font-size:12.5px;color:#3d3739;}
.proofline b{font-family:'Iskry',sans-serif;font-weight:700;color:var(--ink);}
h1{font-family:'Iskry',sans-serif;font-weight:700;letter-spacing:-.6px;text-align:center;-webkit-text-stroke:.7px currentColor;}
h1 span{color:var(--rose);}
.sub{text-align:center;font-size:14px;line-height:1.4;color:#3d3739;}
.cta{display:flex;align-items:center;justify-content:center;gap:10px;height:54px;border-radius:27px;background:var(--ink);color:#fff;font-family:'Iskry',sans-serif;font-weight:700;font-size:16px;letter-spacing:.8px;text-transform:uppercase;}
.press{display:flex;align-items:center;justify-content:center;gap:14px;}
.press .lab{white-space:nowrap;font-size:10.5px;letter-spacing:1.4px;text-transform:uppercase;color:var(--soft);}
.press img{display:block;opacity:.85;}
.chips{display:flex;flex-wrap:wrap;justify-content:center;gap:7px;}
.chip{display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 11px;border-radius:15px;background:#fff;border:1.5px solid var(--line);font-size:12.5px;}
.chip svg{color:var(--rose);}
.trust{display:flex;justify-content:center;gap:18px;font-size:12px;color:#3d3739;}
.trust div{display:flex;align-items:center;gap:5px;}
.trust svg{color:var(--rose);}
"""

HEAD = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=390, initial-scale=1">
<title>Bala hero __V__ (concept by @koolestpro)</title><style>__BASE__ __CSS__</style></head><body>
<div class="offer"><b>Save 10%</b> when you bundle &middot; HSA/FSA eligible</div>
<header><span>__I_MENU__</span><img src="__LOGO__" alt="Bala"><span class="cart">0</span></header>
"""
PRESS = ('<div class="press"><span class="lab">As seen in</span><img src="__P_WSJ__" style="height:13px" alt="The Wall Street Journal">'
         '<img src="__P_GOOP__" style="height:15px" alt="goop"><img src="__P_GLAM__" style="height:13px" alt="Glamour"></div>')
H1 = 'Weights &amp; activewear,<br><span>but make it cute.</span>'
SUB = 'Wearable weights, Pilates props and matching sets.'
PROOF = '__STARS__ <b>4.9</b> from 1,865 Bala Bangles reviews'

VARIANTS = {
 "v1": ("Range flatlay + product labels", """
.hero{position:relative;height:404px;background:#FBEBEE;overflow:hidden;}
.hero img.kit{position:absolute;left:50%;top:8px;transform:translateX(-50%);width:310px;height:388px;display:block;}
.cats{display:flex;justify-content:center;gap:7px;margin-top:14px;}
.cats span{height:32px;padding:0 12px;border:1.5px solid var(--line);border-radius:16px;display:flex;align-items:center;font-size:12.5px;white-space:nowrap;}
.tag{position:absolute;z-index:2;background:#fff;border-radius:16px;padding:6px 11px;font-size:11.5px;line-height:1.2;box-shadow:0 6px 16px rgba(160,70,90,.16);text-align:center;}
.tag b{display:block;font-family:'Iskry',sans-serif;font-weight:700;font-size:13px;}
.stack{padding:14px 16px 0;}
.stack h1{font-size:31px;line-height:1.06;margin-top:8px;}
.stack .sub{margin-top:8px;}
.stack .cta{margin-top:14px;}
.stack .press{margin-top:14px;}
""", """
<div class="hero">
  <img class="kit" src="__KIT__" alt="Bala Bangles, Bala Bra, Flared Legging and Everyday Sweatshirt in Blush">
  <div class="tag" style="left:12px;top:22px;"><b>Bala Bangles</b>1&ndash;3 lb, wrists or ankles</div>
  <div class="tag" style="right:12px;top:62px;"><b>Bala Bra</b>matching sets</div>
  <div class="tag" style="right:12px;top:262px;"><b>Flared Legging</b></div>
  <div class="tag" style="left:12px;top:318px;"><b>Everyday Sweatshirt</b></div>
</div>
<div class="stack">
  <div class="proofline">__PROOF__</div>
  <h1>__H1__</h1>
  <div class="sub">__SUB__</div>
  <div class="cta">Shop best sellers __I_ARROW__</div>
  <div class="cats"><span>Weights</span><span>Pilates props</span><span>Activewear</span><span>Bundles</span></div>
  __PRESS__
</div>
"""),
 "v2": ("Lifestyle top + press sticker + chips", """
.hero{position:relative;height:378px;overflow:hidden;background:#E9A3BC;}
.hero img.ph{position:absolute;left:-14px;top:-130px;width:418px;height:auto;display:block;}
.sticker{position:absolute;right:12px;bottom:14px;width:96px;height:96px;border-radius:50%;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;box-shadow:0 8px 20px rgba(0,0,0,.18);transform:rotate(-8deg);}
.sticker img{display:block;}
.sticker span{font-size:9.5px;letter-spacing:1.2px;text-transform:uppercase;color:var(--soft);}
.stack{padding:14px 16px 0;}
.stack h1{font-size:31px;line-height:1.06;margin-top:8px;}
.stack .chips{margin-top:12px;}
.stack .cta{margin-top:14px;}
.stack .trust{margin-top:12px;}
""", """
<div class="hero">
  <img class="ph" src="__LIFE_PINK__" alt="Woman wearing Blush Bala Bangles holding a camera">
  <div class="sticker"><span>as seen in</span><img src="__P_GLAM__" style="height:16px" alt="Glamour"></div>
</div>
<div class="stack">
  <div class="proofline">__PROOF__</div>
  <h1>__H1__</h1>
  <div class="chips"><span class="chip">__I_CHECK__Wearable weights</span><span class="chip">__I_CHECK__Pilates props</span><span class="chip">__I_CHECK__Activewear</span></div>
  <div class="cta">Shop best sellers __I_ARROW__</div>
  <div class="trust"><div>__I_TAG__Bundle &amp; save 10%</div><div>__I_HSA__HSA/FSA eligible</div></div>
</div>
"""),
 "v3": ("Full-bleed photo, text on scrim", """
.hero{position:relative;height:762px;overflow:hidden;background:#1d3324;}
.hero img{position:absolute;left:0;top:-20px;width:390px;height:auto;display:block;}
.scrim{position:absolute;left:0;right:0;bottom:0;height:470px;background:linear-gradient(180deg,rgba(24,44,30,0) 0%,rgba(24,44,30,.78) 36%,rgba(20,38,26,.96) 100%);}
.txt{position:absolute;left:16px;right:16px;bottom:18px;z-index:2;color:#fff;}
.txt .proofline{color:rgba(255,255,255,.9);} .txt .proofline b{color:#fff;}
.txt h1{font-size:33px;line-height:1.06;margin-top:8px;color:#fff;} .txt h1 span{color:#F6B9C8;}
.txt .sub{color:rgba(255,255,255,.88);margin-top:8px;}
.txt .cta{margin-top:14px;background:#fff;color:var(--ink);}
.cats{display:flex;justify-content:center;gap:8px;margin-top:12px;}
.cats span{height:32px;padding:0 13px;border:1.5px solid rgba(255,255,255,.55);border-radius:16px;display:flex;align-items:center;font-size:12.5px;}
""", """
<div class="hero">
  <img src="__LIFE_GREEN__" alt="Woman wearing Bala Bangles on her ankles">
  <div class="scrim"></div>
  <div class="txt">
    <div class="proofline">__PROOF_W__</div>
    <h1>__H1__</h1>
    <div class="sub">__SUB__</div>
    <div class="cta">Shop best sellers __I_ARROW_D__</div>
    <div class="cats"><span>Weights</span><span>Pilates props</span><span>Activewear</span></div>
  </div>
</div>
"""),
 "v4": ("Text first, range band below", """
.top{background:#FBEBEE;padding:18px 16px 16px;}
.top h1{font-size:33px;line-height:1.06;}
.top .sub{margin-top:9px;}
.top .proofline{margin-top:10px;}
.top .cta{margin-top:14px;}
.band{position:relative;height:420px;overflow:hidden;background:#E8EDF0;}
.band img{position:absolute;left:50%;top:-6px;transform:translateX(-50%);width:346px;height:432px;display:block;}
.band .tag{position:absolute;z-index:2;background:#fff;border-radius:14px;padding:5px 10px;font-family:'Iskry',sans-serif;font-weight:700;font-size:12.5px;box-shadow:0 6px 16px rgba(0,0,0,.1);}
""", """
<div class="top">
  <h1>__H1__</h1>
  <div class="sub">__SUB__</div>
  <div class="proofline">__PROOF__</div>
  <div class="cta">Shop best sellers __I_ARROW__</div>
</div>
<div class="band">
  <img src="__KIT_SEA__" alt="Bala Power Kit in Sea: mat, Bangles, ring and kettlebell">
  <span class="tag" style="left:14px;top:18px;">Bangles</span><span class="tag" style="right:14px;top:140px;">Power Ring</span><span class="tag" style="left:14px;top:250px;">Mat</span><span class="tag" style="right:20px;top:330px;">Kettlebell</span>
</div>
"""),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rep = {
        "__F_ISB__": uri("Iskry-Bold.woff"), "__F_DIA__": uri("Diatype-Regular.woff"),
        "__LOGO__": uri("logo.png"), "__KIT__": uri("kit_studio_street.jpg"), "__KIT_SEA__": uri("kit_power_sea.jpg"),
        "__LIFE_PINK__": uri("life_pink_camera.png"), "__LIFE_GREEN__": uri("life_green_ankles.png"),
        "__P_WSJ__": uri("press_wsj.png"), "__P_GOOP__": uri("press_goop.png"), "__P_GLAM__": uri("press_glamour.png"),
        "__I_MENU__": icon("menu", 26, "#1C1A1B"), "__I_ARROW__": icon("arrow-right", 18, "#fff"),
        "__I_ARROW_D__": icon("arrow-right", 18, "#1C1A1B"), "__I_CHECK__": icon("check-circle-outline", 15),
        "__I_TAG__": icon("tag-outline", 15), "__I_HSA__": icon("hospital-box-outline", 15),
    }
    for k, (title, css, body) in VARIANTS.items():
        html = (HEAD + body + "</body></html>").replace("__BASE__", BASE_CSS).replace("__CSS__", css).replace("__V__", f"{k}: {title}")
        html = (html.replace("__PRESS__", PRESS).replace("__H1__", H1).replace("__SUB__", SUB)
                .replace("__PROOF_W__", PROOF.replace("__STARS__", stars(12, "#fff")))
                .replace("__PROOF__", PROOF).replace("__STARS__", stars(12, "#1C1A1B")))
        for a, b in rep.items():
            html = html.replace(a, b)
        assert "__" not in html.replace("__proto__", ""), [x for x in html.split("__")[1::2]][:5]
        (OUT / f"{k}.html").write_text(html, encoding="utf-8")
        print("wrote", k, title)


if __name__ == "__main__":
    main()
