---
name: sound-effects
description: Searches Freesound.org for free sound effects, whooshes, transitions, UI pops, ambient beds, and foley to use in video sound design. Use this whenever the user needs a sound effect, transition sound, ambient bed, foley, or "some kind of sound for this cut/edit" — e.g. "find a whoosh for this transition," "I need a soft pop for when the text appears," "get some rain ambience for this scene." Requires a .env file with FREESOUND_API_KEY (free account, no billing risk) — if one isn't found, ask the user for the key or where their video-gen folder is, rather than failing silently. Pairs with video-review and ai-video-generation for full sound design (SFX + ambience here, voiceover via Higgsfield generate_audio or inference.sh TTS apps, music via inference.sh if needed).
---

# Sound Effects Search (Freesound.org)

Freesound is the free/no-billing-risk source for actual sound effects in this
stack — the same role Pexels/Pixabay play for visuals. It's a large,
community-uploaded library (whooshes, pops, foley, ambience, risers, clicks,
nature sounds, etc.) with a straightforward free API.

## Getting an API key (one-time, for the user to do)

Freesound requires a free account and an API key — there's no keyless public
tier. If `FREESOUND_API_KEY` isn't in `.env` yet:
1. Ask the user to create a free account at https://freesound.org and apply for an API key at https://freesound.org/apiv2/apply/ (approval is typically instant/automatic).
2. Ask them to paste the key, or add `FREESOUND_API_KEY=...` to `video-gen/.env` themselves.
3. Don't fabricate a key or silently skip the search — it'll just 401, which is fine, just say so plainly.

This is a simple API-key search (`Authorization: Token <key>` header) — no OAuth2 flow needed for what this skill does. OAuth2 is only required for downloading a sound's *original* uploaded file or for upload/rate/comment actions, none of which this skill uses.

## Running a search

```bash
python3 scripts/search_freesound.py "<query>" --keys /path/to/video-gen/.env --duration-max 4 --limit 10
```

- `--duration-max <seconds>`: filter to short clips — almost always what you want for a transition/whoosh/pop rather than a 3-minute ambient loop.
- `--license "Creative Commons 0"`: filter to CC0 (no attribution required) if the user wants zero attribution obligations. Omit to see everything (most Freesound content is Attribution or Attribution-Noncommercial, which just means crediting the creator if the video is published — check `license` in the results and mention it to the user if it's not CC0).
- `--sort downloads_desc` or `--sort rating_desc`: bias toward well-vetted, popular sounds rather than raw relevance — often better for generic SFX needs (a "whoosh" search returns thousands of hits, and quality varies a lot).
- Returns JSON with `download_url` pointing directly at the hq mp3 preview (~128kbps, no auth needed to fetch it), plus `license`, `username` (for attribution if the license requires it), and `page_url`.

## Downloading

Either pass `--download ./sfx/` to grab every result's preview mp3 in one go, or fetch a specific one:

```bash
curl -L -o whoosh_01.mp3 "<download_url>"
```

## Using it in an edit

Once downloaded, mix into a video with ffmpeg the same way as any other audio layer — e.g. overlay a whoosh right at a cut point:

```bash
ffmpeg -i video.mp4 -i whoosh_01.mp3 -filter_complex \
  "[1:a]adelay=<cut_time_ms>|<cut_time_ms>,volume=0.8[sfx]; [0:a][sfx]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" -c:v copy output.mp4
```

Adjust `adelay` (in milliseconds) to line the effect up with the exact cut/beat you're accenting.

## Attribution note

Most Freesound content is Attribution or Attribution-Noncommercial licensed — legally usable, but check the `license` field on each result. If it's not CC0 and the user is publishing the video commercially, mention that crediting the `username`/`page_url` is expected (or that a CC0-filtered search avoids the question entirely).

## Terminal fallback

Same as the rest of this stack: if a search or download call times out in Cowork's ~45s command budget (unlikely here — Freesound's search API has been fast in similar-sized requests elsewhere in this stack), the same script runs fine from a terminal with no such ceiling.
