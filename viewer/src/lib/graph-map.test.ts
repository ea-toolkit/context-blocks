import { describe, expect, it } from 'vitest';

import { blockGraphToDomainMapProps } from './graph-map';
import type { BlockGraph } from './studio-types';

const g: BlockGraph = {
  nodes: [
    {
      id: 'a',
      name: 'A',
      type: 'incident',
      type_label: 'Incidents',
      type_icon: 'IN',
      layer: 'behavioral',
      layer_color: '#1ABC9C',
      confidence: 0.9,
      description: 'd',
      relationship_count: 1,
      incoming_count: 0,
      outgoing_count: 1,
    },
  ],
  edges: [{ source: 'a', target: 'b', type: 'affects' }],
  layers: [{ key: 'behavioral', label: 'Behavioral', color: '#1ABC9C' }],
  entity_types: [{ key: 'incident', label: 'Incidents', layer: 'behavioral' }],
};

describe('blockGraphToDomainMapProps', () => {
  it('maps snake_case DTOs to DomainMap camelCase props', () => {
    const p = blockGraphToDomainMapProps(g);
    expect(p.entities[0]).toMatchObject({
      id: 'a',
      typeLabel: 'Incidents',
      typeIcon: 'IN',
      layerColor: '#1ABC9C',
      outgoingCount: 1,
      relationshipCount: 1,
    });
    expect(p.edges[0]).toEqual({ source: 'a', target: 'b', type: 'affects' });
    expect(p.layers[0]).toEqual({ key: 'behavioral', label: 'Behavioral', color: '#1ABC9C' });
    expect(p.entityTypes[0]).toEqual({ key: 'incident', label: 'Incidents', layer: 'behavioral' });
  });
});
