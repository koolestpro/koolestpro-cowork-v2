#!/usr/bin/env python3
"""Finalize the 2026-10-25 weekly CRO Fix (Fishwife shop-all collection page):
captions (humanizer-passed, X counted, caption_fit checked), social-content pair, review
pack HTML, manifest + captions.txt, SYNC_DATA merge, targets_pool usedFor, tracker row.
Pattern: finalize_topicals_cro.py (2026-10-18)."""
import json, re, shutil, sys, pathlib, html as H
from datetime import datetime, timezone
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".ai-workflow" / "tools"))
from caption_fit import check as fit_check
SLUG = "fishwife_shop-all-collection"; BR = "fishwife"; BRAND = "Fishwife"
DATE = "2026-10-25"; NOW = datetime.now(timezone.utc).isoformat(timespec="seconds")
ITEM_ID = f"cro-fix-{SLUG}-20261025"
OUTD = f"outputs/cro-fixes/{BR}"
IMG = {k: f"{OUTD}/koolestpro_{SLUG}_{v}.png" for k, v in
       {"VARIANTS": "variants-board", "COVER": "carousel_slide1", "BA": "carousel_slide2", "ANNO": "carousel_slide3", "ANNO-GRAPHIC": "annotated"}.items()}
CAROUSEL = f"outputs/cro-fixes/{SLUG}_carousel.html"
CONTENT = f"outputs/cro-fixes/{SLUG}_content.html"
REBUILD = f"outputs/cro-fixes/{SLUG}_rebuild.html"
TITLE = "400px of banner. No product names."
URL = "https://eatfishwife.com/collections/all"

LINKEDIN = """COLLECTION PAGE: Fishwife's shop-all page has one job on a phone. Help someone pick a tin.

On a 390px screen, the first 400px under the header is a banner that says "Shop Tinned Fish & More!" The first product name shows up at 863px. The screen ends at 844.

Two product photos do peek in at the bottom. Both are new drops: Tuna Belly (21 reviews) and the Advent Calendar (2 reviews). The Fly By Jing smoked salmon, with 641 reviews, sits in row two. Gold Label, with 520, is in row three.

The cards also show a star average with no count. So 5.0 from 2 reviews looks exactly as safe as 4.9 from 641.

So I rebuilt screen one with what's already on their site:

1. The banner shrinks from 400px to 118px. Same photo, same "Everything Fishwife" heading.
2. Four tins fit above the fold, sorted by most reviewed. All four are in their own Best Sellers collection.
3. Every rating shows its count: 4.9 (641), 4.9 (520), 4.9 (343), 4.9 (223).
4. Pack size under each name, and an Add button on the card where it used to say Shop Now.
5. The new drops still get a spot, right after the tins people already trust.

The packaging is half the reason people buy Fishwife, so I kept it big. I just wanted it sitting next to a name and a number.

This is unofficial concept work. Fishwife isn't a client."""

XC = {
 "x_variants": """Fishwife's shop-all page, 4 ways. Same tins, same photos.

A: grid first
B: slim photo band
C: shop by fish
D: starter pack first

Hot take: a collection page should show products before it shows a banner.

Which would you ship? My pick goes up next.""",
 "x_carousel": """Collection page teardown: Fishwife.

1 Screen one is a 400px banner and no product names
2 Same tins, four of them now above the fold
3 The three questions a shopper asks before scrolling

Review counts and prices came from their own site.""",
 "x_ba": """Fishwife shop-all page, before and after.

Before:
❌ 400px banner on screen one
❌ First product name at 863px
❌ Stars with no review count

After:
✅ 4 tins above the fold
✅ 4.9 (641), not just 4.9
✅ An Add button on every card""",
 "x_anno": """Collection page fix: Fishwife.

What a shopper wonders on screen one:
1 Where are the tins?
2 Is this one any good?
3 Can I just add it?

The old page answered with a banner. Now four tins, counted ratings and an Add button answer them.""",
 "x_anno_graphic": """On Fishwife's shop-all page, the Advent Calendar shows 5.0 stars. That's from 2 reviews.

The Fly By Jing smoked salmon shows 4.9, from 641.

Without the count they look the same. So every rating in the rebuild shows it, and the most reviewed tins go first.""",
}
X = list(XC.values())
XKEY = {"x_variants": ("X-VARIANTS", "VARIANTS"), "x_carousel": ("X-CAROUSEL", "CAROUSEL3"), "x_cover": ("X-COVER", "COVER"), "x_ba": ("X-BA", "BA"),
        "x_anno": ("X-ANNO", "ANNO"), "x_anno_graphic": ("X-ANNO-GRAPHIC", "ANNO-GRAPHIC")}

def check(t, name, limit=None):
    assert "—" not in t and "&mdash;" not in t and "–" not in t, f"dash in {name}"
    assert "\\n" not in t
    for w in ["unlock", "digital journey", "holistic", "synergize", "valuable insights", "it's important to note", "delve", "seamless", "leverage"]:
        assert w not in t.lower(), f"blocked word '{w}' in {name}"
    if limit: assert len(t) < limit, f"{name} is {len(t)} chars"
check(LINKEDIN, "linkedin")
for k, t in XC.items():
    check(t, k, 280); print(f"{k}: {len(t)} chars")
    if k != "x_carousel":
        r = fit_check(t, IMG[XKEY[k][1]], "Twitter"); assert not r, (k, r)
for p in list(IMG.values()) + [CAROUSEL, REBUILD]:
    assert (ROOT / p).exists(), f"missing {p}"
if "--captions-only" in sys.argv: sys.exit(0)

# ---- social content pair
K = "CRO-FISHWIFE"
items = {
 f"{K}-COVER": {"assetPath": IMG["COVER"], "usedIn": "carousel slide 1 (cover: BEFORE phone with the 400px banner and 863px marks + AFTER phone, real logo)"},
 f"{K}-BA": {"assetPath": IMG["BA"], "usedIn": "carousel slide 2, standalone before/after post", "caption": LINKEDIN},
 f"{K}-ANNO": {"assetPath": IMG["ANNO"], "usedIn": "carousel slide 3, standalone annotation post"},
 f"{K}-VARIANTS": {"assetPath": IMG["VARIANTS"], "usedIn": "variants board (4 hero directions A-D, neutral, no pick shown); X debate post that goes out BEFORE the carousel"},
 f"{K}-ANNO-GRAPHIC": {"assetPath": IMG["ANNO-GRAPHIC"], "usedIn": "standalone clear-background annotation graphic (1080x1080)"},
 f"{K}-CAROUSEL": {"assetPath": CAROUSEL, "usedIn": "the review/export HTML (all 3 slides + download panel)",
                   "captionOptions": [{"id": "linkedin", "caption": LINKEDIN, "hashtags": ["#CRO", "#Shopify", "#EcommerceUX", "#CollectionPage"]}]},
 **{f"{K}-{XKEY[k][0]}": {"assetPath": ([IMG["COVER"], IMG["BA"], IMG["ANNO"]] if k == "x_carousel" else IMG[XKEY[k][1]]),
                              "caption": t, "platform": "X", "captionKey": k, "chars": len(t)} for k, t in XC.items()},
}
lib = {"brand": BRAND, "brandSlug": BR, "isConceptBrand": False,
       "note": "Real brand, unofficial portfolio/concept CRO work. Not a Fishwife client engagement.",
       "pipelineItemId": ITEM_ID, "items": items, "knownGaps": []}
(ROOT / f"{BR}-social-content.json").write_text(json.dumps(lib, indent=2, ensure_ascii=False), encoding="utf-8")
md = [f"# {BRAND} - Social Content Library", "", "Real brand. Unofficial portfolio/concept CRO work, not a Fishwife client engagement.", "",
      f"Pipeline item: `{ITEM_ID}`", "", "| Key | Asset | Use |", "|---|---|---|"]
for k, v in items.items():
    ap = v['assetPath'] if isinstance(v['assetPath'], str) else ", ".join(v['assetPath'])
    md.append(f"| `{k}` | `{ap}` | {v.get('usedIn', 'X caption, ' + str(v.get('chars')) + ' chars')} |")
md += ["", "Posting plan: the variants board posts first on X (debate, day before the carousel; rule 2026-10-11). Then the 3-slide carousel goes to LinkedIn, Instagram AND X, and slide 2, slide 3 and the clear-bg annotated graphic each also post alone on X. The cover never posts alone (2026-10-15 rule).", "",
       f"## LinkedIn / Instagram caption ({K}-BA, {K}-CAROUSEL)", "", "```", LINKEDIN, "```", "", "## X captions (no hashtags, each under 280)", ""]
for k, t in XC.items():
    key = f"{K}-{XKEY[k][0]}"; md += [f"### {key} ({len(t)} chars)", "", "```", t, "```", ""]
(ROOT / f"{BR}-social-content.md").write_text("\n".join(md), encoding="utf-8")

# ---- captions.txt + manifest
(ROOT / OUTD / "captions.txt").write_text("LINKEDIN / INSTAGRAM\n\n" + LINKEDIN + "\n\n" + "\n\n".join(f"{XKEY[k][0]} ({len(t)} chars)\n\n{t}" for k, t in XC.items()) + "\n", encoding="utf-8")
(ROOT / OUTD / "manifest.json").write_text(json.dumps({
  "brand": BRAND, "slug": SLUG, "date": DATE, "pipelineItemId": ITEM_ID, "pageType": "Collection Page", "url": URL,
  "images": IMG, "carouselHtml": CAROUSEL, "annotationHtml": f"outputs/cro-fixes/{SLUG}_annotation.html", "variantsBoardHtml": f"outputs/cro-fixes/{SLUG}_variants-board.html", "heroVariants": "outputs/cro-fixes/fishwife/_variants/ (CHOICE.md)",
  "rebuildHtml": REBUILD, "reviewPack": CONTENT, "audit": f"outputs/audits/{SLUG}_audit.md",
  "facts": f"outputs/cro-fixes/{SLUG}_facts.json", "brief": f"outputs/cro-fixes/{SLUG}_build-brief.md",
  "captions": f"{OUTD}/captions.txt", "builders": [".ai-workflow/prep_fishwife_assets.py", ".ai-workflow/build_fishwife_rebuild.py", ".ai-workflow/build_fishwife_phones.py", ".ai-workflow/build_fishwife_carousel.py", ".ai-workflow/build_fishwife_annotation.py"],
  "exportedVia": "each page's own captureSlide()/captureSheet() (html2canvas, scale 2) driven by headless Playwright"}, indent=2, ensure_ascii=False), encoding="utf-8")


import base64, io
from PIL import Image
def embed(p, w=1080):
    im = Image.open(ROOT / p).convert("RGB")
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=84, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

# ---- review pack HTML (tab ids are what harvest_content.py reads)
TABS = [("tab-linkedin", "LinkedIn", LINKEDIN), ("tab-ig", "Instagram", LINKEDIN)] + \
       [(f"tab-{k.replace('_', '-')}", f"{XKEY[k][0]} ({len(t)})", t) for k, t in XC.items()]
def pre(t): return "<pre>" + H.escape(t) + "</pre>"
rel = lambda p: p.replace("outputs/cro-fixes/", "")
content = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CRO Fix review pack - Fishwife Shop-All Collection - @koolestpro</title>
<style>body{{background:#0e0e0e;color:#e8e8e8;font-family:ui-monospace,Menlo,monospace;margin:0;padding:32px 20px 80px;}}
.w{{max-width:1180px;margin:0 auto;}}h1{{font:800 26px system-ui;margin:0 0 6px}}h2{{font:700 16px system-ui;color:#FA9C0F;margin:34px 0 12px;letter-spacing:.5px}}
.m{{color:#999;font-size:12px}}.g{{display:flex;gap:14px;flex-wrap:wrap}}.g img{{width:360px;border-radius:8px;border:1px solid #222}}
pre{{white-space:pre-wrap;background:#171717;border:1px solid #262626;border-radius:10px;padding:14px;font-size:13px;line-height:1.55;max-width:760px}}
iframe{{width:390px;height:844px;border:1px solid #333;border-radius:18px;background:#fff}}.tabs button{{background:#1b1b1b;color:#ccc;border:1px solid #333;border-radius:6px;padding:7px 12px;margin:0 6px 6px 0;cursor:pointer;font:inherit}}
.dl-pipe{{background:rgba(123,47,190,.14)!important;border-color:rgba(123,47,190,.4)!important;color:#c79bff!important}}</style></head><body><div class="w">
<h1>Fishwife shop-all collection page: {H.escape(TITLE)}</h1>
<div class="m">COLLECTION PAGE · Weekly CRO Fix · {DATE} · status Created · unofficial concept work, Fishwife is not a client</div>
<h2>#1 FINDING</h2><pre>On a 390x844 phone (popups closed), the shop-all collection page spends y=98 to 498 on a banner whose only message is "Shop Tinned Fish &amp; More!". Filter pills start at y=540, the "Everything Fishwife" heading at 588, and the first product name at y=863, past the 844px screen. The two cards that peek in are new drops (Tuna Belly 4.5 from 21 reviews, Advent Calendar 5.0 from 2) while Fly By Jing smoked salmon (4.9 from 641) and Gold Label (4.9 from 520) sit in rows two and three. Cards show the star average with no review count. Full audit: outputs/audits/{SLUG}_audit.md. Hero variants: outputs/cro-fixes/fishwife/_variants/CHOICE.md (B chosen in this unattended run).</pre>
<h2>CAROUSEL (EXPORTED PNGs)</h2><div class="g">{''.join(f'<img src="{embed(IMG[k], 720)}">' for k in ("COVER","BA","ANNO"))}</div>
<h2>VARIANTS BOARD (X DEBATE POST, GOES OUT FIRST)</h2><div class="g"><img src="{embed(IMG['VARIANTS'], 1600)}" style="width:760px"></div>
<h2>STANDALONE ANNOTATED GRAPHIC</h2><div class="g"><img src="{embed(IMG['ANNO-GRAPHIC'], 1080)}" style="width:540px"></div>
<h2>THE REBUILD (LIVE HTML, 390x844)</h2><div class="g"><img src="{embed(OUTD + '/_assets/after_raw_full.png', 780)}" style="width:390px"></div><p class="m">Live, scrollable version: <a style="color:#FA9C0F" href="{rel(REBUILD)}">{H.escape(REBUILD)}</a> (self-contained, opens on its own)</p>
<h2>CAPTIONS</h2><div class="m">Variants board -> X first (the day before). Then carousel -> LinkedIn, Instagram and X. Each graphic -> its own X single.</div><br>
<div class="tabs">{''.join(f'<button onclick="sh({i})">{H.escape(lab)}</button>' for i,(tid,lab,_) in enumerate(TABS))}</div>
<div id="caps">{''.join(f'<div class="tab-panel" id="{tid}">{pre(t)}</div>' for tid,lab,t in TABS)}</div>
<h2>PIPELINE</h2><div class="tabs"><button class="dl-pipe" onclick="sendToPipeline()">Send to Content Pipeline</button></div><div id="pipeline-status" class="m"></div>
<p class="m">Files: {H.escape(CAROUSEL)} · outputs/audits/{SLUG}_audit.md · {OUTD}/manifest.json</p></div>
<script>
function sh(n){{document.querySelectorAll('#caps .tab-panel').forEach((p,i)=>p.style.display=i===n?'':'none')}}sh(0);
const POST_BRAND='Fishwife',POST_SLUG='{SLUG}',POST_TYPE='CRO Fix',POST_FOLDER='{CAROUSEL}';
function sendToPipeline(){{const now=new Date();const data={{id:'{ITEM_ID}',type:POST_TYPE,title:{json.dumps(TITLE)},slug:POST_SLUG,status:'Created',day:'',created:now.toISOString(),folder:POST_FOLDER,week:'Week of October 25',month:'October 2026',monthSlug:'2026-10',assets:{{images:{json.dumps(list(IMG.values()))}}}}};
console.log('EXPORT_POST_JSON',JSON.stringify(data));const b=new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=POST_SLUG+'_pipeline.json';document.body.appendChild(a);a.click();a.remove();document.getElementById('pipeline-status').textContent='Exported. Open ridwan_content_system_updated.html and sync.';}}
</script></body></html>"""
(ROOT / CONTENT).write_text(content, encoding="utf-8")
print("social pair, captions.txt, manifest, review pack written")
if "--no-state" in sys.argv: sys.exit(0)

# ---- SYNC_DATA merge
cs = ROOT / "ridwan_content_system_updated.html"; src = cs.read_text(encoding="utf-8")
rx = re.compile(r'(<script id="cowork-sync-data" type="application/json">)(.*?)(</script>)', re.S)
m = rx.search(src); data = json.loads(m.group(2))
item = {"id": ITEM_ID, "type": "CRO Fix", "title": TITLE, "slug": SLUG, "status": "Created", "day": "",
        "created": NOW, "folder": CAROUSEL, "week": "Week of October 25", "month": "October 2026", "monthSlug": "2026-10",
        "captions": {"linkedin": LINKEDIN, "x": X}, "assets": {"images": list(IMG.values())}}
shutil.copy(cs, str(cs) + ".bak")
ex = next((i for i in data["items"] if i.get("id") == ITEM_ID), None)
if ex is not None:
    ex["captions"] = item["captions"]; ex["assets"] = item["assets"]; ex["title"] = item["title"]; print("SYNC: existing item refreshed (no duplicate)")
else:
    data["items"].append(item); print("SYNC: added", ITEM_ID, "items now", len(data["items"]))
data["months"].setdefault("2026-10", {"label": "October 2026", "htmlPath": "outputs/ideas/ideas_2026-10.html", "jsonPath": "outputs/ideas/ideas_2026-10.json", "totalIdeas": 0})
data["meta"]["updatedAt"] = NOW
cs.write_text(src[:m.start(2)] + json.dumps(data, ensure_ascii=False, indent=2) + src[m.end(2):], encoding="utf-8")

# ---- targets pool (per-stream usedFor only; status stays Available)
tp = ROOT / "targets_pool.json"; T = json.loads(tp.read_text(encoding="utf-8"))
t = next(x for x in T["targets"] if x["brand"] == BRAND)
if not any(u.get("pipelineItemId") == ITEM_ID for u in t["usedFor"]):
    t["usedFor"].append({"stream": "cro-fix", "date": DATE, "pipelineItemId": ITEM_ID,
      "note": "Zero prior cro-fix entries. Collection page (/collections/all, shop all), first screen. Food/beverage chosen to rotate away from beauty (Topicals 10-18) and fitness (Bala 10-11); last food pick was Fly By Jing 10-04. Fishwife had the highest lead potential among the zero-entry targets (High/Medium vs Brightland Medium/High). #1 finding: 400px banner on screen one, first product name at 863px; ratings show no review counts. A mystery-discount quiz popup also covers screen one on load but was not used as the lead (last week was a popup finding). Concept work only, Fishwife is not a client."})
    t["lastUsedAt"] = NOW; T["meta"]["updatedAt"] = NOW
    tp.write_text(json.dumps(T, indent=2, ensure_ascii=False), encoding="utf-8"); print("targets_pool updated, status left", t["status"])

# ---- tracker
import openpyxl
wb = openpyxl.load_workbook(ROOT / "outputs/weekly-tracker.xlsx"); ws = wb["Weekly Posts"]
if not any(r[2] == SLUG for r in ws.iter_rows(min_row=2, values_only=True)):
    ws.append([DATE, BRAND, SLUG, "CRO Fix", "Created", None, CAROUSEL, LINKEDIN[:200].rsplit(" ", 1)[0] + "...", "Yes"])
    wb.save(ROOT / "outputs/weekly-tracker.xlsx"); print("tracker row added")
