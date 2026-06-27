# Context Blocks — Domain-Constrained Retrieval (DCR) Architecture

> Version 1.0 — May 29, 2026
> 
> This document defines the retrieval layer for Context Blocks. It is the result of deep study of three production retrieval systems (Cognee, Graphiti, gBrain) combined with our unique typed entity meta-model.

---

## 1. Design Philosophy

Context Blocks is not a generic knowledge graph. It is a **typed, layered domain knowledge base** with an 18-type entity meta-model across 6 knowledge layers. The retrieval layer leverages this typing to deliver capabilities no generic system can match:

- **Typed intent classification**: query understanding that knows which knowledge layers matter
- **Typed graph traversal**: edge-aware BFS that follows relationship types based on query intent
- **Confidence-weighted ranking**: prefer paths through well-documented entities
- **Gap detection**: treat retrieval dead-ends as actionable curation signals
- **Context traces**: full hop-by-hop explainability

### Core Principle

The retrieval layer is **pluggable at the storage level, opinionated at the logic level.** Storage backends (in-memory, FAISS, PostgreSQL) are swappable. The retrieval logic (intent classification, typed traversal, confidence weighting, gap detection) is ours and does not change with scale.

---

## 2. Pipeline Overview

```
                          ┌─────────────────────┐
                          │    User Question     │
                          └──────────┬──────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  STAGE 0: Query Understanding    │
                    │  (zero LLM — regex + meta-model) │
                    │                                   │
                    │  Input:  question string           │
                    │  Output: intent weight vector      │
                    │          layer priority weights    │
                    │          edge type priorities      │
                    │          extracted keywords        │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  STAGE 0.5: Query Decomposition  │
                    │  (optional — one cheap LLM call)  │
                    │                                   │
                    │  Compound queries split into       │
                    │  2-4 sub-queries, each with own    │
                    │  intent classification              │
                    │                                   │
                    │  Skip if: single-intent detected   │
                    └────────────────┬────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
    ┌─────────▼─────────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐
    │  Vector Search     │ │  Keyword Search    │ │  Graph Search      │
    │                    │ │                    │ │                    │
    │  Embed question    │ │  BM25 on entity    │ │  BFS from top      │
    │  Cosine similarity │ │  names + body text │ │  vector results    │
    │  Top 2K candidates │ │  Top 2K candidates │ │  Typed edge filter │
    │                    │ │                    │ │  Max 3 hops        │
    └─────────┬─────────┘ └─────────┬─────────┘ └─────────┬─────────┘
              │                      │                      │
              └──────────────────────┼──────────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  STAGE 2: Fusion                  │
                    │                                   │
                    │  RRF across all search results     │
                    │  + Layer priority boost            │
                    │  + Cosine re-score blend           │
                    │    (0.7 × RRF + 0.3 × cosine)    │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  STAGE 3: Scoring Adjustments     │
                    │                                   │
                    │  Confidence boost                  │
                    │    score *= (0.5 + confidence)    │
                    │  Relationship density boost        │
                    │    score *= log(1 + edge_count)   │
                    │  Source document boost             │
                    │    score *= (1+0.02×log(1+docs))  │
                    │  Floor-ratio gate (configurable)   │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  STAGE 4: Dedup                   │
                    │                                   │
                    │  Layer 1: Exact entity ID dedup    │
                    │  Layer 2: Text similarity > 0.85   │
                    │  Layer 3: Inverse relationship     │
                    │           dedup                    │
                    │  Layer 4: Type diversity (intent-   │
                    │           aware — skip for listing │
                    │           queries)                 │
                    │  Layer 5: Layer diversity           │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  STAGE 5: Context Building        │
                    │                                   │
                    │  Build hop-by-hop trace            │
                    │  Assemble entity context text      │
                    │  Flag gaps (low confidence,        │
                    │    missing links, orphans)         │
                    │  Enforce token budget              │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  STAGE 6: Synthesis               │
                    │  (one LLM call)                   │
                    │                                   │
                    │  Answer with entity citations      │
                    │  Score: ANSWERABLE / PARTIAL /     │
                    │         NOT_ANSWERABLE             │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │  STAGE 7: Gap Detection           │
                    │                                   │
                    │  Gap taxonomy:                     │
                    │    - Missing entity                │
                    │    - Low-confidence hub             │
                    │    - Broken relationship            │
                    │    - Orphan entity                  │
                    │                                   │
                    │  Gaps → Workbench items             │
                    │  Gaps → Eval coverage scoring       │
                    │  Gaps → DDC curation signal         │
                    └────────────────┬────────────────┘
                                     │
                          ┌──────────▼──────────┐
                          │   RetrievalResult    │
                          │                      │
                          │   answer: str         │
                          │   citations: []       │
                          │   score: enum         │
                          │   trace: []           │
                          │   gaps: []            │
                          │   metrics: {}         │
                          └──────────────────────┘
```

---

## 3. Stage Details

### Stage 0: Query Understanding

**Purpose:** Classify query intent and set retrieval parameters. Zero LLM calls.

**Input:** Raw question string.

**Output:**
```python
@dataclass
class QueryUnderstanding:
    intent_weights: dict[str, float]     # {process: 0.7, ownership: 0.4}
    layer_priorities: dict[str, float]   # {behavioral: 1.5, organizational: 1.2, ...}
    edge_priorities: list[str] | None    # [triggers, handles, produces] or None (all)
    keywords: list[str]                  # extracted search terms
    is_listing_query: bool               # "list all systems" → skip type diversity
    is_comparison_query: bool            # "which 2 systems are similar?" → same-type focus
```

**Intent patterns** (regex-based, zero cost):
```python
INTENT_PATTERNS = {
    'entity':       [r'\bwhat is\b', r'\bdefine\b', r'\bexplain\b', r'\bdescribe\b'],
    'process':      [r'\bhow does\b', r'\bhow do\b', r'\bworkflow\b', r'\bflow\b', r'\bsteps?\b'],
    'relationship': [r'\bconnects?\b', r'\bdepends?\b', r'\brelat', r'\bintegrat'],
    'ownership':    [r'\bwho owns\b', r'\bresponsib', r'\bteam\b', r'\bowner\b'],
    'temporal':     [r'\bwhen\b', r'\bchanged\b', r'\bhistory\b', r'\bbefore\b'],
    'diagnostic':   [r'\bwhat.s missing\b', r'\bgap\b', r'\bincomplete\b'],
    'listing':      [r'\blist all\b', r'\bshow all\b', r'\bhow many\b', r'\ball the\b'],
    'comparison':   [r'\bsimilar\b', r'\bcompare\b', r'\bdifference\b', r'\bvs\b'],
}
```

**Intent → Layer priority mapping** (from meta-model config, not hardcoded):
```yaml
# In meta-model.yaml (user-configurable)
intent_layer_weights:
  entity:       {structural: 1.5, language: 1.3}
  process:      {behavioral: 1.5, structural: 1.2}
  relationship: {}                                   # no bias
  ownership:    {organizational: 1.5}
  temporal:     {decision: 1.3}
  diagnostic:   {}                                   # no bias
  listing:      {}                                   # no bias
  comparison:   {}                                   # no bias
```

**Intent → Edge type priorities** (from meta-model config):
```yaml
intent_edge_priorities:
  process:    [triggers, handles, produces, consumes, executed_by]
  ownership:  [owned_by, belongs_to, managed_by, executed_by]
  relationship: null                                 # follow all
  entity: null                                       # follow all
```

**Multi-intent handling:** When multiple intents match, return a weight vector. Layer priorities are scaled relative to the strongest intent to prevent sub-1.0 de-prioritization:

```python
intent_weights = {ownership: 0.7, process: 0.5}
max_weight = max(intent_weights.values())  # 0.7

layer_priorities = {}
for intent, weight in intent_weights.items():
    relative_strength = weight / max_weight
    for layer, base_boost in INTENT_LAYER_WEIGHTS[intent].items():
        layer_priorities[layer] = max(
            layer_priorities.get(layer, 1.0),
            1.0 + (base_boost - 1.0) * relative_strength
        )

# Result: {organizational: 1.5, behavioral: 1.36, structural: 1.14}
# All above 1.0 — multi-intent boosts, never de-prioritizes
```

### Stage 0.5: Query Decomposition (Optional)

**Purpose:** Split compound queries into independent sub-queries.

**When to trigger:**
- Multiple intents detected with weight > 0.3
- Question contains "and" joining two distinct clauses
- Question length > 15 words

**When to skip:**
- Single intent detected
- Short, focused question
- Listing or comparison query

**Implementation:** One cheap LLM call (Haiku / gpt-4o-mini):
```
System: "Split this question into independent sub-questions. Return as JSON array. 
         If the question is already simple, return it unchanged."
User: "Who owns the billing service and what processes does it trigger?"
Output: ["Who owns the billing service?", "What processes does the billing service trigger?"]
```

Each sub-query runs independently through Stages 1-4 with its own intent classification.

**Sub-query merge strategy (normalized merge):**
```python
def merge_subquery_results(subquery_results: list[list[ScoredEntity]]) -> list[ScoredEntity]:
    """Merge results from multiple sub-queries with additive evidence.
    
    Each sub-query's scores are normalized to 0-1 before merging.
    Entities found by multiple sub-queries get a cross-query bonus —
    additive evidence, not winner-takes-all. This ensures an entity
    found at moderate scores by ALL sub-queries ranks higher than
    one found at high score by a single sub-query.
    """
    entity_map: dict[str, CBEntity] = {}
    score_accumulator: dict[str, list[float]] = defaultdict(list)
    
    for results in subquery_results:
        if not results:
            continue
        max_score = max((r.score for r in results), default=1.0)
        for entity in results:
            normalized = entity.score / max_score if max_score > 0 else 0
            score_accumulator[entity.id].append(normalized)
            entity_map[entity.id] = entity.entity
    
    # Final score: mean of normalized scores + cross-query bonus
    merged = []
    for eid, scores in score_accumulator.items():
        cross_query_bonus = 0.15 * (len(scores) - 1)  # bonus per additional sub-query hit
        final_score = min((sum(scores) / len(scores)) + cross_query_bonus, 1.0)
        merged.append(ScoredEntity(entity=entity_map[eid], score=final_score))
    
    return sorted(merged, key=lambda x: -x.score)
```

Results merge before Stage 5 context building.

**Cost:** ~$0.003 per decomposition. Skip for simple queries = $0.

### Stage 1: Parallel Search

Three search methods execute in parallel:

#### 1a. Vector Search
```python
async def vector_search(query_embedding: ndarray, top_k: int = 200) -> list[ScoredEntity]:
    """Cosine similarity against entity embeddings."""
    # For each entity: score = dot(query_embedding, entity_embedding) / (||q|| × ||e||)
    # Return top 200 candidates sorted by score descending
```

**What gets embedded** (at index time, once):
```python
def embed_text(entity: CBEntity) -> str:
    """Build the text that gets embedded for search.
    
    Includes relationship names so vector search can find entities
    by their connections (e.g., "what connects to eligibility service?"
    finds claims-gateway via its routes_to relationship).
    """
    parts = [entity.name, entity.type_label, entity.description]
    
    # Add top relationship names for connection-aware search
    rel_text = " ".join(
        f"{r.type} {r.target_name}" for r in entity.relationships[:5]
    )
    if rel_text:
        parts.append(rel_text)
    
    if entity.overview:
        parts.append(entity.overview[:150])
    
    return " | ".join(parts)
    
# Example: "Claims Gateway | System | Entry point for all claim submissions | 
#           routes_to Eligibility Service routes_to Rules Engine owned_by Claims Operations |
#           The Claims Gateway handles incoming EDI 837 files..."
```

**Embedding provider** (configurable):
- Default: Fastembed `BAAI/bge-small-en-v1.5` (local, free, 384 dims)
- Better: OpenAI `text-embedding-3-small` (API, $0.02/M tokens, 1536 dims)
- The embedding model is configured once and all entities re-embedded if changed.

#### 1b. Keyword Search
```python
async def keyword_search(query_text: str, top_k: int = 200) -> list[ScoredEntity]:
    """BM25 / text matching on entity fields."""
    # Search against: entity.name (weight: 3x), entity.description (weight: 2x), entity.body (weight: 1x)
    # BM25 or simple TF-IDF depending on backend
    # Return top 200 candidates sorted by relevance
```

**Why keyword search matters:** Jargon terms like "CWID", "EOB", "837P" match perfectly on keywords but poorly on vector similarity. The language layer entities depend on keyword search.

**Name-field priority:** Entity name matches are weighted 3× higher than body matches. "Claims Gateway" appearing in a query should strongly match the entity named "Claims Gateway."

#### 1c. Graph Search (Typed Traversal)
```python
async def graph_search(
    seed_entity_ids: list[str],     # Top results from vector search
    max_hops: int = 3,
    edge_types: list[str] | None = None,  # From intent classification
) -> list[ScoredEntity]:
    """BFS from seed entities, following typed edges."""
    # Hop decay: farther hops are noisier, penalize accordingly
    hop_decay = {0: 1.0, 1: 0.85, 2: 0.70, 3: 0.55}
    
    visited = set()
    frontier = [(eid, 0) for eid in seed_entity_ids[:max_seeds]]  # configurable, default 15
    results = []
    
    while frontier:
        entity_id, hop = frontier.pop(0)
        if entity_id in visited or hop > max_hops:
            continue
        visited.add(entity_id)
        
        entity = storage.get_entity(entity_id)
        decay = hop_decay.get(hop, 0.5)
        results.append(ScoredEntity(
            entity=entity,
            hop_number=hop,
            hop_decay=decay,
            matched_by='graph',
        ))
        
        # Follow relationships — TYPED if edge_types specified
        for rel in entity.relationships:
            if edge_types is None or rel.type in edge_types:
                frontier.append((rel.target_id, hop + 1))
    
    return results
```

**Typed traversal example:**
- Query: "How does a claim flow from submission to payment?"
- Intent: process → edge_types = [triggers, handles, produces, consumes, routes_to]
- Seed: claims-gateway (from vector search)
- Hop 1: claims-gateway →[routes_to]→ eligibility-service
- Hop 2: eligibility-service →[triggers]→ adjudication process
- Hop 3: adjudication →[produces]→ claim-adjudicated event
- Skipped: claims-gateway →[owned_by]→ claims-operations (not a process edge)

Without typed traversal, the BFS would follow `owned_by` and return the claims-operations team — irrelevant to "how does it flow?"

### Stage 2: Fusion

**Purpose:** Merge results from all three search methods into one ranked list.

#### RRF (Reciprocal Rank Fusion)
```python
def rrf_fuse(result_lists: list[list[ScoredEntity]], k: int = 60) -> list[ScoredEntity]:
    """Merge multiple ranked lists using RRF."""
    scores: dict[str, float] = defaultdict(float)
    entity_map: dict[str, ScoredEntity] = {}
    
    for result_list in result_lists:
        for rank, entity in enumerate(result_list):
            scores[entity.id] += 1 / (k + rank)
            entity_map[entity.id] = entity
    
    # Normalize to 0-1
    max_score = max(scores.values()) if scores else 1
    for eid in scores:
        scores[eid] /= max_score
    
    # Sort by fused score
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return [(entity_map[eid], score) for eid, score in ranked]
```

**Why RRF works:** Entities found by multiple search methods rank highest. An entity found by vector AND keyword AND graph is almost certainly relevant. An entity found by only one method might be a false positive.

#### Layer Priority Boost
```python
def apply_layer_boost(results: list, layer_priorities: dict[str, float]):
    """Boost entities from priority layers based on query intent."""
    for entity, score in results:
        boost = layer_priorities.get(entity.layer, 1.0)
        entity.score = score * boost
```

#### Cosine Re-score
```python
def cosine_rescore(results: list, query_embedding: ndarray):
    """Blend RRF score with direct cosine similarity."""
    for entity in results:
        cosine = cosine_similarity(query_embedding, entity.embedding)
        entity.score = 0.7 * entity.score + 0.3 * cosine
```

### Stage 3: Scoring Adjustments

Three multiplicative boosts, all applied only above the floor-ratio gate:

```python
def apply_scoring_adjustments(results: list, bottom_cutoff: float = 0.15):
    """Apply confidence, density, and source boosts.
    
    Args:
        bottom_cutoff: fraction of score range to skip (0.15 = skip bottom 15%).
        Entities in the bottom tier don't receive boosts — prevents noise from
        being elevated by confidence/density signals.
    """
    if not results:
        return
    
    min_score = min(e.score for e in results)
    max_score = max(e.score for e in results)
    low_score_cutoff = min_score + bottom_cutoff * (max_score - min_score)
    
    for entity in results:
        if entity.score < low_score_cutoff:
            continue  # Skip bottom tier — don't boost noise
        
        # 1. Confidence boost (linear with floor):
        #    confidence=1.00 → ×1.00 (no penalty)
        #    confidence=0.75 → ×0.875 (mild penalty)
        #    confidence=0.50 → ×0.75 (moderate penalty)
        #    confidence=0.00 → ×0.50 (halved but not filtered)
        #    Configurable via confidence_weight (0.0 = disabled, 1.0 = full)
        confidence_factor = 0.5 + 0.5 * entity.confidence
        entity.score *= (1.0 - confidence_weight) + confidence_weight * confidence_factor
        
        # 2. Relationship density: hub entities rank higher
        #    score *= (1 + 0.03 × log(1 + edge_count))
        edge_count = len(entity.relationships)
        entity.score *= (1 + 0.03 * math.log(1 + edge_count))
        
        # 3. Source document count: well-evidenced entities rank higher
        #    score *= (1 + 0.02 × log(1 + source_count))
        source_count = len(entity.source_documents)
        entity.score *= (1 + 0.02 * math.log(1 + source_count))
```

### Stage 4: Dedup

Five-layer pipeline. Intent-aware — listing/comparison queries skip diversity filters.

```python
def dedup(results: list, intent: QueryUnderstanding) -> list:
    """5-layer dedup pipeline."""
    
    # Layer 1: Exact entity ID dedup (keep highest scored)
    results = dedup_by_id(results)
    
    # Layer 2: Text similarity — Jaccard > 0.85 → remove lower scored
    results = dedup_by_text_similarity(results, threshold=0.85)
    
    # Layer 3: Inverse relationship dedup
    # A.exposes→B and B.exposed_by→A are the same hop — merge
    results = dedup_inverse_relationships(results)
    
    # Layer 4: Type diversity (skip for listing/comparison queries)
    if not intent.is_listing_query and not intent.is_comparison_query:
        results = enforce_type_diversity(results, max_ratio=0.5)
    
    # Layer 5: Layer diversity (ensure all relevant layers represented)
    if not intent.is_listing_query:
        results = enforce_layer_diversity(results)
    
    return results
```

### Stage 5: Context Building + Trace

**Purpose:** Build the context that goes to the LLM, with full traceability.

```python
@dataclass
class RetrievalHop:
    entity_id: str
    entity_name: str
    entity_type: str
    layer: str
    confidence: float
    hop_number: int                # 0 = direct match, 1+ = graph traversal
    matched_by: str                # 'vector' | 'keyword' | 'graph'
    relationship_from: str | None  # entity we traversed from
    relationship_type: str | None  # edge type we followed
    fused_score: float             # final score after all stages
    gap_flag: bool                 # True if low confidence or open questions
    gap_reason: str | None         # 'low_confidence' | 'has_open_questions' | 'orphan' | 'broken_ref'

@dataclass
class RetrievalTrace:
    question: str
    sub_queries: list[str]         # from decomposition (or [question] if no decomposition)
    intent_weights: dict[str, float]
    hops: list[RetrievalHop]
    total_entities_searched: int
    total_entities_retrieved: int
    vector_search_ms: int
    keyword_search_ms: int
    graph_search_ms: int
    synthesis_ms: int
    total_ms: int
    tokens_used: int
    gaps: list[Gap]
```

**Context assembly:**
```python
def build_context(hops: list[RetrievalHop], token_budget: int = 8000) -> str:
    """Assemble entity context for the LLM, within token budget."""
    context_parts = []
    tokens_used = 0
    
    for hop in sorted(hops, key=lambda h: -h.fused_score):
        entity = storage.get_entity(hop.entity_id)
        
        # Build entity context block
        block = f"Entity: {entity.name} ({entity.type_label}, confidence: {entity.confidence})\n"
        block += f"Description: {entity.description}\n"
        if entity.overview:
            block += f"Overview: {entity.overview}\n"
        
        # Add relationships
        rels = [f"  {r.type} → {r.target_id}" for r in entity.relationships[:5]]
        if rels:
            block += "Relationships:\n" + "\n".join(rels) + "\n"
        
        # Add source provenance
        if entity.source_documents:
            block += f"Sources: {', '.join(entity.source_documents[:3])}\n"
        
        block_tokens = len(block) // 4  # approximate
        if tokens_used + block_tokens > token_budget:
            break
        
        context_parts.append(block)
        tokens_used += block_tokens
    
    return "\n---\n".join(context_parts)
```

### Stage 6: Synthesis

One LLM call that produces an answer with citations:

```python
SYNTHESIS_PROMPT = """Given the following domain knowledge entities and the user's question, 
provide a clear answer with citations.

For each claim in your answer, cite the source entity in brackets: [entity-name]

If you cannot fully answer the question from the provided context, say what's missing.

Rate your answer:
- ANSWERABLE: the context fully addresses the question
- PARTIAL: the context partially addresses it but key information is missing
- NOT_ANSWERABLE: the context does not contain enough information

Question: {question}

Context:
{context}
"""
```

### Stage 7: Gap Detection

**Purpose:** Transform retrieval failures into actionable curation signals.

```python
@dataclass
class Gap:
    gap_type: str          # missing_entity | low_confidence_hub | broken_relationship | orphan_entity
    entity_id: str | None  # the entity with the issue (None for missing_entity)
    description: str       # human-readable description
    suggested_action: str  # what to do about it
    severity: str          # high | medium | low
    source_question: str   # the question that surfaced this gap

GAP_TAXONOMY = {
    'missing_entity': {
        'description': 'No relevant entity exists in the KB for this concept',
        'action': 'Extract new entity from source documents or add missing domain knowledge',
        'severity': 'high',
    },
    'thin_coverage': {
        'description': 'Related entities exist but content is too thin to answer the question',
        'action': 'Enrich existing entities with more detail from source documents',
        'severity': 'high',
    },
    'low_confidence_hub': {
        'description': 'Key entity in the answer path has confidence < 0.4',
        'action': 'Enrich this entity with more source evidence',
        'severity': 'high',
    },
    'broken_relationship': {
        'description': 'Relationship target exists but has no description or overview',
        'action': 'Fill in the target entity content',
        'severity': 'medium',
    },
    'orphan_entity': {
        'description': 'Retrieved entity has zero typed relationships',
        'action': 'Add relationships to connect this entity to the graph',
        'severity': 'low',
    },
}
```

**Gap detection logic:**
```python
def detect_gaps(hops: list[RetrievalHop], answer_score: str) -> list[Gap]:
    gaps = []
    
    for hop in hops:
        # Low confidence hub
        if hop.confidence < 0.4 and hop.hop_number <= 1:
            gaps.append(Gap(
                gap_type='low_confidence_hub',
                entity_id=hop.entity_id,
                description=f'{hop.entity_name} has {hop.confidence:.0%} confidence',
                suggested_action=f'Enrich {hop.entity_name} with more source documents',
                severity='high',
                source_question=question,
            ))
        
        # Broken relationship
        if hop.relationship_from and hop.entity_id:
            entity = storage.get_entity(hop.entity_id)
            if entity and not entity.description:
                gaps.append(Gap(
                    gap_type='broken_relationship',
                    entity_id=hop.entity_id,
                    description=f'{hop.entity_name} exists but has no description',
                    suggested_action=f'Add description to {hop.entity_name}',
                    severity='medium',
                    source_question=question,
                ))
        
        # Orphan entity
        if len(storage.get_entity(hop.entity_id).relationships) == 0:
            gaps.append(Gap(
                gap_type='orphan_entity',
                entity_id=hop.entity_id,
                description=f'{hop.entity_name} has no relationships',
                suggested_action=f'Add relationships for {hop.entity_name}',
                severity='low',
                source_question=question,
            ))
    
    # NOT_ANSWERABLE — distinguish between thin coverage vs truly missing
    if answer_score == 'NOT_ANSWERABLE':
        entities_found = len([h for h in hops if h.fused_score > 0])
        
        if entities_found > 0:
            # Entities exist but descriptions are too thin to answer
            gaps.append(Gap(
                gap_type='thin_coverage',
                entity_id=hops[0].entity_id if hops else None,
                description=f'Found {entities_found} related entities but content is insufficient',
                suggested_action='Enrich existing entities with more detail from source documents',
                severity='high',
                source_question=question,
            ))
        else:
            # No relevant entities found at all
            gaps.append(Gap(
                gap_type='missing_entity',
                entity_id=None,
                description='No entities in the KB could answer this question',
                suggested_action='Extract new entities from source documents or add missing domain knowledge',
                severity='high',
                source_question=question,
            ))
    
    return gaps
```

---

## 4. Storage Backends

All backends implement the same interface:

```python
class StorageBackend(ABC):
    """Abstract storage — retrieval logic is backend-agnostic."""
    
    @abstractmethod
    async def vector_search(self, query_embedding: ndarray, top_k: int) -> list[ScoredEntity]:
        """Cosine similarity search over entity embeddings."""
    
    @abstractmethod
    async def keyword_search(self, query: str, top_k: int) -> list[ScoredEntity]:
        """BM25 / full-text search over entity text fields."""
    
    @abstractmethod
    async def graph_neighbors(
        self, entity_ids: list[str], max_hops: int, edge_types: list[str] | None
    ) -> list[ScoredEntity]:
        """BFS graph traversal from seed entities."""
    
    @abstractmethod
    async def get_entity(self, entity_id: str) -> CBEntity | None:
        """Direct entity lookup by ID."""
    
    @abstractmethod
    async def get_all_entities(self) -> list[CBEntity]:
        """Load all entities (for indexing)."""
```

### InMemoryBackend (demo, up to 10K entities)
```
Embeddings:  numpy ndarray (N × D), cosine via dot product
Keywords:    simple string matching with TF-IDF weighting
Graph:       dict[str, list[Relationship]] adjacency list
Persistence: none — rebuilt from entity files on startup
```

### FAISSBackend (beta, up to 100K entities)
```
Embeddings:  FAISS HNSW index (persistent, approximate NN)
Keywords:    SQLite FTS5 or Whoosh
Graph:       NetworkX directed graph (persistent via pickle)
Persistence: FAISS index + SQLite + pickle files
```

### PostgresBackend (production, 100K+ entities)
```
Embeddings:  pgvector HNSW index
Keywords:    PostgreSQL tsvector + BM25 via ts_rank
Graph:       recursive CTE queries on relationship table
Persistence: full ACID database
```

---

## 5. What Gets Embedded

### Entity Embeddings (at index time)
```python
def build_entity_embedding_text(entity: CBEntity) -> str:
    """Text that gets embedded for each entity."""
    return f"{entity.name} | {entity.type_label} | {entity.description} | {entity.overview[:200] if entity.overview else ''}"
```

### Relationship Embeddings (optional, for relationship-aware search)
```python
def build_relationship_embedding_text(source: CBEntity, rel_type: str, target: CBEntity) -> str:
    """Triple embedding for relationship-aware retrieval."""
    return f"{source.name} {rel_type} {target.name}: {source.description} → {target.description}"
```

### Embedding Providers (configurable)
```yaml
# In config
embedding:
  provider: fastembed          # fastembed | openai | ollama
  model: BAAI/bge-small-en-v1.5
  dimensions: 384
```

---

## 6. Configuration

All retrieval parameters are configurable via the meta-model YAML:

```yaml
# In meta-model.yaml
retrieval:
  # Stage 0
  intent_layer_weights:
    process: {behavioral: 1.5, structural: 1.2}
    ownership: {organizational: 1.5}
    entity: {structural: 1.5, language: 1.3}
  
  intent_edge_priorities:
    process: [triggers, handles, produces, consumes, executed_by]
    ownership: [owned_by, belongs_to, managed_by]
  
  # Stage 1
  vector_search_top_k: 200
  keyword_search_top_k: 200
  graph_max_hops: 3
  graph_max_seeds: 15              # 15-20 for <5K entities, 10 for 50K+
  
  # Stage 2
  rrf_k: 60
  cosine_blend_weight: 0.3       # 0.7×RRF + 0.3×cosine
  
  # Stage 3
  confidence_weight: 1.0          # 0.0 = disabled, 1.0 = full sigmoid strength
  bottom_cutoff: 0.15             # skip bottom 15% of score range from boosts
  
  # Stage 4
  text_similarity_threshold: 0.85
  type_diversity_max_ratio: 0.5
  
  # Stage 5
  token_budget: 8000
  max_results: 15
  
  # Stage 6
  synthesis_model: claude-sonnet-4-6
  
  # Embedding
  embedding:
    provider: fastembed
    model: BAAI/bge-small-en-v1.5
    dimensions: 384
```

---

## 7. Cost Model

| Operation | Cost | When |
|-----------|------|------|
| Entity embedding (indexing) | $0.02 for 400 entities (OpenAI) or $0 (Fastembed) | Once, at index time |
| Query embedding | $0.0001 per query (OpenAI) or $0 (Fastembed) | Per query |
| Query decomposition | $0.003 per compound query | Only for compound queries |
| Synthesis LLM call | $0.01-0.03 per query | Per query |
| **Total per simple query** | **$0.01-0.03** | |
| **Total per compound query** | **$0.02-0.06** | |
| **Full eval run (30 questions)** | **$0.60-1.50** | |

---

## 8. What Makes This Different

| Capability | Cognee | Graphiti | gBrain | **Context Blocks DCR** |
|---|---|---|---|---|
| Query intent classification | Basic (cognitive layer routing) | No | Yes (entity/temporal/event/general) | **Yes + meta-model layer awareness** |
| Typed graph traversal | No (generic BFS) | No (generic BFS) | No | **Yes (edge types filtered by intent)** |
| Confidence-weighted ranking | No | No | Salience weight (different) | **Yes (entity confidence scores)** |
| Gap detection | No | No | No | **Yes (4-type taxonomy, DDC signals)** |
| Context traces | No | No | No | **Yes (hop-by-hop explainability)** |
| Layer priority boosting | No | No | No | **Yes (from typed meta-model)** |
| Intent-aware dedup | No | No | Type diversity only | **Yes (skip diversity for listing queries)** |
| Retrieval feedback loop | Feedback weight (basic) | No | No | **Yes (Workbench → re-retrieval → gap resolved)** |

---

## 9. Implementation Phases

### Phase 1: Core Retrieval (target: 1 week)
- [ ] `StorageBackend` abstract interface
- [ ] `InMemoryBackend` (numpy + dict)
- [ ] Entity embedding at index time (Fastembed)
- [ ] Stage 0: Query understanding (regex intent classification)
- [ ] Stage 1: Vector search + keyword search + graph BFS
- [ ] Stage 2: RRF fusion + layer boost + cosine re-score
- [ ] Stage 3: Confidence weighting + floor gate
- [ ] Stage 4: 5-layer dedup
- [ ] Stage 5: Context building + trace generation
- [ ] Stage 6: Synthesis (LLM call)
- [ ] Stage 7: Gap detection
- [ ] CLI: `context-blocks retrieve "question" --output <dir>`

### Phase 2: Evals Integration (target: 3 days)
- [ ] Question generator (from seed context + sampled docs)
- [ ] Eval runner (question → retrieve → judge → score)
- [ ] Coverage report with gap list
- [ ] CLI: `context-blocks eval --output <dir>`

### Phase 3: Query Decomposition (target: 2 days)
- [ ] Stage 0.5: Compound query detection
- [ ] LLM decomposition call
- [ ] Sub-query parallel execution + result merge

### Phase 4: Advanced Backends (target: when needed)
- [ ] FAISSBackend
- [ ] PostgresBackend
- [ ] Relationship embeddings (triple search)

---

## 10. References

### Codebases Studied
- **Cognee** (github.com/topoteretes/cognee) — triplet scoring, neighborhood expansion
- **Graphiti** (github.com/getzep/graphiti) — RRF, parallel search, temporal filtering
- **gBrain** (github.com/garrytan/gbrain) — multi-stage ranking, dedup pipeline, floor gate

### Academic References
- Bruch et al. 2022 — RRF analysis (arxiv:2210.11934)
- Korean ontology-KG-RAG paper Dec 2025 (arxiv:2512.08398)
- Yu 2026 — "AI-native Knowledge Graphs" newsletter (LinkedIn, April 2026)
- FLARE — Forward-Looking Active Retrieval (NeurIPS 2025)

---

## Addendum: Final Review Feedback (Round 3)

### Additional Gap Type: Ambiguous Entity
```python
'ambiguous_entity': {
    'description': 'Multiple entities with similar names retrieved at similar scores',
    'action': 'Disambiguate in KB or add distinguishing descriptions',
    'severity': 'medium',
}
```
Detection: if two high-scored entities (>0.7) have Jaccard name similarity >0.6, flag as ambiguous.

### Context Assembly: Layer-Interleaved (not just score-sorted)
Round-robin through layers by priority before filling budget. Ensures a process+ownership query includes at least one entity from each relevant layer, not 15 structural entities.

### Synthesis Prompt Enhancement
Pass intent summary to the synthesis LLM:
```
Query intent: process (focus on flow and sequence)
Given the following domain knowledge...
```
Cost: ~20 tokens. Materially improves answer structure.

### Adaptive max_results
If synthesis returns PARTIAL, auto-retry with max_results=25 (from 15). One extra LLM call (~$0.02) for meaningfully better answers on complex queries.

### Naming Decisions
- Internal: **DCR** (Domain-Constrained Retrieval)
- External/README: **Domain-Aware Retrieval** — "constrained" sounds limiting
- `NOT_ANSWERABLE` stays (consistent with DDC taxonomy)

### Demo Priority (June 25)
The trace view showing hop-by-hop path is the most compelling demo moment. No other tool shows this. Build it into the Workbench or Ask page before the conference.
