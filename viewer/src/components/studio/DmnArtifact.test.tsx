import { render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

const importXML = vi.fn().mockResolvedValue(undefined);
const zoom = vi.fn();
const destroy = vi.fn();

vi.mock('dmn-js/lib/Viewer', () => ({
  default: vi.fn().mockImplementation(() => ({
    importXML,
    getActiveViewer: () => ({ get: () => ({ zoom }) }),
    destroy,
  })),
}));

// eslint-disable-next-line import/first
import DmnArtifact from './DmnArtifact';

afterEach(() => {
  vi.clearAllMocks();
});

describe('DmnArtifact', () => {
  it('fetches the dmn xml and imports it into the viewer', async () => {
    globalThis.fetch = vi
      .fn()
      .mockResolvedValue({ text: () => Promise.resolve('<definitions/>') }) as unknown as typeof fetch;
    render(<DmnArtifact url="/blocks/x/artifacts/pricing.dmn" />);
    await waitFor(() => expect(importXML).toHaveBeenCalledWith('<definitions/>'));
  });

  it('shows an error when import fails', async () => {
    globalThis.fetch = vi
      .fn()
      .mockResolvedValue({ text: () => Promise.resolve('bad') }) as unknown as typeof fetch;
    importXML.mockRejectedValueOnce(new Error('parse'));
    render(<DmnArtifact url="/x.dmn" />);
    expect(await screen.findByText(/Could not render/i)).toBeInTheDocument();
  });
});
