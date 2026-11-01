#!/usr/bin/env python3
"""Finalize the 2026-11-01 weekly CRO Fix (FleeMoto 17/14 supermoto wheel set PRODUCT PAGE):
captions (humanizer-passed, X counted, caption_fit checked), social-content pair, review
pack HTML, manifest + captions.txt, SYNC_DATA merge, targets_pool usedFor, tracker row.
Pattern: finalize_fishwife_cro.py (2026-10-25). Adds the outreach-lead steps (targets_pool add,
replo-rebuilds-pages registration, redesign-hooks entry) from the 2026-10-26 rules."""
import json, re, shutil, sys, pathlib, html as H
from datetime import datetime, timezone
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".ai-workflow" / "tools"))
from caption_fit import check as fit_check
SLUG = "fleemoto_supermoto-wheels-pdp"; BR = "fleemoto"; BRAND = "FleeMoto"
DATE = "2026-11-01"; NOW = datetime.now(timezone.utc).isoformat(timespec="seconds")
ITEM_ID = f"cro-fix-{SLUG}-20261101"
OUTD = f"outputs/cro-fixes/{BR}"
IMG = {k: f"{OUTD}/koolestpro_{SLUG}_{v}.png" for k, v in
       {"VARIANTS": "variants-board", "COVER": "carousel_slide1", "BA": "carousel_slide2", "ANNO": "carousel_slide3", "ANNO-GRAPHIC": "annotated"}.items()}
CAROUSEL = f"outputs/cro-fixes/{SLUG}_carousel.html"
CONTENT = f"outputs/cro-fixes/{SLUG}_content.html"
REBUILD = f"outputs/cro-fixes/{SLUG}_rebuild.html"
TITLE = "Price: 903px down. Screen: 844px."
URL = "https://fleemoto.shop/products/17-14-chrome-super-moto-wheels-set-for-yozma-in-10-tuttio-valintinsu"

LINKEDIN = """PRODUCT PAGE (PDP): FleeMoto sells a $319.99 supermoto wheel set for small e-motos. On a phone, you can't see the price.

I checked it at 390x844. The title starts at 626px. Add to cart is at 895px, the price at 903px. The screen ends at 844.

So screen one is the header, a photo of the whole bike, and the title. That's it.

Two more things sit under the buy buttons:
❌ The fit list (Yozma in 10, Valintinsu EM5, Tuttio), about 200px below Add to cart
❌ "pre-orders will ship 2 weeks after order"

For a wheel set, "will it fit my bike?" comes before "add to cart". And at $319.99 I'd want to know about a 2-week wait before I pay, not after.

What I changed, using only what's on their page:

1. The wheel pair is the hero now, cut out from their own white-background photo. The bike shots moved to an "On the bike" section.
2. Price and a Pre-order tag sit right under the title.
3. A "Fits these bikes" box with the three listed models goes above the button, with a "Not sure? Ask us" link to their contact page.
4. One button: "Pre-order · $319.99". "Ships 2 weeks after order" sits under it.
5. Below that: a fit check, what's in the set, how the pre-order works, an FAQ and their own add-on parts.

There are no reviews on the redesign, because the store doesn't show any yet. I wasn't going to make some up.

This is unofficial concept work. FleeMoto isn't a client."""

XC = {
 "x_variants": """Product page, 3 ways: FleeMoto's $319.99 supermoto wheel set. Same photos, same facts.

A: studio shot + fit box
B: gallery + thumbnails
C: photo grid

My take: a parts page should answer "will it fit?" before it asks for money.

Which would you ship? A, B or C?""",
 "x_carousel": """PDP teardown: FleeMoto's $319.99 wheel set.

1 The price sits 903px down. A phone screen is 844
2 Same wheels, with price, fit and the button on screen one
3 The 3 questions a rider asks before buying wheels

Every fact came from their live page.""",
 "x_ba": """FleeMoto wheel set PDP, before and after.

Before:
❌ Price 903px down, past the screen
❌ Fit list under the buy buttons
❌ 2-week pre-order wait easy to miss

After:
✅ $319.99 on screen one
✅ 3 listed bikes above the button
✅ "Ships 2 weeks after order" by the button""",
 "x_anno": """Product page fix: FleeMoto wheel set.

What a rider wonders on screen one:
1 How much is it?
2 Will it fit my bike?
3 When does it ship?

The old page answered all three below the fold. Now the price, the fit list and the ship time sit around one Pre-order button.""",
 "x_anno_graphic": """Wheels only help if they bolt on.

On FleeMoto's wheel set page (PDP), the list of bikes it fits sat 200px under Add to cart. On a phone, that's below the first screen.

In the redesign it sits above the button, with a link to ask if your bike isn't listed.""",
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
K = "CRO-FLEEMOTO"
items = {
 f"{K}-COVER": {"assetPath": IMG["COVER"], "usedIn": "carousel slide 1 (cover: BEFORE phone with the title-only first screen and the 903px price mark + AFTER phone, real header wordmark)"},
 f"{K}-BA": {"assetPath": IMG["BA"], "usedIn": "carousel slide 2, standalone before/after post", "caption": LINKEDIN},
 f"{K}-ANNO": {"assetPath": IMG["ANNO"], "usedIn": "carousel slide 3, standalone annotation post"},
 f"{K}-VARIANTS": {"assetPath": IMG["VARIANTS"], "usedIn": "variants board (3 product-page first screens A-C, no heading text on the image, neutral, no pick shown); X debate post that goes out BEFORE the carousel"},
 f"{K}-ANNO-GRAPHIC": {"assetPath": IMG["ANNO-GRAPHIC"], "usedIn": "standalone clear-background annotation graphic (1080x1080)"},
 f"{K}-CAROUSEL": {"assetPath": CAROUSEL, "usedIn": "the review/export HTML (all 3 slides + download panel)",
                   "captionOptions": [{"id": "linkedin", "caption": LINKEDIN, "hashtags": ["#CRO", "#Shopify", "#EcommerceUX", "#ProductPage"]}]},
 **{f"{K}-{XKEY[k][0]}": {"assetPath": ([IMG["COVER"], IMG["BA"], IMG["ANNO"]] if k == "x_carousel" else IMG[XKEY[k][1]]),
                              "caption": t, "platform": "X", "captionKey": k, "chars": len(t)} for k, t in XC.items()},
}
lib = {"brand": BRAND, "brandSlug": BR, "isConceptBrand": False,
       "note": "Real brand, unofficial portfolio/concept CRO work. Not a FleeMoto client engagement. FleeMoto is a cold-email lead (tier 2); the redesign is the outreach hook.",
       "pipelineItemId": ITEM_ID, "items": items, "knownGaps": []}
(ROOT / f"{BR}-social-content.json").write_text(json.dumps(lib, indent=2, ensure_ascii=False), encoding="utf-8")
md = [f"# {BRAND} - Social Content Library", "", "Real brand. Unofficial portfolio/concept CRO work, not a FleeMoto client engagement.", "",
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
  "brand": BRAND, "slug": SLUG, "date": DATE, "pipelineItemId": ITEM_ID, "pageType": "Product Page (PDP)", "url": URL,
  "images": IMG, "carouselHtml": CAROUSEL, "annotationHtml": f"outputs/cro-fixes/{SLUG}_annotation.html", "variantsBoardHtml": f"outputs/cro-fixes/{SLUG}_variants-board.html", "heroVariants": "outputs/cro-fixes/fleemoto/_variants/ (CHOICE.md)", "presentation": "outputs/cro-fixes/fleemoto_supermoto-wheels-pdp_presentation/",
  "rebuildHtml": REBUILD, "reviewPack": CONTENT, "audit": f"outputs/audits/{SLUG}_audit.md",
  "facts": f"outputs/cro-fixes/{SLUG}_facts.json", "brief": f"outputs/cro-fixes/{SLUG}_build-brief.md",
  "captions": f"{OUTD}/captions.txt", "builders": [".ai-workflow/prep_fleemoto_assets.py", ".ai-workflow/build_fleemoto_rebuild.py", ".ai-workflow/build_fleemoto_phones.py", ".ai-workflow/build_fleemoto_carousel.py", ".ai-workflow/build_fleemoto_annotation.py", ".ai-workflow/build_fleemoto_compare.py", ".ai-workflow/finalize_fleemoto_cro.py"],
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
<title>CRO Fix review pack - FleeMoto Wheel Set PDP - @koolestpro</title>
<style>body{{background:#0e0e0e;color:#e8e8e8;font-family:ui-monospace,Menlo,monospace;margin:0;padding:32px 20px 80px;}}
.w{{max-width:1180px;margin:0 auto;}}h1{{font:800 26px system-ui;margin:0 0 6px}}h2{{font:700 16px system-ui;color:#FA9C0F;margin:34px 0 12px;letter-spacing:.5px}}
.m{{color:#999;font-size:12px}}.g{{display:flex;gap:14px;flex-wrap:wrap}}.g img{{width:360px;border-radius:8px;border:1px solid #222}}
pre{{white-space:pre-wrap;background:#171717;border:1px solid #262626;border-radius:10px;padding:14px;font-size:13px;line-height:1.55;max-width:760px}}
iframe{{width:390px;height:844px;border:1px solid #333;border-radius:18px;background:#fff}}.tabs button{{background:#1b1b1b;color:#ccc;border:1px solid #333;border-radius:6px;padding:7px 12px;margin:0 6px 6px 0;cursor:pointer;font:inherit}}
.dl-pipe{{background:rgba(123,47,190,.14)!important;border-color:rgba(123,47,190,.4)!important;color:#c79bff!important}}</style></head><body><div class="w">
<h1>FleeMoto wheel set product page (PDP): {H.escape(TITLE)}</h1>
<div class="m">PRODUCT PAGE (PDP) · Weekly CRO Fix · {DATE} · status Created · unofficial concept work, FleeMoto is not a client</div>
<h2>#1 FINDING</h2><pre>On a 390x844 phone the product title starts at y=626, Add to cart at y=895 and the price at y=903, past the 844px screen. The fit list ("compatibility": Yozma in 10, valintinsu em5, tuttio) starts at y=1093, about 200px under Add to cart and below the Shop Pay button, and "pre-orders will ship 2 weeks after order" sits at y=1021, also under the buttons. The description stops mid-sentence ("These 17/14 inch chrome super moto"). No reviews are shown (none invented in the rebuild). Full audit: outputs/audits/{SLUG}_audit.md. Hero variants: outputs/cro-fixes/fleemoto/_variants/CHOICE.md (A chosen in this unattended run). Outreach: tier-2 lead in the build queue; compare images in outputs/cro-fixes/{SLUG}_presentation/.</pre>
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
const POST_BRAND='FleeMoto',POST_SLUG='{SLUG}',POST_TYPE='CRO Fix',POST_FOLDER='{CAROUSEL}';
function sendToPipeline(){{const now=new Date();const data={{id:'{ITEM_ID}',type:POST_TYPE,title:{json.dumps(TITLE)},slug:POST_SLUG,status:'Created',day:'',created:now.toISOString(),folder:POST_FOLDER,week:'Week of November 1',month:'November 2026',monthSlug:'2026-11',assets:{{images:{json.dumps(list(IMG.values()))}}}}};
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
        "created": NOW, "folder": CAROUSEL, "week": "Week of November 1", "month": "November 2026", "monthSlug": "2026-11",
        "captions": {"linkedin": LINKEDIN, "x": X}, "assets": {"images": list(IMG.values())}}
shutil.copy(cs, str(cs) + ".bak")
ex = next((i for i in data["items"] if i.get("id") == ITEM_ID), None)
if ex is not None:
    ex["captions"] = item["captions"]; ex["assets"] = item["assets"]; ex["title"] = item["title"]; print("SYNC: existing item refreshed (no duplicate)")
else:
    data["items"].append(item); print("SYNC: added", ITEM_ID, "items now", len(data["items"]))
data["months"].setdefault("2026-11", {"label": "November 2026", "htmlPath": "outputs/ideas/ideas_2026-11.html", "jsonPath": "outputs/ideas/ideas_2026-11.json", "totalIdeas": 0})
data["meta"]["updatedAt"] = NOW
cs.write_text(src[:m.start(2)] + json.dumps(data, ensure_ascii=False, indent=2) + src[m.end(2):], encoding="utf-8")

# ---- targets pool (per-stream usedFor only; status stays Available)
tp = ROOT / "targets_pool.json"; T = json.loads(tp.read_text(encoding="utf-8"))
t = next((x for x in T["targets"] if x["brand"] == BRAND), None)
if t is None:
    t = {"id": "target-fleemoto-20261101", "brand": BRAND, "url": URL, "category": "other", "pageType": "Product Page",
         "leadPotential": "High", "visualPotential": "Medium",
         "mobileIssueSummary": "PDP (mobile, 390x844, checked 2026-11-01): title at 626px, Add to cart at 895px and price at 903px, past the screen; the fit list sits ~200px under the buy buttons and the 2-week pre-order note is under them too. Description stops mid-sentence. No reviews shown.",
         "isRealBrand": True, "isClient": False, "status": "Available", "usedFor": [], "source": "outreach-directory-scrape", "outreachLead": True,
         "notes": "Small e-moto parts store (8 products, Horizon theme, text-only logo). Added 2026-11-01 from buildQueue (tier 2, contactable).", "addedAt": NOW, "lastUsedAt": None}
    T["targets"].append(t); print("targets_pool: added FleeMoto")
if not any(u.get("pipelineItemId") == ITEM_ID for u in t["usedFor"]):
    t["usedFor"].append({"stream": "cro-fix", "date": DATE, "pipelineItemId": ITEM_ID,
      "note": "Build queue pick (tier 2: emailed, no reply, problemWorth 3, buildPage Product Page). First cro-fix entry for this brand. Auto/moto parts rotates away from food (Fishwife 10-25), beauty (Topicals 10-18) and fitness (Bala 10-11). #1 finding: price 903px down and Add to cart 895px on a 844px screen; fit list ~200px under the buy buttons. Contactable store, outreach hook written. Concept work only, FleeMoto is not a client."})
    t["lastUsedAt"] = NOW; T["meta"]["updatedAt"] = NOW
    tp.write_text(json.dumps(T, indent=2, ensure_ascii=False), encoding="utf-8"); print("targets_pool updated, status left", t["status"])

# ---- tracker
import openpyxl
wb = openpyxl.load_workbook(ROOT / "outputs/weekly-tracker.xlsx"); ws = wb["Weekly Posts"]
if not any(r[2] == SLUG for r in ws.iter_rows(min_row=2, values_only=True)):  # one row per post
    ws.append([DATE, BRAND, SLUG, "CRO Fix", "Created", None, CAROUSEL, LINKEDIN[:200].rsplit(" ", 1)[0] + "...", "Yes"])
    wb.save(ROOT / "outputs/weekly-tracker.xlsx"); print("tracker row added")

# ---- replo-rebuilds-pages.json (real-redesign, for the Saturday Template Showcase 7+ days later)
rp = ROOT / "replo-rebuilds-pages.json"; RP = json.loads(rp.read_text(encoding="utf-8"))
if not any(p.get("showcaseSlug") == SLUG for p in RP["pages"]):
    shutil.copy(rp, str(rp) + ".bak-2026-11-01")
    RP["pages"].append({"kind": "real-redesign", "isRealBrand": True, "isClient": False, "targetId": t["id"], "liveUrl": URL,
        "brand": BRAND, "brandSlug": BR, "pageType": "Product Page", "showcaseSlug": SLUG, "sourcePath": REBUILD,
        "presentationDir": f"outputs/cro-fixes/{SLUG}_presentation/", "active": True, "retired": False, "usedForTemplateShowcase": False,
        "sortOrder": max(p.get("sortOrder", 0) for p in RP["pages"]) + 1, "builtBy": "cro-fix", "date": DATE,
        "notes": "Sunday CRO Fix 2026-11-01. Full PDP redesign of fleemoto.shop's 17/14 chrome super moto wheel set. Every fact from the live page; no reviews shown (store has none). Header logo is text-only on the live site, carried over as text. Showcase caption must say 'Concept redesign of FleeMoto'."})
    rp.write_text(json.dumps(RP, indent=2, ensure_ascii=False), encoding="utf-8"); print("replo-rebuilds-pages: registered")

# ---- outreach/redesign-hooks.json (tier-2 lead: next follow-up becomes the redesign email)
hp = ROOT / "outreach/redesign-hooks.json"; HK = json.loads(hp.read_text(encoding="utf-8"))
if not any(h.get("domain") == "fleemoto.shop" and h.get("pagePath") == REBUILD for h in HK["hooks"]):
    HK["hooks"].append({"domain": "fleemoto.shop", "brand": BRAND, "targetId": t["id"], "pageType": "Product Page",
        "problemPage": URL, "pagePath": REBUILD, "mobileStripPath": f"outputs/cro-fixes/{SLUG}_presentation/fleemoto-mobile-strip.png",
        "builtBy": "cro-fix", "date": DATE, "status": "ready",
        "compareImagePath": f"outputs/cro-fixes/{SLUG}_presentation/fleemoto-compare.png",
        "compareFullPath": f"outputs/cro-fixes/{SLUG}_presentation/fleemoto-compare-full.png",
        "emailAngle": "The price (903px) and Add to cart (895px) sit below a phone's first screen, and the list of bikes the set fits is under the buy buttons. The redesign puts price, fit and one Pre-order button on screen one."})
    hp.write_text(json.dumps(HK, indent=2, ensure_ascii=False), encoding="utf-8"); print("redesign-hooks: added")
