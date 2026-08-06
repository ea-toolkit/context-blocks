import { render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import * as client from '../../lib/studio-client';
import type { BlockOntology as BlockOntologyData } from '../../lib/studio-types';
import BlockOntology from './BlockOntology';

afterEach(() => vi.restoreAllMocks());

const onto: BlockOntologyData = {
  source: 'incidents/meta-model.yaml',
  layers: [
    { key: 'behavioral', label: 'Behavioral', color: '#1ABC9C' },
    { key: 'structural', label: 'Structural', color: '#4A90E2' },
  ],
  types: [
    { key: 'incident', label: 'Incidents', layer: 'behavioral' },
    { key: 'service', label: 'Services', layer: 'structural' },
  ],
  relationship_fields: ['affects', 'resolved_by'],
};

describe('BlockOntology', () => {
  it('renders types grouped by layer + the relationship fields', async () => {
    vi.spyOn(client.studio, 'getOntology').mockResolvedValue({ ok: true, status: 200, body: onto });
    render(<BlockOntology block="incidents" />);
    expect(await screen.findByText('Behavioral')).toBeInTheDocument();
    expect(screen.getByText('Structural')).toBeInTheDocument();
    expect(screen.getByText('Incidents')).toBeInTheDocument();
    expect(screen.getByText('Services')).toBeInTheDocument();
    expect(screen.getByText('affects')).toBeInTheDocument();
    expect(screen.getByText(/Relationship fields \(2\)/)).toBeInTheDocument();
  });

  it('shows an error when it fails to load', async () => {
    vi.spyOn(client.studio, 'getOntology').mockResolvedValue({ ok: false, status: 500, body: null });
    render(<BlockOntology block="incidents" />);
    expect(await screen.findByText(/Could not load the ontology/i)).toBeInTheDocument();
  });
});
