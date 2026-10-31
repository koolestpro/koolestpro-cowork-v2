"""
build_ts_ig_carousel.py: the 6-slide Instagram carousel for a Template Showcase
run (docs/system/template-showcase-ig-carousel.md), 1080x1350 each.

Added 2026-10-17 (template-showcase-weekly, moult_hp-01 + halos_pp-01). Until
now every run hand-built these slides; this makes them one command so the
format stays identical run to run and only gets better.

Usage:
  python3 build_ts_ig_carousel.py config.json

config.json:
{
  "page": "/abs/path/to/index.html",
  "out_dir": "/abs/outputs/templates/{slug}_{date}/ig-carousel",
  "full_page_png": "/abs/.../{slug}-full-page.png",
  "full_raw_png": "/abs/.../desktop-full.jpg",  (REQUIRED: raw 1440-wide full-page capture, used by slide 5)
  "mobile_shots": ["/abs/mob_hero.png", "/abs/mob_mid.png", "/abs/mob_foot.png"],
  "brand": "MOULT", "page_label": "homepage",
  "hero_selector": "section.hero",
  "sections": [["HEADER & HERO SECTION", "section.hero"], ["PRODUCT SECTION", "#featured-product"]],
  "cover_headline": "A homepage built to sell one brush",
  "slide2_title": "The whole page in one view", "slide2_sub": "...",
  "slide3_eyebrow": "MOBILE VIEW", "slide3_title": "Same page on a phone.",
  "brand_bg": "#22352B", "brand_ink": "#FBF7EF", "accent": "#C4552F",
  "fonts": [["Fraunces", "Headings"], ["Manrope", "Body and UI"]],
  "palette": ["#22352B", "#C4552F", "#FBF7EF", "#8FA48F"],
  "tools": ["HTML + CSS", "Claude"],
  "cta_title": "Want your store built next?",
  "cta_line": "I build Shopify pages for DTC brands...",
  "cta_url": "koolestpro.com/services/page-build"
}

Rules baked in: no gradient TEXT (gradients only on backgrounds/bars/buttons),
headline >= 88px, body >= 40px, footer >= 26px, real page captures only.
"""
import base64, io, json, os, subprocess, sys, tempfile

from PIL import Image
from playwright.sync_api import sync_playwright

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills",
                   "page-presentation-kit", "scripts")
W, H = 1080, 1350
FOOT = "@koolestpro | Shopify CRO &amp; UX Design"


def b64(img, fmt="JPEG", q=88):
    buf = io.BytesIO()
    if fmt == "JPEG":
        img.convert("RGB").save(buf, "JPEG", quality=q)
    else:
        img.save(buf, "PNG")
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


def capture_sections(page_path, hero_sel, sections, tmp):
    """Desktop (1440) element captures after walking the page so reveal
    animations have fired. Returns {selector: PIL image}."""
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
        pg.goto("file://" + page_path)
        pg.wait_for_timeout(1200)
        hgt = pg.evaluate("document.body.scrollHeight")
        y = 0
        while y < hgt:
            pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(250); y += 700
        pg.evaluate("""() => { document.querySelectorAll('*').forEach(el => {
            const cs = getComputedStyle(el);
            if (cs.position === 'fixed' || cs.position === 'sticky') el.style.setProperty('position','static','important');
            if (parseFloat(cs.opacity) < 1 && el.className && String(el.className).includes('fade')) el.style.opacity = 1; }); }""")
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
        for sel in [hero_sel] + [s for _, s in sections]:
            if sel in out:
                continue
            f = os.path.join(tmp, f"sec_{len(out)}.png")
            pg.locator(sel).first.screenshot(path=f)
            out[sel] = Image.open(f).convert("RGB")
        br.close()
    return out


def phones_strip(shots, tmp):
    f = os.path.join(tmp, "phones.png")
    subprocess.run([sys.executable, os.path.join(KIT, "build_device_still.py"), "preview",
                    "--style", "flat_packed_3", *sum([["--screenshot", s] for s in shots], []),
                    "--output", f, "--width", "1800", "--height", "1300",
                    "--bg-mode", "transparent"], check=True)
    im = Image.open(f).convert("RGBA")
    return im.crop(im.getbbox())


BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:'DM Sans',sans-serif;position:relative}
.h{font-family:'Syne',sans-serif;font-weight:800;letter-spacing:-2px;line-height:1.0}
.foot{position:absolute;left:0;right:0;bottom:44px;text-align:center;font-size:26px;font-weight:500}
.chip{display:inline-block;padding:10px 26px;border-radius:40px;background:rgba(0,0,0,.55);color:#fff}
"""


def slide1(c, hero):
    hero_w = 960
    hero_img = hero.copy()
    if hero_img.height / hero_img.width > 0.62:
        hero_img = hero_img.crop((0, 0, hero_img.width, int(hero_img.width * 0.62)))
    return f"""<style>{BASE_CSS}
body{{background:#0B0710}}
.glow1{{position:absolute;width:900px;height:900px;left:-300px;top:-320px;border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,.42),transparent 65%);filter:blur(30px)}}
.glow2{{position:absolute;width:1000px;height:1000px;right:-380px;bottom:-300px;border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,.55),transparent 65%);filter:blur(30px)}}
.dia{{position:absolute;border:2px solid rgba(255,149,0,.5);transform:rotate(45deg)}}
.eyebrow{{position:absolute;left:60px;top:70px;font-size:30px;font-weight:700;letter-spacing:4px;color:#FF9500}}
.title{{position:absolute;left:60px;top:126px;width:960px;font-size:{c.get('cover_size', 100)}px;color:#fff}}
.card{{position:absolute;left:60px;bottom:200px;width:{hero_w}px;border-radius:26px;overflow:hidden;background:#fff;padding:10px;box-shadow:0 40px 90px rgba(0,0,0,.6)}}
.card img{{width:100%;display:block;border-radius:18px}}
.swipe{{position:absolute;left:60px;bottom:58px;font-size:34px;font-weight:700;color:#fff}}
.bar{{position:absolute;left:60px;bottom:118px;width:180px;height:6px;border-radius:3px;background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE)}}
</style>
<div class="glow1"></div><div class="glow2"></div>
<div class="dia" style="width:70px;height:70px;right:90px;top:90px"></div>
<div class="dia" style="width:36px;height:36px;right:107px;top:107px"></div>
<div class="eyebrow">CONCEPT STORE BUILD · {c['brand']}</div>
<div class="h title">{c['cover_headline']}</div>
<div class="card"><img src="{b64(hero_img)}"></div>
<div class="bar"></div>
<div class="swipe">Swipe to see the whole page &rarr;</div>"""


def slide2(c, full):
    return f"""<style>{BASE_CSS}
body{{background:#EEEEF0}}
.col{{position:absolute;left:50px;right:50px;top:56px;bottom:100px;display:flex;flex-direction:column;align-items:center}}
.t{{text-align:center;font-size:92px;color:#111}}
.s{{text-align:center;font-size:40px;color:#555;line-height:1.25;margin:18px 30px 30px}}
.img{{flex:1;min-height:0;width:100%;display:flex;align-items:center;justify-content:center}}
.img img{{max-width:100%;max-height:100%;border-radius:10px;box-shadow:0 20px 60px rgba(0,0,0,.12)}}
.foot{{color:#666}}
</style>
<div class="col"><div class="h t">{c['slide2_title']}</div><div class="s">{c['slide2_sub']}</div>
<div class="img"><img src="{b64(full, q=86)}"></div></div><div class="foot">{FOOT}</div>"""


def slide3(c, phones):
    return f"""<style>{BASE_CSS}
body{{background:{c['brand_bg']}}}
.e{{position:absolute;left:70px;top:70px;font-size:30px;font-weight:700;letter-spacing:4px;color:{c['accent_on_bg']}}}
.t{{position:absolute;left:70px;top:120px;width:940px;font-size:100px;color:{c['brand_ink']}}}
.ph{{position:absolute;left:40px;right:40px;top:{c.get('phones_top', 470)}px;bottom:120px;display:flex;align-items:center;justify-content:center}}
.ph img{{max-width:100%;max-height:100%;filter:drop-shadow(0 30px 50px rgba(0,0,0,.35))}}
</style>
<div class="e">{c['slide3_eyebrow']}</div><div class="h t">{c['slide3_title']}</div>
<div class="ph"><img src="{b64(phones, 'PNG')}"></div><div class="foot"><span class="chip">{FOOT}</span></div>"""


def slide4(c, secs):
    blocks = ""
    # 2026-10-31: crop height is derived from the space actually available
    # (canvas minus top offset, footer, labels and gaps) instead of a fixed
    # 0.44 ratio, which left a ~250px empty band at the bottom of the slide
    # (kura_lp-01). 960 = content width (1080 - 2*60).
    n = max(1, len(secs))
    avail = H - 56 - 120 - n * (60 + 18) - n * 36
    # Budget in rendered px (960 wide). A section shorter than its share keeps
    # its natural height and hands the leftover to the taller ones, so the
    # slide fills down to the footer instead of ending in an empty band.
    nat = [img.height * 960 / img.width for _, img in secs]
    budget = [min(h, 960 * 0.9) for h in nat]
    share = avail / n
    short = [i for i, h in enumerate(budget) if h <= share]
    tall = [i for i in range(n) if i not in short]
    if tall:
        spare = avail - sum(budget[i] for i in short)
        for i in tall:
            budget[i] = min(budget[i], spare / len(tall))
    for (label, img), bh in zip(secs, budget):
        im = img
        if im.height * 960 / im.width > bh:
            im = im.crop((0, 0, im.width, int(im.width * bh / 960)))
        blocks += f"""<div class="lab h">{label}</div><div class="crop"><img src="{b64(im)}"></div>"""
    return f"""<style>{BASE_CSS}
body{{background:{c['light_bg']}}}
.wrap{{position:absolute;left:60px;right:60px;top:56px}}
.lab{{font-size:56px;color:{c['accent']};letter-spacing:-1px;margin:0 0 18px}}
.crop{{border-radius:18px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.14);margin-bottom:36px}}
.crop img{{width:100%;display:block}}
.foot{{color:#777}}
</style><div class="wrap">{blocks}</div><div class="foot">{FOOT}</div>"""


def slide5(c, full_raw):
    # tiles: consecutive page bands, each a 1440x900 window, rotated as a wall
    tiles = []
    step = max(1, (full_raw.height - 900) // 11)
    for i in range(12):
        y = min(i * step, full_raw.height - 900)
        tiles.append(b64(full_raw.crop((0, y, 1440, y + 900)).resize((720, 450)), q=80))
    cells = "".join(f'<img src="{t}">' for t in tiles)
    return f"""<style>{BASE_CSS}
body{{background:{c['brand_bg']}}}
.wall{{position:absolute;left:-560px;top:-420px;width:2200px;display:grid;grid-template-columns:repeat(3,720px);gap:26px;transform:rotate(-30deg);transform-origin:center}}
.wall img{{width:720px;height:450px;border-radius:14px;box-shadow:0 18px 40px rgba(0,0,0,.35)}}
</style><div class="wall">{cells}{cells}</div><div class="foot"><span class="chip">{FOOT}</span></div>"""


def slide6(c):
    fb = lambda r: "serif" if r.lower().startswith("head") else "sans-serif"  # py3.10-safe (no nested quotes in f-strings)
    fonts = "".join(f'<div class="fc"><div class="fn" style="font-family:\'{n}\',{fb(r)}">{n}</div><div class="fr">{r}</div></div>' for n, r in c["fonts"])
    sw = "".join(f'<div class="sw"><div class="sq" style="background:{h}"></div><div class="hx">{h.upper()}</div></div>' for h in c["palette"])
    tools = "".join(f'<span class="tool">{t}</span>' for t in c["tools"])
    fam = "&family=".join(n.replace(" ", "+") for n, _ in c["fonts"])  # css2 API wants repeated family=, not "|"
    # 2026-10-24: @import must be the first rule or the browser drops it
    # (fonts were rendering in a fallback serif, Manrope included).
    return f"""<style>@import url('https://fonts.googleapis.com/css2?family={fam}&display=swap');
{BASE_CSS}
body{{background:#0B0710;color:#fff}}
.glow{{position:absolute;width:900px;height:900px;left:-360px;top:-380px;border-radius:50%;background:radial-gradient(circle,rgba(255,149,0,.30),transparent 65%)}}
.glow2{{position:absolute;width:900px;height:900px;right:-380px;bottom:-360px;border-radius:50%;background:radial-gradient(circle,rgba(123,47,190,.45),transparent 65%)}}
.w{{position:absolute;left:64px;right:64px;top:60px}}
.t{{font-size:88px}}
.rule{{width:220px;height:7px;border-radius:4px;background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);margin:18px 0 26px}}
.k{{font-size:28px;font-weight:700;letter-spacing:3px;color:#FF9500;margin:0 0 16px}}
.row{{display:flex;gap:18px;margin-bottom:26px}}
.fc{{flex:1;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:20px 24px}}
.fn{{font-size:38px;white-space:nowrap}} .fr{{font-size:26px;color:rgba(255,255,255,.6);margin-top:4px}}
.sw{{flex:1}} .sq{{height:76px;border-radius:12px;border:1px solid rgba(255,255,255,.2)}} .hx{{font-size:26px;color:rgba(255,255,255,.7);margin-top:8px}}
.tool{{display:inline-block;font-size:30px;padding:10px 24px;border-radius:30px;border:1px solid rgba(255,255,255,.3);margin-right:12px}}
.div{{height:1px;background:rgba(255,255,255,.15);margin:0 0 22px}}
.ct{{font-size:76px;line-height:1.02;margin-bottom:12px}}  /* 2026-10-24: 88px wrapped to 3 lines and pushed the button onto the footer */
.cl{{font-size:40px;line-height:1.25;color:rgba(255,255,255,.75);margin-bottom:26px}}
.btn{{display:inline-block;font-size:34px;font-weight:700;padding:20px 40px;border-radius:50px;background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE)}}
.foot{{color:rgba(255,255,255,.55);bottom:30px}}
</style><div class="glow"></div><div class="glow2"></div>
<div class="w"><div class="h t">Project Snapshot</div><div class="rule"></div>
<div class="k">FONTS USED</div><div class="row">{fonts}</div>
<div class="k">COLOR PALETTE</div><div class="row">{sw}</div>
<div class="k">TOOLS USED</div><div style="margin-bottom:28px">{tools}</div>
<div class="div"></div>
<div class="h ct">{c['cta_title']}</div><div class="cl">{c['cta_line']}</div>
<span class="btn">{c['cta_url']}</span></div><div class="foot">{FOOT}</div>"""


def render(htmls, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for i, h in enumerate(htmls, 1):
            pg.set_content("<!doctype html><html><head><meta charset='utf-8'></head><body>" + h + "</body></html>")
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(600)
            pg.screenshot(path=os.path.join(out_dir, f"slide{i}.png"))
            print("saved", os.path.join(out_dir, f"slide{i}.png"))
        br.close()


def main(cfg_path):
    c = json.load(open(cfg_path))
    c.setdefault("accent_on_bg", c["accent"])
    c.setdefault("light_bg", "#F6F3EE")
    with tempfile.TemporaryDirectory() as tmp:
        secs = capture_sections(c["page"], c["hero_selector"], c["sections"], tmp)
        phones = phones_strip(c["mobile_shots"], tmp)
        full = Image.open(c["full_page_png"]).convert("RGB")
        full.thumbnail((1960, 2400))
        full_raw = Image.open(c["full_raw_png"]).convert("RGB")
        htmls = [slide1(c, secs[c["hero_selector"]]), slide2(c, full), slide3(c, phones),
                 slide4(c, [(l, secs[s]) for l, s in c["sections"]]), slide5(c, full_raw), slide6(c)]
        render(htmls, c["out_dir"])


if __name__ == "__main__":
    main(sys.argv[1])
