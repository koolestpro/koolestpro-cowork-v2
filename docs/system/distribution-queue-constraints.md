## 📅 LINKEDIN + DISTRIBUTION QUEUE CONSTRAINTS

* **LinkedIn: max 1 post/day, hard cap.** Never more than one row on the same `scheduled_date` on LinkedIn, even at different times. Check every other LinkedIn row on a date before scheduling. Twitter is exempt from a daily cap.
* **No two rows on the same platform** may share the same exact `(scheduled_date, scheduled_time_local)`. A LinkedIn and a Twitter post at the same time are fine. Use standard slots `09:00/13:00/18:00/23:00`; if a day is full, space additional times ≥60-90 min apart. Before calling the reschedule webhook, pull the live sheet and confirm the target slot is free (the webhook blind-overwrites and does not check).
* **A 200 from the reschedule webhook is not proof it landed** — re-read the affected rows after calling it.
* `koolestpro-populate_sheet.py` handles fresh batches correctly via `find_open_week()`; known caveat — `taken_keys` is seeded only from local `queue.json`, not a live sheet read, so it can drift.
* **Never auto-publish.** Every generator stops at status `Created`; `Published` is only set by the real posting step.
