#!/usr/bin/env python3
"""Maps / Ad Library prospects -> the Outreach Google Sheet.

The weekly BrowserAct (Maps) and Ad Library tasks queue scored prospects in .ai-workflow/pending-push/*.json
for KoolestFlow. This script reads the same files and sends them to the Sheet too:
  - prospect with a website  -> Discovery tab (Discovery scores it, finds an email, dedupes against Leads)
  - prospect with an email but no website -> Leads tab as track Build (email 1 offers a free ad creative)
Skipped: brands already in the taken-brands ledger as "emailed" is not tracked there, so we only skip
what this script already sent (state/koolestflow_sent.json) and what the Sheet already holds (Api dedupes).

Run:  python outreach/scrapers/koolestflow_to_sheet.py [--dry-run]
"""
import argparse, glob, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import directory_scrape as ds  # reuses load_env, api_call, clean, is_store_domain

ROOT = ds.ROOT
SENT = ds.STATE / "koolestflow_sent.json"


def prospects():
    seen = set()
    for pat in ("pending-push/*.json", "pending-push/imported/*.json", "pending-push/failed/*.json"):
        for f in sorted(glob.glob(str(ROOT / ".ai-workflow" / pat))):
            try:
                data = json.load(open(f))
            except Exception:
                continue
            for p in (data.get("prospects") if isinstance(data, dict) else data) or []:
                pid = p.get("id") or p.get("brand_name")
                if pid and pid not in seen:
                    seen.add(pid)
                    yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    env = ds.load_env()
    sent = set(json.loads(SENT.read_text())) if SENT.exists() else set()

    disc_rows, lead_rows, ids = [], [], []
    for p in prospects():
        pid = p.get("id") or p.get("brand_name")
        if pid in sent:
            continue
        email = (p.get("email") or "").strip().lower()
        site = ds.clean(p.get("website_url") or "")
        country = p.get("country") or ""
        notes = " | ".join(x for x in [p.get("city"), p.get("signals"), p.get("source_query")] if x)[:500]
        if site and ds.is_store_domain(site):
            disc_rows.append({"domain": site, "source": "koolestflow " + (p.get("source") or ""), "brand": p.get("brand_name", ""),
                              "country": country, "niche": p.get("niche", ""), "emails": [email] if email else [],
                              "phone": p.get("whatsapp", ""), "signals": (p.get("signals") or "")[:300], "data": notes})
            ids.append(pid)
        elif email:
            lead_rows.append({"brand": p.get("brand_name", ""), "email": email, "country": country, "niche": p.get("niche", ""),
                              "source": "koolestflow " + (p.get("source") or ""), "track": "Build", "notes": notes})
            ids.append(pid)

    print(f"{len(disc_rows)} with a website (to Discovery), {len(lead_rows)} email-only (to Leads), {len(sent)} already sent before")
    if args.dry_run or not (disc_rows or lead_rows):
        print("dry run: nothing pushed" if args.dry_run else "nothing new")
        return
    added = merged = 0
    for i in range(0, len(disc_rows), 100):
        r = ds.api_call(env, "add_discovery_rows", {"rows": disc_rows[i:i + 100]})
        added += r.get("added", 0)
        merged += r.get("merged", 0)
    skipped = 0
    for f in lead_rows:
        try:
            ds.api_call(env, "add_lead", {"fields": f})
            added += 1
        except BaseException as e:  # duplicates come back as an error: fine
            skipped += 1
    SENT.write_text(json.dumps(sorted(sent | set(ids))))
    print(f"Sheet: {added} added, {merged} merged, {skipped} email-only already known or rejected")


if __name__ == "__main__":
    main()
