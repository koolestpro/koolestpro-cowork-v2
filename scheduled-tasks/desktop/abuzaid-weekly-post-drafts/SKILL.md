---
name: abuzaid-weekly-post-drafts
description: Drafts the upcoming week's 7 Abuzaid Facebook posts (humanized, with image prompts) from the June 2026 content calendar, every Saturday.
---

You are drafting one week of Facebook posts for the page "Abuzaid Aragib" (أَبُو زَيْدٍ الرَّاغِبُ), following the existing June 2026 content calendar. This task runs every Saturday morning to prepare the week ahead.

MODEL REQUIREMENT, NON-NEGOTIABLE:
Perform ALL content writing on Claude Sonnet, never Opus. Draft posts by spawning subagents with the Agent tool using model: "sonnet". Opus may only orchestrate, inspect, and compile. Do not write final post copy directly on Opus.

POST LENGTH AND PARAGRAPH RULES, STRICT:

The posts must be short enough for Facebook readers to actually finish.

Length:
- Minimum: 400 characters.
- Target: 120–220 words.
- Hard maximum: 280 words.
- Only complex rebuttals may reach 320 words, and only if cutting more would damage clarity.
- Never use the old 500-word ceiling unless Ridwan explicitly asks for a long-form post.

Paragraphs:
- Default paragraph length: 1 sentence.
- Average paragraph length: 2/3 sentences.
- Maximum paragraph length: 4 sentences.
- Maximum words per paragraph: 50 words.
- If a paragraph passes 50 words, split it.
- If a sentence passes 32 words, rewrite or split it.
- No dense blocks.
- No paragraph should look longer than 3 lines on mobile.

Rhythm:
- Open with a sharp first line.
- Use short paragraphs.
- Let one idea breathe before moving to the next.
- End with a strong closer, not a summary.
- Do not over-explain.
- Do not turn a Facebook post into an article.

Final scan before saving:
- Count exact words for each post.
- Confirm every post is under 280 words unless marked as a rare complex rebuttal.
- Confirm no paragraph exceeds 35 words.
- Confirm no paragraph has more than 2 sentences.

After each post, include:
WORD COUNT: [exact count]
LONGEST PARAGRAPH: [word count]

STEP 1 — Read Sources First

Read these before drafting:

- Calendar:
  /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/outputs/30-day-content-plan-June-2026.md

- Project rules:
  /Users/mac/Downloads/Islamic Content/CLAUDE.md

- Skill/reference files:
  /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/SKILL.md
  /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/references/voice-persona.md
  /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/references/image-guide.md
  /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/references/image-memory.md
  /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/references/people-reference.md
  /Users/mac/Downloads/Islamic Content/abuzaid-content-engine/references/opposing-outlets.md

Follow these rules exactly. Do not improvise against them.

STEP 2 — Determine The Week

Compute the coming Monday, meaning the Monday two days after the Saturday run date.

Draft seven posts, Monday through Sunday, for the week beginning on that Monday.

Use the exact date, angle, pillar, tone mode, image category, and posting time listed in the calendar.

If the run date falls outside the June 2026 calendar range, draft the next seven days using the same weekly rhythm:

- Monday: Reform / Mode A
- Tuesday: Religion / Mode B
- Wednesday: Politics & Society / Mode A
- Thursday: Historic Reference / Mode B
- Friday: Unity / Mode B
- Saturday: Media Rebuttal or Internal Issue / Mode A
- Sunday: Reform Call or Religion Reflection / Mode B

If calendar extension is needed, clearly note that the calendar needs extending.

STEP 3 — Draft Each Post

For each of the seven days:

- Write a complete Facebook post on the day’s assigned angle.
- Apply Abu Zayd’s voice exactly: direct, grounded, Yoruba Muslim, Islamic, civic, sharp without sounding chaotic.
- Length: minimum 450 characters, target 120–220 words, hard maximum 280 words. Complex rebuttals/analysis may reach 350 words only when necessary.
- No affiliations.
- No event promotion.
- No third-party branding.
- No hashtags unless explicitly requested.
- No em dashes anywhere in the body.
- End every standalone post with a blank line, then:

- أَبُو زَيْدٍ الرَّاغِبُ

Run the humanizer skill on every draft. This is mandatory.

Before finalizing each post, scan for:
- em dashes in the body
- AI-sounding phrasing
- weak generic claims
- over-explaining
- missing Islamic grounding
- incorrect Arabic spelling
- tone drifting away from Abu Zayd

STEP 4 — Image Prompts

For every post, write TWO image prompts:

1. ORIGINAL IMAGE PROMPT FOR COMPARISON
A simpler prompt close to the format guide and calendar image category.

2. UPDATED IMAGE PROMPT
A stronger Abu Zayd house-style prompt matching the Week 1 visual quality:
- premium Islamic editorial poster quality
- deep emerald green, gold, cream, black
- cinematic or illustrated composition where appropriate
- Yoruba/Nigerian Muslim context where relevant
- clear visual metaphor, not generic decoration
- strong readable typography
- no stock-photo clichés
- no circular seal unless explicitly requested
- default branding is the linear wordmark footer:

Arabic:
أَبُو زَيْدٍ الرَّاغِبُ

English:
ABU ZAYD AR-RĀGHIB

Descriptor:
ISLAM • HISTORY • REFORM

The updated prompt should usually be better than the original prompt.

Do NOT generate images. Stop at image prompts unless Ridwan explicitly asks for image generation.

STEP 5 — Qur’an And Hadith Accuracy

This is strict.

If a post or image prompt quotes the Qur’an:

- Use the exact Arabic text.
- Verify the ayah before including it.
- Never allow AI to invent, approximate, distort, or stylize incorrect Qur’an text.
- In the image prompt, state that Qur’an text must be rendered deterministically or added afterward as a verified text layer.
- If exact Qur’an rendering cannot be guaranteed, the image should avoid Arabic Qur’an text and use a non-text visual metaphor instead.

Hadith citations must also be checked and worded carefully.

Do not treat sacred text like decorative text.

STEP 6 — Save Output

Save all seven posts to one markdown file:

/Users/mac/Downloads/Islamic Content/abuzaid-content-engine/outputs/week-of-YYYY-MM-DD-posts.md

Use the Monday date in the filename.

For each day include:

- weekday and date
- pillar and mode
- recommended posting time
- full humanized article
- ORIGINAL IMAGE PROMPT FOR COMPARISON
- UPDATED IMAGE PROMPT

Do not post anything to Facebook.

After saving, present the file path to Ridwan and give a one-line summary of the week’s theme.