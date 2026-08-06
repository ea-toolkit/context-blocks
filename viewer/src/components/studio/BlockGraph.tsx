import { useEffect, useState } from 'react';

import { studio } from '../../lib/studio-client';
import type { BlockGraph as BlockGraphData } from '../../lib/studio-types';
import DomainMap from '../map/DomainMap';

interface Props {
  block: string;
}

/** Live per-block knowledge graph — fetches the graph endpoint and feeds the
 * shared DomainMap (React Flow + Organic/Hubs/Tree layouts + search). */
export default function BlockGraph({ block }: Props) {
  const [data, setData] = useState<BlockGraphData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);
    studio.getGraph(block).then((res) => {
      if (!active) return;
      if (res.ok && res.body) setData(res.body);
      else setError('Could not load the graph.');
      setLoading(false);
    });
    return () => {
      active = false;
    };
  }, [block]);

  if (loading) return <p className="studio-empty">Loading graph…</p>;
  if (error) return <p className="studio-empty">{error}</p>;
  if (!data || data.nodes.length === 0) {
    return <p className="studio-empty">No entities to graph yet — add some entities first.</p>;
  }

  // Map the API DTOs (snake_case) to DomainMap's props (camelCase).
  const entities = data.nodes.map((n) => ({
    id: n.id,
    name: n.name,
    type: n.type,
    typeLabel: n.type_label,
    typeIcon: n.type_icon,
    layer: n.layer,
    layerColor: n.layer_color,
    confidence: n.confidence,
    description: n.description,
    relationshipCount: n.relationship_count,
    incomingCount: n.incoming_count,
    outgoingCount: n.outgoing_count,
  }));
  const edges = data.edges.map((e) => ({ source: e.source, target: e.target, type: e.type }));
  const layers = data.layers.map((l) => ({ key: l.key, label: l.label, color: l.color }));
  const entityTypes = data.entity_types.map((t) => ({ key: t.key, label: t.label, layer: t.layer }));

  return (
    <div className="studio-graph">
      <DomainMap entities={entities} edges={edges} layers={layers} entityTypes={entityTypes} />
    </div>
  );
}
