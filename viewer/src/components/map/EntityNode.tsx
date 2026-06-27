/**
 * EntityNode — custom ReactFlow node for a CBEntity.
 *
 * Design:
 * - Rectangle 180×60px
 * - Background: layerColor at 15% opacity
 * - Border: layerColor, solid for high confidence, dashed for low
 * - Top handle (target), bottom handle (source)
 * - Name truncated, type icon badge bottom-right
 */
import React from 'react';
import { Handle, Position, type NodeProps } from '@xyflow/react';
import { getConfidenceTier } from '../../lib/types';

export interface EntityNodeData {
  id: string;
  name: string;
  type: string;
  typeLabel: string;
  typeIcon: string;
  layer: string;
  layerColor: string;
  confidence: number;
  description: string;
}

const NODE_WIDTH = 180;
const NODE_HEIGHT = 60;

export default function EntityNode({ data, selected }: NodeProps) {
  const d = data as unknown as EntityNodeData;
  const tier = getConfidenceTier(d.confidence);
  const borderStyle = tier === 'sketched' ? 'dashed' : 'solid';
  const layerColor = d.layerColor ?? '#666';

  const bgColor = hexToRgba(layerColor, 0.15);
  const borderColor = hexToRgba(layerColor, tier === 'solid' ? 1 : tier === 'muted' ? 0.65 : 0.4);
  const selectedRing = selected ? `0 0 0 2px ${layerColor}` : 'none';

  return (
    <div
      style={{
        width: NODE_WIDTH,
        height: NODE_HEIGHT,
        background: bgColor,
        border: `2px ${borderStyle} ${borderColor}`,
        borderRadius: 4,
        boxShadow: selectedRing,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        padding: '0 10px',
        position: 'relative',
        cursor: 'pointer',
        fontFamily: 'var(--cb-font-body, Inter, system-ui, sans-serif)',
        transition: 'box-shadow 0.15s',
        overflow: 'hidden',
      }}
      title={d.description || d.name}
    >
      <Handle
        type="target"
        position={Position.Top}
        style={{
          background: borderColor,
          width: 8,
          height: 8,
          border: `2px solid var(--cb-bg, #0f1117)`,
        }}
      />
      <Handle
        type="source"
        position={Position.Bottom}
        style={{
          background: borderColor,
          width: 8,
          height: 8,
          border: `2px solid var(--cb-bg, #0f1117)`,
        }}
      />

      {/* Name */}
      <div
        style={{
          fontSize: 12,
          fontWeight: 600,
          color: 'var(--cb-text, #e2e8f0)',
          lineHeight: 1.3,
          whiteSpace: 'nowrap',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          paddingRight: 24,
        }}
      >
        {d.name}
      </div>

      {/* Type label */}
      <div
        style={{
          fontSize: 10,
          color: hexToRgba(layerColor, 0.85),
          marginTop: 2,
          whiteSpace: 'nowrap',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          paddingRight: 24,
        }}
      >
        {d.typeLabel}
      </div>

      {/* Type icon badge — bottom right */}
      <div
        style={{
          position: 'absolute',
          right: 6,
          bottom: 6,
          fontSize: 9,
          fontWeight: 700,
          background: hexToRgba(layerColor, 0.2),
          color: hexToRgba(layerColor, 0.9),
          padding: '1px 4px',
          borderRadius: 2,
          lineHeight: 1.4,
          letterSpacing: '0.02em',
        }}
      >
        {d.typeIcon}
      </div>
    </div>
  );
}

/** Convert hex color to rgba string. Falls back to the original color if not parseable. */
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
