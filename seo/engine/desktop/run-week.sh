#!/usr/bin/env bash
# Desktop runner for the weekly SEO cycle of THIS project (the repo this file sits in).
#   ./seo/engine/desktop/run-week.sh
# Needs: Claude Code CLI logged in (`claude`), python3, git, and this project's keys in <repo>/.env.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
DATE="$(date +%F)"
LOG_DIR="$REPO/seo/project/runs/$DATE"
mkdir -p "$LOG_DIR"
cd "$REPO"

if git rev-parse --git-dir >/dev/null 2>&1; then git pull --ff-only || echo "git pull failed; continuing on local copy"; fi

PROMPT="Run this week's SEO cycle exactly as written in seo/engine/SOP.md.
Read seo/engine/rules.md and everything in seo/project/ first. Write all output to seo/project/runs/$DATE/.
Never publish an article, merge a PR, edit live pages, or send email without approval: drafts only.
If a credential is missing, skip that step, say so in notes.md and carry on.
Finish by committing the run folder and logs (if this is a git repo) and printing a short summary."

claude -p "$PROMPT" \
  --permission-mode acceptEdits \
  --allowedTools "Bash(python3 seo/engine/tools/*) Bash(git *) Read Write Edit Glob Grep WebFetch WebSearch Skill" \
  2>&1 | tee "$LOG_DIR/desktop-run.log"
