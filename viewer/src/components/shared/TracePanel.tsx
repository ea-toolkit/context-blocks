/**
 * Retrieval Trace Panel — shows the full retrieval path for a query.
 *
 * Two audiences:
 *   User  — understand what was found, what's missing, how confident
 *   Builder — debug pipeline stages, see funnel, inspect scores
 */
import { useState } from 'react';
import { ChevronDown, ChevronRight, HelpCircle, Zap, Search, GitBranch, Layers, Filter, FileText } from 'lucide-react';
import type { EvalHop, StageTrace } from '../../lib/types';

interface TracePanelProps {
  hops: EvalHop[];
  stageFunnel?: StageTrace;
}

const GAP_REASON_LABELS: Record<string, string> = {
  low_confidence: 'Low documentation quality — entity may be poorly documented',
  orphan_entity: 'No typed relationships — isolated entity in the knowledge graph',
};

const METHOD_LABELS: Record<string, string> = {
  vector: 'Semantic similarity',
  keyword: 'Text match',
  graph: 'Relationship traversal',
};

function FoundByBadges({ methods }: { methods: string[] | null }) {
  if (!methods || methods.length === 0) return null;
  return (
    <span className="found-by">
      {methods.map(m => (
        <span
          key={m}
          className={`found-by__method found-by__method--${m}`}
          title={METHOD_LABELS[m] || m}
        >
          {m}
        </span>
      ))}
    </span>
  );
}

function HopRow({ hop }: { hop: EvalHop }) {
  const isGap = hop.gap_flag;
  return (
    <div className={`trace-hop ${isGap ? 'trace-hop--gap' : ''}`}>
      <div className="trace-hop__content">
        <div className="trace-hop__name">
          {hop.entity_name}
        </div>
        <div className="trace-hop__meta">
          <span className="badge badge--layer" style={{ fontSize: '10px' }}>
            {hop.entity_type}
          </span>
          <FoundByBadges methods={hop.found_by} />
        </div>
        <div className="trace-hop__scores">
          <span title="Entity documentation quality in the knowledge base">
            Quality {(hop.confidence * 100).toFixed(0)}%
          </span>
          <span className="trace-hop__scores-sep">·</span>
          <span title="How relevant this entity is to your question (higher = better match)">
            Relevance {hop.fused_score.toFixed(2)}
          </span>
        </div>
        {hop.relationship_from && (
          <div className="trace-hop__via">
            via <strong>{hop.relationship_type}</strong> from {hop.relationship_from}
          </div>
        )}
        {isGap && hop.gap_reason && (
          <div className="trace-hop__gap-reason">
            ⚠ {GAP_REASON_LABELS[hop.gap_reason] || hop.gap_reason}
          </div>
        )}
      </div>
    </div>
  );
}

function PipelineFunnel({ stages }: { stages: StageTrace }) {
  const steps = [
    { label: 'Vector', count: stages.vector_candidates, icon: <Zap size={10} />, desc: 'Semantic similarity search' },
    { label: 'Keyword', count: stages.keyword_candidates, icon: <Search size={10} />, desc: 'Text pattern matching' },
    { label: 'Graph', count: stages.graph_candidates, icon: <GitBranch size={10} />, desc: 'Relationship traversal' },
    { label: 'Fused', count: stages.fused_unique, icon: <Layers size={10} />, desc: 'Merged and ranked' },
    { label: 'Deduped', count: stages.after_dedup, icon: <Filter size={10} />, desc: 'Duplicates removed' },
    { label: 'Selected', count: stages.context_selected, icon: <FileText size={10} />, desc: 'Sent to LLM' },
  ];

  const max = Math.max(...steps.map(s => s.count), 1);
  const tokenPct = stages.token_budget > 0
    ? Math.round((stages.tokens_used / stages.token_budget) * 100)
    : 0;

  return (
    <div className="trace-funnel">
      <div className="trace-funnel__header">Pipeline Stages</div>
      <div className="stage-funnel">
        {steps.map(step => (
          <div key={step.label} className="stage-funnel__step" title={step.desc}>
            <span className="stage-funnel__label">
              {step.icon} {step.label}
            </span>
            <div
              className="stage-funnel__bar"
              style={{ width: `${(step.count / max) * 100}%`, minWidth: step.count > 0 ? '4px' : '0' }}
            />
            <span className="stage-funnel__count">{step.count}</span>
          </div>
        ))}
      </div>
      <div className="trace-funnel__tokens">
        <div className="trace-funnel__token-bar-track">
          <div
            className="trace-funnel__token-bar-fill"
            style={{ width: `${Math.min(tokenPct, 100)}%` }}
          />
        </div>
        <span className="trace-funnel__token-label">
          {stages.tokens_used.toLocaleString()} / {stages.token_budget.toLocaleString()} tokens
        </span>
      </div>
    </div>
  );
}

function HelpSection() {
  const [open, setOpen] = useState(false);
  return (
    <div className="trace-help">
      <button className="trace-help__toggle" onClick={() => setOpen(!open)}>
        <HelpCircle size={12} />
        How to read this trace
        {open ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
      </button>
      {open && (
        <div className="trace-help__body">
          <div className="trace-help__item">
            <strong>Quality %</strong> — How well-documented this entity is in the knowledge base (from extraction).
          </div>
          <div className="trace-help__item">
            <strong>Relevance</strong> — How closely this entity matches your question (0–1+, higher is better).
          </div>
          <div className="trace-help__item">
            <strong>Direct matches</strong> — Found directly from your question via semantic or keyword search.
          </div>
          <div className="trace-help__item">
            <strong>Graph hops</strong> — Found by following relationships from direct matches. Depth 1 = one hop away, depth 2 = two hops, etc.
          </div>
          <div className="trace-help__item">
            <span className="found-by__method found-by__method--vector" style={{ fontSize: 9 }}>vector</span>{' '}
            Semantic similarity · {' '}
            <span className="found-by__method found-by__method--keyword" style={{ fontSize: 9 }}>keyword</span>{' '}
            Text match · {' '}
            <span className="found-by__method found-by__method--graph" style={{ fontSize: 9 }}>graph</span>{' '}
            Relationship traversal
          </div>
          <div className="trace-help__item">
            <strong>⚠ Gap</strong> — Entity has a quality issue (low documentation or no relationships). These are flagged as knowledge gaps.
          </div>
        </div>
      )}
    </div>
  );
}

export default function TracePanel({ hops, stageFunnel }: TracePanelProps) {
  if (!hops || hops.length === 0) {
    return (
      <div className="trace-panel__header">
        <span className="trace-panel__title">Retrieval Trace</span>
        <span style={{ fontSize: 'var(--cb-font-size-xs)', color: 'var(--cb-text-faint)' }}>
          No entities retrieved
        </span>
      </div>
    );
  }

  const directHops = hops.filter(h => h.hop_number === 0);
  const graphHops = hops.filter(h => h.hop_number > 0);
  const gapCount = hops.filter(h => h.gap_flag).length;

  return (
    <div>
      {/* Header */}
      <div className="trace-panel__header">
        <span className="trace-panel__title">Retrieval Trace</span>
        <span style={{ fontSize: 'var(--cb-font-size-xs)', color: 'var(--cb-text-faint)' }}>
          {hops.length} entities
          {gapCount > 0 && (
            <span style={{ color: 'var(--cb-score-incomplete)', marginLeft: 6 }}>
              {gapCount} ⚠
            </span>
          )}
        </span>
      </div>

      {/* Pipeline funnel */}
      {stageFunnel && <PipelineFunnel stages={stageFunnel} />}

      {/* Direct matches section */}
      {directHops.length > 0 && (
        <div className="trace-section">
          <div className="trace-section__header">
            <span className="trace-section__title">Direct Matches</span>
            <span className="trace-section__count">{directHops.length}</span>
          </div>
          <div className="trace-section__desc">
            Found directly from your question
          </div>
          {directHops.map((hop, i) => (
            <HopRow key={`${hop.entity_id}-${i}`} hop={hop} />
          ))}
        </div>
      )}

      {/* Graph hops section */}
      {graphHops.length > 0 && (
        <div className="trace-section">
          <div className="trace-section__header">
            <span className="trace-section__title">Graph Hops</span>
            <span className="trace-section__count">{graphHops.length}</span>
          </div>
          <div className="trace-section__desc">
            Found by following relationships
          </div>
          {graphHops.map((hop, i) => (
            <HopRow key={`${hop.entity_id}-${i}`} hop={hop} />
          ))}
        </div>
      )}

      {/* Help legend */}
      <HelpSection />
    </div>
  );
}
