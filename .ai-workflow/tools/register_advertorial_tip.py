#!/usr/bin/env python3
"""Register the advertorial Tips carousel into the central pipeline.

Updates the EXISTING backlog item (tip-advertorial-what-it-actually-is-20260510)
in place -- per CLAUDE.md's Cowork Responsibilities, ids are never duplicated
for a backlog item that already exists. Only touches the JSON inside
<script id="cowork-sync-data">, everything else in the file is preserved
byte-for-byte.
"""
import json
import re

SYNC_FILE = "ridwan_content_system_updated.html"
ITEM_ID = "tip-advertorial-what-it-actually-is-20260510"

with open(SYNC_FILE, "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r'(<script id="cowork-sync-data" type="application/json">)(.*?)(</script>)', html, re.DOTALL)
assert m, "could not find cowork-sync-data script block"
data = json.loads(m.group(2))

item = next((it for it in data["items"] if it.get("id") == ITEM_ID), None)
assert item is not None, f"item {ITEM_ID} not found -- refusing to create a duplicate id"

LINKEDIN_CAPTION = (
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
X_SINGLES = [
    "An advertorial has one job: make a stranger believe you. Not inform them, not rank on Google, "
    "not fill space before the PDP.",
    "A landing page repeats your ad. An advertorial builds trust before the ad's claim gets tested.",
    "Most \"advertorials\" are blog posts in a costume. That's why cold traffic reads them and still "
    "doesn't buy.",
]

item["status"] = "Created"
item["day"] = ""
item["folder"] = "outputs/tips/advertorial-page-6-elements_2026-07-31.html"
item["week"] = "Week of July 27"
item["linkedAt"] = "2026-07-31T00:00:00Z"
item["captions"] = {"linkedin": LINKEDIN_CAPTION, "x": X_SINGLES}
item["assets"] = {
    "images": [
        f"outputs/tips/advertorial-page-6-elements-assets/slide{i}.png" for i in range(1, 8)
    ],
    "video": None,
}

import datetime
data["meta"]["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

new_json = json.dumps(data, indent=2, ensure_ascii=False)
html = html[: m.start(2)] + new_json + html[m.end(2) :]

with open(SYNC_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"[ok] updated item {ITEM_ID}: status={item['status']} folder={item['folder']}")
