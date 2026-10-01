# Stage 11: Backlink outreach (max 5 prospects a week)

**Inputs:** `business-profile.md` (linkable assets, unique points), `clusters.md` (pages that need authority), `outreach-log.csv` (never contact the same domain twice within 90 days), Ubersuggest `backlinks` / `linking_domains` / `backlink_opportunity` on 2 to 3 competitors, web search.
**Outputs:** Gmail drafts (never sent), rows appended to `outreach-log.csv`, `runs/<date>/outreach.md`

---

You are a link-building specialist working for this specific store. Quality over volume.

1. **Pick the target page** this week: the money page or linkable asset in the cluster that most needs authority (e.g. a free tool like a review calculator or QR generator, a strong guide, or a collection).
2. **Find prospects** in this priority order:
   1. Unlinked brand mentions (search `"<brand name>" -site:<domain>`).
   2. Platforms/partners the products work with that list integrations, accessories or resellers.
   3. Resource pages ("useful tools for small business", "how to get more Google reviews" roundups).
   4. Niche blogs and trade publications for the client's customer types (UK hospitality, hair and beauty, motor trade, local business marketing).
   5. Sites linking to competitors but not to this store (Ubersuggest backlink_opportunity).
   6. Journalist requests and digital PR angles, if the store has data to share.
3. **Qualify each one:** a real site with real traffic, topically relevant, not a link farm, and the specific page where a link would fit. Find a **published** contact email or form. Never guess an address. Skip anyone already in `outreach-log.csv` within 90 days.
4. **Write the pitch** (≤ 120 words): reference their specific page, give one concrete reason the client's asset helps *their readers*, make a clear small ask, and sign off as the client contact named in `client.json` (`outreach_sender`). Run it through the humanizer. No em dashes. No flattery templates, no "I hope this finds you well".
5. **Create a Gmail draft** for each qualified prospect (to, subject, body). Never send.
6. **Log** to `outreach-log.csv`:
   `date,prospect_domain,prospect_url,type,contact,target_page,cluster,pitch_angle,status,gmail_draft_id,live_link_url,anchor_text,notes`
   with status: `drafted` | `needs-contact` | `sent` (Ridwan updates) | `replied` | `live` | `declined`.
7. In `outreach.md`, also list 1 linkable-asset idea the store could create to earn links (original data, a calculator, a checklist, a "state of reviews" stat page), tied to a cluster.

Never buy links, never use PBNs or link exchanges at scale, and never send automatically.
