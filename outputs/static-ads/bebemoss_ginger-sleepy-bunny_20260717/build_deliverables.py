#!/usr/bin/env python3
"""Emit index.html review page + {brand}-social-content.json/.md from one caption source."""
import json, os, html

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(D, "..", "..", ".."))
SLUG = "bebemoss_ginger-sleepy-bunny"
DATE = "20260717"
ITEM_ID = f"static-ad-{SLUG}-{DATE}"
FOLDER = f"outputs/static-ads/{SLUG}_{DATE}/index.html"
TITLE = "Bebemoss — Ginger the Sleepy Bunny · 4-Angle Static Ad Showcase"
DISC = "Unofficial concept work. Not affiliated with or commissioned by Bebemoss."

# ---------- FINAL CAPTIONS (humanized, straight quotes, no invented claims) ----------
LI = (
"Bebemoss sells a $44 crocheted bunny. No discount codes, no countdown timers, "
"no \"10,000 reviews\" banner slapped across the page.\n\n"
"So I set myself a rule: build 4 ad directions for one of their toys and don't invent a single claim.\n\n"
"Where each one came from:\n\n"
"Problem: most \"first toys\" are plastic and in a landfill before the kid starts school. This one gets kept.\n\n"
"Benefit: GOTS organic cotton, crocheted by hand, made to EU toy-safety standards. Real specs, no filler.\n\n"
"Social proof: one actual review, \"she's actually a work of art.\" Plus their 4.9 from wholesale buyers on Faire.\n\n"
"Offer: they have no sale to run, so I told the truth instead. It's made to order, by hand. That's the reason to act, not a fake timer.\n\n"
"Same bunny. Same photo. Four different reasons to care, depending on where the buyer's head is when they see it.\n\n"
"That's most of the job with ad creative. Not \"make it pop.\" Figure out what the person needs to hear first.\n\n"
"Concept work. I'm not affiliated with Bebemoss, I just liked the product enough to think about how I'd sell it."
)

X1 = ("4 ad directions from one $44 crocheted bunny.\n\n"
"No fake discounts. No made-up review counts. Every line traces back to something real about the brand.\n\n"
"Same product, 4 different reasons to buy it. That's the whole game.\n\n"
"(concept work, not affiliated with Bebemoss)")

X2 = ("Best social proof isn't \"10,000 reviews.\"\n\n"
"It's one specific line: \"when she peeked out of the bag, I was amazed, she's actually a work of art.\"\n\n"
"Built a whole ad around that one real review. Specific beats big every time.\n\n"
"(concept, not affiliated)")

X3 = ("Bebemoss has no discount to run. So how do you write an \"act now\" ad without lying?\n\n"
"You don't fake a countdown. You tell the truth: it's crocheted by hand, made to order, not sitting in a warehouse.\n\n"
"Real scarcity does the work a fake timer can't.")

CAP_PROBLEM = ("Most \"first toys\" are plastic, and in a landfill before the kid starts school. "
"A hand-crocheted organic cotton one is the toy they actually keep. "
"(Concept ad for Bebemoss, not affiliated.)")
CAP_BENEFIT = ("Made by hand, made to keep. GOTS organic cotton, every stitch crocheted by an artisan mom, "
"built to EU toy-safety standards. (Concept ad for Bebemoss, not affiliated.)")
CAP_PROOF = ("\"When she peeked out of the bag, I was amazed, she's actually a work of art.\" "
"4.9 from wholesale buyers, made by 120+ artisan moms. (Concept ad for Bebemoss, not affiliated.)")
CAP_OFFER = ("Not mass-stocked. Each Bebemoss bunny gets crocheted when you order it. Real scarcity, no fake timer. "
"Meet Ginger the Sleepy Bunny, $44. (Concept ad, not affiliated.)")

HASH = ["#ecommerce", "#dtc", "#advertising", "#adcreative", "#cro", "#brandstrategy"]

ADS = [
    ("ad-1-problem-solution.png", "Problem / Solution", CAP_PROBLEM, "SA-BEBEMOSS-PROBLEM"),
    ("ad-2-benefit-result.png",   "Benefit / Result",   CAP_BENEFIT,  "SA-BEBEMOSS-BENEFIT"),
    ("ad-3-social-proof.png",     "Social Proof / Trust",CAP_PROOF,    "SA-BEBEMOSS-PROOF"),
    ("ad-4-offer-urgency.png",    "Offer / Urgency",    CAP_OFFER,    "SA-BEBEMOSS-OFFER"),
]

# ============ index.html ============
def esc(s): return html.escape(s).replace("\n", "<br>")
cards = ""
for fn, angle, cap, key in ADS:
    cards += f"""
    <div class="card">
      <img src="{fn}" alt="{angle}">
      <div class="meta">
        <div class="angle">{angle}<span class="key">{key}</span></div>
        <p>{esc(cap)}</p>
      </div>
    </div>"""

xblocks = "".join(f'<div class="xpost"><span class="key">SA-BEBEMOSS-X{i+1}</span><p>{esc(x)}</p></div>'
                  for i, x in enumerate([X1, X2, X3]))

index_html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(TITLE)}</title>
<style>
:root{{--o:#FF9500;--p:#7B2FBE;--pk:#E040A0;}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#080808;color:#eee;font-family:-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.6;padding:40px 20px}}
.wrap{{max-width:1080px;margin:0 auto}}
.hd{{text-align:center;margin-bottom:8px;font-family:'Syne',sans-serif;font-weight:800;font-size:30px}}
.sub{{text-align:center;color:#888;font-size:13px;margin-bottom:6px}}
.disc{{text-align:center;color:#FF9500;font-size:12px;background:rgba(255,149,0,.08);border:1px solid rgba(255,149,0,.25);border-radius:8px;padding:8px 14px;max-width:640px;margin:14px auto 40px}}
.combo{{text-align:center;margin:0 auto 48px;max-width:620px}}
.combo img{{width:100%;border-radius:14px;border:1px solid #1e1e1e}}
.section-label{{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--o);margin:0 0 16px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:48px}}
.card{{background:#0d0d0d;border:1px solid #1c1c1c;border-radius:14px;overflow:hidden}}
.card img{{width:100%;display:block}}
.card .meta{{padding:16px 18px 20px}}
.angle{{font-family:'Syne',sans-serif;font-weight:700;font-size:15px;color:#fff;display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}}
.key{{font-family:'DM Mono',monospace;font-size:9px;color:#666;background:#151515;padding:3px 8px;border-radius:5px;letter-spacing:1px}}
.card p{{font-size:13px;color:#bbb}}
.capbox{{background:#0d0d0d;border:1px solid #1c1c1c;border-radius:14px;padding:24px;margin-bottom:24px}}
.capbox h3{{font-family:'Syne',sans-serif;font-size:16px;margin-bottom:12px}}
.capbox p{{font-size:14px;color:#cfcfcf;white-space:normal}}
.xpost{{border-top:1px solid #1c1c1c;padding:16px 0}}
.xpost:first-of-type{{border-top:none}}
.hash{{color:#7aa2ff;font-size:12px;margin-top:10px}}
</style></head>
<body><div class="wrap">
  <div class="hd">Ginger the Sleepy Bunny — Static Ad Showcase</div>
  <div class="sub">Bebemoss · 4 ad angles · generated {DATE[:4]}-{DATE[4:6]}-{DATE[6:]}</div>
  <div class="disc">{html.escape(DISC)} Product photography is AI-generated (gpt-image-2), not a real product photo. Ad layouts and text composited over it. Facts sourced from bebemoss.com and Faire; no figures were invented.</div>

  <div class="combo">
    <div class="section-label">Combined LinkedIn Showcase — SA-BEBEMOSS-COMBO</div>
    <img src="combined-showcase.png" alt="Combined 2x2 showcase">
  </div>

  <div class="section-label">The 4 Ad Concepts</div>
  <div class="grid">{cards}
  </div>

  <div class="section-label">LinkedIn Caption — SA-BEBEMOSS-COMBO</div>
  <div class="capbox"><p>{esc(LI)}</p><div class="hash">{' '.join(HASH)}</div></div>

  <div class="section-label">X / Twitter Posts</div>
  <div class="capbox">{xblocks}</div>

  <!-- ══ PIPELINE EXPORT ══ -->
  <div style="max-width:600px;margin:24px auto 0;">
  <div style="background:#0a0a0a;border:1px solid rgba(255,149,0,0.2);border-radius:12px;padding:24px;">
    <div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;margin-bottom:8px;">Content Pipeline</div>
    <div style="font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.45);line-height:1.7;margin-bottom:18px;">Export this post to the content system. Downloads a <code>.json</code> file — open <code>ridwan_content_system_updated.html</code> and sync to register it.</div>
    <button onclick="sendToPipeline()" style="background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;font-family:'Syne',sans-serif;font-weight:700;font-size:13px;padding:12px 28px;border:none;border-radius:8px;cursor:pointer;letter-spacing:0.5px;">Send to Content Pipeline →</button>
    <div id="pipeline-status" style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.35);margin-top:12px;min-height:16px;"></div>
  </div>
  </div>
</div>
<script>
const POST_BRAND  = 'Bebemoss';
const POST_SLUG   = '{SLUG}';
const POST_TYPE   = 'Static Ad';
const dateStr     = '{DATE}';
const POST_FOLDER = 'outputs/static-ads/' + POST_SLUG + '_' + dateStr + '/index.html';
function sendToPipeline() {{
  const now = new Date();
  const data = {{
    id:        '{ITEM_ID}',
    type:      POST_TYPE,
    title:     '{TITLE}',
    slug:      POST_SLUG,
    status:    'Created',
    day:       '',
    created:   now.toISOString(),
    folder:    POST_FOLDER,
    week:      'Week of ' + now.toLocaleDateString('en-US', {{ month: 'long', day: 'numeric' }}),
    month:     now.toLocaleDateString('en-US', {{ month: 'long', year: 'numeric' }}),
    monthSlug: now.toISOString().slice(0, 7)
  }};
  console.log('EXPORT_POST_JSON', JSON.stringify(data));
  const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = POST_SLUG + '_pipeline.json';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
  const s = document.getElementById('pipeline-status');
  if (s) s.textContent = '✓ Exported — open ridwan_content_system_updated.html and sync.';
}}
</script>
</body></html>"""

open(os.path.join(D, "index.html"), "w").write(index_html)
print("wrote index.html")

# ============ {brand}-social-content.json ============
def asset(key, atype, path, caption, plats, hashtags=None):
    return {"platform": plats, "assetType": atype, "assetPath": path,
            "caption": caption, "hashtags": hashtags or [],
            "status": "Not Posted", "postedAt": None}

base = f"outputs/static-ads/{SLUG}_{DATE}/"
sc = {
  "brand": "Bebemoss",
  "brandSlug": "bebemoss",
  "relatedPipelineItemIds": [ITEM_ID],
  "disclaimer": DISC,
  "notes": "Product photography AI-generated (gpt-image-2), flagged. All claims sourced from bebemoss.com and Faire; nothing invented.",
  "assets": {
    "SA-BEBEMOSS-COMBO":   asset("combo","image",base+"combined-showcase.png",LI,["linkedin","instagram"],HASH),
    "SA-BEBEMOSS-PROBLEM": asset("problem","image",base+"ad-1-problem-solution.png",CAP_PROBLEM,["linkedin","instagram"]),
    "SA-BEBEMOSS-BENEFIT": asset("benefit","image",base+"ad-2-benefit-result.png",CAP_BENEFIT,["linkedin","instagram"]),
    "SA-BEBEMOSS-PROOF":   asset("proof","image",base+"ad-3-social-proof.png",CAP_PROOF,["linkedin","instagram"]),
    "SA-BEBEMOSS-OFFER":   asset("offer","image",base+"ad-4-offer-urgency.png",CAP_OFFER,["linkedin","instagram"]),
    "SA-BEBEMOSS-X1":      asset("x-combo","text",base+"combined-showcase.png",X1,["x"]),
    "SA-BEBEMOSS-X2":      asset("x-proof","text",base+"ad-3-social-proof.png",X2,["x"]),
    "SA-BEBEMOSS-X3":      asset("x-offer","text",base+"ad-4-offer-urgency.png",X3,["x"]),
  }
}
open(os.path.join(ROOT, "bebemoss-social-content.json"), "w").write(json.dumps(sc, indent=2))
print("wrote bebemoss-social-content.json")

# ============ {brand}-social-content.md ============
md = f"""# BEBEMOSS — Social Media Content
**Brand:** Bebemoss (Ginger the Sleepy Bunny) · {DISC}
**Posts covered:** Static Ad Showcase ({DATE[:4]}-{DATE[4:6]}-{DATE[6:]})
**Machine-readable version:** `bebemoss-social-content.json` — same keys, used by automation. Update both together.

> Note: product photography is AI-generated (gpt-image-2) and flagged as such. Every claim traces to bebemoss.com or Faire — nothing was invented.

---

## HOW TO USE THIS FILE

| Platform | What to post | Caption key |
|---|---|---|
| LinkedIn | Combined 2x2 showcase | SA-BEBEMOSS-COMBO |
| LinkedIn / Instagram | Any single ad concept | SA-BEBEMOSS-PROBLEM, -BENEFIT, -PROOF, -OFFER |
| Twitter/X | Combined showcase | SA-BEBEMOSS-X1 |
| Twitter/X | Social proof ad | SA-BEBEMOSS-X2 |
| Twitter/X | Offer/urgency ad | SA-BEBEMOSS-X3 |

All assets live in `{base}`. Every caption already carries the "concept, not affiliated" framing — keep it in when posting.

---

## STATIC AD SHOWCASE — {DATE[:4]}-{DATE[4:6]}-{DATE[6:]}

**SA-BEBEMOSS-COMBO — `combined-showcase.png`** (LinkedIn)
```
{LI}

{' '.join(HASH)}
```

**SA-BEBEMOSS-PROBLEM — `ad-1-problem-solution.png`**
```
{CAP_PROBLEM}
```

**SA-BEBEMOSS-BENEFIT — `ad-2-benefit-result.png`**
```
{CAP_BENEFIT}
```

**SA-BEBEMOSS-PROOF — `ad-3-social-proof.png`**
```
{CAP_PROOF}
```

**SA-BEBEMOSS-OFFER — `ad-4-offer-urgency.png`**
```
{CAP_OFFER}
```

**SA-BEBEMOSS-X1 — combined showcase (X)**
```
{X1}
```

**SA-BEBEMOSS-X2 — social proof (X)**
```
{X2}
```

**SA-BEBEMOSS-X3 — offer/urgency (X)**
```
{X3}
```
"""
open(os.path.join(ROOT, "bebemoss-social-content.md"), "w").write(md)
print("wrote bebemoss-social-content.md")
print("DONE")
