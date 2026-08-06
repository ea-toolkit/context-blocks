/** Renders an ontology "schema blueprint": entity types grouped by layer
 * (layer-colored cards) + the relationship-field allowlist. Pure render — fed by
 * either baked meta-model data (the Ontology page) or the live API (the Studio). */

export interface SchemaLayer {
  key: string;
  label: string;
  color: string;
}

export interface SchemaType {
  key: string;
  label: string;
  layer: string;
}

interface Props {
  source?: string;
  layers: SchemaLayer[];
  types: SchemaType[];
  relationshipFields: string[];
}

export default function OntologySchema({ source, layers, types, relationshipFields }: Props) {
  const typesByLayer: Record<string, SchemaType[]> = {};
  for (const t of types) {
    (typesByLayer[t.layer] ||= []).push(t);
  }

  return (
    <div className="studio-ontology">
      {source && <div className="studio-path">{source}</div>}

      <div className="studio-schema">
        {layers.map((layer) => (
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
        <div className="studio-section__title">Relationship fields ({relationshipFields.length})</div>
        <div>
          {relationshipFields.map((r) => (
            <span key={r} className="studio-chip">
              {r}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
