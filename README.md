<div align="center">

# Context Blocks

**Turn your docs into a domain knowledge base. Then find what's missing.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**18 entity types · 6 knowledge layers · 55 relationship types · gap detection built in**

</div>

---

## What is Context Blocks?

Context Blocks reads your company's documentation and builds a typed, structured knowledge base — systems, processes, teams, APIs, business rules, jargon, decisions. Then it evaluates that knowledge base from multiple perspectives (developer, architect, product owner, new joiner) and tells you exactly where the gaps are.

Every other tool in this space extracts what's there. Context Blocks measures what's *not* there.

**The gap is the product.** Every unanswered question becomes a curation target.

Outputs [OKF-compatible](https://github.com/google/open-knowledge-format) knowledge bases — directories of Markdown files with YAML frontmatter that any agent, Obsidian vault, or LLM can read directly. No vendor lock-in, no proprietary format.

## How it works

```
 Documents + Seed Context
          │
          ▼
 ┌─────────────────────┐
 │   Extract (Phase 1)  │  LLM reads docs → typed entities with
 │                      │  confidence scores, relationships,
 │                      │  source provenance, open questions
 └──────────┬───────────┘
            │
            ▼
 ┌─────────────────────┐
 │   Dedup              │  LLM-judged duplicate merging
 └──────────┬───────────┘
            │
            ▼
 ┌─────────────────────┐
 │   Entity KB          │  Markdown files + YAML frontmatter
 │   (18 types,         │  Human-readable AND machine-parseable
 │    6 layers)         │
 └──────────┬───────────┘
            │
     ┌──────┴──────┐
     ▼             ▼
 ┌────────┐   ┌─────────┐
 │  Ask   │   │  Eval   │  4 question sources × persona views
 │  (DAR) │   │         │  → coverage scores
 └────┬───┘   └────┬────┘
      │            │
      ▼            ▼
 ┌─────────────────────┐
 │   Gaps               │  CLEAN · INCOMPLETE · MISSING
 │                      │  Every gap = a curation target
 └──────────┬───────────┘
            │
            ▼
 ┌─────────────────────┐
 │   Curate → Re-eval  │  Coverage improves each cycle
 └─────────────────────┘
```

## What makes this different

| | Context Blocks | Typical knowledge tools |
|---|---|---|
| **Gap detection** | Scores every question as CLEAN / INCOMPLETE / MISSING | Extract what's there, hope it's enough |
| **Typed ontology** | 18 entity types constrained by a meta-model | Freeform nodes or generic "entity" |
| **Persona evaluation** | "60% complete for a developer, 20% for an architect" | No evaluation at all |
| **Knowledge layers** | Structural · Behavioral · Reference · Organizational · Language · Decision | Flat graph |
| **Research-backed** | Built on DDC methodology with published empirical findings | No theoretical foundation |

## Quick Start

```bash
pip install context-blocks
```

```bash
export LLM_API_KEY=your-anthropic-key       # Required
export OPENAI_API_KEY=your-openai-key       # Optional (embeddings; falls back to local)
```

```bash
cb init my-domain --seed seed.md            # Create a context block
cb phase1 ./docs --seed seed.md -b my-domain # Extract entities
cb dedup -b my-domain                       # Merge duplicates
cb eval -b my-domain --seed seed.md --personas # Evaluate coverage
```

## Try the Demo

A synthetic healthcare claims domain ships with 410 pre-extracted entities — no API keys needed:

```bash
cd viewer && npm install && npm run dev
# Open http://localhost:4321 — browse entities, layers, gaps, and graph
```

Or run the full pipeline yourself:

```bash
cb phase1 synthetic-domains/healthcare-claims/docs \
  --seed synthetic-domains/healthcare-claims/seed-context.md \
  --output synthetic-domains/healthcare-claims/output
```

## Features

### Context Blocks (Bounded Contexts)

Organize knowledge into scoped blocks — one per domain, team, or product area:

```bash
cb init payments --seed payments-seed.md
cb init identity --seed identity-seed.md

cb phase1 ./docs --seed seed.md --block payments
cb eval --block payments --seed seed.md --personas

# Or set a default
export CB_BLOCK=payments
```

### Evaluate

Generate questions from four sources, measure how well the KB answers them:

| Source | What it tests |
|---|---|
| Seed context | Can the KB flesh out what the onboarding doc promises? |
| Source docs | Did extraction capture what's in the original documents? |
| Persona templates | Does a developer / architect / PO / new joiner have what they need? |
| Work items (DDC) | Can the KB help resolve real tickets and incidents? |

### Retrieve (DAR Pipeline)

Ask questions against your KB with Domain-Aware Retrieval:

- Typed intent classification — knows if you're asking about a process, system, or relationship
- Parallel search — vector + keyword + typed graph traversal
- Confidence-weighted RRF fusion with layer priority boosts
- Full retrieval traces — see exactly which entities contributed and why

### Export

```bash
# Obsidian vault — wikilinks, Map of Content, organized by type
cb export-obsidian --block my-domain

# Single markdown for AI agent context windows
cb export-skill --block my-domain --title "My Domain KB"

# With token budget
cb export-skill --block my-domain --max-tokens 10000
```

## MCP Server (Agent Integration)

Let AI agents query your KB directly via the [Model Context Protocol](https://modelcontextprotocol.io):

```bash
pip install 'context-blocks[mcp]'
cb mcp                                  # stdio (Claude Desktop, local CLI)
cb mcp --transport streamable-http      # HTTP (Copilot, remote agents, web tools)
cb mcp --block my-domain                # serve a single block
```

**6 tools exposed:** `list_blocks`, `get_overview`, `search_entities`, `get_entity`, `ask_kb`, `get_gap_report`

Block-aware: agents call `list_blocks()` first to discover available domains, then pass the block name to any tool. Single-block projects work automatically without specifying.

Configure via env vars or CLI flags:

| Setting | Env var | CLI flag | Default |
|---|---|---|---|
| Transport | `CB_MCP_TRANSPORT` | `--transport` | `stdio` |
| Host | `CB_MCP_HOST` | `--host` | `127.0.0.1` |
| Port | `CB_MCP_PORT` | `--port` | `8000` |

**Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "context-blocks": {
      "command": "cb",
      "args": ["mcp"]
    }
  }
}
```

**Remote agents** (Copilot, web tools):

```bash
cb mcp --transport streamable-http --host 0.0.0.0 --port 8080
# or
export CB_MCP_TRANSPORT=streamable-http
export CB_MCP_HOST=0.0.0.0
export CB_MCP_PORT=8080
cb mcp
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

## Under the Hood

Capabilities you get without configuring anything:

| Capability | What it does |
|---|---|
| Prompt caching | Anthropic `cache_control` on system prompts — reduces cost on repeated calls |
| Crash-safe resume | Pipeline state saved per-document with file hashes — resume after crash without re-processing |
| 3-tier repair ladder | Parse JSON → smart retry (broken JSON only, ~5K tokens) → full retry — maximizes entity salvage |
| Per-entity validation | Valid entities saved even when some fail — no all-or-nothing batches |
| Dual embedding providers | OpenAI API if key present, local Fastembed (BAAI/bge-small-en-v1.5) as fallback — works offline |
| Relationship-aware embeddings | Entity relationships included in embedding text — improves "what connects to X" queries |
| Post-extraction dedup | LLM-judged duplicate detection with Jaccard similarity pre-filter |
| Hedged statement detection | Extracts uncertain statements as open questions — surfaces gaps at extraction time |
| New jargon detection | Flags domain terms not in seed context — auto-discovers terminology |
| Cost tracking | Per-operation cost estimates including wasted retry tokens |
| LLM call tracing | Every prompt/response saved to SQLite — full audit trail |

## CLI Reference

| Command | Description |
|---|---|
| `cb init <name>` | Initialize a new context block |
| `cb blocks` | List all context blocks |
| `cb phase1` | Extract entities from documents |
| `cb dedup` | Merge duplicate entities |
| `cb eval` | Run coverage evaluation |
| `cb eval --personas` | Include persona-driven completeness checks |
| `cb eval --work-items <dir>` | Include real work items (DDC mode) |
| `cb ask "question"` | Ask a question from the terminal |
| `cb serve` | Start the API server for the viewer |
| `cb reformat` | Regenerate entity markdown from JSON (no API) |
| `cb export-obsidian` | Export as Obsidian vault with wikilinks |
| `cb export-skill` | Export as single markdown for agent context |
| `cb mcp` | Start MCP server for AI agent integration (stdio) |

All commands accept `--block <name>` or `-b`. Set `CB_BLOCK` env var as default.

## Viewer

Web UI with 8 pages (requires Node >= 18):

**Ask** — question input with grounded answers and retrieval traces
**Digest** — domain overview, knowledge layers, top questions
**Explorer** — browse entities by type with detail panel
**Map** — interactive entity relationship graph
**Workbench** — coverage, questions, health checks, review queue
**Evals** — run explorer with KPI strip and breakdowns
**Glossary** — searchable domain terminology
**Gaps** — coverage summary with actionable gap cards

```bash
cb serve --block my-domain    # API server (terminal 1)
cd viewer && npm run dev      # Viewer (terminal 2)
```

## Cost

| Operation | Typical cost |
|---|---|
| Extract 50 docs | ~$7 |
| Eval 30 questions | ~$0.60 |
| Dedup 400 entities | ~$0.05 |
| Single Ask query | ~$0.02 |

## Input Formats

| Format | Extension | Install |
|---|---|---|
| Markdown | `.md` | Built-in |
| Plain text | `.txt` | Built-in |
| HTML | `.html`, `.htm` | Built-in |
| PDF | `.pdf` | `pip install 'context-blocks[pdf]'` |
| Word | `.docx` | `pip install 'context-blocks[docx]'` |
| PowerPoint | `.pptx` | `pip install 'context-blocks[pptx]'` |

Or install everything: `pip install 'context-blocks[all]'`

Confluence exports (HTML) and Notion exports (Markdown) work out of the box.

## Configuration

Customize eval personas in `context_blocks/config/persona-templates.yaml`. Entity types and knowledge layers are defined in `viewer/src/config/meta-model.yaml` (viewer) and `context_blocks/meta_model.py` (extraction pipeline).

## Research

Built on the Demand-Driven Context (DDC) methodology.

- **Paper**: [arxiv.org/abs/2603.14057](https://arxiv.org/abs/2603.14057)
- **Conference**: CreateWith London 2026

## License

MIT
