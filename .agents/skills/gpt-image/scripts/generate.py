#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.31.0"]
# ///
"""
GPT Image Router — Multi-provider image generation.
Reads model-registry.json, picks the best backend for the image type and budget,
and delegates generation. Drop-in replacement for the old OpenAI-only generate.py.
"""

import os, sys, json, re, argparse, textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
REGISTRY_PATH = os.path.join(SKILL_DIR, "model-registry.json")

sys.path.insert(0, SCRIPT_DIR)
from providers import get_provider
from prompt_expander import expand_prompt, format_report

# DALL-E 3-era names people copy from older guides. gpt-image models use
# low/medium/high/auto, so map the old names instead of rejecting them.
QUALITY_ALIASES = {"hd": "high", "standard": "medium"}


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def detect_image_type(prompt, registry):
    """Scan prompt keywords to guess image type. First match wins."""
    prompt_lower = prompt.lower()
    order = registry["auto_detect_rules"]["priority_order"]
    for typ in order:
        info = registry["image_types"][typ]
        for kw in info.get("keywords", []):
            if kw.lower() in prompt_lower:
                return typ
    return "static-ad-visual"  # safest default


def _provider_has_key(provider, registry):
    """Check if a provider's API key exists in shell env or .env file."""
    prov_info = registry["providers"].get(provider, {})
    env_key = prov_info.get("env_key")
    if not env_key:
        return False
    # 1. Shell env
    if os.environ.get(env_key):
        return True
    # 2. .env files
    env_paths = [
        os.path.join(SKILL_DIR, ".env"),
        os.path.join(os.getcwd(), ".env"),
    ]
    for ep in env_paths:
        if os.path.exists(ep):
            with open(ep) as f:
                for line in f:
                    if line.strip().startswith(env_key + "="):
                        return True
    return False


def _parse_entry(entry, registry):
    """Parse a registry entry string into (provider, model, quality_hint)."""
    known_providers = list(registry["providers"].keys())
    qualities = ["low", "medium", "high", "auto"]

    working = entry
    quality_hint = None

    # Strip quality suffix if present
    if "_" in working:
        last = working.rsplit("_", 1)[1]
        if last in qualities:
            quality_hint = last
            working = working[:working.rfind("_")]

    provider = None
    model = None
    parts = working.split("_")

    if len(parts) >= 2:
        # Try matching provider at end: "flux-dev_together"
        if parts[-1] in known_providers:
            provider = parts[-1]
            model = "_".join(parts[:-1])
        # Try matching provider at start: "openai_gpt-image-2"
        elif parts[0] in known_providers:
            provider = parts[0]
            model = "_".join(parts[1:])

    if not provider:
        for p in known_providers:
            if working.startswith(p + "-") or working.startswith(p + "_"):
                provider = p
                model = working
                break
            elif working == p:
                provider = p
                model = p
                break
        if not provider:
            for p in known_providers:
                if p in working:
                    provider = p
                    model = working
                    break

    if not provider:
        provider = parts[0] if parts else working
        model = "_".join(parts[1:]) if len(parts) > 1 else working

    return provider, model, quality_hint


def pick_model(image_type, budget_mode, registry):
    """
    Return (provider_name, model_id, quality_hint) for the given type and budget.
    Falls back through tiers if the preferred model's provider has no API key.
    """
    type_info = registry["image_types"][image_type]
    budget_info = registry["budget_modes"][budget_mode]
    preferred_tiers = budget_info["preferred_tiers"]

    # Try tiers in order for the requested budget
    for tier in preferred_tiers:
        ranked = type_info["tier_ranking"].get(tier, [])
        for entry in ranked:
            provider, model, quality_hint = _parse_entry(entry, registry)
            if provider and model and _provider_has_key(provider, registry):
                return provider, model, quality_hint

    # Fallback: try ALL tiers across ALL budgets, cheapest first
    all_budgets = ["cheap", "balanced", "premium"]
    for bm in all_budgets:
        tiers = registry["budget_modes"][bm]["preferred_tiers"]
        for tier in tiers:
            ranked = type_info["tier_ranking"].get(tier, [])
            for entry in ranked:
                provider, model, quality_hint = _parse_entry(entry, registry)
                if provider and model and _provider_has_key(provider, registry):
                    return provider, model, quality_hint

    # Ultimate fallback: parse the type's fallback string directly
    fallback = type_info.get("fallback", "openai_gpt-image-2_medium")
    provider, model, quality_hint = _parse_entry(fallback, registry)
    if provider and model and _provider_has_key(provider, registry):
        return provider, model, quality_hint

    # Last resort: any provider that has a key configured
    for p in registry["providers"]:
        if _provider_has_key(p, registry):
            models = list(registry["providers"][p]["models"].keys())
            if models:
                return p, models[0], None

    # Nothing at all configured
    raise RuntimeError(
        "No image generation providers are configured. "
        "Add at least one API key to your .env file (e.g., OPENAI_API_KEY)."
    )


def format_cost_table(registry):
    """Print a nice cost comparison table."""
    lines = []
    lines.append("\n" + "=" * 60)
    lines.append("MODEL REGISTRY — COST PER 1,000 IMAGES (1024x1024)")
    lines.append("=" * 60)
    cost_data = registry.get("cost_comparison", {}).get("rankings", {}).get("cheapest_to_most_expensive", [])
    for item in cost_data:
        lines.append(f"  {item}")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="GPT Image Router — generate images via the best model for the job",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        EXAMPLES:
          # Auto-detect type, balanced budget (default)
          python3 generate.py --prompt "Create a book cover titled 'The Art of CRO'" --output cover.png

          # Force type and cheap budget
          python3 generate.py --prompt "A hand holding a skincare bottle" --type product-lifestyle --budget cheap --output photo.png

          # Explicit provider override (skips routing)
          python3 generate.py --prompt "Logo for a coffee brand" --provider ideogram --model ideogram-v3 --output logo.png

          # Show cost table
          python3 generate.py --show-costs
        """)
    )
    parser.add_argument("--prompt", default="", help="Generation prompt")
    parser.add_argument("--output", default="output.png", help="Output file path")
    parser.add_argument("--size", default="1024x1024", help="Image size, e.g. 1024x1536")
    parser.add_argument("--quality", default="medium", choices=["low", "medium", "high", "auto", "hd", "standard"], help="Quality tier (hd/standard are mapped to high/medium)")
    parser.add_argument("--output-format", default="png", choices=["png", "jpeg", "webp"], help="Output format")
    parser.add_argument("--output-compression", type=int, help="JPEG/WebP compression 0-100")
    parser.add_argument("--n", type=int, default=1, help="Number of variants")
    parser.add_argument("--type", help="Image type category (auto-detected if omitted)")
    parser.add_argument("--budget", default="balanced", choices=["cheap", "balanced", "premium"], help="Budget mode")
    parser.add_argument("--provider", help="Force a specific provider (skips auto-routing)")
    parser.add_argument("--model", help="Force a specific model (use with --provider)")
    parser.add_argument("--env-file", help="Path to .env file with API keys")
    parser.add_argument("--expand", default="auto", choices=["off", "lint", "auto", "llm"],
                        help="Prompt expansion: auto (default), off, lint only, or always use the LLM")
    parser.add_argument("--expand-model", default=None,
                        help="Chat model for --expand llm (default: GPT_IMAGE_EXPANDER_MODEL or gpt-4o-mini)")
    parser.add_argument("--expand-min-words", type=int, default=30,
                        help="auto expands prompts shorter than this (default: 30)")
    parser.add_argument("--show-costs", action="store_true", help="Print cost table and exit")
    parser.add_argument("--show-route", action="store_true", help="Print chosen route without generating")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if not args.prompt and not args.show_costs:
        parser.error("--prompt is required (unless using --show-costs)")

    registry = load_registry()

    if args.show_costs:
        print(format_cost_table(registry))
        return

    # Determine image type
    image_type = args.type
    if not image_type:
        image_type = detect_image_type(args.prompt, registry)
        if args.verbose:
            print(f"[router] Auto-detected type: {image_type}")

    # Validate type
    if image_type not in registry["image_types"]:
        print(f"[router] Unknown type '{image_type}'. Known types: {list(registry['image_types'].keys())}")
        sys.exit(1)

    # Pick provider and model
    if args.provider and args.model:
        provider_name = args.provider
        model_id = args.model
        quality_hint = None
        if args.verbose:
            print(f"[router] Forced provider: {provider_name}, model: {model_id}")
    else:
        provider_name, model_id, quality_hint = pick_model(image_type, args.budget, registry)
        if args.verbose:
            print(f"[router] Picked provider: {provider_name}, model: {model_id}, quality_hint: {quality_hint}")

    # Determine final quality (accept the DALL-E 3-era hd/standard aliases)
    final_quality = (quality_hint or args.quality).lower()
    final_quality = QUALITY_ALIASES.get(final_quality, final_quality)

    # Prompt expansion: the layer ChatGPT applies before it calls its image model.
    # auto stays deterministic on --show-route so a preview never spends a chat call.
    final_prompt = args.prompt
    expand_report = None
    if args.expand != "off":
        allow_llm = not args.show_route
        final_prompt, expand_report = expand_prompt(
            args.prompt,
            image_type=image_type,
            mode=args.expand,
            min_words=args.expand_min_words,
            model=args.expand_model,
            env_file=args.env_file,
            allow_llm=allow_llm,
        )
        if not args.show_route:
            for line in format_report(expand_report):
                print(f"[expand] {line}")
        if args.verbose and final_prompt != args.prompt:
            print(f"[expand] Final prompt: {final_prompt}")

    # Show route and exit if requested
    if args.show_route:
        type_desc = registry["image_types"][image_type]["description"]
        print(f"\n{'='*60}")
        print(f"ROUTE PREVIEW")
        print(f"{'='*60}")
        print(f"  Prompt:     {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}")
        if final_prompt != args.prompt:
            print(f"  Prompt+:    {final_prompt[:80]}{'...' if len(final_prompt) > 80 else ''}")
        elif expand_report and expand_report.get("would_expand"):
            print(f"  Prompt lint: short prompt ({expand_report['word_count_before']} words) - expand it in the agent")
        print(f"  Type:       {image_type}")
        print(f"  Budget:     {args.budget}")
        print(f"  Provider:   {provider_name}")
        print(f"  Model:      {model_id}")
        print(f"  Quality:    {final_quality}")
        print(f"  Size:       {args.size}")
        print(f"  Type desc:  {type_desc}")
        print(f"{'='*60}\n")
        return

    # Instantiate provider
    try:
        provider = get_provider(provider_name, env_file=args.env_file)
    except RuntimeError as e:
        print(f"[router] ERROR: {e}")
        print(f"[router] To use {provider_name}, add {registry['providers'][provider_name]['env_key']}=... to your .env file")
        sys.exit(1)

    # Generate
    print(f"[router] Generating via {provider_name}/{model_id} | type={image_type} | budget={args.budget} | quality={final_quality}")
    try:
        paths = provider.generate(
            prompt=final_prompt,
            size=args.size,
            quality=final_quality,
            output_path=args.output,
            n=args.n,
            model_id=model_id,
        )
    except NotImplementedError as e:
        print(f"[router] ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[router] Generation failed: {e}")
        sys.exit(1)

    # Post-process: convert format/compression if needed
    if args.output_format != "png" or args.output_compression is not None:
        try:
            from PIL import Image
            for p in paths:
                img = Image.open(p)
                if img.mode in ("RGBA", "P") and args.output_format in ("jpeg", "jpg"):
                    img = img.convert("RGB")
                save_kwargs = {}
                if args.output_format in ("jpeg", "jpg") and args.output_compression is not None:
                    save_kwargs["quality"] = args.output_compression
                    save_kwargs["optimize"] = True
                elif args.output_format == "webp" and args.output_compression is not None:
                    save_kwargs["quality"] = args.output_compression
                new_p = os.path.splitext(p)[0] + f".{args.output_format}"
                img.save(new_p, **save_kwargs)
                if new_p != p:
                    os.remove(p)
                print(f"[router] Saved: {new_p}")
        except ImportError:
            print("[router] Warning: Pillow not installed; skipping format conversion. Install with: pip install Pillow")
            for p in paths:
                print(f"[router] Saved: {p}")
    else:
        for p in paths:
            print(f"[router] Saved: {p}")

    print(f"[router] Done. {len(paths)} image(s) generated.")


if __name__ == "__main__":
    main()
