#!/usr/bin/env python3
"""Build the October 16, 2026 Tips week pack from verified screen evidence."""
import base64
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
sys.path.insert(0, os.path.join(ROOT, ".ai-workflow/tips-weekly-2026-10-09"))
from common import shell, cta_slide, page

DATE = "2026-10-16"
OUT = os.path.join(ROOT, "outputs", "tips")
EV = os.path.join(HERE, "ev")
os.makedirs(OUT, exist_ok=True)


def image(name):
    path = os.path.join(EV, name)
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def screenshot(src, width, height, alt):
    return (
        f'<div style="width:{width}px;height:{height}px;flex:none;border-radius:30px;'
        f'padding:8px;background:rgba(255,255,255,.16);box-shadow:0 28px 65px rgba(0,0,0,.48)">'
        f'<img src="{src}" alt="{alt}" crossorigin="anonymous" '
        'style="display:block;width:100%;height:100%;object-fit:contain;border-radius:22px;background:#111">'
        '</div>'
    )


def callout(label, copy):
    return (
        '<div style="padding:0 0 20px;border-bottom:2px solid rgba(255,255,255,.14)">'
        f'<div class="eyebrow" style="font-size:32px">{label}</div>'
        f'<div class="body" style="margin-top:10px;color:#fff">{copy}</div></div>'
    )


def meta(slug, title, lane, page_title):
    return {
        "slug": slug,
        "title": title,
        "lane": lane,
        "page_title": page_title,
        "folder": f"outputs/tips/{slug}_{DATE}.html",
        "id": f"tip-{slug}-{DATE.replace('-', '')}",
    }


def finish(m, slides, tabs, notes, xmap=None):
    doc = page(m, slides, tabs, notes)
    doc = doc.replace("Tips week pack 2026-10-09", "Tips week pack 2026-10-16")
    old_download = (
        "const a=document.createElement('a');a.href=URL.createObjectURL(blob);"
        "a.download=POST_SLUG+'_pipeline.json';a.click();URL.revokeObjectURL(a.href);"
    )
    new_download = (
        "const a=document.createElement('a');const href=URL.createObjectURL(blob);"
        "a.href=href;a.download=POST_SLUG+'_pipeline.json';document.body.appendChild(a);"
        "a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(href),1000);"
    )
    if old_download not in doc:
        raise RuntimeError("Expected pipeline download code was not found.")
    doc = doc.replace(old_download, new_download)
    path = os.path.join(ROOT, m["folder"])
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    pack[m["slug"]] = {
        "meta": m,
        "slides": len(slides),
        "tabs": {tid: text for tid, _label, text in tabs},
        "lane": m["lane"],
        "xmap": xmap or {"X1": 1},
        "notes": notes,
    }
    print(f"Wrote {m['folder']} ({len(slides)} slide(s))")


pack = {}
caraway = image("caraway_after.png")
v1ce = image("v1ce_live.png")
owala = image("owala_live.png")
bebemoss = image("bebemoss_widget.png")
tapro = image("tapro_search_overlap.png")
kyte = image("kyte_size_button.png")

# Lane A: build breakdown, using the verified portion of the Caraway concept build.
m = meta("caraway-product-page-proof-before-scroll", "Price and proof before the scroll",
         "A Build breakdown", "Caraway: price and proof before the scroll")
slide = shell(f"""
<div class="h" style="font-size:88px">Price first.<br>Proof too.</div>
<div style="flex:1;min-height:0;display:flex;align-items:center;gap:44px;margin-top:28px">
  {screenshot(caraway, 440, 640, "Caraway product page concept with price, reviews, benefits, shipping and returns")}
  <div style="flex:1;min-width:0;display:flex;flex-direction:column;justify-content:space-evenly;gap:22px">
    {callout("PRICE + RATINGS", "$125. 4.7 stars.<br>18,886 reviews.")}
    {callout("PRODUCT DETAILS", "Four benefit chips under the pan photo.")}
    {callout("DELIVERY", "Free shipping, returns,<br>30-day trial.")}
  </div>
</div>
<div class="cap" style="margin-top:18px">Unofficial Caraway concept rebuild. Not client work.</div>
""", 1, 1)
caraway_li = """This Caraway concept rebuild puts useful product details on the first screen.

The first screen shows the $125 price, 4.7 stars from 18,886 reviews, four product benefits, shipping, returns and a 30-day trial.

This is an unofficial concept rebuild, not client work.

#Shopify #CRO #ProductPage"""
caraway_x = "This Caraway concept puts $125, 4.7 stars from 18,886 reviews, four product benefits, shipping, returns and a 30-day trial on one screen. Unofficial redesign, not client work."
finish(m, [slide], [
    ("tab-linkedin", "LinkedIn", caraway_li),
    ("tab-x-image", "X (this image)", caraway_x),
], "<p><b>Lane A, build breakdown.</b> The source is the Caraway concept rebuild. The crop keeps the visible price, rating, benefit chips and shipping terms, and excludes an unverified testimonial. Caraway is not a client.</p><p>Evidence: <code>outputs/cro-fixes/caraway/_assets/phones/caraway_after_v2_phone.png</code>, captured in the concept build.</p>")

# Lane B: found page, using a fresh live V1CE capture from October 15.
m = meta("v1ce-tap-card-explains-the-next-step", "V1CE explains the tap before the card",
         "B Found page", "V1CE: explain the tap before the card")
slide = shell(f"""
<div class="h" style="font-size:88px">A tap opens<br>reviews.</div>
<div style="flex:1;min-height:0;display:flex;align-items:center;gap:52px;margin-top:22px">
  {screenshot(v1ce, 420, 720, "V1CE live Tap Review Card product page")}
  <div style="flex:1;min-width:0;display:flex;flex-direction:column;justify-content:center;gap:36px">
    {callout("THE JOB", "A tap opens the review page.")}
    {callout("PROOF", "Trustpilot rating and verified review count sit above the product photo.")}
    <div class="body" style="font-size:34px;color:rgba(255,255,255,.7)">V1CE live page, captured October 15.</div>
  </div>
</div>
""", 1, 1)
v1ce_li = """V1CE tells you what the Tap Review Card does before the product photo.

Tap the card to a customer's phone. Their review page opens. The page also shows a Trustpilot rating and verified review count near the top.

The value is easy to understand before someone scrolls through the product details. Found on V1CE's live page, captured October 15. V1CE is not a client.

#Shopify #CRO #ProductPage"""
v1ce_x = "V1CE's Tap Review Card page explains the job before the product photo: tap the card and the review page opens. It also shows Trustpilot's 4.4 rating and 1,092 verified reviews near the top."
finish(m, [slide], [
    ("tab-linkedin", "LinkedIn", v1ce_li),
    ("tab-x-image", "X (this image)", v1ce_x),
], "<p><b>Lane B, found page.</b> Fresh live capture from October 15. The screen shows the Tap Review Card title, the product explanation, a Trustpilot rating and review count, and the product image. V1CE is a public example, not a client.</p><p>Evidence: <code>https://v1ce.co/</code>, captured locally at <code>.ai-workflow/tips-weekly-2026-10-16/ev/v1ce_live.png</code>.</p>")

# Lane C: six-slide V4 carousel with three dated mobile-audit examples.
m = meta("three-mobile-checks-before-you-ship", "Three mobile checks before you ship",
         "C Save-worthy list (V4 carousel)", "Three mobile checks before you ship")
N = 6
cover = f"""
<div style="position:absolute;inset:0;background:
  radial-gradient(120% 80% at 0% 0%,rgba(255,149,0,.52),transparent 55%),
  radial-gradient(90% 70% at 100% 100%,rgba(123,47,190,.70),transparent 60%),
  radial-gradient(70% 60% at 100% 10%,rgba(224,64,160,.30),transparent 60%),#0B0B0D"></div>
<div class="dots"></div>
<svg width="1080" height="1350" style="position:absolute;inset:0">
  <rect x="48" y="48" width="984" height="1254" rx="6" stroke="rgba(255,255,255,.55)" stroke-width="3" fill="none" stroke-opacity=".6"/>
  <path d="M48 110V48h62M970 48h62v62M1032 1240v62h-62M110 1302H48v-62" stroke="#fff" stroke-width="6" fill="none"/>
</svg>
"""
cards = [
    ("BEBEMOSS", bebemoss, 240, 252),
    ("TAPRO", tapro, 360, 415),
    ("KYTE BABY", kyte, 240, 242),
]
card_html = "".join(
    f'<div style="display:flex;flex-direction:column;align-items:center;gap:14px">'
    f'<div class="eyebrow" style="font-size:30px">{label}</div>'
    f'<div style="width:{w}px;height:{h}px;padding:6px;border-radius:24px;background:rgba(255,255,255,.9);box-shadow:0 22px 46px rgba(0,0,0,.5)">'
    f'<img src="{src}" alt="{label} mobile audit evidence" crossorigin="anonymous" '
    'style="display:block;width:100%;height:100%;object-fit:contain;border-radius:18px;background:#fff"></div></div>'
    for label, src, w, h in cards
)
slides = [
    f"""<div class="slide" data-n="1">{cover}
<div class="in" style="padding-top:90px">
  <div class="h" style="font-size:108px">Phone QA.<br>3 checks.</div>
  <div class="body" style="margin-top:28px;color:#fff">A quick phone pass, built from real audit screens.</div>
  <div style="flex:1;min-height:0;display:flex;align-items:center;justify-content:space-between;gap:24px;margin-top:25px">{card_html}</div>
  <div class="cap" style="margin-top:8px">Public-site audits. Not client work.</div>
</div>{'<div class="foot"><span><b>@koolestpro</b> | Shopify CRO &amp; UX</span><span class="count">1 / 6</span></div>'}</div>""",
    shell(f"""
<div class="eyebrow">BEBEMOSS</div>
<div class="h" style="font-size:90px;margin-top:22px">Offer tab<br>hides price.</div>
<div style="flex:1;min-height:0;display:flex;align-items:center;justify-content:center;margin-top:24px">
  {screenshot(bebemoss, 560, 585, "Bebemoss collection screenshot with discount tab covering a product name and price")}
</div>
<div class="body" style="margin-top:10px;color:#fff">Collection page audit.</div>
""", 2, N, wm_icon=None),
    shell(f"""
<div class="eyebrow">TAPRO</div>
<div class="h" style="font-size:90px;margin-top:22px">Search icon<br>over text.</div>
<div style="flex:1;min-height:0;display:flex;align-items:center;justify-content:center;margin-top:24px">
  {screenshot(tapro, 740, 680, "TAPro mobile homepage screenshot showing a search icon overlapping promo headline text")}
</div>
<div class="body" style="margin-top:10px;color:#fff">The audit found a duplicate search icon.</div>
""", 3, N),
    shell(f"""
<div class="eyebrow">KYTE BABY</div>
<div class="h" style="font-size:90px;margin-top:22px">Looks<br>disabled.</div>
<div style="flex:1;min-height:0;display:flex;align-items:center;justify-content:center;gap:50px;margin-top:20px">
  {screenshot(kyte, 560, 565, "Kyte Baby size selector and gray button that looked disabled")}
  <div class="body" style="flex:1;color:#fff">The audit found it was tappable. The visual state was the problem.</div>
</div>
<div class="cap" style="margin-top:10px">Product page audit.</div>
""", 4, N),
    shell("""
<div class="h" style="font-size:96px">Tap.<br>Then check.</div>
<div style="flex:1;min-height:0;display:flex;flex-direction:column;justify-content:space-evenly;margin-top:36px">
  <div style="display:flex;align-items:center;gap:28px"><span class="eyebrow" style="font-size:40px;color:#FF9500">01</span><span class="body" style="color:#fff">Scroll to the product grid.</span></div>
  <div style="display:flex;align-items:center;gap:28px"><span class="eyebrow" style="font-size:40px;color:#FF9500">02</span><span class="body" style="color:#fff">Check what overlaps the choice.</span></div>
  <div style="display:flex;align-items:center;gap:28px"><span class="eyebrow" style="font-size:40px;color:#FF9500">03</span><span class="body" style="color:#fff">Tap the option and watch its state.</span></div>
</div>
""", 5, N),
    cta_slide(6, N, "Need a<br>CRO audit?", "I can review the page your shoppers see.", "Start with the first screen.")
        .replace("Get a CRO audit &#8594;", "Use this checklist on your store &#8594;")
        .replace("koolestpro.com/services/cro-audit", "Save this for your next mobile review."),
]
carousel_li = """Three things from public-site audits:

Bebemoss: a fixed discount tab covers a toy's name and price in the collection grid.
TAPro: a search icon sits on its promo headline, while the header already has another.
Kyte Baby: the size button looked disabled, though the audit found it was tappable.

Different pages. Same useful habit: scroll to where the decision happens, then tap. Don't stop at the page load.

These are public-site audit examples, not client work.

#Shopify #CRO #MobileUX"""
carousel_cover = "Three mobile checks from public-site audits. Not client work."
carousel_ig = """Three mobile checks before you ship:

Bebemoss: a discount tab covers a product name and price.
TAPro: a search icon overlaps the promo headline.
Kyte Baby: the size button looked disabled, but it was tappable.

Scroll to the decision. Tap the control. Watch what changes.

Public-site audits, not client work.

#ShopifyDesign #CRO #eCommerce #ShopifyDeveloper #ConversionOptimization #WebDesign #Shopify #UXDesign"""
x1 = "Bebemoss's fixed 10% tab covers a toy's name and price in the collection grid."
x2 = "TAPro's mobile screenshot shows a search icon sitting on the promo headline. The audit identified it as a duplicate control."
x3 = "Kyte Baby's size button looked disabled, but the audit found it was tappable. The visual state is the problem."
finish(m, slides, [
    ("tab-linkedin-cover", "LinkedIn (cover only)", carousel_cover),
    ("tab-linkedin", "LinkedIn", carousel_li),
    ("tab-ig", "Instagram", carousel_ig),
    ("tab-x1", "X 1 (Bebemoss)", x1),
    ("tab-x2", "X 2 (TAPro)", x2),
    ("tab-x3", "X 3 (Kyte Baby)", x3),
], "<p><b>Lane C, six-slide V4 carousel.</b> One audit screenshot per finding, followed by a phone QA sequence.</p><p>Evidence: Bebemoss audit, August 18, 2026, <code>outputs/audits/bebemoss_toys-collection_audit.md</code>; TAPro audit, August 31, 2026, <code>outputs/audits/tapro_audit.md</code>; Kyte Baby audit, September 20, 2026, <code>outputs/audits/kytebaby_sleep-bag-oat-1-0-pdp_audit.md</code>. All are public-site audits, not client work. Dates are kept here for provenance only.</p>", {"X1": 2, "X2": 3, "X3": 4})

# Lane D: expert remix of NN/g guidance, grounded in a fresh Owala product-page capture.
m = meta("owala-product-page-answers-fast", "Owala: answer the product questions fast",
         "D Expert remix", "Owala: answer the product questions fast")
slide = shell(f"""
<div class="h" style="font-size:90px">Price.<br>Color choice.</div>
<div class="body" style="margin-top:18px;color:#fff">Nielsen Norman Group's product-page guidance, on an Owala screen.</div>
<div style="flex:1;min-height:0;display:flex;align-items:center;gap:44px;margin-top:22px">
  {screenshot(owala, 410, 840, "Owala FreeSip mobile product page with price, reviews, colors and add to cart")}
  <div style="flex:1;min-width:0;display:flex;flex-direction:column;justify-content:space-evenly;gap:18px">
    {callout("PRODUCT", "FreeSip is named beside its price.")}
    {callout("PROOF", "The page shows 34,332 reviews.")}
    {callout("CHOICE", "Color options are visible on the same screen.")}
    <div class="cap">Source: Nielsen Norman Group, "Ecommerce Product Pages".</div>
  </div>
</div>
""", 1, 1)
owala_li = """Product pages should put key answers where shoppers can find them.

Nielsen Norman Group's ecommerce product-page guidance makes that point. Owala's live FreeSip page gives a useful example: the product name, $39.99 price, 34,332 reviews and color choices appear in one phone view.

That is a screen observation, not a conversion claim. Owala is not a client.

Source: Nielsen Norman Group, "Ecommerce Product Pages".
#Shopify #CRO #ProductPage"""
owala_x = "NN/g says product pages should help shoppers find information quickly. Owala's FreeSip page shows the name, $39.99 price, 34,332 reviews and color options in one mobile view. Not a conversion claim."
finish(m, [slide], [
    ("tab-linkedin", "LinkedIn", owala_li),
    ("tab-x-image", "X (this image)", owala_x),
], "<p><b>Lane D, expert remix.</b> Remixes Nielsen Norman Group's <a href=\"https://www.nngroup.com/articles/ecommerce-product-pages/\">Ecommerce Product Pages</a> guidance about answering product questions quickly. The Owala screenshot is a live public-page example, captured October 15. Owala is not a client.</p>")

with open(os.path.join(HERE, "week_pack.json"), "w", encoding="utf-8") as f:
    json.dump(pack, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(pack)} post records to .ai-workflow/tips-weekly-2026-10-16/week_pack.json")
