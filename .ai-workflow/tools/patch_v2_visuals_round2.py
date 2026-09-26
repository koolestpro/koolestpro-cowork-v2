#!/usr/bin/env python3
"""Round 2 visual pass on the V2 Tips carousel prototype:
1. Replace the cover's stock-feeling real photo with a custom, on-topic
   motion visual (a UI button ghosting/trailing itself, like excess motion
   actually looks) built from CSS + an inline Iconify 'zap' icon -- no
   external image dependency, no stock photo standing in for the concept.
2. Add small Iconify icon-badge visual anchors to slides 2, 4, 6 (the
   text-only slides) so every slide carries a visual element, not just typography.
All icon SVG paths sourced from api.iconify.design (lucide set), inlined so
export doesn't depend on network reachability at capture time.
"""
import re, sys, pathlib

ROOT = pathlib.Path("/sessions/stoic-youthful-hamilton/mnt/koolestpro-cowork-v2")
TARGET = ROOT / "outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html"

html = TARGET.read_text(encoding="utf-8")

def replace_once(old, new, s, label=""):
    n = s.count(old)
    if n != 1:
        sys.exit(f"ANCHOR FAIL [{label}]: found {n} occurrences, expected 1")
    return s.replace(old, new, 1)

# ---- icon paths (lucide set via Iconify, fetched + inlined) ----
ICON_ZAP = '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>'
ICON_SPARKLES = '<path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594zM20 2v4m2-2h-4"/><circle cx="4" cy="20" r="2"/>'
ICON_WALLET = '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>'
ICON_HELP = '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3m.08 4h.01"/>'

def icon_badge(path, size=44, icon_size=22):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:rgba(255,149,0,0.08);'
            f'border:1px solid rgba(255,149,0,0.25);display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
            f'<svg width="{icon_size}" height="{icon_size}" viewBox="0 0 24 24" fill="none" stroke="#FF9500" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg></div>')

A = "'"

# =====================================================================
# 1. COVER SLIDE — replace stock product photo with a built motion visual
# =====================================================================
old_cover_img = (
 '<div style="border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,0.1);height:250px;flex-shrink:0;">'
 '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/v1785276545/koolestpro/tips-carousel/halos-pdp-hero-cover.png" '
 'style="width:100%;height:100%;object-fit:cover;object-position:center;" onerror="this.parentNode.style.display=' + A + 'none' + A + '"></div>'
)

def ghost(top, left, opacity, gradient=False):
    bg = 'background:linear-gradient(90deg,#FF9500,#E040A0);' if gradient else f'background:rgba(255,149,0,{opacity});'
    label = ('display:flex;align-items:center;justify-content:center;font-family:\'DM Mono\',monospace;'
              'font-size:11px;font-weight:700;color:#fff;letter-spacing:1px;') if gradient else ''
    content = 'ADD TO CART' if gradient else ''
    return (f'<div style="position:absolute;top:{top}px;left:{left}px;width:180px;height:46px;border-radius:23px;{bg}{label}">{content}</div>')

new_cover_visual = (
 '<div style="position:relative;height:250px;border-radius:12px;overflow:hidden;background:#0a0a0a;'
 'border:1px solid rgba(255,255,255,0.1);flex-shrink:0;">'
 '<div style="position:absolute;top:-60px;right:-40px;width:220px;height:220px;border-radius:50%;'
 'background:radial-gradient(circle,rgba(255,149,0,0.18),transparent 70%);filter:blur(50px);pointer-events:none;"></div>'
 '<div style="position:absolute;bottom:-50px;left:-30px;width:180px;height:180px;border-radius:50%;'
 'background:radial-gradient(circle,rgba(123,47,190,0.16),transparent 70%);filter:blur(45px);pointer-events:none;"></div>'
 + ghost(96, 66, 0.08)
 + ghost(88, 78, 0.16)
 + ghost(80, 90, 0.30)
 + ghost(72, 102, 0.55)
 + ghost(64, 114, 1, gradient=True)
 + f'<div style="position:absolute;top:16px;right:16px;width:40px;height:40px;border-radius:50%;'
   f'background:rgba(0,0,0,0.5);border:1px solid rgba(255,149,0,0.4);display:flex;align-items:center;justify-content:center;">'
   f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF9500" stroke-width="2" '
   f'stroke-linecap="round" stroke-linejoin="round">{ICON_ZAP}</svg></div>'
 '</div>'
)

html = replace_once(old_cover_img, new_cover_visual, html, label="cover-visual")

# =====================================================================
# 2. SLIDE 2 — icon badge next to "The myth" pill
# =====================================================================
old_s2_tag = ('<div style="margin-bottom:20px;"><div style="display:inline-block;background:#FF9500;color:#000;'
              'font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;'
              'padding:5px 12px;border-radius:4px;">The myth</div></div>')
new_s2_tag = ('<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">'
              '<div style="display:inline-block;background:#FF9500;color:#000;font-family:\'DM Mono\',monospace;'
              'font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;border-radius:4px;">The myth</div>'
              + icon_badge(ICON_SPARKLES) + '</div>')
html = replace_once(old_s2_tag, new_s2_tag, html, label="slide2-icon")

# =====================================================================
# 3. SLIDE 4 — icon badge next to "The reality" pill
# =====================================================================
old_s4_tag = ('<div style="margin-bottom:20px;"><div style="display:inline-block;background:#FF9500;color:#000;'
              'font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;'
              'padding:5px 12px;border-radius:4px;">The reality</div></div>')
new_s4_tag = ('<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">'
              '<div style="display:inline-block;background:#FF9500;color:#000;font-family:\'DM Mono\',monospace;'
              'font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;border-radius:4px;">The reality</div>'
              + icon_badge(ICON_WALLET) + '</div>')
html = replace_once(old_s4_tag, new_s4_tag, html, label="slide4-icon")

# =====================================================================
# 4. SLIDE 6 — icon badge next to the eyebrow label
# =====================================================================
old_s6_tag = ('<div style="font-family:\'DM Mono\',monospace;font-size:10px;font-weight:500;letter-spacing:2px;'
              'text-transform:uppercase;color:rgba(255,255,255,0.35);">The only question that matters</div>')
new_s6_tag = ('<div style="display:flex;align-items:center;justify-content:space-between;">'
              '<div style="font-family:\'DM Mono\',monospace;font-size:10px;font-weight:500;letter-spacing:2px;'
              'text-transform:uppercase;color:rgba(255,255,255,0.35);">The only question that matters</div>'
              + icon_badge(ICON_HELP) + '</div>')
html = replace_once(old_s6_tag, new_s6_tag, html, label="slide6-icon")

TARGET.write_text(html, encoding="utf-8")
print("PATCHED", TARGET, len(html), "chars")
