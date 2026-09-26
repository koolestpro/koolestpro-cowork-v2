const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(ROOT, 'cowork_config.json');

/**
 * Minimal .env loader — no dotenv dependency needed.
 * Only sets a var if it isn't already present in the environment,
 * so real shell exports always win over the file.
 */
function loadEnvFile() {
  const envPath = path.join(ROOT, '.env');
  if (!fs.existsSync(envPath)) return;
  const lines = fs.readFileSync(envPath, 'utf8').split('\n');
  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const match = line.match(/^([A-Z0-9_]+)=(.*)$/i);
    if (!match) continue;
    const [, key, value] = match;
    if (process.env[key] === undefined && value !== '') {
      process.env[key] = value.replace(/^["']|["']$/g, '');
    }
  }
}
loadEnvFile();

function loadConfig() {
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

function resolveFromRoot(relativePath) {
  return path.join(ROOT, relativePath);
}

function readText(relativePath) {
  return fs.readFileSync(resolveFromRoot(relativePath), 'utf8');
}

function ensureDir(relativePath) {
  fs.mkdirSync(resolveFromRoot(relativePath), { recursive: true });
}

function slugify(text, maxLength = 50) {
  return String(text || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, maxLength);
}

function cleanupModelText(text) {
  return String(text || '')
    .replace(/^```(?:json|html|markdown|md)?\s*/i, '')
    .replace(/```\s*$/i, '')
    .trim();
}

function extractJsonArray(text) {
  const cleaned = cleanupModelText(text);
  const match = cleaned.match(/\[[\s\S]*\]/);
  if (!match) {
    throw new Error('Could not find a JSON array in the model response.');
  }
  return JSON.parse(match[0]);
}

function monthLabelFromSlug(monthSlug) {
  const [year, month] = String(monthSlug).split('-').map(Number);
  return new Date(Date.UTC(year, month - 1, 1)).toLocaleDateString('en-US', {
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC'
  });
}

function monthSlugFromLabel(label) {
  const parsed = new Date(`${label} 01`);
  if (Number.isNaN(parsed.getTime())) return '';
  return `${parsed.getFullYear()}-${String(parsed.getMonth() + 1).padStart(2, '0')}`;
}

function getCurrentMonthSlug() {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
}

function getCurrentMonthLabel() {
  return monthLabelFromSlug(getCurrentMonthSlug());
}

function getCurrentWeekLabel() {
  const now = new Date();
  const day = now.getDay();
  const monday = new Date(now);
  monday.setDate(now.getDate() + (day === 0 ? -6 : 1 - day));
  return `Week of ${monday.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`;
}

function computeSyncHash(payload) {
  return crypto.createHash('sha1').update(JSON.stringify(payload)).digest('hex').slice(0, 12);
}

function normalizeItem(item) {
  const normalized = { ...item };
  if (!normalized.monthSlug && normalized.month) {
    normalized.monthSlug = monthSlugFromLabel(normalized.month);
  }
  if (!normalized.month && normalized.monthSlug) {
    normalized.month = monthLabelFromSlug(normalized.monthSlug);
  }
  if (!normalized.day) {
    normalized.day = normalized.type === 'Tip'
      ? 'Monday'
      : normalized.type === 'CRO Fix'
        ? 'Wednesday'
        : 'Friday';
  }
  return normalized;
}

function normalizePipelineData(data) {
  const pipeline = {
    meta: { version: '3.0.0', updatedAt: null, syncHash: '' },
    months: {},
    items: [],
    ...data
  };

  pipeline.meta = {
    version: '3.0.0',
    updatedAt: pipeline.meta?.updatedAt || null,
    syncHash: pipeline.meta?.syncHash || '',
    ...pipeline.meta
  };

  pipeline.months = pipeline.months || {};
  pipeline.items = Array.isArray(pipeline.items) ? pipeline.items.map(normalizeItem) : [];

  pipeline.items.forEach(item => {
    if (!item.monthSlug) return;
    if (!pipeline.months[item.monthSlug]) {
      pipeline.months[item.monthSlug] = {
        label: item.month || monthLabelFromSlug(item.monthSlug)
      };
    }
  });

  Object.keys(pipeline.months).forEach(monthSlug => {
    const meta = pipeline.months[monthSlug] || {};
    const inferredHtmlPath = `outputs/ideas/ideas_${monthSlug}.html`;
    const inferredJsonPath = `outputs/ideas/ideas_${monthSlug}.json`;
    const absoluteJsonPath = resolveFromRoot(inferredJsonPath);

    if (!meta.label) meta.label = monthLabelFromSlug(monthSlug);
    if (!meta.htmlPath && fs.existsSync(resolveFromRoot(inferredHtmlPath))) {
      meta.htmlPath = inferredHtmlPath;
    }
    if (!meta.jsonPath && fs.existsSync(absoluteJsonPath)) {
      meta.jsonPath = inferredJsonPath;
    }
    if (fs.existsSync(absoluteJsonPath)) {
      try {
        const monthFile = JSON.parse(fs.readFileSync(absoluteJsonPath, 'utf8'));
        if (!meta.topic && monthFile.topic) meta.topic = monthFile.topic;
        if (!meta.generatedAt && monthFile.generatedAt) meta.generatedAt = monthFile.generatedAt;
        if (!meta.totalIdeas && Array.isArray(monthFile.ideas)) meta.totalIdeas = monthFile.ideas.length;
      } catch (error) {
        // Ignore malformed month files and preserve the rest of the pipeline data.
      }
    }
    pipeline.months[monthSlug] = meta;
  });

  return pipeline;
}

function loadPipelineData() {
  const config = loadConfig();
  const pipelinePath = resolveFromRoot(config.paths.pipeline_data);
  if (!fs.existsSync(pipelinePath)) {
    return normalizePipelineData({});
  }
  try {
    return normalizePipelineData(JSON.parse(fs.readFileSync(pipelinePath, 'utf8')));
  } catch (error) {
    throw new Error(`Could not read pipeline data: ${error.message}`);
  }
}

function savePipelineData(pipeline) {
  const config = loadConfig();
  const normalized = normalizePipelineData(pipeline);
  normalized.meta.updatedAt = new Date().toISOString();
  normalized.meta.syncHash = computeSyncHash({
    months: normalized.months,
    items: normalized.items
  });
  fs.writeFileSync(
    resolveFromRoot(config.paths.pipeline_data),
    JSON.stringify(normalized, null, 2)
  );
  return normalized;
}

function registerMonth(pipeline, monthSlug, details) {
  pipeline.months[monthSlug] = {
    label: monthLabelFromSlug(monthSlug),
    ...pipeline.months[monthSlug],
    ...details
  };
}

/**
 * Builds the system prompt from CLAUDE.md project rules.
 * This gives the API the same project context Claude in Cowork has natively.
 */
function buildProjectSystemPrompt() {
  const claudeMdPath = path.join(ROOT, 'CLAUDE.md');
  const claudeMd = fs.existsSync(claudeMdPath) ? fs.readFileSync(claudeMdPath, 'utf8') : '';

  return `You are the Koolestpro content automation system for Ridwan Adekunle (@koolestpro).
You are running in local pipeline automation mode. Follow all rules below exactly.

${claudeMd}

---
AUTOMATION OUTPUT CONTRACT:
- Return ONLY the exact format requested. No preamble, no explanations, no commentary.
- For HTML output: start with <!DOCTYPE html> and end with </html>. Nothing before or after.
- For JSON output: return only valid JSON. No markdown fences, no comments.
- For Markdown output: return plain markdown. No code fences wrapping the entire output.`;
}

async function callClaude(promptText, options = {}) {
  const config = loadConfig();
  if (!process.env.ANTHROPIC_API_KEY) {
    throw new Error('ANTHROPIC_API_KEY not set');
  }

  const requestBody = {
    model: options.model || config.anthropic_api.model,
    max_tokens: options.maxTokens || config.anthropic_api.max_tokens,
    messages: [{ role: 'user', content: promptText }]
  };

  // Attach project rules as system message so every call follows brand + export rules
  if (options.systemPrompt) {
    requestBody.system = options.systemPrompt;
  }

  const response = await fetch(config.anthropic_api.endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'anthropic-version': '2023-06-01',
      'x-api-key': process.env.ANTHROPIC_API_KEY,
      // Enable extended output — allows up to 128K output tokens for long HTML files
      'anthropic-beta': 'output-128k-2025-02-19'
    },
    body: JSON.stringify(requestBody)
  });

  if (!response.ok) {
    throw new Error(`API ${response.status}: ${await response.text()}`);
  }

  const data = await response.json();
  return data.content
    .filter(block => block.type === 'text')
    .map(block => block.text)
    .join('\n')
    .trim();
}

/**
 * Calls DeepSeek's API directly — this is the in-Cowork replacement for
 * manually pasting .ai-workflow/deepseek-task.md into OpenCode Desktop.
 * DeepSeek's API is OpenAI-compatible chat completions.
 */
async function callDeepSeek(promptText, options = {}) {
  if (!process.env.DEEPSEEK_API_KEY) {
    throw new Error('DEEPSEEK_API_KEY not set (check .env)');
  }

  // IMPORTANT — found by testing, not documented anywhere obvious:
  // requesting the DEEPSEEK_HEAVY_MODEL/DEEPSEEK_LIGHT_MODEL aliases from
  // .env (deepseek-v4-pro / deepseek-v4-flash) puts the model in reasoning
  // mode — it fills reasoning_content first and, on a long/detailed build
  // prompt, can burn the ENTIRE max_tokens budget on reasoning before
  // writing a single character of real output (observed: 2800 max_tokens,
  // 0 chars of content, on this project's actual CRO-rebuild task prompt).
  // reasoning_effort:'low' is the lowest the API accepts and did not fix
  // this reliably on complex prompts.
  // Explicitly requesting model:"deepseek-chat" instead routes to a plain
  // non-reasoning completion on the same underlying model — no
  // reasoning_content field at all, full budget goes to real output.
  // Since this pipeline's job is executing an already-fully-specified task
  // spec (all the reasoning already happened upstream, in Skill A/B/etc.),
  // non-reasoning mode is the right default. Pass options.reasoning:true
  // to opt into the heavy/light reasoning models for something that
  // genuinely needs multi-step thinking mid-generation.
  const model = options.model
    || (options.reasoning
      ? (options.tier === 'light' ? process.env.DEEPSEEK_LIGHT_MODEL : process.env.DEEPSEEK_HEAVY_MODEL)
      : 'deepseek-chat');

  const messages = [];
  if (options.systemPrompt) {
    messages.push({ role: 'system', content: options.systemPrompt });
  }
  messages.push({ role: 'user', content: promptText });

  const body = {
    model,
    messages,
    max_tokens: options.maxTokens || 8000,
    temperature: options.temperature ?? 0.4
  };
  if (options.reasoning) {
    body.reasoning_effort = options.reasoningEffort || 'low';
  }

  const response = await fetch('https://api.deepseek.com/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.DEEPSEEK_API_KEY}`
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    throw new Error(`DeepSeek API ${response.status}: ${await response.text()}`);
  }

  const data = await response.json();
  const choice = data.choices && data.choices[0];
  if (!choice) {
    throw new Error(`DeepSeek API returned no choices: ${JSON.stringify(data)}`);
  }

  const content = (choice.message && choice.message.content || '').trim();

  // Reasoning models spend part of the budget "thinking" before writing the
  // real answer, so a single call very often isn't enough for a full HTML
  // file within a short terminal timeout. Rather than throwing away a
  // truncated-but-real partial answer, hand it back with enough metadata
  // for the caller to request a continuation instead of starting over.
  if (options.allowTruncated) {
    return { content, finishReason: choice.finish_reason, usage: data.usage };
  }

  if (choice.finish_reason === 'length') {
    throw new Error('DeepSeek response was cut off (finish_reason=length) — retry with a higher maxTokens or pass allowTruncated:true to handle it.');
  }
  return content;
}

async function executeSkill(options) {
  const skillText = fs.readFileSync(resolveFromRoot(options.skillPath), 'utf8');
  const sections = [];

  if (options.contextLabel) {
    sections.push(`AUTOMATION CONTEXT: ${options.contextLabel}`);
  }

  if (options.inputs) {
    sections.push('INPUTS:');
    Object.entries(options.inputs).forEach(([key, value]) => {
      sections.push(`${key}:`);
      sections.push(typeof value === 'string' ? value : JSON.stringify(value, null, 2));
      sections.push('');
    });
  }

  if (options.instructions) {
    sections.push('TASK INSTRUCTIONS:');
    sections.push(options.instructions.trim());
  }

  if (options.outputRules?.length) {
    sections.push('STRICT OUTPUT RULES:');
    options.outputRules.forEach(rule => sections.push(`- ${rule}`));
  }

  const prompt = [
    skillText.trim(),
    '',
    '---',
    'AUTOMATION RUNTIME',
    sections.join('\n').trim()
  ].join('\n');

  const caller = options.provider === 'deepseek' ? callDeepSeek : callClaude;
  return caller(prompt, {
    maxTokens: options.maxTokens,
    model: options.model,
    tier: options.tier,
    systemPrompt: options.systemPrompt
  });
}

module.exports = {
  ROOT,
  buildProjectSystemPrompt,
  callClaude,
  callDeepSeek,
  cleanupModelText,
  ensureDir,
  executeSkill,
  extractJsonArray,
  getCurrentMonthLabel,
  getCurrentMonthSlug,
  getCurrentWeekLabel,
  loadConfig,
  loadEnvFile,
  loadPipelineData,
  monthLabelFromSlug,
  normalizePipelineData,
  readText,
  registerMonth,
  resolveFromRoot,
  savePipelineData,
  slugify
};
