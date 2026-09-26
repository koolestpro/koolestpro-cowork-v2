# Template 01 — Watches and luxury accessories

**Demo brand: MERIDIAN.** Registered in `store-templates.json` at the project root.

A three-page premium storefront template. Static HTML/CSS/JS, no build step, no dependencies to install. Drop the folder on Vercel, Netlify, or open `index.html` directly.

The art direction is tuned for watches, and carries just as well for jewellery, eyewear, leather goods, fragrance and premium menswear accessories. For a different vertical, check `store-templates.json` before building something new — reskinning a tested template beats a fresh build.

MERIDIAN is a **fictitious brand**. It exists to demonstrate the template. Nothing in here is a real client or a real result, and the page says so in three places.

---

## What's in it

| Page | File | What it does |
|---|---|---|
| Home | `index.html` | Parallax hero, featured grid, calibre editorial with animated counters, pinned horizontal story, promo banner, ownership split, atelier, auto-scrolling reviews, FAQ, newsletter, footer |
| Collection | `collection.html` | Category filter chips, sort, animated grid, sticky filter bar |
| Product | `product.html?id=m-01` | Sticky gallery with click-zoom, thumbnails, variant picker, quantity, spec table, related products |

Plus, on every page: announcement ticker, sticky header that hides on scroll down, mobile menu, in-memory cart drawer, WhatsApp float, page-transition curtain, preloader.

## Motion

- **GSAP 3.12 + ScrollTrigger** (cdnjs) — word-level headline reveals, section reveals, parallax, counters, the pinned horizontal section
- **Lenis 1.1** (jsDelivr) — momentum scrolling, with a silent fallback to native scroll if the CDN is blocked
- Magnetic buttons, fill-sweep button hovers, image zoom on card hover
- Everything honours `prefers-reduced-motion`

---

## Reskinning it for a client

**You edit one file: `assets/js/site.config.js`.** Nothing else.

1. **Brand** — name, wordmark, tagline, WhatsApp number, socials. Set `conceptNotice: null` to remove the disclaimer on a real build.
1b. **Credits (`builtBy`)** — the Koolestpro watermark appears in three places, all from this one object: the top ribbon, a fixed badge in the bottom-left corner, and a line under the footer. The corner badge fades out on its own once the footer credit scrolls into view, so the two never stack. Set `builtBy: null` to strip all three when handing a build to a paying client.
2. **Theme** — five colours, two fonts. `googleFonts` is the query string from fonts.google.com, so any pairing works.
3. **Currency** — symbol, locale, decimals. Switch `₦`/`en-NG` to `$`/`en-US` and every price on every page reformats.
4. **Copy** — hero, section headings, editorial blocks, value props, FAQ, reviews. Each section has an `index` (the `01 /` label) and a `label`.
5. **Products** — the `products` array. Each entry needs `id`, `name`, `ref`, `category`, `price`, `image`, `gallery`, `short`, `blurb`, `rating`, `reviewCount`, `stock`, `variants`, `specs`. Add or remove freely; the collection page, featured grid, PDP, and related rails all read from it.
6. **Images** — drop replacements into `assets/img/` using the same filenames, or point the config at new ones. Absolute URLs (Cloudinary) work too.

A full reskin is a config edit plus an image swap. Expect 20-30 minutes, not a rebuild.

### Things worth knowing

- `featured.ids` picks which four products show on the homepage grid.
- `story.panels` drives the pinned horizontal section. Four panels is the sweet spot; more just makes the pin longer.
- Category chips come from `categories`, matched against each product's `category`.
- The cart is **in-memory only** — it resets on reload. That is deliberate for a demo. Wire it to a real backend or Shopify Buy SDK if this ever becomes a live store.
- Checkout, the float button and the "speak to a specialist" CTA all go to WhatsApp on **+234 811 750 0831**, with a prefilled message set in `brand.whatsappMessage`. For an international build, swap the drawer button in `chromeBottom()` for a real checkout link.
- Sticky offsets follow the retracting header. The topbar hides on scroll down, and `--sticky-top` drops to 0 with it, so the collection filter bar and the PDP info column pin flush to the top instead of floating mid-screen.

---

## Images

All 14 images were generated with gpt-image-2 at 1024px, converted to WebP (~925KB for the whole set). To regenerate one, the prompt pattern is:

> Ultra-premium studio product photograph of a [description]. Slight three-quarter angle, floating centered on a seamless deep charcoal-black background, single soft key light from upper left, subtle soft reflection beneath, no text, no logos, no watermark, no people. Editorial luxury catalogue photography, sharp macro detail.

Keeping the background and lighting language identical across products is what makes the grid look like one shoot rather than a stock pile.

---

## Verified

Headless Chromium, desktop 1440×900 and mobile 390×844, all three pages:

- Zero console errors or page errors
- Add to cart, quantity, variant selection, drawer totals
- Collection filtering and sorting
- FAQ accordion, mobile menu, pinned horizontal section
- Full-page renders reviewed at both widths

## Known limits

- Content renders from JS, so there is no server-rendered HTML for crawlers. Fine for a sales demo or a sample site. If a client build needs SEO, port the config into a static site generator.
- The pinned horizontal section is desktop only. Below 860px it becomes a scroll-snapping horizontal rail.
- Lenis loads from jsDelivr. On a locked-down network the page falls back to native scrolling without breaking.
