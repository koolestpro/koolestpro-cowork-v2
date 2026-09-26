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
  savePipelineData,
  slugify,
  resolveFromRoot
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

async function runAudit(store, url, notes, screenshot) {
  const config = loadConfig();
  return cleanupModelText(await executeSkill({
    skillPath: config.skills.cro_stack.audit,
    systemPrompt: buildProjectSystemPrompt(),
    contextLabel: 'run_cro_fix.js audit stage',
    inputs: {
      'Store name': store,
      URL: url || '(not provided)',
      Notes: notes || '(none provided)',
      Screenshot: screenshot || '(not provided)'
    },
    instructions: `
Run in non-interactive automation mode.
If a screenshot is missing, continue in text-only mode using the store name, URL, and notes.
Make assumptions explicit.
Produce the audit brief that downstream CRO stack steps can consume.
    `,
    outputRules: [
      'Return markdown only.',
      'Keep the structured audit brief format.',
      'Do not ask the user for more information.'
    ],
    maxTokens: 9000
  }));
}

async function runRebuild(auditBrief, store, screenshot) {
  const config = loadConfig();
  return cleanupModelText(await executeSkill({
    skillPath: config.skills.cro_stack.rebuild,
    systemPrompt: buildProjectSystemPrompt(),
    contextLabel: 'run_cro_fix.js rebuild stage',
    inputs: {
      'Store name': store,
      'Audit brief': auditBrief,
      Screenshot: screenshot || '(not provided)'
    },
    instructions: `
Run in non-interactive automation mode.
Build a mobile-first rebuild that follows the audit brief.
If no screenshot is available, use clearly labeled placeholder or assumed visual structure where needed.
Return a complete standalone rebuild HTML file.
Use real photo avatar pattern for Ridwan: <img src="../../assets/ridwan/avatar-circle.jpg" ...>
Do not use CSS gradient text — use SVG gradients for any gradient-coloured headings.
    `,
    outputRules: [
      'Return only a complete HTML5 document starting with <!DOCTYPE html>.',
      'Do not include markdown fences or commentary.'
    ],
    maxTokens: 32000
  }));
}

async function runCaptions(auditBrief, rebuildHtml, store) {
  const config = loadConfig();
  return cleanupModelText(await executeSkill({
    skillPath: config.skills.cro_stack.captions,
    systemPrompt: buildProjectSystemPrompt(),
    contextLabel: 'run_cro_fix.js captions stage',
    inputs: {
      'Store name': store,
      'Audit brief': auditBrief,
      // Pass more rebuild context so captions are grounded in the actual design decisions
      'Build summary context': rebuildHtml.slice(0, 8000)
    },
    instructions: `
Run in non-interactive automation mode.
Use the audit brief as the source of truth and the rebuild context as supporting detail.
Write the full CRO caption pack for this project.
    `,
    outputRules: [
      'Return markdown only.',
      'Include all labeled caption sections and the Skill E handoff.',
      'Do not ask for more information.'
    ],
    maxTokens: 9000
  }));
}

async function runContentPack(auditBrief, rebuildHtml, captions, store, screenshot) {
  const config = loadConfig();
  return cleanupModelText(await executeSkill({
    skillPath: config.skills.cro_stack.content_pack,
    systemPrompt: buildProjectSystemPrompt(),
    contextLabel: 'run_cro_fix.js content pack stage',
    inputs: {
      'Store name': store,
      'Audit brief': auditBrief,
      'Rebuild HTML': rebuildHtml,
      Captions: captions,
      'Before screenshot': screenshot || '(not provided)',
      'After screenshot': '(not available in automation mode)'
    },
    instructions: `
Run in non-interactive automation mode.
Build the final CRO content pack HTML — the carousel, before/after, annotations, and caption tabs.
If before/after screenshots are unavailable, include clearly labelled placeholder slots.
Use SVG gradients for any gradient-coloured text — never CSS -webkit-background-clip: text.
Include the real photo avatar: <img src="../../assets/ridwan/avatar-circle.jpg" ...>
Download selector must hide: [data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap
    `,
    outputRules: [
      'Return only a complete HTML5 document starting with <!DOCTYPE html>.',
      'Do not add markdown fences or commentary.'
    ],
    maxTokens: 32000
  }));
}

async function main() {
  const args = parseArgs();

  let store = args.store;
  let url = args.url;
  let notes = args.notes;
  let screenshot = args.screenshot;

  if (!store) store = await prompt('Store name (e.g. "Eddie Bauer"): ');
  if (!url) url = await prompt('Store URL (or press Enter to skip): ');
  if (!notes) notes = await prompt('Initial notes (optional): ');
  if (!screenshot) screenshot = await prompt('Screenshot path (optional): ');

  if (!store) {
    console.error('❌ Store name required');
    process.exit(1);
  }

  const slug = slugify(store);
  const config = loadConfig();
  const outputDir = path.join(resolveFromRoot(config.outputs.cro_dir), slug);

  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(path.join(outputDir, 'screenshots'), { recursive: true });

  console.log(`\n🎯 Generating CRO stack for: ${store}`);
  console.log(`📁 Output folder: ${outputDir}`);
  console.log(`   Model: ${config.anthropic_api.model}`);
  console.log(`   Rebuild + Content Pack: up to 32,000 tokens each\n`);

  try {
    const auditBrief = await runAudit(store, url, notes, screenshot);
    fs.writeFileSync(path.join(outputDir, 'audit_brief.md'), auditBrief);
    console.log('   ✅ audit_brief.md saved');

    const rebuildHtml = await runRebuild(auditBrief, store, screenshot);
    fs.writeFileSync(path.join(outputDir, 'rebuild.html'), rebuildHtml);
    console.log('   ✅ rebuild.html saved');

    const captions = await runCaptions(auditBrief, rebuildHtml, store);
    fs.writeFileSync(path.join(outputDir, 'captions.md'), captions);
    console.log('   ✅ captions.md saved');

    const contentPack = await runContentPack(auditBrief, rebuildHtml, captions, store, screenshot);
    fs.writeFileSync(path.join(outputDir, 'content_pack.html'), contentPack);
    console.log('   ✅ content_pack.html saved');

    const pipeline = loadPipelineData();
    pipeline.items.push({
      id: `cro-${slug}-${Date.now()}`,
      type: 'CRO Fix',
      title: `CRO Fix: ${store}`,
      slug,
      status: 'Created',
      day: 'Wednesday',
      created: new Date().toISOString(),
      folder: `${config.outputs.cro_dir}/${slug}`,
      week: getCurrentWeekLabel(),
      month: getCurrentMonthLabel(),
      monthSlug: getCurrentMonthSlug(),
      source: 'cro-stack'
    });

    const savedPipeline = savePipelineData(pipeline);
    syncEmbeddedViews(savedPipeline);

    console.log('   ✅ pipeline_data.json updated');
    console.log('   ✅ content views synced');
    console.log(`\n📂 Open: ${path.join(outputDir, 'content_pack.html')}\n`);
  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
}

main();
