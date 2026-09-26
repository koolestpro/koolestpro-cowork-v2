#!/bin/bash
# Idempotent Playwright/Chromium environment setup for this ARM64 sandbox.
# Safe to run at the start of every session/scheduled task — skips any step
# that's already done, so it costs ~1s on a warm sandbox and a handful of
# bash calls on a cold one.
#
# Usage:
#   source .ai-workflow/tools/bootstrap_env.sh
# (must be *sourced*, not executed, so the exports survive in the calling
#  shell — a plain `bash bootstrap_env.sh` sets them in a subshell that exits
#  immediately and the exports are lost)
#
# REWRITTEN 2026-09-08 after a cold sandbox exposed two real failures in the
# old version, both of which silently cost several wasted bash calls:
#
#   1. `python3 -m playwright install chromium` is NOT resumable. Each attempt
#      restarts the 195MB download from zero and gets killed by the command
#      ceiling somewhere around 40-60%, forever. Fixed by downloading the build
#      zips directly with `wget -c`, which genuinely resumes across calls.
#
#   2. Browsers must NOT live in ~/.cache. That is on /sessions, which is a
#      ~9.8GB volume already mostly consumed by the mounted project, and
#      extracting chromium there filled it to 100% and broke the rest of the
#      run. /tmp is on a different, roomier volume. Hence
#      PLAYWRIGHT_BROWSERS_PATH.
#
# Both /tmp locations are wiped between sandboxes, so a cold start pays the
# download again. That is fine and expected; what matters is that it now
# completes instead of looping.

set -e

LIBDIR="/tmp/pw_libs/extracted/usr/lib/aarch64-linux-gnu"
export PLAYWRIGHT_BROWSERS_PATH="/tmp/pw-browsers"
CDN="https://cdn.playwright.dev/dbazure/download/playwright/builds"

# 1. Playwright python package
if ! python3 -c "import playwright" 2>/dev/null; then
  echo "[bootstrap] installing playwright..."
  pip install playwright --break-system-packages -q
fi

# 2. libXdamage.so.1 (chromium's missing shared lib; no root, so no apt install)
if [ ! -f "$LIBDIR/libXdamage.so.1" ]; then
  echo "[bootstrap] fetching libxdamage1..."
  mkdir -p /tmp/pw_libs
  (
    cd /tmp/pw_libs
    apt-get download libxdamage1 >/tmp/pw_libs/apt_download.log 2>&1
    mkdir -p extracted
    dpkg-deb -x libxdamage1_*.deb extracted 2>/dev/null || true
  )
fi
export LD_LIBRARY_PATH="$LIBDIR:$LD_LIBRARY_PATH"

# 3. Browser builds. Revision comes from the installed package rather than being
#    hardcoded, so a playwright upgrade cannot silently pin the wrong build.
CHROMIUM_REV=$(python3 -c "
import json, glob
p = glob.glob('$HOME/.local/lib/python*/site-packages/playwright/driver/package/browsers.json') \
    or glob.glob('/usr/lib/python3*/site-packages/playwright/driver/package/browsers.json')
d = json.load(open(p[0]))
print(next(b['revision'] for b in d['browsers'] if b['name'] == 'chromium'))
")
FFMPEG_REV=$(python3 -c "
import json, glob
p = glob.glob('$HOME/.local/lib/python*/site-packages/playwright/driver/package/browsers.json') \
    or glob.glob('/usr/lib/python3*/site-packages/playwright/driver/package/browsers.json')
d = json.load(open(p[0]))
print(next(b['revision'] for b in d['browsers'] if b['name'] == 'ffmpeg'))
")

mkdir -p /tmp/pwdl "$PLAYWRIGHT_BROWSERS_PATH"

fetch_and_extract () {   # $1 zip basename, $2 cdn subpath, $3 destination dir
  local zip="/tmp/pwdl/$1.zip" dest="$PLAYWRIGHT_BROWSERS_PATH/$3"
  [ -f "$dest/INSTALLATION_COMPLETE" ] && return 0
  echo "[bootstrap] downloading $1 (resumable, may need more than one call)..."
  wget -c -q -O "$zip" "$CDN/$2"
  unzip -q -o "$zip" -d "$dest"
  touch "$dest/INSTALLATION_COMPLETE"
  rm -f "$zip"          # free the volume immediately, the extract is what matters
  echo "[bootstrap] $1 ready"
}

# Both chromium builds are needed: headless launches use headless_shell, while
# video recording needs the full build. Installing only one fails at launch with
# a misleading "Executable doesn't exist" pointing at the other.
fetch_and_extract "chromium" \
  "chromium/$CHROMIUM_REV/chromium-linux-arm64.zip" "chromium-$CHROMIUM_REV"
fetch_and_extract "chromium-headless-shell" \
  "chromium/$CHROMIUM_REV/chromium-headless-shell-linux-arm64.zip" \
  "chromium_headless_shell-$CHROMIUM_REV"
fetch_and_extract "ffmpeg" \
  "ffmpeg/$FFMPEG_REV/ffmpeg-linux-arm64.zip" "ffmpeg-$FFMPEG_REV"

chmod +x "$PLAYWRIGHT_BROWSERS_PATH/chromium-$CHROMIUM_REV/chrome-linux/chrome" \
         "$PLAYWRIGHT_BROWSERS_PATH/chromium_headless_shell-$CHROMIUM_REV/chrome-linux/headless_shell" \
         "$PLAYWRIGHT_BROWSERS_PATH/ffmpeg-$FFMPEG_REV/ffmpeg-linux" 2>/dev/null || true

echo "[bootstrap] ready. browsers=$PLAYWRIGHT_BROWSERS_PATH chromium=$CHROMIUM_REV"
