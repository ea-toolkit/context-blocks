/** Maps an artifact filename to the renderer that should display it.
 *
 * A small registry so adding/swapping a renderer is contained. Config-gated
 * renderers (raw `.drawio` via a self-hosted embed, `.uml`/`.puml` via a
 * self-hosted PlantUML server) fall back to a download card until enabled —
 * never wire in a public diagrams.net / plantuml.com dependency.
 */

export type RendererKind = 'image' | 'svg' | 'bpmn' | 'xml' | 'drawio' | 'uml' | 'download';

const IMAGE_EXTS = ['.png', '.jpg', '.jpeg', '.gif', '.webp'];

export function rendererFor(filename: string): RendererKind {
  const lower = filename.toLowerCase();
  const ext = lower.slice(lower.lastIndexOf('.'));

  // draw.io export convention: <name>.drawio.svg is a plain SVG.
  if (lower.endsWith('.drawio.svg')) return 'svg';
  if (IMAGE_EXTS.includes(ext)) return 'image';
  if (ext === '.svg') return 'svg';
  if (ext === '.bpmn') return 'bpmn';
  if (ext === '.xml') return 'xml';
  if (ext === '.drawio') return 'drawio';
  if (ext === '.uml' || ext === '.puml') return 'uml';
  return 'download';
}
