#!/usr/bin/env python3
"""
Append the 2026-08-28 Tips carousel (CHECKOUTMYTH) to the Koolestpro per-brand
social-content library — both koolestpro-social-content.json and its .md sibling.

Additive only: new keys are added, existing keys are never overwritten (the
script aborts if any CHECKOUTMYTH key already exists). No -GRAPHIC-A/B/C keys,
retired 2026-07-18.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_PATH = os.path.join(ROOT, 'koolestpro-social-content.json')
MD_PATH = os.path.join(ROOT, 'koolestpro-social-content.md')

TOKEN = 'CHECKOUTMYTH'
PREFIX = f'TIP-KOOLESTPRO-{TOKEN}'
ASSET_DIR = 'outputs/tips/checkout-payment-method-myth-assets'
POST_HTML = 'outputs/tips/checkout-payment-method-myth_2026-08-28.html'
PIPELINE_ID = 'idea-checkout-abandonment-fix-the-payment-method-order-1777030231175-ebzqg'
SLIDES = [f'{ASSET_DIR}/slide{i}.png' for i in range(1, 8)]

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

HOOK = """You added Apple Pay. They still left.

Baymard puts "there weren't enough payment methods" at 9% of abandonments. Second from the bottom.

Extra costs sit at 40%, and another 12% can't work out the total before checkout.

The wallet row was never the problem. The number you're hiding is.

When does a first time buyer on your store actually see the real total?"""

IG = """You added Apple Pay. They still left.

Baymard's abandonment research puts "not enough payment methods" at 9%. Second from the bottom.

Extra costs sit at 40%. Another 12% can't work out the total before checkout.

The average US checkout shows 23.48 form elements. An ideal one needs 12 to 14.

Your checkout isn't short a button. It's hiding the number people care about.

Save this. Follow @koolestpro for more Shopify CRO tips."""

IG_TAGS = ['#ShopifyDesign', '#CRO', '#eCommerce', '#ShopifyDeveloper', '#ConversionOptimization',
           '#WebDesign', '#Shopify', '#UXDesign', '#DigitalMarketing', '#ShopifyLiquid']

THREAD = """1/ You added Apple Pay. They still left. The wallet row was never the thing costing you the sale.

2/ Baymard asked shoppers with real purchase intent why they abandoned. 9% said there weren't enough payment methods. Second from the bottom of the list.

3/ 40% said extra costs were too high. Shipping and tax showing up after they'd already decided to buy.

4/ Another 12% said they couldn't work out the total order cost up front at all.

5/ Same research: the average US checkout shows 23.48 form elements. An ideal one needs 12 to 14.

6/ So your checkout isn't short a payment button. It's carrying ten fields it doesn't need and hiding the total until step three.

7/ Fix the order instead. Full total on the cart page, guest checkout, fewer fields, wallets last. Follow @koolestpro for more Shopify CRO."""

X1 = ("Adding a payment button is the cheapest fix on your checkout and the smallest one. "
      "9% abandon over payment choice. 40% abandon over the total.")
X2 = ("Four wallet buttons, total revealed at step three. Or: total on the cart page, guest "
      "checkout, wallets last. Only one of those gets paid.")
X3 = ("Most checkout optimisation is just turning on more payment providers. That isn't "
      "optimisation. That's adding options to a screen people already left.")


def entry(platform, asset_type, path, caption, tags=None):
    return {'platform': platform, 'assetType': asset_type, 'assetPath': path,
            'caption': caption, 'hashtags': tags or [],
            'status': 'Not Posted', 'postedAt': None}


NEW = {
    f'{PREFIX}-CAROUSEL': entry(['linkedin', 'instagram'], 'carousel', SLIDES, LINKEDIN),
    f'{PREFIX}-COVER': entry(['linkedin'], 'image', SLIDES[0], HOOK),
    f'{PREFIX}-IG': entry(['instagram'], 'carousel', SLIDES, IG, IG_TAGS),
    f'{PREFIX}-X-THREAD': entry(['x'], 'text', None, THREAD),
    f'{PREFIX}-X1': entry(['x'], 'text', None, X1),
    f'{PREFIX}-X2': entry(['x'], 'text', None, X2),
    f'{PREFIX}-X3': entry(['x'], 'text', None, X3),
}

MD_TABLE_ROWS = f"""| `{PREFIX}-CAROUSEL` | 7-slide carousel (slide1-7.png) | LinkedIn, Instagram | LinkedIn long-form |
| `{PREFIX}-COVER` | slide1.png | LinkedIn | Hook post |
| `{PREFIX}-IG` | 7-slide carousel (slide1-7.png) | Instagram | Instagram caption (with hashtags) |
| `{PREFIX}-X-THREAD` | text only | X | 7-tweet thread |
| `{PREFIX}-X1` / `-X2` / `-X3` | text only | X | Single tweets |
"""

MD_POST_LINE = (f"Post: `{POST_HTML}` · Pipeline id: `{PIPELINE_ID}` · Status: Created "
                f"(awaiting manual review) · All 7 slide images exported to `{ASSET_DIR}/`.\n")

MD_SECTION = f"""
---

## Checkout Abandonment: The Payment Method Myth (2026-08-28)

Myth vs Reality carousel, Conversion Strategy pillar. Every figure is primary-source Baymard,
read directly from https://baymard.com/lists/cart-abandonment-rate on 2026-08-28: 40% extra
costs vs 9% too few payment methods, 12% could not calculate the total up front, and 23.48
average checkout form elements against an ideal 12 to 14. No invented metrics.

### {PREFIX}-CAROUSEL — LinkedIn long-form

```
{LINKEDIN}
```

### {PREFIX}-COVER — Hook post

```
{HOOK}
```

### {PREFIX}-IG — Instagram caption

```
{IG}

{' '.join(IG_TAGS)}
```

### {PREFIX}-X-THREAD — X thread

```
{THREAD}
```

### {PREFIX}-X1 / X2 / X3 — Single tweets

```
X1 (The Rule): {X1}

X2 (The Contrast): {X2}

X3 (The Hot Take): {X3}
```
"""


def main():
    for p in [JSON_PATH, MD_PATH, os.path.join(ROOT, POST_HTML)] + \
             [os.path.join(ROOT, s) for s in SLIDES]:
        if not os.path.exists(p):
            sys.exit(f'FAIL: missing file {p}')

    for t in (X1, X2, X3):
        if len(t) > 280:
            sys.exit(f'FAIL: X single over 280 chars ({len(t)})')

    data = json.load(open(JSON_PATH, encoding='utf-8'))
    clashes = [k for k in NEW if k in data['assets']]
    if clashes:
        sys.exit(f'FAIL: keys already exist, refusing to overwrite: {clashes}')

    data['assets'].update(NEW)
    if PIPELINE_ID not in data['relatedPipelineItemIds']:
        data['relatedPipelineItemIds'].append(PIPELINE_ID)
    json.dump(data, open(JSON_PATH, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

    md = open(MD_PATH, encoding='utf-8').read()
    if PREFIX in md:
        sys.exit('FAIL: md already references this post')

    # append the new rows to the HOW TO USE table, immediately after the last row
    anchor = '| `TIP-KOOLESTPRO-THUMBZONE-X1` / `-X2` / `-X3` | text only | X | Single tweets |\n'
    if anchor not in md:
        sys.exit('FAIL: md key-table anchor row not found')
    md = md.replace(anchor, anchor + MD_TABLE_ROWS, 1)

    # add the Post: provenance line after the most recent existing one
    post_anchor = ("Post: `outputs/tips/trust-signals-over-credibility_2026-08-14.html`")
    i = md.find(post_anchor)
    if i < 0:
        sys.exit('FAIL: md post-provenance anchor not found')
    j = md.find('\n', i) + 1
    md = md[:j] + '\n' + MD_POST_LINE + md[j:]

    md = md.rstrip('\n') + '\n' + MD_SECTION
    open(MD_PATH, 'w', encoding='utf-8').write(md)

    # verify
    check = json.load(open(JSON_PATH, encoding='utf-8'))
    added = [k for k in check['assets'] if k.startswith(PREFIX)]
    print(f'json: added {len(added)} keys -> {added}')
    print(f'json: total assets now {len(check["assets"])}')
    md2 = open(MD_PATH, encoding='utf-8').read()
    print(f'md: {md2.count(PREFIX)} references to {PREFIX}')

    # No-em-dash rule applies to the POSTABLE COPY. The md's own section headings
    # keep the file's existing "### KEY — label" convention, which is structure,
    # not copy, so only the captions are asserted here.
    bad = [k for k, v in NEW.items() if '—' in v['caption']]
    if bad:
        sys.exit(f'FAIL: em dash in caption for {bad}')
    print('captions: no em dashes, all X singles under 280 chars')


if __name__ == '__main__':
    main()
