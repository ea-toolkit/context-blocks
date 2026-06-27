"""Pydantic model for the knowledge summary — fixed-size mental model."""

from pydantic import BaseModel, Field, field_validator


class KnowledgeSummary(BaseModel):
    """The agent's current understanding of the domain — rewritten after each document.

    This is FIXED SIZE. It replaces the previous summary, never grows unbounded.
    Max ~1500 words across all fields.
    """

    domain_architecture: str = Field(
        description="How the systems connect, major components, data flow patterns. 3-5 sentences."
    )
    key_relationships: list[str] = Field(
        description="Important connections noticed across documents. 3-5 items."
    )
    decisions_and_reasoning: list[str] = Field(
        description="Why things are the way they are — architectural choices and trade-offs. 2-4 items."
    )

    @field_validator("key_relationships", "decisions_and_reasoning", mode="before")
    @classmethod
    def coerce_str_to_list(cls, v: str | list) -> list[str]:
        """Accept both string (old format) and list (new format)."""
        if isinstance(v, str):
            # Split on newlines or bullet points
            lines = [line.lstrip("- ").strip() for line in v.split("\n") if line.strip()]
            return lines if lines else [v]
        return v

    open_questions: list[str] = Field(
        max_length=5,
        description="Top 5 most important unanswered questions."
    )
    jargon_learned: dict[str, str] = Field(
        default_factory=dict,
        description="Domain terms learned that weren't in the seed context. Keep top 20."
    )
    documents_read: int = Field(
        default=0,
        description="Total number of documents read so far."
    )
    entities_discovered_count: int = Field(
        default=0,
        description="Total number of entities extracted across all documents."
    )

    def to_prompt_text(self) -> str:
        """Format the summary for inclusion in the analysis prompt."""
        lines = [
            f"You have read {self.documents_read} document(s) and discovered {self.entities_discovered_count} entities so far.",
            "",
            "### Your Current Domain Understanding",
            self.domain_architecture,
            "",
            "### Key Relationships and Patterns",
            *[f"- {r}" for r in self.key_relationships],
            "",
            "### Decisions and Reasoning",
            *[f"- {d}" for d in self.decisions_and_reasoning],
            "",
        ]

        if self.open_questions:
            lines.append("### Open Questions")
            for q in self.open_questions[:5]:
                lines.append(f"- {q}")
            lines.append("")

        if self.jargon_learned:
            lines.append("### Jargon Learned")
            for term, meaning in list(self.jargon_learned.items())[:20]:
                lines.append(f"- **{term}**: {meaning}")
            lines.append("")

        lines.append("Use this understanding to make better connections. If this document answers a previous question or contradicts something, note that.")

        return "\n".join(lines)
