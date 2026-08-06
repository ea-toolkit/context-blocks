import { render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

vi.mock('../map/DomainMap', () => ({
  default: (p: { entities: { id: string }[]; edges: unknown[] }) => (
    <div data-testid="map">
      types:{p.entities.map((e) => e.id).sort().join(',')}|edges:{p.edges.length}
    </div>
  ),
}));

// eslint-disable-next-line import/first
import * as client from '../../lib/studio-client';
import type { DomainMapProps } from '../map/DomainMap';
import OntologyView from './OntologyView';

const baked = {
  entities: [
    { id: 'a', name: 'A', type: 'system', typeLabel: 'Systems', typeIcon: 'SY', layer: 'structural', layerColor: '#4A90E2', confidence: 1, description: '', relationshipCount: 1, incomingCount: 0, outgoingCount: 1 },
    { id: 'b', name: 'B', type: 'data-model', typeLabel: 'Data Models', typeIcon: 'DM', layer: 'structural', layerColor: '#4A90E2', confidence: 1, description: '', relationshipCount: 1, incomingCount: 1, outgoingCount: 0 },
  ],
  edges: [{ source: 'a', target: 'b', type: 'persists' }],
  layers: [],
  entityTypes: [],
} as DomainMapProps;

afterEach(() => {
  vi.restoreAllMocks();
  window.history.pushState({}, '', '/ontology');
});

describe('OntologyView', () => {
  it('renders the baked type-graph when no ?block is set', async () => {
    window.history.pushState({}, '', '/ontology');
    render(<OntologyView {...baked} />);
    // 2 entities of 2 types → 2 type nodes, 1 type edge
    expect(await screen.findByTestId('map')).toHaveTextContent('types:data-model,system|edges:1');
  });

  it('renders the live block type-graph when ?block is set', async () => {
    window.history.pushState({}, '', '/ontology?block=incidents');
    vi.spyOn(client.studio, 'getGraph').mockResolvedValue({
      ok: true,
      status: 200,
      body: {
        nodes: [
          { id: 'x', name: 'X', type: 'incident', type_label: 'Incidents', type_icon: 'IN', layer: 'behavioral', layer_color: '#1ABC9C', confidence: 1, description: '', relationship_count: 0, incoming_count: 0, outgoing_count: 0 },
        ],
        edges: [],
        layers: [],
        entity_types: [],
      },
    });
    render(<OntologyView {...baked} />);
    expect(await screen.findByText(/types:incident/)).toBeInTheDocument();
  });
});
