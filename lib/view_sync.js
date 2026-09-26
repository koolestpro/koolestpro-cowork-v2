const fs = require('fs');
const path = require('path');

const { loadConfig, resolveFromRoot } = require('./cowork_runtime');

function escapeScriptJson(value) {
  return JSON.stringify(value, null, 2).replace(/<\/script/gi, '<\\/script');
}

function replaceMarkedBlock(filePath, startMarker, endMarker, replacement) {
  const source = fs.readFileSync(filePath, 'utf8');
  const start = source.indexOf(startMarker);
  const end = source.indexOf(endMarker);

  if (start === -1 || end === -1 || end < start) {
    throw new Error(`Missing sync markers in ${path.basename(filePath)}`);
  }

  const next = [
    source.slice(0, start + startMarker.length),
    '\n',
    replacement.trim(),
    '\n',
    source.slice(end)
  ].join('');

  fs.writeFileSync(filePath, next);
}

function syncEmbeddedViews(pipeline) {
  const config = loadConfig();
  const payload = {
    meta: pipeline.meta,
    months: pipeline.months,
    items: pipeline.items
  };

  const block = [
    '<script id="cowork-sync-data" type="application/json">',
    escapeScriptJson(payload),
    '</script>'
  ].join('\n');

  replaceMarkedBlock(
    resolveFromRoot(config.paths.content_pipeline_html),
    '<!-- COWORK_SYNC_DATA_START -->',
    '<!-- COWORK_SYNC_DATA_END -->',
    block
  );

  replaceMarkedBlock(
    resolveFromRoot(config.paths.content_system_html),
    '<!-- COWORK_SYNC_DATA_START -->',
    '<!-- COWORK_SYNC_DATA_END -->',
    block
  );
}

module.exports = { syncEmbeddedViews };
