#!/bin/bash
# git-sync.sh — keep this Mac and GitHub in step. Run by hand any time, or hourly via
# launchd (.ai-workflow/com.koolestpro.git-sync.plist).
#
# Pulls first (so work done from your phone / Codex / another machine lands here),
# then commits and pushes anything new from this Mac. Never force-pushes.

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1
LOG=".ai-workflow/git-sync.log"
say() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG"; }

git remote get-url origin >/dev/null 2>&1 || { say "no origin remote, run scripts/setup-github.sh first"; exit 0; }

# 1. Save local work.
git add -A
if git diff --cached --name-only | grep -qE '(^|/)\.env$'; then
  git reset -q; say "refusing: a .env file was staged"; exit 1
fi
git diff --cached --quiet || git commit -q -m "Auto-sync from $(scutil --get ComputerName 2>/dev/null || hostname) $(date +%Y-%m-%d\ %H:%M)"

# 2. Bring in remote work, replaying ours on top.
if ! git pull -q --rebase origin main; then
  git rebase --abort 2>/dev/null
  say "CONFLICT: the same file changed here and on GitHub. Resolve by hand: cd $(pwd) && git pull --rebase"
  exit 1
fi

# 3. Publish.
if git push -q origin main; then say "synced ($(git rev-parse --short HEAD))"; else say "push failed, will retry next run"; fi
