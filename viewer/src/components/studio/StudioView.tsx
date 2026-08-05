import { useCallback, useEffect, useState } from 'react';

import { STUDIO_API_BASE, studio } from '../../lib/studio-client';
import type { BlockSummary } from '../../lib/studio-types';
import CreateBlockForm from './CreateBlockForm';

type Mode = { kind: 'list' } | { kind: 'create' };

/** Top-level Studio authoring surface: list blocks + create a new one. */
export default function StudioView() {
  const [blocks, setBlocks] = useState<BlockSummary[]>([]);
  const [online, setOnline] = useState<boolean | null>(null);
  const [mode, setMode] = useState<Mode>({ kind: 'list' });

  const refresh = useCallback(async () => {
    const res = await studio.listBlocks();
    if (res.ok && res.body) {
      setBlocks(res.body);
      setOnline(true);
    } else {
      setOnline(false);
    }
  }, []);

  useEffect(() => {
    studio
      .health()
      .then((r) => setOnline(r.ok))
      .catch(() => setOnline(false));
    void refresh();
  }, [refresh]);

  const isOnline = online === true;

  return (
    <div className="studio">
      <div className="studio__header">
        <div>
          <div className="studio__title">Blocks</div>
          <div className="studio__subtitle">Create and author context blocks.</div>
        </div>
        <div className={`studio-status ${isOnline ? '' : 'studio-status--offline'}`}>
          <span className="studio-status__dot" />
          <span>{online === null ? 'Connecting…' : isOnline ? 'Studio API online' : 'Studio API offline'}</span>
        </div>
      </div>

      {online === false && (
        <div className="studio-offline">
          The Studio API is not reachable at <code>{STUDIO_API_BASE}</code>. Start it with:{' '}
          <code>uvicorn context_blocks.studio_api:create_studio_app --factory --port 8322</code>
        </div>
      )}

      {mode.kind === 'create' ? (
        <CreateBlockForm
          onCreated={() => {
            setMode({ kind: 'list' });
            void refresh();
          }}
          onCancel={() => setMode({ kind: 'list' })}
        />
      ) : (
        <>
          <div className="studio-toolbar">
            <button
              className="studio-btn studio-btn--primary"
              disabled={!isOnline}
              onClick={() => setMode({ kind: 'create' })}
            >
              ＋ Create Block
            </button>
          </div>

          {blocks.length === 0 ? (
            <p className="studio-empty">{isOnline ? 'No blocks yet. Create one to get started.' : ''}</p>
          ) : (
            <div className="studio-blocks">
              {blocks.map((b) => (
                <button
                  key={b.name}
                  className="studio-block-card"
                  onClick={() => {
                    /* branch 3: open block detail */
                  }}
                >
                  <div className="studio-block-card__label">{b.label || b.name}</div>
                  <div className="studio-block-card__meta">
                    {b.name} · {b.entity_count} entities
                  </div>
                </button>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
