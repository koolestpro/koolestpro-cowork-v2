---
name: text-to-speech
description: Generates voiceover audio from text using Groq (Orpheus models, cheap, native Arabic support) or OpenAI (gpt-4o-mini-tts, no character limit, steerable tone), billed against the user's existing prepaid GROQ_API_KEY/OPENAI_API_KEY balances — no Higgsfield dependency. Use this whenever the user wants a voiceover, narration, or spoken audio for a video, asks to "generate a voiceover," "add narration," "make this talk," or needs Arabic or English TTS. This is the primary voiceover tool in the stack; Higgsfield's generate_audio still works as a fallback but isn't the default going forward.
---

# Text-to-Speech (Groq + OpenAI, Cowork-native)

## Why this exists

The stack originally used Higgsfield's `generate_audio` MCP tool for voiceover. The user has moved off Higgsfield and already runs a Groq + OpenAI + DeepSeek combo in their own app (a speaking-practice feature with Arabic conversation) — this skill wraps the same two TTS providers they already trust and already have keys for, so voiceover generation doesn't depend on a tool they're deprecating.

## Auth

Reads `GROQ_API_KEY` and/or `OPENAI_API_KEY` from `video-gen/.env` (pass `--env <path>` if elsewhere). Both are already in this stack's `.env` for other purposes (Whisper fallback in `video-review`), so no new signup needed for either provider.

## Choosing a provider

**OpenAI (`--provider openai`, default model `gpt-4o-mini-tts`)** — use for English content, or anything where you don't want to think about character limits. ~$0.015/minute of audio, no hard input-length wall, 13 voices (alloy, ash, coral, echo, fable, nova, onyx, sage, shimmer, ballad, verse, marin, cedar), and a `--instructions` flag that steers tone/delivery in plain language (e.g. `"warm, upbeat, conversational, like a friend recommending a product"`). Confirmed working live.

**Groq (`--provider groq`, Orpheus models)** — the natural choice for **Arabic** (`--lang ar`, `canopylabs/orpheus-arabic-saudi`, authentic Saudi dialect, 6 voices) since it's what the user's own app already relies on. Also works for English (`--lang en`). $22/1M chars (English) or $40/1M chars (Arabic) — cheap, but has a **hard 200-character-per-call limit**; this skill's script auto-splits longer text into chunks on sentence boundaries and concatenates the resulting wav files, so it's transparent to use, just know a long script becomes several API calls under the hood. Supports inline bracketed vocal directions in the text itself (`[warm]`, `[cheerful]`, `[professionally]`, `[whisper]`, etc.) — more directions = more performed, none = natural conversational cadence.

**One-time setup gotcha (confirmed live):** Groq's Orpheus models require accepting model-specific terms in the Groq console before the API will serve them — a real request came back `400 model_terms_required` even with a valid key, pointing at `https://console.groq.com/playground?model=<model>`. This is a one-time click for the account owner, not something fixable from Cowork. If Groq calls fail with that error, tell the user to accept terms there first.

## Running it

```bash
python3 scripts/tts.py "<script text>" --provider openai --voice nova \
  --instructions "warm, upbeat, conversational" --env /path/to/video-gen/.env --out vo.mp3
```

```bash
python3 scripts/tts.py "[warm] <script text>" --provider groq --lang en --voice troy \
  --env /path/to/video-gen/.env --out vo.wav
```

```bash
python3 scripts/tts.py "<Arabic script>" --provider groq --lang ar --voice noura \
  --env /path/to/video-gen/.env --out vo.wav
```

Output duration won't necessarily match a naive words-per-minute estimate — always `ffprobe` the result to get the real duration before timing it against video, rather than assuming.

## Mixing into a video

Same pattern as before: extend/trim the video to fit if needed (a freeze-frame extension on a closing CTA card is a legitimate, common technique — better than rushing the read), mix the voiceover over any existing ambient bed at an appropriate relative volume, and run `loudnorm` for consistent levels. See the `sound-effects` skill for layering in SFX on top.

## Terminal fallback

Same as the rest of this stack — if a call times out in Cowork's ~45s command budget (unlikely here, both are typically fast single requests), the same script runs fine from a terminal.
