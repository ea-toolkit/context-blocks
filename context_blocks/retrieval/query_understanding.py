"""Stage 0: Query Understanding — zero LLM, regex-based intent classification.

Maps query intent to knowledge layer priorities and edge type filters.
Meta-model-aware: "How does X work?" prioritizes behavioral layer entities.
"""
import re
from context_blocks.retrieval.types import QueryUnderstanding

# Intent patterns — each intent can have multiple regex patterns
INTENT_PATTERNS: dict[str, list[str]] = {
    "entity": [r"\bwhat is\b", r"\bdefine\b", r"\bexplain\b", r"\bdescribe\b", r"\btell me about\b"],
    "process": [r"\bhow does\b", r"\bhow do\b", r"\bwhat happens\b", r"\bwhat occurs\b", r"\bworkflow\b", r"\bflow\b", r"\bsteps?\b", r"\bpipeline\b", r"\bprocess\b", r"\bsequence\b"],
    "relationship": [r"\bconnects?\b", r"\bdepends?\b", r"\brelat", r"\bintegrat", r"\binteract"],
    "ownership": [r"\bwho owns\b", r"\bresponsib", r"\bteam\b", r"\bowner\b", r"\bmanages?\b", r"\bmanaged by\b"],
    "temporal": [r"\bwhen did\b", r"\bwhen was\b", r"\bwhen does\b", r"\bchanged\b", r"\bhistory\b", r"\bbefore\b", r"\bafter\b", r"\bsince when\b"],
    "diagnostic": [r"\bwhat.s missing\b", r"\bgap\b", r"\bincomplete\b", r"\bwhat.*don.t know\b"],
    "listing": [r"\blist all\b", r"\bshow all\b", r"\bhow many\b", r"\ball the\b", r"\bevery\b"],
    "comparison": [r"\bsimilar\b", r"\bcompare\b", r"\bdifference\b", r"\bvs\b", r"\bversus\b"],
}

# Intent → layer priority boosts (configurable via meta-model.yaml)
DEFAULT_INTENT_LAYER_WEIGHTS: dict[str, dict[str, float]] = {
    "entity": {"structural": 1.5, "language": 1.3},
    "process": {"behavioral": 1.5, "structural": 1.2},
    "relationship": {},  # no bias — all layers equal
    "ownership": {"organizational": 1.5},
    "temporal": {"decision": 1.3},
    "diagnostic": {},  # no bias
    "listing": {},
    "comparison": {},
}

# Intent → edge types to follow during graph traversal
DEFAULT_INTENT_EDGE_PRIORITIES: dict[str, list[str] | None] = {
    "process": ["triggers", "handles", "produces", "consumes", "executed_by", "routes_to"],
    "ownership": ["owned_by", "belongs_to", "managed_by", "executed_by"],
    "relationship": None,  # follow all
    "entity": None,
    "temporal": None,
    "diagnostic": None,
    "listing": None,
    "comparison": None,
}


def classify_query(question: str) -> QueryUnderstanding:
    """Classify a question's intent and derive retrieval parameters.

    Returns intent weight vector (not single class) to handle compound queries.
    All layer priorities stay >= 1.0 — multi-intent boosts, never de-prioritizes.
    """
    question_lower = question.lower()

    # Score each intent by pattern matches
    # First match = strong signal (0.6), additional matches boost further (diminishing)
    intent_weights: dict[str, float] = {}
    for intent, patterns in INTENT_PATTERNS.items():
        match_count = sum(1 for p in patterns if re.search(p, question_lower))
        if match_count > 0:
            intent_weights[intent] = min(1.0, 0.6 + 0.15 * (match_count - 1))

    # Default to "general" if no intent matched
    if not intent_weights:
        intent_weights = {"entity": 0.3}

    # Detect listing/comparison queries
    is_listing = "listing" in intent_weights
    is_comparison = "comparison" in intent_weights

    # Compute layer priorities — scale relative to strongest intent
    max_weight = max(intent_weights.values()) if intent_weights else 1.0
    layer_priorities: dict[str, float] = {}

    for intent, weight in intent_weights.items():
        relative_strength = weight / max_weight
        layer_weights = DEFAULT_INTENT_LAYER_WEIGHTS.get(intent, {})
        for layer, base_boost in layer_weights.items():
            layer_priorities[layer] = max(
                layer_priorities.get(layer, 1.0),
                1.0 + (base_boost - 1.0) * relative_strength,
            )

    # Compute edge priorities — use the dominant intent's edge types
    dominant_intent = max(intent_weights, key=intent_weights.get)
    edge_priorities = DEFAULT_INTENT_EDGE_PRIORITIES.get(dominant_intent)

    # Extract keywords (simple tokenization + stopword removal)
    stopwords = {"the", "a", "an", "is", "are", "was", "were", "do", "does", "did",
                 "how", "what", "who", "when", "where", "why", "which", "that",
                 "this", "it", "to", "for", "of", "in", "on", "at", "by", "with",
                 "and", "or", "but", "not", "from", "about", "all", "can", "will",
                 "be", "has", "have", "had", "i", "my", "me", "we", "our", "you",
                 "your", "tell", "show", "list", "give", "want", "know", "need"}
    keywords = [w for w in re.findall(r"\w+", question_lower) if w not in stopwords and len(w) > 1]

    return QueryUnderstanding(
        original_question=question,
        intent_weights=intent_weights,
        layer_priorities=layer_priorities,
        edge_priorities=edge_priorities,
        keywords=keywords,
        is_listing_query=is_listing,
        is_comparison_query=is_comparison,
    )
