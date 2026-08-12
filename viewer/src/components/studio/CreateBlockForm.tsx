import { useState, type FormEvent } from 'react';

import { detailMessage, studio } from '../../lib/studio-client';
import type { BlockDetail, CreateBlockPayload } from '../../lib/studio-types';

interface Props {
  onCreated: (block: BlockDetail) => void;
  onCancel?: () => void;
}

/** Create-block form. Mirrors the Studio API POST /blocks contract. */
export default function CreateBlockForm({ onCreated, onCancel }: Props) {
  const [name, setName] = useState('');
  const [label, setLabel] = useState('');
  const [description, setDescription] = useState('');
  const [ontologyMode, setOntologyMode] = useState<'default' | 'custom'>('default');
  const [ontologyYaml, setOntologyYaml] = useState('');
  const [seed, setSeed] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (!name.trim()) {
      setError('Name is required');
      return;
    }
    const payload: CreateBlockPayload = { name: name.trim() };
    if (label.trim()) payload.label = label.trim();
    if (description.trim()) payload.description = description.trim();
    if (ontologyMode === 'custom' && ontologyYaml.trim()) payload.ontology_yaml = ontologyYaml;
    if (seed.trim()) payload.seed_context = seed;

    setSubmitting(true);
    try {
      const res = await studio.createBlock(payload);
      if (res.ok && res.body) {
        onCreated(res.body);
      } else {
        setError(detailMessage(res.body));
      }
    } catch {
      setError('Could not reach the Studio API');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="studio-form" onSubmit={handleSubmit}>
      <div className="studio-form__title">Create Block</div>

      <div className="studio-field">
        <label htmlFor="cb-name">Name (kebab-case)</label>
        <input
          id="cb-name"
          className="studio-input"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="payments"
          autoComplete="off"
        />
      </div>

      <div className="studio-field">
        <label htmlFor="cb-label">Label</label>
        <input
          id="cb-label"
          className="studio-input"
          value={label}
          onChange={(e) => setLabel(e.target.value)}
          placeholder="Cost Control"
          autoComplete="off"
        />
      </div>

      <div className="studio-field">
        <label htmlFor="cb-description">Description</label>
        <input
          id="cb-description"
          className="studio-input"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          autoComplete="off"
        />
      </div>

      <fieldset className="studio-field">
        <legend>Ontology</legend>
        <label className="studio-radio">
          <input
            type="radio"
            name="onto"
            checked={ontologyMode === 'default'}
            onChange={() => setOntologyMode('default')}
          />
          Default (built-in 18-type meta-model)
        </label>
        <label className="studio-radio">
          <input
            type="radio"
            name="onto"
            checked={ontologyMode === 'custom'}
            onChange={() => setOntologyMode('custom')}
          />
          Custom YAML
        </label>
        {ontologyMode === 'custom' && (
          <textarea
            aria-label="Ontology YAML"
            className="studio-textarea"
            rows={10}
            value={ontologyYaml}
            onChange={(e) => setOntologyYaml(e.target.value)}
            placeholder={'layers:\n  behavioral: { label: Behavioral }\nentity_types:\n  incident: { layer: behavioral, directory: incidents, label: Incidents }\nrelationship_fields:\n  - affects'}
          />
        )}
      </fieldset>

      <div className="studio-field">
        <label htmlFor="cb-seed">Seed context (optional markdown)</label>
        <textarea
          id="cb-seed"
          className="studio-textarea"
          rows={4}
          value={seed}
          onChange={(e) => setSeed(e.target.value)}
          placeholder="# Bounded context orientation..."
        />
      </div>

      {error && (
        <ul className="studio-errors">
          <li>{error}</li>
        </ul>
      )}

      <div className="studio-actions">
        <button type="submit" className="studio-btn studio-btn--primary" disabled={submitting}>
          {submitting ? 'Creating…' : 'Create Block'}
        </button>
        {onCancel && (
          <button type="button" className="studio-btn" onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
