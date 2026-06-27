/**
 * GlossaryTable — searchable, filterable glossary for jargon entities.
 *
 * Receives all jargon entities as a plain array (serialized from Astro).
 * Filter tabs and search are fully client-side.
 */
import { useState, useMemo } from 'react';

export interface GlossaryEntry {
  id: string;
  name: string;
  typeLabel: string;
  description: string;
  layerColor: string;
}

interface Props {
  entries: GlossaryEntry[];
}

type FilterTab = 'all' | string;

/** Derive the short category name from typeLabel: "Business Jargon" → "Business" */
function categoryFromTypeLabel(typeLabel: string): string {
  // typeLabel values: e.g. "Business Jargon", "Tech Jargon", "Business Terminology", etc.
  // Take the first word — vocabulary-agnostic, no hardcoded enum values.
  return typeLabel.split(/\s+/)[0] ?? typeLabel;
}

export function GlossaryTable({ entries }: Props) {
  const [query, setQuery] = useState('');
  const [activeTab, setActiveTab] = useState<FilterTab>('all');

  // Derive unique category tabs from the data, not from hardcoded strings.
  const categories = useMemo<string[]>(() => {
    const seen = new Set<string>();
    for (const e of entries) {
      seen.add(categoryFromTypeLabel(e.typeLabel));
    }
    return [...seen].sort();
  }, [entries]);

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();
    return entries
      .filter(e => {
        if (activeTab !== 'all' && categoryFromTypeLabel(e.typeLabel) !== activeTab) {
          return false;
        }
        if (q) {
          return (
            e.name.toLowerCase().includes(q) ||
            e.description.toLowerCase().includes(q)
          );
        }
        return true;
      })
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [entries, query, activeTab]);

  return (
    <div className="glossary-root">
      {/* Search + filter toolbar */}
      <div className="glossary-toolbar">
        <input
          className="glossary-search"
          type="search"
          placeholder="Search terms..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          aria-label="Search glossary terms"
        />

        <div className="glossary-tabs" role="tablist" aria-label="Filter by category">
          <button
            role="tab"
            aria-selected={activeTab === 'all'}
            className={`glossary-tab${activeTab === 'all' ? ' glossary-tab--active' : ''}`}
            onClick={() => setActiveTab('all')}
          >
            All
            <span className="glossary-tab__count">{entries.length}</span>
          </button>

          {categories.map(cat => {
            const count = entries.filter(
              e => categoryFromTypeLabel(e.typeLabel) === cat
            ).length;
            return (
              <button
                key={cat}
                role="tab"
                aria-selected={activeTab === cat}
                className={`glossary-tab${activeTab === cat ? ' glossary-tab--active' : ''}`}
                onClick={() => setActiveTab(cat)}
              >
                {cat}
                <span className="glossary-tab__count">{count}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Results count */}
      <p className="glossary-results-count">
        {filtered.length === entries.length
          ? `${entries.length} terms`
          : `${filtered.length} of ${entries.length} terms`}
      </p>

      {/* Table */}
      {filtered.length === 0 ? (
        <div className="glossary-empty">
          No terms match your search.
        </div>
      ) : (
        <table className="glossary-table" aria-label="Glossary">
          <thead>
            <tr>
              <th className="glossary-th glossary-th--term">Term</th>
              <th className="glossary-th glossary-th--type">Type</th>
              <th className="glossary-th glossary-th--desc">Description</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(entry => (
              <tr key={entry.id} className="glossary-row">
                <td className="glossary-td glossary-td--term">
                  <a
                    href={`/explorer?entity=${entry.id}`}
                    className="glossary-term-link"
                  >
                    {entry.name}
                  </a>
                </td>
                <td className="glossary-td glossary-td--type">
                  <span
                    className="glossary-type-badge"
                    style={{ '--badge-color': entry.layerColor } as React.CSSProperties}
                  >
                    {categoryFromTypeLabel(entry.typeLabel)}
                  </span>
                </td>
                <td className="glossary-td glossary-td--desc">
                  {entry.description || (
                    <span className="glossary-no-desc">No description</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <style>{`
        .glossary-root {
          font-family: var(--cb-font-body);
        }

        /* Toolbar */
        .glossary-toolbar {
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          gap: var(--cb-space-md);
          margin-bottom: var(--cb-space-md);
        }

        .glossary-search {
          flex: 1;
          min-width: 200px;
          max-width: 360px;
          padding: var(--cb-space-sm) var(--cb-space-md);
          font-size: var(--cb-font-size-sm);
          font-family: var(--cb-font-body);
          background: var(--cb-surface-raised);
          border: 1px solid var(--cb-border-strong);
          border-radius: var(--cb-radius-sm);
          color: var(--cb-text);
          outline: none;
          transition: border-color 0.15s;
        }
        .glossary-search:focus {
          border-color: var(--cb-primary);
        }
        .glossary-search::placeholder {
          color: var(--cb-text-faint);
        }

        /* Tabs */
        .glossary-tabs {
          display: flex;
          gap: var(--cb-space-xs);
          flex-wrap: wrap;
        }

        .glossary-tab {
          display: inline-flex;
          align-items: center;
          gap: var(--cb-space-xs);
          padding: var(--cb-space-xs) var(--cb-space-md);
          font-size: var(--cb-font-size-sm);
          font-family: var(--cb-font-body);
          font-weight: 500;
          border: 1px solid var(--cb-border);
          border-radius: var(--cb-radius-sm);
          background: transparent;
          color: var(--cb-text-muted);
          cursor: pointer;
          transition: background 0.15s, color 0.15s, border-color 0.15s;
        }
        .glossary-tab:hover {
          background: var(--cb-surface-hover);
          color: var(--cb-text);
        }
        .glossary-tab--active {
          background: var(--cb-primary-muted);
          color: var(--cb-text);
          border-color: var(--cb-primary);
        }
        .glossary-tab__count {
          font-size: var(--cb-font-size-xs);
          color: var(--cb-text-faint);
          font-weight: 400;
        }
        .glossary-tab--active .glossary-tab__count {
          color: var(--cb-text-muted);
        }

        /* Results count */
        .glossary-results-count {
          font-size: var(--cb-font-size-sm);
          color: var(--cb-text-faint);
          margin-bottom: var(--cb-space-md);
        }

        /* Empty state */
        .glossary-empty {
          text-align: center;
          padding: var(--cb-space-2xl);
          color: var(--cb-text-faint);
          font-size: var(--cb-font-size-sm);
          border: 1px solid var(--cb-border);
          border-radius: var(--cb-radius);
        }

        /* Table */
        .glossary-table {
          width: 100%;
          border-collapse: collapse;
          font-size: var(--cb-font-size-sm);
        }

        .glossary-th {
          padding: var(--cb-space-sm) var(--cb-space-md);
          text-align: left;
          font-size: var(--cb-font-size-xs);
          font-weight: 600;
          color: var(--cb-text-faint);
          text-transform: uppercase;
          letter-spacing: 0.06em;
          border-bottom: 1px solid var(--cb-border-strong);
          white-space: nowrap;
        }
        .glossary-th--term { width: 22%; }
        .glossary-th--type { width: 14%; }
        .glossary-th--desc { width: 64%; }

        .glossary-row {
          border-bottom: 1px solid var(--cb-border);
          transition: background 0.1s;
        }
        .glossary-row:last-child {
          border-bottom: none;
        }
        .glossary-row:hover {
          background: var(--cb-surface-hover);
        }

        .glossary-td {
          padding: var(--cb-space-md);
          vertical-align: top;
          line-height: 1.5;
        }
        .glossary-td--term {
          font-weight: 500;
        }
        .glossary-td--desc {
          color: var(--cb-text-muted);
        }

        .glossary-term-link {
          color: var(--cb-text);
          font-weight: 600;
          text-decoration: none;
          transition: color 0.15s;
        }
        .glossary-term-link:hover {
          color: var(--cb-primary);
          text-decoration: none;
        }

        /* Type badge */
        .glossary-type-badge {
          display: inline-block;
          padding: 2px 8px;
          border-radius: var(--cb-radius-sm);
          font-size: var(--cb-font-size-xs);
          font-weight: 500;
          color: var(--badge-color, var(--cb-text-muted));
          background: color-mix(in srgb, var(--badge-color, transparent) 12%, transparent);
          border: 1px solid color-mix(in srgb, var(--badge-color, var(--cb-border)) 30%, transparent);
          white-space: nowrap;
        }

        .glossary-no-desc {
          color: var(--cb-text-faint);
          font-style: italic;
        }
      `}</style>
    </div>
  );
}
