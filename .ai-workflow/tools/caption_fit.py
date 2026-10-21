#!/usr/bin/env python3
"""
caption_fit.py: does this caption actually describe the image(s) it's posted with?

Added 2026-09-28 after Ridwan spotted captions that didn't match their image:
a single static ad going out with "Four ad directions from one pan...", and
CRO annotated graphics carrying a before/after or carousel caption. Root cause
was populate_sheet.py dealing captions out of a shared pool by index; the fix is
per-image caption keys (see populate_sheet.py CALENDAR). This module is the
safety net that catches whatever still slips through.

Rules (each returns a reason string; empty list = fits):
  R1 multi-image talk on a single-image row  ("four ad directions", "swipe",
     "carousel", "slides", "all 4 ads", "these ads", "👇")
  R2 stray char-count line pasted into the caption ("158 chars")
  (No rule for "X ..." / "OK ..." line markers: that contrast frame is one of
   Ridwan's proven X patterns, see docs/system/x-caption-playbook.md.)
  R3 before/after asset whose caption never contrasts before vs after
     (soft: only when the caption is an X single)
  R4 empty caption

Used by populate_sheet.py (per row, at build time) and runnable on the whole
queue:  python3 caption_fit.py [--queue outputs/distribution-queue/queue.json]
"""
import argparse, json, os, re, sys

MULTI_RE = re.compile(
    r"\b(four|4|five|5|three|3|two|2)\s+(static\s+)?(ad|ads|directions|angles|slides|images|graphics|creatives)\b"
    r"|\bswipe\b|\b(this|the|my|our)\s+carousel\b|\bslides?\s*\d|\bthese\s+(ads|slides|images)\b|\ball\s+(four|4|five|5)\b|👇|→\s*swipe",
    re.I)
CHARCOUNT_RE = re.compile(r"(^|\n)\s*\d{2,4}\s*chars?\s*$", re.I)
BA_WORDS_RE = re.compile(r"\bbefore\b|\bafter\b|\bwas\b.*\bnow\b|\bfrom\b.*\bto\b|\bold\b.*\bnew\b|\bfix(ed|es)?\b|\bmoved?\b|\brebuil|\bredesign|\bchanged?\b", re.I | re.S)


def asset_kind(path):
    b = os.path.basename(path or "").lower()
    # Order matters (fixed 2026-10-11): the old bare "_ba" substring test matched
    # every Bala file ("koolestpro_bala_...") and called them all before/afters.
    if "variants-board" in b:
        return "variants"
    if "carousel_slide2" in b:
        return "before-after"
    if "annotat" in b or "carousel_slide3" in b:
        return "annotated"
    if "carousel_slide1" in b or "cover" in b:
        return "cover"
    if "before-after" in b or re.search(r"_ba(?=[._-]|$)", os.path.splitext(b)[0] + "."):
        return "before-after"
    if "combined-showcase" in b:
        return "combo"
    m = re.search(r"ad-(\d)", b)
    if m:
        return f"ad-{m.group(1)}"
    return "other"


def check(caption, asset_paths, platform=""):
    reasons = []
    cap = caption or ""
    assets = [a.strip() for a in (asset_paths or "").replace(";", "\n").split("\n") if a.strip()]
    if not cap.strip():
        return ["caption-fit: empty caption"]
    if CHARCOUNT_RE.search(cap):
        reasons.append("caption-fit: stray char-count line in caption")
    if len(assets) == 1:
        kind = asset_kind(assets[0])
        m = MULTI_RE.search(cap)
        # the combined showcase IS all four ads in one image, so multi-ad talk fits it
        if m and kind != "combo":
            reasons.append(f"caption-fit: caption talks about several images ('{m.group(0)}') but row posts one {kind} image")
        if kind == "before-after" and platform == "Twitter" and not BA_WORDS_RE.search(cap):
            reasons.append("caption-fit: before/after image but caption never contrasts before vs after")
    return reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", default="outputs/distribution-queue/queue.json")
    ap.add_argument("--all", action="store_true", help="include Posted rows")
    a = ap.parse_args()
    rows = json.load(open(a.queue, encoding="utf-8"))["rows"]
    bad = 0
    for r in rows:
        if r.get("status") == "Posted" and not a.all:
            continue
        rs = check(r.get("caption"), r.get("asset_paths"), r.get("platform"))
        if rs:
            bad += 1
            print(f"{r['scheduled_date']} {r['platform']:9} {r['post_id']}\n    asset: {os.path.basename((r.get('asset_paths') or '').split(';')[0].strip())}\n    " + "\n    ".join(rs))
    print(f"\n{bad} row(s) with caption/image problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
