"""Custom exceptions for Context Blocks."""


class ContextBlocksError(Exception):
    """Base exception for all Context Blocks errors."""


class ConfigurationError(ContextBlocksError):
    """Raised when configuration is invalid or missing."""


class DocumentLoadError(ContextBlocksError):
    """Raised when a document cannot be loaded or parsed."""


class ExtractionError(ContextBlocksError):
    """Raised when entity extraction fails for a document."""


class LLMError(ContextBlocksError):
    """Raised when an LLM call fails."""


class MetaModelError(ContextBlocksError):
    """Raised when an entity doesn't fit the meta-model."""
