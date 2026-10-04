#!/bin/bash
# One-time setup on your Mac (run in Terminal, not through Claude):
#   bash ~/koolestpro-cowork-v2/outreach/scrapers/install_mac.sh
# Installs Playwright + Chromium into a private venv and (optionally) schedules the scraper daily at 07:30.
set -e
ROOT="$HOME/koolestpro-cowork-v2"
cd "$ROOT/outreach/scrapers"
python3 -m venv .venv
./.venv/bin/pip install --quiet playwright certifi
./.venv/bin/playwright install chromium
echo "Installed. Test it without pushing anything:"
echo "  $ROOT/outreach/scrapers/.venv/bin/python $ROOT/outreach/scrapers/directory_scrape.py --dry-run --headed"
read -p "Schedule it daily at 07:30? (y/N) " yn
if [ "$yn" = "y" ]; then
  PLIST="$HOME/Library/LaunchAgents/com.koolestpro.directory-scrape.plist"
  cp "$ROOT/outreach/scrapers/com.koolestpro.directory-scrape.plist" "$PLIST"
  launchctl unload "$PLIST" 2>/dev/null || true
  launchctl load "$PLIST"
  echo "Scheduled. Log: $ROOT/outreach/scrapers/state/scrape.log"
fi
