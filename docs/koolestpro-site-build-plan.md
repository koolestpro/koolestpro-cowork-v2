# koolestpro.com — Site Build Plan

**Created:** 2026-08-21
**Status:** Approved via process-interviewer, ready to execute
**Parent docs:** `docs/koolestpro-growth-operating-plan.md` (Track A2 defines the site structure this implements), `docs/koolestpro-content-operating-plan.md` (feeds /work and /resources)

---

## Goal

Ship `koolestpro.com` as the single destination every client-acquisition channel points at, so that a stranger from either market lands, understands the offer, sees a real price and real proof, and can contact Ridwan without a DM negotiation.

## Context

Six of Ridwan's clients came from content and zero from outbound, because outbound has never been sent and content has never had anywhere to send anyone. The domain was registered 2026-08-20. This plan turns Track A of the growth plan into a concrete build.

The site is also the single strongest proof artifact in the business: it is the thing a prospect judges the work by before reading a word. It must read as a **service business**, not a portfolio, because craft-portfolio signals are what have been attracting recruiters instead of clients.

## Confirmed Decisions

| Decision | Answer | Why |
|---|---|---|
| v1 scope | Full A2 skeleton, both markets, one pass | Shared nav/design system; splitting causes rework |
| Proof strategy | All 6 real clients, honest framing | Scope/craft/speed now, numbers and quotes slot in when clients supply them. No invented figures. Concept builds in a separate labelled section |
| Build method | **Next.js** (App Router, static generation, TypeScript, Tailwind) | Ridwan's call. Mitigation: server components by default, minimal client JS, so Nigerian mobile stays fast |
| Conversion path | Cal.com + WhatsApp + email link | Zero new credentials, works on deploy day. Contact form deferred until an email service is connected |
| Art direction | Dark editorial + live build previews | Stays on the existing brand system. Real work shown live in device frames a visitor can scroll inside, not flat screenshots |
| Outbound | `/for/{brand}` personalised prospect pages, noindexed | Turns "here's an image in a DM" into "here's a page about your store" |
| SEO in v1 | 4 Replo comparison pages, fully written and fact-checked | Near-zero competition, highest intent, most quotable by AI search |

## Site Map

```
INTERNATIONAL (root, USD, Cal.com)
/                             Homepage
/services/store-build         Full build — scope, process, price
/services/page-build          Single page (PDP/LP/advertorial) — price
/services/cro-audit           Paid audit — sample report, price
/work                         Case study index
/work/{slug}                  Individual case studies
/about                        Ridwan, process, location
/book                         Cal.com embed + qualifying questions
/resources                    SEO hub index
/resources/{slug}             4 comparison articles

NIGERIA / AFRICA (₦, WhatsApp-first)
/ng                           "Get a real website for your business"
/ng/website                   Naira packages
/ng/samples                   Live sample gallery + the Lumora demo
/ng/stories                   The three Nigerian anchor case studies

OUTBOUND (noindex)
/for/{slug}                   Personalised prospect page
```

## Detailed Steps

### Step 1: Scaffold and design system
**What happens:** Next.js App Router project at `site/`. Tailwind configured with the brand tokens (Syne + DM Mono, `#FF9500`/`#E040A0`/`#7B2FBE` on near-black). Shared layout, nav, footer, SEO/schema component, motion primitives.
**Output:** A running dev server with routing and one styled page.
**Notes:** Server components by default. Client JS only for the nav toggle, the device-frame previews and scroll reveals.

### Step 2: Content as data
**What happens:** All facts live in typed content files, not scattered in JSX — `content/services.ts`, `content/work/*.md`, `content/resources/*.md`, `content/prospects/*.json`, `content/site.config.ts` (contact details, prices, socials).
**Why:** Adding a case study or a prospect page becomes a data edit, not a build. Also makes the "never invent a number" rule enforceable: a case study with no `metric` renders the scope-and-craft variant automatically.

### Step 3: International pages
**What happens:** Homepage, three service pages (each carrying a published price), `/about`, `/book`.
**Decisions:** Every service page carries a price or range. No "contact for pricing."

### Step 4: /work
**What happens:** Index plus a case study per real client, using the B3 format: situation, what was wrong, what was built, result, what it cost, client quote. Concept builds (KURA, HALOS, MERIDIAN, Lumora) in a visibly separate section labelled as concept work.
**Notes:** Quote and metric fields render only when populated. Offline client sites are described as no longer live rather than implied live.

### Step 5: Nigeria pages
**What happens:** `/ng`, `/ng/website` (Naira ladder), `/ng/samples` (Lumora demo + real samples as they deploy), `/ng/stories` (the three anchor stories).
**Decisions:** WhatsApp primary CTA with prefilled per-page message. No Cal.com. Naira only.

### Step 6: /resources
**What happens:** Hub plus 4 written comparison articles. Article + FAQ schema, question-as-H2 with the answer in the first 40 words (AEO format).
**Notes:** Product facts about Replo, PageFly, Shogun and Instant get verified against current sources before publishing, not written from memory.

### Step 7: /for/{slug}
**What happens:** Personalised prospect page generated from a JSON record: their brand, the problems found, before/after, live rebuild link, price, CTA. `noindex` on every one.

### Step 8: Verify
**What happens:** Build, then headless render every route at 1440x900 and 390x844. Confirm zero console errors, no broken images, correct meta/schema per page, and Lighthouse-class weight on mobile. Fix before declaring done.
**Notes:** This project's standing rule — verify by rendering, not by reading markup. Two-tier QA per the Template Showcase precedent.

### Step 9: Deploy — Ridwan's step
**What happens:** Vercel project connected, then Cloudflare in front (nameservers to Cloudflare, apex CNAME to `cname.vercel-dns.com`, record **Proxied**).
**Owner:** Ridwan. No Vercel token exists in this project, so Claude cannot deploy.
**Notes:** Cloudflare is not optional — Nigerian ISPs block Vercel's shared IP range.

## Edge Cases and Failure Modes

- **No testimonial yet** → case study renders scope/craft/speed variant. Never a placeholder quote.
- **No metric yet** → the result block leads with what was built and how fast. Never an invented figure.
- **Client site offline** (justdarlings, Jellys Glamour) → say so plainly, show archived visuals, no live link.
- **Concept build mistaken for a client** → concept work sits in its own section with a persistent label, and never appears in the client grid.
- **Unverified aggregate claims** ("100+ builds") → dropped unless Ridwan confirms the number is real.
- **Prospect objects to a `/for/` page** → page deleted immediately, pre-written apology, no copy retained.
- **Nigerian visitor can't reach the site** → Cloudflare proxy is the fix and must be set up at launch, not after complaints.
- **Site reads as a job application** → every page ends at a service/price/booking CTA, never at "let's connect."

## Dependencies

| Dependency | Owner | Status |
|---|---|---|
| Vercel account + project | Ridwan | **Blocking deploy** |
| Cloudflare account + nameserver switch | Ridwan | **Blocking Nigeria reach** |
| WhatsApp Business number | Ridwan | Needed for all `/ng` CTAs |
| Cal.com account + event type | Ridwan | Needed for `/book` |
| Public email on the domain | Ridwan | `hello@koolestpro.com` recommended over the personal Gmail |
| Client permission to be named | Ridwan | Needed before publishing named international case studies |
| Screenshots for offline sites | Ridwan | Before those stories become untellable |
| Fiverr/Contra review text | Ridwan | Feeds the proof wall (B5) |

## Open Questions

1. Is "100+ builds" a real, defensible number?
2. Do Tap and Rate, Champion Biotics, Mother of Macros and Captain & Skipper permit being named publicly?
3. Confirmed scope for Captain & Skipper (growth plan flags it as unverified).

## Success Criteria

- A stranger from either market lands, understands the offer, sees a price and proof, and can contact Ridwan without negotiating in a DM.
- Every content CTA and every outbound touch has a real destination on the domain.
- Adding a case study, a resource article or a prospect page is a single-file edit.
- Site is reachable from Nigeria without a VPN.

---

# Build Log

## 2026-08-21 — v1 built and verified, not yet deployed

Built at `site/`. Next.js 16.3.1, App Router, TypeScript, Tailwind. 26 public
routes plus `/for/*`, all statically prerendered, zero npm audit findings.

**Confirmed by Ridwan during the interview:** "100+ builds" is a real number and
is now on the homepage with its source recorded in `content/site.config.ts`.
Naming the international clients is approved. WhatsApp `+2348117500831`, email
`sirridwan721@gmail.com`, booking is **Calendly** (`calendly.com/sirridwan721/30min`),
not Cal.com as the growth plan assumed.

**Decisions taken during the build, with reasons:**

- **Live iframes of client sites were abandoned after testing.** `motherofmacros.com`
  sends `X-Frame-Options: DENY` and `frame-ancestors 'none'`, so a live-preview
  panel would have shipped visibly broken. Client work now uses real screenshots
  in browser chrome with a link out. The interactive previews are Ridwan's own
  builds (MERIDIAN, Lumora), self-hosted under `/live/` and genuinely scrollable
  in the page. Stronger anyway: a prospect can poke at them.
- **`aminazaid.com` returns HTTP 404** from its Wix server, checked 2026-08-21.
  The request reached the server, so this is a real signal rather than a network
  problem. The plan lists the site as live. Its record is set to `private` and
  is not linked until Ridwan confirms the real URL. **Open item.**
- **Captain & Skipper is `publish: false`.** The growth plan flags its scope as
  unverified, and publishing an unverified scope is the exact failure the
  never-invent rule exists to prevent. Assets are already in place; flip one flag
  once the scope is confirmed. **Open item.**
- **Next 16, not 15.** Next 15.1.6 carries a published CVE and the 15.x line
  still bundles a vulnerable postcss. Nothing had been built yet, so moving to
  16 was cheaper than patching around it.

**Defects found by rendering, all fixed:**

| Found | Cause | Fix |
|---|---|---|
| Champion Biotics cover 404 everywhere | the asset was never copied, a bad `cp` line | frame extracted from the client's own screen recording, recorder overlay cropped, composited onto the brand background so the `/work` grid reads as one set |
| `/services/store-build` weighed 1031kB on mobile | proof cards used a CSS `background-image`, which bypasses image optimisation and shipped the full-size PNG | `next/image`; page is now 257kB |
| 52 instances of 11px body text | drift below this project's own 12px floor | raised to 12px, uppercase tracking labels left as the documented exception |
| Naira price ranges broke after the dash | figures too wide for the card | own size step for NGN, unbreakable figures, range wraps as a unit |
| "from ₦1M" rendered at 9px on mobile | the label was em-relative to a 20px price | pinned to 12px |
| Lumora demo was 22MB | source PNGs | converted to WebP and references rewritten, now 804kB, every reference verified to resolve |

**A process note worth keeping:** two rounds of "fixes" were verified against a
stale server, because a failed build left the previous `next start` process
serving old assets while the checks reported false problems (CSS 500s, phantom
overflow) and false passes. `npm run verify` now builds first, fails on a bad
build, serves the fresh output, then checks — so a stale pass is no longer
possible. **Never verify against a server you did not just restart.**

**Verified, not assumed:** 26 routes at 1440x900 and 390x844, 52 renders. Zero
console errors, zero broken images, zero horizontal overflow, one h1 per page,
title/description/canonical present everywhere. Every page 238-275kB total on
mobile. Live embed opened and driven: the Lumora iframe loads, renders 28
product cards, no broken images. `/for/example-brand` 404s while `live: false`;
flipped to `live: true` and confirmed it emits `noindex, nofollow, nocache` and
stays out of the sitemap, then flipped back. Concept builds audited on `/work`:
all three labelled, both offline client sites marked "no longer live", no client
card mislabelled.

**Blocked on Ridwan, in order:**

1. **Vercel project + Cloudflare DNS.** No Vercel token exists in this project,
   so Claude cannot deploy. Cloudflare in front is mandatory, not a nicety.
2. **Confirm the live `aminazaid.com` URL**, or leave the record unlinked.
3. **Confirm Captain & Skipper's scope**, then set `publish: true`.
4. **Add the qualifying questions to the Calendly event** (store URL, revenue
   band, timeline, budget band). The page tells visitors to have them ready;
   Calendly has to actually ask.
5. **Client testimonials and numbers.** Every case study renders the honest
   scope-and-craft variant today. The quote and metric slots are built and
   empty. This is the single biggest upgrade available to the site and it costs
   four messages, not a rebuild.

## 2026-08-21 (later) — v2: art direction rebuilt, "Cinematic / dark canvas"

Ridwan reviewed v1 and rejected the look, not the structure: *"it does not look
like a website to me... I don't want to really use my existing branding... less
text and more visual elements... something portfolio-worthy."*

Presented three art directions. He chose **Cinematic / dark canvas** with motion
pushed hard. The data layer, routes, prices, case-study records, SEO and the
never-invent guarantees were untouched — this was a presentation-layer rebuild.

**What changed**

- **Brand retired.** The orange/magenta/purple gradient set is gone from
  `tailwind.config.ts`. New palette is three colours: void `#070707`, bone
  `#f5f3ef`, signal red `#ff3b1f`. **No gradient appears anywhere on the site.**
  Buttons are hard-edged and invert on hover.
- **Type.** Syne + DM Mono replaced by **Anton** (display, one weight) and
  **Archivo** (everything else). Display type is uppercase, set 46–240px, and
  mixes solid with `-webkit-text-stroke` outlined words.
- **Text load cut hard.** The homepage runs on about 120 words. Long-form prose
  now lives only on `/resources/*`, which is where search depth belongs anyway.
  Semantic h1/h2, alt text and JSON-LD are unchanged, so nothing was traded away
  for the reduction.
- **New motion system** in `components/fx.tsx`: film grain, a difference-blend
  custom cursor, per-word kinetic headings, clip-path unmasks, magnetic buttons,
  parallax, marquees and count-ups. Everything degrades to static content under
  `prefers-reduced-motion` or on a coarse pointer.
- **Canvas hero** (`HeroField.tsx`): a 260-particle flow field that the cursor
  pushes away from itself. 2D canvas rather than WebGL — a few hundred bytes of
  maths against a ~30kB library, no driver to fail on, invisible difference at
  this particle count. Skipped entirely on touch and reduced motion.
- **Signature interaction** (`RevealCompare.tsx`): the client's original page
  with the rebuild underneath, uncovered by the visitor. Built on real assets —
  the matched 780x1688 Obvi and Bebemoss before/after pairs already in
  `outputs/cro-fixes/`.
- **Pinned horizontal work reel** (`Reel.tsx`) on desktop; a native snap rail on
  touch.
- **Navigation is a full-screen index overlay**, not a header bar. Every page
  opens on the work rather than on a menu.

**Defects found by testing, all fixed**

| Found | Cause | Fix |
|---|---|---|
| Every scroll animation dead, reveal panel blank | `Unmask` put the clip-path on the element it was observing, so it hid itself, reported `intersectionRatio: 0`, and never opened | observe an unclipped wrapper, clip an inner element |
| "After" image never downloaded | it starts inside a zero-area clip, so a lazy loader never considers it visible | loads eagerly |
| Hero overflowed the viewport at 760px tall; headline clipped under the header | width-only `clamp()` | `clamp(46px, min(14vw,19vh), 240px)` plus top padding; verified at 900/760/680/844 |
| Reveal showed the one region where both versions look alike | a tall mobile page cropped into a full-width landscape strip, top 29% at 1.5x | constrained to 940px at 3/4; shows ~60% of both at ~1:1 |
| Mobile drag-to-compare stuck after two move events | the browser claims horizontal drags as a pan gesture and cancels the pointer stream | replaced with tap-to-wipe: no gesture conflict, no aiming, and a real button so it works from the keyboard |
| 22px horizontal overflow on mobile home | the Reel's touch rail used negative margins as if inside `.shell`, but it renders outside it | margins dropped |
| Build silently failing while a stale server served old assets | a JSX comment placed as a second child of an expression slot | caught by `npm run verify`, which builds first and fails on a bad build |

**A correction worth recording:** the first diagnosis of the dead-animation bug
blamed `overflow-x: clip` on `body`. That was wrong. The real cause was the
self-clipping observer above. The overflow rule was still moved from `body` to
`html` (the conventional place) and its comment corrected to stop asserting
something that was never demonstrated.

**Verified:** 26 routes x 2 viewports = 52 renders, zero problems — no console
errors, no broken images, no horizontal overflow, no sub-12px text, correct
metadata throughout. The reveal was driven with a real cursor on desktop and a
real tap on an emulated iPhone 13, both confirmed working. Page weight 260–351kB
on mobile; the homepage is heaviest because both reveal images load eagerly,
which is the right trade for the one interaction the site is built around.

**Unchanged and still blocked on Ridwan:** Vercel + Cloudflare deploy, the
`aminazaid.com` URL, Captain & Skipper's scope, Calendly qualifying questions,
and client testimonials/metrics.

## 2026-08-23 — Reference research, and the five changes it caused

Ridwan asked to stop guessing at the direction and look at real sites. Eight
studio/agency sites were opened in a browser and read live; six were assessable
(Obys stalled on its own preloader, Locomotive refused with a bot challenge).
Full writeup: `docs/koolestpro-site-reference-research.md`.

**Applied:**

1. **Hero now leads with real work.** Exo Ape opens on a photograph with no
   headline; Basement runs type over dark footage. Neither opens on an
   abstraction. The canvas particle field is retired — `HeroField.tsx` is no
   longer imported — and `HeroBackdrop` plays a real HALOS scroll capture,
   offset to the right 62% on desktop so the display type keeps clean space.
2. **"In motion" section added.** `outputs/templates/` already held bezel-framed
   scroll videos for HALOS, KURA, Champion Biotics, Tap and Rate and others, and
   the site used none of them. Three are now cropped to their screen region,
   re-encoded for web (hero 397kB, reels 632kB/1.2MB) and served with posters.
3. **The no-metric case study stopped apologising.** Basement writes narrative
   outcomes rather than percentages. An ongoing engagement now reads as the
   result; the absent figure is noted underneath instead of leading.
4. **Solo is stated.** Designjoy names its single operator explicitly. The hero
   now reads "One person, not an agency."
5. **Density direction validated, not changed.** Exo Ape's homepage is ~90
   words, 'kin's is one sentence. This site at ~120 is in range.

**Left as Ridwan's decisions, deliberately not edited:**

- **Prices are below market.** US freelance Shopify builds commonly run
  $2,000-5,000; the site publishes $1,200-1,800. The growth plan gates rises on
  proof milestones, so changing them unilaterally would break his own rule.
- **No risk reversal exists.** Every comparable solo operator has one. The terms
  are a commercial decision, not a design one.

**Bug found and fixed during the change:** `WorkVideo` sets `relative` on itself,
and passing `absolute` in via `className` silently lost — two conflicting
Tailwind position utilities resolve by stylesheet order, not class-list order —
collapsing the hero backdrop to zero height. Fixed by positioning a wrapper
instead of overriding the component. Caught by inspecting computed geometry, not
by the build.

**Verified:** 26 routes x 2 viewports, zero problems. Hero video confirmed
playing (`paused: false`, real currentTime) with correct geometry.

## 2026-08-23 (later) — Work presentation rebuilt, Nigeria page rewritten, portfolio added

Ridwan shared three competitor sites and said the work presentation was the
problem: *"Everywhere my work is being shown is not shown professionally."*

**Sites read live:** `my-shopify-portfolio.webflow.io` (Akinbola Adetomiwa — a
near-exact peer: Shopify + Replo, solo, dark), `alvarostudio.es`,
`manastatics.com`. Each solves the volume problem differently:

| Site | Device |
|---|---|
| Akinbola | Two counter-scrolling marquee rows of full page screenshots, plus a client logo bar under "6+ years of design experience" |
| Alvaro | Overlapping collage cluster of client brand marks; scarcity ("2 spots left"); a free brand review; buyer-question FAQ |
| Mana | Tabbed dense grid (Statics / Landing Pages); animated counters; **Pricing in the nav** |

Common to all three: plain language, an availability signal, a cheap or free
entry offer, visible volume, named testimonials, and money/time answered in an
FAQ.

**Applied:**

1. **`WorkWall`** — two counter-scrolling rows of 18 real page screenshots
   (Tap and Rate, Champion Biotics, Captain & Skipper, KURA), sourced from
   `replo-rebuilds/portfolio/images/exports/` where a consistent 675x1461 set
   already existed. 444kB total. Concept builds carry a Concept tag inside the
   wall, so volume never blurs the client/concept line.
2. **`ClientBar`** — a wordmark row of real clients only. Set as type, not logo
   files: no client logo assets exist and typesetting a name is honest where a
   reconstructed logo would not be.
3. **The old plate reel is gone** from the homepage — the wall replaces it.
4. **`/ng` rewritten end to end** for a shop owner arriving from a WhatsApp
   link: plain words, short sentences, a **visible horizontal nav** instead of
   the full-screen index overlay (a design-audience convention that buyer should
   not have to discover), a permanent WhatsApp button in the bar, numbered
   "What you get" and "How it works", prices with a plain-English payment note,
   and a six-question FAQ covering skill, payment, time, pictures, changes and
   ownership. The hero now carries a real device mockup of the demo store with
   its WhatsApp order button visible, composited into the project's own
   calibrated iPhone frame.
5. **`/portfolio` added** — the hiring page for recruiters, applications and
   interviews. Credentials, the full 13-project list, skills grouped by
   Design/Build/Page types/Growth, and the frameworks. No prices, no packages:
   those would be noise to someone deciding whether to interview him. Facts are
   the ones he already publishes on `koolestpro.github.io/koolestpro-portfolio`.
6. **Copy simplified across home, work, about and book.** "Buried below the
   fold" → "You had to scroll to find it". "Three ways in" → "Three ways to work
   with me". And so on.
7. **Location corrected to Kwara State.** `site.location.city` is now
   `region`; no town is guessed, because he named a state. Local SEO would be
   stronger with a city — ask before filling it in.

**Process fix:** `npm run verify` now frees port 3111 before starting. A
leftover server had already caused one round of phantom MIME/404 failures
against stale chunks — the third time that trap has bitten in this project.

**Verified:** 27 routes x 2 viewports = 54 renders, zero problems. NG hero
confirmed to fit at 900px, 760px and mobile with the headline never clipped.

**Still open:** client testimonials, a risk-reversal offer, the pricing
decision, `aminazaid.com`'s real URL, Captain & Skipper's scope, and the Vercel
+ Cloudflare deploy.

## 2026-08-26 — Before/after rebuilt, KURA over HALOS, new hero, mobile pass

Ridwan's notes: the before/after presentation was poor and not mobile
responsive; the motion section should use KURA (handmade) rather than HALOS
(AI-assisted); the hero could use a creative video rather than his own work;
everything must be mobile responsive; and Portfolio was missing from the
footer and top bar.

**1. `BeforeAfter` replaces `RevealCompare`.** Both requests are satisfied at
once: both versions are visible simultaneously, split by a divider that drags
left to right.

- **Presentation.** The panel now takes the source pair's own aspect ratio
  (900/1948), so the *whole* page shows on both sides. The old component
  cropped a tall mobile page into a 3:4 letterbox, which showed roughly the top
  60% — the one region where before and after look alike.
- **Responsive by breakpoint, not by guess.** Width-driven below 640px
  (346x749 on an iPhone 13 — sized by height it came out 227px wide, too small
  to read), height-driven above (308x666 at 1440x900). Rule lives in
  `.ba-panel`.
- **The touch drag works this time.** `touch-action: none` is scoped to the
  handle alone. The earlier attempt put the drag on the whole panel, and the
  browser claimed horizontal drags as a pan gesture and cancelled the pointer
  stream after two move events. Verified on an emulated iPhone 13: 50 → 88 → 12.
- Keyboard accessible: `role="slider"` with arrow, Home and End keys.
- The section is now two columns — the slider beside a numbered list of what
  actually changed, since the slider alone showed the difference without ever
  naming it.

**2. Motion section is KURA.** `kura-1.mp4` (homepage) and `kura-2.mp4`
(listicle), cropped from the laptop captures and re-encoded. HALOS reel clips
are no longer referenced.

**3. New hero video.** Pexels footage: close-up of hands scrolling a phone in
the dark (id 33942937, by Özgür Sürmeli). On-topic — a mobile buyer is his
subject — and naturally near-black, so display type sits on it without a heavy
scrim. `HeroBackdrop` is full-bleed again; the right-hand offset existed only
to avoid a competing client-page headline, which this footage does not have.
312kB, 15s.
**Note:** the first download silently truncated and produced a corrupt encode.
Content-length is now checked and the transfer resumed until complete, then
integrity confirmed with `ffmpeg -f null -` before encoding.

**4. Mobile pass.** Zero horizontal overflow across 13 routes, and tap targets
audited properly: 23-29 sub-32px targets per page became **zero under 40px**.
Fixed with a coarse-pointer-only `::before` hit area (`.tap` and `.ul-draw`)
plus `summary { min-height: 44px }` — layout and desktop hover targets are
untouched.

**5. Portfolio is now findable.** It was only in the full-screen overlay. It now
has a permanent slot in the top bar on desktop and its own "Pages" column in the
footer, which lists every page for the current market.

**Verified:** 27 routes x 2 viewports = 54 renders, zero problems. Hero video
confirmed playing. Slider drag confirmed on emulated touch in both directions.

## 2026-08-27 — Hero re-cut, four comparisons, NG templates, free tier, footer

**1. Hero is his own work again.** Ridwan: the stock phone footage *"looks cool
but doesn't tell my story."* Correct — it was on-topic but generic. The hero
now plays a 2x2 montage of four **KURA** pages scrolling at once, built with
one ffmpeg filter graph from the existing laptop captures, desaturated and
darkened. All four panels are KURA because he prefers the handmade build to
carry the site. 760kB, 16s. The wash went to 0.68 because several KURA pages
are cream and bone type has to clear the brightest panel, not the average.

**2. Four before/afters, switchable.** `CompareGallery` + `content/comparisons.ts`
replace the single hardcoded pair: **Obvi, Gainful, Material Kitchen,
Bebemoss** — the four matched 780x1688 pairs that already existed in
`outputs/cro-fixes/`. A real tablist (arrow keys work), each with its own
problem statement and four-point change list. All pairs stay mounted so
switching never re-downloads. Adding a fifth is a data edit.

**3. Nigeria templates gallery.** `content/templates.ts` drives it, so new
designs are a three-step data edit with no code. Lumora (skincare) and Meridian
(watches/jewellery) are in, each composited into the project's calibrated
iPhone frame, each labelled Demo. A dashed "More coming" slot is honest filler
rather than a fake third card.

**4. Free tier, with the boundary drawn.** Ridwan asked for a free option but
worried it would cannibalise the paid work. The section states the split
exactly as the growth plan's D5 does: free gets up to 5 products, his branding,
WhatsApp orders, a live link he keeps. Paid begins at card payments, own
domain, more products, changes after handover, and admin access. The framing
line is *"a shop window. It shows what you sell. It does not take the money."*
Capped at three a week, which is also from D5.

**5. Footer rebuilt.** Social links are now inline-SVG icons (LinkedIn,
Instagram, YouTube, TikTok; lettermarks for Fiverr and Contra, which have no
recognised glyph). His face and a three-line bio sit above the columns. The old
"Elsewhere" column became "For hiring", carrying both portfolio links.

**6. Original portfolio is now served from this domain.** Copied from
`replo-rebuilds/portfolio` to `site/public/portfolio-original/`. A naive copy
was **1.1GB** because the folder holds every video export; copying only the 69
assets `index.html` actually references gave 23MB, and re-encoding those in
place at the same filenames (so the HTML needed no edits) gave **5.9MB**.
Verified: 41 images, none broken, zero failed requests. Linked from the footer
and from `/portfolio`, and disallowed in robots.txt since it duplicates
`/portfolio` content.

**Bug found and fixed:** the footer link columns rendered on one line
("IndexWorkAuditPage build…"). `.ul-draw` sets `display: inline-block` and is
defined after `@tailwind utilities`, so it beat the `block` class on each link.
Fixed by wrapping each link in its own div rather than editing the shared class.

**Weight:** desktop home 1.86MB → **1.33MB** after re-encoding the montage
(720p tiles, crf 35, 16s). Mobile home 573kB with **zero video** — the gate
holds. `/ng` 386kB.

**Verified:** 27 routes x 2 viewports = 54 renders, zero problems. Tab switching
confirmed to change both slider and change list.

## 2026-08-27 (later) — /portfolio absorbs the original, contact page, footer rebuild

Ridwan asked to merge `/portfolio-original/index.html` into `/portfolio` so
prospects meet one document, keeping the new site's presentation.

**Correction worth recording: he does have testimonials.** An earlier note in
this project said none existed. Three are published on his own portfolio —
Champion Biotics, Tap & Rate, Mother of Macros — and they are now on
`/portfolio`, attributed to the company exactly as he has them.

**Everything mined from the original, nothing invented:** the three
testimonials, the five-step process with its real descriptions, the 18-tool
stack, six FAQ answers, the two-paragraph bio, the four credential badges, and
the contact form's field set and project-type list.

**`/portfolio` now runs:** availability badge and CTA above the fold with the
portrait beside it · credentials · work wall · four-way before/after gallery ·
testimonials · 13 projects · "What I work in" as four numbered panels with
blurbs and chips (was four plain lists) · five-step process · the stack grouped
Design/Build/Data · about with frameworks and social icons · FAQ · contact form.

**`/contact` added** — email, WhatsApp, phone, location, hours, social icons,
the enquiry form and a Calendly embed on one page.

**Footer rebuilt** into three bands: the oversized ask plus three buttons, then
the portrait/bio/icons, then four reference columns. Previously the giant word
and the columns shared one rhythm and the practical links got lost.

**Icons:** Fiverr and Contra had placeholder lettermarks and looked like
dummies. Both now use traced versions of their real marks. **Fiverr is excluded
from the About block on `/portfolio`** per Ridwan — it shows volume but anchors
the price low, and that page is read by people deciding what to pay him. It
stays in the site footer.

**Portrait:** `ridwan-alpha-2.png` from his own portfolio files, exported to
`ridwan-portrait.webp` (31kB) and a square crop for the footer (16kB).

**Contact form has no backend.** Submitting composes a pre-filled email and
hands it to the visitor's mail client. Deliberate: a form that silently fails is
worse than no form. Only `onSubmit` changes if an endpoint is added.

**Judgement call flagged for Ridwan:** the original's "CRO in practice" section
carries six percentage badges (+18% ATC, +24% review engagement, −19% bounce,
and so on). They read as general CRO benchmarks, but unattributed next to his
name a prospect could reasonably take them as his client results. They were left
off rather than reproduced. If they are sourced, they can go back with the
source named.

**Performance audit** (`scripts/perf.mjs`, new): the only asset above 60kB on
the whole site is `hero.mp4` at **698kB**, and it loads on desktop only.
Homepage desktop 1330kB, mobile 575kB with zero video. Every other route is
17–201kB. `/portfolio-original` is 5.9MB on disk but costs nothing unless
someone opens it.

**Tooling:** `scripts/shots.mjs` added. Heading lookups in `node -e` one-liners
were failing silently because shell quoting mangled comparison operators inside
the inline scripts — it looked like a DOM problem for three attempts. Screenshot
work now goes through a real file.

**Verified:** 28 routes x 2 viewports = 56 renders, zero problems.

## 2026-08-27 (final) — Contra mark corrected, Fiverr unlinked, video on mobile, original portfolio retired

**Contra's mark is a four-pointed star, not a "C".** It was drawn as a letterform
twice from memory and was wrong both times. The path is now lifted from the SVG
on contra.com itself (`viewBox 0 0 24 24`, four concave quadrants). Checking the
real thing took one browser visit; guessing it took two rounds.

**Fiverr removed site-wide.** It left `site.socials` entirely rather than being
excluded per-surface, which drops it from the footer, the contact page, the
portfolio and the JSON-LD `sameAs` in one edit. The reason is recorded in the
config: it shows real volume but anchors the price low, and this site is read by
people deciding what to pay him. The account still exists; it is just not linked.

**Video now plays on mobile** (Ridwan's call — the motion is worth the bytes).
`WorkVideo` no longer gates on `min-width: 1024px`; only an explicit
`prefers-reduced-motion` opts out. The near-viewport observer, `preload="none"`
and the pause-when-offscreen behaviour all stay, so nothing downloads until a
visitor actually approaches a section.

**Reel clips re-encoded for phones.** They used to be desktop-only so their
weight did not matter; now it does. `kura-1` 939kB → 703kB, `kura-2` 1896kB →
734kB (shorter and narrower — a busy listicle page compresses poorly). The
orphaned HALOS `reel-*.mp4` files were deleted. `public/motion` is now 2.3MB
total, down from 5.3MB.

**Mobile homepage cost, measured honestly:** ~1.3MB on arrival (hero only),
~3.1MB if a visitor scrolls the whole page and every video loads. That is the
accepted trade for motion on phones.

**`/portfolio-original` deleted.** `/portfolio` now carries all of its content,
so keeping both was the confusion Ridwan wanted removed. The folder, the footer
link and the robots.txt disallow are all gone.

**Tooling:** `scripts/check-video.mjs` added — scrolls a page at a given
viewport and reports whether every `<video>` actually reached a playing state,
rather than merely being present in the DOM.

**Verified:** 28 routes x 2 viewports = 56 renders, zero problems. All three
videos confirmed playing on an emulated iPhone 13 and on desktop.

---

## Round 10 — Meridian first, /ng repositioned, SEO + AEO pass (2026-08-27)

### What Ridwan asked for
1. Feature Meridian ahead of Lumora on `/ng` and `/ng/samples` (Lumora is due an upgrade).
2. The `/ng` before/after should use the same component as the homepage and portfolio.
3. `/ng` is not Nigeria-only: Nigeria first, expanding outward.
4. Do every SEO/AEO task that can be done in code, and hand back a plan for the manual parts.

### Ordering and positioning
- `content/templates.ts` now carries the display order explicitly, Meridian first. `app/ng/samples/page.tsx` had its own duplicate `SAMPLES` array; it was deleted and the page now maps the shared `templates` export, so order is set in one place.
- `/ng` swapped its single hardcoded `RevealCompare` (Bebemoss only) for `CompareGallery`, the same four-brand switcher the homepage and portfolio use.
- Positioning: badge is now "Nigeria first · Africa next", the title reads "Website for your business — Nigeria & Africa", `areaServed` in schema includes Africa, and the nav/footer market label reads "Nigeria & Africa · ₦". Copy adds: message me from elsewhere in Africa and I will quote in your currency.

### SEO and AEO work
| Added | Why |
|---|---|
| `app/opengraph-image.tsx` + per-route cards for work, services, writing, /ng, /portfolio, /work, /about, /contact, /resources | Every shared link previously had no preview image at all. This was the single most visible gap. |
| `lib/og-card.tsx` | One renderer for all of them. Backgrounds pass through sharp: resized to card size, normalised to JPEG, scrim baked into the pixels. |
| `app/llms.txt/route.ts` | Answer-engine brief generated from the same content files the pages use, so it cannot drift. Carries prices, the concept-brand disclaimer, and both FAQ sets. |
| `ProfessionalService` with `@id` in `app/layout.tsx` | One canonical business entity site-wide with geo, priceRange and areaServed, referenced rather than redeclared per page. |
| `content/schema.ts` | Shared `breadcrumb()` builder. Breadcrumbs now on work, services, portfolio, /ng, about, contact, resources and both index pages. |
| `CollectionPage` + `ItemList` on `/work` and `/resources` | Reads as a set of works rather than unrelated links. |
| `FAQPage` on `/ng` | Six buyer questions lifted out of JSX into `content/services.ts` as `ngFaq`, then used for both the accordion and the schema. |

### Three bugs found and fixed during the pass
1. **`/work/meridian` failed the build with `TypeError: u2 is not iterable`.** Satori decodes PNG and JPEG only, and Meridian's cover is WebP. Every background now goes through sharp first.
2. **The KURA card shipped an unreadable headline.** Satori silently drops a `linear-gradient` on an empty absolutely-positioned div, so the CSS scrim never rendered. The scrim is now composited into the image by sharp.
3. **`/work/[slug]` set `openGraph.images` to the raw cover**, which overrides the file convention. Removed: the raw cover is the wrong aspect ratio for a feed card and carries no title or brand.

### Verified
`npm run verify` — 28 routes x 2 viewports, 0 problems. Alt-text audit across every `<Image>`/`<img>` in `app/` and `components/`: none missing. Cards fetched and looked at, not just diffed.

---

## Round 11 — Static ads, Shopify positioning, stacked packages (2026-08-27)

### What Ridwan asked for
Static ads shown properly (modelled on `manastatics.com`) on their own page plus
home, portfolio and `/ng`; far more Shopify on the site, specifically to rank for
"Shopify designer / developer / expert in Nigeria"; `/ng` packages restructured so
free and Starter are template/coded while Standard and Premium are built on a real
ecommerce platform; packages that stack; migration offered from Standard up; his X
profile added.

### The honesty problem this round surfaced
Obvi, Gainful, Material Kitchen, Bebemoss, V1CE and Versed are all
`isClient: false` in `targets_pool.json` — real brands, unsolicited work. The site
was already showing four of them in `CompareGallery` on three pages with **no
label**, and `comparisons.ts`'s own doc comment called them "these clients". Adding
20 ad creatives for five more real brands would have compounded it into what reads
unmistakably as a client list.

Fixed before shipping any of it: `CompareGallery` now prints "{brand} is not a
client — I rebuilt this uninvited" on every panel, `AdStrip` tags every frame
Concept, `/statics` carries the line in its hero, on every brand tab and in a
section of its own, and both content files' comments were corrected. `llms.txt`
states it for answer engines too.

### Built
| Thing | Note |
|---|---|
| `/statics` | 20 creatives, 5 brands, filter by brand. Selecting a brand reveals the brief it answered and what every claim was sourced from — Mana's dense tabbed grid, plus the pairing Ridwan asked for. |
| `content/statics.ts` | Ad data. `spec: true` on every record with a comment explaining why it can never be otherwise. |
| `components/AdGallery.tsx`, `AdStrip.tsx` | Gallery, and a drifting strip for home and portfolio. All images lazy; `/statics` loads 105kB of an ~976kB library. |
| `/ng/shopify` | The query page for "Shopify developer in Nigeria". `/ng` stays in plain language for a shop owner who has never heard the word; this one names the platform in the H1 because its reader searched for it. Six FAQ answers phrased the way people type them, with FAQPage schema. |
| Packages | Starter / Standard / Premium, stacking. Each card states its build (`Hand-coded` vs `Shopify or WooCommerce`) and inherits the tier below. Migration included from Standard up, plus an add-ons block for migration and ad creative sold on their own. |
| X profile | In `site.socials`, so it appears in the icon row and in `sameAs` schema automatically. Logo taken from the real brand mark, not drawn — the Contra lesson. |

### One bug worth recording
`next/og` cannot render **₦**. Satori tries to fetch a dynamic font for anything
outside the bundled Latin range and a failed fetch renders as tofu — the build
still exits 0, so this is silent. OG card text must say "NGN". Noted in
`lib/og-card.tsx`.

### Verified
`npm run verify` — 30 routes x 2 viewports, 0 problems. Gallery filter driven
live (4 of 20 visible after selecting a brand). Social icon row rendered and
zoomed to confirm the X mark is the real one. Page weights re-measured:
`/statics` 105kB mobile, `/ng/shopify` 29kB, homepage unchanged at 1,311kB.
