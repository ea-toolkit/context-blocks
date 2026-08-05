---
globs: ["context_blocks/**/*.py"]
---

# Pipeline Conventions — Context Blocks Extraction

Apply when writing or modifying Python code in `context_blocks/`.

## LLM Gateway
- Anthropic: always streaming (no Instructor, no tool-use)
- Gemini: native JSON schema via response_mime_type + response_schema
- Other providers: Instructor via litellm as fallback
- Always include JSON schema in prompt (dynamic from Pydantic model, never hardcoded)
- System prompt carries stable content (instructions + seed + meta-model) for caching

## Retry Policy
- Only retry on retryable errors (503, 429, timeout, connection errors)
- Code bugs (AttributeError, TypeError, KeyError) → fail immediately, never retry
- Smart retry: send broken JSON + errors only (~5K tokens), never re-send full prompt for schema issues
- Max retries: 1 for streaming, 2 for Gemini (due to 503 rate limiting)
- Every failed call logs wasted tokens and estimated cost

## Validation
- ValidationError must be caught BEFORE ValueError (Pydantic v2 inheritance)
- Per-entity validation: salvage valid entities when some fail
- Salvaged entities get `needs-review` tag
- Raw extraction JSON always saved to output/extractions/ regardless of validation outcome

## Normalization
- `_normalize_extraction_json()` handles field name mismatches as a safety net
- The JSON schema in the prompt should prevent most mismatches
- Add new normalization rules only when a pattern appears across 3+ docs
- Non-dict entities in JSON arrays → filter out with warning log

## Prompt Caching
- Anthropic: system prompt as text block with cache_control ephemeral
- Gemini: implicit caching (automatic when system prompt prefix is stable)
- Stable content (instructions + seed + meta-model) goes in system parameter
- Dynamic content (summary + entity tree + document) goes in user message

## Cost Awareness
- Log input/output tokens on every call
- Log cache hit metrics (cache_read_input_tokens, cached_content_token_count)
- Circuit breaker: 3 consecutive failures → abort run
- Save raw JSON before validation — never re-run LLM for format changes
