#!/usr/bin/env python3
"""
write_topic_log.py — writes this week's ranked Tips topic candidates to trend-radar-log.json.

koolestpro-tips-weekly reads the LAST entry in this file's "weeks" array as its
Layer 1 topic source (see docs/koolestpro-content-operating-plan.md Step 11 and
that task's own SKILL.md Step 1). If the latest entry's "week" key doesn't match
the current ISO week, tips-weekly treats it as stale (trend-radar didn't run or
found nothing usable) and falls back to its existing backlog-first logic — this
script doesn't need to know about that fallback, it just needs to write an honest
record of what did or didn't happen this run.

Usage:
    python3 write_topic_log.py --log /path/to/trend-radar-log.json --entry entry.json

Where entry.json is a single object:
{
  "week": "2026-W31",
  "sourcesUsed": ["x"],
  "sourcesSkipped": [{"source": "reddit", "reason": "no provider configured"}],
  "candidateTopics": [
    {"rank": 1, "topic": "...", "angle": "Myth vs Reality", "sourceUrl": "...", "score": 42, "rationale": "..."},
    ...
  ],
  "pickedTopic": { ... same shape as the rank-1 candidateTopics entry, or null if nothing cleared the relevance bar ... }
}

Re-running with the same "week" value REPLACES that week's entry (idempotent —
a run that's re-triggered same-day doesn't create duplicate weeks), never appends
a second entry for a week that's already there.
"""

import argparse
import json
import os
from datetime import datetime, timezone


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    ap.add_argument("--entry", required=True, help="Path to a JSON object, or '-' for stdin")
    args = ap.parse_args()

    if os.path.exists(args.log):
        with open(args.log) as f:
            log = json.load(f)
    else:
        log = {
            "meta": {
                "description": "Weekly trend-radar Tips topic candidates. koolestpro-tips-weekly "
                                "reads the last entry in weeks[] for its Layer 1 topic pick. "
                                "See docs/koolestpro-content-operating-plan.md Step 11.",
            },
            "weeks": [],
        }

    if args.entry == "-":
        import sys
        entry = json.load(sys.stdin)
    else:
        with open(args.entry) as f:
            entry = json.load(f)

    if "week" not in entry:
        raise SystemExit("entry must have a 'week' key, e.g. '2026-W31'")

    log["weeks"] = [w for w in log["weeks"] if w.get("week") != entry["week"]]
    entry["writtenAt"] = datetime.now(timezone.utc).isoformat()
    log["weeks"].append(entry)
    log["meta"]["updatedAt"] = entry["writtenAt"]

    with open(args.log, "w") as f:
        json.dump(log, f, indent=2)

    print(json.dumps({"week": entry["week"], "picked": entry.get("pickedTopic", {}).get("topic") if entry.get("pickedTopic") else None, "total_weeks_logged": len(log["weeks"])}, indent=2))


if __name__ == "__main__":
    main()
