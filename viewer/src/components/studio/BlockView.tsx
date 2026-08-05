import { useCallback, useEffect, useState } from 'react';

import { detailMessage, studio } from '../../lib/studio-client';
import type { BlockDetail, EntityListItem } from '../../lib/studio-types';
import AddEntityForm from './AddEntityForm';
import ArtifactsSection from './ArtifactsSection';

interface Props {
  name: string;
  onBack: () => void;
}

/** Block detail: ontology (types/layers) + the block's entity list. */
export default function BlockView({ name, onBack }: Props) {
  const [block, setBlock] = useState<BlockDetail | null>(null);
  const [entities, setEntities] = useState<EntityListItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    const detail = await studio.getBlock(name);
    if (!detail.ok || !detail.body) {
      setError(detailMessage(detail.body));
      setLoading(false);
      return;
    }
    setBlock(detail.body);
    const ents = await studio.listEntities(name);
    setEntities(ents.ok && ents.body ? ents.body : []);
    setLoading(false);
  }, [name]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <div>
      <div className="studio-toolbar" style={{ justifyContent: 'flex-start' }}>
        <button className="studio-btn" onClick={onBack}>
          ← Back to blocks
        </button>
      </div>

      {loading && <p className="studio-empty">Loading…</p>}
      {error && (
        <ul className="studio-errors">
          <li>{error}</li>
        </ul>
      )}

      {block && (
        <>
          <div className="studio__header">
            <div>
              <div className="studio__title">{block.label || block.name}</div>
              {block.description && <div className="studio__subtitle">{block.description}</div>}
            </div>
          </div>

          <div className="studio-section">
            <div className="studio-section__title">Ontology</div>
            <div className="studio-path">{block.ontology}</div>
            <div>
              {block.ontology_detail.types.map((t) => (
                <span key={t} className="studio-chip">
                  {t}
                </span>
              ))}
            </div>
            <div>
              {block.ontology_detail.layers.map((l) => (
                <span key={l} className="studio-chip studio-chip--layer">
                  {l}
                </span>
              ))}
            </div>
          </div>

          <div className="studio-section">
            <div className="studio-entities-head">
              <div className="studio-section__title">Entities ({entities.length})</div>
              {!adding && (
                <button className="studio-btn studio-btn--primary" onClick={() => setAdding(true)}>
                  ＋ Add Entity
                </button>
              )}
            </div>

            {adding && (
              <AddEntityForm
                blockName={name}
                onAdded={() => {
                  setAdding(false);
                  void load();
                }}
                onCancel={() => setAdding(false)}
              />
            )}

            {entities.length === 0 ? (
              <p className="studio-empty">No entities yet.</p>
            ) : (
              <table className="studio-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Name</th>
                    <th>Path</th>
                  </tr>
                </thead>
                <tbody>
                  {entities.map((e) => (
                    <tr key={e.path}>
                      <td>{e.id}</td>
                      <td>{e.type}</td>
                      <td>{e.name}</td>
                      <td className="studio-path">{e.path}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          <ArtifactsSection block={name} />
        </>
      )}
    </div>
  );
}
