"""LLM Gateway — provider-agnostic interface for all LLM calls.

Single interface: extract_structured(prompt, ResponseModel)
Auto-selects strategy based on provider:

- anthropic: Direct SDK streaming + JSON parse + Pydantic validation (all prompt sizes)
- others: Instructor + litellm (fallback for local/unknown providers)

Repair ladder on validation failure:
1. Stream response → extract JSON → normalize fields → validate with Pydantic
2. On failure: smart retry (send broken JSON + errors only, ~5K tokens instead of full prompt)
3. If smart retry fails: full retry (re-send entire prompt)
"""

import json
import re
import time
from typing import TypeVar

import httpx
import instructor
import structlog
from pydantic import BaseModel, ValidationError

from context_blocks.config import get_settings
from context_blocks.exceptions import LLMError
from context_blocks.infrastructure.llm.token_utils import estimate_tokens
from context_blocks.infrastructure.llm.trace import save_trace

logger = structlog.get_logger(__name__)

T = TypeVar("T", bound=BaseModel)

# Model ID mapping — config short names to Anthropic API model IDs.
# Short names (e.g. "claude-sonnet-4-6") are accepted directly by the API,
# so this map only exists for explicit dated-version pinning.
ANTHROPIC_MODEL_MAP: dict[str, str] = {}


def _get_anthropic_model_id(model: str) -> str:
    """Convert a config-style model name to Anthropic's direct API model ID."""
    return ANTHROPIC_MODEL_MAP.get(model, model)


def _get_anthropic_client():
    """Get a direct Anthropic client with proper timeout configuration."""
    import anthropic

    settings = get_settings()
    http_client = httpx.Client(
        timeout=httpx.Timeout(
            timeout=settings.llm_request_timeout,
            connect=settings.llm_connect_timeout,
            read=settings.llm_request_timeout,
            write=30.0,
        )
    )
    return anthropic.Anthropic(api_key=settings.llm_api_key, http_client=http_client)


def _get_instructor_client() -> tuple[instructor.Instructor, str]:
    """Get an Instructor client for non-Anthropic providers.

    Returns (client, model_string).
    """
    settings = get_settings()
    provider = settings.llm_provider
    model = settings.llm_model

    import litellm

    litellm.api_key = settings.llm_api_key
    litellm.request_timeout = int(settings.llm_request_timeout)
    client = instructor.from_litellm(litellm.completion)

    if provider == "openai":
        return client, model
    return client, f"{provider}/{model}"


def _get_gemini_client():
    """Get a Google GenAI client for Gemini models."""
    from google import genai

    settings = get_settings()
    api_key = settings.google_api_key or settings.llm_api_key
    return genai.Client(api_key=api_key)


# Gemini model ID mapping
GEMINI_MODEL_MAP = {
    "gemini-2.5-flash": "gemini-2.5-flash",
    "gemini-2.5-pro": "gemini-2.5-pro",
    "gemini-flash": "gemini-2.5-flash",
}


def _get_gemini_model_id(model: str) -> str:
    """Convert a config-style model name to Gemini's model ID."""
    return GEMINI_MODEL_MAP.get(model, model)


def _select_strategy() -> str:
    """Select extraction strategy based on provider.

    - Anthropic: streaming text + JSON parse + Pydantic validation
    - Gemini: streaming with native JSON schema (constrained decoding, zero retries)
    - Others: Instructor via litellm (safety net for JSON compliance)
    """
    settings = get_settings()

    if settings.llm_provider == "anthropic":
        return "streaming"

    if settings.llm_provider == "gemini":
        return "gemini"

    return "instructor"


def _get_retryable_api_errors() -> tuple:
    """Get provider-specific API error types that are worth retrying."""
    errors = []
    try:
        import anthropic
        errors.extend([
            anthropic.APIConnectionError,
            anthropic.APITimeoutError,
            anthropic.InternalServerError,
            anthropic.RateLimitError,
        ])
    except ImportError:
        pass
    return tuple(errors) if errors else (type(None),)  # empty tuple that never matches


def _extract_json_from_text(text: str) -> dict:
    """Extract and parse JSON from LLM text response.

    Handles: raw JSON, markdown-fenced JSON, JSON with surrounding text.
    """
    # Try direct parse first
    text = text.strip()
    if text.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

    # Try markdown code fence
    fenced = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Find the outermost JSON object
    json_start = text.find("{")
    json_end = text.rfind("}") + 1
    if json_start >= 0 and json_end > json_start:
        try:
            return json.loads(text[json_start:json_end])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"No valid JSON found in response ({len(text)} chars)")


def _normalize_extraction_json(data: dict) -> dict:
    """Normalize LLM JSON output to match our Pydantic model field names.

    The LLM sometimes uses slightly different field names than our model expects.
    This maps common variations to the correct names.
    """
    # Normalize top-level fields
    if "summary" in data and "document_summary" not in data:
        data["document_summary"] = data.pop("summary")
    if "source" in data and "source_document" not in data:
        data["source_document"] = data.pop("source")

    # Normalize entities — skip any non-dict entries (LLM sometimes returns strings)
    raw_entities = data.get("entities", [])
    non_dict = [e for e in raw_entities if not isinstance(e, dict)]
    if non_dict:
        logger.warning(
            "non_dict_entities_dropped",
            count=len(non_dict),
            sample=str(non_dict[0])[:100],
        )
    data["entities"] = [e for e in raw_entities if isinstance(e, dict)]
    for entity in data["entities"]:
        # "type" → "entity_type"
        if "type" in entity and "entity_type" not in entity:
            entity["entity_type"] = entity.pop("type")

        # Ensure "description" exists — LLM frequently omits it
        if "description" not in entity:
            overview = entity.get("overview", "")
            if overview:
                # Use first sentence of overview as description
                first_sentence = overview.split(".")[0].strip()
                entity["description"] = first_sentence[:200]
            else:
                entity["description"] = entity.get("name", "No description")

        # Normalize relationships
        for rel in entity.get("relationships", []):
            if "type" in rel and "relationship_type" not in rel:
                rel["relationship_type"] = rel.pop("type")
            if "target" in rel and "target_entity_id" not in rel:
                rel["target_entity_id"] = rel.pop("target")
            if "target_id" in rel and "target_entity_id" not in rel:
                rel["target_entity_id"] = rel.pop("target_id")
            if "target_name" in rel and "target_entity_name" not in rel:
                rel["target_entity_name"] = rel.pop("target_name")
            # Ensure target_entity_name exists (LLM sometimes omits it)
            if "target_entity_name" not in rel:
                rel["target_entity_name"] = rel.get("target_entity_id", "")
            # Ensure reasoning exists (LLM sometimes uses 'description' instead)
            if "reasoning" not in rel:
                rel["reasoning"] = rel.pop("description", "")

    # Normalize decision_log
    # Normalize decision_log — skip non-dict entries
    data["decision_log"] = [d for d in data.get("decision_log", []) if isinstance(d, dict)]
    for decision in data["decision_log"]:
        if "subject" not in decision:
            # LLM uses various field names for the subject
            for alt in ("topic", "entity_id", "entity", "name", "concept"):
                if alt in decision:
                    decision["subject"] = decision.pop(alt)
                    break
            if "subject" not in decision:
                decision["subject"] = "unknown"
        if "decision" not in decision:
            for alt in ("entity_type", "classification", "action"):
                if alt in decision:
                    decision["decision"] = decision.pop(alt)
                    break
            if "decision" not in decision:
                decision["decision"] = ""
        if "reasoning" not in decision:
            for alt in ("reason", "explanation", "rationale"):
                if alt in decision:
                    decision["reasoning"] = decision.pop(alt)
                    break
            if "reasoning" not in decision:
                decision["reasoning"] = ""

    return data


def _build_json_instruction(response_model: type[BaseModel]) -> str:
    """Build a JSON schema instruction dynamically from the Pydantic model.

    Generates a sample JSON structure showing exact field names, types, and
    which fields are required. Works for any response model (DocumentExtractionResult,
    KnowledgeSummary, etc.) — no hardcoded schemas.
    """
    schema_example = _generate_schema_example(response_model)

    # Add entity-specific field name warnings for DocumentExtractionResult
    extra_rules = ""
    from context_blocks.models.entity import DocumentExtractionResult
    if response_model is DocumentExtractionResult:
        extra_rules = """
CRITICAL field name rules:
- Entity type field is "entity_type", NOT "type"
- Relationship target is "target_entity_id", NOT "target_id" or "target"
- Relationship type is "relationship_type", NOT "type"
- "description" is REQUIRED on every entity (one-line summary, separate from overview)
- "reasoning" is REQUIRED on every entity (why this type classification)
"""

    return f"""

IMPORTANT: Return your ENTIRE response as a single valid JSON object matching this EXACT schema.
Use these EXACT field names — do not rename, abbreviate, or skip any required field.

```json
{schema_example}
```
{extra_rules}
Return ONLY the JSON object. No markdown code fences, no explanation before or after."""


def _generate_schema_example(model: type[BaseModel], indent: int = 0) -> str:
    """Generate a sample JSON structure from a Pydantic model, showing field names and types."""
    lines = ["{"]
    fields = model.model_fields
    field_items = list(fields.items())

    for i, (name, field_info) in enumerate(field_items):
        comma = "," if i < len(field_items) - 1 else ""
        required = "REQUIRED" if field_info.is_required() else "optional"
        desc = field_info.description or ""
        # Truncate long descriptions
        if len(desc) > 80:
            desc = desc[:77] + "..."

        annotation = field_info.annotation
        sample = _get_sample_value(name, annotation, indent + 2)
        pad = "  " * (indent + 1)
        lines.append(f'{pad}"{name}": {sample}{comma}  // {required}. {desc}')

    lines.append("  " * indent + "}")
    return "\n".join(lines)


def _get_sample_value(name: str, annotation, indent: int) -> str:
    """Get a sample JSON value for a field based on its type."""
    import typing

    origin = getattr(annotation, "__origin__", None)

    # Handle Optional types
    if origin is typing.Union:
        args = [a for a in annotation.__args__ if a is not type(None)]
        if args:
            return _get_sample_value(name, args[0], indent)

    # Handle list types
    if origin is list:
        inner = annotation.__args__[0] if annotation.__args__ else str
        if isinstance(inner, type) and issubclass(inner, BaseModel):
            inner_example = _generate_schema_example(inner, indent)
            return f"[\n{'  ' * indent}{inner_example}\n{'  ' * (indent - 1)}]"
        elif inner is str:
            return '["example"]'
        else:
            return "[]"

    # Handle dict types
    if origin is dict:
        return '{"key": "value"}'

    # Handle nested Pydantic models
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return _generate_schema_example(annotation, indent)

    # Handle enums
    if isinstance(annotation, type):
        try:
            import enum
            if issubclass(annotation, enum.Enum):
                values = [e.value for e in annotation][:5]
                return f'"{values[0]}"'
        except TypeError:
            pass

    # Primitives
    if annotation is str or annotation == str:
        return f'"..."'
    if annotation is int or annotation == int:
        return "0"
    if annotation is float or annotation == float:
        return "0.0"
    if annotation is bool or annotation == bool:
        return "true"

    return '"..."'


def _build_smart_retry_prompt(broken_json: str, errors: str, response_model: type[BaseModel]) -> str:
    """Build a lightweight retry prompt with just the broken JSON and errors.

    This is much cheaper than re-sending the full prompt (~5K tokens vs ~13K).
    The LLM doesn't need the original document to fix structural/schema errors.
    """
    # Extract valid enum values from the model for reference
    enum_hints = _get_enum_hints(response_model)

    return f"""Your previous JSON output had validation errors. Fix ONLY the errors below.
Do not add or remove entities. Do not change content that is already valid.

## Your output (with errors):
{broken_json}

## Validation errors:
{errors}

{enum_hints}

Return the corrected JSON. Return ONLY the JSON object, no explanation."""


def _get_enum_hints(response_model: type[BaseModel]) -> str:
    """Valid entity_type values for the retry prompt — the active/custom ontology's types, or the default."""
    hints = []

    try:
        from context_blocks.meta_model import EntityType
        from context_blocks.ontology import get_active_ontology

        ont = get_active_ontology()
        entity_types = sorted(ont.types) if ont is not None else [e.value for e in EntityType]
        hints.append(f"## Valid entity_type values:\n{', '.join(entity_types)}")
    except ImportError:
        pass

    return "\n\n".join(hints)


async def extract_structured(
    prompt: str,
    response_model: type[T],
    system_prompt: str | None = None,
    temperature: float = 0.0,
    max_retries: int = 1,
    task_name: str = "unknown",
    document_name: str | None = None,
) -> T:
    """Extract structured output from an LLM call.

    Strategy:
    - Anthropic: streaming text + JSON parse + Pydantic validation (all prompts)
    - Others: Instructor via litellm (safety net for JSON compliance)

    On validation failure, attempts a smart retry (JSON + errors only)
    before falling back to a full retry.

    All calls are traced to SQLite for debugging and replay.
    """
    settings = get_settings()
    prompt_tokens = estimate_tokens(prompt + (system_prompt or ""))
    strategy = _select_strategy()

    model = settings.llm_model
    if settings.llm_provider == "anthropic":
        model = _get_anthropic_model_id(model)
    elif settings.llm_provider == "gemini":
        model = _get_gemini_model_id(model)

    start_time = time.time()

    logger.info(
        "llm_call_start",
        model=model,
        response_model=response_model.__name__,
        prompt_tokens_est=prompt_tokens,
        task=task_name,
        document=document_name,
        strategy=strategy,
    )

    try:
        if strategy == "streaming":
            response = await _extract_streaming(
                prompt, response_model, system_prompt, model, max_retries
            )
        elif strategy == "gemini":
            response = await _extract_gemini(
                prompt, response_model, system_prompt, model
            )
        else:
            response = await _extract_instructor(
                prompt, response_model, system_prompt, temperature, max_retries, model
            )

        duration_ms = int((time.time() - start_time) * 1000)
        response_json = response.model_dump_json()
        response_tokens = estimate_tokens(response_json)

        logger.info(
            "llm_call_complete",
            model=model,
            response_model=response_model.__name__,
            duration_ms=duration_ms,
            response_tokens_est=response_tokens,
            strategy=strategy,
        )

        save_trace(
            task=task_name,
            document=document_name,
            model=model,
            system_prompt=system_prompt,
            user_prompt=prompt,
            response_raw=response_json,
            response_model=response_model.__name__,
            prompt_tokens_est=prompt_tokens,
            response_tokens_est=response_tokens,
            duration_ms=duration_ms,
            status="success",
        )

        return response

    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)

        # Estimate wasted cost (Sonnet: $3/M input, $15/M output)
        wasted_cost = (prompt_tokens / 1_000_000) * 3.0

        logger.error(
            "llm_call_failed",
            model=model,
            error=str(e)[:500],
            duration_ms=duration_ms,
            strategy=strategy,
            prompt_tokens_wasted=prompt_tokens,
            estimated_cost_wasted=f"${wasted_cost:.4f}",
        )

        save_trace(
            task=task_name,
            document=document_name,
            model=model,
            system_prompt=system_prompt,
            user_prompt=prompt,
            response_raw=None,
            response_model=response_model.__name__,
            prompt_tokens_est=prompt_tokens,
            response_tokens_est=0,
            duration_ms=duration_ms,
            status="error",
            error=str(e)[:1000],
        )

        raise LLMError(f"LLM call failed: {e}") from e


async def _extract_instructor(
    prompt: str,
    response_model: type[T],
    system_prompt: str | None,
    temperature: float,
    max_retries: int,
    model: str,
) -> T:
    """Non-Anthropic path: use Instructor via litellm for structured output."""
    client, model_str = _get_instructor_client()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    return client.chat.completions.create(
        model=model_str,
        messages=messages,
        response_model=response_model,
        temperature=temperature,
        max_retries=max_retries,
    )


async def _extract_gemini(
    prompt: str,
    response_model: type[T],
    system_prompt: str | None,
    model: str,
    max_retries: int = 2,
) -> T:
    """Gemini path: streaming with native JSON schema (constrained decoding).

    Uses response_mime_type + response_schema for guaranteed valid JSON.
    Retries on transient errors (503 rate limiting, connection issues).
    Implicit caching activates automatically when system_prompt prefix is stable.
    """
    import asyncio
    from google.genai import types

    client = _get_gemini_client()

    config = types.GenerateContentConfig(
        max_output_tokens=65536,  # Flash supports up to 65K output
        response_mime_type="application/json",
        response_schema=response_model,
    )
    if system_prompt:
        config.system_instruction = system_prompt

    last_error = None
    for attempt in range(1, max_retries + 2):
        try:
            full_text = ""
            final_usage = None

            async for chunk in await client.aio.models.generate_content_stream(
                model=model,
                contents=prompt,
                config=config,
            ):
                if chunk.text:
                    full_text += chunk.text
                if chunk.usage_metadata:
                    final_usage = chunk.usage_metadata

            # Log cache and token metrics
            cached_tokens = 0
            input_tokens = 0
            output_tokens = 0
            if final_usage:
                cached_tokens = getattr(final_usage, "cached_content_token_count", 0) or 0
                input_tokens = getattr(final_usage, "prompt_token_count", 0) or 0
                output_tokens = getattr(final_usage, "candidates_token_count", 0) or 0

            logger.debug(
                "gemini_response_received",
                attempt=attempt,
                response_chars=len(full_text),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cached_tokens=cached_tokens,
                cache_hit=cached_tokens > 0,
            )

            # Parse — Gemini's constrained decoding should produce valid JSON
            result = response_model.model_validate_json(full_text)
            return result

        except Exception as e:
            last_error = e
            error_str = str(e)

            # Retry on transient errors (503, 429 rate limit, connection issues)
            if "503" in error_str or "429" in error_str or "UNAVAILABLE" in error_str or "overloaded" in error_str.lower():
                wait_secs = 5 * attempt  # 5s, 10s, 15s backoff
                logger.warning(
                    "gemini_transient_error",
                    attempt=attempt,
                    error=error_str[:200],
                    retry_in_secs=wait_secs,
                )
                await asyncio.sleep(wait_secs)
                continue

            # Non-transient error — fail immediately
            logger.error(
                "gemini_error",
                attempt=attempt,
                error_type=type(e).__name__,
                error=error_str[:200],
            )
            raise LLMError(f"Gemini extraction failed: {e}") from e

    raise LLMError(f"Gemini extraction failed after {max_retries + 1} attempts: {last_error}")


async def _extract_streaming(
    prompt: str,
    response_model: type[T],
    system_prompt: str | None,
    model: str,
    max_retries: int,
) -> T:
    """Anthropic path: streaming + JSON parse + Pydantic validation.

    Uses prompt caching: the system prompt is marked as cacheable so it's
    processed once and reused across sequential calls (90% discount on reads).

    Repair ladder:
    1. Stream response as plain text
    2. Extract JSON → normalize fields → validate with Pydantic
    3. On validation failure: per-entity salvage → smart retry → full retry
    """
    client = _get_anthropic_client()

    # Add JSON format instruction to the prompt
    json_prompt = prompt + _build_json_instruction(response_model)

    last_error = None
    for attempt in range(1, max_retries + 2):
        try:
            # Stream the response with prompt caching enabled
            create_kwargs = {
                "model": model,
                "max_tokens": 64000,
                "messages": [{"role": "user", "content": json_prompt}],
            }

            # Structure system prompt for caching:
            # Pass as a text block with cache_control so Anthropic caches the
            # KV state and skips prefill on subsequent calls (90% input discount).
            # Cache TTL resets on every hit — sequential pipeline keeps it alive.
            if system_prompt:
                create_kwargs["system"] = [
                    {
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"},
                    }
                ]

            with client.messages.stream(**create_kwargs) as stream:
                message = stream.get_final_message()

            # Guard against empty or non-text responses
            if not message.content or not hasattr(message.content[0], "text"):
                raise ValueError("Empty or non-text response from API")

            text = message.content[0].text

            # Log cache metrics
            usage = message.usage
            cache_created = getattr(usage, "cache_creation_input_tokens", 0) or 0
            cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0

            logger.debug(
                "streaming_response_received",
                attempt=attempt,
                response_chars=len(text),
                input_tokens=usage.input_tokens,
                output_tokens=usage.output_tokens,
                cache_created_tokens=cache_created,
                cache_read_tokens=cache_read,
            )

            # Repair ladder: extract JSON → normalize fields → validate with Pydantic
            raw_data = _extract_json_from_text(text)
            raw_data = _normalize_extraction_json(raw_data)
            result = response_model.model_validate(raw_data)
            return result

        except ValidationError as e:
            # MUST be caught before ValueError (ValidationError IS a ValueError in Pydantic v2)
            last_error = e
            error_count = e.error_count()
            logger.warning(
                "pydantic_validation_failed",
                attempt=attempt,
                error_count=error_count,
                first_errors=str(e)[:300],
            )

            # Try per-entity validation — salvage what we can
            partial = _validate_entities_individually(raw_data, response_model)
            if partial is not None:
                return partial

            # Smart retry: send parsed JSON (not raw LLM text) + errors
            # Only if we haven't exhausted attempts — smart retry is an extra API call
            if attempt <= max_retries:
                smart_result = await _smart_retry(
                    client, model, system_prompt,
                    json.dumps(raw_data, indent=2),  # clean JSON, not raw LLM text
                    e, response_model,
                )
                if smart_result is not None:
                    return smart_result

                logger.warning("smart_retry_failed", attempt=attempt)

            continue

        except (json.JSONDecodeError, ValueError) as e:
            # Actual JSON parse failures (not ValidationError — that's caught above)
            last_error = e
            logger.warning(
                "json_parse_failed",
                attempt=attempt,
                error=str(e)[:200],
            )
            # JSON was malformed — full retry (smart retry can't help here)
            continue

        except (ConnectionError, TimeoutError, OSError) as e:
            # Network/connection errors — worth retrying
            last_error = e
            logger.warning(
                "streaming_connection_error",
                attempt=attempt,
                error=str(e)[:200],
            )
            continue

        except _get_retryable_api_errors() as e:
            # Provider API errors (rate limit, server error, timeout)
            last_error = e
            logger.warning(
                "streaming_api_error",
                attempt=attempt,
                error_type=type(e).__name__,
                error=str(e)[:200],
            )
            continue

        except Exception as e:
            # Code bugs (AttributeError, TypeError, KeyError, etc.)
            # Retrying won't help — fail immediately to avoid wasting tokens
            logger.error(
                "streaming_code_error",
                attempt=attempt,
                error_type=type(e).__name__,
                error=str(e)[:200],
            )
            raise LLMError(f"Code error during extraction (not retryable): {e}") from e

    raise LLMError(
        f"Streaming extraction failed after {max_retries + 1} attempts: {last_error}"
    )


def _validate_entities_individually(raw_data: dict, response_model: type[T]) -> T | None:
    """Validate entities one-by-one, keeping valid ones and tagging invalid ones.

    If all entities fail, returns None (caller should try smart retry or full retry).
    If some pass, returns a result with valid entities + tagged partial entities.
    """
    from context_blocks.models.entity import ExtractedEntity, DocumentExtractionResult

    # Only applies to DocumentExtractionResult
    if response_model is not DocumentExtractionResult:
        return None

    entities_data = raw_data.get("entities", [])
    if not entities_data:
        return None

    valid_entities = []
    invalid_count = 0

    for i, entity_data in enumerate(entities_data):
        try:
            entity = ExtractedEntity.model_validate(entity_data)
            valid_entities.append(entity)
        except ValidationError as entity_error:
            invalid_count += 1
            # Try to salvage with 'needs-review' tag and relaxed validation
            salvaged = _try_salvage_entity(entity_data)
            if salvaged is not None:
                valid_entities.append(salvaged)
            else:
                logger.warning(
                    "entity_validation_failed",
                    entity_index=i,
                    entity_id=entity_data.get("id", "unknown"),
                    error=str(entity_error)[:200],
                )

    if not valid_entities:
        return None

    # Build a result with whatever we could salvage
    try:
        result = DocumentExtractionResult(
            source_document=raw_data.get("source_document", raw_data.get("source", "unknown")),
            document_summary=raw_data.get("document_summary", raw_data.get("summary", "")),
            entities=valid_entities,
            questions=raw_data.get("questions", []),
            new_jargon=raw_data.get("new_jargon", []),
            decision_log=[],  # skip decision log validation — not worth failing over
        )

        logger.info(
            "partial_validation_success",
            valid_entities=len(valid_entities),
            invalid_entities=invalid_count,
            total_entities=len(entities_data),
        )

        return result

    except Exception:
        return None


def _try_salvage_entity(entity_data: dict) -> "ExtractedEntity | None":
    """Try to fix common validation errors and salvage an entity.

    Applies relaxed defaults for non-critical fields.
    """
    from context_blocks.models.entity import ExtractedEntity

    # Fix common issues
    data = dict(entity_data)

    # Clamp confidence to valid range
    if "confidence" in data:
        try:
            conf = float(data["confidence"])
            data["confidence"] = max(0.0, min(1.0, conf))
        except (ValueError, TypeError):
            data["confidence"] = 0.5

    # Default missing non-critical fields
    data.setdefault("status", "active")
    data.setdefault("tags", [])
    data.setdefault("relationships", [])
    data.setdefault("hedged_statements", [])
    data.setdefault("reasoning", "")
    data.setdefault("overview", data.get("description", ""))
    data.setdefault("details", "")

    # Add needs-review tag
    if "needs-review" not in data.get("tags", []):
        data.setdefault("tags", [])
        data["tags"].append("needs-review")

    try:
        return ExtractedEntity.model_validate(data)
    except ValidationError:
        return None


async def _smart_retry(
    client,
    model: str,
    system_prompt: str | None,
    broken_text: str,
    validation_error: ValidationError,
    response_model: type[T],
) -> T | None:
    """Attempt to fix validation errors by sending just the JSON + errors.

    Much cheaper than a full retry (~5K tokens vs ~13K). The LLM doesn't
    need the original document to fix structural errors like wrong enum
    values or missing required fields.

    Returns the validated result, or None if the fix attempt failed.
    """
    try:
        retry_prompt = _build_smart_retry_prompt(
            broken_json=broken_text[:8000],  # cap to avoid huge payloads
            errors=str(validation_error)[:2000],
            response_model=response_model,
        )

        retry_tokens = estimate_tokens(retry_prompt)

        create_kwargs = {
            "model": model,
            "max_tokens": 64000,
            "messages": [{"role": "user", "content": retry_prompt}],
        }
        if system_prompt:
            create_kwargs["system"] = [
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ]

        with client.messages.stream(**create_kwargs) as stream:
            message = stream.get_final_message()

        if not message.content or not hasattr(message.content[0], "text"):
            return None

        text = message.content[0].text
        raw_data = _extract_json_from_text(text)
        raw_data = _normalize_extraction_json(raw_data)
        result = response_model.model_validate(raw_data)

        logger.info(
            "smart_retry_success",
            retry_tokens=retry_tokens,
            entities=len(raw_data.get("entities", [])),
        )

        return result

    except Exception as e:
        logger.warning(
            "smart_retry_error",
            error=str(e)[:200],
        )
        return None
