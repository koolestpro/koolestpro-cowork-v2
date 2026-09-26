#!/bin/bash
# import_pending_push.sh — Mac-side half of the hybrid lead-gen pipeline.
#
# The cloud scheduled task scores leads and drops them in .ai-workflow/pending-push/.
# This drains that queue into the LOCAL KoolestFlow instance, which is the only
# store that actually persists (see CLAUDE.md, 2026-09-01). Safe to run on a timer:
# it does nothing when the queue is empty or the backend is down, and each file is
# archived only after the push is verified by reading the state back.
#
# Install as a launchd job:
#   cp .ai-workflow/com.koolestpro.leadgen-import.plist ~/Library/LaunchAgents/
#   launchctl load ~/Library/LaunchAgents/com.koolestpro.leadgen-import.plist
#
# Run by hand any time:
#   ./.ai-workflow/tools/import_pending_push.sh

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PENDING_DIR="$PROJECT_ROOT/.ai-workflow/pending-push"
ARCHIVE_DIR="$PENDING_DIR/imported"
FAILED_DIR="$PENDING_DIR/failed"
LOG_FILE="$PROJECT_ROOT/.ai-workflow/leadgen-import.log"

mkdir -p "$ARCHIVE_DIR" "$FAILED_DIR"

say() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_FILE"; }

shopt -s nullglob
FILES=("$PENDING_DIR"/*.json)
if [ ${#FILES[@]} -eq 0 ]; then
  exit 0   # nothing queued; stay silent so the timer doesn't spam the log
fi

# Read the local backend URL from .env rather than hardcoding the port.
BASE_URL=$(grep -E '^KOOLESTFLOW_LOCAL_BASE_URL=' "$PROJECT_ROOT/.env" 2>/dev/null | cut -d= -f2- | tr -d '"'"'"' ')
BASE_URL="${BASE_URL:-http://127.0.0.1:8787}"

# Probe /api/health, NOT /api/state. /api/state sits behind _require_auth()
# and answers 401 without a session cookie, which `curl -f` treats as failure —
# so probing it reports a perfectly healthy backend as unreachable. /api/health
# is handled before the auth gate in backend/app.py.
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "$BASE_URL/api/health" 2>/dev/null)
if [ "$HTTP_CODE" != "200" ]; then
  if [ "$HTTP_CODE" = "000" ]; then
    say "KoolestFlow backend not reachable at $BASE_URL - ${#FILES[@]} file(s) still queued, will retry."
  else
    say "KoolestFlow backend at $BASE_URL answered /api/health with HTTP $HTTP_CODE - ${#FILES[@]} file(s) still queued, will retry."
  fi
  exit 0
fi

say "Backend up at $BASE_URL. ${#FILES[@]} file(s) to import."

for f in "${FILES[@]}"; do
  name="$(basename "$f")"

  # A file whose brands were already written to the ledger by a failed push
  # must bypass the ledger skip check, or every lead in it is dropped.
  EXTRA=""
  if grep -q '"ledgerAlreadyRecorded": *true' "$f"; then
    EXTRA="--ignore-ledger"
    say "  $name: ledger already recorded for these brands, passing --ignore-ledger"
  fi

  say "  importing $name ..."
  if python3 "$PROJECT_ROOT/.ai-workflow/tools/push_prospects_file.py" "$f" $EXTRA >>"$LOG_FILE" 2>&1; then
    mv "$f" "$ARCHIVE_DIR/$name"
    say "  OK: $name imported and archived."
  else
    code=$?
    # Exit code 2 means the push reported success but the state read back
    # empty - a real persistence failure, not a transient network blip.
    if [ $code -eq 2 ]; then
      mv "$f" "$FAILED_DIR/$name"
      say "  FAILED: $name pushed but did not persist. Moved to failed/. Check the backend."
    else
      say "  FAILED: $name (exit $code). Left in queue for the next run."
    fi
  fi
done

say "Import run finished."
