import { render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import * as client from '../../lib/studio-client';
import type { BlockSummary } from '../../lib/studio-types';
import BlockSelector from './BlockSelector';

afterEach(() => vi.restoreAllMocks());

const blocks = [
  { name: 'cost-control', label: 'Cost Control' },
  { name: 'incidents', label: '' },
] as BlockSummary[];

describe('BlockSelector', () => {
  it('lists blocks (with a Built data option)', async () => {
    vi.spyOn(client.studio, 'listBlocks').mockResolvedValue({ ok: true, status: 200, body: blocks });
    render(<BlockSelector />);
    expect(await screen.findByRole('combobox')).toBeInTheDocument();
    expect(screen.getByText('Built data')).toBeInTheDocument();
    expect(screen.getByText('Cost Control · live')).toBeInTheDocument();
    expect(screen.getByText('incidents · live')).toBeInTheDocument();
  });

  it('renders nothing when the Studio API has no blocks', async () => {
    vi.spyOn(client.studio, 'listBlocks').mockResolvedValue({ ok: true, status: 200, body: [] });
    const { container } = render(<BlockSelector />);
    // allow the effect to run
    await Promise.resolve();
    expect(container.querySelector('select')).toBeNull();
  });
});
