import { describe, expect, it } from 'vitest';

import type { DomainMapProps } from '../components/map/DomainMap';
import { induceTypeGraph } from './type-graph';

const props: DomainMapProps = {
  entities: [
    { id: 'i1', name: 'Inc1', type: 'incident', typeLabel: 'Incidents', typeIcon: 'IN', layer: 'behavioral', layerColor: '#1ABC9C', confidence: 1, description: '', relationshipCount: 1, incomingCount: 0, outgoingCount: 1 },
    { id: 'i2', name: 'Inc2', type: 'incident', typeLabel: 'Incidents', typeIcon: 'IN', layer: 'behavioral', layerColor: '#1ABC9C', confidence: 1, description: '', relationshipCount: 1, incomingCount: 0, outgoingCount: 1 },
    { id: 's1', name: 'Svc1', type: 'service', typeLabel: 'Services', typeIcon: 'SV', layer: 'structural', layerColor: '#4A90E2', confidence: 1, description: '', relationshipCount: 2, incomingCount: 2, outgoingCount: 0 },
  ],
  edges: [
    { source: 'i1', target: 's1', type: 'affects' },
    { source: 'i2', target: 's1', type: 'affects' },
  ],
  layers: [],
  entityTypes: [],
};

describe('induceTypeGraph', () => {
  it('collapses entities to one node per type with counts', () => {
    const g = induceTypeGraph(props);
    const byType = Object.fromEntries(g.entities.map((n) => [n.id, n]));
    expect(new Set(g.entities.map((n) => n.id))).toEqual(new Set(['incident', 'service']));
    expect(byType['incident'].description).toBe('2 entities');
    expect(byType['service'].description).toBe('1 entity');
    expect(byType['incident'].name).toBe('Incidents');
  });

  it('collapses edges to distinct type->type relationships', () => {
    const g = induceTypeGraph(props);
    expect(g.edges).toHaveLength(1); // two incident->service affects edges → one
    expect(g.edges[0]).toMatchObject({ source: 'incident', target: 'service', type: 'affects' });
  });

  it('computes type-level degree', () => {
    const g = induceTypeGraph(props);
    const byType = Object.fromEntries(g.entities.map((n) => [n.id, n]));
    expect(byType['incident'].outgoingCount).toBe(1);
    expect(byType['service'].incomingCount).toBe(1);
  });
});
