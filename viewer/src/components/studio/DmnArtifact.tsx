import { useEffect, useRef, useState } from 'react';

// dmn-js vendor styles (DRD + decision-table + literal-expression views).
// Embedded font variant avoids external font fetches.
import 'dmn-js/dist/assets/diagram-js.css';
import 'dmn-js/dist/assets/dmn-js-shared.css';
import 'dmn-js/dist/assets/dmn-js-drd.css';
import 'dmn-js/dist/assets/dmn-js-decision-table.css';
import 'dmn-js/dist/assets/dmn-js-literal-expression.css';
import 'dmn-js/dist/assets/dmn-font/css/dmn-embedded.css';

interface Props {
  url: string;
}

interface DmnCanvas {
  zoom: (mode: string) => void;
}
interface DmnActiveViewer {
  get: (name: string) => DmnCanvas;
}
interface DmnViewerInstance {
  importXML: (xml: string) => Promise<unknown>;
  getActiveViewer: () => DmnActiveViewer | undefined;
  destroy: () => void;
}
type DmnViewerCtor = new (opts: { container: HTMLElement }) => DmnViewerInstance;

/** Read-only DMN decision model (decision requirements graph + tables). dmn-js
 * is browser-only, so it's dynamically imported at render time (this component
 * only mounts inside a client island). Mirrors BpmnArtifact. */
export default function DmnArtifact({ url }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    let viewer: DmnViewerInstance | null = null;

    async function run() {
      setLoading(true);
      setError(null);
      try {
        const xml = await (await fetch(url)).text();
        if (cancelled || !containerRef.current) return;
        const DmnViewer = (await import('dmn-js/lib/Viewer')).default as unknown as DmnViewerCtor;
        viewer = new DmnViewer({ container: containerRef.current });
        await viewer.importXML(xml);
        if (cancelled) return;
        try {
          // Only the DRD view has a zoomable canvas; table/expression views don't.
          viewer.getActiveViewer()?.get('canvas').zoom('fit-viewport');
        } catch {
          /* zoom is best-effort */
        }
        setLoading(false);
      } catch {
        if (!cancelled) {
          setError('Could not render this DMN file.');
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
    <div className="studio-dmn">
      {loading && <p className="studio-empty">Rendering decision model…</p>}
      {error && <p className="studio-empty">{error}</p>}
      <div ref={containerRef} className="studio-dmn__canvas" />
    </div>
  );
}
