"""Context Block management — create, list, and resolve blocks."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class BlockConfig(BaseModel):
    """Configuration for a single context block."""

    name: str
    description: str = ""
    label: str = ""
    ontology: str = "default"
    output: str = ""
    seed_context: str = ""
    model: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    entity_count: int = 0
    last_updated: str = ""


class BlockRegistry:
    """Manages the blocks.yaml registry at a project root."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.registry_path = self.root / "blocks.yaml"

    def _load(self) -> dict[str, dict]:
        if not self.registry_path.exists():
            return {}
        raw = yaml.safe_load(self.registry_path.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}

    def _save(self, data: dict[str, dict]) -> None:
        self.registry_path.write_text(
            yaml.dump(data, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )

    def list_blocks(self) -> list[BlockConfig]:
        data = self._load()
        return [BlockConfig(name=name, **cfg) for name, cfg in data.items()]

    def get(self, name: str) -> BlockConfig | None:
        data = self._load()
        if name not in data:
            return None
        return BlockConfig(name=name, **data[name])

    def exists(self, name: str) -> bool:
        return name in self._load()

    def create(self, config: BlockConfig) -> Path:
        data = self._load()
        if config.name in data:
            msg = f"Block '{config.name}' already exists"
            raise ValueError(msg)

        block_dir = self.root / config.name
        block_dir.mkdir(parents=True, exist_ok=True)
        (block_dir / "entities").mkdir(exist_ok=True)
        (block_dir / "extractions").mkdir(exist_ok=True)

        block_yaml = block_dir / "block.yaml"
        block_data = config.model_dump(exclude={"name"})
        block_yaml.write_text(
            yaml.dump(block_data, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )

        data[config.name] = {
            k: v for k, v in config.model_dump(exclude={"name"}).items() if v
        }
        self._save(data)

        return block_dir

    def update_stats(self, name: str, entity_count: int) -> None:
        data = self._load()
        if name not in data:
            return
        data[name]["entity_count"] = entity_count
        data[name]["last_updated"] = datetime.now(timezone.utc).isoformat()
        self._save(data)

    def resolve_block(self, block_name: str | None) -> BlockConfig:
        """Resolve which block to use. Auto-selects if only one exists."""
        blocks = self.list_blocks()

        if block_name:
            config = self.get(block_name)
            if not config:
                available = ", ".join(b.name for b in blocks) if blocks else "(none)"
                msg = f"Block '{block_name}' not found. Available: {available}"
                raise ValueError(msg)
            return config

        if len(blocks) == 1:
            return blocks[0]

        if len(blocks) == 0:
            msg = "No blocks found. Run 'cb init <name>' first."
            raise ValueError(msg)

        names = ", ".join(b.name for b in blocks)
        msg = f"Multiple blocks exist ({names}). Specify one with --block <name>."
        raise ValueError(msg)

    def block_output_dir(self, name: str) -> Path:
        """Resolve a block's entity-output directory.

        Honors a block's custom ``output`` path (relative to the project root, or
        absolute) so the Python registry agrees with blocks.yaml and the viewer.
        Falls back to ``root/name`` for default blocks or unregistered names.
        """
        config = self.get(name)
        if config and config.output:
            return self.root / config.output
        return self.root / name


def find_project_root(start: Path | None = None) -> Path:
    """Walk up from start dir looking for blocks.yaml or .contextblocks marker.
    Falls back to current working directory."""
    current = (start or Path.cwd()).resolve()
    for parent in [current, *current.parents]:
        if (parent / "blocks.yaml").exists():
            return parent
        if (parent / ".contextblocks").exists():
            return parent
    return Path.cwd().resolve()
