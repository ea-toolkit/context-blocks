"""Extract Seed Entities task — creates foundation entities from the seed context.

Runs ONCE before any document analysis. The seed context is the most reliable
source — human-written, intentional. Entities created here form the skeleton
that documents flesh out.
"""

import structlog

from context_blocks.exceptions import ExtractionError
from context_blocks.infrastructure.llm.gateway import extract_structured
from context_blocks.models.entity import DocumentExtractionResult
from context_blocks.prompts.seed_extract import (
    SEED_EXTRACT_SYSTEM_PROMPT,
    build_seed_extract_prompt,
)

logger = structlog.get_logger(__name__)


async def extract_seed_entities(seed_context: str) -> DocumentExtractionResult:
    """Extract foundation entities from the seed context.

    Args:
        seed_context: The full seed context markdown content.

    Returns:
        DocumentExtractionResult with foundation entities.

    Raises:
        ExtractionError: If extraction fails.
    """
    logger.info("seed_extraction_start")

    prompt = build_seed_extract_prompt(seed_context)

    try:
        result = await extract_structured(
            prompt=prompt,
            response_model=DocumentExtractionResult,
            system_prompt=SEED_EXTRACT_SYSTEM_PROMPT,
            temperature=0.0,
            task_name="seed_extract",
            document_name="seed-context",
        )

        result.source_document = "seed-context"

        logger.info(
            "seed_extraction_complete",
            entities_extracted=len(result.entities),
            questions=len(result.questions),
        )

        return result

    except Exception as e:
        logger.error("seed_extraction_failed", error=str(e))
        raise ExtractionError(f"Failed to extract seed entities: {e}") from e
