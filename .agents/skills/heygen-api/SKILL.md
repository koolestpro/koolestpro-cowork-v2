---
name: heygen-api
description: Generate talking-avatar videos and manage HeyGen assets directly through HeyGen's pay-as-you-go Direct API, billed against the user's prepaid HEYGEN_API_KEY balance — separate from the HyperFrames MCP connector, which bills a HeyGen web-plan subscription instead. Use this whenever the user wants to create an avatar/talking-head video via HeyGen specifically (not a generic "make a video" request — that's ai-video-generation), check their HeyGen credit balance, or browse HeyGen avatars/voices, and they want it billed to their own API key rather than a web plan. Trigger on "HeyGen," "avatar video," "talking head video with my HeyGen key," "check my HeyGen credits/quota," or similar.
---

# HeyGen Direct API (Cowork-native)

## Why this exists, and why it's separate from the MCP connector

There are two different ways to reach HeyGen from this Cowork session, and they bill differently:

1. **HyperFrames MCP connector** (already connected) — bills against a HeyGen **web-plan subscription**. Good for HyperFrames-style programmable video projects, but requires an active paid web plan.
2. **This skill (Direct API)** — bills against the **prepaid `HEYGEN_API_KEY` credit pool** (pay-as-you-go, $5 minimum top-up, no subscription). Use this whenever the user wants to spend from that pool instead of a web plan.

Don't conflate the two — if the user says "use my HeyGen API key" or "use my API credits," that means this skill, not the MCP connector.

## Auth

Reads `HEYGEN_API_KEY` from `video-gen/.env` (pass `--env <path>` if the connected folder isn't `video-gen`), or the environment. Ask the user for the key if neither is found — don't proceed without it, since every call needs it.

## Cost discipline

Real money, prepaid. Before generating:

1. Check `quota` first if it's been a while — confirms the key still works and shows exactly what free/paid pools remain (the account had 300 general API credits plus several one-time free pools as of setup: 3x Avatar IV, 1x B-roll, 3x HyperFrames render, 5x HyperFrames API render, 1x Hyperion render, 3x Video Agent v2, 3x image, 3x video upscale, 3x speech cleanup, 1x podcast, 2x generative element pools — spend the free pools before the general 300 credits where applicable).
2. Confirm the avatar_id/voice_id are right before generating — a wrong ID either fails outright (fine, no cost) or produces a video with the wrong avatar/voice (costs credits for a throwaway result). Look them up with `avatars`/`voices` first if unsure, don't guess IDs.
3. Tell the user what's about to be spent before calling `generate` for anything beyond a trivial test, and don't retry a failed generation blindly — check the error first.

## Commands

```bash
python3 scripts/heygen.py --env /path/to/video-gen/.env quota
```
Free to call, always safe to run to sanity-check the key.

```bash
python3 scripts/heygen.py --env ... voices --limit 10 --lang English
```
Lists voices (2000+ total in this account as of testing — always pass `--limit` and filter by `--lang` rather than dumping the whole list).

```bash
python3 scripts/heygen.py --env ... avatars --limit 10
```
**Confirmed broken in Cowork (July 3, 2026):** `/v2/avatars` times out consistently in this sandbox — tested at 15s, 40s, and 43s (Cowork's shell tool caps a single command around 45s), every attempt failed with a connection timeout, while `/v2/voices` (2,330 voices) and the quota endpoint both returned in a few seconds over the same connection. This isn't a bug in the script, it's a real limitation of the Cowork sandbox's request budget against what appears to be a genuinely large/slow response for this account. **Don't keep retrying it in Cowork** — it will keep timing out. Use one of these instead:
- Ask the user for the avatar_id directly (fastest — they can copy it from the HeyGen dashboard's Avatars page).
- **Terminal fallback:** if the user has `infsh`/terminal access, running the same `curl -H "x-api-key: $HEYGEN_API_KEY" https://api.heygen.com/v2/avatars` from an actual terminal has no ~45s ceiling and may simply take longer to complete rather than fail outright — worth trying there if the avatar_id truly isn't known any other way.
- `avatar_group.list` is fast (confirmed <1s) but only returns custom-created avatar groups, not the full public catalog — worth checking first in case the user already has a custom avatar/group set up, since that response is small.

```bash
python3 scripts/heygen.py --env ... generate --avatar-id <id> --voice-id <id> --text "what the avatar should say" --title "my video"
```
Kicks off a Studio video render (text script + voice, driving an avatar) via `POST /v2/video/generate`. Returns a `video_id`. This is the standard avatar-talks-a-script flow — for audio-driven lipsync, digital-twin/Avatar IV, or other engines, check `https://docs.heygen.com/reference/create-an-avatar-video-v2` for the fuller `video_inputs` schema (this wrapper covers the common case, not every parameter).

```bash
python3 scripts/heygen.py --env ... status <video_id>
python3 scripts/heygen.py --env ... wait <video_id>     # polls until completed/failed
```
`status` checks once; `wait` polls every 10s (tune with `--interval`/`--max-polls`) until the render finishes, then prints the result including the final video URL.

## Terminal fallback

Cowork's shell tool caps a single command around 45 seconds. `/v2/avatars` has been confirmed to exceed that ceiling every time it's been tried here (see above) — the same `scripts/heygen.py` (or a plain `curl`) run from an actual terminal has no such ceiling and may just take longer rather than fail outright. If any call in this skill times out in Cowork, that's the fallback: same script, same `.env`, run it from the terminal instead.

## Reference

- Full API reference: https://docs.heygen.com/reference
- This wrapper covers: quota, voices, avatars, Studio video generation (text+avatar), status/wait. It does NOT cover Avatar IV audio-driven generation, digital-twin creation, templates, or webhooks — for those, either extend `scripts/heygen.py` following the same auth pattern (`x-api-key` header, same base URL) or call the relevant endpoint directly with curl using the key from `.env`.
