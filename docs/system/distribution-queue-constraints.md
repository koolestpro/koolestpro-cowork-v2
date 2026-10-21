## 📅 LINKEDIN + DISTRIBUTION QUEUE CONSTRAINTS

* **LinkedIn: max 1 post/day, hard cap.** Never more than one row on the same `scheduled_date` on LinkedIn, even at different times. Check every other LinkedIn row on a date before scheduling. Twitter is exempt from a daily cap.
* **No two rows on the same platform** may share the same exact `(scheduled_date, scheduled_time_local)`. A LinkedIn and a Twitter post at the same time are fine. Use standard slots `09:00/13:00/18:00/23:00`; if a day is full, space additional times ≥60-90 min apart. Before calling the reschedule webhook, pull the live sheet and confirm the target slot is free (the webhook blind-overwrites and does not check).
* **A 200 from the reschedule webhook is not proof it landed** — re-read the affected rows after calling it.
* `koolestpro-populate_sheet.py` handles fresh batches correctly via `find_open_week()`; known caveat — `taken_keys` is seeded only from local `queue.json`, not a live sheet read, so it can drift.
* **Never auto-publish.** Every generator stops at status `Created`; `Published` is only set by the real posting step.


## Template Showcase spacing (2026-10-10, Ridwan)

Same rule as CRO Fix and Static Ad: never post a page's assets back to back. Same brand at least 5 days apart on any platform (7 preferred), enforced by `.ai-workflow/tools/space_queue.py`. A page's lead assets (cover video, IG carousel, cover image, preview) are scheduled before its laptop video, mobile video, full page and mobile strip, and a different brand's cover always wins over the same brand's secondary cut or another page of the same brand. Run `space_queue.py --include-ig` (dry run first, 0 violations) after every assembly.

Volume (same date): 2 showcase pages a week, different brands, 4 lead posts each (LinkedIn cover video, IG carousel, X preview, X mobile strip); laptop video, mobile video and full page queue as secondary filler.

## Variants board goes first (2026-10-11)

A CRO Fix variants-board X row (assets contain `variants-board`) always posts before that audit's carousel rows: the day before its LinkedIn hero, or opening the hero's day with the hero pushed a day. `space_queue.py` rule 3c enforces it; the board and its hero within one day count as one bundle for the brand cooldown. Distribution assembly never posts it after the carousel.
