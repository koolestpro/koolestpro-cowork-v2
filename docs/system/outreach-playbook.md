# Outreach playbook

**Who this is for:** whoever is sending Koolestpro's outreach. Written 2026-09-07, when Ridwan decided to hire someone to run it rather than send every message himself.

**Part of** [04 Outbound](04-outbound.md). Strategy lives in `docs/koolestpro-growth-operating-plan.md` Tracks D and E. This file is the executable version: who to message, what to say, what to do when they reply.

---

## Read this part twice

Six clients have come from content. **Outbound has produced zero, because nobody has ever sent it.** You are not maintaining a working machine. You are starting one. Expect the first few weeks to teach us things this document gets wrong, and say so when they do.

Four rules that get someone removed from this job if broken:

1. **Send by hand. Never use DM automation, bots, or third party sending tools on Instagram.** A ban costs the channel permanently, and Instagram DM is the whole Nigeria motion. This is not caution, it is the single largest risk in the plan.
2. **Never say or imply that Lumora, MERIDIAN, KURA or HALOS was a client.** They are demo builds. If a prospect asks, they are "a demo store we built to show what the free version looks like." Getting this wrong is worse than losing the deal.
3. **Never quote a price that is not on the published ladder, and never re-quote someone mid conversation.** If they push on price, that goes to Ridwan.
4. **Never promise a date.** You do not control the build queue.

---

## The two markets never mix

| | Nigeria / Africa | International |
|---|---|---|
| Who | Businesses selling through DMs, often already running Meta or TikTok ads | Shopify brands doing roughly $10k to $200k a month |
| First channel | Instagram DM | Email |
| Currency | Naira | USD |
| Opening gift | A free ad creative, then a free sample site | A hero section teaser, then a live rebuild |
| Tone | **Respectful and warm. Always open with a time-based greeting** | **Concise and peer level. No greeting at all** |

Wrong currency in the wrong market is an instant tell that this is a template. Check before every send.

### The greeting rule is not optional

Nigerian business culture expects politeness before business. A message that opens cold reads as rude, and rude does not get a reply no matter how good the offer is. So every Nigerian DM opens with **"Good morning"**, **"Good afternoon"** or **"Good evening"**, picked from *their* local time, not yours.

The reverse holds internationally. A greeting there reads as filler and wastes the notification preview, so those messages start on the observation.

KoolestFlow already enforces both. `ai_engine.py` computes the correct greeting from the prospect's `local_time` and instructs the model to use only that one for Nigeria, Ghana and Senegal, and explicitly forbids any greeting for US, UK and Canada. **If you are writing by hand, match what the app would have produced.** Do not fight it.

### One real tension, and how to resolve it

The blueprint this system was built from says the first 8 to 12 words must be notification-optimised: a concrete detail, never a generic greeting, because the preview is what decides whether the message gets opened at all.

That collides with the Nigerian greeting rule. Both are right, so do both:

> Good afternoon. Saw the two ankara sets you posted on Tuesday.

The greeting takes two words. The specific detail still lands inside the preview. What kills the message is not the greeting, it is spending the next fifteen words introducing yourself before you have shown you looked.

---

## Your day

About 45 minutes, five days a week.

1. Open KoolestFlow. Filter to `pipeline_stage: First Message Ready`.
2. Work the list top down by `fit_score`. Highest first.
3. For each one, spend two minutes actually looking at their Instagram or their site. You need one true, specific detail before you send anything. No detail, no send. Move them to `Needs Review` with a note instead.
4. Send the right template with that detail filled in.
5. Update the prospect in KoolestFlow immediately. Stage, date sent, what you said if you changed anything.
6. Check yesterday's sends for replies. Handle per the reply guide below.
7. Anything you are unsure about goes in the daily note to Ridwan rather than getting an improvised answer.

Target volume is 15 to 20 qualified prospects a week. That is deliberately small. This channel dies from volume, not from patience.

### Account safety, which is the real constraint

Right now there is **one** Instagram account: Ridwan's personal one, the same account all his content is posted from. It carries his face, his work and years of effort. Instagram bans in clusters, so losing it would take the content channel and the outreach channel in the same afternoon.

Numbers from the blueprint this system was built on, for an established account:

| | |
|---|---|
| Safe daily ceiling | 10 to 20 DMs |
| Absolute maximum | **never above 20 per day, per account** |
| Also flagged | 50 DMs in ten minutes, 100 follows in an hour, 200 rapid likes |

The blueprint's warning is the part people miss: **"even if you're doing it manually, if it looks automated, you're toast."** Bursts are the tell, not totals. Fifteen DMs spread over a working day is invisible. The same fifteen in twenty minutes is a pattern.

At 15 to 20 a week, this plan sits roughly ten times under the ceiling. That headroom is deliberate and it is not an invitation to use it. The limit on this business is how many free sample sites can be built, not how many messages can be sent.

**Multiple accounts and proxies are explicitly not in scope yet.** The blueprint covers anti-detect browsers, mobile proxies and account warm-up ladders, and that is the right playbook for aggressive volume later. Ridwan's decision for now is one account, conservative pace, no automation of any kind. Revisit only when fulfilment can absorb more than it currently can.

**The two minute look is the job.** Anyone can paste a template. The reason this works at all is that the first line proves a human looked. If you find yourself sending the same first line twice in a day, stop.

**What to look for is in the app, not here.** Open a prospect, hit edit, and the "What to look for" panel lists it for that prospect's market. Type what you find into "What you saw". That field is the only free text the message generator receives, so an empty one produces a generic DM no matter which template you pick. The app now tells you when it is empty, and what else is missing, right at the generate button.

---

## Nigeria: Instagram DM

Every prospect carries a `track` in KoolestFlow. It decides which message they get.

### Build track: real business, no website

The most common and the best fit. They have followers, real products, real comments, and no site.

```
[Good morning / Good afternoon / Good evening], [one true specific thing:
the product in their last post, the comments asking for price, the fact
that orders go through DM].

I build online stores for businesses like yours. Before anything else I
usually make one free ad creative using your own product photos, so you
can see the quality first. No cost, and nothing owed either way.

Would you like me to send one?
```

Why it opens with the ad and not the site: they already buy ads, so a better ad reads as value immediately. It costs us half an hour instead of a full day, and their new ad still has nowhere good to land, which sets up the site conversation without us arguing for it.

### Marketplace track: selling on Jumia, Konga or JiJi

```
[Good morning / Good afternoon / Good evening], I saw your store on
[marketplace]. [One true specific thing: a product, the review count,
how long they have been selling.]

You are already doing the hard part, which is moving product. The part
that is missing is that the customer belongs to [marketplace] and not to
you. No list, no repeat buyers, and they take a cut of every order.

I build stores that fix that. I can make you a free ad creative first so
you can see the work before you decide anything. Would that be useful?
```

### Fix track: has a site, but it is weak

```
[Good morning / Good afternoon / Good evening], I had a look at
[their site]. [One true specific thing you actually saw: the mobile
layout, the checkout, a slow gallery, no prices visible.]

I do conversion work on stores like this. I would be happy to send a
quick before and after of one section of your page, free, so you can see
what I mean rather than take my word for it.

Would you like me to?
```

**Note on all three:** these are the hand-written fallback. KoolestFlow's `generate_message()` produces the same shape from the prospect's own data and picks the greeting from their local time. Prefer the app's output. Use these when you are writing manually or the app is unavailable.

### Follow ups

One follow up after four days. One more after nine. Then stop and mark them `No Response`. Three messages to someone who has not replied is where this starts feeling like spam.

**Follow up 1, day +4:**

```
Hi, following up on this. Still happy to make that free [ad creative /
before and after] if you want it. No pressure either way.
```

**Follow up 2, day +9:**

```
Last one from me. If it is ever useful, the offer stands. Good luck with
[their business name].
```

That last line is not softness. Someone who says no in September sometimes says yes in January, and a graceful exit is what keeps that possible.

---

## International: email first

Sequence per prospect, escalating channels. Not four campaigns at once.

| Day | Channel | Note |
|---|---|---|
| 0 | Email | The only channel safe to semi automate |
| +4 | Instagram DM | Manual, short, it lands in Requests |
| +9 | LinkedIn | Only if there is a named ecommerce or marketing lead |
| +14 | Site contact form | Last resort, when no email exists |

Send from `hello@mail.koolestpro.com`, never the main domain, so a spam complaint cannot poison it. Always include an opt out.

**Day 0 email:**

```
Subject: [Brand] product page, one thing

Hi [name],

I look at Shopify product pages for a living. Yours came up while I was
going through [category] brands.

[One specific, checkable observation. Not a compliment. Something you
actually saw on the page.]

I rebuilt a section of it to show what I mean. Two minute look, no
attachment, just a link:

[link]

If it is useful, happy to talk. If not, no reply needed and I will not
follow up more than twice.

Ridwan
Koolestpro, koolestpro.com
```

**Day +4, Instagram DM.** Short. It lands in Requests, so length works against you.

```
Hi, I sent an email a few days ago about [brand]'s product page and the
[specific thing]. Might have gone to promotions. The rebuild is here if
you want a look: [link]
```

---

## When they reply

| They say | You do |
|---|---|
| "Yes send it" | Mark `Interested` in KoolestFlow, tell Ridwan the same day. He builds the asset. Do not promise when. |
| "How much?" | Send the published ladder for their market, nothing else. Do not negotiate, do not discount, do not invent a package. |
| "Who are you / is this real?" | Point at koolestpro.com/work. Real client names only. Never the demo brands. |
| "Not interested" | Mark `Not Interested`. Reply once, briefly, politely. Never argue. |
| Anything technical or unusual | Do not improvise. Say you will check and come back, then ask Ridwan. |
| Anger, or asking how you got their details | Apologise once, mark `Do Not Contact`, stop. Never explain the scraping. |

**Prices you may quote, and nothing else:**

Nigeria: Starter ₦250k to ₦500k, Business ₦500k to ₦1M, Premium ₦1M and up.
International: audit $150 to $250, page build $600 to $900, full build $1,200 to $1,800.

Anything beyond those numbers is Ridwan's call, including every discount request.

---

## What to record, every time

In KoolestFlow, on the prospect:

- `pipeline_stage` moved to reflect what actually happened
- `first_message` or `follow_up_1`, the text you really sent, not the template
- `last_contact_at`
- `last_reply` pasted verbatim when they reply, including a rude one
- `notes` for anything a future conversation would need

**Paste replies word for word.** Summarised replies lose the thing that would have told us why the message worked.

---

## What changed here, and why

The growth plan says in two places that Ridwan sends every message himself (D6, E5). Hiring someone overrides that, but only partly, so the split is written down rather than assumed:

**The hire sends without asking:** any template above, with the personalisation filled in, to any prospect already sitting at `First Message Ready`.

**Ridwan approves first:** anything off template, any price question beyond the published ladder, any promise about timing or scope, and every free asset before it goes out.

**Unchanged:** manual sending only. A person sending by hand is still manual. Automation is still banned.

---

## Known gaps, so nobody wastes time hunting

- **No reply has ever been handled.** The reply table above is reasoning, not experience. Expect to rewrite it after the first twenty real replies.
- **Fulfilment is thin.** Two store template verticals exist, watches and skincare. A reply from a furniture or food brand has no template behind it yet, so it becomes a from scratch build. Do not let demand outrun this quietly, flag it early.
- **Instagram posting is blocked, Instagram DM is not.** Different problem, unrelated to this playbook. Nothing here waits on Meta.
- **Nigeria has no case study yet.** `/ng/stories` is empty. The first delivered free site should become one.
