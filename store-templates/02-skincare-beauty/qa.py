#!/usr/bin/env python3
"""
QA harness for this template. Drives real Chromium against all three pages at
desktop and mobile, exercises every interactive control, and reports anything
broken. Run it before calling a build or a reskin done.

  export LD_LIBRARY_PATH=/tmp/pw_libs/extracted/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH
  python3 qa.py [--shots-dir DIR]
"""
import argparse, os, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent.resolve()
PAGES = [("home", "index.html"), ("collection", "collection.html"), ("product", "product.html?id=lum-serum")]
VIEWPORTS = [("desktop", 1440, 900), ("mobile", 390, 844)]
IGNORE = ("favicon",)
# Third-party hosts. A blip here is an environment problem, not a template bug,
# so it is reported separately instead of failing the run.
THIRD_PARTY = ("fonts.googleapis.com", "fonts.gstatic.com", "cdnjs.cloudflare.com", "cdn.jsdelivr.net")

fails, notes, warns = [], [], []
VENDOR = None


def check(cond, msg):
    (notes if cond else fails).append(("PASS " if cond else "FAIL ") + msg)


def walk(pg):
    """Scroll top to bottom in viewport steps, then back up. Fires every
    ScrollTrigger and forces every loading=lazy image to actually fetch, so
    the checks that follow see the finished page rather than the first fold."""
    prev, same = -1, 0
    for _ in range(80):
        pg.evaluate("window.scrollBy(0, Math.round(innerHeight * 0.8))")
        pg.wait_for_timeout(160)
        y = pg.evaluate("() => Math.round(window.scrollY)")
        same = same + 1 if y == prev else 0
        if same >= 2:
            break
        prev = y
    pg.wait_for_timeout(900)


def audit(pw, name, path, label, w, h, shots):
    tag = f"{label}/{name}"
    br = pw.chromium.launch()
    ctx = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=1,
                         is_mobile=(label == "mobile"), has_touch=(label == "mobile"))
    pg = ctx.new_page()

    # Serve GSAP/Lenis/fonts from a local vendor dir when asked, so a CDN
    # outage cannot turn into a false failure. Same bytes, no network.
    if VENDOR:
        def route_cdn(route, req):
            name = req.url.split("?")[0].split("/")[-1]
            local = os.path.join(VENDOR, name)
            if os.path.exists(local):
                ctype = "text/css" if name.endswith(".css") else "application/javascript"
                route.fulfill(status=200, content_type=ctype, body=open(local, "rb").read())
            elif "fonts.googleapis.com" in req.url:
                # Real faces, inlined as data URIs, so screenshots show the
                # actual typography rather than a Georgia/Helvetica fallback.
                fc = os.path.join(VENDOR, "fonts.css")
                route.fulfill(status=200, content_type="text/css",
                              body=open(fc, "rb").read() if os.path.exists(fc) else b"")
            elif "fonts.gstatic.com" in req.url:
                route.fulfill(status=200, content_type="text/css", body=b"")
            else:
                route.continue_()
        for pat in ("**/gsap.min.js", "**/ScrollTrigger.min.js", "**/lenis.min.js",
                    "**fonts.googleapis.com**", "**fonts.gstatic.com**"):
            pg.route(pat, route_cdn)
    errs, bad_req, third = [], [], []

    def on_req_failed(r):
        if any(i in r.url for i in IGNORE):
            return
        (third if any(t in r.url for t in THIRD_PARTY) else bad_req).append(
            f"{tag} {r.url.split('/')[-1][:48]}: {r.failure}")

    pg.on("console", lambda m: errs.append(f"{tag} console.{m.type}: {m.text}") if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(f"{tag} pageerror: {e}"))
    pg.on("requestfailed", on_req_failed)

    # Wait on a real DOM signal, not a network lifecycle event. GSAP, Lenis and
    # Google Fonts are third parties; if one of them hangs, "load" and even
    # "domcontentloaded" never fire and the run dies on an environment problem
    # rather than a template one.
    url = (ROOT / path.split("?")[0]).as_uri() + ("?" + path.split("?")[1] if "?" in path else "")
    last = None
    for attempt in range(3):
        try:
            pg.goto(url, wait_until="commit", timeout=20000)
            pg.wait_for_selector(".hdr", state="attached", timeout=25000)
            pg.wait_for_selector("#preloader", state="detached", timeout=15000)
            last = None
            break
        except Exception as e:  # noqa: BLE001 - retrying any nav/boot stall
            last = e
            pg.wait_for_timeout(2000)
    if last:
        fails.append(f"FAIL {tag} page never booted after 3 attempts -> {type(last).__name__}")
        ctx.close(); br.close()
        return
    pg.wait_for_timeout(1400)  # settle after the preloader curtain

    check(not errs, f"{tag} no console/page errors" + ("" if not errs else " -> " + "; ".join(errs[:3])))
    check(not bad_req, f"{tag} no failed first-party requests" + ("" if not bad_req else " -> " + "; ".join(bad_req[:3])))
    if third:
        warns.append(f"WARN {tag} third-party asset unreachable (environment, not the template) -> {third[0]}")

    # preloader must be gone
    check(pg.locator("#preloader").count() == 0, f"{tag} preloader removed")

    # nothing overflowing the viewport horizontally
    over = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(over <= 1, f"{tag} no horizontal overflow (overflow={over}px)")

    # walk the whole page so lazy images fetch and every ScrollTrigger fires
    walk(pg)

    broken = pg.evaluate("""() => [...document.images]
        .filter(i => !i.complete || i.naturalWidth === 0)
        .map(i => i.getAttribute('src'))""")
    check(not broken, f"{tag} all images loaded" + ("" if not broken else f" -> {broken[:4]}"))

    over2 = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(over2 <= 1, f"{tag} no horizontal overflow after full scroll (overflow={over2}px)")

    # nothing left invisible: a data-reveal whose ScrollTrigger never fired
    unrevealed = pg.evaluate("""() => [...document.querySelectorAll('[data-reveal]')]
        .filter(e => e.offsetParent !== null && +getComputedStyle(e).opacity < 0.9).length""")
    check(unrevealed == 0, f"{tag} all reveals fired ({unrevealed} still hidden)")

    pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(800)

    # chrome present on every page
    for sel, what in [("#topbar", "topbar"), (".hdr", "header"), (".ftr", "footer"),
                      (".wa-float", "whatsapp float"), (".concept-ribbon", "concept ribbon")]:
        check(pg.locator(sel).count() > 0, f"{tag} has {what}")

    # ---- page-specific interaction ----
    if name == "home":
        check(pg.locator(".card").count() >= 4, f"{tag} featured grid rendered")
        check(pg.locator(".story-panel").count() == 4, f"{tag} routine panels rendered")
        check(pg.locator(".review").count() >= 8, f"{tag} review rail rendered")
        # counters actually ran
        vals = pg.eval_on_selector_all(".stat .v", "els => els.map(e => e.textContent)")
        check(all(v not in ("0", "") for v in vals), f"{tag} stat counters ran -> {vals}")
        # faq accordion
        pg.locator(".faq-q").first.click(); pg.wait_for_timeout(700)
        hgt = pg.eval_on_selector(".faq-i:first-child .faq-a", "e => e.getBoundingClientRect().height")
        check(hgt > 20, f"{tag} faq opens (h={round(hgt)}px)")
        pg.locator(".faq-q").first.click(); pg.wait_for_timeout(600)

    if name == "collection":
        total = pg.locator(".card").count()
        check(total == 12, f"{tag} all 12 products render (got {total})")
        pg.locator('.chip[data-cat="Body"]').click(); pg.wait_for_timeout(700)
        body_n = pg.locator(".card").count()
        check(body_n == 4, f"{tag} Body filter -> 4 (got {body_n})")
        lbl = pg.locator("#count-lbl").inner_text()
        check("product" in lbl.lower(), f"{tag} count label reads '{lbl}'")
        pg.select_option("#sort", "low"); pg.wait_for_timeout(700)
        prices = pg.eval_on_selector_all(".card-price span:first-child",
                                         "els => els.map(e => +e.textContent.replace(/[^0-9]/g,''))")
        check(prices == sorted(prices), f"{tag} sort low->high {prices}")
        pg.locator('.chip[data-cat="All"]').click(); pg.wait_for_timeout(700)

    if name == "product":
        check(pg.locator(".pdp-thumbs button").count() >= 2, f"{tag} gallery thumbs render")
        check(pg.locator(".spec-table tr").count() >= 5, f"{tag} spec table renders")
        check(pg.locator(".pdp-assure div").count() == 4, f"{tag} assurances render")
        pg.locator("#qty-inc").click(); pg.wait_for_timeout(250)
        check(pg.locator("#qty-val").inner_text() == "2", f"{tag} qty increments")
        check("36,000" in pg.locator("#pdp-total").inner_text(),
              f"{tag} qty updates total -> {pg.locator('#pdp-total').inner_text()}")
        pg.locator("#opts .opt").nth(1).click(); pg.wait_for_timeout(250)
        check(pg.locator("#opts .opt.on").inner_text() == "Travel 10ml", f"{tag} variant selects")
        pg.locator("#pdp-add").click(); pg.wait_for_timeout(900)
        check(pg.locator("#drawer").evaluate("e => e.classList.contains('on')"), f"{tag} bag opens on add")
        check(pg.locator("#cart-count").inner_text() == "2", f"{tag} bag count = 2")
        sub = pg.locator("#cart-sub").inner_text()
        check("36,000" in sub, f"{tag} bag subtotal correct -> {sub}")
        pg.locator("#drawer-body .qty button[data-d='-1']").click(); pg.wait_for_timeout(400)
        check(pg.locator("#cart-count").inner_text() == "1", f"{tag} bag decrement works")
        pg.locator("#cart-close").click(); pg.wait_for_timeout(700)
        check(not pg.locator("#drawer").evaluate("e => e.classList.contains('on')"), f"{tag} bag closes")

    # mobile menu (topbar retracts on scroll down, so return to the top first)
    if label == "mobile":
        pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(800)
        pg.locator("#burger").click(); pg.wait_for_timeout(900)
        vis = pg.eval_on_selector(".mnav", "e => getComputedStyle(e).clipPath")
        check("inset(0px)" in vis or vis == "none", f"{tag} mobile menu opens (clip={vis})")
        pg.locator("#burger").click(); pg.wait_for_timeout(700)

    # sticky filter bar must follow the retracting topbar
    if name == "collection":
        pg.evaluate("window.scrollTo(0, 1400)"); pg.wait_for_timeout(900)
        pg.evaluate("window.scrollTo(0, 2200)"); pg.wait_for_timeout(900)
        top = pg.eval_on_selector(".filters", "e => Math.round(e.getBoundingClientRect().top)")
        check(-2 <= top <= 120, f"{tag} filter bar pinned sensibly (top={top}px)")
        pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(600)

    if shots:
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(shots, f"{name}-{label}.png"), full_page=(name != "home"))
        if name == "home":
            pg.screenshot(path=os.path.join(shots, f"{name}-{label}-full.png"), full_page=True)

    ctx.close(); br.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots-dir")
    ap.add_argument("--vendor-dir", help="serve gsap/lenis/fonts from here instead of the CDN")
    a = ap.parse_args()
    global VENDOR
    VENDOR = a.vendor_dir
    if a.shots_dir:
        os.makedirs(a.shots_dir, exist_ok=True)
    with sync_playwright() as pw:
        for label, w, h in VIEWPORTS:
            for name, path in PAGES:
                audit(pw, name, path, label, w, h, a.shots_dir)
    for line in notes:
        print(line)
    print("-" * 60)
    for line in dict.fromkeys(warns):
        print(line)
    for line in fails:
        print(line)
    print(f"\n{len(notes)} passed, {len(fails)} failed, {len(set(warns))} warnings")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
