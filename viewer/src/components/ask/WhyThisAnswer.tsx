import { CheckCircle, AlertTriangle, XCircle, ExternalLink } from 'lucide-react';
import type { EvalHop, EvalGap } from '../../lib/types';

interface WhyThisAnswerProps {
  hops: EvalHop[];
  gaps: EvalGap[];
  ddcClass: string;
  citations: string[];
}

const LAYER_COLORS: Record<string, string> = {
  structural: '#4A90E2',
  behavioral: '#1ABC9C',
  reference: '#0891B2',
  organizational: '#9B59B6',
  language: '#F39C12',
  decision: '#B45309',
};

function ScoreIcon({ ddcClass }: { ddcClass: string }) {
  switch (ddcClass) {
    case 'CLEAN': return <CheckCircle size={14} />;
    case 'INCOMPLETE': return <AlertTriangle size={14} />;
    default: return <XCircle size={14} />;
  }
}

function confidenceLine(hops: EvalHop[], gaps: EvalGap[], citations: string[]): string {
  if (gaps.length === 0) {
    return `High confidence — ${hops.length} entities, ${citations.length} citations`;
  }
  const highGaps = gaps.filter(g => g.severity === 'high').length;
  if (highGaps > 0) {
    return `Partial — ${highGaps} critical knowledge gap${highGaps > 1 ? 's' : ''} detected`;
  }
  return `Partial — ${gaps.length} knowledge gap${gaps.length > 1 ? 's' : ''} detected`;
}

export default function WhyThisAnswer({ hops, gaps, ddcClass, citations }: WhyThisAnswerProps) {
  const topEntities = [...hops]
    .sort((a, b) => b.fused_score - a.fused_score)
    .slice(0, 5);

  return (
    <div className="why-answer">
      <div className="why-answer__title">Why this answer</div>
      <div className="why-answer__header">
        <span className={`score-badge score-badge--${ddcClass.toLowerCase()}`}>
          <ScoreIcon ddcClass={ddcClass} /> {ddcClass}
        </span>
        <span className="why-answer__confidence">
          {confidenceLine(hops, gaps, citations)}
        </span>
      </div>

      {topEntities.length > 0 && (
        <div className="why-answer__entities">
          <span className="why-answer__label">Grounded in</span>
          <div className="why-answer__pills">
            {topEntities.map(hop => (
              <a
                key={hop.entity_id}
                href={`/explorer?entity=${hop.entity_id}`}
                className="why-answer__pill"
                title={`${hop.entity_name} (${hop.entity_type}) — relevance ${hop.fused_score.toFixed(2)}`}
              >
                <span
                  className="why-answer__pill-dot"
                  style={{ background: LAYER_COLORS[hop.layer] || 'var(--cb-text-faint)' }}
                />
                {hop.entity_name}
                <ExternalLink size={10} className="why-answer__pill-link" />
              </a>
            ))}
          </div>
        </div>
      )}

      {gaps.length > 0 && (
        <div className="why-answer__gaps">
          {gaps.slice(0, 3).map((gap, i) => (
            <div key={i} className="why-answer__gap">
              <AlertTriangle size={12} />
              <span>{gap.description}</span>
            </div>
          ))}
          {gaps.length > 3 && (
            <span className="why-answer__gap-more">
              +{gaps.length - 3} more gap{gaps.length - 3 > 1 ? 's' : ''}
            </span>
          )}
        </div>
      )}
    </div>
  );
}
