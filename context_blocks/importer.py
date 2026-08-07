"""Bulk entity import — shared core used by the Studio API and the CLI.

Takes already-loaded entity markdown, validates each document against a block's
ontology, routes it to the correct type directory, and writes it. Pure logic,
no HTTP/FastAPI dependency, so the CLI can call it without a running server.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Literal

from context_blocks.meta_model import get_directory_for_type
from context_blocks.ontology import Ontology
from context_blocks.validation import validate_entity_frontmatter

OnConflict = Literal["error", "skip", "overwrite"]


@dataclass
class EntityImportResult:
    id: str
    type: str = ""
    status: Literal["created", "skipped", "failed"] = "created"
    path: str = ""
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class BulkImportResult:
    results: list[EntityImportResult] = field(default_factory=list)

    @property
    def created(self) -> int:
        return sum(r.status == "created" for r in self.results)

    @property
    def skipped(self) -> int:
        return sum(r.status == "skipped" for r in self.results)

    @property
    def failed(self) -> int:
        return sum(r.status == "failed" for r in self.results)


def bulk_add_entities(
    ontology: Ontology,
    output_dir: Path,
    items: Iterable[tuple[str, str | None]],
    on_conflict: OnConflict = "error",
) -> BulkImportResult:
    """Validate and write a batch of entity documents into ``output_dir/entities``.

    Args:
        ontology: the block's ontology (types + relationship allowlist).
        output_dir: the block's output directory (entities are written under
            ``output_dir/entities/<type-directory>/<id>.md``).
        items: iterable of ``(content, expected_id)`` — full entity markdown and
            an optional expected id the frontmatter must match.
        on_conflict: how to treat an id that already exists on disk —
            ``error`` (report failed), ``skip`` (leave existing), or
            ``overwrite`` (replace).

    Returns:
        A ``BulkImportResult`` with a per-item outcome. Invalid documents are
        reported as ``failed`` and never written; the batch is not aborted.
    """
    output_dir = Path(output_dir)
    results: list[EntityImportResult] = []
    seen_in_batch: set[str] = set()

    for content, expected_id in items:
        result = validate_entity_frontmatter(content, ontology, expected_id=expected_id)
        if not result.valid:
            results.append(
                EntityImportResult(
                    id=expected_id or "", status="failed", errors=result.error_messages
                )
            )
            continue

        entity_type = str(result.frontmatter["type"])
        entity_id = str(result.frontmatter["id"])
        directory = get_directory_for_type(entity_type, ontology=ontology)
        dest_dir = output_dir / "entities" / directory
        dest = dest_dir / f"{entity_id}.md"

        if entity_id in seen_in_batch:
            results.append(
                EntityImportResult(
                    id=entity_id,
                    type=entity_type,
                    status="failed",
                    errors=[f"duplicate id '{entity_id}' within this batch"],
                )
            )
            continue

        if dest.exists() and on_conflict != "overwrite":
            if on_conflict == "skip":
                seen_in_batch.add(entity_id)
                results.append(
                    EntityImportResult(
                        id=entity_id,
                        type=entity_type,
                        status="skipped",
                        path=str(dest.relative_to(output_dir)),
                    )
                )
            else:  # "error"
                results.append(
                    EntityImportResult(
                        id=entity_id,
                        type=entity_type,
                        status="failed",
                        errors=[f"entity '{entity_id}' already exists"],
                    )
                )
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        seen_in_batch.add(entity_id)
        results.append(
            EntityImportResult(
                id=entity_id,
                type=entity_type,
                status="created",
                path=str(dest.relative_to(output_dir)),
                warnings=result.warning_messages,
            )
        )

    return BulkImportResult(results=results)
