#!/usr/bin/env python3
"""
Registers the typography-hierarchy Tips carousel.

1. Updates the EXISTING backlog item in ridwan_content_system_updated.html
   in place, by its existing id. Does not create a new id (duplicate ids for
   the same backlog topic is a known past bug).
2. Appends TIP-KOOLESTPRO-TYPE6-* keys to koolestpro-social-content.json/.md.

Status is set to "Created". Never "Published".
"""

import json
import os
import re
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SYS = os.path.join(ROOT, "ridwan_content_system_updated.html")
SC_JSON = os.path.join(ROOT, "koolestpro-social-content.json")
SC_MD = os.path.join(ROOT, "koolestpro-social-content.md")

ITEM_ID = "idea-typography-hierarchy-that-converts-the-6-level-sys-1777030231175-j3p4a"
SLUG = "typography-hierarchy-six-levels"
FOLDER = "outputs/tips/typography-hierarchy-six-levels_2026-09-18.html"
ASSETS = "outputs/tips/typography-hierarchy-six-levels-assets"
TITLE = "Six levels. Six jobs."
NOW = "2026-09-18T00:00:00Z"

SLIDES = [f"{ASSETS}/slide{i}.png" for i in range(1, 8)]

LINKEDIN_CAPTION = (
    "Your headline got bigger. The page still feels flat.\n\n"
    "Hierarchy is a ranking, not a size. Six things set at 32px is not six levels. "
    "It's one level, printed six times.\n\n"
    "Six levels, six jobs: page promise, section signpost, block claim, body, action, "
    "fine print. If a level has no job, it isn't a level.\n\n"
    "And two of those six can be pure space. Nothing has to get bigger.\n\n"
    "Repost if your last redesign ended with everything one step bigger."
)

X1 = ("Hierarchy is a ranking, not a size.\n\n"
      "Six things set at 32px is not six levels. It's one level, printed six times.")
X2 = ("Bumping the H1 to 48px: everything else grows to keep up, nothing leads.\n\n"
      "Adding 40px of space above it: nothing got bigger, and it finally wins.")
X3 = ("Most \"the page feels flat\" feedback gets fixed with spacing, not font size. "
      "You keep reaching for the size picker because it's the only lever you've been taught.")

X_THREAD = (
    "1/ Your headline got bigger. The page still feels flat. Here's the typography thing "
    "almost every Shopify store gets backwards:\n\n"
    "2/ The myth: if it matters, make it bigger. So the H1 grows. Then the subhead grows to "
    "keep up. Then the price. Now everything is loud and nothing leads.\n\n"
    "3/ The reality: hierarchy is a ranking, not a size. Six things set at 32px is not six "
    "levels. It's one level, printed six times.\n\n"
    "4/ Nielsen Norman Group: on an average visit people read at most about 28% of the words "
    "on a page. They aren't reading. They're hunting for the one thing that wins.\n\n"
    "5/ Stop counting sizes. Assign jobs. Page promise (the outcome), section signpost "
    "(where am I), block claim (why this part), body (the proof), action (the button), "
    "fine print (the risk).\n\n"
    "6/ Two of those six levels can be pure space. Same sizes, bigger gaps, and the page "
    "finally reads. Nothing got bigger. Things stopped touching.\n\n"
    "7/ Test it: squint at your PDP. Name what you see first. Can't do it in two seconds? "
    "Font size won't save you. More Shopify CRO: @koolestpro"
)

IG_CAPTION = (
    "Your headline got bigger. The page still feels flat.\n\n"
    "Hierarchy is a ranking, not a size. Six things set at 32px is not six levels. "
    "It's one level, printed six times.\n\n"
    "Six levels, six jobs. Two of them can be pure space. Nothing has to get bigger.\n\n"
    "Save this for your next build. Follow @koolestpro for more Shopify CRO."
)

IG_TAGS = ["ShopifyDesign", "CRO", "eCommerce", "ShopifyDeveloper", "ConversionOptimization",
           "WebDesign", "Shopify", "UXDesign", "Typography", "ProductPage"]

NEW_ASSETS = {
    "TIP-KOOLESTPRO-TYPE6-COVER": {
        "platform": ["linkedin"],
        "assetType": "image",
        "assetPath": SLIDES[0],
        "caption": LINKEDIN_CAPTION,
        "hashtags": ["ShopifyCRO", "Typography", "WebDesign"],
        "status": "Not Posted",
        "postedAt": None,
    },
    "TIP-KOOLESTPRO-TYPE6-CAROUSEL": {
        "platform": ["linkedin", "instagram"],
        "assetType": "carousel",
        "assetPath": SLIDES,
        "caption": LINKEDIN_CAPTION,
        "hashtags": ["ShopifyCRO", "Typography", "WebDesign"],
        "status": "Not Posted",
        "postedAt": None,
    },
    "TIP-KOOLESTPRO-TYPE6-IG": {
        "platform": ["instagram"],
        "assetType": "carousel",
        "assetPath": SLIDES,
        "caption": IG_CAPTION,
        "hashtags": IG_TAGS,
        "status": "Not Posted",
        "postedAt": None,
    },
    "TIP-KOOLESTPRO-TYPE6-X-THREAD": {
        "platform": ["x"],
        "assetType": "text",
        "assetPath": None,
        "caption": X_THREAD,
        "hashtags": [],
        "status": "Not Posted",
        "postedAt": None,
    },
    "TIP-KOOLESTPRO-TYPE6-X1": {
        "platform": ["x"], "assetType": "text", "assetPath": None,
        "caption": X1, "hashtags": [], "status": "Not Posted", "postedAt": None,
    },
    "TIP-KOOLESTPRO-TYPE6-X2": {
        "platform": ["x"], "assetType": "text", "assetPath": None,
        "caption": X2, "hashtags": [], "status": "Not Posted", "postedAt": None,
    },
    "TIP-KOOLESTPRO-TYPE6-X3": {
        "platform": ["x"], "assetType": "text", "assetPath": None,
        "caption": X3, "hashtags": [], "status": "Not Posted", "postedAt": None,
    },
}


def check_x_limits():
    """Hard gate: every X post counted against 280, newlines included."""
    ok = True
    singles = {"X1": X1, "X2": X2, "X3": X3}
    for name, txt in singles.items():
        n = len(txt)
        flag = "ok" if n <= 280 else "OVER"
        print(f"  {name}: {n} chars [{flag}]")
        ok = ok and n <= 280
    for i, tweet in enumerate(X_THREAD.split("\n\n"), 1):
        n = len(tweet)
        flag = "ok" if n <= 280 else "OVER"
        print(f"  thread {i}: {n} chars [{flag}]")
        ok = ok and n <= 280
    if not ok:
        raise SystemExit("[FAIL] an X post exceeds 280 characters")


def check_assets():
    for p in SLIDES:
        full = os.path.join(ROOT, p)
        if not os.path.exists(full):
            raise SystemExit(f"[FAIL] missing asset: {p}")
    if not os.path.exists(os.path.join(ROOT, FOLDER)):
        raise SystemExit(f"[FAIL] missing output file: {FOLDER}")
    print(f"  all 7 slide PNGs + the HTML file exist on disk")


def update_pipeline():
    html = open(SYS, encoding="utf-8").read()
    m = re.search(r'(<script id="cowork-sync-data"[^>]*>)(.*?)(</script>)', html, re.S)
    data = json.loads(m.group(2))

    hits = [i for i in data["items"] if i.get("id") == ITEM_ID]
    if len(hits) != 1:
        raise SystemExit(f"[FAIL] expected 1 item with id {ITEM_ID}, found {len(hits)}")
    item = hits[0]
    if item.get("status") != "Idea":
        print(f"  [warn] item status was {item.get('status')!r}, not 'Idea'")

    item.update({
        "type": "Tip",
        "title": TITLE,
        "slug": SLUG,
        "status": "Created",
        "day": "",
        "folder": FOLDER,
        "linkedAt": NOW,
        "week": "Week of September 18",
        "month": "September 2026",
        "monthSlug": "2026-09",
        "captions": {"linkedin": LINKEDIN_CAPTION, "x": [X1, X2, X3]},
        "assets": {"images": SLIDES, "video": None},
    })

    ids = [i.get("id") for i in data["items"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("[FAIL] duplicate ids in SYNC_DATA.items")

    months = data.setdefault("months", {})
    if "2026-09" not in months:
        months["2026-09"] = {
            "label": "September 2026",
            "htmlPath": "outputs/ideas/ideas_2026-09.html",
            "jsonPath": "outputs/ideas/ideas_2026-09.json",
            "totalIdeas": 0,
        }
        print("  added months['2026-09']")

    new_json = json.dumps(data, indent=2, ensure_ascii=False)
    html = html[:m.start(2)] + new_json + html[m.end(2):]
    open(SYS, "w", encoding="utf-8").write(html)
    print(f"  pipeline item {ITEM_ID} updated in place (status Created), "
          f"{len(data['items'])} items total")


def update_social_content():
    d = json.load(open(SC_JSON, encoding="utf-8"))
    assets = d["assets"]
    for k, v in NEW_ASSETS.items():
        if k in assets:
            print(f"  [skip] {k} already present")
            continue
        assets[k] = v
        print(f"  [add] {k}")
    if ITEM_ID not in d["relatedPipelineItemIds"]:
        d["relatedPipelineItemIds"].append(ITEM_ID)
    json.dump(d, open(SC_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    block = [
        "",
        "## TIP-KOOLESTPRO-TYPE6 — Six levels. Six jobs. (typography hierarchy, 2026-09-18)",
        "",
        f"Post file: `{FOLDER}`",
        f"Assets: `{ASSETS}/slide1..7.png`",
        f"Pipeline item: `{ITEM_ID}`",
        "",
        "| Key | Platform | Asset |",
        "|---|---|---|",
        f"| TIP-KOOLESTPRO-TYPE6-COVER | LinkedIn | `{SLIDES[0]}` |",
        "| TIP-KOOLESTPRO-TYPE6-CAROUSEL | LinkedIn, Instagram | slides 1-7 |",
        "| TIP-KOOLESTPRO-TYPE6-IG | Instagram | slides 1-7 |",
        "| TIP-KOOLESTPRO-TYPE6-X-THREAD | X | text, 7 tweets |",
        "| TIP-KOOLESTPRO-TYPE6-X1/X2/X3 | X | text singles |",
        "",
        "### LinkedIn / carousel caption",
        "",
        "```",
        LINKEDIN_CAPTION,
        "```",
        "",
        "### Instagram caption",
        "",
        "```",
        IG_CAPTION,
        "",
        " ".join("#" + t for t in IG_TAGS),
        "```",
        "",
        "### X thread",
        "",
        "```",
        X_THREAD,
        "```",
        "",
        "### X singles (each counted against 280)",
        "",
        "```",
        X1,
        "```",
        "",
        "```",
        X2,
        "```",
        "",
        "```",
        X3,
        "```",
        "",
    ]
    md = open(SC_MD, encoding="utf-8").read()
    if "TIP-KOOLESTPRO-TYPE6" not in md:
        open(SC_MD, "a", encoding="utf-8").write("\n".join(block))
        print("  appended TYPE6 block to koolestpro-social-content.md")
    else:
        print("  [skip] TYPE6 block already in .md")


if __name__ == "__main__":
    print("X character limits:")
    check_x_limits()
    print("\nAssets:")
    check_assets()
    print("\nPipeline:")
    update_pipeline()
    print("\nSocial content library:")
    update_social_content()
    print("\ndone")
