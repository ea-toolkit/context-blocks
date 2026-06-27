# Context Blocks — Architecture Notes

## Current Architecture (v1): Simple Python + Claude API

Direct API calls, sequential document processing, state managed in files.
Chosen for speed of iteration — prove the prompts work before adding infrastructure.

## Future Architecture: Deep Agents (LangChain deepagents or equivalent)

When the core prompts and pipeline are proven, migrate to deep agent architecture for:

- **Planning tools** — agent creates a reading plan after first-pass scan, tracks progress
- **Sub-agent delegation** — separate agents for: document scanning, entity extraction, relationship mapping, gap analysis
- **Context isolation** — each sub-agent gets its own context window, only results bubble up to orchestrator
- **Persistent memory** — accumulated domain understanding persists across sessions, not just within one run
- **Virtual file system** — agent reads/writes entity files directly

### Why not now:
- Core prompt quality is the bottleneck, not orchestration
- Adding LangGraph/deepagents before prompts are tuned = infrastructure without results
- Risk: 2 weeks on plumbing, mediocre output because prompts aren't right

### When to migrate:
- After Phase 1 + Phase 2 work end-to-end on a real enterprise domain
- After we've calibrated the prompts on at least 2 domains
- When we need: parallel processing, multi-session persistence, or error recovery at scale

### Reference:
- LangChain deepagents: pip install deepagents (MIT licensed, model-agnostic)
- Built on LangGraph state machines
- Inspired by Claude Code and Manus internal architecture
- Four pillars: planning, sub-agent delegation, persistent memory, detailed system prompts
