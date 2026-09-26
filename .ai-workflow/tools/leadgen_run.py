#!/usr/bin/env python3
"""leadgen_run.py — cloud-side half of the hybrid lead-gen pipeline.

Runs BrowserAct discovery + enrichment + scoring, then writes the scored
prospects to .ai-workflow/pending-push/{week}_{slug}.json. It deliberately
does NOT push to KoolestFlow: the Vercel deployment does not persist writes
(see CLAUDE.md, 2026-09-01), and the local instance is unreachable from a
cloud sandbox. import_pending_push.sh on Ridwan's Mac completes the loop.

Two problems this solves that the monolithic bridge could not:

  1. Resumability. A cloud shell call is capped near 170s and background
     processes do not survive between calls, while one enrichment can take
     several minutes. State is checkpointed to .leadgen-state.json after
     every step, so each call resumes exactly where the last one stopped.
     Call it repeatedly until it prints RUN_COMPLETE.

  2. Credit waste. Brands already in the taken-brands ledger are skipped
     before enrichment is started, not after.

Usage:
  python3 .ai-workflow/tools/leadgen_run.py --budget 150     # run/resume
  python3 .ai-workflow/tools/leadgen_run.py --status         # inspect, no API calls
  python3 .ai-workflow/tools/leadgen_run.py --reset          # discard in-flight state
"""
import argparse
import csv
import datetime
import io
import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import browseract_client as bc
import browseract_koolestflow_bridge as bridge
import koolestflow_client as kc

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
AI = os.path.join(PROJECT_ROOT, ".ai-workflow")
STATE_PATH = os.path.join(AI, ".leadgen-state.json")
ROTATION_PATH = os.path.join(AI, "browseract_rotation.json")
LOG_PATH = os.path.join(AI, "browseract-weekly-log.json")
PENDING_DIR = os.path.join(AI, "pending-push")

# A stalled BrowserAct task is abandoned past this many seconds. The API will
# happily leave a task "running" far longer than its own docs suggest, and
# holding the slot also trips the account's concurrent-task cap.
ENRICH_DEADLINE = 420


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def iso_week():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%G-W%V")


def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def start_run():
    """Pick the current rotation slot and kick off discovery."""
    rot = read_json(ROTATION_PATH)
    idx = rot["meta"].get("currentIndex", 0)
    limit = rot["meta"].get("limitPerRun", 5)
    slot = rot["areas"][idx]

    key = bc.load_api_key()
    wf = bridge.env("BROWSERACT_LEADGEN_WORKFLOW_ID")
    if not (key and wf):
        raise SystemExit("BROWSERACT_API_KEY or BROWSERACT_LEADGEN_WORKFLOW_ID missing from .env")

    log(f"Stage 1: discovering up to {limit} businesses in '{slot['area']}' for '{slot['keyword']}'...")
    res = bc.run_task(key, wf, {
        "URL": "https://www.google.com/maps",
        "Area": slot["area"], "Keyword": slot["keyword"], "datalimit": str(limit),
    })
    task_id = res.get("id")
    if not task_id:
        raise SystemExit("discovery task did not start (no id returned)")
    log(f"  discovery task {task_id} started")

    state = {
        "week": iso_week(), "startedAt": now_iso(), "rotationIndex": idx,
        "discoveryTaskId": task_id, "rows": None, "cursor": 0,
        "prospects": [], "skipped": [], "pending": None, "finalized": False,
        "sourceQuery": f"Area={slot['area']}; Keyword={slot['keyword']}",
        **{k: slot[k] for k in ("area", "keyword", "niche", "country", "city", "audienceType")},
    }
    write_json(STATE_PATH, state)
    return state


def collect_discovery(state, key):
    final = bc.get_task(key, state["discoveryTaskId"])
    status = final.get("status")
    if status not in ("finished", "failed", "canceled"):
        log(f"  discovery still {status}...")
        return False
    rows = []
    files = (final.get("output") or {}).get("files") or []
    if files:
        with urllib.request.urlopen(files[0], timeout=60) as r:
            rows = list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig"))))
    state["rows"] = rows
    write_json(STATE_PATH, state)
    log(f"Stage 1 complete: {len(rows)} businesses found")
    return True


def empty_enrichment():
    return {k: "" for k in ("website_url", "instagram_url", "facebook_url", "linkedin_url",
                            "tiktok_url", "x_url", "youtube_url", "email", "phone", "whatsapp")}


def parse_enrichment(task_result):
    """Returns (enrichment, outcome) where outcome is one of:
    'ok' | 'empty' | 'failed'.

    The distinction matters and used to be collapsed. On 2026-09-01, 3 of 5
    enrichment tasks came back status='failed' and were silently scored as
    "no contact details found" — indistinguishable, in the output, from a
    business that genuinely has no online presence. A failed task is a
    retryable infrastructure event; an empty result is a real finding.
    """
    if not task_result:
        return empty_enrichment(), "failed"
    if task_result.get("status") != "finished":
        return empty_enrichment(), "failed"
    try:
        rows = json.loads((task_result.get("output") or {}).get("string") or "[]")
    except json.JSONDecodeError:
        return empty_enrichment(), "failed"
    if not rows:
        return empty_enrichment(), "empty"
    return bridge.parse_enrichment_row(rows[0]), "ok"


def finalize(state):
    """Write the pending-push file, advance rotation, append the weekly log."""
    os.makedirs(PENDING_DIR, exist_ok=True)
    slug = f"{slugify(state['area'])}-{slugify(state['keyword'])}"
    out_path = os.path.join(PENDING_DIR, f"{state['week']}_{slug}.json")

    stalled = [p["brand_name"] for p in state["prospects"] if p.get("_enrichmentIncomplete")]
    for p in state["prospects"]:
        p.pop("_enrichmentIncomplete", None)

    write_json(out_path, {
        "meta": {
            "week": state["week"], "ranAt": now_iso(),
            "area": state["area"], "keyword": state["keyword"], "niche": state["niche"],
            "country": state["country"], "city": state["city"],
            "sourceQuery": state["sourceQuery"],
            "ledgerAlreadyRecorded": False,
            "enrichmentIncomplete": stalled,
            "note": "Scored in the cloud, not yet pushed. import_pending_push.sh on the Mac pushes this into the local KoolestFlow instance and records the brands in the taken-brands ledger.",
        },
        "prospects": state["prospects"],
    })
    log(f"Wrote {len(state['prospects'])} prospect(s) -> {os.path.relpath(out_path, PROJECT_ROOT)}")

    rot = read_json(ROTATION_PATH)
    rot["meta"]["currentIndex"] = (state["rotationIndex"] + 1) % len(rot["areas"])
    rot["meta"]["updatedAt"] = now_iso()
    write_json(ROTATION_PATH, rot)

    entry = {
        "week": state["week"], "ranAt": now_iso(),
        "areaUsed": state["area"], "keywordUsed": state["keyword"],
        "leadsScored": len(state["prospects"]), "leadsPushed": 0,
        "status": "queued",
        "pendingPushFile": os.path.relpath(out_path, PROJECT_ROOT),
        "note": (f"{len(state['prospects'])} scored and queued for local import. "
                 f"{len(state['skipped'])} skipped as already taken. "
                 + (f"Enrichment stalled for: {', '.join(stalled)}. " if stalled else "")
                 + "leadsPushed stays 0 until import_pending_push.sh confirms the local push."),
    }
    lg = read_json(LOG_PATH, {"runs": []})
    lg.setdefault("runs", []).append(entry)
    write_json(LOG_PATH, lg)

    state["finalized"] = True
    write_json(STATE_PATH, state)
    log(f"Rotation advanced to index {rot['meta']['currentIndex']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--budget", type=float, default=150.0, help="seconds of work before checkpointing and exiting")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--reset", action="store_true")
    args = ap.parse_args()

    if args.reset:
        if os.path.exists(STATE_PATH):
            os.remove(STATE_PATH)
        log("state cleared")
        return

    state = read_json(STATE_PATH)

    if args.status:
        if not state:
            log("no run in flight")
        else:
            rows = state.get("rows")
            log(f"week={state['week']} area={state['area']} finalized={state['finalized']} "
                f"progress={state['cursor']}/{len(rows) if rows is not None else '?'} "
                f"scored={len(state['prospects'])} skipped={len(state['skipped'])}")
        return

    started = time.time()

    def left():
        return args.budget - (time.time() - started)

    if not state or state.get("finalized"):
        if state and state.get("finalized") and state.get("week") == iso_week():
            log("RUN_COMPLETE (already finalized for this week)")
            return
        state = start_run()

    key = bc.load_api_key()
    enrich_wf = bridge.env("BROWSERACT_ENRICH_WORKFLOW_ID")
    ledger_keys = set(kc.load_ledger().get("brands", {}).keys())

    while state["rows"] is None:
        if collect_discovery(state, key):
            break
        if left() < 20:
            log("RUN_PAUSED (waiting on discovery)")
            return
        time.sleep(15)

    rows = state["rows"]

    while state["cursor"] < len(rows) and left() > 35:
        i = state["cursor"]
        row = rows[i]
        name = bridge._map_row_name(row)
        if not name:
            state["cursor"] = i + 1
            write_json(STATE_PATH, state)
            continue

        # Skip brands already taken, before spending an enrichment credit.
        probe = {"brand_name": name, "city": state["city"]}
        if kc._ledger_key_str(kc.dedupe_key(probe)) in ledger_keys:
            log(f"skip (already taken): {name}")
            state["skipped"].append(name)
            state["cursor"] = i + 1
            write_json(STATE_PATH, state)
            continue

        pend = state.get("pending") or {}
        if pend.get("index") != i:
            query = f"{name} {state['city']} {state['country']}".strip()
            try:
                res = bc.run_task(key, enrich_wf, {"Company_name": query})
            except Exception as e:
                log(f"could not start enrichment for '{name}': {e}")
                write_json(STATE_PATH, state)
                log("RUN_PAUSED")
                return
            if not res.get("id"):
                # Usually the concurrent-task cap; abandoned tasks hold slots.
                log(f"enrichment did not start for '{name}' (likely concurrency cap) - will retry next call")
                write_json(STATE_PATH, state)
                log("RUN_PAUSED")
                return
            pend = {"index": i, "task_id": res["id"], "started_at": time.time()}
            state["pending"] = pend
            write_json(STATE_PATH, state)
            log(f"enrich started for '{name}' -> {pend['task_id']}")

        done, gave_up = None, False
        while left() > 25:
            st = bc.get_task_status(key, pend["task_id"]).get("status")
            if st in ("finished", "failed", "canceled"):
                done = bc.get_task(key, pend["task_id"])
                break
            if time.time() - pend.get("started_at", time.time()) > ENRICH_DEADLINE:
                gave_up = True
                log(f"enrichment for '{name}' exceeded {ENRICH_DEADLINE}s (status={st}) - continuing without it")
                break
            time.sleep(10)
        if done is None and not gave_up:
            write_json(STATE_PATH, state)
            log("RUN_PAUSED")
            return

        enrichment, outcome = parse_enrichment(done)

        # Retry a failed task once before giving up on the lead. BrowserAct
        # fails tasks intermittently; on 2026-09-01 three leads in one run were
        # written off as "no contacts" purely because of this.
        attempts = pend.get("attempts", 1)
        if outcome == "failed" and not gave_up and attempts < 2 and left() > 40:
            log(f"enrichment FAILED for '{name}' - retrying once")
            try:
                res = bc.run_task(key, enrich_wf, {"Company_name": f"{name} {state['city']} {state['country']}".strip()})
            except Exception as e:
                res = {}
            if res.get("id"):
                state["pending"] = {"index": i, "task_id": res["id"],
                                    "started_at": time.time(), "attempts": attempts + 1}
                write_json(STATE_PATH, state)
                continue  # re-enter the loop and wait on the retry
            log(f"  retry could not be started for '{name}'")

        prospect = bridge.build_prospect(row, enrichment, state["niche"], state["country"],
                                         state["city"], state["audienceType"], state["sourceQuery"], None)
        if gave_up or outcome == "failed":
            # Flagged so the run summary can say which classifications are
            # unverified — a lead with no contact data because enrichment broke
            # must never look like a lead that genuinely has no presence.
            prospect["_enrichmentIncomplete"] = True
            prospect["notes"] += (" | WARNING: contact enrichment did not complete for this lead, so the "
                                  "absence of a website/Instagram here is unverified. Check by hand before "
                                  "treating it as a no-website prospect.")
        state["prospects"].append(prospect)
        state["cursor"] = i + 1
        state["pending"] = None
        write_json(STATE_PATH, state)
        log(f"scored {name}: fit={prospect['fit_score']} {prospect['status']}")

    if state["cursor"] < len(rows):
        log(f"RUN_PAUSED ({state['cursor']}/{len(rows)} done)")
        return

    finalize(state)
    log("RUN_COMPLETE")


if __name__ == "__main__":
    main()
