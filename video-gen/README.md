# video-gen

Persistent home for the Cowork side of Ridwan's video creation stack (see
`video-creation-stack.md` for the full reference doc). Connect this folder at
the start of any Cowork session that needs it — the pieces below only work
once it's mounted.

**Read this if a video comes back with the wrong voice or no music:** the
`.skill` files install account-wide and show up in *any* Cowork project, but
the API keys they need only live in this folder's `.env`. A project that
doesn't have `video-gen` connected can't actually run `text-to-speech.skill`
or `sound-effects.skill` even though they look installed — Claude will
silently fall back to whatever else is available (confirmed case: the
already-connected Higgsfield MCP for voiceover, which can't do music at all).
**Always connect this folder** when working on video/audio in a new project,
and tell Claude explicitly to use these two skills rather than leaving the
choice open. Full root-cause writeup in `video-creation-stack.md` §0.1.

**`.env` has been copied into these project folders so far** (July 5, 2026):
`dropshipping` and `koolestpro-cowork-v2`. If a key ever rotates, update the
copy in each of those too, or they go stale. `video-creation-stack.md` §0.1
keeps the current list.

## Contents

- `.env` — API keys (Pexels, Pixabay, inference.sh, HeyGen, Groq/OpenAI,
  DeepSeek, Shotstack placeholder). Not committed anywhere, just sits in this
  folder. **`INFSH_API_KEY` and `HEYGEN_API_KEY` have real money behind
  them** — everything else here is free-tier.
- `video-creation-stack.md` — the full stack reference doc (generation,
  stock, editing, review layers, credential hygiene, and what's Cowork-native
  vs. terminal-only).
- `*.skill` files — Cowork skill bundles, install via Settings > Capabilities
  > Skills, or just tell Claude to use the copy in this folder:
  - `video-review.skill` — download + transcript + frame analysis for any
    video (free, `/watch` equivalent)
  - `stock-footage.skill` — Pexels/Pixabay b-roll search (free)
  - `ai-video-generation.skill` — text/image-to-video, avatar/lipsync via
    inference.sh's REST API (paid, prepaid credits)
  - `heygen-api.skill` — talking-avatar video via HeyGen's Direct API (paid,
    prepaid credits — separate from the HyperFrames MCP connector, which
    bills a HeyGen web-plan subscription instead)
  - `sound-effects.skill` — Freesound.org SFX/ambience/**background music**
    search (free account, `FREESOUND_API_KEY` set and confirmed working)
  - `text-to-speech.skill` — voiceover via Groq (Orpheus) or OpenAI
    (gpt-4o-mini-tts), billed against `GROQ_API_KEY`/`OPENAI_API_KEY`. **Primary
    voiceover tool now** — replaces Higgsfield as the default (see below).
- `_staging/`, `_staging2/`, `_staging3/`, `_staging4/` — editable source for
  the skills above (in case something needs tweaking without unzipping the
  `.skill` file). Harmless leftovers, not required for the skills to work.
- `infsh_test_paper_boat.mp4` — sample output from the live `ai-video-generation`
  test (July 3, 2026, `pruna/p-video`, ~$0.05-0.11 spent) — proof the full
  pipeline works, not something you need to keep.
- `BreezeLoop_Video1_ProblemHook_VO_v1.mp4` / `_v2.mp4` / `_v3.mp4` — the
  sound-design progression: v1 has Higgsfield voiceover only; v2 adds a 1.12x
  speed-up, a new OpenAI voiceover, and real Freesound whoosh/pop SFX at
  detected scene cuts; v3 adds a Freesound background music bed and real
  `xfade` visual transitions (whip-blur) synced to each whoosh instead of
  hard jump cuts.
- `BreezeLoop_Video1_Feature_1x1_v2.mp4` / `_9x16_v2.mp4` — rescue pass on a
  version the user built in a different project without this folder
  connected (different/generic voice, no music). Re-voiced with OpenAI,
  scene-cut SFX and a Freesound music bed added back in both aspect ratios.
  See `video-creation-stack.md` §3 and §0.1 for the full incident + fix.

## Voiceover: `text-to-speech.skill` is primary; Higgsfield is fallback only

The user has moved off Higgsfield for voiceover. `text-to-speech.skill` wraps
Groq (Orpheus, best for Arabic — matches the provider combo already used in
the user's own speaking-practice app) and OpenAI (`gpt-4o-mini-tts`, best
default for English, no character limit, steerable `--instructions`). Both
bill against the already-present `GROQ_API_KEY`/`OPENAI_API_KEY`. **Groq
status:** the model terms were accepted in the Groq console on July 4, 2026,
but a live re-test right after still returned `400 model_terms_required` —
likely a propagation delay or an org mismatch between the console session and
the API key; retry in a few minutes before assuming it's still broken. OpenAI
has no such gotcha and works immediately.

Background music now comes from the same Freesound source as SFX —
`sound-effects.skill` isn't just whooshes/pops, it covers full music beds too
(search a mood/genre query, filter to CC0, trim/fade to length).

Higgsfield's `generate_audio` (`seed_audio` model, ~0.1 credits/generation,
no `.env` key needed) still works as a fallback if neither Groq nor OpenAI
is available.

## Terminal fallback

Cowork's shell tool caps a single command at ~45 seconds. If a skill call
times out because of that (confirmed case: HeyGen's `/v2/avatars` endpoint),
the same `scripts/*.py` files run fine from an actual terminal with no such
ceiling — same `.env`, same flags. That's the fallback whenever a skill
"refuses to work" for sandbox-timing reasons rather than a real error.

## Keys (`.env` format)

```
INFSH_API_KEY=...       # inference.sh — real money
HEYGEN_API_KEY=...      # HeyGen Direct API — real money
PEXELS_API_KEY=...      # free
PIXABAY_API_KEY=...     # free
GROQ_API_KEY=...        # Whisper fallback + text-to-speech.skill (accept Orpheus terms in console first)
OPENAI_API_KEY=...      # Whisper fallback + text-to-speech.skill (primary voiceover)
FREESOUND_API_KEY=...   # free — confirmed working
```

Every skill above reads keys from this file via `--env /path/to/video-gen/.env`
(or `--keys` for stock-footage). If a key's missing or wrong, the skills fail
with a clear "no API key" / 401 error rather than silently doing nothing.
