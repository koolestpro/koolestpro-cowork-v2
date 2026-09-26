#!/usr/bin/env python3
"""
budget_ledger.py — shared spend tracker for koolestpro-trend-radar.

Every paid source (X, Reddit) records its estimated spend here before/after a
pull. Nothing else in this skill enforces budget on its own — x_search.py and
reddit_search.py both import and call check_and_reserve() BEFORE making the
network call, so a run halts before overspending, not after.

Ledger file is a flat JSON: {"months": {"2026-07": {"x": 0.35, "reddit": 0.0}}}.
One ledger per project (path passed explicitly, default trend-radar-spend-ledger.json
at the project root) — this keeps the ledger itself project-local/portable, same as
the rest of this skill.

Usage as a library:
    from budget_ledger import check_and_reserve, current_month_spend

    ok, reason = check_and_reserve(ledger_path, source="x", estimated_cost=0.25, monthly_cap=5.0)
    if not ok:
        print(f"Halting X pull: {reason}")
        sys.exit(0)
    ... make the actual API call ...
"""

import json
import os
from datetime import datetime, timezone


def _month_key(dt=None):
    dt = dt or datetime.now(timezone.utc)
    return dt.strftime("%Y-%m")


def load_ledger(path):
    if not os.path.exists(path):
        return {"months": {}}
    try:
        with open(path) as f:
            data = json.load(f)
            if "months" not in data:
                data["months"] = {}
            return data
    except (json.JSONDecodeError, OSError):
        return {"months": {}}


def save_ledger(path, ledger):
    with open(path, "w") as f:
        json.dump(ledger, f, indent=2)


def current_month_spend(path, source, dt=None):
    ledger = load_ledger(path)
    month = _month_key(dt)
    return ledger.get("months", {}).get(month, {}).get(source, 0.0)


def check_and_reserve(path, source, estimated_cost, monthly_cap, dt=None):
    """
    Checks whether adding estimated_cost to this month's running total for `source`
    would exceed monthly_cap. If it would, returns (False, reason) WITHOUT recording
    anything — the caller should skip the pull entirely rather than do a partial one.
    If it's within budget, records the spend immediately (reserve-then-spend, not
    spend-then-record, so a crash mid-pull can't silently skip the ledger write) and
    returns (True, None).
    """
    month = _month_key(dt)
    ledger = load_ledger(path)
    months = ledger.setdefault("months", {})
    month_data = months.setdefault(month, {})
    running = month_data.get(source, 0.0)

    if running + estimated_cost > monthly_cap:
        return False, (
            f"{source} spend this month is ${running:.2f}, adding ${estimated_cost:.2f} "
            f"would exceed the ${monthly_cap:.2f} cap. Skipping this pull."
        )

    month_data[source] = round(running + estimated_cost, 4)
    save_ledger(path, ledger)
    return True, None


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Inspect or reset the trend-radar spend ledger.")
    ap.add_argument("--ledger", default="trend-radar-spend-ledger.json")
    ap.add_argument("--show", action="store_true", help="Print the ledger as-is")
    args = ap.parse_args()

    if args.show:
        print(json.dumps(load_ledger(args.ledger), indent=2))
