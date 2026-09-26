#!/usr/bin/env python3
"""One-off backfill: queue the 4 remaining Kura pages (pdp, advertorial,
listicle, post-purchase) using their already-hosted Cloudinary video assets
and the captions cached from replo-rebuilds. Custom cadence per Ridwan
2026-07-21: LinkedIn+Instagram 1 page every 2 weeks, Twitter 1 post every 3
days. No local HTML/companion page exists for these (video-only, Cloudinary-
hosted) so this bypasses harvest_content.py/populate_sheet.py and writes
queue rows directly.
"""
import json
import os

ROOT = "/sessions/beautiful-peaceful-bardeen/mnt/koolestpro-cowork-v2"
os.chdir(ROOT)

cloud = json.load(open("kura-cloudinary-assets.json"))
social_path = "kura-social-content.json"
social = json.load(open(social_path))

# LI/IG captions (from assets/_archive/replo-pages-cache-retired/kura-social-content.md)
LI = {
    "pdp": """Before there was a homepage, a listicle, or an advertorial, there was one product page.

I started this portfolio with the hardest page to build well: the product page. It's the page that carries the most weight. It has to introduce the brand, agitate the problem, present the solution, prove it works, kill every objection, and ask for the sale, all without losing the reader halfway down.

KURA's PDP follows a villain/hero structure. The "villain" section names the problem most people never think about: plastic boards that harbor bacteria, wood boards that crack and stain. Then the "hero" section introduces KURA as the upgrade, using 304 stainless steel that's non-porous and dishwasher safe.

From there, a before/after comparison, a 3-step how-it-works block, review cards, three circular trust-stat indicators, a head-to-head comparison table against generic boards, an 8-question FAQ accordion, three trust pillars, and an email capture. Thirteen sections in total, each one a deliberate handoff to the next.

The buy box is sticky on desktop. Star rating sits above the product title. Price is impossible to miss. None of that is decoration. It's conversion architecture.

Built in HTML/CSS/vanilla JS. No page builder. No theme.

Need a store like this built for your brand? DM me.

#ecommerce #productpage #CRO #shopify #replo #webdesign #brandstrategy #uidesign""",
    "advertorial": """Cold traffic lands differently.

Someone who finds your product page from an ad already has their guard up. They know they're being sold to. The headline is a pitch. The bullet points are claims.

An advertorial changes the dynamic entirely. Instead of saying "buy this," it says "let me show you something you didn't know about your kitchen." Instead of a product headline, there's a publication masthead. Instead of benefit bullets, there are paragraphs written in editorial voice, with expert citations, reader case studies, and a sticky product rail that travels alongside the article quietly.

By the time the reader reaches the CTA, they think they've reached their own conclusion.

For KURA, I built the full editorial treatment, published under a fictional site called The Kitchen Standard. Article: "The One Item In Your Kitchen That's Making You Sick."

Opening hook, problem deep dive, discovery moment, product introduction, mechanism explanation, expert authority quote, two customer transformation stories, mid-article CTA, objection handling, final close with urgency, five reader comments for social proof. Every section earns the next.

Built in pure HTML/CSS/JS. Two-column editorial layout. Sticky rail on desktop. Full mobile collapse.

Need a store like this built for your brand? DM me.

#ecommerce #advertorial #CRO #paidtraffic #contentmarketing #replo #shopify""",
    "listicle": """The listicle is one of the most underused pages in eCommerce funnels.

Most brands don't build them. The ones that do usually hand them off to a content writer who treats it like a blog post, no CTA flow, no before/after, no conversion architecture.

A listicle done properly does two things at once. First: it earns organic search traffic on problem-aware queries. Second: it moves those people from awareness to purchase without feeling like a sales pitch.

This is the KURA listicle, built on my li-03 template. The headline: "5 Problems Your Cutting Board Is Causing Right Now." Each problem block follows the same structure: agitate the pain, show what changes, introduce the mechanism. Then the page pivots: transformation strip, social proof, final CTA.

Two-column alternating layout on desktop. Full single-column collapse on mobile. Inline CTAs at the highest-friction moments.

If your store is running paid traffic to a product page and wondering why it doesn't convert, this is the page you're missing.

Need one built for your brand? DM me.

#ecommerce #contentmarketing #CRO #shopify #replo #webdesign #conversionoptimization""",
    "post-purchase": """Everyone optimizes the page before checkout. Almost nobody optimizes the page after it.

Once a customer pays, most stores hand them a default confirmation screen and move on. That's a mistake. The five seconds right after checkout are the highest-trust moment in the entire funnel.

For KURA, the post-purchase page does three jobs at once. First, it confirms the order like a brand moment, not a receipt. Second, it makes a one-time offer, 30% off a second board size, with a live countdown and a genuine one-click add, no new checkout flow. Third, it prevents buyer's remorse before it starts: a 3-step "what happens next" block, social proof, a care guide, and a community email capture.

Post-purchase pages are the most overlooked page type in eCommerce. They're also some of the cheapest revenue on the table, since the traffic is already paid for.

Built in HTML/CSS/vanilla JS. Countdown timer, click feedback, and scroll animations all hand-coded.

Need a store like this built for your brand? DM me.

#ecommerce #postpurchase #CRO #shopify #replo #upsell""",
}

IG = {
    "pdp": """The page that started it all.

Villain section. Hero section. Before/after. Reviews. Trust stats. Comparison table. 8-question FAQ. Sticky buy box.

Everything a real DTC product page needs, built from a $12 AliExpress listing into something that looks like it belongs on a million-dollar brand's storefront.

→ KURA PDP. The flagship build in the portfolio.

Need a store like this? DM me.

#ecommerce #shopify #productpage #CRO #replo #webdesign #uidesign #ecommercedesign""",
    "advertorial": """What if your ad didn't look like an ad?

The KURA advertorial reads like a kitchen health article. It sells like a product page.

Editorial masthead. Pullquotes. Expert citations. A sticky product card that follows the reader down the page. In-article CTAs placed where the persuasion peaks. Fake reader comments at the bottom to seal the close.

The reader thinks they're reading content. They're moving through a conversion funnel.

→ Full build in the portfolio. Need a store like this? DM me.

#ecommerce #advertorial #CRO #paidtraffic #replo #shopify #contentmarketing""",
    "listicle": """Most ecom brands don't have a listicle page.

The ones that do convert cold traffic at a different rate entirely.

A listicle earns the click from search. Then it earns the sale through the read. Problem → solution → transformation → proof → CTA. In that order. Every time.

This is the KURA listicle, "5 Problems Your Cutting Board Is Causing Right Now." Looks editorial. Works like a funnel.

→ Full build in the portfolio. Both views in this clip. Need one? DM me.

#ecommerce #CRO #contentmarketing #replo #shopify #webdesign #conversionoptimization""",
    "post-purchase": """The page nobody builds. The page that pays for itself.

KURA's post-purchase screen: order confirmed, a 30%-off upsell with a live countdown, a 3-step reassurance block, reviews, a care guide, and a community signup.

The customer already bought. This page makes sure they don't regret it, and gives them one easy reason to buy again.

→ Full build in the portfolio. Need one for your store? DM me.

#ecommerce #postpurchase #CRO #shopify #replo #upsell #ecommercedesign""",
}

X = {
    "pdp": {
        "cover": "The PDP is the page that has to do the most work.\n\nIt has to sell the product, kill every objection, and never feel long even though it's long.\n\nKURA's, desktop and mobile, side by side. The template this whole portfolio started from.",
        "laptop": "KURA PDP on desktop.\n\n13 sections: hero, why-KURA, villain, upgrade, before/after, how it works, reviews, trust stats, comparison table, FAQs, trust pillars, email signup.\n\nBuilt to Replo-template quality. Zero page builders.",
        "mobile": "KURA product page, mobile.\n\nSticky buy box, variant selector, mini FAQ above the fold. Villain section, upgrade section, before/after, reviews, all stacked clean with zero layout shift.",
    },
    "advertorial": {
        "cover": "Cold traffic doesn't know they have a problem yet.\n\nThis page tells them. Then solves it. Then asks for the sale.\n\nKURA advertorial, desktop + mobile side by side. This is the page type that makes paid traffic actually work.",
        "laptop": "KURA advertorial on desktop.\n\nTwo-column editorial layout. Sticky product card in the rail. Scroll-triggered fade-ins. Five fake-but-believable reader comments at the bottom for social proof.",
        "mobile": "KURA advertorial on mobile.\n\nEditorial masthead → hook → problem deep dive → product intro → expert quote → user stories → CTA → reader comments.\n\nReads like content. Works like a funnel.",
    },
    "listicle": {
        "cover": "The listicle is one of the most slept-on pages in ecom funnels.\n\nDone right, it earns organic traffic AND converts that traffic. Two jobs. One page.\n\nKURA li-03, both views. Zero libraries. All hand-coded.",
        "laptop": "Listicle on desktop.\n\nTwo-column problem/solution alternating layout. Inline CTAs at the exact moment the reader is most persuaded. Review cards pulling social proof.\n\nEditorial at the top. Funnel at the bottom.",
        "mobile": "KURA listicle on mobile.\n\nProblem block → transformation strip → review cards → CTA. Alternating layouts, before/after states, full responsive collapse.",
    },
    "post-purchase": {
        "cover": "The highest-intent moment in any funnel is the 5 seconds right after checkout.\n\nMost brands waste it on a blank confirmation screen. KURA's turns it into an upsell, a trust builder, and a community invite.",
        "laptop": "Post-purchase on desktop.\n\nLive countdown JS. One-click upsell. 3-step reassurance block. Review cards. Care guide. Email capture with share buttons.\n\nMost stores skip this page. It's free revenue sitting right after checkout.",
        "mobile": "KURA post-purchase page, mobile.\n\nOrder confirmed → one-click upsell (countdown, no new checkout) → what to expect → reviews → care guide → email signup.\n\nBuyer's remorse prevention, built into the page.",
    },
}

PAGES = [
    ("pdp", "pdp", "Product Page (PDP)"),
    ("advertorial", "ad-01", "Advertorial"),
    ("listicle", "listicle", "Listicle"),
    ("post-purchase", "pp-01", "Post-Purchase / Thank You"),
]

# ---- 1. Extend kura-social-content.json ----
for key, cloud_key, page_label in PAGES:
    v = cloud["pages"][key]
    prefix = "PDP" if key == "pdp" else ("AD" if key == "advertorial" else ("LI" if key == "listicle" else "PP"))
    social["assets"][f"TS-KURA-{prefix}-COVER-VID"] = {
        "platform": ["linkedin", "instagram"], "assetType": "video",
        "assetUrl": v["cover"]["url"], "assetPath": None,
        "caption": LI[key], "hashtags": [], "status": "Not Posted", "postedAt": None,
        "note": f"Cloudinary-hosted only, no local file. {page_label} cover video.",
    }
    social[f"_ig_{key}"] = None  # placeholder removed below
    social["assets"][f"TS-KURA-{prefix}-COVER-VID-IG"] = {
        "platform": ["instagram"], "assetType": "video",
        "assetUrl": v["cover"]["url"], "assetPath": None,
        "caption": IG[key], "hashtags": [], "status": "Not Posted", "postedAt": None,
        "note": f"Cloudinary-hosted only, no local file. {page_label} cover video (IG caption variant).",
    }
    del social[f"_ig_{key}"]
    for asset_kind in ("cover", "laptop", "mobile"):
        social["assets"][f"TS-KURA-{prefix}-{asset_kind.upper()}-VID-X"] = {
            "platform": ["x"], "assetType": "video",
            "assetUrl": v[asset_kind]["url"], "assetPath": None,
            "caption": X[key][asset_kind], "hashtags": [], "status": "Not Posted", "postedAt": None,
            "note": f"Cloudinary-hosted only, no local file. {page_label} {asset_kind} video.",
        }

social["knownGaps"] = social.get("knownGaps", "") + (
    " | 2026-07-21: pdp/advertorial/listicle/post-purchase have video assets only "
    "(Cloudinary-hosted, confirmed by Ridwan). No local stills exist for these 4 pages; "
    "Ridwan says stills live in the replo-rebuilds folder, not connected in this session "
    "-- revisit once that folder is connected to add TS-KURA-{PAGE}-PREVIEW/-MOSAIC image entries."
)
json.dump(social, open(social_path, "w"), indent=2)
print("[kura] social-content.json updated:", len(social["assets"]), "total asset entries")

# ---- 2. Build queue rows ----
qpath = "outputs/distribution-queue/queue.json"
q = json.load(open(qpath))
existing_ids = {r["post_id"] for r in q["rows"]}

def mkrow(post_id, pid, platform, date, time_local, et, asset_url, caption, note):
    # caption_json MUST mirror populate_sheet.py's contract: a pre-escaped JSON
    # string literal (including surrounding quotes) — this is what the Make
    # scenario's {{1.`14`}} reference drops verbatim into the post body for
    # BOTH the LinkedIn and X branches. Bug fixed 2026-07-22: this used to be
    # left as "" here, which would have posted these rows with blank text
    # once their scheduled date arrived (LinkedIn rows read column 14 too).
    return {
        "post_id": post_id, "pipeline_item_id": pid, "stream": "Template Showcase",
        "platform": platform, "scheduled_date": date, "scheduled_time_local": time_local,
        "intended_et": et, "asset_paths": "", "caption": caption,
        "caption_source_tab": "kura-social-content.json (backfill 2026-07-21)",
        "status": "Draft",
        "qa_status": f"Not run through automated QA (no local HTML source) - pre-existing Ridwan-authored captions, Cloudinary video-only asset. {note}",
        "posted_at": None, "content_system_folder": "",
        "caption_json": json.dumps(caption, ensure_ascii=False), "asset_urls": asset_url,
    }

new_rows = []

# LinkedIn + Instagram: 1 page every 2 weeks, starting 2026-08-07 (2wk after kura_hp-01's LI post 2026-07-24)
li_ig_dates = ["2026-08-07", "2026-08-21", "2026-09-04", "2026-09-18"]
for (key, cloud_key, label), date in zip(PAGES, li_ig_dates):
    v = cloud["pages"][key]
    prefix = "pdp" if key == "pdp" else ("ad-01" if key == "advertorial" else ("li-03" if key == "listicle" else "pp-01"))
    pid = f"template-showcase-kura_{prefix}-20260721"
    li_id = f"{pid}-{date.replace('-','')}-li-0900"
    if li_id not in existing_ids:
        new_rows.append(mkrow(li_id, pid, "LinkedIn", date, "14:00", "09:00 ET",
                               v["cover"]["url"], LI[key], f"{label} cover video, LinkedIn."))
    ig_id = f"{pid}-{date.replace('-','')}-ig-1200"
    if ig_id not in existing_ids:
        new_rows.append(mkrow(ig_id, pid, "Instagram", date, "17:00", "12:00 ET",
                               v["cover"]["url"], IG[key], f"{label} cover video, Instagram."))

# Twitter: 1 post every 3 days starting 2026-07-28, cycling cover/laptop/mobile per page in order
import datetime
et_slots = [("14:00", "09:00 ET"), ("18:00", "13:00 ET"), ("23:00", "18:00 ET")]
d = datetime.date(2026, 7, 28)
slot_i = 0
for key, cloud_key, label in PAGES:
    v = cloud["pages"][key]
    prefix = "pdp" if key == "pdp" else ("ad-01" if key == "advertorial" else ("li-03" if key == "listicle" else "pp-01"))
    pid = f"template-showcase-kura_{prefix}-20260721"
    for asset_kind in ("cover", "laptop", "mobile"):
        date_str = d.isoformat()
        time_local, et = et_slots[slot_i % 3]
        x_id = f"{pid}-{date_str.replace('-','')}-x-{time_local.replace(':','')}"
        if x_id not in existing_ids:
            new_rows.append(mkrow(x_id, pid, "Twitter", date_str, time_local, et,
                                   v[asset_kind]["url"], X[key][asset_kind],
                                   f"{label} {asset_kind} video, Twitter (3-day cadence)."))
        d += datetime.timedelta(days=3)
        slot_i += 1

q["rows"].extend(new_rows)
q["meta"]["updated"] = "2026-07-21T00:00:00+00:00"
json.dump(q, open(qpath, "w"), indent=2)
print("[kura] queue rows added:", len(new_rows), "| total rows now:", len(q["rows"]))

# ---- 3. Rewrite CSV mirror ----
import csv
cols = list(q["rows"][0].keys())
with open("outputs/distribution-queue/queue.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in q["rows"]:
        w.writerow(r)
print("[kura] csv mirror rewritten")
