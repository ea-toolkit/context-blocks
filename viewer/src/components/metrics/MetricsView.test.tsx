import { render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import * as client from '../../lib/studio-client';
import type { BlockMetrics } from '../../lib/studio-types';
import MetricsView from './MetricsView';

afterEach(() => vi.restoreAllMocks());

const METRICS: BlockMetrics = {
  block: 'incident-management',
  work_efforts: {
    total: 3,
    with_gaps: 1,
    total_calls: 8,
    total_gaps: 2,
    gap_rate: 0.25,
    outcomes: [{ outcome: 'resolved', count: 2 }],
    recent: [
      { id: 'we-1', intent: 'triage WOM timeouts', outcome: 'resolved', call_count: 4, gap_count: 1, started_at: '2026-08-11T10:00:00+00:00', ended_at: '2026-08-11T10:20:00+00:00' },
    ],
  },
  top_entities: [{ entity_id: 'wom-connector', hits: 5 }],
  gaps: [{ tool: 'get_entity', args: { entity_id: 'missing-runbook' }, at: '2026-08-11T10:05:00+00:00', intent: 'triage WOM timeouts' }],
  changes: {
    total: 2,
    by_action: { created: 1, updated: 1 },
    by_actor: [{ actor: 'luffy', count: 2 }],
    recent: [{ at: '2026-08-11T10:10:00+00:00', entity_id: 'wom-connector', entity_type: 'service', action: 'updated', actor: 'luffy', work_effort_id: 'we-1', summary: 'WOM Connector' }],
  },
};

function mockOk() {
  vi.spyOn(client.studio, 'health').mockResolvedValue({ ok: true, status: 200, body: { status: 'ok', root: '/', blocks: 1 } });
  vi.spyOn(client.studio, 'getMetrics').mockResolvedValue({ ok: true, status: 200, body: METRICS });
}

describe('MetricsView', () => {
  it('renders the block name and key stats', async () => {
    mockOk();
    render(<MetricsView block="incident-management" />);
    expect(await screen.findByText('incident-management')).toBeInTheDocument();
    expect(screen.getByText('25%')).toBeInTheDocument(); // gap rate
    expect(screen.getByText('missing-runbook')).toBeInTheDocument(); // gap surfaced
    // wom-connector appears as both a top entity and in the change timeline
    expect(screen.getAllByText('wom-connector').length).toBeGreaterThan(0);
  });

  it('shows an offline message when the Studio API is down', async () => {
    vi.spyOn(client.studio, 'health').mockResolvedValue({ ok: false, status: 0, body: null });
    render(<MetricsView block="incident-management" />);
    await waitFor(() => expect(screen.getByText(/not reachable/i)).toBeInTheDocument());
  });

  it('shows an empty state when there is no activity', async () => {
    vi.spyOn(client.studio, 'health').mockResolvedValue({ ok: true, status: 200, body: { status: 'ok', root: '/', blocks: 1 } });
    vi.spyOn(client.studio, 'getMetrics').mockResolvedValue({
      ok: true, status: 200,
      body: { ...METRICS, work_efforts: { ...METRICS.work_efforts, total: 0 }, changes: { ...METRICS.changes, total: 0 } },
    });
    render(<MetricsView block="incident-management" />);
    await waitFor(() => expect(screen.getByText(/No activity yet/i)).toBeInTheDocument());
  });
});
