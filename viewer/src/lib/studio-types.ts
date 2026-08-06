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
