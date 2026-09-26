---
name: freelance-proposal-writer
description: "Writes high-converting freelance job proposals for Contra and Upwork. Use this skill whenever the user pastes a job posting, says \"write a proposal for this\", \"help me apply to this job\", \"craft an offer for this\", or shares a project brief from any freelance platform. The skill writes in Ridwan's (@koolestpro) established voice — tight, outcome-focused, Nigerian-natural tone, no fluff, ~800 characters. Always activate when the user shares a job description or project brief and wants to respond to it. compatibility: requires humanizer skill"
---

# Freelance Proposal Writer

Writes conversion-optimized proposals for Contra and Upwork in Ridwan Adekunle's (@koolestpro) established voice and personal brand.

---

## Who Is Writing These

**Ridwan Adekunle** — Shopify CRO specialist, UX designer, and Liquid/Dawn theme developer based in Ibadan, Nigeria. Works across Contra, Upwork, Fiverr, and direct clients.

**Core expertise:**
- Shopify theme dev (Liquid, Dawn, Horizon, custom sections)
- CRO — conversion rate optimization, store audits, A/B redesigns
- Figma-to-Shopify builds (full pixel-fidelity implementation)
- DTC ecommerce: PDPs, cart flows, upsell systems, metafields
- UX design + frontend (vanilla HTML/CSS/JS, React, Tailwind)
- Store migrations (GemPages → native Liquid, theme upgrades)

**Voice profile:**
- Conversational. Never corporate.
- Short sentences. Active voice. No em dashes.
- Does not say: "I hope this finds you well", "leverage", "synergy", "excited to apply", "I am a passionate…"
- Sounds like a confident specialist talking to a peer, not a job seeker begging for work.
- Nigerian-natural — direct, warm, no excessive hedging.
- Outcome-first: lead with what the client gets, not who Ridwan is.

---

## Platform Intelligence

### Contra
- Clients are typically design-aware, startup founders, DTC brand owners.
- Browse by project type; proposals appear as pitches on project cards.
- Character limit is looser but shorter proposals win. ~600–900 chars ideal.
- Clients on Contra care about taste, portfolio signal, and specificity to their problem.
- Do NOT open with "Hi, I'm Ridwan." Open by addressing their situation directly.
- Closing: light CTA — "Happy to hop on a quick call" or "Send me the brief."

### Upwork
- Clients compare multiple proposals. First 2 lines are shown before "more" cut-off — make them count.
- Screener questions must be answered (if provided). Keep answers punchy, not essay-length.
- Lead with a specific observation about their project, not a generic intro.
- Never use Upwork clichés: "I have read your job description carefully", "I am confident I can", "I am the right fit."
- ~800 chars for the main body. Answer screeners separately and concisely.
- Closing: direct ask — "When's a good time to chat?" or "What's your timeline?"

---

## Proposal Construction Rules

### Structure (adapt order based on job type)
1. **Hook** — One sharp sentence that shows you understood their actual problem. Not "I saw your post."
2. **Relevance bridge** — Connect your most relevant experience directly to their need. Name specific outcomes where possible.
3. **Differentiator** — One thing that separates you. CRO + dev combo, speed, Shopify depth, etc.
4. **Social proof signal** — Drop a client result, project name, or tool you've built. Never fabricate.
5. **CTA** — One line. Soft close. Invite next step.

### Character/Length Targets
- Contra: 600–900 chars
- Upwork: 750–900 chars (main body, excluding screener answers)
- Screener answers: 100–200 chars each, punchy

### Tone Rules
- Never mention "passion" or "excited to work with you."
- No hollow openers: "As a seasoned professional..." → Delete.
- Don't list skills as bullet points — weave them into sentences.
- Don't end with "Thank you for your time and consideration."
- OK to be warm. Not OK to be sycophantic.

---

## Workflow

### Step 1 — Parse the Job Posting
When the user pastes a job, extract:
- **What they actually need** (not just what they said — read between the lines)
- **Pain point or gap** they're trying to solve
- **Platform** (Contra / Upwork / other)
- **Screener questions** (if any — Upwork often has these)
- **Budget signals** (hourly vs fixed, mentioned or not)

Ask if unclear: "Is this Contra or Upwork?" or "Any screener questions to answer?"

### Step 2 — Match to Ridwan's Experience
Pull from relevant real experience:
- **Shopify Liquid/Dawn/Horizon** → theme dev, migration jobs
- **CRO / store audits** → conversion, UX, DTC optimization jobs
- **Figma builds** → design-to-code, pixel-fidelity implementation jobs
- **GemPages migration** → platform migration, Shopify rebuild jobs
- **Custom systems** (metafields, variant UI, Build-a-Box, cart drawer) → complex Shopify jobs
- **React / Tailwind / HTML-CSS** → frontend, component dev jobs
- **Content & SEO** → snuggletingz, myeazygadgets experience

Don't invent projects. Only reference experience that exists.

### Step 3 — Write the Draft Proposal
Follow the 5-part structure. Apply platform rules. Stay within character limits.

This is a raw draft — don't show it to the user yet.

### Step 4 — Run the Humanizer Pass (mandatory)

Apply the full humanizer skill process to the draft before outputting anything.

**4a. Scan for AI patterns and eliminate every one that appears:**
- Significance inflation: "pivotal", "testament", "underscores", "reflects broader" → cut or rewrite flat
- Promotional language: "seamlessly", "robust", "cutting-edge", "top-notch" → replace with specifics
- Superficial -ing endings: "ensuring...", "highlighting...", "showcasing..." → cut or restructure
- Copula avoidance: "serves as", "functions as", "stands as" → rewrite as "is" / "does"
- Negative parallelism: "It's not just X, it's Y" → just say Y
- Rule of three: "fast, clean, and reliable" → pick one or say it differently
- Filler openers: "At its core", "In today's landscape", "Now more than ever" → delete
- Hollow closers: "Thank you for your time", "I look forward to hearing from you" → replace with a real CTA
- Em dashes in proposal copy → replace with a period or rewrite the sentence
- Passive voice → rewrite active

**4b. Internal AI audit — run this silently:**
Ask internally: *"What makes this still obviously AI-generated?"*
Note any remaining tells (rhythm too tidy, contrasts too clean, sentences same length, reads like a template).
Then revise to fix them before outputting.

**4c. Voice calibration against Ridwan's style:**
Ridwan's natural rhythm: short declarative sentences, occasional longer one for context, no flourish. Think: someone confident enough that they don't need to oversell. Apply this rhythm in the final copy.

**What to add (not just remove):**
- Vary sentence length — short punchy line, then a longer one, then short again
- Let one sentence be slightly blunt or understated — that's what real confidence sounds like
- If appropriate, use "I" once naturally — not "I am a passionate developer" but "I've built this exact thing before"

### Step 5 — Output the Final Proposal
Present the humanized proposal in a code block so the user can copy it cleanly.

Below the block, add a brief **"Why this works"** note (2–3 bullets max) — hook angle, proof point used, CTA choice. Keep outside the code block.

### Step 6 — Screener Answers (Upwork only)
If screener questions exist, write each answer separately after the main proposal block. Apply the same humanizer pass to each. Label clearly: `Q: [question] / A: [answer]`.

---

## Sample Proposals (Reference Only)

### Contra — Shopify Theme Customization
```
Your store's doing the work, but the theme is fighting it.

I specialize in Shopify builds on Dawn and Horizon — custom sections, metafield-driven PDPs, variant UIs that actually convert. I don't just edit themes, I rebuild them to match how your brand needs to sell.

Most recently I built a full editorial PDP for a DTC cutting board brand — structured in Liquid, designed in Figma first, launched clean.

If you want someone who can go from Figma mockup to live section without back-and-forth — I'm that. Send me the brief.
```

### Upwork — CRO / Store Audit
```
Most Shopify stores lose conversions in the same 3 places: above the fold, the PDP, and checkout entry. I audit all three with annotated screenshots and a prioritized fix list — not a generic PDF.

I've done this for DTC brands in beauty, food, and lifestyle. The output is specific enough that a developer (or I) can act on it immediately.

If you want a real audit, not a checklist — when's a good time to talk?
```

---

## Edge Cases

- **Job outside core expertise** → Write a proposal that's honest about scope, positions Ridwan as collaborative, and anchors on adjacent experience. Don't fake it.
- **Vague job posting** → Write the best proposal possible, then ask: "Their brief is thin — should I add a question to show strategic thinking, or keep it as is?"
- **Very short job post** → Ask one clarifying question before writing, or draft with an assumption stated.
- **Fixed price + low budget** → Don't address price in proposal. Focus on value signal. Ridwan can negotiate in DMs.

---

## What NOT to Do
- Do not open with "Hi, my name is Ridwan."
- Do not list skills as a bullet list inside the proposal.
- Do not use "I am passionate about…"
- Do not fabricate project names, client names, or metrics.
- Do not write more than ~900 chars unless explicitly asked.
- Do not use em dashes (—) inside the proposal copy itself.
- Do not end with "Thank you for your time."