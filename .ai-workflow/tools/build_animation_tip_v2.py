#!/usr/bin/env python3
"""V2 format prototype: region-swaps LEANER slide content into the proven
animation-budget carousel (2026-07-17), reusing its exact carousel/PNG/PDF/
pipeline/tabs JS byte-for-byte. Only slides 2, 4, 5, 6 change content
(headline-only + micro anchor, one idea per slide). Slides 1, 3, 7 already
matched the target format and are kept as-is for a clean before/after."""
import re, sys, pathlib

ROOT = pathlib.Path("/sessions/stoic-youthful-hamilton/mnt/koolestpro-cowork-v2")
REF = ROOT / "outputs/tips/animation-budget-motion-conversion_2026-07-17.html"
OUT = ROOT / "outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html"

html = REF.read_text(encoding="utf-8")

def sub_once(pattern, repl, s, flags=0, label=""):
    new, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
    if n != 1:
        sys.exit(f"ANCHOR FAIL [{label}] matched {n} times")
    return new

GLOW_TR = '<div style="position:absolute;top:-80px;right:-60px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.16),rgba(224,64,160,0.07),transparent 70%);filter:blur(70px);pointer-events:none;"></div>'
GLOW_BL = '<div style="position:absolute;bottom:-60px;left:-40px;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.15),transparent 70%);filter:blur(60px);pointer-events:none;"></div>'
DOTGRID = '<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.02) 1px,transparent 1px);background-size:24px 24px;pointer-events:none;"></div>'
ATTR = '<div style="position:absolute;bottom:18px;right:24px;font-family:\'DM Mono\',monospace;font-size:12px;color:rgba(255,255,255,0.18);z-index:10;">Ridwan - Shopify CRO &amp; UX Designer</div>'
RULE = '<div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,#FF9500,#E040A0,#7B2FBE);margin:18px 0;"></div>'
PILL = lambda t: f'<div style="display:inline-block;background:#FF9500;color:#000;font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;border-radius:4px;">{t}</div>'
OUTBOX = lambda t: f'<div style="display:inline-block;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.5);font-family:\'DM Mono\',monospace;font-size:9px;font-weight:500;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border-radius:4px;">{t}</div>'

def wrap(bg, inner):
    return (f'<div class="slide" style="background:{bg};">\n{GLOW_TR}\n{GLOW_BL}\n{DOTGRID}\n'
            f'<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;flex-direction:column;">\n{inner}\n</div>\n{ATTR}\n</div>')

A = "'"

# ── SLIDE 2 (V2) — "More motion. More premium. More sales." one idea, no pill stack, no bullets ──
s2_inner = (
 f'<div style="margin-bottom:20px;">{PILL("The myth")}</div>'
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
 f'<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:44px;line-height:1.16;letter-spacing:-1.5px;color:#fff;">More motion.<br>More premium.<br>More sales.</div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);line-height:1.6;margin-top:24px;max-width:400px;">That'+A+'s the trap every Shopify brand falls into &mdash; and it'+A+'s wrong.</div></div>'
)
slide2 = wrap('#0a0a0a', s2_inner)

# ── SLIDE 3 (V2) — trim subline only, keep the proven stat layout ──
s3_inner = (
 f'<div style="margin-bottom:20px;">{OUTBOX("The number")}</div>'
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
 f'<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:78px;line-height:1;letter-spacing:-2px;color:#FF9500;">100ms</div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:12px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-top:10px;">of extra delay &asymp; 1% fewer sales</div>'
 f'{RULE}'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);line-height:1.65;max-width:420px;">Amazon'+A+'s own load-time data. Motion is the easiest way to add that delay by accident.</div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:12px;color:rgba(255,255,255,0.28);margin-top:16px;">Source: Amazon load-time study</div></div>'
)
slide3 = wrap('#0d0b08', s3_inner)

# ── SLIDE 4 (V2) — one idea only, dropped the second stacked statement ──
s4_inner = (
 f'<div style="margin-bottom:20px;">{PILL("The reality")}</div>'
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
 f'<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:38px;line-height:1.16;letter-spacing:-1px;color:#fff;">Motion is a <span style="color:#FF9500;">budget</span>, not a decoration.</div>'
 f'{RULE}'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);line-height:1.7;max-width:400px;">Every animation spends attention and speed. It has to buy something back.</div></div>'
)
slide4 = wrap('#080808', s4_inner)

# ── SLIDE 5 (V2) — 3 short labels, no explanatory sentences ──
def label3(n, t):
    return (f'<div style="display:flex;align-items:center;gap:16px;padding:13px 0;">'
            f'<div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,#FF9500,#7B2FBE);display:flex;align-items:center;justify-content:center;font-family:\'Syne\',sans-serif;font-weight:800;font-size:14px;color:#fff;">{n}</div>'
            f'<div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:19px;color:#fff;">{t}</div></div>')
s5_inner = (
 f'<div style="margin-bottom:22px;">{OUTBOX("Where motion earns its place")}</div>'
 f'<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:30px;line-height:1.16;letter-spacing:-1px;color:#fff;">Only 3 things earn the budget.</div>'
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;margin-top:6px;">'
 f'{label3(1,"Selection feedback")}{label3(2,"Add-to-cart confirmation")}{label3(3,"Proof reveal")}</div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:13px;color:rgba(255,255,255,0.3);line-height:1.6;border-top:1px solid rgba(255,255,255,0.06);padding-top:14px;">Everything else is spending the budget for nothing.</div>'
)
slide5 = wrap('#0a0a0a', s5_inner)

# ── SLIDE 6 (V2) — collapsed 4-item checklist into ONE question ──
s6_inner = (
 f'<div style="font-family:\'DM Mono\',monospace;font-size:10px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);">The only question that matters</div>'
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
 f'<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:36px;line-height:1.22;letter-spacing:-1px;color:#fff;">Does this animation fire on a decision the shopper is making?</div>'
 f'{RULE}'
 f'<div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:24px;color:#FF9500;">If not &mdash; cut it.</div></div>'
)
slide6 = wrap('#0a0a0a', s6_inner)

# ---- split existing track into 7 slide blocks, keep 1/3/7 (idx 0,2,6), replace 2/4/5/6 (idx 1,3,4,5) ----
start = html.index('<div id="track">') + len('<div id="track">')
end = html.index('    </div><!-- /track -->')
track_body = html[start:end]

pieces = re.split(r'(?=<div class="slide")', track_body)
pieces = [p for p in pieces if p.strip().startswith('<div class="slide"')]
if len(pieces) != 7:
    sys.exit(f"Expected 7 slides, found {len(pieces)}")

new_slides = [pieces[0], slide2, slide3, slide4, slide5, slide6, pieces[6]]
slides_html = "\n\n".join(s.rstrip() for s in new_slides)
html = html[:start] + "\n\n" + slides_html + "\n\n" + html[end:]

# ---- remove the dangling empty "Section 2" header (no content ever followed it) ----
html = sub_once(
  r'<!-- ══════════════════════════════════════════\n     SECTION 2 — INDIVIDUAL GRAPHIC CARDS\n══════════════════════════════════════════ -->\n<div class="section-divider"></div>\n<div class="section-label">② Individual Graphic Cards</div>\n\n',
  '', html, label="section2-remove")

# ---- title / filenames / consts ----
html = html.replace(
  '<title>Animation Budget: When Motion Helps Conversion — @koolestpro</title>',
  '<title>Animation Budget V2 (Prototype) — @koolestpro</title>', 1)
html = html.replace("const POST_SLUG   = 'animation-budget-motion-conversion';",
                    "const POST_SLUG   = 'animation-budget-motion-conversion-v2';", 1)
html = html.replace("const POST_FOLDER = 'outputs/tips/animation-budget-motion-conversion_2026-07-17.html';",
                    "const POST_FOLDER = 'outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html';", 1)
html = html.replace("koolestpro_animation-budget_slide", "koolestpro_animation-budget-v2_slide")
html = html.replace("pdf.save('koolestpro_animation-budget.pdf');",
                    "pdf.save('koolestpro_animation-budget-v2.pdf');", 1)

# ---- prototype banner (page chrome only, outside any captured .slide) ----
banner = ('<div style="max-width:588px;margin:0 auto 28px;padding:14px 18px;background:rgba(255,149,0,0.08);'
          'border:1px solid rgba(255,149,0,0.3);border-radius:10px;font-family:\'DM Mono\',monospace;'
          'font-size:11px;color:#FF9500;line-height:1.7;">&#9888; V2 FORMAT PROTOTYPE &mdash; review only, not yet sent to the '
          'content pipeline. Slides 1, 3 &amp; 7 unchanged; slides 2, 4, 5, 6 rebuilt to one idea per slide. '
          'Compare against outputs/tips/animation-budget-motion-conversion_2026-07-17.html.</div>\n\n')
html = sub_once(r'<body>\n\n', '<body>\n\n' + banner, html, label="banner")

OUT.write_text(html, encoding="utf-8")
print("WROTE", OUT, len(html), "chars")
