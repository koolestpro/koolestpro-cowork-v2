#!/usr/bin/env python3
"""
audit_mobile_strips.py — backstop sweep for the mandatory mobile-strip asset.

WHY THIS EXISTS (2026-09-02, Ridwan's instruction). `{slug}-mobile-strip.png`
became a required Template Showcase deliverable with its own X post, and his
concern was specifically that it would quietly go missing: "If it has not been
seen, we want to make sure this is not skipped." Instructions in scheduled-task
prompts are the first line of defence, but a run that goes long, hits a
renderer crash, or is simply written by a future model that skims the prompt
can still drop it. This script is the check that does not depend on anyone
remembering.

It reports three independent gaps, because the asset can go missing at three
different points in the chain:

  1. SOURCE   — a built replo-rebuilds page with no strip in its own
                presentation/ folder. Cheapest place to fix, and the Wednesday
                page-build task is supposed to create it here.
  2. PACKAGE  — a shipped Template Showcase / store-template package under
                outputs/templates/ with no strip file. This is the one that
                actually costs a post.
  3. QUEUE    — a Template Showcase / Store Template pipeline item in
                SYNC_DATA that has a distribution[] array but no row whose
                angle mentions the strip, or whose strip row has no asset
                path. This catches the case where the file exists but never
                reached the X calendar, which is the exact failure Ridwan
                described.

Anything predating the asset's introduction (--since, default 2026-09-02) is
reported separately as HISTORICAL BACKLOG rather than as a gap, and does not
affect the exit code. Without that split the weekly check would report the same
11 pre-existing packages forever and quickly get ignored, which is exactly how a
real gap would then slip past unnoticed.

Exit code is 1 when a NEW gap is found, so a caller can gate on it.

Usage:
    python3 audit_mobile_strips.py [--project-root DIR] [--json] [--since YYYY-MM-DD]
"""

import argparse
import glob
import json
import os
import re
import sys
from datetime import date, datetime

STRIP_GLOB = "*mobile-strip*"
# The date the asset became mandatory (CLAUDE.md CORRECTED v8).
INTRODUCED = date(2026, 9, 2)
DATE_IN_NAME = re.compile(r"_(\d{4})-?(\d{2})-?(\d{2})$")
SHOWCASE_TYPES = {"Template Showcase"}
SHOWCASE_STREAMS = {"Template Showcase", "Store Template", "Store Template (Paid)"}


def _has_strip(folder):
    return bool(glob.glob(os.path.join(folder, STRIP_GLOB)))


def _folder_date(path, fallback_file=None):
    """Date a package/page belongs to: parsed from a trailing _YYYY-MM-DD in the
    folder name where present, else the mtime of a representative file."""
    m = DATE_IN_NAME.search(os.path.basename(path.rstrip("/")))
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    probe = fallback_file or path
    if os.path.exists(probe):
        return datetime.fromtimestamp(os.path.getmtime(probe)).date()
    return date.min


def _split(items, since):
    """(new_gaps, historical_backlog) by each item's (label, date) pair."""
    new, old = [], []
    for label, d in items:
        (new if d >= since else old).append(label)
    return new, old


def audit_sources(root):
    """Built replo-rebuilds pages missing a strip in their presentation/ folder."""
    missing, ok = [], []
    for page in sorted(glob.glob(os.path.join(root, "replo-rebuilds/brands/*/pages/*"))):
        if not os.path.isfile(os.path.join(page, "index.html")):
            continue
        rel = os.path.relpath(page, root)
        if _has_strip(os.path.join(page, "presentation")):
            ok.append(rel)
        else:
            missing.append((rel, _folder_date(page, os.path.join(page, "index.html"))))
    return ok, missing


def audit_packages(root):
    """Shipped showcase packages under outputs/templates/ missing a strip."""
    missing, ok = [], []
    for pkg in sorted(glob.glob(os.path.join(root, "outputs/templates/*"))):
        if not os.path.isdir(pkg):
            continue
        rel = os.path.relpath(pkg, root)
        if _has_strip(pkg):
            ok.append(rel)
        else:
            missing.append((rel, _folder_date(pkg)))
    return ok, missing


def load_sync_items(root):
    path = os.path.join(root, "ridwan_content_system_updated.html")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        m = re.search(r'<script id="cowork-sync-data"[^>]*>(.*?)</script>', f.read(), re.S)
    if not m:
        return []
    try:
        return json.loads(m.group(1)).get("items", [])
    except json.JSONDecodeError:
        return []


def audit_queue(root):
    """Assembled showcase items whose distribution rows have no usable strip post."""
    missing, ok, unassembled = [], [], []
    for item in load_sync_items(root):
        if item.get("type") not in SHOWCASE_TYPES:
            continue
        rows = item.get("distribution") or []
        label = item.get("id", "?")
        if not rows:
            # Not assembled yet — the Monday task hasn't run for it. Not a gap.
            unassembled.append(label)
            continue
        strip_rows = [r for r in rows
                      if "mobile-strip" in json.dumps(r).lower()
                      or "at a glance" in (r.get("angle") or "").lower()]
        created = (item.get("created") or "")[:10]
        try:
            d = date.fromisoformat(created)
        except ValueError:
            d = date.min
        if not strip_rows:
            missing.append((f"{label}: no mobile-strip row in distribution[]", d))
        elif not any(r.get("asset_paths") or r.get("asset_urls") for r in strip_rows):
            missing.append((f"{label}: mobile-strip row exists but carries no asset path", d))
        else:
            ok.append(label)
    return ok, missing, unassembled


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--since", default=INTRODUCED.isoformat(),
                    help="anything older than this is historical backlog, not a gap")
    a = ap.parse_args()
    root = os.path.abspath(a.project_root)
    since = date.fromisoformat(a.since)

    src_ok, src_raw = audit_sources(root)
    pkg_ok, pkg_raw = audit_packages(root)
    q_ok, q_raw, q_pending = audit_queue(root)

    src_new, src_old = _split(src_raw, since)
    pkg_new, pkg_old = _split(pkg_raw, since)
    q_new, q_old = _split(q_raw, since)

    result = {
        "since": since.isoformat(),
        "sources":  {"ok": len(src_ok), "gaps": src_new, "backlog": src_old},
        "packages": {"ok": len(pkg_ok), "gaps": pkg_new, "backlog": pkg_old},
        "queue":    {"ok": len(q_ok), "gaps": q_new, "backlog": q_old,
                     "not_yet_assembled": q_pending},
    }

    if a.json:
        print(json.dumps(result, indent=2))
    else:
        for name, ok, new, old in (
            ("SOURCE PAGES", src_ok, src_new, src_old),
            ("PACKAGES", pkg_ok, pkg_new, pkg_old),
            ("QUEUE ROWS", q_ok, q_new, q_old),
        ):
            print(f"{name:<14} {len(ok)} ok, {len(new)} gap(s), {len(old)} historical")
            for p in new:
                print(f"  GAP       {p}")
            for p in old:
                print(f"  backlog   {p}")
        if q_pending:
            print(f"(not yet assembled, not a gap: {len(q_pending)})")

    total = len(src_new) + len(pkg_new) + len(q_new)
    backlog = len(src_old) + len(pkg_old) + len(q_old)
    print()
    if total:
        print(f"{total} NEW gap(s) since {since}. Build a missing strip with:\n"
              f"  python3 .ai-workflow/skills/page-presentation-kit/scripts/"
              f"build_mobile_strip.py \"<page>\" \"<out>/{{slug}}-mobile-strip.png\" --file")
    else:
        print(f"No new gaps since {since}.")
    if backlog:
        print(f"{backlog} historical item(s) predate the asset. Backfilling is optional "
              f"and Ridwan's call, not something to do unprompted — each one costs a "
              f"Playwright capture, and re-running populate_sheet.py on an already "
              f"assembled item would append a new X row to a week that has passed.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
