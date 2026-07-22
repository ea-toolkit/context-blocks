import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

// Multi-block builds: build-blocks.mjs sets CB_BLOCK_BASE=/<block>/ and
// CB_OUT_DIR=dist/<block> per block. Defaults keep single-block builds at root.
export default defineConfig({
  base: process.env.CB_BLOCK_BASE || '/',
  outDir: process.env.CB_OUT_DIR || './dist',
  integrations: [react()],
  server: { port: 4321 },
  vite: {
    optimizeDeps: { include: ['dagre'] },
  },
});
