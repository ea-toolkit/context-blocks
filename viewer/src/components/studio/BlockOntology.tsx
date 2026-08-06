import { useEffect, useState } from 'react';

import { studio } from '../../lib/studio-client';
import type { BlockOntology as BlockOntologyData } from '../../lib/studio-types';
import OntologySchema from '../ontology/OntologySchema';

interface Props {
  block: string;
}

/** Live per-block ontology view — fetches /blocks/{name}/ontology and renders
 * the shared OntologySchema. */
export default function BlockOntology({ block }: Props) {
  const [data, setData] = useState<BlockOntologyData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);
    studio.getOntology(block).then((res) => {
      if (!active) return;
      if (res.ok && res.body) setData(res.body);
      else setError('Could not load the ontology.');
      setLoading(false);
    });
    return () => {
      active = false;
    };
  }, [block]);

  if (loading) return <p className="studio-empty">Loading ontology…</p>;
  if (error) return <p className="studio-empty">{error}</p>;
  if (!data) return null;

  return (
    <OntologySchema
      source={data.source}
      layers={data.layers}
      types={data.types}
      relationshipFields={data.relationship_fields}
    />
  );
}
