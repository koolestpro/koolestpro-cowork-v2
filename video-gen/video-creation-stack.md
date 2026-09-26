# Video Creation Stack — Reference

**Status:** Living reference document, not an auto-triggered skill. Read this yourself, or paste it into a Claude/Codex conversation for context on what's available and why each piece was chosen.

**Last updated:** July 4, 2026 (portability fix + BreezeLoop "Feature" v2 rescue)

---

## 0. What this covers

Everything currently installed or connected for AI video creation: generation, stock footage, sound design, editing, and review. Includes what was evaluated and rejected, and why — so the reasoning doesn't get lost.

**Cross-tool note:** the original `ai-video-generation` and `watch` skills were installed globally in your terminal (Claude Code / Codex CLI). As of this update, **all Cowork-native equivalents live in this same `video-gen` folder**: `video-review.skill`, `stock-footage.skill`, `ai-video-generation.skill`, `heygen-api.skill`, `sound-effects.skill`, and `text-to-speech.skill`. Install any of them via Settings → Capabilities → Skills, or just tell Claude to use the copy in this folder. See §9 for verified status of each.

**Terminal-as-fallback policy:** Cowork's shell tool caps a single command at roughly 45 seconds, which occasionally isn't enough (confirmed case: HeyGen's `/v2/avatars` endpoint, see §1). When a Cowork skill call times out or otherwise "refuses to work" for reasons that look like a sandbox constraint rather than a real error, the fallback is running the exact same underlying script from an actual terminal (Claude Code/Codex), which has no such ceiling. Every skill's `scripts/` folder is the same code either way — nothing terminal-only needs to be maintained separately.

---

## 0.1 Read this before using the pipeline in a *different* Cowork project

**The single most important fact in this document:** the `.skill` files are installed once and become available account-wide, in any Cowork project. **The `.env` file is not** — it only exists inside this specific `video-gen` folder. A skill with no `.env` to read from has no `GROQ_API_KEY`/`OPENAI_API_KEY`/`FREESOUND_API_KEY`/etc. to call with, so if a different Cowork project doesn't have this folder connected, `text-to-speech.skill` and `sound-effects.skill` can't actually run — even though they show up as "installed."

**What happens instead, confirmed live (July 4, 2026):** the user built `BreezeLoop_Video1_Feature_1x1.mp4` / `_9x16.mp4` in what was very likely a different Cowork project/chat without this folder connected. The result had a voiceover, but a different, generic-sounding one — and **no background music at all**. A spectrogram check on the uploaded audio confirmed it: voice energy only, concentrated below ~4kHz with silence gaps between phrases, no continuous broadband/bass content a music bed would leave. The most likely explanation is that without `.env` access, Claude fell back to the already-connected **Higgsfield MCP** for voiceover (a different voice than our OpenAI `nova` + instructions setup) — and since Higgsfield's `generate_audio` explicitly can't do music, and Freesound wasn't reachable without a key, no music got added at all. This is not a bug in the skills — it's a silent capability gap when the folder isn't connected, and the docs didn't warn loudly enough that this would happen.

**To avoid this in any new project:**
1. **Always connect this `video-gen` folder** at the start of any Cowork session that will touch video/audio generation — even a "new" project for something else. The skills are portable; the keys are not.
2. If you want a project to work with a *copy* of `.env` instead (e.g. a separate client folder), copy the file and point `--env` at that copy — don't assume the skill will find keys on its own.
3. **Tell Claude explicitly** to use `text-to-speech.skill` / `sound-effects.skill` from this stack rather than leaving it to pick a tool — that removes the ambiguity that let Higgsfield get used silently.
4. **If a result comes back with a different voice than expected, or missing music/SFX:** that's the signature of this exact issue. Ask directly which tool/skill was actually called, and check `ls` on the connected folder / `grep KEY .env` before assuming something is broken elsewhere.

**Where `.env` has been deployed so far (keep this list current — if a key rotates, update every copy below or they go stale):**
| Project folder | `.env` copied | Notes |
|---|---|---|
| `video-gen` | Source of truth | This is the master copy |
| `dropshipping` | July 5, 2026 | Havenlyte/BreezeLoop ads live here — see `AGENTS.md` and `ads/video-1/SOURCES_and_NOTES.md` |
| `koolestpro-cowork-v2` | July 5, 2026 | Pointer doc at `docs/video-audio-stack-pointer.md`, doesn't touch `CLAUDE.md` |

Confirmed: this project's `SOURCES_and_NOTES.md` in `dropshipping/ads/video-1/` names the exact tool that got silently substituted — "AI TTS via the video-gen creative stack ('Ava'/seed_audio)" is Higgsfield, not our OpenAI/Groq setup, and "Music + SFX: original synthesized in-house (ffmpeg)" is a placeholder tone, not a real Freesound track. Direct confirmation of the failure mode described above, not just a hypothesis.

---

## 1. Generation layer

### inference.sh
- **What:** Pay-per-execution AI runtime. No subscription — prepaid credits, deducted per API call.
- **Terminal:** CLI (`infsh` / `belt`), logged in, small credit balance added. Skill: `ai-video-generation` installed via `npx skills add inference-sh/skills --skill ai-video-generation --agent claude-code` (from the official `inference-sh/skills` repo, not the `skillsh/skills` mirror).
- **Cowork:** inference.sh has a plain key-based REST API (`https://api.inference.sh`, `Authorization: Bearer <key>`) that the CLI itself is built on — no login session needed. `video-gen/ai-video-generation.skill` calls this directly with `INFSH_API_KEY` from `.env`.
- **Covers:** 40+ models across text-to-video, image-to-video, and avatar/lipsync — including HeyGen's own models available through inference.sh's catalog (`heygen/avatar-video`, `heygen/lipsync`), so there are three separate ways to reach HeyGen-style avatar generation (see the HeyGen entry below). Does **not** cover standalone sound effects/music generation for general use — see §3 for why that gap is filled by Freesound instead.
- **Real example apps found via live search:** `pruna/p-video` (cheapest tier, text/image-to-video, 720p/1080p), `alibaba/wan-2-7-t2v` / `alibaba/wan-2-7-i2v`, `klingai/video-v2-6`, `xai/grok-imagine-video`. Always search first though — the catalog changes.
- **Cost discipline:** test new prompts/workflows on the cheapest model in a category first (WAN/P-Video tier runs roughly $0.05–0.11/clip) before spending on Kling/Grok/Veo-tier models.
- **Live generation test (confirmed end-to-end):** ran `pruna/p-video` with the prompt "a small paper boat gently floating on a calm blue pond, soft daylight" — completed in ~14s, billed 13 CPU-seconds, returned a real downloadable video (`output.video`, a direct URL — note the shape isn't always nested under a `uri` key, varies per app). Downloaded and verified as a valid MP4.
- **Finding worth keeping:** inference.sh's own docs disagree with each other on task-status numeric codes (one page says `10` = Failed, another implies `9` = Completed) — the real completed task above had `status: 10` with a valid output and no error. The skill polls for `output`/`error` presence rather than trusting a specific number, which is why it worked despite the doc inconsistency.

### HeyGen — Direct API (pay-as-you-go)
- **What:** Standalone API billing pool, separate from any HeyGen web subscription. Minimum top-up $5.
- **Key:** stored as `HEYGEN_API_KEY` in `video-gen/.env` (real money — see §6).
- **Confirmed balance:** 300 general API credits, plus one-time free testing credits: 3× Avatar IV, 1× B-roll, 3× HyperFrames render, 5× HyperFrames API render, 1× Hyperion render, 3× Video Agent v2, 3× image, 3× video upscale, 3× speech cleanup, 1× podcast, 2× generative element pools.
- **Cowork skill:** `video-gen/heygen-api.skill` wraps the Direct API — quota check, avatar/voice listing, Studio video generation (`POST /v2/video/generate`), status polling. Auth confirmed live: quota + voice listing (2,330 voices) both returned real data.
- **Confirmed broken in Cowork: `GET /v2/avatars`.** Tested at 15s, 40s, and 43s (Cowork's shell tool caps a single command at ~45s) — every attempt timed out, while `/v2/voices` (~3s) and quota both worked fine over the same connection. `avatar_group.list` is fast (<1s) but only returns custom avatar groups (this account has 0). **Practical fallback:** get the avatar_id from the HeyGen dashboard directly, or run the listing from an actual terminal (no ~45s ceiling there).
- **`generate` still untested** — needs a valid avatar_id, which the avatars listing couldn't produce in this session. Auth itself is fully confirmed.
- **Three ways to reach HeyGen now, don't conflate them:**
  1. **HyperFrames MCP connector** (already connected) — bills a HeyGen **web-plan subscription**. `list_projects` confirmed live.
  2. **`heygen-api.skill` (Direct API)** — bills the **prepaid `HEYGEN_API_KEY` pool** described above.
  3. **`ai-video-generation.skill` → `heygen/avatar-video` or `heygen/lipsync` apps** — bills the **inference.sh credit pool** instead.

### Higgsfield — connected, voiceover now a fallback, not primary
- **Status:** MCP connector present in Cowork, free plan (`balance` → 10 credits).
- **Video/image generation:** still gated behind the top-tier Studio subscription for the pay-as-you-go pool — on hold, see §8.
- **Voiceover/TTS — demoted to fallback:** `generate_audio` (model `seed_audio`, ByteDance) still works (0.1 credits/generation) but is no longer the default voiceover tool — the user is moving off Higgsfield generally. **`text-to-speech.skill` (Groq + OpenAI, §3) is now the primary voiceover tool.** Keep Higgsfield in mind only if both Groq and OpenAI are unavailable.
- **Revisit the video/image side if:** volume becomes consistent enough monthly to justify Starter ($15/mo) / Plus ($39/mo) / Ultra ($99/mo).

---

## 2. Stock footage layer

### Pexels
- Free API, no cost, generous limits. Key: `PEXELS_API_KEY`.
- Photo search: `GET https://api.pexels.com/v1/search?query=...` — Video search: `GET https://api.pexels.com/videos/search?query=...` — Auth header: `Authorization: $PEXELS_API_KEY`

### Pixabay
- Free API, no cost. Key: `PIXABAY_API_KEY`.
- Photo search: `GET https://pixabay.com/api/?key=$PIXABAY_API_KEY&q=...` — Video search: `GET https://pixabay.com/api/videos/?key=$PIXABAY_API_KEY&q=...`

**Cowork status:** `stock-footage.skill` confirmed working end-to-end with real keys (both Pexels and Pixabay returned real video results). One sandbox-specific fix was needed: Pexels' host blocks Python's default `urllib` user agent (Cloudflare bot detection, HTTP 403) — the script now sends a normal-looking User-Agent header, same fix the inference.sh wrapper needed.

---

## 3. Sound design layer (voiceover + SFX)

Added after finishing a first BreezeLoop (Havenlyte neck-fan) ad: the raw generation output had video but only a near-silent generated ambient track (-52dB mean volume) — no real voiceover or sound design. This layer fills that gap, and has since moved off Higgsfield for voiceover entirely.

### Voiceover: `text-to-speech.skill` (Groq + OpenAI) — primary tool
- **Why it replaced Higgsfield:** the user is moving off Higgsfield and already runs a Groq + OpenAI + DeepSeek combo in their own app (a speaking-practice feature with Arabic conversation) — this skill wraps the same two providers, billed against the `GROQ_API_KEY`/`OPENAI_API_KEY` already in `.env`, no new signup.
- **Two providers, pick by need:**
  - **OpenAI (`gpt-4o-mini-tts`)** — English, no character-limit chunking to manage, ~$0.015/min, `--instructions` steers tone in plain language ("energetic, upbeat, confident, fast-paced UGC ad read"). **Confirmed working live** — this generated the BreezeLoop v2 voiceover.
  - **Groq (Orpheus models)** — the natural choice for **Arabic** (`canopylabs/orpheus-arabic-saudi`, authentic Saudi dialect, matches what the user's own app already does) or cheap English (`canopylabs/orpheus-v1-english`). $22–40/1M chars, hard 200-char-per-call limit (the script auto-chunks and concatenates). **Setup gotcha (still open):** Groq's Orpheus models require accepting model-specific terms in the console (`https://console.groq.com/playground?model=<model>`). The user reported accepting terms on July 4, 2026, but a live re-test immediately after still returned the same `400 model_terms_required` error. This may just be console→API propagation delay (retry in a few minutes) or a mismatch between the console session's org and the org tied to `GROQ_API_KEY` — worth a quick re-test before assuming it's broken. OpenAI remains the reliable default in the meantime.
- Always `ffprobe` the output for real duration rather than estimating from word count or script length — confirmed repeatedly across both Higgsfield and OpenAI that naive estimates are off.
- Full usage in `text-to-speech.skill`'s `SKILL.md`.

### Voiceover: Higgsfield `generate_audio` — fallback only
- Still works (`seed_audio` model, ~0.1 credits/generation, no key needed, already-connected MCP) but no longer the default — kept only as a fallback if both Groq and OpenAI are unavailable.

### Sound effects / ambience: Freesound.org (`sound-effects.skill`)
- **Why Freesound:** closest audio equivalent to Pexels/Pixabay — free account, simple API-key auth (`Authorization: Token <key>`, no OAuth2 needed for search or downloading the mp3 "preview" files search returns), large community library covering whooshes, UI pops, foley, ambience, risers, etc.
- **Status: confirmed working live.** `FREESOUND_API_KEY` is set in `.env` and a real search (`"whoosh transition swoosh"`, CC0-filtered, sorted by downloads) returned real results with working `download_url`s — used directly in BreezeLoop v2 (see below).
- **License note:** filter with `--license "Creative Commons 0"` for zero-attribution results (used for BreezeLoop v2's whoosh and pop); without the filter most results are Attribution/Attribution-Noncommercial, fine to use but expects a credit if publishing commercially.

### BreezeLoop v2 — full sound design pass (July 4, 2026)
Took the original 15s BreezeLoop hook video and, per the user's request for more energy and real sound design:
1. **Sped up 1.12x** — video via `setpts=PTS/1.12`, original ambient audio via `atempo=1.12` — landing at 13.4s, matched almost exactly to a newly-written, punchier script.
2. **New voiceover** via `text-to-speech.skill`, OpenAI `gpt-4o-mini-tts`, voice `nova`, `--instructions "energetic, upbeat, confident, fast-paced UGC ad read, like an excited creator recommending a product to a friend"` — 13.37s, no freeze-frame extension needed this time since the sped-up video and new VO landed almost exactly together.
3. **Real scene-cut detection** (`ffprobe … select=gt(scene,0.35)`) found the actual transition points in the sped-up video (2.67s, 6.23s, 10.7s) rather than guessing evenly-spaced beats.
4. **Freesound SFX layered at those cuts:** a whoosh (CC0, `florianreichelt`) at each of the three transitions, plus a pop (CC0, `Breviceps`) accenting the final price/CTA reveal.
5. **Mixed** (`amix`): lowered original ambient bed (0.16), VO (1.05), three whoosh instances at their delay points (0.65 each), pop (0.75) — then `loudnorm` (I=-14, TP=-1.5, LRA=11) for final broadcast-consistent levels.
- **Result:** `BreezeLoop_Video1_ProblemHook_VO_v2.mp4`, 13.4s, mean -15.2dB / max -1.4dB — healthy headroom, no clipping, noticeably more energetic pacing than v1 plus real transition SFX instead of VO-only.

### Background music (new capability, Freesound)
- No new key or provider needed — Freesound covers music beds as well as SFX/ambience. Searched `"upbeat background music loop"` filtered to CC0, found `Tropicorp Advertisement` (37.6s, tagged ad/advertisement/corporate/upbeat/happy — a near-perfect generic UGC-ad bed), by `code_box`, CC0.
- **Picking a track:** search with a mood/genre query plus `--license "Creative Commons 0"` and `--duration-max` roughly 2-3x the video length so there's room to trim to a clean segment; corporate/ad-tagged CC0 tracks from prolific uploaders (`code_box`, `EEE3333E`) turned up reliably.
- **Mixing in:** trim/fade the track to the video's exact duration (`atrim` + a 1s `afade=out` right before the end so it doesn't cut abruptly), keep it quiet under the mix (~0.10-0.14 relative volume — it's a bed, not a lead) — same `amix` pattern as the other audio layers.

### BreezeLoop v3 — background music + visual transitions synced to SFX (July 4, 2026)
Per the user's request for background music and transitions that pair with the SFX:
1. **Real scene cuts from v2 (2.67s, 6.23s, 10.7s)** became actual visual transitions instead of hard jump-cuts: split the sped-up video into 4 segments at those points and rejoined with `xfade` (0.25s `hblur` — a quick horizontal motion-blur "whip" — pairs naturally with a whoosh sound, unlike a plain crossfade). Note: chaining `xfade` shrinks total duration by the transition length each time (3 × 0.25s here), so the video came out to 12.67s post-transitions.
2. **Freeze-frame extended** by 0.75s on the final CTA card (same technique as v1) to get back to ~13.43s, matching the voiceover length.
3. **Whoosh timing recalculated** to the new transition windows (each `xfade` reports where in the output timeline its blend actually lands, which shifts slightly earlier than the original cut points as transitions compound) — whooshes now hit at 2.545s / 5.855s / 10.075s instead of the raw v2 cut estimates, so the sound lines up with the actual visual blur, not a stale timestamp.
4. **Full mix:** ambient bed (0.14) + VO (1.05) + 3 whooshes (0.6 each, retimed) + pop accenting the CTA (0.7, at 12.7s) + new background music bed (0.11, faded out over the last second) → `amix` → `loudnorm` (I=-14, TP=-1.5, LRA=11).
- **ffmpeg technique worth keeping:** `ffmpeg -h filter=xfade` lists all ~40 transition names for this ffmpeg build (4.4.2) — some names from other tutorials (`zoomin`) aren't in this build and fail with "Unable to parse option value"; always check the real list rather than assuming a name works, `hblur`/`smoothleft`/`circleopen` etc. are all valid here.
- **Result:** `BreezeLoop_Video1_ProblemHook_VO_v3.mp4`, 13.43s, mean -15.1dB / max -1.2dB — now has a real music bed under the VO/SFX and visual whip-transitions timed to each whoosh instead of static jump cuts.

### BreezeLoop "Feature" v1 → v2 rescue (July 4, 2026) — the portability incident
The user extended the ad with more sales points (new 24.3s script covering bladeless design, neck-wrap, portability, price, and a `shop now at Havenlyte.co` CTA) in what was very likely a different Cowork project — the uploaded `BreezeLoop_Video1_Feature_1x1.mp4` / `_9x16.mp4` had a voiceover but a different voice than our tuned setup, and **no music at all**. See §0.1 for the root cause (folder not connected → no `.env` keys → likely silent fallback to Higgsfield voiceover with no music capability).
- **Diagnosis method:** `ffmpeg showspectrumpic` on the extracted audio confirmed voice-only content (energy under ~4kHz, clear silence gaps between phrases, no continuous broadband bed) before touching anything — worth doing this check whenever "is there music in this" isn't obvious just from `volumedetect`.
- **Fix:** transcribed the existing script via Groq Whisper (`whisper-large-v3`) to recover the exact wording, regenerated a clean voiceover with `text-to-speech.skill` (OpenAI `nova`, same energetic UGC instructions as v2/v3), scene-detected real cuts in the new footage (4.33s / 10.4s / 15.2s / 18.24s, after de-duplicating a noisy detector's near-duplicate hits within ~1s of each other — handheld/product-demo footage throws a lot more low-confidence candidates than a clean 4-beat ad), layered in whoosh SFX at those cuts plus a pop on the price/CTA, added the same Freesound background music bed, froze the last frame by ~1.85s so the extended 26.1s voiceover fits without rushing, and ran `loudnorm`.
- **1x1/9x16 shortcut:** confirmed via `cmp` that both aspect-ratio uploads shared byte-identical audio tracks, so the entire audio mix was built once and remuxed onto each video's picture track separately rather than duplicating the whole pipeline.
- **Result:** `BreezeLoop_Video1_Feature_1x1_v2.mp4` and `_9x16_v2.mp4`, both 26.17s, mean -15.7dB / max -1.5dB.

---

## 4. Editing / assembly layer

### ffmpeg + Claude (primary, free)
- Confirmed present in the Cowork sandbox (`ffmpeg 4.4.2`). Describe the edit in plain language (cuts, transitions, captions, pacing, audio mixing/normalization) and Claude writes/runs the ffmpeg pipeline directly. This is also how voiceover gets mixed in and how the sound-effects skill's downloads get layered onto a cut.
- Best for: one-off videos, testing a style before scaling it.

### Shotstack (fallback, pay-as-you-go)
- JSON-based cloud rendering API. Free sandbox for testing, pay-as-you-go from ~$0.40/min, no forced subscription.
- Not yet set up — revisit if the ffmpeg-in-chat approach starts feeling limiting at scale. Placeholder `SHOTSTACK_API_KEY` line sits commented out in `.env`.

### CapCut skill (mcpmarket.com) — evaluated, rejected
- Unofficial third-party wrapper, requires paying for CapCut Pro/Business to get full functionality, defeating the point. **Decision: not installed.**

---

## 5. Video analysis / review layer

### `watch` skill (bradautomates/claude-video) — terminal (Claude Code / Codex)
- Downloads via `yt-dlp`, extracts frames, pulls a timestamped transcript (captions first, Whisper fallback). MIT license, 2.5k+ GitHub stars. Installed at `~/.claude/skills/watch` and/or `~/.codex/skills/watch`.

### `video-review.skill` — Cowork-native equivalent
- `scripts/prepare_video.py` downloads via `yt-dlp` (auto-installed via pip if missing, invoked as `python3 -m yt_dlp` to dodge PATH issues), pulls captions first and falls back to Whisper (Groq/OpenAI key via `--env video-gen/.env`) only if none exist, samples frames via `ffmpeg`.
- **Sandbox-specific fix baked in:** YouTube needs a JS runtime to solve signature challenges; yt-dlp only auto-enables `deno` (usually absent), but Cowork ships Node — the script passes `--js-runtimes node`.
- **Verified working end-to-end:** real YouTube download + caption extraction + timestamped transcript + frame sampling, all confirmed live. Also used informally this pass via plain `ffmpeg`/`ffprobe` to inspect the uploaded BreezeLoop video directly (local file, no download needed).
- **Network note:** some direct-CDN hosts (e.g. raw `googleapis.com` storage links) return 403 from bot protection — doesn't affect real yt-dlp-supported sites, which set proper headers.

---

## 6. Credential hygiene

All keys live in `video-gen/.env` — the connected folder is the persistent, Cowork-accessible equivalent of the terminal's local `.env`:

```
INFSH_API_KEY=...       # inference.sh — REAL MONEY
HEYGEN_API_KEY=...      # HeyGen Direct API — REAL MONEY
PEXELS_API_KEY=...      # free
PIXABAY_API_KEY=...     # free
GROQ_API_KEY=...        # free tier / pay-per-use — Whisper fallback + text-to-speech.skill (accept Orpheus model terms in console first)
OPENAI_API_KEY=...      # pay-per-use — Whisper fallback + text-to-speech.skill (primary voiceover, no terms gotcha)
FREESOUND_API_KEY=...   # free — confirmed working, real searches return results
DEEPSEEK_API_KEY=...    # not currently used by any video skill (used elsewhere in the user's own app)
# SHOTSTACK_API_KEY=    # only needed if the ffmpeg-in-chat approach needs to scale
```

`INFSH_API_KEY` and `HEYGEN_API_KEY` have real money behind them — this file sits in a connected folder rather than a public repo, which is the right place for it, but it's still worth keeping this folder itself out of anything that gets shared or synced publicly. The Higgsfield voiceover fallback needs no key at all (uses the connected MCP connector directly). Regenerate any key from its dashboard if you're ever unsure it's still private.

**Groq console step — reported done, not yet reflected on the API side:** the user accepted the Orpheus model terms at `https://console.groq.com/playground?model=canopylabs/orpheus-v1-english` on July 4, 2026, but a live re-test right after still returned `400 model_terms_required`. Likely a propagation delay or an org mismatch between the console session and `GROQ_API_KEY` — retry `text-to-speech.skill --provider groq` in a few minutes before assuming something's actually wrong.

---

## 7. Suggested pipeline (putting it together)

1. **Source generation** — `ai-video-generation.skill` (inference.sh) or `heygen-api.skill` (HeyGen Direct API) or the HyperFrames MCP connector (bills web plan instead)
2. **B-roll** — `stock-footage.skill` (Pexels/Pixabay), free, working
3. **Voiceover** — `text-to-speech.skill` (Groq or OpenAI), primary; Higgsfield `generate_audio` as fallback only
4. **Sound effects, ambience, and background music** — `sound-effects.skill` (Freesound), free, confirmed working for SFX, ambience, and full music beds
5. **Assembly/mixing** — describe the edit to Claude, ffmpeg does the cuts, speed changes, `xfade` visual transitions synced to SFX, VO mixing, SFX/music layering, and loudness normalization; Shotstack if it needs to scale later
6. **Review** — `video-review.skill` before publishing
7. **Iterate** — show Claude reference videos in the style you're chasing; that's the ongoing style-transfer mechanism until/unless a formal brief skill gets built later

---

## 8. Open / deferred decisions

- **Higgsfield video/image generation:** on hold until pay-per-use makes sense or volume justifies a subscription. Voiceover moved off Higgsfield entirely to `text-to-speech.skill`, see §3.
- **Formal "video-production-brief" skill:** deliberately not built yet — this document is the interim reference instead.
- **HeyGen Direct API `generate` still untested end-to-end:** blocked on getting a valid avatar_id, since `/v2/avatars` can't be listed inside Cowork's command-time budget (see §1). Give Claude an avatar_id from the HeyGen dashboard (Content → Avatars) to unblock a real test, or try listing avatars from a terminal instead.
- **Groq TTS still blocked despite reported terms acceptance** (see §6) — re-test in a few minutes in case it's a propagation delay; OpenAI works without it in the meantime.

---

## 9. Cowork setup status (as of July 4, 2026)

What's actually confirmed working in *this* environment, checked live:

| Piece | Status |
|---|---|
| HeyGen HyperFrames MCP connector | **Live** — `list_projects` responded (0 projects yet) |
| Higgsfield MCP connector | **Live** — `balance` responded (10 credits, free plan); `generate_audio`/`list_voices` confirmed working with a real successful voiceover generation |
| ffmpeg | **Present** in sandbox (4.4.2) |
| yt-dlp | Not pre-installed, auto-installs via pip in-session; YouTube needs `--js-runtimes node` (handled automatically) |
| `INFSH_API_KEY` | **Set in `.env`, fully confirmed** — real paid generation ran successfully end-to-end |
| `HEYGEN_API_KEY` | **Set in `.env`, auth confirmed live** (quota + voices confirmed) — `generate` untested, blocked on avatar_id |
| `PEXELS_API_KEY` / `PIXABAY_API_KEY` | **Set in `.env`, confirmed working** — real search results returned |
| `GROQ_API_KEY` / `OPENAI_API_KEY` | Set in `.env`, wired into `video-review.skill`'s `--env` flag and `text-to-speech.skill`. OpenAI TTS **confirmed working live**; Groq TTS still returns `400 model_terms_required` even after the user reported accepting terms — retest, likely propagation delay |
| `FREESOUND_API_KEY` | **Set in `.env`, confirmed working live** — real searches (SFX, and now full background music) returned real CC0 results, used directly in BreezeLoop v2/v3 |
| `video-review.skill` | **Built + tested end-to-end** |
| `stock-footage.skill` | **Built + tested end-to-end** with real keys |
| `ai-video-generation.skill` | **Built + tested end-to-end** — real paid generation confirmed working |
| `heygen-api.skill` | **Built, auth tested** (quota + voices) — `generate` blocked on avatar_id |
| `sound-effects.skill` | **Built + tested end-to-end** with real key — used live in BreezeLoop v2/v3 for SFX and background music |
| `text-to-speech.skill` | **Built + tested end-to-end** — OpenAI confirmed live; Groq still blocked on `model_terms_required` despite reported terms acceptance |

This `video-gen` folder is the persistent home for the Cowork side of the stack — reconnect it at the start of any Cowork session that needs these pieces. Sample outputs: `infsh_test_paper_boat.mp4` (inference.sh test), `BreezeLoop_Video1_ProblemHook_VO_v1.mp4` (first voiceover pass, Higgsfield), `BreezeLoop_Video1_ProblemHook_VO_v2.mp4` (sped-up + OpenAI voiceover + Freesound SFX), and `BreezeLoop_Video1_ProblemHook_VO_v3.mp4` (adds a Freesound background music bed and `xfade` visual transitions synced to the SFX, shared alongside this doc).
