"""Domain-Aware Retrieval (DAR) — typed, confidence-weighted retrieval for Context Blocks.

7-stage pipeline:
  Stage 0:   Query understanding (intent classification, layer priorities)
  Stage 0.5: Query decomposition (optional, for compound queries)
  Stage 1:   Parallel search (vector + keyword + typed graph traversal)
  Stage 2:   Fusion (RRF + layer boost + cosine re-score)
  Stage 3:   Scoring adjustments (confidence + density + source boosts)
  Stage 4:   Dedup (5-layer pipeline)
  Stage 5:   Context building + trace generation
  Stage 6:   Synthesis (LLM answer with citations)
  Stage 7:   Gap detection (DDC feedback signals)
"""
