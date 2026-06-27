/**
 * EvalsView — Eval Run Explorer dashboard.
 *
 * Layout (top → bottom):
 * 1. Run header — run selector, question count, avg latency
 * 2. KPI strip — CLEAN / INCOMPLETE / MISSING with coverage bar
 * 3. Breakdown row — source mix + layer bars side by side
 * 4. Persona cards (if persona data exists)
 * 5. Question explorer — filter chips + expandable rows
 */
import { useState, useMemo, useCallback } from 'react';
import type { EvalRun, EvalResult, EvalStats, DDCClass } from '../../lib/types';

interface Props {
  runs: EvalRun[];
}

// ── Shared badges ─────────────────────────────────────────────────────────

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

// ── 1. Run Header ─────────────────────────────────────────────────────────

function RunHeader({ runs, activeRunId, onSelect }: {
  runs: EvalRun[];
  activeRunId: string;
  onSelect: (id: string) => void;
}) {
  const run = runs.find(r => r.id === activeRunId);
  if (!run) return null;

  const avgMs = run.results.length > 0
    ? Math.round(run.results.reduce((s, r) => s + r.total_ms, 0) / run.results.length)
    : 0;

  return (
    <div className="evals__header">
      <div className="evals__header-left">
        <h1 className="evals__title">Eval Run Explorer</h1>
        <p className="evals__subtitle">
          Knowledge base coverage scored against {run.stats.total} questions
        </p>
      </div>
      <div className="evals__header-right">
        <select
          value={activeRunId}
          onChange={e => onSelect(e.target.value)}
          className="evals__run-select"
        >
          {runs.map(r => (
            <option key={r.id} value={r.id}>
              {r.label} ({r.stats.total} questions)
            </option>
          ))}
        </select>
        <div className="evals__header-meta">
          <span className="evals__meta-item">{run.stats.total} questions</span>
          <span className="evals__meta-sep">·</span>
          <span className="evals__meta-item">avg {(avgMs / 1000).toFixed(1)}s</span>
        </div>
      </div>
    </div>
  );
}

// ── 2. KPI Strip ──────────────────────────────────────────────────────────

function KPIStrip({ stats }: { stats: EvalStats }) {
  return (
    <div className="evals__kpi">
      <div className="evals__kpi-card">
        <div className="evals__kpi-value">{stats.total}</div>
        <div className="evals__kpi-label">Questions</div>
      </div>
      <div className="evals__kpi-card">
        <div className="evals__kpi-value" style={{ color: 'var(--cb-score-clean)' }}>
          {stats.cleanPct}%
        </div>
        <div className="evals__kpi-label">Clean</div>
        <div className="evals__kpi-count">{stats.clean} of {stats.total}</div>
      </div>
      <div className="evals__kpi-card">
        <div className="evals__kpi-value" style={{ color: 'var(--cb-score-incomplete)' }}>
          {stats.incompletePct}%
        </div>
        <div className="evals__kpi-label">Incomplete</div>
        <div className="evals__kpi-count">{stats.incomplete} of {stats.total}</div>
      </div>
      <div className="evals__kpi-card">
        <div className="evals__kpi-value" style={{ color: 'var(--cb-score-missing)' }}>
          {stats.missingPct}%
        </div>
        <div className="evals__kpi-label">Missing</div>
        <div className="evals__kpi-count">{stats.missing} of {stats.total}</div>
      </div>

      <div className="evals__kpi-bar">
        {stats.cleanPct > 0 && (
          <div style={{ width: `${stats.cleanPct}%`, background: 'var(--cb-score-clean)' }} />
        )}
        {stats.incompletePct > 0 && (
          <div style={{ width: `${stats.incompletePct}%`, background: 'var(--cb-score-incomplete)' }} />
        )}
        {stats.missingPct > 0 && (
          <div style={{ width: `${stats.missingPct}%`, background: 'var(--cb-score-missing)' }} />
        )}
      </div>
    </div>
  );
}

// ── 3. Breakdown Row ──────────────────────────────────────────────────────

function SourceBreakdown({ perSource }: { perSource: EvalStats['perSource'] }) {
  const sources = Object.entries(perSource);
  if (sources.length === 0) return null;

  return (
    <div className="evals__breakdown-card">
      <h3 className="evals__breakdown-title">By Source</h3>
      <div className="evals__breakdown-items">
        {sources.map(([source, counts]) => {
          const total = counts.clean + counts.incomplete + counts.missing;
          const cleanPct = total > 0 ? Math.round(counts.clean / total * 100) : 0;
          return (
            <div key={source} className="evals__source-row">
              <div className="evals__source-label">
                <SourceBadge source={source} />
                <span className="evals__source-count">{total}</span>
              </div>
              <div className="evals__source-bar">
                {counts.clean > 0 && (
                  <div style={{ width: `${counts.clean / total * 100}%`, background: 'var(--cb-score-clean)' }} />
                )}
                {counts.incomplete > 0 && (
                  <div style={{ width: `${counts.incomplete / total * 100}%`, background: 'var(--cb-score-incomplete)' }} />
                )}
                {counts.missing > 0 && (
                  <div style={{ width: `${counts.missing / total * 100}%`, background: 'var(--cb-score-missing)' }} />
                )}
              </div>
              <span className="evals__source-pct">{cleanPct}%</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function LayerBreakdown({ perLayer }: { perLayer: EvalStats['perLayer'] }) {
  const layers = Object.entries(perLayer).sort((a, b) => {
    const aTotal = a[1].clean + a[1].incomplete + a[1].missing;
    const bTotal = b[1].clean + b[1].incomplete + b[1].missing;
    return bTotal - aTotal;
  });

  if (layers.length === 0) return null;
  const maxTotal = Math.max(...layers.map(([_, v]) => v.clean + v.incomplete + v.missing));

  return (
    <div className="evals__breakdown-card">
      <h3 className="evals__breakdown-title">By Knowledge Layer</h3>
      <div className="evals__breakdown-items">
        {layers.map(([layer, counts]) => {
          const total = counts.clean + counts.incomplete + counts.missing;
          const cleanPct = total > 0 ? Math.round(counts.clean / total * 100) : 0;
          return (
            <div key={layer} className="evals__layer-row">
              <span className="evals__layer-label">{layer || 'unclassified'}</span>
              <div className="evals__layer-bar">
                {counts.clean > 0 && (
                  <div style={{ width: `${counts.clean / maxTotal * 100}%`, background: 'var(--cb-score-clean)' }} />
                )}
                {counts.incomplete > 0 && (
                  <div style={{ width: `${counts.incomplete / maxTotal * 100}%`, background: 'var(--cb-score-incomplete)' }} />
                )}
                {counts.missing > 0 && (
                  <div style={{ width: `${counts.missing / maxTotal * 100}%`, background: 'var(--cb-score-missing)' }} />
                )}
              </div>
              <span className="evals__layer-pct">{cleanPct}%</span>
              <span className="evals__layer-count">{total}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── 4. Persona Cards ──────────────────────────────────────────────────────

function PersonaCards({ perPersona }: { perPersona: EvalStats['perPersona'] }) {
  const personas = Object.entries(perPersona);
  if (personas.length === 0) return null;

  return (
    <div className="evals__section">
      <h3 className="evals__section-title">Coverage by Persona</h3>
      <p className="evals__section-desc">
        How well the KB serves each role. 0% means no question from this persona was fully answerable.
      </p>
      <div className="evals__persona-grid">
        {personas.map(([name, counts]) => {
          const total = counts.clean + counts.incomplete + counts.missing;
          const cleanPct = total > 0 ? Math.round(counts.clean / total * 100) : 0;
          return (
            <div key={name} className="persona-card">
              <div className="persona-card__name">{name}</div>
              <div className="persona-card__coverage" style={{
                color: cleanPct > 50 ? 'var(--cb-score-clean)'
                  : cleanPct > 0 ? 'var(--cb-score-incomplete)'
                  : 'var(--cb-score-missing)',
              }}>
                {cleanPct}%
              </div>
              <div className="evals__persona-bar">
                {counts.clean > 0 && <div style={{ width: `${counts.clean / total * 100}%`, background: 'var(--cb-score-clean)' }} />}
                {counts.incomplete > 0 && <div style={{ width: `${counts.incomplete / total * 100}%`, background: 'var(--cb-score-incomplete)' }} />}
                {counts.missing > 0 && <div style={{ width: `${counts.missing / total * 100}%`, background: 'var(--cb-score-missing)' }} />}
              </div>
              <div className="persona-card__breakdown">
                <span>{counts.clean} clean</span>
                <span>{counts.incomplete} incomplete</span>
                <span>{counts.missing} missing</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── 5. Question Explorer ──────────────────────────────────────────────────

type ScoreFilter = DDCClass | 'all';

function QuestionExplorer({ results }: { results: EvalResult[] }) {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);
  const [scoreFilter, setScoreFilter] = useState<ScoreFilter>('all');
  const [sourceFilter, setSourceFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [gapsOnly, setGapsOnly] = useState(false);

  const sources = useMemo(() => {
    const s = new Set(results.map(r => r.source));
    return ['all', ...Array.from(s).sort()];
  }, [results]);

  const filtered = useMemo(() => {
    let f = results;
    if (scoreFilter !== 'all') f = f.filter(r => r.ddc_class === scoreFilter);
    if (sourceFilter !== 'all') f = f.filter(r => r.source === sourceFilter);
    if (gapsOnly) f = f.filter(r => r.gaps.length > 0);
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      f = f.filter(r =>
        (r.topic || '').toLowerCase().includes(q) ||
        r.question.toLowerCase().includes(q) ||
        (r.source_file || '').toLowerCase().includes(q)
      );
    }
    return f;
  }, [results, scoreFilter, sourceFilter, gapsOnly, searchQuery]);

  const toggleExpand = useCallback((idx: number) => {
    setExpandedIdx(prev => prev === idx ? null : idx);
  }, []);

  const scoreCounts = useMemo(() => ({
    all: results.length,
    CLEAN: results.filter(r => r.ddc_class === 'CLEAN').length,
    INCOMPLETE: results.filter(r => r.ddc_class === 'INCOMPLETE').length,
    MISSING: results.filter(r => r.ddc_class === 'MISSING').length,
  }), [results]);

  return (
    <div className="evals__section">
      <h3 className="evals__section-title">Question Explorer</h3>

      {/* Search + filters */}
      <div className="evals__filters">
        <input
          type="text"
          placeholder="Search questions..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          className="evals__search"
        />

        <div className="evals__filter-chips">
          {(['all', 'CLEAN', 'INCOMPLETE', 'MISSING'] as ScoreFilter[]).map(s => (
            <button
              key={s}
              onClick={() => setScoreFilter(s)}
              className={`evals__chip ${scoreFilter === s ? 'evals__chip--active' : ''} ${
                s === 'CLEAN' ? 'evals__chip--clean'
                : s === 'INCOMPLETE' ? 'evals__chip--incomplete'
                : s === 'MISSING' ? 'evals__chip--missing'
                : ''
              }`}
            >
              {s === 'all' ? 'All' : s}
              <span className="evals__chip-count">{scoreCounts[s]}</span>
            </button>
          ))}
        </div>

        <div className="evals__filter-row">
          <select
            value={sourceFilter}
            onChange={e => setSourceFilter(e.target.value)}
            className="evals__filter-select"
          >
            {sources.map(s => (
              <option key={s} value={s}>{s === 'all' ? 'All sources' : s}</option>
            ))}
          </select>

          <label className="evals__filter-toggle">
            <input
              type="checkbox"
              checked={gapsOnly}
              onChange={e => setGapsOnly(e.target.checked)}
            />
            <span>Has gaps only</span>
          </label>
        </div>
      </div>

      {/* Results count */}
      <div className="evals__results-count">
        {filtered.length === results.length
          ? `${results.length} questions`
          : `${filtered.length} of ${results.length} questions`}
      </div>

      {/* Question rows */}
      {filtered.length === 0 ? (
        <div className="evals__empty">No questions match your filters.</div>
      ) : (
        <div className="evals__question-list">
          {filtered.map((r, i) => (
            <QuestionRow
              key={i}
              result={r}
              isExpanded={expandedIdx === i}
              onToggle={() => toggleExpand(i)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function QuestionRow({ result, isExpanded, onToggle }: {
  result: EvalResult;
  isExpanded: boolean;
  onToggle: () => void;
}) {
  const gapSummary = result.gaps.length > 0
    ? result.gaps[0].description.slice(0, 60)
    : null;

  return (
    <div className={`evals__qrow ${isExpanded ? 'evals__qrow--expanded' : ''}`}>
      <div className="evals__qrow-header" onClick={onToggle}>
        <div className="evals__qrow-main">
          <div className="evals__qrow-topic">
            {result.topic || result.question.slice(0, 80)}
          </div>
          <div className="evals__qrow-meta">
            <SourceBadge source={result.source} persona={result.persona} />
            {result.layer_hint && (
              <span className="evals__qrow-layer">{result.layer_hint}</span>
            )}
            {gapSummary && (
              <span className="evals__qrow-gap-hint">{gapSummary}</span>
            )}
          </div>
        </div>
        <div className="evals__qrow-right">
          <span className="evals__qrow-entities">
            {result.entities_retrieved} entities
          </span>
          <span className="evals__qrow-time">
            {(result.total_ms / 1000).toFixed(1)}s
          </span>
          <ScoreBadge score={result.ddc_class} />
          <span className="evals__qrow-chevron">{isExpanded ? '▲' : '▼'}</span>
        </div>
      </div>

      {isExpanded && <QuestionDetail result={result} />}
    </div>
  );
}

function QuestionDetail({ result }: { result: EvalResult }) {
  const topHops = result.hops.slice(0, 8);
  const gapHops = result.hops.filter(h => h.gap_flag);

  return (
    <div className="evals__qdetail">
      {/* Answer */}
      <div className="evals__qdetail-section">
        <div className="evals__qdetail-label">Answer</div>
        <div className="evals__qdetail-answer">
          {result.answer.slice(0, 600)}{result.answer.length > 600 ? '...' : ''}
        </div>
      </div>

      {/* Retrieved entities */}
      {topHops.length > 0 && (
        <div className="evals__qdetail-section">
          <div className="evals__qdetail-label">
            Retrieved Entities
            <span className="evals__qdetail-count">{result.entities_retrieved}</span>
          </div>
          <div className="evals__qdetail-hops">
            {topHops.map((h, i) => (
              <div key={i} className={`evals__hop ${h.gap_flag ? 'evals__hop--gap' : ''}`}>
                <span className="evals__hop-rank">#{h.hop_number}</span>
                <span className="evals__hop-name">{h.entity_name}</span>
                <span className="evals__hop-type">{h.entity_type}</span>
                <span className="evals__hop-score">{h.fused_score.toFixed(2)}</span>
                {h.found_by && h.found_by.length > 0 && (
                  <span className="found-by">
                    {h.found_by.map((m, j) => (
                      <span key={j} className={`found-by__method found-by__method--${m}`}>{m}</span>
                    ))}
                  </span>
                )}
                {h.gap_flag && h.gap_reason && (
                  <span className="evals__hop-gap-reason">{h.gap_reason}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Citations */}
      {result.citations.length > 0 && (
        <div className="evals__qdetail-section">
          <div className="evals__qdetail-label">Citations</div>
          <div className="evals__qdetail-pills">
            {[...new Set(result.citations)].slice(0, 10).map((c, i) => (
              <span key={i} className="entity-pill" style={{ cursor: 'default' }}>{c}</span>
            ))}
          </div>
        </div>
      )}

      {/* Gaps */}
      {result.gaps.length > 0 && (
        <div className="evals__qdetail-section">
          <div className="evals__qdetail-label">
            Gap Diagnosis
            <span className="evals__qdetail-count">{result.gaps.length}</span>
          </div>
          <div className="evals__qdetail-gaps">
            {result.gaps.map((g, i) => (
              <div key={i} className={`evals__gap evals__gap--${g.severity}`}>
                <div className="evals__gap-header">
                  <span className={`evals__gap-severity evals__gap-severity--${g.severity}`}>
                    {g.severity}
                  </span>
                  <span className="evals__gap-type">{g.gap_type}</span>
                </div>
                <div className="evals__gap-desc">{g.description}</div>
                {g.suggested_action && (
                  <div className="evals__gap-action">{g.suggested_action}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Trace summary */}
      {result.trace_summary && (
        <div className="evals__qdetail-section">
          <div className="evals__qdetail-label">Trace</div>
          <div className="evals__qdetail-trace">{result.trace_summary}</div>
        </div>
      )}
    </div>
  );
}

// ── Main ──────────────────────────────────────────────────────────────────

export default function EvalsView({ runs }: Props) {
  const [activeRunId, setActiveRunId] = useState(
    runs.length > 0 ? runs[runs.length - 1].id : ''
  );

  if (runs.length === 0) {
    return (
      <div className="evals__empty-state">
        <h2>No eval runs found</h2>
        <p>Run <code>context-blocks eval</code> to generate evaluation results.</p>
      </div>
    );
  }

  const activeRun = runs.find(r => r.id === activeRunId) ?? runs[runs.length - 1];

  return (
    <div className="evals">
      <RunHeader
        runs={runs}
        activeRunId={activeRun.id}
        onSelect={setActiveRunId}
      />

      <KPIStrip stats={activeRun.stats} />

      <div className="evals__breakdown-row">
        <SourceBreakdown perSource={activeRun.stats.perSource} />
        <LayerBreakdown perLayer={activeRun.stats.perLayer} />
      </div>

      <PersonaCards perPersona={activeRun.stats.perPersona} />

      <QuestionExplorer results={activeRun.results} />
    </div>
  );
}
