# Contributing to Context Blocks

## Getting Started

```bash
git clone https://github.com/ea-toolkit/context-blocks.git
cd context-blocks
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
# Fill in LLM_API_KEY and OPENAI_API_KEY in .env
```

## Code Conventions

- Python 3.11+ with type hints on all function signatures
- Pydantic for validation at system boundaries
- Conventional commits (`feat:`, `fix:`, `chore:`, `docs:`)
- One concern per PR

## Branch Naming

- `feat/<issue-number>-<short-description>`
- `fix/<issue-number>-<short-description>`
- `chore/<description>`

## PR Process

1. Create an issue first (or pick an existing one)
2. Create a branch from `main`
3. Implement, test, commit
4. Open PR referencing the issue (`Closes #N`)
5. Wait for review

## Running Tests

```bash
pytest
```

## Project Structure

```
context_blocks/       Python package
  cli.py              CLI entry point (Typer)
  config.py           Settings (pydantic-settings)
  pipeline.py         Extraction pipeline
  meta_model.py       Entity types, layers, relationships
  retrieval/          DAR retrieval pipeline
  infrastructure/     LLM gateway, embeddings
  prompts/            LLM prompt templates
  tasks/              Pipeline task implementations
viewer/               Astro + React web UI
synthetic-domains/    Demo data (healthcare-claims)
templates/            Seed context templates
tests/                pytest test suite
```
