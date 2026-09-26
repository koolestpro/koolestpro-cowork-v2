#!/usr/bin/env python3
"""Add a supporting visual (avatar + name) to the cover slide (slide 1) of the
V2 Tips carousel prototype, per Ridwan's standing rule: the cover slide should
always carry a supporting visual, not just typography, while keeping text minimal."""
import re, sys, pathlib

ROOT = pathlib.Path("/sessions/stoic-youthful-hamilton/mnt/koolestpro-cowork-v2")
TARGET = ROOT / "outputs/tips/animation-budget-motion-conversion-v2_2026-07-28.html"

html = TARGET.read_text(encoding="utf-8")

def sub_once(pattern, repl, s, flags=0, label=""):
    new, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
    if n != 1:
        sys.exit(f"ANCHOR FAIL [{label}] matched {n} times")
    return new

old = '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.35);">Conversion Strategy</div>'

new = (
 '<div style="display:flex;align-items:center;gap:12px;">'
 '<div style="width:44px;height:44px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,149,0,0.4);flex-shrink:0;">'
 '<img src="https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle_mvcdss" style="width:100%;height:100%;object-fit:cover;" onerror="this.parentNode.style.display=\'none\'"></div>'
 '<div><div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:14px;color:#fff;">Ridwan Adekunle</div>'
 '<div style="font-family:\'DM Mono\',monospace;font-size:10px;color:rgba(255,255,255,0.4);margin-top:1px;">Shopify CRO &amp; UX Designer</div></div></div>'
 '<div style="font-family:\'DM Mono\',monospace;font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-top:16px;">Conversion Strategy</div>'
)

html = sub_once(re.escape(old), new, html, label="slide1-visual")

TARGET.write_text(html, encoding="utf-8")
print("PATCHED", TARGET, len(html), "chars")
