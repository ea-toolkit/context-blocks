import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import OntologySchema from './OntologySchema';

describe('OntologySchema', () => {
  it('renders types grouped by layer + the relationship fields', () => {
    render(
      <OntologySchema
        source="meta-model.yaml"
        layers={[
          { key: 'structural', label: 'Structural', color: '#4A90E2' },
          { key: 'behavioral', label: 'Behavioral', color: '#1ABC9C' },
        ]}
        types={[
          { key: 'system', label: 'Systems', layer: 'structural' },
          { key: 'process', label: 'Processes', layer: 'behavioral' },
        ]}
        relationshipFields={['depends_on', 'owned_by']}
      />,
    );
    expect(screen.getByText('Structural')).toBeInTheDocument();
    expect(screen.getByText('Behavioral')).toBeInTheDocument();
    expect(screen.getByText('Systems')).toBeInTheDocument();
    expect(screen.getByText('Processes')).toBeInTheDocument();
    expect(screen.getByText('depends_on')).toBeInTheDocument();
    expect(screen.getByText(/Relationship fields \(2\)/)).toBeInTheDocument();
  });
});
