#!/bin/bash
# cloud-run-finish.sh — last step of every cloud-Routine scheduled task.
#
#   bash scripts/cloud-run-finish.sh "<task-name>"
#
# Commits the run's output and pushes it to main, so the Mac picks it up on its
# next hourly git-sync (and the launchd importer drains any pending-push files).
# Never force-pushes. Refuses to commit a .env.

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1
TASK="${1:-scheduled task}"

git add -A
if git diff --cached --name-only | grep -qE '(^|/)\.env$'; then
  git reset -q; echo "xx refusing: a .env file was staged"; exit 1
fi
if git diff --cached --quiet; then echo "   nothing to commit"; exit 0; fi
git commit -q -m "Cloud run: $TASK $(date -u +%Y-%m-%d)" || exit 1

for i in 1 2 3 4; do
  if git pull -q --rebase origin main && git push -q origin HEAD:main; then
    echo "   pushed $(git rev-parse --short HEAD) to main"; exit 0
  fi
  git rebase --abort 2>/dev/null
  sleep $((2**i))
done

# Could not land on main (conflict or push refused): keep the work on a branch.
BR="cloud-run/$(echo "$TASK" | tr -c 'a-zA-Z0-9-' '-')$(date -u +%Y%m%d-%H%M)"
if git push -q origin "HEAD:refs/heads/$BR"; then
  echo "!! could not push to main; work saved on branch $BR (merge it by hand)"
else
  echo "xx push failed entirely; output exists only in this session"
fi
exit 1
