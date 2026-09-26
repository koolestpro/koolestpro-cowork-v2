#!/usr/bin/env python3
"""
Register the 2026-08-21 Tips carousel in ridwan_content_system_updated.html.

Updates the EXISTING April backlog item in place by its existing id
(idea-mobile-thumb-zone-7-tap-target-fails-1776763992475-780pp) rather than
creating a new one, per koolestpro-tips-weekly Step 1 and the 2026-07-12
duplicate-id bug in the content operating plan's Build Log.

Replaces only the JSON inside <script id="cowork-sync-data">; all UI code is
left untouched.
"""
import json
import os
import re
import shutil
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SYS = os.path.join(ROOT, 'ridwan_content_system_updated.html')
ITEM_ID = 'idea-mobile-thumb-zone-7-tap-target-fails-1776763992475-780pp'
SLUG = 'thumb-zone-mobile-reach'
FOLDER = 'outputs/tips/thumb-zone-mobile-reach_2026-08-21.html'
ASSET_DIR = 'outputs/tips/thumb-zone-mobile-reach-assets'
TITLE = "Your store isn't mobile optimised. It just fits the screen."

LINKEDIN = """Your store isn't mobile optimised. It just fits the screen.

Those are two different things, and only one of them sells.

Responsive means your layout reflows at 390px wide.

It says nothing about whether a thumb can reach the button.

Here is the test most owners run. Phone in both hands, at a desk, good light. Everything looks fine.

Here is the real one. One hand, standing on a bus, thumb anchored bottom right.

Now pick a size, set a quantity, and buy.

Apple has published a 44pt minimum tap target for years. Google says 48dp.

Measure your swatches against that before you argue with me.

What I keep finding on Shopify product pages:

Add to cart that only exists above the fold.
Variant swatches sized for a mouse cursor.
Filters parked in the top left, the hardest corner for a right thumb.
Quantity steppers you have to aim at.

None of that needs a redesign to fix.

Move the decisions into the bottom third. Make them big enough to hit without looking.

Every page is a product. Every click is a choice. Make the choice easy to hit.

Save this and test your own PDP tonight."""

X_POSTS = [
    "Responsive is about the screen. Buying happens in the thumb's reach. Your layout can pass one "
    "and fail the other on the same page.",
    "Add to cart above the fold only: a stretch every time. A sticky buy bar in the bottom third: "
    "one thumb, no aiming, no thought.",
    "Most mobile testing is a founder holding their phone in two hands at a desk. That is not a "
    "test. That is a screenshot with extra steps.",
]


def main():
    html = open(SYS, encoding='utf-8').read()
    m = re.search(r'(<script id="cowork-sync-data"[^>]*>)(.*?)(</script>)', html, re.S)
    if not m:
        raise SystemExit('FAIL: cowork-sync-data block not found')
    data = json.loads(m.group(2))

    # file-linking check: never register an entry without a real file on disk
    for rel in [FOLDER] + [f'{ASSET_DIR}/slide{i}.png' for i in range(1, 8)]:
        if not os.path.exists(os.path.join(ROOT, rel)):
            raise SystemExit(f'FAIL: referenced file missing on disk: {rel}')

    matches = [i for i in data['items'] if i['id'] == ITEM_ID]
    if len(matches) != 1:
        raise SystemExit(f'FAIL: expected exactly 1 item with id {ITEM_ID}, found {len(matches)}')
    item = matches[0]
    if item['status'] != 'Idea':
        raise SystemExit(f'FAIL: item status is already "{item["status"]}", refusing to overwrite')

    now = datetime.now(timezone.utc)
    item.update({
        # was "CRO Fix" while it sat in the backlog as a generic idea; the artifact
        # that actually got built is a Tips carousel, so the record now matches it.
        'type': 'Tip',
        'title': TITLE,
        'slug': SLUG,
        'status': 'Created',
        'day': '',
        'folder': FOLDER,
        'pillar': 'Digital Craftsmanship',
        'brief': ("Myth vs Reality carousel: responsive layout is not the same as mobile "
                  "optimised. Grounds the claim in Apple's published 44pt and Google's 48dp "
                  "minimum tap targets, then names the patterns that sit outside a one-handed "
                  "thumb's reach on a Shopify PDP."),
        'angle': ("Ergonomics over breakpoints. Built from published platform standards only, "
                  "with no invented conversion metrics."),
        'week': 'Week of August 17',
        'linkedAt': now.isoformat(),
        'isNew': True,
        'captions': {'linkedin': LINKEDIN, 'x': X_POSTS},
        'assets': {'images': [f'{ASSET_DIR}/slide{i}.png' for i in range(1, 8)]},
    })

    if item['monthSlug'] not in data['months']:
        raise SystemExit(f'FAIL: month {item["monthSlug"]} missing from SYNC_DATA.months')

    # integrity: unique ids, every non-Idea item has a folder
    ids = [i['id'] for i in data['items']]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit(f'FAIL: duplicate ids present: {dupes}')

    data['meta']['updatedAt'] = now.isoformat()

    shutil.copy(SYS, SYS + '.bak-thumbzone')
    new_json = json.dumps(data, indent=2, ensure_ascii=False)
    html = html[:m.start(2)] + '\n' + new_json + '\n' + html[m.end(2):]
    open(SYS, 'w', encoding='utf-8').write(html)

    # re-parse to confirm the file we just wrote is still valid
    check = re.search(r'<script id="cowork-sync-data"[^>]*>(.*?)</script>',
                      open(SYS, encoding='utf-8').read(), re.S)
    reparsed = json.loads(check.group(1))
    out = [i for i in reparsed['items'] if i['id'] == ITEM_ID][0]
    print(f'updated in place: {out["id"]}')
    print(f'  type={out["type"]}  status={out["status"]}  folder={out["folder"]}')
    print(f'  captions.x={len(out["captions"]["x"])}  assets.images={len(out["assets"]["images"])}')
    print(f'  total items={len(reparsed["items"])} (unchanged: no new id created)')


if __name__ == '__main__':
    main()
