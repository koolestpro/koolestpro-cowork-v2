#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const {
  buildProjectSystemPrompt,
  cleanupModelText,
  ensureDir,
  executeSkill,
  getCurrentMonthLabel,
  getCurrentMonthSlug,
  getCurrentWeekLabel,
  loadConfig,
  loadPipelineData,
  readText,
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

/**
 * Single-pass HTML generation.
 *
 * Previously this was two API calls:
 *   1. generate markdown content package (7K tokens max)
 *   2. render HTML from that markdown (16K tokens max — but silently capped at 8192 without beta header)
 *
 * Both calls used only the first 7K–12K chars of a 60K-char template, so the
 * model never saw 80% of the structural blueprint.
 *
 * Now: one call, full template, 32K output tokens, system prompt with all
 * project rules — same context Claude in Cowork has when generating manually.
 */
async function generateHtml(idea, angle) {
  const config = loadConfig();
  // Pass the FULL template — no truncation. 60KB input is ~15K tokens, well within limits.
  const fullTemplate = readText(config.skills.content_engine.template);

  return cleanupModelText(await executeSkill({
    skillPath: config.skills.content_engine.file,
    systemPrompt: buildProjectSystemPrompt(),
    contextLabel: 'run_tip.js single-pass HTML generation',
    inputs: {
      Topic: idea,
      Angle: angle,
      'Template reference — replicate this exact HTML structure, CSS system, slide patterns, download logic, and tab system': fullTemplate
    },
    instructions: `
Generate a complete, production-ready HTML file for this Tip post.

Use the Template reference as your exact structural blueprint:
- Replicate its slide patterns, CSS class names, glow blobs, dot grid, swipe logic, dot indicators, and pager
- Replicate its download panel (PNG per slide, Download All, Download PDF)
- Replicate its caption tabs (LinkedIn Long-form, Hook, Instagram, Tweet thread)
- Replicate its export panel with exportPostData() and "Export to Cowork →" button

Generate fresh, original content across all 8 carousel slides for the given Topic and Angle.
Use Ridwan's frameworks and big ideas where relevant.

GRADIENT TEXT: For any gradient-coloured stat numbers or headline highlights, use SVG <text> with
<linearGradient> fill (width ≥ 300px). Never use CSS -webkit-background-clip: text.

AVATAR: Use the real photo pattern in the LK header:
<div class="lk-av" style="padding:0;overflow:hidden;">
  <img src="../../assets/ridwan/avatar-circle.jpg" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" onerror="this.parentNode.innerHTML='<span>R</span>'">
</div>

DOWNLOAD LOGIC: The toHide selector must include: [data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap

No Notion references of any kind.
    `,
    outputRules: [
      'Return only a complete HTML5 document starting with <!DOCTYPE html>.',
      'Do not wrap in code fences or add any preamble text before <!DOCTYPE html>.',
      'The file must be fully self-contained — all CSS and JS inline, fonts from Google Fonts CDN only.',
      'Include all 8 carousel slides, 3 single graphic variations, and all post copy tabs.',
      'Include the download panel with working html2canvas + jsPDF logic.'
    ],
    maxTokens: 32000
  }));
}

function addToPipeline(pipeline, item) {
  pipeline.items.push(item);
  return savePipelineData(pipeline);
}

async function main() {
  const args = parseArgs();
  let idea = args.idea;
  let angle = args.angle;

  if (!idea) idea = await prompt('Tip idea / topic: ');
  if (!angle) angle = await prompt('Angle (educational / contrarian / story / framework) [educational]: ') || 'educational';

  if (!idea) {
    console.error('❌ Idea required');
    process.exit(1);
  }

  const slug = slugify(idea);
  const date = new Date().toISOString().split('T')[0];
  const filename = `${slug}_${date}`;
  const config = loadConfig();
  const outputDir = resolveFromRoot(config.outputs.tips_dir);

  ensureDir(config.outputs.tips_dir);

  console.log(`\n💡 Generating Tip post: ${idea}`);
  console.log(`   Angle: ${angle}`);
  console.log(`📁 Output folder: ${outputDir}`);
  console.log(`   Model: ${config.anthropic_api.model}`);
  console.log(`   Tokens: up to 32,000 (single-pass)\n`);

  try {
    console.log('   ⏳ Generating HTML (single pass — this takes ~30–60s)...');
    const html = await generateHtml(idea, angle);

    fs.writeFileSync(path.join(outputDir, `${filename}.html`), html);
    console.log(`   ✅ ${filename}.html saved (${Math.round(html.length / 1024)}KB)`);

    const pipeline = loadPipelineData();
    const savedPipeline = addToPipeline(pipeline, {
      id: `tip-${slug}-${Date.now()}`,
      type: 'Tip',
      title: idea,
      slug,
      status: 'Created',
      day: 'Monday',
      created: new Date().toISOString(),
      folder: `${config.outputs.tips_dir}/${filename}.html`,
      week: getCurrentWeekLabel(),
      month: getCurrentMonthLabel(),
      monthSlug: getCurrentMonthSlug(),
      source: 'tip-generator'
    });
    syncEmbeddedViews(savedPipeline);

    console.log(`   ✅ pipeline_data.json updated`);
    console.log(`   ✅ content views synced`);
    console.log(`\n📂 Open: ${path.join(outputDir, `${filename}.html`)}\n`);
  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
}

main();
