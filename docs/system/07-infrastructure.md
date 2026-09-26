# 07 — Infrastructure

**Part of** [`SYSTEM-MAP.md`](../../SYSTEM-MAP.md). Live numbers in `SYSTEM-STATUS.html`.

---

## What it is for

Everything the other six run on: the reusable scripts, the scheduling, the credentials, the spend caps, and the environment limits that shape what is even possible. Most of the hard-won knowledge in this project is really knowledge about this layer.

---

## What is in it

**`.ai-workflow/tools/`** — 51 Python scripts plus helpers. Roughly four families:

| Family | Examples |
|---|---|
| Distribution chain | `harvest_content.py`, `harvest_store_template.py`, `qa_check.py`, `populate_sheet.py`, `feed_linkedin.py`, `feed_media.py`, `append_sheet_rows.py`, `sort_distribution_queue.py`, `sync_content_system.py` |
| Export and capture | `export_tip_slides.py`, `export_static_images.py`, `screenshot.py`, `nav_click_test.py`, `upload_assets.py` |
| Lead-gen | `browseract_client.py`, `browseract_koolestflow_bridge.py`, `ad_library_koolestflow_bridge.py`, `apify_client.py`, `koolestflow_client.py`, `lead_playbook.py`, `leadgen_run.py`, `ingest_browseract_leads.py`, `import_pending_push.sh` |
| Per-build one-offs | `build_*_tip.py`, `patch_v2_*.py`, `register_*.py`, `update_social_content_*.py` |

**`.ai-workflow/skills/`** — three project-local skill copies: `koolestpro-trend-radar`, `page-presentation-kit`, `static-ad-image`.

**`.ai-workflow/project-constitution.md`** — the canonical code patterns (capture functions, div-balance checks) that task specs pull from.

**15 scheduled tasks.** Weekly shape:

| Day | Time | Task |
|---|---|---|
| Mon | 07:51 | `koolestpro-weekly-distribution-assembly` |
| Mon | 08:18 | `koolestpro-target-pool-refresh` (biweekly) |
| Mon | 08:49 | `koolestpro-replo-cache-staleness-check` (now runs `audit_mobile_strips.py`) |
| Tue | 09:05 | `koolestpro-browseract-weekly` |
| Wed | 09:00 | `koolestpro-adlibrary-weekly` |
| Wed | 09:21 | `koolestpro-weekly-template-build` |
| Fri | 08:51 | `koolestpro-trend-radar-weekly` — **disabled** |
| Fri | 09:04 | `koolestpro-static-ad-weekly` |
| Fri | 09:28 | `koolestpro-tips-weekly` |
| Sat | 09:09 | `koolestpro-template-showcase-weekly` |
| Sun | 09:12 | `koolestpro-weekly-cro-fix` |
| every 2 days | 09:35 | `koolestpro-distribution-health-check` |

Plus three disabled or unrelated: `shopify-cro-job-alerts`, `abuzaid-weekly-post-drafts`, `abuzaid-saturday-batch`.

**Credentials in `.env`** (names only, never values): `APIFY_*`, `BROWSERACT_*`, `DEEPSEEK_*`, `FREESOUND_API_KEY`, `GOOGLE_OAUTH_*`, `GROQ_API_KEY`, `HEYGEN_API_KEY`, `INFSH_API_KEY`, `KOOLESTFLOW_*`, `OPENAI_API_KEY`, `PEXELS_API_KEY`, `PIXABAY_API_KEY`, `TIKTOK_*` (production and sandbox), `X_BEARER_TOKEN`.

**Spend ledgers:** `trend-radar-spend-ledger.json`, checked **before** every paid call rather than after.

---

## The environment limits, which are load-bearing

These are not trivia. Most bugs in this project's history trace to one of them.

**A cloud bash call is killed near 178 seconds.** Not the ~45s quoted in older parts of `CLAUDE.md`, and nowhere near the 8-9 minutes an old task prompt assumed. Both numbers appear in the docs because both were believed at different times; 178s is the measured one.

**Background processes do not survive between calls.** Each call gets a fresh PID namespace. `nohup ... &` is silently reaped, and `pgrep -f <pattern>` matches the polling command's own command line, cheerfully reporting a dead process as alive. There is no fire-and-poll escape hatch. Anything slower than one call has to checkpoint and resume, which is exactly why `leadgen_run.py` exists.

**Playwright works on this ARM64 sandbox.** Recipe in `.ai-workflow/tools/README.md`; `bootstrap_env.sh` is the idempotent setup. `export LD_LIBRARY_PATH=$HOME/pw/xd/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH` first.

**`device_bash` is a Linux VM, not the real Mac.** No launchd from there. This is why the KoolestFlow importer had to be a real launchd job on Ridwan's own machine.

**Two scheduled triggers previously became unreachable** from later sessions and had to be recreated as `-v2`. Recorded so a vanished task is recognised as a known failure mode rather than a mystery.

---

## How authoring works

CRO Fix rebuilds and redesigns of real businesses are built privately in an external page builder (Lovable/Figma Make/Claude Design/v0) that Claude drives; everything else (Tips, Static Ad pages, Template Showcase pages, store templates) is authored by Claude here. See "AI Workflow Architecture" and "QUALITY RATCHET" in the parent `CLAUDE.md`.

**Claude owns end-to-end:** content strategy, visual design decisions, copy, structure, HTML/CSS/JS, export-ready QA, final approval.

**Use a script when one exists:** `build_split_page.py`, `build_device_still.py`, `build_caraway_*.py`, the region-swap Tips build — accept their output. For authored HTML, author it here.

**Delegation is the exception, not the default:** only for purely mechanical, fully-specified, high-volume scaffolding where the intent is pinned down and no script exists. Say **"delegate this one"** explicitly; otherwise Claude writes it.

To have Claude write it directly (the standing default): just build. No special phrase needed.

---

## State

**Live:** 12 of 15 scheduled tasks. All 51 tools. Playwright. Claude authors output HTML directly (delegation only on explicit request).

**Disabled:** `koolestpro-trend-radar-weekly` (see [01](01-content-production.md)), `shopify-cro-job-alerts`, and the two Abuzaid tasks, which belong to a different project entirely.

**Has nothing left to watch:** `koolestpro-replo-cache-staleness-check` was built to watch `replo-pages-cache/`, which is retired. It has been repurposed to run `audit_mobile_strips.py`, but its name and description still describe the old job. Worth renaming so it does not read as stale.

**Exhausted:** gpt-image credits on both OpenAI keys, and Cloudinary's free AI image quota. The standing protocol is a prompt-pack handoff.

---

## Rules

| Rule | Where |
|---|---|
| Check the spend ledger **before** a paid call, never after. | Trend Radar section |
| Total X spend, posting and reads combined, stays under ~$5/month without explicit say-so. | same |
| gpt-image: one call per bash command, always `--quality low`, always `1024x1536`. Text goes in the prompt with "reading exactly:". PIL must never draw ad copy. | Static Ad "GENERATION METHOD" |
| Static Ads default to a prompt pack (image API only when Ridwan asks). Other streams: gpt-image → Cloudinary generate-image (50/mo free) → builder image gen for rebuild heroes → prompt pack. Never silently spend elsewhere; inference.sh only if named. | "NO IMAGE CREDITS" |
| Task specs, when delegation IS used, are self-contained. `CLAUDE.md` and the operating plans are excluded from auto-inlining on purpose; distil the rules that matter into the spec's own `RULES:` section. | "Running a delegated build" |
| Verify div balance and run a live Playwright click-through after any HTML region-swap. A lazy regex once left orphaned markup that broke navigation invisibly. | "V2 Density" |
| Scratch and intermediate files may be deleted freely without asking. If `rm` fails with "Operation not permitted," use the file-delete-permission tool. | CORRECTED v6 |
| Keep the instruction surface under budget: `AGENTS.md` 6 KiB (injected every request), `CLAUDE.md` 40 KiB, `SYSTEM-MAP.md` 16 KiB. `build_system_status.py` flags any regrowth. Trim, or move detail to a scoped doc — never let the rulebook regrow. | "Context budget" section of `SYSTEM-STATUS.html` |

---

## Known gaps

- **The ~45s vs 178s discrepancy is still in the docs.** Several `CLAUDE.md` sections quote the old figure. Harmless where it makes a run more conservative, misleading where someone reasons from it.
- **51 scripts with no index.** Several are single-build one-offs that will never run again (`_kura_backfill.py`, the `patch_v2_*` family, `build_bebemoss_arrows.py`). Nothing distinguishes those from the canonical reusable tools except reading them.
- **No dependency manifest for the Python side.** `package.json` covers Node; the Python tooling relies on whatever `bootstrap_env.sh` installs.
- **One scheduled task's name no longer matches its job** (the replo cache check).
- **No alerting.** A disabled task, a stalled launchd importer or a silent skip is only visible if someone looks. `SYSTEM-STATUS.html` and its Monday regeneration are the compensating control, and they are a dashboard rather than an alert.
