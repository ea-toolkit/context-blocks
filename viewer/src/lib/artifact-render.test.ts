import { describe, expect, it } from 'vitest';

import { rendererFor } from './artifact-render';

describe('rendererFor', () => {
  it('maps image extensions', () => {
    for (const f of ['a.png', 'a.JPG', 'a.jpeg', 'a.gif', 'a.webp']) {
      expect(rendererFor(f)).toBe('image');
    }
  });

  it('maps svg and the drawio.svg export convention', () => {
    expect(rendererFor('a.svg')).toBe('svg');
    expect(rendererFor('arch.drawio.svg')).toBe('svg');
  });

  it('maps bpmn / xml', () => {
    expect(rendererFor('flow.bpmn')).toBe('bpmn');
    expect(rendererFor('config.xml')).toBe('xml');
  });

  it('maps config-gated formats to their own kinds (fallback until enabled)', () => {
    expect(rendererFor('arch.drawio')).toBe('drawio');
    expect(rendererFor('seq.uml')).toBe('uml');
    expect(rendererFor('seq.puml')).toBe('uml');
  });

  it('falls back to download for unknown types', () => {
    expect(rendererFor('data.bin')).toBe('download');
  });
});
