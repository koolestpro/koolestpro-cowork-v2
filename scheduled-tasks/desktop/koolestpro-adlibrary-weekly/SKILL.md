---
name: koolestpro-adlibrary-weekly
description: Weekly Meta Ad Library lead-gen rotation (Wednesdays ~09:00). Scores leads in the cloud and QUEUES them to .ai-workflow/pending-push/; the Mac-side importer pushes them into local KoolestFlow.
---

This is the weekly automated run of the Meta Ad Library lead-gen pipeline for Ridwan's koolestpro-cowork-v2 project. You are a fresh session with no memory of prior conversations — follow these steps exactly. This is a SIBLING task to koolestpro-browseract-weekly (Tuesdays, Google Maps discovery) — same destination, different discovery source (paid ads instead of organic Maps listings).

CONTEXT: A script at .ai-workflow/tools/ad_library_koolestflow_bridge.py queries the Meta Ad Library (via the curious_coder/facebook-ads-library-scraper Apify actor) for businesses running ads in a given country/category, classifies each lead into a Build/Fix/Scale/Marketplace track (see .ai-workflow/tools/lead_playbook.py) using where their ad links to and an automated site-quality check, and scores them for Ridwan's KoolestFlow app (cold-dm-app).

⚠️⚠️ HYBRID PIPELINE — RESOLVED 2026-09-01, READ FIRST. This task no longer pushes to KoolestFlow. The "KNOWN OPEN ISSUE" flagged on 2026-08-27 (prospects vanishing from /api/state) is now confirmed and root-caused: KoolestFlow's Vercel deployment keeps prospects in SQLite on an ephemeral serverless filesystem. It accepts POST /api/state, echoes back a plausible count, and then serves an empty list from the next cold lambda. A BrowserAct run on 2026-09-01 lost all 5 of its leads this way, and the false success also marked all 5 brands "taken" in the ledger. Ridwan's real data lives on the LOCAL instance (KOOLESTFLOW_LOCAL_BASE_URL, http://127.0.0.1:8787), which no cloud sandbox can reach.

The fix Ridwan chose: score in the cloud, queue to a file, let his Mac import it. You run with --queue. A launchd job on his Mac (.ai-workflow/tools/import_pending_push.sh, every 30 min) drains .ai-workflow/pending-push/ into local KoolestFlow, verifies the write stuck, and only then records the brands in the taken-brands ledger. Leads queue safely while his Mac is asleep. Do not "fix" this by pushing directly — you will lose the leads.

⚠️ 2026-08-27 CORRECTIONS — STILL FULLY IN FORCE. The first live run (2026-08-26) pushed 4 leads and Ridwan rejected ALL FOUR: one (CeraVe Skincare) was a Konga.com marketplace product listing, not a real prospect's own site, and the other three (Soluna SKIN, and two "Korean skincare expert" pages at interview.lovi.care) were not Nigerian businesses at all. Two root causes were found and fixed the same day — both are already implemented in the script, this section explains WHY so a future session doesn't undo them:

1. **`country=NG` alone does not scope results — confirmed by direct testing (flipping `is_targeted_country` true/false produced byte-identical output).** What actually works: putting the city as literal text in the search query. `q=kids` returned Jumia/Amazon/Nestlé and other global brands; `q=kids Lagos` returned 10/10 genuinely Nigerian small businesses. `build_ad_library_url()` now always appends `--city` (or "Nigeria" as a fallback) to the keyword automatically — this happens inside the script from the `--city` arg you already pass in step 5, no extra flag needed. Do not remove this.

2. **Every lead (on an NG run) must also show an explicit Nigeria signal** — ₦/NGN/Naira, +234 or a Nigerian mobile prefix, "Lagos"/"Abuja"/"Nigeria", or a .ng/.com.ng domain — checked against the ad's page NAME, its body/card text, AND its link, or it must link to a Nigerian marketplace domain (konga.com, jumia.com/.com.ng, jiji.ng). No signal = skipped, not queued. (First version of this check missed signals sitting in the page name alone, e.g. "Zoom Exclusive Dental Care Lagos" — fixed same day, page_name is now included.)

3. **Marketplace sellers (Konga/Jumia/JiJi) are a valid lead type, handled differently — not banned.** Ridwan's own words: "There's nothing bad in looking for a seller on JiJi, Konga, or Jumia, but the aim is to find a way to contact them from their social media accounts and pitch them on having a website." A marketplace link is never treated as the prospect's own website (no site-quality check runs against it), the record's notes explicitly say it's a marketplace listing and that Ridwan needs to find their Instagram/WhatsApp manually, and it only qualifies at all if page_like_count >= 500 (only pursue marketplace sellers who look like they're already doing real volume/have budget).

4. **Priority: businesses with NO website yet.** Every lead carries a `track` field (Build/Fix/Scale/Low Priority), and the order sorts Build-track first. Do not change this ordering without Ridwan's say-so.

5. **Nigeria-only for now.** Do not run this task against a non-NG slot even if one is ever added to the rotation file, until Ridwan says otherwise.

6. **Known blind spot, not auto-fixed:** a re-run on 2026-08-27 pushed "Burger King Nigeria" — it passed every filter (only 5,785 page likes on that specific Facebook page) despite being a large international franchise that already has its own site and isn't really a from-scratch-website prospect. Like-count alone can't distinguish "small local business" from "famous chain's smaller regional page." Flag anything that looks like a recognizable national/international brand name in your run summary for Ridwan to eyeball, even if it passed the automated filters.

7. **Taken-brands ledger.** `.ai-workflow/taken-brands-ledger.json` prevents the same brand being sent twice across BOTH sources (Ad Library and BrowserAct/Maps share one push path). As of the hybrid change, the CLOUD run no longer writes the ledger — the Mac-side importer does, on a verified push. Do not write it yourself and do not call KoolestFlow's API directly. Since 2026-09-30 the script READS the ledger before queueing: brands already in it (or repeated within the same batch) are printed as "skipping X — already taken (...)" and left out of the queue file, and if nothing new remains no file is written at all ("Queued 0 prospect(s) -> no file written"). That means the ledger file must be present wherever you run the script; if you copy the tools into a cloud sandbox, copy taken-brands-ledger.json with them.

STEPS:

1. The project folder is normally mounted directly in the cloud bash tool at `/sessions/<session>/mnt/koolestpro-cowork-v2/` — check with `ls` and use it directly; no device_stage_files round-trip is needed. Only if it is NOT mounted, fall back to device tools; if neither is available, stop and report the run was skipped.

2. Confirm APIFY_API_TOKEN is present in .env. If missing, log status "error" with that note and do not attempt the run. (KOOLESTFLOW_* vars are no longer required for this task, since it does not push.)

3. Read ad_library_rotation.json. Take the entry at meta.currentIndex from the slots array (must be a Nigeria slot with a real `city` value — see rules 1 and 5 above), and meta.limitPerRun (this should be 10 — the actor rejects counts below 10; if it's lower, the script auto-bumps it, but use what's in the file).

4. Run (cloud Bash, allow up to 5-8 minutes — a single synchronous Apify call, no manual polling needed):
   python3 .ai-workflow/tools/ad_library_koolestflow_bridge.py --country "<country>" --keyword "<keyword>" --limit <limitPerRun> --niche "<niche>" --city "<city>" --audience-type "<audienceType>" --queue
   ALWAYS pass --queue. Do NOT pass --dry-run (it scores nothing to a file). Do NOT omit --city (see rule 1).

5. Capture the FULL stderr output, not just the final "Queued N" line — the script prints each skipped lead with its reason (mega-brand / no Nigeria signal / marketplace-but-low-likes / already taken). If the script wrote no file, set pendingPushFile to null and status to "skipped" in step 7. You need all of this for step 9.

6. Update ad_library_rotation.json: currentIndex = (currentIndex + 1) mod (length of slots), updatedAt = current ISO timestamp via shell `date -u +%Y-%m-%dT%H:%M:%S.000Z`.

7. Append one entry to ad-library-weekly-log.json's runs array: {"week": "<ISO week>", "ranAt": "<ISO timestamp>", "countryUsed": "<country>", "keywordUsed": "<keyword>", "leadsScored": <N>, "leadsPushed": 0, "pendingPushFile": "<relative path the script printed>", "brandsQueued": [<exact brand names, from the script's own output>], "brandsSkipped": {"megaBrand": [...], "noNigeriaSignal": [...], "marketplaceLowVolume": [...], "alreadyTaken": [...]}, "status": "queued"/"error"/"skipped", "note": "<summary or error, and flag any brand that looks like a recognizable chain per rule 6>"}. Populate brandsSkipped from the actual printed skip reasons, don't guess. leadsPushed stays 0 — only the Mac importer can turn that into a real number.

8. If the folder is mounted you have already written the files in place; verify by re-parsing both JSON files. Only if you had to fall back to device tools, write ad_library_rotation.json and ad-library-weekly-log.json back via SendUserFile + device_commit_files. Do NOT write taken-brands-ledger.json back — the cloud run no longer modifies it.

9. End with a plain-text summary that MUST include: the exact brand names queued this run (not just a count), the exact brand names skipped and why (grouped by reason), which country/niche/track priority ran, the pending-push filename, any brand that looks like a recognizable national/international chain (rule 6), and anything else needing Ridwan's attention. "Queued" is the correct success state — never claim leads reached KoolestFlow, you cannot verify that from here. This exact-brands reporting requirement is a standing instruction from Ridwan (2026-08-26) — a summary that only gives a count is not acceptable.

Do not touch outreach_tracker.json, dm_leads_pool.json, or send any outbound messages — this task's only job is Ad Library discovery + scoring + queueing.