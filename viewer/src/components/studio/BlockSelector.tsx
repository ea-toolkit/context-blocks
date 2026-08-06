import { useEffect, useState } from 'react';

import { blockHref, useActiveBlock } from '../../lib/active-block';
import { studio } from '../../lib/studio-client';
import type { BlockSummary } from '../../lib/studio-types';

/** Sidebar selector for the active LIVE block. Lists blocks from the Studio API;
 * choosing one sets `?block=` so Map/Ontology render it live. "Built data" clears
 * back to the baked build-time view. Hidden when the Studio API has no blocks. */
export default function BlockSelector() {
  const active = useActiveBlock();
  const [blocks, setBlocks] = useState<BlockSummary[]>([]);

  useEffect(() => {
    studio.listBlocks().then((r) => setBlocks(r.ok && r.body ? r.body : []));
  }, []);

  if (blocks.length === 0) return null;

  return (
    <select
      className="app-block-selector"
      value={active ?? ''}
      onChange={(e) => {
        window.location.href = blockHref(window.location.pathname, e.target.value);
      }}
      aria-label="Active block (live)"
    >
      <option value="">Built data</option>
      {blocks.map((b) => (
        <option key={b.name} value={b.name}>
          {b.label || b.name} · live
        </option>
      ))}
    </select>
  );
}
