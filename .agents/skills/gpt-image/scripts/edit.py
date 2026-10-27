#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.31.0"]
# ///
"""
GPT Image Router — Multi-provider image editing.
Defaults to OpenAI (best edit support) but allows explicit provider override.
Drop-in replacement for the old OpenAI-only edit.py.
"""

import os, sys, json, argparse, textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
REGISTRY_PATH = os.path.join(SKILL_DIR, "model-registry.json")

sys.path.insert(0, SCRIPT_DIR)
from providers import get_provider
from prompt_expander import expand_prompt, format_report

QUALITY_ALIASES = {"hd": "high", "standard": "medium"}


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="GPT Image Router — edit images via the best backend",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        EXAMPLES:
          # Default: OpenAI edit (best multi-image compositing)
          python3 edit.py --prompt "Change background to sunset" --images photo.png --output sunset.png

          # Multi-image compositing (OpenAI only)
          python3 edit.py --prompt "Place product from Image 2 into scene Image 1" --images scene.png product.png --output composite.png

          # Stability edit (single image search-and-replace)
          python3 edit.py --prompt "Remove the red car" --images photo.png --provider stability --model sd-3-5-large --output cleaned.png
        """)
    )
    parser.add_argument("--prompt", required=True, help="Editing instruction")
    parser.add_argument("--images", required=True, nargs="+", help="Input image path(s)")
    parser.add_argument("--output", default="output.png", help="Output file path")
    parser.add_argument("--size", default="1024x1024", help="Output size")
    parser.add_argument("--quality", default="medium", choices=["low", "medium", "high", "auto", "hd", "standard"], help="Quality tier (hd/standard are mapped to high/medium)")
    parser.add_argument("--output-format", default="png", choices=["png", "jpeg", "webp"], help="Output format")
    parser.add_argument("--output-compression", type=int, help="JPEG/WebP compression 0-100")
    parser.add_argument("--n", type=int, default=1, help="Number of variants")
    parser.add_argument("--provider", help="Provider override (default: openai)")
    parser.add_argument("--model", help="Model override")
    parser.add_argument("--env-file", help="Path to .env file with API keys")
    parser.add_argument("--expand", default="auto", choices=["off", "lint", "auto", "llm"],
                        help="Prompt expansion: auto (default), off, lint only, or always use the LLM")
    parser.add_argument("--expand-model", default=None,
                        help="Chat model for --expand llm (default: GPT_IMAGE_EXPANDER_MODEL or gpt-4o-mini)")
    parser.add_argument("--expand-min-words", type=int, default=20,
                        help="auto expands edit instructions shorter than this (default: 20)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()
    registry = load_registry()

    # Editing support matrix
    edit_providers = {
        "openai": {"max_images": 10, "models": ["gpt-image-2"]},
        "stability": {"max_images": 1, "models": ["sd-3-5-large", "sd-3-5-large-turbo"]},
    }

    # Determine provider
    provider_name = args.provider or "openai"
    model_id = args.model or ("gpt-image-2" if provider_name == "openai" else "sd-3-5-large")

    if provider_name not in edit_providers:
        supported = ", ".join(edit_providers.keys())
        print(f"[router] ERROR: Provider '{provider_name}' does not support image editing.")
        print(f"[router] Editing is only supported by: {supported}")
        print(f"[router] For compositing/editing with other providers, generate from scratch instead.")
        sys.exit(1)

    edit_info = edit_providers[provider_name]
    if len(args.images) > edit_info["max_images"]:
        print(f"[router] ERROR: {provider_name} supports max {edit_info['max_images']} input image(s), got {len(args.images)}")
        sys.exit(1)

    if args.verbose:
        print(f"[router] Edit mode: provider={provider_name}, model={model_id}, images={len(args.images)}")

    # Instantiate provider
    try:
        provider = get_provider(provider_name, env_file=args.env_file)
    except RuntimeError as e:
        print(f"[router] ERROR: {e}")
        print(f"[router] To use {provider_name}, add {registry['providers'][provider_name]['env_key']}=... to your .env file")
        sys.exit(1)

    # Normalize quality aliases and expand the edit instruction. Edit prompts use
    # stricter rules that preserve identity and forbid inventing extra changes.
    final_quality = args.quality.lower()
    final_quality = QUALITY_ALIASES.get(final_quality, final_quality)

    final_prompt = args.prompt
    if args.expand != "off":
        final_prompt, expand_report = expand_prompt(
            args.prompt,
            mode=args.expand,
            min_words=args.expand_min_words,
            model=args.expand_model,
            env_file=args.env_file,
            is_edit=True,
        )
        for line in format_report(expand_report):
            print(f"[expand] {line}")
        if args.verbose and final_prompt != args.prompt:
            print(f"[expand] Final instruction: {final_prompt}")

    # Run edit
    print(f"[router] Editing via {provider_name}/{model_id} | images={len(args.images)} | quality={final_quality}")
    try:
        paths = provider.edit(
            prompt=final_prompt,
            images=args.images,
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
        print(f"[router] Editing failed: {e}")
        sys.exit(1)

    # Post-process format
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
            print("[router] Warning: Pillow not installed; skipping format conversion.")
            for p in paths:
                print(f"[router] Saved: {p}")
    else:
        for p in paths:
            print(f"[router] Saved: {p}")

    print(f"[router] Done. {len(paths)} image(s) edited.")


if __name__ == "__main__":
    main()
