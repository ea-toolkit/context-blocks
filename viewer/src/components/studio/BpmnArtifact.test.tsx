import { render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

const importXML = vi.fn().mockResolvedValue(undefined);
const zoom = vi.fn();
const destroy = vi.fn();

vi.mock('bpmn-js/lib/Viewer', () => ({
  default: vi.fn().mockImplementation(() => ({
    importXML,
    get: () => ({ zoom }),
    destroy,
  })),
}));

// eslint-disable-next-line import/first
import BpmnArtifact from './BpmnArtifact';

afterEach(() => {
  vi.clearAllMocks();
});

describe('BpmnArtifact', () => {
  it('fetches the bpmn xml and imports it into the viewer', async () => {
    globalThis.fetch = vi
      .fn()
      .mockResolvedValue({ text: () => Promise.resolve('<definitions/>') }) as unknown as typeof fetch;
    render(<BpmnArtifact url="/blocks/x/artifacts/flow.bpmn" />);
    await waitFor(() => expect(importXML).toHaveBeenCalledWith('<definitions/>'));
  });

  it('shows an error when import fails', async () => {
    globalThis.fetch = vi
      .fn()
      .mockResolvedValue({ text: () => Promise.resolve('bad') }) as unknown as typeof fetch;
    importXML.mockRejectedValueOnce(new Error('parse'));
    render(<BpmnArtifact url="/x.bpmn" />);
    expect(await screen.findByText(/Could not render/i)).toBeInTheDocument();
  });
});
