# Template 02 — Skincare and beauty

**Demo brand: Lumora Skin.** Registered in `store-templates.json` at the project root.

A three-page storefront template in a light, warm editorial direction. Static HTML/CSS/JS, no build step, nothing to install. Drop the folder on Vercel or Netlify, or open `index.html` directly.

The art direction is tuned for skincare, and carries for cosmetics, haircare, wellness and supplements, candles and home fragrance, and food and drink brands that want a natural look. It is deliberately the opposite end of the range from Template 01, which is dark luxury. Before building anything new, check `store-templates.json` — reskinning a tested template beats a fresh build.

Lumora Skin is a **fictitious brand**. It exists to demonstrate the template. Nothing here is a real client or a real result, and the page says so in two places.

---

## What's in it

| Page | File | What it does |
|---|---|---|
| Home | `index.html` | Parallax hero, featured grid, formula editorial with animated counters, pinned horizontal routine, gift-set promo, ordering steps, founder story, auto-scrolling reviews, FAQ, newsletter, footer |
| Range | `collection.html` | Category filter chips, sort, animated grid, sticky filter bar |
| Product | `product.html?id=lum-serum` | Sticky gallery with click-zoom, thumbnails, size picker, quantity, ingredient table, related products |

Plus, on every page: announcement ticker, sticky header that hides on scroll down, mobile menu, in-memory bag drawer, WhatsApp float, page-transition curtain, preloader.

## Motion

- **GSAP 3.12 + ScrollTrigger** — word-level headline reveals, section reveals, parallax, counters, the pinned horizontal routine
- **Lenis 1.1** — momentum scrolling, with a silent fallback to native scroll if the CDN is blocked
- Magnetic buttons, fill-sweep button hovers, image zoom on card hover
- Everything honours `prefers-reduced-motion`

---

## Reskinning it for a client

**You edit one file: `assets/js/site.config.js`.** Nothing else.

1. **Brand** — name, wordmark, tagline, WhatsApp number, socials. Set `conceptNotice: null` to remove the disclaimer on a real build.
2. **Credits (`builtBy`)** — the Koolestpro credit appears in the top ribbon, a corner badge on desktop, and under the footer, all from this one object. Set `builtBy: null` to strip all of them when handing a build to a paying client.
3. **Theme** — colours, radii and two fonts. `googleFonts` is the query string from fonts.google.com, so any pairing works. See **Theme tokens** below.
4. **Labels** — every string the engine renders on its own (`Add to bag`, `Your bag`, `products`, the PDP assurances, and so on). This is what stops a reskin for a different vertical from reading like a skincare shop.
5. **Currency** — symbol, locale, decimals. Switch `₦`/`en-NG` to `$`/`en-US` and every price on every page reformats.
6. **Copy** — hero, section headings, editorial blocks, ordering steps, FAQ, reviews. Each section has an `index` (the `01 /` label), a `label`, and an `anchor` that sets its `id` so nav links can point at it.
7. **Products** — the `products` array. Each entry needs `id`, `name`, `ref`, `category`, `price`, `image`, `gallery`, `short`, `blurb`, `rating`, `reviewCount`, `stock`, `variants`, `specs`. Add or remove freely; the range page, featured grid, PDP and related rails all read from it.
8. **Images** — drop replacements into `assets/img/` using the same filenames, or point the config at new ones. Absolute URLs (Cloudinary) work too.

A full reskin is a config edit plus an image swap. Expect 25-35 minutes, not a rebuild.

### Theme tokens

The stylesheet hard-codes no colours, so the same sheet renders a dark theme if a config asks for one. Beyond Template 01's five, this config carries:

| Token | What it does |
|---|---|
| `onAccent` | Text colour on an accent-filled surface. On a light theme this is near-white; on a dark theme it is near-black. |
| `line` / `lineSoft` | Border colours. Separate tokens because a light theme needs darker hairlines than a dark theme needs lighter ones. |
| `ink2` / `ink3` | Secondary and tertiary text. Kept at .74 and .56 alpha so both clear 4.5:1 on the cream background. |
| `scrim` | An `R,G,B` triplet, not a colour. Used inside `rgba(var(--scrim), a)` for the hero scrim, glass headers and the sticky filter bar. |
| `shadow` | The elevation shadow. A light theme has to build depth with shadow where a dark theme gets it free from contrast. |
| `radiusLg` | Media corner radius, separate from the control radius. |

### Things worth knowing

- `featured.ids` picks which four products show on the homepage grid.
- `story.panels` drives the pinned horizontal routine. Four panels is the sweet spot; more just makes the pin longer.
- Category chips come from `categories`, matched against each product's `category`. Every product's category must appear in that list or it will only ever show under "All".
- `labels.lowStock` takes a `{n}` placeholder. The low-stock line shows at `stock <= 10`.
- The bag is **in-memory only** — it resets on reload. That is deliberate for a demo. Wire it to a real backend or the Shopify Buy SDK if this becomes a live store.
- Checkout, the float button and the hero's secondary CTA all go to WhatsApp on the number in `brand.whatsapp`, with a prefilled message from `brand.whatsappMessage`. For an international build, swap the drawer button in `chromeBottom()` for a real checkout link.
- Sticky offsets follow the retracting header. The topbar hides on scroll down and `--sticky-top` drops to 0 with it, so the filter bar and the PDP info column pin flush instead of floating mid-screen.
- The corner watermark is hidden below 640px. It is a fixed badge, so on a narrow screen it landed on whatever sat bottom-left — on the PDP, the product title. The ribbon and footer credit still carry the attribution there.

---

## Engine differences from Template 01

`assets/js/app.js` here is a superset of Template 01's. It is backwards compatible: Template 01's config runs on it unchanged, because every addition falls back to Template 01's wording and ids.

1. **`labels`** — Template 01 hard-coded "Add to selection", "owners", "pieces", the four watch assurances and "Worn with, or instead of." into the engine. All of it now comes from config, with those exact strings as the defaults.
2. **`anchor` per section** — Template 01 hard-coded `#calibre`, `#atelier`, `#anatomy`. Sections now take their id from config, so a skincare build can use `#formula`, `#kitchen`, `#routine` and have the nav point at them.
3. **Light-mode-safe theme injection** — Template 01's CSS hard-coded `#0A0A0B` in six places for text-on-accent. Those are now the `onAccent` token, along with the line, ink, scrim and shadow tokens above.
4. **Review rail thumbs are not lazy** — the rail sits up to 3,400px off-screen horizontally, so `loading="lazy"` meant the avatars only fetched once the marquee carried them into view and popped in blank. Ten 44px images cost less than that. (This one was self-inflicted: the attribute was added while writing this engine and removed after QA caught it. Template 01 never had it.)
5. **`#toast` hidden state** — Template 01 hid the toast with `translateY(140%)`, which on a short message cleared the viewport by only 17px and rendered as a stray dark pill in full-page screenshots. Now `calc(100% + 60px)` plus an opacity fade. **Back-ported to Template 01 on 2026-08-28.**
6. **Corner watermark hidden below 640px** — a fixed badge lands on whatever sits bottom-left, which on the PDP is the product title. **Back-ported to Template 01 on 2026-08-28**, after it collided with "Meridian Chronograph 41" in a showcase mockup.

If Template 01 is ever revisited further, this engine can replace its `app.js` as-is.

---

## Images

All 16 images were generated with gpt-image-2 at `--quality low`, output straight to WebP (1.5MB for the whole set). Every product shot shares one background and lighting sentence, which is what makes the grid read as a single shoot rather than a stock pile:

> Editorial beauty-brand product photograph. [Subject.] Floating centred on a seamless warm sand-cream background (#F0E4D4), soft diffused daylight from the upper left, gentle warm shadow falling to the lower right, shallow depth of field, fine natural texture. Muted warm palette of cream, sand, terracotta clay and soft olive. Calm, premium, natural skincare catalogue photography. No text, no logos, no lettering on labels, no watermark, no people, no clutter.

Two composition rules for the full-bleed images, learned by getting them wrong first:

- **`hero.webp`** must keep the subject in the **right 40%** and leave the left 60% as empty wall. The desktop scrim is weighted left, so a centred subject sits underneath the headline.
- **`promo-sets.webp`** is the mirror: subject in the **left half**, right half empty. That scrim is weighted right.

Labels are left blank on purpose. A demo store with an invented brand name printed on every bottle reads worse than clean unbranded packaging, and it makes the set reusable for a reskin.

---

## Verifying it

`qa.py` drives real Chromium against all three pages at 1440×900 and 390×844, exercises every control, and fails loudly. Run it after any change, and before shipping a reskin.

```bash
export LD_LIBRARY_PATH=/tmp/pw_libs/extracted/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH
python3 qa.py --shots-dir /tmp/shots --vendor-dir /tmp/qa-vendor
```

It checks: console and page errors, failed first-party requests, preloader teardown, every image decoded after a full scroll, horizontal overflow at both widths, every `data-reveal` actually revealed, the chrome on each page, the grid and routine panels, stat counters, FAQ accordion, category filter counts, sort order, quantity, variants, bag add/decrement/subtotal/close, the mobile menu, and the sticky filter offset.

Two things worth knowing about the harness:

- `--vendor-dir` serves GSAP, Lenis and the fonts from local files instead of the CDN, so an outage cannot produce a false failure. It also puts the real typography into the screenshots. Populate it with `gsap.min.js`, `ScrollTrigger.min.js`, `lenis.min.js` and a `fonts.css` of data-URI `@font-face` rules. Without the flag it uses the live CDN.
- It waits on a DOM signal, not on `load`. Three third parties can hang the load event, and a font CDN should not be able to fail a template's QA.

**Last run: 117 passed, 0 failed** (2026-08-28), both widths, all three pages.

Screenshots are worth looking at as well as the assertions. Two real defects on this build — the mobile hero scrimmed to near-invisible, and the toast pill showing in full-page captures — passed every assertion and were only caught by looking.

## Known limits

- Content renders from JS, so there is no server-rendered HTML for crawlers. Fine for a sales demo or a sample site. If a client build needs SEO, port the config into a static site generator.
- The pinned horizontal routine is desktop only. Below 860px it becomes a scroll-snapping horizontal rail.
- GSAP, Lenis and Google Fonts come from CDNs. The page degrades correctly if they fail outright (reveals show, preloader tears down, scrolling falls back to native), but a hanging CDN will delay first paint. Vendor them locally if that matters for a particular build.
- A full-page screenshot of the homepage shows a tall gap where the pinned routine sits. That is the ScrollTrigger pin spacer, not a layout hole. Sections are contiguous; check `offsetTop` if in doubt.
