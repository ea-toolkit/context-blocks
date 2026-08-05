"""Tests for BlockRegistry / BlockConfig.

Focus: the `output` and `label` block fields must survive a load round-trip and
`block_output_dir` must honor a block's custom `output` path (reconciles the
Python registry with what blocks.yaml and the JS viewer already use).
"""

from pathlib import Path

import yaml

from context_blocks.blocks import BlockConfig, BlockRegistry


def _write_registry(root: Path, data: dict) -> None:
    (root / "blocks.yaml").write_text(
        yaml.dump(data, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )


def test_get_preserves_output_and_label(tmp_path: Path) -> None:
    _write_registry(
        tmp_path,
        {"demo": {"ontology": "default", "output": "custom/out", "label": "Demo Label"}},
    )
    cfg = BlockRegistry(tmp_path).get("demo")
    assert cfg is not None
    assert cfg.output == "custom/out"
    assert cfg.label == "Demo Label"


def test_list_blocks_preserves_output_and_label(tmp_path: Path) -> None:
    _write_registry(
        tmp_path,
        {"demo": {"output": "nested/data", "label": "Demo"}},
    )
    blocks = BlockRegistry(tmp_path).list_blocks()
    assert len(blocks) == 1
    assert blocks[0].output == "nested/data"
    assert blocks[0].label == "Demo"


def test_block_output_dir_honors_output(tmp_path: Path) -> None:
    _write_registry(tmp_path, {"demo": {"output": "nested/entities-root"}})
    reg = BlockRegistry(tmp_path)
    assert reg.block_output_dir("demo") == tmp_path / "nested" / "entities-root"


def test_block_output_dir_honors_absolute_output(tmp_path: Path) -> None:
    abs_out = tmp_path / "elsewhere" / "block-data"
    _write_registry(tmp_path, {"demo": {"output": str(abs_out)}})
    reg = BlockRegistry(tmp_path)
    assert reg.block_output_dir("demo") == abs_out


def test_block_output_dir_defaults_to_name(tmp_path: Path) -> None:
    _write_registry(tmp_path, {"demo": {"ontology": "default"}})
    reg = BlockRegistry(tmp_path)
    assert reg.block_output_dir("demo") == tmp_path / "demo"


def test_block_output_dir_unregistered_name_defaults_to_name(tmp_path: Path) -> None:
    _write_registry(tmp_path, {"demo": {"ontology": "default"}})
    reg = BlockRegistry(tmp_path)
    assert reg.block_output_dir("nonexistent") == tmp_path / "nonexistent"


def test_create_default_block_has_empty_output_and_label(tmp_path: Path) -> None:
    reg = BlockRegistry(tmp_path)
    reg.create(BlockConfig(name="plain"))
    cfg = reg.get("plain")
    assert cfg is not None
    assert cfg.output == ""
    assert cfg.label == ""
    # Default block resolves to root/name (output not written when empty).
    assert reg.block_output_dir("plain") == tmp_path / "plain"
