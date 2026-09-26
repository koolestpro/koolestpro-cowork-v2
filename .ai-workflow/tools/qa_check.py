#!/usr/bin/env python3
"""
qa_check.py — V2 distribution pipeline, Step 4.

Automated quality pass over a harvested content record, run after harvest and
before the row is written to the Sheet. FLAG-NOT-BLOCK: a failing check never
stops content reaching the queue — it writes qa_status = "Needs Review: <reason>"
so Ridwan reviews it, but the row is still created.

Five checks (per the V2 plan):
  1. File existence     — every asset path in the record resolves on disk.
  2. Export-compat scan  — grep the source HTML for banned patterns already
                           documented in CLAUDE.md (CSS gradient text, banned
                           SVG gradient text, missing chrome-hide selectors,
                           stat/headline SVG viewBox width < 300px).
  3. Visual inspection   — CANNOT be fully automated (needs Claude's eyes). This
                           script lists the images/thumbnails to open and marks
                           them "manual-visual-pending" so the calling task
                           knows to Read them. Not a Pass on its own.
  4. Claims spot-check   — flag any specific number / % / trust-claim / other
                           brand name in a caption for verification against the
                           audit brief or live source (per the V1CE HSBC/IBM
                           near-miss).
  5. Caption-asset match — heuristic sanity: the brand appears in the caption,
                           caption isn't empty, X-post count is plausible.

Exit: writes qa fields back into the record JSON (in place unless --out given)
and prints a summary. Overall qa_status is "Pass" only if checks 1, 2, 5 pass
AND there are no unresolved visual/claims flags requiring human eyes; otherwise
"Needs Review: <semicolon-joined reasons>".

Usage:
    python3 qa_check.py <harvest_record.json> [--project-root DIR] [--out FILE]
"""

import argparse
import json
import os
import re
import sys

# ---- banned patterns from CLAUDE.md gradient/export rules ----
BANNED_HTML_PATTERNS = [
    (r"-webkit-background-clip:\s*text", "CSS gradient text (-webkit-background-clip:text) — invisible in html2canvas export"),
    (r"background-clip:\s*text", "CSS background-clip:text — gradient text banned, use solid colors"),
    (r'fill\s*=\s*["\']url\(#grad', "SVG gradient text (fill=url(#grad...)) — banned per updated CLAUDE.md, use solid colors"),
]
# chrome-hide selectors that MUST all appear in a capture routine if the file
# has a captureSlide/captureFixed function
REQUIRED_CHROME_SELECTORS = [".swb", "#download-panel", ".posts-shell"]

# caption text that names a trust/authority claim worth verifying
# NOTE on the leading \b: it must NOT apply to the "$" alternative. A word
# boundary cannot exist between a space and "$" (both non-word), so the old
# "\b(...|\$\s?\d)" form silently never matched a price — "$29.74" went
# unflagged for the life of this script. Prices are precisely the kind of
# number CLAUDE.md forbids inventing, so \b is now scoped to the word
# alternatives only. Decimals are matched too, so the snippet reads "1.5%"
# rather than clipping to "5%".
CLAIM_HINTS = re.compile(
    r"(?:\b(?:trusted by|used by|clients?|customers?|as seen|featured in|"
    r"\d[\d,]*(?:\.\d+)?\s*"
    r"(?:%|percent|reviews?|customers?|stores?|brands?|sales?|orders?))|"
    r"\$\s?\d[\d,]*(?:\.\d+)?)", re.IGNORECASE)

# The concept-build disclaimer CLAUDE.md REQUIRES on KURA/HALOS/MERIDIAN/Lumora
# posts is itself built from the words CLAIM_HINTS looks for ("not a client",
# "not a real Gainful customer"). Flagging it told Ridwan to go verify the one
# sentence that exists to prevent a false claim, and buried the real flags in
# noise. Match these spans first and skip any claim hit that falls inside one.
#
# Deliberately narrow: it suppresses only the negated phrase itself, so
# "800,000 customers" two sentences later still flags normally.
CLAIM_DISCLAIMERS = re.compile(
    r"(?:is\s+)?not\s+a\s+(?:live\s+)?client(?:\s+site)?"
    r"|not\s+a\s+real\s+\w+\s+customers?"
    r"|no\s+client\s+attached"
    r"|,\s*no\s+client\b"
    r"|\bconcept\s+build\b"
    r"|\bmy\s+own\s+build\b",
    re.IGNORECASE)


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve(project_root, rel):
    return rel if os.path.isabs(rel) else os.path.join(project_root, rel)


def check_files(record, root):
    reasons, missing = [], []
    assets = record.get("assets", {})
    paths = list(assets.get("images", []))
    vid = assets.get("video")
    if isinstance(vid, list):
        paths += vid
    elif vid:
        paths.append(vid)
    for p in paths:
        if not os.path.exists(resolve(root, p)):
            missing.append(p)
    if missing:
        reasons.append(f"missing asset file(s): {', '.join(missing)}")
    return {"pass": not missing, "checked": len(paths), "missing": missing}, reasons


def check_export_compat(record, root):
    reasons = []
    companion = record.get("companion_html")
    if not companion:
        return {"pass": True, "scanned": False, "note": "no companion_html to scan"}, reasons
    path = resolve(root, companion)
    if not os.path.exists(path):
        return {"pass": True, "scanned": False, "note": f"companion not found: {companion}"}, reasons
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    hits = []
    for pat, msg in BANNED_HTML_PATTERNS:
        if re.search(pat, html):
            hits.append(msg)

    # chrome-hide selector completeness (only if a capture routine exists)
    if re.search(r"html2canvas\s*\(", html):
        tohide_blocks = re.findall(r"querySelectorAll\((['\"])(.*?)\1\)", html)
        joined = " ".join(b[1] for b in tohide_blocks)
        if joined:
            for sel in REQUIRED_CHROME_SELECTORS:
                if sel not in joined:
                    hits.append(f"chrome-hide selector '{sel}' missing from capture routine (Bug 1 risk)")

    # SVG viewBox width < 300 on stat/headline text
    for m in re.finditer(r'<svg[^>]*\bwidth=["\'](\d+)["\'][^>]*>(.*?)</svg>', html, re.DOTALL | re.IGNORECASE):
        width = int(m.group(1))
        inner = m.group(2)
        if "<text" in inner and width < 300:
            hits.append(f"SVG width={width}px < 300px with <text> inside — export-clip risk (Bug 2)")
            break

    if hits:
        reasons.append("export-compat: " + "; ".join(sorted(set(hits))))
    return {"pass": not hits, "scanned": True, "hits": sorted(set(hits))}, reasons


def check_claims(record):
    reasons, flags = [], []
    caps = record.get("captions", {})
    texts = []
    if caps.get("linkedin"):
        texts.append(("linkedin", caps["linkedin"]))
    for i, x in enumerate(caps.get("x", []) or []):
        texts.append((f"x[{i}]", x))
    for label, t in texts:
        safe = [(d.start(), d.end()) for d in CLAIM_DISCLAIMERS.finditer(t)]
        for m in CLAIM_HINTS.finditer(t):
            # Inside a required disclaimer? Then this is compliance text, not a
            # claim anyone can verify. Skip it.
            if any(s <= m.start() and m.end() <= e for s, e in safe):
                continue
            snippet = t[max(0, m.start() - 20): m.end() + 20].replace("\n", " ").strip()
            flags.append(f"{label}: \"...{snippet}...\"")
    if flags:
        reasons.append(f"claims to verify ({len(flags)}): " + " | ".join(flags[:6]))
    return {"pass": not flags, "flags": flags}, reasons


X_CHAR_LIMIT = 280  # non-Premium X accounts hard-cap at this length


def check_caption_asset_match(record):
    reasons = []
    caps = record.get("captions", {})
    brand = (record.get("brand") or "").strip()
    li = caps.get("linkedin", "") or ""
    x = caps.get("x", []) or []
    if not li and not x:
        reasons.append("no LinkedIn or X caption harvested — nothing to post")
    if brand and li and brand.lower() not in li.lower() and brand.lower() != "koolestpro":
        # brand absence is a soft flag (some captions are intentionally brand-agnostic)
        reasons.append(f"brand '{brand}' not mentioned in LinkedIn caption — check caption matches this asset")
    return {"pass": not reasons, "brand": brand}, reasons


X_FULL_KEYS = ("x", "x_singles", "x_angles", "x_thread")


def check_x_caption_lengths(record):
    """Catches the 2026-07-22 bug class: multiple X post variants getting
    concatenated into one over-length body downstream (populate_sheet.py) or
    a single harvested variant that's simply too long on its own.

    Fixed 2026-07-29: this used to only scan the compact `captions.x` field,
    which the JSON Standard defines as optional and which harvest_content.py
    only ever populated from block-based skills' 'x'/'x_singles' keys — for
    the tab-based skills (CRO Fix, Tips), the real variants live under
    captions_full's x_angles/x_thread and this check saw nothing, so it
    passed 6 rows that were later confirmed to be 522-921 chars. Now scans
    every X-flavoured key in captions_full directly, which is what
    populate_sheet.py actually draws from."""
    reasons = []
    checked = []
    overlong = []
    full = record.get("captions_full", {})
    for key in X_FULL_KEYS:
        v = full.get(key, {}).get("text")
        if v is None:
            continue
        variants = v if isinstance(v, list) else [v]
        for i, text in enumerate(variants):
            checked.append(f"{key}[{i}]")
            if len(text) > X_CHAR_LIMIT:
                overlong.append((f"{key}[{i}]", len(text)))
    if overlong:
        detail = ", ".join(f"{label}={n} chars" for label, n in overlong)
        reasons.append(f"X caption variant(s) over {X_CHAR_LIMIT}-char limit: {detail} — "
                        f"will be rejected by X for non-Premium accounts; verify populate_sheet.py "
                        f"isn't joining multiple variants into one post body")
    return {"pass": not overlong, "checked": len(checked), "overlong": overlong}, reasons


def main():
    ap = argparse.ArgumentParser(description="Automated QA pass over a harvested content record (flag-not-block).")
    ap.add_argument("record")
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    rec_path = os.path.abspath(args.record)
    record = load(rec_path)

    root = args.project_root
    if not root:
        d = os.path.dirname(rec_path)
        while d != "/" and not os.path.exists(os.path.join(d, "CLAUDE.md")):
            d = os.path.dirname(d)
        root = d if os.path.exists(os.path.join(d, "CLAUDE.md")) else os.path.dirname(rec_path)
    root = os.path.abspath(root)

    files_r, files_reasons = check_files(record, root)
    export_r, export_reasons = check_export_compat(record, root)
    claims_r, claims_reasons = check_claims(record)
    match_r, match_reasons = check_caption_asset_match(record)
    xlen_r, xlen_reasons = check_x_caption_lengths(record)

    # images the calling task (Claude) must actually open and eyeball
    visual_targets = list(record.get("assets", {}).get("images", []))

    hard_reasons = files_reasons + export_reasons + match_reasons + xlen_reasons  # block-worthy → Needs Review
    soft_reasons = claims_reasons                                   # human-eyes flags

    needs_review = bool(hard_reasons) or bool(soft_reasons) or bool(visual_targets)
    if needs_review:
        all_reasons = hard_reasons + soft_reasons
        if visual_targets:
            all_reasons = all_reasons + [f"manual-visual-pending: open {len(visual_targets)} image(s) to eyeball brand/legibility/framing"]
        qa_status = "Needs Review: " + "; ".join(all_reasons)
    else:
        qa_status = "Pass"

    record["qa"] = {
        "qa_status": qa_status,
        "checks": {
            "file_existence": files_r,
            "export_compat": export_r,
            "claims_spotcheck": claims_r,
            "caption_asset_match": match_r,
            "x_caption_lengths": xlen_r,
            "visual_inspection": {
                "pass": None,
                "manual_visual_pending": visual_targets,
                "note": "Claude must Read these images and confirm dark-theme brand look, legible headline, no broken layout, correct device framing (Template Showcase).",
            },
        },
    }
    record["qa_status"] = qa_status  # top-level convenience for the Sheet writer

    out = args.out or rec_path
    with open(out, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    print(f"[qa] {record.get('pipeline_item_id','?')} -> {qa_status}")
    if hard_reasons:
        print("  HARD flags:", "; ".join(hard_reasons))
    if soft_reasons:
        print("  claim flags:", "; ".join(soft_reasons))
    if visual_targets:
        print(f"  visual: open {len(visual_targets)} image(s) for manual review")
    print(f"[qa] record updated in place: {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
