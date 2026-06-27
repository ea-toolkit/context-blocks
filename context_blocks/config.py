"""Configuration for Context Blocks — loaded from .env file."""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    # LLM
    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-4-6"
    llm_api_key: str = ""
    llm_endpoint: str | None = None
    llm_temperature: float = 0.0
    llm_max_tokens: int = 64000
    llm_request_timeout: float = 600.0
    llm_connect_timeout: float = 10.0

    # Google (Gemini) — separate key since users may have both configured
    google_api_key: str = ""

    # Token management
    context_window_default: int = 100_000
    response_token_reserve: int = 8_000
    synthesis_max_tokens: int = 4000

    # Pipeline
    min_doc_tokens: int = 20
    max_consecutive_failures: int = 3

    # Retrieval
    retrieval_token_budget: int = 8000
    retrieval_max_results: int = 15
    retrieval_vector_top_k: int = 200
    retrieval_graph_max_hops: int = 3
    gap_confidence_threshold: float = 0.4

    # API server
    api_port: int = 8321

    # Logging
    log_level: str = "INFO"

    # Paths
    output_dir: Path = Path("output")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }


def get_settings() -> Settings:
    """Get application settings. Cached after first call."""
    return Settings()
