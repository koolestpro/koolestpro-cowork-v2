#!/bin/bash
# fix-mac.sh — one-time repair and upgrade for this Mac (2026-10-11). Safe to run more than once.
#
# Run in Terminal:
#   cd ~/koolestpro-cowork-v2 && git fetch origin && git show origin/main:scripts/fix-mac.sh > /tmp/fix-mac.sh && bash /tmp/fix-mac.sh
#
# It: 1) gets the stuck git sync going again with the new conflict-proof sync script,
#     2) puts the Ad Library rotation back on "kids" after the double run of 2026-10-07,
#     3) replaces the three separate launchd jobs with one catch-up job that runs anything missed
#        within ~5 minutes of the Mac waking or coming back online, and hands imported leads to the Sheet,
#     4) runs the catch-up job once now and prints what happened.

set -uo pipefail
ROOT="$HOME/koolestpro-cowork-v2"
cd "$ROOT" || { echo "Project folder not found at $ROOT"; exit 1; }
AGENTS="$HOME/Library/LaunchAgents"
echo "== Koolestpro Mac fix: $(date)"

echo; echo "== 1. Why the sync stopped (last lines of the old sync log)"
tail -n 5 .ai-workflow/git-sync.log 2>/dev/null || echo "(no log)"
git status -sb | head -n 3

echo; echo "== 1. Getting the latest sync script from GitHub and syncing"
git fetch -q origin main || { echo "Cannot reach GitHub. Check the internet connection and run this again."; exit 1; }
# Take the new scripts from GitHub first, so the merge below finds identical copies and the sync can resolve conflicts itself.
git checkout origin/main -- scripts/git-sync.sh scripts/mac-catchup.sh .ai-workflow/com.koolestpro.catchup.plist
bash scripts/git-sync.sh
tail -n 6 .ai-workflow/git-sync.log

echo; echo "== 2. Ad Library rotation"
python3 - <<'EOF'
import json, datetime, pathlib
p = pathlib.Path(".ai-workflow/ad_library_rotation.json")
mark = pathlib.Path(".ai-workflow/.stamps/rotation-fix-2026-10-07")
r = json.loads(p.read_text())
idx = r["meta"].get("currentIndex")
slots = [s.get("keyword") for s in r["slots"]]
print("currentIndex", idx, "->", slots[idx] if isinstance(idx, int) and idx < len(slots) else "?")
if mark.exists():
    print("already fixed earlier, leaving it")
elif idx == 3 and datetime.date.today() < datetime.date(2026, 10, 14):
    r["meta"]["currentIndex"] = 2
    r["meta"]["updatedAt"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    p.write_text(json.dumps(r, indent=2) + "\n")
    mark.parent.mkdir(parents=True, exist_ok=True); mark.write_text("done\n")
    print("fixed: currentIndex 3 -> 2, next Wednesday runs:", slots[2])
else:
    print("no change needed")
EOF

echo; echo "== 3. Replacing the old launchd jobs with the catch-up job"
mkdir -p "$AGENTS" .ai-workflow/.stamps
for old in com.koolestpro.git-sync com.koolestpro.leadgen-import com.koolestpro.directory-scrape; do
  if [ -f "$AGENTS/$old.plist" ]; then
    launchctl unload "$AGENTS/$old.plist" 2>/dev/null
    mv "$AGENTS/$old.plist" "$AGENTS/$old.plist.disabled"
    echo "turned off $old (file kept as $old.plist.disabled)"
  fi
done
# Carry over today's scrape if the old 07:30 job already ran, so it is not run twice.
if [ -f outreach/scrapers/state/scrape.log ] && [ -n "$(find outreach/scrapers/state/scrape.log -newermt "$(date +%Y-%m-%d) 07:30" 2>/dev/null)" ]; then
  date +%Y-%m-%d > .ai-workflow/.stamps/scrape-day
fi
cp .ai-workflow/com.koolestpro.catchup.plist "$AGENTS/"
launchctl unload "$AGENTS/com.koolestpro.catchup.plist" 2>/dev/null
launchctl load "$AGENTS/com.koolestpro.catchup.plist" && echo "catch-up job installed: runs every 5 minutes and at login"
[ -x outreach/scrapers/.venv/bin/python ] || echo "NOTE: the scraper's Playwright setup is missing. Run: bash outreach/scrapers/install_mac.sh (answer N to scheduling)"

echo; echo "== 4. Running the catch-up job once now (this can take a while if the daily scrape is due)"
bash scripts/mac-catchup.sh
tail -n 12 .ai-workflow/catchup.log 2>/dev/null
echo; echo "== Done. Last sync:"; tail -n 2 .ai-workflow/git-sync.log
echo "Check later with: tail .ai-workflow/catchup.log"
