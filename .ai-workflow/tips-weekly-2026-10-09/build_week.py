#!/usr/bin/env python3
"""Tips week pack 2026-10-09: four posts across four lanes (A, C, E, B).

Run from the project root:  python3 .ai-workflow/tips-weekly-2026-10-09/build_week.py
Writes outputs/tips/<slug>_2026-10-09.html for each post. Evidence images are embedded
as data URIs (crops in .ai-workflow/tips-weekly-2026-10-09/ev/, made by crops.py).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import O, P, M, icon, img64, shell, cta_slide, page

DATE = "2026-10-09"
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = os.path.join(ROOT, "outputs", "tips")
os.makedirs(OUT, exist_ok=True)
POSTS = {}


def meta(slug, title, lane, page_title):
    return dict(slug=slug, title=title, lane=lane, page_title=page_title,
                folder=f"outputs/tips/{slug}_{DATE}.html", id=f"tip-{slug}-{DATE.replace('-', '')}")


def head_row(label, ico):
    """Plain eyebrow + icon badge. No gradient pill, and never a post-type name (Ridwan, 2026-10-09)."""
    return f'<div class="row"><div class="eyebrow">{label}</div><div class="icon">{icon(ico, 60)}</div></div>'


# =====================================================================================
# POST 1  Lane A, build breakdown: Material Kitchen homepage first screen (single image)
# =====================================================================================
m1 = meta("materialkitchen-first-screen-build-breakdown", "Same photo. New first screen.",
          "Lane A: Build breakdown", "Material Kitchen first screen: build breakdown")


def phone(src, w, h, label, accent):
    lab_style = f"color:{O}" if accent else "color:rgba(255,255,255,.75)"
    return f'''<div style="display:flex;flex-direction:column;align-items:center;gap:18px">
  <div class="eyebrow" style="font-size:34px;{lab_style}">{label}</div>
  <div style="width:{w}px;height:{h}px;border-radius:30px;padding:8px;background:{"linear-gradient(160deg,%s,%s)" % (O, P) if accent else "rgba(255,255,255,.18)"}">
    <div style="width:100%;height:100%;border-radius:24px;overflow:hidden;background:#FBF8EF">
      <img src="{src}" style="width:100%;height:auto;display:block"></div></div></div>'''


def callout(n, text):
    return f'''<div style="display:flex;align-items:center;gap:18px">
  <div style="width:58px;height:58px;flex:none;border-radius:50%;background:{O};color:#0B0B0D;font-family:'DM Sans';font-weight:700;font-size:32px;display:flex;align-items:center;justify-content:center">{n}</div>
  <div style="font-size:32px;font-weight:700;line-height:1.15">{text}</div></div>'''


def marker(n, top):
    return (f'<div style="position:absolute;right:-26px;top:{top}px;width:56px;height:56px;border-radius:50%;background:{O};'
            f'color:#0B0B0D;font-family:"DM Sans";font-weight:700;font-size:30px;text-align:center;line-height:46px;'
            f'border:5px solid #0B0B0D">{n}</div>')


# after phone: 300x654 inner img area from crop 780x1700 -> scale 0.3744 (8px padding each side)
AW, AH = 339, 720
sc = (AW - 16) / 780
after = phone(img64("mk_after.jpg"), AW, AH, "AFTER", True)
# numbered markers are drawn into ev/mk_after.jpg (html2canvas misplaces absolutely positioned text)
before = phone(img64("mk_before.jpg"), 258, 500, "BEFORE", False)
p1 = shell(f"""
  <div class="h" style="font-size:90px">Same photo.<br>New <span class="o">fold.</span></div>
  <div style="flex:1;min-height:0;display:flex;align-items:flex-end;gap:26px;margin-top:40px">
    <div style="opacity:.92">{before}</div>
    {after}
    <div style="flex:1;display:flex;flex-direction:column;gap:44px;padding:0 0 90px 16px">
      {callout(1, "A 5-star review line")}{callout(2, "Their own guarantees as chips")}{callout(3, "A best seller with its price")}
    </div>
  </div>
  <div class="body" style="margin-top:30px;color:#fff">All of it above the scroll. Same brand.</div>
  <div class="cap" style="margin-top:12px">materialkitchen.com, July 2026. Unsolicited redesign, not a client.</div>
""", 1, 1, wm_icon="utensils")

t1 = [
    ("tab-linkedin", "LinkedIn", """Same hero photo. Different first screen.

Left is Material Kitchen's homepage on a phone, the way I captured it in July. Right is the first screen I rebuilt for it.

The original has a lovely photo, a headline and one green button. Then roughly 400px of empty cream before anything else shows up. No rating, no price. Their real 5-star reviews were sitting about two-thirds of the way down the page.

I made three moves:
1. A 5-star review line right under the subhead.
2. The promises from their own announcement bar (guaranteed for life, 30-day trial, free shipping over $100) turned into chips.
3. Their best seller, The Trio of Knives, with its price ($195, was $225) and an Add to cart, still above the fold.

The photo and the brand stayed. What changed is how much a first-time visitor can decide before they scroll.

This was an unsolicited redesign. Material Kitchen isn't a client.

Before Black Friday traffic lands, open your homepage on your phone and list the proof you already have further down. Move one piece up.

Want a second pair of eyes on your first screen? koolestpro.com/services/cro-audit

#Shopify #CRO #ShopifyDesign #Ecommerce #HomepageDesign"""),
    ("tab-hook", "Hook", """Same photo. Different first screen.

Material Kitchen's homepage had a great hero and then 400px of nothing. I moved a review line, their own guarantees and a priced best seller above the fold.

What's sitting below your fold that should be above it?"""),
    ("tab-x-image", "X (this image)", """Same hero photo, different first screen.

Material Kitchen's homepage (left): photo, headline, button, then ~400px of empty space.

My rebuild (right): a review line, their own guarantees as chips, and a best seller with its price.

Unsolicited redesign, not a client."""),
]
POSTS[m1["slug"]] = (m1, [p1], t1, """<p><b>Lane A, build breakdown.</b> Evidence: Ridwan's own audit and rebuild, <code>outputs/audits/materialkitchen_homepage_audit.md</code>, before <code>outputs/cro-fixes/materialkitchen_before_popup.png</code> (first screen after the modal is closed), after <code>outputs/cro-fixes/materialkitchen_after_phone.png</code>.</p>
<p><b>Check before posting:</b> the review quote inside the rebuild screenshot ("It cut through tomatoes...") is not quoted in the audit file. The audit only confirms real 5-star quotes exist lower on the page. Confirm it is a real Material Kitchen review, or re-shoot the rebuild with a quote you can verify.</p>""")

# =====================================================================================
# POST 2  Lane C, save-worthy list as a 6-slide V4 carousel: 4 first-screen leaks
# =====================================================================================
m2 = meta("first-screen-leaks-before-bfcm", "4 first-screen leaks to fix before Black Friday",
          "Lane C: Save-worthy list (V4 carousel)", "4 first-screen leaks: carousel")
N2 = 6
glyph = 'stroke="rgba(255,255,255,.55)" stroke-width="3" fill="none" stroke-linecap="round"'


def tilt(src, w, deg, x, y, z=1):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({deg}deg);z-index:{z};'
            f'border-radius:22px;padding:6px;background:rgba(255,255,255,.9);box-shadow:0 30px 60px rgba(0,0,0,.55)">'
            f'<img src="{src}" style="display:block;width:100%;border-radius:17px"></div>')


cover_bg = f"""
<div style="position:absolute;inset:0;background:
  radial-gradient(120% 80% at 0% 0%,rgba(255,149,0,.55),transparent 55%),
  radial-gradient(90% 70% at 100% 100%,rgba(123,47,190,.75),transparent 60%),
  radial-gradient(70% 60% at 100% 10%,rgba(224,64,160,.35),transparent 60%),#0B0B0D"></div>
<div class="dots"></div>
<svg width="1080" height="1350" style="position:absolute;inset:0">
  <rect x="48" y="48" width="984" height="1254" rx="6" {glyph} stroke-opacity=".6"/>
  <path d="M48 110V48h62M970 48h62v62M1032 1240v62h-62M110 1302H48v-62" stroke="#fff" stroke-width="6" fill="none"/>
</svg>
{tilt(img64("gainful_offers.jpg"), 470, 6, 548, 150, 2)}
{tilt(img64("obvi_widget.jpg"), 400, -5, 600, 470, 3)}"""
s21 = f"""<div class="slide" data-n="1">{cover_bg}<div class="in" style="padding:140px 96px 180px">
  <div class="h" style="font-size:420px;letter-spacing:-14px;line-height:.8;margin-top:10px;color:{O}">4</div>
  <div style="flex:1"></div>
  <div class="h" style="font-size:124px;letter-spacing:-5px;line-height:.95">FIRST<br>SCREEN<br>LEAKS</div>
  <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-top:38px">
    <div class="body" style="color:#fff;font-size:42px">Fix them before<br>Black Friday traffic lands.</div>
    <div style="font-family:'Syne';font-weight:800;font-size:36px;letter-spacing:3px;white-space:nowrap;padding-bottom:6px">SWIPE &#8594;</div></div>
</div><div class="foot" style="justify-content:center"><span><b>@koolestpro</b> | Shopify CRO &amp; UX</span></div></div>"""


def leak(n, slide_n, ico, head_html, ev, source, body, hsize=96):
    return shell(f"""
  {head_row(f"LEAK #{n}", ico)}
  <div class="h" style="font-size:{hsize}px;margin-top:40px">{head_html}</div>
  <div class="card" style="flex:1;margin-top:40px;padding:22px;background:#F4F1EC;border-color:rgba(255,149,0,.55);display:flex;align-items:center;justify-content:center">
    <img src="{img64(ev)}" style="display:block;width:100%;height:auto;border-radius:18px"></div>
  <div class="cap" style="margin-top:14px">{source}</div>
  <div class="body" style="margin-top:18px">{body}</div>
""", slide_n, N2, wm_icon=ico)


s22 = leak(1, 2, "ticket-percent", 'Two offers.<br>One <span class="o">screen.</span>', "gainful_offers.jpg",
           "gainful.com, captured Aug 2026", "25% to subscribe. 25% with a code. Which one do I get?")
s23 = leak(2, 3, "heading-1", 'Back in stock<br>is not a<br><span class="o">headline.</span>', "obvi_headline.jpg",
           "myobvi.com, captured Aug 2026", "Say what it is and what it does. Then the restock note.", hsize=88)
s24 = leak(3, 4, "accessibility", 'An app sits<br>on your<br><span class="o">button.</span>', "obvi_widget.jpg",
           "myobvi.com, captured Aug 2026", "Test the first screen on a real phone, every app on.", hsize=92)
s25 = leak(4, 5, "badge-dollar-sign", 'Your price<br>is <span class="o">whispering.</span>', "gainful_price.jpg",
           "gainful.com, captured Aug 2026", "Give the price its own line by the button.", hsize=88)
s26 = cta_slide(6, N2, 'Which leak<br>is on <span class="o">yours?</span>',
                "I audit Shopify first screens on a real phone, before the sale weeks.", "Save this before Black Friday.")

t2 = [
    ("tab-linkedin", "LinkedIn", """4 first-screen leaks I found on real Shopify stores. All fixable before Black Friday.

Every slide is a real screenshot from audits I ran in August, so the live pages may have changed since.

1. Two offers on one screen. Gainful showed "Subscribe and Save 25%" in the top bar and "New Customers: 25% off w/ code FLAV25" right under the logo. That's two different 25% deals before you've seen a product. Pick one for the first screen.

2. A headline that isn't one. Obvi's biggest text was "BACK IN STOCK!". That only helps someone who already wanted the product. Say what it is and what it does, then add the restock note.

3. An app sitting on the button. On mobile, Obvi's accessibility widget sat on top of the SHOP NOW button. Tap that corner and you get a settings panel instead of the store. Check your page with every app switched on.

4. The quietest price on the page. Gainful's "14 Servings | $31.47" was small gray text next to the stars, on a page where every choice changes the total. Give the price its own line near the button.

None of these needs a redesign. They need someone to look at the first screen on an actual phone.

Want me to look at yours before the sale weeks? koolestpro.com/services/cro-audit

#Shopify #CRO #BlackFriday #Ecommerce #ShopifyTips"""),
    ("tab-hook", "Hook", """4 first-screen leaks from real Shopify stores.

Two offers fighting. A headline that says nothing. An app on top of the buy button. A price nobody sees.

Which one is on yours?"""),
    ("tab-twitter-thread", "X Thread", """1/ 4 first-screen leaks I found auditing real Shopify stores. Each one is a screenshot. Fix them before Black Friday traffic lands:

2/ Two offers, one screen. Gainful showed "Subscribe and Save 25%" up top and "New Customers: 25% off w/ code FLAV25" under the logo. Two 25% deals before any product. Keep one.

3/ A headline that isn't one. Obvi's biggest text was "BACK IN STOCK!". Useful only if you already wanted it. Lead with what it is and what it does.

4/ An app on the button. Obvi's accessibility widget sat on top of SHOP NOW on mobile. Tap the corner and a settings panel opens instead of the store. Test with every app on.

5/ The quietest price on the page. Gainful's "14 Servings | $31.47" was small gray text beside the stars. Give the price its own line near the button.

6/ All four are from August audits, so the pages may have changed. The check still works: open your store on a phone and look at the first screen only."""),
    ("tab-twitter-angles", "X Singles", """X1 (slide 2, two offers)
Two 25% deals before you've seen a product.

"Subscribe and Save 25%" up top. "New Customers: 25% off w/ code FLAV25" under the logo.

Which one do I get? A shopper shouldn't have to ask. One offer per first screen.

X2 (slide 4, widget on the button)
Obvi's accessibility widget sat right on top of the SHOP NOW button on mobile.

Tap the corner and you get a settings panel instead of the store.

Check your first screen with every app switched on. Apps move things around.

X3 (slide 5, quiet price)
The price was the quietest thing on this screen.

"14 Servings | $31.47" in small gray type next to the stars, on a page where every choice changes the total.

Give the price its own line, close to the button."""),
    ("tab-ig", "Instagram", """4 first-screen leaks I found on real Shopify stores. Fix them before Black Friday.

1. Two offers on one screen. Two different 25% deals before you see a product. Keep one.
2. "Back in stock" as the headline. Say what it is and what it does first.
3. An app widget sitting on top of the buy button on mobile. Test with every app on.
4. A price in small gray type. Give it its own line near the button.

Screenshots are from audits I ran in August, so the live pages may have changed.

Save this for your pre-sale checklist. Follow @koolestpro for more Shopify CRO.

#Shopify #ShopifyStore #CRO #BlackFriday #Ecommerce #ConversionRateOptimization #ShopifyDesign #UXDesign #OnlineStore #ShopifyTips"""),
]
POSTS[m2["slug"]] = (m2, [s21, s22, s23, s24, s25, s26], t2, """<p><b>Lane C, save-worthy list, shipped as the week's one V4 carousel.</b> Evidence: Ridwan's own audits <code>outputs/audits/gainful_customize-your-protein_audit.md</code> (findings 1 and 2) and <code>outputs/audits/obvi_homepage_audit.md</code> (headline + accessibility widget findings), screenshots <code>outputs/cro-fixes/_gainful_before_raw.png</code> and <code>_obvi_before_raw.png</code>. Orange boxes added by Koolestpro. Both are real brands, audited unsolicited, not clients.</p>""")

# =====================================================================================
# POST 3  Lane E, sourced take: Baymard extra costs (single image)
# =====================================================================================
m3 = meta("extra-costs-top-checkout-killer", "40% of checkout quitters blame extra costs",
          "Lane E: Sourced take", "Extra costs: sourced take")
reasons = [("Extra costs too high", "shipping, tax, fees", 40), ("Delivery too slow", "", 20),
           ("Didn't trust the site with a card", "", 19), ("Had to create an account", "", 18),
           ("Checkout too long or complicated", "", 17)]
bars = "".join(f'''<div>
  <div class="row" style="margin-bottom:10px"><div style="font-size:32px;font-weight:{700 if i == 0 else 500};color:{"#fff" if i == 0 else "rgba(255,255,255,.75)"}">{a}{(' <span style="color:rgba(255,255,255,.5);font-weight:500">(' + b + ')</span>') if b else ''}</div>
  <div style="font-family:Syne;font-weight:800;font-size:36px;color:{O if i == 0 else "rgba(255,255,255,.75)"}">{v}%</div></div>
  <div style="height:{30 if i == 0 else 20}px;border-radius:12px;background:rgba(255,255,255,.07)"><div style="height:100%;width:{v * 2.3:.0f}%;border-radius:12px;background:{f"linear-gradient(90deg,{O},{M})" if i == 0 else "rgba(255,255,255,.38)"}"></div></div></div>'''
               for i, (a, b, v) in enumerate(reasons))
p3 = shell(f"""
  <div class="row" style="align-items:flex-start"><div class="h" style="font-size:240px;letter-spacing:-10px;line-height:.82;color:{O}">40%</div><div class="icon">{icon("receipt", 60)}</div></div>
  <div class="h" style="font-size:60px;letter-spacing:-2px;line-height:1.08;margin-top:22px">of checkout quitters<br>blame <span class="o">extra costs.</span></div>
  <div class="card" style="flex:1;margin-top:36px;padding:36px 44px;display:flex;flex-direction:column;justify-content:space-between">{bars}</div>
  <div class="body" style="margin-top:26px;color:#fff">Show shipping on the product page.</div>
  <div class="cap" style="margin-top:10px">Source: Baymard Institute, US shoppers, updated Sept 2025</div>
""", 1, 1, wm_icon="receipt")

t3 = [
    ("tab-linkedin", "LinkedIn", """40% of US shoppers who quit at checkout say the extra costs were too high. Shipping, tax, fees.

That's from Baymard Institute's checkout abandonment research (page updated September 2025, with "just browsing" answers left out). It's the top reason by a wide margin. Slow delivery is second at 20%.

Most of those costs exist long before anyone opens the cart. You already know your shipping rate, your free-shipping threshold and your duties. The shopper just meets them too late.

So a lot of the fix is timing. Show the cost where people decide, on the product page and in the cart, instead of on step three of checkout.

Ways I see stores do it well:
A shipping line right next to the price.
A free-shipping threshold with a progress bar in the cart.
Duties and taxes stated up front for international orders.

Black Friday brings a lot of first-time buyers who don't know your shipping policy yet. Tell them before checkout does.

Source: baymard.com/lists/cart-abandonment-rate

#Shopify #CRO #Checkout #Ecommerce #BlackFriday"""),
    ("tab-hook", "Hook", """The top reason people quit checkout isn't the checkout. It's the shipping cost they only meet there.

40% of US checkout abandoners say extra costs were too high (Baymard Institute).

Where does your store first show the shipping cost?"""),
    ("tab-x-image", "X (this image)", """40% of US shoppers who abandon at checkout say the extra costs were too high: shipping, tax, fees.

That's the #1 reason, double slow delivery (20%). Source: Baymard Institute.

Show the cost on the product page, not on step three of checkout."""),
]
POSTS[m3["slug"]] = (m3, [p3], t3, """<p><b>Lane E, sourced take.</b> Every number on the image comes from Baymard Institute, <a href="https://baymard.com/lists/cart-abandonment-rate" style="color:#FF9500">baymard.com/lists/cart-abandonment-rate</a> (page last updated 22 Sept 2025, read 9 Oct 2026): reasons for abandonment during checkout, US online shoppers, "just browsing" excluded. 40% extra costs, 20% delivery too slow, 19% didn't trust the site with card info, 18% account creation required, 17% checkout too long or complicated. No Koolestpro result is claimed.</p>""")

# =====================================================================================
# POST 4  Lane B, found page: Allbirds price + shipping chip (single image)
# =====================================================================================
m4 = meta("allbirds-shipping-next-to-price", "Allbirds puts shipping next to the price",
          "Lane B: Found page", "Allbirds found page")
p4 = shell(f"""
  <div class="h" style="font-size:92px">Shipping sits<br>by the <span class="o">price.</span></div>
  <div class="card" style="flex:1;margin-top:40px;padding:0;background:#ECE9E3;border:4px solid rgba(255,149,0,.7);display:flex;align-items:center">
    <img src="{img64("allbirds_price.jpg")}" style="display:block;width:100%;height:auto"></div>
  <div class="body" style="margin-top:28px;color:#fff">Allbirds answers the top checkout worry before you pick a size.</div>
  <div class="cap" style="margin-top:10px">allbirds.com, mobile, captured 9 Oct 2026. Not a client.</div>
""", 1, 1, wm_icon="truck")

t4 = [
    ("tab-linkedin", "LinkedIn", """Allbirds puts the shipping next to the price.

On the Men's Tree Runner page on mobile, the price reads "$100 + FREE SHIPPING", with the shipping as a chip right beside the number, above the product photo. I captured it today, 9 October.

Why it works: extra costs are the most common reason people quit checkout. Baymard's research puts it at 40% of US checkout abandonments. Allbirds answers that question before you've even picked a size.

They say it three times on the same screen: the announcement bar, the price chip, and a line under the size button. Each one sits where a decision happens.

If you offer free shipping over a threshold, say it next to the price. If you charge for shipping, show the rate there too. A cost people can see early is easier to accept than one that shows up at step three.

Allbirds isn't a client. I just think this one is worth copying.

#Shopify #CRO #ProductPage #Ecommerce"""),
    ("tab-hook", "Hook", """One chip next to the price: "+ FREE SHIPPING".

Allbirds answers the top checkout worry on the product page, before you pick a size.

Does your price tell me what I'll actually pay?"""),
    ("tab-x-image", "X (this image)", """Allbirds puts "+ FREE SHIPPING" right next to the $100 price on its Tree Runner page.

Extra costs are the #1 reason shoppers quit checkout (Baymard: 40% of US abandonments). This answers it before you've picked a size.

Not a client. Worth copying."""),
]
POSTS[m4["slug"]] = (m4, [p4], t4, """<p><b>Lane B, found page.</b> Live capture of <a href="https://www.allbirds.com/products/mens-tree-runners" style="color:#FF9500">allbirds.com/products/mens-tree-runners</a>, 390&times;844 mobile viewport, 9 Oct 2026 (email modal and cookie banner dismissed first). Orange ring added by Koolestpro. Credited brand, never implied as a client. Pairs with the Baymard sourced take; schedule them at least a day apart.</p>""")


for slug, (mt, slides, tabs, notes) in POSTS.items():
    path = os.path.join(ROOT, mt["folder"])
    open(path, "w").write(page(mt, slides, tabs, notes))
    print(path, len(slides), "slides")

json.dump({s: {"meta": v[0], "tabs": {t[0]: t[2] for t in v[2]}, "slides": len(v[1])} for s, v in POSTS.items()},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "week_pack.json"), "w"), indent=1)
