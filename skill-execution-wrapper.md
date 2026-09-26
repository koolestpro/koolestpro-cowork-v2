# Skill Execution Wrapper

This file defines how the local `.js` scripts execute Claude skills inside this repo.

The goal is simple:

- Skills are the source of truth for generation logic.
- Scripts provide runtime context, file IO, and pipeline updates.
- The content pipeline and content system read from the same synced data.

## Core Rule

No generator script should ship content from a hardcoded prompt alone.

Every content script must:

1. Load the skill path from `cowork_config.json`.
2. Read the skill file from `skills/`.
3. Append `AUTOMATION RUNTIME` context.
4. Pass task-specific inputs and strict output rules.
5. Save the result into the correct output folder.
6. Update `pipeline_data.json`.
7. Sync the embedded data inside:
   - `content_pipeline.html`
   - `ridwan_content_system_updated.html`

## Runtime Files

- `cowork_config.json`
  Central registry for skill paths, output folders, and sync targets.

- `lib/cowork_runtime.js`
  Shared runtime for config loading, skill execution, pipeline IO, and date helpers.

- `lib/view_sync.js`
  Pushes the latest pipeline payload into both HTML files through the embedded JSON block.

## Wrapper Contract

Every wrapper follows this shape:

```js
const result = await executeSkill({
  skillPath: "skills/...",
  contextLabel: "run_x.js stage name",
  inputs: {
    Topic: "...",
    Notes: "...",
    "Template reference": "..."
  },
  instructions: `
Run in non-interactive automation mode.
Use the provided inputs as the source of truth.
  `,
  outputRules: [
    "Return markdown only.",
    "Do not ask follow-up questions."
  ],
  maxTokens: 7000
});
```

## Script Mapping

### `run_ideas.js`

Skill:
- `skills/koolestpro_idea_generator_skill.md`

Wrapper behavior:
- Sends current month, topic, prior titles, and known monthly sets.
- Expects a JSON array only.
- Writes:
  - `outputs/ideas/ideas_YYYY-MM.json`
  - `outputs/ideas/ideas_YYYY-MM.html`
- Registers the month inside `pipeline_data.json`.
- Pushes all monthly ideas into the pipeline with:
  - `month`
  - `monthSlug`
  - `source: "monthly-ideas"`

### `run_tip.js`

Skill:
- `skills/koolestpro_content_engine_final.md`

Wrapper behavior:
- First pass: asks for the written content package in markdown.
- Second pass: asks the same skill to render the final HTML using `templates/tips.html` as a structural reference.
- Writes:
  - `outputs/tips/{slug}_{date}.md`
  - `outputs/tips/{slug}_{date}.html`
- Adds the created Tip item to the pipeline.

### `run_cro_fix.js`

Stack:
- `skill_A_store_auditor.md`
- `skill_B_store_rebuilder_v2.md`
- `skill_D_caption_writer.md`
- `skill_E_cro_content_maker.md`

Wrapper behavior:
- Runs the CRO stack in order.
- Supports text-only automation when screenshots are missing.
- Writes:
  - `audit_brief.md`
  - `rebuild.html`
  - `captions.md`
  - `content_pack.html`
- Adds the created CRO Fix item to the pipeline.

## Embedded Sync Contract

Both HTML files contain this marker block:

```html
<!-- COWORK_SYNC_DATA_START -->
<script id="cowork-sync-data" type="application/json">...</script>
<!-- COWORK_SYNC_DATA_END -->
```

`lib/view_sync.js` replaces only that block.

This means:

- The dashboard always sees the latest monthly idea data.
- The content system idea bank always sees the same monthly idea data.
- The HTML files remain editable without rebuilding the whole page.

## Data Shape

`pipeline_data.json` now stores:

```json
{
  "meta": {
    "version": "3.0.0",
    "updatedAt": "ISO string",
    "syncHash": "short hash"
  },
  "months": {
    "2026-04": {
      "label": "April 2026",
      "topic": "Shopify CRO",
      "htmlPath": "outputs/ideas/ideas_2026-04.html",
      "jsonPath": "outputs/ideas/ideas_2026-04.json",
      "generatedAt": "ISO string",
      "totalIdeas": 15
    }
  },
  "items": []
}
```

## Automation Rules

- Skills must support non-interactive automation mode.
- Scripts must not wait for approval mid-run.
- Missing screenshots do not block the CRO stack.
- Monthly ideas are canonical for the pipeline.
- The content system is a view over synced pipeline data, not a separate idea source.

## If You Add New Scripts

Use the same pattern:

1. Add the skill path to `cowork_config.json`.
2. Add the runtime wrapper in the new script.
3. Save outputs into `outputs/...`.
4. Update `pipeline_data.json`.
5. Call `syncEmbeddedViews(savedPipeline)`.

