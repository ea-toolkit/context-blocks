---
globs: ["viewer/**/*.tsx", "viewer/**/*.ts", "viewer/**/*.astro", "viewer/**/*.css"]
---

# Vocabulary-Agnostic Frontend

Apply when writing or modifying any file in `viewer/`.

## Rule
The viewer must render ANY meta-model, not just the current one. All entity types, layers, relationship types, and their labels/colors come from `viewer/src/config/meta-model.yaml` at build time.

## What This Means
- **NEVER** write `if (type === 'system')` or `if (layer === 'structural')` or any conditional based on a specific type/layer/relationship name
- **NEVER** hardcode entity type labels, icons, or colors in components
- **ALWAYS** derive display properties from the meta-model config or entity data
- Unknown types must render with a generic fallback (gray color, `?` icon, type key as label)
- If you rename every type, layer, and relationship in `meta-model.yaml`, the UI must still build and render correctly

## Test
Before committing FE changes, mentally check: "If I added a new entity type called `custom-thing` to meta-model.yaml, would this component render it correctly without code changes?"

## Allowed Exceptions
- Graph layout hints (e.g., dagre rank positions) can be type-aware since they affect visualization quality
- Hardcoded style maps (NODE_STYLES) are optional enrichments — unknown types fall back to config-derived values
