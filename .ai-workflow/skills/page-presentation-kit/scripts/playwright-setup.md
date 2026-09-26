# screenshot.py — real mobile screenshots (Playwright)

Captures a real mobile-viewport screenshot of a live URL or local HTML file. Used for before/after CRO visual evidence — see `koolestpro-cro-content-maker-skill-e`.

## One-time environment setup (this sandbox is ARM64 — needs two workarounds)

Playwright's own `playwright install chromium` downloader is **not resumable** and this sandbox's bash tool has a hard ~45s ceiling per call, so a single `playwright install chromium` call usually gets killed mid-download. Workaround: download the zip directly with `curl -L -C -` (which the CDN does support resuming, unlike Playwright's built-in downloader) and extract it into Playwright's cache path yourself.

```bash
pip install playwright --break-system-packages
python3 -m playwright --version   # confirm install

# Find the exact build URL + version from a first (likely killed) attempt:
#   python3 -m playwright install chromium
# It prints e.g. "...builds/chromium/1228/chromium-linux-arm64.zip" and
# "...builds/chromium/1228/chromium-headless-shell-linux-arm64.zip" — note the build number (1228 here, will change over time).

# Download both directly (resumable, single call usually enough for each):
curl -L -C - -o chromium.zip "https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/<BUILD>/chromium-linux-arm64.zip"
curl -L -C - -o headless-shell.zip "https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/<BUILD>/chromium-headless-shell-linux-arm64.zip"

# Extract into Playwright's expected cache locations:
mkdir -p ~/.cache/ms-playwright/chromium-<BUILD> && cd ~/.cache/ms-playwright/chromium-<BUILD> && unzip -q /path/to/chromium.zip && touch INSTALLATION_COMPLETE
mkdir -p ~/.cache/ms-playwright/chromium_headless_shell-<BUILD> && cd ~/.cache/ms-playwright/chromium_headless_shell-<BUILD> && unzip -q /path/to/headless-shell.zip && touch INSTALLATION_COMPLETE
```

**Missing shared library:** the binary needs `libXdamage.so.1`, which isn't installed and there's no root/sudo in this sandbox. `apt-get download` (not `install`) works without root — it just fetches the `.deb` to the current directory:

```bash
apt-get download libxdamage1
mkdir -p extracted && dpkg-deb -x libxdamage1_*.deb extracted
export LD_LIBRARY_PATH=/full/path/to/extracted/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH
```

Set that `LD_LIBRARY_PATH` export before every `python3 screenshot.py ...` call (bash calls don't share env between calls, so it has to be re-exported each time, or baked into a wrapper script).

## Known site-specific patch made to the uploaded script

The original script used `wait_until="networkidle"` for live URLs, which times out (30s) on sites with a persistent connection (live-chat widgets, analytics beacons, etc. — e.g. v1ce.co never goes network-idle because of its chat widget). Patched to try `networkidle` with a short 12s timeout first, falling back to `wait_until="load"` + a 1.5s settle delay. This is now the default behavior in this copy of the script.

## Usage (unchanged from the original tool doc)

```bash
python3 screenshot.py "https://example.com/product/xyz" "before.png" --clean
python3 screenshot.py "/path/to/rebuild.html" "after.png" --file --full-page
```
