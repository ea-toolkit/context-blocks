import { useEffect, useState } from 'react';

import { useActiveBlock } from '../../lib/active-block';
import { blockGraphToDomainMapProps } from '../../lib/graph-map';
import { studio } from '../../lib/studio-client';
import DomainMap, { type DomainMapProps } from './DomainMap';

/** The Map view: renders baked build-time data by default, or the active block
 * LIVE from the Studio API when `?block=<name>` is set. */
export default function MapView(baked: DomainMapProps) {
  const block = useActiveBlock();
  const [live, setLive] = useState<DomainMapProps | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!block) {
      setLive(null);
      return;
    }
    let active = true;
    setLoading(true);
    studio.getGraph(block).then((res) => {
      if (!active) return;
      setLive(res.ok && res.body ? blockGraphToDomainMapProps(res.body) : null);
      setLoading(false);
    });
    return () => {
      active = false;
    };
  }, [block]);

  if (block && loading) {
    return <div className="map__loading">Loading “{block}” live…</div>;
  }
  return <DomainMap {...(live ?? baked)} />;
}
