import type { DomainMapProps, SerializedEdge, SerializedEntity } from '../components/map/DomainMap';

/** Aggregate an entity-level graph to the TYPE level: one node per entity type
 * (colored by layer, sized by instance count), edges = the distinct
 * relationships that occur between types. This is the ontology "schema graph" —
 * how the domain's concepts actually connect. Rendered with the same DomainMap. */
export function induceTypeGraph(props: DomainMapProps): DomainMapProps {
  const { entities, edges } = props;

  const typeOf = new Map(entities.map((e) => [e.id, e.type]));
  const firstOfType = new Map<string, SerializedEntity>();
  const count = new Map<string, number>();
  for (const e of entities) {
    count.set(e.type, (count.get(e.type) ?? 0) + 1);
    if (!firstOfType.has(e.type)) firstOfType.set(e.type, e);
  }

  // Distinct (sourceType, rel, targetType) triples.
  const typeEdges = new Map<string, SerializedEdge>();
  for (const edge of edges) {
    const st = typeOf.get(edge.source);
    const tt = typeOf.get(edge.target);
    if (!st || !tt) continue;
    const key = `${st}|${edge.type}|${tt}`;
    if (!typeEdges.has(key)) typeEdges.set(key, { source: st, target: tt, type: edge.type });
  }

  const out = new Map<string, number>();
  const inc = new Map<string, number>();
  for (const e of typeEdges.values()) {
    out.set(e.source, (out.get(e.source) ?? 0) + 1);
    inc.set(e.target, (inc.get(e.target) ?? 0) + 1);
  }

  const typeNodes: SerializedEntity[] = [...firstOfType.entries()].map(([type, meta]) => {
    const n = count.get(type) ?? 0;
    return {
      id: type,
      name: meta.typeLabel,
      type,
      typeLabel: meta.typeLabel,
      typeIcon: meta.typeIcon,
      layer: meta.layer,
      layerColor: meta.layerColor,
      confidence: 1,
      description: `${n} ${n === 1 ? 'entity' : 'entities'}`,
      outgoingCount: out.get(type) ?? 0,
      incomingCount: inc.get(type) ?? 0,
      relationshipCount: (out.get(type) ?? 0) + (inc.get(type) ?? 0),
    };
  });

  return {
    entities: typeNodes,
    edges: [...typeEdges.values()],
    layers: props.layers,
    entityTypes: props.entityTypes,
  };
}
