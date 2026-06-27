"""Pydantic models for document scanning — used with Instructor for structured output."""

from enum import Enum

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Classification of document types found in enterprise knowledge bases."""

    ARCHITECTURE_OVERVIEW = "architecture_overview"
    API_SPEC = "api_spec"
    PROCESS_DOC = "process_doc"
    GLOSSARY = "glossary"
    RUNBOOK = "runbook"
    DATA_MODEL = "data_model"
    DECISION_RECORD = "decision_record"
    MEETING_NOTES = "meeting_notes"
    CONFIGURATION = "configuration"
    TUTORIAL = "tutorial"
    ONBOARDING = "onboarding"
    INCIDENT_REPORT = "incident_report"
    OTHER = "other"


class DocumentScope(str, Enum):
    """Whether a document covers broad or narrow content."""

    BROAD = "broad"  # Covers multiple systems/concepts
    NARROW = "narrow"  # Focuses on one specific thing


class ScannedDocument(BaseModel):
    """Result of scanning a single document."""

    filename: str = Field(description="The document filename")
    folder: str = Field(default="", description="Parent folder name if meaningful")
    doc_type: DocumentType = Field(description="What kind of document this is")
    scope: DocumentScope = Field(description="Broad (overview) or narrow (specific)")
    summary: str = Field(description="One sentence: what this document is about")
    reading_priority: int = Field(
        ge=1,
        le=3,
        description="1 = read first (overviews, glossaries), 2 = read second (processes), 3 = read last (specs, runbooks)"
    )
    reasoning: str = Field(description="Why this reading priority was assigned")


class ScanResult(BaseModel):
    """Complete scan result for all documents, ordered by reading priority."""

    documents: list[ScannedDocument] = Field(
        description="All documents classified and ordered by reading priority"
    )
    total_documents: int = Field(description="Total number of documents scanned")
    reading_order_summary: str = Field(
        description="Brief summary of the recommended reading approach"
    )
