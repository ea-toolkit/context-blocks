# Context Blocks

**Turn your company's docs into a knowledge base AI agents can actually use — then find out what's missing.**

Point it at your documentation. Get a structured domain knowledge base with typed entities, relationships, and confidence scores. Then run evals from multiple perspectives — developer, architect, product owner — and see exactly where your documentation is thin.

The gap is the product. Every unanswered question becomes a curation target.

## Quick Start

```bash
# Install
pip install context-blocks

# Configure API keys
export LLM_API_KEY=your-anthropic-key      # Required
export OPENAI_API_KEY=your-openai-key      # Optional (for embeddings; falls back to local)

# Initialize a context block
cb init my-domain --seed path/to/seed.md

# Extract entities from your docs
cb phase1 path/to/docs --seed path/to/seed.md --block my-domain

# Merge duplicate entities
cb dedup --block my-domain

# Run evals — see what your KB covers and what's missing
cb eval --block my-domain --seed path/to/seed.md --docs path/to/docs --personas

# Start the API server
cb serve --block my-domain

# Start the viewer (separate terminal, requires Node >= 18)
cd viewer && npm install && npm run dev
```

## Try It With Demo Data

A synthetic healthcare claims domain is included with pre-extracted entities — no API keys needed to explore:

```bash
# Start the viewer on the pre-built demo KB
cd viewer && npm install && npm run dev
# Open http://localhost:4321 — browse 410 entities across 6 knowledge layers

# Or run the full pipeline yourself (requires API keys)
cb phase1 synthetic-domains/healthcare-claims/docs \
  --seed synthetic-domains/healthcare-claims/seed-context.md \
  --output synthetic-domains/healthcare-claims/output
```

## What It Does

### Extract
Feed in your company's docs (Confluence exports, runbooks, architecture docs, markdown, PDFs). Context Blocks extracts a typed knowledge base: systems, processes, teams, decisions, business rules, jargon — **18 entity types across 6 knowledge layers**.

Each entity gets:
- **Type classification** from a typed ontology (system, process, data-model, domain-logic, etc.)
- **Confidence score** — how certain the extraction is
- **Source document provenance** — which doc created each entity
- **Relationships** — how entities connect across the domain
- **Open questions** — hedged statements and uncertainties flagged during extraction

### Context Blocks (Bounded Contexts)
Organize knowledge into scoped blocks — one per domain, team, or product area. Each block is an independent knowledge unit with its own entities, extractions, and configuration.

```bash
# Create blocks for different domains
cb init payments --seed payments-seed.md
cb init identity --seed identity-seed.md

# All commands accept --block or -b
cb phase1 ./docs --seed seed.md --block payments
cb eval --block payments --seed seed.md --personas

# Or set CB_BLOCK env var
export CB_BLOCK=payments
cb eval --seed seed.md --personas
```

### Evaluate
Generate questions from four sources and measure how well your KB answers them:

| Source | What it tests |
|---|---|
| **Seed context** | Can the KB flesh out what the onboarding doc promises? |
| **Source docs** | Did extraction capture what's in the original documents? |
| **Persona templates** | Does a developer / architect / PO / new joiner have what they need? |
| **Work items (DDC)** | Can the KB help resolve real Jira tickets and incidents? |

Results map to the DDC taxonomy: **CLEAN** (fully answerable), **INCOMPLETE** (partial), **MISSING** (not answerable).

### Retrieve
Ask questions against your KB with the Domain-Aware Retrieval (DAR) pipeline:
- **Typed intent classification** — understands if you're asking about a process, system, ownership, or relationship
- **Parallel search** — vector + keyword + typed graph traversal
- **Confidence-weighted fusion** — RRF scoring with layer priority boosts
- **Full retrieval traces** — see exactly which entities were found, via which relationships, at what confidence

### Find Gaps
Every eval question that scores INCOMPLETE or MISSING is a gap. Gaps include:
- What was found (entities)
- What's missing
- Suggested curation action
- Source (which perspective found this gap)

### Export
Get your KB out into the tools you already use:

```bash
# Obsidian vault with wikilinks and Map of Content
cb export-obsidian --block my-domain

# Single portable markdown for AI agent context windows
cb export-skill --block my-domain --title "My Domain KB"

# With token budget for smaller context windows
cb export-skill --block my-domain --max-tokens 10000
```

### Curate (DDC Loop)
The Demand-Driven Context cycle: evaluate, find gaps, curate entities to fill them, re-evaluate. Coverage improves with each cycle.

## CLI Commands

| Command | Description |
|---|---|
| `cb init <name>` | Initialize a new context block |
| `cb blocks` | List all context blocks in the project |
| `cb phase1` | Extract entities from documents |
| `cb dedup` | Merge duplicate entities after extraction |
| `cb eval` | Run coverage evaluation |
| `cb eval --dry-run` | Preview generated questions without running retrieval |
| `cb eval --personas` | Include persona-driven completeness checks |
| `cb eval --work-items <dir>` | Include real work items (DDC mode) |
| `cb ask "question"` | Ask a single question from the terminal |
| `cb serve` | Start the API server for the viewer |
| `cb reformat` | Regenerate entity markdown from extraction JSON (free, no API) |
| `cb export-obsidian` | Export KB as Obsidian vault with wikilinks |
| `cb export-skill` | Export KB as single portable markdown for agent context |

All commands accept `--block <name>` (or `-b`) to target a specific context block, or `--output <dir>` for direct path override. Set `CB_BLOCK` env var as default.

## Input Formats

| Format | Status |
|---|---|
| Markdown (.md) | Supported |
| Plain text (.txt) | Supported |
| PDF (.pdf) | Supported (via pypdf) |

## Viewer

Web UI with 8 pages (requires Node >= 18):
- **Ask** — question input with grounded answers and retrieval trace panel (requires API server: `cb serve`)
- **Digest** — domain overview, knowledge layers, top questions
- **Explorer** — browse entities by type with detail panel
- **Map** — interactive graph (navigation + exploration modes)
- **Workbench** — 4-tab curation hub: coverage, questions, health checks, review queue
- **Evals** — run explorer with KPI strip, source/layer breakdowns, question detail
- **Glossary** — searchable domain terminology
- **Gaps** — coverage summary with actionable gap cards

## Under the Hood

Capabilities you get without configuring anything:

| Capability | What it does |
|---|---|
| **Prompt caching** | Anthropic `cache_control` on system prompts — reduces cost on repeated calls |
| **Crash-safe resume** | Pipeline state saved per-document with file hashes — resume after crash without re-processing |
| **3-tier repair ladder** | Parse JSON → smart retry (broken JSON only, ~5K tokens) → full retry — maximizes entity salvage |
| **Per-entity validation** | Valid entities saved even when some fail — no all-or-nothing batches |
| **Dual embedding providers** | OpenAI API if key present, local Fastembed (BAAI/bge-small-en-v1.5) as fallback — works offline |
| **Relationship-aware embeddings** | Entity relationships included in embedding text — improves retrieval for "what connects to X" queries |
| **Post-extraction dedup** | LLM-judged duplicate detection with Jaccard similarity pre-filter — same-type only |
| **Hedged statement detection** | Extracts uncertain statements as open questions — surfaces knowledge gaps at extraction time |
| **New jargon detection** | Flags domain terms not in seed context — auto-discovers terminology |
| **Cost tracking** | Per-operation cost estimates including wasted retry tokens |
| **LLM call tracing** | Every prompt/response saved to SQLite — full audit trail |

## Architecture

```
Documents + Seed Context
        |
    Phase 1: Extraction (LLM reads docs, extracts typed entities)
        |
    Dedup: Merge ambiguous entities (LLM judges)
        |
    Entity KB (markdown files with YAML frontmatter)
        |
    ┌───────────────────────────────────┐
    |  Domain-Aware Retrieval (DAR)     |
    |  Stage 0: Intent classification   |
    |  Stage 1: Vector+Keyword+Graph    |
    |  Stage 2: RRF Fusion              |
    |  Stage 3: Confidence scoring      |
    |  Stage 4: 5-layer dedup           |
    |  Stage 5: Context building        |
    |  Stage 6: LLM synthesis           |
    |  Stage 7: Gap detection           |
    └───────────────────────────────────┘
        |
    Evals (4 question sources) → Coverage Report
        |
    Gaps → Curation → Re-eval → Improvement
```

## Meta-Model

18 entity types organized in 6 knowledge layers:

| Layer | Types | Question it answers |
|---|---|---|
| **Structural** | system, software-component, api, data-model, data-product, platform | What exists? |
| **Behavioral** | process, business-event, domain-logic | How does it work? |
| **Reference** | reference-data | What are the allowed values? |
| **Organizational** | team, persona, capability, offering, external-party | Who is involved? |
| **Language** | jargon-business, jargon-tech | What do terms mean? |
| **Decision** | decision | Why was this chosen? |

55 typed relationship types connect entities across layers.

## Configuration

### Persona Templates
Customize eval personas by editing `context_blocks/config/persona-templates.yaml`:

```yaml
personas:
  developer:
    label: Developer Onboarding
    description: What a new developer needs before their first ticket
    checks:
      - "API documentation for each system mentioned"
      - "Source code repository locations"
      - "Deployment and release process"
```

### Meta-Model
Entity types and knowledge layers for the viewer are defined in `viewer/src/config/meta-model.yaml`. The extraction pipeline uses `context_blocks/meta_model.py` as its source of truth. Both must stay in sync when adding custom types.

## Cost

| Operation | Typical cost |
|---|---|
| Extract 50 docs | ~$7 |
| Eval 30 questions | ~$0.60 |
| Dedup 400 entities | ~$0.05 |
| Single Ask query | ~$0.02 |

## Research

Built on the Demand-Driven Context (DDC) methodology.

- **arXiv paper**: [arxiv.org/abs/2603.14057](https://arxiv.org/abs/2603.14057)
- **Conference**: CreateWith London 2026

## License

MIT
