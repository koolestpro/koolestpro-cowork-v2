#!/bin/bash
# cloud-run-start.sh — first step of every scheduled task that runs as a cloud
# Routine (claude.ai cloud session) instead of on the Mac's desktop app.
#
#   bash scripts/cloud-run-start.sh
#
# Why: desktop-app scheduled tasks only run while the Mac is awake, the Claude
# app is open and the project folder is connected. Missed runs wait for the Mac
# (and get suspended as "device_absent"). Cloud Routines run on schedule with
# the Mac off. They work on a fresh clone of the GitHub repo, so this script:
#   1. Puts the clone on an up-to-date main (the Mac's hourly git-sync pulls main).
#   2. Writes a local .env from the cloud environment's secrets, because several
#      tools read .env directly. .env is gitignored and never committed.
#   3. Sets a git identity for the run's commit.

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

# 1. Fresh main.
for i in 1 2 3 4; do git fetch -q origin main && break; sleep $((2**i)); done
git checkout -q -B main origin/main || { echo "xx could not check out main"; exit 1; }

# 2. .env from environment variables (names from .env.example plus a few extras).
keys=$( { sed -n 's/^\([A-Z][A-Z0-9_]*\)=.*/\1/p' .env.example; \
          printf '%s\n' OUTREACH_API_TOKEN OUTREACH_API_URL SERPER_API_KEY GOOGLE_SEARCH_API_KEY GOOGLE_SEARCH_CX; } | sort -u )
umask 077
: > .env
n=0
for k in $keys; do
  v="${!k-}"
  [ -n "$v" ] && { printf '%s=%s\n' "$k" "$v" >> .env; n=$((n+1)); }
done
echo "   .env written with $n key(s) from the cloud environment (not committed)"

# 3. Commit identity.
git config user.name  >/dev/null || git config user.name  "Koolestpro cloud routine"
git config user.email >/dev/null || git config user.email "noreply@anthropic.com"

echo "   ready on main at $(git rev-parse --short HEAD)"
