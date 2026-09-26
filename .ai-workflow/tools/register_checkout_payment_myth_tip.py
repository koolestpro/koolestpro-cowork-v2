#!/usr/bin/env python3
"""
Register the 2026-08-28 Tips carousel in ridwan_content_system_updated.html.

Updates the EXISTING April backlog item in place by its existing id
(idea-checkout-abandonment-fix-the-payment-method-order-1777030231175-ebzqg)
rather than creating a new one, per koolestpro-tips-weekly Step 1 and the
2026-07-12 duplicate-id bug in the content operating plan's Build Log.

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
ITEM_ID = 'idea-checkout-abandonment-fix-the-payment-method-order-1777030231175-ebzqg'
SLUG = 'checkout-payment-method-myth'
FOLDER = 'outputs/tips/checkout-payment-method-myth_2026-08-28.html'
ASSET_DIR = 'outputs/tips/checkout-payment-method-myth-assets'
TITLE = "You added Apple Pay. They still left."

LINKEDIN = """You added Apple Pay. They still left.

So you turned on Shop Pay too. Then Google Pay.

The wallet row is four buttons wide now and nothing moved.

Baymard asked shoppers with real intent why they abandoned.

9% said there weren't enough payment methods.

That reason sits second from the bottom of the whole list.

40% said the extra costs were too high. Shipping and tax landing after they had already decided to buy.

Another 12% couldn't work out the total order cost up front at all.

You have been optimising the smallest reason on the page.

The same research puts the average US checkout at 23.48 form elements. An ideal one runs 12 to 14.

Your checkout isn't short a button. It's carrying ten fields it doesn't need.

What I'd fix first:

Show the full total on the cart page, shipping included

Let people pay as a guest before asking them to register

Cut the fields nobody reads

Then add the wallets, after all of that

None of it needs a new theme.

Convert first. Then get clever.

Save this and open your own cart page."""

# Kept as a LIST of individually-sized tweets, never one glued blob — see the
# 2026-07-29 X caption tab-split bug in harvest_content.py. Each is under 280.
X_POSTS = [
    "Adding a payment button is the cheapest fix on your checkout and the smallest one. "
    "9% abandon over payment choice. 40% abandon over the total.",
    "Four wallet buttons, total revealed at step three. Or: total on the cart page, guest "
    "checkout, wallets last. Only one of those gets paid.",
    "Most checkout optimisation is just turning on more payment providers. That isn't "
    "optimisation. That's adding options to a screen people already left.",
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

    for t in X_POSTS:
        if len(t) > 280:
            raise SystemExit(f'FAIL: X post over 280 chars ({len(t)}): {t[:60]}...')

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
        'pillar': 'Conversion Strategy',
        'brief': ("Myth vs Reality carousel: adding payment methods is the smallest available "
                  "fix for cart abandonment. Grounded entirely in Baymard's published reasons "
                  "for abandonment (40% extra costs vs 9% too few payment methods) and their "
                  "23.48 vs 12-14 checkout form-element benchmark."),
        'angle': ("Reorder the checkout instead of adding to it. Built from primary-source "
                  "Baymard figures only, with no invented conversion metrics."),
        'week': 'Week of August 24',
        'linkedAt': now.isoformat(),
        'isNew': True,
        'captions': {'linkedin': LINKEDIN, 'x': X_POSTS},
        'assets': {'images': [f'{ASSET_DIR}/slide{i}.png' for i in range(1, 8)]},
    })

    if item['monthSlug'] not in data['months']:
        raise SystemExit(f'FAIL: month {item["monthSlug"]} missing from SYNC_DATA.months')

    # integrity: unique ids
    ids = [i['id'] for i in data['items']]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit(f'FAIL: duplicate ids present: {dupes}')

    data['meta']['updatedAt'] = now.isoformat()

    shutil.copy(SYS, SYS + '.bak-checkoutmyth')
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
