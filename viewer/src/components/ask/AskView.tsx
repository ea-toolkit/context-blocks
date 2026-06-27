import { useState, useMemo, useCallback, useEffect, useRef } from 'react';
import {
  Send, ArrowLeft, Loader2,
  AlertTriangle, CheckCircle, XCircle, WifiOff, RefreshCw, Code2,
} from 'lucide-react';
import { marked } from 'marked';
import type { EvalResult } from '../../lib/types';
import WhyThisAnswer from './WhyThisAnswer';
import DevTracePanel from './DevTracePanel';

const API_BASE = import.meta.env.PUBLIC_CB_API_BASE || 'http://localhost:8321';
const HEALTH_POLL_INTERVAL = 10_000;
const RECENT_KEY = 'cb-recent-questions';
const RECENT_RESULTS_KEY = 'cb-recent-results';
const RECENT_MAX = 5;

function saveRecentQuestion(question: string, ddcClass: string, result: EvalResult) {
  try {
    // Save to recent list
    const items = JSON.parse(localStorage.getItem(RECENT_KEY) || '[]');
    const filtered = items.filter((i: { question: string }) => i.question !== question);
    filtered.unshift({ question, ddcClass, timestamp: Date.now() });
    localStorage.setItem(RECENT_KEY, JSON.stringify(filtered.slice(0, RECENT_MAX)));

    // Save full result keyed by question
    const results = JSON.parse(localStorage.getItem(RECENT_RESULTS_KEY) || '{}');
    results[question] = result;
    // Prune old results not in the recent list
    const recentQs = new Set(filtered.slice(0, RECENT_MAX).map((i: { question: string }) => i.question));
    for (const key of Object.keys(results)) {
      if (!recentQs.has(key)) delete results[key];
    }
    localStorage.setItem(RECENT_RESULTS_KEY, JSON.stringify(results));

    renderRecentSidebar(filtered.slice(0, RECENT_MAX));
  } catch (_) {}
}

function loadCachedResult(question: string): EvalResult | null {
  try {
    const results = JSON.parse(localStorage.getItem(RECENT_RESULTS_KEY) || '{}');
    return results[question] || null;
  } catch (_) {
    return null;
  }
}

function renderRecentSidebar(items: { question: string; ddcClass: string }[]) {
  const el = document.getElementById('recent-questions');
  if (!el) return;
  el.innerHTML = items.map(item => {
    const q = item.question || '';
    const short = q.length > 45 ? q.slice(0, 45) + '...' : q;
    const cls = (item.ddcClass || '').toLowerCase();
    const dot = cls === 'clean' ? '#22c55e' : cls === 'incomplete' ? '#eab308' : cls === 'missing' ? '#ef4444' : '#475569';
    return `<a href="/?q=${encodeURIComponent(q)}" class="app-sidebar-nav__recent-item" title="${q.replace(/"/g, '&quot;')}"><span style="width:6px;height:6px;border-radius:50%;background:${dot};flex-shrink:0"></span><span>${short.replace(/</g, '&lt;')}</span></a>`;
  }).join('');
}

interface AskViewProps {
  results: EvalResult[];
}

function renderMarkdownAnswer(answer: string): string {
  marked.setOptions({ breaks: true, gfm: true });
  return marked.parse(answer) as string;
}

function AnswerBody({ answer }: { answer: string }) {
  const html = useMemo(() => renderMarkdownAnswer(answer), [answer]);
  return (
    <div
      className="cb-markdown"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

function AnswerView({
  result,
  onBack,
  onAskFollowUp,
  serverOnline,
  devMode,
  onToggleDev,
}: {
  result: EvalResult;
  onBack: () => void;
  onAskFollowUp: (q: string) => void;
  serverOnline: boolean | null;
  devMode: boolean;
  onToggleDev: () => void;
}) {
  const [followUp, setFollowUp] = useState('');
  const isOnline = serverOnline === true;
  const isError = result.source === 'error';

  const handleFollowUp = () => {
    if (followUp.trim() && isOnline) {
      onAskFollowUp(followUp.trim());
      setFollowUp('');
    }
  };

  const rawResult = useMemo(() => ({
    question: result.question,
    score: result.score,
    ddc_class: result.ddc_class,
    citations: result.citations,
    entities_retrieved: result.entities_retrieved,
    total_ms: result.total_ms,
    hops: result.hops,
    gaps: result.gaps,
    stage_trace: result.stage_trace,
  }), [result]);

  return (
    <div className="ask-answer">
      <div className="ask-answer__header">
        <button onClick={onBack} className="ask-answer__back">
          <ArrowLeft size={14} /> Back
        </button>
        <button
          onClick={onToggleDev}
          className={`ask-answer__dev-toggle ${devMode ? 'ask-answer__dev-toggle--active' : ''}`}
          title={devMode ? 'Hide dev trace' : 'Show dev trace'}
        >
          <Code2 size={14} />
          <span>Dev</span>
        </button>
      </div>

      <div className="ask-answer__content">
        <h2 className="ask-answer__question">{result.question}</h2>

        <div className="ask-answer__meta">
          {!isError && (
            <span className="ask-answer__meta-item">
              {result.entities_retrieved} entities · {(result.total_ms / 1000).toFixed(1)}s
            </span>
          )}
          {result.source !== 'live' && !isError && result.persona && (
            <span className="source-badge source-badge--persona">{result.persona}</span>
          )}
        </div>

        <AnswerBody answer={result.answer} />

        {!isError && result.hops.length > 0 && (
          <WhyThisAnswer
            hops={result.hops}
            gaps={result.gaps}
            ddcClass={result.ddc_class}
            citations={result.citations}
          />
        )}

        {devMode && !isError && (
          <DevTracePanel
            hops={result.hops}
            gaps={result.gaps}
            stageTrace={result.stage_trace ?? null}
            citations={result.citations}
            answer={result.answer}
            totalMs={result.total_ms}
            question={result.question}
            ddcClass={result.ddc_class}
            rawResult={rawResult}
          />
        )}

        <div className="ask-answer__followup">
          <div className="ask-answer__followup-box" style={{ opacity: isOnline ? 1 : 0.6 }}>
            <input
              type="text"
              placeholder={isOnline ? 'Ask a follow-up question...' : 'Server offline'}
              value={followUp}
              onChange={e => setFollowUp(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') handleFollowUp(); }}
              disabled={!isOnline}
              className="ask-answer__followup-input"
            />
            <button
              onClick={handleFollowUp}
              disabled={!isOnline || !followUp.trim()}
              className={`ask-answer__followup-btn ${isOnline && followUp.trim() ? 'ask-answer__followup-btn--active' : ''}`}
            >
              <Send size={14} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function AskView({ results }: AskViewProps) {
  const [selectedResult, setSelectedResult] = useState<EvalResult | null>(null);
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [serverOnline, setServerOnline] = useState<boolean | null>(null);
  const [devMode, setDevMode] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('dev') === 'true') setDevMode(true);
    const pendingQ = params.get('q');
    if (pendingQ) {
      const cached = loadCachedResult(pendingQ);
      if (cached) {
        setSelectedResult(cached);
      } else {
        setQuery(pendingQ);
      }
      window.history.replaceState({}, '', params.get('dev') === 'true' ? '/?dev=true' : '/');
    }
  }, []);

  useEffect(() => {
    const check = () => {
      fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) })
        .then(r => r.ok ? setServerOnline(true) : setServerOnline(false))
        .catch(() => setServerOnline(false));
    };
    check();
    const interval = setInterval(check, HEALTH_POLL_INTERVAL);
    return () => clearInterval(interval);
  }, []);

  const askQuestion = useCallback(async (question: string) => {
    if (!question.trim() || !serverOnline) return;
    setIsLoading(true);

    try {
      const res = await fetch(`${API_BASE}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, full_trace: devMode }),
      });

      if (!res.ok) {
        const errorText = await res.text().catch(() => 'Unknown error');
        throw new Error(`Server returned ${res.status}: ${errorText}`);
      }

      const data = await res.json();

      const liveResult: EvalResult = {
        question,
        source: 'live',
        source_file: '',
        layer_hint: '',
        topic: '',
        persona: '',
        score: data.score,
        ddc_class: data.ddc_class,
        answer: data.answer,
        citations: data.citations ?? [],
        entities_retrieved: data.entities_retrieved ?? 0,
        total_ms: data.total_ms ?? 0,
        trace_summary: '',
        hops: data.hops ?? [],
        gaps: data.gaps ?? [],
        stage_trace: data.stage_trace ?? null,
      };
      setSelectedResult(liveResult);
      saveRecentQuestion(question, data.ddc_class ?? 'MISSING', liveResult);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setSelectedResult({
        question,
        source: 'error',
        source_file: '',
        layer_hint: '',
        topic: '',
        persona: '',
        score: 'not_answerable',
        ddc_class: 'MISSING',
        answer: `**Connection failed.** ${message}\n\nCheck that \`cb serve\` is running at ${API_BASE}.`,
        citations: [],
        entities_retrieved: 0,
        total_ms: 0,
        trace_summary: '',
        hops: [],
        gaps: [],
      });
    } finally {
      setIsLoading(false);
    }
  }, [serverOnline, devMode]);

  const handleSubmit = useCallback(() => {
    if (query.trim() && serverOnline) {
      askQuestion(query);
    }
  }, [query, serverOnline, askQuestion]);

  if (selectedResult) {
    return (
      <AnswerView
        result={selectedResult}
        onBack={() => { setSelectedResult(null); setQuery(''); }}
        onAskFollowUp={(q) => { askQuestion(q); }}
        serverOnline={serverOnline}
        devMode={devMode}
        onToggleDev={() => setDevMode(d => !d)}
      />
    );
  }

  if (isLoading) {
    return (
      <div className="ask-loading">
        <Loader2 size={32} className="animate-spin" style={{ color: 'var(--cb-primary)' }} />
        <p>Searching knowledge base...</p>
      </div>
    );
  }

  const isOnline = serverOnline === true;
  const isChecking = serverOnline === null;

  return (
    <div className="ask-landing">
      <div className="ask-landing__hero">
        <h1 className="ask-landing__title">Ask your domain anything</h1>
        <p className="ask-landing__subtitle">
          Grounded answers from your knowledge base — with full retrieval traces.
        </p>
      </div>

      <div className="ask-landing__input-box" style={{ opacity: isOnline ? 1 : 0.85 }}>
        <div className="ask-landing__input-row">
          <textarea
            ref={textareaRef}
            placeholder={isOnline ? 'Ask your domain anything...' : 'Server offline — start cb serve to ask questions'}
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit();
              }
            }}
            disabled={!isOnline}
            className="ask-landing__textarea"
            rows={2}
          />
          <button
            onClick={handleSubmit}
            disabled={!isOnline || !query.trim()}
            className={`ask-landing__send ${isOnline && query.trim() ? 'ask-landing__send--active' : ''}`}
          >
            <Send size={18} />
          </button>
        </div>

        <div className="ask-landing__status">
          {isChecking ? (
            <>
              <RefreshCw size={10} className="animate-spin" />
              <span>Connecting...</span>
            </>
          ) : isOnline ? (
            <>
              <span className="ask-landing__status-dot" />
              <span>Connected</span>
            </>
          ) : (
            <>
              <WifiOff size={12} style={{ color: 'var(--cb-score-incomplete)' }} />
              <span style={{ color: 'var(--cb-score-incomplete)' }}>Server offline</span>
            </>
          )}
        </div>
      </div>

      {serverOnline === false && (
        <div className="ask-landing__offline">
          <WifiOff size={18} style={{ color: 'var(--cb-score-incomplete)', flexShrink: 0, marginTop: 2 }} />
          <div>
            <div className="ask-landing__offline-title">Start the Context Blocks server</div>
            <div className="ask-landing__offline-desc">
              The Q&A server needs to be running to answer questions. Start it with:
            </div>
            <code className="ask-landing__offline-code">
              cb serve --output &lt;your-output-dir&gt;
            </code>
            <div className="ask-landing__offline-hint">
              This page auto-detects when the server comes online.
            </div>
          </div>
        </div>
      )}

      {!query && results.length > 0 && (
        <div className="ask-landing__examples">
          <div className="ask-landing__examples-label">Example questions</div>
          <div className="ask-landing__examples-list">
            {results.slice(0, 6).map((r, i) => (
              <button
                key={i}
                onClick={() => {
                  if (isOnline) {
                    askQuestion(r.question);
                  } else {
                    setSelectedResult(r);
                  }
                }}
                className="ask-landing__example-pill"
              >
                {r.question.length > 60 ? r.question.slice(0, 60) + '...' : r.question}
              </button>
            ))}
          </div>
          {!isOnline && results.length > 0 && (
            <div className="ask-landing__examples-hint">
              Click to view pre-computed answers from the last evaluation run.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
