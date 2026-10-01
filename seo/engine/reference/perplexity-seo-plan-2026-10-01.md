<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# I need a perfect prompt for generating blog post articles that are seo optimized on a target keyword or phrase and also based on a certain post idea

the post must be engaging, well structured and formatted, no em dashes, must follow a standard framework that top brands and seo agencies use. the primary goal is on seo

Here’s a strong **master prompt** you can use to generate SEO-optimized blog posts from a target keyword and a post idea. It is structured for search intent, readability, and on-page SEO best practices, including clear headings, short paragraphs, natural keyword use, and answer-first writing.[^1_1][^1_2][^1_3]

## Copy this prompt

```text
You are an expert SEO content strategist and senior blog writer.

Write a high-quality blog post based on the following inputs:

Target keyword / phrase: [INSERT KEYWORD]
Post idea / angle: [INSERT POST IDEA]
Target audience: [INSERT AUDIENCE]
Search intent: [INSERT INTENT: informational, commercial, transactional, navigational]
Brand voice: [INSERT VOICE]
Desired word count: [INSERT WORD COUNT RANGE]

Primary goal:
Create an SEO-optimized blog post that ranks well, matches search intent, and keeps readers engaged.

Requirements:
- Use the target keyword naturally in the title, introduction, at least one H2, and throughout the body without keyword stuffing.
- Build the article around the post idea while staying tightly aligned with the target keyword.
- Follow a standard SEO framework used by top brands and agencies: hook, clear structure, scannable headings, detailed body sections, FAQs if relevant, and a strong conclusion.
- Use H2 and H3 headings in a logical hierarchy.
- Start each major section with a direct answer or key takeaway, then expand.
- Keep paragraphs short and easy to scan.
- Use simple, clear language.
- Include bullet points or numbered lists where they improve readability.
- Do not use em dashes.
- Make the article engaging, polished, and useful, not generic or fluffy.
- Focus on search intent above all else.
- Include internal-link placeholders where relevant like: [Internal link to related article].
- Include external-source placeholders where relevant like: [External source].
- Avoid overly promotional language unless the topic requires it.
- Write for humans first, but make it fully SEO-friendly.

Output format:
1. SEO title options: give 5 options.
2. Meta description: 1 option, under 160 characters.
3. URL slug: 1 option.
4. Article outline: H1, H2s, and H3s.
5. Full blog post: write the complete article.
6. FAQs: include 3 to 5 relevant FAQs if useful for the topic.

Formatting rules:
- Use markdown.
- Make the content easy to skim.
- No em dashes.
- Do not mention SEO tactics explicitly inside the article unless it fits naturally.
- Make sure the article feels like something a top brand or SEO agency would publish.
```


## Better version for agency use

If you want a more advanced version, use this one. It gives the model more control over structure, SEO depth, and content quality, which is closer to how agencies write briefs.[^1_2][^1_4][^1_5]

```text
Act as a senior SEO strategist, content editor, and expert blog writer.

Your job is to create a search-optimized blog post from a target keyword and post idea.

INPUTS
- Target keyword: [INSERT KEYWORD]
- Secondary keywords: [INSERT SECONDARY KEYWORDS]
- Post idea: [INSERT POST IDEA]
- Search intent: [INSERT INTENT]
- Audience: [INSERT AUDIENCE]
- Brand voice: [INSERT BRAND VOICE]
- Word count target: [INSERT RANGE]
- Internal links: [INSERT LINKS OR TOPICS]
- External sources to reference: [INSERT SOURCES IF ANY]

GOAL
Produce a blog post that is highly relevant to the keyword, satisfies search intent, and is structured to perform well in search results.

CONTENT RULES
- Include the primary keyword in the title, introduction, one H2, and conclusion.
- Use secondary keywords naturally where relevant.
- Match the article structure to the search intent.
- Organize the post with a logical hierarchy of H2s and H3s.
- Lead each section with the main point first.
- Use short paragraphs and concise sentences.
- Add examples, steps, comparisons, or lists where useful.
- Include FAQ sections only if they add value.
- Write in a polished, authoritative, and reader-friendly style.
- Do not use em dashes.
- Avoid keyword stuffing.
- Avoid vague filler and generic explanations.
- Make the post feel original, useful, and publication-ready.

DELIVERABLES
A. 5 SEO title options
B. Meta description
C. Suggested URL slug
D. Full outline with H1, H2s, H3s
E. Full article in markdown
F. FAQ section
G. Suggested internal link placements
H. Suggested CTA

Before writing, think like a top SEO agency and choose the best structure for ranking and readability.
```


## Framework to follow

The strongest blog structure usually looks like this: title, hook-driven introduction, clearly grouped H2 sections, supporting H3s, optional FAQ, and conclusion with a next step. Good SEO briefs also specify the target keyword, related terms, search intent, audience, headings, and word count, which is why the prompt above asks for those inputs.[^1_6][^1_3][^1_4][^1_7][^1_1][^1_2]

## How to use it well

For best results, replace the placeholders with a very specific keyword and a focused post idea. For example, instead of “Shopify SEO,” use “Shopify SEO checklist for product pages” plus an angle like “for small e-commerce stores trying to rank faster.” That makes the output more aligned with real search intent and easier to rank.[^1_3][^1_1]

A useful next step is to turn this into a reusable **template prompt** for your content workflow, with slots for keyword, angle, audience, CTA, and internal links. Would you like me to turn this into a shorter copy-paste version for ChatGPT, Claude, or Perplexity style prompting?

<span style="display:none">[^1_10][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://www.semrush.com/blog/seo-blog-post/

[^1_2]: https://www.semrush.com/blog/seo-content-brief/

[^1_3]: https://blog.hubspot.com/marketing/blog-search-engine-optimization

[^1_4]: https://www.contentharmony.com/blog/how-to-build-content-briefs/

[^1_5]: https://www.stackmatix.com/blog/seo-content-brief-creation

[^1_6]: https://www.godaddy.com/resources/skills/how-to-write-a-blog-post

[^1_7]: https://www.semrush.com/blog/content-brief/

[^1_8]: https://www.wix.com/blog/blog-seo

[^1_9]: https://www.semrush.com/blog/blog-seo/

[^1_10]: https://surferseo.com/blog/perfect-blog-post-structure/


---

# Can I automate this? I'm thinking about setting up a system on my desktop where I use Claude to do this automation. At every stage there is a prompt for whatever we need. I already have OverSuggest connected to Claude.

Once a week I want to have a blog post that goes out and I want to also track how my posts are doing and make an informed decision, not just create generic posts. I want to make sure I determine a target keyword and a topic or a phrase or a content idea based on what I need for my business, for my SEO to improve.

I need to automate everything. I just want to make sure AI uses the right system to create my article, post it to my Shopify store, add the right image to it, and that we always track and see how those blocks are doing and whatever else I need to improve my SEO.

Yes, you can automate this, and the cleanest setup is a **weekly content pipeline** that researches a topic, generates the article, creates or selects an image, publishes to Shopify, and then measures results in a repeatable loop. Shopify’s APIs support blog/articles management, and Shopify’s own guidance emphasizes tracking SEO, engagement, and conversion metrics so you can improve posts instead of publishing blindly.[^2_1][^2_2][^2_3][^2_4][^2_5]

## Best automation shape

The best structure is a 5-step system: topic and keyword selection, brief generation, article creation, image creation, publishing to Shopify, then performance tracking and iteration. That is the same general pipeline used in fully automated content systems: research, write, generate image, publish, and monitor.[^2_4][^2_5][^2_6]

## Recommended workflow

1. **Keyword and topic selection.** Pull from business goals, search intent, and existing gaps so the post is useful for SEO and revenue, not just generic content.[^2_3][^2_4]
2. **Content brief generation.** Have Claude produce the title ideas, search intent, outline, H2s, internal links, FAQ ideas, and metadata before writing.[^2_7][^2_8]
3. **Article generation.** Claude writes the post using your house style, SEO rules, and formatting constraints, including no em dashes and strong readability.[^2_9][^2_10]
4. **Image generation or selection.** Use a design or image tool to create a featured image that matches the article topic and brand style, then attach it to the post.[^2_6]
5. **Publish to Shopify.** Use Shopify’s blog/article endpoints to create the post, set SEO data, tags, and the featured image.[^2_2][^2_11]
6. **Track performance.** Review Search Console, GA4, and Shopify Analytics for clicks, impressions, average position, organic traffic, CTR, and conversions.[^2_5][^2_1][^2_3]

## What to track

For blog SEO, the most useful metrics are impressions, average position, organic clicks, organic CTR, sessions from search, engagement time, and assisted conversions. Shopify also recommends looking at content performance through engagement, SEO, and conversion categories so you can tell whether a post is ranking, being read, and helping the business.[^2_1][^2_3][^2_5]
A practical rule is to keep a weekly scorecard for each post: target keyword, current rank, clicks, CTR, organic sessions, and any leads or sales influenced by the article.[^2_12][^2_3]

## Tools and setup

Since you already have OverSuggest connected to Claude, that can fit well into the research stage for keyword discovery and topic selection. Then you can connect Claude to your automation layer through scripts or an orchestrator, with Shopify Admin API handling publishing and Google tools handling measurement. If you want a desktop-based setup, a scheduler plus a local script runner can trigger the workflow every week and log results to a sheet or database.[^2_2][^2_4][^2_6]

## Simple architecture

| Stage | What it does | Suggested component |
| :-- | :-- | :-- |
| Research | Finds keyword and topic | Claude + OverSuggest |
| Brief | Builds outline and SEO plan | Claude |
| Writing | Produces blog post | Claude |
| Image | Creates featured image | Image tool or designer workflow |
| Publishing | Posts to Shopify | Shopify Admin API [^2_2] |
| Tracking | Monitors SEO and content performance | Search Console, GA4, Shopify Analytics [^2_1][^2_3][^2_5] |

## Important caution

Full automation is possible, but I would not make it fully hands-off at first. The safest version is “**semi-automated with approval**” so you can review the keyword choice, outline, and final draft before publishing, especially while you are still tuning quality and ranking outcomes. That keeps the system efficient without letting weak topics or bad drafts go live.[^2_4][^2_5]

## Practical next step

The best build is a weekly pipeline that starts with keyword research, then creates a content brief, article, image, and Shopify post, and finally records SEO results in a dashboard for the next round of decisions. That gives you a real content engine instead of random blog publishing.[^2_3][^2_6][^2_1]

Would you like me to design the exact automation blueprint for your desktop, including the Claude prompts for each stage, the Shopify API flow, and the weekly tracking sheet structure?

<span style="display:none">[^2_13][^2_14]</span>

<div align="center">⁂</div>

[^2_1]: https://www.shopify.com/blog/content-performance-tracking

[^2_2]: https://shopify.dev/docs/api/admin-rest/latest/resources/blog

[^2_3]: https://www.shopify.com/blog/seo-management

[^2_4]: https://www.shopify.com/blog/ecommerce-seo-audit

[^2_5]: https://www.shopify.com/blog/seo-tracking

[^2_6]: https://dev.to/miledevs/how-we-built-a-fully-automated-shopify-blog-pipeline-with-ai-3p9l

[^2_7]: https://www.semrush.com/blog/seo-content-brief/

[^2_8]: https://www.semrush.com/blog/content-brief/

[^2_9]: https://www.semrush.com/blog/seo-blog-post/

[^2_10]: https://surferseo.com/blog/perfect-blog-post-structure/

[^2_11]: https://shopify.dev/docs/api/storefront/latest/objects/blog

[^2_12]: https://webmedic.com/shopify-blog-seo

[^2_13]: https://www.shopify.com/blog/content-metrics

[^2_14]: https://apps.shopify.com/seo-auto-write-easy-blog


---

# Yes, please design the complete desktop automation blueprint

Yes. The best setup is a **weekly content factory** on your desktop with five layers: strategy, generation, publishing, tracking, and optimization. Shopify supports article creation with title, body, tags, image, and publishing options through its Admin APIs, and Shopify recommends tracking SEO, traffic, engagement, and conversion metrics so the system improves over time instead of just publishing content.[^3_1][^3_2][^3_3][^3_4]

## System design

Think of this as an assembly line:

1. **Strategy layer.** Choose the business goal, keyword, search intent, and content angle.
2. **Brief layer.** Claude turns that into a content brief with title options, outline, FAQs, and metadata.
3. **Draft layer.** Claude writes the full article in your preferred framework and style.
4. **Publish layer.** The post is sent to Shopify with the featured image, tags, and SEO fields.
5. **Analytics layer.** Performance is tracked weekly so the next article is based on real data, not guesses.[^3_3][^3_5][^3_1]

## Weekly workflow

### 1. Pick the target

The system should begin with a business-focused keyword selection step, not random topic ideas. Use search intent, your product/service priorities, and existing site gaps to choose the keyword and angle. If OverSuggest is already connected, let it feed keyword ideas into Claude for scoring and topic selection.[^3_2][^3_6]

### 2. Build the brief

Claude should generate a structured brief before writing. The brief should include target keyword, secondary keywords, audience, intent, title options, H2/H3 outline, internal links, CTA, and FAQ ideas. That aligns with how SEO briefs are typically built for consistent execution.[^3_7][^3_8]

### 3. Write the post

Claude writes the article using your rules:

- SEO first.
- No em dashes.
- Strong readability.
- Short paragraphs.
- Direct answers first.
- Clear heading hierarchy.
- Natural keyword placement.[^3_9][^3_10]


### 4. Create the image

Generate or select a featured image after the article is finalized. The image prompt should match the topic, brand style, and article angle, and the automation should save the image locally before upload. Shopify’s article APIs support attaching an image when creating the post.[^3_4][^3_3]

### 5. Publish to Shopify

Use Shopify’s Admin API to create the article in your chosen blog, attach tags, set the slug/handle, and publish immediately or schedule it. Shopify’s article resources support publishing, scheduling, images, and metadata, so this part is very automatable.[^3_3][^3_4]

### 6. Track results

Every week, pull metrics for each post:

- Impressions.
- Clicks.
- Organic CTR.
- Average position.
- Organic sessions.
- Engagement time.
- Conversions or assisted conversions.[^3_5][^3_1][^3_2]

Shopify recommends combining search performance data with website analytics and content performance reporting to make decisions based on actual outcomes. Posts with high impressions but low CTR are strong candidates for title and meta description optimization.[^3_11][^3_6][^3_2][^3_5]

## Desktop automation stack

Here is a practical stack for your setup:


| Layer | Recommended role |
| :-- | :-- |
| Claude | Strategy, briefs, drafting, revision |
| OverSuggest | Keyword discovery and idea generation |
| Desktop scheduler | Weekly trigger |
| Script runner | Orchestrates each stage |
| Image tool | Creates featured image |
| Shopify Admin API | Publishes articles [^3_3][^3_4] |
| Google Search Console | Tracks impressions, CTR, position [^3_2] |
| Shopify Analytics | Tracks sessions, engagement, revenue [^3_11][^3_5] |
| Sheet or database | Stores weekly results and decisions |

## Automation flow

A clean flow would look like this:

1. Scheduler runs every week.
2. Script asks Claude for topic ideas based on your business goals.
3. OverSuggest provides keyword candidates.
4. Claude scores and selects the best keyword.
5. Claude generates the brief.
6. Claude writes the article.
7. Image is created or selected.
8. Script uploads content and image to Shopify.
9. Script records the target keyword, URL, publish date, and post ID.
10. A separate weekly job pulls analytics and creates a performance report.[^3_1][^3_5][^3_3]

## Decision rules

To avoid generic content, your system should include rules like these:

- If the keyword has low relevance to business goals, reject it.
- If the article does not satisfy search intent, regenerate the brief.
- If the draft lacks clear section depth, rewrite before publishing.
- If a post gets impressions but poor CTR, update title and meta description.
- If a post ranks but does not convert, improve internal links and CTA.
- If a post gets no traction after a reasonable period, compare it against better-performing topics and reuse the winning pattern.[^3_6][^3_2][^3_5]


## Build phases

### Phase 1: Semi-automated

Use Claude to generate the topic, brief, draft, and image prompt, but review before publishing. This is the safest starting point because it protects quality while you tune the system.

### Phase 2: Fully automated publishing

Once the prompts and metrics are stable, let the system publish automatically to Shopify through the API.[^3_4][^3_3]

### Phase 3: Optimization loop

Add a weekly report that flags underperforming posts and suggests updates based on search visibility, CTR, engagement, and conversions.[^3_11][^3_2][^3_5]

## What I recommend you build first

Start with a simple version:

- One weekly article.
- One keyword.
- One featured image.
- One publish action.
- One performance report.

That gives you a real system fast, and it is much easier to refine than trying to automate everything at once. Shopify’s SEO guidance makes it clear that consistent measurement and iteration matter as much as publishing.[^3_2][^3_6][^3_1]

## Next deliverable

The next best step is to turn this into a concrete operating system with:

- exact Claude prompts for each stage,
- a folder structure for your desktop,
- the Shopify publishing payload,
- and a weekly tracking sheet template.

Should I draft the full **Claude prompt pack + workflow map + weekly content scorecard** for you next?

<span style="display:none">[^3_12][^3_13][^3_14]</span>

<div align="center">⁂</div>

[^3_1]: https://www.shopify.com/blog/content-metrics

[^3_2]: https://www.shopify.com/blog/seo-management

[^3_3]: https://shopify.dev/docs/api/admin-rest/latest/resources/article

[^3_4]: https://shopify.dev/docs/api/admin-graphql/latest/mutations/articleCreate

[^3_5]: https://www.shopify.com/blog/content-marketing-analytics

[^3_6]: https://www.shopify.com/blog/ecommerce-seo-audit

[^3_7]: https://www.semrush.com/blog/seo-content-brief/

[^3_8]: https://www.semrush.com/blog/content-brief/

[^3_9]: https://www.semrush.com/blog/seo-blog-post/

[^3_10]: https://surferseo.com/blog/perfect-blog-post-structure/

[^3_11]: https://www.shopify.com/blog/content-performance-tracking

[^3_12]: https://shopify.dev/docs/api/admin-rest/2024-07/resources/article

[^3_13]: https://apps.shopify.com/seometriks

[^3_14]: https://help.shopify.com/en/manual/online-store/web-performance/overview


---

# Yes, please give me the complete prompt pack and workflow map

Absolutely. Below is a complete **desktop automation blueprint + Claude prompt pack** you can implement as a weekly SEO blog system for your Shopify store. It is designed around Shopify’s article publishing capabilities and the SEO metrics Shopify recommends tracking, including impressions, CTR, average position, organic traffic, and conversions.[^4_1][^4_2][^4_3][^4_4]

## System architecture

Your automation should run as a pipeline with five modules:

1. **Strategy and keyword selection.** Use OverSuggest plus Claude to choose the best topic based on business goals, intent, and SEO opportunity.
2. **Brief creation.** Claude creates an SEO content brief with title, outline, intent, angle, and metadata.
3. **Draft generation.** Claude writes the full article in your preferred structure and voice.
4. **Publishing.** The script creates the Shopify article, attaches tags and image, and publishes or schedules it using the Admin API.[^4_5][^4_1]
5. **Tracking and optimization.** Weekly reporting checks Search Console and Shopify Analytics for clicks, impressions, CTR, average position, traffic, and conversions.[^4_2][^4_3][^4_4]

## Folder structure

Use one root folder on your desktop:

```text
Blog-Automation/
  input/
    business-goals.txt
    keywords.csv
    content-ideas.csv
  prompts/
    01-topic-selection.txt
    02-content-brief.txt
    03-article-draft.txt
    04-image-prompt.txt
    05-title-meta-optimizer.txt
    06-shopify-ready-finalizer.txt
    07-weekly-report.txt
  output/
    briefs/
    drafts/
    images/
    published/
    reports/
  logs/
    content-log.csv
    performance-log.csv
  config/
    brand-voice.txt
    seo-rules.txt
    prompt-rules.txt
```


## Workflow map

### Stage 1: Topic selection

Input: business goal, seed ideas, keyword list, current gaps.\
Output: one target keyword, one content angle, one search intent, one priority score.

### Stage 2: Brief generation

Input: target keyword and angle.\
Output: SEO brief with title options, outline, FAQs, CTA, internal links, and target word count.

### Stage 3: Draft writing

Input: brief and style rules.\
Output: full article in markdown or HTML.

### Stage 4: Image creation

Input: article title, angle, brand style, and visual direction.\
Output: featured image prompt or final image file.

### Stage 5: Shopify publish

Input: final article, tags, handle, image, publish date.\
Output: created Shopify article ID and URL.[^4_1][^4_5]

### Stage 6: Weekly reporting

Input: URL list and date ranges.\
Output: performance summary, ranking changes, CTR issues, update recommendations.[^4_3][^4_4][^4_2]

## Claude prompt pack

### 1. Topic selection prompt

```text
You are an SEO strategist for an e-commerce business.

Goal:
Choose the best blog topic for this week based on business value and SEO opportunity.

Inputs:
- Business goal: [INSERT GOAL]
- Target audience: [INSERT AUDIENCE]
- Seed keywords: [INSERT KEYWORDS]
- Product/service focus: [INSERT FOCUS]
- Existing content gaps: [INSERT GAPS]
- Brand tone: [INSERT TONE]

Task:
1. Generate 10 topic ideas.
2. Score each idea from 1 to 10 for SEO potential, business relevance, and content ease.
3. Choose the best one.
4. Return the final target keyword, search intent, content angle, and a 1-sentence reason.

Rules:
- Prioritize search intent and business relevance.
- Avoid generic topics.
- Prefer topics that can lead to traffic and conversions.
- Output as a clean table plus final recommendation.
```


### 2. Content brief prompt

```text
You are a senior SEO content strategist.

Create a detailed SEO brief for the following topic.

Target keyword: [INSERT KEYWORD]
Content angle: [INSERT ANGLE]
Search intent: [INSERT INTENT]
Audience: [INSERT AUDIENCE]
Brand voice: [INSERT VOICE]
Word count target: [INSERT RANGE]

Requirements:
- Give 5 title options.
- Write one meta description under 160 characters.
- Suggest one URL slug.
- Build a full outline with H1, H2s, and H3s.
- Include primary and secondary keyword suggestions.
- Include internal link opportunities.
- Include CTA ideas.
- Include 3 to 5 FAQ questions.
- Keep the structure optimized for SEO and readability.
- Make it specific, not generic.
```


### 3. Article drafting prompt

```text
You are an expert blog writer and SEO editor.

Write the full article based on this brief.

Brief:
[PASTE BRIEF]

Requirements:
- Use markdown formatting.
- Follow the outline exactly unless a small improvement is necessary.
- Put the main keyword in the title, intro, at least one H2, and conclusion.
- Write for humans first and search engines second.
- Keep paragraphs short.
- Use clear H2 and H3 headings.
- Include examples where helpful.
- Include bullets or numbered lists where useful.
- Do not use em dashes.
- Do not be fluffy or repetitive.
- End with a practical CTA.
- Include FAQ section if provided in the brief.

Output:
- Final title
- Full article
- Meta description
- URL slug
- Suggested image concept
```


### 4. Image prompt

```text
Create a featured image concept for this blog post.

Article title: [INSERT TITLE]
Topic: [INSERT TOPIC]
Audience: [INSERT AUDIENCE]
Brand style: [INSERT STYLE]
Color palette: [INSERT COLORS]
Image goal: [INSERT GOAL]

Requirements:
- Clean, modern, professional.
- Relevant to the article topic.
- Suitable for a Shopify blog featured image.
- No text heavy composition unless necessary.
- Landscape orientation.
- Return a concise image generation prompt and alt text.
```


### 5. Finalizer prompt

```text
You are preparing this blog post for Shopify publication.

Task:
1. Clean the article formatting.
2. Ensure the meta title and meta description are optimized.
3. Suggest tags.
4. Suggest the final URL handle.
5. Ensure the featured image alt text is SEO-friendly.
6. Check for keyword usage, readability, and formatting issues.
7. Return the final version ready for publishing.

Rules:
- No em dashes.
- Keep the post polished and publication-ready.
- Do not invent claims.
- Keep the structure consistent with the brief.
```


### 6. Weekly report prompt

```text
You are an SEO analyst.

Analyze this blog post performance data and give improvement actions.

Inputs:
- Target keyword: [INSERT KEYWORD]
- URL: [INSERT URL]
- Publish date: [INSERT DATE]
- Impressions: [INSERT VALUE]
- Clicks: [INSERT VALUE]
- CTR: [INSERT VALUE]
- Average position: [INSERT VALUE]
- Organic sessions: [INSERT VALUE]
- Conversions: [INSERT VALUE]
- Notes: [INSERT NOTES]

Task:
1. Summarize performance.
2. Identify what is working.
3. Identify what is weak.
4. Recommend 3 actions to improve rankings or CTR.
5. Recommend whether to update, expand, re-optimize, or leave as is.
6. Return a simple decision: improve, monitor, or replace.

Keep the analysis practical and focused on SEO growth.
```


## Shopify publish flow

Use Shopify’s article creation endpoint to publish the post. Shopify’s GraphQL Admin API supports article title, body, tags, image, handle, and scheduling, which makes this step suitable for automation. Your script should:[^4_5][^4_1]

1. Create the article body from Claude’s final output.
2. Upload or reference the featured image.
3. Set tags, handle, and publish date.
4. Submit the article to the blog.
5. Save the article ID, URL, and publish timestamp in your log.[^4_6][^4_1][^4_5]

## Tracking workflow

Your weekly tracking should compare content performance data against the same article’s business impact. Shopify recommends monitoring impressions, CTR, average position, organic traffic, and conversions, and then using those numbers to decide what to update. A simple decision framework:[^4_4][^4_2][^4_3]

- **High impressions, low CTR:** improve title and meta description.
- **Good CTR, weak rankings:** expand content and strengthen internal links.
- **Good traffic, low conversions:** improve CTA and product linkage.
- **Strong conversions:** replicate the topic pattern and interlink more aggressively.[^4_2][^4_3]


## Content log template

Use a CSV or sheet with these columns:

```text
publish_date,target_keyword,title,url,handle,blog,word_count,impressions,clicks,ctr,avg_position,organic_sessions,conversions,status,next_action
```


## Recommended operating rules

- Publish once per week on the same day.
- Never publish without keyword intent approval.
- Never skip the brief stage.
- Always store the final prompt outputs.
- Always track the same metrics for every post.
- Review the previous week before choosing the next topic.
- Update old posts every 4 to 8 weeks if they show impressions but weak CTR or rankings.[^4_7][^4_3][^4_4]


## Best implementation order

1. Build the folder structure.
2. Create the prompt files.
3. Connect Claude to the topic-selection stage.
4. Connect Shopify publishing.
5. Add tracking exports.
6. Add a weekly review report.
7. Add auto-optimization rules.

## What I would build first

Start with a semi-automated version:

- Claude selects the topic.
- Claude writes the brief.
- Claude writes the article.
- You approve before publish.
- The script posts to Shopify.
- A weekly report suggests updates.

That gives you control while still removing most of the manual work. Once quality is consistent, you can move to full automation.

I can turn this into a **ready-to-use desktop SOP document** next, or I can build the **exact prompt files one by one in copy-paste format**.

<span style="display:none">[^4_10][^4_11][^4_8][^4_9]</span>

<div align="center">⁂</div>

[^4_1]: https://shopify.dev/docs/api/admin-graphql/2026-04/mutations/articleCreate

[^4_2]: https://www.shopify.com/blog/content-performance-tracking

[^4_3]: https://www.shopify.com/blog/ecommerce-seo-audit

[^4_4]: https://www.shopify.com/blog/seo-management

[^4_5]: https://shopify.dev/docs/api/admin-graphql/latest/mutations/articlecreate

[^4_6]: https://shopify.dev/docs/api/admin-graphql/latest/objects/Article

[^4_7]: https://www.shopify.com/blog/content-metrics

[^4_8]: https://shopify.dev/docs/api/admin-graphql/latest/mutations/articleCreate

[^4_9]: https://shopify.dev/docs/api/admin-graphql/latest/payloads/ArticleCreatePayload

[^4_10]: https://shopify-dev.shopifycloud.com/docs/api/admin-graphql/2025-07/objects/mutation

[^4_11]: https://www.withone.ai/knowledge/shopify-admin/conn_mod_def::GJ7Fib16qVg::brG4-\_mYSTuu4-9ks3hUyg


---

# I want both the SOP document and the copy-paste prompt files now

Below is the full **desktop SOP document** plus the **copy-paste prompt files** you can save into your system right away. Shopify’s article API supports title, body, tags, image, handle, and scheduling, and Shopify recommends tracking SEO, engagement, and conversion metrics so your workflow can improve over time.[^5_1][^5_2][^5_3][^5_4]

## SOP document

### 1. Purpose

Build one SEO-focused Shopify blog post per week with minimal manual work. The system should choose a keyword based on business value, generate a strong content brief, write the article, create or select a featured image, publish to Shopify, and measure performance after publishing.[^5_4][^5_5][^5_1]

### 2. Goal

The primary goal is SEO growth that supports business growth. The content should rank, attract qualified traffic, and drive useful actions such as clicks, leads, or sales.[^5_6][^5_1][^5_4]

### 3. Tools

- Claude for strategy, briefing, writing, and analysis.
- OverSuggest for keyword discovery.
- Shopify Admin API for publishing articles.[^5_2][^5_3]
- Google Search Console for impressions, clicks, CTR, and average position.
- Shopify Analytics for traffic, engagement, and conversion outcomes.[^5_5][^5_1][^5_4]
- Local desktop folders for prompts, outputs, logs, and reports.


### 4. Weekly operating flow

1. Gather business goal and content priorities.
2. Generate keyword and topic candidates.
3. Score and select one keyword and angle.
4. Create the content brief.
5. Write the article.
6. Generate or select the featured image.
7. Finalize SEO fields and formatting.
8. Publish to Shopify.
9. Log the article details.
10. Review results the following week and decide whether to update, expand, or leave the post as-is.[^5_1][^5_4][^5_5]

### 5. Approval rules

Use semi-automation first. Topic, brief, title, and final article should be reviewed before publish until quality is stable. Once the output is consistently good, you can allow auto-publishing with a safety check for sensitive topics or weak keyword matches.[^5_4][^5_1]

### 6. Publishing rules

The article should include:

- A target keyword in the title, intro, at least one H2, and conclusion.
- A clear URL handle.
- Tags.
- A featured image.
- A strong meta title and meta description.
- Optional scheduled publish time.[^5_7][^5_3][^5_2]


### 7. Tracking rules

Track each post with the same metrics every week:

- Impressions.
- Clicks.
- CTR.
- Average position.
- Organic sessions.
- Engagement.
- Conversions.[^5_6][^5_5][^5_1]


### 8. Decision rules

- High impressions, low CTR = improve title and meta description.
- Good CTR, weak position = expand content and improve internal links.
- Traffic without conversions = improve CTA and linking to offers.
- Strong performance = use the same pattern for future posts.[^5_5][^5_1][^5_4]


### 9. File handling

Keep every output in a structured folder so you can audit the system later. Save the final brief, draft, image prompt, final post, and performance report for each week.

### 10. Review cycle

Every week, review the previous post before creating the next one. The new topic should be influenced by what worked last week, not just by fresh ideas.[^5_1][^5_4]

## Copy-paste prompt files

### 01-topic-selection.txt

```text
You are an SEO strategist for an e-commerce business.

Goal:
Choose the best blog topic for this week based on business value and SEO opportunity.

Inputs:
- Business goal: [INSERT GOAL]
- Target audience: [INSERT AUDIENCE]
- Seed keywords: [INSERT KEYWORDS]
- Product/service focus: [INSERT FOCUS]
- Existing content gaps: [INSERT GAPS]
- Brand tone: [INSERT TONE]

Task:
1. Generate 10 topic ideas.
2. Score each idea from 1 to 10 for SEO potential, business relevance, and content ease.
3. Choose the best one.
4. Return the final target keyword, search intent, content angle, and a 1-sentence reason.

Rules:
- Prioritize search intent and business relevance.
- Avoid generic topics.
- Prefer topics that can lead to traffic and conversions.
- Output as a clean table plus final recommendation.
```


### 02-content-brief.txt

```text
You are a senior SEO content strategist.

Create a detailed SEO brief for the following topic.

Target keyword: [INSERT KEYWORD]
Content angle: [INSERT ANGLE]
Search intent: [INSERT INTENT]
Audience: [INSERT AUDIENCE]
Brand voice: [INSERT VOICE]
Word count target: [INSERT RANGE]

Requirements:
- Give 5 title options.
- Write one meta description under 160 characters.
- Suggest one URL slug.
- Build a full outline with H1, H2s, and H3s.
- Include primary and secondary keyword suggestions.
- Include internal link opportunities.
- Include CTA ideas.
- Include 3 to 5 FAQ questions.
- Keep the structure optimized for SEO and readability.
- Make it specific, not generic.
```


### 03-article-draft.txt

```text
You are an expert blog writer and SEO editor.

Write the full article based on this brief.

Brief:
[PASTE BRIEF]

Requirements:
- Use markdown formatting.
- Follow the outline exactly unless a small improvement is necessary.
- Put the main keyword in the title, intro, at least one H2, and conclusion.
- Write for humans first and search engines second.
- Keep paragraphs short.
- Use clear H2 and H3 headings.
- Include examples where helpful.
- Include bullets or numbered lists where useful.
- Do not use em dashes.
- Do not be fluffy or repetitive.
- End with a practical CTA.
- Include FAQ section if provided in the brief.

Output:
- Final title
- Full article
- Meta description
- URL slug
- Suggested image concept
```


### 04-image-prompt.txt

```text
Create a featured image concept for this blog post.

Article title: [INSERT TITLE]
Topic: [INSERT TOPIC]
Audience: [INSERT AUDIENCE]
Brand style: [INSERT STYLE]
Color palette: [INSERT COLORS]
Image goal: [INSERT GOAL]

Requirements:
- Clean, modern, professional.
- Relevant to the article topic.
- Suitable for a Shopify blog featured image.
- No text heavy composition unless necessary.
- Landscape orientation.
- Return a concise image generation prompt and alt text.
```


### 05-finalizer.txt

```text
You are preparing this blog post for Shopify publication.

Task:
1. Clean the article formatting.
2. Ensure the meta title and meta description are optimized.
3. Suggest tags.
4. Suggest the final URL handle.
5. Ensure the featured image alt text is SEO-friendly.
6. Check for keyword usage, readability, and formatting issues.
7. Return the final version ready for publishing.

Rules:
- No em dashes.
- Keep the post polished and publication-ready.
- Do not invent claims.
- Keep the structure consistent with the brief.
```


### 06-shopify-publish.txt

```text
You are preparing structured data for Shopify article publishing.

Inputs:
- Final title: [INSERT TITLE]
- Body HTML or markdown: [INSERT BODY]
- URL handle: [INSERT HANDLE]
- Tags: [INSERT TAGS]
- Featured image URL or file name: [INSERT IMAGE]
- Publish date: [INSERT DATE OR NOW]
- Blog ID or blog handle: [INSERT BLOG]

Return:
1. A clean publish payload.
2. The fields that must be mapped to Shopify.
3. A short checklist for verifying the published article.
4. A fallback version if the image upload fails.

Rules:
- Use Shopify-friendly field names.
- Keep the output structured and easy to copy into automation.
```


### 07-weekly-report.txt

```text
You are an SEO analyst.

Analyze this blog post performance data and give improvement actions.

Inputs:
- Target keyword: [INSERT KEYWORD]
- URL: [INSERT URL]
- Publish date: [INSERT DATE]
- Impressions: [INSERT VALUE]
- Clicks: [INSERT VALUE]
- CTR: [INSERT VALUE]
- Average position: [INSERT VALUE]
- Organic sessions: [INSERT VALUE]
- Conversions: [INSERT VALUE]
- Notes: [INSERT NOTES]

Task:
1. Summarize performance.
2. Identify what is working.
3. Identify what is weak.
4. Recommend 3 actions to improve rankings or CTR.
5. Recommend whether to update, expand, re-optimize, or leave as is.
6. Return a simple decision: improve, monitor, or replace.

Keep the analysis practical and focused on SEO growth.
```


## Workflow map

### Weekly cycle

1. **Monday:** topic selection.
2. **Tuesday:** content brief.
3. **Wednesday:** draft generation.
4. **Thursday:** image creation and final review.
5. **Friday:** publish to Shopify.
6. **Next week:** track metrics and update the report.[^5_4][^5_5][^5_1]

### Data flow

```text
Business goal
→ keyword ideas
→ selected target keyword
→ SEO brief
→ article draft
→ image prompt
→ final article
→ Shopify publish
→ analytics tracking
→ decision log
→ next topic selection
```


## Suggested log columns

```text
week,publish_date,target_keyword,title,url,handle,tags,word_count,impressions,clicks,ctr,avg_position,organic_sessions,conversions,decision,next_action
```


## Implementation notes

Shopify’s article model supports immediate or scheduled publishing, URL handle customization, tags, images, and blog association, so your automation can handle the core publishing workflow cleanly. Shopify also emphasizes content freshness, content gaps, and ongoing SEO performance monitoring, which is why the tracking loop matters as much as the publishing loop.[^5_3][^5_7][^5_2][^5_1][^5_4]

I can turn this into a **single polished SOP PDF-style document** next, or I can write the **exact workflow in step-by-step checklist format** for your desktop.

<span style="display:none">[^5_10][^5_8][^5_9]</span>

<div align="center">⁂</div>

[^5_1]: https://www.shopify.com/blog/content-performance-tracking

[^5_2]: https://shopify.dev/docs/api/admin-graphql/latest/mutations/articleCreate

[^5_3]: https://shopify.dev/docs/api/admin-graphql/2026-04/mutations/articleCreate

[^5_4]: https://www.shopify.com/blog/seo-management

[^5_5]: https://www.shopify.com/blog/conversion-metrics

[^5_6]: https://www.shopify.com/blog/marketing-effectiveness-measurement

[^5_7]: https://shopify.dev/docs/api/admin-graphql/latest/queries/article

[^5_8]: https://shopify.dev/docs/api/admin-graphql/latest/objects/Article

[^5_9]: https://shopify.dev/docs/api/admin-graphql/latest/enums/MetafieldDefinitionPinnedStatus

[^5_10]: https://shopify.dev/docs/api/admin-graphql/latest/unions/MetafieldReference


---

# plss look at the prompt I found below and take whatever you can add to the plan

You are an SEO content strategist and conversion-focused copywriter for a Shopify store in the [NICHE] space. Your goal is to create a content plan and briefs that grow organic traffic AND revenue, not just rankings.

CONTEXT

- Store: [STORE NAME / URL]
- Primary goal: [e.g., increase organic revenue, improve conversion rate from organic, build top-of-funnel authority]
- Target audience: [describe ideal customer, location, pain points]
- Brand voice: [e.g., friendly, expert, no fluff, clear CTAs]

STRATEGY RULES

1. Customer journey first
    - Plan content for all stages of the buyer journey:
• Awareness: problem-aware, not solution-aware (educational, “what is”, “why”, “how to fix X”)
• Consideration: comparing solutions, “best X for Y”, “X vs Y”, “how to choose X”
• Decision: product-focused, “buying guide”, “review”, “is X worth it”, “X for [use case]”
• Post-purchase / retention: setup guides, troubleshooting, upgrades, complementary products
    - For each content idea, clearly label which journey stage it targets.
2. Keyword selection rules
    - Do NOT automatically prefer high search volume keywords.
    - Prioritize keywords with:
• Clear commercial or high-intent informational intent (e.g., “best”, “review”, “vs”, “for [use case]”, “how to choose”, “buy”, “price”, “worth it”)
• Lower search volume but strong conversion potential (long-tail, specific use cases, niche problems)
• Evidence of intent from Search Console queries and on-site behavior if provided.
    - When suggesting keywords, always include:
• Primary keyword
• 3–5 supporting/related keywords
• Intent type: informational / commercial / transactional
• Why this keyword can convert (1–2 sentences)
3. Use data-driven signals (when available)
    - If I provide Search Console data (queries, impressions, CTR, positions), use it to:
• Identify low-CTR but high-impression pages that need better titles/meta/content.
• Find queries already bringing sessions/conversions, even if volume is low, and create more content around them.
    - If I provide analytics (sessions, conversion rate, revenue by landing page), prioritize topics that support or expand on high-converting pages.
4. Content types and formats
    - For each journey stage, suggest a mix of:
• Blog posts / guides
• Collection/page copy improvements
• FAQ pages
• Comparison pages (“X vs Y”)
• Buying guides and “best X for Y” lists
• How-to and troubleshooting articles
• Post-purchase guides and cross-sell content
    - For each content piece, specify:
• Target stage (awareness/consideration/decision/post-purchase)
• Primary keyword + intent
• Secondary keywords
• Recommended format (guide, listicle, comparison, how-to, etc.)
• Suggested word count range
• Core CTA (e.g., “view collection”, “book consultation”, “add to cart”, “read related guide”)
5. On-page SEO requirements for every brief
    - Provide:
• SEO title (under ~60 characters, includes primary keyword, written for CTR)
• Meta description (under ~155 characters, includes primary keyword + clear benefit/CTA)
• Suggested H1
• H2/H3 outline with logical flow and keyword placement
• Internal linking suggestions: which existing pages/collections/products to link to and from
• Any schema opportunities (FAQ, HowTo, Product, Review) if relevant
    - Ensure content matches search intent better than current top results (more specific, more actionable, more tailored to [TARGET AUDIENCE]).
6. Conversion focus
    - For every content brief, include:
• Where in the journey this content fits
• What action the reader should take next
• Suggested internal CTAs and placement (early, mid, end)
• How this content supports revenue (direct sales, email capture, product discovery, trust-building)

TASK
Based on the above rules, do the following:

1. Propose a 90-day content plan with:
    - 10–20 content ideas mapped across awareness, consideration, decision, and post-purchase stages.
    - For each idea: title working draft, primary keyword, intent, journey stage, format, and why it can convert despite possibly low search volume.
2. For the top 3–5 ideas you recommend starting with, create detailed content briefs including:
    - SEO title, meta description, H1
    - Full H2/H3 outline
    - Primary and secondary keywords with intent
    - Internal linking plan (which pages to link to and from)
    - Suggested CTAs and where to place them
    - Notes on how to make this content clearly better than current top results for the target keyword.
3. Explicitly call out:
    - Which pieces target low-volume, high-intent keywords and why they’re valuable.
    - How the overall plan balances top-of-funnel traffic growth with bottom-of-funnel conversion.

If I provide any Search Console or analytics data in the next message, update your recommendations to:

- Favor topics and keywords already showing signs of traction (impressions, sessions, conversions).
- Identify quick-win pages to optimize for CTR and relevance before creating new content.

Yes. This prompt is much better than a generic “write me a blog post” prompt because it already bakes in buyer journey, intent, conversion, internal linking, and performance measurement. What I would add is a **content-cluster system, quick-win optimization rules, prioritization scoring, and a post-publish refresh loop** so the plan becomes revenue-driven, not just traffic-driven.[^6_1][^6_2][^6_3]

## What to add

### 1. Content clusters

Group topics into clusters around one core money page or collection, instead of treating each article as isolated. Shopify recommends internal link strategy because it helps search engines understand topical authority and improves rankings across related pages.[^6_4][^6_5]
Add a rule that every content idea must belong to one of these cluster types:

- Core money page support.
- Comparison support.
- Problem-solution support.
- Post-purchase support.
- FAQ/support content.


### 2. Priority scoring

Add a scoring model so the system chooses topics based on business value, not just keyword volume. I would score every idea from 1 to 5 on:

- Search intent strength.
- Conversion potential.
- Internal linking opportunity.
- Existing ranking traction.
- Content difficulty.
- Revenue relevance.[^6_3][^6_6][^6_1]

Then rank by total score and only push the top ideas into the brief stage.

### 3. Quick-win optimization

Before creating new content, the system should check Search Console and analytics for pages that already have impressions, sessions, or conversions but underperform on CTR or rankings. Shopify explicitly recommends using engagement, SEO, and conversion data to improve content performance and identify what to update.[^6_7][^6_6][^6_1]
Your plan should say:

- If a page has high impressions and low CTR, rewrite title and meta.
- If a page has rankings but weak engagement, expand content and improve internal links.
- If a page converts well, create adjacent support content around it.


### 4. Internal link map

The prompt is strong on internal linking, but I would make it more operational. For each brief, require:

- Link from at least 2 relevant existing pages into the new post.
- Link from the new post to 1 to 3 money pages or collections.
- Use descriptive anchor text.
- Ensure the post sits inside a cluster, not alone.[^6_5][^6_4]


### 5. Content refresh rules

Add a rule that old content gets refreshed on a schedule. Shopify’s SEO guidance emphasizes ongoing auditing, content structure, internal links, metadata, and measurement rather than one-time publishing.[^6_8][^6_9][^6_4]
A good refresh rule is:

- Review posts at 30 days and 90 days.
- Refresh low-CTR pages first.
- Update posts with new FAQs, examples, and internal links.


### 6. Conversion CTA mapping

The prompt already asks for CTAs, but I’d make them stage-specific:

- Awareness: read related guide, join email list.
- Consideration: compare products, view collection.
- Decision: add to cart, book call, check pricing.
- Post-purchase: setup guide, accessories, troubleshooting.[^6_2][^6_1][^6_3]


## Improved planning logic

Here is the planning logic I would add to your system:

```text
Step 1: Pull candidate topics from keyword tools, Search Console, analytics, and business priorities.
Step 2: Score each topic for revenue relevance, intent, ranking opportunity, and link potential.
Step 3: Classify each topic by buyer journey stage.
Step 4: Assign each topic to a content cluster and money page.
Step 5: Build briefs only for the highest-priority topics.
Step 6: After publishing, track performance by impressions, CTR, sessions, conversions, and assisted revenue.
Step 7: Refresh posts that show traction but underperform on CTR or conversions.
```


## Add this to the prompt

You can paste this into your master prompt under a new section called **PRIORITIZATION AND CLUSTER RULES**:

```text
PRIORITIZATION AND CLUSTER RULES
- Do not select topics based on search volume alone.
- Score each topic using: intent strength, conversion potential, current traction, internal linking opportunity, and revenue relevance.
- Assign every topic to a buyer journey stage and a content cluster.
- Before suggesting new content, check for quick-win pages with impressions, CTR issues, ranking potential, or conversion value.
- Prioritize updates to pages that already show traction before creating brand-new topics.
- Make sure every new article links to and from relevant money pages, collection pages, and support content.
- Ensure every brief includes a refresh plan for 30 days and 90 days after publication.
```


## Add this to the workflow

Your 90-day workflow should follow this order:

1. Audit existing content and pick quick wins.
2. Build cluster map around core money pages.
3. Select new content ideas by stage.
4. Create briefs for top-priority ideas.
5. Publish one or two pieces per week.
6. Track performance by keyword, page, and cluster.
7. Refresh and interlink winners.
8. Retire or merge weak content.

## Why this makes the plan stronger

This approach turns your blog into a **growth system** instead of a publishing habit. Shopify’s guidance on content analytics, SEO management, and ecommerce audits all point toward the same idea: track what matters, improve what already has traction, and build authority through structured internal linking and consistent measurement.[^6_6][^6_10][^6_7][^6_4][^6_5]

If you want, I can now rewrite your prompt into a **single upgraded master prompt** with all these additions integrated cleanly.

<span style="display:none">[^6_11]</span>

<div align="center">⁂</div>

[^6_1]: https://www.shopify.com/blog/content-metrics

[^6_2]: https://www.shopify.com/enterprise/blog/ecommerce-content-strategy

[^6_3]: https://www.shopify.com/blog/content-marketing-tips

[^6_4]: https://www.shopify.com/blog/ecommerce-seo-audit

[^6_5]: https://www.shopify.com/blog/seo-checklist-online-store

[^6_6]: https://www.shopify.com/blog/content-marketing-analytics

[^6_7]: https://www.shopify.com/blog/content-performance-tracking

[^6_8]: https://www.shopify.com/blog/technical-seo-audit

[^6_9]: https://www.shopify.com/blog/seo-campaign

[^6_10]: https://www.shopify.com/blog/seo-management

[^6_11]: https://www.shopify.com/enterprise/blog/ecommerce-site-audit


---

# Yes please. I want to make sure that whatever AI agent is running this, it should understand the business it is working for so that we can still filter that into whatever we are creating (to just make things more personalised rather than just taking information online). I believe you understand. Tap and write. Might be similar to other competitors but they still have what makes them unique so we want to always follow that. I expect it to first understand the site, understand the product they offer, and the way it was designed so we can always personalise content whenever and wherever possible.

Absolutely. What you need is not just a prompt that writes content, but a **brand-aware content operating system** that first learns the business, the site structure, the products, the audience, and the unique design/positioning before it creates anything. Shopify’s own SEO and content guidance emphasizes aligning content with business goals, doing content audits, mapping keywords to the right pages, improving product-page specificity, and tracking performance over time.[^7_1][^7_2][^7_3][^7_4]

## Upgraded master prompt

Copy this as your new master prompt:

```text
You are an SEO content strategist, conversion-focused copywriter, and brand analyst for a Shopify store.

Your first job is to understand the business deeply before creating anything.

PHASE 1: BUSINESS UNDERSTANDING
Before writing, analyze and summarize:
1. Store identity
   - What the store sells
   - What problem it solves
   - Who it serves
   - What category it belongs to
   - What makes it different from competitors

2. Product understanding
   - Main products or collections
   - Bestsellers or priority offers
   - Price positioning
   - Key features, benefits, and use cases
   - Common objections or purchase barriers

3. Brand and site understanding
   - Brand voice and personality
   - Visual style and design direction
   - Site structure and navigation
   - Key pages, collections, and conversion points
   - Existing content themes and messaging patterns

4. Business goals
   - Primary revenue goal
   - SEO goal
   - Conversion goal
   - Audience growth goal
   - Retention or upsell goal

5. Competitive positioning
   - What the business shares with competitors
   - What makes it unique
   - What angles or messages should be emphasized
   - What should be avoided because it sounds generic

Only after this understanding is clear should you create content.

PHASE 2: CONTENT STRATEGY RULES
- Do not create generic content.
- Always personalize ideas to the business, product, audience, and site structure.
- Prefer content that reflects the store’s actual offers, voice, and customer problems.
- Use competitors as reference points, but always preserve and highlight the store’s unique value.
- Map every topic to the buyer journey:
  Awareness, Consideration, Decision, or Post-purchase.
- Prioritize keywords with strong intent and revenue relevance, not just volume.
- Use data from Search Console, analytics, product performance, and existing site content whenever available.
- Before suggesting new content, identify quick-win pages already showing traction.
- Make sure each idea connects to a relevant money page, collection, product, or support page.
- Avoid keyword stuffing and avoid writing like a template.
- No em dashes.

PHASE 3: PLANNING TASK
Based on the business understanding, create a 90-day content plan with 10 to 20 ideas.

For each idea include:
- Working title
- Primary keyword
- Supporting keywords
- Intent type
- Journey stage
- Format
- Why it can convert
- Related product/collection/page to link to
- Suggested CTA
- Priority score from 1 to 10

Also highlight:
- Low-volume, high-intent keywords
- Quick-win optimization opportunities
- Existing pages that should be refreshed before creating new content
- Content clusters that support core money pages

PHASE 4: BRIEF CREATION TASK
For the top 3 to 5 ideas, create detailed content briefs.

For each brief include:
- SEO title
- Meta description
- Suggested H1
- Full H2/H3 outline
- Primary and secondary keywords
- Search intent
- Journey stage
- Internal linking plan
- CTA placement suggestions
- Schema opportunities
- Notes on how to make the content better than current top results
- Specific personalization notes tied to the business, products, audience, or brand

PHASE 5: OUTPUT RULES
- Be specific, strategic, and business-aware.
- Use plain language.
- Be practical and actionable.
- Make sure the plan balances traffic growth with revenue growth.
- Always include one section called "Business Understanding" before the content plan.
- Always include one section called "What Makes This Brand Unique" where you call out positioning, tone, product strengths, or design cues that should be reflected in content.
- If data is provided, use it to adjust priorities and recommend quick wins.
- If data is not provided, make reasonable strategic assumptions and say what should be validated next.

OUTPUT FORMAT
1. Business Understanding
2. What Makes This Brand Unique
3. 90-Day Content Plan
4. Top Priority Briefs
5. Quick-Win Optimizations
6. Recommended Content Clusters
7. Next Actions

Write as if you are building a real content system for a Shopify brand, not just generating blog posts.
```


## Why this version is stronger

This version forces the AI to **learn the business first**, which is exactly what you asked for. It pushes the agent to understand products, site structure, design cues, audience pain points, and competitive positioning before it starts producing content, so the output feels personalized instead of scraped from the internet.[^7_2][^7_5][^7_1]

## Add this short rule block

You should also add this near the top as a permanent instruction:

```text
PERSONALIZATION RULE
Every recommendation must be tailored to the store’s actual products, collections, audience, brand tone, and site structure. If a suggestion could apply to any store, rewrite it until it clearly fits this specific brand.
```


## Add this for competitor handling

```text
COMPETITOR RULE
Use competitors only to identify market patterns, not to copy them. If competitors share similar offers, emphasize what makes this store unique in positioning, product value, voice, design, bundles, use cases, or audience focus.
```


## Add this for site-first thinking

```text
SITE-FIRST RULE
Before suggesting new content, analyze the website structure and determine:
- which product or collection pages need support,
- which pages are already strong and should receive internal links,
- which pages have quick-win SEO potential,
- and which content gaps align with current business priorities.
```


## Add this for data-driven prioritization

```text
DATA PRIORITY RULE
If Search Console or analytics data is available, prioritize:
- pages with high impressions but low CTR,
- queries already generating conversions,
- landing pages with strong engagement,
- and pages closest to revenue.
Create new content only after quick-win optimization opportunities are reviewed.
```


## Simple operating principle

The agent should always work in this order:

1. Understand the store.
2. Understand the products.
3. Understand the audience.
4. Understand the site structure.
5. Understand the competitive landscape.
6. Find quick wins.
7. Build the content plan.
8. Write the briefs.
9. Optimize for SEO and conversion.
10. Track and refine.[^7_3][^7_4][^7_5][^7_2]

I can now turn this into a **final master prompt pack** with:

- one version for strategy,
- one for briefs,
- one for publishing,
- and one for weekly optimization.

<span style="display:none">[^7_10][^7_6][^7_7][^7_8][^7_9]</span>

<div align="center">⁂</div>

[^7_1]: https://www.shopify.com/blog/ecommerce-seo-audit

[^7_2]: https://www.shopify.com/ca/blog/content-audit

[^7_3]: https://www.shopify.com/blog/seo-goals

[^7_4]: https://www.shopify.com/blog/content-performance-tracking

[^7_5]: https://www.shopify.com/blog/cro-checklist

[^7_6]: https://www.shopify.com/enterprise/blog/ecommerce-site-audit

[^7_7]: https://www.shopify.com/blog/seo-management

[^7_8]: https://www.shopify.com/enterprise/blog/enterprise-seo

[^7_9]: https://help.shopify.com/en/manual/promoting-marketing/seo/seo-overview

[^7_10]: https://www.shopify.com/blog/site-audit


---

# Yeah, so does this include a backlink outreaching for link building and everything like that?

Yes, and it should. The system you’re building should include **off-page SEO**, meaning backlink outreach, partner mentions, guest posts, digital PR, and linkable content assets, not just blog creation and publishing [^8_1][^8_2][^8_3]. Shopify SEO guidance also points to broader SEO management, content strategy, and performance monitoring, which fits a workflow that combines on-page content with authority building [^8_4][^8_5][^8_6].

## How to add it

Add a new module to the automation called **Link Building and Outreach**. It should sit after content planning, because the content plan determines what assets you can pitch externally, and before weekly reporting, because outreach results should influence future priorities [^8_5][^8_2][^8_7].

### The outreach module should do four things

- Find link opportunities.
- Create linkable assets.
- Prepare outreach targets and pitches.
- Track replies, placements, and acquired links [^8_8][^8_3][^8_7].


## What the AI should understand

The agent should not treat backlinks as random SEO tasks. It should understand:

- Which pages are **money pages** and deserve links.
- Which blog posts are **linkable assets**.
- Which competitors or adjacent brands are getting links.
- Which suppliers, partners, directories, and communities fit the store [^8_2][^8_9][^8_3].

That makes link building more strategic and more personalized to the business.

## Updated master prompt block

Add this section to your master prompt:

```text
OFF-PAGE SEO AND LINK BUILDING RULES
- Include backlink outreach and authority-building in the SEO strategy.
- Do not focus only on on-page content.
- Identify linkable assets the store can create, such as original research, data reports, guides, checklists, comparisons, calculators, templates, and product-use resources.
- Recommend backlink opportunities from:
  - suppliers and manufacturers,
  - partners and vendors,
  - relevant niche blogs,
  - comparison and review sites,
  - resource pages,
  - industry directories,
  - community websites,
  - journalists and publications,
  - unlinked brand mentions,
  - guest posts,
  - broken link replacements,
  - digital PR placements.
- Prioritize outreach opportunities that are relevant to the niche and the store’s actual offers.
- Use competitor backlink patterns as inspiration, not as copy.
- Track outreach status, live links earned, anchor text, target page, and referral traffic.
- Tie every outreach target to a specific page, keyword cluster, or business goal.
```


## Add this outreach workflow

```text
1. Identify priority pages that need authority.
2. Create or select a linkable asset.
3. Build an outreach list by category.
4. Draft personalized pitches.
5. Send outreach.
6. Track replies and live links.
7. Measure referral traffic and ranking impact.
8. Feed results back into the content plan.
```


## Recommended outreach targets

For a Shopify brand, the system should look at:

- Supplier or manufacturer partner pages.
- Authorized retailer directories.
- Niche blog guest posts.
- Product review sites.
- Resource pages.
- Industry associations.
- Relevant newsletters.
- Community or event pages.
- “Best of” roundups.
- Journalist requests.
- Broken link opportunities [^8_2][^8_9][^8_3].


## Best content for link building

The content plan should deliberately create assets that people want to reference:

- Original research.
- Survey results.
- Comparison guides.
- Stats pages.
- Buying guides.
- Troubleshooting hubs.
- Calculators.
- Checklists.
- Templates.
- “How to choose” resources [^8_8][^8_10][^8_7].


## What to track

The outreach system should track:

- Prospect domain.
- Contact person.
- Outreach date.
- Pitch angle.
- Target page.
- Link status.
- Live URL.
- Anchor text.
- Referral traffic.
- Ranking movement after link acquisition [^8_2][^8_3][^8_7].


## Bottom line

So yes, backlink outreach should absolutely be part of the plan. The smartest version is not “content first, backlinks later” in a vague way, but a unified system where content, linkable assets, internal linking, and outreach all support the same business goals [^8_4][^8_5][^8_2].

I can now fold this into your **final master prompt** and give you a single complete version that includes:

- brand understanding,
- content planning,
- brief creation,
- publishing,
- analytics,
- and backlink outreach.

<span style="display:none">[^8_11][^8_12][^8_13]</span>

<div align="center">⁂</div>

[^8_1]: https://www.outreachlabs.com/seo/backlink/link-building/ecommerce/

[^8_2]: https://www.thespearpoint.com/blog/seo-for-shopify-complete-guide

[^8_3]: https://www.obsessai.com/guides/ecommerce-link-building

[^8_4]: https://www.shopify.com/blog/seo-management

[^8_5]: https://www.shopify.com/blog/ecommerce-seo-audit

[^8_6]: https://www.shopify.com/blog/content-performance-tracking

[^8_7]: https://www.braincuber.com/tutorial/shopify-seo-management-complete-guide

[^8_8]: https://easyappsecom.com/guides/shopify-backlink-strategy

[^8_9]: https://www.obsessai.com/guides/shopify-seo-checklist

[^8_10]: https://craftshift.com/shopify-seo-checklist-2026/

[^8_11]: https://www.launchtip.com/blog/how-to-add-backlinks-to-your-shopify-store-a-complete-guide

[^8_12]: https://seology.ai/blog/link-building-shopify-2026-strategy

[^8_13]: https://logeix.com/shopify-seo/link-building

