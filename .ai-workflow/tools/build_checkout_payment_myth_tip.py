#!/usr/bin/env python3
"""
Region-swap builder for the 2026-08-28 Tips carousel:
"You added Apple Pay. They still left." (checkout abandonment / payment method myth)

Base file: outputs/tips/thumb-zone-mobile-reach_2026-08-21.html
  (structural descendant of the approved V2 reference
   animation-budget-motion-conversion-v2_2026-07-28.html: 540x680 portrait,
   scale:2 capture, mandatory chrome-hiding, headline-only density)

Only slide content strings, copy-tab text and the per-post constants are swapped.
JS / CSS / geometry / capture functions are reused byte-for-byte.
Every replacement uses an exact literal boundary, never a lazy multi-slide regex.

ALL FIGURES ARE PRIMARY-SOURCE BAYMARD, fetched and read directly from
https://baymard.com/lists/cart-abandonment-rate on 2026-08-28:
  - reasons for abandonment (excluding "just browsing"):
      40% extra costs too high  /  9% there weren't enough payment methods
  - average US checkout = 23.48 form elements; ideal = 12-14
Secondary aggregators were circulating a wrong "19% payment method not offered"
figure for this same chart; that is Baymard's credit-card-trust line, not the
payment-methods line. Do not reintroduce it. No invented metrics anywhere.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, 'outputs/tips/thumb-zone-mobile-reach_2026-08-21.html')
OUT = os.path.join(ROOT, 'outputs/tips/checkout-payment-method-myth_2026-08-28.html')

SLUG = 'checkout-payment-method-myth'
FOLDER = 'outputs/tips/checkout-payment-method-myth_2026-08-28.html'
TITLE = "You added Apple Pay. They still left."
DL = 'checkout-payment-myth'

ATTR = ('<div style="position:absolute;bottom:18px;right:24px;font-family:\'DM Mono\',monospace;'
        'font-size:12px;color:rgba(255,255,255,0.18);z-index:10;">Ridwan - Shopify CRO &amp; UX Designer</div>')

GLOWS = (
    '<div style="position:absolute;top:-80px;right:-60px;width:340px;height:340px;border-radius:50%;'
    'background:radial-gradient(circle,rgba(255,149,0,0.16),rgba(224,64,160,0.07),transparent 70%);'
    'filter:blur(70px);pointer-events:none;"></div>\n'
    '<div style="position:absolute;bottom:-60px;left:-40px;width:280px;height:280px;border-radius:50%;'
    'background:radial-gradient(circle,rgba(123,47,190,0.15),transparent 70%);filter:blur(60px);'
    'pointer-events:none;"></div>\n'
    '<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.02) 1px,'
    'transparent 1px);background-size:24px 24px;pointer-events:none;"></div>'
)
# cool-first variant, for rhythm across slides
GLOWS_ALT = (
    '<div style="position:absolute;top:-70px;left:-70px;width:320px;height:320px;border-radius:50%;'
    'background:radial-gradient(circle,rgba(123,47,190,0.17),rgba(224,64,160,0.06),transparent 70%);'
    'filter:blur(70px);pointer-events:none;"></div>\n'
    '<div style="position:absolute;bottom:-70px;right:-50px;width:300px;height:300px;border-radius:50%;'
    'background:radial-gradient(circle,rgba(255,149,0,0.15),transparent 70%);filter:blur(60px);'
    'pointer-events:none;"></div>\n'
    '<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.02) 1px,'
    'transparent 1px);background-size:24px 24px;pointer-events:none;"></div>'
)

PAD_OPEN = ('<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;'
            'flex-direction:column;">')


def slide(bg, glows, inner):
    return (f'<div class="slide" style="background:{bg};">\n{glows}\n{PAD_OPEN}\n'
            f'{inner}\n</div>\n{ATTR}\n</div>\n')


def badge(svg_inner):
    """44px circular icon badge holding an inlined Iconify (lucide) glyph."""
    return ('<div style="width:44px;height:44px;border-radius:50%;background:rgba(255,149,0,0.08);'
            'border:1px solid rgba(255,149,0,0.25);display:flex;align-items:center;'
            'justify-content:center;flex-shrink:0;">'
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FF9500" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            f'{svg_inner}</svg></div>')


# Iconify lucide glyphs, fetched once from api.iconify.design and inlined so the
# export never depends on network reachability at html2canvas time.
ICON_CARD = '<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20"/>'
ICON_RECEIPT = (
    '<path d="M12 17V7m4 1h-6a2 2 0 0 0 0 4h4a2 2 0 0 1 0 4H8"/>'
    '<path d="M4 3a1 1 0 0 1 1-1a1.3 1.3 0 0 1 .7.2l.933.6a1.3 1.3 0 0 0 1.4 0l.934-.6a1.3 1.3 0 0 1 '
    '1.4 0l.933.6a1.3 1.3 0 0 0 1.4 0l.933-.6a1.3 1.3 0 0 1 1.4 0l.934.6a1.3 1.3 0 0 0 1.4 0l.933-.6'
    'A1.3 1.3 0 0 1 19 2a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1a1.3 1.3 0 0 1-.7-.2l-.933-.6a1.3 1.3 0 0 '
    '0-1.4 0l-.934.6a1.3 1.3 0 0 1-1.4 0l-.933-.6a1.3 1.3 0 0 0-1.4 0l-.933.6a1.3 1.3 0 0 1-1.4 '
    '0l-.934-.6a1.3 1.3 0 0 0-1.4 0l-.933.6a1.3 1.3 0 0 1-.7.2a1 1 0 0 1-1-1z"/>')
ICON_SCAN_EYE = (
    '<path d="M3 7V5a2 2 0 0 1 2-2h2m10 0h2a2 2 0 0 1 2 2v2m0 10v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 '
    '1-2-2v-2"/><circle cx="12" cy="12" r="1"/>'
    '<path d="M18.944 12.33a1 1 0 0 0 0-.66a7.5 7.5 0 0 0-13.888 0a1 1 0 0 0 0 .66a7.5 7.5 0 0 0 '
    '13.888 0"/>')

PILL_SOLID = ('<div style="display:inline-block;background:#FF9500;color:#000;font-family:\'DM Mono\','
              'monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;'
              'padding:5px 12px;border-radius:4px;">{}</div>')
PILL_OUTLINE = ('<div style="display:inline-block;border:1px solid rgba(255,255,255,0.2);'
                'color:rgba(255,255,255,0.5);font-family:\'DM Mono\',monospace;font-size:9px;'
                'font-weight:500;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;'
                'border-radius:4px;">{}</div>')


def head_row(tag_html, badge_html, mb=20):
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;'
            f'margin-bottom:{mb}px;">{tag_html}{badge_html}</div>')


# ── COVER VISUAL ─────────────────────────────────────────────────────────────
# Dominant treatment this week: DATA-VIZ FACE-OFF (a sibling of the Stat/Numeral
# Hero treatment). Two proportional horizontal bars carrying the whole thesis at
# a glance: the reason you fixed is tiny, the reason you ignored is four times
# bigger. Deliberately different from the last three shipped covers:
#   2026-08-21 thumb-zone  -> device/diagram composition (phone outline + arc)
#   2026-08-14 trust       -> scattered icon-badge constellation
#   2026-07-31 advertorial -> flow-chain of boxes
# None of them carried a chart, so this reads as a genuinely new cover concept.
#
# Bar widths are honest to the data: 300px represents 40%, so the 9% bar is
# 300 * 9/40 = 67px. Do not eyeball these if the numbers ever change.
def bar_row(label, label_color, bar_w, bar_bg, value, value_color):
    return (
        '<div>'
        f'<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;'
        f'letter-spacing:2px;text-transform:uppercase;color:{label_color};margin-bottom:9px;">'
        f'{label}</div>'
        '<div style="display:flex;align-items:center;gap:12px;">'
        f'<div style="height:38px;width:{bar_w}px;border-radius:6px;background:{bar_bg};"></div>'
        f'<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:30px;line-height:1;'
        f'letter-spacing:-1px;color:{value_color};">{value}</div>'
        '</div></div>'
    )


COVER_VISUAL = (
    '<div style="position:relative;height:272px;border-radius:12px;overflow:hidden;background:#0a0a0a;'
    'border:1px solid rgba(255,255,255,0.1);flex-shrink:0;">'
    '<div style="position:absolute;bottom:-70px;right:-40px;width:240px;height:240px;border-radius:50%;'
    'background:radial-gradient(circle,rgba(255,149,0,0.20),transparent 70%);filter:blur(50px);'
    'pointer-events:none;"></div>'
    '<div style="position:absolute;top:-50px;left:-30px;width:190px;height:190px;border-radius:50%;'
    'background:radial-gradient(circle,rgba(123,47,190,0.16),transparent 70%);filter:blur(45px);'
    'pointer-events:none;"></div>'
    # space-between, not center: the first cut centred three items in the card and
    # left a visible dead band under the footnote on the exported PNG. Pinning the
    # footnote to the bottom edge fills the card instead. Verified on the export.
    '<div style="position:relative;z-index:2;height:100%;padding:26px 24px;display:flex;'
    'flex-direction:column;justify-content:space-between;">'
    + bar_row('Extra costs too high', '#FF9500', 300,
              'linear-gradient(90deg,#FF9500,#E040A0)', '40%', '#FF9500')
    + bar_row('Too few payment methods', 'rgba(255,255,255,0.4)', 67,
              'rgba(255,255,255,0.20)', '9%', 'rgba(255,255,255,0.45)')
    + '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:500;letter-spacing:1.6px;'
      'text-transform:uppercase;color:rgba(255,255,255,0.26);">Baymard: why shoppers abandon carts</div>'
    '</div></div>'
)

COVER_META = (
    '<div style="display:flex;align-items:center;gap:10px;margin-top:16px;">'
    '<div style="width:36px;height:36px;border-radius:50%;overflow:hidden;'
    'border:2px solid rgba(255,149,0,0.4);flex-shrink:0;">'
    '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" '
    'style="width:100%;height:100%;object-fit:cover;" onerror="this.parentNode.style.display=\'none\'">'
    '</div><div><div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:13px;color:#fff;">'
    'Ridwan Adekunle</div><div style="font-family:\'DM Mono\',monospace;font-size:10px;'
    'color:rgba(255,255,255,0.4);margin-top:1px;">Shopify CRO &amp; UX Designer</div></div></div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2.5px;'
    'text-transform:uppercase;color:rgba(255,255,255,0.35);margin-top:14px;">Conversion Strategy</div>'
)

COVER_HEADLINE = (
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:34px;line-height:1.16;'
    'letter-spacing:-1px;color:#fff;">You added Apple Pay. '
    '<span style="color:#FF9500;">They still left.</span></div></div>'
)

SWIPE = (
    '<div style="display:flex;align-items:center;gap:8px;">'
    '<span style="font-family:\'DM Mono\',monospace;font-size:10px;letter-spacing:2px;'
    'text-transform:uppercase;color:rgba(255,255,255,0.35);">Swipe</span>'
    '<div style="width:48px;height:1px;background:linear-gradient(to right,rgba(255,255,255,0.2),'
    '#FF9500);"></div><svg width="16" height="16" viewBox="0 0 16 16" fill="none">'
    '<path d="M6 4l4 4-4 4" stroke="#FF9500" stroke-width="1.5" stroke-linecap="round" '
    'stroke-linejoin="round"/></svg></div>'
)

S1 = slide('#080808', GLOWS, COVER_VISUAL + COVER_META + COVER_HEADLINE + SWIPE)

# ── SLIDE 2 — THE MYTH ───────────────────────────────────────────────────────
S2 = slide('#0a0a0a', GLOWS, (
    head_row(PILL_SOLID.format('The myth'), badge(ICON_CARD)) +
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:40px;line-height:1.18;'
    'letter-spacing:-1.4px;color:#fff;">They left because<br>I don\'t take<br>their payment method.</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.6;margin-top:24px;max-width:400px;">So you switched on three more wallets and '
    'waited for the numbers to move.</div></div>'
))

# ── SLIDE 3 — STAT / PROOF (numeral hero on a SECOND Baymard fact) ───────────
# Deliberately not a repeat of the cover's 40/9 bars: a different published
# number, in a different visual form (numeral + field-stack comparison), so the
# proof slide adds evidence instead of restating the cover.
# The field-stack comparison also exists to fill the frame: numeral + text alone
# left a dead band at the bottom on the first cut of last week's equivalent slide.
def field_stack(n, w, color):
    """One thin rounded bar per form element. The ROW COUNT IS THE CLAIM, so it
    must match the cited figure exactly: 23 rows for Baymard's 23.48 average,
    13 rows for the midpoint of their 12-14 ideal. The first cut drew 12 vs 7,
    which quietly misrepresented both numbers on a slide whose whole job is
    citing them. Never eyeball these counts."""
    return ''.join(
        f'<div style="height:4px;width:{w}px;border-radius:2px;background:{color};'
        f'margin-bottom:3px;"></div>' for _ in range(n))


FIELD_COMPARE = (
    '<div style="display:flex;align-items:flex-end;gap:34px;">'
    '<div style="display:flex;flex-direction:column;align-items:flex-start;gap:10px;">'
    '<div>' + field_stack(23, 128, 'rgba(255,255,255,0.14)') + '</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2px;'
    'text-transform:uppercase;color:rgba(255,255,255,0.35);">Average &middot; 23</div></div>'
    '<div style="display:flex;flex-direction:column;align-items:flex-start;gap:10px;">'
    '<div>' + field_stack(13, 128, 'rgba(255,149,0,0.55)') + '</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2px;'
    'text-transform:uppercase;color:#FF9500;">Ideal &middot; 12 to 14</div></div>'
    '</div>'
)

S3 = slide('#0d0b08', GLOWS_ALT, (
    '<div style="margin-bottom:20px;">' + PILL_OUTLINE.format('The count') + '</div>'
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;">'
    '<div><div style="display:flex;align-items:baseline;gap:6px;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:104px;line-height:1;'
    'letter-spacing:-3px;color:#FF9500;">23</div>'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:34px;line-height:1;'
    'letter-spacing:-1px;color:#FF9500;">.48</div></div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:12px;font-weight:500;letter-spacing:2px;'
    'text-transform:uppercase;color:rgba(255,255,255,0.5);margin-top:12px;">'
    'Form elements in the average US checkout</div>'
    '<div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,'
    '#FF9500,#E040A0,#7B2FBE);margin:18px 0;"></div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.65;max-width:420px;">Baymard puts an ideal checkout at 12 to 14. Your buyer is '
    'filling in the difference.</div></div>' + FIELD_COMPARE + '</div>'
))

# ── SLIDE 4 — THE REALITY ────────────────────────────────────────────────────
S4 = slide('#0a0a0a', GLOWS, (
    head_row(PILL_OUTLINE.format('The reality'), badge(ICON_RECEIPT)) +
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:38px;line-height:1.16;'
    'letter-spacing:-1.4px;color:#fff;">Nobody abandons a checkout they can already '
    '<span style="color:#FF9500;">see the end of.</span></div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.6;margin-top:24px;max-width:410px;">40 in 100 leave over the total. '
    '9 in 100 leave over payment choice.</div></div>'
))


# ── SLIDE 5 — WHERE IT SHOWS UP ──────────────────────────────────────────────
def xpill(label):
    return ('<span style="position:relative;font-family:\'DM Mono\',monospace;font-size:13px;'
            'padding:5px 28px 5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;'
            f'color:rgba(255,255,255,0.3);">{label}'
            '<span style="position:absolute;right:10px;top:50%;transform:translateY(-50%);'
            'font-size:9px;color:#FF9500;">&#10005;</span></span>')


S5 = slide('#0a0a0a', GLOWS_ALT, (
    '<div style="margin-bottom:18px;">' + PILL_OUTLINE.format('Where it shows up') + '</div>'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:32px;line-height:1.18;'
    'letter-spacing:-1px;color:#fff;">Every one of these is a smaller fix than the total.</div>'
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;margin:8px 0;">'
    '<div style="display:flex;flex-wrap:wrap;gap:8px;">' +
    xpill('ANOTHER WALLET BUTTON') + xpill('A SECOND TRUST BADGE') + xpill('EXIT POPUP, 10% OFF') +
    xpill('SHIPPING REVEALED AT STEP 3') + xpill('ACCOUNT REQUIRED TO PAY') +
    '</div>'
    '<div><div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;'
    'letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-bottom:10px;">'
    'Build this instead</div>'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:24px;line-height:1.3;'
    'color:#FF9500;">Full total on the cart page. Guest checkout. Wallets last.</div></div>'
    '</div>'
))

# ── SLIDE 6 — THE FILTER ─────────────────────────────────────────────────────
S6 = slide('#0a0a0a', GLOWS, (
    head_row(PILL_SOLID.format('The filter'), badge(ICON_SCAN_EYE)) +
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:38px;line-height:1.16;'
    'letter-spacing:-1.4px;color:#fff;">Can a first time buyer see the real total before they pick '
    'how to pay?</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.6;margin-top:24px;max-width:410px;">If not, no payment button you add will fix it. '
    'Convert first, then get clever.</div></div>'
))

# ── SLIDE 7 — CTA ────────────────────────────────────────────────────────────
S7 = slide('#080808', GLOWS, (
    '<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;'
    'text-align:center;">'
    '<div style="width:150px;height:150px;border-radius:50%;overflow:hidden;'
    'border:2px solid rgba(255,149,0,0.4);margin-bottom:22px;flex-shrink:0;">'
    '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2" '
    'style="width:100%;height:100%;object-fit:cover;object-position:center top;" '
    'onerror="this.style.display=\'none\'"></div>'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:32px;line-height:1.14;'
    'letter-spacing:-1px;color:#fff;">Want to know where your checkout is leaking?</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.6;margin:16px 0 26px;max-width:380px;">I\'ll walk your cart and checkout the way '
    'a first time buyer sees it.</div>'
    '<div style="display:inline-flex;align-items:center;gap:8px;padding:13px 30px;'
    'background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;'
    'font-family:\'DM Mono\',monospace;font-weight:700;font-size:14px;border-radius:32px;">'
    'DM me "AUDIT" &rarr;</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.3);'
    'margin-top:22px;">Follow @koolestpro for more</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:12px;color:rgba(255,255,255,0.2);'
    'margin-top:6px;">Save this and open your own cart page.</div></div>'
))

TRACK = '<div id="track">\n\n' + '\n'.join([S1, S2, S3, S4, S5, S6, S7]) + '\n    </div>\n\n    '

# ── COPY TABS ────────────────────────────────────────────────────────────────
TAB_LINKEDIN = """You added Apple Pay. They still left.

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

TAB_HOOK = """You added Apple Pay. They still left.

Baymard puts "there weren't enough payment methods" at 9% of abandonments. Second from the bottom.

Extra costs sit at 40%, and another 12% can't work out the total before checkout.

The wallet row was never the problem. The number you're hiding is.

When does a first time buyer on your store actually see the real total?"""

TAB_THREAD = """1/ You added Apple Pay. They still left. The wallet row was never the thing costing you the sale.

2/ Baymard asked shoppers with real purchase intent why they abandoned. 9% said there weren't enough payment methods. Second from the bottom of the list.

3/ 40% said extra costs were too high. Shipping and tax showing up after they'd already decided to buy.

4/ Another 12% said they couldn't work out the total order cost up front at all.

5/ Same research: the average US checkout shows 23.48 form elements. An ideal one needs 12 to 14.

6/ So your checkout isn't short a payment button. It's carrying ten fields it doesn't need and hiding the total until step three.

7/ Fix the order instead. Full total on the cart page, guest checkout, fewer fields, wallets last. Follow @koolestpro for more Shopify CRO."""

TAB_SINGLES = """Tweet A (The Rule):
Adding a payment button is the cheapest fix on your checkout and the smallest one. 9% abandon over payment choice. 40% abandon over the total.

Tweet B (The Contrast):
Four wallet buttons, total revealed at step three. Or: total on the cart page, guest checkout, wallets last. Only one of those gets paid.

Tweet C (The Hot Take):
Most checkout optimisation is just turning on more payment providers. That isn't optimisation. That's adding options to a screen people already left."""

TAB_IG = """You added Apple Pay. They still left.

Baymard's abandonment research puts "not enough payment methods" at 9%. Second from the bottom.

Extra costs sit at 40%. Another 12% can't work out the total before checkout.

The average US checkout shows 23.48 form elements. An ideal one needs 12 to 14.

Your checkout isn't short a button. It's hiding the number people care about.

Save this. Follow @koolestpro for more Shopify CRO tips.

#ShopifyDesign #CRO #eCommerce #ShopifyDeveloper #ConversionOptimization #WebDesign #Shopify #UXDesign #DigitalMarketing #ShopifyLiquid"""

LK_CAPTION = (
    "    <strong>You added Apple Pay. They still left.</strong><br>\n"
    "    Baymard puts \"there weren't enough payment methods\" at 9% of abandonments. Extra costs "
    "sit at 40%.<br>\n"
)


def swap_region(html, start_lit, end_lit, new, label):
    i = html.find(start_lit)
    if i < 0:
        sys.exit(f'FAIL: start boundary not found for {label}')
    j = html.find(end_lit, i + len(start_lit))
    if j < 0:
        sys.exit(f'FAIL: end boundary not found for {label}')
    return html[:i] + new + html[j:]


def swap_lit(html, old, new, label, expect=1):
    n = html.count(old)
    if n != expect:
        sys.exit(f'FAIL: {label} found {n} times, expected {expect}')
    return html.replace(old, new)


def main():
    h = open(BASE, encoding='utf-8').read()

    # 1. slides
    h = swap_region(h, '<div id="track">', '<!-- /track -->', TRACK, 'track')

    # 2. LinkedIn preview caption inside the frame
    h = swap_region(
        h, '  <div class="lk-caption" data-chrome>\n', '    <span class="lk-see-more">',
        '  <div class="lk-caption" data-chrome>\n' + LK_CAPTION, 'lk-caption')

    # 3. copy tabs
    for tab_id, text in [('tab-linkedin', TAB_LINKEDIN), ('tab-hook', TAB_HOOK),
                         ('tab-twitter-thread', TAB_THREAD),
                         ('tab-twitter-angles', TAB_SINGLES), ('tab-ig', TAB_IG)]:
        start = f'<div id="{tab_id}" class="tab-panel'
        i = h.find(start)
        if i < 0:
            sys.exit(f'FAIL: tab {tab_id} not found')
        ps = h.find('<pre>', i)
        pe = h.find('</pre>', ps)
        h = h[:ps] + '<pre>' + text + h[pe:]

    # 4. per-post constants / filenames / titles
    h = swap_lit(h, '<title>Mobile Thumb Zone: Reach Beats Responsive @koolestpro</title>',
                 '<title>Checkout Abandonment: The Payment Method Myth @koolestpro</title>', 'title')
    h = swap_lit(h, "const POST_SLUG   = 'thumb-zone-mobile-reach';",
                 f"const POST_SLUG   = '{SLUG}';", 'POST_SLUG')
    h = swap_lit(h, "const POST_FOLDER = 'outputs/tips/thumb-zone-mobile-reach_2026-08-21.html';",
                 f"const POST_FOLDER = '{FOLDER}';", 'POST_FOLDER')
    h = swap_lit(h, '`koolestpro_thumb-zone_slide${idx + 1}.png`',
                 '`koolestpro_' + DL + '_slide${idx + 1}.png`', 'slide dl name')
    h = swap_lit(h, "pdf.save('koolestpro_thumb-zone.pdf');",
                 f"pdf.save('koolestpro_{DL}.pdf');", 'pdf name')
    h = swap_lit(h, "a.download = 'koolestpro_thumb-zone_' + name + '.png';",
                 "a.download = 'koolestpro_" + DL + "_' + name + '.png';", 'card dl name')
    h = swap_lit(h, 'title: "Your store isn\'t mobile optimised. It just fits the screen.",',
                 f'title: "{TITLE}",', 'pipeline title')

    # 5. project-wide no-em-dash rule: assert none survive in rendered content.
    #    (Base file already had its pipeline-panel em dashes fixed upstream.)
    visible = re.sub(r'<!--.*?-->', '', h, flags=re.S)
    if '—' in visible or '&mdash;' in visible:
        sys.exit('FAIL: em dash present in rendered content')

    open(OUT, 'w', encoding='utf-8').write(h)

    # ── verification: whole-file and per-slide div balance ───────────────────
    o, c = h.count('<div'), h.count('</div>')
    print(f'whole file: <div={o}  </div>={c}  {"OK" if o == c else "MISMATCH"}')
    i = h.find('<div id="track">')
    j = h.find('<!-- /track -->')
    parts = h[i:j].split('<div class="slide"')
    print(f'slides in track: {len(parts) - 1}')
    for k, s in enumerate(parts[1:], 1):
        so, sc = s.count('<div') + 1, s.count('</div>')
        print(f'  slide {k}: <div={so} </div>={sc} {"OK" if so == sc else "MISMATCH"}')
    print('wrote', OUT)
    if o != c:
        sys.exit(1)


if __name__ == '__main__':
    main()
