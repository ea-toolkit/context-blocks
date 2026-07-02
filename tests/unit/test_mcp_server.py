"""Tests for the MCP server — block discovery, entity querying, search, gap reports."""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
import yaml

from context_blocks.mcp_server import (
    _block_cache,
    _extract_rels,
    _get_available_blocks,
    _load_entities,
    _parse_frontmatter,
    _resolve_block,
    ask_kb,
    get_entity,
    get_gap_report,
    get_overview,
    list_blocks,
    search_entities,
)

FIXTURES = Path(__file__).parent.parent / "fixtures" / "mcp_kb"


@pytest.fixture(autouse=True)
def _reset_state(monkeypatch):
    """Reset global MCP server state before each test."""
    _block_cache.clear()
    import context_blocks.mcp_server as mod

    monkeypatch.setattr(mod, "_single_output", "")
    monkeypatch.setattr(mod, "_project_root", Path.cwd())


@pytest.fixture()
def single_block(monkeypatch):
    """Configure MCP server to serve the fixture KB as a single block."""
    import context_blocks.mcp_server as mod

    monkeypatch.setattr(mod, "_single_output", str(FIXTURES))
    return FIXTURES


@pytest.fixture()
def multi_block(tmp_path, monkeypatch):
    """Configure MCP server with a blocks.yaml pointing to two fixture blocks."""
    import shutil

    import context_blocks.mcp_server as mod

    block_a = tmp_path / "healthcare"
    block_b = tmp_path / "payments"
    shutil.copytree(FIXTURES / "entities", block_a / "entities")

    (block_b / "entities" / "systems").mkdir(parents=True)
    (block_b / "entities" / "systems" / "payment-gateway.md").write_text(
        "---\ntype: system\nid: payment-gateway\nname: Payment Gateway\n"
        "description: Handles payments\nstatus: active\nconfidence: 0.9\n---\n\n"
        "# Payment Gateway\n\n## Overview\nProcesses card payments.\n"
    )

    blocks_yaml = {
        "healthcare": {"description": "Healthcare claims domain", "entity_count": 4},
        "payments": {"description": "Payment processing domain", "entity_count": 1},
    }
    (tmp_path / "blocks.yaml").write_text(yaml.dump(blocks_yaml))

    monkeypatch.setattr(mod, "_project_root", tmp_path)
    return tmp_path


# ── Frontmatter parsing ──


class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        raw = "---\ntype: system\nid: foo\n---\n\n# Foo\nBody text."
        fm, body = _parse_frontmatter(raw)
        assert fm["type"] == "system"
        assert fm["id"] == "foo"
        assert "# Foo" in body

    def test_no_frontmatter(self):
        raw = "# Just a heading\n\nSome text."
        fm, body = _parse_frontmatter(raw)
        assert fm == {}
        assert "Just a heading" in body

    def test_invalid_yaml(self):
        raw = "---\n: [invalid\n---\nBody."
        fm, body = _parse_frontmatter(raw)
        assert fm == {}


# ── Relationship extraction ──


class TestExtractRels:
    def test_string_relationship(self):
        fm = {"owned_by": "team-alpha"}
        rels = _extract_rels(fm)
        assert len(rels) == 1
        assert rels[0] == {"type": "owned_by", "target_id": "team-alpha"}

    def test_list_relationship(self):
        fm = {"related_systems": ["sys-a", "sys-b"]}
        rels = _extract_rels(fm)
        assert len(rels) == 2
        assert rels[0]["target_id"] == "sys-a"
        assert rels[1]["target_id"] == "sys-b"

    def test_no_relationships(self):
        fm = {"type": "system", "id": "foo"}
        assert _extract_rels(fm) == []

    def test_mixed_relationships(self):
        fm = {"depends_on": ["sys-a"], "owned_by": "team-x", "triggers": ["evt-1"]}
        rels = _extract_rels(fm)
        assert len(rels) == 3
        types = {r["type"] for r in rels}
        assert types == {"depends_on", "owned_by", "triggers"}


# ── Entity loading ──


class TestLoadEntities:
    def test_loads_all_fixture_entities(self):
        entities = _load_entities(FIXTURES / "entities")
        assert len(entities) == 4
        ids = {e["id"] for e in entities}
        assert ids == {"claims-gateway", "adjudication-engine", "claim-routing-process", "eob"}

    def test_entity_fields(self):
        entities = _load_entities(FIXTURES / "entities")
        gateway = next(e for e in entities if e["id"] == "claims-gateway")
        assert gateway["name"] == "Claims Gateway"
        assert gateway["type"] == "system"
        assert gateway["layer"] == "Structural"
        assert gateway["status"] == "active"
        assert gateway["confidence"] == 0.92
        assert gateway["source_documents"] == ["doc-001.md"]
        assert "Central ingress" in gateway["body"]

    def test_entity_relationships_loaded(self):
        entities = _load_entities(FIXTURES / "entities")
        gateway = next(e for e in entities if e["id"] == "claims-gateway")
        rel_types = {r["type"] for r in gateway["relationships"]}
        assert "related_systems" in rel_types
        assert "depends_on" in rel_types

    def test_layer_mapping(self):
        entities = _load_entities(FIXTURES / "entities")
        layers = {e["id"]: e["layer"] for e in entities}
        assert layers["claims-gateway"] == "Structural"
        assert layers["claim-routing-process"] == "Behavioral"
        assert layers["eob"] == "Language"

    def test_skips_non_markdown(self, tmp_path):
        entity_dir = tmp_path / "entities" / "systems"
        entity_dir.mkdir(parents=True)
        (entity_dir / "notes.txt").write_text("not a markdown file")
        (entity_dir / ".DS_Store").write_text("")
        entities = _load_entities(tmp_path / "entities")
        assert len(entities) == 0

    def test_skips_files_without_frontmatter(self, tmp_path):
        entity_dir = tmp_path / "entities" / "systems"
        entity_dir.mkdir(parents=True)
        (entity_dir / "bare.md").write_text("# No frontmatter\nJust text.")
        entities = _load_entities(tmp_path / "entities")
        assert len(entities) == 0


# ── Block discovery ──


class TestListBlocks:
    def test_single_block(self, single_block):
        blocks = list_blocks()
        assert len(blocks) == 1
        assert blocks[0]["has_entities"] is True

    def test_multi_block(self, multi_block):
        blocks = list_blocks()
        assert len(blocks) == 2
        names = {b["name"] for b in blocks}
        assert names == {"healthcare", "payments"}

    def test_multi_block_descriptions(self, multi_block):
        blocks = list_blocks()
        hc = next(b for b in blocks if b["name"] == "healthcare")
        assert hc["description"] == "Healthcare claims domain"
        assert hc["entity_count"] == 4

    def test_no_blocks(self, tmp_path, monkeypatch):
        import context_blocks.mcp_server as mod

        monkeypatch.setattr(mod, "_project_root", tmp_path)
        monkeypatch.setenv("CB_OUTPUT_DIR", str(tmp_path / "nonexistent"))
        blocks = list_blocks()
        assert len(blocks) == 1
        assert blocks[0].get("message", "").startswith("No blocks")


# ── Block resolution ──


class TestResolveBlock:
    def test_auto_resolve_single(self, single_block):
        data = _resolve_block("")
        assert "error" not in data
        assert len(data["entities"]) == 4

    def test_ambiguous_multi_block(self, multi_block):
        data = _resolve_block("")
        assert "error" in data
        assert "Multiple blocks" in data["error"]

    def test_explicit_block_name(self, multi_block):
        data = _resolve_block("healthcare")
        assert "error" not in data
        assert len(data["entities"]) == 4

    def test_unknown_block(self, multi_block):
        data = _resolve_block("nonexistent")
        assert "error" in data
        assert "not found" in data["error"]

    def test_caches_entities(self, single_block):
        _resolve_block("")
        first_entities = _block_cache[list(_block_cache.keys())[0]]["entities"]
        _resolve_block("")
        second_entities = _block_cache[list(_block_cache.keys())[0]]["entities"]
        assert first_entities is second_entities


# ── get_overview ──


class TestGetOverview:
    def test_overview_stats(self, single_block):
        result = get_overview()
        assert result["total_entities"] == 4
        assert result["total_relationships"] > 0
        assert 0 < result["average_confidence"] <= 1.0

    def test_overview_by_type(self, single_block):
        result = get_overview()
        assert result["entities_by_type"]["system"] == 2
        assert result["entities_by_type"]["process"] == 1
        assert result["entities_by_type"]["jargon-business"] == 1

    def test_overview_by_layer(self, single_block):
        result = get_overview()
        assert result["entities_by_layer"]["Structural"] == 2
        assert result["entities_by_layer"]["Behavioral"] == 1
        assert result["entities_by_layer"]["Language"] == 1

    def test_overview_includes_block_name(self, single_block):
        result = get_overview()
        assert "block" in result

    def test_overview_multi_block_requires_name(self, multi_block):
        result = get_overview()
        assert "error" in result

    def test_overview_multi_block_explicit(self, multi_block):
        result = get_overview(block="payments")
        assert result["total_entities"] == 1
        assert result["block"] == "payments"


# ── search_entities ──


class TestSearchEntities:
    def test_search_by_name(self, single_block):
        results = search_entities("claims gateway")
        assert len(results) > 0
        assert results[0]["id"] == "claims-gateway"

    def test_search_by_description(self, single_block):
        results = search_entities("routing queues")
        ids = {r["id"] for r in results}
        assert "claim-routing-process" in ids

    def test_search_by_body(self, single_block):
        results = search_entities("EDI 837")
        assert len(results) > 0
        assert results[0]["id"] == "claims-gateway"

    def test_search_no_results(self, single_block):
        results = search_entities("quantum computing blockchain")
        assert len(results) == 0

    def test_search_empty_query(self, single_block):
        results = search_entities("")
        assert len(results) == 0

    def test_search_filter_by_type(self, single_block):
        results = search_entities("claims", entity_type="process")
        assert all(r["type"] == "process" for r in results)

    def test_search_filter_by_layer(self, single_block):
        results = search_entities("claims", layer="Structural")
        assert all(r["layer"] == "Structural" for r in results)

    def test_search_limit(self, single_block):
        results = search_entities("claims", limit=1)
        assert len(results) <= 1

    def test_search_includes_block_name(self, single_block):
        results = search_entities("claims")
        assert all("block" in r for r in results)

    def test_search_includes_relationships(self, single_block):
        results = search_entities("claims gateway")
        gateway = next(r for r in results if r["id"] == "claims-gateway")
        assert "relationships" in gateway

    def test_search_relevance_order(self, single_block):
        results = search_entities("claims")
        scores = [r["relevance_score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_search_multi_block_explicit(self, multi_block):
        results = search_entities("payment", block="payments")
        assert len(results) == 1
        assert results[0]["id"] == "payment-gateway"
        assert results[0]["block"] == "payments"


# ── get_entity ──


class TestGetEntity:
    def test_get_existing_entity(self, single_block):
        result = get_entity("claims-gateway")
        assert result["id"] == "claims-gateway"
        assert result["name"] == "Claims Gateway"
        assert result["type"] == "system"
        assert result["confidence"] == 0.92
        assert "Central ingress" in result["body"]

    def test_get_entity_relationships(self, single_block):
        result = get_entity("claims-gateway")
        targets = {r["target_id"] for r in result["relationships"]}
        assert "adjudication-engine" in targets
        assert "member-registry" in targets

    def test_get_entity_source_documents(self, single_block):
        result = get_entity("claims-gateway")
        assert result["source_documents"] == ["doc-001.md"]

    def test_get_entity_includes_block(self, single_block):
        result = get_entity("claims-gateway")
        assert "block" in result

    def test_entity_not_found(self, single_block):
        result = get_entity("nonexistent-entity")
        assert "error" in result
        assert "not found" in result["error"]

    def test_get_entity_multi_block(self, multi_block):
        result = get_entity("payment-gateway", block="payments")
        assert result["id"] == "payment-gateway"
        assert result["block"] == "payments"

    def test_get_entity_wrong_block(self, multi_block):
        result = get_entity("claims-gateway", block="payments")
        assert "error" in result


# ── get_gap_report ──


class TestGetGapReport:
    def test_gap_report_coverage(self, single_block):
        result = get_gap_report()
        assert result["total_questions"] == 5
        assert result["coverage"]["CLEAN"] == 1
        assert result["coverage"]["INCOMPLETE"] == 2
        assert result["coverage"]["MISSING"] == 2

    def test_gap_report_gap_count(self, single_block):
        result = get_gap_report()
        assert result["gap_count"] == 4

    def test_gap_report_persona_filter(self, single_block):
        result = get_gap_report(persona="developer")
        assert result["total_questions"] == 2
        assert result["persona_filter"] == "developer"

    def test_gap_report_persona_filter_case_insensitive(self, single_block):
        result = get_gap_report(persona="Developer")
        assert result["total_questions"] == 2

    def test_gap_report_no_evals(self, tmp_path, monkeypatch):
        import context_blocks.mcp_server as mod

        entity_dir = tmp_path / "entities" / "systems"
        entity_dir.mkdir(parents=True)
        monkeypatch.setattr(mod, "_single_output", str(tmp_path))
        result = get_gap_report()
        assert "error" in result
        assert "No eval" in result["error"]

    def test_gap_report_includes_block_name(self, single_block):
        result = get_gap_report()
        assert "block" in result

    def test_gap_details_structure(self, single_block):
        result = get_gap_report()
        gaps = result["gaps"]
        assert len(gaps) > 0
        gap = gaps[0]
        assert "question" in gap
        assert "ddc_class" in gap
        assert "source" in gap
        assert "gaps_detected" in gap

    def test_gap_report_multi_block(self, multi_block):
        result = get_gap_report(block="healthcare")
        assert "error" in result  # no evals dir in healthcare fixture

    def test_gap_report_excludes_clean(self, single_block):
        result = get_gap_report()
        gap_classes = {g["ddc_class"] for g in result["gaps"]}
        assert "CLEAN" not in gap_classes


# ── run_server config ──


class TestRunServerConfig:
    def test_defaults_to_stdio(self, monkeypatch):
        """run_server resolves to stdio when no transport is specified."""
        import context_blocks.mcp_server as mod

        resolved = []
        monkeypatch.setattr(mod.mcp, "run", lambda transport: resolved.append(transport))
        monkeypatch.setattr(mod, "_single_output", str(FIXTURES))
        mod.run_server(output_dir=str(FIXTURES))
        assert resolved == ["stdio"]

    def test_transport_from_env(self, monkeypatch):
        """CB_MCP_TRANSPORT env var is respected."""
        import context_blocks.mcp_server as mod

        resolved = []
        monkeypatch.setattr(mod.mcp, "run", lambda transport: resolved.append(transport))
        monkeypatch.setattr(mod, "_single_output", str(FIXTURES))
        monkeypatch.setenv("CB_MCP_TRANSPORT", "streamable-http")
        mod.run_server(output_dir=str(FIXTURES))
        assert resolved == ["streamable-http"]

    def test_cli_transport_overrides_env(self, monkeypatch):
        """Explicit transport param takes precedence over env var."""
        import context_blocks.mcp_server as mod

        resolved = []
        monkeypatch.setattr(mod.mcp, "run", lambda transport: resolved.append(transport))
        monkeypatch.setattr(mod, "_single_output", str(FIXTURES))
        monkeypatch.setenv("CB_MCP_TRANSPORT", "sse")
        mod.run_server(output_dir=str(FIXTURES), transport="streamable-http")
        assert resolved == ["streamable-http"]

    def test_host_port_from_env(self, monkeypatch):
        """CB_MCP_HOST and CB_MCP_PORT env vars configure HTTP transport."""
        import context_blocks.mcp_server as mod

        monkeypatch.setattr(mod.mcp, "run", lambda transport: None)
        monkeypatch.setattr(mod, "_single_output", str(FIXTURES))
        monkeypatch.setenv("CB_MCP_TRANSPORT", "streamable-http")
        monkeypatch.setenv("CB_MCP_HOST", "0.0.0.0")
        monkeypatch.setenv("CB_MCP_PORT", "9090")
        mod.run_server(output_dir=str(FIXTURES))
        assert mod.mcp.settings.host == "0.0.0.0"
        assert mod.mcp.settings.port == 9090

    def test_cli_host_port_overrides_env(self, monkeypatch):
        """Explicit host/port params take precedence over env vars."""
        import context_blocks.mcp_server as mod

        monkeypatch.setattr(mod.mcp, "run", lambda transport: None)
        monkeypatch.setattr(mod, "_single_output", str(FIXTURES))
        monkeypatch.setenv("CB_MCP_HOST", "0.0.0.0")
        monkeypatch.setenv("CB_MCP_PORT", "9090")
        mod.run_server(output_dir=str(FIXTURES), transport="streamable-http", host="10.0.0.1", port=3000)
        assert mod.mcp.settings.host == "10.0.0.1"
        assert mod.mcp.settings.port == 3000

    def test_stdio_does_not_set_host_port(self, monkeypatch):
        """stdio transport should not touch host/port settings."""
        import context_blocks.mcp_server as mod

        original_host = mod.mcp.settings.host
        original_port = mod.mcp.settings.port
        monkeypatch.setattr(mod.mcp, "run", lambda transport: None)
        monkeypatch.setattr(mod, "_single_output", str(FIXTURES))
        mod.run_server(output_dir=str(FIXTURES), transport="stdio")
        assert mod.mcp.settings.host == original_host
        assert mod.mcp.settings.port == original_port


# ── ask_kb ──


class TestAskKb:
    def _make_mock_result(self, with_synthesis=False):
        from context_blocks.retrieval.types import (
            AnswerScore,
            Gap,
            RetrievalHop,
            RetrievalResult,
            RetrievalTrace,
        )

        hops = [
            RetrievalHop(
                entity_id="claims-gateway",
                entity_name="Claims Gateway",
                entity_type="system",
                layer="Structural",
                confidence=0.92,
                hop_number=0,
                matched_by="vector",
                fused_score=0.85,
                found_by=["vector", "keyword"],
            ),
            RetrievalHop(
                entity_id="claim-routing-process",
                entity_name="Claim Routing Process",
                entity_type="process",
                layer="Behavioral",
                confidence=0.78,
                hop_number=1,
                matched_by="graph",
                fused_score=0.62,
                found_by=["graph"],
                relationship_from="claims-gateway",
                relationship_type="triggers",
            ),
        ]
        trace = RetrievalTrace(
            question="How does claim routing work?",
            sub_queries=[],
            intent_weights={"process": 0.7, "entity": 0.3},
            hops=hops,
            total_entities_retrieved=2,
            total_ms=150,
        )
        gaps = [
            Gap(
                gap_type="thin_coverage",
                entity_id="claim-routing-process",
                description="Process entity has limited detail",
                suggested_action="Add routing rules documentation",
                severity="medium",
                source_question="How does claim routing work?",
            )
        ]

        if with_synthesis:
            answer = "The Claims Gateway routes claims based on type and priority."
            score = AnswerScore.ANSWERABLE
            citations = ["claims-gateway", "claim-routing-process"]
        else:
            answer = "(No synthesis function configured — retrieval only)"
            score = AnswerScore.PARTIAL
            citations = []

        return RetrievalResult(
            answer=answer,
            citations=citations,
            score=score,
            trace=trace,
            gaps=gaps,
            context_text="Entity: Claims Gateway (system)\nCentral ingress...",
        )

    def _inject_mock_pipeline(self, block_name="mcp_kb", has_llm=False):
        """Pre-populate _block_cache with a mocked pipeline."""
        mock_result = self._make_mock_result(with_synthesis=has_llm)
        mock_pipeline = MagicMock()
        mock_pipeline.retrieve = AsyncMock(return_value=mock_result)
        suffix = "synth" if has_llm else "retrieval"
        _block_cache[f"pipeline_{block_name}_{suffix}"] = {"pipeline": mock_pipeline}
        return mock_pipeline

    # ── Retrieval mode (no API key) ──

    @pytest.mark.asyncio
    async def test_retrieval_mode_without_api_key(self, single_block, monkeypatch):
        """ask_kb works without LLM_API_KEY — returns retrieval mode."""
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        self._inject_mock_pipeline("mcp_kb", has_llm=False)

        result = await ask_kb("How does claim routing work?")

        assert "error" not in result
        assert result["mode"] == "retrieval"
        assert len(result["entities"]) == 2
        assert result["entities"][0]["id"] == "claims-gateway"
        assert result["entities"][0]["score"] == 0.85
        assert result["entities"][0]["found_by"] == ["vector", "keyword"]
        assert "context_text" in result
        assert result["intent"] == {"process": 0.7, "entity": 0.3}
        assert "answer" not in result
        assert "ddc_class" not in result
        assert "citations" not in result

    @pytest.mark.asyncio
    async def test_retrieval_mode_returns_gaps(self, single_block, monkeypatch):
        """Retrieval mode still returns gap detection results."""
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        self._inject_mock_pipeline("mcp_kb", has_llm=False)

        result = await ask_kb("test")
        assert len(result["gaps"]) == 1
        assert result["gaps"][0]["type"] == "thin_coverage"
        assert result["gaps"][0]["severity"] == "medium"

    @pytest.mark.asyncio
    async def test_retrieval_mode_context_text(self, single_block, monkeypatch):
        """Retrieval mode returns assembled context for the calling agent."""
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        self._inject_mock_pipeline("mcp_kb", has_llm=False)

        result = await ask_kb("test")
        assert result["context_text"] == "Entity: Claims Gateway (system)\nCentral ingress..."

    # ── Synthesis mode (with API key) ──

    @pytest.mark.asyncio
    async def test_synthesis_mode_with_api_key(self, single_block, monkeypatch):
        """ask_kb synthesizes answer when LLM_API_KEY is set."""
        monkeypatch.setenv("LLM_API_KEY", "test-key")
        self._inject_mock_pipeline("mcp_kb", has_llm=True)

        result = await ask_kb("How does claim routing work?")

        assert "error" not in result
        assert result["mode"] == "synthesis"
        assert "answer" in result
        assert result["ddc_class"] == "CLEAN"
        assert result["citations"] == ["claims-gateway", "claim-routing-process"]
        assert len(result["entities"]) == 2

    @pytest.mark.asyncio
    async def test_synthesis_mode_still_returns_entities(self, single_block, monkeypatch):
        """Synthesis mode also returns entities and context_text."""
        monkeypatch.setenv("LLM_API_KEY", "test-key")
        self._inject_mock_pipeline("mcp_kb", has_llm=True)

        result = await ask_kb("test")
        assert "entities" in result
        assert "context_text" in result
        assert "intent" in result

    # ── Common behavior ──

    @pytest.mark.asyncio
    async def test_no_entities_error(self, tmp_path, monkeypatch):
        """ask_kb returns error when no entities exist."""
        import context_blocks.mcp_server as mod

        monkeypatch.setattr(mod, "_single_output", str(tmp_path))
        result = await ask_kb("anything")
        assert "error" in result
        assert "No entities" in result["error"]

    @pytest.mark.asyncio
    async def test_includes_block_and_question(self, single_block, monkeypatch):
        """ask_kb includes block name and original question."""
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        self._inject_mock_pipeline("mcp_kb", has_llm=False)

        result = await ask_kb("test question")
        assert "block" in result
        assert result["question"] == "test question"

    @pytest.mark.asyncio
    async def test_entity_fields(self, single_block, monkeypatch):
        """Each entity has the expected fields."""
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        self._inject_mock_pipeline("mcp_kb", has_llm=False)

        result = await ask_kb("test")
        entity = result["entities"][0]
        assert "id" in entity
        assert "name" in entity
        assert "type" in entity
        assert "layer" in entity
        assert "confidence" in entity
        assert "score" in entity
        assert "found_by" in entity

    @pytest.mark.asyncio
    async def test_multi_block(self, multi_block, monkeypatch):
        """ask_kb works with explicit block name in multi-block setup."""
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        self._inject_mock_pipeline("healthcare", has_llm=False)

        result = await ask_kb("test", block="healthcare")
        assert "error" not in result
        assert result["block"] == "healthcare"
