#!/usr/bin/env python3
"""
Region-swap builder for the 2026-08-21 Tips carousel:
"Your store isn't mobile optimised. It just fits the screen." (thumb zone / mobile reach)

Base file: outputs/tips/trust-signals-over-credibility_2026-08-14.html
  (itself a structural clone of the approved V2 reference
   animation-budget-motion-conversion-v2_2026-07-28.html: 540x680 portrait,
   scale:2 capture, mandatory chrome-hiding, headline-only density)

Only slide content strings, copy-tab text and the per-post constants are swapped.
JS / CSS / geometry / capture functions are reused byte-for-byte.
Every replacement uses an exact literal boundary, never a lazy multi-slide regex.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, 'outputs/tips/trust-signals-over-credibility_2026-08-14.html')
OUT = os.path.join(ROOT, 'outputs/tips/thumb-zone-mobile-reach_2026-08-21.html')

SLUG = 'thumb-zone-mobile-reach'
FOLDER = 'outputs/tips/thumb-zone-mobile-reach_2026-08-21.html'
TITLE = "Your store isn't mobile optimised. It just fits the screen."
DL = 'thumb-zone'

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


ICON_PHONE = '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>'
ICON_HAND = ('<path d="M18 11V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2m0 4V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v2m0 '
             '4.5V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 '
             '0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>')
ICON_TARGET = ('<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/>'
               '<circle cx="12" cy="12" r="2"/>')

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
# Dominant treatment this week: geometric/diagrammatic composition. A phone
# outline with a warm thumb-reach arc sweeping the bottom third, the buy button
# stranded in the dimmed top zone. Deliberately different from 2026-08-14's
# scattered icon-badge constellation and 2026-07-31's flow-chain of boxes.
#
# NOTE on bounding the reach arc: html2canvas does NOT honour `overflow:hidden`
# on an absolutely-positioned child that extends past its parent, so the first
# cut of this visual had the arc bleeding out past the phone's right edge in the
# exported PNG (fine in the browser, broken in the export). Fixed by making both
# arc layers bounded by construction: the shaded region is a radial-gradient
# background on an inset:0 div (can't exceed its box), and the arc stroke is an
# inline SVG whose circle is clipped at the SVG's own declared width/height,
# which html2canvas *does* enforce (see CLAUDE.md's SVG viewBox rule).
COVER_VISUAL = (
    '<div style="position:relative;height:272px;border-radius:12px;overflow:hidden;background:#0a0a0a;'
    'border:1px solid rgba(255,255,255,0.1);flex-shrink:0;display:flex;align-items:center;'
    'justify-content:center;">'
    '<div style="position:absolute;bottom:-70px;right:-40px;width:240px;height:240px;border-radius:50%;'
    'background:radial-gradient(circle,rgba(255,149,0,0.20),transparent 70%);filter:blur(50px);'
    'pointer-events:none;"></div>'
    '<div style="position:absolute;top:-50px;left:-30px;width:190px;height:190px;border-radius:50%;'
    'background:radial-gradient(circle,rgba(123,47,190,0.16),transparent 70%);filter:blur(45px);'
    'pointer-events:none;"></div>'
    # phone body (inner content box is exactly 136 x 216)
    '<div style="position:relative;z-index:2;width:136px;height:216px;border-radius:20px;'
    'border:1.5px solid rgba(255,255,255,0.3);background:#0d0d0d;overflow:hidden;'
    'box-shadow:0 0 40px rgba(0,0,0,0.6);">'
    # reach shading, bounded by its own box
    # stops run all the way to 100% of the 124px radius so the shaded region ends
    # exactly where the SVG arc stroke below sits. An earlier cut faded out at 73%
    # and read as a separate glow disc floating inside the arc.
    '<div style="position:absolute;inset:0;background:radial-gradient(circle 124px at 100% 97%,'
    'rgba(255,149,0,0.26) 0%,rgba(255,149,0,0.16) 55%,rgba(255,149,0,0.08) 88%,'
    'rgba(255,149,0,0.03) 99%,transparent 100%);"></div>'
    # reach boundary line, clipped at the SVG's declared 136x216 bounds
    '<svg width="136" height="216" viewBox="0 0 136 216" fill="none" '
    'style="position:absolute;top:0;left:0;display:block;">'
    '<circle cx="136" cy="210" r="124" stroke="#FF9500" stroke-opacity="0.55" stroke-width="1.3" '
    'fill="none"/></svg>'
    # stranded buy button, top zone
    '<div style="position:absolute;top:16px;left:13px;right:13px;height:26px;border-radius:6px;'
    'border:1px dashed rgba(255,255,255,0.3);display:flex;align-items:center;justify-content:center;'
    'font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:1px;'
    'color:rgba(255,255,255,0.45);">ADD TO CART</div>'
    # undersized swatch row, mid zone
    '<div style="position:absolute;top:56px;left:13px;display:flex;gap:6px;">'
    '<div style="width:13px;height:13px;border-radius:3px;border:1px solid rgba(255,255,255,0.22);"></div>'
    '<div style="width:13px;height:13px;border-radius:3px;border:1px solid rgba(255,255,255,0.22);"></div>'
    '<div style="width:13px;height:13px;border-radius:3px;border:1px solid rgba(255,255,255,0.22);"></div>'
    '</div>'
    # body lines
    '<div style="position:absolute;top:82px;left:13px;right:32px;height:6px;border-radius:3px;'
    'background:rgba(255,255,255,0.07);"></div>'
    '<div style="position:absolute;top:96px;left:13px;right:50px;height:6px;border-radius:3px;'
    'background:rgba(255,255,255,0.07);"></div>'
    # thumb pivot dot
    '<div style="position:absolute;bottom:12px;right:12px;width:16px;height:16px;border-radius:50%;'
    'background:#FF9500;box-shadow:0 0 18px rgba(255,149,0,0.7);"></div>'
    '</div>'
    # zone captions
    '<div style="position:absolute;top:24px;left:26px;font-family:\'DM Mono\',monospace;font-size:9px;'
    'font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.32);">'
    'Out of reach</div>'
    '<div style="position:absolute;bottom:24px;right:26px;font-family:\'DM Mono\',monospace;font-size:9px;'
    'font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;">Thumb zone</div>'
    '</div>'
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
    'text-transform:uppercase;color:rgba(255,255,255,0.35);margin-top:14px;">Digital Craftsmanship</div>'
)

COVER_HEADLINE = (
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:28px;line-height:1.18;'
    'letter-spacing:-0.5px;color:#fff;">Your store isn\'t mobile optimised. '
    'It just <span style="color:#FF9500;">fits the screen.</span></div></div>'
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
    head_row(PILL_SOLID.format('The myth'), badge(ICON_PHONE)) +
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    # 40px, not 44px: at 44 "on my phone." wrapped onto its own second line in the
    # export and broke the three-beat rhythm of the myth. Verified on the PNG.
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:40px;line-height:1.18;'
    'letter-spacing:-1.4px;color:#fff;">It looks fine<br>on my phone.<br>So it\'s ready.</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.6;margin-top:24px;max-width:400px;">That check tests your layout. '
    'It never tests the hand holding it.</div></div>'
))

# ── SLIDE 3 — STAT / PROOF (numeral hero, real published standard) ───────────
# The tap-target comparison below the numeral is not decoration: the first cut of
# this slide was numeral + text only and left ~22% dead bands top and bottom on
# the exported PNG. Showing 44pt against a typical 28px swatch fills the frame
# AND makes the number concrete instead of abstract.
TAP_COMPARE = (
    '<div style="display:flex;align-items:flex-end;gap:26px;">'
    '<div style="display:flex;flex-direction:column;align-items:center;gap:10px;">'
    '<div style="width:84px;height:84px;border-radius:12px;border:1.5px solid #FF9500;'
    'background:rgba(255,149,0,0.12);display:flex;align-items:center;justify-content:center;'
    'font-family:\'Syne\',sans-serif;font-weight:800;font-size:20px;color:#FF9500;">44</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2px;'
    'text-transform:uppercase;color:#FF9500;">Hits every time</div></div>'
    '<div style="display:flex;flex-direction:column;align-items:center;gap:10px;">'
    '<div style="width:53px;height:53px;border-radius:8px;border:1px dashed rgba(255,255,255,0.28);'
    'display:flex;align-items:center;justify-content:center;font-family:\'Syne\',sans-serif;'
    'font-weight:800;font-size:15px;color:rgba(255,255,255,0.42);">28</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2px;'
    'text-transform:uppercase;color:rgba(255,255,255,0.35);">Needs aiming</div></div>'
    '</div>'
)

S3 = slide('#0d0b08', GLOWS_ALT, (
    '<div style="margin-bottom:20px;">' + PILL_OUTLINE.format('The standard') + '</div>'
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;">'
    '<div><div style="display:flex;align-items:baseline;gap:10px;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:104px;line-height:1;'
    'letter-spacing:-3px;color:#FF9500;">44</div>'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:34px;line-height:1;'
    'letter-spacing:-1px;color:#FF9500;">pt</div></div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:12px;font-weight:500;letter-spacing:2px;'
    'text-transform:uppercase;color:rgba(255,255,255,0.5);margin-top:12px;">'
    'Apple\'s published minimum tap target</div>'
    '<div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,'
    '#FF9500,#E040A0,#7B2FBE);margin:18px 0;"></div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.65;max-width:420px;">Google says 48dp. Both standards are older than your theme. '
    'Go measure your swatches against them.</div></div>' + TAP_COMPARE + '</div>'
))

# ── SLIDE 4 — THE REALITY ────────────────────────────────────────────────────
S4 = slide('#0a0a0a', GLOWS, (
    head_row(PILL_OUTLINE.format('The reality'), badge(ICON_HAND)) +
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:40px;line-height:1.16;'
    'letter-spacing:-1.4px;color:#fff;">Responsive is about the screen. '
    'Buying happens in <span style="color:#FF9500;">the thumb\'s reach.</span></div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.6;margin-top:24px;max-width:400px;">One hand, on the move. That is how your '
    'product page actually gets used.</div></div>'
))

# ── SLIDE 5 — HOW IT SHOWS UP ────────────────────────────────────────────────
def xpill(label):
    return ('<span style="position:relative;font-family:\'DM Mono\',monospace;font-size:13px;'
            'padding:5px 28px 5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;'
            f'color:rgba(255,255,255,0.3);">{label}'
            '<span style="position:absolute;right:10px;top:50%;transform:translateY(-50%);'
            'font-size:9px;color:#FF9500;">&#10005;</span></span>')


S5 = slide('#0a0a0a', GLOWS_ALT, (
    '<div style="margin-bottom:18px;">' + PILL_OUTLINE.format('Where it shows up') + '</div>'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:32px;line-height:1.18;'
    'letter-spacing:-1px;color:#fff;">Every one of these sits outside the arc.</div>'
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;margin:8px 0;">'
    '<div style="display:flex;flex-wrap:wrap;gap:8px;">' +
    xpill('ADD TO CART ONLY UP TOP') + xpill('28PX SWATCHES') + xpill('TOP-LEFT FILTER BAR') +
    xpill('PINHEAD QTY STEPPERS') + xpill('CLOSE X IN THE CORNER') +
    '</div>'
    '<div><div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;'
    'letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-bottom:10px;">'
    'Build this instead</div>'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:24px;line-height:1.3;'
    'color:#FF9500;">A sticky buy bar in the bottom third. Nothing else fighting it.</div></div>'
    '</div>'
))

# ── SLIDE 6 — THE FILTER ─────────────────────────────────────────────────────
S6 = slide('#0a0a0a', GLOWS, (
    head_row(PILL_SOLID.format('The filter'), badge(ICON_TARGET)) +
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:40px;line-height:1.16;'
    'letter-spacing:-1.4px;color:#fff;">Can you buy it with one thumb, standing up?</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.6;margin-top:24px;max-width:410px;">If it takes two hands, the layout is the '
    'problem. Every click is a choice, so make the choice easy to hit.</div></div>'
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
    'letter-spacing:-1px;color:#fff;">Want to know what\'s out of reach on your store?</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.6;margin:16px 0 26px;max-width:380px;">I\'ll check your product page the way '
    'your customers actually hold it.</div>'
    '<div style="display:inline-flex;align-items:center;gap:8px;padding:13px 30px;'
    'background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;'
    'font-family:\'DM Mono\',monospace;font-weight:700;font-size:14px;border-radius:32px;">'
    'DM me "AUDIT" &rarr;</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.3);'
    'margin-top:22px;">Follow @koolestpro for more</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:12px;color:rgba(255,255,255,0.2);'
    'margin-top:6px;">Save this and test your own PDP tonight.</div></div>'
))

TRACK = '<div id="track">\n\n' + '\n'.join([S1, S2, S3, S4, S5, S6, S7]) + '\n    </div>\n\n    '

# ── COPY TABS ────────────────────────────────────────────────────────────────
TAB_LINKEDIN = """Your store isn't mobile optimised. It just fits the screen.

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

TAB_HOOK = """Your store isn't mobile optimised. It just fits the screen.

Responsive means the layout reflows. It says nothing about whether a thumb can reach the button.

Your customer is one handed, on the move, aiming at a 28px swatch.

What's the last thing on your product page you actually tried to tap one handed?"""

TAB_THREAD = """1/ Your store isn't mobile optimised. It just fits the screen. Those are two different things and only one of them sells.

2/ Responsive means the layout reflows at 390px. It says nothing about whether a thumb can reach the button that takes the money.

3/ The test most owners run: phone in both hands, at a desk. The test that matters: one hand, standing up, thumb anchored bottom right.

4/ Apple has published a 44pt minimum tap target for years. Google says 48dp. Go measure the swatches on your own product page.

5/ What I keep finding: add to cart only above the fold, swatches sized for a mouse, filters in the top left corner, steppers you have to aim at.

6/ None of it needs a redesign. Move the decisions into the bottom third of the screen and size them to be hit without looking.

7/ One filter for every mobile layout: can you buy it with one thumb, standing up? Follow @koolestpro for more Shopify CRO."""

TAB_SINGLES = """THE RULE
Responsive is about the screen. Buying happens in the thumb's reach. Your layout can pass one and fail the other on the same page.

THE CONTRAST
Add to cart above the fold only: a stretch every time. A sticky buy bar in the bottom third: one thumb, no aiming, no thought.

THE HOT TAKE
Most mobile testing is a founder holding their phone in two hands at a desk. That is not a test. That is a screenshot with extra steps."""

TAB_IG = """Your store isn't mobile optimised. It just fits the screen.

Responsive means the layout reflows. It says nothing about whether a thumb can reach the button.

Apple's minimum tap target is 44pt. Google says 48dp. Most swatches ship smaller.

Move the decisions into the bottom third of the screen.

Can you buy it with one thumb, standing up?

Save this. Follow @koolestpro for more Shopify CRO tips.

#ShopifyDesign #CRO #eCommerce #ShopifyDeveloper #ConversionOptimization #WebDesign #Shopify #UXDesign #DigitalMarketing #ShopifyLiquid"""

LK_CAPTION = (
    "    <strong>Your store isn't mobile optimised. It just fits the screen.</strong><br>\n"
    "    Responsive means the layout reflows. It says nothing about whether a thumb can reach the "
    "button that takes the money.<br>\n"
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
    h = swap_lit(h, '<title>Trust Signals That Kill Sales: @koolestpro</title>',
                 '<title>Mobile Thumb Zone: Reach Beats Responsive @koolestpro</title>', 'title')
    h = swap_lit(h, "const POST_SLUG   = 'trust-signals-over-credibility-problem';",
                 f"const POST_SLUG   = '{SLUG}';", 'POST_SLUG')
    h = swap_lit(h, "const POST_FOLDER = 'outputs/tips/trust-signals-over-credibility_2026-08-14.html';",
                 f"const POST_FOLDER = '{FOLDER}';", 'POST_FOLDER')
    h = swap_lit(h, '`koolestpro_trust-signals_slide${idx + 1}.png`',
                 '`koolestpro_' + DL + '_slide${idx + 1}.png`', 'slide dl name')
    h = swap_lit(h, "pdf.save('koolestpro_trust-signals.pdf');",
                 f"pdf.save('koolestpro_{DL}.pdf');", 'pdf name')
    h = swap_lit(h, "a.download = 'koolestpro_trust-signals_' + name + '.png';",
                 "a.download = 'koolestpro_" + DL + "_' + name + '.png';", 'card dl name')
    h = swap_lit(h, 'title: "Trust Signals That Kill Sales: The Over-Credibility Problem",',
                 f'title: "{TITLE}",', 'pipeline title')

    # 5. inherited em dash in the pipeline-export panel's own UI chrome. Not
    #    publishable copy, but the no-em-dash rule is project-wide, so fix it
    #    here in the builder (reproducible) rather than by hand-editing output.
    h = swap_lit(h, 'file &mdash; open <code>' if '&mdash;' in h else 'file — open <code>',
                 'file. Open <code>', 'pipeline panel em dash')
    h = swap_lit(h, "'✓ Exported — open ridwan_content_system_updated.html and sync.'",
                 "'✓ Exported. Open ridwan_content_system_updated.html and sync.'",
                 'pipeline status em dash')
    # the only em dashes left are inside HTML comments (section dividers), which
    # are never rendered — assert that, so a real one can't slip back in later.
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
