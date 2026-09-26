#!/usr/bin/env python3
"""One-off builder: creates the Animation Budget Tip carousel by region-swapping
content into the gold-standard reference (reusing its exact carousel/PNG/PDF/
pipeline/tabs JS). Keeps all export machinery byte-identical to the proven file."""
import re, sys, pathlib

ROOT = pathlib.Path("/sessions/eager-nice-archimedes/mnt/koolestpro-cowork-v2")
REF = ROOT / "outputs/tips/funnel-awareness-framework_2026-05-10.html"
OUT = ROOT / "outputs/tips/animation-budget-motion-conversion_2026-07-17.html"

html = REF.read_text(encoding="utf-8")

def sub_once(pattern, repl, s, flags=0, label=""):
    new, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
    if n != 1:
        sys.exit(f"ANCHOR FAIL [{label}] matched {n} times")
    return new

# ---- component helpers ----
GLOW_TR = '<div style="position:absolute;top:-80px;right:-60px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.16),rgba(224,64,160,0.07),transparent 70%);filter:blur(70px);pointer-events:none;"></div>'
GLOW_BL = '<div style="position:absolute;bottom:-60px;left:-40px;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.15),transparent 70%);filter:blur(60px);pointer-events:none;"></div>'
DOTGRID = '<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.02) 1px,transparent 1px);background-size:24px 24px;pointer-events:none;"></div>'
ATTR = '<div style="position:absolute;bottom:18px;right:24px;font-family:\'DM Mono\',monospace;font-size:10px;color:rgba(255,255,255,0.18);z-index:10;">Ridwan - Shopify CRO &amp; UX Designer</div>'
RULE = '<div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,#FF9500,#E040A0,#7B2FBE);margin:18px 0;"></div>'
PILL = lambda t: f'<div style="display:inline-block;background:#FF9500;color:#000;font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;border-radius:4px;">{t}</div>'
OUTBOX = lambda t: f'<div style="display:inline-block;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.5);font-family:\'DM Mono\',monospace;font-size:9px;font-weight:500;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border-radius:4px;">{t}</div>'

def wrap(bg, inner):
    return (f'<div class="slide" style="background:{bg};">\n{GLOW_TR}\n{GLOW_BL}\n{DOTGRID}\n'
            f'<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;flex-direction:column;">\n{inner}\n</div>\n{ATTR}\n</div>')

def xpill(t):
    return (f'<span style="position:relative;font-family:\'DM Mono\',monospace;font-size:11px;padding:5px 26px 5px 12px;'
            f'border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:rgba(255,255,255,0.32);">{t}'
            f'<span style="position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:9px;color:#FF9500;">✕</span></span>')

def dotbullet(t):
    return (f'<div style="display:flex;align-items:flex-start;gap:14px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.05);">'
            f'<div style="width:10px;height:10px;border-radius:50%;flex-shrink:0;margin-top:4px;background:linear-gradient(135deg,#FF9500,#7B2FBE);"></div>'
            f'<div style="font-family:\'DM Mono\',monospace;font-size:13px;line-height:1.55;color:rgba(255,255,255,0.62);">{t}</div></div>')

def numstep(n, t):
    return (f'<div style="display:flex;align-items:flex-start;gap:14px;padding:11px 0;">'
            f'<div style="width:30px;height:30px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,#FF9500,#7B2FBE);display:flex;align-items:center;justify-content:center;font-family:\'Syne\',sans-serif;font-weight:800;font-size:13px;color:#fff;">{n}</div>'
            f'<div style="font-family:\'DM Mono\',monospace;font-size:12.5px;line-height:1.55;color:rgba(255,255,255,0.6);padding-top:3px;">{t}</div></div>')

def recaprow(t):
    return (f'<div style="display:flex;align-items:stretch;gap:14px;padding:9px 0;">'
            f'<div style="width:3px;border-radius:2px;flex-shrink:0;background:linear-gradient(to bottom,#FF9500,#7B2FBE);"></div>'
            f'<div style="font-family:\'DM Mono\',monospace;font-size:12.5px;line-height:1.5;color:rgba(255,255,255,0.6);">{t}</div></div>')

A = "'"  # apostrophe, kept out of f-string braces
H = lambda size,txt: '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:'+str(size)+'px;line-height:1.14;letter-spacing:-1px;color:#fff;">'+txt+'</div>'
EY = 'margin-bottom:20px;'

# ---- 7 slides ----
h1 = H(42, "Your store"+A+"s animations aren"+A+"t making it look premium. They"+A+"re making it convert <span style=\"color:#FF9500;\">worse.</span>")
s1_inner = (
 f'<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.35);">Conversion Strategy</div>'
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
 f'{h1}'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:13px;color:rgba(255,255,255,0.5);line-height:1.6;margin-top:20px;">The motion myth every Shopify brand falls for.</div></div>'
 f'<div style="display:flex;align-items:center;gap:8px;"><span style="font-family:\'DM Mono\',monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);">Swipe</span>'
 f'<div style="width:48px;height:1px;background:linear-gradient(to right,rgba(255,255,255,0.2),#FF9500);"></div>'
 f'<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6 4l4 4-4 4" stroke="#FF9500" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
slide1 = wrap('#080808', s1_inner)

s2_inner = (
 f'<div style="{EY}">{PILL("The myth")}</div>'
 f'{H(32,"More motion means a more premium store. And premium stores convert better.")}'
 f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 8px;">{xpill("animate every section")}{xpill("fade in on scroll everywhere")}{xpill("parallax = premium")}{xpill("movement holds attention")}</div>'
 f'<div style="margin-top:6px;">{dotbullet("You added scroll animations to look high-end. Your add-to-cart rate quietly dropped.")}{dotbullet("Every effect you love in the Figma preview is a delay on a real phone.")}</div>')
slide2 = wrap('#0a0a0a', s2_inner)

s3_inner = (
 f'<div style="{EY}">{OUTBOX("The number")}</div>'
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
 f'<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:78px;line-height:1;letter-spacing:-2px;color:#FF9500;">100ms</div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:12px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-top:10px;">of extra delay &asymp; 1% fewer sales</div>'
 f'{RULE}'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:13px;color:rgba(255,255,255,0.5);line-height:1.65;max-width:420px;">That\'s what Amazon found in its own load-time testing. Motion is the easiest way to add that delay without noticing.</div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:10px;color:rgba(255,255,255,0.28);margin-top:16px;">Source: Amazon load-time study</div></div>')
slide3 = wrap('#0d0b08', s3_inner)

h4 = H(38, 'Motion is a <span style="color:#FF9500;">budget</span>, not a decoration.')
bigidea = 'Design isn'+A+'t decoration. It'+A+'s direction.'
s4_inner = (
 f'<div style="{EY}">{PILL("The reality")}</div>'
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
 f'{h4}'
 f'{RULE}'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:13.5px;color:rgba(255,255,255,0.5);line-height:1.7;max-width:430px;">You get a small amount of attention and speed to spend on a page. Every animation spends some of it, so it has to buy something back.</div>'
 f'<div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:17px;color:#fff;margin-top:26px;">{bigidea}</div></div>')
slide4 = wrap('#080808', s4_inner)

B = lambda t: '<b style="color:#fff;font-weight:700;">'+t+'</b>'
h5 = H(30, "Spend it on decisions. Cut it everywhere else.")
step1 = numstep(1, B("Selection feedback.")+" The variant, size, or bundle a shopper picks should react instantly, so they trust the choice registered.")
step2 = numstep(2, B("Add-to-cart confirmation.")+" A fast, clear response the moment money is on the line lowers doubt.")
step3 = numstep(3, B("Proof reveal.")+" Let reviews and guarantees arrive as the shopper scrolls to them, so trust lands while they decide.")
s5_inner = (
 f'<div style="{EY}">{OUTBOX("Where motion earns its place")}</div>'
 f'{h5}'
 f'<div style="margin:20px 0 6px;">{step1}{step2}{step3}</div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:11px;color:rgba(255,255,255,0.3);line-height:1.6;margin-top:auto;border-top:1px solid rgba(255,255,255,0.06);padding-top:14px;">Everything else is spending budget for nothing: hero parallax, section-by-section fades, floating shapes.</div>')
slide5 = wrap('#0a0a0a', s5_inner)

h6 = H(32, "Run every animation through this.")
r1 = recaprow("Does it fire on a decision the shopper is making? If no, cut it.")
r2 = recaprow("Does it delay when they can tap or read? If yes, cut it.")
r3 = recaprow("Does it move something above the fold? Then be very careful.")
r4 = recaprow("Does it still feel smooth on a mid-range Android? If not, it isn"+A+"t shipping.")
s6_inner = (
 f'<div style="font-family:\'DM Mono\',monospace;font-size:10px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);{EY}">The 4-question audit</div>'
 f'{h6}'
 f'<div style="margin-top:22px;">{r1}{r2}{r3}{r4}</div>')
slide6 = wrap('#0a0a0a', s6_inner)

avatar_img = '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2" style="width:100%;height:100%;object-fit:cover;object-position:center top;" onerror="this.style.display=' + A + 'none' + A + '"></div>'
h7 = H(32, "Want to know which animations are costing you sales?")
sub7 = 'I'+A+'ll audit your store'+A+'s motion and CRO.'
cta_btn = '<div style="display:inline-flex;align-items:center;gap:8px;padding:13px 30px;background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;font-family:' + A + 'DM Mono' + A + ',monospace;font-weight:700;font-size:12px;border-radius:32px;">DM me "AUDIT" &rarr;</div>'
s7_inner = (
 f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">'
 f'<div style="width:150px;height:150px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,149,0,0.4);margin-bottom:22px;flex-shrink:0;">'
 f'{avatar_img}'
 f'{h7}'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:13px;color:rgba(255,255,255,0.5);line-height:1.6;margin:16px 0 26px;max-width:380px;">{sub7}</div>'
 f'{cta_btn}'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:11px;color:rgba(255,255,255,0.3);margin-top:22px;">Follow @koolestpro for more</div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:10px;color:rgba(255,255,255,0.2);margin-top:6px;">Save this for your next build.</div></div>')
slide7 = wrap('#080808', s7_inner)

slides_html = "\n\n".join([slide1,slide2,slide3,slide4,slide5,slide6,slide7])

# ---- replace slides region (between track open and /track close) ----
start = html.index('<div id="track">') + len('<div id="track">')
end = html.index('    </div><!-- /track -->')
html = html[:start] + "\n\n" + slides_html + "\n\n" + html[end:]

# ---- pager ----
html = sub_once(r'<div id="pager">1 / 10</div>', '<div id="pager">1 / 7</div>', html, label="pager")
# ---- TOTAL ----
html = sub_once(r'const TOTAL = 10;', 'const TOTAL = 7;', html, label="TOTAL")

# ---- lk avatar (header) -> cloudinary ----
html = sub_once(
  r'<img src="\.\./\.\./assets/ridwan/avatar-circle\.jpg"[^>]*onerror="this\.parentNode\.innerHTML=\'<span>R</span>\'">',
  '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" onerror="this.style.display=\'none\'">',
  html, label="avatar")

# ---- lk-caption ----
cap_old = re.search(r'<div class="lk-caption" data-chrome>.*?</div>', html, re.S).group(0)
cap_new = ('<div class="lk-caption" data-chrome>\n'
 '    <strong>Your store\'s animations aren\'t making it look premium. They\'re making it convert worse.</strong><br>\n'
 '    Motion isn\'t free. Every effect adds delay, and delay costs sales. Spend it on decisions, cut it everywhere else.<br>\n'
 '    <span class="lk-see-more">...see more</span>\n  </div>')
html = html.replace(cap_old, cap_new, 1)

# ---- download-panel buttons (10 -> 7) ----
dl_old = re.search(r'<div id="dl-buttons">.*?</div>', html, re.S).group(0)
dl_new = ('<div id="dl-buttons">\n'
 + "\n".join(f'    <button class="dl-btn" onclick="dlSlide({i})">Slide {i+1}</button>' for i in range(7))
 + '\n    <button class="dl-btn dl-all" onclick="dlAll()">Download All PNGs</button>'
 + '\n    <button class="dl-btn dl-pdf" onclick="dlPDF()">Export PDF</button>\n  </div>')
html = html.replace(dl_old, dl_new, 1)
html = html.replace('PNG exports at 2× resolution (1080×1360px). PDF contains all slides in sequence.',
                    'PNG exports at 2× resolution (1080×1360px). PDF contains all 7 slides in sequence.', 1)

# ---- consts / filenames / pdf / title ----
html = html.replace("const POST_SLUG   = 'funnel-awareness-framework';", "const POST_SLUG   = 'animation-budget-motion-conversion';", 1)
html = html.replace("const POST_FOLDER = 'outputs/tips/funnel-awareness-framework_2026-05-10.html';", "const POST_FOLDER = 'outputs/tips/animation-budget-motion-conversion_2026-07-17.html';", 1)
html = html.replace('koolestpro_funnel-framework_slide', 'koolestpro_animation-budget_slide', 1)
html = html.replace("pdf.save('koolestpro_funnel-awareness-framework.pdf');", "pdf.save('koolestpro_animation-budget.pdf');", 1)
html = html.replace("title: POST_BRAND + ' — ' + 'Match Your Funnel to Your Audience',",
                    'title: "Your store\'s animations are costing you sales",', 1)
html = html.replace('<title>Funnel Awareness Framework — @koolestpro</title>',
                    '<title>Animation Budget: When Motion Helps Conversion — @koolestpro</title>', 1)

# ---- graphic cards (Section 2) ----
gcards = f'''<div class="posts-shell">

<div class="gcard-wrap">
  <div class="gcard" id="gcard-a" style="background:#080808;">
    <div style="position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);"></div>
    <div style="position:absolute;top:34px;left:34px;width:26px;height:26px;border-top:2px solid rgba(255,149,0,0.4);border-left:2px solid rgba(255,149,0,0.4);"></div>
    <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;justify-content:center;padding:56px 48px;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:110px;line-height:0.8;color:#FF9500;opacity:0.18;margin-bottom:-6px;">&ldquo;</div>
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:40px;line-height:1.18;letter-spacing:-1px;color:#fff;">Motion is a budget, not a decoration. Spend it where decisions happen.</div>
      <div style="height:3px;width:52px;border-radius:2px;background:linear-gradient(to right,#FF9500,#E040A0,#7B2FBE);margin-top:22px;"></div>
    </div>
    <div style="position:absolute;bottom:22px;left:48px;font-family:'DM Mono',monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);">Conversion Strategy</div>
    <div style="position:absolute;bottom:22px;right:48px;font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.3);">@koolestpro</div>
  </div>
  <div class="gcard-btns"><button class="dl-btn" onclick="dlCard('gcard-a','graphic-a')">Download PNG</button></div>
</div>

<div class="gcard-wrap">
  <div class="gcard" id="gcard-b" style="background:#080808;">
    <div style="position:absolute;top:38%;left:50%;transform:translate(-50%,-50%);width:360px;height:360px;border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.22),transparent 70%);filter:blur(60px);pointer-events:none;"></div>
    <div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.02) 1px,transparent 1px);background-size:24px 24px;pointer-events:none;"></div>
    <div style="position:absolute;top:34px;left:34px;">{PILL("The number")}</div>
    <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:48px;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:92px;line-height:1;letter-spacing:-3px;color:#FF9500;">100ms</div>
      <div style="font-family:'DM Mono',monospace;font-size:13px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.55);margin-top:10px;">&asymp; 1% fewer sales</div>
      <div style="font-family:'DM Mono',monospace;font-size:12px;color:rgba(255,255,255,0.4);margin-top:18px;max-width:340px;line-height:1.6;">Motion is the easiest delay to add by accident.</div>
    </div>
    <div style="position:absolute;bottom:22px;right:48px;font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.3);">@koolestpro</div>
  </div>
  <div class="gcard-btns"><button class="dl-btn" onclick="dlCard('gcard-b','graphic-b')">Download PNG</button></div>
</div>

<div class="gcard-wrap">
  <div class="gcard" id="gcard-c" style="background:#060606;">
    <div style="position:absolute;top:-60px;right:-50px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.2),transparent 70%);filter:blur(70px);pointer-events:none;"></div>
    <div style="position:absolute;bottom:-70px;left:-50px;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.22),transparent 70%);filter:blur(70px);pointer-events:none;"></div>
    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:420px;height:420px;border-radius:50%;border:1px solid rgba(255,255,255,0.04);"></div>
    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:320px;height:320px;border-radius:50%;border:1px solid rgba(255,255,255,0.05);"></div>
    <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:56px;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:90px;line-height:0.8;color:#FF9500;opacity:0.16;">&ldquo;</div>
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:34px;line-height:1.3;color:#fff;max-width:400px;">Motion is a budget, not a decoration. Spend it where decisions happen.</div>
    </div>
    <div style="position:absolute;bottom:24px;left:50%;transform:translateX(-50%);font-family:'DM Mono',monospace;font-size:10px;letter-spacing:1px;color:rgba(255,255,255,0.3);">@koolestpro</div>
  </div>
  <div class="gcard-btns"><button class="dl-btn" onclick="dlCard('gcard-c','graphic-c')">Download PNG</button></div>
</div>

</div>'''
posts_old = re.search(r'<div class="posts-shell">.*?</div>\s*(?=<!--)', html, re.S).group(0)
html = html.replace(posts_old, gcards + "\n\n", 1)

# ---- dlCard helper (insert before Tab logic) ----
dlcard_js = '''// ── Graphic card download ──
async function dlCard(id, name) {
  const el = document.getElementById(id);
  if (!el) return;
  const toHide = document.querySelectorAll('[data-chrome], #download-panel, .section-label, .section-divider, .gcard-btns');
  toHide.forEach(x => x.style.visibility = 'hidden');
  try {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    const canvas = await html2canvas(el, { scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#080808', logging: false });
    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    a.download = 'koolestpro_animation-budget_' + name + '.png';
    a.click();
  } finally {
    toHide.forEach(x => x.style.visibility = '');
  }
}

// ── Tab logic ──'''
html = sub_once(r'// ── Tab logic ──', dlcard_js, html, label="dlcard-insert")

# ---- tabs (buttons + 5 panels) ----
tabs_new = '''<div class="tab-buttons">
    <button class="tab-btn active" onclick="openTab(this,'tab-linkedin')">LinkedIn</button>
    <button class="tab-btn" onclick="openTab(this,'tab-hook')">Hook</button>
    <button class="tab-btn" onclick="openTab(this,'tab-twitter-thread')">X Thread</button>
    <button class="tab-btn" onclick="openTab(this,'tab-twitter-angles')">X Singles</button>
    <button class="tab-btn" onclick="openTab(this,'tab-ig')">Instagram</button>
  </div>

  <div id="tab-linkedin" class="tab-panel active">
    <pre>Your store's animations aren't making it look premium. They're making it convert worse.

I know that's not what you want to hear after a weekend of adding scroll effects.

Here's the trap most Shopify brands fall into: more motion feels more high-end, and high-end feels like it should sell more. So they animate everything.

But motion isn't free. Amazon found that every 100ms of extra delay cost them about 1% in sales. Animations are the easiest way to add that delay without realising it.

The fix is to treat motion as a budget, not decoration. You get a small amount of attention and speed to spend on a page. Every animation spends some of it, so it has to buy something back.

Where it actually earns its place:

Selection feedback, so a shopper trusts their variant or bundle registered.
Add-to-cart confirmation, right when money is on the line.
Proof reveal, so reviews and guarantees land as they scroll to decide.

Everything else is spending budget for nothing: hero parallax, section-by-section fades, floating shapes.

Run every animation through one question: does it fire on a decision the shopper is making? If not, cut it.

Save this before your next build. And if you want to know which animations are quietly costing you sales, my DMs are open.</pre>
    <button class="copy-btn" onclick="copyText('tab-linkedin')">Copy</button>
  </div>

  <div id="tab-hook" class="tab-panel">
    <pre>Your store's animations aren't making it look premium. They're making it convert worse.

Motion isn't free. Every effect adds delay, and delay costs sales.

Spend it on decisions. Cut it everywhere else.

What's the first animation you'd defend to the death, and are you sure it's earning its place?</pre>
    <button class="copy-btn" onclick="copyText('tab-hook')">Copy</button>
  </div>

  <div id="tab-twitter-thread" class="tab-panel">
    <pre>1/ Your store's animations aren't making it look premium. They're making it convert worse. A thread on the motion myth quietly killing your Shopify sales:

2/ The myth: more motion = more premium = more sales. So brands animate every section. Fade-ins everywhere. Parallax heroes. It looks high-end in the Figma preview.

3/ The problem: motion isn't free. Amazon found every 100ms of extra delay cost about 1% in sales. Animations are the easiest way to add that delay without noticing.

4/ The reframe: motion is a budget, not decoration. You get a little attention and speed to spend per page. Every animation spends some of it. It has to buy something back.

5/ Where it earns its place: selection feedback (variant registered), add-to-cart confirmation (money's on the line), proof reveal (reviews land as they decide).

6/ Everything else is spending budget for nothing: hero parallax, section-by-section fades, floating shapes. Cut them.

7/ One question for every animation: does it fire on a decision the shopper is making? If not, kill it. Follow @koolestpro for more Shopify CRO.</pre>
    <button class="copy-btn" onclick="copyText('tab-twitter-thread')">Copy</button>
  </div>

  <div id="tab-twitter-angles" class="tab-panel">
    <pre>THE RULE
Motion is a budget, not decoration. You get a little attention and speed per page. Every animation spends some of it, so it had better buy something back.

THE CONTRAST
A scroll reveal on your reviews: earns its place. A parallax hero: spends the same budget and hands you nothing back.

THE HOT TAKE
Most of the animations you added to look premium are quietly lowering your add-to-cart rate. Fancy and converting are not the same thing.</pre>
    <button class="copy-btn" onclick="copyText('tab-twitter-angles')">Copy</button>
  </div>

  <div id="tab-ig" class="tab-panel">
    <pre>Your store's animations aren't making it look premium. They're making it convert worse.

Motion isn't free. Every effect adds delay, and Amazon found 100ms of delay costs about 1% in sales.

Treat motion as a budget. Spend it on decisions: selection feedback, add-to-cart confirmation, proof reveals.

Cut the parallax and the section-by-section fades. They're spending budget for nothing.

Save this. Follow @koolestpro for more Shopify CRO tips.

#ShopifyDesign #CRO #eCommerce #ShopifyDeveloper #ConversionOptimization #WebDesign #Shopify #UXDesign #DigitalMarketing #ShopifyLiquid</pre>
    <button class="copy-btn" onclick="copyText('tab-ig')">Copy</button>
  </div>'''
tabs_old = re.search(r'<div class="tab-buttons">.*?<button class="copy-btn" onclick="copyText\(\'tab-twitter-thread\'\)">Copy</button>\s*</div>', html, re.S).group(0)
html = html.replace(tabs_old, tabs_new, 1)

OUT.write_text(html, encoding="utf-8")
print("WROTE", OUT, len(html), "chars")
