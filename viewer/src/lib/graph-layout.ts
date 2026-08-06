/** Pure graph helpers used by the graph layouts (kept framework-free + testable). */

/** Undirected degree (in + out) for each node id. Edges to unknown nodes are ignored. */
export function nodeDegrees(
  nodes: { id: string }[],
  edges: { source: string; target: string }[],
): Map<string, number> {
  const degree = new Map<string, number>();
  for (const n of nodes) degree.set(n.id, 0);
  for (const e of edges) {
    if (degree.has(e.source)) degree.set(e.source, (degree.get(e.source) ?? 0) + 1);
    if (degree.has(e.target)) degree.set(e.target, (degree.get(e.target) ?? 0) + 1);
  }
  return degree;
}
