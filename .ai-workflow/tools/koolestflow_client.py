#!/usr/bin/env python3
"""
koolestflow_client.py — shared push/dedupe logic for getting prospects
into KoolestFlow (cold-dm-app), factored out of
browseract_koolestflow_bridge.py so any future lead source (Ad Library,
BrowserAct, or something else later) can reuse the same, tested push
path instead of re-implementing it. See project memory
project_koolestflow_app.md for the API/schema this mirrors.

Taken-brands ledger (added 2026-08-26, Ridwan's instruction): every
brand ever pushed to KoolestFlow through this client, from ANY source,
must be documented locally and never sent again — even if it's later
deleted/archived from KoolestFlow itself, or if KoolestFlow's own state
ever gets reset. The ledger at .ai-workflow/taken-brands-ledger.json is
the durable record; live KoolestFlow state is still checked too (belt
and suspenders), but the ledger is what survives independent of the
app's own data.
"""

import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DEFAULT_LEDGER_PATH = os.path.join(PROJECT_ROOT, ".ai-workflow", "taken-brands-ledger.json")


def koolestflow_login(base_url, password):
    req = urllib.request.Request(
        f"{base_url}/api/auth/login",
        data=json.dumps({"password": password}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        cookie = resp.headers.get("Set-Cookie", "").split(";")[0]
        return cookie


def koolestflow_get_state(base_url, cookie):
    req = urllib.request.Request(f"{base_url}/api/state", headers={"Cookie": cookie})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def koolestflow_save_state(base_url, cookie, state):
    req = urllib.request.Request(
        f"{base_url}/api/state",
        data=json.dumps(state).encode(),
        headers={"Content-Type": "application/json", "Cookie": cookie},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def dedupe_key(prospect):
    return (re.sub(r"[^a-z0-9]+", "", prospect.get("brand_name", "").lower()),
            re.sub(r"[^a-z0-9]+", "", prospect.get("city", "").lower()))


def _ledger_key_str(key_tuple):
    return "|".join(key_tuple)


def load_ledger(path=DEFAULT_LEDGER_PATH):
    if not os.path.exists(path):
        return {
            "meta": {
                "description": "Every brand ever pushed to KoolestFlow via koolestflow_client.py, "
                                "from any discovery source (Ad Library, BrowserAct/Maps, etc). "
                                "Checked before every push so a brand is never sent to KoolestFlow "
                                "twice, even across sources or if it's later removed from KoolestFlow itself.",
                "dedupeKeyFormula": "lowercased brand_name + city, non-alphanumeric stripped, joined with '|'",
            },
            "brands": {},
        }
    with open(path) as f:
        return json.load(f)


def save_ledger(ledger, path=DEFAULT_LEDGER_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
        f.write("\n")


def push_to_koolestflow(base_url, password, new_prospects, dry_run=False, ledger_path=DEFAULT_LEDGER_PATH):
    """Always GETs current state first, dedupes on brand_name+city against
    BOTH live KoolestFlow state and the local taken-brands ledger, POSTs the
    full merged list back — KoolestFlow's save_state REPLACES the whole
    prospects table, never post just the new batch alone.

    Returns a summary dict: {"added": int, "added_brands": [...], "skipped_brands": [...], "total": int}
    so callers can print an exact-brand-name report rather than just a count.
    """
    ledger = load_ledger(ledger_path)
    ledger_keys = set(ledger.get("brands", {}).keys())

    if dry_run:
        print(json.dumps(new_prospects, indent=2))
        print(f"\n[dry run] {len(new_prospects)} prospect(s) would be pushed. No API call made, ledger not updated.", file=sys.stderr)
        return {"added": 0, "added_brands": [], "skipped_brands": [p.get("brand_name", "") for p in new_prospects], "total": None}

    cookie = koolestflow_login(base_url, password)
    state = koolestflow_get_state(base_url, cookie)
    existing = state.get("prospects", [])
    existing_keys = {dedupe_key(p) for p in existing}

    added = 0
    added_brands = []
    skipped_brands = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    for p in new_prospects:
        key = dedupe_key(p)
        key_str = _ledger_key_str(key)
        if key in existing_keys or key_str in ledger_keys:
            reason = "already in KoolestFlow" if key in existing_keys else "already taken (ledger)"
            print(f"  skip ({reason}): {p.get('brand_name', '(unnamed)')}", file=sys.stderr)
            skipped_brands.append(p.get("brand_name", "(unnamed)"))
            continue
        existing.append(p)
        existing_keys.add(key)
        ledger_keys.add(key_str)
        ledger.setdefault("brands", {})[key_str] = {
            "brandName": p.get("brand_name", ""),
            "city": p.get("city", ""),
            "country": p.get("country", ""),
            "websiteUrl": p.get("website_url", ""),
            "source": p.get("source", ""),
            "sourceQuery": p.get("source_query", ""),
            "koolestflowId": p.get("id", ""),
            "takenAt": now,
        }
        added += 1
        added_brands.append(p.get("brand_name", "(unnamed)"))

    result = koolestflow_save_state(base_url, cookie, {"prospects": existing, "runs": state.get("runs", [])})

    # Verify the write actually stuck before claiming success or touching the
    # ledger. The Vercel deployment accepts the POST, echoes back a plausible
    # count, and then serves an empty list on the next request because its
    # filesystem is ephemeral (confirmed 2026-09-01, see CLAUDE.md). Trusting
    # the POST response cost a full run of leads and marked them all "taken".
    # NOTE: this check catches the failure but cannot guarantee it. If the same
    # warm lambda serves both the POST and this read, it still holds the data in
    # its own /tmp and answers correctly; a later cold instance returns nothing.
    # Verified 2026-09-01: an immediate read-back said 5, a read minutes later
    # said 0. So a pass here means "not obviously broken", not "durable". The
    # only real fix is a backend that persists - hence the pending-push queue.
    persisted = None
    try:
        time.sleep(3)
        verify_cookie = koolestflow_login(base_url, password)
        persisted = len(koolestflow_get_state(base_url, verify_cookie).get("prospects") or [])
    except Exception as e:
        print(f"  WARNING: could not verify the push ({e}). Treating it as unconfirmed.", file=sys.stderr)

    if persisted is not None and persisted < len(existing):
        print(f"\nPUSH DID NOT PERSIST: posted {len(existing)} prospect(s), "
              f"but reading the state back returns {persisted}.", file=sys.stderr)
        print("  This backend is discarding writes. The ledger was NOT updated, so these "
              "brands stay available for a later push.", file=sys.stderr)
        return {"added": 0, "added_brands": [], "skipped_brands": skipped_brands,
                "total": persisted, "persisted": False}

    save_ledger(ledger, ledger_path)

    print(f"Pushed {added} new prospect(s) to KoolestFlow. Total prospects now: {result.get('prospects')}.")
    if added_brands:
        print("  Brands taken this run:")
        for name in added_brands:
            print(f"    - {name}")
    if skipped_brands:
        print("  Brands skipped (already taken):")
        for name in skipped_brands:
            print(f"    - {name}")

    return {"added": added, "added_brands": added_brands, "skipped_brands": skipped_brands, "total": result.get("prospects")}
