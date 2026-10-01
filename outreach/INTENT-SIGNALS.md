# Intent signals: reach out within days of a buying signal (design, not built yet)

Written 2026-10-01 from Ridwan's idea: when a company posts a job or a request that Ridwan could fulfil, email the right person within 1 to 3 days. This is source A in the research thread, and the thread's highest-converting lead source.

## Where signals come from, and what is realistic

| Source | Realistic? | Notes |
|---|---|---|
| Free job feeds: **Remotive**, **RemoteOK** (JSON, no key), **Jooble** (free key, 60+ countries), **Adzuna** (free key, about 16 countries, 250 calls a day on the default limit) ([overview](https://github.com/earnnova-dev/awesome-remote-job-apis)) | Yes | Searchable by keyword ("Shopify developer", "ecommerce", "CRO"). Returns title, company, location, link, date. No official Nigeria coverage on Adzuna. Check each one's terms and attribution rules |
| Hacker News "Who is hiring", company careers pages, Shopify Experts jobs | Mostly yes | Public pages |
| LinkedIn Jobs, Indeed, Wellfound | Risky | Their terms forbid scraping and they block it. Safer: Jooble and Adzuna already aggregate many of these postings |
| **Upwork** | **No** | Upwork's terms forbid copying or scraping, and a client's company name is normally hidden; posts that include a company name or email break Upwork's rules ([Upwork support](https://support.upwork.com/hc/en-us/articles/211063328-Why-was-my-job-post-removed)). Paid scrapers exist but go against the terms and would not reveal the company. The legitimate use is Ridwan answering those jobs with proposals |
| **Contra** | Almost certainly no | Not verified from here; assume the same client privacy and no scraping. Use the platform normally |
| Public posts asking for a Shopify developer on X, Reddit, LinkedIn, Shopify Community | Yes, partly | Search feeds and alerts; the poster's website is often in their profile |

## The pipeline

1. **Poll the feeds** every 30 minutes for a keyword set and countries (Apps Script `UrlFetchApp`). Keep only postings newer than 72 hours (the date is in the feed). Dedupe by company.
2. **Company to website:** the job link or the company profile usually names the site. Otherwise a guess from the company name is verified by fetching the site and matching the name. If the site cannot be confirmed, drop it. Wrong guesses are worse than missing ones.
3. **Score it** with the store rubric (small and upcoming wanted, big brand not).
4. **Who to email:** a decision maker (founder, head of e-commerce or marketing), not HR: HR does not buy services. Free email finding is limited (site contact pages and published addresses); a paid contact-data source would give names.
5. **Write and send fast:** a new `play` (`hiring_signal`) whose first email names the real posting honestly ("saw you're looking for a Shopify developer"). Never pretends to be an applicant. Offers the faster, fixed-price alternative to a hire.
6. **Speed:** these leads skip the approval queue ordering and go to the front of the send queue (still inside the daily cap and the lead's working hours; the cap exists to protect the Gmail account).

## Open decisions for Ridwan

- Which keyword set and countries to start with.
- Whether to pay for a contact-data source once this works (names of decision makers).
- Whether to email the hiring contact at all when no decision maker can be found.
