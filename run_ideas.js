#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const {
  buildProjectSystemPrompt,
  ensureDir,
  executeSkill,
  extractJsonArray,
  getCurrentMonthLabel,
  getCurrentMonthSlug,
  loadConfig,
  loadPipelineData,
  registerMonth,
  resolveFromRoot,
  savePipelineData,
  slugify
} = require('./lib/cowork_runtime');
const { syncEmbeddedViews } = require('./lib/view_sync');

function parseArgs() {
  const args = {};
  process.argv.slice(2).forEach(arg => {
    const match = arg.match(/^--(\w+)=(.+)$/);
    if (match) args[match[1]] = match[2];
  });
  return args;
}

async function prompt(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => rl.question(question, answer => {
    rl.close();
    resolve(answer);
  }));
}

async function generateIdeas(topic, pipeline, monthLabel, monthSlug) {
  const config = loadConfig();
  const existingTitles = pipeline.items.map(item => item.title).filter(Boolean);
  const existingMonths = Object.entries(pipeline.months)
    .sort((a, b) => b[0].localeCompare(a[0]))
    .map(([slug, meta]) => `- ${meta.label || slug}: ${meta.totalIdeas || 0} ideas`);

  const response = await executeSkill({
    skillPath: config.skills.idea_generator.file,
    systemPrompt: buildProjectSystemPrompt(),
    contextLabel: 'run_ideas.js monthly idea generation',
    inputs: {
      'Target month': `${monthLabel} (${monthSlug})`,
      'Starting point': topic || 'General Shopify CRO and ecommerce design',
      'Existing idea titles to avoid': existingTitles.length ? existingTitles.join('\n') : '(none yet)',
      'Existing monthly idea sets': existingMonths.length ? existingMonths.join('\n') : '(none yet)'
    },
    instructions: `
Run in non-interactive automation mode.
Do not ask for approval and do not ask follow-up questions.
Generate 15 fresh ideas for the target month.
Skew toward underused pillars based on the existing titles and months provided.
Every idea must fit Ridwan's brand, frameworks, and current Shopify/CRO positioning.
Return data that can feed the monthly idea bank, the content pipeline, and Cowork scripts.
    `,
    outputRules: [
      'Return only one valid JSON array.',
      'Each item must contain: title, brief, type, pillar, priority, angle.',
      'Allowed type values: Tip, CRO Fix, Case Study, Personal.',
      'Allowed priority values: Hot, Warm, Cold.',
      'Do not wrap the JSON in markdown or code fences.'
    ],
    maxTokens: 7000
  });

  return extractJsonArray(response);
}

function buildIdeasHtml(monthLabel, monthSlug, ideas, monthMeta) {
  const payload = JSON.stringify({
    monthLabel,
    monthSlug,
    monthMeta,
    ideas
  });

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${monthLabel} Ideas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #090909;
    --card: #111111;
    --card-2: #171717;
    --border: rgba(255,255,255,0.1);
    --text: #ffffff;
    --text-dim: rgba(255,255,255,0.65);
    --text-faint: rgba(255,255,255,0.36);
    --grad: linear-gradient(135deg, #FF9500 0%, #E040A0 50%, #7B2FBE 100%);
    --syne: 'Syne', sans-serif;
    --mono: 'DM Mono', monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: radial-gradient(circle at top right, rgba(224,64,160,0.14), transparent 25%), #090909;
    color: var(--text);
    font-family: var(--mono);
    min-height: 100vh;
    padding: 32px 20px 72px;
  }
  .wrap { max-width: 1280px; margin: 0 auto; }
  .eyebrow {
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    background: var(--grad);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 10px;
  }
  h1 {
    font-family: var(--syne);
    font-size: clamp(34px, 6vw, 60px);
    line-height: 1;
    margin-bottom: 14px;
  }
  .sub {
    max-width: 760px;
    color: var(--text-dim);
    margin-bottom: 24px;
  }
  .rule { height: 2px; background: var(--grad); border-radius: 999px; margin-bottom: 28px; }
  .nav {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 24px;
  }
  .nav a, .nav button {
    font-family: var(--mono);
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.03);
    color: var(--text);
    padding: 10px 14px;
    border-radius: 999px;
    text-decoration: none;
    cursor: pointer;
  }
  .nav a:hover, .nav button:hover { background: var(--grad); border-color: transparent; }
  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin-bottom: 24px;
  }
  .stat {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px;
  }
  .stat small {
    display: block;
    color: var(--text-faint);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
  }
  .stat strong {
    display: block;
    font-family: var(--syne);
    font-size: 34px;
    line-height: 1;
    background: var(--grad);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }
  .toolbar {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 20px;
  }
  .toolbar button, .toolbar input {
    font-family: var(--mono);
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--card);
    color: var(--text);
    padding: 10px 14px;
  }
  .toolbar button.active {
    background: var(--grad);
    border-color: transparent;
  }
  .toolbar input { min-width: 220px; border-radius: 12px; }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
  }
  .card {
    background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .card-head, .card-meta, .card-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }
  .badge, .priority, .mini {
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-radius: 999px;
    padding: 5px 10px;
    border: 1px solid var(--border);
  }
  .priority.hot { background: var(--grad); border-color: transparent; }
  .priority.warm { color: #FFB84D; border-color: rgba(255,149,0,0.35); }
  .priority.cold { color: var(--text-faint); }
  .title { font-family: var(--syne); font-size: 20px; line-height: 1.15; }
  .brief { color: var(--text-dim); font-size: 12px; line-height: 1.65; }
  .angle {
    font-size: 11px;
    line-height: 1.6;
    padding-top: 10px;
    border-top: 1px dashed var(--border);
    background: var(--grad);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }
  .card-actions button {
    flex: 1;
    border: 1px solid var(--border);
    background: var(--card-2);
    color: var(--text);
    padding: 10px 12px;
    border-radius: 10px;
    cursor: pointer;
  }
  .card-actions button:hover { background: var(--grad); border-color: transparent; }
  .empty {
    border: 1px dashed var(--border);
    border-radius: 18px;
    padding: 28px;
    color: var(--text-dim);
    text-align: center;
  }
</style>
</head>
<body>
<div class="wrap">
  <div class="eyebrow">Monthly Idea Set</div>
  <h1>${monthLabel}</h1>
  <p class="sub">${monthMeta.topic ? `Starting point: ${monthMeta.topic}. ` : ''}This view is synced from the skill-driven idea generator and feeds the content pipeline.</p>
  <div class="rule"></div>

  <div class="nav">
    <a href="../../content_pipeline.html">Open Pipeline</a>
    <a href="../../ridwan_content_system_updated.html">Open Content System</a>
    <button type="button" id="copy-json">Copy JSON Summary</button>
  </div>

  <div class="stats">
    <div class="stat"><small>Total Ideas</small><strong id="stat-total">0</strong></div>
    <div class="stat"><small>Hot Priority</small><strong id="stat-hot">0</strong></div>
    <div class="stat"><small>CRO Fix</small><strong id="stat-cro">0</strong></div>
    <div class="stat"><small>Tips</small><strong id="stat-tip">0</strong></div>
  </div>

  <div class="toolbar">
    <button class="filter active" data-type="all">All</button>
    <button class="filter" data-type="Tip">Tip</button>
    <button class="filter" data-type="CRO Fix">CRO Fix</button>
    <button class="filter" data-type="Case Study">Case Study</button>
    <button class="filter" data-type="Personal">Personal</button>
    <input id="search" type="text" placeholder="Search ideas">
  </div>

  <div class="grid" id="ideas-grid"></div>
  <div class="empty" id="empty" hidden>No ideas match this filter.</div>
</div>

<script>
const DATA = ${payload};
let activeType = 'all';
let query = '';

function updateStats() {
  document.getElementById('stat-total').textContent = DATA.ideas.length;
  document.getElementById('stat-hot').textContent = DATA.ideas.filter(item => item.priority === 'Hot').length;
  document.getElementById('stat-cro').textContent = DATA.ideas.filter(item => item.type === 'CRO Fix').length;
  document.getElementById('stat-tip').textContent = DATA.ideas.filter(item => item.type === 'Tip').length;
}

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function copyIdea(index) {
  const idea = DATA.ideas[index];
  const text = [idea.title, idea.brief, idea.angle].filter(Boolean).join('\\n\\n');
  navigator.clipboard.writeText(text);
}

function render() {
  const filtered = DATA.ideas.filter(item => {
    const typePass = activeType === 'all' || item.type === activeType;
    const text = [item.title, item.brief, item.angle, item.pillar].join(' ').toLowerCase();
    const searchPass = !query || text.includes(query);
    return typePass && searchPass;
  });

  const grid = document.getElementById('ideas-grid');
  const empty = document.getElementById('empty');
  if (!filtered.length) {
    grid.innerHTML = '';
    empty.hidden = false;
    return;
  }

  empty.hidden = true;
  grid.innerHTML = filtered.map(item => {
    const index = DATA.ideas.indexOf(item);
    return ''
      + '<article class="card">'
      +   '<div class="card-head">'
      +     '<span class="badge">' + escapeHtml(item.type) + '</span>'
      +     '<span class="priority ' + String(item.priority || '').toLowerCase() + '">' + escapeHtml(item.priority) + '</span>'
      +   '</div>'
      +   '<div class="title">' + escapeHtml(item.title) + '</div>'
      +   '<div class="brief">' + escapeHtml(item.brief) + '</div>'
      +   '<div class="angle">' + escapeHtml(item.angle) + '</div>'
      +   '<div class="card-meta">'
      +     '<span class="mini">' + escapeHtml(item.pillar) + '</span>'
      +     '<span class="mini">' + escapeHtml(DATA.monthLabel) + '</span>'
      +   '</div>'
      +   '<div class="card-actions">'
      +     '<button type="button" onclick="copyIdea(' + index + ')">Copy</button>'
      +   '</div>'
      + '</article>';
  }).join('');
}

document.querySelectorAll('.filter').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.filter').forEach(node => node.classList.remove('active'));
    button.classList.add('active');
    activeType = button.dataset.type;
    render();
  });
});

document.getElementById('search').addEventListener('input', event => {
  query = event.target.value.trim().toLowerCase();
  render();
});

document.getElementById('copy-json').addEventListener('click', () => {
  navigator.clipboard.writeText(JSON.stringify(DATA.ideas, null, 2));
});

updateStats();
render();
</script>
</body>
</html>`;
}

async function main() {
  const args = parseArgs();
  const pipeline = loadPipelineData();
  const topic = args.topic || await prompt('Monthly focus / starting point (or press Enter for general): ') || '';
  const monthLabel = getCurrentMonthLabel();
  const monthSlug = getCurrentMonthSlug();
  const config = loadConfig();
  const outputDir = resolveFromRoot(config.outputs.ideas_dir);

  ensureDir(config.outputs.ideas_dir);

  console.log(`\n💡 Generating ideas for ${monthLabel}`);
  console.log(`📚 Existing pipeline items: ${pipeline.items.length}\n`);

  try {
    const ideas = await generateIdeas(topic, pipeline, monthLabel, monthSlug);
    const monthMeta = {
      label: monthLabel,
      slug: monthSlug,
      topic,
      generatedAt: new Date().toISOString(),
      totalIdeas: ideas.length,
      htmlPath: `${config.outputs.ideas_dir}/ideas_${monthSlug}.html`,
      jsonPath: `${config.outputs.ideas_dir}/ideas_${monthSlug}.json`
    };

    const jsonPath = path.join(outputDir, `ideas_${monthSlug}.json`);
    fs.writeFileSync(jsonPath, JSON.stringify({ ...monthMeta, ideas }, null, 2));

    registerMonth(pipeline, monthSlug, monthMeta);

    pipeline.items = pipeline.items.filter(item => item.monthSlug !== monthSlug || item.source !== 'monthly-ideas');
    ideas.forEach(idea => {
      pipeline.items.push({
        id: `idea-${slugify(idea.title)}-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
        type: idea.type,
        title: idea.title,
        slug: slugify(idea.title),
        brief: idea.brief,
        angle: idea.angle,
        pillar: idea.pillar,
        priority: idea.priority,
        status: 'Idea',
        day: idea.type === 'Tip' ? 'Monday' : idea.type === 'CRO Fix' ? 'Wednesday' : 'Friday',
        created: new Date().toISOString(),
        month: monthLabel,
        monthSlug,
        week: null,
        source: 'monthly-ideas',
        sourceSet: monthSlug
      });
    });

    const html = buildIdeasHtml(monthLabel, monthSlug, ideas, monthMeta);
    const htmlPath = path.join(outputDir, `ideas_${monthSlug}.html`);
    fs.writeFileSync(htmlPath, html);

    const savedPipeline = savePipelineData(pipeline);
    syncEmbeddedViews(savedPipeline);

    console.log(`   ✅ ideas_${monthSlug}.json saved`);
    console.log(`   ✅ ideas_${monthSlug}.html saved`);
    console.log(`   ✅ pipeline_data.json updated`);
    console.log(`   ✅ content views synced`);
    console.log(`\n📂 Open: ${htmlPath}\n`);
  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
}

main();
