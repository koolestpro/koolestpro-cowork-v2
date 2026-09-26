#!/usr/bin/env python3
"""Append the advertorial Tips carousel to koolestpro-social-content.json/.md.

Adds new keys only -- never touches existing ANIMBUDGET entries. Keeps the
two files in sync (same keys) per CLAUDE.md's Per-Brand Social Content
Library convention.
"""
import json

JSON_FILE = "koolestpro-social-content.json"
MD_FILE = "koolestpro-social-content.md"
TOKEN = "ADVERTORIAL"
PIPELINE_ID = "tip-advertorial-what-it-actually-is-20260510"

SLIDES = [f"outputs/tips/advertorial-page-6-elements-assets/slide{i}.png" for i in range(1, 8)]

LINKEDIN_LONGFORM = (
    "You think an advertorial is a longer landing page. That's why cold traffic keeps bouncing.\n\n"
    "Most Shopify brands treat it like homework. Copy from the ad, stretch it out, ship it, move on.\n\n"
    "Cold traffic converts around 1.5%. Warmed-up traffic can hit 60%+. That gap is one page most "
    "brands never build properly.\n\n"
    "An advertorial isn't a landing page. It isn't a blog post either. Its only job is making a "
    "stranger believe you before anything else.\n\n"
    "It runs on 3 beats that actually carry the weight:\n\n"
    "The hook that stops the scroll.\n\n"
    "The proof that kills the doubt.\n\n"
    "The reveal that earns the click.\n\n"
    "Everything else on the page just clears the path between those three.\n\n"
    "Before you write your next one, ask yourself this: does this page make a stranger believe you "
    "before it asks them to buy? If not, it's just copy.\n\n"
    "Save this for your next funnel build."
)
HOOK = (
    "You think an advertorial is a longer landing page. That's why cold traffic keeps bouncing.\n\n"
    "Its only job is making a stranger believe you before anything else.\n\n"
    "Hook, proof, reveal. Those 3 beats carry the whole page.\n\n"
    "Which page in your funnel is doing homework instead of doing its job?"
)
IG_CAPTION = (
    "You think an advertorial is a longer landing page. That's why cold traffic keeps bouncing.\n\n"
    "It isn't a landing page. It isn't a blog post either.\n\n"
    "Its only job is making a stranger believe you before anything else.\n\n"
    "The hook stops the scroll. The proof kills the doubt. The reveal earns the click. That's the "
    "whole page.\n\n"
    "Save this. Follow @koolestpro for more Shopify CRO tips.\n\n"
    "#ShopifyDesign #CRO #eCommerce #ShopifyDeveloper #ConversionOptimization #WebDesign #Shopify "
    "#UXDesign #DigitalMarketing #ShopifyLiquid"
)
X_THREAD = (
    "1/ You think an advertorial is a longer landing page. That's why cold traffic keeps bouncing. "
    "A short thread on what it actually is:\n\n"
    "2/ The myth: a landing page with more words, or a blog post you hope ranks one day. Both miss "
    "the job entirely.\n\n"
    "3/ Cold traffic converts around 1.5%. Warmed-up traffic can hit 60%+. That gap is one page most "
    "Shopify brands skip.\n\n"
    "4/ The reality: its only job is making a stranger believe you before anything else. Trust moves "
    "first. The product comes after.\n\n"
    "5/ It runs on 3 beats: the hook that stops the scroll, the proof that kills the doubt, the "
    "reveal that earns the click.\n\n"
    "6/ Everything else on the page just clears the path between those three.\n\n"
    "7/ One question before you ship the next one: does it make a stranger believe you before it "
    "asks them to buy? Follow @koolestpro for more."
)
X1 = (
    "An advertorial has one job: make a stranger believe you. Not inform them, not rank on Google, "
    "not fill space before the PDP."
)
X2 = "A landing page repeats your ad. An advertorial builds trust before the ad's claim gets tested."
X3 = (
    "Most \"advertorials\" are blog posts in a costume. That's why cold traffic reads them and still "
    "doesn't buy."
)

# ── JSON ──────────────────────────────────────────────────────────────────
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

if PIPELINE_ID not in data["relatedPipelineItemIds"]:
    data["relatedPipelineItemIds"].append(PIPELINE_ID)

new_entries = {
    f"TIP-KOOLESTPRO-{TOKEN}-CAROUSEL": {
        "platform": ["linkedin"],
        "assetType": "carousel",
        "assetPath": SLIDES,
        "caption": LINKEDIN_LONGFORM,
        "hashtags": [],
        "status": "Not Posted",
        "postedAt": None,
    },
    f"TIP-KOOLESTPRO-{TOKEN}-COVER": {
        "platform": ["linkedin"],
        "assetType": "image",
        "assetPath": SLIDES[0],
        "caption": HOOK,
        "hashtags": [],
        "status": "Not Posted",
        "postedAt": None,
    },
    f"TIP-KOOLESTPRO-{TOKEN}-IG": {
        "platform": ["instagram"],
        "assetType": "carousel",
        "assetPath": SLIDES,
        "caption": IG_CAPTION,
        "hashtags": [],
        "status": "Not Posted",
        "postedAt": None,
    },
    f"TIP-KOOLESTPRO-{TOKEN}-X-THREAD": {
        "platform": ["x"],
        "assetType": "text",
        "assetPath": None,
        "caption": X_THREAD,
        "hashtags": [],
        "status": "Not Posted",
        "postedAt": None,
    },
    f"TIP-KOOLESTPRO-{TOKEN}-X1": {
        "platform": ["x"], "assetType": "text", "assetPath": None,
        "caption": X1, "hashtags": [], "status": "Not Posted", "postedAt": None,
    },
    f"TIP-KOOLESTPRO-{TOKEN}-X2": {
        "platform": ["x"], "assetType": "text", "assetPath": None,
        "caption": X2, "hashtags": [], "status": "Not Posted", "postedAt": None,
    },
    f"TIP-KOOLESTPRO-{TOKEN}-X3": {
        "platform": ["x"], "assetType": "text", "assetPath": None,
        "caption": X3, "hashtags": [], "status": "Not Posted", "postedAt": None,
    },
}

for key in new_entries:
    assert key not in data["assets"], f"key collision: {key} already exists"
data["assets"].update(new_entries)

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

# ── Markdown ──────────────────────────────────────────────────────────────
with open(MD_FILE, "r", encoding="utf-8") as f:
    md = f.read()

table_row_anchor = "| `TIP-KOOLESTPRO-ANIMBUDGET-X1` / `-X2` / `-X3` | text only | X | Single tweets |\n"
assert table_row_anchor in md, "table anchor not found in md file"
new_rows = (
    f"| `TIP-KOOLESTPRO-{TOKEN}-CAROUSEL` | 7-slide carousel (slide1-7.png) | LinkedIn | LinkedIn long-form |\n"
    f"| `TIP-KOOLESTPRO-{TOKEN}-COVER` | slide1.png | LinkedIn | Hook post |\n"
    f"| `TIP-KOOLESTPRO-{TOKEN}-IG` | 7-slide carousel (slide1-7.png) | Instagram | Instagram caption (with hashtags) |\n"
    f"| `TIP-KOOLESTPRO-{TOKEN}-X-THREAD` | text only | X | 7-tweet thread |\n"
    f"| `TIP-KOOLESTPRO-{TOKEN}-X1` / `-X2` / `-X3` | text only | X | Single tweets |\n"
)
md = md.replace(table_row_anchor, table_row_anchor + new_rows)

post_line_anchor = (
    "Post: `outputs/tips/animation-budget-motion-conversion_2026-07-17.html` · "
    "Pipeline id: `idea-animation-budget-when-motion-helps-conversion-1776763992475-jjrc6` · "
    "Status: Created (awaiting manual review) · All 10 image assets exported to "
    "`outputs/tips/animation-budget-assets/`.\n"
)
assert post_line_anchor in md, "post-line anchor not found in md file"
new_post_line = (
    f"\nPost: `outputs/tips/advertorial-page-6-elements_2026-07-31.html` · "
    f"Pipeline id: `{PIPELINE_ID}` · "
    "Status: Created (awaiting manual review) · All 7 slide images exported to "
    "`outputs/tips/advertorial-page-6-elements-assets/`.\n"
)
md = md.replace(post_line_anchor, post_line_anchor + new_post_line)

new_section = f"""
---

## An Advertorial Is Not a Landing Page (2026-07-31)

### TIP-KOOLESTPRO-{TOKEN}-CAROUSEL — LinkedIn long-form

```
{LINKEDIN_LONGFORM}
```

### TIP-KOOLESTPRO-{TOKEN}-COVER — Hook post

```
{HOOK}
```

### TIP-KOOLESTPRO-{TOKEN}-IG — Instagram caption

```
{IG_CAPTION}
```

### TIP-KOOLESTPRO-{TOKEN}-X-THREAD — X thread

```
{X_THREAD}
```

### TIP-KOOLESTPRO-{TOKEN}-X1 / X2 / X3 — Single tweets

```
X1 (The Rule): {X1}

X2 (The Contrast): {X2}

X3 (The Hot Take): {X3}
```
"""
md = md.rstrip("\n") + "\n" + new_section

with open(MD_FILE, "w", encoding="utf-8") as f:
    f.write(md)

print("[ok] updated", JSON_FILE, "and", MD_FILE)
