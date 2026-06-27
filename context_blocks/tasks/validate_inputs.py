"""Input validation — checks seed context and documents before processing."""

from pathlib import Path

import structlog

from context_blocks.exceptions import ConfigurationError
from context_blocks.infrastructure.llm.token_utils import estimate_tokens

logger = structlog.get_logger(__name__)

# Minimum seed context size (characters) to be useful
MIN_SEED_CONTEXT_SIZE = 200

# Maximum seed context size to avoid eating the context window
MAX_SEED_CONTEXT_TOKENS = 10_000


def validate_seed_context(seed_context_path: Path) -> str:
    """Validate and load the seed context file.

    Args:
        seed_context_path: Path to the seed context markdown file.

    Returns:
        The seed context content as a string.

    Raises:
        ConfigurationError: If seed context is missing, empty, or too short.
    """
    if not seed_context_path.exists():
        raise ConfigurationError(f"Seed context file not found: {seed_context_path}")

    content = seed_context_path.read_text(encoding="utf-8").strip()

    if not content:
        raise ConfigurationError("Seed context file is empty")

    if len(content) < MIN_SEED_CONTEXT_SIZE:
        raise ConfigurationError(
            f"Seed context is too short ({len(content)} chars). "
            f"Minimum {MIN_SEED_CONTEXT_SIZE} chars needed. "
            "Fill in at least sections 1, 4, and 10 of the template."
        )

    tokens = estimate_tokens(content)
    if tokens > MAX_SEED_CONTEXT_TOKENS:
        logger.warning(
            "seed_context_large",
            tokens=tokens,
            max_recommended=MAX_SEED_CONTEXT_TOKENS,
            message="Seed context is very large — this may reduce room for document content in prompts",
        )

    # Check for unfilled template markers
    unfilled_sections = content.count("<!-- ")
    filled_sections = sum(
        1 for line in content.split("\n")
        if line.strip() and not line.startswith("#") and not line.startswith("<!--") and not line.startswith("|") and not line.startswith("---") and len(line.strip()) > 10
    )

    if filled_sections < 5:
        logger.warning(
            "seed_context_sparse",
            filled_sections=filled_sections,
            message="Seed context has few filled sections — results will be better with more context",
        )

    logger.info(
        "seed_context_validated",
        size_chars=len(content),
        estimated_tokens=tokens,
    )

    return content
