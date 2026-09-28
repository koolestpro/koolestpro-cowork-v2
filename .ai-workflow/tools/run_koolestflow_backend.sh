#!/bin/bash
# run_koolestflow_backend.sh — keeps the local KoolestFlow backend (127.0.0.1:8787) up.
#
# Started by launchd (com.koolestpro.koolestflow-backend.plist) at login and restarted
# automatically if it exits. The leadgen importer (import_pending_push.sh) needs this
# running, otherwise lead files pile up in .ai-workflow/pending-push/.
#
# Install once:
#   ./.ai-workflow/tools/install_koolestflow_backend_agent.sh
#
# The backend reads cold-email-app/.env.local (or .env) itself, so no keys live here.

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
APP_DIR="$PROJECT_ROOT/cold-email-app"

# launchd starts with a bare PATH; prefer Homebrew / python.org Python over the
# /usr/bin/python3 Xcode stub.
export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/Current/bin:/usr/bin:/bin"
PY="$(command -v python3)"

# If something is already listening on 8787 (e.g. started by hand in Terminal),
# don't start a second copy that would crash on "address in use" and loop.
if /usr/sbin/lsof -nP -iTCP:8787 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] port 8787 already in use, not starting a second backend; sleeping 5 min"
  sleep 300
  exit 0
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] starting KoolestFlow backend with $PY"
cd "$APP_DIR" || { echo "cannot cd to $APP_DIR"; exit 1; }
exec "$PY" -u backend/app.py
