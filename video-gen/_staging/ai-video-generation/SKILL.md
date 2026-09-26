---
name: ai-video-generation
description: Generate AI video, image, and audio using inference.sh's pay-per-execution API — text-to-video, image-to-video, avatar/lipsync (including HeyGen models available through inference.sh's own catalog), and 40+ other models across providers (Kling, Wan/Alibaba, Grok, Pruna, etc.), billed against the user's prepaid inference.sh credit balance. Use this whenever the user wants to generate a video clip, animate an image, create a talking-head/avatar video, or asks to "generate a video," "animate this image," "make an AI clip," "text to video," "image to video," or similar, in this Cowork sandbox (not the terminal `infsh`/`belt` CLI, which is a separate setup — this skill is the direct-API equivalent that works without any CLI install or login). Always search for the right app first rather than guessing an app id, since the catalog changes.
---

# AI Video Generation (inference.sh, Cowork-native)

## Why this exists

The terminal-side `ai-video-generation` skill wraps the `infsh`/`belt` CLI, which needs an interactive login session that doesn't carry over into a Cowork sandbox. This skill does the same job by calling inference.sh's REST API directly with an API key — no CLI, no login, works standalone in any Cowork session as long as the key is available.

## Auth

Reads `INFSH_API_KEY` from `video-gen/.env` (or `INFERENCE_API_KEY` — either name works, matching what's actually in the environment/`.env`). If the connected folder isn't `video-gen`, pass `--env <path-to-.env>` explicitly. If neither is found, ask the user for the key — don't fabricate one or silently skip the auth header, since generation calls will just fail with a 401.

## Cost discipline (read before running anything)

**This is real money**, not a free tier like the stock-footage/video-review skills. Prepaid credits are deducted per call. Before generating:

1. **Search first, don't guess app IDs.** The catalog changes and guessing wastes a call. Run `search` and pick from real results.
2. **Test cheap before expensive.** The WAN/P-Video tier (`pruna/p-video`, `alibaba/wan-2-7-*`) runs roughly $0.05–0.11/clip — use those to validate a prompt/workflow before spending on a Kling/Grok/Veo-tier model for the final output.
3. **Tell the user roughly what a call will cost before running it**, if you can find pricing info (check the app's page or ask if unsure), especially for anything beyond the cheap tier. Don't burn credits on a guess when a quick confirmation costs nothing.
4. **Don't loop-retry expensive calls.** If a generation fails, check `error` in the response before blindly re-running it — re-running a failed $2 call three times because of a bad prompt is an easy way to waste money for no reason.

## Running it

```bash
python3 scripts/infsh.py --env /path/to/video-gen/.env search "<what you need>"
```

Returns real app identifiers (`namespace/name`) with descriptions — read the description to check what inputs it expects before running it (e.g. does it want `prompt`, or `image` + `prompt`, or `image` + `audio`).

```bash
python3 scripts/infsh.py --env /path/to/video-gen/.env run <namespace/name> --input '{"prompt": "..."}'
```

- Blocks and polls until the task has an `output` or `error` (default: every 5s, up to 5 minutes — tune with `--poll-interval`/`--poll-max` for longer jobs).
- Use `--no-wait` to get a task id back immediately instead (useful for long renders) — check on it later with `status`.
- `--setup '<json>'` for apps with setup parameters (e.g. picking a specific sub-model/variant).

```bash
python3 scripts/infsh.py --env ... status <task_id>
python3 scripts/infsh.py --env ... cancel <task_id>
```

### Feeding it a local image/audio file (image-to-video, lipsync, avatar apps)

Most of these apps take a `uri` for image/audio inputs, not raw bytes — upload first:

```bash
python3 scripts/infsh.py --env ... upload ./portrait.jpg
# -> {"uri": "https://..." or "inf://files/..."}
python3 scripts/infsh.py --env ... run heygen/avatar-video --input '{"image": "<uri>", "text": "hello there"}'
```

### Downloading the result

The completed task's `output` object contains URIs to the generated file(s) (shape varies per app — usually something like `output.video.uri` or `output.image.uri`). Grab it with:

```bash
python3 scripts/infsh.py --env ... download "<uri>" ./output.mp4
```

## Confirmed working end-to-end (July 3, 2026)

A real test generation ran successfully against `pruna/p-video`: `run pruna/p-video --input '{"prompt": "a small paper boat gently floating on a calm blue pond, soft daylight"}'` completed in ~14 seconds, billed 13 CPU-seconds, and returned `"output": {"seed": null, "video": "https://cloud.inference.sh/app/files/..."}`. Note the output shape here is a bare URL string under `video`, not nested under a `uri` key — confirms the "shape varies per app" warning above is real, don't assume a fixed output schema across apps. Also confirmed: this API's own numeric task-status codes are inconsistent across inference.sh's own docs pages (one page lists 10 as "Failed", another as "Completed") — the completed task above actually had `status: 10` with a valid output and no error, which is exactly why this script polls for `output`/`error` presence rather than trusting a specific status number. Don't "fix" that to check for a specific numeric status later without re-verifying against a live task first.

## Terminal fallback

If a call from this skill hangs, times out, or otherwise "refuses to work" in the Cowork sandbox (its shell tool caps a single command around 45 seconds, which can be too short for large/slow responses), the exact same `scripts/infsh.py` runs fine from an actual terminal with no such ceiling — same `--env` flag, same everything. Unzip the `.skill` file or grab the script from `video-gen/_staging/ai-video-generation/scripts/infsh.py` if a terminal fallback is needed.

## Known-good app examples (verified live, July 2026 — always re-search before relying on these, the catalog moves)

| Use case | App id | Notes |
|---|---|---|
| Cheap text/image-to-video | `pruna/p-video` | 720p/1080p, audio support, cheapest tier |
| Text-to-video | `alibaba/wan-2-7-t2v` | up to 15s, 720p/1080p |
| Image-to-video | `alibaba/wan-2-7-i2v` | first/last frame, video continuation |
| Higher-end video w/ native sound | `klingai/video-v2-6` | text-to-video and image-to-video |
| Talking avatar (HeyGen, via inference.sh) | `heygen/avatar-video` | photo/digital avatars, up to 4K — a second way to use HeyGen tech, separate from the direct HeyGen API key/skill |
| Lip-sync existing video to new audio (HeyGen) | `heygen/lipsync` | speed/precision modes |
| Video-to-video / lipsync (non-HeyGen) | `pixverse-lipsync`, `latentsync-1-5` | alternatives if HeyGen-branded apps aren't wanted |

## Where the API differs from the terminal CLI

- No `infsh login` step — the key goes straight in the `Authorization: Bearer` header.
- No local credit-balance command; check spend via inference.sh's dashboard (Settings → Billing) since there's no confirmed free balance-check REST endpoint as of this writing — don't assume one exists without checking `https://inference.sh/docs/api/rest/billing` first if you need it.
