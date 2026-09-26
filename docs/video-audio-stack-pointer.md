# Video/audio creative stack — available in this project

This folder now has its own `.env` (copied July 5, 2026 from the `video-gen`
project), so voiceover, sound effects, and background music generation work
directly here — useful for any explainer clips, product demos, or audio
treatments layered into carousels/CRO content/banners.

**Use these two Cowork skills explicitly, by name, rather than leaving the
choice open to whatever's already connected:**
- `text-to-speech.skill` — voiceover via OpenAI (`gpt-4o-mini-tts`, reliable
  default, steerable `--instructions` for tone) or Groq Orpheus (best for
  Arabic; currently blocked by a Groq-console terms-acceptance propagation
  issue, see the master doc)
- `sound-effects.skill` — Freesound.org search for SFX, ambience, and full
  **background music** beds (filter `--license "Creative Commons 0"` for
  zero-attribution results)

**Why this file exists:** a different project (`dropshipping`) generated a
video without this `.env` connected, and Claude silently fell back to a
different MCP connector for voiceover with no music capability at all —
noticeably lower quality, and it took a manual fix to catch. Connecting
`.env` here up front avoids the same silent fallback in this project.

**Full reference:** credential hygiene, ffmpeg techniques (speed-ramping,
`xfade` transitions, loudnorm targets, scene-cut detection), and the
complete incident writeup live in the `video-gen` project's
`video-creation-stack.md` and `README.md`. Connect that folder too if you
want the full writeup — this file + this folder's `.env` is enough to
actually run both skills here.

This does not change or override anything in `CLAUDE.md` — it's a
supplementary pointer for video/audio work only.
