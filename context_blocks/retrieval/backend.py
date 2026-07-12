"""Storage backend interface and InMemoryBackend implementation.

The retrieval logic is backend-agnostic. Only the storage layer changes
with scale: InMemory (demo) → FAISS (beta) → Postgres (production).
"""
import math
import re
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import Path

import numpy as np
import structlog
import yaml

from context_blocks.ontology import Ontology, load_ontology
from context_blocks.retrieval.types import ScoredEntity

logger = structlog.get_logger(__name__)


class StorageBackend(ABC):
    """Abstract storage — retrieval logic doesn't know which backend is used."""

    @abstractmethod
    async def vector_search(self, query_embedding: np.ndarray, top_k: int = 200) -> list[ScoredEntity]:
        """Cosine similarity search over entity embeddings."""

    @abstractmethod
    async def keyword_search(self, query: str, top_k: int = 200) -> list[ScoredEntity]:
        """Full-text / BM25 search over entity text fields."""

    @abstractmethod
    async def graph_neighbors(
        self, entity_ids: list[str], max_hops: int = 3,
        edge_types: list[str] | None = None, max_seeds: int = 15,
    ) -> list[ScoredEntity]:
        """BFS graph traversal from seed entities with typed edge filtering."""

    @abstractmethod
    async def get_entity(self, entity_id: str) -> ScoredEntity | None:
        """Direct entity lookup by ID."""

    @abstractmethod
    def get_all_entity_ids(self) -> list[str]:
        """Return all entity IDs in the backend."""

    @abstractmethod
    def entity_count(self) -> int:
        """Total entity count."""


class InMemoryBackend(StorageBackend):
    """In-memory storage for demo/testing (up to ~10K entities).

    Embeddings: numpy array, cosine via dot product
    Keywords: simple TF-IDF-like matching on entity fields
    Graph: dict adjacency list from frontmatter relationships
    """

    def __init__(self, ontology: Ontology | None = None):
        self.entities: dict[str, ScoredEntity] = {}
        self.embeddings: dict[str, np.ndarray] = {}
        self.embedding_matrix: np.ndarray | None = None
        self.embedding_ids: list[str] = []
        self.graph: dict[str, list[dict]] = defaultdict(list)  # entity_id → [{type, target_id}]
        self.reverse_graph: dict[str, list[dict]] = defaultdict(list)  # target_id → [{type, source_id}]
        self._ontology = ontology

    def load_from_entity_dir(self, entity_dir: Path):
        """Load all entity markdown files into memory."""
        if not entity_dir.exists():
            logger.warning("entity_dir_not_found", path=str(entity_dir))
            return

        if self._ontology is None:
            self._ontology = load_ontology(entity_dir)

        count = 0
        for type_dir in sorted(entity_dir.iterdir()):
            if not type_dir.is_dir():
                continue
            for filepath in sorted(type_dir.glob("*.md")):
                entity = self._parse_entity_file(filepath, type_dir.name)
                if entity:
                    self.entities[entity.entity_id] = entity

                    # Build graph from relationships
                    for rel in entity.relationships:
                        self.graph[entity.entity_id].append(rel)
                        self.reverse_graph[rel["target_id"]].append({
                            "type": rel["type"],
                            "source_id": entity.entity_id,
                        })

                    count += 1

        logger.info("inmemory_backend_loaded", entities=count, graph_edges=sum(len(v) for v in self.graph.values()))

    def index_embeddings(self, embeddings: dict[str, np.ndarray]):
        """Set entity embeddings for vector search."""
        self.embeddings = embeddings
        self.embedding_ids = list(embeddings.keys())
        if self.embedding_ids:
            self.embedding_matrix = np.stack([embeddings[eid] for eid in self.embedding_ids])
            # Normalize for cosine similarity via dot product
            norms = np.linalg.norm(self.embedding_matrix, axis=1, keepdims=True)
            norms[norms == 0] = 1  # avoid division by zero
            self.embedding_matrix = self.embedding_matrix / norms
            logger.info("embeddings_indexed", count=len(self.embedding_ids), dims=self.embedding_matrix.shape[1])

    async def vector_search(self, query_embedding: np.ndarray, top_k: int = 200) -> list[ScoredEntity]:
        """Cosine similarity via normalized dot product."""
        if self.embedding_matrix is None or len(self.embedding_ids) == 0:
            return []

        # Normalize query
        query_norm = np.linalg.norm(query_embedding)
        if query_norm == 0:
            return []
        query_normalized = query_embedding / query_norm

        # Cosine similarity = dot product of normalized vectors
        similarities = self.embedding_matrix @ query_normalized
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            eid = self.embedding_ids[idx]
            entity = self.entities.get(eid)
            if entity:
                scored = ScoredEntity(
                    entity_id=entity.entity_id,
                    name=entity.name,
                    entity_type=entity.entity_type,
                    layer=entity.layer,
                    confidence=entity.confidence,
                    description=entity.description,
                    overview=entity.overview,
                    body=entity.body,
                    relationships=entity.relationships,
                    source_documents=entity.source_documents,
                    score=float(similarities[idx]),
                    matched_by="vector",
                )
                results.append(scored)

        return results

    async def keyword_search(self, query: str, top_k: int = 200) -> list[ScoredEntity]:
        """Simple keyword matching with field weighting.

        Name matches: 3x weight
        Description matches: 2x weight
        Body matches: 1x weight
        """
        query_terms = set(re.findall(r'\w+', query.lower()))
        if not query_terms:
            return []

        scored = []
        for entity in self.entities.values():
            name_terms = set(re.findall(r'\w+', entity.name.lower()))
            desc_terms = set(re.findall(r'\w+', entity.description.lower()))
            body_terms = set(re.findall(r'\w+', entity.body.lower()[:2000]))

            name_hits = len(query_terms & name_terms)
            desc_hits = len(query_terms & desc_terms)
            body_hits = len(query_terms & body_terms)

            score = (name_hits * 3.0 + desc_hits * 2.0 + body_hits * 1.0) / max(len(query_terms), 1)

            if score > 0:
                result = ScoredEntity(
                    entity_id=entity.entity_id,
                    name=entity.name,
                    entity_type=entity.entity_type,
                    layer=entity.layer,
                    confidence=entity.confidence,
                    description=entity.description,
                    overview=entity.overview,
                    body=entity.body,
                    relationships=entity.relationships,
                    source_documents=entity.source_documents,
                    score=score,
                    matched_by="keyword",
                )
                scored.append(result)

        scored.sort(key=lambda x: -x.score)
        return scored[:top_k]

    async def graph_neighbors(
        self, entity_ids: list[str], max_hops: int = 3,
        edge_types: list[str] | None = None, max_seeds: int = 15,
    ) -> list[ScoredEntity]:
        """BFS from seed entities with typed edge filtering and hop decay."""
        hop_decay = {0: 1.0, 1: 0.85, 2: 0.70, 3: 0.55}

        # Adaptive seed count
        adaptive_seeds = min(max_seeds, max(5, len(self.entities) // 100))
        seeds = entity_ids[:adaptive_seeds]

        visited: set[str] = set()
        frontier: list[tuple[str, int, str | None, str | None]] = [
            (eid, 0, None, None) for eid in seeds
        ]
        results: list[ScoredEntity] = []

        while frontier:
            entity_id, hop, rel_from, rel_type = frontier.pop(0)
            if entity_id in visited or hop > max_hops:
                continue
            visited.add(entity_id)

            entity = self.entities.get(entity_id)
            if not entity:
                continue

            decay = hop_decay.get(hop, 0.5)
            result = ScoredEntity(
                entity_id=entity.entity_id,
                name=entity.name,
                entity_type=entity.entity_type,
                layer=entity.layer,
                confidence=entity.confidence,
                description=entity.description,
                overview=entity.overview,
                body=entity.body,
                relationships=entity.relationships,
                source_documents=entity.source_documents,
                score=decay,
                matched_by="graph",
                hop_number=hop,
                hop_decay=decay,
                relationship_from=rel_from,
                relationship_type=rel_type,
            )
            results.append(result)

            # Follow edges — TYPED if edge_types specified
            for rel in self.graph.get(entity_id, []):
                if edge_types is None or rel["type"] in edge_types:
                    frontier.append((rel["target_id"], hop + 1, entity_id, rel["type"]))

        return results

    async def get_entity(self, entity_id: str) -> ScoredEntity | None:
        return self.entities.get(entity_id)

    def get_all_entity_ids(self) -> list[str]:
        return list(self.entities.keys())

    def entity_count(self) -> int:
        return len(self.entities)

    def _parse_entity_file(self, filepath: Path, type_dir_name: str) -> ScoredEntity | None:
        """Parse an entity markdown file into a ScoredEntity."""
        try:
            content = filepath.read_text(encoding="utf-8")
            parts = content.split("---", 2)
            if len(parts) < 3:
                return None

            fm = yaml.safe_load(parts[1].strip())
            if not fm or not isinstance(fm, dict):
                return None

            body = parts[2].strip()

            entity_type = fm.get("type", type_dir_name)
            layer = self._ontology.get_layer(entity_type) if self._ontology else "unknown"

            # Extract relationships — only fields declared in the ontology
            relationships = []
            for key, value in fm.items():
                if self._ontology and self._ontology.is_relationship_field(key):
                    targets = value if isinstance(value, list) else [value]
                    for target in targets:
                        if isinstance(target, str) and len(target) > 0:
                            relationships.append({"type": key, "target_id": target})

            return ScoredEntity(
                entity_id=fm.get("id", filepath.stem),
                name=fm.get("name", filepath.stem),
                entity_type=entity_type,
                layer=layer,
                confidence=fm.get("confidence", 0.5) if isinstance(fm.get("confidence"), (int, float)) else 0.5,
                description=fm.get("description", ""),
                overview="",
                body=body,
                relationships=relationships,
                source_documents=fm.get("source_documents", []) if isinstance(fm.get("source_documents"), list) else [],
            )
        except Exception as e:
            logger.warning("entity_parse_failed", filepath=str(filepath), error=str(e))
            return None
