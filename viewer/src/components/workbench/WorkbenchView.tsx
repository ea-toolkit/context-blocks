import { useState, useMemo } from 'react';
import { getConfidenceTier } from '../../lib/types';
import type { CBQuestion, CBEntity, EvalResult, EvalStats } from '../../lib/types';

// ── Types ──────────────────────────────────────────────────────────────────

interface LintIssueRow {
  entity: CBEntity;
  issues: string[];
  owner?: string;
}

interface Props {
  questions: CBQuestion[];
  lintIssues: LintIssueRow[];
  reviewQueue: CBEntity[];
  evalResults: EvalResult[];
  evalStats: EvalStats | null;
}

type Tab = 'coverage' | 'questions' | 'health' | 'review';

// ── Shared helpers ─────────────────────────────────────────────────────────

function EmptyState({ message }: { message: string }) {
  return (
    <div className="workbench__empty">{message}</div>
  );
}

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

function OwnerBadge({ owner }: { owner: string }) {
  return (
    <span className="badge" style={{
      background: 'rgba(124, 92, 252, 0.1)',
      color: 'var(--cb-primary)',
      fontSize: 'var(--cb-font-size-xs)',
    }}>
      {owner}
    </span>
  );
}

// ── Tab 1: Coverage (from eval results) ────────────────────────────────────

type CoverageFilter = 'CLEAN' | 'INCOMPLETE' | 'MISSING';

function CoverageTab({ results, stats }: { results: EvalResult[]; stats: EvalStats }) {
  const [activeFilter, setActiveFilter] = useState<CoverageFilter>('MISSING');
  const [sourceFilter, setSourceFilter] = useState('all');

  const sources = useMemo(() => {
    const s = new Set(results.map(r => r.source));
    return ['all', ...Array.from(s).sort()];
  }, [results]);

  const filtered = useMemo(() => {
    let f = results.filter(r => r.ddc_class === activeFilter);
    if (sourceFilter !== 'all') f = f.filter(r => r.source === sourceFilter);
    return f;
  }, [results, activeFilter, sourceFilter]);

  return (
    <div>
      {/* Big numbers */}
      <div className="workbench__coverage-stats">
        <div>
          <span className="workbench__coverage-num" style={{ color: 'var(--cb-score-clean)' }}>
            {stats.cleanPct}%
          </span>
          <span className="workbench__coverage-label">clean</span>
        </div>
        <div>
          <span className="workbench__coverage-num" style={{ color: 'var(--cb-score-incomplete)' }}>
            {stats.incompletePct}%
          </span>
          <span className="workbench__coverage-label">incomplete</span>
        </div>
        <div>
          <span className="workbench__coverage-num" style={{ color: 'var(--cb-score-missing)' }}>
            {stats.missingPct}%
          </span>
          <span className="workbench__coverage-label">missing</span>
        </div>
      </div>

      {/* Coverage bar */}
      <div className="workbench__coverage-bar">
        {stats.cleanPct > 0 && <div style={{ width: `${stats.cleanPct}%`, background: 'var(--cb-score-clean)' }} />}
        {stats.incompletePct > 0 && <div style={{ width: `${stats.incompletePct}%`, background: 'var(--cb-score-incomplete)' }} />}
        {stats.missingPct > 0 && <div style={{ width: `${stats.missingPct}%`, background: 'var(--cb-score-missing)' }} />}
      </div>

      {/* Layer breakdown */}
      {Object.keys(stats.perLayer).length > 0 && (
        <p className="workbench__coverage-layers">
          {Object.entries(stats.perLayer)
            .filter(([_, v]) => v.missing > 0)
            .sort((a, b) => b[1].missing - a[1].missing)
            .slice(0, 3)
            .map(([layer, v]) => {
              const total = v.clean + v.incomplete + v.missing;
              return `${layer} (${Math.round(v.missing / total * 100)}% missing)`;
            })
            .join(', ')}{' '}
          carry the most missing knowledge.
        </p>
      )}

      {/* Filter row */}
      <div className="workbench__filter-row">
        <div className="tab-group" style={{ marginBottom: 0 }}>
          {(['CLEAN', 'INCOMPLETE', 'MISSING'] as CoverageFilter[]).map(tab => {
            const count = results.filter(r => r.ddc_class === tab).length;
            return (
              <button
                key={tab}
                className={`tab-group__tab ${activeFilter === tab ? 'tab-group__tab--active' : ''}`}
                onClick={() => setActiveFilter(tab)}
              >
                {tab}
                <span className="tab-group__tab-count">{count}</span>
              </button>
            );
          })}
        </div>
        <select
          value={sourceFilter}
          onChange={(e) => setSourceFilter(e.target.value)}
          className="workbench__source-select"
        >
          {sources.map(s => (
            <option key={s} value={s}>{s === 'all' ? 'All sources' : s}</option>
          ))}
        </select>
      </div>

      {/* Gap cards */}
      {filtered.length === 0 ? (
        <EmptyState message={`No ${activeFilter.toLowerCase()} questions${sourceFilter !== 'all' ? ` from ${sourceFilter}` : ''}.`} />
      ) : (
        filtered.map((r, i) => <GapCard key={i} result={r} />)
      )}
    </div>
  );
}

function GapCard({ result }: { result: EvalResult }) {
  const [expanded, setExpanded] = useState(false);
  const foundEntities = result.hops.slice(0, 5).map(h => h.entity_name);
  const gapDescriptions = result.gaps.map(g => g.description);

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

      {result.ddc_class !== 'CLEAN' && gapDescriptions.length > 0 && (
        <div style={{ marginTop: 'var(--cb-space-sm)' }}>
          <div className="gap-card__label">Missing</div>
          {gapDescriptions.slice(0, 2).map((desc, i) => (
            <div key={i} className="gap-card__detail">{desc}</div>
          ))}
        </div>
      )}

      <div className="gap-card__action">
        <div>
          <div className="gap-card__label">Suggested action</div>
          <div className="gap-card__suggested">{suggestedAction}</div>
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'var(--cb-space-md)', paddingTop: 'var(--cb-space-sm)', borderTop: '1px solid var(--cb-border)' }}>
        <SourceBadge source={result.source} persona={result.persona} />
        <button
          onClick={() => setExpanded(!expanded)}
          style={{ background: 'none', border: 'none', color: 'var(--cb-text-faint)', cursor: 'pointer', fontSize: 'var(--cb-font-size-xs)' }}
        >
          {expanded ? 'Hide answer ▲' : 'Show answer ▼'}
        </button>
      </div>

      {expanded && (
        <div className="workbench__expanded-answer">
          {result.answer}
        </div>
      )}
    </div>
  );
}

// ── Tab 2: Questions ───────────────────────────────────────────────────────

function QuestionsTab({ questions }: { questions: CBQuestion[] }) {
  if (questions.length === 0) {
    return <EmptyState message="No unresolved questions. The knowledge base looks complete." />;
  }

  return (
    <div>
      {questions.map((q, i) => (
        <div key={i} className="question-card" style={{ marginBottom: 'var(--cb-space-sm)' }}>
          <div className="question-card__text">{q.text}</div>
          <div className="question-card__source" style={{ marginTop: 'var(--cb-space-xs)', display: 'flex', alignItems: 'center', gap: 'var(--cb-space-sm)', flexWrap: 'wrap' }}>
            <span>From:</span>
            <a href={`/explorer?entity=${q.entityId}&type=${q.entityType}`}>
              {q.entityName}
            </a>
            <span className="badge badge--question" style={{
              opacity: getConfidenceTier(q.entityConfidence) === 'sketched' ? 0.4
                : getConfidenceTier(q.entityConfidence) === 'muted' ? 0.65 : 1,
            }}>
              {q.entityType} · {(q.entityConfidence * 100).toFixed(0)}% confidence
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Tab 3: Health (lint issues) ────────────────────────────────────────────

const ISSUE_SEVERITY: Record<string, { bg: string; color: string }> = {
  'Missing description':       { bg: 'rgba(239,68,68,0.12)',  color: '#f87171' },
  'No relationships (orphan)': { bg: 'rgba(245,158,11,0.12)', color: '#fbbf24' },
  'No source documents':       { bg: 'rgba(245,158,11,0.12)', color: '#fbbf24' },
};
const DEFAULT_SEVERITY = { bg: 'rgba(148,163,184,0.12)', color: '#94a3b8' };

function issueBadgeStyle(issue: string): React.CSSProperties {
  if (issue.startsWith('Low confidence')) return { background: 'rgba(239,68,68,0.12)', color: '#f87171' };
  if (issue.includes('broken reference')) return { background: 'rgba(239,68,68,0.12)', color: '#f87171' };
  const s = ISSUE_SEVERITY[issue] ?? DEFAULT_SEVERITY;
  return { background: s.bg, color: s.color };
}

function HealthTab({ lintIssues }: { lintIssues: LintIssueRow[] }) {
  if (lintIssues.length === 0) {
    return <EmptyState message="No health issues found. All entities look healthy." />;
  }

  return (
    <div>
      {lintIssues.map((row, i) => {
        const sevColor = row.issues.length >= 4 ? '#f87171' : row.issues.length >= 2 ? '#fbbf24' : '#94a3b8';
        return (
          <div key={i} className="workbench__health-card">
            <span className="workbench__health-dot" style={{ background: sevColor }} />
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="workbench__health-header">
                <a href={`/explorer?entity=${row.entity.id}&type=${row.entity.type}`} className="workbench__health-name">
                  {row.entity.name}
                </a>
                <span className="badge" style={{ background: 'var(--cb-surface-raised)', color: 'var(--cb-text-faint)' }}>
                  {row.entity.typeLabel}
                </span>
                {row.owner && <OwnerBadge owner={row.owner} />}
                <span className="workbench__health-count">
                  {row.issues.length} issue{row.issues.length !== 1 ? 's' : ''}
                </span>
              </div>
              <div className="workbench__health-issues">
                {row.issues.map((issue, j) => (
                  <span key={j} className="badge" style={issueBadgeStyle(issue)}>{issue}</span>
                ))}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ── Tab 4: Review queue ────────────────────────────────────────────────────

function ReviewTab({ reviewQueue }: { reviewQueue: CBEntity[] }) {
  if (reviewQueue.length === 0) {
    return <EmptyState message="No entities tagged for review." />;
  }

  return (
    <div>
      {reviewQueue.map((entity, i) => (
        <div key={i} className="workbench__health-card">
          <div style={{ flex: 1, minWidth: 0 }}>
            <div className="workbench__health-header">
              <a href={`/explorer?entity=${entity.id}&type=${entity.type}`} className="workbench__health-name">
                {entity.name}
              </a>
              <span className="badge" style={{ background: 'var(--cb-surface-raised)', color: 'var(--cb-text-faint)' }}>
                {entity.typeLabel}
              </span>
              <span className="badge badge--question" style={{
                opacity: getConfidenceTier(entity.confidence) === 'sketched' ? 0.4
                  : getConfidenceTier(entity.confidence) === 'muted' ? 0.65 : 1,
              }}>
                {(entity.confidence * 100).toFixed(0)}% confidence
              </span>
            </div>
            {entity.description && (
              <div className="workbench__review-desc">{entity.description}</div>
            )}
            {entity.tags.length > 0 && (
              <div className="workbench__health-issues">
                {entity.tags.map((tag, t) => (
                  <span key={t} className="badge" style={{ background: 'var(--cb-surface-raised)', color: 'var(--cb-text-faint)' }}>
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Main ──────────────────────────────────────────────────────────────────

export default function WorkbenchView({ questions, lintIssues, reviewQueue, evalResults, evalStats }: Props) {
  const hasEvals = evalResults.length > 0 && evalStats !== null;
  const [activeTab, setActiveTab] = useState<Tab>(hasEvals ? 'coverage' : 'questions');

  const tabs: { key: Tab; label: string; count: number }[] = [
    ...(hasEvals ? [{ key: 'coverage' as Tab, label: 'Coverage', count: evalResults.length }] : []),
    { key: 'questions', label: 'Questions', count: questions.length },
    { key: 'health',    label: 'Health',    count: lintIssues.length },
    { key: 'review',    label: 'Review',    count: reviewQueue.length },
  ];

  return (
    <div className="workbench">
      <div className="workbench__header">
        <p className="workbench__subtitle">
          Everything that needs human attention — coverage gaps, unresolved questions, entity health, and review queue.
        </p>
      </div>

      {/* Tab bar */}
      <div className="workbench__tabs">
        {tabs.map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`workbench__tab ${activeTab === tab.key ? 'workbench__tab--active' : ''}`}
          >
            {tab.label}
            <span className={`workbench__tab-count ${activeTab === tab.key ? 'workbench__tab-count--active' : ''}`}>
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === 'coverage' && hasEvals && <CoverageTab results={evalResults} stats={evalStats} />}
      {activeTab === 'questions' && <QuestionsTab questions={questions} />}
      {activeTab === 'health' && <HealthTab lintIssues={lintIssues} />}
      {activeTab === 'review' && <ReviewTab reviewQueue={reviewQueue} />}
    </div>
  );
}
