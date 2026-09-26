#!/usr/bin/env python3
"""Rebuild the cover slide (slide 1) so a real image leads, per Ridwan's note:
the cover should be mostly images, with text kept minimal. Replaces the
avatar-row-only version with: real product photo (hero, framed) -> small
avatar+name row -> eyebrow -> headline (smaller, no separate subline) -> swipe cue."""
import re, sys, pathlib

ROOT = pathlib.Path("/sessions/stoic-youthful-hamilton/mnt/koolestpro-cowork-v2")
TARGET = ROOT / "outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html"

html = TARGET.read_text(encoding="utf-8")

def sub_once(pattern, repl, s, flags=0, label=""):
    new, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
    if n != 1:
        sys.exit(f"ANCHOR FAIL [{label}] matched {n} times")
    return new

IMG_URL = "https://res.cloudinary.com/drl0rscuf/image/upload/v1785276545/koolestpro/tips-carousel/halos-pdp-hero-cover.png"
A = "'"

old = (
 '<div style="display:flex;align-items:center;gap:12px;">'
 '<div style="width:44px;height:44px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,149,0,0.4);flex-shrink:0;">'
 '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" style="width:100%;height:100%;object-fit:cover;" onerror="this.parentNode.style.display=\'none\'"></div>'
 '<div><div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:14px;color:#fff;">Ridwan Adekunle</div>'
 '<div style="font-family:\'DM Mono\',monospace;font-size:10px;color:rgba(255,255,255,0.4);margin-top:1px;">Shopify CRO &amp; UX Designer</div></div></div>'
 '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-top:16px;">Conversion Strategy</div>'
 '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
 '<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:42px;line-height:1.14;letter-spacing:-1px;color:#fff;">Your store'
 + A + 's animations aren'
 + A + 't making it look premium. They'
 + A + 're making it convert <span style="color:#FF9500;">worse.</span></div>'
 '<div style="font-family:\'DM Mono\',monospace;font-size:15px;color:rgba(255,255,255,0.5);line-height:1.6;margin-top:20px;">The motion myth every Shopify brand falls for.</div></div>'
)

new = (
 f'<div style="border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,0.1);height:250px;flex-shrink:0;">'
 f'<img src="{IMG_URL}" style="width:100%;height:100%;object-fit:cover;object-position:center;" onerror="this.parentNode.style.display={A}none{A}"></div>'
 f'<div style="display:flex;align-items:center;gap:10px;margin-top:16px;">'
 f'<div style="width:36px;height:36px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,149,0,0.4);flex-shrink:0;">'
 f'<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" style="width:100%;height:100%;object-fit:cover;" onerror="this.parentNode.style.display={A}none{A}"></div>'
 f'<div><div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:13px;color:#fff;">Ridwan Adekunle</div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:10px;color:rgba(255,255,255,0.4);margin-top:1px;">Shopify CRO &amp; UX Designer</div></div></div>'
 f'<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-top:14px;">Conversion Strategy</div>'
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;">'
 f'<div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:28px;line-height:1.18;letter-spacing:-0.5px;color:#fff;">Your store'
 + A + 's animations aren'
 + A + 't making it look premium. They'
 + A + 're making it convert <span style="color:#FF9500;">worse.</span></div></div>'
)

html = sub_once(re.escape(old), new, html, label="slide1-hero-image")

TARGET.write_text(html, encoding="utf-8")
print("PATCHED", TARGET, len(html), "chars")
