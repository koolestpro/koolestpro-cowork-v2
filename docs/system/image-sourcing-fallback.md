## 📸 NO IMAGE CREDITS — PROMPT-PACK HANDOFF (project-wide)

Applies to every stream that generates images (static ads, store-template product shots, rebuild hero images, carousel cover visuals).

**Static Ads: the prompt pack IS the default (2026-09-18).** Static Ad runs never call a paid image API unless Ridwan asks for generated images in that request ("generate the images", "use the API"). The default run researches, writes the copy, and exports the prompt pack below; Ridwan runs it in ChatGPT and sends the images back. Static ads were the main OpenAI spend.

**Every other stream: fallback order (2026-09-18).**
1. `gpt-image` (OpenAI) if it has credits.
2. **Cloudinary `generate-image`** (MCP, free plan: 50 generations per month, models include nano-banana, FLUX, Ideogram, Recraft, gpt-image). Check `get-usage-details` → `image_generation.usage < limit` first. It was 50/50 on 2026-09-18.
3. For rebuild hero images only: the page builder's own image generation (Lovable/Figma Make), which spends builder credits, not OpenAI.
4. Otherwise a **prompt pack**. Never silently spend on another paid service (inference.sh only if Ridwan names it). Stock (Pexels/Pixabay/Unsplash) is fine for backgrounds and scenes, never as a stand-in for a real product.

**Write `.ai-workflow/pending-{stream}-{slug}.md`** containing: the block detail/error + keys tried; target/product selection and why; the research table (every real, traceable claim + source); the prompts verbatim/copy-paste ready (self-contained fenced block per image, size + intended filename above each, "reading exactly:" quoting); the captions (humanizer-checked); a "still to do on return" checklist with pipeline constants. Then present the file in chat.

**Register nothing until real files exist.** On a blocked run: no pipeline record, no `usedFor`, no social-content pair, delete the empty `outputs/` folder. Say plainly nothing shipped. Do not improvise a renderer or let PIL draw ad copy.

**Ingesting when Ridwan returns the exports:** save images to the real output folder under the exact filenames; look at every image before accepting; assemble derived assets (2x2 showcase + size-checked `-x` for X); build `index.html`; register what was skipped (status `Created`, `usedFor`, social-content pair); present `index.html`; delete the pending file. Note in the record that images were produced manually via ChatGPT.
