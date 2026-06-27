/**
 * Gaps View — where your documentation is thin.
 * Shows coverage summary + gap cards tabbed by CLEAN/INCOMPLETE/MISSING.
 * Each gap card shows: question, found entities, missing info, suggested action, source.
 */
import { useState, useMemo } from 'react';
import type { EvalResult, EvalStats } from '../../lib/types';

interface GapsViewProps {
  results: EvalResult[];
  stats: EvalStats;
}

type TabKey = 'CLEAN' | 'INCOMPLETE' | 'MISSING';

function ScoreBadge({ score }: { score: string }) {
  const cls = score === 'CLEAN' ? 'score-badge--clean'
    : score === 'INCOMPLETE' ? 'score-badge--incomplete'
    : 'score-badge--missing';
  return <span className={`score-badge ${cls}`}>{score}</span>;
}

function SourceBadge({ source, persona }: { source: string; persona?: string }) {
  const label = persona ? `${source}:${persona}` : source;
  const cls = source === 'persona' ? 'source-badge--persona'
    : source === 'work-item' ? 'source-badge--work-item'
    : '';
  return <span className={`source-badge ${cls}`}>{label}</span>;
}

function CoverageHeader({ stats }: { stats: EvalStats }) {
  const total = stats.total;
  return (
    <div style={{ marginBottom: 'var(--cb-space-xl)' }}>
      <h1 style={{ fontSize: 'var(--cb-font-size-2xl)', fontWeight: 700, marginBottom: 'var(--cb-space-sm)' }}>
        Where your documentation is thin
      </h1>
      <p style={{ color: 'var(--cb-text-muted)', marginBottom: 'var(--cb-space-lg)', maxWidth: 600 }}>
        Gaps aren't bugs — they're the map of what to capture next. Each question was run against
        the knowledge base and scored by how completely it could be answered.
      </p>

      {/* Big numbers */}
      <div style={{ display: 'flex', gap: 'var(--cb-space-xl)', marginBottom: 'var(--cb-space-lg)' }}>
        <div>
          <span style={{ fontSize: 'var(--cb-font-size-2xl)', fontWeight: 700, color: 'var(--cb-score-clean)' }}>
            {stats.cleanPct}%
          </span>
          <span style={{ fontSize: 'var(--cb-font-size-sm)', color: 'var(--cb-text-faint)', marginLeft: 'var(--cb-space-xs)' }}>
            clean
          </span>
        </div>
        <div>
          <span style={{ fontSize: 'var(--cb-font-size-2xl)', fontWeight: 700, color: 'var(--cb-score-incomplete)' }}>
            {stats.incompletePct}%
          </span>
          <span style={{ fontSize: 'var(--cb-font-size-sm)', color: 'var(--cb-text-faint)', marginLeft: 'var(--cb-space-xs)' }}>
            incomplete
          </span>
        </div>
        <div>
          <span style={{ fontSize: 'var(--cb-font-size-2xl)', fontWeight: 700, color: 'var(--cb-score-missing)' }}>
            {stats.missingPct}%
          </span>
          <span style={{ fontSize: 'var(--cb-font-size-sm)', color: 'var(--cb-text-faint)', marginLeft: 'var(--cb-space-xs)' }}>
            missing
          </span>
        </div>
      </div>

      {/* Coverage bar */}
      <div style={{ display: 'flex', height: 8, borderRadius: 4, overflow: 'hidden', background: 'var(--cb-surface-raised)', marginBottom: 'var(--cb-space-md)' }}>
        {stats.cleanPct > 0 && <div style={{ width: `${stats.cleanPct}%`, background: 'var(--cb-score-clean)' }} />}
        {stats.incompletePct > 0 && <div style={{ width: `${stats.incompletePct}%`, background: 'var(--cb-score-incomplete)' }} />}
        {stats.missingPct > 0 && <div style={{ width: `${stats.missingPct}%`, background: 'var(--cb-score-missing)' }} />}
      </div>

      {/* Layer breakdown */}
      {Object.keys(stats.perLayer).length > 0 && (
        <p style={{ fontSize: 'var(--cb-font-size-sm)', color: 'var(--cb-text-muted)' }}>
          {Object.entries(stats.perLayer)
            .filter(([_, v]) => v.missing > 0)
            .sort((a, b) => b[1].missing - a[1].missing)
            .slice(0, 3)
            .map(([layer, v]) => {
              const layerTotal = v.clean + v.incomplete + v.missing;
              const missingPct = Math.round(v.missing / layerTotal * 100);
              return `${layer} (${missingPct}% missing)`;
            })
            .join(', ')}{' '}
          carry the most missing knowledge.
        </p>
      )}
    </div>
  );
}

function GapCard({ result }: { result: EvalResult }) {
  const [expanded, setExpanded] = useState(false);

  // Extract found entity names from hops
  const foundEntities = result.hops.slice(0, 5).map(h => h.entity_name);

  // Get gap descriptions
  const gapDescriptions = result.gaps.map(g => g.description);

  // Suggest action based on gap type
  const suggestedAction = result.gaps.length > 0
    ? result.gaps[0].gap_type === 'thin_coverage'
      ? 'Enrich existing entities with more detail from source documents.'
      : result.gaps[0].gap_type === 'missing_entity'
        ? 'Author a new entity or document covering this topic.'
        : result.gaps[0].gap_type === 'orphan_entity'
          ? 'Add relationships to connect this entity to the graph.'
          : 'Investigate and resolve this knowledge gap.'
    : result.ddc_class === 'CLEAN'
      ? 'Fully documented — no action needed.'
      : 'Review answer quality and enrich if needed.';

  return (
    <div className="gap-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--cb-space-sm)' }}>
        <div className="gap-card__question">
          {result.topic || result.question.slice(0, 100)}
        </div>
        <ScoreBadge score={result.ddc_class} />
      </div>

      {/* Found entities */}
      {foundEntities.length > 0 && (
        <div>
          <div className="gap-card__label">Found</div>
          <div className="gap-card__pills">
            {foundEntities.map((name, i) => (
              <span key={i} className="entity-pill" style={{ cursor: 'default' }}>{name}</span>
            ))}
          </div>
        </div>
      )}

      {/* Missing info */}
      {result.ddc_class !== 'CLEAN' && gapDescriptions.length > 0 && (
        <div style={{ marginTop: 'var(--cb-space-sm)' }}>
          <div className="gap-card__label">Missing</div>
          {gapDescriptions.slice(0, 2).map((desc, i) => (
            <div key={i} className="gap-card__detail">{desc}</div>
          ))}
        </div>
      )}

      {/* Suggested action */}
      <div className="gap-card__action">
        <div>
          <div className="gap-card__label">Suggested action</div>
          <div className="gap-card__suggested">{suggestedAction}</div>
        </div>
        {result.ddc_class !== 'CLEAN' && (
          <button
            className="score-badge score-badge--incomplete"
            style={{ cursor: 'pointer', border: '1px solid var(--cb-border)' }}
          >
            Start curation
          </button>
        )}
      </div>

      {/* Source + expand */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'var(--cb-space-md)', paddingTop: 'var(--cb-space-sm)', borderTop: '1px solid var(--cb-border)' }}>
        <SourceBadge source={result.source} persona={result.persona} />
        <button
          onClick={() => setExpanded(!expanded)}
          style={{ background: 'none', border: 'none', color: 'var(--cb-text-faint)', cursor: 'pointer', fontSize: 'var(--cb-font-size-xs)' }}
        >
          {expanded ? 'Hide answer ▲' : 'Show answer ▼'}
        </button>
      </div>

      {/* Expanded answer */}
      {expanded && (
        <div style={{ marginTop: 'var(--cb-space-md)', padding: 'var(--cb-space-md)', background: 'var(--cb-surface-raised)', borderRadius: 'var(--cb-radius-sm)', fontSize: 'var(--cb-font-size-sm)', color: 'var(--cb-text-muted)', lineHeight: 1.6, maxHeight: 300, overflowY: 'auto' }}>
          {result.answer}
        </div>
      )}
    </div>
  );
}

export default function GapsView({ results, stats }: GapsViewProps) {
  const [activeTab, setActiveTab] = useState<TabKey>('MISSING');
  const [sourceFilter, setSourceFilter] = useState<string>('all');

  const sources = useMemo(() => {
    const s = new Set(results.map(r => r.source));
    return ['all', ...Array.from(s).sort()];
  }, [results]);

  const filtered = useMemo(() => {
    let f = results.filter(r => r.ddc_class === activeTab);
    if (sourceFilter !== 'all') {
      f = f.filter(r => r.source === sourceFilter);
    }
    return f;
  }, [results, activeTab, sourceFilter]);

  if (results.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: 'var(--cb-space-2xl)', color: 'var(--cb-text-faint)' }}>
        <p>Run <code>context-blocks eval --personas --work-items</code> to generate gap analysis.</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 900 }}>
      <CoverageHeader stats={stats} />

      {/* Tabs */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--cb-space-md)' }}>
        <div className="tab-group" style={{ marginBottom: 0 }}>
          {(['CLEAN', 'INCOMPLETE', 'MISSING'] as TabKey[]).map(tab => {
            const count = results.filter(r => r.ddc_class === tab).length;
            return (
              <button
                key={tab}
                className={`tab-group__tab ${activeTab === tab ? 'tab-group__tab--active' : ''}`}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
                <span className="tab-group__tab-count">{count}</span>
              </button>
            );
          })}
        </div>

        {/* Source filter */}
        <select
          value={sourceFilter}
          onChange={(e) => setSourceFilter(e.target.value)}
          style={{
            background: 'var(--cb-surface)', border: '1px solid var(--cb-border)',
            borderRadius: 'var(--cb-radius-sm)', color: 'var(--cb-text-muted)',
            padding: '4px 8px', fontSize: 'var(--cb-font-size-xs)',
          }}
        >
          {sources.map(s => (
            <option key={s} value={s}>{s === 'all' ? 'All sources' : s}</option>
          ))}
        </select>
      </div>

      {/* Gap cards */}
      {filtered.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 'var(--cb-space-xl)', color: 'var(--cb-text-faint)' }}>
          No {activeTab.toLowerCase()} questions{sourceFilter !== 'all' ? ` from ${sourceFilter}` : ''}.
        </div>
      ) : (
        filtered.map((r, i) => <GapCard key={i} result={r} />)
      )}
    </div>
  );
}
