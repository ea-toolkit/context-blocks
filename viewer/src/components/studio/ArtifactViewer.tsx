import { useEffect, useState } from 'react';

import { rendererFor } from '../../lib/artifact-render';
import { artifactUrl } from '../../lib/studio-client';
import type { ArtifactInfo } from '../../lib/studio-types';
import BpmnArtifact from './BpmnArtifact';
import DmnArtifact from './DmnArtifact';

interface Props {
  block: string;
  artifact: ArtifactInfo;
}

/** Renders a single artifact by type. Images/SVG inline; XML as text; bpmn and
 * config-gated formats (raw .drawio, .uml) fall back to a download card. */
export default function ArtifactViewer({ block, artifact }: Props) {
  const kind = rendererFor(artifact.filename);
  const url = artifactUrl(block, artifact.filename);

  if (kind === 'image' || kind === 'svg') {
    return <img className="studio-artifact-img" src={url} alt={artifact.filename} loading="lazy" />;
  }
  if (kind === 'bpmn') {
    return <BpmnArtifact url={url} />;
  }
  if (kind === 'dmn') {
    return <DmnArtifact url={url} />;
  }
  if (kind === 'xml') {
    return <XmlArtifact url={url} />;
  }
  return <ArtifactFallback kind={kind} url={url} filename={artifact.filename} />;
}

function XmlArtifact({ url }: { url: string }) {
  const [text, setText] = useState<string | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    let active = true;
    fetch(url)
      .then((r) => r.text())
      .then((t) => {
        if (active) setText(t);
      })
      .catch(() => {
        if (active) setError(true);
      });
    return () => {
      active = false;
    };
  }, [url]);

  if (error) return <p className="studio-empty">Could not load file.</p>;
  if (text === null) return <p className="studio-empty">Loading…</p>;
  return <pre className="studio-code">{text}</pre>;
}

function ArtifactFallback({ kind, url, filename }: { kind: string; url: string; filename: string }) {
  const note =
    kind === 'bpmn'
      ? 'BPMN preview is coming (bpmn-js renderer).'
      : kind === 'drawio'
        ? 'Raw .drawio needs a configured renderer — export to .drawio.svg to preview here, or download.'
        : kind === 'uml'
          ? 'UML/PlantUML needs a configured renderer — download to view.'
          : 'No inline preview for this file type.';
  return (
    <div className="studio-artifact-fallback">
      <p className="studio-empty">{note}</p>
      <a className="studio-btn" href={url} download={filename} target="_blank" rel="noreferrer">
        Download {filename}
      </a>
    </div>
  );
}
