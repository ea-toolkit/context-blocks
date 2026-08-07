/**
 * Entity Loader — reads entity markdown files and builds the registry at build time.
 *
 * Pattern: follows architecture-catalog's registry-loader.ts
 * - Reads all .md files from entity type directories
 * - Parses YAML frontmatter
 * - Extracts relationships from frontmatter keys
 * - Builds edges between entities
 * - Computes stats and health
 *
 * Graceful degradation:
 * - Missing frontmatter → skip file, log warning
 * - Unknown entity type → assign to "unknown" layer
 * - Broken refs → store but don't create edge
 * - Missing fields → empty string, never crash
 */
import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';
import {
  loadMetaModel,
  getLayerForType,
  getLayerConfig,
  getEntityTypeConfig,
  isRelationshipField,
  isStandardField,
} from '../config/meta-model-loader';
import type {
  CBEntity,
  CBEdge,
  CBQuestion,
  CBEntityHealth,
  CBDomainSummary,
  CBStats,
  CBRegistry,
  CBRelationship,
} from './types';

function findFirstDemoDomain(base: string): string | null {
  const syntheticDir = path.join(base, 'synthetic-domains');
  if (!fs.existsSync(syntheticDir)) return null;
  try {
    for (const domain of fs.readdirSync(syntheticDir)) {
      const outputDir = path.join(syntheticDir, domain, 'output');
      if (fs.existsSync(path.join(outputDir, 'entities'))) return outputDir;
    }
  } catch { /* ignore read errors */ }
  return null;
}

function resolveOutputDir(): string {
  if (process.env.CB_OUTPUT_DIR) return path.resolve(process.env.CB_OUTPUT_DIR);

  const projectRoot = path.resolve(process.cwd(), '..');
  const candidates = [
    path.join(projectRoot, 'output'),
    path.join(process.cwd(), 'output'),
    findFirstDemoDomain(projectRoot),
    findFirstDemoDomain(process.cwd()),
  ];
  for (const dir of candidates) {
    if (dir && fs.existsSync(dir)) return dir;
  }

  console.warn('[entity-loader] No output directory found. Set CB_OUTPUT_DIR or place output in <project>/output/');
  return path.join(projectRoot, 'output');
}

const OUTPUT_DIR = resolveOutputDir();

/** Parse YAML frontmatter from markdown content. Returns [frontmatter, body]. */
function parseFrontmatter(content: string): [Record<string, unknown>, string] {
  const match = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!match) return [{}, content];

  try {
    const fm = yaml.load(match[1]) as Record<string, unknown>;
    return [fm ?? {}, match[2].trim()];
  } catch {
    return [{}, content];
  }
}

/** Extract open questions from entity markdown body. */
function extractOpenQuestions(body: string): string[] {
  const questions: string[] = [];
  const section = body.match(/## Open Questions\s*\n([\s\S]*?)(?=\n## |\n$|$)/);
  if (!section) return questions;

  for (const line of section[1].split('\n')) {
    const trimmed = line.replace(/^[-*]\s*/, '').trim();
    if (trimmed && trimmed.length > 5) {
      questions.push(trimmed);
    }
  }
  return questions;
}

/** Extract relationships from entity frontmatter. */
function extractRelationships(fm: Record<string, unknown>): CBRelationship[] {
  const rels: CBRelationship[] = [];

  for (const [key, value] of Object.entries(fm)) {
    if (isStandardField(key)) continue;

    // Check if it's a known relationship field OR an unknown field with entity-id-like values
    const isKnownRel = isRelationshipField(key);
    if (!isKnownRel && typeof value !== 'string' && !Array.isArray(value)) continue;

    const targets = Array.isArray(value) ? value : [value];
    for (const target of targets) {
      if (typeof target === 'string' && target.length > 0) {
        rels.push({ type: key, targetId: target });
      }
    }
  }

  return rels;
}

/** Load a single entity from a markdown file. Returns null on failure. */
function loadEntityFile(filepath: string, typeKey: string): CBEntity | null {
  try {
    const content = fs.readFileSync(filepath, 'utf-8');
    const [fm, body] = parseFrontmatter(content);

    const id = (fm.id as string) || path.basename(filepath, '.md');
    const name = (fm.name as string) || id;
    const typeConfig = getEntityTypeConfig(typeKey);
    const layerKey = getLayerForType(typeKey);
    const layerConfig = getLayerConfig(layerKey);

    return {
      id,
      name,
      type: typeKey,
      description: (fm.description as string) || '',
      status: (fm.status as string) || 'active',
      confidence: typeof fm.confidence === 'number' ? fm.confidence : 0.5,
      tags: Array.isArray(fm.tags) ? fm.tags.map(String) : [],
      sourceDocuments: Array.isArray(fm.source_documents) ? fm.source_documents.map(String) : [],
      layer: layerKey,
      layerColor: layerConfig.color,
      typeLabel: typeConfig.label,
      typeIcon: typeConfig.icon,
      body,
      openQuestions: extractOpenQuestions(body),
      relationships: extractRelationships(fm),
      fields: fm,
    };
  } catch {
    console.warn(`[entity-loader] Failed to load: ${filepath}`);
    return null;
  }
}

/** Load the domain summary from analysis-report.md. */
function loadDomainSummary(): CBDomainSummary {
  const reportPath = path.join(OUTPUT_DIR, 'analysis-report.md');
  const fallback: CBDomainSummary = {
    narrative: 'No analysis report found. Run the pipeline to generate domain understanding.',
    keyRelationships: '',
    questions: [],
  };

  if (!fs.existsSync(reportPath)) return fallback;

  try {
    const content = fs.readFileSync(reportPath, 'utf-8');

    // Extract domain understanding section
    const narrativeMatch = content.match(
      /## Current Domain Understanding\s*\n([\s\S]*?)(?=\n## |---|\n### Key Relationships)/
    );
    const narrative = narrativeMatch?.[1]?.trim() || fallback.narrative;

    // Extract key relationships
    const relMatch = content.match(
      /### Key Relationships\s*\n([\s\S]*?)(?=\n## |---|\n### )/
    );
    const keyRelationships = relMatch?.[1]?.trim() || '';

    // Extract open questions
    const qMatch = content.match(
      /### Open Questions\s*\n([\s\S]*?)(?=\n## |---|\n$)/
    );
    const questions: string[] = [];
    if (qMatch) {
      for (const line of qMatch[1].split('\n')) {
        const q = line.replace(/^[-*]\s*/, '').trim();
        if (q && q.length > 5) questions.push(q);
      }
    }

    return { narrative, keyRelationships, questions };
  } catch {
    return fallback;
  }
}

/** Build the complete registry from entity files and config. */
export async function loadRegistry(): Promise<CBRegistry> {
  const config = loadMetaModel();
  const entitiesDir = path.join(OUTPUT_DIR, 'entities');

  const entities = new Map<string, CBEntity>();
  const edges: CBEdge[] = [];
  const allQuestions: CBQuestion[] = [];
  const health = new Map<string, CBEntityHealth>();
  const byLayer = new Map<string, Map<string, CBEntity[]>>();

  // Initialize byLayer structure from config
  for (const layerKey of Object.keys(config.layers)) {
    byLayer.set(layerKey, new Map());
  }

  // Scan entity type directories
  for (const [typeKey, typeConfig] of Object.entries(config.entity_types)) {
    const typeDir = path.join(entitiesDir, typeConfig.directory);
    if (!fs.existsSync(typeDir)) continue;

    const files = fs.readdirSync(typeDir).filter(f => f.endsWith('.md') && !f.startsWith('_'));

    for (const file of files) {
      const entity = loadEntityFile(path.join(typeDir, file), typeKey);
      if (!entity) continue;

      entities.set(entity.id, entity);

      // Index by layer → type
      const layerMap = byLayer.get(entity.layer) ?? new Map();
      const typeList = layerMap.get(typeKey) ?? [];
      typeList.push(entity);
      layerMap.set(typeKey, typeList);
      byLayer.set(entity.layer, layerMap);

      // Collect questions
      for (const q of entity.openQuestions) {
        allQuestions.push({
          text: q,
          entityId: entity.id,
          entityName: entity.name,
          entityType: entity.type,
          entityConfidence: entity.confidence,
        });
      }
    }
  }

  // Build edges from relationships
  const entityIds = new Set(entities.keys());
  for (const entity of entities.values()) {
    const brokenRefs: string[] = [];

    for (const rel of entity.relationships) {
      if (entityIds.has(rel.targetId)) {
        edges.push({
          source: entity.id,
          target: rel.targetId,
          type: rel.type,
        });
      } else {
        brokenRefs.push(rel.targetId);
      }
    }

    // Compute health
    health.set(entity.id, {
      hasDescription: entity.description.length > 0,
      hasRelationships: entity.relationships.length > 0,
      hasSourceDocuments: entity.sourceDocuments.length > 0,
      isOrphan: entity.relationships.length === 0,
      isLowConfidence: entity.confidence < 0.55,
      brokenRefs,
    });
  }

  // Compute stats
  const confidences = [...entities.values()].map(e => e.confidence);
  const stats: CBStats = {
    totalEntities: entities.size,
    totalEdges: edges.length,
    totalQuestions: allQuestions.length,
    totalDocuments: new Set([...entities.values()].flatMap(e => e.sourceDocuments)).size,
    avgConfidence: confidences.length ? confidences.reduce((a, b) => a + b, 0) / confidences.length : 0,
    highConfidence: confidences.filter(c => c >= 0.85).length,
    mediumConfidence: confidences.filter(c => c >= 0.55 && c < 0.85).length,
    lowConfidence: confidences.filter(c => c < 0.55).length,
    entitiesByLayer: {},
    entitiesByType: {},
  };

  for (const [layerKey, typeMap] of byLayer) {
    let layerTotal = 0;
    for (const [typeKey, typeEntities] of typeMap) {
      stats.entitiesByType[typeKey] = typeEntities.length;
      layerTotal += typeEntities.length;
    }
    stats.entitiesByLayer[layerKey] = layerTotal;
  }

  // Sort questions by priority (low confidence entities first)
  allQuestions.sort((a, b) => a.entityConfidence - b.entityConfidence);

  // Build jargon list
  const jargon = [...entities.values()]
    .filter(e => e.type === 'jargon-business' || e.type === 'jargon-tech')
    .sort((a, b) => a.name.localeCompare(b.name));

  const domainSummary = loadDomainSummary();

  console.log(`[context-blocks] Registry loaded: ${entities.size} entities, ${edges.length} edges, ${allQuestions.length} questions`);

  // Seed context: an explicit CB_SEED_FILE (from the multi-block build) wins,
  // else the block's own seed-context.md sitting beside entities/.
  const seedPath = process.env.CB_SEED_FILE
    ? path.resolve(process.env.CB_SEED_FILE)
    : path.join(OUTPUT_DIR, 'seed-context.md');
  let seed = '';
  try {
    if (fs.existsSync(seedPath)) seed = fs.readFileSync(seedPath, 'utf-8');
  } catch { /* no seed context for this block */ }

  return {
    entities,
    edges,
    domainSummary,
    stats,
    byLayer,
    allQuestions,
    jargon,
    health,
    seed,
  };
}
