"""Tests for the 17-type entity meta-model."""

from context_blocks.meta_model import (
    ENTITY_TYPE_CONFIG,
    EntityLayer,
    EntityType,
    format_meta_model_for_prompt,
    get_all_types_for_layer,
    get_directory_for_type,
    get_layer_for_type,
    get_meta_model_reference,
)


def test_entity_type_count():
    """There must be exactly 18 entity types."""
    assert len(EntityType) == 18


def test_all_types_have_config():
    """Every entity type must have an entry in ENTITY_TYPE_CONFIG."""
    for entity_type in EntityType:
        assert entity_type in ENTITY_TYPE_CONFIG, f"Missing config for {entity_type.value}"


def test_all_configs_have_required_fields():
    """Every config entry must have layer, directory, and description."""
    for entity_type, config in ENTITY_TYPE_CONFIG.items():
        assert "layer" in config, f"Missing 'layer' for {entity_type.value}"
        assert "directory" in config, f"Missing 'directory' for {entity_type.value}"
        assert "description" in config, f"Missing 'description' for {entity_type.value}"


def test_directories_are_unique():
    """No two entity types should share the same output directory."""
    directories = [config["directory"] for config in ENTITY_TYPE_CONFIG.values()]
    assert len(directories) == len(set(directories)), "Duplicate directories found"


def test_all_layers_have_types():
    """Every layer must have at least one entity type."""
    for layer in EntityLayer:
        types = get_all_types_for_layer(layer)
        assert len(types) > 0, f"Layer {layer.value} has no entity types"


def test_structural_layer_has_6_types():
    """Structural layer should have exactly 6 types (including software-component)."""
    types = get_all_types_for_layer(EntityLayer.STRUCTURAL)
    assert len(types) == 6


def test_behavioral_layer_has_3_types():
    """Behavioral layer should have exactly 3 types."""
    types = get_all_types_for_layer(EntityLayer.BEHAVIORAL)
    assert len(types) == 3


def test_directory_lookup():
    """get_directory_for_type should return the correct directory."""
    assert get_directory_for_type(EntityType.SYSTEM) == "systems"
    assert get_directory_for_type(EntityType.JARGON_BUSINESS) == "jargon-business"
    assert get_directory_for_type(EntityType.DECISION) == "decisions"


def test_layer_lookup():
    """get_layer_for_type should return the correct layer."""
    assert get_layer_for_type(EntityType.SYSTEM) == EntityLayer.STRUCTURAL
    assert get_layer_for_type(EntityType.PROCESS) == EntityLayer.BEHAVIORAL
    assert get_layer_for_type(EntityType.DECISION) == EntityLayer.DECISION


def test_meta_model_reference_count():
    """get_meta_model_reference should return 18 entries."""
    refs = get_meta_model_reference()
    assert len(refs) == 18


def test_format_meta_model_for_prompt():
    """Prompt formatter should produce readable text with all 6 layers."""
    text = format_meta_model_for_prompt()
    assert "Structural Layer" in text
    assert "Behavioral Layer" in text
    assert "Reference Layer" in text
    assert "Organizational Layer" in text
    assert "Language Layer" in text
    assert "Decision Layer" in text
    assert "system" in text
    assert "domain-logic" in text
