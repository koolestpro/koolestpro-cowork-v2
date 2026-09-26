#!/usr/bin/env python3
"""
harvest_content.py — V2 distribution pipeline, Step 2.

Parse a generator's companion HTML output, pull out every caption/copy variant
it already writes plus the real file paths of every generated asset, and emit a
single structured record (JSON). This is the bridge between content GENERATION
(V1, already built) and content DISTRIBUTION (V2): the harvested record is what
qa_check.py inspects and populate_sheet.py expands into per-post Sheet rows.

Caption DOM differs per skill (confirmed by direct inspection of real outputs):
  - CRO Fix  (outputs/cro-fixes/{slug}_content.html):
        div.tab-panel#tab-linkedin / #tab-ig / #tab-hook /
        #tab-twitter-angles / #tab-twitter-thread   -> text in a <pre>
  - Tips     (outputs/tips/{slug}.html):
        div.tab-panel#tab-li-long / #tab-li-hook / #tab-x-thread /
        #tab-x-singles / #tab-ig                     -> text in a <pre>
  - Static Ad (outputs/static-ads/{slug}_{date}/index.html):
        div.copy-block > div.section-title("LinkedIn Caption") + <p>
        div.copy-block > div.section-title("X Posts") + N x div.x-post
  - Template Showcase (outputs/templates/{slug}_{date}/index.html):
        same copy-block/x-post structure as Static Ad.

So there are two structural families (tab-based, block-based) and four
skill flavours. We match by known ID/class per skill, never by guessing.

Usage:
    python3 harvest_content.py <companion_html> [--out record.json]
                              [--project-root DIR] [--merge-pipeline]

If --out is omitted, the record is written next to the companion HTML as
`{slug}_harvest.json` and also printed to stdout.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("harvest_content.py requires beautifulsoup4 (pip install beautifulsoup4 --break-system-packages)")

ASSET_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".mp4", ".webm", ".mov", ".gif", ".pdf")
# Never treat these as post assets — they're chrome/branding, not deliverables.
ASSET_SKIP_SUBSTR = ("cloudinary.com", "avatar-circle", "data:", "assets/frames/")

# Unified tab-id -> canonical-name map. Two tab vocabularies exist in real
# outputs (confirmed): the CRO-Fix/gold-standard-Tips scheme (tab-linkedin,
# tab-twitter-angles, tab-twitter-thread) and the newer content-engine Tips
# scheme (tab-li-long, tab-li-hook, tab-x-singles, tab-x-thread). Parse by
# DOM structure, not skill type, so both are covered regardless of which
# generator produced the file.
UNIFIED_TAB_MAP = {
    "tab-linkedin": "linkedin",
    "tab-li-long": "linkedin",
    "tab-li-hook": "hook",
    "tab-hook": "hook",
    "tab-ig": "instagram",
    "tab-twitter-angles": "x_angles",
    "tab-x-singles": "x_singles",
    "tab-twitter-thread": "x_thread",
    "tab-x-thread": "x_thread",
}

# Infer skill flavour from the output folder when the POST_TYPE const is absent
# (older hand-built files lack it).
FOLDER_TYPE_MAP = {
    "cro-fixes": "CRO Fix",
    "tips": "Tip",
    "static-ads": "Static Ad",
    "templates": "Template Showcase",
    "case-studies": "Case Study",
}

BLOCK_TITLE_MAP = {
    "linkedin caption": "linkedin",
    "x posts": "x",
    "twitter posts": "x",
}


def read_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_post_consts(html):
    """Pull POST_BRAND / POST_SLUG / POST_TYPE / POST_FOLDER / dateStr from the
    inline <script> block. These are the authoritative identity fields."""
    consts = {}
    for key in ("POST_BRAND", "POST_SLUG", "POST_TYPE", "POST_FOLDER", "dateStr"):
        m = re.search(rf"(?:const\s+)?{key}\s*=\s*'([^']*)'", html)
        if m:
            consts[key] = m.group(1)
    return consts


def build_item_id(consts):
    """Reproduce the id sendToPipeline() builds so the harvest record joins
    cleanly to the pipeline item / Sheet row."""
    ptype = consts.get("POST_TYPE", "")
    slug = consts.get("POST_SLUG", "")
    date = consts.get("dateStr", "")
    if not date:
        date = datetime.now(timezone.utc).strftime("%Y%m%d")
    base = ptype.lower().replace(" ", "-")
    return f"{base}-{slug}-{date}"


def clean(text):
    if text is None:
        return ""
    # collapse trailing whitespace runs but keep paragraph breaks
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").split("\n")]
    out = "\n".join(lines).strip()
    return out


# Bug fixed 2026-07-29: tab-twitter-angles / tab-twitter-thread (and the Tips
# content-engine's tab-x-singles / tab-x-thread) each pack MULTIPLE standalone
# tweet variants into one <pre>/panel as human-readable plain text (e.g.
# "Tweet A (The Rule):\n...\n\nTweet B (The Contrast):\n...") rather than
# separate DOM elements the way Static Ad/Template Showcase's .x-post divs
# are. Treating that whole blob as ONE caption string caused two confirmed
# live bugs: a single-tweet slot got all 3 variants glued together (>280
# chars, reads as "Tweet A ... Tweet B ... Tweet C ..."), and the char-limit
# check in qa_check.py/populate_sheet.py never fired because it only runs on
# list values. Fix: recognize these multi-variant shapes and always emit a
# LIST of individually-sized tweet strings, never one opaque blob.
# Two label conventions confirmed in real output ("Tweet A (The Rule):" and
# "ANGLE A:") — different generation runs of the same tab use different
# wording, so match both rather than assuming one is canonical.
TWEET_LABEL_RE = re.compile(r'^(?:Tweet|ANGLE)\s+[A-Z0-9]\b[^\n]*:[ \t]*\n', re.MULTILINE | re.IGNORECASE)
THREAD_LINE_RE = re.compile(r'(?=^\d+/[ \t])', re.MULTILINE)

# Bug found 2026-09-08 on outputs/tips/cold-warm-hot-page-matching_2026-05-10.html
# (and present in several other older tips: shopify_page_types_carousel.html,
# why-your-pdp-loses-sales-at-60-scroll_2026-04-29.html): the "X Singles x3"
# tab's own variants are NOT labeled "Tweet A"/"ANGLE A" (TWEET_LABEL_RE), nor
# numbered "1/" (THREAD_LINE_RE) — they use short all-caps headers like
# "THE RULE:" / "— THE RULE —" separated by a standalone line of box-drawing
# dashes ("────" or "———"). tab-x-singles was never wired into either split
# path, so it always fell through as one un-split blob glued together with
# ~140-180 char variants each — over 280 combined, and it's exactly the kind
# of multi-variant shape the module's own docstring says should always become
# a list. Splitting on the separator line alone (keeping each chunk's own
# label) is enough — verified each resulting chunk stays well under 280 chars.
SEPARATOR_LINE_RE = re.compile(r'\n\s*[─\-—]{4,}\s*\n')

# Tips (content-engine scheme) sometimes marks the X-singles tab with real
# per-variant DOM (div.tw-block > div.tw-text) instead of plain text labels —
# prefer that structure when present, it's more reliable than regex-guessing.
def _tw_block_variants(panel):
    blocks = panel.select("div.tw-block")
    if not blocks:
        return None
    out = []
    for b in blocks:
        t = b.find(class_="tw-text") or b
        txt = clean(t.get_text())
        if txt:
            out.append(txt)
    return out or None


def split_multi_tweet_text(tab_id, text):
    """Return a list of standalone tweet strings if this tab's raw text is a
    known multi-variant blob, else None (caller keeps it as a single string)."""
    if tab_id in ("tab-twitter-angles",):
        parts = [p.strip() for p in TWEET_LABEL_RE.split(text) if p.strip()]
        if len(parts) > 1:
            return parts
    if tab_id in ("tab-twitter-thread", "tab-x-thread"):
        parts = [p.strip() for p in THREAD_LINE_RE.split(text) if p.strip()]
        if len(parts) > 1:
            return parts
    if tab_id in ("tab-x-singles",):
        parts = [p.strip() for p in SEPARATOR_LINE_RE.split(text) if p.strip()]
        if len(parts) > 1:
            return parts
    return None


# Noise elements that must never leak into harvested caption text — some
# older Tips output wraps a tab's real copy alongside a UI label/copy-button
# inside the same panel with no <pre>, so a blind panel.get_text() glues
# "X / TWITTER · THREAD" + "Copy" button text onto the real caption.
PANEL_NOISE_CLASSES = ("post-label",)
PANEL_NOISE_TAGS = ("button",)


def _panel_text_excluding_chrome(panel):
    import copy as _copy
    clone = _copy.copy(panel)
    for tag in clone.find_all(PANEL_NOISE_TAGS):
        tag.decompose()
    for cls in PANEL_NOISE_CLASSES:
        for el in clone.find_all(class_=cls):
            el.decompose()
    return clean(clone.get_text())


def parse_tab_captions(soup):
    """CRO Fix / Tips: div.tab-panel[id^=tab-] with caption text inside —
    usually a <pre>, sometimes (older Tips files) plain divs. Skill-agnostic —
    matches on the unified tab vocabulary. Emits a LIST for tabs known to
    carry multiple standalone tweet variants, a single string otherwise.

    Bug fixed 2026-09-08: a third, oldest Tips DOM flavour exists too —
    div.tpanel (not div.tab-panel) with the real caption text inside a
    div.pcontent child (not a <pre>). Confirmed live on
    outputs/tips/cold-warm-hot-page-matching_2026-05-10.html, which was
    silently returning zero captions ("DOM may have changed" warning) even
    though the file has a complete 5-tab Post Copy section. Only 1 file in
    outputs/tips/ uses this flavour as of 2026-09-08 (grep for
    class="tpanel confirmed), so this is a narrow widen, not a rewrite."""
    caps = {}
    for panel in soup.select("div.tab-panel[id^='tab-'], div.tpanel[id^='tab-']"):
        tab_id = panel.get("id", "")
        canonical = UNIFIED_TAB_MAP.get(tab_id, tab_id.replace("tab-", ""))

        block_variants = _tw_block_variants(panel)
        if block_variants:
            caps[canonical] = {"text": block_variants, "source_tab": tab_id}
            continue

        pre = panel.find("pre")
        pcontent = panel.find(class_="pcontent")
        if pre:
            text = clean(pre.get_text())
        elif pcontent:
            text = clean(pcontent.get_text())
        else:
            text = _panel_text_excluding_chrome(panel)
        if not text:
            continue

        variants = split_multi_tweet_text(tab_id, text)
        caps[canonical] = {"text": variants if variants else text, "source_tab": tab_id}
    return caps


# Trailing run of hashtags at the end of a caption ("#foo #bar #baz"), with
# optional leading blank line/whitespace before it. Ridwan's preference
# (confirmed 2026-07-22, after the first live KURA X post): no hashtags on X.
TRAILING_HASHTAGS_RE = re.compile(r"\s*(?:#[\w-]+\s*){1,}$")


def strip_trailing_hashtags(text):
    return TRAILING_HASHTAGS_RE.sub("", text).rstrip()


def parse_block_captions(soup):
    """Static Ad / Template Showcase: div.copy-block with .section-title + p / .x-post."""
    caps = {}
    for block in soup.select("div.copy-block"):
        title_el = block.find(class_="section-title")
        if not title_el:
            continue
        title = title_el.get_text(strip=True).lower()
        canonical = BLOCK_TITLE_MAP.get(title)
        if canonical is None:
            continue  # skip Research Notes and any non-caption blocks
        if canonical == "x":
            # separator="\n" is required here — bug fixed 2026-07-22: bare
            # get_text() drops <br>/<p> tag boundaries entirely, gluing
            # adjacent lines together with zero whitespace (e.g. "code.This
            # is KURA" instead of a line break between them). This shipped
            # in the first live KURA X post before anyone caught it.
            posts = [clean(x.get_text(separator="\n")) for x in block.select(".x-post")]
            posts = [re.sub(r"^\d+\.\s*", "", p) for p in posts if p]
            posts = [strip_trailing_hashtags(p) for p in posts]
            caps["x"] = {"text": posts, "source_tab": "copy-block:X Posts"}
        else:
            p = block.find("p")
            text = clean(p.get_text(separator="\n") if p else block.get_text(separator="\n").replace(title_el.get_text(), ""))
            if text:
                caps[canonical] = {"text": text, "source_tab": f"copy-block:{title_el.get_text(strip=True)}"}
    return caps


def infer_type(consts, companion_path):
    """POST_TYPE const wins; else infer from the folder the companion lives in."""
    ptype = consts.get("POST_TYPE", "")
    if ptype:
        return ptype
    parts = os.path.abspath(companion_path).split(os.sep)
    for seg in reversed(parts):
        if seg in FOLDER_TYPE_MAP:
            return FOLDER_TYPE_MAP[seg]
    return ""


def collect_assets(soup, companion_path, project_root, extra_dirs=None,
                    scan_parent_folder=True, slug=""):
    """Real asset paths: <img>/<video>/<source> src in the companion, resolved
    relative to the companion's folder, plus any deliverable-looking sibling
    files in that folder (and any extra_dirs). Returns project-root-relative
    paths where possible.

    scan_parent_folder=False skips the blind directory scan of the companion's
    own folder — used when that folder is shared with unrelated sibling posts
    (e.g. outputs/tips/) and a dedicated extra_dirs asset folder was found
    instead. When True but a slug is given, the scan is filtered to files
    whose name contains the slug, so a shared folder doesn't leak siblings."""
    folder = os.path.dirname(os.path.abspath(companion_path))
    found = {}

    def add(rel_or_abs):
        if not rel_or_abs:
            return
        if any(s in rel_or_abs for s in ASSET_SKIP_SUBSTR):
            return
        if rel_or_abs.startswith(("http://", "https://")):
            return
        abspath = rel_or_abs
        if not os.path.isabs(abspath):
            abspath = os.path.normpath(os.path.join(folder, rel_or_abs))
        if not os.path.exists(abspath):
            return
        if os.path.splitext(abspath)[1].lower() not in ASSET_EXTS:
            return
        rel = os.path.relpath(abspath, project_root) if project_root else abspath
        found[abspath] = rel

    for tag in soup.find_all(["img", "video", "source"]):
        add(tag.get("src"))
        add(tag.get("poster"))
    # sibling deliverables in the companion's own folder, plus any extra dirs
    # (covers files rendered client-side into a folder, not referenced by <img>).
    scan_dirs = ([folder] if scan_parent_folder else []) + [d for d in (extra_dirs or []) if os.path.isdir(d)]
    for d in scan_dirs:
        require_slug = scan_parent_folder and d == folder and slug
        for name in sorted(os.listdir(d)):
            if require_slug and slug not in name:
                continue
            p = os.path.join(d, name)
            if os.path.isfile(p) and os.path.splitext(name)[1].lower() in ASSET_EXTS:
                add(p)

    imgs, vids = [], []
    for abspath, rel in found.items():
        ext = os.path.splitext(abspath)[1].lower()
        (vids if ext in (".mp4", ".webm", ".mov") else imgs).append(rel)
    return sorted(imgs), sorted(vids)


def to_pipeline_captions(caps, ptype):
    """Reduce the full harvest to the compact captions field the JSON Standard
    defines: {linkedin: str, x: [str]}. Falls back through every X-flavoured
    tab (x, x_singles, x_angles, x_thread) so tab-based skills (CRO Fix,
    Tips) populate this optional cache too, not just block-based skills."""
    out = {}
    if "linkedin" in caps:
        out["linkedin"] = caps["linkedin"]["text"]
    x_val = None
    for key in ("x", "x_singles", "x_angles", "x_thread"):
        v = caps.get(key, {}).get("text")
        if v:
            x_val = v
            break
    if isinstance(x_val, str):
        x_val = [x_val]
    if x_val:
        out["x"] = x_val
    return out


def harvest(companion_path, project_root):
    html = read_html(companion_path)
    soup = BeautifulSoup(html, "lxml")
    consts = extract_post_consts(html)
    ptype = infer_type(consts, companion_path)

    # Select parser by DOM structure, not by skill type — some files carry no
    # POST_TYPE const and the two families are unambiguous by their markup.
    if soup.select("div.tab-panel[id^='tab-'], div.tpanel[id^='tab-']"):
        caps = parse_tab_captions(soup)
    elif soup.select("div.copy-block"):
        caps = parse_block_captions(soup)
    else:
        caps = {}

    # CRO Fix graphics land in a brand subfolder (outputs/cro-fixes/{brand}/),
    # not the companion's own folder — search it too.
    extra_dirs = []
    if ptype == "CRO Fix" and consts.get("POST_BRAND"):
        brand_slug = consts["POST_BRAND"].lower().replace(" ", "-")
        base = os.path.dirname(os.path.abspath(companion_path))
        for cand in (brand_slug, consts.get("POST_SLUG", "").split("_")[0]):
            if cand:
                extra_dirs.append(os.path.join(base, cand))
    # Tips (and any generator sharing a flat folder with sibling posts, e.g.
    # outputs/tips/) render slide PNGs into a dedicated "{slug}-assets" or
    # "{slug}" subfolder rather than the companion's own folder — search it
    # too, and DON'T fall back to a blind scan of the shared parent folder
    # (that grabs unrelated sibling posts' assets, e.g. another tip's PDF).
    slug = consts.get("POST_SLUG", "")
    base = os.path.dirname(os.path.abspath(companion_path))
    scan_parent_folder = True
    if slug:
        # Try the full slug first, then progressively shorter word-prefixes
        # of it (asset folders are sometimes named from a shortened slug,
        # e.g. slug "animation-budget-motion-conversion" -> folder
        # "animation-budget-assets"). Longest match wins; stop at 2 words
        # to avoid over-matching an unrelated sibling folder.
        words = slug.split("-")
        prefixes = ["-".join(words[:n]) for n in range(len(words), 1, -1)]
        candidates = [slug] + [p + "-assets" for p in prefixes] + prefixes
        for cand_name in candidates:
            cand = os.path.join(base, cand_name)
            if os.path.isdir(cand):
                extra_dirs.append(cand)
                scan_parent_folder = False
                break
    imgs, vids = collect_assets(
        soup, companion_path, project_root, extra_dirs=extra_dirs,
        scan_parent_folder=scan_parent_folder, slug=slug,
    )

    folder_rel = consts.get("POST_FOLDER") or (
        os.path.relpath(os.path.abspath(companion_path), project_root)
        if project_root else companion_path
    )

    record = {
        "pipeline_item_id": build_item_id(consts),
        "brand": consts.get("POST_BRAND", ""),
        "slug": consts.get("POST_SLUG", ""),
        "type": ptype,
        "content_system_folder": folder_rel,
        "companion_html": os.path.relpath(os.path.abspath(companion_path), project_root)
        if project_root else companion_path,
        "harvested_at": datetime.now(timezone.utc).isoformat(),
        "captions": to_pipeline_captions(caps, ptype),
        "captions_full": caps,
        "assets": {"images": imgs, "video": vids[0] if len(vids) == 1 else vids},
        "warnings": [],
    }
    if not caps:
        record["warnings"].append("no captions parsed — DOM may have changed for this skill")
    if not imgs and not vids:
        record["warnings"].append("no assets found on disk — client-side exports may not have been run yet")
    if not ptype:
        record["warnings"].append("POST_TYPE constant not found — skill flavour could not be determined")
    return record


def merge_into_pipeline(record, project_root):
    """Populate the optional captions/assets fields on the matching
    pipeline_data.json item (idempotent — matches by id)."""
    path = os.path.join(project_root, "pipeline_data.json")
    if not os.path.exists(path):
        return "pipeline_data.json not found — skipped merge"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get("items", []):
        if item.get("id") == record["pipeline_item_id"]:
            item["captions"] = record["captions"]
            item["assets"] = record["assets"]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return f"merged captions/assets into pipeline item {record['pipeline_item_id']}"
    return f"no pipeline item with id {record['pipeline_item_id']} — merge skipped (harvest still emitted)"


def main():
    ap = argparse.ArgumentParser(description="Harvest captions + assets from a generator companion HTML.")
    ap.add_argument("companion_html")
    ap.add_argument("--out", default=None)
    ap.add_argument("--project-root", default=None,
                    help="project root for computing relative paths (default: auto-detect by walking up for CLAUDE.md)")
    ap.add_argument("--merge-pipeline", action="store_true",
                    help="also write captions/assets onto the matching pipeline_data.json item")
    args = ap.parse_args()

    companion = os.path.abspath(args.companion_html)
    if not os.path.exists(companion):
        sys.exit(f"companion HTML not found: {companion}")

    root = args.project_root
    if not root:
        d = os.path.dirname(companion)
        while d != "/" and not os.path.exists(os.path.join(d, "CLAUDE.md")):
            d = os.path.dirname(d)
        root = d if os.path.exists(os.path.join(d, "CLAUDE.md")) else os.path.dirname(companion)
    root = os.path.abspath(root)

    record = harvest(companion, root)

    out = args.out or os.path.join(os.path.dirname(companion), f"{record['slug'] or 'content'}_harvest.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    if args.merge_pipeline:
        record["_merge_result"] = merge_into_pipeline(record, root)

    print(json.dumps(record, indent=2, ensure_ascii=False))
    print(f"\n[harvest] record written to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
