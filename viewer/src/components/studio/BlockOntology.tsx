import { useEffect, useState } from 'react';

import { studio } from '../../lib/studio-client';
import type { BlockOntology as BlockOntologyData, OntologyTypeInfo } from '../../lib/studio-types';

interface Props {
  block: string;
}

/** The block's ontology "schema blueprint": entity types grouped by layer,
 * plus the relationship-field allowlist. Full schema (all declared types),
 * independent of which entities currently exist. */
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

  const typesByLayer: Record<string, OntologyTypeInfo[]> = {};
  for (const t of data.types) {
    (typesByLayer[t.layer] ||= []).push(t);
  }

  return (
    <div className="studio-ontology">
      <div className="studio-path">{data.source}</div>

      <div className="studio-schema">
        {data.layers.map((layer) => (
          <div key={layer.key} className="studio-schema__layer" style={{ borderTopColor: layer.color }}>
            <div className="studio-schema__layer-head" style={{ color: layer.color }}>
              {layer.label}
            </div>
            <div>
              {(typesByLayer[layer.key] ?? []).map((t) => (
                <span key={t.key} className="studio-chip" title={t.key}>
                  {t.label}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="studio-section">
        <div className="studio-section__title">
          Relationship fields ({data.relationship_fields.length})
        </div>
        <div>
          {data.relationship_fields.map((r) => (
            <span key={r} className="studio-chip">
              {r}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
