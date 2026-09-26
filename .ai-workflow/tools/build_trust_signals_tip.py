import re, sys

SRC = "outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html"
DST = "outputs/tips/trust-signals-over-credibility_2026-08-14.html"

with open(SRC, "r", encoding="utf-8") as f:
    text = f.read()

orig_open = text.count("<div")
orig_close = text.count("</div>")
assert orig_open == orig_close, f"reference file itself unbalanced: {orig_open} vs {orig_close}"

# ── 1. Title ──
old_title = "<title>Animation Budget V2 (Prototype) &mdash; @koolestpro</title>"
old_title2 = "<title>Animation Budget V2 (Prototype) — @koolestpro</title>"
new_title = "<title>Trust Signals That Kill Sales: @koolestpro</title>"
if old_title2 in text:
    assert text.count(old_title2) == 1
    text = text.replace(old_title2, new_title)
else:
    assert text.count(old_title) == 1
    text = text.replace(old_title, new_title)

# ── 2. Remove the "V2 FORMAT PROTOTYPE" review banner ──
banner_start = text.find('<div style="max-width:588px;margin:0 auto 28px;padding:14px 18px;background:rgba(255,149,0,0.08)')
banner_end = text.find("</div>", banner_start) + len("</div>")
assert banner_start != -1
text = text[:banner_start] + text[banner_end:]

# ── 3. Replace the 7-slide block (between <div id="track"> and its closing marker) ──
track_start_marker = '<div id="track">\n'
track_end_marker = '\n    </div><!-- /track -->'
ts = text.find(track_start_marker)
te = text.find(track_end_marker)
assert ts != -1 and te != -1 and te > ts, "track markers not found"
slides_region_start = ts + len(track_start_marker)

GLOW = '''<div style="position:absolute;top:-80px;right:-60px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.16),rgba(224,64,160,0.07),transparent 70%);filter:blur(70px);pointer-events:none;"></div>
<div style="position:absolute;bottom:-60px;left:-40px;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.15),transparent 70%);filter:blur(60px);pointer-events:none;"></div>
<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.02) 1px,transparent 1px);background-size:24px 24px;pointer-events:none;"></div>'''

ATTRIB = '<div style="position:absolute;bottom:18px;right:24px;font-family:\'DM Mono\',monospace;font-size:12px;color:rgba(255,255,255,0.18);z-index:10;">Ridwan - Shopify CRO &amp; UX Designer</div>'

ICON_SHIELD = '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12l2 2l4-4"/>'
ICON_BADGE = '<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77a4 4 0 0 1 6.74 0a4 4 0 0 1 4.78 4.78a4 4 0 0 1 0 6.74a4 4 0 0 1-4.77 4.78a4 4 0 0 1-6.75 0a4 4 0 0 1-4.78-4.77a4 4 0 0 1 0-6.76"/><path d="m9 12l2 2l4-4"/>'
ICON_LOCK = '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
ICON_LAYERS = '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z"/><path d="M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12"/><path d="M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17"/>'
ICON_TARGET = '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>'
ICON_HELP = '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3m.08 4h.01"/>'
ICON_AWARD = '<path d="m15.477 12.89l1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/>'
ICON_STAR = '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.12 2.12 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.12 2.12 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.12 2.12 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.12 2.12 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.12 2.12 0 0 0 1.597-1.16z"/>'

def icon_badge(icon_path, size=44, isize=22):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:rgba(255,149,0,0.08);'
            f'border:1px solid rgba(255,149,0,0.25);display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
            f'<svg width="{isize}" height="{isize}" viewBox="0 0 24 24" fill="none" stroke="#FF9500" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{icon_path}</svg></div>')

def small_badge_icon(icon_path, top=None, left=None, right=None, bottom=None, size=48, isize=20, opacity=0.32, rot=0):
    pos = []
    if top is not None: pos.append(f"top:{top}px")
    if left is not None: pos.append(f"left:{left}px")
    if right is not None: pos.append(f"right:{right}px")
    if bottom is not None: pos.append(f"bottom:{bottom}px")
    pos_str = ";".join(pos)
    transform = f"transform:rotate({rot}deg);" if rot else ""
    return (f'<div style="position:absolute;{pos_str};width:{size}px;height:{size}px;border-radius:50%;'
            f'background:rgba(255,149,0,0.06);border:1px solid rgba(255,149,0,0.16);display:flex;align-items:center;'
            f'justify-content:center;opacity:{opacity};{transform}">'
            f'<svg width="{isize}" height="{isize}" viewBox="0 0 24 24" fill="none" stroke="#FF9500" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{icon_path}</svg></div>')

# ── SLIDE 1 — COVER ──
cover_visual = (
    '<div style="position:relative;height:250px;border-radius:12px;overflow:hidden;background:#0a0a0a;border:1px solid rgba(255,255,255,0.1);flex-shrink:0;">'
    '<div style="position:absolute;top:-60px;right:-40px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.18),transparent 70%);filter:blur(50px);pointer-events:none;"></div>'
    '<div style="position:absolute;bottom:-50px;left:-30px;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.16),transparent 70%);filter:blur(45px);pointer-events:none;"></div>'
    + small_badge_icon(ICON_SHIELD, top=22, left=30, size=50, isize=22, opacity=0.4)
    + small_badge_icon(ICON_LOCK, top=18, right=42, size=42, isize=18, opacity=0.32, rot=-8)
    + small_badge_icon(ICON_STAR, bottom=26, left=52, size=44, isize=18, opacity=0.28)
    + small_badge_icon(ICON_AWARD, bottom=20, right=34, size=48, isize=20, opacity=0.3, rot=6)
    + small_badge_icon(ICON_LAYERS, top=64, left=128, size=38, isize=16, opacity=0.2)
    + small_badge_icon(ICON_LOCK, bottom=70, right=110, size=36, isize=15, opacity=0.18, rot=10)
    + '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:104px;height:104px;border-radius:50%;'
      'background:linear-gradient(135deg,rgba(255,149,0,0.28),rgba(123,47,190,0.22));border:1.5px solid #FF9500;'
      'box-shadow:0 0 34px rgba(255,149,0,0.32);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;">'
    f'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON_BADGE}</svg>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:1px;color:#fff;">REAL</div>'
    '</div>'
    '</div>'
)

slide1 = f'''<div class="slide" style="background:#080808;">
{GLOW}
<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;flex-direction:column;">
{cover_visual}<div style="display:flex;align-items:center;gap:10px;margin-top:16px;"><div style="width:36px;height:36px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,149,0,0.4);flex-shrink:0;"><img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" style="width:100%;height:100%;object-fit:cover;" onerror="this.parentNode.style.display='none'"></div><div><div style="font-family:'Syne',sans-serif;font-weight:700;font-size:13px;color:#fff;">Ridwan Adekunle</div><div style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.4);margin-top:1px;">Shopify CRO &amp; UX Designer</div></div></div><div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-top:14px;">Conversion Strategy</div><div style="flex:1;display:flex;flex-direction:column;justify-content:center;"><div style="font-family:'Syne',sans-serif;font-weight:800;font-size:28px;line-height:1.18;letter-spacing:-0.5px;color:#fff;">You think more trust badges build more trust. That's exactly what's making shoppers <span style="color:#FF9500;">bounce.</span></div></div><div style="display:flex;align-items:center;gap:8px;"><span style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);">Swipe</span><div style="width:48px;height:1px;background:linear-gradient(to right,rgba(255,255,255,0.2),#FF9500);"></div><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6 4l4 4-4 4" stroke="#FF9500" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
</div>
{ATTRIB}
</div>'''

# ── SLIDE 2 — THE MYTH ──
slide2 = f'''<div class="slide" style="background:#0a0a0a;">
{GLOW}
<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;flex-direction:column;">
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;"><div style="display:inline-block;background:#FF9500;color:#000;font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;border-radius:4px;">The myth</div>{icon_badge(ICON_LAYERS)}</div><div style="flex:1;display:flex;flex-direction:column;justify-content:center;"><div style="font-family:'Syne',sans-serif;font-weight:800;font-size:44px;line-height:1.16;letter-spacing:-1.5px;color:#fff;">Add every badge.<br>More proof.<br>More sales.</div><div style="font-family:'DM Mono',monospace;font-size:15px;color:rgba(255,255,255,0.5);line-height:1.6;margin-top:24px;max-width:400px;">That's the logic behind most Shopify product pages. It's backwards.</div></div>
</div>
{ATTRIB}
</div>'''

# ── SLIDE 3 — THE TELL (proof, no fabricated stat) ──
slide3 = f'''<div class="slide" style="background:#0d0b08;">
{GLOW}
<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;flex-direction:column;">
<div style="margin-bottom:20px;"><div style="display:inline-block;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.5);font-family:'DM Mono',monospace;font-size:9px;font-weight:500;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border-radius:4px;">The tell</div></div><div style="flex:1;display:flex;flex-direction:column;justify-content:center;"><div style="font-family:'Syne',sans-serif;font-weight:800;font-size:120px;line-height:1;letter-spacing:-4px;color:#FF9500;">1</div><div style="font-family:'DM Mono',monospace;font-size:12px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-top:10px;">real detail beats a row of badges</div><div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,#FF9500,#E040A0,#7B2FBE);margin:18px 0;"></div><div style="font-family:'DM Mono',monospace;font-size:15px;color:rgba(255,255,255,0.5);line-height:1.65;max-width:420px;">Not a percentage. A design principle: specific beats generic, every time a shopper is deciding whether to trust you.</div></div>
</div>
{ATTRIB}
</div>'''

# ── SLIDE 4 — THE REALITY ──
slide4 = f'''<div class="slide" style="background:#080808;">
{GLOW}
<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;flex-direction:column;">
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;"><div style="display:inline-block;background:#FF9500;color:#000;font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;border-radius:4px;">The reality</div>{icon_badge(ICON_TARGET)}</div><div style="flex:1;display:flex;flex-direction:column;justify-content:center;"><div style="font-family:'Syne',sans-serif;font-weight:800;font-size:36px;line-height:1.18;letter-spacing:-1px;color:#fff;">Past three badges, shoppers stop reading <span style="color:#FF9500;">proof.</span></div><div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,#FF9500,#E040A0,#7B2FBE);margin:18px 0;"></div><div style="font-family:'DM Mono',monospace;font-size:15px;color:rgba(255,255,255,0.5);line-height:1.7;max-width:400px;">A wall of logos doesn't build trust. It signals something here needs explaining.</div></div>
</div>
{ATTRIB}
</div>'''

# ── SLIDE 5 — HOW IT SHOWS UP (X pills + one clean statement) ──
def x_pill(label):
    return (f'<span style="position:relative;font-family:\'DM Mono\',monospace;font-size:13px;padding:5px 28px 5px 12px;'
            f'border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:rgba(255,255,255,0.3);">{label}'
            f'<span style="position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:9px;color:#FF9500;">&#10005;</span></span>')

pills = ''.join([x_pill(l) for l in ["SECURE CHECKOUT","MONEY-BACK","AS SEEN IN","VERIFIED","24/7 SUPPORT","TRUSTED BY THOUSANDS"]])

slide5 = f'''<div class="slide" style="background:#0a0a0a;">
{GLOW}
<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;flex-direction:column;">
<div style="margin-bottom:18px;"><div style="display:inline-block;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.5);font-family:'DM Mono',monospace;font-size:9px;font-weight:500;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border-radius:4px;">Where it shows up</div></div><div style="font-family:'Syne',sans-serif;font-weight:800;font-size:32px;line-height:1.18;letter-spacing:-1px;color:#fff;">Six generic badges lose to one specific truth.</div><div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;margin:8px 0;"><div style="display:flex;flex-wrap:wrap;gap:8px;">{pills}</div><div><div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-bottom:10px;">Keep this instead</div><div style="font-family:'Syne',sans-serif;font-weight:700;font-size:24px;line-height:1.3;color:#FF9500;">A real review. A real name. A real photo.</div></div></div>
</div>
{ATTRIB}
</div>'''

# ── SLIDE 6 — THE QUESTION ──
slide6 = f'''<div class="slide" style="background:#0a0a0a;">
{GLOW}
<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;flex-direction:column;">
<div style="display:flex;align-items:center;justify-content:space-between;"><div style="font-family:'DM Mono',monospace;font-size:10px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);">The only question that matters</div>{icon_badge(ICON_HELP)}</div><div style="flex:1;display:flex;flex-direction:column;justify-content:center;"><div style="font-family:'Syne',sans-serif;font-weight:800;font-size:34px;line-height:1.22;letter-spacing:-1px;color:#fff;">If you could keep only one trust signal, which one would you keep?</div><div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,#FF9500,#E040A0,#7B2FBE);margin:18px 0;"></div><div style="font-family:'Syne',sans-serif;font-weight:700;font-size:24px;color:#FF9500;">That's the only one doing any work.</div></div>
</div>
{ATTRIB}
</div>'''

# ── SLIDE 7 — CTA ──
slide7 = f'''<div class="slide" style="background:#080808;">
{GLOW}
<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;flex-direction:column;">
<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;"><div style="width:150px;height:150px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,149,0,0.4);margin-bottom:22px;flex-shrink:0;"><img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2" style="width:100%;height:100%;object-fit:cover;object-position:center top;" onerror="this.style.display='none'"></div><div style="font-family:'Syne',sans-serif;font-weight:800;font-size:32px;line-height:1.14;letter-spacing:-1px;color:#fff;">Want your product page to earn trust instead of performing it?</div><div style="font-family:'DM Mono',monospace;font-size:15px;color:rgba(255,255,255,0.5);line-height:1.6;margin:16px 0 26px;max-width:380px;">I'll audit which trust signals on yours are actually doing something.</div><div style="display:inline-flex;align-items:center;gap:8px;padding:13px 30px;background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;font-family:'DM Mono',monospace;font-weight:700;font-size:14px;border-radius:32px;">DM me "AUDIT" &rarr;</div><div style="font-family:'DM Mono',monospace;font-size:15px;color:rgba(255,255,255,0.3);margin-top:22px;">Follow @koolestpro for more</div><div style="font-family:'DM Mono',monospace;font-size:12px;color:rgba(255,255,255,0.2);margin-top:6px;">Save this before your next PDP audit.</div></div>
</div>
{ATTRIB}
</div>'''

new_slides_block = "\n\n".join([slide1, slide2, slide3, slide4, slide5, slide6, slide7]) + "\n"

text = text[:slides_region_start] + new_slides_block + text[te:]

# ── 4. lk-caption ──
old_caption = '''<strong>Your store's animations aren't making it look premium. They're making it convert worse.</strong><br>
    Motion isn't free. Every effect adds delay, and delay costs sales. Spend it on decisions, cut it everywhere else.<br>
    <span class="lk-see-more">...see more</span>'''
new_caption = '''<strong>You think more trust badges build more trust. That's exactly what's making shoppers bounce.</strong><br>
    Past three badges, shoppers stop reading proof and start reading defense. One real detail beats a row of them.<br>
    <span class="lk-see-more">...see more</span>'''
assert text.count(old_caption) == 1, "caption not found"
text = text.replace(old_caption, new_caption)

# ── 5. Constants ──
text = text.replace(
    "const POST_SLUG   = 'animation-budget-motion-conversion-v2';",
    "const POST_SLUG   = 'trust-signals-over-credibility-problem';"
)
text = text.replace(
    "const POST_FOLDER = 'outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html';",
    "const POST_FOLDER = 'outputs/tips/trust-signals-over-credibility_2026-08-14.html';"
)
text = text.replace(
    "title: \"Your store's animations are costing you sales\",",
    "title: \"Trust Signals That Kill Sales: The Over-Credibility Problem\","
)
text = text.replace("koolestpro_animation-budget-v2_slide", "koolestpro_trust-signals_slide")
text = text.replace("koolestpro_animation-budget-v2.pdf", "koolestpro_trust-signals.pdf")
text = text.replace("koolestpro_animation-budget_", "koolestpro_trust-signals_")

# ── 6. Download panel resolution note (unchanged, still 7 slides) — no edit needed ──

with open(DST, "w", encoding="utf-8") as f:
    f.write(text)

opens = text.count("<div")
closes = text.count("</div>")
print(f"div open={opens} close={closes} balanced={opens==closes}")
print("Written:", DST)
