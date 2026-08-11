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
  :root {
    --bg:#0f1117; --surface:#161922; --surface-hover:#1c2030;
    --border:rgba(255,255,255,0.08); --border-hover:rgba(124,92,252,0.55);
    --text:#e2e8f0; --muted:#94a3b8; --faint:#475569;
    --primary:#7c5cfc; --primary-muted:rgba(124,92,252,0.14);
    --font:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
    --mono:'SF Mono','Fira Code','JetBrains Mono',monospace;
  }
  @media (prefers-color-scheme: light) {
    :root { --bg:#f8fafc; --surface:#ffffff; --surface-hover:#f1f5f9;
      --border:rgba(15,17,23,0.10); --text:#0f1117; --muted:#475569; --faint:#94a3b8;
      --primary-muted:rgba(124,92,252,0.10); }
  }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--text); font-family:var(--font);
    min-height:100vh; display:flex; align-items:center; justify-content:center; padding:32px; }
  .wrap { width:100%; max-width:600px; }
  .brand { display:flex; align-items:center; gap:12px; margin-bottom:8px; }
  .logo { display:grid; grid-template-columns:repeat(3,7px); grid-template-rows:repeat(3,7px); gap:3px; }
  .logo i { width:7px; height:7px; border-radius:2px; background:var(--primary); }
  .logo i:nth-child(3n+2) { background:var(--primary-muted); }
  h1 { font-size:22px; font-weight:600; letter-spacing:-0.02em; }
  p.sub { color:var(--muted); font-size:14px; margin:0 0 28px 34px; }
  .grid { display:flex; flex-direction:column; gap:12px; }
  .card { display:flex; align-items:center; gap:14px; padding:20px 22px; background:var(--surface);
    border:1px solid var(--border); border-radius:12px; text-decoration:none; color:var(--text);
    transition:border-color 160ms, background 160ms, transform 160ms; }
  .card:hover { background:var(--surface-hover); border-color:var(--border-hover); transform:translateY(-1px); }
  .dot { width:9px; height:9px; border-radius:3px; background:var(--primary);
    box-shadow:0 0 0 4px var(--primary-muted); flex-shrink:0; }
  .name { font-size:16px; font-weight:600; flex:1; }
  .meta { color:var(--muted); font-size:12px; font-family:var(--mono); }
  .foot { margin-top:26px; color:var(--faint); font-size:12px; text-align:center; font-family:var(--mono); }
</style>
</head>
<body>
  <div class="wrap">
    <div class="brand">
      <span class="logo"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>
      <h1>Context Blocks</h1>
    </div>
    <p class="sub">${blocks.length} block${blocks.length === 1 ? '' : 's'} in this workspace — select one to explore.</p>
    <div class="grid">
${cards}
    </div>
    <p class="foot">${process.env.CB_WORKSPACE || 'default'} workspace</p>
  </div>
</body>
</html>
`;
fs.writeFileSync(path.join(distDir, 'index.html'), indexHtml);
console.log(`✓ wrote parent dist/index.html (${blocks.length} blocks)`);
console.log(`\nServe with:  cd viewer && npx serve dist   → open the parent page, switch via sidebar dropdown.`);
