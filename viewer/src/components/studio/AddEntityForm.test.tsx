import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import * as client from '../../lib/studio-client';
import type { AddEntityResponse } from '../../lib/studio-types';
import AddEntityForm from './AddEntityForm';

afterEach(() => vi.restoreAllMocks());

const textarea = () => screen.getByLabelText(/Entity markdown/i);
const submit = () => fireEvent.click(screen.getByRole('button', { name: /Validate & Add/i }));

describe('AddEntityForm', () => {
  it('renders the textarea', () => {
    render(<AddEntityForm blockName="incidents" onAdded={() => {}} />);
    expect(textarea()).toBeInTheDocument();
  });

  it('requires content and does not call the API', async () => {
    const spy = vi.spyOn(client.studio, 'addEntity');
    render(<AddEntityForm blockName="incidents" onAdded={() => {}} />);
    submit();
    expect(await screen.findByText(/Paste entity markdown first/i)).toBeInTheDocument();
    expect(spy).not.toHaveBeenCalled();
  });

  it('adds a valid entity and calls onAdded', async () => {
    const body: AddEntityResponse = { id: 'checkout-outage', type: 'incident', path: 'entities/incidents/checkout-outage.md' };
    const spy = vi.spyOn(client.studio, 'addEntity').mockResolvedValue({ ok: true, status: 201, body });
    const onAdded = vi.fn();
    render(<AddEntityForm blockName="incidents" onAdded={onAdded} />);
    fireEvent.change(textarea(), { target: { value: '---\ntype: incident\n---' } });
    submit();
    await waitFor(() => expect(onAdded).toHaveBeenCalled());
    expect(spy).toHaveBeenCalledWith('incidents', '---\ntype: incident\n---');
  });

  it('renders per-field validation errors on 422', async () => {
    vi.spyOn(client.studio, 'addEntity').mockResolvedValue({
      ok: false,
      status: 422,
      body: { detail: { errors: ['type: not a known entity type', 'id: must be kebab-case'] } },
    });
    render(<AddEntityForm blockName="incidents" onAdded={() => {}} />);
    fireEvent.change(textarea(), { target: { value: '---\ntype: banana\n---' } });
    submit();
    expect(await screen.findByText(/not a known entity type/i)).toBeInTheDocument();
    expect(screen.getByText(/must be kebab-case/i)).toBeInTheDocument();
  });

  it('shows a generic message on a non-422 error', async () => {
    vi.spyOn(client.studio, 'addEntity').mockResolvedValue({
      ok: false,
      status: 409,
      body: { detail: "Entity 'checkout-outage' already exists in block 'incidents'" },
    });
    render(<AddEntityForm blockName="incidents" onAdded={() => {}} />);
    fireEvent.change(textarea(), { target: { value: '---\ntype: incident\n---' } });
    submit();
    expect(await screen.findByText(/already exists/i)).toBeInTheDocument();
  });
});
