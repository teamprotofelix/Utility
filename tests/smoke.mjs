import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
const root = path.resolve(import.meta.dirname, '..');
const registryCode = fs.readFileSync(path.join(root, 'tools.js'), 'utf8');
const ctx = { window: {} };
vm.runInNewContext(registryCode, ctx);
const tools = ctx.window.UTILITY_TOOLS;
assert.ok(Array.isArray(tools) && tools.length >= 1, 'Must have at least one tool');
assert.equal(new Set(tools.map(x => x.id)).size, tools.length, 'IDs must be unique');
for (const tool of tools) {
  assert.match(tool.id, /^[a-z0-9-]+$/);
  assert.ok(tool.name && tool.description && tool.subtitle && Array.isArray(tool.category));
  for (const key of ['url', 'repository']) {
    if (tool[key]) assert.equal(new URL(tool[key]).protocol, 'https:');
  }
  assert.ok(fs.existsSync(path.join(root, tool.image)), `Missing image: ${tool.image}`);
}
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
assert.match(html, /id="tool-grid"/);
assert.match(html, /id="search-tools"/);
assert.match(html, /id="filters"/);
assert.match(html, /rel="noopener noreferrer"/);
for (const asset of html.matchAll(/(?:src|href)="(\.\/assets\/[^\"]+)"/g)) {
  assert.ok(fs.existsSync(path.join(root, asset[1])), `Missing asset: ${asset[1]}`);
}
assert.equal(fs.readFileSync(path.join(root, 'CNAME'), 'utf8').trim(), 'util.moip.ai.kr');
console.log(`PASS: ${tools.length} tool(s), assets, HTTPS links, domain and HTML hooks`);
