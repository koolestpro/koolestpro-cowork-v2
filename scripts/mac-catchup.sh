#!/bin/bash
# mac-catchup.sh — one job that makes sure nothing scheduled on this Mac is ever skipped for good.
#
# launchd runs it every 5 minutes and at login (.ai-workflow/com.koolestpro.catchup.plist). Each run is
# cheap: it checks what is overdue and only does that. So when the Mac was asleep, off or offline, every
# missed job runs within about 5 minutes of it coming back online:
#   1. git sync            (scripts/git-sync.sh)              if the last good sync is over 55 minutes old
#   2. lead import         (.ai-workflow/tools/import_pending_push.sh)   whenever leads are queued
#   3. leads to the Sheet  (outreach/scrapers/koolestflow_to_sheet.py)   right after an import, and once a day
#   4. directory scrape    (outreach/scrapers/directory_scrape.py)       once a day, any time after 07:30
# Stamps live in .ai-workflow/.stamps/ (not in git). Log: .ai-workflow/catchup.log

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1
STAMPS="$ROOT/.ai-workflow/.stamps"
LOG="$ROOT/.ai-workflow/catchup.log"
mkdir -p "$STAMPS"
say() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" >> "$LOG"; }
age() { [ -f "$STAMPS/$1" ] && echo $(( $(date -u +%s) - $(cat "$STAMPS/$1" 2>/dev/null || echo 0) )) || echo 999999999; }
mark() { date -u +%s > "$STAMPS/$1"; }

# One run at a time (a long directory scrape must not overlap the next 5-minute run).
LOCK="$STAMPS/.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  # A lock older than 3 hours is left over from a crash or a sleep mid-run.
  if [ -n "$(find "$LOCK" -maxdepth 0 -mmin +180 2>/dev/null)" ]; then rm -rf "$LOCK"; mkdir "$LOCK" || exit 0; else exit 0; fi
fi
trap 'rm -rf "$LOCK"' EXIT

# Offline? Do nothing now; the next run 5 minutes later tries again.
if ! curl -s -o /dev/null -m 6 https://github.com; then exit 0; fi

PY="$ROOT/outreach/scrapers/.venv/bin/python"; [ -x "$PY" ] || PY="python3"

# 1. Git sync, hourly.
if [ "$(age git-sync)" -gt 3300 ]; then
  bash "$ROOT/scripts/git-sync.sh" >/dev/null 2>&1 && say "git sync ok" || say "git sync did not finish, see .ai-workflow/git-sync.log"
fi

# 2. Lead import whenever something is queued, then 3. hand new leads to the outreach Sheet.
shopt -s nullglob
queued=("$ROOT"/.ai-workflow/pending-push/*.json)
before=$(ls "$ROOT/.ai-workflow/pending-push/imported" 2>/dev/null | wc -l | tr -d ' ')
if [ ${#queued[@]} -gt 0 ]; then
  bash "$ROOT/.ai-workflow/tools/import_pending_push.sh" >/dev/null 2>&1
  after=$(ls "$ROOT/.ai-workflow/pending-push/imported" 2>/dev/null | wc -l | tr -d ' ')
  [ "$after" -gt "$before" ] && { say "imported $((after - before)) lead file(s)"; rm -f "$STAMPS/to-sheet"; }
fi
if [ "$(age to-sheet)" -gt 86000 ]; then
  if "$PY" "$ROOT/outreach/scrapers/koolestflow_to_sheet.py" >> "$LOG" 2>&1; then mark to-sheet; say "leads to Sheet ok"; else say "leads to Sheet failed, will retry"; fi
fi

# 4. Directory scrape once a day, at or after 07:30 local time.
today=$(date +%Y-%m-%d)
if [ "$(cat "$STAMPS/scrape-day" 2>/dev/null)" != "$today" ] && [ "$(date +%H%M)" -ge 0730 ]; then
  say "directory scrape starting (missed or due)"
  if "$PY" "$ROOT/outreach/scrapers/directory_scrape.py" >> "$ROOT/outreach/scrapers/state/scrape.log" 2>&1; then
    echo "$today" > "$STAMPS/scrape-day"; say "directory scrape ok"
  else
    say "directory scrape failed, will retry in 5 minutes (see outreach/scrapers/state/scrape.log)"
  fi
fi
exit 0
