#!/usr/bin/env python3
"""Build the Fishwife shop-all COLLECTION PAGE CRO rebuild (the "after" first screen) + hero variants.

Weekly CRO Fix, 2026-10-25 (unattended run). Fallback flow: Claude authors the page directly from
outputs/cro-fixes/fishwife_shop-all-collection_build-brief.md (no page builder driven in an unattended run).

#1 finding (live page https://eatfishwife.com/collections/all, 390x844, 2026-10-25, popups closed):
the whole first screen is a 400px banner whose only message is "Shop Tinned Fish & More!". Filter pills
start at y=540 and the first product name sits at y=863, below the 844px screen. A shopper on the page
whose only job is choosing a tin sees no product name, no rating and no way to buy until they scroll.
Supporting (SEEN + MEASURED): the cards show a star average with no review count, so the Advent Calendar
(5.0 from 2 reviews) looks exactly as proven as the Fly By Jing smoked salmon (4.9 from 641); and the
first row is two new drops (21 and 2 reviews) while the most-reviewed tins sit further down.

Every number below is from the live site on 2026-10-25: review counts from each PDP's JSON-LD
aggregateRating, prices from /products.json, best-seller badges only on products in their own
/collections/best-sellers. Real logo (header <img> fishwife-logo.png), real fonts (Recoleta + Albert
Sans from their theme CDN), real packshots (background removed) and their own banner photo.

Usage: python3 build_fishwife_rebuild.py            -> full rebuild (variant B, slim photo band)
       python3 build_fishwife_rebuild.py --variants -> 4 hero variant pages in _variants/
"""
import base64, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "outputs" / "cro-fixes" / "fishwife" / "_assets"
OUT = ROOT / "outputs" / "cro-fixes" / "fishwife_shop-all-collection_rebuild.html"
VOUT = ROOT / "outputs" / "cro-fixes" / "fishwife" / "_variants"


def uri(p: pathlib.Path) -> str:
    mime = {".png": "image/png", ".woff2": "font/woff2", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".webp": "image/webp"}[p.suffix]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def icon(name, size=16, color="currentColor"):
    svg = (A / "icons" / f"ic_{name}.svg").read_text()
    return (svg.replace('width="1em"', f'width="{size}"').replace('height="1em"', f'height="{size}"')
               .replace('fill="currentColor"', f'fill="{color}"')
               .replace("<svg ", '<svg aria-hidden="true" style="display:block;flex-shrink:0" ', 1))


def stars(avg, size=12, color="#F2A900"):
    r = round(avg * 2) / 2; full = int(r); half = (r - full) == 0.5
    s = "".join(icon("star-fill", size, color) for _ in range(full))
    if half: s += icon("star-half-fill", size, color)
    s += "".join(icon("star-fill", size, "#E2DCCB") for _ in range(5 - full - (1 if half else 0)))
    return f'<span class="stars">{s}</span>'


# name, pack, rating, reviews, price, cutout, badge   (all from the live site, 2026-10-25)
P = {
    "fbj":     ("Smoked Salmon with Fly By Jing Chili Crisp", "3-pack", 4.9, 641, "$40", "fbj", "BEST SELLER"),
    "gold":    ("Gold Label Smoked Salmon", "3-pack", 4.9, 520, "$37", "gold", "BEST SELLER"),
    "starter": ("The Starter Pack", "7 tins, one of each", 4.9, 343, "$88", "starter", "BEST SELLER"),
    "sard":    ("Sardines with Preserved Lemon", "3-pack", 4.9, 223, "$32", "sard", "BEST SELLER"),
    "tuna":    ("Albacore Tuna in Olive Oil", "3-pack", 4.9, 198, "$32", "tuna", None),
    "zhong":   ("Smoked Salmon with Sweet &amp; Spicy Zhong", "3-pack", 4.9, 110, "$40", "zhong", None),
    "spicy":   ("The Spicy Trio", "3-pack", 4.9, 44, "$45", "spicy", None),
    "belly":   ("Tuna Belly", "3-pack", 4.5, 21, "$75", "belly", "JUST DROPPED"),
}


def card(k):
    n, pack, r, c, pr, cut, badge = P[k]
    b = f'<span class="badge{" new" if badge == "JUST DROPPED" else ""}">{badge}</span>' if badge else ""
    return f"""<div class="card"><div class="ph">{b}<img src="__CUT_{cut}__" alt=""></div>
  <div class="info"><h3>{n}</h3><div class="pack">{pack}</div>
  <div class="rv">{stars(r, 11)}<b>{r}</b><span>({c})</span></div>
  <div class="row"><span class="pr">{pr}</span><button class="add">{icon('plus', 13, '#111')}Add</button></div></div></div>"""


CSS = """
@font-face{font-family:'Recoleta';src:url(__F_RM__) format('woff2');font-weight:500;font-display:block;}
@font-face{font-family:'Recoleta';src:url(__F_RS__) format('woff2');font-weight:600;font-display:block;}
@font-face{font-family:'Albert Sans';src:url(__F_AR__) format('woff2');font-weight:400;font-display:block;}
@font-face{font-family:'Albert Sans';src:url(__F_AM__) format('woff2');font-weight:500;font-display:block;}
@font-face{font-family:'Albert Sans';src:url(__F_AB__) format('woff2');font-weight:700;font-display:block;}
:root{--ink:#111;--cream:#FFFCF3;--sun:#FDCD62;--sea:#397CC0;--kelp:#2F7D55;--line:#1a1a1a;--soft:#5b5548;--plinth:#F3ECDC;}
*{margin:0;padding:0;box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{font-family:'Albert Sans',system-ui,sans-serif;color:var(--ink);background:var(--cream);width:100%;max-width:430px;margin:0 auto;}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important;}}
.annc{height:30px;background:#FFF8EA;display:flex;align-items:center;justify-content:center;gap:7px;font-size:13px;border-bottom:1px solid #efe6d2;}
.annc b{font-weight:700;}
header{height:68px;display:flex;align-items:center;justify-content:space-between;padding:0 14px;background:var(--cream);border-bottom:1.5px solid var(--line);}
header .g{display:flex;gap:6px;}
header .ci{width:36px;height:36px;border:1.5px solid var(--line);border-radius:50%;display:flex;align-items:center;justify-content:center;}
header img.logo{height:46px;display:block;}
.stars{display:inline-flex;gap:1px;}
.band{position:relative;height:118px;overflow:hidden;border-bottom:1.5px solid var(--line);}
.band img{position:absolute;left:0;top:-96px;width:390px;height:auto;}
.band .scrim{position:absolute;inset:0;background:linear-gradient(90deg,rgba(18,58,36,.92) 0%,rgba(18,58,36,.78) 58%,rgba(18,58,36,.15) 100%);}
.band .t{position:absolute;left:16px;top:16px;right:110px;color:#fff;}
h1{font-family:'Recoleta',serif;font-weight:600;font-size:29px;line-height:1.02;letter-spacing:-.3px;}
.band p{font-size:13px;line-height:1.3;margin-top:6px;color:#e8f1ea;}
.pills{display:flex;gap:7px;padding:12px 14px 0;overflow:hidden;white-space:nowrap;}
.pills span{border:1.5px solid var(--line);border-radius:6px;padding:6px 11px;font-size:13.5px;background:#fff;}
.pills span.on{background:var(--sun);font-weight:500;}
.sortrow{display:flex;justify-content:space-between;align-items:center;padding:10px 14px 0;font-size:12.5px;color:var(--soft);}
.sortrow b{color:var(--ink);font-weight:700;}
.sortrow .f{display:flex;align-items:center;gap:5px;color:var(--ink);font-weight:500;}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px 14px 0;}
.card{background:#fff;border:1.5px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;}
.card .ph{height:132px;background:var(--plinth);position:relative;display:flex;align-items:center;justify-content:center;border-bottom:1.5px solid var(--line);}
.card .ph img{max-width:74%;max-height:112px;object-fit:contain;}
.badge{position:absolute;left:7px;top:7px;background:var(--ink);color:var(--sun);font-size:9.5px;font-weight:700;letter-spacing:.6px;padding:3px 6px;border-radius:4px;}
.badge.new{background:var(--sea);color:#fff;}
.info{padding:8px 9px 9px;display:flex;flex-direction:column;flex:1;}
.card h3{font-family:'Recoleta',serif;font-weight:600;font-size:14.5px;line-height:1.12;min-height:32px;}
.pack{font-size:11.5px;color:var(--soft);margin-top:2px;}
.rv{display:flex;align-items:center;gap:4px;font-size:12px;margin-top:5px;}
.rv span{color:var(--soft);}
.row{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:8px;}
.pr{font-weight:700;font-size:16px;}
.add{display:flex;align-items:center;gap:4px;height:32px;padding:0 12px;border:1.5px solid var(--line);border-radius:999px;background:var(--sun);font-family:'Albert Sans',sans-serif;font-weight:700;font-size:13px;color:#111;}
.newbie{margin:18px 14px 0;border:1.5px solid var(--line);border-radius:12px;background:#A6D9FB;padding:14px;display:flex;gap:12px;align-items:center;}
.newbie img{height:96px;}
.newbie b{font-family:'Recoleta',serif;font-weight:600;font-size:19px;display:block;line-height:1.1;}
.newbie small{display:block;font-size:12.5px;color:#22303a;margin-top:4px;line-height:1.35;}
.sec{font-family:'Recoleta',serif;font-weight:600;font-size:22px;padding:24px 14px 0;}
footer{padding:28px 16px 40px;font-size:11px;color:#8a8273;text-align:center;}
"""

HEAD = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fishwife | Everything Fishwife (CRO rebuild concept by @koolestpro)</title>
<!-- Unofficial concept rebuild by @koolestpro. Fishwife is not a client. All facts from eatfishwife.com, 2026-10-25. -->
<style>__CSS__</style></head><body>
<div class="annc">__TRUCK__ <b>Free shipping</b> on orders $75+</div>
<header><div class="g"><span class="ci">__MENU__</span><span class="ci">__SEARCH__</span></div><img class="logo" src="__LOGO__" alt="Fishwife"><div class="g"><span class="ci">__USER__</span><span class="ci">__BAG__</span></div></header>
"""

BAND = """<div class="band"><img src="__BANNER__" alt=""><div class="scrim"></div>
  <div class="t"><h1>Everything Fishwife</h1><p>Tinned fish, caviar, bundles and merch.</p></div></div>"""

PILLS = """<div class="pills"><span class="on">All Goods</span><span>Tinned Fish</span><span>Caviar</span><span>Bundles</span><span>Merch</span><span>Gifts</span></div>"""
SORT = """<div class="sortrow"><span>Sort: <b>Most reviewed</b></span><span class="f">__SLIDERS__ Filter</span></div>"""

GRID1 = '<div class="grid">' + card("fbj") + card("gold") + card("starter") + card("sard") + "</div>"

BELOW = ('<div class="newbie"><img src="__CUT_starter__" alt=""><div><b>New to tinned fish?</b><small>The Starter Pack: 7 tins, one of each, from smoky to citrusy. 4.9 from 343 reviews, $88.</small></div></div>'
         '<div class="sec">More tins</div><div class="grid">' + card("tuna") + card("zhong") + card("spicy") + card("belly") + "</div>"
         '<footer>Unofficial concept rebuild by @koolestpro. Fishwife is not a client.<br>Products, prices and review counts from eatfishwife.com, Oct 25 2026.</footer>')

# --- variant families (same assets, same facts) -------------------------------------
# A: grid first (no band, a one-line title row)
VAR_A = """<div style="padding:14px 14px 0;display:flex;align-items:baseline;justify-content:space-between;"><h1 style="font-size:26px;">Everything Fishwife</h1><span style="font-size:12px;color:#5b5548;">Tins, caviar, merch</span></div>""" + PILLS + SORT + GRID1
# B: slim photo band + grid  (CHOSEN)
VAR_B = BAND + PILLS + SORT + GRID1
# C: shop by fish tiles, then the grid
VAR_C = """<div style="padding:14px 14px 0;"><h1 style="font-size:26px;">Everything Fishwife</h1></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:10px 14px 0;">
 <div style="border:1.5px solid #1a1a1a;border-radius:10px;background:#F3ECDC;height:96px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:6px;font-size:12px;font-weight:700;"><img src="__CUT_gold__" style="height:58px;margin-bottom:4px;">Salmon</div>
 <div style="border:1.5px solid #1a1a1a;border-radius:10px;background:#F3ECDC;height:96px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:6px;font-size:12px;font-weight:700;"><img src="__CUT_tuna__" style="height:58px;margin-bottom:4px;">Tuna</div>
 <div style="border:1.5px solid #1a1a1a;border-radius:10px;background:#F3ECDC;height:96px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:6px;font-size:12px;font-weight:700;"><img src="__CUT_sard__" style="height:50px;margin-bottom:4px;">Sardines</div>
 <div style="border:1.5px solid #1a1a1a;border-radius:10px;background:#F3ECDC;height:96px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:6px;font-size:12px;font-weight:700;"><img src="__CUT_starter__" style="height:58px;margin-bottom:4px;">Bundles</div>
</div>""" + SORT + GRID1
# D: starter spotlight first (answers their own popup question: "Are you new to tinned fish?")
VAR_D = """<div style="margin:12px 14px 0;border:1.5px solid #1a1a1a;border-radius:12px;background:#A6D9FB;padding:12px 14px;display:flex;gap:12px;align-items:center;">
 <img src="__CUT_starter__" style="height:118px;"><div><div style="font-size:11px;font-weight:700;letter-spacing:.8px;">NEW TO TINNED FISH?</div>
 <h1 style="font-size:24px;margin-top:3px;">Start with The Starter Pack</h1><div class="rv" style="margin-top:6px;">__STARS49__<b>4.9</b><span>(343)</span> &middot; <b>$88</b></div>
 <button class="add" style="margin-top:8px;">Add to cart</button></div></div>""" + PILLS + SORT + '<div class="grid">' + card("fbj") + card("gold") + "</div>"


def fill(html):
    rep = {
        "__CSS__": CSS,
        "__F_RM__": uri(A / "fonts" / "Recoleta-Medium.woff2"), "__F_RS__": uri(A / "fonts" / "Recoleta-SemiBold.woff2"),
        "__F_AR__": uri(A / "fonts" / "AlbertSans-Regular.woff2"), "__F_AM__": uri(A / "fonts" / "AlbertSans-Medium.woff2"),
        "__F_AB__": uri(A / "fonts" / "AlbertSans-Bold.woff2"),
        "__LOGO__": uri(A / "logo_sm.png"), "__BANNER__": uri(A / "banner.webp"),
        "__TRUCK__": icon("truck", 15), "__MENU__": icon("list", 19), "__SEARCH__": icon("magnifying-glass", 18),
        "__USER__": icon("user", 18), "__BAG__": icon("shopping-bag", 18), "__SLIDERS__": icon("sliders-horizontal", 15),
        "__STARS49__": stars(4.9, 12),
    }
    for k in ("fbj", "gold", "starter", "sard", "tuna", "zhong", "spicy", "belly"):
        rep[f"__CUT_{k}__"] = uri(A / "cut" / f"{k}.webp")
    for k, v in rep.items():
        html = html.replace(k, v)
    return html


def page(top, below=True):
    b = BELOW if below else ""
    if top is VAR_D:  # D already leads with the starter block; do not repeat it below
        b = b[b.index('<div class="sec">'):]
    return fill(HEAD + top + b + "</body></html>")


def main():
    if "--variants" in sys.argv:
        VOUT.mkdir(parents=True, exist_ok=True)
        for k, top in {"v1": VAR_A, "v2": VAR_B, "v3": VAR_C, "v4": VAR_D}.items():
            (VOUT / f"{k}.html").write_text(page(top), encoding="utf-8"); print("wrote", k)
        return
    OUT.write_text(page(VAR_B), encoding="utf-8"); print("wrote", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
