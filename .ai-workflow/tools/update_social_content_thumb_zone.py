#!/usr/bin/env python3
"""
Append the 2026-08-21 Tips carousel to koolestpro-social-content.json / .md.

Follows the existing per-post namespacing convention in this file
(TIP-KOOLESTPRO-{TOKEN}-...), token THUMBZONE. Adds new keys only, never
overwrites an existing one. No -GRAPHIC-A/B/C keys (retired 2026-07-18).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_PATH = os.path.join(ROOT, 'koolestpro-social-content.json')
MD_PATH = os.path.join(ROOT, 'koolestpro-social-content.md')

TOKEN = 'THUMBZONE'
ASSET_DIR = 'outputs/tips/thumb-zone-mobile-reach-assets'
SLIDES = [f'{ASSET_DIR}/slide{i}.png' for i in range(1, 8)]
PIPELINE_ID = 'idea-mobile-thumb-zone-7-tap-target-fails-1776763992475-780pp'

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

HOOK = """Your store isn't mobile optimised. It just fits the screen.

Responsive means the layout reflows. It says nothing about whether a thumb can reach the button.

Your customer is one handed, on the move, aiming at a 28px swatch.

What's the last thing on your product page you actually tried to tap one handed?"""

IG = """Your store isn't mobile optimised. It just fits the screen.

Responsive means the layout reflows. It says nothing about whether a thumb can reach the button.

Apple's minimum tap target is 44pt. Google says 48dp. Most swatches ship smaller.

Move the decisions into the bottom third of the screen.

Can you buy it with one thumb, standing up?

Save this. Follow @koolestpro for more Shopify CRO tips."""

IG_TAGS = ['#ShopifyDesign', '#CRO', '#eCommerce', '#ShopifyDeveloper', '#ConversionOptimization',
           '#WebDesign', '#Shopify', '#UXDesign', '#DigitalMarketing', '#ShopifyLiquid']

THREAD = """1/ Your store isn't mobile optimised. It just fits the screen. Those are two different things and only one of them sells.

2/ Responsive means the layout reflows at 390px. It says nothing about whether a thumb can reach the button that takes the money.

3/ The test most owners run: phone in both hands, at a desk. The test that matters: one hand, standing up, thumb anchored bottom right.

4/ Apple has published a 44pt minimum tap target for years. Google says 48dp. Go measure the swatches on your own product page.

5/ What I keep finding: add to cart only above the fold, swatches sized for a mouse, filters in the top left corner, steppers you have to aim at.

6/ None of it needs a redesign. Move the decisions into the bottom third of the screen and size them to be hit without looking.

7/ One filter for every mobile layout: can you buy it with one thumb, standing up? Follow @koolestpro for more Shopify CRO."""

X1 = ("Responsive is about the screen. Buying happens in the thumb's reach. Your layout can pass "
      "one and fail the other on the same page.")
X2 = ("Add to cart above the fold only: a stretch every time. A sticky buy bar in the bottom "
      "third: one thumb, no aiming, no thought.")
X3 = ("Most mobile testing is a founder holding their phone in two hands at a desk. That is not "
      "a test. That is a screenshot with extra steps.")


def entry(platform, asset_type, path, caption, tags=None):
    return {'platform': platform, 'assetType': asset_type, 'assetPath': path,
            'caption': caption, 'hashtags': tags or [], 'status': 'Not Posted', 'postedAt': None}


NEW = {
    f'TIP-KOOLESTPRO-{TOKEN}-CAROUSEL': entry(
        ['linkedin', 'instagram'], 'carousel', SLIDES, LINKEDIN),
    f'TIP-KOOLESTPRO-{TOKEN}-COVER': entry(
        ['linkedin'], 'image', SLIDES[0], HOOK),
    f'TIP-KOOLESTPRO-{TOKEN}-IG': entry(
        ['instagram'], 'carousel', SLIDES, IG + '\n\n' + ' '.join(IG_TAGS), IG_TAGS),
    f'TIP-KOOLESTPRO-{TOKEN}-X-THREAD': entry(['x'], 'text', None, THREAD),
    f'TIP-KOOLESTPRO-{TOKEN}-X1': entry(['x'], 'text', None, X1),
    f'TIP-KOOLESTPRO-{TOKEN}-X2': entry(['x'], 'text', None, X2),
    f'TIP-KOOLESTPRO-{TOKEN}-X3': entry(['x'], 'text', None, X3),
}

MD_TABLE_ROWS = f"""| `TIP-KOOLESTPRO-{TOKEN}-CAROUSEL` | 7-slide carousel (slide1-7.png) | LinkedIn, Instagram | LinkedIn long-form |
| `TIP-KOOLESTPRO-{TOKEN}-COVER` | slide1.png | LinkedIn | Hook post |
| `TIP-KOOLESTPRO-{TOKEN}-IG` | 7-slide carousel (slide1-7.png) | Instagram | Instagram caption (with hashtags) |
| `TIP-KOOLESTPRO-{TOKEN}-X-THREAD` | text only | X | 7-tweet thread |
| `TIP-KOOLESTPRO-{TOKEN}-X1` / `-X2` / `-X3` | text only | X | Single tweets |"""

MD_BLOCKS = f"""

---

## Post 4 — Mobile thumb zone (2026-08-21)

**Carousel:** `outputs/tips/thumb-zone-mobile-reach_2026-08-21.html`
**Slides:** `{ASSET_DIR}/slide1-7.png`
**Pipeline item:** `{PIPELINE_ID}`

### TIP-KOOLESTPRO-{TOKEN}-CAROUSEL — LinkedIn long-form

```
{LINKEDIN}
```

### TIP-KOOLESTPRO-{TOKEN}-COVER — Hook post

```
{HOOK}
```

### TIP-KOOLESTPRO-{TOKEN}-IG — Instagram caption

```
{IG}

{' '.join(IG_TAGS)}
```

### TIP-KOOLESTPRO-{TOKEN}-X-THREAD — X thread

```
{THREAD}
```

### TIP-KOOLESTPRO-{TOKEN}-X1 / X2 / X3 — Single tweets

```
X1 (The Rule): {X1}

X2 (The Contrast): {X2}

X3 (The Hot Take): {X3}
```
"""


def main():
    # ── JSON ────────────────────────────────────────────────────────────────
    data = json.load(open(JSON_PATH, encoding='utf-8'))
    clashes = [k for k in NEW if k in data['assets']]
    if clashes:
        raise SystemExit(f'FAIL: keys already exist, refusing to overwrite: {clashes}')

    for rel in SLIDES:
        if not os.path.exists(os.path.join(ROOT, rel)):
            raise SystemExit(f'FAIL: asset missing on disk: {rel}')

    data['assets'].update(NEW)
    if PIPELINE_ID not in data['relatedPipelineItemIds']:
        data['relatedPipelineItemIds'].append(PIPELINE_ID)
    json.dump(data, open(JSON_PATH, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

    # ── MD (keep the sibling in step with the JSON) ──────────────────────────
    md = open(MD_PATH, encoding='utf-8').read()
    if f'TIP-KOOLESTPRO-{TOKEN}-CAROUSEL' in md:
        raise SystemExit('FAIL: markdown already contains this post')
    anchor = '| `TIP-KOOLESTPRO-TRUSTSIGNALS-X1` / `-X2` / `-X3` | text only | X | Single tweets |'
    if anchor not in md:
        raise SystemExit('FAIL: markdown key-table anchor row not found')
    md = md.replace(anchor, anchor + '\n' + MD_TABLE_ROWS, 1)
    md = md.rstrip() + '\n' + MD_BLOCKS
    open(MD_PATH, 'w', encoding='utf-8').write(md)

    check = json.load(open(JSON_PATH, encoding='utf-8'))
    print(f'json: {len(check["assets"])} asset keys ({len(NEW)} added)')
    print(f'      relatedPipelineItemIds={len(check["relatedPipelineItemIds"])}')
    print(f'md:   {open(MD_PATH, encoding="utf-8").read().count("TIP-KOOLESTPRO-" + TOKEN)} '
          f'references to the new token')


if __name__ == '__main__':
    main()
