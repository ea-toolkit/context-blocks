import { useEffect, useRef, useState } from 'react';

// bpmn-js vendor styles (the reference app forgot these → unstyled diagrams).
// Embedded font variant avoids external font fetches.
import 'bpmn-js/dist/assets/diagram-js.css';
import 'bpmn-js/dist/assets/bpmn-js.css';
import 'bpmn-js/dist/assets/bpmn-font/css/bpmn-embedded.css';

interface Props {
  url: string;
}

interface BpmnCanvas {
  zoom: (mode: string) => void;
}
interface BpmnViewerInstance {
  importXML: (xml: string) => Promise<unknown>;
  get: (name: string) => BpmnCanvas;
  destroy: () => void;
}
type BpmnViewerCtor = new (opts: { container: HTMLElement }) => BpmnViewerInstance;

/** Read-only BPMN diagram. bpmn-js is browser-only, so it's dynamically
 * imported at render time (this component only mounts inside a client island). */
export default function BpmnArtifact({ url }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    let viewer: BpmnViewerInstance | null = null;

    async function run() {
      setLoading(true);
      setError(null);
      try {
        const xml = await (await fetch(url)).text();
        if (cancelled || !containerRef.current) return;
        const BpmnViewer = (await import('bpmn-js/lib/Viewer')).default as unknown as BpmnViewerCtor;
        viewer = new BpmnViewer({ container: containerRef.current });
        await viewer.importXML(xml);
        if (cancelled) return;
        try {
          viewer.get('canvas').zoom('fit-viewport');
        } catch {
          /* zoom is best-effort */
        }
        setLoading(false);
      } catch {
        if (!cancelled) {
          setError('Could not render this BPMN file.');
          setLoading(false);
        }
      }
    }

    void run();
    return () => {
      cancelled = true;
      if (viewer) {
        try {
          viewer.destroy();
        } catch {
          /* already gone */
        }
      }
    };
  }, [url]);

  return (
    <div className="studio-bpmn">
      {loading && <p className="studio-empty">Rendering diagram…</p>}
      {error && <p className="studio-empty">{error}</p>}
      <div ref={containerRef} className="studio-bpmn__canvas" />
    </div>
  );
}
