#!/usr/bin/env bash
# Desktop backup runner for the weekly SEO cycle.
# Runs Claude Code headless on this repo, following seo/SOP.md for one client.
#
#   ./seo/desktop/run-week.sh tapandrate
#
# Needs: Claude Code CLI logged in (`claude`), python3, git, and secrets in the repo-root .env
# (SHOPIFY_<SLUG>_DOMAIN/_TOKEN, GOOGLE_CLIENT_ID/_SECRET/_REFRESH_TOKEN).
# Gmail drafts + Ubersuggest + gpt-image need those connectors/skills on this machine too.
set -euo pipefail

CLIENT="${1:?usage: run-week.sh <client-slug>}"
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
DATE="$(date +%F)"
LOG_DIR="$REPO/seo/clients/$CLIENT/runs/$DATE"
mkdir -p "$LOG_DIR"
cd "$REPO"

git pull --ff-only || echo "git pull failed; continuing on local copy"

PROMPT="Run the weekly SEO cycle for client '$CLIENT' exactly as written in seo/SOP.md.
Read seo/config/seo-rules.md and the client's files first. Write everything to seo/clients/$CLIENT/runs/$DATE/.
Never publish an article, never edit live pages, never send email: Shopify hidden draft and Gmail drafts only.
If a credential is missing, skip that step, say so in notes.md and carry on.
Finish by committing the run folder and logs with message 'seo($CLIENT): weekly run $DATE' and pushing."

claude -p "$PROMPT" \
  --permission-mode acceptEdits \
  --allowedTools "Bash(python3 seo/tools/*) Bash(git *) Read Write Edit Glob Grep WebFetch WebSearch Skill mcp__Ubersuggest mcp__Gmail__create_draft mcp__Cloudinary__upload-asset" \
  2>&1 | tee "$LOG_DIR/desktop-run.log"
