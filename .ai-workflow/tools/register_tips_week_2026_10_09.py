#!/usr/bin/env python3
"""Register the 2026-10-09 Tips week pack (4 posts, 4 lanes).

1. Adds 4 NEW items to SYNC_DATA.items in ridwan_content_system_updated.html (none came
   from the Idea backlog, so no backlog id is reused). Status "Created", never "Published".
   Skips any id that already exists. Refuses if a folder or asset is missing on disk.
2. Appends TIP-KOOLESTPRO-<TOPIC>-* keys to koolestpro-social-content.json/.md. Every
   single-image caption carries one assetPath + captionKey (caption = image rule, 2026-09-28).

Run from anywhere:  python3 .ai-workflow/tools/register_tips_week_2026_10_09.py [--dry-run]
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK = json.load(open(os.path.join(ROOT, ".ai-workflow/tips-weekly-2026-10-09/week_pack.json")))
SYS = os.path.join(ROOT, "ridwan_content_system_updated.html")
SC_JSON = os.path.join(ROOT, "koolestpro-social-content.json")
SC_MD = os.path.join(ROOT, "koolestpro-social-content.md")
NOW = "2026-10-09T16:00:00Z"
DRY = "--dry-run" in sys.argv

TOPIC = {  # slug -> (key stem, lane, x single slide map)
    "materialkitchen-first-screen-build-breakdown": ("MKFOLD", "A Build breakdown", {"X1": 1}),
    "first-screen-leaks-before-bfcm": ("LEAKS4", "C Save-worthy list (V4 carousel)", {"X1": 2, "X2": 4, "X3": 5}),
    "extra-costs-top-checkout-killer": ("COSTS40", "E Sourced take", {"X1": 1}),
    "allbirds-shipping-next-to-price": ("ALLBIRDSSHIP", "B Found page", {"X1": 1}),
}


def split_tags(text):
    lines = text.rstrip().split("\n")
    if lines and lines[-1].startswith("#"):
        return "\n".join(lines[:-1]).rstrip(), [t.lstrip("#") for t in lines[-1].split()]
    return text, []


def x_singles(tabs):
    if "tab-x-image" in tabs:
        return {"X1": tabs["tab-x-image"]}
    out = {}
    for part in re.split(r"\n\n(?=X\d )", tabs["tab-twitter-angles"]):
        head, body = part.split("\n", 1)
        out[head.split()[0]] = body.strip()
    return out


def build():
    items, assets, md = [], {}, []
    for slug, v in PACK.items():
        m, tabs, n = v["meta"], v["tabs"], v["slides"]
        stem, lane, xmap = TOPIC[slug]
        adir = f"outputs/tips/{slug}-assets"
        slides = [f"{adir}/slide{i}.png" for i in range(1, n + 1)]
        for p in [m["folder"], *slides]:
            if not os.path.exists(os.path.join(ROOT, p)):
                raise SystemExit(f"[FAIL] missing on disk: {p}")
        li, li_tags = split_tags(tabs["tab-linkedin"])
        xs = x_singles(tabs)
        for k, t in xs.items():
            if len(t) > 280:
                raise SystemExit(f"[FAIL] {slug} {k} is {len(t)} chars")
        if "tab-twitter-thread" in tabs:
            for i, t in enumerate(tabs["tab-twitter-thread"].split("\n\n"), 1):
                if len(t) > 280:
                    raise SystemExit(f"[FAIL] {slug} thread {i} is {len(t)} chars")
        for t in tabs.values():
            if "—" in t:
                raise SystemExit(f"[FAIL] em dash in {slug}")
        items.append({
            "id": m["id"], "type": "Tip", "title": m["title"], "slug": slug, "status": "Created", "day": "",
            "created": NOW, "folder": m["folder"], "week": "Week of October 9", "month": "October 2026",
            "monthSlug": "2026-10", "brand": "Koolestpro", "lane": lane, "linkedAt": NOW,
            "captions": {"linkedin": li, "x": list(xs.values())},
            "assets": {"images": slides, "video": None},
        })
        K = f"TIP-KOOLESTPRO-{stem}"
        base = {"status": "Not Posted", "postedAt": None}
        if n == 1:
            assets[f"{K}-COVER"] = {"platform": ["linkedin"], "assetType": "image", "assetPath": slides[0],
                                    "captionKey": f"{K}-COVER", "caption": li, "hashtags": li_tags, **base}
        else:
            assets[f"{K}-COVER"] = {"platform": ["linkedin"], "assetType": "image", "assetPath": slides[0],
                                    "captionKey": f"{K}-COVER", "caption": li, "hashtags": li_tags, **base}
            assets[f"{K}-CAROUSEL"] = {"platform": ["linkedin"], "assetType": "carousel", "assetPath": slides,
                                       "captionKey": f"{K}-CAROUSEL", "caption": li, "hashtags": li_tags, **base}
            ig, ig_tags = split_tags(tabs["tab-ig"])
            assets[f"{K}-IG"] = {"platform": ["instagram"], "assetType": "carousel", "assetPath": slides,
                                 "captionKey": f"{K}-IG", "caption": ig, "hashtags": ig_tags, **base}
            assets[f"{K}-X-THREAD"] = {"platform": ["x"], "assetType": "text", "assetPath": None,
                                       "captionKey": f"{K}-X-THREAD", "caption": tabs["tab-twitter-thread"], "hashtags": [], **base}
        for k, t in xs.items():
            assets[f"{K}-{k}"] = {"platform": ["x"], "assetType": "image", "assetPath": slides[xmap[k] - 1],
                                  "captionKey": f"{K}-{k}", "caption": t, "hashtags": [], **base}
        # markdown block
        md += ["", f"## {K} | {m['title']} (Tips week pack 2026-10-09, lane {lane})", "",
               f"Post file: `{m['folder']}`", f"Assets: `{adir}/slide1..{n}.png`", f"Pipeline item: `{m['id']}`", "",
               "| Key | Platform | Asset |", "|---|---|---|"]
        for k, a in assets.items():
            if k.startswith(K + "-"):
                ap = a["assetPath"]
                md.append(f"| {k} | {', '.join(a['platform'])} | {('slides 1-%d' % n) if isinstance(ap, list) else ('`%s`' % ap if ap else 'text')} |")
        for k, a in assets.items():
            if k.startswith(K + "-"):
                md += ["", f"### {k}", "", "```", a["caption"] + (("\n\n" + " ".join("#" + t for t in a["hashtags"])) if a["hashtags"] else ""), "```"]
    return items, assets, md


def main():
    items, assets, md = build()
    print(f"{len(items)} items, {len(assets)} caption keys built")
    if DRY:
        return
    html = open(SYS, encoding="utf-8").read()
    m = re.search(r'(<script id="cowork-sync-data"[^>]*>)(.*?)(</script>)', html, re.S)
    data = json.loads(m.group(2))
    have = {i.get("id") for i in data["items"]}
    added = 0
    for it in items:
        if it["id"] in have:
            print("  [skip] item exists", it["id"]); continue
        data["items"].append(it); added += 1
    ids = [i.get("id") for i in data["items"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("[FAIL] duplicate ids in SYNC_DATA.items")
    months = data.setdefault("months", {})
    if "2026-10" not in months:
        months["2026-10"] = {"label": "October 2026", "htmlPath": "outputs/ideas/ideas_2026-10.html",
                             "jsonPath": "outputs/ideas/ideas_2026-10.json", "totalIdeas": 0}
        print("  added months['2026-10']")
    if added:
        shutil.copyfile(SYS, SYS + ".bak")
        html = html[:m.start(2)] + json.dumps(data, indent=2, ensure_ascii=False) + html[m.end(2):]
        open(SYS, "w", encoding="utf-8").write(html)
    print(f"  pipeline: {added} added, {len(data['items'])} items total")

    d = json.load(open(SC_JSON, encoding="utf-8"))
    new = 0
    for k, v in assets.items():
        if k in d["assets"]:
            print("  [skip]", k); continue
        d["assets"][k] = v; new += 1
    for it in items:
        if it["id"] not in d["relatedPipelineItemIds"]:
            d["relatedPipelineItemIds"].append(it["id"])
    d["updated"] = NOW
    json.dump(d, open(SC_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    if new:
        with open(SC_MD, "a", encoding="utf-8") as f:
            f.write("\n".join(md) + "\n")
    print(f"  social content: {new} keys added")


if __name__ == "__main__":
    main()
