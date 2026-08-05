import { defineConfig } from 'vitest/config';

export default defineConfig({
  // esbuild (vitest's default transformer) handles TSX via the automatic JSX
  // runtime — no @vitejs/plugin-react needed for component tests.
  esbuild: { jsx: 'automatic' },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
  },
});
