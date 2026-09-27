#!/usr/bin/env python3
"""Finalize the 2026-09-27 weekly CRO Fix (Minimalist Niacinamide 10% PDP):
captions (humanizer-passed, X counted), social-content pair, review pack HTML,
manifest + captions.txt, SYNC_DATA merge, targets_pool usedFor, weekly tracker row."""
import json, re, shutil, pathlib, html as H
from datetime import datetime, timezone
ROOT = pathlib.Path(__file__).resolve().parent.parent
SLUG = "minimalist_niacinamide-10-serum-pdp"; BR = "minimalist"; BRAND = "Minimalist"
DATE = "2026-09-27"; NOW = datetime.now(timezone.utc).isoformat(timespec="seconds")
ITEM_ID = f"cro-fix-{SLUG}-20260927"
OUTD = f"outputs/cro-fixes/{BR}"
IMG = {k: f"{OUTD}/koolestpro_{SLUG}_{v}.png" for k, v in
       {"COVER": "carousel_slide1", "BA": "carousel_slide2", "ANNO": "carousel_slide3", "ANNO-GRAPHIC": "annotated"}.items()}
CAROUSEL = f"outputs/cro-fixes/{SLUG}_carousel.html"
CONTENT = f"outputs/cro-fixes/{SLUG}_content.html"
REBUILD = f"outputs/cro-fixes/{SLUG}_rebuild.html"
TITLE = "The price sat two scrolls down."

LINKEDIN = """PRODUCT PAGE (PDP): Minimalist's Niacinamide 10% serum page opens on a really good studio photo. On a phone, that photo is the entire first screen.

The product name starts right at the bottom edge. The price (₹539) is about 1,576px down. Add to Cart is at 1,870px. So a shopper scrolls twice before they find out what it costs.

There's also a chat bubble that pops up asking "Is this safe to use while pregnant?" The page does answer that. Inside a closed accordion, near the bottom.

I rebuilt the first screen using only what was already on the page and in Minimalist's own policies:

1. A headline that says what it does: control oil, refine pores, even out tone. The product name sits under it.
2. The 3.9 rating from 1,480 reviews, ₹539 with the MRP, the sizes and one Add to Cart, all on screen one.
3. Pregnancy-safe and dermatologist patch-tested as chips next to the price.
4. Ships in 48 hours, Cash on Delivery and 7-day replacement, right under the button.

I kept the photo. It just shouldn't have to sell the serum on its own.

This is unofficial concept work. Minimalist isn't a client."""

# One caption per X post (2026-09-27 rule): the 3-image carousel + each of the 4 graphics.
XC = {
 "x_carousel": """PDP teardown: Minimalist's Niacinamide 10% serum.

1 The price sat two scrolls down
2 Same serum, new first screen
3 The questions it now answers up front

Swipe through. Every fact came from their own page.""",
 "x_cover": """Minimalist's serum PDP, measured on a phone:

Screen 1 ends at 844px. Only the photo.
Price: 1,576px down.
Add to Cart: 1,870px down.

Great photo.
It shouldn't have to sell the serum alone.""",
 "x_ba": """Minimalist's serum PDP: great photo, then nothing.

Before:
X Screen one is only the photo
X Price 1,576px down
X Add to Cart at 1,870px

After:
OK Headline, rating, price and button on screen one

Same serum.
Nothing invented. Just moved up.""",
 "x_anno": """PDP fix: Minimalist's serum page already answered "safe in pregnancy?"

The answer sat in a closed accordion. Meanwhile a chat bubble asked the same question on screen one.

Moved it next to the price.

Same serum.
Better answers = better conversion.""",
 "x_anno_graphic": """Redesigned this PDP (Minimalist Niacinamide 10%) around one thing:

What a buyer asks before scrolling.

1 What will it do for my skin?
2 Is it safe while I'm pregnant?
3 What does it cost?

All 3 answers were already on the page.
Now they're on screen one.""",
}
X = list(XC.values())
XKEY = {"x_carousel": ("X-CAROUSEL", "CAROUSEL3"), "x_cover": ("X-COVER", "COVER"), "x_ba": ("X-BA", "BA"),
        "x_anno": ("X-ANNO", "ANNO"), "x_anno_graphic": ("X-ANNO-GRAPHIC", "ANNO-GRAPHIC")}

def check(t, name, limit=None):
    assert "—" not in t and "&mdash;" not in t, f"em dash in {name}"
    assert "\\n" not in t
    if limit: assert len(t) < limit, f"{name} is {len(t)} chars"
check(LINKEDIN, "linkedin")
for k, t in XC.items(): check(t, k, 280); print(f"{k}: {len(t)} chars")
for p in list(IMG.values()) + [CAROUSEL, REBUILD]:
    assert (ROOT / p).exists(), f"missing {p}"

# ---- social content pair
K = "CRO-MINIMALIST"
items = {
 f"{K}-COVER": {"assetPath": IMG["COVER"], "usedIn": "carousel slide 1 (cover: live-page scroll-depth ruler + AFTER phone, real logo)"},
 f"{K}-BA": {"assetPath": IMG["BA"], "usedIn": "carousel slide 2, standalone before/after post", "caption": LINKEDIN},
 f"{K}-ANNO": {"assetPath": IMG["ANNO"], "usedIn": "carousel slide 3, standalone annotation post"},
 f"{K}-ANNO-GRAPHIC": {"assetPath": IMG["ANNO-GRAPHIC"], "usedIn": "standalone clear-background annotation graphic (1080x1080)"},
 f"{K}-CAROUSEL": {"assetPath": CAROUSEL, "usedIn": "the review/export HTML (all 3 slides + download panel)",
                   "captionOptions": [{"id": "linkedin", "caption": LINKEDIN, "hashtags": ["#CRO", "#Shopify", "#EcommerceUX", "#ProductPage"]}]},
 **{f"{K}-{XKEY[k][0]}": {"assetPath": ([IMG["COVER"], IMG["BA"], IMG["ANNO"]] if k == "x_carousel" else IMG[XKEY[k][1]]),
                              "caption": t, "platform": "X", "captionKey": k, "chars": len(t)} for k, t in XC.items()},
}
lib = {"brand": BRAND, "brandSlug": BR, "isConceptBrand": False,
       "note": "Real brand, unofficial portfolio/concept CRO work. Not a Minimalist client engagement.",
       "pipelineItemId": ITEM_ID, "items": items, "knownGaps": []}
(ROOT / f"{BR}-social-content.json").write_text(json.dumps(lib, indent=2, ensure_ascii=False), encoding="utf-8")
md = [f"# {BRAND} - Social Content Library", "", "Real brand. Unofficial portfolio/concept CRO work, not a Minimalist client engagement.", "",
      f"Pipeline item: `{ITEM_ID}`", "", "| Key | Asset | Use |", "|---|---|---|"]
for k, v in items.items(): md.append(f"| `{k}` | `{v['assetPath']}` | {v.get('usedIn', 'X caption, ' + str(v.get('chars')) + ' chars')} |")
md += ["", "Posting plan (2026-09-27 rule): the 3-slide carousel goes to LinkedIn, Instagram AND X; each of the 4 graphics also posts alone on X.", "",
       f"## LinkedIn / Instagram caption ({K}-BA, {K}-CAROUSEL)", "", "```", LINKEDIN, "```", "", "## X captions (no hashtags, each under 280)", ""]
for k, t in XC.items():
    key = f"{K}-{XKEY[k][0]}"; md += [f"### {key} ({len(t)} chars) -> `{items[key]['assetPath']}`", "", "```", t, "```", ""]
(ROOT / f"{BR}-social-content.md").write_text("\n".join(md), encoding="utf-8")

# ---- captions.txt + manifest
(ROOT / OUTD / "captions.txt").write_text("LINKEDIN / INSTAGRAM\n\n" + LINKEDIN + "\n\n" + "\n\n".join(f"{XKEY[k][0]} ({len(t)} chars)\n\n{t}" for k, t in XC.items()) + "\n", encoding="utf-8")
(ROOT / OUTD / "manifest.json").write_text(json.dumps({
  "brand": BRAND, "slug": SLUG, "date": DATE, "pipelineItemId": ITEM_ID, "pageType": "Product Page (PDP)",
  "url": "https://beminimalist.co/products/niacinamide-10-with-matmarine",
  "images": IMG, "carouselHtml": CAROUSEL, "annotationHtml": f"outputs/cro-fixes/{SLUG}_annotation.html",
  "rebuildHtml": REBUILD, "reviewPack": CONTENT, "audit": f"outputs/audits/{SLUG}_audit.md",
  "facts": f"outputs/cro-fixes/{SLUG}_facts.json", "brief": f"outputs/cro-fixes/{SLUG}_build-brief.md",
  "captions": f"{OUTD}/captions.txt", "builders": [".ai-workflow/build_minimalist_rebuild.py", ".ai-workflow/build_minimalist_carousel.py", ".ai-workflow/build_minimalist_annotation.py"],
  "exportedVia": "each page's own captureSlide()/captureSheet() (html2canvas, scale 2) driven by headless Playwright"}, indent=2, ensure_ascii=False), encoding="utf-8")

# ---- review pack HTML (tab ids are what harvest_content.py reads)
TABS = [("tab-linkedin", "LinkedIn", LINKEDIN), ("tab-ig", "Instagram", LINKEDIN)] + \
       [(f"tab-{k.replace('_', '-')}", f"{XKEY[k][0]} ({len(t)})", t) for k, t in XC.items()]
def pre(t): return "<pre>" + H.escape(t) + "</pre>"
rel = lambda p: p.replace("outputs/cro-fixes/", "")
content = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CRO Fix review pack - Minimalist Niacinamide 10% PDP - @koolestpro</title>
<style>body{{background:#0e0e0e;color:#e8e8e8;font-family:ui-monospace,Menlo,monospace;margin:0;padding:32px 20px 80px;}}
.w{{max-width:1180px;margin:0 auto;}}h1{{font:800 26px system-ui;margin:0 0 6px}}h2{{font:700 16px system-ui;color:#FA9C0F;margin:34px 0 12px;letter-spacing:.5px}}
.m{{color:#999;font-size:12px}}.g{{display:flex;gap:14px;flex-wrap:wrap}}.g img{{width:360px;border-radius:8px;border:1px solid #222}}
pre{{white-space:pre-wrap;background:#171717;border:1px solid #262626;border-radius:10px;padding:14px;font-size:13px;line-height:1.55;max-width:760px}}
iframe{{width:390px;height:844px;border:1px solid #333;border-radius:18px;background:#fff}}.tabs button{{background:#1b1b1b;color:#ccc;border:1px solid #333;border-radius:6px;padding:7px 12px;margin-right:6px;cursor:pointer;font:inherit}}
.dl-pipe{{background:rgba(123,47,190,.14)!important;border-color:rgba(123,47,190,.4)!important;color:#c79bff!important}}</style></head><body><div class="w">
<h1>Minimalist Niacinamide 10% Face Serum: {H.escape(TITLE)}</h1>
<div class="m">PRODUCT PAGE (PDP) · Weekly CRO Fix · {DATE} · status Created · unofficial concept work, Minimalist is not a client</div>
<h2>#1 FINDING</h2><pre>On a 390x844 phone the first screen is only the product photo. Name at y=813, price (₹539) at y=1576, Add to Cart at y=1870. The page's own chat bubble asks "Is this safe to use while pregnant?" while the answer ("Pregnancy/Lactation: Safe") sits in a closed accordion.</pre>
<h2>CAROUSEL (EXPORTED PNGs)</h2><div class="g">{''.join(f'<img src="{rel(IMG[k])}">' for k in ("COVER","BA","ANNO"))}</div>
<h2>STANDALONE ANNOTATED GRAPHIC</h2><div class="g"><img src="{rel(IMG['ANNO-GRAPHIC'])}" style="width:540px"></div>
<h2>THE REBUILD (LIVE HTML, 390x844)</h2><iframe src="{rel(REBUILD)}"></iframe>
<h2>CAPTIONS</h2><div class="m">Carousel -> LinkedIn, Instagram and X. Each graphic -> its own X single.</div><br>
<div class="tabs">{''.join(f'<button onclick="sh({i})">{H.escape(lab)}</button>' for i,(tid,lab,_) in enumerate(TABS))}</div>
<div id="caps">{''.join(f'<div class="tab-panel" id="{tid}">{pre(t)}</div>' for tid,lab,t in TABS)}</div>
<h2>PIPELINE</h2><div class="tabs"><button class="dl-pipe" onclick="sendToPipeline()">Send to Content Pipeline</button></div><div id="pipeline-status" class="m"></div>
<p class="m">Files: {H.escape(CAROUSEL)} · outputs/audits/{SLUG}_audit.md · {OUTD}/manifest.json</p></div>
<script>
function sh(n){{document.querySelectorAll('#caps .tab-panel').forEach((p,i)=>p.style.display=i===n?'':'none')}}sh(0);
const POST_BRAND='Minimalist',POST_SLUG='{SLUG}',POST_TYPE='CRO Fix',POST_FOLDER='{CAROUSEL}';
function sendToPipeline(){{const now=new Date();const data={{id:'{ITEM_ID}',type:POST_TYPE,title:{json.dumps(TITLE)},slug:POST_SLUG,status:'Created',day:'',created:now.toISOString(),folder:POST_FOLDER,week:'Week of September 27',month:'September 2026',monthSlug:'2026-09',assets:{{images:{json.dumps(list(IMG.values()))}}}}};
console.log('EXPORT_POST_JSON',JSON.stringify(data));const b=new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=POST_SLUG+'_pipeline.json';document.body.appendChild(a);a.click();a.remove();document.getElementById('pipeline-status').textContent='Exported. Open ridwan_content_system_updated.html and sync.';}}
</script></body></html>"""
(ROOT / CONTENT).write_text(content, encoding="utf-8")

# ---- SYNC_DATA merge
cs = ROOT / "ridwan_content_system_updated.html"; src = cs.read_text(encoding="utf-8")
rx = re.compile(r'(<script id="cowork-sync-data" type="application/json">)(.*?)(</script>)', re.S)
m = rx.search(src); data = json.loads(m.group(2))
item = {"id": ITEM_ID, "type": "CRO Fix", "title": TITLE, "slug": SLUG, "status": "Created", "day": "",
        "created": NOW, "folder": CAROUSEL, "week": "Week of September 27", "month": "September 2026", "monthSlug": "2026-09",
        "captions": {"linkedin": LINKEDIN, "x": X}, "assets": {"images": list(IMG.values())}}
ex = next((i for i in data["items"] if i.get("id") == ITEM_ID), None)
if ex is not None:
    ex["captions"] = item["captions"]; ex["assets"] = item["assets"]; data["meta"]["updatedAt"] = NOW
    shutil.copy(cs, str(cs) + ".bak")
    cs.write_text(src[:m.start(2)] + json.dumps(data, ensure_ascii=False, indent=2) + src[m.end(2):], encoding="utf-8")
    print("SYNC: existing item captions refreshed (no duplicate added)")
else:
    shutil.copy(cs, str(cs) + ".bak")
    data["items"].append(item)
    data["months"].setdefault("2026-09", {"label": "September 2026", "htmlPath": "outputs/ideas/ideas_2026-09.html", "jsonPath": "outputs/ideas/ideas_2026-09.json", "totalIdeas": 0})
    data["meta"]["updatedAt"] = NOW
    new = json.dumps(data, ensure_ascii=False, indent=2)
    cs.write_text(src[:m.start(2)] + new + src[m.end(2):], encoding="utf-8")
    print("SYNC: added", ITEM_ID, "items now", len(data["items"]))

# ---- targets pool
tp = ROOT / "targets_pool.json"; T = json.loads(tp.read_text(encoding="utf-8"))
t = next(x for x in T["targets"] if x["brand"] == "Minimalist")
if not any(u.get("pipelineItemId") == ITEM_ID for u in t["usedFor"]):
    t["usedFor"].append({"stream": "cro-fix", "date": DATE, "pipelineItemId": ITEM_ID,
      "note": "Zero prior cro-fix entries. Niacinamide 10% Face Serum PDP. Beauty/skincare chosen to rotate away from baby (Kyte Baby, 09-20) and home-kitchen (Caraway, 09-07/09). #1 finding: photo-only first screen, price at 1,576px, Add to Cart at 1,870px. Concept work only, Minimalist is not a client."})
    t["lastUsedAt"] = NOW; T["meta"]["updatedAt"] = NOW
    tp.write_text(json.dumps(T, indent=2, ensure_ascii=False), encoding="utf-8"); print("targets_pool updated, status left", t["status"])

# ---- tracker
import openpyxl
wb = openpyxl.load_workbook(ROOT / "outputs/weekly-tracker.xlsx"); ws = wb["Weekly Posts"]
if not any(r[2] == SLUG for r in ws.iter_rows(min_row=2, values_only=True)):
    ws.append([DATE, BRAND, SLUG, "CRO Fix", "Created", None, CAROUSEL, LINKEDIN[:200].rsplit(" ", 1)[0] + "...", "Yes"])
    wb.save(ROOT / "outputs/weekly-tracker.xlsx"); print("tracker row added")
