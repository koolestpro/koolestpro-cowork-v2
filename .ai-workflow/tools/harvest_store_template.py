#!/usr/bin/env python3
"""Harvest a STORE TEMPLATE launch package into a distribution harvest record.

Why this exists (2026-09-01)
----------------------------
Every other content stream ships a companion `index.html` that
`harvest_content.py` parses for caption tabs. Store template packages
(Lumora, Meridian, and every future one built under `store-templates/`) do
NOT — their deliverable is the mockup asset set plus a hand-written post set
that already lives, fully humanized, in `{brand-slug}-social-content.json`.

So Lumora and Meridian sat registered in SYNC_DATA with status "Created" and
zero distribution rows: `harvest_content.py` had no HTML to read, and the
"Template Showcase" calendar matched only video assets (cover.mp4 / laptop.mp4
/ mobile.mp4) that a stills-only store template never produces. They could
never reach the Sheet.

This script closes that gap by reading the post set straight from the
social-content library — which CLAUDE.md already names as the durable source
of truth for captions ("If they ever disagree, the brand social-content file
wins") — and emitting a record shaped exactly like `harvest_content.py`'s, so
qa_check.py / populate_sheet.py / feed_*.py / sync_content_system.py all
consume it unchanged.

Angle -> caption key mapping is driven by each asset record's own `angle`
field, which the Store Template Launch Content rule in CLAUDE.md already
requires. The five X angles are showcase / free-offer / niche / build-in-public /
full-page-at-a-glance (the mobile strip, added 2026-09-02).

Usage
-----
    python3 .ai-workflow/tools/harvest_store_template.py lumora \
        --out /tmp/lumora_harvest.json --project-root .

    # force a paid/client build (no free-site offer angle)
    python3 .ai-workflow/tools/harvest_store_template.py acme \
        --offer-type paid --out /tmp/acme_harvest.json --project-root .
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

# Caption keys the "Store Template" CALENDAR slots reference. Keeping these as
# named constants means a typo here fails loudly rather than silently
# producing an empty caption in a scheduled row.
K_LINKEDIN = "linkedin"
K_INSTAGRAM = "instagram"
K_X_SHOWCASE = "x_showcase"
K_X_FREEOFFER = "x_freeoffer"
K_X_NICHE = "x_niche"
K_X_BUILDPUBLIC = "x_buildpublic"
K_X_RESULTS = "x_results"  # paid builds use this in place of x_freeoffer
K_X_GLANCE = "x_glance"    # the mobile-strip "full page at a glance" post

# Substrings matched (case-insensitively) against an asset record's `angle`.
# Order matters: the first hit wins, and the bare "showcase" catch-all is last
# so a more specific angle is never swallowed by it.
X_ANGLE_RULES = [
    ("free offer", K_X_FREEOFFER),
    ("free site", K_X_FREEOFFER),
    ("nigeria package", K_X_FREEOFFER),
    ("niche", K_X_NICHE),
    ("build in public", K_X_BUILDPUBLIC),
    ("build-in-public", K_X_BUILDPUBLIC),
    # mobile-strip angle (2026-09-02). Listed ABOVE the generic result/process
    # rules so "full page at a glance" cannot be swallowed by them.
    ("at a glance", K_X_GLANCE),
    ("full page", K_X_GLANCE),
    ("mobile strip", K_X_GLANCE),
    ("mobilestrip", K_X_GLANCE),
    ("result", K_X_RESULTS),
    ("outcome", K_X_RESULTS),
    ("process", K_X_RESULTS),
]

EM_DASH_RE = re.compile(r"[—–]|&mdash;|&ndash;")


def load_sync_items(project_root):
    """Return SYNC_DATA.items from the content system, or [] if unreadable."""
    path = os.path.join(project_root, "ridwan_content_system_updated.html")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    m = re.search(r'<script id="cowork-sync-data"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return []
    try:
        return json.loads(m.group(1)).get("items", [])
    except json.JSONDecodeError:
        return []


def resolve_pipeline_item(social, items, warnings):
    """Find the real SYNC_DATA item id.

    The known gotcha this guards against (documented in the weekly assembly
    task): a harvest record carrying an id that does not exist in SYNC_DATA
    creates orphaned duplicate rows instead of joining to the existing item.
    So we take the id from `relatedPipelineItemIds` and VERIFY it resolves,
    rather than synthesizing one from the slug.
    """
    related = social.get("relatedPipelineItemIds") or []
    by_id = {it.get("id"): it for it in items}
    for rid in related:
        if rid in by_id:
            return rid, by_id[rid]
    # Fall back to a slug match before giving up — a renamed id is recoverable,
    # a guessed one is not.
    slug = social.get("brandSlug", "")
    for it in items:
        if slug and slug in (it.get("slug") or "") and it.get("type") == "Template Showcase":
            warnings.append(
                f"relatedPipelineItemIds {related} did not resolve; matched by slug to '{it['id']}'")
            return it["id"], it
    warnings.append(
        f"could not resolve any pipeline item id from {related} — row(s) will not join to SYNC_DATA")
    return (related[0] if related else f"store-template-{slug}"), None


def classify(key_name, rec):
    """Map one social-content asset record to a caption key."""
    platforms = [p.lower() for p in (rec.get("platform") or [])]
    angle = (rec.get("angle") or "").lower()
    if "linkedin" in platforms:
        return K_LINKEDIN
    if "instagram" in platforms:
        return K_INSTAGRAM
    if "x" in platforms or "twitter" in platforms:
        for needle, key in X_ANGLE_RULES:
            if needle in angle:
                return key
        return K_X_SHOWCASE
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("brand", help="brand slug, e.g. 'lumora' (reads {brand}-social-content.json)")
    ap.add_argument("--out", required=True, help="path to write the harvest record")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--offer-type", choices=["free", "paid", "auto"], default="auto",
                    help="'auto' (default): concept/demo brands are free-offer builds, "
                         "real named clients are paid. Override when auto guesses wrong.")
    args = ap.parse_args()

    root = os.path.abspath(args.project_root)
    sc_path = os.path.join(root, f"{args.brand}-social-content.json")
    if not os.path.exists(sc_path):
        sys.exit(f"[harvest-st] no social-content file at {sc_path}")

    with open(sc_path, "r", encoding="utf-8") as f:
        social = json.load(f)

    warnings = []
    items = load_sync_items(root)
    item_id, item = resolve_pipeline_item(social, items, warnings)

    # ── offer type ────────────────────────────────────────────────────────
    # A concept/demo brand exists to advertise the free sample-site offer.
    # A real named client build is paid work and must never carry the
    # "I'll build you one free" angle.
    if args.offer_type == "auto":
        offer_type = "free" if social.get("isConceptBrand") else "paid"
    else:
        offer_type = args.offer_type
    stream = "Store Template" if offer_type == "free" else "Store Template (Paid)"

    # ── captions + assets ─────────────────────────────────────────────────
    captions_full, images, seen = {}, [], set()
    for key_name, rec in (social.get("assets") or {}).items():
        ckey = classify(key_name, rec)
        if not ckey:
            warnings.append(f"{key_name}: no platform matched, skipped")
            continue
        text = (rec.get("caption") or "").strip()
        tags = rec.get("hashtags") or []
        if tags:
            text = f"{text}\n\n{' '.join(tags)}" if text else " ".join(tags)
        if not text:
            warnings.append(f"{key_name}: empty caption")
        if EM_DASH_RE.search(text):
            warnings.append(f"{key_name}: contains an em dash (banned project-wide)")
        if ckey in captions_full:
            warnings.append(
                f"{key_name}: duplicate caption key '{ckey}' — keeping the first, dropping this one")
        else:
            captions_full[ckey] = {"text": text, "source_tab": key_name}

        p = rec.get("assetPath") or ""
        if p and p not in seen:
            seen.add(p)
            if os.path.exists(os.path.join(root, p)):
                images.append(p)
            else:
                warnings.append(f"{key_name}: assetPath missing on disk -> {p}")

    # A paid build has no free-offer angle by definition. If one was written
    # anyway, drop it rather than let a paid client post advertise free work.
    if offer_type == "paid" and K_X_FREEOFFER in captions_full:
        captions_full[K_X_RESULTS] = captions_full.pop(K_X_FREEOFFER)
        warnings.append(
            "paid build: free-offer caption remapped to the results slot — REVIEW that its "
            "wording does not still offer a free site")
    if offer_type == "free" and K_X_FREEOFFER not in captions_full:
        warnings.append("free-offer build has no 'Free offer / Nigeria package' angle caption")

    folder = social.get("assetDir") or ""
    if item and item.get("folder"):
        cand = item["folder"]
        # Prefer a real companion page when one exists; otherwise keep the
        # directory (the File Linking rule is satisfied by the asset dir).
        if cand.endswith(".html") and os.path.exists(os.path.join(root, cand)):
            folder = cand

    record = {
        "pipeline_item_id": item_id,
        "brand": social.get("brand", ""),
        "slug": social.get("brandSlug", args.brand),
        "type": stream,
        "offer_type": offer_type,
        "is_concept_brand": bool(social.get("isConceptBrand")),
        "concept_notice": social.get("conceptNotice", ""),
        "template_id": social.get("templateId", ""),
        "content_system_folder": folder,
        "companion_html": "",
        "source_social_content": os.path.relpath(sc_path, root),
        "harvested_at": datetime.now(timezone.utc).isoformat(),
        "captions": {k: v["text"] for k, v in captions_full.items()},
        "captions_full": captions_full,
        "assets": {"images": images, "video": []},
        "warnings": warnings,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    print(f"[harvest-st] record written to {args.out}")
    print(f"[harvest-st] brand={record['brand']} stream={stream} offer_type={offer_type}")
    print(f"[harvest-st] pipeline_item_id={item_id} (resolved in SYNC_DATA: {item is not None})")
    print(f"[harvest-st] caption keys: {sorted(captions_full)}")
    print(f"[harvest-st] assets on disk: {len(images)}")
    for w in warnings:
        print(f"[harvest-st] WARNING: {w}")


if __name__ == "__main__":
    main()
