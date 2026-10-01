# Stage 7: Finalize for Shopify

**Inputs:** `article.md` (humanized), `brief.md`, `image.json`, snapshot, `client.json` (blog handle, author).
**Outputs:** `runs/<date>/body.html`, `runs/<date>/publish.json`

---

You are preparing this article for Shopify.

1. Convert `article.md` to clean semantic HTML for the article body: `<h2>`, `<h3>`, `<p>`, `<ul>/<ol>`, `<table>`, `<a href>`, `<strong>`. **Do not include the H1** (Shopify renders the title as H1). No inline styles, no `<div>` wrappers, no classes.
2. Internal links: absolute paths (`/collections/nfc-cards`). Check each one against the snapshot. Remove or replace any that don't exist.
3. External links: add `target="_blank" rel="noopener"`.
4. Append FAQPage JSON-LD (`<script type="application/ld+json">`) built from the FAQ section. Add HowTo JSON-LD if the brief asked for it.
5. Write `publish.json`:
   - `title` (= H1), `handle`, `seo_title` (≤ 60), `seo_description` (≤ 155)
   - `summary_html`: 1 to 2 sentence excerpt in `<p>`
   - `tags`: 3 to 6, from the cluster + product type (use the existing blog's tag style if it has one)
   - `author`, `blog_handle` from client.json
   - `image_url`, `image_alt` from image.json
   - `primary_keyword`, `cluster`, `stage`, `word_count`
6. **QA gate.** Report pass/fail for each check:
   - em dash count = 0 in both files
   - seo_title ≤ 60, seo_description ≤ 155
   - keyword in title, first 100 words, ≥ 1 H2, conclusion
   - every internal href exists in the snapshot
   - every number, price or claim traces to the profile or a cited source
   - word count within the brief's range
   - valid JSON-LD (parse it)
   If anything fails, fix it and re-run the gate. Don't hand over until everything passes.

---

## Platform `nextjs-resources` (koolestpro.com)

Skip `body.html` / `publish.json`. Write `runs/<date>/article.json`, one object matching the site's `Article` type in `content/resources.ts`:

```json
{
  "slug": "lowercase-hyphenated",
  "title": "≤ 60 chars, used as <title>",
  "h1": "short on-page heading",
  "description": "70 to 155 chars, used as meta description",
  "targetQuestion": "the exact question this page answers",
  "updated": "YYYY-MM-DD",
  "readingMinutes": 6,
  "pricesCheckedOn": "Month YYYY (only if prices are mentioned)",
  "blocks": [{"type": "p", "text": "..."}, {"type": "h2", "text": "A question a person would type?"}],
  "faq": [{"q": "...", "a": "..."}],
  "cta": {"text": "one sentence", "href": "/services/page-build", "label": "button label"}
}
```
Block types allowed: `p`, `h2`, `h3`, `ul` (`items`), `table` (`head`, `rows`), `callout` (`title`, `text`), `verdict` (`pick`, `text`). Text is plain: no markdown, no HTML. Inline links aren't supported yet, so put internal-link suggestions in a `callout` and in `notes.md`. Every `h2` is a question, and the next `p` answers it in under 40 words. The site renders Article + FAQPage JSON-LD itself, so don't add schema.
Then run `python3 seo/tools/site_publish.py --client <slug> --run <run> --dry-run`. It enforces the QA gate (unique slug, lengths, em dashes, real CTA route).
