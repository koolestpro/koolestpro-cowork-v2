#!/usr/bin/env python3
"""
inject_format_radar.py — writes new Format Radar findings into content_pipeline.html.

Per CLAUDE.md's core rule ("Cowork must ONLY read and write to this JSON block")
applied to the new FORMAT_RADAR_DATA block (see docs/koolestpro-content-operating-plan.md
Step 11 and the comment inside content_pipeline.html itself): this script

  1. Reads the existing <script id="format-radar-data"> block.
  2. Appends only genuinely NEW findings (deduped by id — skips if an id already exists,
     same "use id to prevent duplicates" rule as SYNC_DATA.items).
  3. NEVER touches existing entries' status (a Ridwan dismiss/mark-tried action in the
     browser only persists to localStorage, not back into this file — see the comment
     in content_pipeline.html's loadFormatRadarState() for why that's an accepted
     limitation of a local-first, no-server system).
  4. Bumps meta.syncHash so the browser's cached state invalidates and picks up the
     new findings on next load.
  5. Preserves all surrounding HTML/CSS/JS byte-for-byte — replaces ONLY the JSON
     inside the <script id="format-radar-data"> tag.

Usage:
    python3 inject_format_radar.py \\
        --html /path/to/content_pipeline.html \\
        --findings new_findings.json     # a JSON array of finding objects, or "-" for stdin

Each finding object must have at minimum: id, week, sourcePlatform, description.
Recommended fields (all optional but expected by content_pipeline.html's render):
    exampleUrl, creatorHandle, whyItWorks, suggestedMedium, feasibilityNote, status
"status" defaults to "new" if not provided — that's what makes it show up as a
flagged card. Never pass "dismissed" or "tried" here; those only happen via the
UI, this script is additive-only.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone

BLOCK_RE = re.compile(
    r'(<script id="format-radar-data" type="application/json">\n)(.*?)(\n</script>)',
    re.S,
)


def load_findings_arg(path):
    if path == "-":
        return json.load(sys.stdin)
    with open(path) as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(description="Append new Format Radar findings into content_pipeline.html.")
    ap.add_argument("--html", required=True)
    ap.add_argument("--findings", required=True, help="Path to a JSON array of findings, or '-' for stdin")
    args = ap.parse_args()

    with open(args.html) as f:
        html = f.read()

    m = BLOCK_RE.search(html)
    if not m:
        print("ERROR: could not find the format-radar-data script block. "
              "Has content_pipeline.html's structure changed?", file=sys.stderr)
        sys.exit(1)

    current = json.loads(m.group(2))
    existing_ids = {f["id"] for f in current.get("findings", [])}

    new_findings = load_findings_arg(args.findings)
    added = 0
    skipped = []
    for f in new_findings:
        if "id" not in f:
            print(f"WARNING: skipping a finding with no id: {f}", file=sys.stderr)
            continue
        if f["id"] in existing_ids:
            skipped.append(f["id"])
            continue
        f.setdefault("status", "new")
        current.setdefault("findings", []).append(f)
        existing_ids.add(f["id"])
        added += 1

    now_iso = datetime.now(timezone.utc).isoformat()
    current.setdefault("meta", {})["updatedAt"] = now_iso
    current["meta"]["syncHash"] = hashlib.sha256(
        json.dumps(current["findings"], sort_keys=True).encode()
    ).hexdigest()[:16]

    new_block_json = json.dumps(current, indent=2)
    new_html = html[: m.start()] + m.group(1) + new_block_json + m.group(3) + html[m.end():]

    with open(args.html, "w") as f:
        f.write(new_html)

    print(json.dumps({
        "added": added,
        "skipped_duplicate_ids": skipped,
        "total_findings_now": len(current.get("findings", [])),
        "new_sync_hash": current["meta"]["syncHash"],
    }, indent=2))


if __name__ == "__main__":
    main()
