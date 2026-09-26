#!/usr/bin/env python3
"""refresh_contacts.py — re-enrich prospects that landed with no contact details.

Split into two modes so it fits the hybrid pipeline: the slow BrowserAct work
runs in the cloud, and the Mac only applies a small patch file to the local
KoolestFlow instance.

  # 1. In the cloud (or anywhere with BrowserAct access):
  python3 .ai-workflow/tools/refresh_contacts.py enrich \\
      --file .ai-workflow/pending-push/imported/2026-W36_lekki-fashion-boutique.json \\
      --out  .ai-workflow/pending-push/patches/2026-W36_lekki-contacts.json

  # 2. On Ridwan's Mac, with the local backend running:
  python3 .ai-workflow/tools/refresh_contacts.py apply \\
      --file .ai-workflow/pending-push/patches/2026-W36_lekki-contacts.json

Why this exists: on 2026-09-01 all 5 leads of a run reached KoolestFlow with no
Instagram, email or phone. Two causes, both since fixed in
browseract_koolestflow_bridge.parse_enrichment_row() — the parser read a field
name that does not exist in the Contact Finder output (`page_url` instead of
`current_page_url`), throwing away the real profile URL on every lead ever
enriched; and 3 of the 5 tasks had actually FAILED rather than found nothing.
This script re-runs those leads through the corrected parser.

`apply` only ever fills fields that are currently empty. It will not overwrite
a contact Ridwan has already edited by hand.
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import browseract_client as bc
import browseract_koolestflow_bridge as bridge
import koolestflow_client as kc

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CONTACT_FIELDS = ("website_url", "instagram_url", "email", "whatsapp")
POLL_DEADLINE = 420


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def has_contact(p):
    return any((p.get(f) or "").strip() for f in CONTACT_FIELDS)


def enrich(args):
    with open(args.file) as f:
        payload = json.load(f)
    prospects = payload.get("prospects") or []
    targets = [p for p in prospects if args.all or not has_contact(p)]
    if not targets:
        log("Every prospect already has a contact channel. Nothing to do.")
        return

    key = bc.load_api_key()
    wf = bridge.env("BROWSERACT_ENRICH_WORKFLOW_ID")

    # Resume support: BrowserAct's concurrent-task cap and the sandbox's call
    # ceiling both interrupt this routinely. Anything already in the out file is
    # kept and skipped, so re-running costs no repeat credits.
    patches = []
    if os.path.exists(args.out):
        patches = json.load(open(args.out)).get("patches") or []
    done_names = {p["brand_name"] for p in patches}
    targets = [p for p in targets if p.get("brand_name") not in done_names]
    if done_names:
        log(f"Resuming: {len(done_names)} already done, {len(targets)} to go.")
    log(f"Re-enriching {len(targets)} of {len(prospects)} prospect(s)...")

    def flush():
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as f:
            json.dump({"meta": {"source": os.path.basename(args.file),
                                "note": "Contact-only patch. apply mode fills empty fields on matching "
                                        "prospects in local KoolestFlow; it never overwrites existing values."},
                       "patches": patches}, f, indent=2, ensure_ascii=False)

    for p in targets:
        name = p.get("brand_name", "")
        query = f"{name} {p.get('city','')} {p.get('country','')}".strip()
        try:
            res = bc.run_task(key, wf, {"Company_name": query})
        except Exception as e:
            log(f"  {name}: could not start ({e})")
            continue
        tid = res.get("id")
        if not tid:
            log(f"  {name}: task did not start (likely the concurrent-task cap) - rerun later")
            continue
        log(f"  {name}: task {tid}")

        started, final = time.time(), None
        while time.time() - started < POLL_DEADLINE:
            st = bc.get_task_status(key, tid).get("status")
            if st in ("finished", "failed", "canceled"):
                final = bc.get_task(key, tid)
                break
            time.sleep(10)

        if not final or final.get("status") != "finished":
            log(f"  {name}: {final.get('status') if final else 'timed out'} - skipped")
            continue
        try:
            rows = json.loads((final.get("output") or {}).get("string") or "[]")
        except json.JSONDecodeError:
            rows = []
        if not rows:
            log(f"  {name}: workflow returned nothing (genuinely no online presence found)")
            continue

        e = bridge.parse_enrichment_row(rows[0])
        found = {k: v for k, v in e.items() if v and k in CONTACT_FIELDS}
        if not found:
            log(f"  {name}: no usable contact channel in the result")
            continue
        patches.append({"brand_name": name, "city": p.get("city", ""), **found})
        flush()   # checkpoint after every success, not at the end
        log(f"  {name}: " + ", ".join(f"{k}={v}" for k, v in found.items()))

    flush()
    log(f"\nWrote {len(patches)} patch record(s) -> {os.path.relpath(args.out, PROJECT_ROOT)}")


def apply_patch(args):
    with open(args.file) as f:
        patches = json.load(f).get("patches") or []
    if not patches:
        log("No patches in file.")
        return

    base = bridge.env("KOOLESTFLOW_LOCAL_BASE_URL", "http://127.0.0.1:8787")
    pw = bridge.env("KOOLESTFLOW_APP_PASSWORD")
    cookie = kc.koolestflow_login(base, pw)
    state = kc.koolestflow_get_state(base, cookie)
    prospects = state.get("prospects") or []
    log(f"Target: {base} ({len(prospects)} prospects)")

    by_key = {kc.dedupe_key(p): p for p in prospects}
    updated = 0
    for patch in patches:
        key = kc.dedupe_key({"brand_name": patch["brand_name"], "city": patch.get("city", "")})
        target = by_key.get(key)
        if not target:
            log(f"  no matching prospect for {patch['brand_name']} - skipped")
            continue
        changed = []
        for field in CONTACT_FIELDS:
            if patch.get(field) and not (target.get(field) or "").strip():
                target[field] = patch[field]
                changed.append(field)
        if changed:
            if target.get("next_action") == "Find contact channel manually" and \
                    (target.get("instagram_url") or target.get("whatsapp")):
                target["next_action"] = "Send first DM"
            updated += 1
            log(f"  {patch['brand_name']}: filled {', '.join(changed)}")
        else:
            log(f"  {patch['brand_name']}: already had these fields, left alone")

    if not updated:
        log("Nothing to update.")
        return
    kc.koolestflow_save_state(base, cookie, {"prospects": prospects, "runs": state.get("runs", [])})

    verify = kc.koolestflow_get_state(base, kc.koolestflow_login(base, pw))
    log(f"\nUpdated {updated} prospect(s). State now holds {len(verify.get('prospects') or [])}.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)

    e = sub.add_parser("enrich", help="re-run BrowserAct enrichment, write a patch file")
    e.add_argument("--file", required=True, help="a pending-push run file")
    e.add_argument("--out", required=True)
    e.add_argument("--all", action="store_true", help="re-enrich every prospect, not just contactless ones")

    a = sub.add_parser("apply", help="apply a patch file to local KoolestFlow")
    a.add_argument("--file", required=True)

    args = ap.parse_args()
    (enrich if args.mode == "enrich" else apply_patch)(args)


if __name__ == "__main__":
    main()
