import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import * as client from '../../lib/studio-client';
import type { ArtifactInfo } from '../../lib/studio-types';
import ArtifactsSection from './ArtifactsSection';

afterEach(() => vi.restoreAllMocks());

const arts: ArtifactInfo[] = [
  { filename: 'arch.drawio.svg', path: 'artifacts/arch.drawio.svg', size: 2048, content_type: 'image/svg+xml' },
];

describe('ArtifactsSection', () => {
  it('shows empty state when there are no artifacts', async () => {
    vi.spyOn(client.studio, 'listArtifacts').mockResolvedValue({ ok: true, status: 200, body: [] });
    render(<ArtifactsSection block="incidents" />);
    expect(await screen.findByText(/No artifacts yet/i)).toBeInTheDocument();
  });

  it('lists artifacts with sizes', async () => {
    vi.spyOn(client.studio, 'listArtifacts').mockResolvedValue({ ok: true, status: 200, body: arts });
    render(<ArtifactsSection block="incidents" />);
    expect(await screen.findByText('arch.drawio.svg')).toBeInTheDocument();
    expect(screen.getByText('2.0 KB')).toBeInTheDocument();
  });

  it('uploads a file and refreshes the list', async () => {
    const list = vi.spyOn(client.studio, 'listArtifacts').mockResolvedValue({ ok: true, status: 200, body: [] });
    const up = vi
      .spyOn(client.studio, 'uploadArtifact')
      .mockResolvedValue({ ok: true, status: 201, body: arts[0] });
    render(<ArtifactsSection block="incidents" />);
    await screen.findByText(/No artifacts yet/i);

    const input = screen.getByLabelText(/Upload artifact/i);
    const file = new File(['<svg/>'], 'arch.drawio.svg', { type: 'image/svg+xml' });
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => expect(up).toHaveBeenCalledWith('incidents', file));
    expect(list.mock.calls.length).toBeGreaterThanOrEqual(2); // mount + after upload
  });

  it('shows a 415 error for unsupported types', async () => {
    vi.spyOn(client.studio, 'listArtifacts').mockResolvedValue({ ok: true, status: 200, body: [] });
    vi.spyOn(client.studio, 'uploadArtifact').mockResolvedValue({ ok: false, status: 415, body: null });
    render(<ArtifactsSection block="incidents" />);
    await screen.findByText(/No artifacts yet/i);

    const input = screen.getByLabelText(/Upload artifact/i);
    const file = new File(['x'], 'notes.md', { type: 'text/markdown' });
    fireEvent.change(input, { target: { files: [file] } });

    expect(await screen.findByText(/Unsupported file type/i)).toBeInTheDocument();
  });
});
