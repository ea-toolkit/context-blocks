/**
 * Types mirroring the Studio API (context_blocks/studio_api.py) response models.
 * These are wire DTOs — field names match the JSON the API returns (snake_case).
 */

export interface OntologySummary {
  source: string;
  types: string[];
  layers: string[];
  relationship_field_count: number;
}

export interface BlockSummary {
  name: string;
  description: string;
  label: string;
  ontology: string;
  output: string;
  seed_context: string;
  model: string;
  entity_count: number;
  created_at: string;
  last_updated: string;
  output_dir: string;
}

export interface BlockDetail extends BlockSummary {
  ontology_detail: OntologySummary;
}

export interface EntityListItem {
  id: string;
  type: string;
  name: string;
  path: string;
}

export interface AddEntityResponse {
  id: string;
  type: string;
  path: string;
  warnings: string[];
}

export interface ArtifactInfo {
  filename: string;
  path: string;
  size: number;
  content_type: string;
}

export interface GraphNode {
  id: string;
  name: string;
  type: string;
  type_label: string;
  type_icon: string;
  layer: string;
  layer_color: string;
  confidence: number;
  description: string;
  relationship_count: number;
  incoming_count: number;
  outgoing_count: number;
}

export interface GraphEdge {
  source: string;
  type: string;
  target: string;
}

export interface GraphLayer {
  key: string;
  label: string;
  color: string;
}

export interface GraphEntityType {
  key: string;
  label: string;
  layer: string;
}

export interface BlockGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
  layers: GraphLayer[];
  entity_types: GraphEntityType[];
}

export interface OntologyTypeInfo {
  key: string;
  label: string;
  layer: string;
}

export interface OntologyLayerInfo {
  key: string;
  label: string;
  color: string;
}

export interface BlockOntology {
  source: string;
  layers: OntologyLayerInfo[];
  types: OntologyTypeInfo[];
  relationship_fields: string[];
}

export interface StudioHealth {
  status: string;
  root: string;
  blocks: number;
}

/** Payload for POST /blocks (mirrors CreateBlockRequest). */
export interface CreateBlockPayload {
  name: string;
  description?: string;
  label?: string;
  model?: string;
  ontology?: string;
  ontology_yaml?: string;
  seed_context?: string;
}

/** Live metrics for a block (GET /blocks/{name}/metrics) — the demand log + change log. */
export interface WorkEffortSummary {
  id: string;
  intent: string;
  outcome: string | null;
  call_count: number;
  gap_count: number;
  started_at: string;
  ended_at: string | null;
}

export interface ChangeEvent {
  at: string;
  entity_id: string;
  entity_type: string;
  action: string;
  actor: string;
  work_effort_id: string;
  summary: string;
}

export interface GapEntry {
  tool: string;
  args: Record<string, unknown>;
  summary: string;
  at: string;
  intent: string;
}

export interface BlockMetrics {
  block: string;
  work_efforts: {
    total: number;
    with_gaps: number;
    total_calls: number;
    total_gaps: number;
    gap_rate: number;
    outcomes: { outcome: string; count: number }[];
    recent: WorkEffortSummary[];
  };
  top_entities: { entity_id: string; hits: number }[];
  gaps: GapEntry[];
  changes: {
    total: number;
    by_action: Record<string, number>;
    by_actor: { actor: string; count: number }[];
    recent: ChangeEvent[];
  };
}
