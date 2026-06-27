"""Embedding utilities for the retrieval pipeline.

Supports local (Fastembed) and API (OpenAI) embedding providers.
Configurable: swap providers without changing retrieval logic.
"""
import numpy as np
import structlog

logger = structlog.get_logger(__name__)


def build_entity_text(entity) -> str:
    """Build the text that gets embedded for an entity.

    Includes relationship names for connection-aware search.
    """
    parts = [entity.name, entity.entity_type, entity.description]

    # Add top relationship names
    rel_text = " ".join(
        f"{r['type']} {r['target_id']}" for r in entity.relationships[:5]
    )
    if rel_text:
        parts.append(rel_text)

    # Add overview prefix if available
    if entity.body:
        # Extract first 150 chars of body (skip markdown headers)
        body_text = entity.body.replace("#", "").strip()[:150]
        if body_text:
            parts.append(body_text)

    return " | ".join(parts)


class LocalEmbedder:
    """Fastembed-based local embedder. No API cost."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from fastembed import TextEmbedding
                self._model = TextEmbedding(model_name=self.model_name)
                logger.info("fastembed_loaded", model=self.model_name)
            except ImportError:
                logger.error("fastembed_not_installed")
                raise ImportError("pip install fastembed")
        return self._model

    async def embed(self, text: str) -> np.ndarray:
        """Embed a single text."""
        model = self._get_model()
        embeddings = list(model.embed([text]))
        return np.array(embeddings[0], dtype=np.float32)

    async def embed_batch(self, texts: list[str]) -> list[np.ndarray]:
        """Embed multiple texts efficiently."""
        model = self._get_model()
        embeddings = list(model.embed(texts))
        return [np.array(e, dtype=np.float32) for e in embeddings]


class OpenAIEmbedder:
    """OpenAI embedding API. Better quality, costs $0.02/M tokens."""

    def __init__(self, model: str = "text-embedding-3-small", api_key: str | None = None):
        self.model = model
        self.api_key = api_key
        self._client = None

    def _get_client(self):
        if self._client is None:
            import openai
            self._client = openai.OpenAI(api_key=self.api_key)
            logger.info("openai_embedder_loaded", model=self.model)
        return self._client

    async def embed(self, text: str) -> np.ndarray:
        """Embed a single text."""
        client = self._get_client()
        response = client.embeddings.create(input=[text], model=self.model)
        return np.array(response.data[0].embedding, dtype=np.float32)

    async def embed_batch(self, texts: list[str]) -> list[np.ndarray]:
        """Embed multiple texts. OpenAI supports batching natively."""
        client = self._get_client()
        # OpenAI batch limit is 2048 inputs
        all_embeddings = []
        for i in range(0, len(texts), 2048):
            batch = texts[i:i + 2048]
            response = client.embeddings.create(input=batch, model=self.model)
            for item in response.data:
                all_embeddings.append(np.array(item.embedding, dtype=np.float32))
        return all_embeddings


def get_embedder(provider: str = "auto", api_key: str | None = None):
    """Get the best available embedder.

    provider: 'openai', 'fastembed', or 'auto' (tries OpenAI first, falls back to local)
    """
    if provider == "openai" or (provider == "auto" and api_key):
        try:
            return OpenAIEmbedder(api_key=api_key)
        except Exception:
            if provider == "openai":
                raise
            logger.info("openai_unavailable_falling_back_to_fastembed")

    return LocalEmbedder()


async def index_entities(backend, embedder) -> int:
    """Embed all entities in the backend and index them for vector search.

    Returns number of entities embedded.
    """
    entities = {eid: backend.entities[eid] for eid in backend.get_all_entity_ids()}

    if not entities:
        logger.warning("no_entities_to_embed")
        return 0

    # Build embedding texts
    texts = {}
    for eid, entity in entities.items():
        texts[eid] = build_entity_text(entity)

    # Batch embed
    entity_ids = list(texts.keys())
    text_list = [texts[eid] for eid in entity_ids]

    logger.info("embedding_entities", count=len(text_list))
    embeddings_list = await embedder.embed_batch(text_list)

    # Index in backend
    embeddings = {eid: emb for eid, emb in zip(entity_ids, embeddings_list)}
    backend.index_embeddings(embeddings)

    return len(embeddings)
