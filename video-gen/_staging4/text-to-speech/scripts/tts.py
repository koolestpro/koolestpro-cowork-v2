#!/usr/bin/env python3
"""
Text-to-speech wrapper for the two pay-per-use providers already in the
stack's .env: Groq (Orpheus models) and OpenAI (gpt-4o-mini-tts / tts-1 /
tts-1-hd). No Higgsfield dependency -- this is the replacement.

Usage:
    python3 tts.py "<text>" --provider openai --voice nova --out vo.mp3
    python3 tts.py "<text>" --provider groq --lang en --voice troy --out vo.wav
    python3 tts.py "<text>" --provider groq --lang ar --voice noura --out vo.wav

Provider notes (read before picking one):

- Groq (canopylabs/orpheus-v1-english / orpheus-arabic-saudi):
    * $22 / 1M chars (English), $40 / 1M chars (Arabic-Saudi dialect).
    * HARD LIMIT: 200 characters per API call. This script auto-splits
      longer text into <=200-char chunks on sentence boundaries, generates
      each chunk separately, and concatenates the resulting wav files with
      ffmpeg. This means a long script makes multiple API calls -- fine for
      cost (still cheap) but worth knowing about for rate limits.
    * Only "wav" response_format is supported (no mp3).
    * English voices: autumn, diana, hannah (female), austin, daniel, troy (male).
    * Arabic (Saudi) voices: lulwa, noura, aisha (female), abdullah, fahad, sultan (male).
    * Supports bracketed vocal directions in the input text, e.g.
      "[warm] Welcome to..." or "[professionally] Here's the plan." -- more
      directions = more performed/expressive, none = natural conversational
      cadence. Great for ad reads; don't overuse or it gets hammy.
    * This is the natural choice for Arabic content (it's what's already
      proven out in the user's own app), and works fine for English too.

- OpenAI (gpt-4o-mini-tts default, tts-1/tts-1-hd also available):
    * gpt-4o-mini-tts: $0.60/1M input text tokens + $12/1M audio output
      tokens, works out to roughly $0.015/minute of audio -- cheap, and no
      200-character wall, so a full ad script goes out in one call.
    * 13 voices: alloy, ash, coral, echo, fable, nova, onyx, sage, shimmer,
      ballad, verse, marin, cedar.
    * `--instructions "<tone description>"` steers delivery (only honored by
      gpt-4o-mini-tts, ignored by tts-1/tts-1-hd) -- e.g. "warm, upbeat,
      conversational, like a friend recommending a product" instead of
      Groq's inline bracketed-direction style.
    * Good default for English marketing/ad voiceover since there's no
      chunking to manage and the per-call cost for a 15-30s script is a
      fraction of a cent either way.

Pick Groq when: the content is Arabic, or a Groq Orpheus voice/style is
specifically wanted. Pick OpenAI when: it's English and you'd rather not
think about the 200-char chunking, or you want steerable `instructions`.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

GROQ_URL = "https://api.groq.com/openai/v1/audio/speech"
OPENAI_URL = "https://api.openai.com/v1/audio/speech"
# Both hosts (like several others in this stack) front with Cloudflare bot
# detection that blocks Python's default urllib user agent (HTTP 403, error
# code 1010) -- a normal-looking UA sidesteps it, same fix as inference.sh
# and the stock-footage skill needed.
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) video-gen-cowork-skill/1.0"

GROQ_VOICES = {
    "en": {"autumn", "diana", "hannah", "austin", "daniel", "troy"},
    "ar": {"lulwa", "noura", "aisha", "abdullah", "fahad", "sultan"},
}
OPENAI_VOICES = {"alloy", "ash", "coral", "echo", "fable", "nova", "onyx", "sage", "shimmer", "ballad", "verse", "marin", "cedar"}


def load_key(env_path, key_name):
    key = os.environ.get(key_name, "")
    if env_path and os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == key_name and v.strip():
                    key = v.strip()
    return key


def split_for_groq(text, limit=195):
    """Split text into <=limit-char chunks on sentence boundaries where
    possible, falling back to word boundaries. Keeps bracketed vocal
    directions attached to the sentence they modify where it can."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, current = [], ""
    for sent in sentences:
        candidate = (current + " " + sent).strip() if current else sent
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                chunks.append(current)
            if len(sent) <= limit:
                current = sent
            else:
                # sentence itself too long -- hard-split on words
                words = sent.split()
                current = ""
                for w in words:
                    cand2 = (current + " " + w).strip() if current else w
                    if len(cand2) <= limit:
                        current = cand2
                    else:
                        chunks.append(current)
                        current = w
    if current:
        chunks.append(current)
    return chunks


def call_groq(text, voice, lang, key, out_path):
    model = "canopylabs/orpheus-v1-english" if lang == "en" else "canopylabs/orpheus-arabic-saudi"
    if voice not in GROQ_VOICES[lang]:
        print(f"warning: '{voice}' not in known {lang} voice list {GROQ_VOICES[lang]}, trying anyway", file=sys.stderr)

    chunks = split_for_groq(text)
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        body = json.dumps({"model": model, "input": chunk, "voice": voice, "response_format": "wav"}).encode()
        req = urllib.request.Request(
            GROQ_URL, data=body, method="POST",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": USER_AGENT},
        )
        chunk_path = f"{out_path}.part{i}.wav"
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                with open(chunk_path, "wb") as f:
                    f.write(resp.read())
        except urllib.error.HTTPError as e:
            print(json.dumps({"error": f"Groq HTTP {e.code}: {e.read().decode()}", "chunk": chunk}))
            sys.exit(1)
        chunk_paths.append(chunk_path)

    if len(chunk_paths) == 1:
        os.rename(chunk_paths[0], out_path)
    else:
        list_file = f"{out_path}.concat.txt"
        with open(list_file, "w") as f:
            for p in chunk_paths:
                f.write(f"file '{os.path.abspath(p)}'\n")
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", out_path],
            capture_output=True,
        )
        os.remove(list_file)
        for p in chunk_paths:
            os.remove(p)

    print(json.dumps({"provider": "groq", "model": model, "voice": voice, "chunks": len(chunks), "out": out_path}, indent=2))


def call_openai(text, voice, model, instructions, response_format, key, out_path):
    if voice not in OPENAI_VOICES:
        print(f"warning: '{voice}' not in known OpenAI voice list {OPENAI_VOICES}, trying anyway", file=sys.stderr)
    body = {"model": model, "input": text, "voice": voice, "response_format": response_format}
    if instructions and model == "gpt-4o-mini-tts":
        body["instructions"] = instructions
    req = urllib.request.Request(
        OPENAI_URL, data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(out_path, "wb") as f:
                f.write(resp.read())
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"OpenAI HTTP {e.code}: {e.read().decode()}"}))
        sys.exit(1)
    print(json.dumps({"provider": "openai", "model": model, "voice": voice, "out": out_path}, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text")
    ap.add_argument("--provider", choices=["groq", "openai"], required=True)
    ap.add_argument("--env", default=None, help="path to .env with GROQ_API_KEY/OPENAI_API_KEY")
    ap.add_argument("--voice", required=True)
    ap.add_argument("--lang", choices=["en", "ar"], default="en", help="groq only: english or arabic-saudi model")
    ap.add_argument("--model", default="gpt-4o-mini-tts", help="openai only: gpt-4o-mini-tts, tts-1, or tts-1-hd")
    ap.add_argument("--instructions", default=None, help="openai gpt-4o-mini-tts only: steer tone/style")
    ap.add_argument("--format", default=None, help="openai only: mp3 (default), wav, opus, aac, flac, pcm")
    ap.add_argument("--out", required=True, help="output file path")
    args = ap.parse_args()

    if args.provider == "groq":
        key = load_key(args.env, "GROQ_API_KEY")
        if not key:
            print(json.dumps({"error": "no GROQ_API_KEY found"}))
            sys.exit(1)
        call_groq(args.text, args.voice, args.lang, key, args.out)
    else:
        key = load_key(args.env, "OPENAI_API_KEY")
        if not key:
            print(json.dumps({"error": "no OPENAI_API_KEY found"}))
            sys.exit(1)
        call_openai(args.text, args.voice, args.model, args.instructions, args.format or "mp3", key, args.out)


if __name__ == "__main__":
    main()
