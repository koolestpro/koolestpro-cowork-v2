# Make.com Publishing Scenario — Koolestpro Distribution (Step 7)

Status: **spec ready, not yet created live.** Blocked on platform tokens (see below).
Modeled 1:1 on Ridwan's already-working **"Abu Zayd Afternoon Post"** scenario
(id 6225494), which uses the exact pattern V2 needs.

## Why it isn't live yet (read this first)

Two hard facts found on 2026-07-14 by inspecting the Make account:

1. **No platform tokens.** Abu Zayd posts to Facebook via a raw `http:MakeRequest`
   to `graph.facebook.com/...` with an access token embedded in the module — NOT a
   native Make OAuth connection (that's why LinkedIn/IG/X don't appear in the
   connections list). Koolestpro distribution needs the equivalent tokens for
   **LinkedIn**, **Instagram** (Graph API via a linked Facebook Page/IG Business
   account), and **Twitter/X** (API v2). None exist yet.
2. **Free plan, 1 scenario slot left** (2 max, Abu Zayd uses one). 15-min minimum
   polling interval, 1000 ops/month.

Creating the scenario now would occupy the last free slot with modules that error
on every run. So it's specced here and created the moment at least one platform
token exists. **The scenario also can't run until Ridwan connects the platforms** —
which he confirmed still needs doing.

## Architecture (clone of Abu Zayd, retargeted)

```
[google-sheets: filterRows]           ← trigger, every 15 min
  spreadsheet: Koolestpro Distribution Queue (1I5SrLnwAfVV5260Y_nAytio49gh-NKmJeJdFXH3nqzg)
  sheet: Sheet1
  filter: status = "Ready"
      AND scheduled_date = today (formatDate(now;"YYYY-MM-DD"))
      AND scheduled_time_et hour <= current ET hour
        │
        ▼
[builtin: BasicRouter]  ← one route per platform, gated by the row's `platform`
  ├── Route LinkedIn  (filter: platform = "LinkedIn")
  │      [http: MakeRequest]  POST LinkedIn UGC/Posts API  (TODO token)
  │      → on success: [google-sheets: updateRow] status="Posted", posted_at=now
  │      → on error:   error handler = "retry 3x, 5-min backoff" then
  │                    [google-sheets: updateRow] status="Failed: {{error.message}}"
  ├── Route Instagram (filter: platform = "Instagram")
  │      [http: MakeRequest]  POST graph.facebook.com IG media + media_publish (TODO token)
  │      → updateRow Posted / Failed  (same handler)
  └── Route Twitter   (filter: platform = "Twitter")
         [http: MakeRequest]  POST api.twitter.com/2/tweets (+ media upload) (TODO token)
         → updateRow Posted / Failed  (same handler)
```

Column indices (0-based, matching the queue CSV header order):
`0 post_id · 1 pipeline_item_id · 2 stream · 3 platform · 4 scheduled_date ·
5 scheduled_time_et · 6 asset_paths · 7 caption · 8 caption_source_tab ·
9 status · 10 qa_status · 11 posted_at · 12 content_system_folder`

So the trigger filter uses `{{1.\`9\`}}` (status) = "Ready", `{{1.\`4\`}}`
(scheduled_date), `{{1.\`5\`}}` (time); the router routes on `{{1.\`3\`}}` (platform);
the caption is `{{1.\`7\`}}`; the image/video is `{{1.\`6\`}}`; updateRow writes
`9` (status) and `11` (posted_at).

## Error handling (Ridwan's choice: retry-then-flag)

Each HTTP post module gets a Make **error handler** route:
- Directive: **Retry** — 3 attempts, 5-minute interval (Free-plan-safe).
- If still failing: **Resume** into a `google-sheets:updateRow` that sets
  `status = "Failed: {{error.message}}"` and leaves `posted_at` empty.
- Never `Ignore`, never `Commit` silently. A failed post is always visible in the
  Sheet as `Failed:` and never re-counts as posted.

## Asset handling note

`asset_paths` are LOCAL project paths (`outputs/...`), not public URLs. The
platform APIs need a publicly-reachable image/video URL or a binary upload.
Before this scenario can post images, one of:
- upload each asset to Cloudinary (already used in this project) and put the
  Cloudinary URL in `asset_paths` at populate time, **or**
- have Make fetch the binary from a synced Drive/Cloudinary copy and multipart-upload.
Decide this when wiring the first platform. (Text-only would post fine today, but
the plan forbids text-only posts, so an asset URL step is required.)

## To create it live (checklist)

1. Get at least one platform API token (LinkedIn is usually the simplest to start).
2. Resolve the asset-URL question above (Cloudinary is the path of least resistance).
3. Then, in a Make-MCP session: `scenarios_create` on team 1960838 with the blueprint
   built from this spec (clone Abu Zayd's module JSON, swap the spreadsheetId to the
   Koolestpro queue sheet, swap Facebook HTTP modules for the LinkedIn/IG/X endpoints,
   set scheduling interval 900s), created **paused**. Test with one `Ready` row before
   activating.

Reference: Abu Zayd blueprint = scenario 6225494 (its `google-sheets:filterRows`,
`builtin:BasicRouter`, `http:MakeRequest`, and `google-sheets:updateRow` modules are
the copy source — same shapes, different sheet + endpoints).
