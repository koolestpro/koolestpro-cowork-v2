#!/bin/bash
# git-sync.sh — keep this Mac and GitHub in step. Run by hand any time; the catch-up job
# (scripts/mac-catchup.sh) runs it hourly and right after the Mac wakes or comes back online.
#
# 2026-10-11 rewrite: the old version stopped for good on the first conflict (the Mac stopped syncing
# on 2026-10-06 because the same file had changed here and on GitHub). This version never gets stuck:
#   - it merges instead of rebasing, so there is always a clear "this Mac" side and "GitHub" side
#   - on a conflict, files this Mac owns (lead queues, logs, ledgers, rotation files, scraper state)
#     keep the Mac's copy, and everything else (code, docs written from the cloud) takes GitHub's copy
#   - the losing copy of every conflicted file is saved under .ai-workflow/sync-conflicts/<time>/, so nothing is lost
# Never force-pushes.

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1
LOG=".ai-workflow/git-sync.log"
say() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG"; }

git remote get-url origin >/dev/null 2>&1 || { say "no origin remote, run scripts/setup-github.sh first"; exit 0; }

# Leftovers from an interrupted run of the old script.
[ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] && { git rebase --abort 2>/dev/null; say "aborted a leftover rebase"; }
[ -f .git/MERGE_HEAD ] && { git merge --abort 2>/dev/null; say "aborted a leftover merge"; }

# Paths the Mac writes and owns. On a conflict the Mac's version wins for these.
mac_owned() {
  case "$1" in
    .ai-workflow/*log*|.ai-workflow/pending-push/*|.ai-workflow/taken-brands-ledger.json|.ai-workflow/*rotation*.json|\
    .ai-workflow/scheduled-tasks-snapshot.json|.ai-workflow/.stamps/*|outreach/scrapers/state/*|outreach/scrapers/output/*|\
    distribution-health-log.md|targets_pool.json|trend-radar-log.json|dm_leads_pool.json|outreach_tracker.json|outputs/*) return 0 ;;
    *) return 1 ;;
  esac
}

# 1. Save local work.
git add -A
if git diff --cached --name-only | grep -qE '(^|/)\.env$'; then
  git reset -q; say "refusing: a .env file was staged"; exit 1
fi
git diff --cached --quiet || git commit -q -m "Auto-sync from $(scutil --get ComputerName 2>/dev/null || hostname) $(date +%Y-%m-%d\ %H:%M)"

# 2. Bring in GitHub's work.
if ! git fetch -q origin main; then say "fetch failed (offline?), will retry"; exit 0; fi
if ! git merge -q --no-edit origin/main >/dev/null 2>&1; then
  stamp="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
  keep=".ai-workflow/sync-conflicts/$stamp"
  mkdir -p "$keep"
  resolved=0
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    mkdir -p "$keep/$(dirname "$f")"
    if mac_owned "$f"; then
      git show "origin/main:$f" > "$keep/$f.github" 2>/dev/null || true
      git checkout --ours -- "$f" 2>/dev/null || git rm -q -- "$f"
      say "conflict in $f: kept this Mac's copy (GitHub's saved in $keep)"
    else
      git show "HEAD:$f" > "$keep/$f.mac" 2>/dev/null || true
      git checkout --theirs -- "$f" 2>/dev/null || git rm -q -- "$f"
      say "conflict in $f: took GitHub's copy (this Mac's saved in $keep)"
    fi
    git add -- "$f" 2>/dev/null
    resolved=$((resolved + 1))
  done < <(git diff --name-only --diff-filter=U)
  if git diff --name-only --diff-filter=U | grep -q .; then
    git merge --abort 2>/dev/null
    say "CONFLICT could not be resolved automatically, will retry next run. Details: git status"
    exit 1
  fi
  git commit -q --no-edit -m "Merge GitHub into $(scutil --get ComputerName 2>/dev/null || hostname): $resolved conflict(s) auto-resolved" || true
  rmdir "$keep" 2>/dev/null || true
fi

# 3. Publish.
if git push -q origin HEAD:main; then
  mkdir -p .ai-workflow/.stamps && date -u +%s > .ai-workflow/.stamps/git-sync
  say "synced ($(git rev-parse --short HEAD))"
else
  say "push failed, will retry next run"
fi
