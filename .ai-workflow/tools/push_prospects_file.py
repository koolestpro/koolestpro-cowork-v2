#!/usr/bin/env python3
"""push_prospects_file.py — push an already-scored prospect file into KoolestFlow.

Why this exists (2026-09-01): the weekly BrowserAct run pushes to
KOOLESTFLOW_BASE_URL, which points at the Vercel deployment. That deployment
accepts POST /api/state and reports success, but a follow-up GET /api/state
returns an empty prospect list, so the leads never actually land. Ridwan's real
prospect data lives on the local instance (KOOLESTFLOW_LOCAL_BASE_URL).

Re-running the whole bridge to recover those leads would spend BrowserAct
credits again on discovery + enrichment. This script skips straight to the push
stage using the scored prospects already saved under .ai-workflow/pending-push/.

Usage:
  # push a saved run into the LOCAL instance (start KoolestFlow's backend first)
  python3 .ai-workflow/tools/push_prospects_file.py \\
      .ai-workflow/pending-push/2026-W36_lekki-fashion-boutique.json --ignore-ledger

  # target the Vercel deployment instead
  python3 .ai-workflow/tools/push_prospects_file.py <file> --remote

--ignore-ledger is needed for any run that was already recorded as "taken" by a
push that did not actually persist. It leaves the ledger history intact and only
bypasses the skip check for this one push.
"""
import argparse
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import koolestflow_client as kc

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def env(name, default=None):
    val = os.environ.get(name)
    if val:
        return val
    env_path = os.path.join(PROJECT_ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{name}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return default


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", help="JSON file with a top-level 'prospects' list")
    p.add_argument("--remote", action="store_true",
                   help="Push to KOOLESTFLOW_BASE_URL (Vercel) instead of the local instance")
    p.add_argument("--ignore-ledger", action="store_true",
                   help="Bypass the taken-brands ledger skip check for this push")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    with open(args.file) as f:
        payload = json.load(f)
    prospects = payload.get("prospects") if isinstance(payload, dict) else payload
    if not prospects:
        print("No prospects in file.", file=sys.stderr)
        sys.exit(1)

    base = env("KOOLESTFLOW_BASE_URL", "https://cold-dm-app.vercel.app") if args.remote \
        else env("KOOLESTFLOW_LOCAL_BASE_URL", "http://127.0.0.1:8787")
    pw = env("KOOLESTFLOW_APP_PASSWORD")
    print(f"Target: {base}", file=sys.stderr)
    print(f"Prospects in file: {len(prospects)}", file=sys.stderr)

    ledger_path = kc.DEFAULT_LEDGER_PATH
    scratch_dir = None
    if args.ignore_ledger and not args.dry_run:
        # Point the ledger check at a scratch copy so the real history is
        # neither consulted for skipping nor rewritten by this push. It lives
        # in a temp dir, not the project: the project folder can be mounted
        # read-restricted, where cleaning up the scratch file fails and leaves
        # a stray file behind.
        scratch_dir = tempfile.mkdtemp(prefix="koolestflow-ledger-")
        ledger_path = os.path.join(scratch_dir, "scratch-ledger.json")
        with open(ledger_path, "w") as f:
            json.dump({"brands": {}}, f)

    result = kc.push_to_koolestflow(base, pw, prospects, dry_run=args.dry_run, ledger_path=ledger_path)

    if scratch_dir:
        shutil.rmtree(scratch_dir, ignore_errors=True)

    # Verify it actually stuck, rather than trusting the POST response.
    if not args.dry_run:
        cookie = kc.koolestflow_login(base, pw)
        state = kc.koolestflow_get_state(base, cookie)
        live = len(state.get("prospects") or [])
        print(f"\nVerification: GET /api/state now returns {live} prospect(s).", file=sys.stderr)
        if live == 0:
            print("WARNING: the push reported success but the state read back empty. "
                  "This backend is not persisting writes.", file=sys.stderr)
            sys.exit(2)
    return result


if __name__ == "__main__":
    main()
