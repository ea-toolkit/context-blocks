"""Validate entity-markdown frontmatter against a block's ontology.

Used by the Studio "add entity" flow to reject malformed entity files before
they enter a block. This validates the *written* frontmatter contract produced
by ``tasks.write_entities.write_entity_file`` — it is deliberately independent
of the LLM extraction schema (``models.entity.ExtractedEntity``), which uses a
different field shape (``entity_type``/``overview``/``details``).

What is validated:
  - the file has a parseable YAML frontmatter block
  - required fields are present and non-empty (see ``REQUIRED_FIELDS``)
  - ``type`` is a known entity type in the ontology
  - ``id`` is kebab-case (and matches an expected id, when the caller supplies one)
  - ``status`` is one of the allowed values
  - every non-standard frontmatter key is a relationship field the ontology allows

What is NOT validated (by design): whether relationship *targets* exist. Dangling
targets are tolerated as a health-lint concern (``brokenRefs``), not a hard error,
matching how the retrieval backend and viewer treat them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import yaml

from context_blocks.ontology import Ontology

# The standard (non-relationship) frontmatter keys an entity file carries.
# Mirrors the set used by tasks.write_entities when merging entities, plus the
# artifact-pointer fields (`diagrams`/`artifacts`) that reference non-md files —
# these are file lists, not entity relationships, so they are not validated as such.
STANDARD_FIELDS: frozenset[str] = frozenset(
    {
        "type", "id", "name", "description", "status", "tags", "source_documents", "confidence",
        "artifacts", "diagrams",
    }
)

# Fields an entity MUST carry to be valid (per the DDC entity-format contract).
REQUIRED_FIELDS: tuple[str, ...] = ("type", "id", "name", "description", "status")

# Allowed status values (matches models.entity.ExtractedEntity.status).
VALID_STATUS: frozenset[str] = frozenset({"active", "deprecated", "planned", "proposed"})

_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

_EMPTY = (None, "", [])


@dataclass(frozen=True)
class FieldError:
    """A single validation problem, tied to the frontmatter field it concerns."""

    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.field}: {self.message}"


@dataclass
class ValidationResult:
    """Outcome of validating one entity file against an ontology.

    ``errors`` block the entity (``valid`` is False when any exist). ``warnings``
    do not block — they surface things worth knowing, e.g. an unrecognized
    frontmatter key that is kept as custom metadata rather than turned into a
    typed graph relationship.
    """

    valid: bool
    errors: list[FieldError] = field(default_factory=list)
    warnings: list[FieldError] = field(default_factory=list)
    frontmatter: dict = field(default_factory=dict)

    @property
    def error_messages(self) -> list[str]:
        return [str(e) for e in self.errors]

    @property
    def warning_messages(self) -> list[str]:
        return [str(w) for w in self.warnings]


def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """Split an entity markdown file into ``(frontmatter, body)``.

    Returns ``(None, content)`` when there is no leading ``---`` block or the
    block is not a valid YAML mapping.
    """
    if not content.lstrip().startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None, parts[2].strip()
    if not isinstance(fm, dict):
        return None, parts[2].strip()
    return fm, parts[2].strip()


def validate_entity_frontmatter(
    content: str,
    ontology: Ontology,
    *,
    expected_id: str | None = None,
) -> ValidationResult:
    """Validate an entity markdown file's frontmatter against ``ontology``.

    Args:
        content: full markdown file content (frontmatter + body).
        ontology: the block's ontology (types + relationship allowlist).
        expected_id: if given (e.g. derived from the target filename), the
            entity's ``id`` must equal it.

    Returns:
        A ``ValidationResult``; ``valid`` is True only when ``errors`` is empty.
        Unknown frontmatter keys are allowed (kept as custom metadata) and
        reported as ``warnings``, not errors.
    """
    errors: list[FieldError] = []
    warnings: list[FieldError] = []

    fm, _ = parse_frontmatter(content)
    if fm is None:
        errors.append(FieldError("frontmatter", "missing or invalid YAML frontmatter block"))
        return ValidationResult(valid=False, errors=errors, frontmatter={})

    # Required fields present and non-empty.
    for name in REQUIRED_FIELDS:
        if name not in fm or fm[name] in _EMPTY:
            errors.append(FieldError(name, "required field is missing or empty"))

    # type must be known in the ontology.
    etype = fm.get("type")
    if etype not in _EMPTY and not ontology.is_known_type(str(etype)):
        known = ", ".join(sorted(ontology.types))
        errors.append(FieldError("type", f"'{etype}' is not a known entity type. Known types: {known}"))

    # id must be kebab-case, and match the expected id when the caller supplies one.
    eid = fm.get("id")
    if eid not in _EMPTY and not _ID_RE.match(str(eid)):
        errors.append(FieldError("id", f"'{eid}' must be kebab-case (lowercase letters, digits, hyphens)"))
    if expected_id is not None and eid not in _EMPTY and str(eid) != expected_id:
        errors.append(FieldError("id", f"'{eid}' must match the expected entity id '{expected_id}'"))

    # status must be an allowed value.
    status = fm.get("status")
    if status not in _EMPTY and str(status) not in VALID_STATUS:
        allowed = ", ".join(sorted(VALID_STATUS))
        errors.append(FieldError("status", f"'{status}' must be one of: {allowed}"))

    # Unknown frontmatter keys are ALLOWED as custom metadata — the ontology
    # defines what is typed/graphed, not the ceiling on what a file may hold. But
    # flag each as a soft warning: it is not turned into a typed graph
    # relationship (this also surfaces a mistyped relationship field such as
    # `depend_on` instead of `depends_on`).
    for key in fm:
        if key in STANDARD_FIELDS or ontology.is_relationship_field(key):
            continue
        warnings.append(
            FieldError(
                key,
                f"'{key}' kept as custom metadata — not a graph relationship "
                f"(if you meant a relationship, use one of the ontology's relationship fields)",
            )
        )

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings, frontmatter=fm)
