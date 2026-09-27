#!/usr/bin/env python3
"""Tips V4 prototype: the typography-hierarchy post rebuilt to the V4 spec.

Native 1080x1350 CSS px per slide (no downscaled 486px canvas), so every size
below is the real on-phone size. Floors: headline >= 96px, body >= 40px
(proportional sans, not mono), labels >= 28px, footer >= 26px.
"""
import os, sys

ICON = lambda n: open(os.path.join(os.path.dirname(__file__), n + ".svg")).read().replace('width="1em" height="1em"', 'width="64" height="64"')

AV = "https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2"
O, P, M = "#FF9500", "#7B2FBE", "#E040A0"

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#1a1a1a;display:flex;flex-direction:column;align-items:center;gap:40px;padding:40px}}
.slide{{width:1080px;height:1350px;position:relative;overflow:hidden;background:#0B0B0D;color:#fff;
  font-family:'DM Sans',sans-serif}}
.glowA{{position:absolute;width:900px;height:900px;border-radius:50%;left:-380px;top:-300px;
  background:radial-gradient(circle,rgba(255,149,0,.30),rgba(224,64,160,.10) 45%,transparent 70%);filter:blur(40px)}}
.glowB{{position:absolute;width:900px;height:900px;border-radius:50%;right:-420px;bottom:-360px;
  background:radial-gradient(circle,rgba(123,47,190,.38),transparent 70%);filter:blur(40px)}}
.dots{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.035) 1.5px,transparent 1.5px);background-size:44px 44px}}
.in{{position:absolute;inset:0;padding:88px 80px 128px;display:flex;flex-direction:column}}
.h{{font-family:'Syne',sans-serif;font-weight:800;letter-spacing:-3px;line-height:1.02}}
.o{{color:{O}}}
.pill{{align-self:flex-start;font-family:'Syne',sans-serif;font-weight:800;font-size:34px;letter-spacing:1px;
  padding:14px 34px;border-radius:60px;color:#fff;background:linear-gradient(90deg,{O},{P})}}
.pill.ghost{{background:transparent;border:3px solid {O}}}
.body{{font-size:42px;line-height:1.32;color:#C9C9CF;font-weight:500}}
.foot{{position:absolute;left:80px;right:80px;bottom:52px;display:flex;justify-content:space-between;align-items:center;
  font-size:27px;color:rgba(255,255,255,.55);font-weight:500}}
.foot b{{color:#fff;font-weight:700}}
.count{{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:40px;padding:8px 22px}}
.card{{min-height:0;overflow:hidden;background:rgba(255,255,255,.035);border:2px solid rgba(255,255,255,.10);border-radius:32px}}
.icon{{width:104px;height:104px;border-radius:50%;background:rgba(255,149,0,.10);border:2px solid rgba(255,149,0,.35);
  display:flex;align-items:center;justify-content:center}}
.row{{display:flex;align-items:center;justify-content:space-between}}
"""

def foot(n, total=7):
    return f'<div class="foot"><span><b>@koolestpro</b> | Shopify CRO &amp; UX</span><span class="count">{n} / {total}</span></div>'

def shell(inner, n, extra_bg=""):
    return f'<div class="slide" data-n="{n}"><div class="glowA"></div><div class="glowB"></div><div class="dots"></div>{extra_bg}<div class="in">{inner}</div>{foot(n)}</div>'

def bars(widths, h, gap, color, radius=12):
    return "".join(f'<div style="width:{w}%;height:{h}px;border-radius:{radius}px;background:{color};margin-bottom:{gap}px"></div>' for w in widths)

# ---------------- slide 1: type-led cover (90-ideas route) ----------------
glyph = 'stroke="rgba(255,255,255,.55)" stroke-width="3" fill="none" stroke-linecap="round"'
cover_art = f"""
<div style="position:absolute;inset:0;background:
  radial-gradient(120% 80% at 0% 0%,rgba(255,149,0,.55),transparent 55%),
  radial-gradient(90% 70% at 100% 100%,rgba(123,47,190,.75),transparent 60%),
  radial-gradient(70% 60% at 100% 10%,rgba(224,64,160,.35),transparent 60%),#0B0B0D"></div>
<div class="dots"></div>
<svg width="1080" height="1350" style="position:absolute;inset:0">
  <rect x="48" y="48" width="984" height="1254" rx="6" {glyph} stroke-opacity=".6"/>
  <path d="M48 110V48h62M970 48h62v62M1032 1240v62h-62M110 1302H48v-62" stroke="#fff" stroke-width="6" fill="none"/>
  <g transform="translate(860,120)" {glyph}><path d="M10 70 L40 0 L70 70 M22 44 H58"/><path d="M92 70 v-34 a18 18 0 0 1 36 0 v34 M92 50 h36"/></g>
  <g transform="translate(830,420)" {glyph}><path d="M0 0h150M0 34h110M0 68h70M0 102h40"/></g>
  <g transform="translate(940,600)" {glyph}><path d="M0 0v130M-18 18L0 0l18 18M-18 112L0 130l18-18"/></g>
  
</svg>"""
s1 = f"""<div class="slide" data-n="1">{cover_art}<div class="in" style="padding:150px 96px 190px">
  <div style="font-size:30px;font-weight:700;letter-spacing:6px;color:rgba(255,255,255,.8)">PRODUCT PAGE TYPOGRAPHY</div>
  <div class="h" style="font-size:400px;letter-spacing:-14px;line-height:.78;margin-top:24px;color:{O}">6</div>
  <div class="h" style="font-size:128px;letter-spacing:-5px;line-height:.95;margin-top:18px">TYPE LEVELS<br>THAT SELL</div>
  <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-top:40px">
    <div class="body" style="color:#fff;font-size:42px">Your headline got bigger.<br>The page still feels flat.</div>
    <div style="font-family:'Syne';font-weight:800;font-size:36px;letter-spacing:3px;white-space:nowrap;padding-bottom:6px">SWIPE →</div></div>
</div><div class="foot" style="justify-content:center"><span><b>@koolestpro</b> | Shopify CRO &amp; UX</span></div></div>"""

# ---------------- slide 2: myth ----------------
loud = "".join(f'<div style="height:{h}px;width:{w}%;background:rgba(255,255,255,.82);border-radius:10px;margin-bottom:22px"></div>'
               for w, h in [(92, 56), (80, 52), (88, 54), (70, 50)])
s2 = shell(f"""
  <div class="row"><div class="pill">MYTH</div><div class="icon">{ICON('megaphone')}</div></div>
  <div class="h" style="font-size:100px;margin-top:48px">If it matters,<br>make it <span class="o">bigger.</span></div>
  <div class="card" style="flex:1;margin-top:56px;padding:44px 48px;position:relative">
    <div style="font-size:30px;font-weight:700;letter-spacing:4px;color:rgba(255,255,255,.5);margin-bottom:34px">EVERYTHING SHOUTS</div>{loud}
  </div>
  <div style="font-family:'Syne';font-weight:800;font-size:48px;color:{O};margin-top:28px">= nothing leads.</div>
  <div class="body" style="margin-top:24px">The H1 grows. Then the subhead. Then the price. Now it's all loud.</div>
""", 2)

# ---------------- slide 3: reality (ranking podium) ----------------
pod = lambda n, h, c, lab: f'''<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end">
  <div style="font-size:32px;font-weight:700;color:rgba(255,255,255,.75);margin-bottom:16px">{lab}</div>
  <div style="width:100%;height:{h}px;border-radius:24px 24px 0 0;background:{c};display:flex;justify-content:center;padding-top:22px;
  font-family:Syne;font-weight:800;font-size:88px;color:#0B0B0D">{n}</div></div>'''
s3 = shell(f"""
  <div class="row"><div class="pill ghost">REALITY</div><div class="icon">{ICON('list-ordered')}</div></div>
  <div class="h" style="font-size:96px;margin-top:48px">Hierarchy is<br>a <span class="o">ranking</span>,<br>not a size.</div>
  <div style="flex:1;display:flex;gap:22px;align-items:flex-end;margin-top:40px;min-height:0;border-bottom:3px solid rgba(255,255,255,.25)">
    {pod(2,250,'rgba(255,255,255,.72)','Signpost')}{pod(1,360,f'linear-gradient(180deg,{O},{M})','Promise')}{pod(3,170,'rgba(255,255,255,.42)','Claim')}
  </div>
  <div class="body" style="margin-top:36px">Six things at 32px isn't six levels. It's one level, printed six times.</div>
""", 3)

# ---------------- slide 4: stat ----------------
scan = "".join(
    f'<div style="height:{h}px;width:{w}%;border-radius:8px;background:{"rgba(255,149,0,.95)" if hi else "rgba(255,255,255,.14)"}"></div>'
    for w, h, hi in [(80, 30, 1), (60, 16, 0), (70, 16, 0), (40, 24, 1), (66, 16, 0), (52, 24, 1), (62, 16, 0)])
s4 = shell(f"""
  <div class="row"><div class="pill ghost">WHY IT BREAKS</div><div class="icon">{ICON('scan-eye')}</div></div>
  <div style="display:flex;gap:48px;align-items:center;margin-top:40px">
    <div class="h" style="font-size:250px;letter-spacing:-12px;line-height:.9;color:{O}">28%</div>
  </div>
  <div class="h" style="font-size:56px;letter-spacing:-2px;line-height:1.1;margin-top:18px">is the most of a page<br>people actually read.</div>
  <div class="card" style="flex:1;margin-top:48px;padding:40px 48px;display:flex;gap:44px">
    <div style="flex:1;display:flex;flex-direction:column;justify-content:space-between">{scan}</div>
    <div style="width:360px;display:flex;flex-direction:column;justify-content:center">
      <div style="font-size:40px;font-weight:700;line-height:1.25">They scan for the one thing that wins.</div>
      <div style="font-size:28px;color:rgba(255,255,255,.55);margin-top:18px">Source: Nielsen Norman Group</div></div>
  </div>
""", 4)

# ---------------- slide 5: the system (levels rendered at their own size) ----------------
lv = [("Page promise", "the outcome", 54, 1), ("Section signpost", "where am I", 46, .92), ("Block claim", "why this part", 44, .84),
      ("Body", "the proof", 40, .74), ("Action", "the button", 36, .64), ("Fine print", "the risk", 32, .54)]
rows = "".join(f'''<div class="row" style="padding:10px 0;border-bottom:2px solid rgba(255,255,255,.08)">
  <div style="display:flex;align-items:center;gap:28px"><div style="width:64px;height:64px;border-radius:50%;background:rgba(255,149,0,.12);
  border:2px solid rgba(255,149,0,.5);display:flex;align-items:center;justify-content:center;font-family:Syne;font-weight:800;font-size:32px;color:{O}">{i+1}</div>
  <div style="font-family:Syne;font-weight:800;font-size:{s}px;letter-spacing:-1px;white-space:nowrap;color:rgba(255,255,255,{a})">{n}</div></div>
  <div style="font-size:32px;white-space:nowrap;color:rgba(255,255,255,.55);font-weight:500">{j}</div></div>''' for i, (n, j, s, a) in enumerate(lv))
s5 = shell(f"""
  <div class="row"><div class="pill">THE SYSTEM</div><div class="icon">{ICON('rows-3')}</div></div>
  <div class="h" style="font-size:100px;margin-top:44px">Six levels.<br>Six <span class="o">jobs.</span></div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;margin-top:24px;min-height:0">{rows}</div>
  <div class="body" style="margin-top:20px;color:#fff">No job? It's not a level. Delete it.</div>
""", 5)

# ---------------- slide 6: missing level (space) ----------------
def panel(label, gap, accent):
    b = f'''<div style="width:88%;height:40px;border-radius:10px;background:rgba(255,255,255,.9);margin-bottom:{gap}px"></div>
    {bars([64,76,56],18,gap if gap>20 else 8,'rgba(255,255,255,.32)',8)}
    <div style="width:80%;height:40px;border-radius:10px;background:rgba(255,255,255,.9);margin-bottom:{gap}px"></div>
    {bars([70,52],18,gap if gap>20 else 8,'rgba(255,255,255,.32)',8)}
    <div style="width:60%;height:56px;border-radius:40px;background:{"linear-gradient(90deg,#FF9500,#E040A0)" if accent else "rgba(255,255,255,.5)"}"></div>'''
    return f'''<div class="card" style="flex:1;padding:36px 34px;{"border-color:rgba(255,149,0,.6)" if accent else ""};display:flex;flex-direction:column">
    <div style="font-size:30px;font-weight:700;letter-spacing:4px;color:{O if accent else "rgba(255,255,255,.5)"};margin-bottom:34px">{label}</div>
    <div style="flex:1;display:flex;flex-direction:column;justify-content:{"space-between" if accent else "flex-start"}">{b}</div></div>'''
s6 = shell(f"""
  <div class="row"><div class="pill">THE MISSING LEVEL</div><div class="icon">{ICON('move-vertical')}</div></div>
  <div class="h" style="font-size:88px;margin-top:44px">Two of your<br>six levels are<br>pure <span class="o">space.</span></div>
  <div style="flex:1;display:flex;gap:28px;margin-top:40px;min-height:0">{panel("CRAMPED",8,False)}{panel("SPACED",26,True)}</div>
  <div class="body" style="margin-top:36px">Same type sizes. Only the gaps changed.</div>
""", 6)

# ---------------- slide 7: CTA ----------------
s7 = f"""<div class="slide" data-n="7"><div class="glowA"></div><div class="glowB"></div><div class="dots"></div>
<div style="position:absolute;inset:48px;border-radius:40px;padding:4px;background:linear-gradient(135deg,{O},{M},{P})">
 <div style="width:100%;height:100%;border-radius:36px;background:#0B0B0D"></div></div>
<div class="in" style="align-items:center;justify-content:center;text-align:center;padding:100px 110px 170px">
  <div style="width:220px;height:220px;border-radius:50%;padding:6px;background:linear-gradient(135deg,{O},{P})">
    <img src="{AV}" style="width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:center top;background:#222"></div>
  <div class="h" style="font-size:80px;margin-top:48px">Which level<br>is your page<br><span class="o">missing?</span></div>
  <div class="body" style="margin-top:40px;max-width:800px">I audit Shopify product pages for hierarchy and the path to checkout.</div>
  <div style="margin-top:44px;padding:28px 60px;border-radius:80px;background:linear-gradient(90deg,{O},{M},{P});font-family:Syne;font-weight:800;font-size:44px">Get a CRO audit →</div>
  <div style="margin-top:36px;font-size:38px;font-weight:700;color:{O}">koolestpro.com/services/cro-audit</div>
  <div style="margin-top:22px;font-size:32px;color:rgba(255,255,255,.6)">Save this for your next build.</div>
</div>{foot(7)}</div>"""

html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{s1}{s2}{s3}{s4}{s5}{s6}{s7}</body></html>"""
out = sys.argv[1] if len(sys.argv) > 1 else "tips_v4_typography.html"
open(out, "w").write(html)
print(out)
