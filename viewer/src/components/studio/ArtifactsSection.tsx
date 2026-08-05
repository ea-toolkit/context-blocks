import { useCallback, useEffect, useRef, useState, type ChangeEvent } from 'react';

import { studio } from '../../lib/studio-client';
import type { ArtifactInfo } from '../../lib/studio-types';
import ArtifactViewer from './ArtifactViewer';

interface Props {
  block: string;
}

// UX hint for the file picker; the server (storage.ARTIFACT_EXTENSIONS) is the
// real allowlist and returns 415 on anything else.
const ACCEPT = '.bpmn,.drawio,.uml,.puml,.xml,.svg,.png,.jpg,.jpeg,.gif,.webp';

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

/** A block's non-md artifacts: list, upload, and preview. */
export default function ArtifactsSection({ block }: Props) {
  const [artifacts, setArtifacts] = useState<ArtifactInfo[]>([]);
  const [selected, setSelected] = useState<ArtifactInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const load = useCallback(async () => {
    const res = await studio.listArtifacts(block);
    setArtifacts(res.ok && res.body ? res.body : []);
  }, [block]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onFile(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setError(null);
    const res = await studio.uploadArtifact(block, file);
    if (res.ok) {
      await load();
    } else if (res.status === 415) {
      setError(`Unsupported file type: ${file.name}`);
    } else {
      setError('Upload failed');
    }
    if (fileRef.current) fileRef.current.value = '';
  }

  return (
    <div className="studio-section">
      <div className="studio-entities-head">
        <div className="studio-section__title">Artifacts ({artifacts.length})</div>
        <button className="studio-btn studio-btn--primary" onClick={() => fileRef.current?.click()}>
          ＋ Upload
        </button>
        <input ref={fileRef} type="file" accept={ACCEPT} hidden onChange={onFile} aria-label="Upload artifact" />
      </div>

      {error && (
        <ul className="studio-errors">
          <li>{error}</li>
        </ul>
      )}

      {artifacts.length === 0 ? (
        <p className="studio-empty">No artifacts yet. Upload diagrams, images, or xml.</p>
      ) : (
        <ul className="studio-artifact-list">
          {artifacts.map((a) => (
            <li key={a.path}>
              <button
                className={`studio-artifact-item ${selected?.path === a.path ? 'is-active' : ''}`}
                onClick={() => setSelected(a)}
              >
                <span>{a.filename}</span>
                <span className="studio-artifact-item__meta">{formatSize(a.size)}</span>
              </button>
            </li>
          ))}
        </ul>
      )}

      {selected && (
        <div className="studio-artifact-view">
          <ArtifactViewer block={block} artifact={selected} />
        </div>
      )}
    </div>
  );
}
