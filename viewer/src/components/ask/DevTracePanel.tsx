import { useState } from 'react';
import {
  ChevronDown, ChevronRight, Copy, Download, Check,
  Brain, Search, Merge, FileText, MessageSquare, AlertTriangle,
} from 'lucide-react';
import type { EvalHop, EvalGap, StageTrace } from '../../lib/types';

interface DevTracePanelProps {
  hops: EvalHop[];
  gaps: EvalGap[];
  stageTrace: StageTrace | null;
  citations: string[];
  answer: string;
  totalMs: number;
  question: string;
  ddcClass: string;
  rawResult: Record<string, unknown>;
}

type TabKey = 'intent' | 'retrieval' | 'fusion' | 'context' | 'answer' | 'gaps';

const TABS: { key: TabKey; label: string; icon: React.ReactNode }[] = [
  { key: 'intent', label: 'Intent', icon: <Brain size={13} /> },
  { key: 'retrieval', label: 'Retrieval', icon: <Search size={13} /> },
  { key: 'fusion', label: 'Fusion', icon: <Merge size={13} /> },
  { key: 'context', label: 'Context', icon: <FileText size={13} /> },
  { key: 'answer', label: 'Answer', icon: <MessageSquare size={13} /> },
  { key: 'gaps', label: 'Gaps', icon: <AlertTriangle size={13} /> },
];

function WeightBar({ label, value, max }: { label: string; value: number; max: number }) {
  const pct = max > 0 ? (value / max) * 100 : 0;
  return (
    <div className="dev-trace__weight-row">
      <span className="dev-trace__weight-label">{label}</span>
      <div className="dev-trace__weight-track">
        <div className="dev-trace__weight-fill" style={{ width: `${pct}%` }} />
      </div>
      <span className="dev-trace__weight-value">{value.toFixed(2)}</span>
    </div>
  );
}

function IntentTab({ stageTrace }: { stageTrace: StageTrace | null }) {
  if (!stageTrace) return <div className="dev-trace__empty">No trace data available</div>;

  const intents = stageTrace.intent_weights || {};
  const layers = stageTrace.layer_priorities || {};
  const maxIntent = Math.max(...Object.values(intents), 0.01);
  const maxLayer = Math.max(...Object.values(layers), 0.01);

  return (
    <div className="dev-trace__tab-content">
      <div className="dev-trace__section">
        <h4 className="dev-trace__section-title">Intent Weights</h4>
        {Object.keys(intents).length === 0 ? (
          <span className="dev-trace__muted">No intents detected</span>
        ) : (
          Object.entries(intents)
            .sort(([, a], [, b]) => b - a)
            .map(([key, val]) => (
              <WeightBar key={key} label={key} value={val} max={maxIntent} />
            ))
        )}
      </div>
      <div className="dev-trace__section">
        <h4 className="dev-trace__section-title">Layer Priorities</h4>
        {Object.keys(layers).length === 0 ? (
          <span className="dev-trace__muted">Default priorities</span>
        ) : (
          Object.entries(layers)
            .sort(([, a], [, b]) => b - a)
            .map(([key, val]) => (
              <WeightBar key={key} label={key} value={val} max={maxLayer} />
            ))
        )}
      </div>
    </div>
  );
}

function RetrievalTab({ stageTrace }: { stageTrace: StageTrace | null }) {
  if (!stageTrace) return <div className="dev-trace__empty">No trace data available</div>;

  const channels = [
    { label: 'Vector', count: stageTrace.vector_candidates, desc: 'Semantic similarity' },
    { label: 'Keyword', count: stageTrace.keyword_candidates, desc: 'Text pattern match' },
    { label: 'Graph', count: stageTrace.graph_candidates, desc: 'Relationship traversal' },
  ];
  const max = Math.max(...channels.map(c => c.count), 1);

  return (
    <div className="dev-trace__tab-content">
      <div className="dev-trace__section">
        <h4 className="dev-trace__section-title">Candidates per Channel</h4>
        {channels.map(ch => (
          <div key={ch.label} className="dev-trace__channel-row">
            <div className="dev-trace__channel-header">
              <span className="dev-trace__channel-label">{ch.label}</span>
              <span className="dev-trace__channel-desc">{ch.desc}</span>
              <span className="dev-trace__channel-count">{ch.count}</span>
            </div>
            <div className="dev-trace__weight-track">
              <div className="dev-trace__weight-fill" style={{ width: `${(ch.count / max) * 100}%` }} />
            </div>
          </div>
        ))}
      </div>
      <div className="dev-trace__section">
        <h4 className="dev-trace__section-title">Funnel</h4>
        <table className="dev-trace__table">
          <tbody>
            <tr><td>Total candidates</td><td>{stageTrace.vector_candidates + stageTrace.keyword_candidates + stageTrace.graph_candidates}</td></tr>
            <tr><td>After fusion (unique)</td><td>{stageTrace.fused_unique}</td></tr>
            <tr><td>After dedup</td><td>{stageTrace.after_dedup}</td></tr>
            <tr><td>Selected for context</td><td>{stageTrace.context_selected}</td></tr>
          </tbody>
        </table>
      </div>
      {stageTrace.search_ms != null && (
        <div className="dev-trace__timing">
          Search time: {stageTrace.search_ms}ms
        </div>
      )}
    </div>
  );
}

function FusionTab({ hops }: { hops: EvalHop[] }) {
  const directHops = hops.filter(h => h.hop_number === 0).sort((a, b) => b.fused_score - a.fused_score);
  const graphHops = hops.filter(h => h.hop_number > 0).sort((a, b) => b.fused_score - a.fused_score);

  const renderEntity = (hop: EvalHop, i: number) => (
    <div key={`${hop.entity_id}-${i}`} className={`dev-trace__entity-row ${hop.gap_flag ? 'dev-trace__entity-row--gap' : ''}`}>
      <span className="dev-trace__entity-rank">{i + 1}</span>
      <div className="dev-trace__entity-info">
        <div className="dev-trace__entity-name">{hop.entity_name}</div>
        <div className="dev-trace__entity-meta">
          <span>{hop.entity_type}</span>
          <span className="dev-trace__sep">/</span>
          <span>{hop.layer}</span>
          {hop.found_by && hop.found_by.map(m => (
            <span key={m} className={`found-by__method found-by__method--${m}`}>{m}</span>
          ))}
        </div>
        {hop.relationship_from && (
          <div className="dev-trace__entity-via">
            via <strong>{hop.relationship_type}</strong> from {hop.relationship_from}
          </div>
        )}
      </div>
      <div className="dev-trace__entity-scores">
        <div title="Fused score">
          <span className="dev-trace__score-label">score</span>
          <span className="dev-trace__score-value">{hop.fused_score.toFixed(3)}</span>
        </div>
        <div title="Documentation confidence">
          <span className="dev-trace__score-label">conf</span>
          <span className="dev-trace__score-value">{(hop.confidence * 100).toFixed(0)}%</span>
        </div>
      </div>
    </div>
  );

  return (
    <div className="dev-trace__tab-content">
      <div className="dev-trace__section">
        <h4 className="dev-trace__section-title">Direct Matches ({directHops.length})</h4>
        <div className="dev-trace__section-desc">Found directly from your question</div>
        <div className="dev-trace__entity-list">
          {directHops.map((hop, i) => renderEntity(hop, i))}
        </div>
      </div>
      {graphHops.length > 0 && (
        <div className="dev-trace__section">
          <h4 className="dev-trace__section-title">Graph Hops ({graphHops.length})</h4>
          <div className="dev-trace__section-desc">Found by following relationships</div>
          <div className="dev-trace__entity-list">
            {graphHops.map((hop, i) => renderEntity(hop, directHops.length + i))}
          </div>
        </div>
      )}
    </div>
  );
}

function ContextTab({ stageTrace, hops }: { stageTrace: StageTrace | null; hops: EvalHop[] }) {
  const tokensUsed = stageTrace?.tokens_used ?? 0;
  const tokenBudget = stageTrace?.token_budget ?? 0;
  const pct = tokenBudget > 0 ? Math.round((tokensUsed / tokenBudget) * 100) : 0;

  return (
    <div className="dev-trace__tab-content">
      <div className="dev-trace__section">
        <h4 className="dev-trace__section-title">Token Budget</h4>
        <div className="dev-trace__budget">
          <div className="dev-trace__budget-bar-track">
            <div
              className="dev-trace__budget-bar-fill"
              style={{ width: `${Math.min(pct, 100)}%` }}
            />
          </div>
          <div className="dev-trace__budget-label">
            {tokensUsed.toLocaleString()} / {tokenBudget.toLocaleString()} tokens ({pct}%)
          </div>
        </div>
      </div>
      <div className="dev-trace__section">
        <h4 className="dev-trace__section-title">Entities in Context ({stageTrace?.context_selected ?? hops.length})</h4>
        <table className="dev-trace__table dev-trace__table--full">
          <thead>
            <tr>
              <th>Entity</th>
              <th>Type</th>
              <th>Score</th>
              <th>Conf</th>
            </tr>
          </thead>
          <tbody>
            {[...hops].sort((a, b) => b.fused_score - a.fused_score).map((hop, i) => (
              <tr key={`${hop.entity_id}-${i}`} className={hop.gap_flag ? 'dev-trace__row--gap' : ''}>
                <td>{hop.entity_name}</td>
                <td>{hop.entity_type}</td>
                <td>{hop.fused_score.toFixed(3)}</td>
                <td>{(hop.confidence * 100).toFixed(0)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function AnswerTab({ stageTrace, citations, answer, totalMs, ddcClass }: {
  stageTrace: StageTrace | null;
  citations: string[];
  answer: string;
  totalMs: number;
  ddcClass: string;
}) {
  const searchMs = stageTrace?.search_ms ?? 0;
  const synthesisMs = stageTrace?.synthesis_ms ?? 0;
  const overheadMs = totalMs - searchMs - synthesisMs;

  return (
    <div className="dev-trace__tab-content">
      <div className="dev-trace__section">
        <h4 className="dev-trace__section-title">Synthesis</h4>
        <table className="dev-trace__table">
          <tbody>
            <tr><td>Score</td><td><span className={`score-badge score-badge--${ddcClass.toLowerCase()}`}>{ddcClass}</span></td></tr>
            <tr><td>Citations</td><td>{citations.length}</td></tr>
            <tr><td>Answer length</td><td>{answer.length} chars (~{Math.round(answer.length / 4)} tokens)</td></tr>
          </tbody>
        </table>
      </div>
      <div className="dev-trace__section">
        <h4 className="dev-trace__section-title">Latency Breakdown</h4>
        <div className="dev-trace__latency">
          <div className="dev-trace__latency-bar">
            {searchMs > 0 && (
              <div
                className="dev-trace__latency-segment dev-trace__latency-segment--search"
                style={{ width: `${(searchMs / totalMs) * 100}%` }}
                title={`Search: ${searchMs}ms`}
              />
            )}
            {synthesisMs > 0 && (
              <div
                className="dev-trace__latency-segment dev-trace__latency-segment--synthesis"
                style={{ width: `${(synthesisMs / totalMs) * 100}%` }}
                title={`Synthesis: ${synthesisMs}ms`}
              />
            )}
            {overheadMs > 0 && (
              <div
                className="dev-trace__latency-segment dev-trace__latency-segment--overhead"
                style={{ width: `${(overheadMs / totalMs) * 100}%` }}
                title={`Overhead: ${overheadMs}ms`}
              />
            )}
          </div>
          <div className="dev-trace__latency-legend">
            <span><span className="dev-trace__legend-dot dev-trace__legend-dot--search" /> Search {searchMs}ms</span>
            <span><span className="dev-trace__legend-dot dev-trace__legend-dot--synthesis" /> Synthesis {synthesisMs}ms</span>
            <span><span className="dev-trace__legend-dot dev-trace__legend-dot--overhead" /> Overhead {overheadMs > 0 ? overheadMs : 0}ms</span>
          </div>
          <div className="dev-trace__latency-total">
            Total: {(totalMs / 1000).toFixed(1)}s
          </div>
        </div>
      </div>
    </div>
  );
}

function GapsTab({ gaps }: { gaps: EvalGap[] }) {
  if (gaps.length === 0) {
    return (
      <div className="dev-trace__tab-content">
        <div className="dev-trace__empty">No gaps detected</div>
      </div>
    );
  }

  return (
    <div className="dev-trace__tab-content">
      <div className="dev-trace__section">
        <h4 className="dev-trace__section-title">Knowledge Gaps ({gaps.length})</h4>
        {gaps.map((gap, i) => (
          <div key={i} className={`dev-trace__gap-card dev-trace__gap-card--${gap.severity}`}>
            <div className="dev-trace__gap-header">
              <span className={`dev-trace__gap-severity dev-trace__gap-severity--${gap.severity}`}>
                {gap.severity}
              </span>
              <span className="dev-trace__gap-type">{gap.gap_type}</span>
            </div>
            <div className="dev-trace__gap-desc">{gap.description}</div>
            {gap.suggested_action && (
              <div className="dev-trace__gap-action">
                Suggested: {gap.suggested_action}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default function DevTracePanel({
  hops, gaps, stageTrace, citations, answer, totalMs, question, ddcClass, rawResult,
}: DevTracePanelProps) {
  const [expanded, setExpanded] = useState(false);
  const [activeTab, setActiveTab] = useState<TabKey>('intent');
  const [copied, setCopied] = useState(false);

  const copyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(rawResult, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadJson = () => {
    const blob = new Blob([JSON.stringify(rawResult, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const slug = question.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40);
    a.download = `trace-${slug}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const gapCount = gaps.length;

  return (
    <div className="dev-trace">
      <button
        className="dev-trace__toggle"
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
        <span className="dev-trace__toggle-label">Dev Trace</span>
        <span className="dev-trace__toggle-badge">7-stage pipeline</span>
      </button>

      {expanded && (
        <>
          <div className="dev-trace__tabs">
            {TABS.map(tab => (
              <button
                key={tab.key}
                className={`dev-trace__tab ${activeTab === tab.key ? 'dev-trace__tab--active' : ''}`}
                onClick={() => setActiveTab(tab.key)}
              >
                {tab.icon}
                <span>{tab.label}</span>
                {tab.key === 'gaps' && gapCount > 0 && (
                  <span className="dev-trace__tab-count">{gapCount}</span>
                )}
              </button>
            ))}
          </div>

          <div className="dev-trace__body">
            {activeTab === 'intent' && <IntentTab stageTrace={stageTrace} />}
            {activeTab === 'retrieval' && <RetrievalTab stageTrace={stageTrace} />}
            {activeTab === 'fusion' && <FusionTab hops={hops} />}
            {activeTab === 'context' && <ContextTab stageTrace={stageTrace} hops={hops} />}
            {activeTab === 'answer' && (
              <AnswerTab
                stageTrace={stageTrace}
                citations={citations}
                answer={answer}
                totalMs={totalMs}
                ddcClass={ddcClass}
              />
            )}
            {activeTab === 'gaps' && <GapsTab gaps={gaps} />}
          </div>

          <div className="dev-trace__footer">
            <button className="dev-trace__action" onClick={copyJson}>
              {copied ? <Check size={12} /> : <Copy size={12} />}
              {copied ? 'Copied' : 'Copy JSON'}
            </button>
            <button className="dev-trace__action" onClick={downloadJson}>
              <Download size={12} />
              Download JSON
            </button>
          </div>
        </>
      )}
    </div>
  );
}
