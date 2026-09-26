#!/usr/bin/env node
/**
 * run_deepseek_task.js
 *
 * In-Cowork replacement for the manual "paste .ai-workflow/deepseek-task.md
 * into OpenCode Desktop" hand-off. Reads a task spec, inlines every file it
 * references, sends the whole thing to DeepSeek's API, and writes the
 * returned file(s) straight to disk — all from one terminal command.
 *
 * A single terminal call in this sandbox has a hard ~45s ceiling, and a full
 * HTML build can take longer than that to generate. Rather than trying to
 * loop internally (which would blow the same ceiling), this script does ONE
 * DeepSeek call per invocation. If the model gets cut off mid-file, it saves
 * the partial output and tells you the exact command to run next — so
 * finishing a big file is just re-running this a couple of times in a row,
 * each one fast enough to fit inside a single call.
 *
 * Uses DeepSeek's non-reasoning "deepseek-chat" model by default. The
 * reasoning-tier models (DEEPSEEK_HEAVY_MODEL/DEEPSEEK_LIGHT_MODEL from
 * .env) were tested and found to spend most or all of the token budget on
 * internal reasoning_content before writing any real output on a detailed
 * build prompt — bad for long files under a terminal timeout. Pass
 * --reasoning if a future task genuinely needs multi-step thinking
 * mid-generation rather than "build exactly this fully-specified thing."
 *
 * Usage:
 *   node run_deepseek_task.js
 *   node run_deepseek_task.js --task=.ai-workflow/deepseek-task.md
 *   node run_deepseek_task.js --reasoning --tier=heavy --max-tokens=8000
 *   node run_deepseek_task.js --continue-from=.ai-workflow/deepseek-output-log/2026-07-05T12-00-00.partial.md
 */

const fs = require('fs');
const path = require('path');
const {
  ROOT,
  callDeepSeek,
  ensureDir,
  resolveFromRoot
} = require('./lib/cowork_runtime');

// Deliberately NOT the full buildProjectSystemPrompt()/CLAUDE.md dump here —
// that's several thousand extra prefill tokens per call and the task spec
// itself already carries whatever CLAUDE.md rules apply to this specific
// build. Keeping this short is what keeps a single run fast.
const LEAN_SYSTEM_PROMPT = `You are the Koolestpro content automation system for Ridwan Adekunle (@koolestpro), running in local pipeline automation mode.
Follow the task spec and reference files you're given exactly. Do not invent data, numbers, or file paths that weren't provided.
Return ONLY what the OUTPUT FORMAT section at the end of the prompt asks for. No preamble, no closing remarks, no markdown code fences around the FILE blocks.`;

// CLAUDE.md is already embedded in full inside Claude's own project context —
// re-inlining it here would just be prefill weight for no benefit.
// Top-level planning docs are useful for a human but not needed to
// generate one HTML file, so they're excluded to keep prefill fast.
// skills/*.md files are excluded too: they're long, mostly-generic
// component libraries, and a well-written task spec (see .ai-workflow/
// deepseek-task.md) should already distill the specific rules that matter
// for THIS build into its own RULES section — that's the point of writing
// the task spec in the first place, rather than re-attaching the whole
// skill file every time.
const REFERENCE_FILE_EXCLUSIONS_EXACT = new Set([
  'CLAUDE.md',
  'docs/koolestpro-content-operating-plan.md'
]);
const REFERENCE_FILE_EXCLUSION_PREFIXES = ['skills/'];

// Keeps prefill light. Large reference files get trimmed with a note
// rather than silently dropped.
const MAX_REFERENCE_FILE_CHARS = 12000;

// Empirically (see .ai-workflow/deepseek-task.md test run, 2026-07-05):
// model:"deepseek-chat" (non-reasoning) produced a complete ~17k-char HTML
// file using 5,030 completion tokens in ~39s, on a ~20k-char prompt. This
// leaves a bit of headroom under the ~45s terminal ceiling; if a build
// needs more than this, it truncates cleanly and --continue-from picks up
// where it left off.
const DEFAULT_MAX_TOKENS = 6000;

function parseArgs() {
  const args = {
    task: '.ai-workflow/deepseek-task.md',
    tier: 'light',
    reasoning: false,
    maxTokens: DEFAULT_MAX_TOKENS,
    continueFrom: null
  };
  process.argv.slice(2).forEach(arg => {
    const match = arg.match(/^--([\w-]+)=(.+)$/);
    if (match) {
      const [, key, value] = match;
      if (key === 'task') args.task = value;
      if (key === 'tier') args.tier = value;
      if (key === 'max-tokens') args.maxTokens = Number(value);
      if (key === 'continue-from') args.continueFrom = value;
      return;
    }
    if (arg === '--reasoning') args.reasoning = true;
  });
  return args;
}

/**
 * Finds every relative file path mentioned in the task spec (skills/*.md,
 * outputs/*.md, outputs/*.html, .ai-workflow/*.md) and inlines the ones
 * that actually exist on disk. This is what lets a plain chat-completion
 * call "read" project files without needing tool use.
 */
function findReferencedFiles(taskText) {
  const pattern = /[\w.\-/]+\.(?:md|html|json)/g;
  const matches = taskText.match(pattern) || [];
  const seen = new Set();
  const found = [];
  for (const relPath of matches) {
    if (seen.has(relPath)) continue;
    if (REFERENCE_FILE_EXCLUSIONS_EXACT.has(relPath)) continue;
    if (REFERENCE_FILE_EXCLUSION_PREFIXES.some(prefix => relPath.startsWith(prefix))) continue;
    seen.add(relPath);
    const abs = resolveFromRoot(relPath);
    if (fs.existsSync(abs) && fs.statSync(abs).isFile()) {
      found.push(relPath);
    }
  }
  return found;
}

function buildInitialPrompt(taskText, referencedFiles) {
  const sections = [
    'TASK SPEC (this is the job — follow every instruction in it exactly):',
    taskText.trim(),
    '',
    '---',
    'REFERENCE MATERIAL (files the task spec above points to — read these fully before building):'
  ];

  if (referencedFiles.length === 0) {
    sections.push('(none of the referenced paths were found on disk — proceed from the task spec alone)');
  }

  referencedFiles.forEach(relPath => {
    let content = fs.readFileSync(resolveFromRoot(relPath), 'utf8').trim();
    if (content.length > MAX_REFERENCE_FILE_CHARS) {
      content = content.slice(0, MAX_REFERENCE_FILE_CHARS)
        + `\n\n[...truncated for speed — ${content.length - MAX_REFERENCE_FILE_CHARS} more characters in the real file at ${relPath}...]`;
    }
    sections.push('');
    sections.push(`=== REFERENCE FILE: ${relPath} ===`);
    sections.push(content);
    sections.push(`=== END REFERENCE FILE: ${relPath} ===`);
  });

  sections.push('');
  sections.push('---');
  sections.push('OUTPUT FORMAT — MANDATORY:');
  sections.push('For every file listed under "FILES:" in the task spec, output it wrapped EXACTLY like this:');
  sections.push('===FILE: <exact relative path from the task spec>===');
  sections.push('<complete file content, nothing else>');
  sections.push('===END FILE===');
  sections.push('');
  sections.push('Repeat that block once per file. Do not wrap the blocks in markdown code fences.');
  sections.push('Anything else the task asks for (build summaries, annotated snippets not listed under FILES:) goes as plain text OUTSIDE the FILE blocks.');
  sections.push('Do not add commentary, apologies, or meta-narration before, between, or after the blocks beyond what was explicitly asked for.');
  sections.push('Keep markup and CSS compact (short class names, no long comments) — being complete matters more than being verbose, since output length is limited per turn.');

  return sections.join('\n');
}

function buildContinuationPrompt(partialContent) {
  const tail = partialContent.slice(-2500);
  return [
    'You are continuing a response that got cut off mid-generation because it ran out of output tokens.',
    'Below is the exact tail end of what you already wrote. Do NOT repeat any of it, do NOT restart any ===FILE: ...=== header, and do NOT re-introduce yourself or summarize.',
    'Continue writing immediately from the exact point this leaves off, as if your next token were being appended directly after it.',
    'Finish all open HTML tags, finish any open ===FILE: ...=== block with a proper ===END FILE=== marker, and stop once everything the original task asked for is complete.',
    '',
    '=== TAIL OF PARTIAL OUTPUT (for context only — do not repeat) ===',
    tail,
    '=== END TAIL ===',
    '',
    'Continue now:'
  ].join('\n');
}

function extractFileBlocks(responseText) {
  const blocks = [];
  const regex = /===FILE:\s*(.+?)\s*===\r?\n([\s\S]*?)\r?\n===END FILE===/g;
  let match;
  while ((match = regex.exec(responseText)) !== null) {
    blocks.push({ path: match[1].trim(), content: match[2] });
  }
  return blocks;
}

function stripFileBlocks(responseText) {
  return responseText.replace(/===FILE:[\s\S]*?===END FILE===/g, '').trim();
}

function savePartial(accumulated) {
  ensureDir('.ai-workflow/deepseek-output-log');
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const partialPath = resolveFromRoot(`.ai-workflow/deepseek-output-log/${stamp}.partial.md`);
  fs.writeFileSync(partialPath, accumulated);
  return partialPath;
}

async function main() {
  const args = parseArgs();
  let prompt;
  let accumulatedSoFar = '';

  if (args.continueFrom) {
    const continuePath = resolveFromRoot(args.continueFrom);
    if (!fs.existsSync(continuePath)) {
      console.error(`--continue-from file not found: ${args.continueFrom}`);
      process.exit(1);
    }
    accumulatedSoFar = fs.readFileSync(continuePath, 'utf8');
    prompt = buildContinuationPrompt(accumulatedSoFar);
    console.log(`Continuing from: ${args.continueFrom} (${accumulatedSoFar.length.toLocaleString()} chars so far)`);
  } else {
    const taskPath = resolveFromRoot(args.task);
    if (!fs.existsSync(taskPath)) {
      console.error(`Task file not found: ${args.task}`);
      process.exit(1);
    }
    const taskText = fs.readFileSync(taskPath, 'utf8');
    const referencedFiles = findReferencedFiles(taskText);
    console.log(`Task: ${args.task}`);
    console.log(`Reference files found: ${referencedFiles.length ? referencedFiles.join(', ') : '(none)'}`);
    prompt = buildInitialPrompt(taskText, referencedFiles);
  }

  console.log(`Model: ${args.reasoning ? `reasoning (${args.tier})` : 'deepseek-chat (non-reasoning)'}  |  max_tokens: ${args.maxTokens}`);
  console.log('Calling DeepSeek...');

  const { content, finishReason } = await callDeepSeek(prompt, {
    reasoning: args.reasoning,
    tier: args.tier,
    maxTokens: args.maxTokens,
    systemPrompt: LEAN_SYSTEM_PROMPT,
    allowTruncated: true
  });

  const fullContent = accumulatedSoFar + content;

  if (finishReason === 'length') {
    const partialPath = savePartial(fullContent);
    const relPartial = path.relative(ROOT, partialPath);
    console.warn(`\nStill truncated (finish_reason=length) after ${fullContent.length.toLocaleString()} chars.`);
    console.warn('Nothing written to the project yet — run this to continue:');
    console.warn(`\n  node run_deepseek_task.js --continue-from=${relPartial}\n`);
    process.exit(2);
  }

  // Finished cleanly — extract and write real output files.
  ensureDir('.ai-workflow/deepseek-output-log');
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const logPath = resolveFromRoot(`.ai-workflow/deepseek-output-log/${stamp}.md`);
  fs.writeFileSync(logPath, fullContent);

  const fileBlocks = extractFileBlocks(fullContent);
  const summaryText = stripFileBlocks(fullContent);

  if (fileBlocks.length === 0) {
    console.warn('\nNo ===FILE: ...=== blocks found in the final response.');
    console.warn(`Full raw response saved to: ${path.relative(ROOT, logPath)}`);
    console.warn('Nothing was written to the project — check the log.');
    process.exit(1);
  }

  console.log('\nFiles written:');
  fileBlocks.forEach(({ path: relPath, content: fileContent }) => {
    const abs = resolveFromRoot(relPath);
    fs.mkdirSync(path.dirname(abs), { recursive: true });
    fs.writeFileSync(abs, fileContent.trim() + '\n');
    console.log(`  - ${relPath} (${fileContent.length.toLocaleString()} chars)`);
  });

  if (summaryText) {
    console.log('\n--- Build summary from DeepSeek ---');
    console.log(summaryText);
  }

  console.log(`\nRaw response log: ${path.relative(ROOT, logPath)}`);
}

main().catch(err => {
  console.error('\nrun_deepseek_task.js failed:', err.message);
  process.exit(1);
});
