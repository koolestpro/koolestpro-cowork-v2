#!/bin/bash
# Installs (or reinstalls) the launchd agent that keeps the KoolestFlow backend running.
# Run once in Terminal on the Mac:
#   bash /Users/mac/koolestpro-cowork-v2/.ai-workflow/tools/install_koolestflow_backend_agent.sh
set -euo pipefail
LABEL="com.koolestpro.koolestflow-backend"
SRC="/Users/mac/koolestpro-cowork-v2/.ai-workflow/$LABEL.plist"
DEST="$HOME/Library/LaunchAgents/$LABEL.plist"

mkdir -p "$HOME/Library/LaunchAgents"
chmod +x /Users/mac/koolestpro-cowork-v2/.ai-workflow/tools/run_koolestflow_backend.sh
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
cp "$SRC" "$DEST"
plutil -lint "$DEST"
launchctl bootstrap "gui/$(id -u)" "$DEST"
launchctl enable "gui/$(id -u)/$LABEL"

sleep 4
if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8787/ | grep -qE "^[0-9]{3}$"; then
  echo "OK: KoolestFlow backend is answering on http://127.0.0.1:8787"
  echo "Draining the lead queue now..."
  bash /Users/mac/koolestpro-cowork-v2/.ai-workflow/tools/import_pending_push.sh || true
else
  echo "Backend not answering yet. Check the log:"
  tail -20 /Users/mac/koolestpro-cowork-v2/.ai-workflow/koolestflow-backend.launchd.log
fi
