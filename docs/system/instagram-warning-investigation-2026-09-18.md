# Instagram "We suspect automated behaviour" warning: investigation (2026-09-18)

Trigger: Ridwan saw `instagram.com/accounts/scraping_warning/` on @koolestpro at ~10:31 WAT on 2026-09-18 (a first warning came earlier, after IG automation started). Instagram posting is **paused** until the cause is settled.

## What the warning means

`scraping_warning` is Instagram's anti-scraping check. It fires when the **logged-in web session** behaves like a bot: many profile/post/media requests in a short burst, image or media fetches driven by a script or extension, or a third-party tool using the account's session. It is not the message Instagram shows for API publishing problems.

## Everything in this project that touches Instagram, checked one by one

| System | Touches Instagram how | Uses Ridwan's logged-in session? | Verdict |
|---|---|---|---|
| Make "Koolestpro Social Distribution" (6565331), IG route | Official Graph API (`graph.instagram.com`, Instagram Login API token) | No, API token | **Low risk.** Only 4 posts ever went out this way (08 Sep ×2, 09 Sep, 12 Sep), well under any limit. API publishing is sanctioned. **Currently paused**: the route filter reads `platform = "Instagrams"` (typo on purpose), so no row matches. |
| `instagram_client.py` | Same official API (publish, token refresh, media list) | No | Low risk. |
| BrowserAct (Tue Maps lead gen + Contact Finder) | BrowserAct's own cloud browser visits business sites; may land on public IG profiles | No: `profile_id` is never passed, so it runs logged-out on BrowserAct's IPs | Cannot flag @koolestpro. |
| Meta Ad Library bridge (Wed) | Apify actor scrapes the public Ad Library | No, Apify's infrastructure | Cannot flag @koolestpro. |
| KoolestFlow `lead_engine.py` | Google search `site:instagram.com`, optional Apify Instagram Profile Scraper | No, Apify/Serper servers, no cookies | Cannot flag @koolestpro. |
| Trend radar (Format Radar) | Configured to browse Instagram **with Claude in Chrome inside Ridwan's real Chrome** | **Yes, it would** | Log shows it never actually ran on IG (skipped W31 and W33 because it could not pick a browser unattended). **Disabled on 2026-09-18** in `trend-radar-config.json` so it can never start. |
| Abu Zayd Make scenario (6225494) | n/a | n/a | Inactive. |

## What was happening in Chrome right before the warning (the strongest lead)

Looking at the open tabs and file timestamps on 2026-09-18:

- The saved reference carousels in `references-for-posts/` were written between **09:35 and 10:03**.
- Open tabs: `instagram.com/koolestpro/`, a Google search for **"instagram carousel downloader"**, **fastdl.app** (carousel downloader) and **tools.trendsee.io/instagram-carousel-downloader**.
- An **"Image Downloader" Chrome extension** was open in the side panel (seen on a Facebook page at the time of the check).
- The warning appeared at **10:31**, about half an hour after the downloading.

Downloader sites and image-grabber extensions pull every image on a page in a burst from the logged-in browser. That is the textbook pattern the scraping check looks for. This fits today's warning much better than the API posting (4 posts in 10 days) or the lead-gen tools (which never use the account).

What this does not prove: the earlier, first warning. If that one also followed a session of saving or downloading posts, or heavy clicking through many prospect profiles in one sitting, it is the same cause.

## Other things that raise risk (not proof)

- Three separate Claude in Chrome browsers are connected to the account, and there are many extensions on the toolbar. Any extension with "read and change data on all sites" can run on instagram.com while logged in.
- Rapidly opening many prospect Instagram profiles from KoolestFlow by hand in one sitting looks like scraping too.

## Actions

Done by Claude (2026-09-18):
1. Confirmed Make IG route is not firing (filter mismatch). No IG executions since 12 Sep.
2. Disabled Instagram browsing in the trend radar (`trend-radar-config.json`).
3. Rulebook: automated browsers (Claude in Chrome, BrowserAct profiles, extensions) must never visit instagram.com while logged in as @koolestpro.

For Ridwan (only he can do these):
1. Stop using carousel downloader sites and image-downloader extensions on Instagram while logged in. To save a post for reference, use Instagram's own **Save** button, or screenshot it.
2. `chrome://extensions`: remove any Instagram/image downloader extension you don't need; for the rest, set **Site access → On click**.
3. Instagram → Settings → **Accounts Center → Password and security → Where you're logged in**: log out sessions you don't recognise. Then change the password and turn on two-factor authentication.
4. Instagram → Settings → **Apps and websites**: keep only "Koolestpro Publishing".
5. Use Instagram normally by hand for 5-7 days (post, reply, browse) with no downloaders.

## Turning Instagram automation back on (when Ridwan says so)

- Change the Make route filter back from `Instagrams` to `Instagram`.
- Start at **1 post per day**, at a fixed human hour, for the first two weeks. The queue had 5-6 IG rows per day on 13-17 Sep; that would have been too much for a newly automated account. Reschedule those rows before re-enabling.
- Never pair automated posting with a burst of downloader or scraper activity on the same day.
