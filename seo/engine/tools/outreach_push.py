#!/usr/bin/env python3
"""Hand this week's link-building prospects to the project's outreach system.

Reads <run>/outreach.json (written by prompts/08-outreach.md):
  [{"domain", "url", "brand", "contact_name", "email", "type", "target_page", "cluster", "pitch_angle",
    "niche", "country", "what_they_sell", "audience", "signal",
    "emails": [{"subject", "body"}, {"subject", "body"}]}]     # step 1 pitch, step 2 follow-up

project.json "outreach.mode":
  "csv"           (default, manual sending) write <run>/outreach-import.csv (one row per email step).
                  You send the pitches yourself from outreach.md until automation is set up.
  "sheet"         (automated) append to the project's outreach Sheet (Leads / Profiles / Sequence tabs,
                  sender in seo/engine/outreach-sender/). Rows go in unapproved
                  (approved=FALSE, email_status=unchecked), so nothing sends until a person ticks them.
                  Needs outreach.sheet_id + the Google sign-in with the spreadsheets scope (gsc_pull.py auth).
  "gmail-drafts"  no-op here: the agent creates Gmail drafts with its Gmail connector instead.
Every mode appends to seo/project/outreach-log.csv and skips domains contacted in the last 90 days.

Usage: python3 seo/engine/tools/outreach_push.py --run seo/project/runs/2026-10-06 [--dry-run]
"""
import argparse
import csv
import json
import sys
import urllib.parse
from datetime import date, datetime, timedelta
from pathlib import Path

from _common import google_access_token, http, load_project, project_dir

LOG_FIELDS = ["date", "prospect_domain", "prospect_url", "type", "contact", "target_page", "cluster",
              "pitch_angle", "status", "gmail_draft_id", "live_link_url", "anchor_text", "notes"]


def recent_domains(days=90):
    log = project_dir() / "outreach-log.csv"
    if not log.exists():
        return set()
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    with log.open() as f:
        return {r["prospect_domain"].lower() for r in csv.DictReader(f) if r.get("date", "") >= cutoff}


def validate(p):
    problems = []
    for k in ("domain", "url", "email", "target_page", "emails"):
        if not p.get(k):
            problems.append(f"{p.get('domain', '?')}: missing {k}")
    blob = json.dumps(p, ensure_ascii=False)
    if "—" in blob or "&mdash;" in blob:
        problems.append(f"{p.get('domain')}: em dash in pitch")
    for e in p.get("emails", []):
        if len(e.get("body", "").split()) > 150:
            problems.append(f"{p.get('domain')}: an email is over 150 words")
    return problems


def dom(url):
    return urllib.parse.urlparse(url if "//" in url else "//" + url).netloc.lower().removeprefix("www.")


class Sheet:
    def __init__(self, sheet_id):
        self.base = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/"
        self.h = {"Authorization": f"Bearer {google_access_token()}"}

    def get(self, rng):
        status, body = http(self.base + urllib.parse.quote(rng), headers=self.h)
        if status != 200:
            sys.exit(f"Sheets read {rng} failed ({status}): {body[:300]}")
        return json.loads(body).get("values", [])

    def append(self, tab, rows):
        url = self.base + urllib.parse.quote(f"{tab}!A1") + ":append?valueInputOption=RAW&insertDataOption=INSERT_ROWS"
        status, body = http(url, data={"values": rows}, headers=self.h, method="POST")
        if status != 200:
            sys.exit(f"Sheets append {tab} failed ({status}): {body[:300]}")


def to_sheet(prospects, cfg, dry):
    oc = cfg.get("outreach", {})
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    track = oc.get("track", "seo-links")
    rows = {"Leads": [], "Profiles": [], "Sequence": []}
    for p in prospects:
        lead_id = f"seo-{date.today():%Y%m%d}-{p['domain'].replace('.', '-')}"
        rows["Leads"].append({
            "lead_id": lead_id, "brand": p.get("brand") or p["domain"], "website": p["url"],
            "contact_name": p.get("contact_name", ""), "email": p["email"], "email_status": "unchecked",
            "country": p.get("country", ""), "niche": p.get("niche", ""), "source": "seo-engine",
            "track": track, "play": p.get("type", ""), "stage": "New", "approved": "FALSE",
            "notes": f"Link target: {p['target_page']} | angle: {p.get('pitch_angle', '')}", "created_at": now})
        rows["Profiles"].append({"lead_id": lead_id, "what_they_sell": p.get("what_they_sell", ""),
                                 "audience": p.get("audience", ""), "signal": p.get("signal", p["url"]),
                                 "site_notes": p.get("pitch_angle", ""), "updated_at": now})
        for i, e in enumerate(p["emails"], 1):
            rows["Sequence"].append({"lead_id": lead_id, "step": i, "subject": e.get("subject", ""),
                                     "body": e["body"], "status": "Draft", "sent_at": ""})
    if dry:
        print(json.dumps(rows, indent=1, ensure_ascii=False))
        return
    if not oc.get("sheet_id"):
        sys.exit("project.json outreach.sheet_id is empty")
    sh = Sheet(oc["sheet_id"])
    lead_header = sh.get("Leads!1:1")[0]
    col = chr(ord("A") + lead_header.index("website"))
    existing = {dom(r[0]) for r in sh.get(f"Leads!{col}2:{col}") if r}
    kept_ids = set()
    for tab, dict_rows in rows.items():
        header = lead_header if tab == "Leads" else sh.get(f"{tab}!1:1")[0]
        keep = [r for r in dict_rows if tab != "Leads" or dom(r["website"]) not in existing]
        if tab == "Leads":
            kept_ids = {r["lead_id"] for r in keep}
        else:
            keep = [r for r in keep if r["lead_id"] in kept_ids]
        if keep:
            sh.append(tab, [[str(r.get(col, "")) for col in header] for r in keep])
    print(f"Sheet: added {len(kept_ids)} lead(s) as track={track}, unapproved. Tick approved + set email_status=valid to send.")


def to_csv(prospects, run):
    out = run / "outreach-import.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["domain", "url", "email", "contact_name", "type", "target_page", "step", "subject", "body"])
        for p in prospects:
            for i, e in enumerate(p["emails"], 1):
                w.writerow([p["domain"], p["url"], p["email"], p.get("contact_name", ""), p.get("type", ""),
                            p["target_page"], i, e.get("subject", ""), e["body"]])
    print(f"CSV: {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cfg = load_project()
    run = Path(args.run)
    prospects = json.loads((run / "outreach.json").read_text())

    seen = recent_domains()
    fresh = [p for p in prospects if p.get("domain", "").lower() not in seen]
    skipped = len(prospects) - len(fresh)
    problems = [x for p in fresh for x in validate(p)]
    if problems:
        sys.exit("QA gate failed:\n  - " + "\n  - ".join(problems))

    mode = cfg.get("outreach", {}).get("mode", "csv")
    if mode == "sheet":
        to_sheet(fresh, cfg, args.dry_run)
    elif mode == "csv":
        if args.dry_run:
            print(f"CSV (dry run): would write {sum(len(p['emails']) for p in fresh)} email row(s) for {len(fresh)} prospect(s)")
        else:
            to_csv(fresh, run)
    else:
        print("mode gmail-drafts: create the drafts with the Gmail connector, then log them.")

    if not args.dry_run:
        log = project_dir() / "outreach-log.csv"
        new = not log.exists()
        with log.open("a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=LOG_FIELDS)
            if new:
                w.writeheader()
            for p in fresh:
                w.writerow({"date": date.today().isoformat(), "prospect_domain": p["domain"], "prospect_url": p["url"],
                            "type": p.get("type", ""), "contact": p["email"], "target_page": p["target_page"],
                            "cluster": p.get("cluster", ""), "pitch_angle": p.get("pitch_angle", ""),
                            "status": "queued" if mode != "gmail-drafts" else "drafted"})
    if skipped:
        print(f"Skipped {skipped} domain(s) contacted in the last 90 days.")


if __name__ == "__main__":
    main()
