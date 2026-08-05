# Python Standards for Context Blocks

## Code Style
- Python 3.11+ minimum
- Ruff for formatting and linting (line length 100)
- Type hints on ALL function signatures (parameters and return types)
- Docstrings on public functions (Google style: Args, Returns, Raises)

## Async
- All I/O operations MUST be async (file reads, API calls, network)
- Use `asyncio.gather` for parallel independent operations
- Never use synchronous `requests` — use `aiohttp` or `httpx`

## Data Validation
- Pydantic models for ALL data crossing boundaries (LLM responses, file parsing, config)
- Instructor for LLM structured output — never parse free text
- Enums for fixed sets (entity types, quality states)

## Error Handling
- Custom exceptions inheriting from `ContextBlocksError` base
- Never bare `except Exception` — catch specific exceptions
- Log errors with structlog before re-raising
- If one document fails processing, log and continue to next

## Imports
- Standard library first, then third-party, then local
- Absolute imports within the package (`from context_blocks.models.entity import ...`)
- No circular imports — if needed, restructure

## Testing
- Every new task MUST have a unit test
- Mock LLM calls in unit tests — don't hit real APIs
- Use pytest fixtures for shared test data
- Test file naming: `test_<module_name>.py`
