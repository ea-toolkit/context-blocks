# Entity Output Format

All generated entities MUST follow this format. No exceptions.

## File Structure
- One entity per file
- Filename: `{id}.md` (kebab-case)
- Stored in: `output/entities/{type-directory}/` (directory from meta-model config)
- Entity type must exist in the meta-model (Python `meta_model.py` or viewer `meta-model.yaml`)

## YAML Frontmatter (required fields)
```yaml
---
type: <entity-type-key>
id: <kebab-case, unique within type, matches filename>
name: <Human Readable Name>
description: <one-line summary>
status: active | deprecated | planned | proposed
tags: [tag1, tag2]
source_documents: [doc-filename-1, doc-filename-2]
confidence: <0.0-1.0>
<relationship_type>: [target-entity-id-1, target-entity-id-2]
---
```

## Body (markdown)
- Start with `## Overview` (2-3 sentences)
- Then `## Details` (specifics)
- Optional: `## Open Questions` (bullet list — parsed by viewer)
- Keep under 150 lines — if longer, split or trim
- Reference other entities by their id, not by prose
- No duplicate information — link, don't repeat

## Naming Rules
- ID should NOT include entity type prefix (`billing-engine` not `system-billing-engine`)
- Use exact names from source docs (don't add `-service`, `-system` suffixes unless the doc uses them)
- Kebab-case everything: `rate-engine-v2` not `RateEngineV2`

## Relationships
- Frontmatter keys that are not standard fields are treated as relationships
- Values are entity IDs (kebab-case), never display names
- Can be string (single target) or list (multiple targets)
- Only add relationships you're confident about
- `source_documents` tracks which input documents this entity was extracted from

## Entity Types (18 types in 6 layers)
Structural: system, software-component, api, data-model, data-product, platform
Behavioral: process, business-event, domain-logic
Reference: reference-data
Organizational: team, persona, capability, offering, external-party
Language: jargon-business, jargon-tech
Decision: decision
