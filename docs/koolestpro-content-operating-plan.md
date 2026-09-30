# Koolestpro Content Operating Plan

## Goal
Build a documented operating system that turns Koolestpro's CRO, design, and Shopify build work into a repeatable lead-generation content engine for LinkedIn and X.

## Context
This plan is for Ridwan Adekunle / Koolestpro, focused on attracting Shopify DTC founders and operators whose mobile product pages, landing pages, and ecommerce funnels are visibly under-optimized. The current repo already has a local-first content pipeline with ideas, tips, CRO fixes, captions, outputs, and tracking. This plan extends that system into a broader weekly production workflow that uses multiple AI tools and APIs while keeping human approval before anything is published.

The priority order is:

1. Lead generation
2. Quality
3. Consistency
4. Portfolio

## Operating Principles

- Lead generation comes first. Every content stream should make the right buyer think, "This person can improve my store."
- Quality is a publishing gate, not a nice-to-have. A weak post should be held back even if the calendar has a slot.
- X is a proof-of-work channel. Posts should show building, shipping, testing, improving, work-in-progress screenshots, finished visuals, and before/after snapshots. Avoid generic strategy posts that feel detached from actual work.
- LinkedIn is the polished authority channel. Posts can be more structured, case-study-like, and explanatory.
- Real-brand posts must be framed as unofficial concepts unless the brand is an actual client.
- The system should automate drafting, asset creation, tracking, and queuing, but publishing requires Ridwan's approval in v1.

## Process Overview

1. Maintain a balanced target pool of Shopify/DTC and DTC/B2B ecommerce brands, categories, and page types.
2. Produce one weekly CRO before/after concept from a strong target page.
3. Produce one weekly static ad image showcase from a product URL, product image, or product notes.
4. Produce one weekly template/page showcase from Koolestpro's page template system.
5. Repurpose the week's work into 15 X proof-of-work posts.
6. Create outreach assets for real-brand concepts.
7. Review and approve all assets before publishing.
8. Push approved posts into Google Sheets/Make.com for scheduling and posting.
9. Track all creative files, source records, captions, graphics, and status in the local repo pipeline.

## Detailed Steps

### Step 1: Maintain the Target and Content Pool

**What happens:** Build and refresh a pool of brands, products, page types, and content ideas that the system can use for weekly production.

**Input:** Brand URLs, Shopify/DTC examples, previous targets, product URLs, product images, product notes, saved template ideas, and generated target suggestions.

**Output:** A ranked pool of possible weekly targets, with category, page type, URL, lead potential, visual potential, and status.

**Decisions:** The system should select from an AI-balanced pool, not a rigid schedule. It should balance strong lead potential with category and page-type variety.

**Owner:** Claude/Codex for strategy and scoring; external APIs or scraping/search tools for sourcing when added; Ridwan for final approval of target quality.

**Notes:** Valid CRO targets include Shopify/DTC product pages, landing pages, collection pages, advertorial/listicle pages, offer pages, and related ecommerce pages. The target should be legitimate enough that a founder/operator might care about conversion and should have a mobile issue that can be shown clearly in one before/after screenshot pair.

### Step 2: Rotate Categories and Page Types

**What happens:** Ensure content does not repeat the same type of brand, product, or page every week.

**Input:** Existing target pool and recent publishing history.

**Output:** A selected target that improves variety while still serving lead generation.

**Decisions:** Rotate across DTC categories and page types, but do not force a weak target just to satisfy rotation.

**Owner:** Claude/Codex for selection logic; local pipeline for tracking history.

**Notes:** Core categories include beauty/skincare, fashion/apparel, home/kitchen, fitness/wellness, baby/pet/lifestyle, food/beverage/supplements, NFC/local-business growth tools, digital business cards, QR/review tools, loyalty cards, appointment/review tools, and other related ecommerce categories. NFC products such as review cards or tap-to-review products are valid as DTC/B2B ecommerce targets because they use direct ecommerce product pages even when the buyer is a business.

Page types to rotate include product page, landing page, collection page, advertorial/listicle, offer/bundle page, homepage section, FAQ page, and post-purchase page.

**Reuse rule (clarified 2026-07-12):** a brand can be used for the same stream more than once over time — it is not permanently excluded after one use. `targets_pool.json` tracks this per-stream via each target's `usedFor` array rather than a single `status` flag, specifically so a brand can serve multiple streams (or the same stream again later) without artificial exhaustion. Selection logic should always prefer a target with zero `usedFor` entries for the stream being picked; only fall back to reusing one that already has an entry when nothing fresher qualifies, and any such reuse must target a different page/section/angle than the prior entry, noted explicitly in both the new `usedFor` record and that run's summary. This matches the existing "Previously used brand still has useful pages" edge case below — it was already the intended behavior, just not correctly implemented in the first pass of the automation (V1CE's `status` got stuck at `"Used"`, which would have wrongly blocked it from every stream, not just the one it had already served — fixed the same day).

### Step 3: Produce the Weekly CRO Before/After Post

**What happens:** Select one target page, audit one mobile section, rebuild the selected section, and package the result into a public before/after post.

**Input:** Target brand, URL, category, page type, mobile screenshot, notes, and any available product context.

**Output:** A complete CRO before/after package:

- Target record: brand, URL, category, page type, and reason selected
- Mobile audit: 5-8 issues ranked by likely sales impact
- Chosen fix area: one section only, usually above-the-fold unless another section has stronger content value
- Rebuilt mobile section: HTML/CSS implementation by default
- Before/after screenshots using the same mobile viewport
- Annotated final graphic with curved-line annotations
- LinkedIn post, X thread or sequence, and 3-5 short X proof-of-work posts
- Pipeline record with status, date, platform plan, and source files

**Decisions:** Use HTML/CSS rebuild as the default method. Use GPT image or another image model for final presentation graphics and annotations, not as the default rebuild method.

**Owner:** Claude/Codex for audit judgment, strategy, prompts, QA, and orchestration. DeepSeek/OpenCode for low-cost HTML/CSS rebuild work. OpenAI/GPT image for final annotated graphics.

**Notes:** The improvement must be visually obvious within 3 seconds. If the improvement is useful but not visually obvious, keep the audit privately for outreach/backlog and choose another page or section for public content.

### Step 4: Produce the Weekly Static Ad Image Showcase

**What happens:** Create static ad concepts for a product and package them as visual content.

**Input:** Product URL or product image plus product notes. The product can be from Ridwan/sample work or from a real target brand.

**Output:** A static ad image package:

- Product/context record
- Four ad concepts
- Individual ad images
- One combined showcase image for LinkedIn
- Separate visual assets for X
- LinkedIn caption and X proof-of-work posts
- Pipeline record

**Decisions:** Default ad angles are problem/solution, benefit/result, social proof/trust, and offer/urgency.

**Owner:** Claude/Codex for concept strategy, positioning, and QA. OpenAI/GPT image for ad images and combined showcase. Other image APIs can be added later if they improve quality, speed, or cost.

**Notes:** Static ad subjects should be labeled internally as either portfolio/static skill demos or lead-generation concept demos. Real-brand concepts must not imply official client work.

### Step 5: Produce the Weekly Template/Page Showcase

**What happens:** Use Koolestpro's template system to create or showcase one page, then turn it into social content.

**Input:** Page brief, product/category, page type, target buyer, offer angle, and selected template.

**Output:** A template/page showcase package:

- Page brief
- Generated page from the template system
- Mobile mockup image for LinkedIn
- Caption explaining the work and positioning
- X proof-of-work posts supported by visuals
- Pipeline record with source files and publish status
- Optional desktop/mobile scroll recording

**Decisions:** Prioritize the most lead-generating page types first: product page, landing/offer page, advertorial/listicle, and collection page. Homepage, FAQ, and post-purchase pages remain supported but lower priority.

**Owner:** Claude/Codex for page strategy and QA. DeepSeek/OpenCode for implementation. OpenAI/GPT image or screenshot tooling for mockups/showcase graphics.

**Cross-project source (decided 2026-07-11):** Koolestpro's actual template/page-building system lives in a separate connected project folder, `replo-rebuilds` — its own standalone repo with its own `CLAUDE.md`/`AGENTS.md`/`WORKFLOW.md` governing templates (`templates/{type}/{template-id}/`) and brand builds (`brands/{brand}/pages/`, `case-study/`, `static-ads/`). That folder stays the source of truth for page-building and isn't merged into this project. Step 5 reads/selects/builds the page there, following its own rules, then copies back only a mobile mockup screenshot + caption into `outputs/templates/{slug}_{date}/` here, with the pipeline JSON's `folder` pointing at that local copy — not at a cross-project path. This keeps the koolestpro pipeline self-contained (nothing breaks if `replo-rebuilds` is ever unmounted), at the cost of one duplicated screenshot per showcase. The real, editable page file stays in `replo-rebuilds` and is linked to from the caption/notes for anyone who wants to open it there.

**Notes:** X posts for this stream should not be generic strategy tips. They should show builder energy: WIP screenshots, finished sections, mobile mockups, and "what I built/changed/shipped" angles.

### Step 6: Repurpose Weekly Work Into X Proof-of-Work Posts

**What happens:** Convert the week's CRO, static ad, and page showcase outputs into a daily X content queue.

**Input:** All visuals, screenshots, WIP states, finished graphics, captions, notes, and lessons from the weekly production cycle.

**Output:** 15 approved X posts for the week, with visuals where possible.

**Decisions:** X should be treated as a visual proof-of-work feed, not a generic education channel.

**Owner:** Claude/Codex for post generation and QA; Make.com/social API for approved scheduling.

**Notes:** Good X post angles include:

- "Built this section today..."
- "Before/after from a mobile PDP fix..."
- "Testing a new offer section layout..."
- "4 static ad directions from one product..."
- "This is the part I changed because the original page buried the action..."
- "WIP vs final..."

### Step 7: Create Outreach Assets for Real-Brand Concepts

**What happens:** For every real-brand CRO or static concept, create a private sales follow-up package.

**Input:** Brand target record, before/after image, audit notes, selected improvements, and public/private links.

**Output:** Outreach package:

- Brand/contact record
- What was improved
- Before/after visual or link
- Short email/DM pitch
- Follow-up sequence
- Status tracking: not contacted, contacted, replied, booked, closed/lost

**Decisions:** Outreach should be included in v1 because lead generation is the primary goal.

**Owner:** Claude/Codex for outreach copy and strategy. Google Sheets or local pipeline for status tracking. Make.com/email/social APIs can be added later for automation after approval.

**Notes:** Tone should be short, useful, specific, and permission-based. Lead with the improvement, mention it is an unofficial concept, share the visual, avoid long audits in the first message, and ask a simple permission-based question such as "Want me to send the 3 changes I'd prioritize next?"

### Step 8: Review, Approve, and Queue

**What happens:** Review the weekly production package and approve only the assets that meet the quality bar.

**Input:** LinkedIn posts, X posts, graphics, screenshots, rebuild files, outreach assets, and pipeline records.

**Output:** Approved content queue ready for Google Sheets/Make.com and rejected/backlog items marked with reasons.

**Decisions:** Publishing requires human approval in v1.

**Owner:** Ridwan for approval. Claude/Codex for QA support and revision recommendations.

**Notes:** Approval checklist:

- Visual looks professional enough to be portfolio-worthy
- Improvement is obvious within 3 seconds
- Caption sounds like Ridwan: direct, practical, builder energy, no generic marketing fluff
- Post connects to lead generation: CRO, Shopify build quality, better product presentation, or conversion
- Public framing is safe for real-brand concept work
- Files are organized for reuse

### Step 9: Publish and Track

**What happens:** Approved posts are moved into the publishing queue and tracked through production, scheduling, publishing, and outreach.

**Input:** Approved post packages and outreach packages.

**Output:** Scheduled/published posts, updated pipeline status, and outreach status.

**Decisions:** Keep the local repo pipeline as the creative source of truth. Use Google Sheets/Make.com as the publishing queue and automation layer.

**Owner:** Local repo pipeline for files and creative records. Google Sheets/Make.com/social APIs for scheduling and posting after approval.

**Notes:** The existing local-first architecture should remain intact. `pipeline_data.json`, `content_pipeline.html`, and `ridwan_content_system_updated.html` should continue to track creative work, while Google Sheets/Make.com can mirror approved publishing data.

### Step 10: TikTok Daily Automation + Instagram Repurposing (planned 2026-07-29)

**What happens:** Turn the existing weekly generation streams into a daily TikTok posting cadence without Ridwan ever recording himself, then repurpose the same TikTok output to Instagram once Instagram posting is unblocked.

**Input:** Tip carousel scripts/backlog, Template Showcase scroll-through videos, CRO Fix before/after graphics, Static Ad image sets — all already produced by Steps 3-5 and koolestpro-tips-weekly.

**Output:** 7 TikTok-ready vertical videos per week, posted automatically, plus a caption entry in the relevant `{brand}-social-content.json`.

**Format mix (Ridwan's choice, 2026-07-29 — rotate all three, not one fixed format):**

1. **Faceless avatar talking-head** — HeyGen (via the `heygen-api` skill) reads a Tip script using a stock avatar, not Ridwan's likeness or voice. Unlimited supply since it's script-driven, not tied to weekly asset generation. Target 2-3x/week.
2. **Repurposed existing video** — Template Showcase's `{slug} mobile.mp4` (already 1080×1350 vertical) or `{slug} cover.mp4`, cut to a 15-30s TikTok-paced clip with on-screen captions. CRO Fix before/after graphics animated into a wipe-transition reveal. Runs whenever that week's generator has fresh output, target 1-2x/week.
3. **Text-hook slideshow** — Tips carousel slides or Static Ad combo images assembled into a captioned slideshow with TTS/voiceover. Target 2-3x/week.

**Decisions:**

- **Posting layer: Blotato**, connected as a native module in the existing "Koolestpro Social Distribution" Make.com scenario (same pattern as the live LinkedIn/X branches). Reasoning: Blotato has already cleared TikTok's Direct Post audit, so posts publish publicly without Ridwan going through his own weeks-long app review; it ships a built-in Faceless Video Generator (ElevenLabs voices) that can generate Format 3 directly instead of building slideshow-assembly tooling from scratch; and it's cross-platform, which is also the most likely path to finally unblock Instagram (see below). Pricing as of 2026-07-29: Starter $29/mo (1,250 credits), Creator $97/mo (5,000 credits), both cover up to 900 TikTok posts/month — a daily cadence fits Starter easily. [Blotato TikTok API pricing](https://www.blotato.com/blog/tiktok-api-pricing)
- **Account warm-up caveat:** if the TikTok account being used is brand new, TikTok's own anti-spam signals mean it should post manually for about 4 weeks before automation is switched on, or risk a shadowban. Confirm account age with Ridwan before flipping this live. [Blotato TikTok connect-accounts guide](https://help.blotato.com/platforms/tiktok/connect-accounts)
- **Instagram repurposing (Phase 2, blocked until):** per `project_instagram_automation_blocked` — the in-house Meta Graph API build is stuck on a Page↔IG account-linking restriction, not a config error. Since Blotato is a separately-audited multi-platform layer, it may sidestep that specific restriction entirely; this should be tested once TikTok is live, before assuming the in-house Meta build needs more debugging. If Blotato's IG connection also hits the same account-linking wall, this stays blocked as before.
- **No new tracking file.** Same reasoning as Step 5's new-store-build track: this is a content/distribution change, not a new lifecycle to track. Register each generated video the normal way (pipeline item + `{brand}-social-content.json` entry), just with an added TikTok row in the distribution queue.
- **Captions follow the project-wide rule** (no em dashes, humanizer pass, real line breaks, hashtags fine on TikTok/Instagram same as LinkedIn/IG convention).

**Owner:** Claude for format/script direction, HeyGen script writing, slideshow assembly specs, and QA. Blotato for TikTok (and eventually Instagram) publishing. Ridwan for Blotato account signup/billing and TikTok account connection — publishing credentials are an account-level decision that has to be made by him.

**Not yet built:** Blotato account doesn't exist yet. Nothing here posts until Ridwan signs up, connects TikTok, and the Make.com module is wired in — same "plan first, build once account exists" pattern as the X rollout.

### Step 10 — CORRECTED 2026-07-30: real pipeline proven, posting path re-scoped to free draft-inbox first

The format-mix and posting-layer decisions above were written 2026-07-29, before any real TikTok video existed for this project. A full build/research pass on 2026-07-29/30 (documented in the Build Log below) changed both.

**What actually got built (not HeyGen, not a slideshow assembler):** real Playwright scroll-capture of live/local pages, frame-by-frame PIL overlay (badges, ring markers, burned-in captions), Groq Orpheus TTS voiceover, and compositing into a calibrated real iPhone bezel. Zero HeyGen avatar work was ever built or tested — Format 1 above stays theoretical until/unless Ridwan wants to revisit it. Five real videos now exist in `outputs/tiktok_mockup/`, deliberately spanning content TYPES rather than re-editing one case study (per Ridwan's explicit 2026-07-30 correction — see Build Log): v3/v4/v5 (CRO Fix, three distinct edit styles on the Material Kitchen case study), v6 (Template Showcase, HALOS PDP), v7 (behind-the-scenes/expertise process video, TAPro). Tip and Static Ad video types are the two pipeline content types still unbuilt.

**Posting layer decision changed: Blotato is not the Phase 1 choice.** Ridwan confirmed 2026-07-30 he isn't ready to spend on anything yet, wants everything documented first, and specifically asked about a path where a video gets sent to TikTok automatically but he publishes it himself — i.e. draft, not live. Researched TikTok's own Content Posting API directly rather than assuming Blotato is the only option, and it turns out TikTok already offers exactly this for free:

- **Direct Post** (`video.publish` scope, `POST /v2/post/publish/video/init/`): goes live/public immediately. Any unaudited app is forced to private-only visibility — lifting that requires TikTok's own compliance audit. This is the slow path Blotato exists to skip.
- **Inbox/Draft upload** (`video.upload` scope, `POST /v2/post/publish/inbox/video/init/`): uploads straight to the creator's own TikTok inbox as a draft. No compliance audit gates this mode's visibility restriction — Ridwan gets an inbox notification in the TikTok app, opens it, reviews, and taps Post himself. This is the free "auto-send, manual-publish" path he described, and it needs nothing beyond a TikTok Developer account.

Setup, whenever Ridwan is ready to move past documentation: register an app at developers.tiktok.com → add the Content Posting API product → request the `video.upload` scope (a lighter approval than the Direct Post audit) → run Login Kit OAuth once for Ridwan's own TikTok account (3+ years old, already active this year until a 2026 posting gap — no new-account shadowban warm-up period applies, unlike Step 10's original warning above which was written for a hypothetical brand-new account) to get an access token + open_id → per video, `POST /v2/post/publish/inbox/video/init/` with `source_info: {source: FILE_UPLOAD, video_size, chunk_size, total_chunk_count}` → PUT the video bytes to the returned `upload_url` → poll `/v2/post/publish/status/fetch/` with the `publish_id`. Blotato (or an equivalent) stays the Phase 2 upgrade once there's real TikTok traction and budget — full public auto-posting, and still the most promising lever for the Instagram Page↔IG-link restriction noted above.

Sources: [Content Posting API — Get Started (Direct Post)](https://developers.tiktok.com/doc/content-posting-api-get-started), [Content Posting API — Get Started (Upload/Inbox)](https://developers.tiktok.com/doc/content-posting-api-get-started-upload-content).

**Status as of 2026-07-30: documentation only.** Nothing built, no scheduled task, no OAuth app registered, no posting integration of any kind. This section exists so the system is ready to execute the moment Ridwan says go — see [[project_tiktok_video_pipeline]] and [[project_tiktok_automation_plan]] memory for the session-level detail.

### Step 11: Trend & Format Awareness Engine for Tips + Cross-Format Discovery (planned 2026-07-30)

**What happens:** A weekly, config-driven research pass across X, Reddit, and Instagram surfaces two things: (a) a ranked shortlist of trending topics/angles in Ridwan's niche to drive that week's Tips carousel topic selection, and (b) an opportunistic "Format Radar" flag whenever a competitor or adjacent creator in the web design/CRO/Shopify space is getting real engagement from a content format or style Ridwan hasn't tried yet, in any medium — image, carousel, infographic, or video/Reel.

**Input:** Ridwan's 3 content pillars (Digital Craftsmanship, Conversion Strategy, Builder's Journey) and their associated niche keywords (Shopify, CRO, DTC ecommerce, web design) as the search filter. X reads via the official pay-per-use API. Reddit reads via a cheap third-party pay-per-call provider (not Reddit's own official API, which floors at $12,000/year for commercial access). Instagram via Claude-in-Chrome browsing — confirmed 2026-07-30 that no viable trend-discovery API exists for Instagram: the Graph API's Hashtag Search only returns posts for a hashtag already known (not discovery), is capped at 30 hashtags/week, and requires the same Page↔IG Business-account link that's already blocking Instagram posting automation (`project_instagram_automation_blocked`).

**Output:**
- **Layer 1 (Tips topic selection):** a ranked candidate-topic list, auto-consumed by `koolestpro-tips-weekly` the same way it already auto-picks a Myth-vs-Reality angle today. No separate approval gate on the topic itself — Ridwan still reviews the finished carousel before it posts, same as every other weekly buffer run.
- **Layer 2 ("Format Radar"):** a flagged card at the top of `content_pipeline.html`, appearing only on weeks something genuinely clears the bar (new-to-Ridwan format, real engagement signal behind it, niche-relevant) — never a manufactured weekly quota, silence is fine most weeks. Each flag includes the source example/link, why it's working, and — if it's a video/Reel format — a note on whether it's buildable with the existing `video-gen`/`outputs/tiktok_mockup/` tooling (HeyGen faceless avatar, repurposed Template Showcase/CRO Fix clips, or a format style like the ones already prototyped in the 2026-07-29/30 TikTok research passes below). Ridwan decides case by case whether to try a flagged format once, adopt it permanently, or use it to replace an existing template — nothing from this layer auto-builds.

**Decisions:**
- **Sources and cost.** X via the official pay-per-use API (App-only Bearer token, no browser login required, fits unattended scheduled runs) — capped at roughly 50 posts read/week (~$1/month), sharing Ridwan's existing $5-7/month X credit pool with posting (the live "Koolestpro Social Distribution" Make.com scenario). If more volume is needed later, raise the read cap, not the run frequency, as long as total X spend stays under ~$5/month — Ridwan's explicit preference. Reddit via a cheap third-party pay-per-call reseller (~$0.002/read; specific provider still TBD, Ridwan's signup) — capped at roughly 100 posts read/week (~$1/month), a separate budget from X. Instagram via Claude-in-Chrome is free but the weakest signal of the three (no real discovery API exists there at all), so treat it as a supplementary check, not a primary source. A running spend estimate halts further pulls mid-run rather than silently exceeding either monthly ceiling.
- **Scope.** Layer 1 feeds Tips only, not CRO Fix/Static Ad/Template Showcase — those three streams are target-brand-driven, not topic-driven, and Ridwan confirmed they're "solid the way we do it."
- **Discovery method.** Keyword-driven by default, not a fixed subreddit/competitor-account allowlist (none specified as of this planning pass). A light relevance/brand-safety filter runs before anything reaches the Tips shortlist or the Format Radar card, so off-brand or irrelevant finds don't waste review time even though everything downstream still gates on Ridwan's approval.
- **Portability (hard requirement).** Must be built as a config-driven, project-agnostic skill (niche keywords, pillars, and output paths living in each project's own CLAUDE.md), matching how `page-presentation-kit` and `static-ad-image` already work, because Ridwan wants to reuse this exact engine later for his separate Islamic content project, with different niche keywords and a different persona, without a rebuild.
- **Charlie Hills' `social-media-skills` repo verdict** (github.com/charlie947/social-media-skills, evaluated in full 2026-07-30 — this whole step was prompted by Ridwan sharing it plus X's new agent-facing API docs). Its own `niche-research` skill (Claude-in-Chrome browsing X/Reddit/Google) is superseded here by the real X/Reddit APIs, which are cheap and more tailored than browser scraping. `hook-generator` is adopted outright (small, no architecture conflict). `post-scorer` and `reels-scripting` are worth building for real once Apify is confirmed working, since they need actual post-history data, not generic advice. `analytics-dashboard` is a good idea but a separate future project, not bundled here. Useful concepts from `post-formatter` (PAS/AIDA/BAB/STAR/SLAY frameworks, concrete line-length/mobile-formatting rules, a tested "repost if" CTA pattern) and `content-matrix` (an 8-format ideation axis: Actionable/Motivational/Analytical/Contrarian/Observation/X vs Y/Present vs Future/Listicle) get folded into `koolestpro-content-engine` and `koolestpro-idea-expander` respectively rather than adopting those two skills wholesale. The rest (`voice-builder`, `profile-optimizer`, `post-writer`, `graphic-designer`/`gemini-infographic`/`gemini-carousel`/`quote-post`, `youtube-thumbnail`, `pinned-comment`) were skipped: redundant with what Ridwan already has, off-architecture (their image-gen skills are manual copy-into-Gemini workflows, which conflicts with the automated DeepSeek/GPT-image pipeline this project already runs), or not applicable to Ridwan's current channels.
- **`koolestpro-idea-expander` (Skill F) needs modernizing regardless of this step.** It still has "Send to Notion" logic and reads the old `ridwan_content_system.html` filename (not the current `_updated.html`), and isn't called by any scheduled task today — it's legacy and manual. Its Phase 2 (mandatory web-search research before generating ideas) is the same job this new engine does better with real platform data instead of generic web search. Plan is to retire that phase in favor of consuming this engine's output, and fix the Notion/filename drift while touching the file.

**Owner:** Claude/Codex for the research logic, ranking, relevance/brand-safety filtering, and Format Radar write-ups. Ridwan for: X Developer Portal billing (already done, live), signing up for a Reddit third-party API provider (not yet done), and reviewing/acting on every Format Radar flag.

**Notes:**
- **Apify wired for real, 2026-07-30.** Ridwan's token (`apify_api_...`) and user ID (`fxaxqSdyGIK6xVyDE`) are saved to this project's `.env` as `APIFY_API_TOKEN`/`APIFY_USER_ID`, for direct REST calls. The Cowork "Apify" MCP connector itself stayed unauthenticated even after Ridwan updated it on his end (`mcp__Apify__search-actors` still failed "User was not found or authentication token is not valid" on retest) — not relied on. `post-scorer`'s eventual build should call Apify's REST API directly via script, same pattern as DeepSeek/HeyGen/Pexels/Pixabay already in this project, using the specific actor named in Charlie's skill file, `apimaestro/linkedin-profile-posts` (`{"username":..., "total_posts":100}`, never pass a `fields` param since it strips engagement data), scored against Ridwan's own post history, not Charlie's benchmark fallback data.
- **Edge cases.** Any single source down or rate-limited that week falls back to whichever sources still work; if all three fail, Tips falls back to its existing default Myth-vs-Reality angle rather than blocking the run. Instagram browsing getting blocked by anti-bot detection gets flagged in the run summary, not failed silently, same "verify, don't assume" pattern already standing in this project.
- **Video-format Format Radar flags** should cross-reference the format-range work already prototyped in `outputs/tiktok_mockup/` (the 2026-07-29/30 research passes found @ecomvso/@marketingomar/@realdennisdemarino5-style patterns and built v3-v7 prototypes spanning Tip/CRO Fix/Template Showcase/behind-the-scenes content types) rather than inventing new video tooling from scratch.

**Not yet built.** This is planning only — no skill file, scheduled task change, `content_pipeline.html` UI change, or CLAUDE.md config section exists yet. The one concrete change made during this planning pass is the `.env` Apify addition above. Next step, once Ridwan is ready to build: a new config-driven skill, wiring its output into `koolestpro-tips-weekly`, the Format Radar card in `content_pipeline.html`, the `koolestpro-content-engine`/`koolestpro-idea-expander` framework/format-axis additions, and a CLAUDE.md config section once the skill exists (matching the `page-presentation-kit`/`static-ad-image` "Export Routing" pattern).

## Weekly Definition of Done

A weekly production cycle is done only when all of these exist:

- 1 approved LinkedIn CRO before/after post
- 1 approved LinkedIn static ad showcase post
- 1 approved LinkedIn template/page showcase post
- 15 approved X proof-of-work posts for the week
- 7 TikTok posts for the week, once Step 10 is live (either the free TikTok draft-inbox path or Blotato connected)
- Outreach assets created for any real-brand CRO/static concept used
- All files saved locally and tracked in the pipeline
- Approved posts pushed to Google Sheets/Make.com publishing queue

## AI/API Role Split

### Claude/Codex

- Strategy and orchestration
- CRO audit judgment
- Content direction
- Documentation
- Skill updates
- Prompt design
- Quality review
- Final approval support

### DeepSeek/OpenCode

- Low-cost HTML/CSS implementation
- Rebuilds of selected mobile sections
- Repetitive code generation
- Template/page implementation
- Cleanup of generated HTML/CSS

### OpenAI/GPT Image

- Static ad image generation
- Final before/after graphics
- Curved-line annotations
- Combined showcase visuals
- Presentation graphics for LinkedIn and X

### Google Sheets / Make.com / Social APIs / n8n

- Publishing queue
- Approval status sync
- Scheduled posting after approval
- Optional outreach tracking and automation

### Future APIs

Other APIs can be integrated later when they clearly improve quality, cost, speed, sourcing, screenshots, scheduling, or image/video generation.

## Source of Truth

The local repo remains the creative source of truth. It should store:

- Target records
- Audits
- Rebuild files
- Screenshots
- Graphics
- Captions
- X post queues
- Outreach assets
- Pipeline status

Google Sheets and Make.com should act as the publishing and automation layer, not the main creative archive.

## Brand Safety Rules

- Use real brand names and URLs internally for targeting, audit files, and lead tracking.
- Public posts should frame work as a concept CRO improvement or unofficial redesign.
- Never imply that a brand hired Ridwan unless they did.
- Blur or partially anonymize brand names/logos for sensitive cases.
- Keep public tone constructive: "what I'd improve" rather than "this brand is bad."
- Save full target details privately for outreach.

## Edge Cases and Failure Modes

- **Not enough good targets:** Use a saved backlog of approved targets, then expand to adjacent DTC/B2B ecommerce categories such as NFC and local-business growth tools, then use portfolio/sample products, then create a template/page showcase. Do not force a weak public before/after post.
- **Previously used brand still has useful pages:** Reuse the brand, but rotate page type or product angle. If a product page was used before, consider collection page, landing page, offer page, advertorial/listicle, homepage section, or another product. Repeat the exact same page only if there is a clearly different section or content angle.
- **Valid page but weak visual content:** Keep the audit privately for outreach/backlog and choose another page or section for public content.
- **AI-generated rebuild looks worse than the original:** Revise or discard it. It cannot publish unless it meets the quality bar.
- **Generated image misrepresents the product or brand:** Regenerate or switch to screenshot/mockup-based visuals.
- **Caption sounds generic:** Rewrite in Ridwan's direct, practical, builder-energy voice.
- **Real-brand post feels risky:** Anonymize, blur branding, or turn it into a private outreach-only asset.
- **Automation fails:** Keep all source files local and manually queue approved assets if needed.
- **Video automation is too slow or unreliable:** Keep page scroll videos optional/manual in v1.

## Dependencies and Requirements

- Existing local repo pipeline remains available.
- Current skills should remain in place until the operating plan is converted into specific skill updates.
- DeepSeek/OpenCode API access for low-cost implementation work.
- OpenAI/GPT image access for graphics and ad images.
- Google Sheets and Make.com access for publishing queue and scheduling automation.
- Social posting APIs or Make.com integrations for LinkedIn/X posting where possible.
- Screenshot tooling for consistent mobile before/after captures.
- File organization rules for outputs, source records, captions, graphics, and outreach assets.

## Open Questions — Resolved (2026-07-05)

- **File schema / separate vs. extended:** Target records and outreach records get their own files — `targets_pool.json` and `outreach_tracker.json` — rather than extending `pipeline_data.json`. Reason: the target/outreach lifecycle (not-contacted → contacted → replied → booked → closed) is different from the content-item lifecycle (Idea → Nominated → Created → Scheduled → Published), and keeping them separate avoids breaking the existing `content_pipeline.html` / `ridwan_content_system_updated.html` parsing of `SYNC_DATA.items`.
- **Screenshot tool:** Claude in Chrome (already connected in this workspace) is the standard for mobile before/after captures — navigate to the target URL, set a mobile viewport, capture. No new dependency needed. Revisit only if a specific site fights the browser tooling (lazy-load, cookie walls, bot detection).
- **Approval UI:** Extend the existing `content_pipeline.html` with approve/reject actions and status per the Step 8 checklist, rather than moving review to Google Sheets or building a new dashboard. Keeps the local repo as the single source of truth for creative review.
- **Social posting method (v1):** Manual. Approved posts are copied from the queue and posted by Ridwan directly. Make.com/API automation is deferred until the target-pool → showcase → X-repurposing production loop is actually running end to end.

**Still open:** exact naming/cadence convention for `targets_pool.json` entries, and when (if ever) to revisit Make.com automation for posting.

## Build Log

Tracks what has actually been built against this plan, so a future v2 pass knows exactly what exists and doesn't re-litigate settled decisions.

### 2026-09-28: Target pool refresh (ISO week 40), 5 candidates added

`koolestpro-target-pool-refresh` ran on an even ISO week. Trigger: **cro-fix** had only 3 fresh targets (Versed, Transparent Labs, Cuts Clothing), under the threshold of 4. static-ad had 6. Template Showcase still sources from replo-rebuilds, so it was not treated as an active stream for this pool. Fresh counts after: cro-fix 3 → 8, static-ad 6 → 11.

Each candidate was loaded live at 390x844 and the screenshot viewed before the issue was written:

- **Fly By Jing** (food-beverage-supplements, Collection Page): two competing prices per card (regular plus a members band), only two products above the fold, chat pill over the second row.
- **Fishwife** (food-beverage-supplements, Collection Page): the first screen is a translucent promo banner, zero products above the fold. Domain is eatfishwife.com, not fishwife.com (an unrelated restaurant).
- **Topicals** (beauty-skincare, Homepage Section): a "Scratch to win" floating pill covers the hero's only Shop now button.
- **Bala** (fitness-wellness, Homepage Section): hairline headline over busy video that never says what is sold, ghost CTA, clipped promo marquee.
- **Brightland** (food-beverage-supplements, Homepage Section): seasonal "Hello, Cozy Season" hero with no value prop, "Mystery Discount" pill over the first product card.

Screened and not added: Western Rise (store closed), Pact (collection page clean on mobile, better as a reference than a before/after), Wild One (clean, weak issue), Kotn, Graza and Olivers Apparel (pages did not render through the sandbox proxy, so nothing could be verified). The fashion-apparel gap (1 target) is still unfilled; worth prioritising next refresh. Nothing was selected, used or published.

### 2026-09-18 — Builders approved for rebuilds, Static Ads default to prompt packs, Tips back to the old style, Instagram paused

- **Rebuilds move to external builders.** CRO Fix rebuilds and redesigns of real businesses (not store templates) are now built in Lovable / Figma Make / Claude Design / v0, driven by Claude over MCP from the page-build brief, then captured and turned into the post. `CLAUDE.md` "AI Workflow Architecture" rewritten to allow it. **Rebuilds stay private**: no public deploy or share link for a real brand's page.
- **Image fallback order:** gpt-image → Cloudinary `generate-image` (free, 50/month; 50/50 used on 2026-09-18) → builder image gen (rebuild heroes only) → prompt pack.
- **Static Ads default to the prompt pack.** No image API call unless Ridwan asks for rendering in that request. Scheduled runs always export the pack. Project skill copy updated; account skill update proposed.
- **Tips: old-style format** (`docs/system/tips-old-style-format.md`), from `references-for-posts/`. Covers must never be boring: a strong visual, or a type-led "90 content ideas" style cover with line-art diagrams.
- **Handle rule relaxed:** `@koolestpro` allowed on every slide (Tips: footer on every slide). The audited brand's logo stays on the CRO cover only.
- **Instagram paused** after a `scraping_warning`. Investigation in `docs/system/instagram-warning-investigation-2026-09-18.md`: API posting (4 posts) and the lead-gen tools don't use the logged-in session; the strongest lead is carousel-downloader sites + an image-downloader extension used ~30 min before the warning. Trend radar's Instagram browsing disabled.
- **Saved for later:** the audience-growth version + Reels/TikTok plan (`docs/audience-growth-v3-prep.md`), with the "90 content ideas" post as its reference.

### 2026-09-07/08 — Step 10 is no longer documentation-only: TikTok drafts LIVE, and the Instagram blocker turned out to be obsolete

Step 10 has said "documentation only, nothing built" since 2026-07-30. That is no longer true for the TikTok half, and the Instagram half was blocked on a requirement that no longer exists.

**TikTok: the open question is answered by testing, not argument.** The 2026-09-04 disposition left one thing unresolved, whether inbox-only drafting needs production app review given the 2026-08-19 rejection. It does not. Refreshed the sandbox token and ran a live inbox init successfully; scope is `user.info.basic,video.upload` with the refresh token good for another ~338 days. `creator_info/query` returns `scope_not_authorized`, which is correct rather than a problem, because that endpoint belongs to `video.publish` (direct post) and this project deliberately does not hold it.

Two tools shipped. `tiktok_push_draft.py` pushes to the inbox, refreshing the token every run and writing the rotated pair back into `.env` atomically so a scheduled run can never fail on the 24h expiry. `build_tiktok_video.py` produces the 1080x1920 video.

**The old prototypes are gone from the project.** `build_v3.py`, `waypoint_scroll_capture.py`, `select_bg_music.py` and `outputs/tiktok_mockup/` no longer exist; only this plan and the memory files still describe them, which is exactly the kind of stale reference worth flagging rather than quietly working around. Instead of resurrecting five one-off prototype styles, `build_tiktok_video.py` rebuilds the single format that actually produced clients (the silent "watch a store get built" scroll video that brought in Jellys Glamour and two PageFly clients), by reusing `scroll_video_raw.py` and `frame_video.py mobile` at a 1080x1920 canvas rather than inventing new capture tooling. Verified end to end against halos-pdp-01: 26.4s, 3.9MB, frames extracted and inspected.

`koolestpro-tiktok-weekly` (Thursdays ~09:11) now runs it, following `.ai-workflow/tiktok-weekly-procedure.md`. Rotation is tracked by a new `usedForTikTok` flag on `replo-rebuilds-pages.json`, deliberately independent of `usedForTemplateShowcase` since a page can serve both. `assets/fonts/` is new (Syne, DM Mono) so burned-in video copy uses the real brand faces.

**Instagram: Blotato is not needed, and neither is the Page link.** The 2026-07-29 plan named Blotato as the likely lever for the Page↔IG restriction. That premise is dead. Meta's *Instagram API with Instagram Login*, live since July 2024, publishes to a professional Instagram account with no Facebook Page required at all. Every attempt since 2026-07-22 was fighting a requirement that had already been removed, which is why no amount of Business Suite debugging was ever going to clear it.

The existing app could not use it (App type None, only offered the legacy Facebook-login product, not convertible), so a second app was created with Ridwan's approval: **Koolestpro Publishing**, Instagram app ID `930775432950893`, redirect URI on the already-live `koolestpro-portfolio.vercel.app/oauth-callback/`, `@koolestpro` added as Instagram Tester, and both `instagram_business_basic` and `instagram_business_content_publish` marked "Ready for testing". The old app is untouched and still owns the Facebook branch. `.ai-workflow/tools/instagram_client.py` handles auth and publishing. Remaining work is the authorize round trip and repointing Make modules 300-307 at `graph.instagram.com`.

**Instagram shipped the same round, 2026-09-08.** The app was authorized against `@koolestpro` (BUSINESS, 53 media), a long-lived token was stored in `.env` and the Make datastore, and Make modules 301/302/304/306 were repointed to `https://graph.instagram.com/v20.0/...` with `instagram_page_access_token`. The Facebook branch was not touched. Verified against the live blueprint after saving, not just in the editor.

Verification caught a real bug that would have undone the whole thing within hours: **module 201**, the datastore write that runs after every X token refresh, lists the fields it writes and `instagram_page_access_token` was not among them, so the next refresh would have blanked it. Same failure this module was patched for once before. Fixed. Any future field added to `koolestpro-config` has to be mirrored in module 201 or it survives only until the next X refresh.

Two mechanical notes for whoever edits this scenario next. Make's URL field treats a typed `/` as a variable-search trigger and drops it when the popup is dismissed, so retyping a full URL corrupts it; double-click the word `facebook` and type `instagram` instead. And `Escape` closes the module dialog discarding every edit in it, which cost one full round of work here.

One item is genuinely open: the token expires 2026-11-07 and refresh is not automated. `instagram_client.py refresh` handles it, and the refreshed value must also be written back to the Make datastore.

**`bootstrap_env.sh` was rewritten** after a cold sandbox exposed two real failures: `python3 -m playwright install` cannot resume, so it restarts a 195MB download on every attempt and never finishes inside the command ceiling; and extracting browsers into `~/.cache` fills `/sessions` to 100%, which is the same partition problem the entry below describes from a different angle. It now uses resumable `wget -c` and `PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers`. Warm start is ~1s.

### 2026-09-07 — Sandbox home partition fills up mid-run and silently deletes the Playwright chromium binary between bash calls

Hit live during this week's `koolestpro-weekly-cro-fix` run (Caraway). `/sessions` (the home directory, separate from the `mnt/` project mounts which have tens of GB free) is only ~9.8GB and was already near-full before this run started. Two things compounded:

1. `pip install rembg` pulls in `numba`/`llvmlite`/`scipy`/`scikit-image` as transitive deps — ~350MB of packages for a one-shot background-removal call. Uninstall these right after use (`pip uninstall -y rembg numba llvmlite scipy scikit-image networkx pymatting onnxruntime --break-system-packages`) rather than leaving them installed for the rest of the session.
2. Failed/partial `playwright install chromium` attempts (timeouts, ENOSPC) leave `/sessions/*/tmp/playwright-download-*` directories behind, sometimes 300-400MB total, that never get cleaned up automatically. These need `rm -rf` before retrying, or the retry fails at the same point every time for the same reason.

**The real trap:** a `playwright install chromium` that completes successfully inside one bash call is NOT durable across separate bash calls in this environment — something (most likely a disk-pressure-triggered cache eviction, since it only ever happened when `/sessions` was near 90%+ full) removed the installed `chrome-linux/` directory between calls more than once this run, even though the tool had reported success and a browser launch had already been verified working immediately after install. Re-running `playwright install` from scratch each time is slow (~90-170s, sometimes exceeding a single call's timeout) and not guaranteed to finish before the call is killed.

**Working fix:** download the chromium build directly with `curl` (fast, ~40s for the ARM64 build from `cdn.playwright.dev/dbazure/download/playwright/builds/chromium/<rev>/chromium-linux-arm64.zip` — check `python3 -m playwright --version`-adjacent driver files or a fresh `playwright install --dry-run` log for the current revision number), `unzip` it straight into `~/.cache/ms-playwright/chromium-<rev>/chrome-linux/`, `chmod +x chrome-linux/chrome`, and `touch INSTALLATION_COMPLETE` — then immediately run whatever needs the browser in the SAME bash call, before risking another eviction. This sidesteps `playwright install`'s own retry/mirror-fallback logic (which was itself burning time hitting multiple CDN mirrors on ENOSPC) and finishes well inside a single call's budget.

**Also worth doing preemptively at the start of any run that will need Playwright:** `df -h /sessions` first. If it's above ~85% used, clean `/sessions/*/tmp/playwright-*` and any leftover ML model caches (e.g. `~/.u2net`, `~/.cache/pip`) before attempting any install, rather than discovering the ENOSPC mid-install.

### 2026-08-27 — Manual Draft→Ready approval gate removed; `populate_sheet.py` now defaults every row to "Ready"

Ridwan's explicit call, unconditional (not gated on `qa_status`). `populate_sheet.py` (Step 5) previously wrote every new queue row as `status = "Draft"` and Step 6 was Ridwan manually flipping approved rows to `"Ready"` in the Sheet before Make.com's posting scenario (6565331) would touch them. That manual gate is now gone: new rows are written straight to `"Ready"`, including rows where `qa_check.py` found problems (`qa_status` starts with `"Needs Review: ..."`). `qa_status` still rides along on every row for visibility, but it no longer blocks anything from being posting-eligible.

**Why this matters going forward:** the "keeping human approval before anything is published" / "publishing requires Ridwan's approval in v1" language earlier in this doc (Operating Principles, Process Overview) is now stale for the `status` gate specifically — there is no more human checkpoint between generation and posting-eligibility other than Ridwan glancing at `qa_status` in the Sheet himself. If a QA-failed row needs to be caught before it goes out, that now has to happen either by Ridwan reading `qa_status` directly, or by a future automated check (e.g. teaching `koolestpro-distribution-health-check` to flag `qa_status` = "Needs Review" rows separately from missed/overdue ones, since right now that task only reads `status`/`posted_at`, not `qa_status`, to decide what's "blocked").

Also updated for consistency: `sync_content_system.py`'s defensive fallback (`r.get("status", "Draft")` → `"Ready"`) for rows that somehow lack a `status` key when synced into `ridwan_content_system_updated.html`.

### 2026-08-21 — Root-caused the long-standing "Playwright goto hangs" problem: cdnjs and Google Fonts are blocked in this sandbox

The 2026-07-31 note inside `export_tip_slides.py` described `page.goto()` hanging on a finished tips file as a mystery ("even though cdnjs/fonts.googleapis/Cloudinary all individually respond in a few seconds via curl"). That premise was wrong. Tested directly this run: **`cdnjs.cloudflare.com` and `fonts.googleapis.com` are NOT reachable from this workspace at all** (curl hangs with no response), while `unpkg.com`, `cdn.jsdelivr.net`, `fonts.gstatic.com` and Cloudinary all respond normally. Every generated carousel loads html2canvas and jsPDF from cdnjs via blocking `<script src>` tags in `<head>`, so the parser stalls and DOMContentLoaded never fires.

The second, quieter half of this mattered more: the blocked Google Fonts CSS meant any export that *did* complete would have rendered in a fallback typeface. A visual QA pass on slides set in the wrong font is close to worthless, and nothing in the pipeline would have flagged it.

**Fix — `.ai-workflow/tools/sandbox_cdn_route.py`** (new, shared): a Playwright request-routing helper that fulfils cdnjs, Google Fonts CSS, and jsdelivr woff2 requests from a local cache in `.ai-workflow/tools/offline_assets/` (html2canvas 1.4.1, jsPDF 2.5.1, and Syne/DM Mono woff2 files pulled from unpkg/jsdelivr). Exposes both `install_routes` (sync) and `install_routes_async`. `export_tip_slides.py` now calls it. **The HTML files are deliberately left untouched** — they keep their cdnjs and Google Fonts URLs, which work fine on Ridwan's own machine. This is a test-harness concern only, not a change to the deliverable.

**Also new: `.ai-workflow/tools/nav_click_test.py`** — the live nav click-through that `koolestpro-tips-weekly` Step 4 has required since the 2026-07-29 orphaned-markup incident existed only as ad-hoc inline scripts written fresh each run. Now a real reusable tool: clicks through every slide via the swipe button and asserts pager position, track transform equals `-idx*540`, the swipe button stays pinned to the card's right edge and vertically centred, that it hides on the last slide, and that there are zero console/page errors. Usage: `python3 .ai-workflow/tools/nav_click_test.py outputs/tips/<file>.html`.

**Chromium bootstrap note:** `bootstrap_env.sh` step 3 still falls back to `python3 -m playwright install chromium`, which is not resumable and gets killed by the ~45s command ceiling on a cold sandbox. The README's manual resumable-curl recipe is still the reliable path (build 1234 as of this date). Worth folding that recipe into the script itself at some point rather than leaving it as documentation.

### 2026-08-21 — Tips carousel: mobile thumb zone (weekly buffer run)

`outputs/tips/thumb-zone-mobile-reach_2026-08-21.html`, 7 slides, Myth vs Reality, Digital Craftsmanship pillar. Topic came from the April backlog (trend-radar-log.json's latest entry is 2026-W33, stale against the current 2026-W34, so the documented fallback applied). Updated the existing backlog item in place by its original id rather than creating a new one; its `type` moved from "CRO Fix" to "Tip" so the record matches the artifact that actually got built.

**Deliberately did not use the metric the backlog item asked for.** That April idea's brief called for "heatmap-informed corrections for Nigerian mobile traffic patterns" and an angle "backed by actual African mobile usage data." No such dataset exists in this project, so the carousel is built on Apple's published 44pt and Google's 48dp minimum tap targets instead, which are real and citable. The item's `brief`/`angle` fields were rewritten to describe what was actually made. Worth watching for elsewhere in the April/May backlog: several of those auto-generated ideas assume data this project has never had.

Two export-only rendering bugs found by looking at the PNGs rather than the markup, both fixed in the builder: html2canvas does not honour `overflow:hidden` on an absolutely-positioned child, so the cover's thumb-reach arc bled outside the phone frame (fixed by bounding both arc layers by construction, one as a radial-gradient background on an `inset:0` div, one as an inline SVG clipped at its own declared width/height); and the stat slide left ~22% dead bands top and bottom, fixed by adding a 44pt-vs-28px tap-target comparison that both fills the frame and makes the number concrete.

### 2026-08-19 — Static Ad Twitter backfill exposed a cross-brand asset-URL collision bug in feed_media.py, fixed same day

While backfilling the new 5-post Twitter cadence (below) across Obvi, Bebemoss, and Material Kitchen's already-queued Static Ad items, an md5 spot-check on the freshly hosted Cloudinary URLs turned up a real bug, not just a caption gap: `feed_media.py` built its Cloudinary `public_id` from only the first 2 hyphen-tokens of `pipeline_item_id` (`"static-ad-{brand}..."` → `"static-ad"`), so every Static Ad item of any brand shared the exact same Cloudinary path for `ad-1`/`ad-2`/`ad-3`/`ad-4`/`combined-showcase`. Confirmed live: V1CE and Material Kitchen's entire Static Ad row sets (10 rows, already pushed to the live Sheet earlier that day) were serving whichever brand's image had been uploaded last — Material Kitchen's Twitter/Instagram rows were pointing at V1CE's actual ad images and vice versa.

**No real damage** — all 10 affected rows were still `status: Draft` in the live Sheet (Ridwan hadn't reviewed/approved them yet), so nothing was ever posted with the wrong creative. Fixed: `feed_media.py`'s prefix now uses the full `pipeline_item_id` (already unique per item) instead of the truncated split. Repaired the already-live Sheet rows via a targeted `batchUpdate` on column P (asset_urls) only — `append_sheet_rows.py` has no update path by design, so this required a one-off manual patch, same pattern as the 2026-08-02 stale-caption repair. Verified with md5 hash comparisons between each corrected Cloudinary URL and its local source file before treating the repair as done. Full technical writeup in `.ai-workflow/tools/DISTRIBUTION.md`.

**Standing lesson:** any time a feeder script's hosting path is derived from a truncated/split identifier rather than the full unique id, treat it as a collision risk — worth an md5 spot-check the first time a new brand/item type runs through it, not just a "did it upload something" check.

### 2026-08-19 — Static Ad Twitter cadence widened 3→5, scattered across the week

Ridwan's instruction: "static ads can generate more than just one post, we should be making 5 posts from static ads but it should be scattered into the schedule date" — clarified on follow-up to mean Twitter specifically (X posts from 3 to 5), not a new platform.

`populate_sheet.py`'s `CALENDAR["Static Ad"]` Twitter block changed from 3 slots clustered on Fri/Sat/Sun (13:00/09:00/18:00) to 5 slots, one per distinct static-ad asset (the 4 individual angles — problem/solution, benefit/result, social proof, offer/urgency — plus the combo showcase), spread Mon 09:00 / Tue 13:00 / Wed 18:00 / Fri 13:00 / Sat 18:00. Verified no collision with any other stream's existing Twitter day+time slot before landing this. Instagram and LinkedIn Static Ad cadence unchanged (still 2 Instagram rows, 0 LinkedIn rows — LinkedIn was explicitly not part of this ask).

Caption supply didn't change alongside it: the static-ad-image skill still only writes 3 X caption variants per run, so `caption_text()`'s modulo cycling means the 4th/5th Twitter slot reuses an earlier variant rather than getting a unique one — this surfaces as a `populate_sheet.py` warning (flag, not block), same as any other caption-variant shortfall in this pipeline.

**Backfilled same day, per Ridwan's follow-up ("update the schedule task instructions to make it global" → clarified as "backfill across ALL existing Static Ad items").** Obvi, Bebemoss ginger, and Material Kitchen trio (the 3 items still on the old 3-post cadence at the time) each got their 2 missing Twitter rows (ad-1 and ad-4) added directly to the local queue — not by re-running `populate_sheet.py`'s full CALENDAR (which would have duplicated ad-2/ad-3/combo under new day/times instead of cleanly adding just the missing 2), but by building only the 2 new slots and merging them in alongside the existing 5 rows. Captions for ad-1/ad-4 came from each brand's `{brand}-social-content.json` (SA-{BRAND}-X1/X2) rather than a fresh `harvest_content.py` pass, because these older Static Ad companion pages use `.capbox`/`.xpost`/`.section-label` classes instead of the `.copy-block`/`.x-post`/`.section-title` classes `harvest_content.py` expects — a real harvester compatibility gap, not fixed here, worth a look if more pre-2026-08 Static Ad pages need re-harvesting. V1CE didn't need backfilling since it was generated fresh under the new 5-slot calendar already. This backfill is also what surfaced the cross-brand Cloudinary collision bug documented above.

### 2026-08-02 — Live distribution Sheet: health audit, stale-caption repair, formatting pass

Ahead of Monday's next `append_sheet_rows.py` run, Ridwan asked for the live 58-row Sheet to be checked for the reported X-post asset-size bug and generally put in good shape before more rows land. Two findings, both fixed directly in the live Sheet (not local queue.json, which was already correct):

- **Asset-size/type bug (the originally reported one): confirmed zero remaining instances.** Audited all 69 unique asset URLs referenced in the sheet against X's real media limits — Ridwan's own manual fix for the "8.8MB LinkedIn PDF matched to an X row" bug fully resolved that bug class.
- **5 stale over-280-char captions found and fixed.** These were rows Ridwan had imported into the live Sheet from a local export taken *before* the 2026-07-29 caption-splitting fix (see below) had propagated to them — `append_sheet_rows.py` is deliberately append-only and never touches existing rows, so the fix never reached them. Pushed corrected caption text directly into the live Sheet via `batchUpdate`. **3 of the 5 were already `status: Posted`** — flagged to Ridwan to spot-check the real @koolestpro account at those timestamps, since the Sheet alone can't confirm whether those specific posts went out truncated or were already caught and fixed manually.
- **Sheet reformatted for review:** frozen header row, basic filter, sorted by scheduled_date → scheduled_time_local → platform, dropdown validation on platform/status/stream, text-wrap on long-text columns (caption, qa_status, asset paths/urls, caption_json), auto-resized row heights, fixed column widths. One-time repair, not a new recurring script — `append_sheet_rows.py` remains the only automated write path. Full detail in `.ai-workflow/tools/DISTRIBUTION.md`'s "Live Sheet health audit + formatting pass" section.

### 2026-08-02 — Growth Operating Plan created; content re-scoped into a two-mode model

A structured planning interview (`process-interviewer`) produced a new sibling doc: **`docs/koolestpro-growth-operating-plan.md`**, covering destination (domain + selling site), proof, prospect intelligence, two separate market engines (Nigeria/Africa and international), search, and a gated ads plan.

**The finding that matters for THIS doc — corrected mid-interview, so read the corrected version, not the first one:**

An initial pass concluded that content had produced zero paying clients. That was **wrong, and a second pass was still wrong**. The corrected count: **six clients trace to content.**

| Format | Clients |
|---|---|
| **TikTok build videos** (no voiceover, music, watch a store get built) | Jellys Glamour, who saw the videos and came to his DMs, plus two foreign PageFly clients |
| **LinkedIn/YouTube teaching content** | aminazaid.com → referred justdarlings → referred scentsavenue.ng |
| Fiverr | Tap and Rate, Champion Biotics |
| Outbound | None — never sent |

Content is Ridwan's strongest channel. What changed is **what the content asks for**:

- **Old content** — "watch me build a store", "here's how to fix yours". A **service signal**. Buyers responded.
- **Current content** — CRO craft carousels showing build quality. An **employment signal**. Recruiters and interviewers respond; Ridwan's words: *"I keep attracting recruiter and getting on interviews but I have not secured a project yet."*

Neither is bad content. The production machinery (Steps 1-11) is sound and stays exactly as-is. Two things change:

1. **Every CTA in craft-mode content now points at a real destination** — a service page or case study on the domain — instead of at engagement.
2. **The two formats that actually sold get restored** as a separate buyer-facing layer (Track F/F1a of the growth plan): teaching content, and an **automated weekly TikTok video** built from the artifacts Step 3's CRO Fix run already produces (hook clip → before scroll → transform → after scroll → end card, no voiceover). Craft mode is not asked to do a job it was never shaped for.

Two other findings from that interview belong here:

- **Step 7 (outreach assets) has never actually run.** `outreach_tracker.json` holds two records — V1CE and Obvi — both `"Not Contacted"`, created 2026-07-12 and untouched since.
- **Step 1's target pool is nearly empty and is now dual-purpose.** `targets_pool.json` had 12 targets, all `Available`. It gains a `segment` field (`nigeria-local` / `international-dtc`) and serves both content selection and outreach from one file, so the two compound instead of forking.
- **`about-me.md`'s "Active Client Projects" list was stale** — imported from an earlier ChatGPT memory, mostly dead dropshipping stores. Corrected 2026-08-02.

Two findings from that interview are direct consequences of this plan and belong here:

- **Step 7 (outreach assets) has never actually run.** `outreach_tracker.json` holds two records — V1CE and Obvi — both `"Not Contacted"`, created 2026-07-12 and untouched since. Every Saturday this system rebuilds a real brand's page for free and the brand owner never hears about it. Track C of the growth plan fixes this.
- **Step 1's target pool is nearly empty.** `targets_pool.json` has 12 targets, all `Available`. At the growth plan's ~20 prospects/week, that is under a week of supply. An Apify-backed weekly refill task is now a required build, not an optional one.

### 2026-07-30 — Trend & Format Awareness Engine planned (Step 11), Apify credentials wired, Charlie Hills' social-media-skills repo evaluated

Ridwan wants a V3 push: keep Tips carousel topics trend-aware instead of cycling the same angles, and catch competitor/adjacent-creator content formats (any medium — image, carousel, infographic, video) that are getting real engagement and that Ridwan isn't doing yet. Prompted by two things he shared: a LinkedIn creator's (Charlie Hills) public Claude-skills repo, and X's own newly-official developer docs for AI-agent access (`docs.x.com/tools/mcp`, `docs.x.com/tools/skill-md`).

Evaluated Charlie Hills' `social-media-skills` repo (github.com/charlie947/social-media-skills, MIT, 1.5k stars) in full via its README plus the raw SKILL.md files for `post-scorer`, `post-formatter`, and `content-matrix`. Its `niche-research` skill drives Claude-in-Chrome to browse X/Reddit/Google — free, but scraping-fragile. Decided to use real APIs for X and Reddit instead, since the cost is trivial at the volumes needed, keeping Claude-in-Chrome only for Instagram, where no trend-discovery API exists at all (confirmed: the Graph API's Hashtag Search only returns posts for an already-known hashtag, capped at 30/week, and requires the same Page↔IG link currently blocking Instagram posting per `project_instagram_automation_blocked`).

Checked X's API pricing directly (web search, 2026): the old subscription tiers closed to new signups in February 2026, replaced by pay-per-use ($0.005/read). Reddit's own commercial API floors at $12,000/year, but third-party resellers exist at roughly $0.002/read. Both are cheap enough at the capped volumes this needs (~50 X reads/week, ~100 Reddit reads/week) to land near $1/month each. Full budget reasoning and caps are in Step 11 above.

**Apify wired for real, separate from this step's core scope.** Ridwan wants `post-scorer` and eventually `reels-scripting` from the same Charlie repo. Found his Apify credentials (an `apify_api_...` token plus a `fxaxqSdyGIK6xVyDE` user ID) and saved them to this project's `.env` as `APIFY_API_TOKEN`/`APIFY_USER_ID`. The Cowork "Apify" MCP connector itself stayed unauthenticated even after Ridwan updated it on his end (repeated `mcp__Apify__search-actors` calls still failed "User was not found or authentication token is not valid" on retest) — worked around by deciding future Apify use (`post-scorer`) will call the REST API directly via script with the `.env` token, same pattern as every other third-party key in this project, rather than depending on that connector.

Full spec written to Step 11 above. Nothing is built yet beyond the `.env` addition — no new skill file, no scheduled task change, no `content_pipeline.html` UI change. Same "plan first, build once decisions are settled" pattern as every other stream in this doc.

### 2026-08-02 — Live Sheet↔local queue append automation built (OAuth device flow, service account blocked by org policy)

Same session where Ridwan revealed he'd already imported the 58-row queue into the "Koolestpro Distribution Queue" Sheet himself, was flipping rows to Ready, and Make was actively posting — confirmed live by reading the Sheet directly (real `Posted`/`Ready` statuses with `posted_at` timestamps not present in local `queue.json`). The weekly assembly task's first-draft Step 6 ("re-import queue.csv, replace current sheet") would have silently overwritten all of that on its first run — caught and corrected before any run happened.

Built a real append mechanism instead. First attempt: a Google Cloud service account, standard pattern — blocked immediately by an org policy (`iam.disableServiceAccountKeyCreation`, part of Google's newer default security baseline on new Cloud projects) that prevents generating a key even after Ridwan flipped the policy to Inactive at the project level. Rather than keep fighting an org security policy, switched to an **OAuth client** (type "TVs and Limited Input devices," project "Koolest Automation") — sidesteps the blocked policy entirely since it isn't a service-account key. One-time device-code authorization: Ridwan added himself as a Test User on the OAuth consent screen (required while it's in "Testing" publishing status — first attempt failed with `access_denied` before this), then visited google.com/device, entered a short code, signed in as `sirridwan721@gmail.com`, approved. Credentials (`GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN`) now live in this project's `.env`, same pattern as its other API keys.

New `.ai-workflow/tools/append_sheet_rows.py`: reads existing `post_id`s straight from the live Sheet via a real Sheets API call, diffs against local `queue.json`, appends only what's missing. Cannot touch an existing row by construction — no update code path exists. Verified live in `--dry-run` against the real sheet: correctly found 0-of-58 new (everything Ridwan already imported matched), confirming the diff logic before any write was ever attempted. Wired into `koolestpro-weekly-distribution-assembly`'s Step 6, replacing the old manual-paste fallback as the primary path (manual-paste is now only the fallback if auth has lapsed).

**Known limitation, not yet resolved:** the OAuth consent screen is in "Testing" status, and Google caps refresh tokens for Testing-status apps at 7 days regardless of activity. `append_sheet_rows.py` will start failing with an auth error roughly weekly until Ridwan switches the project's publishing status to "In production" (Google Cloud Console → "Google Auth Platform" → Audience) — no Google verification review needed for a single-user app, just a one-time "unverified app" click-through on the next re-auth. Until he does that, expect to redo the device-flow approval periodically; the assembly task falls back to its old safe paste-ready-block behavior whenever that happens, so nothing breaks silently.

### 2026-07-29 — X/Twitter over-length caption bug fixed; weekly distribution assembly task built

Ridwan reported live posts/queue entries reading as multiple tweet templates glued into one post, and a "thread" posting as one giant post instead of a thread. Root-caused with real numbers: 8 of 30 Twitter rows in the queue were over 280 chars (up to 921). Cause was structural, not random — CRO Fix's "Twitter Angles" (3 alt single tweets) and "Twitter Thread" (a 5-part script) tabs write all their variants into ONE `<pre>` blob as human-readable plain text (`"Tweet A (...):"` / `"ANGLE A:"` / `"1/ ... 2/ ..."`), instead of separate DOM elements the way Static Ad/Template Showcase's `.x-post` divs already are. `harvest_content.py` had no way to split a blob it couldn't see structure in, so a single-tweet slot got all 3 variants glued together, and the thread slot got all 5 tweets glued into one post (Make has no real reply-chained threading built — that's still an open fast-follow, flagged in `docs/x-twitter-distribution-setup.md`). Worse: the 280-char check in both `populate_sheet.py` and `qa_check.py` only ever ran on list-typed/compact-field values, so it silently never fired for this exact case.

**Fixed, in `.ai-workflow/tools/`:**
- `harvest_content.py` — `parse_tab_captions()` now recognizes and splits both label conventions (`"Tweet A (...):"` and `"ANGLE A:"`) plus numbered thread lines (`"N/ "`) into real lists instead of one opaque string; also prefers per-variant DOM (`div.tw-block`) when a skill already provides it, and strips UI chrome (`.post-label`, `<button>`) out of the panel-text fallback so it never leaks into a caption again.
- `populate_sheet.py` — the `X_CHAR_LIMIT` check now runs on the final resolved caption text unconditionally, not only when the source happened to be a list. CRO Fix's Wed "thread" Twitter slot (`caption_key: x_thread`, `fmt: thread`) is downgraded to a normal single tweet drawing from the same `x_angles` pool as the Fri/Sun slots (Ridwan's call — ship correctly today, revisit real multi-tweet threading later) — all three Twitter slots now rotate through 3 distinct pre-written angles instead of one being broken.
- `qa_check.py` — `check_x_caption_lengths()` now scans every X-flavoured key in `captions_full` (`x`, `x_singles`, `x_angles`, `x_thread`) directly, not just the compact `captions.x` field that tab-based skills (CRO Fix, Tips) never populated.
- New `.ai-workflow/tools/feed_media.py` — Instagram/Twitter's asset-hosting equivalent of `feed_linkedin.py` (which only ever handled LinkedIn's video/PDF-carousel case). Uploads each image/video individually (never combined into a PDF — X/IG's APIs take direct media URLs), same idempotent Cloudinary-cache pattern.

**Live queue repaired:** re-harvested and re-populated the 6 broken CRO Fix rows (V1CE + Material Kitchen) with the fixed code; hit and fixed a known "join fragility" case live (CRO Fix's click-time-based id didn't match the SYNC_DATA item id, which first created 10 orphaned duplicate rows before being caught and corrected — the new weekly task's instructions explicitly call this gotcha out so it isn't repeated unsupervised). Trimmed 3 further over-length Template Showcase (V1CE PDP) X posts by hand — their source companion HTML no longer exists on disk (`outputs/templates/v1ce_tap-review-card-pdp_2026-07-12/`), which also violates CLAUDE.md's File Linking rule; flagged in that row's `qa_status` rather than silently fixed. Confirmed post-fix: 58/58 queue rows still Draft (nothing was ever live-posted with the bug), 0 rows over 280 chars.

**New gap closed — nothing was assembling generated content into the calendar automatically.** Read all 4 weekly generation tasks' prompts directly and confirmed none of them call `harvest_content.py`/`qa_check.py`/`populate_sheet.py` — the whole harvest→QA→populate→feed→sync chain only ever ran when triggered by hand in an interactive session. Built `koolestpro-weekly-distribution-assembly` (Monday 07:51, ahead of `koolestpro-target-pool-refresh`): finds SYNC_DATA items with `status: "Created"` and no `distribution[]` yet, runs the full chain on each, hosts new assets via `feed_linkedin.py` + `feed_media.py`, re-imports the refreshed CSV into the Google Sheet, and ends with a digest calling out every `Needs Review` row — Ridwan's Draft→Ready approval gate is unchanged, this task never sets anything to Ready.

### 2026-07-29 (third pass) — First working TikTok mockup with voiceover, music, and marker callouts; YarnGPT attempted but blocked by Google Drive quota

Ridwan reviewed the first (silent, zooming, framed-card) mockup and asked for four changes: (1) real voiceover, (2) real background music from an API already in the stack, (3) no camera zoom/pan, full mobile width instead of a bordered card, and (4) a moving marker/pointer calling out specific elements instead of just caption text, ending on a CTA card. He explicitly did not want to spend money to get this working.

**YarnGPT (Nigerian-accented open-source TTS) — attempted in full, blocked by an external quota, not a setup failure.** Installed torch/transformers/torchaudio (via direct wheel downloads with `wget -c`, resumed across multiple calls to work around this sandbox's ~45s command ceiling — pip's own resumability is unreliable for large wheels, direct wheel URLs + `wget -c` is the reliable pattern going forward for any future large Python package in this sandbox), vendored the actual `wav_tokenizer` decoder/encoder source directly from the OuteTTS GitHub repo (32 small files, avoiding the full `outetts` PyPI package which pulls in llama-cpp-python/whisper/pygame/etc. that aren't needed just for audio decoding — patched one real upstream bug, a missing `import typing as tp` in `decoder/models.py`). Downloaded the WavTokenizer yaml config fine. The actual model checkpoint (`wavtokenizer_large_speech_320_24k.ckpt`, ~2GB) is hosted on Google Drive and got to 1.73GB downloaded (resumable, same partial file persists across calls) before Google Drive's shared-file quota kicked in: "too many people have downloaded this file... try again in up to 24 hours." This is Google's limit on that specific link, not fixable from this session. **To resume:** re-run the same `gdown.download(id='1-ASeEkrn4HY49yZWHTASgfGFNXdVnLTt', output='wavtokenizer_large_speech_320_24k.ckpt', resume=True)` call (working dir needs the vendored `wav_tokenizer/` folder + config yaml, all of which are disposable/regeneratable from GitHub+HuggingFace if the scratch dir is gone) once 24h have passed, or try an off-hours retry sooner in case the block is shorter in practice.

**What shipped instead, free and already working:** this project's own `video-gen/_staging4/text-to-speech` skill (`tts.py`), wrapping Groq's Orpheus TTS (`canopylabs/orpheus-v1-english`, voice `troy`) against the existing `GROQ_API_KEY` — confirmed live, no new signup, no spend beyond an already-funded balance. (OpenAI TTS was tried first per that skill's own docs but the `OPENAI_API_KEY` is out of quota — 429 `insufficient_quota` — so Groq is the only currently-working provider from that skill until the OpenAI balance is topped up.) Background music came from Freesound (`FREESOUND_API_KEY`, already in `.env`) — "Inside Technology (loop1)", CC BY-NC 4.0, mixed at low volume under the voiceover. **Flag for later:** BY-NC license technically restricts commercial use — fine for this internal test, but if this specific track ships in a real posted video, either swap for a fully-commercial-cleared track or confirm BY-NC is acceptable for promotional content about Ridwan's own paid service.

**New visual technique, reusable for future teardown-style content:** full-bleed static screenshot (crop to fill 1080 width edge to edge, no side margins, no Ken Burns zoom) with an animated orange ring/reticle marker that pops in, holds with a subtle pulse, and slides between callout points on the SAME static frame — before/after cut only happens when the actual page content changes, not for emphasis. Built via a per-frame PIL renderer (`build_v2.py`) driven by the real TTS clip durations (not estimated pacing) so marker movement and the CTA end card land in sync with the voice track; ffmpeg only does zoompan-free encode + audio mux at the end. This callout-marker technique is a strong reusable pattern for the "roast/critique" and "hands-only" format ideas from the second-pass research too, not just this one before/after case.

**Still not started:** the actual TikTok posting mechanism (Blotato, deferred per the earlier correction — no spend yet) and Instagram repurposing. This is still a manually-reviewed content-format prototype, not a live posting pipeline.

### 2026-07-29 (later same day, second pass) — Live TikTok/competitor research, format shortlist revised with real evidence

Browsed TikTok live (Claude in Chrome, logged out) across #shopifytips, #shopifystorereview, and #websitecritique to see real accounts in or near Ridwan's niche and what's actually getting views/saves, not just SEO-blog claims. Three accounts gave concrete, checkable numbers:

- **@ecomvso** (4,934 followers, 44.9K total likes) — screen-recording of real Shopify PDPs/homepages inside a browser-frame mockup, bold on-screen caption text revealing the point ("a conversion optimized homepage like this"), light or no voiceover. Individual videos hit 35K-54.6K views despite the small follower count — the format carries the video, not the account size. One video: 1574 likes, 1069 saves, 63 comments. Save-count running near-equal to like-count across their videos is a strong signal people are bookmarking these as reference material, not just liking and scrolling on.
- **@marketingomar** — hands-only real phone-screen recording (an actual finger scrolling/tapping a real product page), two-line bold caption ("LOOKS LIKE THIS WITH..."). 805 likes, 717 saves on a small account. Faceless, tactile, reads as authentic capture rather than a produced mockup.
- **@realdennisdemarino5** — talking-head, direct-to-camera: "I reviewed 148 Shopify stores & found the same mistake across 80% of the stores." 259 likes, 165 saves, and — most notable — an organic comment reading "Pls have a look at mine bro," i.e. the format generated an inbound lead in the comments section itself. Strongest lead-gen signal seen, but requires being on camera, which conflicts with Ridwan's stated preference. Logged as an option, not pushed.

**Revised shortlist (replaces the speculative one below, same three ideas but now evidence-ranked plus one new entry):**

1. **Before/after reveal, TikTok-native cut (new, top pick)** — take the CRO Fix before/after assets Ridwan's pipeline already produces weekly and re-edit them in the @ecomvso style: browser/phone frame, bold caption text doing the talking, fast reveal pacing. This is directly validated at small-account scale and costs zero new production, it's a re-edit of existing weekly output, not new content.
2. **Hands-only real interaction + caption** — record an actual finger scrolling/tapping a real (or rebuilt) product page, per @marketingomar. Faceless, cheap, feels native rather than corporate.
3. **Roast/critique with zoom-cuts** — original idea, still valid, effectively a more produced version of #1/#2 with a reaction energy layered in via voiceover.
4. **POV hook / bold-stat reveal** — original ideas, kept as lower-priority variants once the above are tested.

Competitor self-promotion pattern observed (per Ridwan's ask about how others promote themselves): none of these accounts hard-sell in the caption. The hook/value carries the video, and the ask ("is it free?", "I need help", "pls review mine") comes organically from viewers in comments. Bios are a single value-prop line plus niche hashtags, nothing elaborate. This matches the existing soft-CTA caption style already used in this project rather than requiring a change.

**Not yet built.** Next step is Ridwan picking a format from the four above (or a live side-by-side look at more examples) before anything is produced.

### 2026-07-29 (later same day) — TikTok plan corrected: no spend yet, format style still open

Ridwan pushed back on both parts of the plan below. He is not ready to pay for Blotato (or any paid platform) right now — he wants the content format proven for free first, and will spend once "everything is working perfectly the way I want." He also rejected the implied format direction: no boring scroll-through video, no boring carousel-to-slideshow, nothing that isn't genuinely native to how people actually consume TikTok. He wants to pick the format together by looking at real reference material, not have one assumed.

Researched actual 2026 TikTok content patterns rather than assuming repurposed-asset formats would work. Finding: generic "trending template" packs (CapCut's own trending-template gallery, checked live) are dominated by music/dance/relationship edit trends, not business content, so "download a template" doesn't map cleanly onto CRO/marketing content. What does map: (1) the voiceover-plus-screen-recording / reaction format, well-established in marketing TikTok as page "roasts" or critiques (roastmylandingpage.com is a real business built on this exact demand), which is inherently NOT boring scrolling because the energy comes from reaction pacing, zoom-cuts on the specific broken element, and a spoken verdict, not a slow scroll; (2) POV-style hook delivery, text synced to quick cuts; (3) bold-stat-reveal hook format, common in the faceless finance/productivity niche. All three use CapCut's genuinely free tools (auto-captions, built-in TTS, zoom/keyframe effects) rather than a paid template pack.

**Revised sequencing:** prove the format for free first (manual posting, free CapCut editing, no Blotato yet), get Ridwan's sign-off on which structure feels right, THEN revisit Blotato/paid automation once the format is validated and budget opens up. Step 10 below still describes the eventual automation layer and format rotation, but its "posting layer: Blotato" decision is now Phase 2, not immediate.

### 2026-07-29 — TikTok daily automation planned (Step 10), not yet built

Ridwan wants daily TikTok posting without recording himself, and eventual repurposing of that TikTok output to Instagram once Instagram is unblocked. Researched current (2026) TikTok automation reality: TikTok's own Content Posting API is free but gates public visibility behind an app audit that takes weeks and is strict for smaller accounts — a real blocker for a "just wire it up" approach.

Decided on **Blotato** as the posting layer (already TikTok-audited, so posts publish publicly without Ridwan running his own review; native Make.com module, same integration pattern as the live LinkedIn/X branches in "Koolestpro Social Distribution"; ships a built-in faceless video generator that can directly produce the slideshow-format videos rather than needing new assembly tooling built here). Format mix locked in: HeyGen avatar talking-head (2-3x/wk), repurposed Template Showcase/CRO Fix video (1-2x/wk), text-hook slideshow from Tips/Static Ad assets (2-3x/wk) — chosen to rotate rather than commit to one format, since none of it requires Ridwan on camera.

Flagged two things Ridwan needs to resolve before this goes live: (1) sign up for Blotato and connect the TikTok account — if that account is brand new, TikTok's anti-spam signals mean it should post manually for ~4 weeks first or risk a shadowban; (2) Blotato may be worth trying for Instagram too, since it's a separately-audited layer that could sidestep the Page↔IG linking restriction currently blocking the in-house Meta Graph API build (`project_instagram_automation_blocked`) — worth testing once TikTok is proven, rather than assuming the in-house build needs more debugging.

Full spec written to Step 10 above. Nothing posts yet — this is planning only, same as every other stream before its account credentials existed.

### 2026-07-29 (fourth pass) — TikTok mockup iterated through 3 edit styles, then corrected into 4 content TYPES; Playwright/Chromium bootstrapped from scratch in the sandbox

Continuing the v2 before/after mockup from earlier the same day: Ridwan reviewed it and gave three concrete corrections (v3) — enumerate at least 3 things changed explicitly in the VO/captions, add a visible BEFORE/AFTER badge so it's clear the page changed, and put the screenshot inside an actual phone bezel that doesn't fill the whole frame so the background can be designed separately. All three were built into `build_v3.py` (calibrated iPhone-frame placement, numbered-ring markers, badge + caption compositing) and approved: "This is much better."

Asked what's next, Ridwan chose to try more distinct **edit styles** on the same Material Kitchen case study before moving on. Built two more: v4 (real Playwright scroll-capture footage of the live site vs. the rebuild, composited into the same phone bezel, crossfaded between) and v5 (fast roast/critique cuts with flash-transitions and punched-in zoom crops, no continuous pan since Ridwan had earlier ruled out in-shot panning). Both reused `build_v3.py`'s constants/helpers rather than duplicating geometry. Both approved.

**Real Playwright/Chromium had to be bootstrapped from nothing for v4** — this sandbox has no root and `playwright install` isn't resumable against its ~45s command ceiling. Fixed by finding the exact browser/ffmpeg build numbers Playwright's driver expects (`browsers.json`) and downloading each zip directly via resumable `curl -L -C -` from `cdn.playwright.dev`, extracting into the exact `~/.cache/ms-playwright/<name>-<build>/` paths Playwright looks for. Reusable for any future real-screenshot/video work in this sandbox without redoing the discovery.

**After v5, Ridwan corrected the whole direction, not the execution:** "everything we have been doing is still the same video, just different style and angle... I want us to have different types of posts, not just different styles of the same post... we want to be able to showcase our work... not just here for CRO fixes." This is the important distinction for this stream going forward — TikTok/Reels output should span the pipeline's actual content TYPES (Tip, CRO Fix, Static Ad, Template Showcase, plus general expertise/portfolio content), not keep re-editing one CRO Fix case study in new visual styles.

Asked which type to try first, Ridwan picked **Template Showcase — new build** (portfolio proof, not another fix). Built v6 from the real HALOS PDP (`halos_pdp-01`, already in `replo-pages-cache/` per the 2026-07-18 entry above, unused): wrote `waypoint_scroll_capture.py` (new — supports a curated hold/travel/hold/travel sequence through specific named sections of a long real page, rather than either a single static crop or an unusably fast full-page scroll) to walk hero → "THE PROBLEM" → "HOW IT WORKS" → stats on the real 13,044px-tall page, timed so each hold exactly matches its VO beat's duration. Swapped the BEFORE/AFTER badge for a "NEW BUILD" tag (there's no before/after on a portfolio piece) and closed on the Template Showcase CTA framing ("need a store built," not a CRO pitch, per the existing standing rule). All facts narrated (98% visible results, 4,000+ studies, 60-day guarantee, the 3-step ritual) were pulled directly from the real page HTML, not invented. Verified frame-by-frame against the real page content before delivery — hero, problem section, how-it-works 01/02/03, and stats all landed exactly where their captions claimed.

**Reusable outputs from this pass, all in `outputs/tiktok_mockup/`:** `build_v3.py` (shared base module — bg canvas, badge/caption layer builders, phone-frame compositing, now imported by every later variant), `fixed_scroll_capture.py` and `waypoint_scroll_capture.py` (real-page scroll capture, fixed-distance and multi-waypoint respectively), `composite_v4_clips.py` (frames a raw scroll clip into the calibrated bezel at v3's exact geometry). **Still not built:** nothing posts anywhere yet — Blotato account still doesn't exist (per Step 10 above), so all 4 videos (v3/v4/v5/v6) are manually-reviewed prototypes proving the format/type range works, same "prove it free first" stance Ridwan set earlier today.

### 2026-07-30 — v7: 5th content TYPE (behind-the-scenes/expertise), not tied to any pipeline artifact

Asked which type to build next (Tip / Static Ad / behind-the-scenes-expertise / "you pick"), Ridwan chose behind-the-scenes/expertise. Unlike v3-v6, this one isn't sourced from a pipeline generator's output at all — built fresh as "3 things I check in the first 10 seconds of a new store," Ridwan's own diagnostic process as proof of skill, no rebuild/fix/portfolio-piece being shown.

**Source:** `TAPro` (taprocard.com) from `targets_pool.json` — chosen specifically because it had zero `usedFor` entries in any stream, keeping it distinct from Material Kitchen (already used 3x for v3-v5) and HALOS (just used for v6). Verified live via Playwright rather than trusting the pool's older note: confirmed a tall promo banner sits above the real logo/nav on load, a floating search icon stays fixed on screen and overlaps body content at every scroll depth, and real client logos (CarBravo, Panda Express, etc.) sit three-plus scrolls down.

**New technical issue found and fixed: real-page scroll timing drifts unpredictably, sometimes a lot.** The `waypoint_scroll_capture.py` script (built for HALOS/v6, where drift was ~1.3s and ignorable) produced a raw TAPro capture 6.2s longer than planned, and it wasn't evenly distributed — the first 3 waypoints landed within ~1s of plan, but the final hold effectively froze the recorder on a static frame for ~14s longer than scripted (confirmed by extracting frames every few seconds — t=31 and t=36 were pixel-identical). Root cause not fully pinned down (candidates: rAF-driven easing losing ticks under real network/image load on a live third-party site vs. a local file, or Playwright's video recorder padding a final frame during context-close) — logged as an open question rather than guessed at. Fix that worked: trim the raw capture's dead tail (`ffmpeg -t`) back to where content actually finished changing, verified by sampling frames every 1-3s and eyeballing them, same as the "verify by exporting" principle already standing in this project.

**New technical pattern: ring-marker placement on real video (not a static screenshot).** v3's `to_canvas_xy()` only worked for the static-screenshot pipeline; for real scroll video, built the equivalent mapping from `frame_video.compute_placement()`'s `screen_x/y/w/h` (raw video is 390x844 CSS px, unscaled by device_scale_factor since Playwright's `record_video_size` takes precedence) and verified marker coordinates two ways: first from a rough screenshot read (wrong — landed on the wrong element entirely, circling the promo banner's own CTA button instead of the real logo), then corrected using an actual pixel-grid overlay drawn on the raw frame (right — landed exactly on the TAPRO logo, the floating search icon, and the client-logo row on the second attempt). Worth remembering: eyeballing a thumbnail is not enough precision for marker placement; grid-overlay the real frame first.

**Audio sequencing note:** rather than force each VO beat into a fixed visual window (risking either two voices overlapping or dead air), built the timeline backward from the CTA card's fixed start time so beat 4 (longest, 7.28s) lands exactly when the CTA visual begins, with beats 1-3 anchored close to but not rigidly locked to their visual windows. No audio overlaps, one minor (acceptable) mismatch where beat 3's caption/ring switches about a second before its own narration finishes.

Delivered as `tapro_myprocess_tiktok.mp4` (34.7s). "MY PROCESS" tag replaces BEFORE/AFTER (v3-v5) and NEW BUILD (v6) since neither applies here. Reusable script: `build_v7_overlay.py` in `outputs/tiktok_mockup/`.

### 2026-07-30 — Asked to plan the full TikTok rotation; Ridwan wants documentation only, plus a free draft-post path researched

After v7 shipped (5 videos, 5 content types proven), asked Ridwan what's next — options offered were building a Tip or Static Ad video, planning the full rotation, or wrapping up. He chose "plan the full rotation." Ran the `process-interviewer` skill to scope it properly rather than assuming.

First interview answer reframed the whole ask: Ridwan is not ready to automate TikTok posting while he's still actively working (i.e. no scheduled task yet) — he wants everything built so far **documented** so it's ready to pick up later. He also raised a specific idea: some path where a video gets sent to TikTok automatically but he publishes it himself, since his TikTok account is 3+ years old (posted regularly in the past, no posts in 2026) and he's not ready to pay for Blotato yet.

Researched TikTok's Content Posting API directly rather than assuming Blotato is the only option (fetched both `get-started` pages from developers.tiktok.com). Confirmed a real, current, free mechanism matching exactly what Ridwan described: Direct Post (`video.publish` scope) requires TikTok's compliance audit to go public, but a separate Inbox/Draft upload mode (`video.upload` scope, `POST /v2/post/publish/inbox/video/init/`) needs no such audit — it lands the video in the creator's own TikTok inbox as a draft, notification and all, for a one-tap manual publish. Relayed this to Ridwan with sources; he confirmed "document it first" rather than build it now.

Wrote this up as a "CORRECTED 2026-07-30" subsection under Step 10 above (kept the original 2026-07-29 draft in place for history, per this project's established pattern) — covers what actually got built (real Playwright/PIL/Groq pipeline, not HeyGen), the content-types-not-styles correction, and the full draft-inbox setup sequence with sources. Status stays "documentation only" — no TikTok Developer app registered, no OAuth, nothing built. Also updated `project_tiktok_automation_plan` memory to match, since its "no paid tools yet, format not chosen" framing was stale now that 5 real videos across 5 types exist.

### 2026-07-30 (later same day) — Automated background-music selector built, replaces manual reused CC-BY-NC placeholder track

Ridwan asked how to pick TikTok music that (a) fits the video and (b) is fully automated, not manually chosen each time — and separately whether official TikTok sounds could be attached programmatically. Researched the official-sound question first: TikTok's Content Posting API has no endpoint to attach a trending sound to an uploaded video, and the only working method found (TokPortal, a paid third-party tool) does it via literal automated device-posting, not a real API — a bigger, paid commitment Ridwan wasn't ready for. He chose to automate background-music selection only and defer official sounds.

**Source: Freesound, not Pixabay.** Pixabay's public API (`pixabay.com/api/docs/`) documents image and video search only — no music/audio endpoint exists despite Pixabay Music being on their website. Freesound's API was already wired into this project (`FREESOUND_API_KEY` in `video-gen/.env`, used by the existing `search_freesound.py` SFX-search script) and supports the two things automated, license-safe selection actually needs: license filtering and duration filtering.

**License fix, not just a new feature.** v3-v7's placeholder track ("Inside Technology," reused across every prototype) is Attribution-NonCommercial — technically not clear for a paid service's promotional video. The new selector filters to ONLY `"Creative Commons 0"` (no attribution needed) or `"Attribution"` (CC-BY, one-line credit) licenses, going forward.

**Built `outputs/tiktok_mockup/select_bg_music.py`.** Maps each content type (`cro_fix_roast`, `cro_fix_scroll`, `template_showcase`, `behind_the_scenes`, `tip`, `static_ad`) to one of 5 mood buckets (energetic_roast, confident_corporate, calm_professional, motivational_tips, commercial_energetic), each with 2 short search queries, filtered to safe licenses + a 25-180s duration window, sorted by relevance score, with the top non-recently-used match downloaded automatically. A `music_usage_log.json` tracks the last 50 picks per mood so the same track doesn't repeat back-to-back.

**Real bug found and fixed while testing, twice:**
- Freesound's query matching is effectively AND-across-words against a tag-based library — the first draft's 4-5 word natural-language queries (e.g. "energetic electronic no vocals drive") returned 0 results every time, confirmed by testing the exact strings directly. Fixed by using short 2-3 word queries that include the literal word "music" (biases results toward actual scored tracks instead of ambience/field-recording SFX — "calm ambient" alone returned 1724 mostly-irrelevant results, "calm ambient music" returned 238 well-matched tracks). Also swapped one query for `commercial_energetic` after its top-scored result ("Pawsome Vibes: Get Your Groove On with 'Meow Meow'") turned out to be an off-topic pet-product jingle despite matching the filter — "advertisement upbeat music" returns cleaner, genuinely commercial-sounding matches.
- The Freesound API returns each track's `license` field as a URL (e.g. `.../publicdomain/zero/1.0/` for CC0, `.../licenses/by/4.0/` for Attribution), NOT the human label string (`"Creative Commons 0"`) used in the search `filter` syntax — the two are different vocabularies. The script's attribution-required check originally compared the returned URL against the label string, which would never match, so it would have silently flagged every track (including genuine CC0 ones) as needing attribution. Fixed by detecting CC0 via a `"publicdomain/zero"` substring check on the URL instead.

**Verified working across all 5 mood buckets** (`energetic_roast`, `confident_corporate`, `calm_professional`, `motivational_tips`, `commercial_energetic`) — each returned a real, correctly-licensed, on-mood track with valid JSON output including an accurate attribution line where required. Also verified the recent-repeat-avoidance logic: three back-to-back runs for `commercial_energetic` returned three different tracks, never the same one twice. `music_usage_log.json` was reset to empty after testing so these test picks don't bias real future selection.

**Status: automation-ready, not yet wired into a build script.** `select_bg_music.py` runs standalone (`python3 select_bg_music.py --content-type <type> --out track.mp3`) but v3-v7's individual build scripts still hard-reference the old placeholder file directly — hooking this selector into those scripts (or into a future scheduled TikTok build task) is a fast-follow, not done in this pass. Official TikTok trending-sound attachment stays out of scope per Ridwan's explicit call, documented in `project_tiktok_automation_plan` memory rather than re-litigated.

### 2026-07-30 (later same day) — Live TikTok research for the 2 remaining content types (Tip, Static Ad)

Asked what the plan is for building Tip and Static Ad TikTok videos, Ridwan asked for fresh live research first rather than guessing a format, same approach used for CRO Fix back on 2026-07-29. Browsed TikTok live (Claude in Chrome, logged out) across #marketingtips, #ecommercetips, #adcreative, #facebookads (a #dtcads attempt was a dead end — a coincidentally-named unrelated account, not the ads niche).

**Tip research — dominant format is talking-head-to-camera or a text/graphic card, NOT a scroll-through video, and saves run consistently high across every account checked:**
- @mange.marketing, "Most Businesses Post Content, But No One Cares... Here's How To Fix That In 3 Simple Steps" — pure numbered-steps graphic card, no face — 18.2K likes / 132 comments / 9,818 saves (54% save ratio).
- @thestevenmellor, "Steal this content strategy" — handwritten whiteboard/sketchbook aesthetic, posted 2022 and still surfacing — 16.5K likes / 219 comments / 13.4K saves (81% save ratio).
- @ecomvso, "Use this Shopify app to build higher-converting product pages" — a REAL screen-recording of an actual product page, same phone-frame style already proven for CRO Fix v4 — 1,715 likes / 27 comments / 1,654 saves (96% save ratio, the highest of anything checked in this pass).
- @haydencashion, "Drive more sales as an e-commerce brand with these tips" — talking head + text card — 2,122 likes / 232 comments / 1,186 saves, and generated real inbound intent in comments ("i need help setting up my store," "how do I start").
- @growthsnapp (small account, talking head) — 136 likes / 20 comments / 72 saves — smaller-account contrast point, still ~53% save ratio.

Saves running 50-95% of like-count across every single account, small or large, is the standout signal — Tip content gets bookmarked as reference material at a rate way above typical entertainment content.

**Static Ad research — no native TikTok convention exists for "post a finished static ad image as a video." The whole #adcreative/#facebookads niche is teaching/breakdown content, not creative showcases:**
- @lukethorburg, "Save these 3 winning ads for sales!" — talking head with real ad screenshots cut in — 2,259 likes / 217 comments / 1,541 saves (68% save ratio); a comment directly asked for more real ad-example breakdowns in other niches.
- @austinrabinecom, "The Only Facebook Ads Guide You'll Need For 2026" — tight talking-head close-up, smaller/newer-looking account — 464 likes / 12 comments / 323 saves (70% save ratio even at small scale).
- @realdennisdemarino5 (already known from the CRO Fix research pass) showed up again here too — confirms critique/authority creators span both the store-teardown and ad-breakdown niches.

**What this means for the two remaining content types, concretely buildable with existing tooling, no new capture technique needed:**
1. **Tip — real screen-recording of an actual tool/technique**, following @ecomvso's exact pattern (highest save ratio found): point the camera-equivalent (Playwright) at a real page/tool, name the specific technique, same `waypoint_scroll_capture.py` + iPhone-bezel pipeline already used for CRO Fix v4 / Template Showcase v6 / BTS v7.
2. **Tip — numbered-steps graphic card**, following @mange.marketing's pattern: no screen recording, no face, just `build_v3.py`'s existing badge/caption/marker compositing repurposed as a pure text-and-graphic step sequence.
3. **Static Ad — ad-breakdown/critique video**: point the roast-style zoom-cut + ring-marker visual language already built for CRO Fix v5 at a real finished ad (Ridwan's own client work or a Koolestpro sample) instead of a webpage, call out why each angle works. This is the format with direct precedent (@lukethorburg, @austinrabinecom) — there's no evidence a plain "here's my finished ad image" video works natively on TikTok at all.

Talking-head-to-camera itself (the majority of what's actually out there in both niches) stays off the table per Ridwan's existing preference not to be on camera — same constraint noted in the original 2026-07-29 research.

**Not yet built** — this is a research/planning pass only, same "prove the format with evidence before producing" discipline used for every prior content type. Next step is Ridwan picking which of the 3 buildable options above to build first (or building more than one).

### 2026-07-30 (later same day) — v8: 6th content TYPE (Static Ad ad-breakdown/critique), first video built from the research above

Ridwan picked option 3 from the research directly above: Static Ad via ad-breakdown/critique. Built `build_v8.py` in `outputs/tiktok_mockup/`, walking through all 4 real finished ad images from `outputs/static-ads/obvi_super-collagen-protein_20260711/` (problem/solution, benefit/result, social proof, offer/urgency) explaining why each angle converts. No Playwright needed here, unlike v4/v6/v7 — purely static PNG inputs, reusing `build_v3.py`'s phone-bezel/badge/caption/ring-marker primitives directly.

**Real bug found and fixed, worth remembering for any future crop-based zoom in this pipeline.** The first pass added "punch-in" zoom crops on wide/short regions (headline text bands, callout rows, the risk-reversal badge strip) rendered with `mode="cover"` (fill-and-crop). This broke badly: a wide/short crop (e.g. the badges strip, ~980x150px, aspect ~6.5) against the phone screen's tall/narrow aspect (~0.456) makes cover-fit scale to match whichever dimension is more "deficient" — for a wide/short crop that's the height, and matching height on a 6.5-aspect source blows the width up so far that only a handful of giant, illegible letters remain on screen. Confirmed on 3 separate QC frames (t=18/30/41) before the fix — @koolestpro's own text was reading as fragments like "e sco" and "l notice". Fixed by dropping crop-based zooms for anything wide/short and instead pointing a ring marker at the detail on the SAME full contain-mode (letterboxed) view — build_v3's actual original technique, proven since v3. Only ad-1's circle photo inset kept a real close-up crop, since it's roughly square rather than a thin wide band and rendered correctly on QC both before and after the fix.

**Also fixed a layout collision:** the new "AD BREAKDOWN" tag pill and `build_v3.build_badge_layer`'s pill (used here for "AD 1/2/3/4") both render in the same top band of the canvas — stacking them produced illegible overlapping text. Fixed by keeping the "AD BREAKDOWN" tag intro-grid-only and letting the per-ad badge carry context during the 4 ad beats (it already says "AD 1 · Problem → Solution" etc., which covers the same ground).

**Structure:** cold open 2x2 grid of all 4 ads ("4 ANGLES. 1 BRAND."), then one beat per ad (full view → marker pointing at the specific proof element: the hair-loss photo inset, the "19g Protein Per Serving" callout box, the first checkmark, the risk-reversal badge row), closing on a "Need ad creative like this for your brand? DM me." CTA card. VO via Groq Orpheus (same `troy` voice as v3-v7 for brand consistency), 6 real beats totaling 48.08s of narration + a silent tail hold, 50.58s final runtime — longer than v3-v7's ~28-35s, a deliberate choice since genuinely explaining 4 distinct ad angles needs more real estate than a single before/after or 3-point checklist; matches the researched precedent (@lukethorburg/@austinrabinecom's multi-example ad breakdowns aren't quick single-beat clips either). Background music via the new `select_bg_music.py` (content-type `static_ad` → `commercial_energetic` mood) — first real production use of that selector outside its own test run, picked "Bright Beginnings (Uplifting Piano and Energetic Drums)" by Gustavo_Alivera, CC-BY (attribution noted here, not overlaid on-screen, matching how this pipeline has always handled licensing so far).

Delivered as `obvi_ad-breakdown_tiktok.mp4` (50.58s). Reusable script: `build_v8.py` in `outputs/tiktok_mockup/` — the crop-vs-marker lesson above applies to any future ad-breakdown or similar detail-callout build in this pipeline.

### 2026-07-21 (later same day) — X/Twitter posting automation is now LIVE

Ridwan resolved the blocker from earlier today: he obtained X API v2 OAuth2 credentials (Client ID/Secret + a one-time manual authorization-code exchange via curl, since Make's built-in OAuth2 connection UI failed against X's API — X requires PKCE with a specific quirk where "S256" is bugged on X's side but "plain" works). The resulting access_token/refresh_token pair is stored in the koolestpro-config Make datastore (record key "main", new fields: `x_oauth2_access_token`, `x_oauth2_refresh_token`, `x_oauth2_expires_at`) alongside the existing `linkedin_token` — same pattern, not a live Make "connection" object.

The Make.com scenario "Koolestpro LinkedIn Distribution" (id 6565331) was renamed to "Koolestpro Social Distribution" and restructured: a new top-level platform router splits LinkedIn vs X before the original 3-branch LinkedIn router (untouched, byte-identical other than module ID renumbering). The new X branch does: (1) refresh the OAuth2 access token via `https://api.x.com/2/oauth2/token` and write the refreshed token back to the datastore every run, since X access tokens only last 2 hours; (2) a new 3-way asset-type router — image (.png/.jpg, using X's single-call `/2/media/upload` endpoint), video (.mp4, using the chunked initialize/append/finalize flow), and a text-only safety net; (3) posts via `https://api.x.com/2/tweets`; (4) marks the sheet row Posted, same as the LinkedIn branches.

This fixes a gap the original LinkedIn scenario had: it never had a plain-image branch (only text/.mp4/.pdf), which mattered since most of this project's output (Static Ad, CRO Fix, Tips carousel) is PNG — the new X image branch is the first branch across either platform that actually handles the account's most common asset type.

One thing flagged as needing live verification before fully trusting it: the video branch's `total_bytes` calculation uses Make's `length()` function on the downloaded file buffer (Make's `http:ActionGetFile` module has no direct fileSize output property, this was double-checked against Make's real module schema) — this hasn't been tested against a real video post yet, only the image path should be treated as proven. Do a live test row before relying on video-to-X posting.

Trigger filter on the shared Google Sheet trigger was widened from `platform=="LinkedIn"` only to `platform=="LinkedIn" OR platform=="X"` (still same "Koolestpro Distribution Queue" sheet, no new sheet/columns needed — the schema already had a platform column per the V2 distribution plan).

Full technical reference: `docs/x-twitter-distribution-setup.md` (written earlier the same day, before the credentials existed — still useful for the OAuth/media-upload mechanics, though the actual implementation ended up using OAuth2 instead of the OAuth1.0a fallback that doc discusses, since X's officially documented current endpoints turned out to support OAuth2 Bearer tokens directly).

### 2026-07-21 — X/Twitter posting automation investigated, blocked on API credentials

Looked into wiring X into the Make.com distribution layer alongside the working LinkedIn scenario. Found the org's Make.com plan is **Free tier, capped at 2 scenarios, both already in use** ("Abu Zayd Afternoon Post" and "Koolestpro LinkedIn Distribution"). Per Ridwan's choice, the fix is not to upgrade the plan but to fold X into the existing LinkedIn scenario — renaming it **"Koolestpro Social Distribution"** — rather than paying for a third scenario slot.

Also found X's API pricing changed in February 2026: the free tier was retired, replaced by pay-per-use ($0.015/post, $0.20 if the post contains a link, no subscription). Before this scenario can be built, Ridwan needs to obtain X Developer Portal API v2 credentials — a Read+Write app with OAuth 1.0a keys.

Wrote the full setup guide and the folded-scenario technical spec — platform router, new image/video branches (LinkedIn's scenario never had a plain-image branch), and X's chunked media upload INIT/APPEND/FINALIZE flow versus LinkedIn's pre-signed-URL flow — to `docs/x-twitter-distribution-setup.md`.

**Not yet built — blocked on Ridwan obtaining credentials.**

### 2026-07-18 — HALOS replaces KURA as the Template Showcase source brand

Ridwan's instruction: the replo schedule should showcase HALOS, the newer brand in `replo-rebuilds`, instead of KURA. HALOS has 3 built pages (`halos-pdp-01` story-arc PDP, `halos-hp-01` custom editorial homepage, `halos-lp-01` direct-response landing page); all three were copied into `replo-pages-cache/` and their image paths verified to resolve from the cache copies (7 / 2 / 10 local refs, zero missing).

`replo-rebuilds-pages.json` gained `active` / `retired` / `sortOrder` per entry. Selection is now "eligible = active AND not yet showcased, lowest sortOrder first" — HALOS at 1–3, the 5 KURA entries at 90 with `active:false`. KURA was **retired rather than deleted** (Ridwan's choice) so the weekly task keeps a fallback once the three HALOS pages are used up; a KURA fallback must be stated explicitly in the run summary rather than taken silently.

One real difference from KURA worth recording: **HALOS has no pre-written caption library.** `kura-social-content.md` sits in the cache and the old task prompt told the run to adapt captions from it. There is no HALOS equivalent, so the task now writes captions from the page itself, humanizes them, and creates `halos-social-content.json`/`.md` on first run. Without this the run would have gone looking for a file that was never going to exist.

`koolestpro-template-showcase-weekly` and `koolestpro-replo-cache-staleness-check` were both updated — the latter now counts only *active* unused entries as real runway (3 today) and escalates at 1 remaining rather than 0, since a one-page buffer is already the point to build another page.

Note: `koolestpro-template-showcase-weekly` is currently **disabled**. The HALOS switch is fully wired but the task will not fire until it's re-enabled.

### 2026-07-18 — Both Friday streams reviewed and fixed after Ridwan rejected the 2026-07-17 output

Ridwan flagged the Friday run's static ads as "very basic" and the Tips carousel as unreadable on small devices. Both were reproduced, root-caused, and fixed; both scheduled tasks were rewritten so it can't recur.

**Static Ad — the fallback was the bug, and it rested on an untested assumption.** The Obvi test ad that Ridwan liked had gpt-image render the whole ad, headline baked into the photograph. The Bebemoss run instead produced a cream text panel stacked above a photo, with the headline drawn in Liberation Sans by PIL. It got there by hitting the ~45s per-command ceiling on `--quality medium` calls, concluding gpt-image couldn't render ad text, and falling back to compositing — justified in its own log by "low-quality gpt-image text overlays routinely misspell headlines," which was never tested.

Measured on 2026-07-18 at 1024×1536 portrait: `--quality medium` takes >44s and is *always* killed (reproducible, warm cache); `--quality low` takes 21–30s and spelled the headline correctly on 4/4 ads. Separately confirmed that detached background processes do **not** survive between bash calls (`setsid nohup` + `disown`, verified dead 25s later), so there is no fire-and-poll escape hatch — every image must finish inside one command. All four Bebemoss ads were regenerated one-per-command at `low` and now match the Obvi standard. PIL is now barred from drawing ad copy at all; its only permitted use in this stream is tiling the 2×2 combined showcase.

**Tips — geometry was right, the type scale had drifted.** The carousel was correctly 540×680, but body copy ran at 10–13px where the gold standard (`funnel-awareness-framework_2026-05-10.html`) uses 15–16px — roughly a 3px drop across every element, which is unreadable at phone size. Worth recording that the typeface was *not* the problem: DM Mono for body copy is correct and matches the gold standard. Fixed by scaling everything inside `.slide` to the new floor (15px primary prose / 13px secondary / 12px footer, uppercase tracking labels exempt) and giving slide 6's list `flex:1` + `space-evenly` to kill a large dead band at the bottom.

**Standalone graphic cards retired** (Ridwan's call): `graphic-a/b/c.png` and the `.gcard` block are no longer produced, and the `TIP-{BRAND}-GRAPHIC-A/B/C` keys were removed from `koolestpro-social-content.json/.md`.

**New tool:** `.ai-workflow/tools/export_tip_slides.py` — drives headless Chromium against a finished tips HTML and calls the file's own `dlSlide(i)`, intercepting each download, so output is byte-identical to clicking the on-page buttons rather than a generic screenshot. Verification of Tips output is now a mandatory step in the scheduled task, not best-effort.

**Process note this run reinforces:** both failures shipped because a run downgraded its own deliverable when it hit a constraint and described the result as finished. Both scheduled-task prompts now say explicitly: if something genuinely can't be produced, say so plainly in the summary rather than shipping a lesser artifact that looks complete — and read the rendered image back before calling any run done.

### 2026-07-17 — Weekly Tips buffer run + DeepSeek reliability finding (koolestpro-tips-weekly)

Ran the weekly Tip carousel cycle. Topic pulled from backlog (existing id `idea-animation-budget-when-motion-helps-conversion-...jjrc6`, updated in place — no duplicate id): **"Animation Budget: When Motion Helps Conversion"**, run as a Myth-vs-Reality contrarian angle in the Conversion Strategy pillar ("your animations aren't making you look premium, they're making you convert worse"). 7 slides, no before/after (conceptual), CTA `DM me "AUDIT"`. Rotated off the funnel/audience-temperature topic that dominated recent Tips. Real stat only (Amazon 100ms ≈ 1% sales), no fabricated client metrics. Output: `outputs/tips/animation-budget-motion-conversion_2026-07-17.html`; 10 assets exported to `outputs/tips/animation-budget-assets/`; registered Created; `koolestpro-social-content.json/.md` created (first Koolestpro-brand entry, `TIP-KOOLESTPRO-ANIMBUDGET-*` keys).

**Finding worth acting on: DeepSeek delegation is unreliable for the full Tips carousel.** Two `run_deepseek_task.js` calls produced a 302-line minimal file that invented its own `showSlide`/`.deck` carousel and dropped every mandatory element (download panel, PDF export, pipeline button, 5 copy tabs, 3 graphic variations) and ignored the specified slide copy. Root cause: `run_deepseek_task.js` truncates referenced files to 12k chars, so DeepSeek never sees the gold standard's real export JS (which lives past line 700), and the full file needs ~40k+ chars across multiple continue calls — it simplifies instead. Fallback that worked and is now reusable: **`.ai-workflow/tools/build_animation_tip.py`** — a deterministic region-swap that reuses the gold-standard reference's exact carousel/PNG/PDF/pipeline/tabs JS byte-for-byte and slots in new slide/graphic/tab content. For future Tips runs, prefer transforming the gold standard over a from-scratch DeepSeek build, or inline the full reference JS into the task spec rather than relying on the truncated auto-inline. Export verified live via headless Playwright (all slides 1080×1360 portrait, no chrome bleed, no console errors; caught and fixed a "100ms" stat overflow at 114px → 78px before finalizing).

### 2026-07-14 — V2 Distribution pipeline built (Steps 1-5, 8; Step 7 pending; Step 3 thumbnail done)

Implemented `koolestpro-v2-distribution-plan.md` — turning the four generation streams into a scheduled cross-platform distribution system. What now exists:

**Step 1 — Rescheduling (done).** Moved the generation tasks into the credit-safe Fri-Sun window: `koolestpro-static-ad-weekly` → Fri ~09:04, `koolestpro-tips-weekly` → Fri ~09:28, `koolestpro-template-showcase-weekly` → Sat ~09:09, `koolestpro-weekly-cro-fix` → Sun ~09:12. `koolestpro-target-pool-refresh` → Monday **biweekly** (cron can't express biweekly, so a Step-0 ISO-even-week parity guard was added to its prompt). New task `koolestpro-replo-cache-staleness-check` (Mon ~08:49) reminds Ridwan when `replo-pages-cache/` is >14 days stale — reminder-only, never attempts the cross-project refresh (structurally impossible from a single-folder scheduled task).

**Steps 2/4/5/8 — Scripts built and tested against all four real output types** (`.ai-workflow/tools/`, see `DISTRIBUTION.md`):
- `harvest_content.py` — per-skill DOM parser. Confirmed two tab vocabularies exist in the wild (CRO-Fix/gold-standard-Tips `#tab-linkedin` scheme vs content-engine `#tab-li-long` scheme) and handles both by parsing on DOM structure, not POST_TYPE. Also finds CRO Fix graphics in the `outputs/cro-fixes/{brand}/` subfolder.
- `qa_check.py` — flag-not-block. In testing it caught real issues: the V1CE "backed by 2 reviews" claim, a brand-agnostic caption, and a banned SVG gradient-text pattern in a Tips file.
- `populate_sheet.py` — expands one record into per-post rows off the encoded weekly calendar. Verified totals: **LinkedIn 3/wk, Instagram 7/wk** (exact plan targets), ~9 distinct Twitter rows across the four streams (→ ~17-18 with the second-angle repost pass, matching the plan's honest ramp). Durable local queue at `outputs/distribution-queue/queue.json`/`.csv`.
- `sync_content_system.py` — attaches a `distribution` array to each matching SYNC_DATA item, additive, UI preserved, `.bak` written, joins by id with slug fallback, never fabricates.

**Step 3 — Video thumbnail (done).** `make_thumbnail.py` added to `page-presentation-kit/scripts/` — device cover + brand glow + rotated headline + diamond accents + tagline, per-platform sizes. Rendered a clean on-brand KURA thumbnail in testing. Uses DejaVu Bold in-sandbox; pass `--font Syne-Bold.ttf` for exact brand parity.

**Step 5 Sheet — created.** Live Google Sheet "Koolestpro Distribution Queue" (id `1I5SrLnwAfVV5260Y_nAytio49gh-NKmJeJdFXH3nqzg`, recorded in `outputs/distribution-queue/sheet.json`), created from the queue CSV via the Drive connector.

**Key architectural decision (the Sheet/Make boundary):** the connected Google **Drive** connector can CREATE the Sheet but **cannot append/edit rows in place**. So the durable source of truth is the local `queue.json`/`queue.csv`; the Sheet is a mirror. Row append + status write-back (Ready → Posted) is Make.com's job.

**Step 7 — Make.com: FIRST LIVE POST ACHIEVED (LinkedIn, text-only).** Scenario **"Koolestpro LinkedIn Distribution"** (id 6565331, team 1960838) created via the Make API, modeled on the proven "Abu Zayd Afternoon Post" pattern: `google-sheets:filterRows` (status=Ready AND platform=LinkedIn) → `http` GET `/v2/userinfo` (author URN) → `http` POST `/v2/ugcPosts` → `google-sheets:updateRow` (status=Posted, posted_at). Confirmed working — a real post published to Ridwan's personal feed from a queue row.

Platform auth findings: LinkedIn requires a developer app attached to a **Company Page** even to post to a *personal* profile (posts go to the personal feed via `w_member_social`; the Page is an administrative shell only). Products needed: "Share on LinkedIn" + "Sign In with LinkedIn using OpenID Connect", both instant-grant. Token generated via the app's Auth → OAuth 2.0 tools. Token is pasted directly into the HTTP modules (same pattern as Abu Zayd) — **note: pushing a full blueprint update via the API resets those token fields**, so prefer small in-UI edits over full-blueprint pushes once a token is in place.

Debugging note worth keeping: the failure mode was `400 ILLEGAL_ARGUMENT "Request body could not be converted to data map"`, then Make's own `"The provided JSON body content is not valid JSON"`. Root cause is that the post body is hand-built JSON with the caption interpolated as a raw string — any line break or quote in a caption breaks it. Resolved for the first post by using a clean single-line caption.

**RESOLVED 2026-07-18 — caption escaping + scheduling gate.**

*Caption escaping (the architecture decision worth keeping):* trying to JSON-escape captions inside a Make expression is fragile — Make's regex/quoting rules make escaping a literal `"` unreliable. The robust fix is to escape **upstream in Python**: `populate_sheet.py` now emits a `caption_json` column (index 13) containing `json.dumps(caption)` — a complete JSON string literal *including its surrounding quotes*. Make's HTTP body then drops it in verbatim (`"text":{{1.\`13\`}}`, deliberately NOT wrapped in quotes). Verified across all 19 queue rows, including a 2,004-char caption with 52 newlines and embedded quotes: every body parses as valid JSON and the caption round-trips byte-identical. **Never go back to interpolating a raw caption into a JSON body.** An `asset_urls` column (index 14) was appended at the same time. Columns are referenced by index in the Make scenario — **append only, never reorder**.

*Scheduling gate:* the trigger filter now requires `scheduled_date` = today AND `scheduled_time_et` <= now, both evaluated with `formatDate(...; "America/New_York")`. This matters because the Make org timezone is **Africa/Lagos** — without the explicit ET timezone the scenario would fire roughly 5 hours early. `posted_at` is also written in ET.

*Two Make bugs found by a live run that fired 4 LinkedIn posts at once (2026-07-18) — do not reintroduce:*

1. **A gate belongs on a MODULE, not inside the trigger's own search filter.** Conditions were first placed in `google-sheets:filterRows`'s `mapper.filter`, referencing `{{1.\`9\`}}` — i.e. referencing the trigger's own output from inside the trigger. Those references don't evaluate there, so the gate silently passed everything and every `Ready` row posted in one run. **Correct placement:** a module-level `"filter"` key on the *next* module (module 2), which is exactly how the working Abu Zayd scenario gates its routes. Trigger-output references (`{{1.\`x\`}}`) only evaluate downstream of the trigger.
2. **`google-sheets:updateRow` silently no-ops without `rowNumber`.** The write-back had `values` but no target row, so no row was ever flipped to `Posted` — meaning the same rows stayed eligible and would have posted again on the next 15-minute run. **Fix:** `"rowNumber": "{{1.\`__ROW_NUMBER__\`}}"` from the trigger bundle.

Together these violated the plan's hard "never post twice a day on LinkedIn" rule (a second post within 24h suppresses the first one's reach). With the gate correctly placed, the weekly calendar's data shape enforces the rule on its own: only one LinkedIn row exists per day, so a same-day gate can only ever match one.

*Operational note:* a full-blueprint push via the API **resets the pasted access token** in every HTTP module. There is no partial-module update in this MCP, so each structural change costs a token re-paste. Batch structural edits together rather than pushing several small ones.

**Timezone — RESOLVED in the sheet, NOT in Make (2026-07-18, Ridwan's decision).** Ridwan is happy with the Make scenario as-is and explicitly does **not** want it edited again (every structural push also costs a token re-paste). His gate reads Make's org clock (**Africa/Lagos**). So the timezone conversion was moved OUT of Make and INTO `populate_sheet.py`: the weekly CALENDAR is still authored in US Eastern, but each slot is converted ET→Africa/Lagos (DST-correct, via `zoneinfo`) and the **local** date/time is what's written to the sheet. The untouched Lagos-clock gate then fires at the correct US moment. Column 5 was renamed `scheduled_time_et` → `scheduled_time_local` (holds his local fire time); a new **index-15** `intended_et` column carries the US time for human reference. Verified: 09:00 ET→14:00, 12:00 ET→17:00, 18:00 ET→23:00 local; and the Make-critical column indices (4 date, 5 time, 9 status, 11 posted_at, 13 caption_json) are unchanged. `--local-tz` flag defaults to `Africa/Lagos` and MUST match the Make org timezone if it ever changes. Because Make runs cloud-side 24/7, Ridwan never needs to be awake/online for a post regardless of the local hour.

**Token re-paste problem SOLVED via a Make data store (2026-07-19).** A full-blueprint API push resets any token pasted into HTTP modules, which made every scenario edit cost a re-paste. Fix: created data store **koolestpro-config** (id 149236, structure id 497474, field `linkedin_token`, record key `main`) and a `datastore:GetRecord` module (id must be capitalised `GetRecord`, not `getRecord`) as step 2 of the scenario. All HTTP modules now use `{{2.linkedin_token}}`. The literal token lives only in the data store record, which blueprint pushes never touch — so Ridwan pasted it once (into the record, no `Bearer` prefix) and never again. Confirmed working end-to-end. This is what makes iterating on video safe: debug loops cost zero re-pastes.

**LinkedIn author = HARDCODE `urn:li:person:V5zHWUI_Ud` in all future builds (2026-07-19).** Ridwan's LinkedIn member id (the `sub` from `/v2/userinfo`) is `V5zHWUI_Ud`. The dynamic userinfo lookup was fragile (broke whenever bubbles were rearranged), so it's replaced by hardcoding the author URN. Future LinkedIn scenario builds should NOT include a userinfo module — put `urn:li:person:V5zHWUI_Ud` directly in the post/registerUpload bodies. (The id itself is not secret; the token is, and that lives in the data store.)

**✅ LinkedIn NATIVE VIDEO WORKING (2026-07-19).** A real KURA homepage video posted to Ridwan's feed, automatically, from a queue row. The working scenario (id 6565331, 10 modules): `filterRows` → `datastore:GetRecord` (token, with the Ready+LinkedIn+due gate on it) → `BasicRouter` splitting on asset_urls empty/not — TEXT route posts `ugcPosts` (shareMediaCategory NONE); VIDEO route does `assets?action=registerUpload` → `http:ActionGetFile` (download the Cloudinary mp4) → POST the binary to `{{registerModule.value.uploadMechanism.\`com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest\`.uploadUrl}}` (octet-stream, Authorization Bearer) → `ugcPosts` with shareMediaCategory VIDEO + media `{{registerModule.value.asset}}` → `updateRow`. Author hardcoded `urn:li:person:V5zHWUI_Ud` in both post bodies. What finally made video work: hardcoding the author (killed the userinfo-lookup fragility) and pushing ONE clean version so the bubble numbering was correct and the dotted-key uploadUrl reference resolved — the earlier 403s were the reference breaking after manual bubble rearranging, not an auth problem. The binary upload DOES send the Bearer token and DOES use POST. This is the reference pattern for future video builds (LinkedIn and, eventually, an image variant).

**(historical) LinkedIn video debugging trail:** Seen errors on the upload step: 401 (token not passed), 403 (upload rejected — likely the dotted-key `uploadMechanism.\`com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest\`.uploadUrl` reference not resolving after bubbles were renumbered by manual edits), 422 (bad post body). One run DID succeed (status 1, 5 ops) before further manual edits reintroduced errors. Manual rearranging also repeatedly broke module connections → `Cannot read ... 'account'` init errors (0 ops). LESSON: LinkedIn native video is the most finicky API in this build; the manual-edit + API-push loop is fighting itself. Cleaner future approach: hardcode the author, and either (a) push one correct version and don't hand-edit, or (b) prefer Instagram Reels for video (Graph API accepts a video URL directly — no binary upload, far simpler) once Meta linking is unblocked.

**✅ LinkedIn PDF DOCUMENT CAROUSEL WORKING (2026-07-21).** The scenario now has THREE routes off the router, auto-selected by the asset URL extension in col 14 (`asset_urls`): empty→text, contains `.mp4`→video, contains `.pdf`→document. The document route uses LinkedIn's newer `/rest/` versioned API (confirmed via docs it supports a `person` owner with `w_member_social`): POST `/rest/documents?action=initializeUpload` (body `{"initializeUploadRequest":{"owner":"urn:li:person:V5zHWUI_Ud"}}`) → `ActionGetFile` (download the PDF) → **PUT** the binary to `{{initModule.value.uploadUrl}}` (Bearer, octet-stream — note PUT, not POST like video) → POST `/rest/posts` with `content.media.id = {{initModule.value.document}}` and `commentary = {{1.\`13\`}}` (the caption_json). REQUIRED headers on the two `/rest/` calls: `X-Restli-Protocol-Version: 2.0.0` AND `LinkedIn-Version: 202606`. Worked first try. Prereqs that bit us: (1) content must be a real PDF hosted publicly — img2pdf builds one from slide PNGs, uploaded to Cloudinary via `/raw/upload`; (2) **Cloudinary blocks PDF/ZIP delivery by default** — Ridwan enabled Settings→Security→"Allow delivery of PDF and ZIP files" (was 401 before, 200 after). Feared-but-didn't-happen: no versioned-API-access 403, and `/rest/posts` accepted the caption's `()`/`#` without REST-escaping. For automation, populate_sheet would put a hosted `.pdf` URL in asset_urls for Tips-carousel LinkedIn rows.

**LinkedIn is now COMPLETE for all three media types (text, video, PDF carousel).** Remaining Step 7:

**Still open on Step 7:**
- **Images/video** not wired yet — needs the Cloudinary unsigned upload preset (see `upload_assets.py`), then LinkedIn's 3-step image flow (initializeUpload → PUT binary → reference the image URN in the post).
- **No date/time gate yet** — the trigger currently matches ANY row with status=Ready + platform=LinkedIn, ignoring `scheduled_date`/`scheduled_time_et`. **Keep the scenario INACTIVE** until this is added, or it will post every Ready row on its next 15-min run.
- **No retry-then-flag error handler yet** (policy chosen: retry 3x with backoff, then write `Failed: <reason>` to the row).
- Instagram still blocked on a temporary Meta account-linking restriction (IG must be Business + linked to a Facebook Page before the Content Publishing API works).

**Step 6 — Human approval REMOVED (2026-08-27, see Build Log).** `populate_sheet.py` now writes every row as `status = "Ready"` by default; there is no more Draft→Ready manual flip.

### 2026-07-10 — Static Ad Image skill (Step 4) built as a standalone, reusable skill

Scope for this pass was deliberately narrow: Step 4 (static ad showcase) plus the weekly buffer schedule. The other 7 steps (target pool automation, CRO before/after automation, template showcase, X repurposing, outreach, full review/approve UI, publishing queue) are untouched — still manual/as-is, same as before this pass.

**Decisions locked in:**

- The skill is general-purpose, not koolestpro-only — same flow works for real client CRO work, just with a different brand/product as input. No separate "client mode."
- Copy sourcing is auto-detected: given copy is used verbatim; a product URL gets fetched and read for benefits/features/reviews; a bare name/photo triggers a web-search research pass. No invented stats or claims — general benefit framing when nothing traceable is found.
- The 4 default ad angles each map to a fixed visual pattern (not user-chosen per run): problem/solution → meme/pain-point or stat-grid; benefit/result → bold headline + product shot + feature bullets; social proof/trust → testimonial quote or star-rating; offer/urgency → CTA banner / cart-urgency style. Pattern set was derived from Ridwan's 17 reference ad images (Kura, Ankhway, Rise Luxus, Balmbare, Primal Queen, Feastables, Saint Jane, etc.) — see the skill's own style-pattern reference file for the mapping.
- No product photo → GPT-image generates a photoreal mockup (same approach as `gen-one-image.py`'s existing Abu Zaid image generation), rather than refusing.
- Backend is GPT-image directly (raster PNG output), not the html2canvas/DeepSeek HTML-rebuild pipeline used for CRO fixes — those are a different tool for a different job.
- Added a 5th pipeline type, `"Static Ad"`, to the JSON Standard in `CLAUDE.md` (previously only Tip/CRO Fix/Case Study/Personal existed — a static ad showcase didn't fit any of them). Output folder convention: `outputs/static-ads/{slug}_{date}/index.html`, a lightweight companion page (not an html2canvas capture target) that carries the 4 ad images + combined showcase + captions + the standard pipeline export button.
- All captions run through the humanizer skill before finalizing, per the project's standing rule.
- Weekly cadence: a Saturday-morning scheduled task runs the skill once against one product (from `targets_pool.json` or koolestpro sample work), producing a `"Created"` pipeline record days ahead of any post date — mirroring the existing (currently disabled) `abuzaid-saturday-batch` pattern rather than inventing a new cadence.
- Posting stays manual in this pass, unchanged from the existing "Social posting method (v1): Manual" decision above.

**Framed for v2 (auto-post) on purpose:** the skill's output boundary is a finished, approved-or-not pipeline record with everything Make.com would need already sitting in the JSON (`title`, `slug`, `folder`, captions, image paths) — so turning on auto-post later is swapping *only* the Step 8/9 "review → you post manually" step for "review → push to Sheets/Make.com," without touching how ads get generated. Nothing in the generation logic assumes manual posting.

### 2026-07-11 — page-presentation-kit built as a portable, project-agnostic skill (supports Step 5)

Started as Step 5 ("Weekly Template/Page Showcase") work, but scope pivoted at Ridwan's request into a standalone, general-purpose skill any project can call into — not koolestpro-specific like static-ad-image effectively is. Step 5 itself (page selection, captions, pipeline registration) is still unbuilt; this only delivers the visual-asset capability Step 5 will eventually call into.

**What it does:** takes any real page (URL or local HTML) and produces desktop/mobile device mockups, a combined presentation graphic, and an optional silent scroll-through video. Real screenshots only (Playwright, bundled into the skill with its proven ARM64 sandbox setup) composited into frames via plain HTML/CSS or a calibrated perspective warp — never regenerated by an image model, so the page content shown is always accurate. Five named styles (`flat-browser-frame`, `angled-3d-perspective`, `multi-device-collage`, `dark-portfolio-shot`, `device-in-hand-lifestyle`) documented in the skill's own `references/mockup-style-patterns.md`, matched to a given reference image or chosen sensibly when none is given.

**Portability mechanism (the actual design goal here):** the skill carries zero opinion about where its output goes. Every project that uses it needs a standardized `## Page Presentation Kit — Export Routing` section in its own `CLAUDE.md` — added to both `koolestpro-cowork-v2` (routes to `outputs/templates/{slug}_{date}/`, matching Step 5's existing convention) and `replo-rebuilds` (routes to `brands/{brand}/case-study/{page-type}/mockups/` and `.../video/`, alongside that project's existing case-study assets) as part of this build. A project with no such section gets a plain local default instead of a failure.

**Reference library:** a shared, growing library lives at `replo-rebuilds/page-presentation-kit-references/{style}/` (mirroring that project's existing `static-ads-references/{source}/` convention) — not duplicated per-project. Grows two ways: explicit dumps ("add these to references") and auto-save whenever a reference is used in an actual generation run.

**Update 2026-07-11 (same day) — static-ad-image retrofitted to match:** Ridwan confirmed the inconsistency should be fixed. static-ad-image now has the same Step 0 "check the current project's CLAUDE.md for an Export Routing section" pattern as page-presentation-kit, added a matching `## Static Ad Image — Export Routing` section to this project's CLAUDE.md (consolidating what was previously hardcoded into the skill itself), and got the same treatment in `replo-rebuilds/CLAUDE.md` (routes to `brands/{brand}/static-ads/{slug}_{date}/`, skips pipeline-JSON registration since that project has no central content pipeline). Both skills now follow the same portability pattern consistently.

### 2026-07-12 — Step 5 automated end-to-end; approval/outreach backlog cleared

Closed the loop on the two loose threads sitting in the pipeline (V1CE CRO Fix, Obvi Static Ad) and built the Step 5 weekly automation the 2026-07-11 build log flagged as still unbuilt.

**Approval + outreach (Step 8 / Step 7):**

- Ran V1CE and Obvi through the Step 8 checklist. Both passed on visual/voice/lead-gen grounds; V1CE's captions were missing the "unofficial concept" disclaimer required by the Brand Safety Rules (Obvi's companion page already had one) — added it to all four caption variants and the tweet section before marking Ready. Both items are now `status: "Ready"` in `ridwan_content_system_updated.html` with a `reviewNote` explaining what changed.
- Wrote and logged outreach packages for both in `outreach_tracker.json` (was empty despite the plan requiring one for every real-brand concept). `contactName` is left as an explicit TBD — no contact name/handle was invented; Ridwan still needs to find the actual DM/email contact before the first send.
- Found and fixed a stale-data bug in `targets_pool.json`: V1CE's `status` was stuck at `"Used"` (single-string `usedFor`) from before the per-stream `usedFor` object pattern existed (that pattern was introduced for Obvi on 2026-07-11). A top-level `"Used"` status silently locks a target out of every future stream, not just the one it was used for, which would have made V1CE (High/High) permanently unavailable to Step 5 despite having only ever been used for one stream. Normalized to `status: "Available"` with object-format `usedFor`, matching Obvi's schema going forward.

**Step 5 automation (Step 5 / Step 9 prep):**

- Extended the JSON Standard with a new `"Template Showcase"` type and two optional, backward-compatible fields — `captions` (`linkedin`, `x[]`) and `assets` (`images[]`, `video`) — so a pipeline record can carry the actual post text and asset paths as data instead of only as a link to an HTML file a future automation step would have to scrape. Older items without these fields remain valid; Cowork must never reject an item for lacking them. This directly serves the "prepare for autopost" ask: when Make.com/Sheets integration is eventually turned on (still deferred per the 2026-07-05 decision above), the Template Showcase records already carry what it needs.
- Added the companion-page pattern for Template Showcase (`outputs/templates/{slug}_{date}/index.html`, mirroring Static Ad's `index.html`) to the "Page Presentation Kit — Export Routing" section of `CLAUDE.md`.
- Created the `koolestpro-template-showcase-weekly` scheduled task (Sundays 09:07, offset from the Saturday static-ad run) that runs Step 5 end-to-end unattended: picks an unused-for-this-stream target from `targets_pool.json` (prioritizing product/landing/advertorial/collection pages per Step 5's own priority order), builds or selects the page in `replo-rebuilds` if that folder happens to be connected in the run, falls back to showcasing one of koolestpro's own already-finished pages if it isn't (an explicit, stated fallback rather than a silent one), generates mockups via `page-presentation-kit`, writes and humanizes the captions itself (never delegated — captions stay a Claude job per the AI Workflow Architecture split), delegates the companion HTML page to DeepSeek per the existing Automatic Delegation Trigger, and registers a `"Template Showcase"` pipeline record — populating the new `captions`/`assets` fields — at status `"Created"`, never `"Published"`.
- This mirrors, and is explicitly modeled on, `koolestpro-static-ad-weekly`'s "buffer run only, human approves later" pattern — no new posting-automation behavior was introduced. Manual posting (Step 9) is still the standing decision; nothing here changes that.

**Correction (2026-07-12, same day):** the note originally here claimed `replo-rebuilds` wasn't connected in this Cowork session — that was wrong. A first `Read` attempt on `replo-rebuilds/CLAUDE.md` errored as out-of-session, but a retry (and a direct `ls` on its mounted path) confirmed it's actually connected alongside `koolestpro-cowork-v2`. So `koolestpro-template-showcase-weekly`'s first Sunday run should be able to reach `replo-rebuilds` normally rather than falling back — the fallback path stays in the task as a safety net (a scheduled task's execution context isn't guaranteed to carry identical mounts to any given interactive session), just isn't expected to trigger by default now. No action needed from Ridwan on this point.

Outreach `contactName`/`contactMethod` for V1CE and Obvi were filled in via a 2026-07-12 web search: V1CE → Instagram `@v1cecard` (unverified as actively monitored) with `v1ce.co/pages/contact-us` as fallback; Obvi → `hello@myobvi.com` as primary with Instagram `@obvi` as an alternate. Neither has been outreach-verified (no test message sent yet) — worth a sanity check before the first real send that these are current.

### 2026-07-12 (later same day) — Per-brand social-content library: the actual caption-to-image answer

Ridwan pointed out he's already building `{brand}-social-content.md` files by hand (found the working precedent: `replo-rebuilds/kura-social-content.md` — a key table like `T-PDP-MOB` mapping each generated asset to a ready-to-post caption, grown over time as more content ships for that brand) and asked for this to be the starting point once autopost gets automated, plus a direct answer to "how do I get the caption for a generated image."

**Decision:** adopted the same convention in `koolestpro-cowork-v2`, one file pair per brand at the project root — `{brand-slug}-social-content.md` (human, matches the kura table+block format) and `{brand-slug}-social-content.json` (machine-readable sibling, same keys, what automation actually reads). Defined a key scheme per content type this project produces: `SA-{BRAND}-PROBLEM/BENEFIT/PROOF/OFFER/COMBO/X1-3` for Static Ad, `CRO-{BRAND}-BA/ANNO/CAROUSEL/X1-3` for CRO Fix, `TS-{BRAND}-DESKTOP/MOBILE/COMBO/VIDEO` for Template Showcase. Built `obvi-social-content.json`/`.md` and `v1ce-social-content.json`/`.md` as the first two real examples, retrofitting existing captions.

**How this relates to the `captions`/`assets` pipeline fields added earlier today:** those stay as a lightweight optional cache on the individual pipeline item (nice for a quick glance in `content_pipeline.html`). The brand social-content file is the actual durable source of truth — it accumulates across every post ever made about that brand, not just one item, and is what a future Make.com/Sheets step should be built against. Documented in `CLAUDE.md` under "Per-Brand Social Content Library." Both weekly scheduled tasks (`koolestpro-static-ad-weekly`, `koolestpro-template-showcase-weekly`) now create/update the relevant brand's file pair as part of their run.

**Real gap surfaced while building the V1CE example:** the before/after, annotated, and carousel-slide PNGs referenced in `v1ce_tap-review-card_captions.md` don't exist on disk yet — `outputs/cro-fixes/v1ce_tap-review-card_content.html` only generates them client-side via html2canvas download buttons, and nobody has clicked them. `v1ce-social-content.json` carries a `knownGaps` field flagging this explicitly rather than pointing automation at a broken path. Obvi's static-ad images don't have this problem — those were saved to disk directly during generation, so `obvi-social-content.json` has zero gaps. Worth exporting the V1CE PNGs before that record is ever fed into a real autopost step.

### 2026-07-12 (later still) — Closed the V1CE known gap; established the headless-export pattern for future CRO Fix posts

Following up on the per-brand social-content library work above: rather than leave `v1ce-social-content.json`'s `knownGaps` (before/after, annotated, and carousel-slide PNGs not yet exported to disk) as a standing TODO, actually resolved it, and generalized the fix into a documented pattern for every future CRO Fix post.

**What was tried and ruled out:** first attempted this via the Claude in Chrome extension (drive the real browser, call the page's capture function, read back the canvas data). Hit a hard wall — the extension can't inject into `file://` pages without a manually-toggled Chrome setting ("Allow access to file URLs") that can't be flipped programmatically, and even if it could, pulling multi-megabyte base64 PNG data back through a tool response into the conversation would have been a real context cost. Both problems evaporate with headless Playwright instead, since it runs in the same sandbox as the mounted project files (no cross-machine issue) and downloads save straight to disk (no giant string ever touches the conversation).

**What worked:** re-ran this project's documented ARM64 Playwright setup (`.ai-workflow/tools/README.md`), then wrote a small script that loads `outputs/cro-fixes/v1ce_tap-review-card_content.html` headlessly and calls its own `captureFixed()`/`captureSlide()` functions directly via `page.evaluate()` — the same html2canvas calls the download buttons already use, not a generic screenshot (screenshots and html2canvas render some things, like SVG gradients, differently — see the existing "Verify before annotating" lesson). `page.expect_download()` intercepts the resulting `a.click()` and saves the real file. All 8 assets (before/after, annotated, and 7 carousel slides — the real count, not the 6 assumed when `v1ce-social-content.json` was first drafted) now exist in `outputs/cro-fixes/v1ce/`. Documented the reusable pattern in `CLAUDE.md`'s "Per-Brand Social Content Library" section so this doesn't need re-deriving next time.

**A real scare that turned out fine:** spot-checking the exported annotated graphic surfaced what looked like a fabricated trust claim — "Also trusted by HSBC & IBM" — nowhere in the captions or visible audit summary. Before treating it as a violation of the "no fake metrics" constraint, checked the actual audit brief (`outputs/audits/v1ce_tap-review-card_audit.md`, Finding 3) and then verified directly against the live `v1ce.co` product page: V1CE's real PDP has a genuine client-logo carousel further down (Rolex, Eventbrite, Accenture, HubSpot, Canva, Lenovo, Aston Martin, HSBC, IBM). The rebuild surfaced a real existing trust signal higher up the page — exactly what the audit recommended — it didn't invent one. No correction needed, but this is the concrete reason the new CLAUDE.md guidance says a Step 8 review that never looks at the actual rendered graphic (as the earlier 2026-07-12 approval pass didn't, because the PNGs didn't exist yet) can miss real issues — verifying a surprising claim against its source, rather than assuming either fabrication or correctness, is what caught this cleanly either way.

**Standing process note (per Ridwan, 2026-07-12):** this Build Log should be updated any time the system changes, not just at the end of a work session — added as a saved preference so future sessions do this by default.

### 2026-07-29 — Page Presentation Kit CORRECTED v4: mosaic retired, mobile status bar added, caption rules generalized

Ridwan flagged two concrete problems with a live queue review and asked for both fixed properly, not patched: (1) he rejected the grid-mosaic full-page image outright — not its execution, the concept itself — and shared a reference showing what he wants instead: the whole page split into exactly two columns side by side. (2) every mobile mockup (stills and video both) was shipping with a completely blank strip under the notch where a real phone always shows time/signal/wifi/battery, which read as empty and unnatural.

**Mosaic → two-column split page.** Built `.ai-workflow/skills/page-presentation-kit/scripts/build_split_page.py`, replacing `build_mosaic.py` for all new work. Keeps the two genuinely useful parts of the old script (walk the page top-to-bottom first so scroll-triggered reveals fire before the screenshot, excise sustained dead/pinned-section zones before splitting) but produces exactly ONE split point instead of many tiles — snapped to the nearest real section gap near the vertical midpoint, not forced to an exact 50/50, so a column break never lands mid-section. Tested against the real `kura-hp-01` page: first pass over-corrected (a pure density-minimum search picked an extreme 30/70 split at the edge of its search window), fixed with a gap-proximity scoring approach that landed 52/48 on retest, clean section boundary, no truncated content. Output renamed `{slug}-full-mosaic.png` → `{slug}-full-page.png`; social-content key `-MOSAIC` → `-FULLPAGE`.

**Mobile status bar.** Built reusable `assets/frames/status-bar-dark.png` / `status-bar-light.png` (via `build_status_bar_asset.py`, regenerate from that script if the design ever needs a tweak, don't hand-edit the PNGs) plus `status_bar_util.py` for shared placement/variant logic. First implementation simply overlaid the bar on top of existing screen content and a live test caught it colliding directly with a page's own logo text ("9KURA41"). Redesigned around a RESERVED strip instead — the bar gets its own space at the very top of the screen rect, the screenshot/video is scaled to fill only the remaining height below it, so there's no possible collision. The strip's background is sampled from the content's own top-edge color (reads as a seamless continuation, not a seam) and the dark/light icon variant auto-picks from that same sampled color, the same idea as iOS's own "auto" status bar style. Built `build_device_still.py` as the new canonical script for the `cover.png`/`preview.png` still deliverables (previously ad hoc Playwright/PIL compositing with no named reusable script — every run redid it from scratch); it and `frame_video.py` (updated for mobile/cover video) both go through `status_bar_util.py`. Tested all code paths — single mobile still, cover still, 3-phone preview still, and framed mobile video — against real `kura-hp-01` screenshots/clips; all render correctly with no collisions and sensible auto-picked variants.

**Caption rules generalized project-wide.** The existing "no em dashes" rule (2026-07-28) was scoped to carousel slides only; Ridwan's instruction this time makes clear it applies to every generated caption/copy in the project — LinkedIn, X, slides, static ad text, CRO fix captions, everything — alongside the existing humanizer-skill and export-formatting (real line breaks, no markdown) requirements. Added a new top-level "Global Content/Caption Rules" section to `CLAUDE.md` so this isn't buried inside one skill's export-routing notes.

Updated `koolestpro-template-showcase-weekly`'s scheduled prompt to reference all of the above (new script names, renamed deliverable/key, explicit status-bar and caption QC lines in its Step 8 summary format) and `CLAUDE.md`'s "Page Presentation Kit — Export Routing" section (new "CORRECTED v4" subsection, updated asset tables, `build_mosaic.py` marked retired in place rather than deleted from the historical record).

**Same-day follow-up:** Ridwan reviewed the first status-bar fix and pointed out it was in the wrong place — a real phone's status bar sits at the same height as the notch/camera, flanking it left and right, not in a separate row below it. Recalibrated the actual transparent slivers beside the notch in `iphone-frame.png` (a live alpha-channel scan, not a guess) and rebuilt the status bar around that: content fills the full screen rect again (the flanking slivers sit entirely above where content starts, so there was never a real need to reserve space once the bar moved to the correct spot), the color-matching fill and dark/light auto-pick logic carried over unchanged. Replaced the single wide bar asset with four small chips sized for the narrow flanks. Verified across every code path including the ±10° rotated preview phones. Ridwan also offered reference phone-mockup templates for further quality improvements — flagged for follow-up.

### 2026-07-29 (3rd follow-up, same day) — Page Presentation Kit CORRECTED v5: 16 reference arrangement styles distilled into 8 named presets, background choice added

Ridwan followed through on the offer above and shared two reference sprite sheets, `Double Screen Template.png` and `Triple Screen Template.png`, saved directly to the project root — 8 phone-arrangement tiles each (16 total), using unrelated "Captain & Skipper" brand content as filler. His instruction: always build multi-phone previews using one of those 16 arrangement styles going forward, freely choosing 2 or 3 phones, on either the koolestpro brand gradient or a plain color, but always keeping the notch-flank status bar design from the fix above.

Cropped and inspected all 16 tiles individually. Several are minor variations of the same underlying geometry, so they collapsed cleanly into 8 reusable named presets added to `build_device_still.py` as a `STYLE_PRESETS` dict: `flat_even_2` (equal flat pair), `flat_stagger_2` (scale/height-staggered flat pair), `crossed_2` (angled crossing pair, moderate scale), `crossed_2_large` (same, larger/tighter) for 2 phones; `flat_even_3` (equal flat row), `flat_arc_3` (arc/stagger, center prominent), `fanned_stack_3` (overlapping card-fan stack), `angled_trio` (the skill's original hardcoded layout, kept as its own selectable preset rather than discarded) for 3 phones. `preview` mode's CLI gained `--style <name>` (required to match the screenshot count, with a clear error listing valid alternatives if it doesn't) and `--list-styles` to enumerate them.

Also added explicit background choice — `--bg-mode gradient` (unchanged brand orange-to-purple glow, still the default) or `--bg-mode plain --bg-color <hex>` — to `single`, `cover`, and `preview` modes. Omitting `--bg-color` under `plain` falls back to `REFERENCE_PLAIN_BG`, a real lavender (222,226,239) sampled directly from Ridwan's own reference tile rather than an arbitrary guess, since he explicitly said a plain color is welcome where it reads better than the brand gradient.

Captured 3 real mobile screenshots from the cached `kura-hp-01` page at genuinely different scroll depths (hero/mid/footer, via a walk-then-screenshot Playwright pass so the page's scroll-triggered reveal animations had actually fired rather than shooting blank/loading content) and test-rendered 4 of the 8 presets against them: `crossed_2` and `fanned_stack_3` on a plain background, `flat_stagger_2` and `flat_arc_3` on the brand gradient. All four rendered correctly — phones positioned/scaled/rotated per their preset, notch-flank status bar present and correctly auto-picking dark/light per phone (including on the rotated phones in `crossed_2`/`fanned_stack_3`, where the status bar rotates with the phone since it's composited before rotation).

Updated `CLAUDE.md`'s "Page Presentation Kit — Export Routing" section with a new "CORRECTED v5" subsection (full preset table mapped to reference tiles, background-choice usage, verification notes) and refreshed the stale "reserved strip" wording left over from the pre-notch-flank version in the asset table above it. Updated `koolestpro-template-showcase-weekly`'s scheduled prompt to require picking a named preset and varying it run to run (checking the last shipped `preview.png` before repeating a choice), and added a "PREVIEW STYLE" line to its Step 8 summary format.

### 2026-07-12 (later still) — CRO Fix stream automated end-to-end; export script made reusable

Closed the last gap in weekly automation: Static Ad (`koolestpro-static-ad-weekly`) and Template Showcase (`koolestpro-template-showcase-weekly`) already ran on a weekly buffer cadence; CRO Fix did not.

- **Generalized the one-off export script from earlier today** into `.ai-workflow/tools/export_static_images.py` — a proper CLI tool (any `content.html` in, any output dir out) instead of an inline script written fresh each time, plus `.ai-workflow/tools/bootstrap_env.sh` to make the ARM64 Playwright/libXdamage setup idempotent across cold sandboxes. Verified against the real V1CE file: all 9 assets (2 graphics + 7 slides + captions.txt) exported correctly in one command, byte-identical to the manual exports already on disk.
- **Wrote `.ai-workflow/weekly-pipeline.md`** as the canonical, self-contained procedure a fresh unsupervised session follows — target selection, audit, DeepSeek rebuild, real screenshots, the two graphics, static export, pipeline sync, target-pool update, social-content library update, tracker logging. Scheduled task prompts point at this doc rather than duplicating steps inline, so future edits apply automatically.
- **Created `koolestpro-weekly-cro-fix`** (Saturdays 09:06, offset from static-ad's 09:02 same morning) — completes all three streams on a weekly unattended buffer cadence. First live unsupervised run is this Saturday; Ridwan is doing a manual "Run now" test before then rather than trusting the cold run sight-unseen.
- **Sheet/Make.com handoff explicitly deferred, again:** Ridwan confirmed "it's not time for Make.com" — `outputs/weekly-tracker.xlsx` (local, via the `xlsx` skill) is the tracker for now. The Make connector is connected and each run's `manifest.json` is deliberately structured for a future handoff, but no scenario is being built yet.
- Documented all of the above in `CLAUDE.md` under "CRO Fix — Static Image Export & Weekly Automation."

### 2026-07-12 (later still) — Corrected Template Showcase's source, fixed the reuse-lockout bug, added pool-refresh automation

Ridwan asked directly how `targets_pool.json` works and whether it prioritizes existing `replo-rebuilds/brands/` pages for Template Showcase — surfaced two real bugs in the automation built earlier the same day, plus a genuine capacity question worth answering with real numbers instead of guessing.

**Bug 1 — Template Showcase was sourcing from the wrong pool.** `koolestpro-template-showcase-weekly` was built to pull a brief from `targets_pool.json` (the real-external-brand pool meant for CRO Fix / Static Ad) and build something new in `replo-rebuilds` every run. That's backwards — checked `replo-rebuilds/brands/` directly and found exactly one finished brand (KURA, 5 pages: PDP, Homepage, Listicle, Advertorial, Post-Purchase), none of which have been run through the koolestpro pipeline yet (`ridwan_content_system_updated.html` has zero `"Template Showcase"` items so far), even though all 5 already have captions drafted in `kura-social-content.md`. Fixed the task's selection order: check `replo-rebuilds/brands/*/pages/` for an existing, not-yet-showcased page FIRST (Step 1A), and only fall back to a `targets_pool.json`-driven new build (Step 1B) when nothing existing remains. Noted honestly that the existing-page well is shallow right now (5 pages, one brand) — sustaining this stream past the next few weeks needs either a 6th KURA page (a landing page — `templates/landing-page/` exists but is empty) or a new portfolio brand, both of which are real creative work per `replo-rebuilds`' own phased workflow, not something to rush inside a background task.

**Bug 2 — same-stream reuse was permanently locked out, contradicting the plan's own rule.** The operating plan's edge cases always allowed reusing a brand for the same stream again (different page/section/angle) — but `koolestpro-static-ad-weekly`'s literal selection logic ("no usedFor entry for this stream") would exclude a target from that stream forever after one use, with no path back. This is the same class of bug as the V1CE `status` lockout fixed earlier today, just at the `usedFor` level instead of `status`. Fixed the task's Step 2 to prefer zero-usedFor targets first, but explicitly allow reuse-with-a-different-angle once the fresh pool for that stream runs low, with a required note in both the new `usedFor` entry and the run summary so reuse is never silent. Documented the general rule in `targets_pool.json`'s schema notes and in this doc's Step 2 section, so it's there for whenever CRO Fix gets its own scheduled task.

**Capacity, with real numbers:** 12 targets, tracked per-stream via `usedFor`, not a shared counter — at weekly cadence that's roughly 12 weeks (~3 months) before a given stream has touched every target at least once. Static Ad is the only stream actually running weekly today; CRO Fix is still manual, so its clock runs slower.

**New: `koolestpro-target-pool-refresh` scheduled task (Fridays 08:09, ahead of Saturday's static-ad and Sunday's template-showcase runs).** Automates Step 1 (pool maintenance) as a threshold check rather than a fixed cadence of additions: computes each active stream's "fresh count" (targets with zero `usedFor` entries for that stream), does nothing if every stream has 4+, and only researches ~5 new candidates when one drops below that. Every new candidate must be genuinely reviewed at a real mobile viewport (via the project's existing `screenshot.py` Playwright tool) before its `mobileIssueSummary` gets written — never guessed from search snippets, matching how the original 12 were built. This task only ever adds to the pool; it never selects, builds, or publishes anything itself.

### 2026-07-12 (later still) — Aligned the parallel CRO Fix pipeline to the corrected reuse pattern

While answering a question about how `targets_pool.json` works, discovered `koolestpro-weekly-cro-fix` (Saturdays 09:06) and its procedure doc `.ai-workflow/weekly-pipeline.md` already existed — built in a parallel session/track, not part of this session's earlier work, timestamped the same day. It generalizes several things from this session's V1CE work (the export script, the ARM64 bootstrap, the verify-against-real-export lesson), which is good, but its target-selection logic (Step 2: filter `status != "Used"`) and marking logic (Step 10: set `status: "Used"`) still used the pre-fix pattern — the exact bug that locked V1CE out of every stream, not just `cro-fix`, corrected earlier today.

**Fixed at Ridwan's request:** `weekly-pipeline.md` Step 2 now filters on `status == "Available"` **and** no `usedFor` entry for `stream: "cro-fix"`, with the same reuse-allowed-with-a-different-angle rule as the other two streams. Step 10 now appends an object-format `{stream: "cro-fix", date, pipelineItemId}` to `usedFor` and explicitly leaves `status` untouched. All three producing tasks (`koolestpro-static-ad-weekly`, `koolestpro-template-showcase-weekly`, and now `weekly-pipeline.md` for `koolestpro-weekly-cro-fix`) are consistent with each other and with `targets_pool.json`'s own schema notes as of this entry.

**Worth knowing going forward:** since CRO Fix is now weekly-automated (not manual, as earlier entries today assumed), two streams draw from the same 12-target pool every week, not one — `koolestpro-target-pool-refresh`'s per-stream threshold check (built earlier today) already accounts for this since it checks `cro-fix` and `static-ad` independently, but the pool will likely need its first real top-up sooner than the original "~3 months" estimate assumed.

### 2026-07-12 (later still) — Content system sync sweep found real backlog drift

Ridwan asked to bring `ridwan_content_system_updated.html` fully up to date. No loose `_pipeline.json` exports were waiting outside the system (Step 1/JSON Ingestion had nothing pending there), but a direct check of `outputs/tips/` against `SYNC_DATA.items` turned up drift that had built up silently over the April–May run:

- **One real export was never merged at all** — `outputs/tips/the-conversion-layer-before-you-touch-design.json` (id `tip-the-conversion-layer-1777028149144`, status `Created`, real file on disk) existed as a sidecar file since 2026-04-24 but was never ingested into `SYNC_DATA.items`. Merged now.
- **Three built tips/CRO-fix pieces existed as finished HTML files but their pipeline items were still sitting at `status: "Idea"` with `folder: null`** — meaning the content system had no idea they were already written: `5-liquid-snippets-cart-abandonment_20260514.html`, `cold-warm-hot-page-matching_2026-05-10.html`, `why-your-pdp-loses-sales-at-60-scroll_2026-04-29.html`. Linked and marked `Created`.
- **Two items claim `status: "Created"` with a `folder` pointing at a file that does not exist on disk** — `tip-your-product-description-is-doing-nothing-here-s-t-1776764798412` (→ `..._2026-04-21.html`, missing) and `tip-why-your-pdp-loses-sales-at-60-scroll-brief-audit--1777031016447` (→ `..._brief-audit-_2026-04-24.html`, missing — this item's `title` field also looks corrupted, it has the brief/angle text pasted directly into the title, likely a tip-generator bug from that run). Left untouched and flagged to Ridwan rather than guessed at — per the File Linking rule, Cowork should flag missing-file links, not silently "fix" them without knowing what actually happened to the file.
- **One orphan file has no pipeline record at all** — `outputs/tips/shopify_page_types_carousel.html`. No id/title anywhere in `SYNC_DATA.items` matches it. Flagged, not fabricated an entry for it (would violate "no fake metrics or values" in spirit — a title/type would have to be guessed).

`meta.updatedAt`/`meta.syncHash` recomputed after the merge (sha1 of `{months, items}`, first 12 hex chars, matching the existing `computeSyncHash` convention in `lib/cowork_runtime.js`).

**Worth knowing going forward:** this kind of drift happens because output-generating skills sometimes export a pipeline JSON sidecar without Cowork actually running the merge step in the same session (the-conversion-layer case), and because early idea-batch items don't automatically get `status`/`folder` updated when someone later hand-builds the HTML outside a scheduled/tracked run. Worth a periodic "does every `outputs/tips/*.html` file have a matching `Created`+ item, and does every `Created`+ item's `folder` actually exist" sweep — not just reacting to explicit JSON exports.

### 2026-07-12 (later still) — New inbound track: Template Showcase now targets new-store-build leads

Ridwan is adding a second inbound audience alongside CRO Fix's existing-store owners: store owners who need a brand-new online store built. Asked to keep it content-only (no new outreach/tracking file) — Template Showcase already produces the right proof-of-work, it just needed a CTA split. `koolestpro-template-showcase-weekly`'s Step 3 now carries a CTA FRAMING RULE: Template Showcase captions close toward "need a store built," CRO Fix/Static Ad keep their audit/fix framing. Documented in `CLAUDE.md` under "Template Showcase = New-Store-Build Inbound Track." If this later needs active lead tracking, the plan (also documented) is a `leadType` field on a schema like `outreach_tracker.json`'s, not reusing `targets_pool.json` — that pool's schema assumes an existing store to audit.

### 2026-07-12 (later still) — Tips carousel automated; corrected a real geometry drift while doing it

Ridwan asked to automate the Tip carousel stream (previously the only one of the four content types still fully manual) and to fix the carousel "instructions" so they work right. Auditing `koolestpro-content-engine`'s SKILL.md against the project's own gold-standard reference file (`outputs/tips/funnel-awareness-framework_2026-05-10.html`) turned up real drift: the skill's written spec says 540×540 square slides, `scale:4` + manual downsample to 1080×1080, and a `captureSlide()` sample with no chrome-hiding — none of that matches the actual reference file (540×680 portrait, `scale:2`, explicit `toHide` sweep, no downsample). Cowork can't edit the skill file itself (read-only cache this session), so the fix lives in `CLAUDE.md`'s new "⚠️ Tips Carousel — Corrected Gold Standard Spec" section, which explicitly overrides the skill's geometry/capture instructions for anything built in this project. Also corrected: the skill's own text implies Claude writes the full HTML directly, which conflicts with this project's AI Workflow Architecture (HTML is always DeepSeek's job) — the new `koolestpro-tips-weekly` scheduled task is written to do Phase 1 (brief/copy) in Claude and delegate Phase 2 (HTML) to DeepSeek, same as every other stream.

**Format decision, backed by 2026 engagement data (via web search):** carousels/document posts are the top-performing organic format on LinkedIn (45.85% engagement rate, 3.4x reach vs single-image, per a Metricool study of 577K posts); myth-busting/contrarian content drives comments specifically via polarization and cognitive dissonance — the strongest single engagement lever in 2026 platform data. Defaulted new Tips carousels to a "Myth vs Reality" contrarian-diagnostic format in the Conversion Strategy pillar, framework carousels as the fallback when a topic has no genuine myth to bust. Also nudged the slide-count default from 8 toward 7 (7-slide LinkedIn carousels outperform other lengths ~18% per 2026 data), without overriding the skill's own "less is always better, don't pad" logic.

**Topic sourcing:** `koolestpro-tips-weekly` pulls from the 30+ unused "Idea" backlog items surfaced in the content-sync sweep above before ever generating something new — and updates the existing item's `id` in place rather than creating a duplicate, to not repeat the exact drift this session already found and fixed once today.

Runs Sundays (after `koolestpro-template-showcase-weekly`). Added `TIP-{BRAND}` to the Per-Brand Social Content Library key scheme (only Static Ad/CRO Fix/Template Showcase had keys before).

### 2026-07-12 (later still) — CRO Fix before/after graphics: bigger, bolder typography; GPT-image confirmed as non-default

Ridwan flagged that the coded `#ba-graphic`/`#anno-graphic` templates weren't visually appealing enough on mobile and said GPT-image's output (tested 2026-07-07) looked better, but running GPT-image at weekly production volume is too expensive to use routinely. Checking the actual V1CE build found the real gap: the headline was shipping at `font-size:32px` on a ~1060px-wide canvas — about 3% of canvas width, unreadable as a scroll-stopping hook at mobile feed-thumbnail scale. That's a template-execution gap, not a fundamental limit of the coded approach.

**Fix:** added an explicit Typography subsection to `.ai-workflow/project-constitution.md`'s canonical before/after & annotation spec — headline bumped from 32px to 52-60px (Syne 800, solid color per the existing hard gradient-text ban), sub-line from 12px to 15-16px, plus a "shrink to thumbnail size and check it's still readable" test before shipping. Also noted: worth flagging to Ridwan that Skill E's own SKILL.md already has a checklist line from 2026-07-07 saying he rejected GPT-image as "not good enough" — today's framing was the opposite (liked the output, cost is the issue) but the practical decision is the same either way: coded template stays canonical, GPT-image stays a manual-only fallback for cases the coded template genuinely can't do.

### 2026-07-12 (later still) — Page Presentation upgraded to a full 10-asset set per page, grounded in real Kura files

Ridwan flagged that `koolestpro-template-showcase-weekly` was under-delivering: it picked a single mockup style and explicitly skipped the video most runs. He pointed directly at `replo-rebuilds/portfolio/images/exports/kura *` as the real, already-proven target output — every KURA page (and several other brands) already ships with 3 videos (cover/laptop/mobile) and roughly 7 images (polished cover + laptop mockups, a raw full-page screenshot, 3 raw mobile crops, and a composed hero collage). Inspected the actual files directly (PIL for images, ffprobe for video) to get real dimensions rather than guessing: 960×720 for cover/laptop video, 1080×1350 portrait for mobile video, 1440×1080 for the polished cover/laptop stills, ~1155×1200 for the raw full screenshot, 675×1461 for the raw mobile crops, 2880×1800 for the preview collage.

Documented the full spec in `CLAUDE.md` under "⚠️ V1 Full Asset Set" and rewrote `koolestpro-template-showcase-weekly` to always produce all 10 assets, never a single mockup. Real gap found: `page-presentation-kit`'s built-in `composite_frame.py` only draws plain CSS rounded-rect device frames, not the photoreal bezel-with-notch look in Ridwan's reference shots — the task now includes a one-time device-bezel calibration step (laptop + iPhone PNGs with transparent screen-cutouts, generated via `gpt-image`, mirroring the skill's own `device-in-hand-lifestyle` calibration pattern), reused afterward via a DeepSeek-built HTML/CSS compositing template for stills and an `ffmpeg overlay` filter for the cover video. Per this project's AI Workflow Architecture, that compositing work is DeepSeek's job — Ridwan explicitly offered this himself, since the original assets were hand-built in Figma.

Format sizes were NOT changed to some new "universal" dimension — kept the already-proven 4:3 (cover/laptop) and 4:5 portrait (mobile) ratios, which are safe non-destructive-crop sizes across Instagram/LinkedIn/Facebook and already validated across dozens of real shipped exports.

**Not yet proven live:** this is a documentation + task-rewrite pass, not a live-tested run — the device-bezel setup in particular needs its first real execution and a visual spot-check against Ridwan's reference images before being trusted going forward. Flagged explicitly in both `CLAUDE.md` and the task's own Step 8 summary requirement.

Also clarified this session: for CRO Fix carousels, only the before/after evidence slide (e.g. V1CE's slide 5) uses a real screenshot — every other slide is GPT-image-generated per the existing preference. This is separate from the `#ba-graphic`/`#anno-graphic` typography fix earlier today, which is about the standalone before/after and annotation graphics, not the carousel slides.

### 2026-07-12 (later still) — Page Presentation v1 spec reviewed against its own first real output, corrected to v2

The first live run of the rewritten `koolestpro-template-showcase-weekly` produced `outputs/templates/v1ce_tap-review-card-pdp_2026-07-12/`. Ridwan reviewed the actual output (not just the spec) and rejected it: no real device bezel anywhere (a raw screenshot with a thin CSS border stood in for a phone frame), the "full page" shot was a partial mobile-viewport capture instead of the whole desktop page, backgrounds were flat grey/black instead of this project's brand gradient system, the 3-phone collage left most of its canvas empty, every asset saved twice under two filename conventions, and — root cause of several of the above — replo-rebuilds wasn't connected for that run, so it silently fell back to reusing an internal page instead of showcasing real replo-rebuilds work.

Corrected in `CLAUDE.md` under "⚠️ V1 Full Asset Set — CORRECTED v2": cut the image list from ~7 down to exactly 3 designed deliverables (cover.png, preview.png, full-mosaic.png) plus the 3 videos, per Ridwan's own instruction to simplify to a fixed reference template. Bigger fix: Ridwan provided his actual Figma-exported device mockup frames (`MacBook Pro.svg` ×2, saved to `assets/frames/macbook-pro.svg` / `-alt.svg`) — read directly as vector source to get exact screen-region coordinates (x:199-1812, y:74-1048 in a 2011×1171 viewBox) rather than needing any AI-generated bezel. This replaces the earlier GPT-image-bezel plan entirely for the laptop. The iPhone frame is still outstanding — Ridwan showed it inline in chat but didn't upload the actual file, so it can't be calibrated yet; flagged as a blocking dependency for the next run.

Also flagged to Ridwan directly (not yet resolved): the scheduled task's own execution context apparently doesn't have the same replo-rebuilds folder connection this live chat session has, even though it's one of the three folders connected here. Two likely fixes suggested: check Cowork's folder/connector settings for the scheduled task specifically, and/or trigger one manual "Run now" so any connection permission prompt can be surfaced and approved (tool approvals persist onto future runs per the scheduling tool's own documentation).

### 2026-07-12 (later still) — iPhone frame calibrated; both device frames now ready

Ridwan tried attaching the iPhone frame file directly in the "Edit scheduled task" dialog (visible in a screenshot he shared, with an "Unable to open file" error) — that dialog is task config only, not a file-attachment surface. He instead dropped the real file (`Apple iPhone X Space Grey (1) copy.png`) directly into the koolestpro-cowork-v2 project folder, which is the correct approach when a file already lives on his machine.

Calibrated it the same rigorous way as the MacBook SVGs, but via alpha-channel scanning instead of vector parsing (PNG, not SVG): scanned the actual alpha channel for opaque-to-transparent boundaries rather than eyeballing coordinates from the chat preview. Result: 450×974px canvas, screen-cutout region x:22-428, y:59-949. Saved to `assets/frames/iphone-frame.png`. Both device frames (`macbook-pro.svg`/`-alt.svg` and now `iphone-frame.png`) are fully calibrated — `koolestpro-template-showcase-weekly` no longer needs any fallback/placeholder path for missing device bezels. Updated in `CLAUDE.md`'s "V1 Full Asset Set — CORRECTED v2" section and the scheduled task itself.

The replo-rebuilds connectivity gap is still open — Ridwan's screenshot showed what looks like a per-task folder selector in the Edit dialog already showing "replo-rebuilds," which may mean it's already configured; this needs confirming on the next actual run rather than assumed fixed.

### 2026-07-12 (later still) — Replo-rebuilds connectivity gap confirmed and resolved with a local sync cache

Ridwan clicked "Run now" with the new Step 0 diagnostic in place: all 3 access methods (relative path, absolute Mac path, shell directory listing) failed, definitively confirming the scheduled task cannot reach `replo-rebuilds` live — not a config oversight, a real architectural limit (scheduled tasks have one project dropdown, no "add folder" option).

Given the choice between a synced manifest, a manual per-run copy step, or accepting the lower-value internal-page fallback permanently, Ridwan chose the sync file. Built `replo-rebuilds-pages.json` at the koolestpro-cowork-v2 root plus `replo-pages-cache/` holding real local copies of all 5 shipped KURA pages (pdp-01, hp-01, li-03/listicle, ad-01/advertorial, pp-01/post-purchase) and a cached copy of `kura-social-content.md`, populated by scanning replo-rebuilds directly in this session (both folders were connected together here). Rewrote `koolestpro-template-showcase-weekly`'s Step 1 to read this local cache as its primary path — genuinely local, not a live cross-project call — with Step 1B (internal-page fallback) now only triggering if every cached entry has already been used. Step 5 was updated to mark a cache entry's `usedForTemplateShowcase` true once it's showcased, so the same page doesn't repeat.

Refresh is manual: next time both projects are connected in one session and a new replo-rebuilds page ships, re-copy its folder into `replo-pages-cache/` and add an entry to the manifest. Documented under CLAUDE.md's new "Replo-Rebuilds Local Sync Cache" subsection.

### 2026-07-13 — First real Template Showcase run reviewed: videos too fast, 2 of 3 unframed, mosaic had dead panels — fixed with two new reusable scripts

`koolestpro-template-showcase-weekly` ran end-to-end for the first time on `kura_hp-01` (from the new local sync cache). Ridwan reviewed the output and flagged real, specific problems: the videos scrolled too fast (actual durations 8s/19s/13.7s against a 25-30s target), only `cover.mp4` had a device bezel and it was off-center with the phone clipped off-canvas, `laptop.mp4`/`mobile.mp4` shipped as bare unframed screen recordings, and `full-mosaic.png` had large blank navy tiles. He explicitly did not want to spend more pipeline credit re-testing the same page.

Root-caused by reading the actual scripts rather than guessing: `scroll_video.py`'s `--duration` defaults to 6s and the v2 spec never pinned a real target; the v2 spec also only required bezel-compositing on `cover.mp4`, never said "all three." The mosaic's blank tiles turned out to be a GSAP scroll-pinned section on the KURA homepage — its visual state is a function of live scroll position, so a static full-page screenshot fundamentally can't show it "revealed," no matter how the slicing works.

Since none of these fixes touch DeepSeek or GPT-image (video framing and mosaic slicing are pure Playwright/ffmpeg/PIL, already specified as Claude's own job, not DeepSeek's), they cost zero paid API credit to build and verify locally against the already-cached `kura-hp-01` page. Built two new reusable scripts in `.ai-workflow/skills/page-presentation-kit/scripts/`:

- `frame_video.py` — composites a raw `scroll_video.py` capture into the real calibrated device bezels (all 3 video variants, not just cover) on the brand-gradient background. Along the way, discovered the source SVG frames actually paint a solid dark screen-fill rather than being transparent there as assumed — fixed by pre-rendering the SVGs to raster PNG and forcibly punching the screen-rect region to true alpha=0 in PIL (`assets/frames/macbook-pro.png` / `-alt.png`).
- `build_mosaic.py` — walks the page top-to-bottom in steps first so one-shot reveal animations fire, then detects and excises sustained near-uniform vertical runs (the scroll-pinned dead zones) before tiling, instead of blindly cutting through them.

Verified both locally: laptop/mobile/cover videos now land at 29.7-30.2s with correctly centered bezels on all three; the mosaic went from 3 broken tiles (2 fully blank) to 8 tiles with real content, with one small residual seam at an excision boundary flagged honestly rather than hidden. Regenerated `outputs/templates/kura_hp-01_2026-07-13/`'s videos and mosaic in place with the fixed versions (originals kept in a `_v1_originals/` subfolder), updated that run's companion page honesty note, and updated CLAUDE.md's Page Presentation spec to "CORRECTED v3" plus the scheduled task itself so the next run — on a different cached page, not kura_hp-01 again — validates the fix on fresh output rather than repeating the same page.

### 2026-07-14 — V2 distribution plan interviewed and written; V1 declared "good enough to build on"

Ridwan asked directly whether the system was ready for "V2." Answer at the time: no — CRO Fix and Tips weekly had never had a live unattended run, Template Showcase had exactly one run (with same-day fixes, unvalidated on a second page), and nothing in the system actually posts anywhere; everything stops at a reviewable buffer folder. He confirmed the scheduled tasks are already tested/proven even though he personally hasn't triggered most of them yet, and clarified V2's actual scope: determine a full cross-platform (LinkedIn/Instagram/Twitter) weekly content calendar, then wire it to a Google Sheet + Make.com so posting happens automatically with a human approval gate — not a rebuild of generation itself.

Ran a full `/process-interviewer` session to extract the plan rather than guessing at it. Key decisions, all confirmed with Ridwan directly:

- **Global rule:** carousel-format posts never go to Twitter; single images and videos do. LinkedIn caps at 1 post/day (posting twice same-day was confirmed via 2026 research to suppress the earlier post's reach) — this is why CRO Fix's before-after + annotated became one 2-slide carousel instead of two separate LinkedIn posts.
- **Weekly hero rotation:** LinkedIn Mon (Tips) / Wed (CRO 2-slide carousel) / Fri (Template Showcase video); Instagram daily with the CRO 7-slide narrative carousel and Static Ad 4-image carousel each getting their own Instagram-exclusive day; Twitter 3x/day, image-only (no text-only filler — Ridwan explicitly rejected that lever), with ~8 of 21 weekly slots filled by reposting assets under a different caption angle, and Wednesday's one thread slot replacing (not adding to) that day's 3 posts.
- **Real unlock found mid-interview:** every generator already writes multiple Twitter-ready caption variants (Hook Variations, Twitter Angles, X Singles, Twitter Thread) directly into its companion HTML — confirmed by reading the actual uploaded output files (`v1ce_tap-review-card_content.html`, `shopify_page_types_carousel.html`, two Template Showcase/Static Ad `index.html` files). The caption-reuse problem for Twitter volume was never a copywriting gap, it's a plumbing gap — nothing extracts that text out of the HTML tabs into anything Make.com could read. Tab IDs differ per skill (documented in the plan) — a harvest script needs a per-skill parser, not one generic selector.
- **Generation schedule moved to spread Ridwan's weekly Cowork credit budget** (renews Fri ~2-3pm ET, typically exhausted by Wed, dead Thursday): Tips + Static Ad → Friday, Template Showcase → Saturday, CRO Fix → Sunday, Target Pool Refresh → Monday and dropped to biweekly. Confirmed safe because generation has always been buffer-ahead-of-need, not same-day — a Tuesday generation still has 6 days of runway before the next Monday.
- **New QA pass, agreed as flag-not-block:** every generated piece gets an automated check (file existence, export-compatibility scan, actual visual inspection of the rendered image, claims spot-check against source, caption-asset match) before it reaches the Sheet as a `Draft` row — codifies lessons from real past incidents (V1CE's HSBC/IBM claim scare, the unframed-video Template Showcase run) into something that runs every time instead of relying on memory.
- **`ridwan_content_system_updated.html` survives V2**, repurposed as a read-only visual mirror of the Sheet with working click-throughs to each post's real source file — not dropped, not left as a second manually-maintained tracker. The known-broken/orphaned entries and the old Tips backlog found in the 2026-07-12 sync sweep were explicitly confirmed as not worth fixing — Ridwan isn't working toward that backlog right now.
- **Checked against current product docs, not assumed:** re-verified on 2026-07-14 that Cowork scheduled tasks still support only one folder each — the `replo-rebuilds` cross-project access limit from 2026-07-13 hasn't changed. Added a reminder-only staleness-check task instead of pretending a real fix exists.

Full plan written to `koolestpro-v2-distribution-plan.md` (project root) using the process-interviewer's plan template — includes the Google Sheet column schema, the exact harvest/QA/approval/Make.com pipeline order, and an explicit Open Questions section (Make.com scenario mechanics — polling interval, retry policy — were not covered in this session and need their own follow-up; same for an Instagram/Twitter fallback when a stream fails to generate, which LinkedIn already has and IG/Twitter don't yet). Nothing in this plan has been built yet — it's a handoff document, not an implementation.

### 2026-08-23 — Template Showcase run 7 (halos_lp-01): split-point snapping fixed, HALOS cache now exhausted

Weekly `koolestpro-template-showcase-weekly` run against `halos_lp-01` (direct-response landing page), the last unused active page in `replo-rebuilds-pages.json`. Two real defects found by the mandatory two-tier QA and fixed rather than shipped:

- **Tier 1, script-level fix in `build_split_page.py`.** `choose_split_point()` accepted a low-density run of ANY length as a "section gap", so a 1-2px band of flat background *inside* a section could win purely by sitting nearest the midpoint. On this page it did exactly that: the first cut landed at y=2738 (precisely 50.0%), slicing through the middle of a 3-across benefit-card row. Added a `min_gap_run=40` filter so only sustained whitespace bands qualify. The cut moved to y=2792, the real seam just above the proof wall, and column 1 now ends on a complete section. This is a general fix, not a per-page tweak, and it applies to every future full-page split.
- **Tier 2, companion-page fix.** `.x-post` had no `white-space: pre-wrap`, so the real line breaks inside each X post collapsed into a single paragraph, meaning the copy displayed on the review page no longer matched the export-ready text stored in `halos-social-content.json`. Added pre-wrap. Worth knowing: the same omission exists in the earlier `halos_hp-01_2026-08-18/index.html`, left as-is rather than retro-edited.

Two things to note about video duration on this run. Raw `scroll_video_raw.py` captures came in at 51.8s (desktop) and 41.8s (mobile) against a nominal `--duration 26`, longer than the 30-38s observed in previous runs. Frame extraction across each full timeline confirmed genuine, continuous scroll progression reaching the real footer with no stall or jump-cut, which is the property that actually matters, so both were kept. If a future run wants to land nearer the original 25-30s target on this sandbox, the lever is `--duration`, not `--steps`.

**Action needed from Ridwan:** all three active HALOS pages are now marked `usedForTemplateShowcase: true`. `replo-rebuilds-pages.json` has zero eligible active entries left, so next week's run will have to fall back to a retired KURA page unless the cache is refreshed with new `replo-rebuilds` pages the next time both projects are connected in one interactive session.

### 2026-08-28 — Tips weekly run: checkout payment-method myth + X-singles label-convention bug root-caused

**Carousel shipped.** `outputs/tips/checkout-payment-method-myth_2026-08-28.html` ("You added Apple Pay. They still left."), 7 slides, Myth vs Reality, Conversion Strategy pillar. Backlog item `idea-checkout-abandonment-fix-the-payment-method-order-1777030231175-ebzqg` updated in place, no new id. Trend-radar was stale (latest entry 2026-W33 against a current 2026-W35), so the original backlog-first fallback ran as designed.

**Every figure is primary-source, and a widely-circulated wrong one was caught.** Secondary aggregators are currently reporting "19% of shoppers abandon because their preferred payment method wasn't offered" and attributing it to Baymard. Fetching Baymard's own page directly shows 19% is their *credit-card-trust* line; the payment-methods line is **9%**. The carousel and all five copy tabs use the real numbers (40% extra costs, 9% too few payment methods, 12% couldn't calculate the total, 23.48 average form elements vs an ideal 12-14). Do not reintroduce the 19% figure.

**Two defects caught by actually looking at the exported PNGs, both fixed and re-exported:**
- Slide 3's field-count comparison drew 12 vs 7 rows for a slide whose entire claim is "23.48 vs 12-14". The row count *is* the claim on that kind of visual, so it now draws a literal 23 and 13. Worth generalising: any built visual that stands in for a cited number has to match the number.
- The cover's chart card centred its three children and left a dead band under the footnote. Switched to `space-between` so the footnote pins to the card's bottom edge.

**X-singles caption bug — root cause found, not just observed.** `koolestpro-tips-weekly` output for 2026-08-14 (trust-signals) and 2026-08-21 (thumb-zone) both carry a live QA flag: `x_angles[0]=435 chars` / `430 chars`, meaning all three single tweets were glued into one over-limit blob. `harvest_content.py`'s `TWEET_LABEL_RE` only splits on a label line whose **last** character before the newline is a colon: `Tweet A (The Rule):` or `ANGLE A:`. Both of those runs used a bare `THE RULE` heading, which never matches, so the splitter silently returned the whole panel as one caption. This run uses the `Tweet A (The Rule):` convention and verifies the split programmatically before registering: 3 separate tweets at 142/137/149 chars. **Every future Tips run must use that exact label shape** and assert the split rather than assuming it.

**Still outstanding for Ridwan:** the 2026-08-14 and 2026-08-21 pipeline items still hold the glued blob and both have Draft/Ready distribution rows scheduled against it. They were left untouched rather than silently rewritten from an unattended run, but they will be rejected by X for a non-Premium account if they go out as-is.

## Success Criteria

The plan is working when:

- Ridwan can produce 3 high-quality LinkedIn posts per week from the system.
- Ridwan can queue 15 X proof-of-work posts per week from the same work.
- Every real-brand concept creates a matching outreach asset.
- Approved posts are tracked locally and pushed to the publishing queue.
- The content visibly shows CRO, Shopify build quality, and practical ecommerce improvement.
- The process reduces manual work without reducing quality.
- The system generates leads, replies, booked calls, or portfolio-worthy proof that supports future client acquisition.


### 2026-09-02 — `{slug}-mobile-strip.png` became a mandatory Template Showcase asset with its own X post, and was enforced rather than just documented

**Where it came from.** During the Wednesday `koolestpro-weekly-template-build` run (HALOS listicle, `halos-li-02`), a throwaway QA contact sheet was generated to review the mobile render: the full mobile page sliced into 6 equal columns placed side by side. Ridwan saw it and asked for it to become a real deliverable: "I love this image, add it to outputs and preview in the future and it should be registered as a type of template for template showcase type of posts and it should always be posted in my x account."

**What it is.** `{slug}-mobile-strip.png` — the entire page at MOBILE viewport width, split into ~6 columns, flush with no outer frame. It is the 4th designed image in the Template Showcase set. It does **not** replace `{slug}-full-page.png`: that one is desktop width in two columns on a neutral canvas, this one shows how the responsive build actually behaves on a phone, end to end, in one frame. Social-content key `TS-{BRAND}-MOBILESTRIP`. Full spec in CLAUDE.md "⚠️⚠️ CORRECTED v8".

**Built by** `.ai-workflow/skills/page-presentation-kit/scripts/build_mobile_strip.py`. It shares `build_split_page.py`'s capture and density analysis rather than duplicating them, so the sticky-header / fixed-element / reveal-animation fixes stay in sync across both. Three things in it are load-bearing:
- Spacing defaults are flush (`pad=0`, `gap=0`) on purpose — that is the composition Ridwan approved, and it is deliberately the OPPOSITE of `preview.png`'s margin-bigger-than-gap rule (CORRECTED v7). Do not "fix" one to match the other.
- Column cuts snap to real section seams (generalizing `build_split_page.py`'s single-cut logic to N-1 cuts) so no boundary slices through a section. Because seam-snapped columns end at different heights, each short column's remainder is filled with the average colour of its own bottom edge, otherwise the strip ends in hard white voids.
- It falls back to tile stitching when `full_page=True` crashes the renderer, which is real and reproducible on image-heavy pages in this sandbox even with `--disable-dev-shm-usage`.

**Scope, widened the same day.** The first decision was "Template Showcase only". Ridwan overrode it within the hour: "Whatever we do, anywhere we are building new pages and anywhere we are doing template showcase, we want to make sure this does not escape." So the Wednesday page-build task now saves a strip into each new page's own `presentation/` folder, and the Saturday showcase task reuses it (or rebuilds it if stale/missing). Still not generated for CRO Fix rebuilds.

**Distribution.** Ridwan chose to ADD a 5th X post rather than displace any of the four existing angles. X #5, Sunday 11:00 ET, angle "full page at a glance". Added to the "Template Showcase", "Store Template" and "Store Template (Paid)" calendars in `populate_sheet.py`, each with its own `x_glance` caption key (falling back `x_glance → x_showcase → x`) so the strip post cannot silently recycle another angle's caption. `harvest_store_template.py` maps the angle text to that key.

**Why this needed enforcement and not just documentation.** Ridwan's actual concern was that it would quietly go missing: "If it has not been seen, we want to make sure this is not skipped." A prompt instruction is the weakest possible guarantee — a run that goes long, hits a renderer crash, or is executed by a future model that skims the prompt will drop it and nothing will notice. Four guards were added beyond the prompts:

1. **The calendar slot itself.** Without a slot the asset could exist and still never be scheduled.
2. **Compressed-sibling preference in `resolve_assets()`** — when a matcher hits both `foo.png` and `foo-x.jpg`, the compressed one wins. This generalizes the narrow `full-page-x` hardcode from the 2026-08-01 Bebemoss incident (Make's fetch limit rejected an 8.3MB image and blocked that day's X post) and means a matcher of plain `mobile-strip` is safe whether or not the oversized sibling exists.
3. **A recovery gate in the Monday assembly task** (Step 2b) — a package arriving without a strip gets one built on the spot rather than silently producing one fewer X row.
4. **`audit_mobile_strips.py`**, run weekly by the Monday `koolestpro-replo-cache-staleness-check` task. Sweeps three independent failure points (source pages, shipped packages, assembled queue rows) and splits NEW gaps from the historical backlog, exiting non-zero only on a new gap so the check stays a real signal.

**Known backlog, deliberately not backfilled:** 11 shipped packages, 10 source pages and 8 assembled queue items predate the asset. Backfilling each costs a Playwright capture, and re-running `populate_sheet.py` on an already-assembled item would append an X row to a week that has already passed. The audit reports the count and leaves the decision to Ridwan.

**Also fixed in the same session** (found while building `halos-li-02`, patched upstream into `templates/listicle/li-02-single-benefit/index.html` so future brands inherit them): the template was missing `html, body { overflow-x: hidden; }`; the offer strip's discount-code chip sat 4px from the CTA and read as one merged blob; and the comparison table carried `min-width: 460px` against a ~308px mobile wrapper, pushing the entire "losing" column off-screen with no scroll affordance.

### 2026-09-26: Project moved to GitHub, out of ~/Downloads, and the lead importer unblocked

**Why.** Ridwan wants to keep working when he is away from the Mac, from any AI tool (Claude, Codex, others) and from his phone, without relying on one vendor's cloud.

**What changed.**
- The folder is now a git repo pushed to `github.com/koolestpro/koolestpro-cowork-v2` (private). `.gitignore` keeps out `.env` files, rendered video, `node_modules`, `.next` and caches (about 490 MB tracked, down from 5 GB on disk). `.env.example` lists every key name.
- `site/`, `cold-email-app/` and `replo-rebuilds/` are submodules pointing at their own repos (`koolestpro`, `cold-dm-app`, `koolestpro-portfolio`).
- The 38 project skills from the Claude account were copied to `.agents/skills/`, with `.claude/skills` symlinked to it, so Codex and Claude read the same skill files. `AGENTS.md` now points there.
- `scripts/setup-github.sh` (one-time) and `scripts/git-sync.sh` (hourly launchd job `com.koolestpro.git-sync`, pull then push, never forced) keep the Mac and GitHub in step. Guide: `docs/work-from-anywhere.md`.
- The project moves from `~/Downloads/koolestpro-cowork-v2` to `~/koolestpro-cowork-v2`.

**Bridge failure found.** `leadgen-import.launchd.log` had 1,028 lines of `Operation not permitted` and no successful run. macOS privacy protection (TCC) blocks launchd's `/bin/bash` from reading `~/Downloads`, so the importer fired every 30 minutes and never ran. Five lead files from W36 to W38 were stuck in `.ai-workflow/pending-push/`. The repo's plist already pointed at `~/koolestpro-cowork-v2`, but the folder was never moved. Moving it fixes this.

**Cloud scheduled tasks.** Only 4 of the 12 live tasks exist as cloud tasks (recreated 2026-09-25): system status, distribution assembly, target pool refresh and template showcase. The template showcase run on 2026-09-26 was marked succeeded but finished in 6 seconds and wrote no files. That means the session could not reach the Mac folder. `target-pool-refresh` still lists `/Users/mac/Downloads/replo-rebuilds`, a folder that no longer exists. After the move, all four need their folder repointed to `~/koolestpro-cowork-v2`. Static ad, tips, CRO fix, BrowserAct, ad library, template build, distribution health check and replo cache check are not in the cloud list. The desktop copies are backed up to `scheduled-tasks/desktop/` by the setup script.

**Follow-up, same day: scheduled tasks rebuilt.** The setup script moved the folder to `/Users/mac/koolestpro-cowork-v2` and backed up 17 desktop task definitions to `scheduled-tasks/desktop/`. All 12 active koolestpro tasks are now cloud scheduled tasks that require the Mac and point at the new folder. The 4 old ones (still aimed at `~/Downloads`) were deleted. Each task's prompt is short. It checks that the folder is reachable, reports `FAILED: project folder not reachable` instead of ending silently, and then follows `scheduled-tasks/desktop/<task>/SKILL.md`. To change a task's behaviour, edit that file in the repo. Not recreated because they were already disabled: trend-radar, tiktok, shopify-cro-job-alerts, and both Abuzaid tasks.

### 2026-09-27 — Carousels in Make, 5MB guard, Tips V4, Template Showcase IG carousel

**Make (scenario 6565331).** Added a carousel route on X (220-225: up to 4 images in one tweet) and on Instagram (310-317: native carousel, 2-10 images). Rows whose `asset_urls` contain `; ` take it; single-image and video routes now exclude them so nothing double-posts. Instagram captions now go through a Parse JSON step, because column 14 is JSON-quoted and was being sent with its quotes and literal `\n`. Instagram stays paused (`Instagrams` filter untouched). The live blueprint was diffed against the intended one after the update: identical, and only modules 203/204/207/301/304/401 changed among the existing ones.

**Under 5MB.** Every image URL Make fetches or sends is rewritten to a Cloudinary delivery transform (`c_limit,w_2160,h_2700,q_auto:good,f_jpg`), tested 717 KB → 227 KB. `feed_media.py` also shrinks any local image over 4.5MB before upload, and no longer trims Instagram carousels to the cover image. Details in `.ai-workflow/tools/DISTRIBUTION.md`.

**Tips V4.** The typography-hierarchy post was filed as a reference (`references-for-posts/tips-best-2026-09-18-typography-hierarchy/`) and rebuilt as the V4 prototype (`references-for-posts/tips-v4-prototype-2026-09-27/`): 1080×1350, headline ≥88px, body ≥40px sans, one dominant visual per slide, 2025 footer and pill system, type-led cover. Spec `docs/system/tips-v4-format.md`; the Tips weekly task, CLAUDE.md router and quality ratchet point at it.

**Template Showcase Instagram = carousel.** Spec `docs/system/template-showcase-ig-carousel.md`, 6 slides modelled on `references-for-posts/shopify rebuilds/`. The template showcase weekly task now builds it every run. No builder script yet; the first run builds it and should save its script for reuse.

### 2026-09-27: Cold email outreach, step 1 (Gmail sender)

**Decisions (Ridwan).** Build his own Artisan-style outreach instead of paying for it. Google Sheets is the data store (not Supabase); KoolestFlow will read it / import via CSV. Send from secondary Gmails, never the main one, starting with koolestpro@gmail.com, low volume split across accounts. He approves the first batch before anything goes live. No Make for outreach: the free plan can't hold it, so sending runs on Google Apps Script at $0. Cold email never goes out from koolestpro.com; info@ stays inbound only. A lookalike domain + Workspace inboxes come after the first paying client.

**Built.** `outreach/gmail-sender/` (`Code.gs`, `appsscript.json`, `SETUP.md`). The script lives in the outreach Sheet and creates 7 tabs: Settings, Leads, Profiles, Sequence, Messages, Memory, Drafts. It sends approved first emails plus due follow-ups in one run, keeps steps 2-5 in the same Gmail thread (Gmail advanced service + In-Reply-To), warms up at 5/day +5/week to a 20/day cap with max 2 per hourly run, stops a sequence on reply, logs every message both ways (including replies Ridwan sends by hand from Gmail), queues a Drafts row and emails an alert, sends drafts marked Approved in-thread, and marks bounces. TEST_MODE (on by default) redirects everything to ALERT_EMAIL. Verified with a simulated Sheet/Gmail run end to end; not yet run in a real Google account.

**Next.** AI reply drafts + per-lead Memory summaries; email finding + MyEmailVerifier; sequence writing from real proof (no invented numbers); lead finders writing to the Sheet; KoolestFlow as the dashboard over the Sheet.

### 2026-09-30: Outreach handoff for Claude Code

Added `outreach/README.md` (goal, Ridwan's decisions, architecture with per-step status, next steps, don'ts) so any agent working from the GitHub repo has the full context of the 2026-09-27 planning chats. CLAUDE.md: new Task Router row for cold email, and rule 3 now records the Google Sheet exception for cold email.
