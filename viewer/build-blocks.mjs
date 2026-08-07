/**
 * Multi-block viewer build (Option A).
 *
 * Reads the block registry (blocks.yaml — gitignored), builds the viewer once
 * per block into dist/<block>/ (each with its own base path, entities, and
 * ontology), then writes a parent dist/index.html linking to each block.
 *
 * All real block names flow from the gitignored blocks.yaml into the gitignored
 * dist/ only — nothing is hardcoded here.
 *
 *   node build-blocks.mjs        (from viewer/)
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';
import yaml from 'js-yaml';

const viewerDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(viewerDir, '..');
const distDir = path.join(viewerDir, 'dist');

// Workspace root: CB_PROJECT_ROOT wins, else CB_WORKSPACE (public|private) →
// the configured path, else the repo root (legacy). Mirrors the Python
// resolve_workspace_root so the build sees the same blocks the CLI/Studio do.
function resolveWorkspaceRoot() {
  if (process.env.CB_PROJECT_ROOT) return path.resolve(process.env.CB_PROJECT_ROOT);
  const ws = (process.env.CB_WORKSPACE || '').trim().toLowerCase();
  if (ws === 'public') return path.resolve(repoRoot, process.env.CB_WORKSPACE_PUBLIC || 'synthetic-domains');
  if (ws === 'private') return path.resolve(repoRoot, process.env.CB_WORKSPACE_PRIVATE || '.private/blocks');
  return repoRoot;
}
const wsRoot = resolveWorkspaceRoot();

function titleCase(id) {
  return id.split(/[-_]/).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

// --- load registry ---------------------------------------------------------
const registryPath = path.join(wsRoot, 'blocks.yaml');
if (!fs.existsSync(registryPath)) {
  console.error(`blocks.yaml not found at ${registryPath}`);
  process.exit(1);
}
console.log(`workspace: ${process.env.CB_WORKSPACE || '(legacy)'} → ${wsRoot}`);
const registry = yaml.load(fs.readFileSync(registryPath, 'utf-8')) || {};

const blocks = Object.entries(registry).map(([id, cfg]) => {
  cfg = cfg || {};
  // entities dir: explicit `output`, else <root>/<id> (must contain entities/)
  const outputDir = path.resolve(wsRoot, cfg.output || id);
  const ontology = cfg.ontology && cfg.ontology !== 'default'
    ? path.resolve(wsRoot, cfg.ontology)
    : null;
  const seedFile = cfg.seed_context ? path.resolve(wsRoot, cfg.seed_context) : null;
  return { id, label: cfg.label || titleCase(id), base: `/${id}/`, outputDir, ontology, seedFile };
}).filter(b => {
  const ok = fs.existsSync(path.join(b.outputDir, 'entities'));
  if (!ok) console.warn(`⚠ skipping "${b.id}" — no entities/ at ${b.outputDir}`);
  return ok;
});

if (!blocks.length) { console.error('No buildable blocks found.'); process.exit(1); }

const manifest = JSON.stringify(blocks.map(b => ({ id: b.id, label: b.label, base: b.base })));

// --- build each block ------------------------------------------------------
fs.rmSync(distDir, { recursive: true, force: true });
console.log(`Building ${blocks.length} block(s): ${blocks.map(b => b.id).join(', ')}\n`);

for (const b of blocks) {
  console.log(`── building "${b.id}" → dist/${b.id}/`);
  const env = {
    ...process.env,
    CB_OUTPUT_DIR: b.outputDir,
    CB_BLOCK_BASE: b.base,
    CB_OUT_DIR: `./dist/${b.id}`,
    CB_BLOCKS_MANIFEST: manifest,
  };
  if (b.ontology) env.CB_META_MODEL = b.ontology;
  else delete env.CB_META_MODEL;
  if (b.seedFile) env.CB_SEED_FILE = b.seedFile;
  else delete env.CB_SEED_FILE;
  const t = Date.now();
  execSync('npx astro build', { cwd: viewerDir, env, stdio: 'inherit' });
  console.log(`   done in ${((Date.now() - t) / 1000).toFixed(1)}s\n`);
}

// --- parent index ----------------------------------------------------------
const cards = blocks.map(b => {
  const count = fs.readdirSync(path.join(b.outputDir, 'entities'), { recursive: true })
    .filter(f => String(f).endsWith('.md')).length;
  return `      <a class="card" href="${b.base}">
        <span class="dot"></span>
        <span class="name">${b.label}</span>
        <span class="meta">${count} entities</span>
      </a>`;
}).join('\n');

const indexHtml = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Context Blocks</title>
<style>
  :root { --bg:#1a1a1a; --card:#222; --text:#e0e0e0; --muted:#999; --border:#444; --accent:#6b8cae; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--text); font-family:system-ui,-apple-system,sans-serif; padding:48px 24px; }
  .wrap { max-width:720px; margin:0 auto; }
  h1 { font-family:'JetBrains Mono',monospace; font-size:24px; letter-spacing:-0.5px; margin:0 0 4px; }
  p.sub { color:var(--muted); margin:0 0 32px; font-size:14px; }
  .grid { display:grid; gap:16px; }
  .card { display:flex; align-items:center; gap:12px; padding:20px; background:var(--card); border:2px solid var(--border); text-decoration:none; color:var(--text); transition:border-color 150ms; }
  .card:hover { border-color:var(--accent); }
  .dot { width:10px; height:10px; background:var(--accent); flex-shrink:0; }
  .name { font-family:'JetBrains Mono',monospace; font-size:16px; flex:1; }
  .meta { color:var(--muted); font-size:13px; }
</style>
</head>
<body>
  <div class="wrap">
    <h1>Context Blocks</h1>
    <p class="sub">${blocks.length} block${blocks.length === 1 ? '' : 's'} — select one to explore.</p>
    <div class="grid">
${cards}
    </div>
  </div>
</body>
</html>
`;
fs.writeFileSync(path.join(distDir, 'index.html'), indexHtml);
console.log(`✓ wrote parent dist/index.html (${blocks.length} blocks)`);
console.log(`\nServe with:  cd viewer && npx serve dist   → open the parent page, switch via sidebar dropdown.`);
