"""Stage 6: Synthesis — LLM generates answer with citations from retrieved context.

One LLM call per query. Returns answer text, score (ANSWERABLE/PARTIAL/NOT_ANSWERABLE),
and extracted entity citations.
"""
import json
import os
import re

import structlog

from context_blocks.config import get_settings
from context_blocks.retrieval.types import AnswerScore

logger = structlog.get_logger(__name__)

SYNTHESIS_PROMPT = """You are answering a question about a domain using structured knowledge entities.

Query intent: {intent_summary}

Given the following domain knowledge entities, provide a clear answer.

RULES:
1. For each claim in your answer, cite the source entity in brackets: [entity-name]
   Use the entity name exactly as given.
2. Only use information from the provided entities. Do not add external knowledge.
3. Rate your answer at the end:
   - ANSWERABLE: the context fully addresses the question
   - PARTIAL: the context partially addresses it but key information is missing
   - NOT_ANSWERABLE: the context does not contain enough information to answer
4. If you cannot fully answer, explain what specific information is missing.

Question: {question}

Context:
{context}

Provide your answer, then on the last line write ONLY one of: ANSWERABLE | PARTIAL | NOT_ANSWERABLE"""


def _format_intent_summary(intent_weights: dict[str, float]) -> str:
    """Readable intent summary for the synthesis prompt."""
    if not intent_weights:
        return "general query"
    top = sorted(intent_weights.items(), key=lambda x: -x[1])[:2]
    parts = []
    for intent, weight in top:
        if intent == "process":
            parts.append("process query — focus on flow and sequence")
        elif intent == "ownership":
            parts.append("ownership query — focus on responsibility and teams")
        elif intent == "entity":
            parts.append("entity query — focus on what it is and how it works")
        elif intent == "relationship":
            parts.append("relationship query — focus on connections")
        elif intent == "temporal":
            parts.append("temporal query — focus on history and changes")
        elif intent == "diagnostic":
            parts.append("diagnostic query — focus on gaps and missing information")
        elif intent == "listing":
            parts.append("listing query — enumerate all matching items")
        elif intent == "comparison":
            parts.append("comparison query — identify similarities and differences")
        else:
            parts.append(f"{intent} query")
    return "; ".join(parts)


def _extract_citations(answer: str) -> list[str]:
    """Extract entity citations from [entity-name] brackets in the answer."""
    return re.findall(r"\[([^\]]+)\]", answer)


def _extract_score(answer: str) -> AnswerScore:
    """Extract the answer score from the last few lines.

    The LLM sometimes adds explanation text after the score line,
    so we scan the last 5 lines instead of just the last one.
    """
    lines = answer.strip().split("\n")
    # Check last 5 lines for the score keyword
    for line in reversed(lines[-5:]):
        line_upper = line.strip().upper()
        if "NOT_ANSWERABLE" in line_upper or "NOT ANSWERABLE" in line_upper:
            return AnswerScore.NOT_ANSWERABLE
        if "PARTIAL" in line_upper:
            return AnswerScore.PARTIAL
        if "ANSWERABLE" in line_upper:
            return AnswerScore.ANSWERABLE

    return AnswerScore.NOT_ANSWERABLE


async def synthesize_with_llm(
    question: str,
    context: str,
    intent_weights: dict[str, float],
    model: str | None = None,
    api_key: str | None = None,
) -> tuple[str, AnswerScore, list[str]]:
    """Synthesize answer using any LLM provider via litellm."""
    import litellm

    settings = get_settings()
    provider = os.environ.get("LLM_PROVIDER", "anthropic")
    model = model or os.environ.get("LLM_MODEL", "claude-sonnet-4-6")
    api_key = api_key or os.environ.get("LLM_API_KEY", "")
    litellm.request_timeout = int(settings.llm_request_timeout)
    litellm_model = model if provider == "openai" else f"{provider}/{model}"

    prompt = SYNTHESIS_PROMPT.format(
        intent_summary=_format_intent_summary(intent_weights),
        question=question,
        context=context,
    )

    settings = get_settings()
    try:
        response = litellm.completion(
            model=litellm_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.synthesis_max_tokens,
            api_key=api_key,
        )
    except Exception as e:
        logger.error("synthesis_api_error", error=str(e))
        return (
            f"[Synthesis failed: {e}] Retrieved entities are shown below:\n\n{context[:1000]}",
            AnswerScore.NOT_ANSWERABLE,
            [],
        )

    answer = response.choices[0].message.content
    score = _extract_score(answer)
    citations = _extract_citations(answer)

    lines = answer.strip().split("\n")
    score_keywords = ["ANSWERABLE", "PARTIAL", "NOT_ANSWERABLE", "NOT ANSWERABLE"]
    while lines and any(s in lines[-1].upper() for s in score_keywords):
        lines.pop()
    answer = "\n".join(lines).strip()

    usage = response.usage
    logger.info(
        "synthesis_complete",
        score=score.value,
        citations=len(citations),
        input_tokens=getattr(usage, "prompt_tokens", 0),
        output_tokens=getattr(usage, "completion_tokens", 0),
    )

    return answer, score, citations


async def synthesize_without_llm(
    question: str,
    context: str,
    intent_weights: dict[str, float],
) -> tuple[str, AnswerScore, list[str]]:
    """Fallback: return context directly without LLM synthesis.

    Useful for testing retrieval quality without API cost.
    """
    if not context.strip():
        return "No relevant entities found.", AnswerScore.NOT_ANSWERABLE, []

    # Simple heuristic: if we have context, it's at least partial
    citations = re.findall(r"Entity: ([^\n(]+)", context)
    answer = f"Based on {len(citations)} retrieved entities:\n\n{context[:2000]}"

    return answer, AnswerScore.PARTIAL, citations


def get_synthesizer(provider: str = "anthropic", api_key: str | None = None):
    """Get a synthesis function based on provider.

    Returns an async function: (question, context, intent_weights) -> (answer, score, citations)
    All providers go through litellm. Use provider="none" to skip LLM synthesis.
    """
    if provider == "none":
        return synthesize_without_llm

    async def _synth(q, c, i):
        return await synthesize_with_llm(q, c, i, api_key=api_key)
    return _synth
