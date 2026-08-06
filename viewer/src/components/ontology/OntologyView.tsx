import { useEffect, useMemo, useState } from 'react';

import { useActiveBlock } from '../../lib/active-block';
import { blockGraphToDomainMapProps } from '../../lib/graph-map';
import { studio } from '../../lib/studio-client';
import { induceTypeGraph } from '../../lib/type-graph';
import DomainMap, { type DomainMapProps } from '../map/DomainMap';

/** Ontology view = the type-level schema graph (entity types as nodes,
 * relationships between types as edges). Baked build-time data by default, or the
 * active block LIVE when `?block=<name>` is set. Reuses DomainMap. */
export default function OntologyView(baked: DomainMapProps) {
  const block = useActiveBlock();
  const [source, setSource] = useState<DomainMapProps>(baked);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!block) {
      setSource(baked);
      return;
    }
    let active = true;
    setLoading(true);
    studio.getGraph(block).then((res) => {
      if (!active) return;
      setSource(res.ok && res.body ? blockGraphToDomainMapProps(res.body) : baked);
      setLoading(false);
    });
    return () => {
      active = false;
    };
  }, [block]);

  const typeGraph = useMemo(() => induceTypeGraph(source), [source]);

  if (block && loading) {
    return <div className="map__loading">Loading “{block}” live…</div>;
  }
  return <DomainMap {...typeGraph} />;
}
