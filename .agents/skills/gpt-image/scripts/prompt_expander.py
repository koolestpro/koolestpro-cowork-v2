#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.31.0"]
# ///
"""
Prompt Expansion Engine for the GPT Image skill.

Raw image APIs receive your prompt verbatim. ChatGPT does not: before calling its
image model it silently rewrites a short request into a detailed, multi-sentence
scene. This module reproduces that layer.

It does three things:
  1. Strips generic quality buzzwords ("photorealistic", "4K", "stunning", ...).
  2. Flags negative phrasing, unquoted text, and missing scene sections.
  3. Optionally rewrites the prompt with an OpenAI chat model using the same
     expansion rules ChatGPT follows (the 2023-10-07 DALL-E 3 instructions).

Modes
  off   passthrough
  lint  sanitize + report only (no semantic rewrites)
  auto  sanitize + rewrite exact common negatives + report; never calls an LLM
  llm   always rewrite with the LLM (needs a chat endpoint key)

CLI
  uv run prompt_expander.py --prompt "coffee mug on a desk" --type product-lifestyle
  uv run prompt_expander.py --prompt "..." --expand llm --json
  uv run prompt_expander.py --prompt "..." --expand lint --output expanded.txt
"""

import argparse
import json
import os
import re
import sys
import time

try:
    import requests
except ImportError:  # allow --expand off/lint without requests installed
    requests = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

DEFAULT_EXPANDER_MODEL = os.environ.get("GPT_IMAGE_EXPANDER_MODEL", "gpt-4o-mini")
DEFAULT_EXPANDER_BASE_URL = os.environ.get("GPT_IMAGE_EXPANDER_BASE_URL", "https://api.openai.com/v1")
DEFAULT_MIN_WORDS = 30
MAX_PROMPT_CHARS = 3800
MAX_LITERAL_TEXT_WORDS = 4

# Generic quality words the image model is told not to use. They add no visual
# information; the expansion should describe the causes of quality instead.
BUZZWORDS = [
    "photorealistic",
    "photo-realistic",
    "hyperrealistic",
    "hyper-realistic",
    "hyper realistic",
    "ultra realistic",
    "ultra-realistic",
    "4k",
    "8k",
    "16k",
    "uhd",
    "ultra-detailed",
    "ultra detailed",
    "hyper-detailed",
    "hyper detailed",
    "highly detailed",
    "extremely detailed",
    "insanely detailed",
    "stunning",
    "beautiful",
    "gorgeous",
    "breathtaking",
    "masterpiece",
    "best quality",
    "highest quality",
    "professional quality",
    "award-winning",
    "award winning",
    "cinematic lighting",
]

_BUZZWORD_RE = re.compile(
    r"(?<![A-Za-z0-9])(" + "|".join(re.escape(b) for b in sorted(BUZZWORDS, key=len, reverse=True)) + r")(?![A-Za-z0-9])",
    re.IGNORECASE,
)

# "no X", "without X", "free of X", "avoid X" up to punctuation / a conjunction.
_NEGATIVE_RE = re.compile(
    r"\b(?:no|without|free\s+of|avoid|zero|don't\s+include|do\s+not\s+include|doesn't\s+include)\s+"
    r"([A-Za-z0-9][A-Za-z0-9'\- ]{0,48}?)"
    r"(?=[,.;:!?]|$|\s+(?:and|or|but)\b)",
    re.IGNORECASE,
)

# Positive rewrites for the most common negative requests. Suggestions only:
# a script should not silently change what the user asked for.
POSITIVE_SUGGESTIONS = {
    "text": "plain, unmarked surfaces with clean negative space",
    "words": "plain, unmarked surfaces with clean negative space",
    "lettering": "plain, unmarked surfaces with clean negative space",
    "typography": "plain, unmarked surfaces with clean negative space",
    "extra text": "plain, unmarked surfaces with clean negative space",
    "people": "a deserted, unpopulated setting",
    "person": "a deserted, unpopulated setting",
    "humans": "a deserted, unpopulated setting",
    "crowd": "a deserted, unpopulated setting",
    "cars": "an empty street with bare asphalt",
    "car": "an empty street with bare asphalt",
    "traffic": "an empty street with bare asphalt",
    "vehicles": "an empty street with bare asphalt",
    "clutter": "a sparse composition with open negative space",
    "logos": "unbranded, plain surfaces",
    "logo": "unbranded, plain surfaces",
    "watermark": "clean, unmarked edges",
}

# Ordinary English phrases that start with "no" but are not visual negatives.
NEGATIVE_SKIP = {
    "one", "more", "less", "longer", "matter", "doubt", "wonder", "need",
    "way", "problem", "issue", "time", "reason", "charge", "cost",
}

MEDIUM_RE = re.compile(
    r"\b(photo|photograph|photography|render|3d|3-d|illustration|painting|watercolor|watercolour|"
    r"vector|logo|ui|ux|screenshot|infographic|collage|film|cinema|anime|sketch|drawing|"
    r"claymation|isometric|macro|portrait|advertisement|ad|poster|packshot|product shot)\b",
    re.IGNORECASE,
)
LIGHTING_RE = re.compile(
    r"\b(light|lighting|lit|sunlight|sun|sunset|sunrise|golden hour|shadow|shadows|backlit|"
    r"softbox|neon|dusk|dawn|overcast|studio|moonlight|candlelight|ambient|glow)\b",
    re.IGNORECASE,
)
SETTING_RE = re.compile(
    r"\b(background|scene|setting|room|interior|exterior|outdoor|indoors|street|studio|"
    r"table|desk|wall|landscape|environment|sky|forest|beach|kitchen|office|cafe|coffee shop)\b",
    re.IGNORECASE,
)
DETAIL_RE = re.compile(
    r"\b(texture|textures|material|fabric|wood|metal|ceramic|glass|leather|linen|skin|pores|"
    r"grain|stitch|stitching|pattern|reflection|reflections|surface|detail|details|clothing|"
    r"wardrobe|hair|eyes|wrinkle|wrinkles)\b",
    re.IGNORECASE,
)

_QUOTED_RE = re.compile(
    r'"([^"\n]{1,120})"'
    r'|“([^”\n]{1,120})”'
    r"|(?<![A-Za-z0-9])'([^'\n]{1,120})'(?![A-Za-z0-9])"
)
_TEXT_INTENT_RE = re.compile(
    r"\b(headline|title|tagline|cta|call to action|button|label|caption|text|reads|says|"
    r"wordmark|sign)\b",
    re.IGNORECASE,
)

EXPANSION_SYSTEM_PROMPT = """You are the hidden prompt-expansion layer that runs before an image model. Turn the user's request into ONE richly detailed, self-contained image prompt, the way ChatGPT rewrites a request before calling DALL-E 3.

Follow these rules exactly:

1. EXPAND, DO NOT PARAPHRASE. Keep the user's subject and intent, then add concrete, plausible specifics: subject and action, materials and textures, clothing, surface details, background and setting, framing and viewpoint, camera/lens and depth of field (for photographic images), lighting direction and quality, colour palette, and mood. Never ask questions. Never leave a section vague.
2. BAN QUALITY BUZZWORDS. Never write: photorealistic, hyperrealistic, hyper-realistic, 4K, 8K, UHD, ultra-detailed, hyper-detailed, highly detailed, stunning, beautiful, gorgeous, breathtaking, masterpiece, professional quality, best quality, highest quality, award-winning, cinematic lighting. Create quality by describing what makes it look real or beautiful: light, texture, lens, materials, atmosphere.
3. NO NEGATIVE PHRASING. Do not write "no X", "without X", "don't include X", "avoid X", or "free of X". State what IS in the scene. Example: "a room with no chairs" becomes "a sparse room with bare walls, a window, and an empty wooden floor".
4. EXACT TEXT. If the user gives literal text, copy it verbatim inside double quotes, keep it to 1-4 words, and specify placement, size, font style, weight, colour, and case. Do not invent extra text.
5. ORDER. Write in this order: medium/style, then subject and action, then fine details and textures, then environment/background, then lighting and mood. Use flowing prose in 2-4 sentences; no labels, no bullets, no headings.
6. PRESERVE. Keep every brand name, slogan, colour, number, product, and explicit constraint the user supplied. Do not add watermarks, signatures, logos, borders, or text the user did not ask for.
7. OUTPUT ONLY THE FINAL PROMPT. No preamble, no explanation, no surrounding quotation marks, no markdown.
{extra}"""

EDIT_EXTRA = """
This is an EDIT of the supplied image(s). Describe only the requested change precisely. Preserve identity, geometry, pose, framing, lighting, and everything not mentioned; end with "Keep everything else exactly the same." Do not invent new subjects or extra changes."""


# ───────────────────────────── helpers ─────────────────────────────

def _read_env_key(key_name, env_file=None):
    """Read a key from the shell env, then .env files. Returns None instead of raising."""
    if os.environ.get(key_name):
        return os.environ[key_name]
    paths = []
    if env_file:
        paths.append(env_file)
    paths.extend([
        os.path.join(SKILL_DIR, ".env"),
        os.path.join(os.getcwd(), ".env"),
    ])
    for path in paths:
        try:
            if not os.path.exists(path):
                continue
            with open(path) as fh:
                for line in fh:
                    line = line.strip()
                    if line.startswith(key_name + "="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except OSError:
            continue
    return None


def _expander_key(env_file=None):
    """Key for the chat-expansion endpoint (any OpenAI-compatible provider)."""
    return (
        _read_env_key("GPT_IMAGE_EXPANDER_API_KEY", env_file)
        or _read_env_key("OPENAI_API_KEY", env_file)
    )


def _expander_endpoint(env_file=None):
    base = (
        os.environ.get("GPT_IMAGE_EXPANDER_BASE_URL")
        or _read_env_key("GPT_IMAGE_EXPANDER_BASE_URL", env_file)
        or DEFAULT_EXPANDER_BASE_URL
    )
    return base.rstrip("/") + "/chat/completions"


def _expander_model(model=None, env_file=None):
    return (
        model
        or os.environ.get("GPT_IMAGE_EXPANDER_MODEL")
        or _read_env_key("GPT_IMAGE_EXPANDER_MODEL", env_file)
        or DEFAULT_EXPANDER_MODEL
    )


def _cleanup_spacing(text):
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([,.;:!?])\1+", r"\1", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"^\s*[,;:]\s*", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def strip_buzzwords(prompt):
    """Remove generic quality buzzwords. Returns (cleaned_prompt, removed_terms)."""
    removed = []

    def repl(match):
        term = match.group(1)
        if term.lower() not in [r.lower() for r in removed]:
            removed.append(term)
        return ""

    cleaned = _BUZZWORD_RE.sub(repl, prompt)
    return _cleanup_spacing(cleaned), removed


def find_negatives(prompt):
    """Report negative phrasing with a positive-rewrite suggestion."""
    warnings = []
    for match in _NEGATIVE_RE.finditer(prompt):
        phrase = match.group(0).strip()
        subject = re.sub(r"^(?:no|without|free\s+of|avoid|zero|don't\s+include|do\s+not\s+include|doesn't\s+include)\s+",
                         "", match.group(0), flags=re.IGNORECASE).strip().lower()
        if subject in NEGATIVE_SKIP or subject.split()[0] in NEGATIVE_SKIP:
            continue
        suggestion = None
        for key, value in POSITIVE_SUGGESTIONS.items():
            if key in subject:
                suggestion = value
                break
        warnings.append({
            "phrase": phrase,
            "subject": subject,
            "suggestion": suggestion or "describe the desired state positively instead",
        })
    return warnings


def rewrite_negatives(prompt):
    """
    Rewrite exact common negative phrases ("no text", "no people") into positive
    descriptions. Returns (rewritten_prompt, changes). Unknown negatives are left
    for the warning list; this never guesses at the user's meaning.
    """
    changes = []

    def repl(match):
        subject = re.sub(
            r"^(?:no|without|free\s+of|avoid|zero|don't\s+include|do\s+not\s+include|doesn't\s+include)\s+",
            "", match.group(0), flags=re.IGNORECASE,
        ).strip().lower()
        replacement = POSITIVE_SUGGESTIONS.get(subject)
        if replacement:
            changes.append({"from": match.group(0).strip(), "to": replacement})
            return replacement
        return match.group(0)

    rewritten = _NEGATIVE_RE.sub(repl, prompt)
    return _cleanup_spacing(rewritten), changes


def check_text_rules(prompt):
    """Check literal text: quotes required, 1-4 words recommended."""
    warnings = []
    quoted = [next(g for g in m.groups() if g is not None) for m in _QUOTED_RE.finditer(prompt)]
    if _TEXT_INTENT_RE.search(prompt) and not quoted:
        warnings.append(
            "Text is mentioned but not quoted. Put literal text in double quotes, "
            'e.g. Headline reads exactly: "OPEN DAILY".'
        )
    for item in quoted:
        words = re.findall(r"\S+", item.strip())
        if len(words) > MAX_LITERAL_TEXT_WORDS:
            warnings.append(
                f'Quoted text "{item}" is {len(words)} words. Keep rendered text to '
                f"{MAX_LITERAL_TEXT_WORDS} words (1-4) to avoid garbled lettering."
            )
    return warnings


def missing_sections(prompt):
    """Which parts of the 5-part blueprint are absent."""
    missing = []
    if not MEDIUM_RE.search(prompt):
        missing.append("medium/style")
    if not DETAIL_RE.search(prompt):
        missing.append("fine details/textures")
    if not SETTING_RE.search(prompt):
        missing.append("background/setting")
    if not LIGHTING_RE.search(prompt):
        missing.append("lighting/mood")
    return missing


def _word_count(text):
    return len(re.findall(r"\S+", text))


def _strip_wrapping_quotes(text):
    text = text.strip()
    if len(text) >= 2 and text[0] in "\"“”'" and text[-1] in "\"“”'":
        text = text[1:-1].strip()
    if text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()
    return text


def build_system_prompt(image_type=None, is_edit=False):
    extra = ""
    if image_type:
        extra += f"\nThe image category is: {image_type}."
    if is_edit:
        extra += EDIT_EXTRA
    return EXPANSION_SYSTEM_PROMPT.format(extra=extra.strip())


def expand_with_llm(prompt, image_type=None, is_edit=False, model=None, env_file=None, timeout=90):
    """Rewrite the prompt with an OpenAI-compatible chat model. Returns (expanded, error)."""
    if requests is None:
        return None, "requests is not installed"
    model = _expander_model(model, env_file)
    key = _expander_key(env_file)
    if not key:
        return None, (
            "No expander key found. Set GPT_IMAGE_EXPANDER_API_KEY (or OPENAI_API_KEY) "
            "in the environment or .env; LLM expansion is optional."
        )
    url = _expander_endpoint(env_file)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": build_system_prompt(image_type, is_edit)},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }
    last_error = None
    for attempt in range(3):
        try:
            resp = requests.post(
                url,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json=payload,
                timeout=timeout,
            )
        except Exception as exc:
            last_error = str(exc)
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
                continue
            return None, last_error

        detail = ""
        try:
            detail = resp.text[:400]
        except Exception:
            pass

        # Quota / auth errors will not fix themselves: report at once.
        lowered = detail.lower()
        if resp.status_code in (401, 403) or "insufficient_quota" in lowered or "credit_balance" in lowered:
            return None, f"HTTP {resp.status_code}: {detail or resp.reason}"

        # Rate limits and transient server errors are worth one or two retries.
        if resp.status_code == 429 or 500 <= resp.status_code < 600:
            last_error = f"HTTP {resp.status_code}: {detail or resp.reason}"
            if attempt < 2:
                time.sleep(2.0 * (attempt + 1))
                continue
            return None, last_error

        try:
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"]
            text = _strip_wrapping_quotes(text)
            if not text:
                return None, "expander returned an empty prompt"
            return text, None
        except Exception as exc:
            return None, f"{exc}" + (f" | {detail}" if detail else "")
    return None, last_error or "unknown error"


def expand_prompt(prompt, image_type=None, mode="auto", min_words=DEFAULT_MIN_WORDS,
                  model=None, env_file=None, is_edit=False, allow_llm=True):
    """
    Expand and lint a prompt.

    Returns (final_prompt, report). The report is JSON-safe and includes the
    original prompt, sanitized prompt, warnings, and whether the LLM ran.
    """
    prompt = (prompt or "").strip()
    mode = (mode or "auto").lower()
    if mode not in ("off", "lint", "auto", "llm"):
        raise ValueError(f"Unknown expansion mode: {mode}")

    sanitized, removed = strip_buzzwords(prompt)
    before_words = _word_count(prompt)
    needs_expansion = before_words < min_words

    report = {
        "mode": mode,
        "image_type": image_type,
        "is_edit": is_edit,
        "original": prompt,
        "sanitized": sanitized,
        "final": prompt,
        "used_llm": False,
        "attempted_llm": False,
        "llm_model": None,
        "llm_error": None,
        "removed_buzzwords": removed,
        "negative_rewrites": [],
        "negative_warnings": find_negatives(sanitized),
        "text_warnings": check_text_rules(sanitized),
        "missing_sections": missing_sections(sanitized),
        "word_count_before": before_words,
        "word_count_after": before_words,
        "needs_expansion": needs_expansion,
        "would_expand": mode == "auto" and needs_expansion,
        "key_available": bool(_expander_key(env_file)),
        "llm_endpoint": _expander_endpoint(env_file),
        "too_long": False,
    }

    if mode == "off":
        report["final"] = prompt
        report["word_count_after"] = before_words
        return prompt, report

    final = sanitized
    report["final"] = final
    report["word_count_after"] = _word_count(final)

    should_llm = mode == "llm"
    report["attempted_llm"] = should_llm and allow_llm
    if should_llm and not allow_llm:
        report["llm_error"] = "LLM expansion skipped (dry run)"
    elif should_llm:
        if not report["key_available"]:
            report["llm_error"] = (
                "No expander key found. Set GPT_IMAGE_EXPANDER_API_KEY (or OPENAI_API_KEY); "
                "LLM expansion is optional."
            )
        else:
            expanded, error = expand_with_llm(
                prompt,
                image_type=image_type,
                is_edit=is_edit,
                model=model,
                env_file=env_file,
            )
            if expanded:
                # The model can still slip in a buzzword; enforce the rule again.
                final, removed_again = strip_buzzwords(expanded)
                for term in removed_again:
                    if term.lower() not in [r.lower() for r in report["removed_buzzwords"]]:
                        report["removed_buzzwords"].append(term)
                report["used_llm"] = True
                report["llm_model"] = _expander_model(model, env_file)
                report["final"] = final
                report["word_count_after"] = _word_count(final)
                report["negative_warnings"] = find_negatives(final)
                report["text_warnings"] = check_text_rules(final)
                report["missing_sections"] = missing_sections(final)
            else:
                report["llm_error"] = error

    # In auto/llm modes, turn the exact common negatives into positive phrasing.
    # lint stays report-only so you can inspect the raw request.
    if mode in ("auto", "llm"):
        rewritten, neg_rewrites = rewrite_negatives(report["final"])
        report["negative_rewrites"] = neg_rewrites
        if rewritten != report["final"]:
            report["final"] = rewritten
            report["word_count_after"] = _word_count(rewritten)
            report["negative_warnings"] = find_negatives(rewritten)
            report["text_warnings"] = check_text_rules(rewritten)
            report["missing_sections"] = missing_sections(rewritten)

    report["too_long"] = len(report["final"]) > MAX_PROMPT_CHARS
    return report["final"], report


def format_report(report):
    """Human-readable report lines (diagnostics, not the prompt)."""
    lines = []
    if report.get("removed_buzzwords"):
        lines.append("Removed quality buzzwords: " + ", ".join(report["removed_buzzwords"]))
    if report.get("used_llm"):
        lines.append(
            f"Expanded {report['word_count_before']} -> {report['word_count_after']} words "
            f"via {report.get('llm_model') or DEFAULT_EXPANDER_MODEL}"
        )
    elif report.get("attempted_llm") and report.get("llm_error"):
        lines.append("Expansion failed, using the linted prompt: " + report["llm_error"])
    elif report.get("would_expand") and report.get("llm_error"):
        lines.append("Expansion advisory: " + report["llm_error"])
    elif report.get("needs_expansion") and report.get("mode") in ("auto", "lint"):
        lines.append(
            f"Short prompt ({report['word_count_before']} words). Expand it with the "
            "SKILL.md rules before generating, or pass --expand llm."
        )
    for change in report.get("negative_rewrites", []):
        lines.append(f'Rewrote negative "{change["from"]}" -> "{change["to"]}"')
    for warning in report.get("negative_warnings", []):
        lines.append(f'Negative phrasing: "{warning["phrase"]}" -> {warning["suggestion"]}')
    for warning in report.get("text_warnings", []):
        lines.append("Text rule: " + warning)
    if report.get("missing_sections") and not report.get("used_llm"):
        lines.append("Missing scene parts: " + ", ".join(report["missing_sections"]))
    if report.get("too_long"):
        lines.append(
            f"Prompt is {len(report['final'])} characters; the image API accepts about "
            f"{MAX_PROMPT_CHARS}. Trim it before generating."
        )
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Expand a short image prompt into the detailed prompt ChatGPT would send.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  uv run prompt_expander.py --prompt "cozy coffee shop desk" --type product-lifestyle
  uv run prompt_expander.py --prompt "cozy coffee shop desk" --expand llm
  uv run prompt_expander.py --prompt "ad with headline 'GLOW UP'" --expand lint --json
  uv run prompt_expander.py --prompt "..." --expand llm --output expanded.txt
        """,
    )
    parser.add_argument("--prompt", required=True, help="Prompt to expand")
    parser.add_argument("--type", dest="image_type", help="Image category (from model-registry.json)")
    parser.add_argument("--expand", default="auto", choices=["off", "lint", "auto", "llm"],
                        help="Expansion mode (default: auto)")
    parser.add_argument("--min-words", type=int, default=DEFAULT_MIN_WORDS,
                        help=f"auto expands prompts shorter than this (default: {DEFAULT_MIN_WORDS})")
    parser.add_argument("--model", default=None,
                        help=f"Chat model for --expand llm (default: {DEFAULT_EXPANDER_MODEL}, "
                             f"or GPT_IMAGE_EXPANDER_MODEL)")
    parser.add_argument("--env-file", help="Path to .env containing OPENAI_API_KEY")
    parser.add_argument("--edit", action="store_true", help="Expansion rules for an edit instruction")
    parser.add_argument("--json", action="store_true", help="Print the full report as JSON")
    parser.add_argument("--output", help="Write the final prompt to this file")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress diagnostics on stderr")
    args = parser.parse_args(argv)

    final, report = expand_prompt(
        args.prompt,
        image_type=args.image_type,
        mode=args.expand,
        min_words=args.min_words,
        model=args.model,
        env_file=args.env_file,
        is_edit=args.edit,
    )

    if args.output:
        with open(args.output, "w") as fh:
            fh.write(final + "\n")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(final)
        if not args.quiet:
            for line in format_report(report):
                print("[expand] " + line, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
