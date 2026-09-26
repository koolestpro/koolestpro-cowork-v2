#!/usr/bin/env python3
"""
Region-swap builder for the Tips carousel:
"Six levels. Six jobs." (typography hierarchy, Myth vs Reality)

Base: outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html
      (the approved V2 reference — CSS, JS, 540x680 geometry, scale:2 capture
       and chrome-hiding are reused byte-for-byte)

Only content regions are swapped, each by an exact literal string match.
Every replacement asserts a match count of exactly 1 before applying.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REF = os.path.join(ROOT, "outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html")
OUT = os.path.join(ROOT, "outputs/tips/typography-hierarchy-six-levels_2026-09-18.html")

SLUG = "typography-hierarchy-six-levels"
FOLDER = "outputs/tips/typography-hierarchy-six-levels_2026-09-18.html"
TITLE = "Six levels. Six jobs."

# ──────────────────────────────────────────────────────────────────────
# Shared slide chrome
# ──────────────────────────────────────────────────────────────────────

DOTGRID = ('<div style="position:absolute;inset:0;background-image:radial-gradient('
           'rgba(255,255,255,0.025) 1px,transparent 1px);background-size:26px 26px;'
           'pointer-events:none;"></div>')


def glow(variant):
    """Glow layouts. Deliberately mirrored from the previous carousel
    (which put warm top-right / cool bottom-left on every slide)."""
    if variant == "a":  # warm top-left, cool bottom-right
        return (
            '<div style="position:absolute;top:-90px;left:-70px;width:340px;height:340px;'
            'border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.17),'
            'rgba(224,64,160,0.07),transparent 70%);filter:blur(70px);pointer-events:none;"></div>'
            '<div style="position:absolute;bottom:-70px;right:-50px;width:290px;height:290px;'
            'border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.16),'
            'transparent 70%);filter:blur(62px);pointer-events:none;"></div>'
        )
    if variant == "b":  # wide warm band across the middle
        return (
            '<div style="position:absolute;top:34%;left:-120px;width:780px;height:300px;'
            'border-radius:50%;background:radial-gradient(ellipse,rgba(255,149,0,0.14),'
            'rgba(224,64,160,0.05),transparent 70%);filter:blur(80px);pointer-events:none;"></div>'
            '<div style="position:absolute;bottom:-80px;left:-60px;width:260px;height:260px;'
            'border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.14),'
            'transparent 70%);filter:blur(60px);pointer-events:none;"></div>'
        )
    # "c" — cool top-right, warm bottom-left
    return (
        '<div style="position:absolute;top:-80px;right:-60px;width:320px;height:320px;'
        'border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.17),'
        'transparent 70%);filter:blur(68px);pointer-events:none;"></div>'
        '<div style="position:absolute;bottom:-70px;left:-50px;width:300px;height:300px;'
        'border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.16),'
        'rgba(224,64,160,0.06),transparent 70%);filter:blur(64px);pointer-events:none;"></div>'
    )


def chips(n):
    """Bottom overlays. Both sit on a semi-opaque backdrop chip so they stay
    legible against whatever is actually behind them at that position."""
    return (
        f'<div style="position:absolute;bottom:16px;left:22px;z-index:12;'
        'background:rgba(0,0,0,0.58);border:1px solid rgba(255,255,255,0.09);'
        'border-radius:20px;padding:5px 13px;font-family:\'DM Mono\',monospace;'
        f'font-size:12px;font-weight:500;color:rgba(255,255,255,0.5);">{n} / 7</div>'
        '<div style="position:absolute;bottom:16px;right:22px;z-index:12;'
        'background:rgba(0,0,0,0.58);border:1px solid rgba(255,255,255,0.09);'
        'border-radius:20px;padding:5px 13px;font-family:\'DM Mono\',monospace;'
        'font-size:12px;color:rgba(255,255,255,0.4);">Ridwan &middot; Shopify CRO</div>'
    )


def badge(icon_paths):
    return (
        '<div style="width:44px;height:44px;border-radius:50%;background:rgba(255,149,0,0.08);'
        'border:1px solid rgba(255,149,0,0.25);display:flex;align-items:center;'
        'justify-content:center;flex-shrink:0;">'
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FF9500" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        + icon_paths + '</svg></div>'
    )


# Iconify / lucide paths, fetched once and inlined (no network at capture time).
ICON_TYPE = '<path d="M12 4v16M4 7V5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2M9 20h6"/>'
ICON_RANK = ('<path d="M11 5h10m-10 7h10m-10 7h10M4 4h1v5M4 9h2m.5 11H3.4c0-1 2.6-1.925 '
             '2.6-3.5a1.5 1.5 0 0 0-2.6-1.02"/>')
ICON_SCAN = ('<path d="M3 7V5a2 2 0 0 1 2-2h2m10 0h2a2 2 0 0 1 2 2v2m0 10v2a2 2 0 0 1-2 2h-2M7 '
             '21H5a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="1"/>'
             '<path d="M18.944 12.33a1 1 0 0 0 0-.66a7.5 7.5 0 0 0-13.888 0a1 1 0 0 0 0 .66a7.5 '
             '7.5 0 0 0 13.888 0"/>')
ICON_ALIGN = '<path d="M15 12H3m14 6H3M21 6H3"/>'
ICON_SPACE = ('<path d="M12 22v-6m0-8V2M4 12H2m8 0H8m8 0h-2m8 0h-2m-5 7l-3 3l-3-3m6-14l-3-3l-3 3"/>')

SHELL_OPEN = ('<div style="position:relative;z-index:2;padding:44px 42px 68px;height:100%;'
              'display:flex;flex-direction:column;">')

EYEBROW_SOLID = ('<div style="display:inline-block;background:#FF9500;color:#000;'
                 'font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;'
                 'letter-spacing:2px;text-transform:uppercase;padding:5px 12px;'
                 'border-radius:4px;">{}</div>')

EYEBROW_OUTLINE = ('<div style="display:inline-block;border:1px solid rgba(255,255,255,0.22);'
                   'color:rgba(255,255,255,0.5);font-family:\'DM Mono\',monospace;font-size:9px;'
                   'font-weight:500;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;'
                   'border-radius:4px;">{}</div>')


def toprow(eyebrow_html, icon_paths):
    return ('<div style="display:flex;align-items:center;justify-content:space-between;'
            'margin-bottom:18px;flex-shrink:0;">' + eyebrow_html + badge(icon_paths) + '</div>')


def anchor(text):
    """Bottom anchor strip for statement slides. Verified on the exported PNG:
    without it, a vertically centred statement leaves a large empty band under
    the copy. Carries a real 'so what', not filler."""
    return ('<div style="flex-shrink:0;margin-top:18px;">'
            '<div style="height:2px;width:100%;border-radius:1px;background:linear-gradient('
            'to right,rgba(255,149,0,0.55),rgba(224,64,160,0.3),rgba(123,47,190,0));'
            'margin-bottom:14px;"></div>'
            '<div style="font-family:\'DM Mono\',monospace;font-size:14px;line-height:1.55;'
            f'color:rgba(255,255,255,0.42);">{text}</div></div>')


# ──────────────────────────────────────────────────────────────────────
# SLIDE 1 — cover. Visual anchor: the squint test, two page mocks side by
# side. Built from flat low-contrast bars rather than CSS filter:blur on
# content, so html2canvas renders it deterministically.
# ──────────────────────────────────────────────────────────────────────

def bar(w, h, color, radius=None, mb=9):
    r = radius if radius is not None else min(h // 2, 6)
    return (f'<div style="width:{w};height:{h}px;border-radius:{r}px;background:{color};'
            f'margin-bottom:{mb}px;"></div>')


# The bar stack sits in its own flex:1 column with space-between so it fills
# the mock's full height. Checked on the export: without this the left mock
# stopped a third of the way down and left a dead band inside the panel.
FILL_COL = ('<div style="flex:1;display:flex;flex-direction:column;'
            'justify-content:space-between;">')

FAIL_MOCK = (
    '<div style="flex:1;background:#0d0d0d;border:1px solid rgba(255,255,255,0.07);'
    'border-radius:10px;padding:14px 13px;display:flex;flex-direction:column;">'
    '<div style="font-family:\'DM Mono\',monospace;font-size:10px;font-weight:700;'
    'letter-spacing:1.6px;text-transform:uppercase;color:rgba(255,255,255,0.32);'
    'margin-bottom:13px;">Nothing wins</div>'
    + FILL_COL
    + bar('88%', 15, 'rgba(255,255,255,0.3)', mb=0)
    + bar('76%', 15, 'rgba(255,255,255,0.29)', mb=0)
    + bar('92%', 15, 'rgba(255,255,255,0.3)', mb=0)
    + bar('70%', 15, 'rgba(255,255,255,0.28)', mb=0)
    + bar('84%', 15, 'rgba(255,255,255,0.3)', mb=0)
    + bar('64%', 15, 'rgba(255,255,255,0.29)', mb=0)
    + bar('80%', 15, 'rgba(255,255,255,0.3)', mb=0)
    + bar('74%', 15, 'rgba(255,255,255,0.3)', mb=0)
    + '</div></div>'
)

PASS_MOCK = (
    '<div style="flex:1;background:#0d0d0d;border:1px solid rgba(255,149,0,0.28);'
    'border-radius:10px;padding:14px 13px;display:flex;flex-direction:column;">'
    '<div style="font-family:\'DM Mono\',monospace;font-size:10px;font-weight:700;'
    'letter-spacing:1.6px;text-transform:uppercase;color:#FF9500;'
    'margin-bottom:13px;">One winner</div>'
    + FILL_COL
    + '<div>' + bar('92%', 32, 'rgba(255,255,255,0.92)', radius=6, mb=14)
    + bar('60%', 10, 'rgba(255,255,255,0.16)')
    + bar('72%', 10, 'rgba(255,255,255,0.15)')
    + bar('54%', 10, 'rgba(255,255,255,0.16)', mb=0) + '</div>'
    + '<div>' + bar('66%', 30, 'linear-gradient(90deg,#FF9500,#E040A0)', radius=15, mb=14)
    + bar('44%', 8, 'rgba(255,255,255,0.12)', mb=0) + '</div>'
    + '</div></div>'
)

SLIDE1 = (
    '<div class="slide" style="background:#080808;">'
    + glow('a') + DOTGRID + SHELL_OPEN
    + '<div style="height:296px;border-radius:14px;background:#0a0a0a;'
      'border:1px solid rgba(255,255,255,0.09);padding:16px;display:flex;gap:14px;'
      'flex-shrink:0;position:relative;">'
    + FAIL_MOCK + PASS_MOCK
    + '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);'
      'width:34px;height:34px;border-radius:50%;background:#080808;'
      'border:1px solid rgba(255,255,255,0.14);display:flex;align-items:center;'
      'justify-content:center;font-family:\'DM Mono\',monospace;font-size:11px;'
      'font-weight:700;color:rgba(255,255,255,0.4);">vs</div>'
    + '</div>'
    + '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
      '<div style="display:inline-block;align-self:flex-start;background:#FF9500;color:#000;'
      'font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2px;'
      'text-transform:uppercase;padding:5px 12px;border-radius:4px;margin-bottom:16px;">'
      'Typography</div>'
      '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:37px;'
      'line-height:1.15;letter-spacing:-1.3px;color:#fff;">Your headline got bigger.<br>'
      'The page still feels <span style="color:#FF9500;">flat</span>.</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:15px;line-height:1.65;'
      'color:rgba(255,255,255,0.5);margin-top:16px;max-width:400px;">'
      'Squint at your product page. If nothing jumps out, size was never the problem.</div>'
      '</div>'
    + '<div style="display:flex;align-items:center;gap:11px;flex-shrink:0;">'
      '<div style="width:38px;height:38px;border-radius:50%;overflow:hidden;'
      'border:2px solid rgba(255,149,0,0.4);flex-shrink:0;">'
      '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" '
      'style="width:100%;height:100%;object-fit:cover;" onerror="this.style.display=\'none\'"></div>'
      '<div><div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:14px;'
      'color:#e8e8e8;">Ridwan Adekunle</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:12px;'
      'color:rgba(255,255,255,0.35);">@koolestpro</div></div></div>'
    + '</div>'
    + '<div style="position:absolute;bottom:16px;right:22px;z-index:12;'
      'background:rgba(0,0,0,0.58);border:1px solid rgba(255,255,255,0.09);'
      'border-radius:20px;padding:5px 13px;font-family:\'DM Mono\',monospace;'
      'font-size:12px;color:rgba(255,255,255,0.4);">Swipe &rarr;</div>'
    + '</div>'
)

# ──────────────────────────────────────────────────────────────────────
# SLIDE 2 — THE MYTH. Large redundant pill badge plus the small eyebrow.
# ──────────────────────────────────────────────────────────────────────

BIG_PILL_SOLID = (
    '<div style="display:inline-flex;align-self:flex-start;align-items:center;'
    'background:#FF9500;color:#000;font-family:\'Syne\',sans-serif;font-weight:800;'
    'font-size:24px;letter-spacing:0.5px;padding:10px 26px;border-radius:30px;'
    'margin-bottom:22px;">MYTH</div>'
)

BIG_PILL_OUTLINE = (
    '<div style="display:inline-flex;align-self:flex-start;align-items:center;'
    'background:rgba(255,149,0,0.1);border:2px solid #FF9500;color:#fff;'
    'font-family:\'Syne\',sans-serif;font-weight:800;font-size:24px;letter-spacing:0.5px;'
    'padding:9px 26px;border-radius:30px;margin-bottom:22px;">REALITY</div>'
)

SLIDE2 = (
    '<div class="slide" style="background:#0a0a0a;">'
    + glow('b') + DOTGRID + SHELL_OPEN
    + toprow(EYEBROW_SOLID.format('The myth'), ICON_TYPE)
    + '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    + BIG_PILL_SOLID
    + '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:44px;'
      'line-height:1.13;letter-spacing:-1.6px;color:#fff;">If it matters,<br>make it bigger.</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:15px;line-height:1.7;'
      'color:rgba(255,255,255,0.5);margin-top:24px;max-width:405px;">'
      'So the H1 grows. Then the subhead grows to keep up. Then the price. '
      'Now the whole page is loud and nothing leads.</div>'
      '</div>'
    + anchor('Loud is not the same as clear. Swipe for what is actually going on.')
    + '</div>'
    + chips(2) + '</div>'
)

# ──────────────────────────────────────────────────────────────────────
# SLIDE 3 — THE REALITY
# ──────────────────────────────────────────────────────────────────────

SLIDE3 = (
    '<div class="slide" style="background:#080808;">'
    + glow('c') + DOTGRID + SHELL_OPEN
    + toprow(EYEBROW_OUTLINE.format('The reality'), ICON_RANK)
    + '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    + BIG_PILL_OUTLINE
    + '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:42px;'
      'line-height:1.13;letter-spacing:-1.5px;color:#fff;">Hierarchy is a '
      '<span style="color:#FF9500;">ranking</span>.<br>Not a size.</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:15px;line-height:1.7;'
      'color:rgba(255,255,255,0.5);margin-top:24px;max-width:405px;">'
      'Six things set at 32px is not six levels. It is one level, printed six times.</div>'
      '</div>'
    + anchor('A ranking needs a number one. Most product pages never pick one.')
    + '</div>'
    + chips(3) + '</div>'
)

# ──────────────────────────────────────────────────────────────────────
# SLIDE 4 — credibility. Real, attributable finding. No invented numbers.
# ──────────────────────────────────────────────────────────────────────

SLIDE4 = (
    '<div class="slide" style="background:#0a0a0a;">'
    + glow('a') + DOTGRID + SHELL_OPEN
    + toprow(EYEBROW_OUTLINE.format('Why it breaks'), ICON_SCAN)
    + '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
      '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:112px;'
      'line-height:0.95;letter-spacing:-5px;color:#FF9500;">28%</div>'
      '<div style="height:3px;width:56px;border-radius:2px;'
      'background:linear-gradient(to right,#FF9500,#E040A0,#7B2FBE);margin:22px 0 20px;"></div>'
      '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:29px;'
      'line-height:1.22;letter-spacing:-0.8px;color:#fff;max-width:420px;">'
      'is the most of a page people actually read.</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:15px;line-height:1.7;'
      'color:rgba(255,255,255,0.5);margin-top:18px;max-width:410px;">'
      'Nielsen Norman Group, on an average visit. Nobody is reading your page. '
      'They are hunting for the one thing that wins.</div>'
      '</div>'
    + anchor('So give them one. One winner per screen, and a job for every level under it.')
    + '</div>'
    + chips(4) + '</div>'
)

# ──────────────────────────────────────────────────────────────────────
# SLIDE 5 — the six-level ladder. The list is also the specimen: each row
# is set at the size its own level would use.
# ──────────────────────────────────────────────────────────────────────

LEVELS = [
    ("1", "Page promise", "the outcome", 22, "#fff"),
    ("2", "Section signpost", "where am I", 20, "rgba(255,255,255,0.93)"),
    ("3", "Block claim", "why this part", 18, "rgba(255,255,255,0.86)"),
    ("4", "Body", "the proof", 16, "rgba(255,255,255,0.72)"),
    ("5", "Action", "the button", 15, "rgba(255,255,255,0.62)"),
    ("6", "Fine print", "the risk", 13, "rgba(255,255,255,0.5)"),
]


def level_row(num, name, job, size, color):
    return (
        '<div style="display:flex;align-items:center;gap:14px;">'
        '<div style="width:28px;height:28px;border-radius:50%;background:rgba(255,149,0,0.1);'
        'border:1px solid rgba(255,149,0,0.32);display:flex;align-items:center;'
        'justify-content:center;flex-shrink:0;font-family:\'DM Mono\',monospace;'
        f'font-size:13px;font-weight:700;color:#FF9500;">{num}</div>'
        f'<div style="flex:1;font-family:\'Syne\',sans-serif;font-weight:700;font-size:{size}px;'
        f'letter-spacing:-0.4px;color:{color};">{name}</div>'
        '<div style="font-family:\'DM Mono\',monospace;font-size:13px;'
        f'color:rgba(255,255,255,0.38);text-align:right;flex-shrink:0;">{job}</div>'
        '</div>'
    )


SLIDE5 = (
    '<div class="slide" style="background:#080808;">'
    + glow('b') + DOTGRID + SHELL_OPEN
    + toprow(EYEBROW_SOLID.format('The system'), ICON_ALIGN)
    + '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:34px;'
      'line-height:1.15;letter-spacing:-1.1px;color:#fff;flex-shrink:0;">'
      'Six levels.<br>Six <span style="color:#FF9500;">jobs</span>.</div>'
    + '<div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;'
      'margin-top:10px;">'
    + "".join(level_row(*lv) for lv in LEVELS)
    + '</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:14px;line-height:1.6;'
      'color:rgba(255,255,255,0.42);flex-shrink:0;">'
      'If a level has no job, it is not a level. Delete it.</div>'
      '</div>'
    + chips(5) + '</div>'
)

# ──────────────────────────────────────────────────────────────────────
# SLIDE 6 — the missing level: space. Cramped vs spaced, same type sizes.
# ──────────────────────────────────────────────────────────────────────

def space_mock(label, label_color, border, gap, justify):
    """Identical bars in both columns. Only the gaps differ, which is the whole
    claim. The bar stack is vertically centred inside the mock so the cramped
    column doesn't leave a dead band under itself (caught on the first export)."""
    rows = (
        bar('86%', 13, 'rgba(255,255,255,0.85)', mb=gap)
        + bar('62%', 9, 'rgba(255,255,255,0.3)', mb=gap)
        + bar('74%', 9, 'rgba(255,255,255,0.3)', mb=gap)
        + bar('58%', 9, 'rgba(255,255,255,0.3)', mb=gap)
        + bar('80%', 13, 'rgba(255,255,255,0.85)', mb=gap)
        + bar('66%', 9, 'rgba(255,255,255,0.3)', mb=0)
    )
    return (
        f'<div style="flex:1;background:#0d0d0d;border:1px solid {border};border-radius:10px;'
        'padding:14px 13px;display:flex;flex-direction:column;">'
        '<div style="font-family:\'DM Mono\',monospace;font-size:10px;font-weight:700;'
        f'letter-spacing:1.6px;text-transform:uppercase;color:{label_color};'
        f'margin-bottom:12px;flex-shrink:0;">{label}</div>'
        f'<div style="flex:1;display:flex;flex-direction:column;justify-content:{justify};">'
        f'{rows}</div></div>'
    )


SLIDE6 = (
    '<div class="slide" style="background:#0a0a0a;">'
    + glow('c') + DOTGRID + SHELL_OPEN
    + toprow(EYEBROW_SOLID.format('The missing level'), ICON_SPACE)
    + '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:36px;'
      'line-height:1.15;letter-spacing:-1.3px;color:#fff;flex-shrink:0;">'
      'Two of your six<br>levels are pure '
      '<span style="color:#FF9500;">space</span>.</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:15px;line-height:1.65;'
      'color:rgba(255,255,255,0.5);margin-top:14px;flex-shrink:0;max-width:410px;">'
      'Same type sizes on both sides. Only the gaps changed.</div>'
    + '<div style="flex:1;display:flex;gap:14px;margin:18px 0 0;min-height:0;">'
    + space_mock('Cramped', 'rgba(255,255,255,0.32)', 'rgba(255,255,255,0.07)', 5, 'flex-start')
    + space_mock('Spaced', '#FF9500', 'rgba(255,149,0,0.28)', 15, 'space-between')
    + '</div>'
    + '<div style="flex-shrink:0;margin-top:16px;font-family:\'DM Mono\',monospace;'
      'font-size:14px;line-height:1.55;color:rgba(255,255,255,0.42);">'
      'Nothing got bigger. Things stopped touching.</div>'
    + '</div>'
    + chips(6) + '</div>'
)

# ──────────────────────────────────────────────────────────────────────
# SLIDE 7 — CTA. Points at a real destination on the domain.
# ──────────────────────────────────────────────────────────────────────

SLIDE7 = (
    '<div class="slide" style="background:#080808;">'
    + glow('a') + DOTGRID
    + '<div style="position:relative;z-index:2;padding:44px 42px 68px;height:100%;'
      'display:flex;flex-direction:column;">'
      '<div style="flex:1;display:flex;flex-direction:column;align-items:center;'
      'justify-content:center;text-align:center;">'
      '<div style="width:144px;height:144px;border-radius:50%;overflow:hidden;'
      'border:2px solid rgba(255,149,0,0.4);margin-bottom:22px;flex-shrink:0;">'
      '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2" '
      'style="width:100%;height:100%;object-fit:cover;object-position:center top;" '
      'onerror="this.style.display=\'none\'"></div>'
      '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:33px;'
      'line-height:1.16;letter-spacing:-1px;color:#fff;max-width:420px;">'
      'Which level is<br>your page missing?</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:15px;line-height:1.6;'
      'color:rgba(255,255,255,0.5);margin:16px 0 26px;max-width:390px;">'
      'I audit Shopify product pages for hierarchy and conversion path.</div>'
      '<div style="display:inline-flex;align-items:center;gap:8px;padding:13px 30px;'
      'background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;'
      'font-family:\'DM Mono\',monospace;font-weight:700;font-size:14px;border-radius:32px;">'
      'Get a CRO audit &rarr;</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:#FF9500;'
      'margin-top:18px;">koolestpro.com/services/cro-audit</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:15px;'
      'color:rgba(255,255,255,0.3);margin-top:16px;">Follow @koolestpro for more</div>'
      '<div style="font-family:\'DM Mono\',monospace;font-size:13px;'
      'color:rgba(255,255,255,0.2);margin-top:6px;">Save this for your next build.</div>'
      '</div></div>'
    + '<div style="position:absolute;bottom:16px;left:22px;z-index:12;'
      'background:rgba(0,0,0,0.58);border:1px solid rgba(255,255,255,0.09);'
      'border-radius:20px;padding:5px 13px;font-family:\'DM Mono\',monospace;'
      'font-size:12px;font-weight:500;color:rgba(255,255,255,0.5);">7 / 7</div>'
      '<div style="position:absolute;bottom:16px;right:22px;z-index:12;'
      'background:rgba(0,0,0,0.58);border:1px solid rgba(255,255,255,0.09);'
      'border-radius:20px;padding:5px 13px;font-family:\'DM Mono\',monospace;'
      'font-size:12px;color:rgba(255,255,255,0.4);">Ridwan &middot; Shopify CRO</div>'
    + '</div>'
)

SLIDES = "\n".join([SLIDE1, SLIDE2, SLIDE3, SLIDE4, SLIDE5, SLIDE6, SLIDE7])

# ──────────────────────────────────────────────────────────────────────
# Post copy (humanizer pass applied: no em dashes, no AI filler, no
# blocklist terms, varied sentence length, real line breaks)
# ──────────────────────────────────────────────────────────────────────

LINKEDIN = """Your headline got bigger. The page still feels flat.

I did this for years. Client says the page feels muddy, I bump the H1, they still say it feels muddy. So I bump the subhead so it doesn't look orphaned. Then the price, so it doesn't get lost. Two rounds later everything is bigger and nothing leads.

Here's what I had wrong. Hierarchy is a ranking, not a size. Six things set at 32px is not six levels. It's one level, printed six times.

Nielsen Norman Group put the number on it: on an average visit, people read at most about 28% of the words on a page. They are not reading. They are scanning for the one thing that wins. If your page doesn't hand them a winner in two seconds, they pick one for you, and it's rarely the one you wanted.

So I stopped counting sizes and started assigning jobs. Six levels, six jobs:

1. Page promise, the outcome
2. Section signpost, where am I
3. Block claim, why this part
4. Body, the proof
5. Action, the button
6. Fine print, the risk

If a level has no job, it isn't a level. Delete it.

And the part most people skip: two of those six levels can be pure space. Same type sizes, different gaps, and suddenly the page reads. Nothing had to get bigger. Things just had to stop touching.

Quick test before you ship. Look at your product page at arm's length and squint. Name what you see first. If you can't do it in two seconds, you don't have a hierarchy problem you can solve with font sizes.

Design isn't decoration, it's direction.

Repost if your last redesign ended with everything one step bigger.

Running a Shopify store and not sure which level yours is missing? I audit product pages for hierarchy and conversion path: koolestpro.com/services/cro-audit"""

HOOK = """Your headline got bigger. The page still feels flat.

Hierarchy is a ranking, not a size. Six things at 32px is one level, printed six times.

Six levels, six jobs. If a level has no job, delete it.

What's the last page you fixed by making something smaller?"""

X_THREAD = """1/ Your headline got bigger. The page still feels flat. Here's the typography thing almost every Shopify store gets backwards:

2/ The myth: if it matters, make it bigger. So the H1 grows. Then the subhead grows to keep up. Then the price. Now everything is loud and nothing leads.

3/ The reality: hierarchy is a ranking, not a size. Six things set at 32px is not six levels. It's one level, printed six times.

4/ Nielsen Norman Group: on an average visit people read at most about 28% of the words on a page. They aren't reading. They're hunting for the one thing that wins.

5/ Stop counting sizes. Assign jobs. Page promise (the outcome), section signpost (where am I), block claim (why this part), body (the proof), action (the button), fine print (the risk).

6/ Two of those six levels can be pure space. Same sizes, bigger gaps, and the page finally reads. Nothing got bigger. Things stopped touching.

7/ Test it: squint at your PDP. Name what you see first. Can't do it in two seconds? Font size won't save you. More Shopify CRO: @koolestpro"""

X_SINGLES = """THE RULE
Hierarchy is a ranking, not a size.

Six things set at 32px is not six levels. It's one level, printed six times.

THE CONTRAST
Bumping the H1 to 48px: everything else grows to keep up, nothing leads.

Adding 40px of space above it: nothing got bigger, and it finally wins.

THE HOT TAKE
Most "the page feels flat" feedback gets fixed with spacing, not font size. You keep reaching for the size picker because it's the only lever you've been taught."""

INSTAGRAM = """Your headline got bigger. The page still feels flat.

Hierarchy is a ranking, not a size. Six things set at 32px is not six levels. It's one level, printed six times.

Nielsen Norman Group found people read at most about 28% of the words on a page. They're scanning for the one thing that wins. Give them one.

Six levels, six jobs:
Page promise, the outcome
Section signpost, where am I
Block claim, why this part
Body, the proof
Action, the button
Fine print, the risk

Two of those can be pure space. Nothing has to get bigger. Things just have to stop touching.

Save this for your next build. Follow @koolestpro for more Shopify CRO.

#ShopifyDesign #CRO #eCommerce #ShopifyDeveloper #ConversionOptimization #WebDesign #Shopify #UXDesign #Typography #ProductPage"""


# ──────────────────────────────────────────────────────────────────────
# Region swap
# ──────────────────────────────────────────────────────────────────────

def swap(html, old, new, label):
    n = html.count(old)
    if n != 1:
        raise SystemExit(f"[FAIL] {label}: expected exactly 1 match, found {n}")
    print(f"  [ok] {label}")
    return html.replace(old, new)


def main():
    html = open(REF, encoding="utf-8").read()

    # 1. title
    html = swap(html,
                "<title>Animation Budget V2 (Prototype) — @koolestpro</title>",
                f"<title>{TITLE} &middot; Typography Hierarchy &middot; @koolestpro</title>",
                "title")

    # 2. drop the V2 prototype review banner (this is a production file)
    banner_start = html.index('<div style="max-width:588px;margin:0 auto 28px;padding:14px 18px;'
                              'background:rgba(255,149,0,0.08);')
    banner_end = html.index('</div>', banner_start) + len('</div>')
    banner = html[banner_start:banner_end]
    html = swap(html, banner + "\n\n", "", "prototype banner removed")

    # 3. slides (whole track region, exact literal boundaries)
    track_open = '  <div id="viewport">\n    <div id="track">\n\n'
    track_close = '\n\n    </div><!-- /track -->'
    s = html.index(track_open) + len(track_open)
    e = html.index(track_close)
    old_slides = html[s:e]
    html = swap(html, old_slides, SLIDES, "7 slides swapped")

    # 4. LinkedIn preview caption
    html = swap(html,
                "<strong>Your store's animations aren't making it look premium. "
                "They're making it convert worse.</strong><br>\n    Motion isn't free. "
                "Every effect adds delay, and delay costs sales. Spend it on decisions, "
                "cut it everywhere else.<br>",
                "<strong>Your headline got bigger. The page still feels flat.</strong><br>\n"
                "    Hierarchy is a ranking, not a size. Six things at 32px is one level, "
                "printed six times. Six levels, six jobs.<br>",
                "lk caption")

    # 5. JS constants + export filenames
    html = swap(html, "const POST_SLUG   = 'animation-budget-motion-conversion-v2';",
                f"const POST_SLUG   = '{SLUG}';", "POST_SLUG")
    html = swap(html,
                "const POST_FOLDER = 'outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html';",
                f"const POST_FOLDER = '{FOLDER}';", "POST_FOLDER")
    html = swap(html, "`koolestpro_animation-budget-v2_slide${idx + 1}.png`",
                "`koolestpro_typography-hierarchy_slide${idx + 1}.png`", "png filename")
    html = swap(html, "pdf.save('koolestpro_animation-budget-v2.pdf');",
                "pdf.save('koolestpro_typography-hierarchy.pdf');", "pdf filename")
    html = swap(html, "a.download = 'koolestpro_animation-budget_' + name + '.png';",
                "a.download = 'koolestpro_typography-hierarchy_' + name + '.png';", "card filename")
    html = swap(html, 'title: "Your store\'s animations are costing you sales",',
                f'title: "{TITLE}",', "pipeline title")

    # 5b. em dashes inherited from the reference's own UI copy
    html = swap(html, "'✓ Exported — open ridwan_content_system_updated.html and sync.'",
                "'✓ Exported. Open ridwan_content_system_updated.html and sync.'",
                "pipeline status em dash")
    html = swap(html,
                "Downloads a <code>.json</code> file — open "
                "<code>ridwan_content_system_updated.html</code> and sync to register it.",
                "Downloads a <code>.json</code> file. Open "
                "<code>ridwan_content_system_updated.html</code> and sync to register it.",
                "pipeline blurb em dash")

    # 6. post copy tabs
    def replace_pre(html, panel_id, new_text, label):
        anchor = f'<div id="{panel_id}" class="tab-panel'
        i = html.index(anchor)
        s = html.index("<pre>", i) + len("<pre>")
        e = html.index("</pre>", s)
        return swap(html, html[s:e], new_text, label)

    html = replace_pre(html, "tab-linkedin", LINKEDIN, "tab linkedin")
    html = replace_pre(html, "tab-hook", HOOK, "tab hook")
    html = replace_pre(html, "tab-twitter-thread", X_THREAD, "tab x thread")
    html = replace_pre(html, "tab-twitter-angles", X_SINGLES, "tab x singles")
    html = replace_pre(html, "tab-ig", INSTAGRAM, "tab instagram")

    # ── validation ──
    # No em dashes in any *copy* the reader sees. Structural HTML comments
    # carried over from the reference (section dividers) are not copy.
    bad = [ln for ln in html.split("\n")
           if ("—" in ln or "&mdash;" in ln)
           and "SECTION" not in ln
           and "<title>" not in ln]
    if bad:
        raise SystemExit(f"[FAIL] em dash found in {len(bad)} line(s): {bad[0][:160]}")

    for forbidden in ["background-clip:text", "background-clip: text",
                      "-webkit-text-fill-color", 'fill="url(#grad']:
        if forbidden in html:
            raise SystemExit(f"[FAIL] gradient text construct present: {forbidden}")

    opens = html.count("<div")
    closes = html.count("</div>")
    print(f"\n  div balance: {opens} open / {closes} close")
    if opens != closes:
        raise SystemExit(f"[FAIL] div imbalance: {opens} vs {closes}")

    for idx, slide in enumerate([SLIDE1, SLIDE2, SLIDE3, SLIDE4, SLIDE5, SLIDE6, SLIDE7], 1):
        o, c = slide.count("<div"), slide.count("</div>")
        status = "ok" if o == c else "FAIL"
        print(f"  slide {idx}: {o} open / {c} close  [{status}]")
        if o != c:
            raise SystemExit(f"[FAIL] slide {idx} div imbalance")

    open(OUT, "w", encoding="utf-8").write(html)
    print(f"\n  wrote {OUT} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
