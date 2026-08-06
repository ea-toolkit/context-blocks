import { useState, type FormEvent } from 'react';

import { detailMessage, studio, validationErrors } from '../../lib/studio-client';

interface Props {
  blockName: string;
  onAdded: () => void;
  onCancel?: () => void;
}

/** Paste-and-validate entity authoring. 422 responses render per-field errors. */
export default function AddEntityForm({ blockName, onAdded, onCancel }: Props) {
  const [content, setContent] = useState('');
  const [errors, setErrors] = useState<string[]>([]);
  const [warnings, setWarnings] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setErrors([]);
    setWarnings([]);
    if (!content.trim()) {
      setErrors(['Paste entity markdown first']);
      return;
    }
    setSubmitting(true);
    try {
      const res = await studio.addEntity(blockName, content);
      if (res.ok) {
        setContent('');
        onAdded(); // refresh the entity list
        const notes = res.body?.warnings ?? [];
        if (notes.length) {
          setWarnings(notes); // keep the form open so the curator sees the notes
        } else if (onCancel) {
          onCancel(); // clean add — close the form
        }
        return;
      }
      if (res.status === 422) {
        const errs = validationErrors(res.body);
        setErrors(errs.length ? errs : [detailMessage(res.body)]);
      } else {
        setErrors([detailMessage(res.body)]);
      }
    } catch {
      setErrors(['Could not reach the Studio API']);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="studio-form" onSubmit={handleSubmit}>
      <div className="studio-form__title">Add Entity</div>
      <p className="studio__subtitle">
        Paste the entity markdown (YAML frontmatter + body). Validated against this block's ontology.
      </p>
      <div className="studio-field">
        <label htmlFor="ae-content">Entity markdown</label>
        <textarea
          id="ae-content"
          className="studio-textarea"
          rows={12}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder={'---\ntype: incident\nid: checkout-outage\nname: Checkout Outage\ndescription: ...\nstatus: active\n---\n\n# Checkout Outage\n\n## Overview\n\n...'}
        />
      </div>

      {errors.length > 0 && (
        <ul className="studio-errors">
          {errors.map((e, i) => (
            <li key={i}>{e}</li>
          ))}
        </ul>
      )}

      {warnings.length > 0 && (
        <ul className="studio-warnings" aria-label="Warnings">
          {warnings.map((w, i) => (
            <li key={i}>{w}</li>
          ))}
        </ul>
      )}

      <div className="studio-actions">
        <button type="submit" className="studio-btn studio-btn--primary" disabled={submitting}>
          {submitting ? 'Validating…' : 'Validate & Add'}
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
