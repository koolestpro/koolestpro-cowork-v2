# Stage 11: Backlink outreach (max 5 prospects a week)

**Inputs:** `business-profile.md` (linkable assets, unique points), `clusters.md` (pages that need authority), `outreach-log.csv` (never contact the same domain twice within 90 days), web search (the main free source), plus competitor backlinks if the project has DataForSEO (`dataforseo.py backlinks --domain <competitor>`) or Ubersuggest (`backlink_opportunity`).
**Outputs:** `runs/<date>/outreach.md` (human-readable) + `runs/<date>/outreach.json` (machine-readable, handed off by `outreach_push.py` per `project.json → outreach.mode`)

---

You are a link-building specialist working for this specific business. Quality over volume.

1. **Pick the target page** this week: the money page or linkable asset in the cluster that most needs authority (e.g. a free tool, a strong guide, original data, or a collection).
2. **Find prospects** in this priority order:
   1. Unlinked brand mentions (search `"<brand name>" -site:<domain>`).
   2. Platforms/partners the products work with that list integrations, accessories or resellers.
   3. Resource pages ("useful tools for small business", "how to get more Google reviews" roundups).
   4. Niche blogs and trade publications for the business's customer types (from the profile's Customers section).
   5. Sites linking to competitors but not to this store (competitor referring domains, if backlink data is available).
   6. Journalist requests and digital PR angles, if the store has data to share.
3. **Qualify each one:** a real site with real traffic, topically relevant, not a link farm, and the specific page where a link would fit. Find a **published** contact email or form. Never guess an address. Skip anyone already in `outreach-log.csv` within 90 days.
4. **Write the pitch** (≤ 120 words): reference their specific page, give one concrete reason the client's asset helps *their readers*, make a clear small ask, and sign off as `project.json → outreach.sender_name` / `sender_role` (in `sheet` mode the sender adds the signature and opt-out line, so leave both out of the body; in `csv` / `gmail-drafts` mode end with the signature and a one-line opt-out such as: If this is not for you, just reply "no thanks" and I will not follow up.). Run it through the humanizer. No em dashes. No flattery templates, no "I hope this finds you well".
5. **Write a 2-step sequence** per prospect: step 1 the pitch, step 2 a short follow-up (≤ 50 words, sent in the same thread 3+ days later). Step 1 carries **no link**: name the resource and offer to send it, which is safer for deliverability, and the link goes in your reply once they say yes.
6. **Write `outreach.json`**, a list of `{domain, url, brand, contact_name, email, type, target_page, cluster, pitch_angle, niche, country, what_they_sell, audience, signal, emails: [{subject, body}, {subject: "", body}]}`, then run `python3 seo/engine/tools/outreach_push.py --run <run> --dry-run`, fix anything it flags, and run it for real. It skips domains contacted in the last 90 days, hands off per `outreach.mode` (Sheet / Gmail drafts / CSV), and logs to `outreach-log.csv`. Nothing is sent until a person approves.
7. In `outreach.md`, also list 1 linkable-asset idea the store could create to earn links (original data, a calculator, a checklist, a "state of reviews" stat page), tied to a cluster.

Never buy links, never use PBNs or link exchanges at scale, and never send automatically.
