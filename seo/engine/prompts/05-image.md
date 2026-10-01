# Stage 6: Featured image

**Inputs:** `article.md`, brief image direction, `snapshot/products.json`, profile visual style.
**Output:** `runs/<date>/image.*`, `image.json` `{ "source": "store|generated", "url": "", "alt": "", "prompt": "" }`

---

1. **Real photo first.** Look through the snapshot's product images for the exact product the article is about (or the closest one). It must be a clean, well-lit image, ideally landscape or easy to crop. If one fits, use its Shopify CDN URL (add `&width=1600`) as `url`, and set `source: store`.
2. **Generate only if no real photo fits.** Use the `gpt-image` skill. Write a prompt in this shape:
   - Scene: the customer's real setting (e.g. a salon reception counter, a café table, a car dealership desk), with the product type in use.
   - Style: the profile's visual style and colours, photoreal, natural light, landscape 3:2.
   - No text, no logos, no fake brand marks, no recognisable faces.
   Upload the result to Cloudinary (`koolestpro/seo/<slug>/<handle>`) and use the secure URL. Set `source: generated`.
3. **Alt text:** describe what's in the image, including the primary keyword only if it fits naturally. ≤ 125 chars.
4. Never recreate the client's logo or product packaging in a generated image.
