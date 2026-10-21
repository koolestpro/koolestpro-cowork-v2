#!/usr/bin/env python3
"""Finalize the 2026-10-11 weekly CRO Fix (Bala homepage, Bala Bangles):
captions (humanizer-passed, X counted, caption_fit checked), social-content pair, review
pack HTML, manifest + captions.txt, SYNC_DATA merge, targets_pool usedFor, tracker row.
Pattern: finalize_flybyjing_cro.py (2026-10-04)."""
import json, re, shutil, sys, pathlib, html as H
from datetime import datetime, timezone
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".ai-workflow" / "tools"))
from caption_fit import check as fit_check
SLUG = "bala_bangles-homepage"; BR = "bala"; BRAND = "Bala"
DATE = "2026-10-11"; NOW = datetime.now(timezone.utc).isoformat(timespec="seconds")
ITEM_ID = f"cro-fix-{SLUG}-20261011"
OUTD = f"outputs/cro-fixes/{BR}"
IMG = {k: f"{OUTD}/koolestpro_{SLUG}_{v}.png" for k, v in
       {"VARIANTS": "variants-board", "COVER": "carousel_slide1", "BA": "carousel_slide2", "ANNO": "carousel_slide3", "ANNO-GRAPHIC": "annotated"}.items()}
CAROUSEL = f"outputs/cro-fixes/{SLUG}_carousel.html"
CONTENT = f"outputs/cro-fixes/{SLUG}_content.html"
REBUILD = f"outputs/cro-fixes/{SLUG}_rebuild.html"
TITLE = "Cute slogan. No product named."
URL = "https://shopbala.com/"

LINKEDIN = """HOMEPAGE: Bala's homepage, on a phone. Screen one is "Fitness, but make it cute" in a hairline font, a 10% bundle discount and an outline button. It never says what Bala sells.

The blue bands on the model's ankles are Bala Bangles, the product the company is named after. Nothing on screen one says so.

The Bangles first show up 3,431px down. Their rating, 4.9 stars from 1,865 reviews, sits at 3,894px.

I rebuilt the first screen using only what was already on their site:

1. Their own Studio to Street Kit photo up top: Bangles, a bra, leggings and a sweatshirt in one color. Each one is labelled on the image, so you see the range before you read anything.
2. 4.9 stars from 1,865 Bangles reviews, right above the headline.
3. A headline that keeps their voice and says what they sell: weights & activewear, but make it cute.
4. One button, Shop best sellers, then Weights, Pilates props, Activewear and Bundles.
5. Their own press logos under it: The Wall Street Journal, goop, Glamour.

The mood stays. It just shows up with the products now.

This is unofficial concept work. Bala isn't a client."""

XC = {
 "x_variants": """Bala's homepage hero, 4 ways. Same brand, same products.

A: the range, labelled
B: lifestyle photo first
C: full-bleed mood shot
D: headline first

Hot take: the prettiest one isn't the one that sells.

Which would you ship, and why? My pick goes up next.""",
 "x_carousel": """Homepage teardown: Bala.

1 Cute slogan, no product named
2 Same mood, now with products
3 The questions screen one now answers

Every number came from their own site.""",
 "x_cover": """Bala's homepage, on a phone:

Screen one: "Fitness, but make it cute" and a bundle discount.
Bala Bangles: 3,431px down.
4.9 stars from 1,865 reviews: 3,894px down.

The product the company is named after isn't on screen one.""",
 "x_ba": """Bala homepage. Same Bangles, different first screen.

Before:
X A slogan that never names the product
X No price
X Rating 3,894px down

After:
OK The range in one labelled photo
OK 4.9 stars up top
OK One clear button

Nothing invented. Just moved up.""",
 "x_anno": """Homepage fix: Bala.

A first-time visitor asks:
1 What do they actually sell?
2 Are they any good?
3 Where do I start?

The answers were all on the site. The first one was 3,431px down.

Now they're on screen one.""",
 "x_anno_graphic": """Redesigned Bala's homepage around 3 questions:

1 What is this brand?
2 Are they any good?
3 Where do I start?

Their site had the answers: weights and matching sets, 4.9 from 1,865 reviews, WSJ, goop and Glamour.

None of them were on screen one.""",
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
K = "CRO-BALA"
items = {
 f"{K}-COVER": {"assetPath": IMG["COVER"], "usedIn": "carousel slide 1 (cover: real crop of the live hero + AFTER phone, real logo)"},
 f"{K}-BA": {"assetPath": IMG["BA"], "usedIn": "carousel slide 2, standalone before/after post", "caption": LINKEDIN},
 f"{K}-ANNO": {"assetPath": IMG["ANNO"], "usedIn": "carousel slide 3, standalone annotation post"},
 f"{K}-VARIANTS": {"assetPath": IMG["VARIANTS"], "usedIn": "variants board (4 hero directions A-D, neutral, no pick shown); X debate post that goes out BEFORE the carousel"},
 f"{K}-ANNO-GRAPHIC": {"assetPath": IMG["ANNO-GRAPHIC"], "usedIn": "standalone clear-background annotation graphic (1080x1080)"},
 f"{K}-CAROUSEL": {"assetPath": CAROUSEL, "usedIn": "the review/export HTML (all 3 slides + download panel)",
                   "captionOptions": [{"id": "linkedin", "caption": LINKEDIN, "hashtags": ["#CRO", "#Shopify", "#EcommerceUX", "#Homepage"]}]},
 **{f"{K}-{XKEY[k][0]}": {"assetPath": ([IMG["COVER"], IMG["BA"], IMG["ANNO"]] if k == "x_carousel" else IMG[XKEY[k][1]]),
                              "caption": t, "platform": "X", "captionKey": k, "chars": len(t)} for k, t in XC.items()},
}
lib = {"brand": BRAND, "brandSlug": BR, "isConceptBrand": False,
       "note": "Real brand, unofficial portfolio/concept CRO work. Not a Bala client engagement.",
       "pipelineItemId": ITEM_ID, "items": items, "knownGaps": []}
(ROOT / f"{BR}-social-content.json").write_text(json.dumps(lib, indent=2, ensure_ascii=False), encoding="utf-8")
md = [f"# {BRAND} - Social Content Library", "", "Real brand. Unofficial portfolio/concept CRO work, not a Bala client engagement.", "",
      f"Pipeline item: `{ITEM_ID}`", "", "| Key | Asset | Use |", "|---|---|---|"]
for k, v in items.items():
    ap = v['assetPath'] if isinstance(v['assetPath'], str) else ", ".join(v['assetPath'])
    md.append(f"| `{k}` | `{ap}` | {v.get('usedIn', 'X caption, ' + str(v.get('chars')) + ' chars')} |")
md += ["", "Posting plan: the variants board posts first on X (debate, day before the carousel; rule 2026-10-11). Then the 3-slide carousel goes to LinkedIn, Instagram AND X, and each of the 4 graphics also posts alone on X.", "",
       f"## LinkedIn / Instagram caption ({K}-BA, {K}-CAROUSEL)", "", "```", LINKEDIN, "```", "", "## X captions (no hashtags, each under 280)", ""]
for k, t in XC.items():
    key = f"{K}-{XKEY[k][0]}"; md += [f"### {key} ({len(t)} chars)", "", "```", t, "```", ""]
(ROOT / f"{BR}-social-content.md").write_text("\n".join(md), encoding="utf-8")

# ---- captions.txt + manifest
(ROOT / OUTD / "captions.txt").write_text("LINKEDIN / INSTAGRAM\n\n" + LINKEDIN + "\n\n" + "\n\n".join(f"{XKEY[k][0]} ({len(t)} chars)\n\n{t}" for k, t in XC.items()) + "\n", encoding="utf-8")
(ROOT / OUTD / "manifest.json").write_text(json.dumps({
  "brand": BRAND, "slug": SLUG, "date": DATE, "pipelineItemId": ITEM_ID, "pageType": "Homepage", "url": URL,
  "images": IMG, "carouselHtml": CAROUSEL, "annotationHtml": f"outputs/cro-fixes/{SLUG}_annotation.html", "variantsBoardHtml": f"outputs/cro-fixes/{SLUG}_variants-board.html", "heroVariants": "references-for-posts/homepage-hero-research-2026-10-11/bala-variants/",
  "rebuildHtml": REBUILD, "reviewPack": CONTENT, "audit": f"outputs/audits/{SLUG}_audit.md",
  "facts": f"outputs/cro-fixes/{SLUG}_facts.json", "brief": f"outputs/cro-fixes/{SLUG}_build-brief.md",
  "captions": f"{OUTD}/captions.txt", "builders": [".ai-workflow/build_bala_rebuild.py", ".ai-workflow/build_bala_carousel.py", ".ai-workflow/build_bala_annotation.py"],
  "exportedVia": "each page's own captureSlide()/captureSheet() (html2canvas, scale 2) driven by headless Playwright"}, indent=2, ensure_ascii=False), encoding="utf-8")

# ---- review pack HTML (tab ids are what harvest_content.py reads)
TABS = [("tab-linkedin", "LinkedIn", LINKEDIN), ("tab-ig", "Instagram", LINKEDIN)] + \
       [(f"tab-{k.replace('_', '-')}", f"{XKEY[k][0]} ({len(t)})", t) for k, t in XC.items()]
def pre(t): return "<pre>" + H.escape(t) + "</pre>"
rel = lambda p: p.replace("outputs/cro-fixes/", "")
content = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CRO Fix review pack - Bala Homepage - @koolestpro</title>
<style>body{{background:#0e0e0e;color:#e8e8e8;font-family:ui-monospace,Menlo,monospace;margin:0;padding:32px 20px 80px;}}
.w{{max-width:1180px;margin:0 auto;}}h1{{font:800 26px system-ui;margin:0 0 6px}}h2{{font:700 16px system-ui;color:#FA9C0F;margin:34px 0 12px;letter-spacing:.5px}}
.m{{color:#999;font-size:12px}}.g{{display:flex;gap:14px;flex-wrap:wrap}}.g img{{width:360px;border-radius:8px;border:1px solid #222}}
pre{{white-space:pre-wrap;background:#171717;border:1px solid #262626;border-radius:10px;padding:14px;font-size:13px;line-height:1.55;max-width:760px}}
iframe{{width:390px;height:844px;border:1px solid #333;border-radius:18px;background:#fff}}.tabs button{{background:#1b1b1b;color:#ccc;border:1px solid #333;border-radius:6px;padding:7px 12px;margin:0 6px 6px 0;cursor:pointer;font:inherit}}
.dl-pipe{{background:rgba(123,47,190,.14)!important;border-color:rgba(123,47,190,.4)!important;color:#c79bff!important}}</style></head><body><div class="w">
<h1>Bala homepage: {H.escape(TITLE)}</h1>
<div class="m">HOMEPAGE · Weekly CRO Fix · {DATE} · status Created · unofficial concept work, Bala is not a client</div>
<h2>#1 FINDING</h2><pre>On a 390x844 phone, screen one is a hairline slogan ("FITNESS, BUT MAKE IT CUTE", 31px in ITC Avant Garde Extra Light, over video), a 10%-off-bundles line and an outline SHOP BUNDLES button. It never names the product. Bala Bangles (the blue bands on the model\'s ankles) first appears at y=3,431; its 4.9 rating from 1,865 reviews at y=3,894. First price on the page: y=1,173, and it is a new launch, not the Bangles.</pre>
<h2>CAROUSEL (EXPORTED PNGs)</h2><div class="g">{''.join(f'<img src="{rel(IMG[k])}">' for k in ("COVER","BA","ANNO"))}</div>
<h2>VARIANTS BOARD (X DEBATE POST, GOES OUT FIRST)</h2><div class="g"><img src="{rel(IMG['VARIANTS'])}" style="width:760px"></div>
<h2>STANDALONE ANNOTATED GRAPHIC</h2><div class="g"><img src="{rel(IMG['ANNO-GRAPHIC'])}" style="width:540px"></div>
<h2>THE REBUILD (LIVE HTML, 390x844)</h2><iframe src="{rel(REBUILD)}"></iframe>
<h2>CAPTIONS</h2><div class="m">Variants board -> X first (the day before). Then carousel -> LinkedIn, Instagram and X. Each graphic -> its own X single.</div><br>
<div class="tabs">{''.join(f'<button onclick="sh({i})">{H.escape(lab)}</button>' for i,(tid,lab,_) in enumerate(TABS))}</div>
<div id="caps">{''.join(f'<div class="tab-panel" id="{tid}">{pre(t)}</div>' for tid,lab,t in TABS)}</div>
<h2>PIPELINE</h2><div class="tabs"><button class="dl-pipe" onclick="sendToPipeline()">Send to Content Pipeline</button></div><div id="pipeline-status" class="m"></div>
<p class="m">Files: {H.escape(CAROUSEL)} · outputs/audits/{SLUG}_audit.md · {OUTD}/manifest.json</p></div>
<script>
function sh(n){{document.querySelectorAll('#caps .tab-panel').forEach((p,i)=>p.style.display=i===n?'':'none')}}sh(0);
const POST_BRAND='Bala',POST_SLUG='{SLUG}',POST_TYPE='CRO Fix',POST_FOLDER='{CAROUSEL}';
function sendToPipeline(){{const now=new Date();const data={{id:'{ITEM_ID}',type:POST_TYPE,title:{json.dumps(TITLE)},slug:POST_SLUG,status:'Created',day:'',created:now.toISOString(),folder:POST_FOLDER,week:'Week of October 11',month:'October 2026',monthSlug:'2026-10',assets:{{images:{json.dumps(list(IMG.values()))}}}}};
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
        "created": NOW, "folder": CAROUSEL, "week": "Week of October 11", "month": "October 2026", "monthSlug": "2026-10",
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
      "note": "Zero prior cro-fix entries. Homepage (first screen), Bala Bangles. Fitness/wellness chosen to rotate away from food/beverage (Fly By Jing, 10-04), beauty (Minimalist, 09-27) and baby (Kyte Baby, 09-20); also the first homepage after four PDPs. Note: the hero changed since the 09-28 review (now \"Fitness, but make it cute\" + Shop Bundles). #1 finding: screen one never names the product; Bala Bangles at 3,431px, its 4.9/1,865 rating at 3,894px. Concept work only, Bala is not a client."})
    t["lastUsedAt"] = NOW; T["meta"]["updatedAt"] = NOW
    tp.write_text(json.dumps(T, indent=2, ensure_ascii=False), encoding="utf-8"); print("targets_pool updated, status left", t["status"])

# ---- tracker
import openpyxl
wb = openpyxl.load_workbook(ROOT / "outputs/weekly-tracker.xlsx"); ws = wb["Weekly Posts"]
if not any(r[2] == SLUG for r in ws.iter_rows(min_row=2, values_only=True)):
    ws.append([DATE, BRAND, SLUG, "CRO Fix", "Created", None, CAROUSEL, LINKEDIN[:200].rsplit(" ", 1)[0] + "...", "Yes"])
    wb.save(ROOT / "outputs/weekly-tracker.xlsx"); print("tracker row added")
