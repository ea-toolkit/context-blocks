"""Pydantic models for entity extraction — used with Instructor for structured LLM output."""

from pydantic import BaseModel, Field

from context_blocks.meta_model import EntityType, RelationshipType


class ExtractedRelationship(BaseModel):
    """A relationship between two entities discovered in a document."""

    relationship_type: str = Field(
        description="The relationship type — use expected types for this entity type (e.g., deployed_on, exposed_by, published_by) or generic types (depends_on, related_to, part_of)"
    )
    target_entity_id: str = Field(
        description="The kebab-case ID of the target entity"
    )
    target_entity_name: str = Field(
        description="The human-readable name of the target entity"
    )
    reasoning: str = Field(
        default="",
        description="Brief explanation of why this relationship exists"
    )


class ExtractedEntity(BaseModel):
    """A single entity extracted from a document."""

    entity_type: EntityType = Field(
        description="One of the 17 entity types from the meta-model"
    )
    id: str = Field(
        description="Unique kebab-case identifier (e.g., 'order-processor', 'payment-workflow')"
    )
    name: str = Field(
        description="Human-readable display name"
    )
    description: str = Field(
        description="One-line summary of what this entity is"
    )
    overview: str = Field(
        description="2-3 sentence overview explaining this entity in the domain context"
    )
    details: str = Field(
        description="Detailed explanation including specifics, behaviors, and important nuances"
    )
    status: str = Field(
        default="active",
        description="Entity status: active, deprecated, planned, or proposed (for things that don't clearly fit any entity type)"
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Labels for filtering and categorization — e.g., 'infrastructure', 'upstream', 'downstream', 'domain-logic', 'conflict', 'low-confidence', 'needs-review', 'seed-context-derived'"
    )
    relationships: list[ExtractedRelationship] = Field(
        default_factory=list,
        description="Relationships to other entities discovered in this document"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="How confident the extraction is (0.0 = guessing, 1.0 = clearly stated)"
    )
    hedged_statements: list[str] = Field(
        default_factory=list,
        description="Any statements in your overview/details that use 'maybe', 'likely', 'probably', 'seems', 'appears to', 'could be'. Rephrase each as a question a domain expert could confirm or deny."
    )
    reasoning: str = Field(
        default="",
        description="Why this was classified as this entity type and not another"
    )


class EntityDecision(BaseModel):
    """A reasoning trace for one decision the agent made during extraction."""

    subject: str = Field(description="What concept or term this decision is about")
    decision: str = Field(description="What the agent decided — e.g., 'classified as system', 'skipped', 'reused existing ID', 'marked as conflict'")
    reasoning: str = Field(description="Why — the chain of thought behind this decision")


class DocumentExtractionResult(BaseModel):
    """The complete extraction result from analyzing one document."""

    source_document: str = Field(
        description="Filename or path of the source document"
    )
    document_summary: str = Field(
        description="Brief summary of what this document covers"
    )
    entities: list[ExtractedEntity] = Field(
        description="All entities extracted from this document"
    )
    questions: list[str] = Field(
        default_factory=list,
        description="Questions the agent has about ambiguous content in this document"
    )
    new_jargon: list[str] = Field(
        default_factory=list,
        description="New domain terms encountered that weren't in the seed context"
    )
    decision_log: list[EntityDecision] = Field(
        default_factory=list,
        description="Reasoning trace — why the agent made each key decision during extraction"
    )


class AccumulatedKnowledge(BaseModel):
    """Running summary of what the agent has learned so far across documents.

    This grows as more documents are processed and is included in every prompt
    to give the agent accumulated context.
    """

    documents_processed: int = Field(default=0)
    entities_discovered: list[str] = Field(
        default_factory=list,
        description="List of entity IDs discovered so far"
    )
    key_insights: list[str] = Field(
        default_factory=list,
        description="Important patterns or connections noticed across documents"
    )
    unresolved_questions: list[str] = Field(
        default_factory=list,
        description="Questions that remain unanswered after reading documents"
    )
    jargon_learned: dict[str, str] = Field(
        default_factory=dict,
        description="New domain terms learned from documents (term -> meaning)"
    )
