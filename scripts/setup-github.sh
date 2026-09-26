#!/bin/bash
# setup-github.sh — one-time setup, run from Terminal on the Mac.
#
#   bash ~/Downloads/koolestpro-cowork-v2/scripts/setup-github.sh
#
# What it does, in order:
#   1. Backs up the desktop app's local scheduled-task definitions into the repo.
#   2. Moves the project OUT of ~/Downloads to ~/koolestpro-cowork-v2.
#      macOS blocks background (launchd) jobs from reading ~/Downloads, which is why
#      the lead importer has failed with "Operation not permitted" on every run.
#   3. Reinstalls the lead importer (launchd) at the new path and runs it once.
#   4. Links site/, cold-email-app/, replo-rebuilds/ as submodules (they keep their own repos).
#   5. Commits everything (secrets and heavy video excluded by .gitignore) and pushes
#      to github.com/koolestpro/koolestpro-cowork-v2.
#   6. Installs an hourly auto-sync so GitHub always has your latest work.
#
# Safe to re-run: every step checks whether it has already been done.

set -uo pipefail

OLD="$HOME/Downloads/koolestpro-cowork-v2"
NEW="$HOME/koolestpro-cowork-v2"
REMOTE="https://github.com/koolestpro/koolestpro-cowork-v2.git"
LA="$HOME/Library/LaunchAgents"

step() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[33m!! %s\033[0m\n' "$*"; }
die()  { printf '\033[31mxx %s\033[0m\n' "$*"; exit 1; }

cd "$HOME" || die "cannot cd home"

# Pick up where we are: before or after the move.
if [ -d "$OLD" ] && [ ! -e "$NEW" ]; then SRC="$OLD"
elif [ -d "$NEW" ]; then SRC="$NEW"
else die "Project folder not found in ~/Downloads or ~/"; fi

# ---------------------------------------------------------------- 1
step "1/6 Backing up desktop scheduled-task definitions"
SCHED="$HOME/Documents/Claude/Scheduled"
if [ -d "$SCHED" ]; then
  mkdir -p "$SRC/scheduled-tasks/desktop"
  rsync -a --include='*/' --include='*.md' --exclude='*' "$SCHED/" "$SRC/scheduled-tasks/desktop/"
  echo "   copied $(find "$SRC/scheduled-tasks/desktop" -name '*.md' | wc -l | tr -d ' ') task files"
  if grep -rIlE '(sk-[A-Za-z0-9_-]{20,}|_API_KEY=[^ ]{8,}|ghp_[A-Za-z0-9]{20,})' "$SRC/scheduled-tasks/desktop" >/dev/null 2>&1; then
    warn "A task file seems to contain a key. Those files are excluded from git until you check them:"
    mkdir -p "$SRC/.git/info"
    grep -rIlE '(sk-[A-Za-z0-9_-]{20,}|_API_KEY=[^ ]{8,}|ghp_[A-Za-z0-9]{20,})' "$SRC/scheduled-tasks/desktop" \
      | sed "s|^$SRC/||" | tee -a "$SRC/.git/info/exclude"
  fi
else
  echo "   no local scheduled tasks folder, skipping"
fi

# ---------------------------------------------------------------- 2
step "2/6 Moving the project out of ~/Downloads"
if [ "$SRC" = "$OLD" ]; then
  mv "$OLD" "$NEW" || die "move failed (is a file open in another app?)"
  echo "   moved to $NEW"
else
  echo "   already at $NEW"
fi
cd "$NEW" || die "cannot cd $NEW"

# ---------------------------------------------------------------- 3
step "3/6 Reinstalling the lead importer (launchd)"
mkdir -p "$LA"
launchctl unload "$LA/com.koolestpro.leadgen-import.plist" 2>/dev/null
cp .ai-workflow/com.koolestpro.leadgen-import.plist "$LA/"
launchctl load "$LA/com.koolestpro.leadgen-import.plist" && echo "   loaded"
sleep 3
bash .ai-workflow/tools/import_pending_push.sh
echo "   queue now: $(ls .ai-workflow/pending-push/*.json 2>/dev/null | wc -l | tr -d ' ') file(s) waiting"
echo "   (if files are still waiting, start KoolestFlow locally; the job retries every 30 min)"

# ---------------------------------------------------------------- 4
step "4/6 Linking companion repos as submodules"
[ -d .git ] || git init -q -b main
git config core.quotepath false
git config http.postBuffer 524288000
add_sub() {  # path url
  if git config -f .gitmodules --get "submodule.$1.url" >/dev/null 2>&1; then
    echo "   $1 already linked"
  elif [ -d "$1/.git" ]; then
    git submodule add -q "$2" "$1" && echo "   linked $1 -> $2"
  else
    warn "$1 is not a git repo, skipping"
  fi
}
add_sub site           https://github.com/koolestpro/koolestpro.git
add_sub cold-email-app https://github.com/koolestpro/cold-dm-app.git
add_sub replo-rebuilds https://github.com/koolestpro/koolestpro-portfolio.git
for d in site cold-email-app replo-rebuilds; do
  [ -d "$d/.git" ] || continue
  n=$(git -C "$d" status --porcelain | wc -l | tr -d ' ')
  [ "$n" != "0" ] && warn "$d has $n uncommitted change(s). Commit + push inside $d when ready, then run scripts/git-sync.sh"
done

# ---------------------------------------------------------------- 5
step "5/6 Committing and pushing to GitHub"
git add -A
BIG=""
while IFS= read -r -d '' f; do
  [ -f "$f" ] && [ "$(stat -f%z "$f")" -gt 95000000 ] && BIG="$BIG$f"$'\n'
done < <(git diff --cached --name-only -z)
[ -n "$BIG" ] && { printf '%s' "$BIG"; die "files above are over GitHub's 100 MB limit; add them to .gitignore and re-run"; }
if git diff --cached --name-only | grep -qE '(^|/)\.env$'; then die ".env got staged, stopping so no secret is pushed"; fi
if ! git diff --cached --quiet; then
  git commit -q -m "Sync koolestpro-cowork-v2 from Mac ($(date +%Y-%m-%d))" && echo "   committed $(git rev-parse --short HEAD)"
fi
git remote get-url origin >/dev/null 2>&1 || git remote add origin "$REMOTE"
if ! git ls-remote origin >/dev/null 2>&1; then
  die "Can't reach $REMOTE. Create it on github.com as a PRIVATE, EMPTY repo (no README), then re-run this script."
fi
git push -u origin main || die "push failed (see message above)"

# ---------------------------------------------------------------- 6
step "6/6 Installing hourly auto-sync to GitHub"
launchctl unload "$LA/com.koolestpro.git-sync.plist" 2>/dev/null
cp .ai-workflow/com.koolestpro.git-sync.plist "$LA/"
launchctl load "$LA/com.koolestpro.git-sync.plist" && echo "   loaded (logs: .ai-workflow/git-sync.log)"

step "Done."
echo "   Project now lives at: $NEW"
echo "   Repo: https://github.com/koolestpro/koolestpro-cowork-v2"
echo "   Next: in the Claude desktop app, reconnect the folder at its new location."
