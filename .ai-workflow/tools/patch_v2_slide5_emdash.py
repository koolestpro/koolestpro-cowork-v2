#!/usr/bin/env python3
"""Patch pass on the V2 prototype:
 1. Remove em dashes from slide 2 and slide 6 copy.
 2. Rebuild slide 5 with bigger text, better layout (flex:1 + space-evenly so
    it fills the frame instead of leaving a gap), and a real screenshot
    reference (an actual crop from assets/_archive/replo-pages-cache-retired/halos-pdp-01, hosted on
    Cloudinary) proving the "selection feedback / add-to-cart confirmation"
    point instead of just asserting it.
"""
import re, sys, pathlib

ROOT = pathlib.Path("/sessions/stoic-youthful-hamilton/mnt/koolestpro-cowork-v2")
TARGET = ROOT / "outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html"

html = TARGET.read_text(encoding="utf-8")

def sub_once(pattern, repl, s, flags=0, label=""):
    new, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
    if n != 1:
        sys.exit(f"ANCHOR FAIL [{label}] matched {n} times")
    return new

A = "'"

# ---- 1. em dash removal (slide 2 + slide 6 only — visible slide content) ----
html = sub_once(
    r"That's the trap every Shopify brand falls into &mdash; and it's wrong\.",
    "That's the trap every Shopify brand falls into. It's wrong.",
    html, label="slide2-emdash")

html = sub_once(
    r"If not &mdash; cut it\.",
    "If not, cut it.",
    html, label="slide6-emdash")

# ---- 2. rebuild slide 5 ----
IMG_URL = "https://res.cloudinary.com/drl0rscuf/image/upload/v1785272337/koolestpro/tips-carousel/halos-pdp-atc-composite.png"

def label3(n, t):
    return (f'<div style="display:flex;align-items:center;gap:18px;padding:14px 0;">'
            f'<div style="width:46px;height:46px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,#FF9500,#7B2FBE);display:flex;align-items:center;justify-content:center;font-family:\'Syne\',sans-serif;font-weight:800;font-size:19px;color:#fff;">{n}</div>'
            f'<div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:25px;color:#fff;">{t}</div></div>')

OUTBOX = lambda t: (f'<div style="display:inline-block;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.5);'
                    f'font-family:\'DM Mono\',monospace;font-size:9px;font-weight:500;letter-spacing:2px;text-transform:uppercase;'
                    f'padding:4px 12px;border-radius:4px;">{t}</div>')

new_s5_inner = (
 f'<div style="margin-bottom:18px;">{OUTBOX("Where motion earns its place")}</div>'
 f'<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:34px;line-height:1.18;letter-spacing:-1px;color:#fff;">Only 3 things earn the budget.</div>'
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;margin:6px 0;">'
 f'{label3(1,"Selection feedback")}{label3(2,"Add-to-cart confirmation")}{label3(3,"Proof reveal")}</div>'
 f'<div style="border-radius:10px;overflow:hidden;border:1px solid rgba(255,255,255,0.12);">'
 f'<img src="{IMG_URL}" style="width:100%;display:block;" onerror="this.parentNode.style.display={A}none{A}"></div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:12px;color:rgba(255,255,255,0.32);margin-top:10px;">From a real PDP I built for HALOS.</div>'
)

# locate slide 5 precisely: it's the one with "Only 3 things earn"/OUTBOX "Where motion earns its place"
pattern = re.compile(
    r'<div class="slide" style="background:#0a0a0a;">(?:(?!</div>\n\n<div class="slide").)*?Where motion earns its place.*?</div>\n</div>',
    re.S)
matches = list(pattern.finditer(html))
if len(matches) != 1:
    sys.exit(f"ANCHOR FAIL [slide5-locate] matched {len(matches)} times")
old_block = matches[0].group(0)

GLOW_TR = '<div style="position:absolute;top:-80px;right:-60px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,0.16),rgba(224,64,160,0.07),transparent 70%);filter:blur(70px);pointer-events:none;"></div>'
GLOW_BL = '<div style="position:absolute;bottom:-60px;left:-40px;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,0.15),transparent 70%);filter:blur(60px);pointer-events:none;"></div>'
DOTGRID = '<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.02) 1px,transparent 1px);background-size:24px 24px;pointer-events:none;"></div>'
ATTR = '<div style="position:absolute;bottom:18px;right:24px;font-family:\'DM Mono\',monospace;font-size:12px;color:rgba(255,255,255,0.18);z-index:10;">Ridwan - Shopify CRO &amp; UX Designer</div>'

new_block = (f'<div class="slide" style="background:#0a0a0a;">\n{GLOW_TR}\n{GLOW_BL}\n{DOTGRID}\n'
             f'<div style="position:relative;z-index:2;padding:46px 44px;height:100%;display:flex;flex-direction:column;">\n{new_s5_inner}\n</div>\n{ATTR}\n</div>')

html = html.replace(old_block, new_block, 1)

TARGET.write_text(html, encoding="utf-8")
print("PATCHED", TARGET, len(html), "chars")
