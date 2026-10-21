# Video + content-calendar version (V4 prep). Portable handoff doc.

Written 2026-10-19 so any AI tool (Claude, Codex, Cursor, Gemini) can continue. Read this first, then `references-for-posts/video-inspo/README.md`.

## Goals (Ridwan's words, condensed)
1. Build a library of saved TikTok and Instagram videos offline in the project folder, analyze them, rank easy to hard, automate the easy ones in many variations.
2. Make Reels and TikToks. TikTok drafts via API and Instagram posting are already wired. LinkedIn video is optional and low priority (few people in the niche do it).
3. Stop random posting. Run a content plan and calendar that builds an audience, not only proof posts.
4. Use the "90 content ideas" reference for post types.

## What already exists (do not rebuild)
- TikTok pipeline: `outputs/tiktok_mockup/` (Playwright scroll capture, phone bezel, caption overlays, Groq/OpenAI TTS). 5 videos across 5 content types.
- TikTok inbox drafts are live with sandbox credentials (2026-09-07). Public posting was rejected in review (2026-09-19), so drafts to inbox, then Ridwan publishes in the app.
- Instagram: Make scenario routes carousels and videos only, max 1 post per day at 17:00. Single images stay off. Token expires 2026-11-07.
- Audio/video tooling: `docs/video-audio-stack-pointer.md` (TTS, Freesound SFX and music, ffmpeg).
- Prior vision: `docs/audience-growth-v3-prep.md`. This doc supersedes its video section.

## Hard rules for this work
- Instagram: never automate, scrape or download from instagram.com. Screen recordings made by Ridwan only.
- No em dashes in copy, no hashtags on X, never invent client results, concept brands stay labelled as concepts.
- Rebuilds of real businesses stay private.
- Videos must span content TYPES (Tip, CRO Fix, Static Ad, Template Showcase, expertise), not only edit styles.

## Step 1: get the saved videos offline
- TikTok: run `scripts/download_tiktok_inspo.sh` in Mac Terminal (yt-dlp, Chrome login). If the collection fails, paste `scripts/tiktok_collect_links.js` into the Chrome console on the collection page, save the copied links as `tiktok/links.txt`, and run the script again. `fb_dl` is Facebook-only and will not work for TikTok. Status 2026-10-19: collection made public, but cloud/VM attempts still failed (TikTok loads the list by script; Chrome remote control kept dropping).
- Instagram: record your screen while playing each saved reel (Mac: Shift+Cmd+5), save into `references-for-posts/video-inspo/instagram-screenrecs/`. Optional one-line `why.md` per file.
- Then fill `catalog.md`.

## Step 2: reel format library, easy to hard
Tiers are for Ridwan's niche (Shopify CRO, design, builds). Each is a recipe the pipeline can template and vary by swapping store, hook, copy and voice.

| Tier | Format | Why this tier | Automation |
|---|---|---|---|
| T1 | Store scroll teardown: scroll a real store, red-pen callouts, voiceover naming 3 fixes | Uses existing Playwright scroll capture + overlays + TTS | Fully automatic from `targets_pool.json` |
| T1 | Before/after flip: old page vs rebuild, wipe transition | Assets already produced by CRO Fix | Automatic from CRO Fix outputs |
| T1 | Text-on-screen tip: big type, 3 to 5 beats, music bed | Tips carousel slides become video beats | Automatic from Tips slides, ffmpeg slideshow with motion |
| T1 | Template showcase: phone bezel scroll of a store template | Pipeline exists | Automatic |
| T2 | Listicle reel: "5 things killing your product page", each beat a cropped screenshot | Needs per-beat image sourcing | Semi-auto, image pack |
| T2 | Myth vs reality, do/don't splits | Simple two-panel template | Automatic with copy input |
| T2 | Build-in-public time lapse of a page being built (Lovable/Figma capture speed-up) | Needs screen recordings of real builds | Semi-auto |
| T3 | Talking head with screen overlay (Ridwan on camera) | Needs face and voice; best for audience growth | Ridwan records, pipeline adds captions, b-roll, cuts |
| T3 | POV freelancer from Ibadan, day-in-the-life | Needs filming | Manual shoot, auto captions |
| T3 | Trend audio / meme formats | Fast-moving, rights issues | Manual, via trend radar |
| T4 | Heavy motion graphics, lip-sync avatar | Costly, off-brand risk | Skip |

**Decision (Ridwan, 2026-10-19): fully automated, no voice.** His own voice could not be reproduced by an AI agent, and the saved references use little or no voice. So every format is music + text-on-screen + captions. Face is allowed, but not recorded: use his existing brand photos or a lightly animated AI version of his face (minimal movement so it does not read as AI), as an intro card, avatar badge or reaction cutaway. Real recording of himself is a future option with no date.
So the T3 talking-head row is replaced by **T2 "face card" reel**: still/lightly animated face + big text hook + b-roll. Start with three automatic formats: store teardown, before/after, text-on-screen tip, plus the face card as a recurring element.
His TikTok collection shows the TYPE of post he wants; it does not cover the whole plan, so the calendar and the 90-ideas mapping still need to be filled by us.

## Step 3: post types, from the "90 content ideas" reference
Source post (kept only as a type reference, do not copy its text): 30 reel ideas, 30 story ideas, 30 single posts, 30 carousels. The groups, in our own words, mapped to Koolestpro:

- Reels (video): follow a trend; behind the scenes of a build; before/after; introduce yourself; walk through a tool; unbox/tour a product or template; answer a client FAQ; bust a myth; "a week in my life"; small tips; reality vs expectation; tutorial; time-lapse of a process; testimonial clip (real only); repurpose old content; tools I use; books I read; industry secrets; common mistakes; POV trend; lesson learned recently; success story (real only); sneak peek of a coming template; collab with another creator; fun challenge.
- Stories: question box, polls, quizzes, quick wins of the week, screenshot of a nice client message (real only), sneak peek, resource giveaway, misconception, truth-or-myth.
- Single posts: story with a lesson, hard truth, milestone, quote, before/after, tool list, bio and hook how-tos, content-idea sources, hashtag strategy (LinkedIn/IG only).
- Carousels: step-by-step tutorial, swipe before/after, top tips, mini case study, myths with corrections, do and don't, things I wish I knew, checklist, industry updates, roadmap to a goal, questions to ask yourself.

Filter for us: keep the ones tied to Shopify, CRO, design, and real work. Drop generic lifestyle prompts (workout, morning routine) unless reframed for a freelancer.

## Step 4: content calendar (draft, per week)
Proof content keeps its slots; audience content fills new ones. Instagram max 1 per day; LinkedIn 1 per day.

| Day | Slot | Format | Platforms |
|---|---|---|---|
| Mon | Resource/save-bait carousel | "30 PDP headline formulas" style | LinkedIn, IG |
| Tue | Proof | CRO Fix carousel | LinkedIn, IG, X |
| Wed | Reel T1 | Store scroll teardown | TikTok draft, IG Reel |
| Thu | Opinion / hot take | Short text or talking-head reel | X, LinkedIn, TikTok |
| Fri | Tip | Tips carousel + text-on-screen reel | LinkedIn, IG, TikTok |
| Sat | Story/behind the scenes | Build time-lapse or POV | TikTok, IG Reel |
| Sun | Light | Poll, Q&A story, repost best | Stories, X |

Monthly arcs: 4 weeks, each with a theme (e.g. product pages, homepages, mobile, checkout), so the page tells a story instead of random posts. Hooks bank and weekly review of saves, shares, follows (not likes).

## Step 5: build order
1. Download + catalog (above).
2. Write one-page recipes for the T1 formats; extend `outputs/tiktok_mockup/` into a variation generator (hook x store x voice x music).
3. Wire TikTok draft push + Instagram Reel queue to the calendar in the Google Sheet.
4. Add the resource-post generator and hooks bank.
5. Build log update in `docs/koolestpro-content-operating-plan.md` after each change (standing rule).

## Research notes still to do
- Current Reels/TikTok length and hook benchmarks (search before citing numbers).
- TikTok trend audio licensing for business accounts.
- Whether the TikTok Content Posting API production review is worth retrying.
