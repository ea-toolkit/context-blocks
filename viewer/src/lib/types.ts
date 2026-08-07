/**
 * Core type definitions for the Context Blocks viewer.
 * All data structures used across pages and components.
 */

/** A single entity loaded from a markdown file. */
export interface CBEntity {
  id: string;
  name: string;
  type: string;
  description: string;
  status: string;
  confidence: number;
  tags: string[];
  sourceDocuments: string[];
  layer: string;
  layerColor: string;
  typeLabel: string;
  typeIcon: string;
  body: string;
  openQuestions: string[];
  relationships: CBRelationship[];
  /** All raw frontmatter fields */
  fields: Record<string, unknown>;
}

/** A relationship extracted from entity frontmatter. */
export interface CBRelationship {
  type: string;
  targetId: string;
}

/** An edge in the entity graph. */
export interface CBEdge {
  source: string;
  target: string;
  type: string;
}

/** A question from the extraction, linked to its source entity. */
export interface CBQuestion {
  text: string;
  entityId: string;
  entityName: string;
  entityType: string;
  entityConfidence: number;
}

/** Entity health assessment. */
export interface CBEntityHealth {
  hasDescription: boolean;
  hasRelationships: boolean;
  hasSourceDocuments: boolean;
  isOrphan: boolean;
  isLowConfidence: boolean;
  brokenRefs: string[];
}

/** Domain-level narrative summary. */
export interface CBDomainSummary {
  narrative: string;
  keyRelationships: string;
  questions: string[];
}

/** Aggregate stats for the entire registry. */
export interface CBStats {
  totalEntities: number;
  totalEdges: number;
  totalQuestions: number;
  totalDocuments: number;
  avgConfidence: number;
  highConfidence: number;
  mediumConfidence: number;
  lowConfidence: number;
  entitiesByLayer: Record<string, number>;
  entitiesByType: Record<string, number>;
}

/** The complete registry — all entities, edges, and computed indexes. */
export interface CBRegistry {
  entities: Map<string, CBEntity>;
  edges: CBEdge[];
  domainSummary: CBDomainSummary;
  stats: CBStats;
  /** layer key → type key → entities */
  byLayer: Map<string, Map<string, CBEntity[]>>;
  /** All questions from all entities */
  allQuestions: CBQuestion[];
  /** Jargon entities (business + tech) */
  jargon: CBEntity[];
  /** Health per entity */
  health: Map<string, CBEntityHealth>;
  /** Block seed context (orientation markdown); empty if none. */
  seed: string;
}

/** Confidence tier for visual rendering. */
export type ConfidenceTier = 'solid' | 'muted' | 'sketched';

export function getConfidenceTier(confidence: number): ConfidenceTier {
  if (confidence >= 0.85) return 'solid';
  if (confidence >= 0.55) return 'muted';
  return 'sketched';
}

/** DDC score class. */
export type DDCClass = 'CLEAN' | 'INCOMPLETE' | 'MISSING';

/** A retrieval hop from eval results. */
export interface EvalHop {
  hop_number: number;
  entity_id: string;
  entity_name: string;
  entity_type: string;
  layer: string;
  matched_by: string;
  confidence: number;
  fused_score: number;
  relationship_from: string | null;
  relationship_type: string | null;
  gap_flag: boolean;
  gap_reason: string | null;
  found_by: string[] | null;
}

/** A gap detected during retrieval. */
export interface EvalGap {
  gap_type: string;
  entity_id: string | null;
  description: string;
  severity: string;
  suggested_action?: string;
}

/** A single eval result from eval-results.json or live API response. */
export interface EvalResult {
  question: string;
  source: string;
  source_file: string;
  layer_hint: string;
  topic: string;
  persona: string;
  score: string;
  ddc_class: DDCClass;
  answer: string;
  citations: string[];
  entities_retrieved: number;
  total_ms: number;
  trace_summary: string;
  hops: EvalHop[];
  gaps: EvalGap[];
  stage_trace?: StageTrace | null;
}

/** Stage-by-stage retrieval trace (from StageTrace). */
export interface StageTrace {
  vector_candidates: number;
  keyword_candidates: number;
  graph_candidates: number;
  fused_unique: number;
  after_dedup: number;
  context_selected: number;
  tokens_used: number;
  token_budget: number;
  intent_weights?: Record<string, number> | null;
  layer_priorities?: Record<string, number> | null;
  search_ms?: number | null;
  synthesis_ms?: number | null;
}

/** Aggregated eval stats. */
export interface EvalStats {
  total: number;
  clean: number;
  incomplete: number;
  missing: number;
  cleanPct: number;
  incompletePct: number;
  missingPct: number;
  perLayer: Record<string, { clean: number; incomplete: number; missing: number }>;
  perSource: Record<string, { clean: number; incomplete: number; missing: number }>;
  perPersona: Record<string, { clean: number; incomplete: number; missing: number }>;
}

/** Complete eval data loaded from JSON files. */
export interface EvalData {
  results: EvalResult[];
  stats: EvalStats;
}

/** A named eval run loaded from one result file. */
export interface EvalRun {
  id: string;
  label: string;
  filename: string;
  results: EvalResult[];
  stats: EvalStats;
}
