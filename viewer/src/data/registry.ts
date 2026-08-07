/**
 * Registry — build-time data singleton.
 *
 * Loaded once during Astro build. All pages and components
 * consume data from here. No direct file reads in components.
 *
 * Pattern: follows architecture-catalog's data/registry.ts
 */
import { loadRegistry } from '../lib/entity-loader';
import type { CBEntity, CBRegistry, CBQuestion } from '../lib/types';

const _registry: CBRegistry = await loadRegistry();

// ── Exports ──

export const entities = _registry.entities;
export const edges = _registry.edges;
export const domainSummary = _registry.domainSummary;
export const stats = _registry.stats;
export const byLayer = _registry.byLayer;
export const allQuestions = _registry.allQuestions;
export const jargon = _registry.jargon;
export const health = _registry.health;
export const seed = _registry.seed;

// ── Helpers ──

export function getEntityById(id: string): CBEntity | undefined {
  return entities.get(id);
}

export function getEntitiesByType(typeKey: string): CBEntity[] {
  for (const typeMap of byLayer.values()) {
    const list = typeMap.get(typeKey);
    if (list) return list;
  }
  return [];
}

export function getEntitiesByLayer(layerKey: string): CBEntity[] {
  const typeMap = byLayer.get(layerKey);
  if (!typeMap) return [];
  return [...typeMap.values()].flat();
}

export function getRelatedEntities(id: string): CBEntity[] {
  const entity = entities.get(id);
  if (!entity) return [];

  const relatedIds = new Set<string>();
  // Outgoing relationships
  for (const rel of entity.relationships) {
    relatedIds.add(rel.targetId);
  }
  // Incoming relationships
  for (const edge of edges) {
    if (edge.target === id) relatedIds.add(edge.source);
  }

  return [...relatedIds]
    .map(rid => entities.get(rid))
    .filter((e): e is CBEntity => e !== undefined);
}

/** Get the top N questions sorted by priority (lowest confidence first). */
export function getTopQuestions(n: number): CBQuestion[] {
  return allQuestions.slice(0, n);
}

/** Get questions for a specific entity. */
export function getEntityQuestions(entityId: string): CBQuestion[] {
  return allQuestions.filter(q => q.entityId === entityId);
}

/** Get entities with health issues. */
export function getLintIssues(): Array<{ entity: CBEntity; issues: string[] }> {
  const results: Array<{ entity: CBEntity; issues: string[] }> = [];

  for (const [id, h] of health) {
    const entity = entities.get(id);
    if (!entity) continue;

    const issues: string[] = [];
    if (!h.hasDescription) issues.push('Missing description');
    if (h.isOrphan) issues.push('No relationships (orphan)');
    if (!h.hasSourceDocuments) issues.push('No source documents');
    if (h.isLowConfidence) issues.push(`Low confidence (${(entity.confidence * 100).toFixed(0)}%)`);
    if (h.brokenRefs.length > 0) issues.push(`${h.brokenRefs.length} broken reference(s)`);

    if (issues.length > 0) {
      results.push({ entity, issues });
    }
  }

  return results.sort((a, b) => b.issues.length - a.issues.length);
}
