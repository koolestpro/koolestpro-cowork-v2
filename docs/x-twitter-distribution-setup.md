# X/Twitter Distribution — Setup Guide & Scenario Spec

Added 2026-07-21. Companion to `koolestpro-v2-distribution-plan.md` (Step 7's "open question" — this doc answers it for the X/Twitter leg specifically). Written before any credentials existed, so Part 1 must be done by Ridwan before Part 2 can actually be built.

---

## Part 1 — Get X API v2 Access (Ridwan does this manually)

**Important cost change (confirmed via web search, 2026-07-21):** as of February 2026, X retired its free API tier. All new developers are on **pay-per-use**: $0.015 per post created (or $0.20 if the post contains a link), plus $0.005 per post read (capped at 2M reads/month). No subscription, no minimum spend — you buy credits upfront in the Developer Console and they draw down per call. Legacy $200/mo Basic and $5,000/mo Pro tiers still exist only for accounts that had them before the change; new accounts can't sign up for those anymore.

At your planned volume (3 image posts/day, ~21/week, no links per the distribution plan's rule) that's roughly 21 × 4.33 × $0.015 ≈ **$1.36/month** — cheap, but worth knowing it's not actually free like the old plan.

**Steps:**
1. Go to `developer.x.com` and apply for a developer account under the account you want posting (probably @koolestpro).
2. Create a new Project + App inside the Developer Portal.
3. Set the app's permissions to **Read and Write** (default is often read-only — this is the #1 thing people miss and then wonder why posting fails with a 403).
4. Under "Keys and tokens," generate:
   - API Key + API Key Secret (needed regardless of auth style)
   - Access Token + Access Token Secret, generated **with Read+Write permissions already set** (regenerate these if you set permissions after they were first created — old tokens don't retroactively gain write access)
5. Go to the Developer Console's billing/credits section and load starting credits (even a small amount, e.g. $10, covers months at this volume).
6. Send me the four credential values (API Key, API Key Secret, Access Token, Access Token Secret) once you have them — I'll store them the same way your LinkedIn token is stored (Make.com datastore, not hardcoded in a scenario), so nothing sensitive sits in this chat's memory.

Note on auth style: X API v2 media/tweet endpoints support both OAuth 1.0a (the four-value method above) and OAuth 2.0 user context. OAuth 1.0a is simpler to wire into raw HTTP modules in Make (matches how your LinkedIn scenario already does raw bearer-token HTTP calls rather than Make's native connector), so that's the default plan below unless you'd rather use Make's native X/Twitter app connector instead (trade-off: native connector handles OAuth signing for you, but is a second thing to keep authorized/refreshed separately from how LinkedIn's token is managed today).

---

## Part 2 — Folded Scenario Spec (built once Part 1 is done)

### Why folded, not standalone
Your Make.com org is on the Free plan: `license.scenarios: 2`, and both slots are already used (`Abu Zayd Afternoon Post`, `Koolestpro LinkedIn Distribution`). Per your call, X gets added as new branches inside the existing LinkedIn scenario rather than a third scenario — no Make upgrade needed.

**Rename:** `Koolestpro LinkedIn Distribution` → `Koolestpro Social Distribution` (reflects it now handles both platforms).

### What stays the same
- Same trigger: `google-sheets:filterRows` on the same sheet (`Koolestpro Distribution Queue`, tab `Untitled`, spreadsheet `1I5SrLnwAfVV5260Y_nAytio49gh-NKmJeJdFXH3nqzg`). No new sheet needed — the `platform` column (col D) already exists in the schema and the V2 distribution plan already assumes rows with `platform = "X"`.
- Same datastore pattern for tokens: `koolestpro-config` datastore gets a second field, e.g. `x_api_key` / `x_api_secret` / `x_access_token` / `x_access_secret`, alongside the existing `linkedin_token` — fetched in the same `datastore:GetRecord` module (key `"main"`) so it's one lookup, not two.
- Same sheet-update-on-success pattern (`status` → `Posted`, `posted_at` → now).

### What changes — new top-level split before the existing router
Add a **platform router** ahead of the current 3-branch asset-type router:

```
[1] google-sheets:filterRows (trigger — same as today, but filter condition changes
    from platform == "LinkedIn" to platform == "LinkedIn" OR platform == "X",
    since one polling trigger can feed both platform branches)
       ↓
[2] datastore:GetRecord (same, now returns both platforms' credentials)
       ↓
[3] builtin:BasicRouter — PLATFORM split
       │
       ├── Route: platform == "LinkedIn"  → existing 3 branches, unchanged
       │
       └── Route: platform == "X"  → NEW asset-type router (below)
```

### New X asset-type router (fixes the gap the LinkedIn scenario had)
The LinkedIn scenario never had a plain-image branch — it only handled text/.mp4/.pdf. Since Static Ad, CRO Fix, and Tips carousel all output PNGs, the X branch **must** include an image path from day one:

```
Route: asset_urls == ""              → text-only tweet (distribution plan says this shouldn't
                                         happen for X — "no text-only posts" — so this branch
                                         mainly exists as a safety net / QA catch, not expected traffic)

Route: asset_urls ends with .png/.jpg → IMAGE branch (this is the one that matters most for you)
Route: asset_urls contains .mp4       → VIDEO branch
```

Each non-text branch follows X's chunked media upload — genuinely different mechanics from LinkedIn's pre-signed-URL pattern, not a drop-in swap:

1. **INIT** — `POST https://upload.twitter.com/1.1/media/upload.json` with `command=INIT`, `media_type` (e.g. `image/png`), `total_bytes`, and `media_category` (`tweet_image` or `tweet_video`). Returns a `media_id`.
2. **Download source** — `http:ActionGetFile` on `{{asset_urls}}`, same as the LinkedIn scenario already does.
3. **APPEND** — `POST .../media/upload.json` with `command=APPEND`, `media_id`, `segment_index`, binary chunk. For your image sizes this is likely a single chunk; video may need multiple.
4. **FINALIZE** — `POST .../media/upload.json` with `command=FINALIZE`, `media_id`.
5. **Create the post** — `POST https://api.x.com/2/tweets`, body `{"text": <caption>, "media": {"media_ids": ["<media_id>"]}}`, `Authorization` header signed with the OAuth 1.0a credentials (or Bearer if you go OAuth2 route).

Unlike LinkedIn (3 separate post-creation payload shapes for text/video/document), X's tweet-creation call is the **same endpoint and shape regardless of media type** — only the upstream media upload differs. So the image and video branches can converge onto one shared "create tweet" module downstream, instead of duplicating it three times like the LinkedIn scenario does.

### Caption column reuse
Same `caption_json` column (N) the LinkedIn scenario reads for pre-quoted JSON text — reuse directly: `{"text":{{1.\`13\`}}, ...}`. No new column needed, but double check X's 280-character limit against what your caption generators actually produce for the X-specific tabs (`#tab-x-thread`, `#tab-x-singles`, `.x-post` divs) — these were already written with X's limit in mind per the harvest step in the V2 plan, so this should already be safe, just worth a spot check on the first live row.

### Not building yet
Threads (multi-tweet, for the Wednesday CRO Fix thread slot in the distribution plan) aren't in this spec — that's a follow-up (each thread tweet needs `reply.in_reply_to_tweet_id` chained to the previous tweet's returned ID). Flag as a fast-follow once single-image/video posting is confirmed working.

---

## Next Steps (in order)

1. Ridwan completes Part 1 (X Developer Portal signup, app, Read+Write tokens, starter credits).
2. Ridwan sends the 4 credential values.
3. Claude stores them in the `koolestpro-config` datastore (same pattern as `linkedin_token`).
4. Claude renames the scenario, adds the platform router + X asset-type router + chunked-upload modules per the spec above.
5. Test with one manual `platform = "X"` row set to `Ready` in the sheet before trusting the live poll.
