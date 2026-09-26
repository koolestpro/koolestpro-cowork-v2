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

**⚠️ Updated 2026-09-08 — don't use `~/.cache` above, it isn't reliable storage here.** `$HOME` (`/sessions/<session>`) lives on its own small ~9.8GB volume that runs close to full as a matter of course (separate from `/`, which has room, and separate from the much larger mounted-folders volume). `~/.cache/ms-playwright/` was observed to get wiped entirely mid-session under disk pressure — right after a clean install and a successful test launch. Two changes to the recipe above:

1. **Only download/extract `chromium-headless-shell-linux-arm64.zip`.** A default `chromium.launch()` (headless=True) uses the dedicated `chromium_headless_shell-<BUILD>` build, not the full `chrome-linux/chrome` binary, so the ~275MB-unpacked full `chromium` package is never actually needed for this project's headless capture scripts — skip downloading `chromium.zip` entirely and save the space.
2. **Extract to `$HOME/tmp/pw-browsers/chromium_headless_shell-<BUILD>/` instead of `~/.cache/...`**, and export `PLAYWRIGHT_BROWSERS_PATH=$HOME/tmp/pw-browsers` before every launch (alongside the `LD_LIBRARY_PATH` export below) — that env var relocates Playwright's whole browser cache. `$HOME/tmp/` was observed to survive across calls where `~/.cache/` did not.

Before any of this, reclaim space: `rm -rf ~/tmp/playwright-download-*` (a bash-ceiling-killed `playwright install chromium` leaves large partial zips there) and `pip cache purge`. Check `df -h /sessions` specifically (not `df -h /`, a different and much less constrained volume) if a download or extraction fails with "No space left on device".

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

---

# capture_page.py — Lovable / Figma Make handoff (2026-09-13)

Takes a finished page out of Lovable, Figma Make, v0 / Bolt / Onlook, or the fallback flow and
returns the exact screenshots this pipeline's mockup, carousel and recap builders expect. The
handoff is just a screenshot, so there is no lock-in. See
`docs/system/rebuild-tooling-and-quality.md` for where the redesign gets made and why.

```bash
# published Lovable / Figma Make URL
python3 capture_page.py --url https://my-app.lovable.app --brand getfit --device both --full

# a local Lovable GitHub export build, or any local HTML
python3 capture_page.py --file /path/to/dist/index.html --brand getfit --full
```

Outputs to `outputs/cro-fixes/_capture/<brand>/`:
- `<brand>-mobile.png` — 390x844 @2 (780x1688), the phone screen; drops into `build_device_still.py`
- `<brand>-full.png` — full page @2 (tall shot for strips / mobile-strip), with `--full`
- `<brand>-desktop.png` — 1440x900 @2, with `--device desktop` or `both`

It reuses `screenshot.py`'s popup handling, forces `reduced_motion="reduce"`, and prints a
`CAPTURE_SUMMARY {json}` line for the next step. Run it with the same Python that has Playwright
(the project venv) — set `LD_LIBRARY_PATH` / `PLAYWRIGHT_BROWSERS_PATH` exactly as for
`screenshot.py` above.
