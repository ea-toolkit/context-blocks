import { render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

vi.mock('./DomainMap', () => ({
  default: (p: { entities: { id: string }[] }) => (
    <div data-testid="map">ids:{p.entities.map((e) => e.id).join(',')}</div>
  ),
}));

// eslint-disable-next-line import/first
import * as client from '../../lib/studio-client';
import type { DomainMapProps } from './DomainMap';
import MapView from './MapView';

const baked = {
  entities: [{ id: 'baked-1' }],
  edges: [],
  layers: [],
  entityTypes: [],
} as unknown as DomainMapProps;

afterEach(() => {
  vi.restoreAllMocks();
  window.history.pushState({}, '', '/map');
});

describe('MapView', () => {
  it('renders baked data when no ?block is set', async () => {
    window.history.pushState({}, '', '/map');
    render(<MapView {...baked} />);
    expect(await screen.findByTestId('map')).toHaveTextContent('ids:baked-1');
  });

  it('renders live data when ?block is set', async () => {
    window.history.pushState({}, '', '/map?block=incidents');
    vi.spyOn(client.studio, 'getGraph').mockResolvedValue({
      ok: true,
      status: 200,
      body: {
        nodes: [
          {
            id: 'live-1',
            name: 'L',
            type: 'x',
            type_label: 'X',
            type_icon: 'X',
            layer: 'behavioral',
            layer_color: '#4A90E2',
            confidence: 1,
            description: '',
            relationship_count: 0,
            incoming_count: 0,
            outgoing_count: 0,
          },
        ],
        edges: [],
        layers: [],
        entity_types: [],
      },
    });
    render(<MapView {...baked} />);
    expect(await screen.findByText(/ids:live-1/)).toBeInTheDocument();
  });
});
