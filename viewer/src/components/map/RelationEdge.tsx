/**
 * RelationEdge — custom ReactFlow edge for entity relationships.
 *
 * - Bezier curve
 * - Color: source node's layerColor at 50% opacity
 * - Label: relationship type (small, muted)
 */
import React from 'react';
import {
  BaseEdge,
  EdgeLabelRenderer,
  getBezierPath,
  type EdgeProps,
} from '@xyflow/react';

export interface RelationEdgeData {
  type: string;
  sourceLayerColor: string;
  showLabel?: boolean;
}

export default function RelationEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
  selected,
}: EdgeProps) {
  const d = data as unknown as RelationEdgeData | undefined;
  const layerColor = d?.sourceLayerColor ?? '#666';
  const relType = d?.type ?? '';
  const showLabel = d?.showLabel ?? false;

  // Build bezier path
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  const strokeColor = hexToRgba(layerColor, selected ? 0.9 : 0.5);
  const strokeWidth = selected ? 2 : 1.5;

  return (
    <>
      <BaseEdge
        id={id}
        path={edgePath}
        style={{
          stroke: strokeColor,
          strokeWidth,
        }}
        markerEnd="url(#cb-arrowhead)"
      />
      {relType && showLabel && (
        <EdgeLabelRenderer>
          <div
            style={{
              position: 'absolute',
              transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
              background: 'var(--cb-surface, #161922)',
              border: '1px solid var(--cb-border, rgba(255,255,255,0.08))',
              padding: '2px 6px',
              borderRadius: 3,
              fontSize: 10,
              fontWeight: 500,
              color: 'var(--cb-text-faint, #475569)',
              pointerEvents: 'none',
              whiteSpace: 'nowrap',
              maxWidth: 120,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              lineHeight: 1.4,
            }}
          >
            {relType.replace(/_/g, ' ')}
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
}

/** SVG marker defs — rendered once in the ReactFlow wrapper */
export function CBEdgeMarkerDefs() {
  return (
    <svg style={{ position: 'absolute', width: 0, height: 0 }}>
      <defs>
        <marker
          id="cb-arrowhead"
          markerWidth="10"
          markerHeight="10"
          refX="9"
          refY="5"
          orient="auto"
        >
          <path d="M1,1 L9,5 L1,9 L3,5 Z" fill="var(--cb-text-faint, #475569)" />
        </marker>
      </defs>
    </svg>
  );
}

function hexToRgba(hex: string, alpha: number): string {
  try {
    const clean = hex.replace('#', '');
    const full = clean.length === 3
      ? clean.split('').map(c => c + c).join('')
      : clean;
    const r = parseInt(full.slice(0, 2), 16);
    const g = parseInt(full.slice(2, 4), 16);
    const b = parseInt(full.slice(4, 6), 16);
    if (isNaN(r) || isNaN(g) || isNaN(b)) return hex;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  } catch {
    return hex;
  }
}
