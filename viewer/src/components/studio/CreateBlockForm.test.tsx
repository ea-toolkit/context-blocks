import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import * as client from '../../lib/studio-client';
import type { BlockDetail } from '../../lib/studio-types';
import CreateBlockForm from './CreateBlockForm';

afterEach(() => vi.restoreAllMocks());

const nameField = () => screen.getByLabelText(/Name \(kebab-case\)/i);
const submit = () => fireEvent.click(screen.getByRole('button', { name: /Create Block/i }));

describe('CreateBlockForm', () => {
  it('renders the name field', () => {
    render(<CreateBlockForm onCreated={() => {}} />);
    expect(nameField()).toBeInTheDocument();
  });

  it('requires a name and does not call the API', async () => {
    const spy = vi.spyOn(client.studio, 'createBlock');
    render(<CreateBlockForm onCreated={() => {}} />);
    submit();
    expect(await screen.findByText(/Name is required/i)).toBeInTheDocument();
    expect(spy).not.toHaveBeenCalled();
  });

  it('creates a block and calls onCreated', async () => {
    const block = { name: 'cost-control', label: 'Cost Control' } as BlockDetail;
    const spy = vi
      .spyOn(client.studio, 'createBlock')
      .mockResolvedValue({ ok: true, status: 201, body: block });
    const onCreated = vi.fn();
    render(<CreateBlockForm onCreated={onCreated} />);
    fireEvent.change(nameField(), { target: { value: 'cost-control' } });
    submit();
    await waitFor(() => expect(onCreated).toHaveBeenCalledWith(block));
    expect(spy).toHaveBeenCalledWith(expect.objectContaining({ name: 'cost-control' }));
  });

  it('shows the API error message on failure', async () => {
    vi.spyOn(client.studio, 'createBlock').mockResolvedValue({
      ok: false,
      status: 409,
      body: { detail: 'Block exists' },
    });
    render(<CreateBlockForm onCreated={() => {}} />);
    fireEvent.change(nameField(), { target: { value: 'dup' } });
    submit();
    expect(await screen.findByText(/Block exists/i)).toBeInTheDocument();
  });

  it('includes ontology_yaml only when custom mode is selected', async () => {
    const spy = vi
      .spyOn(client.studio, 'createBlock')
      .mockResolvedValue({ ok: true, status: 201, body: {} as BlockDetail });
    render(<CreateBlockForm onCreated={() => {}} />);
    fireEvent.change(nameField(), { target: { value: 'incidents' } });
    fireEvent.click(screen.getByLabelText(/Custom YAML/i));
    fireEvent.change(screen.getByLabelText(/Ontology YAML/i), {
      target: { value: 'entity_types:\n  x: { layer: y }' },
    });
    submit();
    await waitFor(() => expect(spy).toHaveBeenCalled());
    expect(spy.mock.calls[0][0]).toHaveProperty('ontology_yaml');
  });
});
