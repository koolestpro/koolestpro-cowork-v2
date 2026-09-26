#!/usr/bin/env python3
"""
Region-swap builder for the weekly Tips carousel (koolestpro-tips-weekly).

Reuses outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html
byte-for-byte (CSS/JS/geometry) and swaps only:
  - <title>
  - the dev-only "V2 FORMAT PROTOTYPE" banner (removed)
  - the 7 slide content blocks (positional split on the `<div class="slide"`
    anchor, never a regex spanning multiple slides)
  - the LK caption preview text
  - the JS constants (POST_SLUG / POST_BRAND / POST_FOLDER) and every
    download filename derived from the old slug
  - the sendToPipeline() title field
  - the 5 post-copy tab <pre> bodies

This topic: "An advertorial is not a landing page" (tip-advertorial-what-it-
actually-is-20260510, existing backlog item, Conversion Strategy pillar,
Myth vs Reality format, 7 slides).
"""
import re
import sys

SRC = "outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html"
DST = "outputs/tips/advertorial-page-6-elements_2026-07-31.html"

OLD_SLUG = "animation-budget-motion-conversion-v2"
NEW_SLUG = "advertorial-page-6-elements"

with open(SRC, "r", encoding="utf-8") as f:
    text = f.read()

orig_open = text.count('<div class="slide"')
orig_open_all = text.count("<div")
orig_close_all = text.count("</div>")
print(f"[check] source file: {orig_open} slide blocks, <div>={orig_open_all} </div>={orig_close_all}")

# ── 1. Title ─────────────────────────────────────────────────────────────
text = text.replace(
    "<title>Animation Budget V2 (Prototype) — @koolestpro</title>",
    "<title>The Advertorial Isn't a Landing Page: @koolestpro</title>",
)

# ── 2. Remove the dev-only V2 prototype banner ──────────────────────────
banner_start = text.index('<div style="max-width:588px;margin:0 auto 28px;')
banner_end = text.index("</div>\n\n<!-- ══", banner_start) + len("</div>")
removed = text[banner_start:banner_end]
assert "V2 FORMAT PROTOTYPE" in removed, "banner anchor mismatch, aborting"
text = text[:banner_start] + text[banner_end:]

# ── 3. Slide content (positional split, not regex) ──────────────────────
ANCHOR = '<div class="slide" style="background:'
END_MARK = "    </div><!-- /track -->"

starts = [m.start() for m in re.finditer(re.escape(ANCHOR), text)]
assert len(starts) == 7, f"expected 7 slide blocks, found {len(starts)}"
end_of_last = text.index(END_MARK)

bounds = starts + [end_of_last]
old_blocks = [text[bounds[i]:bounds[i + 1]] for i in range(7)]
for i, b in enumerate(old_blocks):
    assert b.count("<div") == b.count("</div"), f"slide {i+1} source block unbalanced"

GLOW = (
    '<div style="position:absolute;top:-80px;right:-60px;width:340px;height:340px;'
    'border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.16),'
    'rgba(224,64,160,0.07),transparent 70%);filter:blur(70px);pointer-events:none;"></div>\n'
    '<div style="position:absolute;bottom:-60px;left:-40px;width:280px;height:280px;'
    'border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.15),'
    'transparent 70%);filter:blur(60px);pointer-events:none;"></div>\n'
    '<div style="position:absolute;inset:0;background-image:radial-gradient('
    'rgba(255,255,255,0.02) 1px,transparent 1px);background-size:24px 24px;'
    'pointer-events:none;"></div>\n'
)
ATTRIB = (
    '<div style="position:absolute;bottom:18px;right:24px;font-family:\'DM Mono\','
    'monospace;font-size:12px;color:rgba(255,255,255,0.18);z-index:10;">'
    "Ridwan - Shopify CRO &amp; UX Designer</div>\n"
)

ICON_FILE_TEXT = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24">'
    '<g fill="none" stroke="#FF9500" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">'
    '<path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/>'
    '<path d="M14 2v5a1 1 0 0 0 1 1h5M10 9H8m8 4H8m8 4H8"/></g></svg>'
)
ICON_SHIELD = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24">'
    '<g fill="none" stroke="#FF9500" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">'
    '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'
    '<path d="m9 12l2 2l4-4"/></g></svg>'
)
ICON_HELP = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24">'
    '<g fill="none" stroke="#FF9500" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">'
    '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3m.08 4h.01"/></g></svg>'
)


def slide(bg, inner):
    return (
        f'<div class="slide" style="background:{bg};">\n'
        f"{GLOW}"
        f'<div style="position:relative;z-index:2;padding:46px 44px;height:100%;'
        f'display:flex;flex-direction:column;">\n{inner}\n</div>\n{ATTRIB}</div>\n\n'
    )


# Slide 1 — Cover
s1_visual = (
    '<div style="position:relative;height:250px;border-radius:12px;overflow:hidden;'
    'background:#0a0a0a;border:1px solid rgba(255,255,255,0.1);flex-shrink:0;'
    'display:flex;align-items:center;justify-content:center;">'
    '<div style="position:absolute;top:-60px;right:-40px;width:220px;height:220px;'
    'border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.18),'
    'transparent 70%);filter:blur(50px);pointer-events:none;"></div>'
    '<div style="position:absolute;bottom:-50px;left:-30px;width:180px;height:180px;'
    'border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.16),'
    'transparent 70%);filter:blur(45px);pointer-events:none;"></div>'
    '<div style="position:relative;z-index:2;display:flex;align-items:center;'
    'justify-content:center;gap:0;">'
    '<div style="display:flex;flex-direction:column;align-items:center;opacity:0.4;">'
    '<div style="width:58px;height:58px;border-radius:12px;background:rgba(255,255,255,0.05);'
    'border:1px solid rgba(255,255,255,0.12);display:flex;align-items:center;'
    'justify-content:center;font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;'
    'letter-spacing:1px;color:rgba(255,255,255,0.55);text-align:center;line-height:1.3;">'
    "COLD<br>AD</div></div>"
    '<div style="font-family:\'DM Mono\',monospace;font-size:20px;color:rgba(255,255,255,0.28);'
    'padding:0 10px;">&rarr;</div>'
    '<div style="display:flex;flex-direction:column;align-items:center;">'
    '<div style="width:104px;height:92px;border-radius:14px;'
    'background:linear-gradient(135deg,rgba(255,149,0,0.2),rgba(123,47,190,0.16));'
    'border:1.5px solid #FF9500;box-shadow:0 0 34px rgba(255,149,0,0.28);display:flex;'
    'align-items:center;justify-content:center;font-family:\'Syne\',sans-serif;font-weight:800;'
    'font-size:12px;letter-spacing:0.5px;color:#fff;text-align:center;line-height:1.25;">'
    "ADVER<br>TORIAL</div></div>"
    '<div style="font-family:\'DM Mono\',monospace;font-size:20px;color:rgba(255,255,255,0.28);'
    'padding:0 10px;">&rarr;</div>'
    '<div style="display:flex;flex-direction:column;align-items:center;opacity:0.4;">'
    '<div style="width:58px;height:58px;border-radius:12px;background:rgba(255,255,255,0.05);'
    'border:1px solid rgba(255,255,255,0.12);display:flex;align-items:center;'
    'justify-content:center;font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;'
    'letter-spacing:1px;color:rgba(255,255,255,0.55);">PDP</div></div>'
    "</div></div>"
)
s1_avatar_row = (
    '<div style="display:flex;align-items:center;gap:10px;margin-top:16px;">'
    '<div style="width:36px;height:36px;border-radius:50%;overflow:hidden;'
    'border:2px solid rgba(255,149,0,0.4);flex-shrink:0;">'
    '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" '
    'style="width:100%;height:100%;object-fit:cover;" onerror="this.parentNode.style.display=\'none\'"></div>'
    '<div><div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:13px;color:#fff;">'
    "Ridwan Adekunle</div><div style=\"font-family:'DM Mono',monospace;font-size:10px;"
    'color:rgba(255,255,255,0.4);margin-top:1px;">Shopify CRO &amp; UX Designer</div></div></div>'
)
s1_pillar = (
    '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;'
    'letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.35);'
    'margin-top:14px;">Conversion Strategy</div>'
)
s1_headline = (
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:30px;'
    'line-height:1.22;letter-spacing:-0.5px;color:#fff;">You think an advertorial is a '
    "longer landing page. That's why cold traffic keeps "
    '<span style="color:#FF9500;">bouncing.</span></div></div>'
)
s1_swipe = (
    '<div style="display:flex;align-items:center;gap:8px;">'
    '<span style="font-family:\'DM Mono\',monospace;font-size:10px;letter-spacing:2px;'
    'text-transform:uppercase;color:rgba(255,255,255,0.35);">Swipe</span>'
    '<div style="width:48px;height:1px;background:linear-gradient(to right,'
    'rgba(255,255,255,0.2),#FF9500);"></div>'
    '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6 4l4 4-4 4" '
    'stroke="#FF9500" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
)
new1 = slide("#080808", s1_visual + s1_avatar_row + s1_pillar + s1_headline + s1_swipe)

# Slide 2 — The Myth
s2 = (
    '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">'
    '<div style="display:inline-block;background:#FF9500;color:#000;font-family:\'DM Mono\',monospace;'
    'font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;'
    'border-radius:4px;">The myth</div>'
    '<div style="width:44px;height:44px;border-radius:50%;background:rgba(255,149,0,0.08);'
    'border:1px solid rgba(255,149,0,0.25);display:flex;align-items:center;justify-content:center;'
    f'flex-shrink:0;">{ICON_FILE_TEXT}</div></div>'
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:40px;line-height:1.18;'
    'letter-spacing:-1px;color:#fff;">An advertorial is a landing page with more words.</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.6;margin-top:22px;max-width:400px;">Or a blog post you hope ranks one day. '
    "Both miss the job.</div></div>"
)
new2 = slide("#0a0a0a", s2)

# Slide 3 — The Number (stat)
s3 = (
    '<div style="margin-bottom:20px;"><div style="display:inline-block;border:1px solid '
    'rgba(255,255,255,0.2);color:rgba(255,255,255,0.5);font-family:\'DM Mono\',monospace;'
    'font-size:9px;font-weight:500;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;'
    'border-radius:4px;">The number</div></div>'
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:96px;line-height:1;'
    'letter-spacing:-2px;color:#FF9500;">60%</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:12px;font-weight:500;'
    'letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-top:10px;">'
    "conversion once the gap is closed</div>"
    '<div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,'
    '#FF9500,#E040A0,#7B2FBE);margin:18px 0;"></div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.65;max-width:420px;">Cold traffic alone converts around 1.5%. The advertorial '
    "is the one page most Shopify brands skip.</div>"
    '<div style="font-family:\'DM Mono\',monospace;font-size:12px;color:rgba(255,255,255,0.28);'
    'margin-top:16px;">Pattern across the cold-traffic funnels I\'ve built.</div></div>'
)
new3 = slide("#0d0b08", s3)

# Slide 4 — The Reality
s4 = (
    '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">'
    '<div style="display:inline-block;background:#FF9500;color:#000;font-family:\'DM Mono\',monospace;'
    'font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;'
    'border-radius:4px;">The reality</div>'
    '<div style="width:44px;height:44px;border-radius:50%;background:rgba(255,149,0,0.08);'
    'border:1px solid rgba(255,149,0,0.25);display:flex;align-items:center;justify-content:center;'
    f'flex-shrink:0;">{ICON_SHIELD}</div></div>'
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:36px;line-height:1.18;'
    'letter-spacing:-1px;color:#fff;">Its only job is making a stranger '
    '<span style="color:#FF9500;">believe you.</span></div>'
    '<div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,'
    '#FF9500,#E040A0,#7B2FBE);margin:18px 0;"></div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.7;max-width:400px;">Trust has to move first. The product comes after.</div></div>'
)
new4 = slide("#080808", s4)

# Slide 5 — Where the weight sits (3 beats)
s5 = (
    '<div style="margin-bottom:16px;"><div style="display:inline-block;border:1px solid '
    'rgba(255,255,255,0.2);color:rgba(255,255,255,0.5);font-family:\'DM Mono\',monospace;'
    'font-size:9px;font-weight:500;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;'
    'border-radius:4px;">The 3 beats that carry it</div></div>'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:32px;line-height:1.2;'
    'letter-spacing:-1px;color:#fff;">Only 3 beats carry the weight.</div>'
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;margin:6px 0;">'
    '<div style="display:flex;align-items:center;gap:18px;padding:12px 0;">'
    '<div style="width:44px;height:44px;border-radius:50%;flex-shrink:0;'
    'background:linear-gradient(135deg,#FF9500,#7B2FBE);display:flex;align-items:center;'
    'justify-content:center;font-family:\'Syne\',sans-serif;font-weight:800;font-size:18px;'
    'color:#fff;">1</div><div style="font-family:\'Syne\',sans-serif;font-weight:700;'
    'font-size:21px;color:#fff;">The hook that stops the scroll</div></div>'
    '<div style="display:flex;align-items:center;gap:18px;padding:12px 0;">'
    '<div style="width:44px;height:44px;border-radius:50%;flex-shrink:0;'
    'background:linear-gradient(135deg,#FF9500,#7B2FBE);display:flex;align-items:center;'
    'justify-content:center;font-family:\'Syne\',sans-serif;font-weight:800;font-size:18px;'
    'color:#fff;">2</div><div style="font-family:\'Syne\',sans-serif;font-weight:700;'
    'font-size:21px;color:#fff;">The proof that kills the doubt</div></div>'
    '<div style="display:flex;align-items:center;gap:18px;padding:12px 0;">'
    '<div style="width:44px;height:44px;border-radius:50%;flex-shrink:0;'
    'background:linear-gradient(135deg,#FF9500,#7B2FBE);display:flex;align-items:center;'
    'justify-content:center;font-family:\'Syne\',sans-serif;font-weight:800;font-size:18px;'
    'color:#fff;">3</div><div style="font-family:\'Syne\',sans-serif;font-weight:700;'
    'font-size:21px;color:#fff;">The reveal that earns the click</div></div></div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:13px;color:rgba(255,255,255,0.35);'
    'margin-top:4px;">The other beats just clear the path between them.</div>'
)
new5 = slide("#0a0a0a", s5)

# Slide 6 — The only question
s6 = (
    '<div style="display:flex;align-items:center;justify-content:space-between;">'
    '<div style="font-family:\'DM Mono\',monospace;font-size:10px;font-weight:500;'
    'letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);">'
    "The only question that matters</div>"
    '<div style="width:44px;height:44px;border-radius:50%;background:rgba(255,149,0,0.08);'
    'border:1px solid rgba(255,149,0,0.25);display:flex;align-items:center;justify-content:center;'
    f'flex-shrink:0;">{ICON_HELP}</div></div>'
    '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:34px;line-height:1.22;'
    'letter-spacing:-1px;color:#fff;">Does this page make a stranger believe you before it asks '
    "them to buy?</div>"
    '<div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,'
    '#FF9500,#E040A0,#7B2FBE);margin:18px 0;"></div>'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:24px;color:#FF9500;">'
    "If not, it's just copy.</div></div>"
)
new6 = slide("#0a0a0a", s6)

# Slide 7 — CTA
s7 = (
    '<div style="flex:1;display:flex;flex-direction:column;align-items:center;'
    'justify-content:center;text-align:center;">'
    '<div style="width:150px;height:150px;border-radius:50%;overflow:hidden;'
    'border:2px solid rgba(255,149,0,0.4);margin-bottom:22px;flex-shrink:0;">'
    '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2" '
    'style="width:100%;height:100%;object-fit:cover;object-position:center top;" '
    'onerror="this.style.display=\'none\'"></div>'
    '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:30px;line-height:1.16;'
    'letter-spacing:-1px;color:#fff;">Want your cold traffic to actually warm up before it hits '
    "your PDP?</div>"
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);'
    'line-height:1.6;margin:16px 0 26px;max-width:380px;">I\'ll audit the gap between your ad and '
    "your product page.</div>"
    '<div style="display:inline-flex;align-items:center;gap:8px;padding:13px 30px;'
    'background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;'
    'font-family:\'DM Mono\',monospace;font-weight:700;font-size:14px;border-radius:32px;">'
    'DM me "AUDIT" &rarr;</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.3);'
    'margin-top:22px;">Follow @koolestpro for more</div>'
    '<div style="font-family:\'DM Mono\',monospace;font-size:12px;color:rgba(255,255,255,0.2);'
    'margin-top:6px;">Save this before your next funnel build.</div></div>'
)
new7 = slide("#080808", s7)

new_blocks = [new1, new2, new3, new4, new5, new6, new7]
for i, b in enumerate(new_blocks):
    assert b.count("<div") == b.count("</div"), f"new slide {i+1} unbalanced ({b.count('<div')} vs {b.count('</div')})"

# Splice: rebuild the text with new slide blocks in place of old ones
pieces = []
cursor = 0
for i in range(7):
    pieces.append(text[cursor:bounds[i]])  # keep everything before this slide's start
    pieces.append(new_blocks[i])
    cursor = bounds[i + 1]
pieces.append(text[cursor:])
text = "".join(pieces)

# ── 4. LK caption preview ────────────────────────────────────────────────
old_caption = (
    '    <strong>Your store\'s animations aren\'t making it look premium. They\'re making it convert worse.</strong><br>\n'
    "    Motion isn't free. Every effect adds delay, and delay costs sales. Spend it on decisions, cut it everywhere else.<br>\n"
    '    <span class="lk-see-more">...see more</span>'
)
new_caption = (
    "    <strong>You think an advertorial is a longer landing page. That's why cold traffic keeps "
    "bouncing.</strong><br>\n"
    "    Its only job is making a stranger believe you before anything else. Hook, proof, reveal "
    "carry the weight.<br>\n"
    '    <span class="lk-see-more">...see more</span>'
)
assert old_caption in text, "caption anchor not found"
text = text.replace(old_caption, new_caption)

# ── 5. JS constants + filenames ──────────────────────────────────────────
text = text.replace(
    "const POST_SLUG   = 'animation-budget-motion-conversion-v2';",
    f"const POST_SLUG   = '{NEW_SLUG}';",
)
text = text.replace(
    "const POST_FOLDER = 'outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html';",
    f"const POST_FOLDER = 'outputs/tips/{NEW_SLUG}_2026-07-31.html';",
)
text = text.replace("koolestpro_animation-budget-v2_slide", f"koolestpro_{NEW_SLUG}_slide")
text = text.replace("koolestpro_animation-budget-v2.pdf", f"koolestpro_{NEW_SLUG}.pdf")
text = text.replace("'koolestpro_animation-budget_'", f"'koolestpro_{NEW_SLUG}_'")
assert "animation-budget" not in text, "leftover animation-budget reference after replacements"
text = text.replace(
    'title: "Your store\'s animations are costing you sales",',
    'title: "An advertorial is not a landing page",',
)

# ── 6. Post-copy tab bodies (positional split on <pre> inside each tab id) ──
TAB_IDS = ["tab-linkedin", "tab-hook", "tab-twitter-thread", "tab-twitter-angles", "tab-ig"]

NEW_TAB_TEXT = {
    "tab-linkedin": (
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
    ),
    "tab-hook": (
        "You think an advertorial is a longer landing page. That's why cold traffic keeps bouncing.\n\n"
        "Its only job is making a stranger believe you before anything else.\n\n"
        "Hook, proof, reveal. Those 3 beats carry the whole page.\n\n"
        "Which page in your funnel is doing homework instead of doing its job?"
    ),
    "tab-twitter-thread": (
        "1/ You think an advertorial is a longer landing page. That's why cold traffic keeps bouncing. "
        "A short thread on what it actually is:\n\n"
        "2/ The myth: a landing page with more words, or a blog post you hope ranks one day. Both miss "
        "the job entirely.\n\n"
        "3/ Cold traffic converts around 1.5%. Warmed-up traffic can hit 60%+. That gap is one page most "
        "Shopify brands skip.\n\n"
        "4/ The reality: its only job is making a stranger believe you before anything else. Trust moves "
        "first. The product comes after.\n\n"
        "5/ It runs on 3 beats: the hook that stops the scroll, the proof that kills the doubt, the "
        "reveal that earns the click.\n\n"
        "6/ Everything else on the page just clears the path between those three.\n\n"
        "7/ One question before you ship the next one: does it make a stranger believe you before it "
        "asks them to buy? Follow @koolestpro for more."
    ),
    "tab-twitter-angles": (
        "THE RULE\n"
        "An advertorial has one job: make a stranger believe you. Not inform them, not rank on Google, "
        "not fill space before the PDP.\n\n"
        "THE CONTRAST\n"
        "A landing page repeats your ad. An advertorial builds trust before the ad's claim gets tested.\n\n"
        "THE HOT TAKE\n"
        "Most \"advertorials\" are blog posts in a costume. That's why cold traffic reads them and still "
        "doesn't buy."
    ),
    "tab-ig": (
        "You think an advertorial is a longer landing page. That's why cold traffic keeps bouncing.\n\n"
        "It isn't a landing page. It isn't a blog post either.\n\n"
        "Its only job is making a stranger believe you before anything else.\n\n"
        "The hook stops the scroll. The proof kills the doubt. The reveal earns the click. That's the "
        "whole page.\n\n"
        "Save this. Follow @koolestpro for more Shopify CRO tips.\n\n"
        "#ShopifyDesign #CRO #eCommerce #ShopifyDeveloper #ConversionOptimization #WebDesign #Shopify "
        "#UXDesign #DigitalMarketing #ShopifyLiquid"
    ),
}

for tab_id in TAB_IDS:
    open_anchor = f'<div id="{tab_id}" class="tab-panel'
    start = text.index(open_anchor)
    pre_start = text.index("<pre>", start) + len("<pre>")
    pre_end = text.index("</pre>", pre_start)
    old_pre = text[pre_start:pre_end]
    assert len(old_pre) > 10, f"empty <pre> body for {tab_id}"
    text = text[:pre_start] + NEW_TAB_TEXT[tab_id] + text[pre_end:]

# No em dashes, no markdown asterisks standing in for line breaks, in any tab body
for tab_id, body in NEW_TAB_TEXT.items():
    assert "—" not in body, f"em dash in {tab_id}"
    assert "*" not in body, f"asterisk in {tab_id}"

with open(DST, "w", encoding="utf-8") as f:
    f.write(text)

final_open = text.count("<div")
final_close = text.count("</div>")
print(f"[check] output file: <div>={final_open} </div>={final_close} balanced={final_open == final_close}")
print(f"[ok] wrote {DST}")
