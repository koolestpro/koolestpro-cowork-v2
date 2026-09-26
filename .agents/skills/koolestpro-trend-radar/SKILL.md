---
name: "koolestpro-trend-radar"
description: "Weekly, config-driven trend and content-format discovery across X, Reddit, and Instagram. Layer 1 picks a trending topic to feed a topic-driven content stream (e.g. a \"Tips\" carousel); Layer 2 (\"Format Radar\") flags competitor/adjacent-creator content formats (any medium) getting real engagement that the user hasn't tried yet. Portable — each project supplies its own trend-radar-config.json. Use when a recurring content pipeline should stay trend-aware instead of cycling the same topics, or when the user wants a nudge toward new content formats worth trying."
---

---
name: koolestpro-trend-radar
description: Weekly, config-driven trend and content-format discovery across X, Reddit, and Instagram. Layer 1 picks a trending topic to feed a topic-driven content stream (e.g. a "Tips" carousel); Layer 2 ("Format Radar") flags competitor/adjacent-creator content formats (any medium — image, carousel, infographic, video) that are getting real engagement and that the user hasn't tried yet. Portable across projects — each project supplies its own trend-radar-config.json with its own niche keywords/pillars/output paths. Use when a project wants its recurring content generation to stay trend-aware instead of cycling the same topics, or wants an opportunistic nudge toward new content formats worth trying.
---

# Trend & Format Radar

This skill is project-agnostic. It never hardcodes a niche, a brand voice, or a content pipeline's file layout — all of that lives in the CURRENT project's own `trend-radar-config.json` (project root) and, for narrative context, a "Trend & Format Radar" section in that project's CLAUDE.md. Always read that config file first. If a project doesn't have one yet, that's a sign this skill hasn't been set up there — ask the user for their niche keywords/pillars and the file paths their content system uses, then write a `trend-radar-config.json` following the schema below before doing anything else.

## What this skill produces

**Layer 1 — Topic selection.** A ranked shortlist of trending topics/angles in the project's niche, written to the file named in `config.outputPaths.tipsTopicLog`. Whichever scheduled task generates the project's topic-driven content stream (named in `config.layer1.consumingScheduledTask`) reads the top-ranked entry from the latest week's log entry as its topic pick — this skill does not itself generate the content, only the topic.

**Layer 2 — Format Radar.** An opportunistic flag, written into the project's main content-review file (named in `config.outputPaths.contentPipelineHtml`), whenever a competitor or adjacent creator in the niche is getting real engagement from a content format/style the user isn't currently doing — in any medium. This only fires when something genuinely clears the bar (new-to-the-user format + real engagement signal + niche-relevant) — most weeks should produce nothing here, and that's correct, not a failure. Never manufacture a finding to fill a quota.

Both layers still leave the human in charge: Layer 1's picked topic still goes through whatever review gate the consuming content stream already has before publishing; Layer 2 never auto-builds anything, it's purely a nudge the user acts on (or doesn't) at their own discretion.

## `trend-radar-config.json` schema

```json
{
  "pillars": [{ "name": "...", "keywords": ["...", "..."] }],
  "nicheQueryTerms": ["...", "..."],
  "brandSafetyAvoidTerms": ["..."],
  "sources": {
    "x": { "enabled": true, "maxReadsPerWeek": 50, "monthlyBudgetUSD": 5.0 },
    "reddit": { "enabled": false, "maxReadsPerWeek": 100, "monthlyBudgetUSD": 1.0, "provider": null },
    "instagram": { "enabled": true, "method": "claude-in-chrome" }
  },
  "outputPaths": {
    "tipsTopicLog": "trend-radar-log.json",
    "contentPipelineHtml": "content_pipeline.html",
    "spendLedger": "trend-radar-spend-ledger.json"
  },
  "layer1": { "feedsPostType": "...", "consumingScheduledTask": "...", "autoPickTopRanked": true },
  "layer2": { "name": "Format Radar", "onlySurfaceWhenBarCleared": true, "noManufacturedQuota": true }
}
```

## Sources and how each one actually works

**X (official API, read-only).** Recent search (last 7 days) via `GET https://api.x.com/2/tweets/search/recent`, app-only Bearer token auth — no browser OAuth login needed, which matters because this typically runs inside an unattended scheduled task. The Bearer token is a DIFFERENT credential from any OAuth2 client id/secret the project might already use for posting to X — get it from developer.x.com → the project's app → "Keys and tokens" tab → "Bearer Token" specifically. Store as `X_BEARER_TOKEN` in the project's `.env`. Cost is pay-per-use (~$0.005/post read as of 2026); every call must reserve its estimated cost against the shared spend ledger BEFORE hitting the network, and skip the pull (not crash) if that would exceed `sources.x.monthlyBudgetUSD` for the month.

**Reddit (third-party API, NOT Reddit's own official API).** Reddit's own commercial API has a very high price floor unsuitable for this use case — use a cheap third-party reseller instead (the user picks the provider; this is their decision, not the skill's). Store as `REDDIT_API_BASE_URL` / `REDDIT_API_TOKEN` in `.env`. If either is unset, treat Reddit as contributing nothing this week (a known, expected gap while the user hasn't signed up yet) — never treat a missing Reddit credential as a fatal error for the whole run.

**Instagram (Claude-in-Chrome browsing only — no viable API).** Instagram's own Graph API only supports fetching posts for a hashtag already known (not discovery), is rate-limited to a small number of hashtag lookups per week, and typically requires a Business/Creator account link that may itself be blocked for unrelated reasons in the project. There is no shortcut here — if browsing is used, treat it as the weakest-signal, supplementary source, and if browser automation isn't reliably available inside an unattended scheduled task (a real, common limitation), degrade gracefully: skip Instagram that week and rely on whichever other sources are working, flagging this plainly in the run's summary rather than silently doing nothing.

## Weekly procedure

1. Read `trend-radar-config.json`. Confirm the current ISO week (`YYYY-Www`).
2. For each enabled source, pull candidate posts/content filtered to `nicheQueryTerms` and the pillars' keywords, respecting each source's `maxReadsPerWeek` and budget cap. A source that's disabled, unconfigured, or over budget is skipped — not fatal — and gets listed in that week's `sourcesSkipped`.
3. Run every candidate through a relevance/brand-safety filter (niche keyword match + a blocklist of off-brand/politically-charged terms from `brandSafetyAvoidTerms`) before it's eligible for either layer.
4. Rank the surviving candidates by an engagement score appropriate to the source (e.g. likes + replies weighted higher, since a reply/comment is a stronger signal than a like).
5. **Layer 1:** turn the top few candidates into concrete topic/angle proposals for the project's content stream, write them (plus which one is auto-picked, if `layer1.autoPickTopRanked` is true) to `outputPaths.tipsTopicLog`, keyed by the current ISO week.
6. **Layer 2:** separately evaluate whether any candidate represents a genuinely new-to-the-user content FORMAT (not just topic) with real engagement behind it. If yes, write it as a new finding into `outputPaths.contentPipelineHtml`'s findings block (additive only — dedupe by id, never touch an existing finding's review status). If no candidate clears this bar, write nothing — do not force an entry.
7. Finish with a short, honest summary: which sources ran vs. were skipped and why, what topic got picked for Layer 1, whether anything was flagged for Layer 2, and current month-to-date spend per source against its cap.

## Reusable scripts

A reference implementation of the above (X search, the Reddit stub, the relevance filter, the budget ledger, and the two file-writers for the topic log and the Format Radar block) should live at `.ai-workflow/skills/koolestpro-trend-radar/scripts/` inside whichever project uses this skill. If a project doesn't have these yet, write them there, following the same responsibilities described in "Weekly procedure" above — don't invent a different architecture per project, the scripts are meant to be copied and reconfigured (via `trend-radar-config.json`), not rewritten from scratch each time.

## Hard rules

- Never fabricate engagement numbers, sources, or example links. Every Format Radar finding and every Layer 1 topic candidate must trace back to something actually pulled this run.
- Never let a single source's failure (missing credential, rate limit, budget cap hit) block the other sources or the run as a whole.
- Never auto-build anything from a Layer 2 finding. It is a notification, not a task queue.
- Never spend past a source's configured monthly cap. Reserve-then-spend against the ledger before every paid call, not after.
- If nothing in a given week clears the bar for either layer, say so plainly — silence/an empty result is a valid, honest outcome, not something to paper over with a manufactured finding.

