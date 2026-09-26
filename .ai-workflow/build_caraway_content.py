import base64

A = "outputs/cro-fixes/caraway/_assets/"

def uri(name, mime):
    return f"data:{mime};base64," + open(A+name+".b64").read().strip()

logo_uri   = "data:image/svg+xml;base64," + open(A+"logo_b64.txt").read().strip()
hero_uri   = uri("hero_composite.jpg", "image/jpeg")
ba_uri     = uri("ba-graphic.png", "image/png")
anno_uri   = uri("anno-graphic.png", "image/png")
after_uri  = uri("after_raw.png", "image/png")
before_uri = uri("before_popup3.png", "image/png")

POST_SLUG = "caraway_fry-pan-pdp"
POST_BRAND = "Caraway"

# ---------------------------------------------------------------------------
# CONTEXTUAL ICONS (2026-09-07 correction) — real Iconify SVGs, fetched once,
# inlined as raw path data. Never generic/templated: each icon is chosen for
# what that specific slide's finding actually is (a false-claim seal for the
# myth, a verified checkmark for the reality, a numbered-list icon for the
# repeatable pattern, a star for the review/trust signal, a price tag for
# the price-placement fix). Reused at multiple sizes/opacities/colors below.
# ---------------------------------------------------------------------------
MYTH_PATH = "M225.86 102.82c-3.77-3.94-7.67-8-9.14-11.57c-1.36-3.27-1.44-8.69-1.52-13.94c-.15-9.76-.31-20.82-8-28.51s-18.75-7.85-28.51-8c-5.25-.08-10.67-.16-13.94-1.52c-3.56-1.47-7.63-5.37-11.57-9.14C146.28 23.51 138.44 16 128 16s-18.27 7.51-25.18 14.14c-3.94 3.77-8 7.67-11.57 9.14c-3.25 1.36-8.69 1.44-13.94 1.52c-9.76.15-20.82.31-28.51 8s-7.8 18.75-8 28.51c-.08 5.25-.16 10.67-1.52 13.94c-1.47 3.56-5.37 7.63-9.14 11.57C23.51 109.72 16 117.56 16 128s7.51 18.27 14.14 25.18c3.77 3.94 7.67 8 9.14 11.57c1.36 3.27 1.44 8.69 1.52 13.94c.15 9.76.31 20.82 8 28.51s18.75 7.85 28.51 8c5.25.08 10.67.16 13.94 1.52c3.56 1.47 7.63 5.37 11.57 9.14c6.9 6.63 14.74 14.14 25.18 14.14s18.27-7.51 25.18-14.14c3.94-3.77 8-7.67 11.57-9.14c3.27-1.36 8.69-1.44 13.94-1.52c9.76-.15 20.82-.31 28.51-8s7.85-18.75 8-28.51c.08-5.25.16-10.67 1.52-13.94c1.47-3.56 5.37-7.63 9.14-11.57c6.63-6.9 14.14-14.74 14.14-25.18s-7.51-18.27-14.14-25.18M120 80a8 8 0 0 1 16 0v56a8 8 0 0 1-16 0Zm8 104a12 12 0 1 1 12-12a12 12 0 0 1-12 12"
REALITY_PATH = "M128 24a104 104 0 1 0 104 104A104.11 104.11 0 0 0 128 24m45.66 85.66l-56 56a8 8 0 0 1-11.32 0l-24-24a8 8 0 0 1 11.32-11.32L112 148.69l50.34-50.35a8 8 0 0 1 11.32 11.32"
PATTERN_PATH = "M208 32H48a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16M56.84 75.58a8 8 0 0 1 3.58-10.74l16-8A8 8 0 0 1 88 64v48a8 8 0 0 1-16 0V76.94l-4.42 2.22a8 8 0 0 1-10.74-3.58M92 180a8 8 0 0 1 0 16H68a8 8 0 0 1-6.4-12.8l21.67-28.89A3.92 3.92 0 0 0 84 152a4 4 0 0 0-7.77-1.33a8 8 0 0 1-15.09-5.34a20 20 0 1 1 35 18.53L84 180Zm100 4h-72a8 8 0 0 1 0-16h72a8 8 0 0 1 0 16m0-48h-72a8 8 0 0 1 0-16h72a8 8 0 0 1 0 16m0-48h-72a8 8 0 0 1 0-16h72a8 8 0 0 1 0 16"
STAR_PATH = "m234.29 114.85l-45 38.83L203 211.75a16.4 16.4 0 0 1-24.5 17.82L128 198.49l-50.53 31.08A16.4 16.4 0 0 1 53 211.75l13.76-58.07l-45-38.83a16.46 16.46 0 0 1 9.42-28.86l59.36-5.08l23.13-55.34a16.36 16.36 0 0 1 30.2 0l23.11 55.34l59.36 5.08a16.46 16.46 0 0 1 9.4 28.86Z"
TAG_PATH = "M243.31 136L144 36.69A15.86 15.86 0 0 0 132.69 32H40a8 8 0 0 0-8 8v92.69A15.86 15.86 0 0 0 36.69 144L136 243.31a16 16 0 0 0 22.63 0l84.68-84.68a16 16 0 0 0 0-22.63M84 96a12 12 0 1 1 12-12a12 12 0 0 1-12 12"

def icon(path, size, color, opacity=1):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 256 256" '
            f'style="opacity:{opacity};flex-shrink:0;display:block;"><path fill="{color}" d="{path}"/></svg>')

RIDWAN_AVATAR_SMILE = "https://res.cloudinary.com/drl0rscuf/image/upload/f_png,q_auto/avatar-circle-smile_esjvt2"

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Caraway Fry Pan CRO Fix — Content Pack</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300;1,400&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<style>
  * { box-sizing:border-box; }
  body { background:#0e0e0e; color:#fff; font-family:'DM Mono',monospace; padding:40px 20px 80px; margin:0; }
  .section-label { text-align:center; font-size:11px; letter-spacing:3px; text-transform:uppercase; color:rgba(255,255,255,0.3); margin:50px 0 14px; }
  .section-divider { height:1px; background:rgba(255,255,255,0.08); max-width:588px; margin:0 auto; }

  .lk-frame { max-width:588px; margin:0 auto; background:#1a1a1a; border-radius:14px; overflow:hidden; border:1px solid rgba(255,255,255,0.08); }
  .lk-header { display:flex; align-items:flex-start; gap:10px; padding:14px 16px 10px; }
  .lk-av { width:42px; height:42px; border-radius:50%; overflow:hidden; flex-shrink:0; background:#222; }
  .lk-name { font-family:'Syne',sans-serif; font-weight:700; font-size:14px; color:#fff; }
  .lk-sub { font-size:11px; color:rgba(255,255,255,0.4); margin-top:2px; }

  #viewport { width:540px; height:680px; overflow:hidden; position:relative; margin:0 auto; background:#080808; cursor:grab; }
  #track { display:flex; transition:transform 0.32s cubic-bezier(0.4,0,0.2,1); will-change:transform; }
  .slide { width:540px; height:680px; flex-shrink:0; position:relative; overflow:hidden; font-family:'DM Mono',monospace; }
  .dotgrid { position:absolute; inset:0; background-image:radial-gradient(rgba(255,255,255,0.03) 1px,transparent 1px); background-size:24px 24px; }
  .accentbar { position:absolute; top:0; left:0; right:0; height:3px; background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE); }
  .counter { position:absolute; left:24px; bottom:20px; font-size:10px; color:rgba(255,255,255,0.55); background:rgba(0,0,0,0.4); padding:3px 8px; border-radius:5px; z-index:10; }
  .handle { position:absolute; right:24px; bottom:20px; font-size:9px; color:rgba(255,255,255,0.5); background:rgba(0,0,0,0.4); padding:3px 8px; border-radius:5px; z-index:10; }
  .swb { position:absolute; right:0; top:50%; transform:translateY(-50%); width:32px; height:80px; display:flex; align-items:center; justify-content:center; color:rgba(255,255,255,0.35); font-size:22px; cursor:pointer; z-index:20; background:linear-gradient(to right,transparent,rgba(0,0,0,0.25)); user-select:none; }
  .glow { position:absolute; border-radius:50%; filter:blur(70px); pointer-events:none; }

  .eyebrow { display:inline-flex; align-items:center; gap:6px; border:1px solid rgba(255,149,0,0.4); color:#FF9500; font-size:10px; letter-spacing:2px; text-transform:uppercase; padding:5px 12px; border-radius:999px; }
  .headline { font-family:'Syne',sans-serif; font-weight:800; line-height:1.08; color:#fff; }
  .body-copy { font-family:'DM Mono',monospace; font-size:15px; line-height:1.7; color:rgba(255,255,255,0.55); }

  #dots { display:flex; justify-content:center; gap:6px; padding:12px 0; }
  .dot { width:6px; height:6px; border-radius:50%; background:rgba(255,255,255,0.18); cursor:pointer; }
  .dot.active { background:#FF9500; width:20px; border-radius:3px; }
  #pager { text-align:center; font-size:11px; color:rgba(255,255,255,0.28); padding-bottom:10px; }

  #download-panel { max-width:588px; margin:16px auto 0; text-align:center; }
  #download-panel button { background:#1a1a1a; border:1px solid rgba(255,255,255,0.12); color:#fff; font-family:'DM Mono',monospace; font-size:12px; padding:10px 16px; border-radius:8px; margin:4px; cursor:pointer; }
  #download-status { font-size:11px; color:rgba(255,255,255,0.4); margin-top:8px; min-height:16px; }

  .gcard-wrap { max-width:588px; margin:0 auto; }
  .gcard { width:100%; border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,0.08); }
  .gcard img { width:100%; display:block; }

  .tabs-wrap { max-width:588px; margin:0 auto; }
  .tab-buttons { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px; }
  .tab-btn { background:#151515; border:1px solid rgba(255,255,255,0.1); color:rgba(255,255,255,0.6); font-family:'DM Mono',monospace; font-size:11px; padding:8px 12px; border-radius:8px; cursor:pointer; }
  .tab-btn.active { background:#FF9500; color:#0e0e0e; border-color:#FF9500; }
  .tab-panel { display:none; background:#141414; border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:16px; }
  .tab-panel.active { display:block; }
  .tab-panel pre { white-space:pre-wrap; font-family:'DM Mono',monospace; font-size:13px; color:rgba(255,255,255,0.8); line-height:1.6; margin:0 0 10px; }
  .tab-panel button { background:rgba(255,149,0,0.15); border:1px solid rgba(255,149,0,0.4); color:#FF9500; font-family:'DM Mono',monospace; font-size:11px; padding:6px 12px; border-radius:6px; cursor:pointer; }
</style>
</head>
<body>

<div class="section-label">Section 1 — LinkedIn Carousel Preview</div>
<div class="lk-frame">
  <div class="lk-header" data-chrome>
    <div class="lk-av"><img src="__LOGO__" style="width:70%;height:70%;object-fit:contain;margin:15%;" onerror="this.style.display='none'"></div>
    <div>
      <div class="lk-name">Koolestpro</div>
      <div class="lk-sub">CRO teardown &middot; Product Page (PDP) &middot; Caraway Fry Pan</div>
    </div>
  </div>
  <div id="viewport">
    <div id="track">

      <!-- SLIDE 1 — COVER -->
      <div class="slide" style="background:#080808;">
        <div class="dotgrid"></div>
        <div class="accentbar"></div>
        <div class="glow" style="width:340px;height:340px;background:radial-gradient(circle,rgba(255,149,0,0.22),transparent 70%);top:-80px;right:-100px;"></div>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;">
          <div style="padding:32px 32px 0;display:flex;flex-wrap:wrap;gap:8px;">
            <span class="eyebrow">CRO FIX &middot; CARAWAY</span>
            <span class="eyebrow" style="border-color:rgba(255,255,255,0.28);color:rgba(255,255,255,0.75);">PRODUCT PAGE (PDP)</span>
          </div>
          <div style="padding:16px 32px 0;">
            <div class="headline" style="font-size:38px;">You think a $125 pan sells itself.<br><span style="color:#FF9500;">It doesn't.</span></div>
          </div>
          <div style="flex:1;margin:18px 28px 0;border-radius:16px;overflow:hidden;background:#111;">
            <img src="__AFTER__" style="width:100%;height:100%;object-fit:cover;object-position:top;">
          </div>
          <div style="padding:16px 32px 22px;text-align:center;font-size:11px;color:rgba(255,255,255,0.35);">SWIPE &rarr;</div>
        </div>
        <div class="counter">1 / 7</div>
        <div class="handle">@koolestpro</div>
        <div class="swb" data-chrome onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 2 — MYTH (redesigned 2026-09-07: full-frame, big redundant badge, contextual icon, no dead space) -->
      <div class="slide" style="background:#0c0c0c;">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:#3b82f6;"></div>
        <div style="position:absolute;right:-50px;top:-40px;">__MYTH_ICON_BIG__</div>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;">
          <div style="padding:40px 32px 0;">
            <div style="display:inline-flex;align-items:center;gap:10px;background:rgba(59,130,246,0.16);border:2px solid #3b82f6;border-radius:999px;padding:10px 20px;">
              __MYTH_ICON_SM__
              <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:22px;letter-spacing:1px;text-transform:uppercase;color:#3b82f6;">Myth</span>
            </div>
            <div class="headline" style="font-size:32px;margin-top:22px;">&ldquo;18,886 reviews means the trust is already there.&rdquo;</div>
            <div class="body-copy" style="margin-top:16px;">On a live load, that trust signal can render as the bare word &ldquo;Reviews&rdquo;, with no stars and no count, right next to the price, exactly when a shopper is deciding if $125 is worth it.</div>
          </div>
          <div style="flex:1;margin:24px 32px 32px;border-radius:16px;background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.3);display:flex;align-items:center;gap:18px;padding:0 26px;">
            __STAR_ICON_BLUE__
            <div style="font-family:'DM Mono',monospace;font-size:14px;line-height:1.6;color:rgba(255,255,255,0.75);">18,886 real reviews exist on this page. The problem was never proof. It was timing.</div>
          </div>
        </div>
        <div class="counter">2 / 7</div>
        <div class="handle">@koolestpro</div>
        <div class="swb" data-chrome onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 3 — REALITY (redesigned 2026-09-07) -->
      <div class="slide" style="background:#0c0c0c;">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:#22c55e;"></div>
        <div style="position:absolute;right:-50px;top:-40px;">__REALITY_ICON_BIG__</div>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;">
          <div style="padding:40px 32px 0;">
            <div style="display:inline-flex;align-items:center;gap:10px;background:rgba(34,197,94,0.16);border:2px solid #22c55e;border-radius:999px;padding:10px 20px;">
              __REALITY_ICON_SM__
              <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:22px;letter-spacing:1px;text-transform:uppercase;color:#22c55e;">Reality</span>
            </div>
            <div class="headline" style="font-size:32px;margin-top:22px;">Price, stars, and photo have to land in ONE glance.</div>
            <div class="body-copy" style="margin-top:16px;">Not a scroll. Not a widget that loads late. Fix the order those three things appear in, and the rest of the page has an easier job.</div>
          </div>
          <div style="flex:1;margin:24px 32px 32px;border-radius:16px;background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.3);display:flex;align-items:center;gap:18px;padding:0 26px;">
            __TAG_ICON_GREEN__
            <div style="font-family:'DM Mono',monospace;font-size:14px;line-height:1.6;color:rgba(255,255,255,0.75);">Price now sits directly under the title, at display size, every single load.</div>
          </div>
        </div>
        <div class="counter">3 / 7</div>
        <div class="handle">@koolestpro</div>
        <div class="swb" data-chrome onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 4 — EVIDENCE: BEFORE/AFTER (fixed 2026-09-07: flex:1 now sits inside a real
           flex column so the image container actually fills to the bottom edge, no dead band) -->
      <div class="slide" style="background:#080808;">
        <div class="dotgrid"></div>
        <div class="accentbar"></div>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;">
          <div style="padding:30px 24px 0;display:flex;flex-wrap:wrap;gap:8px;">
            <span class="eyebrow">EVIDENCE</span>
            <span class="eyebrow" style="border-color:rgba(255,255,255,0.28);color:rgba(255,255,255,0.75);">PRODUCT PAGE (PDP)</span>
          </div>
          <div style="padding:12px 24px 0;">
            <div class="headline" style="font-size:24px;">Price &amp; proof, reconnected.</div>
          </div>
          <div style="margin:16px 24px 24px;border-radius:12px;overflow:hidden;flex:1;min-height:0;">
            <img src="__BA__" style="width:100%;height:100%;object-fit:cover;object-position:top;">
          </div>
        </div>
        <div class="counter">4 / 7</div>
        <div class="handle">@koolestpro</div>
        <div class="swb" data-chrome onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 5 — EVIDENCE: ANNOTATED (same flex-column fix as slide 4) -->
      <div class="slide" style="background:#080808;">
        <div class="dotgrid"></div>
        <div class="accentbar"></div>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;">
          <div style="padding:30px 24px 0;display:flex;flex-wrap:wrap;gap:8px;">
            <span class="eyebrow">EVIDENCE</span>
            <span class="eyebrow" style="border-color:rgba(255,255,255,0.28);color:rgba(255,255,255,0.75);">PRODUCT PAGE (PDP)</span>
          </div>
          <div style="padding:12px 24px 0;">
            <div class="headline" style="font-size:24px;">What actually changed, named.</div>
          </div>
          <div style="margin:16px 24px 24px;border-radius:12px;overflow:hidden;flex:1;min-height:0;background:#f7f5ef;">
            <img src="__ANNO__" style="width:100%;height:100%;object-fit:cover;object-position:top;">
          </div>
        </div>
        <div class="counter">5 / 7</div>
        <div class="handle">@koolestpro</div>
        <div class="swb" data-chrome onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 6 — FRAMEWORK TAKEAWAY (redesigned 2026-09-07: pattern baked into a large mini-diagram, not just a tiny label) -->
      <div class="slide" style="background:#0c0c0c;">
        <div class="dotgrid"></div>
        <div class="accentbar" style="background:#E040A0;"></div>
        <div style="position:absolute;right:-50px;top:-40px;">__PATTERN_ICON_BIG__</div>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;">
          <div style="padding:40px 32px 0;">
            <div style="display:inline-flex;align-items:center;gap:10px;background:rgba(224,64,160,0.16);border:2px solid #E040A0;border-radius:999px;padding:10px 20px;">
              __PATTERN_ICON_SM__
              <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:22px;letter-spacing:1px;text-transform:uppercase;color:#E040A0;">The Pattern</span>
            </div>
            <div class="headline" style="font-size:30px;margin-top:22px;">Title. Price. Proof. In that order, touching.</div>
            <div class="body-copy" style="margin-top:16px;">If a shopper has to look in three different places to answer &ldquo;what is it, what does it cost, can I trust it,&rdquo; that gap is where they leave.</div>
          </div>
          <div style="flex:1;margin:24px 32px 32px;border-radius:16px;background:rgba(224,64,160,0.08);border:1px solid rgba(224,64,160,0.3);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:20px;">
            <div style="display:flex;align-items:center;gap:10px;font-family:'Syne',sans-serif;font-weight:800;font-size:22px;color:#fff;">
              <span>Title</span><span style="color:#E040A0;">&rarr;</span><span>Price</span><span style="color:#E040A0;">&rarr;</span><span>Proof</span>
            </div>
            <div style="font-family:'DM Mono',monospace;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.45);">touching, in that order, every load</div>
          </div>
        </div>
        <div class="counter">6 / 7</div>
        <div class="handle">@koolestpro</div>
        <div class="swb" data-chrome onclick="goTo(current+1)">&rsaquo;</div>
      </div>

      <!-- SLIDE 7 — CTA (fixed 2026-09-07: real Cloudinary avatar, not an empty placeholder) -->
      <div class="slide" style="background:#080808;">
        <div class="dotgrid"></div>
        <div class="accentbar"></div>
        <div class="glow" style="width:300px;height:300px;background:radial-gradient(circle,rgba(255,149,0,0.2),transparent 70%);bottom:-80px;left:-80px;"></div>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 40px;">
          <div style="width:180px;height:180px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,149,0,0.4);flex-shrink:0;margin-bottom:20px;">
            <img src="__AVATAR__" style="width:100%;height:100%;object-fit:cover;object-position:center top;" onerror="this.style.display='none'">
          </div>
          <div class="headline" style="font-size:28px;">This is one page. Yours has one too.</div>
          <div class="body-copy" style="margin-top:12px;font-size:14px;">Free CRO teardown, one Product Page (PDP), real screenshots. DM &ldquo;FIX&rdquo; if you want yours.</div>
          <div style="margin-top:24px;padding:12px 28px;border-radius:999px;background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);font-family:'Syne',sans-serif;font-weight:700;font-size:14px;color:#fff;">Repost if this is useful &rarr;</div>
        </div>
        <div class="counter">7 / 7</div>
        <div class="handle">@koolestpro</div>
      </div>

    </div>
  </div>
  <div id="dots" data-chrome></div>
  <div id="pager" data-chrome>1 / 7</div>
</div>

<div id="download-panel">
  <button onclick="dlAll()">Download All Slides</button>
  <button onclick="dlPDF()">Download PDF</button>
  <div id="download-status" aria-live="polite"></div>
</div>

<div class="section-label">Section 2 — Individual Graphic Cards</div>
<div class="section-divider"></div>
<div class="posts-shell" style="max-width:588px;margin:20px auto 0;display:flex;flex-direction:column;gap:16px;">
  <div class="gcard-wrap">
    <div id="ba-graphic" class="gcard"><img src="__BA__"></div>
  </div>
  <div class="gcard-wrap">
    <div id="anno-graphic" class="gcard"><img src="__ANNO__"></div>
  </div>
</div>

<div class="section-label">Section 3 — Post Copy</div>
<div class="section-divider"></div>
<div class="tabs-wrap" style="margin-top:16px;">
  <div class="tab-buttons">
    <button class="tab-btn active" onclick="openTab(this,'tab-linkedin')">LinkedIn</button>
    <button class="tab-btn" onclick="openTab(this,'tab-ig')">Instagram</button>
    <button class="tab-btn" onclick="openTab(this,'tab-hook')">Hook Variations</button>
    <button class="tab-btn" onclick="openTab(this,'tab-twitter-angles')">Twitter Angles</button>
    <button class="tab-btn" onclick="openTab(this,'tab-twitter-thread')">Twitter Thread</button>
  </div>

  <div id="tab-linkedin" class="tab-panel active">
<pre>Product Page (PDP) audit: Caraway's Fry Pan, on mobile.

You think 18,886 reviews means the trust is already there.

It doesn't, if the page can't render them in time.

Real findings, nothing invented:

The price sits top-right, aligned with the review line, disconnected from the title above it. On a fresh load, that review line can paint as the bare word "Reviews" with no stars and no count, right next to the price, exactly when a shopper is deciding if $125 is worth it. And depending on what's loaded above it, the product photo itself can land past the fold.

The rebuild moves price directly under the title, renders stars and count inline every time, and gives the real product photo (background removed, composited on a dark surface) the whole first screen.

Same product. Same price. The only thing that changed is the order the page tells its own story in.

Full before/after and annotated breakdown in the carousel.

Repost if this is useful to someone building a product page right now.</pre>
    <button onclick="copyText('tab-linkedin')">Copy</button>
  </div>

  <div id="tab-ig" class="tab-panel">
<pre>Product Page (PDP) audit: Caraway's $125 fry pan has 18,886 reviews.

On a live load, that trust signal can render as just the word "Reviews," with no stars and no count, right next to the price.

Price also sits disconnected from the title, and the real product photo can miss the first screen entirely.

Swipe for the real before/after. Rebuild puts price under the title, stars + count inline always, and the photo front and center.

Save this if you're auditing your own PDP this week.</pre>
    <button onclick="copyText('tab-ig')">Copy</button>
  </div>

  <div id="tab-hook" class="tab-panel">
<pre>1. You think 18,886 reviews means the trust is already there. It doesn't.
2. A $125 pan with 5 stars can still show up looking unsure of itself.
3. Same fry pan, same product page. The only thing that changed is the order it tells its story in.
4. Price, stars, and photo have to land in ONE glance, not a scroll.</pre>
    <button onclick="copyText('tab-hook')">Copy</button>
  </div>

  <div id="tab-twitter-angles" class="tab-panel">
<pre>[1/3] Product Page (PDP) audit: Caraway's Fry Pan. Price sits top-right, disconnected from the title. Moved it directly underneath at display size. Small change, but now the eye doesn't have to jump.

[2/3] On a live load, the review line can paint as literal text "Reviews," no stars, no count. 18,886 real reviews exist. The fix: never let the number that matters most render empty.

[3/3] Real product photo, background removed, composited dark. Now fills the whole first screen instead of competing with a sweepstakes banner for space.</pre>
    <button onclick="copyText('tab-twitter-angles')">Copy</button>
  </div>

  <div id="tab-twitter-thread" class="tab-panel">
<pre>Audited a $125 product page (PDP). The trust signal wasn't the problem. The timing of it was.

Here's what a live load actually showed, and what I changed:

1/ Price sat top-right, aligned with the review count line. Title sat top-left, two lines up. Your eye has to jump sideways to connect "what is this" to "what does it cost."

2/ The review line (18,886 real reviews) rendered as the bare word "Reviews" on a fresh load. No stars. No count. Right where a shopper decides if $125 is worth it.

3/ The product photo itself can end up past the fold, competing with a sweepstakes banner for the same vertical space.

None of this is a "redesign." It's sequencing: title, price, proof, photo, in that order, touching each other, every time the page loads.

Real screenshots, real before/after in the graphic below.</pre>
    <button onclick="copyText('tab-twitter-thread')">Copy</button>
  </div>
</div>

<!-- PIPELINE EXPORT -->
<div style="max-width:600px;margin:30px auto 0;padding:0 20px 60px;">
<div style="background:#0a0a0a;border:1px solid rgba(255,149,0,0.2);border-radius:12px;padding:24px;">
  <div style="font-family:'DM Mono',monospace;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FF9500;margin-bottom:8px;">Content Pipeline</div>
  <div style="font-family:'DM Mono',monospace;font-size:11px;color:rgba(255,255,255,0.45);line-height:1.7;margin-bottom:18px;">Export this post to the content system. Downloads a <code>.json</code> file, then open <code>ridwan_content_system_updated.html</code> and sync to register it.</div>
  <button onclick="sendToPipeline()" style="background:linear-gradient(90deg,#FF9500,#E040A0,#7B2FBE);color:#fff;font-family:'Syne',sans-serif;font-weight:700;font-size:13px;padding:12px 28px;border:none;border-radius:8px;cursor:pointer;letter-spacing:0.5px;">Send to Content Pipeline &rarr;</button>
  <div id="pipeline-status" style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(255,255,255,0.35);margin-top:12px;min-height:16px;"></div>
</div>
</div>

<script>
const POST_BRAND  = 'Caraway';
const POST_SLUG   = 'caraway_fry-pan-pdp';
const POST_TYPE   = 'CRO Fix';
const POST_FOLDER = 'outputs/cro-fixes/' + POST_SLUG + '_content.html';
const TOTAL = 7;
let current = 0;
const track = document.getElementById('track');
const slides = document.querySelectorAll('.slide');
const dotsWrap = document.getElementById('dots');
for (let i=0;i<TOTAL;i++){
  const d = document.createElement('div');
  d.className = 'dot' + (i===0?' active':'');
  d.onclick = () => goTo(i);
  dotsWrap.appendChild(d);
}
function goTo(i){
  current = Math.max(0, Math.min(TOTAL-1, i));
  track.style.transform = `translateX(-${current*540}px)`;
  document.querySelectorAll('.dot').forEach((d,idx)=>d.classList.toggle('active', idx===current));
  document.getElementById('pager').textContent = `${current+1} / ${TOTAL}`;
}

async function waitForSlideAssets(slide) {
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
  const images = Array.from(slide.querySelectorAll('img'));
  await Promise.all(images.map(img => {
    if (img.complete && img.naturalWidth > 0) return Promise.resolve();
    if (img.decode) return img.decode().catch(() => {});
    return new Promise(resolve => { img.onload = resolve; img.onerror = resolve; });
  }));
}

async function captureSlide(idx) {
  const slide = slides[idx];
  if (!slide) throw new Error(`Slide ${idx + 1} was not found.`);
  const toHide = document.querySelectorAll('[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap');
  toHide.forEach(el => el.style.visibility = 'hidden');
  const prevTransform = track.style.transform;
  const prevTransition = track.style.transition;
  track.style.transform = `translateX(-${idx * 540}px)`;
  track.style.transition = 'none';
  try {
    await waitForSlideAssets(slide);
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    return await html2canvas(slide, { scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#080808', logging: false });
  } finally {
    track.style.transform = prevTransform;
    track.style.transition = prevTransition;
    toHide.forEach(el => el.style.visibility = '');
  }
}

async function captureFixed(id) {
  const el = document.getElementById(id);
  await waitForSlideAssets(el);
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  return await html2canvas(el, { scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#0e0e0e', logging: false });
}

function setDownloadStatus(message) {
  const status = document.getElementById('download-status');
  if (status) status.textContent = message || '';
}

async function dlSlide(idx) {
  try {
    setDownloadStatus(`Preparing slide ${idx + 1}...`);
    const canvas = await captureSlide(idx);
    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    a.download = `koolestpro_${POST_SLUG}_slide${idx + 1}.png`;
    a.click();
    setDownloadStatus(`Slide ${idx + 1} downloaded.`);
  } catch (err) {
    console.error(err);
    setDownloadStatus(`Slide ${idx + 1} failed: ${err.message}`);
  }
}

async function dlAll() {
  for (let i = 0; i < TOTAL; i++) {
    await dlSlide(i);
    await new Promise(r => setTimeout(r, 300));
  }
}

async function dlPDF() {
  try {
    if (!window.jspdf || !window.jspdf.jsPDF) throw new Error('PDF library did not load.');
    if (!window.html2canvas) throw new Error('Canvas library did not load.');
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'px', format: [540, 680], compress: true });
    for (let i = 0; i < TOTAL; i++) {
      setDownloadStatus(`Adding slide ${i + 1} of ${TOTAL} to PDF...`);
      const canvas = await captureSlide(i);
      if (i > 0) pdf.addPage([540, 680], 'portrait');
      pdf.addImage(canvas.toDataURL('image/jpeg', 0.92), 'JPEG', 0, 0, 540, 680);
    }
    setDownloadStatus('Saving PDF...');
    pdf.save(`koolestpro_${POST_SLUG}.pdf`);
    setDownloadStatus('PDF downloaded.');
  } catch (err) {
    console.error(err);
    setDownloadStatus(`PDF failed: ${err.message}`);
  }
}

function openTab(el, id) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  el.classList.add('active');
  document.getElementById(id).classList.add('active');
}
function copyText(id) {
  const text = document.getElementById(id).querySelector('pre').innerText;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector(`[onclick="copyText('${id}')"]`);
    if (btn) { btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = 'Copy', 1800); }
  });
}

function sendToPipeline() {
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const data = {
    id:        POST_TYPE.toLowerCase().replace(/\\s+/g,'-') + '-' + POST_SLUG + '-' + dateStr,
    type:      POST_TYPE,
    title:     'Caraway Fry Pan Product Page (PDP): Price & Proof, Reconnected',
    slug:      POST_SLUG,
    status:    'Created',
    day:       '',
    created:   now.toISOString(),
    folder:    POST_FOLDER,
    week:      'Week of ' + now.toLocaleDateString('en-US', { month: 'long', day: 'numeric' }),
    month:     now.toLocaleDateString('en-US', { month: 'long', year: 'numeric' }),
    monthSlug: now.toISOString().slice(0, 7)
  };
  console.log('EXPORT_POST_JSON', JSON.stringify(data));
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = POST_SLUG + '_pipeline.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
  const s = document.getElementById('pipeline-status');
  if (s) s.textContent = '\\u2713 Exported \\u2014 open ridwan_content_system_updated.html and sync.';
}
</script>
</body>
</html>
"""

html = (html
    .replace("__LOGO__", logo_uri)
    .replace("__AFTER__", after_uri)
    .replace("__BEFORE__", before_uri)
    .replace("__BA__", ba_uri)
    .replace("__ANNO__", anno_uri)
    .replace("__AVATAR__", RIDWAN_AVATAR_SMILE)
    .replace("__MYTH_ICON_BIG__", icon(MYTH_PATH, 320, "#3b82f6", 0.10))
    .replace("__MYTH_ICON_SM__", icon(MYTH_PATH, 26, "#3b82f6"))
    .replace("__REALITY_ICON_BIG__", icon(REALITY_PATH, 320, "#22c55e", 0.10))
    .replace("__REALITY_ICON_SM__", icon(REALITY_PATH, 26, "#22c55e"))
    .replace("__PATTERN_ICON_BIG__", icon(PATTERN_PATH, 320, "#E040A0", 0.10))
    .replace("__PATTERN_ICON_SM__", icon(PATTERN_PATH, 26, "#E040A0"))
    .replace("__STAR_ICON_BLUE__", icon(STAR_PATH, 44, "#3b82f6"))
    .replace("__TAG_ICON_GREEN__", icon(TAG_PATH, 44, "#22c55e"))
)

open("outputs/cro-fixes/caraway_fry-pan-pdp_content.html","w").write(html)
print("content.html written", len(html))
