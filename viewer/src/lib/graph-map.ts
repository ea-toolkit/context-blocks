import type { DomainMapProps } from '../components/map/DomainMap';
import type { BlockGraph } from './studio-types';

/** Map the live graph API response (snake_case DTOs) to DomainMap's props. */
export function blockGraphToDomainMapProps(data: BlockGraph): DomainMapProps {
  return {
    entities: data.nodes.map((n) => ({
      id: n.id,
      name: n.name,
      type: n.type,
      typeLabel: n.type_label,
      typeIcon: n.type_icon,
      layer: n.layer,
      layerColor: n.layer_color,
      confidence: n.confidence,
      description: n.description,
      relationshipCount: n.relationship_count,
      incomingCount: n.incoming_count,
      outgoingCount: n.outgoing_count,
    })),
    edges: data.edges.map((e) => ({ source: e.source, target: e.target, type: e.type })),
    layers: data.layers.map((l) => ({ key: l.key, label: l.label, color: l.color })),
    entityTypes: data.entity_types.map((t) => ({ key: t.key, label: t.label, layer: t.layer })),
  };
}
