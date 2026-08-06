import { render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

vi.mock('../studio/BlockOntology', () => ({
  default: ({ block }: { block: string }) => <div data-testid="live-onto">live:{block}</div>,
}));
vi.mock('./OntologySchema', () => ({
  default: () => <div data-testid="baked-onto">baked</div>,
}));

// eslint-disable-next-line import/first
import OntologyView from './OntologyView';

afterEach(() => window.history.pushState({}, '', '/ontology'));

describe('OntologyView', () => {
  it('renders baked schema when no ?block is set', async () => {
    window.history.pushState({}, '', '/ontology');
    render(<OntologyView layers={[]} types={[]} relationshipFields={[]} />);
    expect(await screen.findByTestId('baked-onto')).toBeInTheDocument();
  });

  it('renders the live block ontology when ?block is set', async () => {
    window.history.pushState({}, '', '/ontology?block=incidents');
    render(<OntologyView layers={[]} types={[]} relationshipFields={[]} />);
    expect(await screen.findByTestId('live-onto')).toHaveTextContent('live:incidents');
  });
});
