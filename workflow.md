# Workflow

This is the working flow for Cowork + Claude inside this repo.

## System Overview

There are four layers:

1. `skills/`
   Contains the instructions Claude should follow.

2. `.js` scripts
   Execute skills, save outputs, and update the pipeline.

3. `pipeline_data.json`
   Canonical shared data store for monthly ideas and generated content items.

4. HTML views
   - `content_pipeline.html`
   - `ridwan_content_system_updated.html`

Both HTML files are synced from the same embedded JSON payload.

## Monthly Workflow

### 1. Generate Monthly Ideas

Run:

```bash
npm run ideas
```

What happens:

- `run_ideas.js` loads the Idea Generator skill.
- Claude returns a JSON array of monthly ideas.
- The script writes the monthly idea files.
- The month is registered in `pipeline_data.json`.
- Both HTML views are synced.

Outputs:

- `outputs/ideas/ideas_YYYY-MM.json`
- `outputs/ideas/ideas_YYYY-MM.html`

### 2. Review Monthly Ideas

Open either:

- `content_pipeline.html`
- `ridwan_content_system_updated.html`

Use:

- The pipeline dashboard for nomination and status tracking.
- The content system for month-grouped browsing and direct links to each monthly idea interface.

### 3. Generate a Tip

Run:

```bash
npm run tip
```

What happens:

- The Content Engine skill writes the markdown content package.
- The same skill renders the final HTML using the tips template as reference.
- The new Tip is added to the pipeline with status `Created`.
- Both HTML views are synced.

### 4. Generate a CRO Fix

Run:

```bash
npm run cro
```

What happens:

- Skill A creates the audit brief.
- Skill B creates the rebuild HTML.
- Skill D writes the caption pack.
- Skill E creates the final content pack.
- The new CRO Fix is added to the pipeline with status `Created`.
- Both HTML views are synced.

## Pipeline Status Flow

Every content item moves through:

`Idea -> Nominated -> Created -> Scheduled -> Published`

Rules:

- Monthly ideas enter as `Idea`.
- Generated Tip and CRO outputs enter as `Created`.
- Manual changes inside the dashboard are stored locally in browser storage.
- Fresh script syncs replace old local state when the pipeline hash changes.

## Monthly Idea Rule

The pipeline now works from monthly idea sets, not a flat one-off list.

That means:

- Every idea should have `month` and `monthSlug`.
- Each month can link to its own `outputs/ideas/ideas_YYYY-MM.html`.
- The content system idea bank must show ideas grouped by month.
- The pipeline dashboard must keep those month groups visible and navigable.

## Content System Rule

`ridwan_content_system_updated.html` is no longer a separate manually curated idea bank.

It is now:

- A brand system reference.
- A month-sorted view over synced pipeline ideas.
- A launcher to:
  - the pipeline dashboard
  - the monthly idea interfaces
  - the next idea-generation run

## No Notion Dependency

This version does not depend on Notion.

Do not build new automation around:

- Notion sync
- Notion MCP
- Notion database IDs

If export text is needed, it should remain generic and reusable in Cowork or any external system.

## Adding New Content Types

If you add a new generator such as `case-study.js` or `personal.js`:

1. Add the skill path to `cowork_config.json`.
2. Create the runtime wrapper in the new script.
3. Save outputs under `outputs/`.
4. Add the generated item to `pipeline_data.json`.
5. Sync both HTML files.

## Debug Checklist

If the system drifts:

1. Check `cowork_config.json` paths.
2. Check the embedded sync block in both HTML files.
3. Check `pipeline_data.json` for `months`, `items`, and `syncHash`.
4. Check that the script called `syncEmbeddedViews(...)`.
5. Check that the skill supports automation mode and the expected output format.
