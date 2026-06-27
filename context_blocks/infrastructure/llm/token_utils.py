"""Token counting and context window management.

Ensures prompts don't exceed model context limits.
"""

import structlog

from context_blocks.config import get_settings

logger = structlog.get_logger(__name__)

CHARS_PER_TOKEN = 4

CONTEXT_LIMITS: dict[str, int] = {
    "claude-sonnet-4-6": 200_000,
    "claude-opus-4-6": 200_000,
    "claude-sonnet-4-5": 200_000,
    "claude-haiku-4-5": 200_000,
    "gpt-4o": 128_000,
    "gpt-4o-mini": 128_000,
    "gemini-2.5-flash": 1_000_000,
    "gemini-2.5-pro": 1_000_000,
}


def _get_response_reserve() -> int:
    return get_settings().response_token_reserve


def _get_default_limit() -> int:
    return get_settings().context_window_default


def estimate_tokens(text: str) -> int:
    """Estimate token count from text length."""
    return len(text) // CHARS_PER_TOKEN


def get_context_limit(model: str) -> int:
    """Get the context window limit for a model."""
    return CONTEXT_LIMITS.get(model, _get_default_limit())


def truncate_if_needed(
    document_content: str,
    seed_context: str,
    accumulated_text: str,
    model: str,
) -> str:
    """Truncate document content if the total prompt would exceed context limits.

    Priority: seed context (never truncated) > accumulated knowledge (trimmed) > document (truncated).

    Args:
        document_content: The document text to potentially truncate.
        seed_context: Seed context (never truncated).
        accumulated_text: Formatted accumulated knowledge text.
        model: Model name for context limit lookup.

    Returns:
        Document content, truncated if necessary.
    """
    limit = get_context_limit(model) - _get_response_reserve()
    overhead = 2000  # system prompt + formatting

    seed_tokens = estimate_tokens(seed_context)
    accumulated_tokens = estimate_tokens(accumulated_text)
    doc_tokens = estimate_tokens(document_content)

    total = seed_tokens + accumulated_tokens + doc_tokens + overhead

    if total <= limit:
        return document_content

    # Calculate how much room the document has
    available_for_doc = limit - seed_tokens - accumulated_tokens - overhead

    if available_for_doc < 1000:
        # Not enough room even for a truncated doc — this shouldn't happen with reasonable seed/accumulated
        logger.warning(
            "context_window_very_tight",
            seed_tokens=seed_tokens,
            accumulated_tokens=accumulated_tokens,
            available=available_for_doc,
        )
        available_for_doc = 5000  # Force minimum

    # Truncate document
    max_chars = available_for_doc * CHARS_PER_TOKEN
    truncated = document_content[:max_chars]

    logger.warning(
        "document_truncated",
        original_tokens=doc_tokens,
        truncated_tokens=estimate_tokens(truncated),
        limit=limit,
    )

    return truncated + "\n\n[... document truncated due to length ...]"
