import { useCallback, useEffect, useState } from 'react';

import { STUDIO_API_BASE, studio } from '../../lib/studio-client';
import type { BlockMetrics } from '../../lib/studio-types';

interface Props {
  /** Build-time block id (from BASE_URL). Empty for a single-block build — resolved via listBlocks. */
  block?: string;
}

function relTime(iso: string | null): string {
  if (!iso) return '—';
  return iso.replace('T', ' ').slice(0, 16);
}

/** Live metrics dashboard: the work-effort demand log + the Context Sourcing change log. */
export default function MetricsView({ block = '' }: Props) {
  const [online, setOnline] = useState<boolean | null>(null);
  const [metrics, setMetrics] = useState<BlockMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    const health = await studio.health();
    if (!health.ok) {
      setOnline(false);
      setLoading(false);
      return;
    }
    setOnline(true);
    // Resolve the block: use the build's id, else the first block the API knows.
    let name = block;
    if (!name) {
      const blocks = await studio.listBlocks();
      name = blocks.body?.[0]?.name ?? '';
    }
    if (!name) {
      setError('No block to show metrics for.');
      setLoading(false);
      return;
    }
    const res = await studio.getMetrics(name);
    if (res.ok && res.body) setMetrics(res.body);
    else setError(`Could not load metrics (status ${res.status}).`);
    setLoading(false);
  }, [block]);

  useEffect(() => {
    void load();
  }, [load]);

  if (online === false) {
    return (
      <div className="metrics-offline">
        <p>The Studio API is not reachable at <code>{STUDIO_API_BASE}</code>.</p>
        <p>Start it with:</p>
        <pre><code>uvicorn context_blocks.studio_api:create_studio_app --factory --port 8322</code></pre>
      </div>
    );
  }

  if (!metrics) {
    return <div className="metrics-loading">{loading ? 'Loading metrics…' : 'No metrics yet.'}</div>;
  }

  const we = metrics.work_efforts;
  const empty = we.total === 0 && metrics.changes.total === 0;

  return (
    <div className="metrics">
      <div className="metrics-head">
        <div>
          <h2 className="metrics-title">{metrics.block}</h2>
          <p className="metrics-sub">What agents asked, where the block fell short, and what changed.</p>
        </div>
        <button className="metrics-refresh" onClick={() => void load()} disabled={loading}>
          {loading ? '…' : '↻ Refresh'}
        </button>
      </div>

      {empty ? (
        <div className="metrics-empty">
          No activity yet. Run an agent against this block (open a work-effort, search, resolve) and
          refresh — the demand log and change history fill in here.
        </div>
      ) : (
        <>
          <div className="metrics-cards">
            <Stat label="Work-efforts" value={we.total} sub={`${we.with_gaps} hit gaps`} />
            <Stat label="Gap rate" value={`${Math.round(we.gap_rate * 100)}%`} sub={`${we.total_gaps}/${we.total_calls} calls`} tone={we.gap_rate > 0.3 ? 'warn' : 'ok'} />
            <Stat label="Changes" value={metrics.changes.total} sub={changeBreakdown(metrics.changes.by_action)} />
            <Stat label="Contributors" value={metrics.changes.by_actor.length} sub={metrics.changes.by_actor.slice(0, 2).map((a) => a.actor).join(', ')} />
          </div>

          <div className="metrics-grid">
            <Panel title="Gaps — where the block fell short">
              {metrics.gaps.length === 0 ? (
                <p className="metrics-none">No gaps recorded. 🎉</p>
              ) : (
                <ul className="metrics-list">
                  {metrics.gaps.map((g, i) => (
                    <li key={i} className="metrics-gap">
                      <span className="metrics-mono">{String(g.args.entity_id ?? g.args.query ?? g.tool)}</span>
                      <span className="metrics-faint">{g.intent}</span>
                    </li>
                  ))}
                </ul>
              )}
            </Panel>

            <Panel title="Top-hit entities">
              {metrics.top_entities.length === 0 ? (
                <p className="metrics-none">No entity lookups yet.</p>
              ) : (
                <ul className="metrics-list">
                  {metrics.top_entities.map((t) => (
                    <li key={t.entity_id} className="metrics-row">
                      <span className="metrics-mono">{t.entity_id}</span>
                      <span className="metrics-count">{t.hits}</span>
                    </li>
                  ))}
                </ul>
              )}
            </Panel>

            <Panel title="Recent work-efforts">
              {we.recent.length === 0 ? (
                <p className="metrics-none">No work-efforts yet.</p>
              ) : (
                <ul className="metrics-list">
                  {we.recent.map((e) => (
                    <li key={e.id} className="metrics-effort">
                      <span className="metrics-effort-intent">{e.intent}</span>
                      <span className="metrics-effort-meta">
                        {e.call_count} calls · {e.gap_count} gaps · {e.outcome || 'open'}
                      </span>
                    </li>
                  ))}
                </ul>
              )}
            </Panel>

            <Panel title="Change timeline">
              {metrics.changes.recent.length === 0 ? (
                <p className="metrics-none">No changes yet.</p>
              ) : (
                <ul className="metrics-list">
                  {metrics.changes.recent.map((c, i) => (
                    <li key={i} className="metrics-change">
                      <span className={`metrics-action metrics-action--${c.action}`}>{c.action}</span>
                      <span className="metrics-mono">{c.entity_id}</span>
                      <span className="metrics-faint">{c.actor} · {relTime(c.at)}</span>
                    </li>
                  ))}
                </ul>
              )}
            </Panel>
          </div>
        </>
      )}
      {error && <p className="metrics-error">{error}</p>}
    </div>
  );
}

function Stat({ label, value, sub, tone }: { label: string; value: string | number; sub?: string; tone?: 'ok' | 'warn' }) {
  return (
    <div className={`metrics-card${tone === 'warn' ? ' metrics-card--warn' : ''}`}>
      <div className="metrics-card-value">{value}</div>
      <div className="metrics-card-label">{label}</div>
      {sub && <div className="metrics-card-sub">{sub}</div>}
    </div>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="metrics-panel">
      <h3 className="metrics-panel-title">{title}</h3>
      {children}
    </section>
  );
}

function changeBreakdown(byAction: Record<string, number>): string {
  return Object.entries(byAction)
    .map(([a, n]) => `${n} ${a}`)
    .join(' · ') || '—';
}
