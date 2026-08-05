"""Block file storage — the single place that knows where/how a block's files live.

**Persistence boundary.** All block *artifact* I/O is routed through here so that a
future storage-backend swap (DB / object store / hosted git per workspace) is a
contained change rather than a rewrite. At OSS level the backend is the local
filesystem under the block's output dir; the markdown+frontmatter entities remain
the source of truth and are handled elsewhere.

Artifacts are the **non-markdown** files an entity references and an agent fetches
on demand — diagrams (.bpmn/.drawio/.uml), images, xml. They are stored as opaque
blobs: NOT validated, NOT in the retrieval pipeline. Rendering is the frontend's
concern; this module only stores, lists, and reads bytes + a content type.
"""

from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from pathlib import Path

ARTIFACTS_DIRNAME = "artifacts"

# Extension allowlist for non-md artifacts the Studio accepts.
ARTIFACT_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".bpmn", ".drawio", ".uml", ".puml", ".xml", ".svg",
        ".png", ".jpg", ".jpeg", ".gif", ".webp",
    }
)

# Content types for extensions that mimetypes guesses poorly or not at all.
_CONTENT_TYPE_OVERRIDES = {
    ".bpmn": "application/xml",
    ".drawio": "application/xml",
    ".uml": "text/plain",
    ".puml": "text/plain",
    ".xml": "application/xml",
    ".svg": "image/svg+xml",
}


@dataclass(frozen=True)
class ArtifactInfo:
    filename: str
    path: str  # relative to the block's output dir
    size: int
    content_type: str


def artifacts_dir(block_output_dir: Path) -> Path:
    """The directory holding a block's non-md artifacts."""
    return block_output_dir / ARTIFACTS_DIRNAME


def is_allowed_artifact(filename: str) -> bool:
    """True if the filename's extension is an accepted artifact type."""
    return Path(filename).suffix.lower() in ARTIFACT_EXTENSIONS


def safe_filename(filename: str) -> str:
    """Reduce an untrusted filename to a safe basename (no path traversal)."""
    return Path(filename).name


def guess_content_type(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext in _CONTENT_TYPE_OVERRIDES:
        return _CONTENT_TYPE_OVERRIDES[ext]
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"


def _info(block_output_dir: Path, path: Path) -> ArtifactInfo:
    return ArtifactInfo(
        filename=path.name,
        path=str(path.relative_to(block_output_dir)),
        size=path.stat().st_size,
        content_type=guess_content_type(path.name),
    )


def save_artifact(block_output_dir: Path, filename: str, data: bytes) -> ArtifactInfo:
    """Store an artifact blob under the block, returning its info. Overwrites by name."""
    name = safe_filename(filename)
    dest_dir = artifacts_dir(block_output_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / name
    dest.write_bytes(data)
    return _info(block_output_dir, dest)


def list_artifacts(block_output_dir: Path) -> list[ArtifactInfo]:
    """List a block's artifacts (empty if none)."""
    d = artifacts_dir(block_output_dir)
    if not d.exists():
        return []
    return [_info(block_output_dir, p) for p in sorted(d.iterdir()) if p.is_file()]


def read_artifact(block_output_dir: Path, filename: str) -> tuple[bytes, str] | None:
    """Return (bytes, content_type) for an artifact, or None if it does not exist."""
    name = safe_filename(filename)
    path = artifacts_dir(block_output_dir) / name
    if not path.is_file():
        return None
    return path.read_bytes(), guess_content_type(name)
