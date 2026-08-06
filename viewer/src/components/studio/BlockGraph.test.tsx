import { render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

vi.mock('../map/DomainMap', () => ({
  default: (props: { entities: unknown[] }) => (
    <div data-testid="domain-map">nodes:{props.entities.length}</div>
  ),
}));

// eslint-disable-next-line import/first
import * as client from '../../lib/studio-client';
import type { BlockGraph as BlockGraphData } from '../../lib/studio-types';
import BlockGraph from './BlockGraph';

afterEach(() => vi.restoreAllMocks());

const graph: BlockGraphData = {
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
      description: '',
      relationship_count: 1,
      incoming_count: 0,
      outgoing_count: 1,
    },
  ],
  edges: [{ source: 'a', target: 'b', type: 'affects' }],
  layers: [{ key: 'behavioral', label: 'Behavioral', color: '#1ABC9C' }],
  entity_types: [{ key: 'incident', label: 'Incidents', layer: 'behavioral' }],
};

describe('BlockGraph', () => {
  it('renders the graph when nodes exist', async () => {
    vi.spyOn(client.studio, 'getGraph').mockResolvedValue({ ok: true, status: 200, body: graph });
    render(<BlockGraph block="incidents" />);
    expect(await screen.findByTestId('domain-map')).toHaveTextContent('nodes:1');
  });

  it('shows an empty state when there are no nodes', async () => {
    vi.spyOn(client.studio, 'getGraph').mockResolvedValue({
      ok: true,
      status: 200,
      body: { nodes: [], edges: [], layers: [], entity_types: [] },
    });
    render(<BlockGraph block="incidents" />);
    expect(await screen.findByText(/No entities to graph/i)).toBeInTheDocument();
  });

  it('shows an error when the graph fails to load', async () => {
    vi.spyOn(client.studio, 'getGraph').mockResolvedValue({ ok: false, status: 500, body: null });
    render(<BlockGraph block="incidents" />);
    expect(await screen.findByText(/Could not load the graph/i)).toBeInTheDocument();
  });
});
