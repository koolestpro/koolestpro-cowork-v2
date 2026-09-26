import base64

root = "outputs/cro-fixes/caraway/_assets/"
logo_b64 = open(root+"logo_b64.txt").read().strip()
hero_b64 = open(root+"composite_b64.txt").read().strip()

logo_uri = f"data:image/svg+xml;base64,{logo_b64}"
hero_uri = f"data:image/jpeg;base64,{hero_b64}"

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fry Pan PDP — Caraway (CRO rebuild)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; font-family:'DM Sans',sans-serif; }}
  body {{ background:#E8E8E8; display:flex; justify-content:center; padding:0; }}
  .phone {{ width:390px; height:844px; background:#F7F5EF; position:relative; overflow:hidden; display:flex; flex-direction:column; }}

  /* FIX 1 — a live browsing session on this PDP surfaced a full-screen email-capture
     popup ("Save Up to $705") that blocks the entire page on load, with the close (X)
     as the only way through. That value proposition now lives in a slim, non-blocking
     top strip instead — always visible, never gates the page. */
  .promo {{ background:#1F2E27; color:#F7F5EF; text-align:center; font-size:11.5px; font-weight:600; padding:7px 14px; letter-spacing:.2px; }}

  .hdr {{ display:flex; align-items:center; justify-content:space-between; padding:10px 16px 8px; }}
  .hdr img.logo {{ height:20px; }}
  .hdr .ic {{ display:flex; gap:14px; align-items:center; }}
  .hdr svg {{ width:19px; height:19px; fill:none; stroke:#1F2E27; stroke-width:1.6; }}
  .hdr .cart {{ position:relative; }}
  .hdr .cart b {{ position:absolute; top:-6px; right:-7px; background:#B5482F; color:#fff; font-size:8px; width:14px; height:14px; border-radius:50%; display:flex; align-items:center; justify-content:center; }}

  /* FIX 2 (nav overflow) — condensed into one row that fully fits 390px with no clipped
     text and no invisible scroll trap. Category chips wrap to a visible second row instead
     of running off the right edge with zero affordance, as they do on the live page. */
  .catnav {{ display:flex; flex-wrap:wrap; gap:6px; padding:0 16px 10px; }}
  .chip {{ font-size:10.5px; font-weight:600; color:#1F2E27; background:#EAE6DB; border-radius:999px; padding:5px 10px; white-space:nowrap; }}
  .chip.hot {{ background:#B5482F; color:#fff; }}

  .crumb {{ font-size:11px; color:#8A8577; padding:0 16px; margin-top:2px; }}

  .top {{ padding:10px 16px 0; }}
  .badge {{ display:inline-flex; align-items:center; gap:5px; background:#EFE3C2; color:#6B5619; font-size:10.5px; font-weight:700; padding:4px 9px; border-radius:6px; margin-bottom:8px; }}

  /* FIX 3 (price placement) — price sits directly below the title, at display weight,
     matching this project's PDP layout rule. On the live page price is a small number
     floated to the top-right, aligned with the reviews line rather than the title
     directly above it — disconnected from the thing it's the price of. */
  h1 {{ font-size:19px; font-weight:700; color:#1F2E27; line-height:1.22; }}
  .price-row {{ display:flex; align-items:baseline; gap:8px; margin-top:6px; }}
  .price-row b {{ font-size:26px; font-weight:700; color:#1F2E27; }}

  /* FIX 4 (social proof) — star rating + real review count render inline and immediately,
     every time. On a live load of the real PDP the reviews widget can paint as bare text
     ("Reviews", no stars, no count) before its third-party script finishes — right next to
     the price, which is exactly where a shopper is deciding whether $125 is worth it. */
  .proof {{ display:flex; align-items:center; gap:6px; margin-top:6px; }}
  .stars {{ color:#C98A2C; font-size:13px; letter-spacing:1px; }}
  .proof span {{ color:#5B584F; font-size:12px; }}

  .pay4 {{ display:flex; align-items:center; gap:6px; margin-top:8px; font-size:12px; color:#5B584F; }}
  .pay4 .mark {{ background:#1F2E27; color:#fff; font-size:9.5px; font-weight:700; padding:2px 6px; border-radius:4px; letter-spacing:.3px; }}

  /* FIX 5 (above the fold) — the real product photo, background removed and composited
     onto a contrasting dark surface for a premium look, now fills the remaining space in
     the first viewport every time. On a live session the same photo can end up competing
     with a sweepstakes banner for vertical space and land past ~850px of scroll instead. */
  /* CORRECTED 2026-09-07 — object-fit:cover on this flex:1 (variable, tall) container was
     cropping/zooming the true 1100x950 (~1.16:1) photo hard, since the container's real
     rendered aspect (~390x440, ~0.89:1) is nowhere close to the source image's aspect. The
     result read as "not the same image" and "way bigger" — a bad crop, not a design choice.
     Fix: object-fit:contain shows the WHOLE photo undistorted; the dark surface (#17201B)
     letterboxes it, which reads as a deliberate premium plinth rather than empty space,
     matching the existing "composite on a contrasting dark background" rule. */
  .heroWrap {{ margin-top:12px; flex:1; min-height:0; border-radius:16px; overflow:hidden; position:relative; background:#17201B; display:flex; align-items:center; justify-content:center; }}
  .heroWrap img {{ width:100%; height:100%; object-fit:contain; object-position:center; display:block; }}
  .heroWrap .swatches {{ position:absolute; bottom:10px; left:0; right:0; display:flex; justify-content:center; gap:7px; }}
  .sw {{ width:16px; height:16px; border-radius:50%; border:2px solid rgba(255,255,255,.85); }}

  /* Sticky purchase bar — no dead space below it, fills to the bottom edge. */
  .sticky {{ background:#F7F5EF; border-top:1px solid #E2DFD3; padding:10px 16px 14px; }}
  .buy {{ display:flex; align-items:center; justify-content:space-between; gap:12px; }}
  .buy .pr b {{ font-size:16px; font-weight:700; color:#1F2E27; }}
  .buy .pr span {{ display:block; font-size:10.5px; color:#8A8577; }}
  .buy button {{ flex:1; max-width:220px; background:#1F2E27; color:#F7F5EF; border:none; border-radius:999px; padding:13px 20px; font-size:14px; font-weight:700; cursor:pointer; }}
</style>
</head>
<body>
<div class="phone">

  <div class="promo">Free Shipping on Orders $90+ &nbsp;|&nbsp; Free Returns &nbsp;|&nbsp; 30-Day Trial</div>

  <div class="hdr">
    <img class="logo" src="{logo_uri}" alt="Caraway Home">
    <div class="ic">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      <div class="cart">
        <svg viewBox="0 0 24 24"><path d="M6 6h15l-1.5 9h-12z"/><path d="M6 6L5 3H2"/><circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/></svg>
      </div>
    </div>
  </div>

  <div class="catnav">
    <div class="chip hot">Shop All</div>
    <div class="chip">Cookware</div>
    <div class="chip">Bakeware</div>
    <div class="chip">Storage</div>
    <div class="chip">Kitchen Tools</div>
  </div>

  <div class="crumb">Shop All / Cookware / Fry Pan</div>

  <div class="top">
    <div class="badge">TOP GIFT</div>
    <h1>Fry Pan — 10.5&quot; Non-Stick Ceramic Fry Pan</h1>

    <div class="price-row">
      <b>$125</b>
    </div>

    <div class="proof">
      <span class="stars">★★★★★</span>
      <span>18,886 Reviews</span>
    </div>

    <div class="pay4">
      <span class="mark">Shop Pay</span>
      <span>4 interest-free payments of $32</span>
    </div>
  </div>

  <div class="heroWrap">
    <img src="{hero_uri}" alt="Caraway Ceramic Fry Pan, Cream">
    <div class="swatches">
      <div class="sw" style="background:#EFE7D6"></div>
      <div class="sw" style="background:#2C3E50"></div>
      <div class="sw" style="background:#8A8577"></div>
      <div class="sw" style="background:#C2A15A"></div>
    </div>
  </div>

  <div class="sticky">
    <div class="buy">
      <div class="pr">
        <b>$125</b>
        <span>10.5&quot; · Cream</span>
      </div>
      <button>Add to Cart</button>
    </div>
  </div>

</div>
</body>
</html>
"""

open("outputs/cro-fixes/caraway_fry-pan-pdp_rebuild.html","w").write(html)
print("written", len(html), "bytes")
