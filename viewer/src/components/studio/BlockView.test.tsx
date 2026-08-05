import { fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import * as client from '../../lib/studio-client';
import type { BlockDetail, EntityListItem } from '../../lib/studio-types';
import BlockView from './BlockView';

afterEach(() => vi.restoreAllMocks());

const block: BlockDetail = {
  name: 'incidents',
  description: 'Incident block',
  label: 'Incidents',
  ontology: 'incidents/meta-model.yaml',
  output: '',
  seed_context: '',
  model: '',
  entity_count: 1,
  created_at: '',
  last_updated: '',
  output_dir: '/x/incidents',
  ontology_detail: {
    source: 'x',
    types: ['incident', 'service'],
    layers: ['behavioral'],
    relationship_field_count: 2,
  },
};

const entities: EntityListItem[] = [
  { id: 'checkout-outage', type: 'incident', name: 'Checkout Outage', path: 'entities/incidents/checkout-outage.md' },
];

function mockOk() {
  vi.spyOn(client.studio, 'getBlock').mockResolvedValue({ ok: true, status: 200, body: block });
  vi.spyOn(client.studio, 'listEntities').mockResolvedValue({ ok: true, status: 200, body: entities });
}

describe('BlockView', () => {
  it('renders ontology types/layers and the entity table', async () => {
    mockOk();
    render(<BlockView name="incidents" onBack={() => {}} />);
    expect(await screen.findByText('Incidents')).toBeInTheDocument();
    expect(screen.getByText('service')).toBeInTheDocument(); // ontology chip
    expect(screen.getByText('behavioral')).toBeInTheDocument(); // layer chip
    expect(screen.getAllByText('incident').length).toBeGreaterThanOrEqual(1);
    expect(await screen.findByText('checkout-outage')).toBeInTheDocument();
    expect(screen.getByText('Checkout Outage')).toBeInTheDocument();
  });

  it('shows an empty state when there are no entities', async () => {
    vi.spyOn(client.studio, 'getBlock').mockResolvedValue({ ok: true, status: 200, body: block });
    vi.spyOn(client.studio, 'listEntities').mockResolvedValue({ ok: true, status: 200, body: [] });
    render(<BlockView name="incidents" onBack={() => {}} />);
    expect(await screen.findByText(/No entities yet/i)).toBeInTheDocument();
  });

  it('calls onBack when Back is clicked', async () => {
    mockOk();
    const onBack = vi.fn();
    render(<BlockView name="incidents" onBack={onBack} />);
    fireEvent.click(await screen.findByText(/Back to blocks/i));
    expect(onBack).toHaveBeenCalled();
  });

  it('surfaces an error when the block cannot be loaded', async () => {
    vi.spyOn(client.studio, 'getBlock').mockResolvedValue({
      ok: false,
      status: 404,
      body: { detail: 'Block not found' },
    });
    render(<BlockView name="ghost" onBack={() => {}} />);
    expect(await screen.findByText(/Block not found/i)).toBeInTheDocument();
  });
});
