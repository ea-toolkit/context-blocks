/**
 * Meta-model config loader — reads the YAML config at build time.
 * Users edit meta-model.yaml to define their own entity types and layers.
 * The viewer renders whatever it finds — no hardcoded type/layer names.
 */
import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';

export interface LayerConfig {
  label: string;
  question: string;
  color: string;
  description: string;
}

export interface EntityTypeConfig {
  layer: string;
  directory: string;
  label: string;
  icon: string;
}

export interface MetaModelConfig {
  layers: Record<string, LayerConfig>;
  entity_types: Record<string, EntityTypeConfig>;
  relationship_fields: string[];
  standard_fields: string[];
}

let _config: MetaModelConfig | null = null;

export function loadMetaModel(): MetaModelConfig {
  if (_config) return _config;

  // Try multiple paths — works in both dev and build mode.
  // CB_META_MODEL lets a block point the viewer at its own custom ontology.
  const candidates = [
    process.env.CB_META_MODEL ? path.resolve(process.env.CB_META_MODEL) : null,
    path.join(process.cwd(), 'src', 'config', 'meta-model.yaml'),
    path.join(process.cwd(), 'viewer', 'src', 'config', 'meta-model.yaml'),
  ].filter((p): p is string => p !== null);

  for (const configPath of candidates) {
    if (fs.existsSync(configPath)) {
      const raw = fs.readFileSync(configPath, 'utf-8');
      _config = yaml.load(raw) as MetaModelConfig;
      return _config;
    }
  }

  throw new Error(`Meta-model config not found. Tried: ${candidates.join(', ')}`);
}

/** Get the layer key for an entity type. Returns 'unknown' if not found. */
export function getLayerForType(typeKey: string): string {
  const config = loadMetaModel();
  return config.entity_types[typeKey]?.layer ?? 'unknown';
}

/** Get layer config by key. Returns a fallback for unknown layers. */
export function getLayerConfig(layerKey: string): LayerConfig {
  const config = loadMetaModel();
  return config.layers[layerKey] ?? {
    label: layerKey,
    question: '',
    color: '#666666',
    description: '',
  };
}

/** Get entity type config. Returns a fallback for unknown types. */
export function getEntityTypeConfig(typeKey: string): EntityTypeConfig {
  const config = loadMetaModel();
  return config.entity_types[typeKey] ?? {
    layer: 'unknown',
    directory: typeKey,
    label: typeKey,
    icon: '?',
  };
}

/** Check if a frontmatter key is a relationship field. */
export function isRelationshipField(key: string): boolean {
  const config = loadMetaModel();
  return (config.relationship_fields ?? []).includes(key);
}

/** Check if a frontmatter key is a standard (non-relationship) field. */
export function isStandardField(key: string): boolean {
  const config = loadMetaModel();
  return (config.standard_fields ?? []).includes(key);
}
