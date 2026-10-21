#!/usr/bin/env python3
"""Finalize the 2026-10-18 weekly CRO Fix (Topicals homepage):
captions (humanizer-passed, X counted, caption_fit checked), social-content pair, review
pack HTML, manifest + captions.txt, SYNC_DATA merge, targets_pool usedFor, tracker row.
Pattern: the 2026-10-11 finalize script."""
import json, re, shutil, sys, pathlib, html as H
from datetime import datetime, timezone
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".ai-workflow" / "tools"))
from caption_fit import check as fit_check
SLUG = "topicals_homepage-hero"; BR = "topicals"; BRAND = "Topicals"
DATE = "2026-10-18"; NOW = datetime.now(timezone.utc).isoformat(timespec="seconds")
ITEM_ID = f"cro-fix-{SLUG}-20261018"
OUTD = f"outputs/cro-fixes/{BR}"
IMG = {k: f"{OUTD}/koolestpro_{SLUG}_{v}.png" for k, v in
       {"VARIANTS": "variants-board", "COVER": "carousel_slide1", "BA": "carousel_slide2", "ANNO": "carousel_slide3", "ANNO-GRAPHIC": "annotated"}.items()}
CAROUSEL = f"outputs/cro-fixes/{SLUG}_carousel.html"
CONTENT = f"outputs/cro-fixes/{SLUG}_content.html"
REBUILD = f"outputs/cro-fixes/{SLUG}_rebuild.html"
TITLE = "A game first. The skincare later."
URL = "https://mytopicals.com/"

LINKEDIN = """HOMEPAGE: Open Topicals on a phone and the first thing you get is a scratch card. "Try your luck. Scratch below to see what you win."

Close it and you get the TOPICALS wordmark, a face, and a promo for one kit. Then a black "Scratch to win" pill sits right on top of the only Shop now button.

What I couldn't find on the homepage was a single star rating. Faded Serum has 4.9 stars from 882 reviews. Like Butter has 4.9 from 719. Neither shows up. And "skincare for flare-ups", which is what Topicals sells, only appears in the browser tab title.

So I rebuilt screen one with what was already on their site:

1. Their own Faded Dark Spot Kit photo, full screen, with the kit name and price on it ($28, was $44).
2. 4.9 from 882 Faded Serum reviews, right above the headline.
3. A headline that names the category and keeps their voice: Skincare for flare-ups. Made fun.
4. One red Shop best sellers button with nothing covering it, then a pill for each flare-up: Dark spots, Dry skin, Under eyes, Body.
5. The $30 kit offer moved up into the top bar, where it doesn't block anything.

The fun stays. The game just stops being the first thing you see.

I'd still keep the scratch card. Just later, once people know what they'd be winning.

This is unofficial concept work. Topicals isn't a client."""

XC = {
 "x_variants": """Topicals' homepage hero, 4 ways. Same brand, same products.

A: best sellers, labelled
B: face photo first
C: full-bleed product
D: headline first

Hot take: the live page opens on a scratch card. Any of these beats that.

Which would you ship? My pick goes up next.""",
 "x_carousel": """Homepage teardown: Topicals.

1 A scratch card loads before the skincare
2 Same products, now named on screen one
3 The three questions screen one now answers

Every rating and price came from their own product pages.""",
 "x_ba": """Topicals homepage, before and after.

Before:
❌ A scratch card fills screen one
❌ "Scratch to win" sits on the Shop now button
❌ Zero star ratings on the page

After:
✅ Says what it treats, on screen one
✅ 4.9 from 882 reviews up top
✅ One button, nothing on top of it""",
 "x_anno": """Homepage fix: Topicals.

What a new visitor wonders:
1 Is this for my skin?
2 Does it actually work?
3 Where do I tap?

The old page answered with a scratch card. Now the headline, the 4.9 rating and one red button answer them on screen one.""",
 "x_anno_graphic": """Topicals sells skincare for flare-ups. Their homepage never says so.

I rebuilt it around what a flare-up shopper asks first: what do they sell, do people rate it, where do I start?

Faded Serum has 4.9 stars from 882 reviews. That number now sits above the headline.""",
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
K = "CRO-TOPICALS"
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
       "note": "Real brand, unofficial portfolio/concept CRO work. Not a Topicals client engagement.",
       "pipelineItemId": ITEM_ID, "items": items, "knownGaps": []}
(ROOT / f"{BR}-social-content.json").write_text(json.dumps(lib, indent=2, ensure_ascii=False), encoding="utf-8")
md = [f"# {BRAND} - Social Content Library", "", "Real brand. Unofficial portfolio/concept CRO work, not a Topicals client engagement.", "",
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
  "brand": BRAND, "slug": SLUG, "date": DATE, "pipelineItemId": ITEM_ID, "pageType": "Homepage", "url": URL,
  "images": IMG, "carouselHtml": CAROUSEL, "annotationHtml": f"outputs/cro-fixes/{SLUG}_annotation.html", "variantsBoardHtml": f"outputs/cro-fixes/{SLUG}_variants-board.html", "heroVariants": "outputs/cro-fixes/topicals/_variants/ (CHOICE.md)",
  "rebuildHtml": REBUILD, "reviewPack": CONTENT, "audit": f"outputs/audits/{SLUG}_audit.md",
  "facts": f"outputs/cro-fixes/{SLUG}_facts.json", "brief": f"outputs/cro-fixes/{SLUG}_build-brief.md",
  "captions": f"{OUTD}/captions.txt", "builders": [".ai-workflow/build_topicals_rebuild.py", ".ai-workflow/build_topicals_carousel.py", ".ai-workflow/build_topicals_annotation.py"],
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
<title>CRO Fix review pack - Topicals Homepage - @koolestpro</title>
<style>body{{background:#0e0e0e;color:#e8e8e8;font-family:ui-monospace,Menlo,monospace;margin:0;padding:32px 20px 80px;}}
.w{{max-width:1180px;margin:0 auto;}}h1{{font:800 26px system-ui;margin:0 0 6px}}h2{{font:700 16px system-ui;color:#FA9C0F;margin:34px 0 12px;letter-spacing:.5px}}
.m{{color:#999;font-size:12px}}.g{{display:flex;gap:14px;flex-wrap:wrap}}.g img{{width:360px;border-radius:8px;border:1px solid #222}}
pre{{white-space:pre-wrap;background:#171717;border:1px solid #262626;border-radius:10px;padding:14px;font-size:13px;line-height:1.55;max-width:760px}}
iframe{{width:390px;height:844px;border:1px solid #333;border-radius:18px;background:#fff}}.tabs button{{background:#1b1b1b;color:#ccc;border:1px solid #333;border-radius:6px;padding:7px 12px;margin:0 6px 6px 0;cursor:pointer;font:inherit}}
.dl-pipe{{background:rgba(123,47,190,.14)!important;border-color:rgba(123,47,190,.4)!important;color:#c79bff!important}}</style></head><body><div class="w">
<h1>Topicals homepage: {H.escape(TITLE)}</h1>
<div class="m">HOMEPAGE · Weekly CRO Fix · {DATE} · status Created · unofficial concept work, Topicals is not a client</div>
<h2>#1 FINDING</h2><pre>On a 390x844 phone, screen one is a full-screen scratch-card game ("Try your luck"). Close it and the hero is the TOPICALS wordmark over a face photo, a one-kit promo H1 at y=668, and a "Scratch to win" pill sitting on the only Shop now button (y=776). "Skincare for flare-ups" exists only in the title tag. The homepage shows zero star ratings; the products carry 4.8 to 5.0 from 129 to 882 reviews (JSON-LD). Hero variants: outputs/cro-fixes/topicals/_variants/CHOICE.md (C chosen by Ridwan, 2026-10-18).</pre>
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
const POST_BRAND='Topicals',POST_SLUG='{SLUG}',POST_TYPE='CRO Fix',POST_FOLDER='{CAROUSEL}';
function sendToPipeline(){{const now=new Date();const data={{id:'{ITEM_ID}',type:POST_TYPE,title:{json.dumps(TITLE)},slug:POST_SLUG,status:'Created',day:'',created:now.toISOString(),folder:POST_FOLDER,week:'Week of October 18',month:'October 2026',monthSlug:'2026-10',assets:{{images:{json.dumps(list(IMG.values()))}}}}};
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
        "created": NOW, "folder": CAROUSEL, "week": "Week of October 18", "month": "October 2026", "monthSlug": "2026-10",
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
      "note": "Zero prior cro-fix entries. Homepage (first screen). Beauty/skincare chosen to rotate away from fitness (previous run 10-11) and food (Fly By Jing, 10-04); Topicals tied Fishwife/Brightland on potential and had the longest-rested category. Hero changed since the 09-28 review (now a full-screen scratch-card modal on load, plus the Scratch to win pill over Shop now). #1 finding: a game gates screen one, no category statement, zero ratings on the homepage. Concept work only, Topicals is not a client."})
    t["lastUsedAt"] = NOW; T["meta"]["updatedAt"] = NOW
    tp.write_text(json.dumps(T, indent=2, ensure_ascii=False), encoding="utf-8"); print("targets_pool updated, status left", t["status"])

# ---- tracker
import openpyxl
wb = openpyxl.load_workbook(ROOT / "outputs/weekly-tracker.xlsx"); ws = wb["Weekly Posts"]
if not any(r[2] == SLUG for r in ws.iter_rows(min_row=2, values_only=True)):
    ws.append([DATE, BRAND, SLUG, "CRO Fix", "Created", None, CAROUSEL, LINKEDIN[:200].rsplit(" ", 1)[0] + "...", "Yes"])
    wb.save(ROOT / "outputs/weekly-tracker.xlsx"); print("tracker row added")
