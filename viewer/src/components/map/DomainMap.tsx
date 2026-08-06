import React, {
  useState,
  useEffect,
  useCallback,
  useMemo,
  useRef,
} from 'react';
import dagre from 'dagre';
import {
  forceSimulation,
  forceLink,
  forceManyBody,
  forceCenter,
  forceCollide,
  type SimulationNodeDatum,
  type SimulationLinkDatum,
} from 'd3-force';
import {
  ReactFlow,
  ReactFlowProvider,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  useReactFlow,
  type Node,
  type Edge,
  type NodeMouseHandler,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import EntityNode, { type EntityNodeData } from './EntityNode';
import RelationEdge, { CBEdgeMarkerDefs } from './RelationEdge';
import { nodeDegrees } from '../../lib/graph-layout';

// ── Types ──────────────────────────────────────────────────────────────────

export interface SerializedEntity {
  id: string;
  name: string;
  type: string;
  typeLabel: string;
  typeIcon: string;
  layer: string;
  layerColor: string;
  confidence: number;
  description: string;
  relationshipCount: number;
  incomingCount: number;
  outgoingCount: number;
}

export interface SerializedEdge {
  source: string;
  target: string;
  type: string;
}

export interface LayerMeta {
  key: string;
  label: string;
  color: string;
}

export interface EntityTypeMeta {
  key: string;
  label: string;
  layer: string;
}

export interface DomainMapProps {
  entities: SerializedEntity[];
  edges: SerializedEdge[];
  layers: LayerMeta[];
  entityTypes: EntityTypeMeta[];
}

type LayoutMode = 'organic' | 'hubs' | 'tree';

// ── Constants ──────────────────────────────────────────────────────────────

const NODE_WIDTH = 180;
const NODE_HEIGHT = 60;
const ZOOM_LABEL_THRESHOLD = 1.2;

const nodeTypes = { entityNode: EntityNode };
const edgeTypes = { relationEdge: RelationEdge };

// ── Layout helpers ─────────────────────────────────────────────────────────

function buildDagreLayout(nodes: Node[], edges: Edge[], direction: 'TB' | 'LR'): Node[] {
  try {
    const g = new dagre.graphlib.Graph();
    g.setGraph({ rankdir: direction, ranksep: 120, nodesep: 60, marginx: 40, marginy: 40 });
    g.setDefaultEdgeLabel(() => ({}));

    for (const node of nodes) g.setNode(node.id, { width: NODE_WIDTH, height: NODE_HEIGHT });
    for (const edge of edges) {
      if (g.hasNode(edge.source) && g.hasNode(edge.target)) g.setEdge(edge.source, edge.target);
    }

    dagre.layout(g);

    return nodes.map(node => {
      const n = g.node(node.id);
      return { ...node, position: { x: n.x - NODE_WIDTH / 2, y: n.y - NODE_HEIGHT / 2 } };
    });
  } catch (err) {
    console.warn('[DomainMap] Dagre layout failed, using fallback.', err);
    return applyFallbackLayout(nodes);
  }
}

interface ForceNode extends SimulationNodeDatum {
  id: string;
}

function buildForceLayout(nodes: Node[], edges: Edge[]): Node[] {
  const nodeIds = new Set(nodes.map(n => n.id));

  const simNodes: ForceNode[] = nodes.map(n => ({ id: n.id, x: 0, y: 0 }));
  const simLinks: SimulationLinkDatum<ForceNode>[] = edges
    .filter(e => nodeIds.has(e.source) && nodeIds.has(e.target))
    .map(e => ({ source: e.source, target: e.target }));

  const nodeMap = new Map(simNodes.map(n => [n.id, n]));
  const nodeCount = simNodes.length;
  const spreadFactor = Math.sqrt(nodeCount) * 25;

  const sim = forceSimulation<ForceNode>(simNodes)
    .force('link', forceLink<ForceNode, SimulationLinkDatum<ForceNode>>(simLinks)
      .id(d => d.id)
      .distance(180)
      .strength(0.4))
    .force('charge', forceManyBody().strength(-300))
    .force('center', forceCenter(0, 0))
    .force('collide', forceCollide(NODE_WIDTH * 0.6))
    .stop();

  // Spread initial positions to avoid starting from origin
  for (const n of simNodes) {
    n.x = (Math.random() - 0.5) * spreadFactor * 2;
    n.y = (Math.random() - 0.5) * spreadFactor * 2;
  }

  // Run simulation synchronously
  const ticks = Math.max(200, Math.min(400, nodeCount));
  for (let i = 0; i < ticks; i++) sim.tick();

  return nodes.map(node => {
    const sn = nodeMap.get(node.id);
    return {
      ...node,
      position: {
        x: (sn?.x ?? 0) - NODE_WIDTH / 2,
        y: (sn?.y ?? 0) - NODE_HEIGHT / 2,
      },
    };
  });
}

function applyFallbackLayout(nodes: Node[]): Node[] {
  const cols = Math.ceil(Math.sqrt(nodes.length));
  return nodes.map((node, i) => ({
    ...node,
    position: {
      x: (i % cols) * (NODE_WIDTH + 40),
      y: Math.floor(i / cols) * (NODE_HEIGHT + 40),
    },
  }));
}

/** "Hubs" layout: well-connected nodes force-clustered in a central core,
 * low-degree leaf nodes arranged on an outer ring. */
function buildHubsLayout(nodes: Node[], edges: Edge[]): Node[] {
  const degree = nodeDegrees(nodes, edges);
  const core = nodes.filter(n => (degree.get(n.id) ?? 0) >= 2);
  const periphery = nodes.filter(n => (degree.get(n.id) ?? 0) < 2);

  // Core via the force simulation (compact, central around origin).
  const coreLaid = core.length ? buildForceLayout(core, edges) : [];

  let maxR = 0;
  for (const n of coreLaid) {
    const r = Math.hypot(n.position.x + NODE_WIDTH / 2, n.position.y + NODE_HEIGHT / 2);
    if (r > maxR) maxR = r;
  }
  const ringR = Math.max(maxR + 320, Math.sqrt(nodes.length) * 55);

  const periLaid = periphery.map((node, i) => {
    const angle = (i / Math.max(periphery.length, 1)) * 2 * Math.PI;
    return {
      ...node,
      position: {
        x: Math.cos(angle) * ringR - NODE_WIDTH / 2,
        y: Math.sin(angle) * ringR - NODE_HEIGHT / 2,
      },
    };
  });

  return [...coreLaid, ...periLaid];
}

function applyLayout(nodes: Node[], edges: Edge[], mode: LayoutMode): Node[] {
  if (mode === 'organic') return buildForceLayout(nodes, edges);
  if (mode === 'hubs') return buildHubsLayout(nodes, edges);
  return buildDagreLayout(nodes, edges, 'TB');
}

// ── Utilities ──────────────────────────────────────────────────────────────

function getConnectedIds(nodeId: string, edges: Edge[]): Set<string> {
  const ids = new Set<string>([nodeId]);
  for (const e of edges) {
    if (e.source === nodeId) ids.add(e.target);
    if (e.target === nodeId) ids.add(e.source);
  }
  return ids;
}

function hexToRgba(hex: string, alpha: number): string {
  try {
    const clean = hex.replace('#', '');
    const full = clean.length === 3
      ? clean.split('').map(c => c + c).join('')
      : clean;
    const r = parseInt(full.slice(0, 2), 16);
    const g = parseInt(full.slice(2, 4), 16);
    const b = parseInt(full.slice(4, 6), 16);
    if (isNaN(r) || isNaN(g) || isNaN(b)) return hex;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  } catch {
    return hex;
  }
}

const LAYOUT_LABELS: Record<LayoutMode, string> = {
  organic: 'Organic',
  hubs: 'Hubs',
  tree: 'Tree',
};
const LAYOUT_MODES: LayoutMode[] = ['organic', 'hubs', 'tree'];

// ── Inner component ────────────────────────────────────────────────────────

function DomainMapInner({ entities, edges: rawEdges, layers, entityTypes }: DomainMapProps) {
  const { fitView, getZoom } = useReactFlow();

  const [activeLayers, setActiveLayers] = useState<Set<string>>(
    new Set(layers.map(l => l.key))
  );
  const [activeTypes, setActiveTypes] = useState<Set<string>>(
    new Set(entityTypes.map(t => t.key))
  );
  const [confidenceMin, setConfidenceMin] = useState(0);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);
  const [layoutMode, setLayoutMode] = useState<LayoutMode>('organic');
  const [focusedNodeId, setFocusedNodeId] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [zoomLevel, setZoomLevel] = useState(0.5);

  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);
  const [isReady, setIsReady] = useState(false);
  const [isComputing, setIsComputing] = useState(false);

  const allNodesRef = useRef<Node[]>([]);
  const allEdgesRef = useRef<Edge[]>([]);

  // ── Build initial nodes + edges ──
  useEffect(() => {
    setIsComputing(true);
    setIsReady(false);

    // Defer to next frame so the "Computing..." message renders
    requestAnimationFrame(() => {
      const rawNodes: Node[] = entities.map(e => ({
        id: e.id,
        type: 'entityNode',
        position: { x: 0, y: 0 },
        data: {
          id: e.id,
          name: e.name,
          type: e.type,
          typeLabel: e.typeLabel,
          typeIcon: e.typeIcon,
          layer: e.layer,
          layerColor: e.layerColor,
          confidence: e.confidence,
          description: e.description,
        } satisfies EntityNodeData,
        width: NODE_WIDTH,
        height: NODE_HEIGHT,
      }));

      const rfEdges: Edge[] = rawEdges.map((e, i) => {
        const sourceEntity = entities.find(en => en.id === e.source);
        return {
          id: `${e.source}--${e.type}--${e.target}--${i}`,
          source: e.source,
          target: e.target,
          type: 'relationEdge',
          data: {
            type: e.type,
            sourceLayerColor: sourceEntity?.layerColor ?? '#666',
            showLabel: false,
          },
        };
      });

      const laid = applyLayout(rawNodes, rfEdges, layoutMode);
      allNodesRef.current = laid;
      allEdgesRef.current = rfEdges;

      setNodes(laid);
      setEdges(rfEdges);
      setIsComputing(false);
      setIsReady(true);
    });
  }, [entities, rawEdges, layoutMode, setNodes, setEdges]);

  // ── Fit view on ready ──
  useEffect(() => {
    if (!isReady) return;
    const t = setTimeout(() => fitView({ padding: 0.1 }), 150);
    return () => clearTimeout(t);
  }, [isReady, fitView]);

  // ── Visible count ──
  const visibleCount = useMemo(() => {
    if (!isReady) return entities.length;
    return allNodesRef.current.filter(node => {
      const d = node.data as EntityNodeData;
      if (!activeLayers.has(d.layer)) return false;
      if (!activeTypes.has(d.type)) return false;
      if (d.confidence < confidenceMin) return false;
      return true;
    }).length;
  }, [activeLayers, activeTypes, confidenceMin, isReady, entities.length]);

  // ── Apply filters + hover + focus ──
  useEffect(() => {
    if (!isReady) return;

    const showLabels = zoomLevel >= ZOOM_LABEL_THRESHOLD;
    const focusIds = focusedNodeId
      ? getConnectedIds(focusedNodeId, allEdgesRef.current)
      : null;

    const filtered = allNodesRef.current.filter(node => {
      const d = node.data as EntityNodeData;
      if (focusIds && !focusIds.has(node.id)) return false;
      if (!activeLayers.has(d.layer)) return false;
      if (!activeTypes.has(d.type)) return false;
      if (d.confidence < confidenceMin) return false;
      return true;
    });

    const visibleIds = new Set(filtered.map(n => n.id));
    const connectedToHovered = hoveredNodeId
      ? getConnectedIds(hoveredNodeId, allEdgesRef.current)
      : null;

    const term = searchTerm.trim().toLowerCase();
    const visibleNodes = filtered.map(node => {
      const d = node.data as EntityNodeData;
      let opacity = 1;
      if (term && !(d.name.toLowerCase().includes(term) || node.id.toLowerCase().includes(term))) {
        opacity = 0.12;
      } else if (hoveredNodeId && connectedToHovered && !connectedToHovered.has(node.id)) {
        opacity = 0.2;
      }
      return {
        ...node,
        data: { ...d },
        style: { ...node.style, opacity, transition: 'opacity 0.15s' },
      };
    });

    const visibleEdges = allEdgesRef.current
      .filter(e => visibleIds.has(e.source) && visibleIds.has(e.target))
      .map(e => {
        let opacity = 1;
        const isHoverConnected = hoveredNodeId && (e.source === hoveredNodeId || e.target === hoveredNodeId);
        if (hoveredNodeId && connectedToHovered) {
          opacity = isHoverConnected ? 1 : 0.1;
        }
        return {
          ...e,
          data: {
            ...(e.data as Record<string, unknown>),
            showLabel: showLabels || !!isHoverConnected,
          },
          style: { opacity, transition: 'opacity 0.15s' },
        };
      });

    setNodes(visibleNodes);
    setEdges(visibleEdges);
  }, [activeLayers, activeTypes, confidenceMin, hoveredNodeId, focusedNodeId, zoomLevel, searchTerm, isReady, setNodes, setEdges]);

  // ── Event handlers ──
  const onNodeClick: NodeMouseHandler = useCallback((_event, node) => {
    setSelectedNodeId(prev => prev === node.id ? null : node.id);
  }, []);

  const onNodeMouseEnter: NodeMouseHandler = useCallback((_event, node) => {
    setHoveredNodeId(node.id);
  }, []);

  const onNodeMouseLeave: NodeMouseHandler = useCallback(() => {
    setHoveredNodeId(null);
  }, []);

  const handleFitView = useCallback(() => {
    fitView({ padding: 0.1, duration: 400 });
  }, [fitView]);

  const handleFocus = useCallback((nodeId: string) => {
    setFocusedNodeId(nodeId);
    setTimeout(() => fitView({ padding: 0.2, duration: 400 }), 50);
  }, [fitView]);

  const handleClearFocus = useCallback(() => {
    setFocusedNodeId(null);
    setTimeout(() => fitView({ padding: 0.1, duration: 400 }), 50);
  }, [fitView]);

  const toggleLayer = useCallback((key: string) => {
    setActiveLayers(prev => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key); else next.add(key);
      return next;
    });
  }, []);

  const toggleType = useCallback((key: string) => {
    setActiveTypes(prev => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key); else next.add(key);
      return next;
    });
  }, []);

  const cycleLayout = useCallback(() => {
    setLayoutMode(prev => {
      const idx = LAYOUT_MODES.indexOf(prev);
      return LAYOUT_MODES[(idx + 1) % LAYOUT_MODES.length];
    });
  }, []);

  const onMoveEnd = useCallback(() => {
    try { setZoomLevel(getZoom()); } catch { /* ignore */ }
  }, [getZoom]);

  const selectedEntity = useMemo(
    () => selectedNodeId ? entities.find(e => e.id === selectedNodeId) : null,
    [selectedNodeId, entities]
  );

  const typesByActiveLayer = useMemo(() => {
    return entityTypes.filter(t => activeLayers.has(t.layer));
  }, [entityTypes, activeLayers]);

  if (!isReady || isComputing) {
    return (
      <div className="map__loading">
        Computing {LAYOUT_LABELS[layoutMode].toLowerCase()} layout for {entities.length} nodes...
      </div>
    );
  }

  return (
    <div className="map">
      {/* ── Filter toolbar ── */}
      <div className="map__toolbar">
        <div className="map__filter-group">
          <input
            type="search"
            placeholder="Find a node…"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="map__search"
            aria-label="Find a node"
          />
        </div>

        <div className="map__divider" />

        <div className="map__filter-group">
          <span className="map__filter-label">Layers</span>
          {layers.map(layer => (
            <label
              key={layer.key}
              className="map__layer-toggle"
              style={{ opacity: activeLayers.has(layer.key) ? 1 : 0.5 }}
            >
              <input
                type="checkbox"
                checked={activeLayers.has(layer.key)}
                onChange={() => toggleLayer(layer.key)}
                style={{ display: 'none' }}
              />
              <span
                className="map__layer-dot"
                style={{
                  background: layer.color,
                  opacity: activeLayers.has(layer.key) ? 1 : 0.3,
                }}
              />
              {layer.label}
            </label>
          ))}
        </div>

        <div className="map__divider" />

        <div className="map__filter-group">
          <span className="map__filter-label">Types</span>
          {typesByActiveLayer.map(t => {
            const layer = layers.find(l => l.key === t.layer);
            const active = activeTypes.has(t.key);
            return (
              <button
                key={t.key}
                onClick={() => toggleType(t.key)}
                className="map__type-btn"
                style={{
                  borderColor: active ? (layer?.color ?? 'var(--cb-border-strong)') : 'var(--cb-border)',
                  background: active ? hexToRgba(layer?.color ?? '#666', 0.12) : 'transparent',
                  color: active ? 'var(--cb-text)' : 'var(--cb-text-faint)',
                }}
              >
                {t.label}
              </button>
            );
          })}
        </div>

        <div className="map__divider" />

        <div className="map__filter-group">
          <span className="map__filter-label">Min confidence</span>
          <input
            type="range"
            min={0}
            max={1}
            step={0.05}
            value={confidenceMin}
            onChange={e => setConfidenceMin(parseFloat(e.target.value))}
            className="map__range"
          />
          <span className="map__range-value">
            {Math.round(confidenceMin * 100)}%
          </span>
        </div>

        <div className="map__divider" />

        {/* Layout mode switcher */}
        <div className="map__layout-switcher">
          {LAYOUT_MODES.map(mode => (
            <button
              key={mode}
              onClick={() => setLayoutMode(mode)}
              className={`map__layout-btn ${layoutMode === mode ? 'map__layout-btn--active' : ''}`}
            >
              {LAYOUT_LABELS[mode]}
            </button>
          ))}
        </div>

        <div className="map__toolbar-right">
          {focusedNodeId && (
            <button onClick={handleClearFocus} className="map__focus-clear-btn">
              Clear focus
            </button>
          )}
          <span className="map__count">
            {visibleCount} / {entities.length}
          </span>
          <button onClick={handleFitView} className="map__fit-btn">
            Fit All
          </button>
        </div>
      </div>

      {/* ── Graph + detail panel ── */}
      <div className="map__body">
        <div className="map__graph">
          <CBEdgeMarkerDefs />
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick}
            onNodeMouseEnter={onNodeMouseEnter}
            onNodeMouseLeave={onNodeMouseLeave}
            onMoveEnd={onMoveEnd}
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
            fitView
            fitViewOptions={{ padding: 0.1 }}
            minZoom={0.05}
            maxZoom={2.5}
            proOptions={{ hideAttribution: true }}
            style={{ background: 'var(--cb-bg, #0f1117)' }}
          >
            <Background
              color="var(--cb-border, rgba(255,255,255,0.08))"
              gap={24}
              size={1}
            />
            <Controls
              position="bottom-left"
              showInteractive={false}
              style={{
                background: 'var(--cb-surface)',
                border: '1px solid var(--cb-border)',
                borderRadius: 4,
              }}
            />
          </ReactFlow>
        </div>

        {/* ── Detail panel ── */}
        {selectedEntity && (
          <div className="map__detail">
            <div className="map__detail-header">
              <div style={{ flex: 1, minWidth: 0 }}>
                <div className="map__detail-name">{selectedEntity.name}</div>
                <div className="map__detail-badges">
                  <span
                    className="badge badge--layer"
                    style={{
                      '--badge-bg': hexToRgba(selectedEntity.layerColor, 0.15),
                      '--badge-color': selectedEntity.layerColor,
                    } as React.CSSProperties}
                  >
                    {selectedEntity.typeLabel}
                  </span>
                  <ConfidenceBadge confidence={selectedEntity.confidence} />
                </div>
              </div>
              <button
                onClick={() => setSelectedNodeId(null)}
                className="map__detail-close"
                aria-label="Close detail panel"
              >
                ×
              </button>
            </div>

            {selectedEntity.description && (
              <p className="map__detail-desc">{selectedEntity.description}</p>
            )}

            <div className="map__detail-stats">
              <StatBox label="Outgoing" value={selectedEntity.outgoingCount} />
              <StatBox label="Incoming" value={selectedEntity.incomingCount} />
            </div>

            <div className="map__detail-id">{selectedEntity.id}</div>

            <button
              onClick={() => handleFocus(selectedEntity.id)}
              className="map__detail-focus-btn"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8" /><path d="M21 21l-4.35-4.35" />
              </svg>
              Focus neighborhood
            </button>

            <a
              href={`/explorer?entity=${encodeURIComponent(selectedEntity.id)}&type=${encodeURIComponent(selectedEntity.type)}`}
              className="map__detail-explorer-link"
            >
              Open in Explorer
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </a>
          </div>
        )}
      </div>

      <style>{`
        @keyframes cb-slide-in {
          from { transform: translateX(20px); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
        .react-flow__controls button {
          background: var(--cb-surface-raised) !important;
          border-color: var(--cb-border) !important;
          color: var(--cb-text-muted) !important;
        }
        .react-flow__controls button:hover {
          background: var(--cb-surface-hover) !important;
          color: var(--cb-text) !important;
        }
        .map__search {
          background: var(--cb-surface-raised);
          color: var(--cb-text);
          border: 1px solid var(--cb-border);
          border-radius: var(--cb-radius-sm);
          padding: 6px 10px;
          font: inherit;
          font-size: var(--cb-font-size-sm);
          min-width: 180px;
        }
        .map__search:focus { outline: none; border-color: var(--cb-primary); }
      `}</style>
    </div>
  );
}

// ── Sub-components ─────────────────────────────────────────────────────────

function ConfidenceBadge({ confidence }: { confidence: number }) {
  const pct = Math.round(confidence * 100);
  const color = confidence >= 0.85 ? '#22c55e' : confidence >= 0.55 ? '#f59e0b' : '#ef4444';
  return (
    <span style={{
      padding: '2px 8px',
      fontSize: 11,
      fontWeight: 600,
      background: hexToRgba(color, 0.12),
      color,
      border: `1px solid ${hexToRgba(color, 0.3)}`,
      borderRadius: 3,
    }}>
      {pct}%
    </span>
  );
}

function StatBox({ label, value }: { label: string; value: number }) {
  return (
    <div className="map__stat-box">
      <div className="map__stat-value">{value}</div>
      <div className="map__stat-label">{label}</div>
    </div>
  );
}

// ── Export with ReactFlowProvider ──────────────────────────────────────────

export default function DomainMap(props: DomainMapProps) {
  return (
    <ReactFlowProvider>
      <DomainMapInner {...props} />
    </ReactFlowProvider>
  );
}
