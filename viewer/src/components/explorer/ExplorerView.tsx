import { useState, useMemo, useCallback, useEffect } from 'react';
import { marked } from 'marked';
import { getConfidenceTier } from '../../lib/types';
import type { CBEntity } from '../../lib/types';

interface LayerGroup {
  key: string;
  label: string;
  color: string;
  types: TypeGroup[];
}

interface TypeGroup {
  key: string;
  label: string;
  icon: string;
  count: number;
}

interface Props {
  layers: LayerGroup[];
  entities: Record<string, CBEntity[]>;
  allEntities: Record<string, CBEntity>;
  initialType?: string;
  initialEntity?: string;
}

export default function ExplorerView({ layers, entities, allEntities, initialType, initialEntity }: Props) {
  const [selectedType, setSelectedType] = useState<string | null>(initialType ?? null);
  const [selectedEntityId, setSelectedEntityId] = useState<string | null>(initialEntity ?? null);
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedLayers, setExpandedLayers] = useState<Set<string>>(
    new Set(layers.map(l => l.key))
  );

  const updateUrl = useCallback((type: string | null, entityId: string | null) => {
    const url = new URL(window.location.href);
    if (type) url.searchParams.set('type', type);
    else url.searchParams.delete('type');
    if (entityId) url.searchParams.set('entity', entityId);
    else url.searchParams.delete('entity');
    window.history.replaceState({}, '', url.toString());
  }, []);

  const currentEntities = useMemo(() => {
    if (!selectedType) return [];
    let list = entities[selectedType] ?? [];
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      list = list.filter(e =>
        e.name.toLowerCase().includes(q) ||
        e.description.toLowerCase().includes(q) ||
        e.id.toLowerCase().includes(q)
      );
    }
    return list.sort((a, b) => b.confidence - a.confidence);
  }, [selectedType, entities, searchQuery]);

  const selectedEntity = selectedEntityId ? allEntities[selectedEntityId] : null;

  const toggleLayer = (key: string) => {
    const next = new Set(expandedLayers);
    if (next.has(key)) next.delete(key);
    else next.add(key);
    setExpandedLayers(next);
  };

  const selectType = (typeKey: string) => {
    setSelectedType(typeKey);
    setSelectedEntityId(null);
    setSearchQuery('');
    updateUrl(typeKey, null);
  };

  const selectEntity = (entityId: string) => {
    setSelectedEntityId(entityId);
    updateUrl(selectedType, entityId);
  };

  const navigateToEntity = useCallback((entityId: string) => {
    const target = allEntities[entityId];
    if (!target) return;
    setSelectedType(target.type);
    setSelectedEntityId(entityId);
    setSearchQuery('');
    updateUrl(target.type, entityId);
  }, [allEntities, updateUrl]);

  useEffect(() => {
    const onPopState = () => {
      const url = new URL(window.location.href);
      setSelectedType(url.searchParams.get('type'));
      setSelectedEntityId(url.searchParams.get('entity'));
    };
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  return (
    <div className="explorer">
      {/* Left sidebar */}
      <div className="explorer__sidebar">
        {layers.map(layer => (
          <div key={layer.key} className="sidebar-group">
            <div
              className="sidebar-group__header"
              onClick={() => toggleLayer(layer.key)}
            >
              <span className={`sidebar-group__chevron ${expandedLayers.has(layer.key) ? 'sidebar-group__chevron--expanded' : ''}`}>
                &#9654;
              </span>
              <span className="sidebar-group__dot" style={{ background: layer.color }} />
              <span>{layer.label}</span>
              <span className="sidebar-group__count">
                {layer.types.reduce((sum, t) => sum + t.count, 0)}
              </span>
            </div>

            {expandedLayers.has(layer.key) && layer.types
              .filter(t => t.count > 0)
              .map(type => (
                <div
                  key={type.key}
                  className={`sidebar-item ${selectedType === type.key ? 'sidebar-item--active' : ''}`}
                  onClick={() => selectType(type.key)}
                >
                  <span>{type.label}</span>
                  <span className="sidebar-item__count">{type.count}</span>
                </div>
              ))
            }
          </div>
        ))}
      </div>

      {/* Middle: entity list */}
      <div className={`explorer__list ${!selectedEntity ? 'explorer__list--wide' : ''}`}>
        {selectedType ? (
          <>
            <input
              type="text"
              placeholder="Search entities..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="explorer__search"
            />
            <div className="explorer__count">
              {currentEntities.length} entities
            </div>
            {currentEntities.map(entity => (
              <EntityListItem
                key={entity.id}
                entity={entity}
                isSelected={selectedEntityId === entity.id}
                onClick={() => selectEntity(entity.id)}
              />
            ))}
          </>
        ) : (
          <div className="explorer__empty">
            Select an entity type from the sidebar
          </div>
        )}
      </div>

      {/* Right: entity detail */}
      {selectedEntity && (
        <div className="explorer__detail">
          <EntityDetail
            entity={selectedEntity}
            allEntities={allEntities}
            onNavigate={navigateToEntity}
          />
        </div>
      )}
    </div>
  );
}

function EntityListItem({ entity, isSelected, onClick }: {
  entity: CBEntity;
  isSelected: boolean;
  onClick: () => void;
}) {
  const tier = getConfidenceTier(entity.confidence);
  const tierClass = tier === 'sketched' ? 'entity-list-item--sketched'
    : tier === 'muted' ? 'entity-list-item--muted' : '';

  return (
    <div
      onClick={onClick}
      className={`entity-list-item ${isSelected ? 'entity-list-item--selected' : ''} ${tierClass}`}
      style={{ '--entity-layer-color': entity.layerColor } as React.CSSProperties}
    >
      <div className="entity-list-item__name">{entity.name}</div>
      <div className="entity-list-item__desc">{entity.description}</div>
      <div className="entity-list-item__footer">
        <span className="entity-list-item__confidence">
          {(entity.confidence * 100).toFixed(0)}%
        </span>
        {entity.openQuestions.length > 0 && (
          <span className="badge badge--question">
            {entity.openQuestions.length} questions
          </span>
        )}
      </div>
    </div>
  );
}

function EntityDetail({ entity, allEntities, onNavigate }: {
  entity: CBEntity;
  allEntities: Record<string, CBEntity>;
  onNavigate: (entityId: string) => void;
}) {
  const bodyHtml = marked.parse(entity.body);
  const tier = getConfidenceTier(entity.confidence);

  const relsByType = new Map<string, string[]>();
  for (const rel of entity.relationships) {
    const list = relsByType.get(rel.type) ?? [];
    list.push(rel.targetId);
    relsByType.set(rel.type, list);
  }

  return (
    <div className="entity-detail">
      <div className="entity-detail__header">
        <div className="entity-detail__name">{entity.name}</div>
        <div className="entity-detail__meta">
          <span className="badge badge--layer" style={{
            '--badge-bg': `${entity.layerColor}20`,
            '--badge-color': entity.layerColor,
          } as React.CSSProperties}>
            {entity.typeLabel}
          </span>
          <span style={{
            fontSize: 'var(--cb-font-size-sm)',
            color: 'var(--cb-text-faint)',
            opacity: tier === 'sketched' ? 0.5 : tier === 'muted' ? 0.75 : 1,
          }}>
            {(entity.confidence * 100).toFixed(0)}% confidence
          </span>
          {entity.status !== 'active' && (
            <span className="badge" style={{ background: 'var(--cb-surface-raised)', color: 'var(--cb-text-faint)' }}>
              {entity.status}
            </span>
          )}
        </div>
        {entity.description && (
          <p style={{ color: 'var(--cb-text-muted)', marginTop: 'var(--cb-space-sm)' }}>
            {entity.description}
          </p>
        )}
      </div>

      <div className="cb-markdown entity-detail__body" dangerouslySetInnerHTML={{ __html: bodyHtml }} />

      {relsByType.size > 0 && (
        <div className="entity-detail__section">
          <div className="entity-detail__section-title">Relationships</div>
          {[...relsByType.entries()].map(([relType, targets]) => (
            <div key={relType} className="relationship-row">
              <span className="relationship-row__type">{relType}</span>
              <span className="relationship-row__arrow">→</span>
              {targets.map(targetId => {
                const target = allEntities[targetId];
                return (
                  <span
                    key={targetId}
                    className="entity-pill"
                    style={{
                      cursor: target ? 'pointer' : 'default',
                      opacity: target ? 1 : 0.5,
                    }}
                    onClick={() => target && onNavigate(targetId)}
                  >
                    {target ? (
                      <>
                        <span className="entity-pill__dot" style={{ background: target.layerColor }} />
                        {target.name}
                      </>
                    ) : (
                      <>{targetId} ⚠️</>
                    )}
                  </span>
                );
              })}
            </div>
          ))}
        </div>
      )}

      {entity.sourceDocuments.length > 0 && (
        <div className="entity-detail__section">
          <div className="entity-detail__section-title">Source Evidence</div>
          <div style={{ fontSize: 'var(--cb-font-size-sm)', color: 'var(--cb-text-muted)' }}>
            Found in {entity.sourceDocuments.length} document{entity.sourceDocuments.length > 1 ? 's' : ''}:
          </div>
          <ul className="source-list">
            {entity.sourceDocuments.map(doc => (
              <li key={doc} className="source-list__item">{doc}</li>
            ))}
          </ul>
        </div>
      )}

      {entity.openQuestions.length > 0 && (
        <div className="entity-detail__section">
          <div className="entity-detail__section-title">
            Open Questions
            <span className="badge badge--question" style={{ marginLeft: '8px' }}>
              {entity.openQuestions.length}
            </span>
          </div>
          {entity.openQuestions.map((q, i) => (
            <div key={i} className="question-card">
              <div className="question-card__text">{q}</div>
            </div>
          ))}
        </div>
      )}

      {entity.tags.length > 0 && (
        <div className="entity-detail__section">
          <div className="entity-detail__section-title">Tags</div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
            {entity.tags.map(tag => (
              <span key={tag} className="badge" style={{ background: 'var(--cb-surface-raised)', color: 'var(--cb-text-faint)' }}>
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
