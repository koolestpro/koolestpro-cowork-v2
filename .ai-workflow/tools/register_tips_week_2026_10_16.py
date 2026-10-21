#!/usr/bin/env python3
"""Register the October 16, 2026 Tips pack in the content system and social library."""
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, ".ai-workflow/tools"))
from caption_fit import check as check_caption_fit

PACK_PATH = os.path.join(ROOT, ".ai-workflow/tips-weekly-2026-10-16/week_pack.json")
SYS = os.path.join(ROOT, "ridwan_content_system_updated.html")
SC_JSON = os.path.join(ROOT, "koolestpro-social-content.json")
SC_MD = os.path.join(ROOT, "koolestpro-social-content.md")
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
DRY = "--dry-run" in sys.argv

TOPIC = {
    "caraway-product-page-proof-before-scroll": ("CARAWAYPROOF", "A Build breakdown"),
    "v1ce-tap-card-explains-the-next-step": ("V1CETAP", "B Found page"),
    "three-mobile-checks-before-you-ship": ("MOBILECHECKS", "C Save-worthy list (V4 carousel)"),
    "owala-product-page-answers-fast": ("OWALAPDP", "D Expert remix"),
}


def split_tags(text):
    lines = text.rstrip().split("\n")
    if lines and lines[-1].startswith("#"):
        return "\n".join(lines[:-1]).rstrip(), [tag.lstrip("#") for tag in lines[-1].split()]
    return text, []


def make_records(pack):
    items, assets, markdown_sections = [], {}, []
    for slug, post in pack.items():
        if slug not in TOPIC:
            raise SystemExit(f"[FAIL] unexpected post in pack: {slug}")
        meta, tabs = post["meta"], post["tabs"]
        stem, lane = TOPIC[slug]
        n = post["slides"]
        asset_dir = f"outputs/tips/{slug}-assets"
        slide_paths = [f"{asset_dir}/slide{i}.png" for i in range(1, n + 1)]
        for path in [meta["folder"], *slide_paths]:
            if not os.path.isfile(os.path.join(ROOT, path)):
                raise SystemExit(f"[FAIL] missing on disk: {path}")
        if "—" in meta["title"] or any("—" in caption for caption in tabs.values()):
            raise SystemExit(f"[FAIL] em dash in {slug}")

        linkedin, linkedin_tags = split_tags(tabs["tab-linkedin"])
        x_captions = {}
        if "tab-x-image" in tabs:
            x_captions["X1"] = tabs["tab-x-image"]
        else:
            for key, caption in tabs.items():
                match = re.fullmatch(r"tab-x(\d+)", key)
                if match:
                    x_captions[f"X{match.group(1)}"] = caption

        xmap = post.get("xmap", {"X1": 1})
        if set(x_captions) != set(xmap):
            raise SystemExit(f"[FAIL] X captions and slide map differ for {slug}")
        for key, caption in x_captions.items():
            if len(caption) > 280:
                raise SystemExit(f"[FAIL] {slug} {key} is {len(caption)} characters")
            if re.search(r"#\w", caption):
                raise SystemExit(f"[FAIL] hashtag in X caption {slug} {key}")
            x_slide = slide_paths[xmap[key] - 1]
            problems = check_caption_fit(caption, x_slide, platform="Twitter")
            if problems:
                raise SystemExit(f"[FAIL] {slug} {key}: {'; '.join(problems)}")

        item = {
            "id": meta["id"],
            "type": "Tip",
            "title": meta["title"],
            "slug": slug,
            "status": "Created",
            "day": "",
            "created": NOW,
            "folder": meta["folder"],
            "week": "Week of October 16",
            "month": "October 2026",
            "monthSlug": "2026-10",
            "brand": "Koolestpro",
            "lane": lane,
            "linkedAt": NOW,
            "captions": {"linkedin": linkedin, "x": list(x_captions.values())},
            "assets": {"images": slide_paths, "video": None},
        }
        items.append(item)

        key_prefix = f"TIP-KOOLESTPRO-{stem}"
        base = {"status": "Not Posted", "postedAt": None}
        cover_caption, cover_tags = split_tags(tabs.get("tab-linkedin-cover", tabs["tab-linkedin"]))
        cover_fit = check_caption_fit(cover_caption, slide_paths[0], platform="LinkedIn")
        if cover_fit:
            raise SystemExit(f"[FAIL] {slug} LinkedIn cover: {'; '.join(cover_fit)}")
        if n == 1:
            linkedin_fit = check_caption_fit(linkedin, slide_paths[0], platform="LinkedIn")
            if linkedin_fit:
                raise SystemExit(f"[FAIL] {slug} LinkedIn: {'; '.join(linkedin_fit)}")
        if n == 1:
            assets[f"{key_prefix}-COVER"] = {
                "platform": ["linkedin"], "assetType": "image", "assetPath": slide_paths[0],
                "captionKey": f"{key_prefix}-COVER", "caption": cover_caption,
                "hashtags": cover_tags, **base,
            }
        else:
            assets[f"{key_prefix}-COVER"] = {
                "platform": ["linkedin"], "assetType": "image", "assetPath": slide_paths[0],
                "captionKey": f"{key_prefix}-COVER", "caption": cover_caption,
                "hashtags": cover_tags, **base,
            }
            assets[f"{key_prefix}-CAROUSEL"] = {
                "platform": ["linkedin"], "assetType": "carousel", "assetPath": slide_paths,
                "captionKey": f"{key_prefix}-CAROUSEL", "caption": linkedin,
                "hashtags": linkedin_tags, **base,
            }
            ig, ig_tags = split_tags(tabs["tab-ig"])
            assets[f"{key_prefix}-IG"] = {
                "platform": ["instagram"], "assetType": "carousel", "assetPath": slide_paths,
                "captionKey": f"{key_prefix}-IG", "caption": ig,
                "hashtags": ig_tags, **base,
            }
        for key, caption in x_captions.items():
            slide_path = slide_paths[xmap[key] - 1]
            assets[f"{key_prefix}-{key}"] = {
                "platform": ["x"], "assetType": "image", "assetPath": slide_path,
                "captionKey": f"{key_prefix}-{key}", "caption": caption,
                "hashtags": [], **base,
            }

        section = [
            "",
            f"## {key_prefix} | {meta['title']} (Tips week pack 2026-10-16, lane {lane})",
            "",
            f"Post file: `{meta['folder']}`",
            f"Assets: `{asset_dir}/slide1..{n}.png`",
            f"Pipeline item: `{meta['id']}`",
            "",
            "| Key | Platform | Asset |",
            "|---|---|---|",
        ]
        for key, asset in assets.items():
            if not key.startswith(key_prefix + "-"):
                continue
            path = asset["assetPath"]
            asset_label = (
                f"slides 1-{n}" if isinstance(path, list)
                else f"`{path}`" if path
                else "text"
            )
            section.append(f"| {key} | {', '.join(asset['platform'])} | {asset_label} |")
        for key, asset in assets.items():
            if key.startswith(key_prefix + "-"):
                text = asset["caption"]
                if asset["hashtags"]:
                    text += "\n\n" + " ".join("#" + tag for tag in asset["hashtags"])
                section.extend(["", f"### {key}", "", "```", text, "```"])
        markdown_sections.append((key_prefix, section))

    if len({item["id"] for item in items}) != len(items):
        raise SystemExit("[FAIL] duplicate IDs in pack")
    return items, assets, markdown_sections


def main():
    pack = json.load(open(PACK_PATH, encoding="utf-8"))
    if set(pack) != set(TOPIC):
        raise SystemExit("[FAIL] pack post set differs from the expected four posts")
    items, new_assets, markdown_sections = make_records(pack)

    with open(SYS, encoding="utf-8") as source:
        html = source.read()
    match = re.search(r'(<script id="cowork-sync-data"[^>]*>)(.*?)(</script>)', html, re.S)
    if not match:
        raise SystemExit("[FAIL] content-system JSON block not found")
    data = json.loads(match.group(2))
    if not isinstance(data.get("items"), list):
        raise SystemExit("[FAIL] content-system items is not a list")
    ids = [item.get("id") for item in data["items"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("[FAIL] duplicate IDs already exist in content system")
    existing_ids = set(ids)

    social = json.load(open(SC_JSON, encoding="utf-8"))
    if not isinstance(social.get("assets"), dict):
        raise SystemExit("[FAIL] social library assets is not an object")
    missing_items = [item for item in items if item["id"] not in existing_ids]
    added_assets = {key: asset for key, asset in new_assets.items() if key not in social["assets"]}
    related_ids = social.setdefault("relatedPipelineItemIds", [])
    related_added = False
    for item in items:
        if item["id"] not in related_ids:
            related_ids.append(item["id"])
            related_added = True
    social["updated"] = NOW
    social["assets"].update(added_assets)

    original_md = open(SC_MD, encoding="utf-8").read()
    new_markdown = [
        line
        for prefix, section in markdown_sections
        if f"## {prefix} |" not in original_md
        and any(key.startswith(prefix + "-") for key in added_assets)
        for line in section
    ]

    if not missing_items and not added_assets and not related_added:
        print("No new pipeline items or social keys to register.")
        return

    for item in missing_items:
        data["items"].append(item)
    months = data.setdefault("months", {})
    if "2026-10" not in months:
        months["2026-10"] = {
            "label": "October 2026",
            "htmlPath": "outputs/ideas/ideas_2026-10.html",
            "jsonPath": "outputs/ideas/ideas_2026-10.json",
            "totalIdeas": 0,
        }
    if len({item.get("id") for item in data["items"]}) != len(data["items"]):
        raise SystemExit("[FAIL] duplicate IDs after registration")

    if DRY:
        print(f"Would add {len(missing_items)} pipeline item(s) and {len(added_assets)} social key(s).")
        print(f"Validated {len(items)} posts and their exported PNGs. No files changed.")
        return

    backup = SYS + ".bak.tips-2026-10-16"
    if os.path.exists(backup):
        raise SystemExit(f"[FAIL] refusing to overwrite existing backup: {backup}")
    shutil.copy2(SYS, backup)
    updated_html = html[:match.start(2)] + json.dumps(data, indent=2, ensure_ascii=False) + html[match.end(2):]
    with open(SYS, "w", encoding="utf-8") as target:
        target.write(updated_html)
    with open(SC_JSON, "w", encoding="utf-8") as target:
        json.dump(social, target, indent=2, ensure_ascii=False)
    if new_markdown:
        with open(SC_MD, "a", encoding="utf-8") as target:
            target.write("\n".join(new_markdown) + "\n")

    print(f"Pipeline: {len(missing_items)} item(s) added; all statuses Created.")
    print(f"Social library: {len(added_assets)} caption key(s) added; all statuses Not Posted.")
    print(f"Content-system backup: {os.path.basename(backup)}")


if __name__ == "__main__":
    main()
