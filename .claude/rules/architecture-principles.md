# Architecture Principles

These are non-negotiable. Every code decision should be checked against these.

## 1. Zero Infrastructure for v1
No graph database. No vector store. No Docker required.
Input: folder of files + seed context. Output: folder of entity files + reports.
If a feature requires infrastructure setup, it's v2 not v1.

## 2. Sequential Reading, Not Chunking
Documents are read one at a time. Each document benefits from accumulated context.
This is NOT chunk-and-process-independently. Order and accumulation matter.

## 3. The Meta-Model is Sacred
All entities must map to one of the 17 types. If something doesn't fit, that's a signal
to discuss with the team — not to create an "other" bucket.
`context_blocks/meta_model.py` is the single source of truth.

## 4. Structured Output Only
Every LLM response must be validated against a Pydantic model via Instructor.
Free-text responses are never acceptable for entity extraction.

## 5. Seed Context in Every Prompt
The seed context is permanent background. It appears in every LLM call.
A document should never be analyzed without the seed context framing it.

## 6. Provider Agnostic
Never import anthropic directly. Always go through the LLM gateway.
A user should be able to switch from Claude to GPT with a .env change only.

## 7. Fail Gracefully, Continue Processing
If document 37 of 100 fails to parse, log the error and move to document 38.
Never crash the entire pipeline because of one bad file.

## 8. Output is Git-Native
Entity files are markdown. Reports are markdown. Everything is diffable,
version-controllable, and human-readable without special tools.
