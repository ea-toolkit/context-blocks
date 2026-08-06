import { describe, expect, it } from 'vitest';

import { nodeDegrees } from './graph-layout';

describe('nodeDegrees', () => {
  it('counts in + out degree per node', () => {
    const d = nodeDegrees(
      [{ id: 'a' }, { id: 'b' }, { id: 'c' }],
      [
        { source: 'a', target: 'b' },
        { source: 'a', target: 'c' },
        { source: 'b', target: 'c' },
      ],
    );
    expect(d.get('a')).toBe(2);
    expect(d.get('b')).toBe(2);
    expect(d.get('c')).toBe(2);
  });

  it('ignores edges to unknown nodes', () => {
    const d = nodeDegrees([{ id: 'a' }], [{ source: 'a', target: 'ghost' }]);
    expect(d.get('a')).toBe(1);
    expect(d.has('ghost')).toBe(false);
  });

  it('is zero for isolated nodes', () => {
    const d = nodeDegrees([{ id: 'x' }], []);
    expect(d.get('x')).toBe(0);
  });
});
