# Instagram + TikTok auto-posting — DONE (2026-09-08)

Both streams are live. This file is kept as the run record; the durable rules now live in
`CLAUDE.md` under "TIKTOK DRAFTS + INSTAGRAM PUBLISHING". Nothing here is outstanding.

---

## TikTok — drafting, live

No production app review is needed; that open question from 2026-09-04 is closed. Verified
by refreshing the sandbox token and running a real inbox init.

| Piece | State |
|---|---|
| `tiktok_push_draft.py` | working, self-refreshing token, `--check` verifies scope |
| `build_tiktok_video.py` | working, verified end to end on halos-pdp-01 (26.4s, 1080x1920) |
| `koolestpro-tiktok-weekly` | live, Thursdays ~09:11 |
| `usedForTikTok` rotation flag | on all 12 manifest entries |
| `assets/fonts/` (Syne, DM Mono) | added |
| `bootstrap_env.sh` | rewritten: resumable downloads, browsers on /tmp |

Worth doing once: hit "Run now" on the task so tool approvals get stored, otherwise an
unattended run can stall on a permission prompt.

---

## Instagram — publishing, live

The Page↔IG blocker was obsolete rather than unresolved. Instagram Login publishes with no
Facebook Page. Do not reopen Business Suite debugging.

| Field | Value |
|---|---|
| Meta app | Koolestpro Publishing, `1094745286417525` |
| Instagram app ID | `930775432950893` |
| Account | `@koolestpro`, BUSINESS, user id `28407989805529147` |
| Token | long-lived, in `.env` and the Make datastore, expires **2026-11-07** |
| Permissions | `instagram_business_basic` + `instagram_business_content_publish` |
| Make modules changed | 301, 302, 304, 306 (URL host + token field), 201 (pass-through) |

Proven this session: OAuth exchange, `me` (returns the real account), and a media container
built from a queued Cloudinary image reaching `FINISHED`. The final `media_publish` call is
the one step not yet exercised, since Ridwan chose to let the schedule do it rather than
force a live post. **First scheduled Instagram row is the real test** — if it fails, check
the Make execution history for that run rather than assuming the wiring is wrong.

### Two gotchas worth remembering

**Module 201 will silently break this if a field is ever added and not mirrored there.** It
writes the datastore after every X token refresh and only writes the fields it lists.
`instagram_page_access_token` was missing and would have been blanked within hours.

**Token refresh is not automated yet.** The token lapses 2026-11-07. `instagram_client.py
refresh` extends it and is safe to run on any cadence, since Meta declining a refresh on a
token under 24h old is reported rather than treated as failure. The intended home is
`koolestpro-distribution-health-check` (every 2 days). **This is the one genuinely open
item.** After refreshing, the new token must also be written back into the Make datastore,
or Make keeps using the old one.

---

## Queue state at handover

52 Instagram rows: 11 `Ready`, 41 `Draft`. The Ready ones become eligible on their existing
scheduled slots. The Drafts still need Ridwan's normal approval pass.
