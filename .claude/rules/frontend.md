---
globs: ["viewer/**"]
---

# Frontend Conventions — Context Blocks Viewer

Apply when writing or modifying any file in `viewer/`.

## Design System
- **This is the project's own design system and it OVERRIDES the global neo-brutalist design rule. Do NOT apply monochrome/brutalist styling (no `border-radius: 0`, no heavy black borders, no black/white-only palette) in `viewer/`.** The viewer is a clean dark theme with rounded corners (`var(--cb-radius*)`) and a purple accent (`var(--cb-primary)`).
- All colors, spacing, typography, radii via CSS variables in `viewer/src/styles/global.css`
- NEVER use inline hex values or hardcoded pixel sizes (including `border-radius: 0`) — always reference `var(--cb-*)`
- NO per-component CSS files — all styles in global.css or inline via CSS variables
- Dark mode is default. Light mode via `[data-theme="light"]` selector
- Both modes must work on every component — test both before committing

## Confidence Rendering
- >= 0.85: solid border, full opacity (confident)
- 0.55-0.84: solid border, muted opacity (uncertain)
- < 0.55: dashed/dotted border, low opacity (sketch/hypothesis)
- NEVER use red for low confidence. Red = error. Low confidence = draft.
- Use the entity's layer color with opacity — not a separate color scale

## Data Flow
- All entity data comes from `viewer/src/data/registry.ts` (build-time singleton)
- NO component should read files directly — always go through the registry
- Registry is built from entity markdown + meta-model.yaml at Astro build time
- React components receive data as serialized props, not via imports

## Component Rules
- Astro components (.astro) for static/server-rendered content
- React components (.tsx) only when client-side interactivity is needed (graphs, search, sidebar state)
- React islands use `client:load` for above-the-fold, `client:only="react"` for browser-only APIs
- Shared components in `viewer/src/components/shared/` — reuse before creating new
- One component per file, file name matches component name

## Graceful Degradation
- Missing entity fields → show empty, never crash
- Unknown entity types → render with generic style from config fallback
- Broken relationship targets → show with ⚠️ indicator, never hide
- Bad/missing data should NEVER produce a build error or blank page

## Typography
- Body: Inter via CSS variable `var(--cb-font-body)`
- Monospace: for data, IDs, code — `var(--cb-font-mono)`
- Size scale: xs (11px), sm (12px), base (14px), md (15px), lg (16px), xl (20px), 2xl (24px)

## Anti-Patterns (NEVER do)
- Do not render all 400+ entities as a flat tag cloud on any page
- Do not use graph as the primary human interface — narrative views come first
- Do not add third-party UI frameworks (no Tailwind, no Chakra, no MUI)
- Do not use `!important` in CSS
- Do not create barrel files (index.ts re-exports)
