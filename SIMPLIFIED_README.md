# Koolestpro Cowork v2 — Simplified Setup

You generate content with simple commands. The dashboard tracks everything. Monthly ideas, created outputs, and the content system stay synced through the local pipeline data.

---

## What Changed from v1

| Old (v1) | New (v2) |
|---|---|
| Tries to query external databases | Uses local pipeline data and synced HTML views |
| Weekly automation script | 3 simple commands: `ideas`, `tip`, `cro` |
| Complex config + workflow files | One HTML dashboard you open in browser |
| Per-week idea generation | Once-a-month idea generation |

---

## Installation (drop into your existing master folder)

The files in this download go into your existing `koolestpro-cowork` folder. They **add** new functionality — they don't replace anything in v1.

**Files to drop in:**
```
koolestpro-cowork/
├── run_ideas.js              ← NEW — monthly idea generator
├── run_tip.js                ← NEW — Tip carousel generator
├── run_cro_fix.js            ← NEW — CRO Fix content generator
├── content_pipeline.html     ← NEW — your dashboard
├── package.json              ← REPLACE the old one
├── SIMPLIFIED_README.md      ← this file
└── outputs/                  ← auto-created when you run a script
    ├── cro-fixes/
    ├── tips/
    └── ideas/
└── skills/                  ← auto-created when you run a script
    └── cro-skill-stack/
       ├── skill_A_store_auditor.md
       ├── skill_B_store_rebuilder_v2.md
       ├── skill_D_caption_writer.md
       ├── skill_E_cro_content_maker.md
    ├── koolestpro_idea_generator_skill.md
    └── koolestpro_content_engine_final.md
```

The old v1 files (`cowork_run_weekly.js`, `cowork_config.json`, `WORKFLOW.md`, etc.) can stay — you can ignore them or delete them. They don't interfere.

---

## Setup (3 minutes)

```bash
cd ~/Downloads/koolestpro-cowork

# 1. Make sure dependencies are installed (one-time)
npm install

# 2. Confirm your API key is set
echo $ANTHROPIC_API_KEY
# (should print sk-ant-...)

# 3. Open the dashboard once to initialize it
open content_pipeline.html
```

That's it. No config files to edit.

---

## The Three Commands

### 1. Generate monthly ideas (run once a month)

```bash
npm run ideas
```

You'll be prompted for a focus topic (or press Enter for general).
Generates **15 ideas** mixing Tips, CRO Fixes, Case Studies, and Personal posts.

**Outputs:**
- `outputs/ideas/ideas_2026-04.html` — visual review file (open in browser)
- `outputs/ideas/ideas_2026-04.json` — raw data
- All ideas auto-added to `pipeline_data.json` with status "Idea"

### 2. Generate a Tip post

```bash
npm run tip
```

Prompts for the tip idea + angle. Generates an 8-slide carousel + 5 caption formats.

**Outputs:**
- `outputs/tips/{slug}_2026-04-22.html` — full carousel + caption tabs (open in browser, copy-to-clipboard buttons)
- `outputs/tips/{slug}_2026-04-22.md` — markdown source
- Auto-added to dashboard with status "Created"

### 3. Generate a CRO Fix post

```bash
npm run cro
```

Prompts for store name, URL, and any initial notes. Generates 3 files:

- `outputs/cro-fixes/{store-slug}/audit_brief.md` — full audit
- `outputs/cro-fixes/{store-slug}/captions.md` — 6 caption formats
- `outputs/cro-fixes/{store-slug}/content_pack.html` — annotation table + 6-slide carousel + caption tabs
- Auto-added to dashboard with status "Created"

---

## The Dashboard

Open `content_pipeline.html` in your browser. It runs entirely locally — no server, no internet needed (except Google Fonts).

### What you can do:

**This Week tab** — 3 slots: Monday (Tip), Wednesday (CRO Fix), Friday (Case Study/Personal). Click "Nominate from ideas" to pick from your idea pool.

**Monthly Ideas tab** — Grid of all this month's ideas. Filter by type or priority. Search by keyword. Click any card to edit. Click "Advance" to move it through statuses.

**Pipeline tab** — Kanban board with 5 columns: Idea → Nominated → Created → Scheduled → Published. Drag cards between columns to update status.

**Archive tab** — Everything you've published, grouped by month.

### Footer actions (always visible):

- **+ Add Item** — Manually add a content piece
- **Import JSON** — Paste your `pipeline_data.json` to load data the scripts saved
- **Copy Export** — Generate copy-paste text for Cowork or your own content log
- **Download Backup** — Save your dashboard data as JSON

---

## The Sync: Scripts ↔ Dashboard

The scripts write to `pipeline_data.json` in your project folder.
The dashboard stores everything in your browser's localStorage.

**To sync script-generated items into the dashboard:**

1. After running `npm run ideas` (or `tip` or `cro`), open `pipeline_data.json` in any text editor
2. Copy the entire contents
3. Open the dashboard → click "Import JSON" → paste → click "Import & Replace"

> Heads up: "Import & Replace" overwrites the dashboard's current state. Click "Download Backup" first if you've made dashboard-only edits you want to keep.

This keeps the two in sync. (Alternative: just use the dashboard's "+ Add Item" if you'd rather track content manually after generating it.)

---

## Your Weekly Rhythm

**Once a month (e.g. first Monday):**
```bash
npm run ideas
```
Then: open dashboard → import the new ideas → review them in the Monthly Ideas tab → mark the best ones as "Nominated" by dragging them or clicking Advance.

**Every Monday:**
1. Open dashboard → This Week tab
2. Look at Monday slot. If empty, click "Nominate from ideas" → pick a Tip
3. Run `npm run tip` with that idea → generates the carousel
4. Open the generated HTML, copy captions, paste into LinkedIn/Twitter
5. In dashboard, click "Advance" on the item → moves to Scheduled
6. After posting → click "Advance" again → Published

**Every Wednesday:** Same flow but for CRO Fix → `npm run cro`.

**Every Friday:** Manual — work on Case Study or Personal post yourself. Add it to the dashboard via "+ Add Item" so it's tracked.

**End of week:** Open dashboard → "Copy Export" → "Nominated this week" → copy into Cowork, your tracker, or your archive.

---

## Troubleshooting

**`Error: API 400` when running scripts**
The model name in the scripts is `claude-sonnet-4-5`. If that errors, edit the script files and try `claude-sonnet-4-20250514` or check your account for the latest available model.

**Dashboard data disappeared**
Browser localStorage is per-domain and cleared if you clear browsing data. Always click "Download Backup" weekly. Restore via "Import JSON".

**`pipeline_data.json` doesn't exist yet**
That's fine — it's created the first time you run a script. The dashboard works without it (it has its own localStorage).

**Generated HTML looks wrong**
The scripts ask Claude to build the HTML each time. If a generation comes out off-brand, just re-run the command. You can also edit any generated HTML directly — they're plain files.

---

## File Reference

| File | What it does |
|---|---|
| `run_ideas.js` | Monthly idea generator |
| `run_tip.js` | Tip post (8-slide carousel + captions) |
| `run_cro_fix.js` | CRO Fix (audit + captions + content pack) |
| `content_pipeline.html` | Dashboard you open in browser |
| `pipeline_data.json` | Created by scripts, imports into dashboard |
| `outputs/ideas/` | Monthly idea HTML files |
| `outputs/tips/` | Generated tip carousels |
| `outputs/cro-fixes/{store}/` | One folder per CRO project |
| `package.json` | npm commands |

---

## What this does NOT do

- ❌ Depend on Notion directly
- ❌ Auto-post to social media (you post manually)
- ❌ Generate images for slides (HTML carousels render in browser; for IG you screenshot or rebuild in Figma)
- ❌ Run on a schedule (you run commands when you need them)

This is a **content generation + tracking system**, not a publishing bot. Which is exactly what you asked for.
