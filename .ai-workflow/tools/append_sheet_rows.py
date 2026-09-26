#!/usr/bin/env python3
"""
append_sheet_rows.py — V2 distribution pipeline, the missing "push new rows
to the live Sheet" step (added 2026-08-02).

Ridwan is now working directly in the "Koolestpro Distribution Queue" Google
Sheet — flipping Draft rows to Ready by hand, and Make.com writes
Posted/posted_at back into it. That means the Sheet is the live, ahead-of-local
source of truth for any row he's already touched. This script must NEVER
overwrite or touch an existing row — it only ever APPENDS rows that aren't
in the Sheet yet (matched by post_id, column A), using a real Sheets API
append call (not a full-file replace like the old Drive-connector approach,
which had no way to avoid clobbering existing rows).

Auth: OAuth client (type "TVs and Limited Input devices"), authorized once
via the device-code flow, refresh token stored in .env. Ridwan is the sole
test user while the OAuth consent screen is in "Testing" publishing status —
IMPORTANT: refresh tokens issued to a Testing-status app expire after 7 days.
If this script starts failing with an "invalid_grant" error, that's almost
certainly why — either redo the device-flow authorization (see this project's
2026-08-02 build log for the exact steps), or switch the OAuth consent
screen's publishing status to "In production" (Google Cloud Console ->
"Google Auth Platform" -> Audience) for a long-lived refresh token that
doesn't expire on a 7-day clock. Production status does not require Google's
verification review for a single-user personal-use app like this one, though
re-authorizing after the switch will show a one-time "Google hasn't verified
this app" warning that's safe to click through (it's Ridwan's own app).

Usage:
    python3 append_sheet_rows.py [--project-root DIR] [--queue FILE] [--dry-run]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse

SHEET_ID = "1I5SrLnwAfVV5260Y_nAytio49gh-NKmJeJdFXH3nqzg"
SHEET_TAB = "Untitled"  # confirmed live 2026-07-22 per populate_sheet.py's COLUMNS comment
COLUMNS = [
    "post_id", "pipeline_item_id", "stream", "platform", "scheduled_date",
    "scheduled_time_local", "intended_et", "asset_paths", "caption",
    "caption_source_tab", "status", "qa_status", "posted_at",
    "content_system_folder", "caption_json", "asset_urls",
]


def find_root(start):
    d = os.path.abspath(start)
    while d != "/" and not os.path.exists(os.path.join(d, "CLAUDE.md")):
        d = os.path.dirname(d)
    return d if os.path.exists(os.path.join(d, "CLAUDE.md")) else os.path.abspath(start)


def load_env(root):
    env = {}
    path = os.path.join(root, ".env")
    if not os.path.exists(path):
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def http_json(url, data=None, headers=None, method=None):
    body = None
    hdrs = dict(headers or {})
    if data is not None:
        if isinstance(data, dict) and hdrs.get("Content-Type", "").startswith("application/x-www-form-urlencoded"):
            body = urllib.parse.urlencode(data).encode()
        else:
            body = json.dumps(data).encode()
            hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method or ("POST" if data is not None else "GET"))
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        raise RuntimeError(f"HTTP {e.code} calling {url}: {err_body}") from None


def get_access_token(env):
    missing = [k for k in ("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_OAUTH_REFRESH_TOKEN") if k not in env]
    if missing:
        sys.exit(f"missing from .env: {missing} — run the device-flow authorization first")
    resp = http_json(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": env["GOOGLE_OAUTH_CLIENT_ID"],
            "client_secret": env["GOOGLE_OAUTH_CLIENT_SECRET"],
            "refresh_token": env["GOOGLE_OAUTH_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if "access_token" not in resp:
        raise RuntimeError(f"token refresh failed: {resp}")
    return resp["access_token"]


def get_existing_post_ids(token):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{urllib.parse.quote(SHEET_TAB)}!A2:A"
    resp = http_json(url, headers={"Authorization": f"Bearer {token}"}, method="GET")
    values = resp.get("values", [])
    return {row[0] for row in values if row}


def append_rows(token, rows):
    url = (f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/"
           f"{urllib.parse.quote(SHEET_TAB)}!A1:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS")
    body = {"values": rows}
    return http_json(url, data=body, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="POST")


def main():
    ap = argparse.ArgumentParser(description="Append brand-new local queue rows to the live Google Sheet — never touches existing rows.")
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--queue", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(args.project_root) if args.project_root else find_root(os.getcwd())
    qpath = args.queue or os.path.join(root, "outputs", "distribution-queue", "queue.json")
    with open(qpath, "r", encoding="utf-8") as f:
        queue = json.load(f)

    env = load_env(root)
    token = get_access_token(env)
    existing = get_existing_post_ids(token)

    new_rows = [r for r in queue["rows"] if r["post_id"] not in existing]
    print(f"[append-sheet] local rows={len(queue['rows'])} already-in-sheet={len(existing)} new-to-append={len(new_rows)}")

    if not new_rows:
        print("[append-sheet] nothing new — sheet already has everything local does. Nothing sent.")
        return

    payload = [[r.get(c, "") for c in COLUMNS] for r in new_rows]

    if args.dry_run:
        print("[append-sheet] DRY RUN — would append:")
        for r in new_rows:
            print(f"  + {r['post_id']} ({r['platform']}, {r['scheduled_date']})")
        return

    result = append_rows(token, payload)
    updated_range = result.get("updates", {}).get("updatedRange", "?")
    print(f"[append-sheet] appended {len(new_rows)} row(s) at {updated_range}")
    for r in new_rows:
        print(f"  + {r['post_id']} ({r['platform']}, {r['scheduled_date']})")


if __name__ == "__main__":
    main()
