/**
 * Eval data loader — discovers all eval-results*.json files and returns named runs.
 * Build-time only. Components access data via the Astro page, not this file directly.
 */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import type { EvalResult, EvalStats, EvalData, EvalRun, DDCClass } from '../lib/types';

function findFirstDemoDomain(base: string): string | null {
  const syntheticDir = join(base, 'synthetic-domains');
  if (!existsSync(syntheticDir)) return null;
  try {
    for (const domain of readdirSync(syntheticDir)) {
      const outputDir = join(syntheticDir, domain, 'output');
      if (existsSync(join(outputDir, 'entities'))) return outputDir;
    }
  } catch { /* ignore */ }
  return null;
}

function resolveOutputDir(): string {
  if (process.env.CB_OUTPUT_DIR) return process.env.CB_OUTPUT_DIR;

  const projectRoot = join(process.cwd(), '..');
  const candidates = [
    join(projectRoot, 'output'),
    join(process.cwd(), 'output'),
    findFirstDemoDomain(projectRoot),
    findFirstDemoDomain(process.cwd()),
  ];
  for (const dir of candidates) {
    if (dir && existsSync(dir)) return dir;
  }
  return join(projectRoot, 'output');
}

const OUTPUT_DIR = resolveOutputDir();

function deriveRunLabel(filename: string): string {
  const name = filename
    .replace(/^eval-results-?/, '')
    .replace(/\.json$/, '');
  if (!name) return 'Latest';
  return name
    .split(/[-_]/)
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

function computeStats(results: EvalResult[]): EvalStats {
  const total = results.length;
  const clean = results.filter(r => r.ddc_class === 'CLEAN').length;
  const incomplete = results.filter(r => r.ddc_class === 'INCOMPLETE').length;
  const missing = results.filter(r => r.ddc_class === 'MISSING').length;

  const perLayer: EvalStats['perLayer'] = {};
  const perSource: EvalStats['perSource'] = {};
  const perPersona: EvalStats['perPersona'] = {};

  for (const r of results) {
    const layer = r.layer_hint || 'unclassified';
    if (!perLayer[layer]) perLayer[layer] = { clean: 0, incomplete: 0, missing: 0 };
    perLayer[layer][r.ddc_class.toLowerCase() as 'clean' | 'incomplete' | 'missing']++;

    if (!perSource[r.source]) perSource[r.source] = { clean: 0, incomplete: 0, missing: 0 };
    perSource[r.source][r.ddc_class.toLowerCase() as 'clean' | 'incomplete' | 'missing']++;

    if (r.persona) {
      if (!perPersona[r.persona]) perPersona[r.persona] = { clean: 0, incomplete: 0, missing: 0 };
      perPersona[r.persona][r.ddc_class.toLowerCase() as 'clean' | 'incomplete' | 'missing']++;
    }
  }

  return {
    total,
    clean,
    incomplete,
    missing,
    cleanPct: total > 0 ? Math.round(clean / total * 100) : 0,
    incompletePct: total > 0 ? Math.round(incomplete / total * 100) : 0,
    missingPct: total > 0 ? Math.round(missing / total * 100) : 0,
    perLayer,
    perSource,
    perPersona,
  };
}

/** Load the primary eval data (eval-results.json). */
export function loadEvalData(): EvalData | null {
  const evalPath = join(OUTPUT_DIR, 'eval-results.json');

  if (!existsSync(evalPath)) {
    console.warn(`[eval-loader] No eval results found at ${evalPath}`);
    return null;
  }

  const raw = readFileSync(evalPath, 'utf-8');
  const results: EvalResult[] = JSON.parse(raw);

  if (!results.length) {
    return null;
  }

  const stats = computeStats(results);
  return { results, stats };
}

/** Discover all eval-results*.json files and return as named runs. */
export function loadAllEvalRuns(): EvalRun[] {
  if (!existsSync(OUTPUT_DIR)) return [];

  const files = readdirSync(OUTPUT_DIR)
    .filter(f => f.startsWith('eval-results') && f.endsWith('.json'))
    .sort();

  const runs: EvalRun[] = [];

  for (const file of files) {
    try {
      const raw = readFileSync(join(OUTPUT_DIR, file), 'utf-8');
      const results: EvalResult[] = JSON.parse(raw);
      if (!results.length) continue;

      const label = deriveRunLabel(file);
      runs.push({
        id: file.replace('.json', ''),
        label,
        filename: file,
        results,
        stats: computeStats(results),
      });
    } catch {
      console.warn(`[eval-loader] Failed to parse ${file}`);
    }
  }

  return runs;
}
