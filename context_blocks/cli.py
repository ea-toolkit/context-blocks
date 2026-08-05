"""Context Blocks CLI — command-line interface for running the pipeline."""

import asyncio
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(
    name="context-blocks",
    help="Demand-driven context engine for enterprise AI",
)
console = Console()


def _resolve_output(block: str | None, output: Path) -> Path:
    """Resolve the output directory from --block or --output.
    --block uses the block registry; --output is a direct path override.
    CB_BLOCK env var is a fallback for --block."""
    import os

    from context_blocks.blocks import BlockRegistry, find_project_root

    block_name = block or os.environ.get("CB_BLOCK")
    if not block_name:
        return output

    project_root = find_project_root()
    registry = BlockRegistry(project_root)
    try:
        config = registry.resolve_block(block_name)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1) from None
    return registry.block_output_dir(config.name)


def _resolve_ontology(block: str | None):
    """Load the block's custom ontology if it registered one; else None (built-in default meta-model)."""
    import os

    from context_blocks.blocks import BlockRegistry, find_project_root
    from context_blocks.ontology import load_ontology_from_file

    block_name = block or os.environ.get("CB_BLOCK")
    if not block_name:
        return None
    try:
        config = BlockRegistry(find_project_root()).resolve_block(block_name)
    except ValueError:
        return None

    onto = getattr(config, "ontology", "default") or "default"
    if onto == "default":
        return None
    onto_path = Path(onto)
    if not onto_path.exists():
        console.print(f"[yellow]Block ontology not found: {onto_path} — using default meta-model.[/yellow]")
        return None
    try:
        return load_ontology_from_file(onto_path)
    except Exception as e:
        console.print(f"[yellow]Failed to load block ontology ({e}) — using default meta-model.[/yellow]")
        return None


# ---------------------------------------------------------------------------
# cb init
# ---------------------------------------------------------------------------
@app.command()
def init(
    name: str = typer.Argument(..., help="Name for the context block (kebab-case)"),
    seed: Path = typer.Option(None, "--seed", "-s", help="Path to seed context file"),
    model: str = typer.Option("", "--model", "-m", help="LLM model override (default: from .env)"),
    description: str = typer.Option("", "--description", "-d", help="Short description of this block"),
    ontology: str = typer.Option("default", "--ontology", help="Ontology profile to use (default, or path to YAML)"),
    root: Path = typer.Option(None, "--root", "-r", help="Project root directory (default: current dir)"),
) -> None:
    """Initialize a new context block with its configuration."""
    from context_blocks.blocks import (
        BlockConfig,
        BlockRegistry,
        find_project_root,
        is_valid_block_name,
    )

    project_root = root or find_project_root()
    registry = BlockRegistry(project_root)

    # Validate name
    if not is_valid_block_name(name):
        console.print(f"[red]Invalid block name '{name}'. Use kebab-case (e.g., 'payments', 'billing-platform').[/red]")
        raise typer.Exit(1)

    if registry.exists(name):
        console.print(f"[red]Block '{name}' already exists.[/red]")
        raise typer.Exit(1)

    # Validate seed context if provided
    seed_path = ""
    if seed:
        if not seed.exists():
            console.print(f"[red]Seed context file not found: {seed}[/red]")
            raise typer.Exit(1)
        seed_path = str(seed.resolve())

    config = BlockConfig(
        name=name,
        description=description,
        ontology=ontology,
        seed_context=seed_path,
        model=model,
    )

    console.print(f"\n[bold]Context Blocks — Init[/bold]\n")

    block_dir = registry.create(config)

    # Copy seed context into the block directory for portability
    if seed:
        import shutil
        dest = block_dir / "seed-context.md"
        shutil.copy2(seed, dest)
        console.print(f"  Seed context: {seed} → {dest}")

    # Create .contextblocks marker if it doesn't exist
    marker = project_root / ".contextblocks"
    if not marker.exists():
        marker.write_text("# Context Blocks project root\n", encoding="utf-8")

    console.print(f"  Block:     [bold]{name}[/bold]")
    console.print(f"  Directory: {block_dir}/")
    console.print(f"  Ontology:  {ontology}")
    if description:
        console.print(f"  Desc:      {description}")
    console.print(f"  Registry:  {registry.registry_path}")
    console.print(f"\n[bold green]Block '{name}' created.[/bold green]")
    console.print(f"\nNext steps:")
    console.print(f"  1. Add documents:  cb extract ./docs/ --seed {seed or '<seed-file>'} --block {name}")
    console.print(f"  2. Run evals:      cb eval --block {name} --seed {seed or '<seed-file>'} --personas")
    console.print(f"  3. Start viewer:   cb serve --block {name}")
    console.print()


# ---------------------------------------------------------------------------
# cb blocks
# ---------------------------------------------------------------------------
@app.command()
def blocks(
    root: Path = typer.Option(None, "--root", "-r", help="Project root directory"),
) -> None:
    """List all context blocks in the project."""
    from context_blocks.blocks import BlockRegistry, find_project_root

    project_root = root or find_project_root()
    registry = BlockRegistry(project_root)

    block_list = registry.list_blocks()
    if not block_list:
        console.print("\n[yellow]No blocks found. Run 'cb init <name>' to create one.[/yellow]\n")
        raise typer.Exit(0)

    console.print(f"\n[bold]Context Blocks — {len(block_list)} block(s)[/bold]\n")

    for b in block_list:
        updated = b.last_updated[:10] if b.last_updated else "never"
        desc = f" — {b.description}" if b.description else ""
        console.print(
            f"  [bold]{b.name}[/bold]{desc}"
        )
        console.print(
            f"    entities: {b.entity_count}  |  ontology: {b.ontology}  |  "
            f"updated: {updated}"
        )

    console.print()


def _run_extract(
    docs: Path,
    seed: Path,
    output: Path,
    block: str | None,
    max_docs: int | None,
) -> None:
    """Shared implementation for extract (and its phase1 alias)."""
    from context_blocks.pipeline import run_phase1

    output = _resolve_output(block, output)
    ontology = _resolve_ontology(block)

    console.print(f"\n[bold]Context Blocks — Extract Entities[/bold]\n")
    console.print(f"  Documents:    {docs}")
    console.print(f"  Seed context: {seed}")
    console.print(f"  Output:       {output}")
    if ontology is not None:
        console.print(f"  Ontology:     {ontology.source} ({len(ontology.types)} types)")
    if max_docs:
        console.print(f"  Max docs:     {max_docs}")
    console.print()

    def _on_progress(current: int, total: int, filename: str) -> None:
        console.print(f"  [bold cyan][{current}/{total}][/bold cyan] Extracting: {filename}")

    try:
        results = asyncio.run(run_phase1(
            docs_dir=docs,
            seed_context_path=seed,
            output_dir=output,
            max_documents=max_docs,
            on_progress=_on_progress,
            ontology=ontology,
        ))
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted. Progress has been saved — re-run to resume.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[red]Extraction failed: {e}[/red]")
        console.print("[dim]Progress has been saved. Fix the issue and re-run — processed docs will be skipped.[/dim]")
        raise typer.Exit(1)

    total_entities = sum(len(r.entities) for r in results)
    console.print(f"\n[bold green]Done![/bold green]")
    console.print(f"  Documents processed: {len(results)}")
    console.print(f"  Entities extracted: {total_entities}")
    console.print(f"  Output: {output}/")
    console.print()


@app.command()
def extract(
    docs: Path = typer.Argument(..., help="Directory containing documents to analyze"),
    seed: Path = typer.Option(..., "--seed", "-s", help="Path to seed context file"),
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory"),
    block: str = typer.Option(None, "--block", "-b", help="Context block name (overrides --output)"),
    max_docs: int | None = typer.Option(None, "--max", "-m", help="Max documents to process"),
) -> None:
    """Extract structured domain entities from documents."""
    _run_extract(docs, seed, output, block, max_docs)


@app.command(hidden=True)
def phase1(
    docs: Path = typer.Argument(..., help="Directory containing documents to analyze"),
    seed: Path = typer.Option(..., "--seed", "-s", help="Path to seed context file"),
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory"),
    block: str = typer.Option(None, "--block", "-b", help="Context block name (overrides --output)"),
    max_docs: int | None = typer.Option(None, "--max", "-m", help="Max documents to process"),
) -> None:
    """(Alias for 'extract') Extract structured domain entities from documents."""
    _run_extract(docs, seed, output, block, max_docs)


@app.command()
def reformat(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory with extractions/"),
    block: str = typer.Option(None, "--block", "-b", help="Context block name (overrides --output)"),
) -> None:
    """Regenerate entity markdown from saved extraction JSON. No API calls — free."""
    from context_blocks.tasks.write_entities import reformat_all_entities

    output = _resolve_output(block, output)

    console.print(f"\n[bold]Context Blocks — Reformat Entities[/bold]\n")
    console.print(f"  Source:  {output}/extractions/")
    console.print(f"  Target:  {output}/entities/")
    console.print()

    total = reformat_all_entities(output)

    if total == 0:
        console.print("[yellow]No extraction JSON files found. Run 'cb extract' first.[/yellow]")
    else:
        console.print(f"\n[bold green]Done![/bold green]")
        console.print(f"  Entities regenerated: {total}")
        console.print(f"  Output: {output}/entities/")
    console.print()


@app.command()
def dedup(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory with entities/"),
    block: str = typer.Option(None, "--block", "-b", help="Context block name (overrides --output)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show candidates without merging"),
) -> None:
    """Merge ambiguous entities after extraction. LLM judges each candidate pair."""
    import json
    import os
    from dotenv import load_dotenv

    load_dotenv()

    output = _resolve_output(block, output)

    from context_blocks.tasks.dedup_entities import run_dedup

    entity_dir = output / "entities"
    if not entity_dir.exists():
        console.print(f"[red]Entity directory not found: {entity_dir}[/red]")
        raise typer.Exit(1)

    console.print(f"\n[bold]Context Blocks — Entity Dedup[/bold]\n")
    console.print(f"  KB:       {entity_dir}")
    console.print(f"  Mode:     {'dry run' if dry_run else 'merge'}")
    console.print()

    api_key = os.environ.get("LLM_API_KEY", "")
    merge_log = run_dedup(entity_dir, api_key=api_key, dry_run=dry_run)

    if not merge_log:
        console.print("  No duplicate candidates found.")
    else:
        merged = sum(1 for e in merge_log if e["action"] == "merge")
        kept = sum(1 for e in merge_log if e["action"] == "keep")

        console.print(f"\n[bold]Results[/bold]\n")
        for entry in merge_log:
            icon = "🔗" if entry["action"] == "merge" else "✓"
            action_color = "yellow" if entry["action"] == "merge" else "dim"
            console.print(
                f"  {icon} [{action_color}]{entry['action'].upper()}[/{action_color}] "
                f"{entry['entity_a']} ↔ {entry['entity_b']}"
            )
            console.print(f"    {entry['reason']}")

        console.print(f"\n  Merged: {merged} | Kept separate: {kept}")

        # Write merge log
        log_path = output / "dedup-log.json"
        log_path.write_text(json.dumps(merge_log, indent=2), encoding="utf-8")
        console.print(f"  Log: {log_path}")

    console.print()


@app.command()
def ask(
    question: str = typer.Argument(..., help="Question to ask the domain knowledge base"),
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory with entities/"),
    block: str = typer.Option(None, "--block", "-b", help="Context block name (overrides --output)"),
    provider: str = typer.Option("anthropic", "--provider", "-p", help="LLM provider for synthesis (anthropic/none)"),
    embedder: str = typer.Option("auto", "--embedder", "-e", help="Embedding provider (openai/fastembed/auto)"),
    show_trace: bool = typer.Option(False, "--trace", "-t", help="Show hop-by-hop retrieval trace"),
    show_gaps: bool = typer.Option(True, "--gaps", "-g", help="Show detected knowledge gaps"),
) -> None:
    """Ask a question to the domain knowledge base using Domain-Aware Retrieval."""
    import os
    from dotenv import load_dotenv

    load_dotenv()

    output = _resolve_output(block, output)

    from context_blocks.retrieval.backend import InMemoryBackend
    from context_blocks.retrieval.embedder import get_embedder, index_entities
    from context_blocks.retrieval.pipeline import RetrievalPipeline
    from context_blocks.retrieval.synthesis import get_synthesizer

    entity_dir = output / "entities"
    if not entity_dir.exists():
        console.print(f"[red]Entity directory not found: {entity_dir}[/red]")
        console.print("Run 'cb extract' first to extract entities.")
        raise typer.Exit(1)

    console.print(f"\n[bold]Context Blocks — Domain-Aware Retrieval[/bold]\n")
    console.print(f"  Question:  {question}")
    console.print(f"  KB:        {entity_dir}")
    console.print()

    async def _ask():
        # Load backend
        backend = InMemoryBackend()
        backend.load_from_entity_dir(entity_dir)
        console.print(f"  Loaded [bold]{backend.entity_count()}[/bold] entities")

        # Set up embedder
        openai_key = os.environ.get("OPENAI_API_KEY")
        emb = get_embedder(provider=embedder, api_key=openai_key)
        count = await index_entities(backend, emb)
        console.print(f"  Embedded [bold]{count}[/bold] entities")

        # Set up synthesizer
        llm_key = os.environ.get("LLM_API_KEY", "")
        synth = get_synthesizer(provider=provider, api_key=llm_key)

        # Run retrieval pipeline
        console.print(f"\n  [dim]Searching...[/dim]")
        pipeline = RetrievalPipeline(backend, embed_fn=emb.embed, synthesize_fn=synth)
        result = await pipeline.retrieve(question)

        # Display answer
        console.print(f"\n[bold]Answer[/bold] ({result.score.value}):\n")
        console.print(result.answer)

        # Display citations
        if result.citations:
            console.print(f"\n[dim]Citations: {', '.join(result.citations[:10])}[/dim]")

        # Display trace
        if show_trace and result.trace.hops:
            console.print(f"\n[bold]Retrieval Trace[/bold] ({len(result.trace.hops)} hops, {result.trace.total_ms}ms):\n")
            for hop in result.trace.hops:
                gap_marker = " [yellow]⚠ GAP[/yellow]" if hop.gap_flag else ""
                via = ""
                if hop.relationship_from:
                    via = f" via {hop.relationship_type} from {hop.relationship_from}"
                console.print(
                    f"  hop {hop.hop_number}: [bold]{hop.entity_name}[/bold] "
                    f"({hop.entity_type}, {hop.matched_by}, "
                    f"conf={hop.confidence:.0%}, score={hop.fused_score:.3f})"
                    f"{via}{gap_marker}"
                )

        # Display gaps
        if show_gaps and result.gaps:
            console.print(f"\n[bold]Knowledge Gaps[/bold] ({len(result.gaps)} detected):\n")
            for gap in result.gaps:
                severity_color = {"high": "red", "medium": "yellow", "low": "dim"}.get(gap.severity, "dim")
                console.print(
                    f"  [{severity_color}]{gap.severity.upper()}[/{severity_color}] "
                    f"[{gap.gap_type}] {gap.description}"
                )
                console.print(f"    → {gap.suggested_action}")

        console.print()

    try:
        asyncio.run(_ask())
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[red]Retrieval failed: {e}[/red]")
        console.print("[dim]Check your API keys (LLM_API_KEY, OPENAI_API_KEY) and try again.[/dim]")
        raise typer.Exit(1)


@app.command()
def serve(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory with entities/"),
    block: str = typer.Option(None, "--block", "-b", help="Context block name (overrides --output)"),
    port: int = typer.Option(None, "--port", help="Server port (default: API_PORT env var or 8321)"),
    provider: str = typer.Option("anthropic", "--provider", help="LLM provider for synthesis"),
    embedder: str = typer.Option("auto", "--embedder", "-e", help="Embedding provider"),
) -> None:
    """Start the API server for live retrieval queries."""
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv()

    output = _resolve_output(block, output)

    if port is None:
        from context_blocks.config import get_settings
        port = get_settings().api_port

    entity_dir = output / "entities"
    if not entity_dir.exists():
        console.print(f"[red]Entity directory not found: {entity_dir}[/red]")
        console.print("Run 'cb extract' first to extract entities.")
        raise typer.Exit(1)

    console.print(f"\n[bold]Context Blocks — API Server[/bold]\n")
    console.print(f"  KB:       {entity_dir}")
    console.print(f"  Port:     {port}")
    console.print(f"  Provider: {provider}")
    console.print(f"  Embedder: {embedder}")
    console.print()
    console.print(f"  Starting server at http://localhost:{port}")
    console.print(f"  API docs at http://localhost:{port}/docs")
    console.print()

    import os
    os.environ["CB_OUTPUT_DIR"] = str(output)

    from context_blocks.api import create_app
    app_instance = create_app(output_dir=str(output), provider=provider, embedder=embedder)
    uvicorn.run(app_instance, host="0.0.0.0", port=port, log_level="info")


@app.command()
def eval(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory with entities/"),
    block: str = typer.Option(None, "--block", "-b", help="Context block name (overrides --output)"),
    seed: Path = typer.Option(None, "--seed", "-s", help="Seed context file for question generation"),
    docs: Path = typer.Option(None, "--docs", "-d", help="Source documents directory for question generation"),
    personas: bool = typer.Option(False, "--personas", help="Include persona-driven completeness checks (requires --seed)"),
    persona_config: Path = typer.Option(None, "--persona-config", help="Custom persona templates YAML (default: built-in)"),
    work_items: Path = typer.Option(None, "--work-items", "-w", help="Directory of work items for DDC evaluation"),
    questions_file: Path = typer.Option(None, "--questions-file", "-f", help="Load questions from JSON file (skip generation)"),
    questions: int = typer.Option(30, "--questions", "-q", help="Target number of eval questions (seed+doc)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Generate and print questions only — no retrieval, no cost"),
    provider: str = typer.Option("anthropic", "--provider", "-p", help="LLM provider for synthesis (anthropic/none)"),
    embedder: str = typer.Option("auto", "--embedder", "-e", help="Embedding provider (openai/fastembed/auto)"),
) -> None:
    """Evaluate KB coverage: generate questions, run retrieval, produce coverage report."""
    import os
    import time
    from dotenv import load_dotenv

    load_dotenv()

    output = _resolve_output(block, output)

    from context_blocks.retrieval.backend import InMemoryBackend
    from context_blocks.retrieval.embedder import get_embedder, index_entities
    from context_blocks.retrieval.evals import (
        EvalQuestion,
        build_coverage_report,
        generate_persona_questions,
        generate_questions,
        load_work_items,
        run_eval,
        write_eval_json,
        write_eval_report,
    )
    from context_blocks.retrieval.pipeline import RetrievalPipeline
    from context_blocks.retrieval.synthesis import get_synthesizer

    entity_dir = output / "entities"
    if not entity_dir.exists():
        console.print(f"[red]Entity directory not found: {entity_dir}[/red]")
        console.print("Run 'cb extract' first to extract entities.")
        raise typer.Exit(1)

    if questions_file and not questions_file.exists():
        console.print(f"[red]Questions file not found: {questions_file}[/red]")
        raise typer.Exit(1)

    if not questions_file and not seed and not docs and not work_items:
        console.print("[red]Provide --questions-file or at least one of --seed, --docs, --work-items.[/red]")
        raise typer.Exit(1)

    if personas and not seed:
        console.print("[red]--personas requires --seed (persona checks need seed context).[/red]")
        raise typer.Exit(1)

    console.print(f"\n[bold]Context Blocks — KB Coverage Eval[/bold]\n")
    console.print(f"  KB:         {entity_dir}")
    if questions_file:
        console.print(f"  Questions:  {questions_file} (pre-curated)")
    else:
        if seed:
            console.print(f"  Seed:       {seed}")
        if docs:
            console.print(f"  Docs:       {docs}")
        if personas:
            console.print(f"  Personas:   {'custom: ' + str(persona_config) if persona_config else 'default (4 personas)'}")
        if work_items:
            console.print(f"  Work items: {work_items}")
        console.print(f"  Questions:  {questions} (seed+doc target)")
    console.print()

    async def _eval():
        import json

        overall_start = time.time()
        llm_key = os.environ.get("LLM_API_KEY", "")

        eval_questions = []

        if questions_file:
            # Load pre-curated questions from file
            console.print(f"[dim]Step 1: Loading questions from {questions_file}...[/dim]")
            raw = json.loads(questions_file.read_text(encoding="utf-8"))
            eval_questions = [
                EvalQuestion(
                    question=q["question"],
                    source=q.get("source", "curated"),
                    source_file=q.get("source_file", ""),
                    layer_hint=q.get("layer_hint", ""),
                    topic=q.get("topic", ""),
                    persona=q.get("persona", ""),
                )
                for q in raw
            ]
        else:
            # Generate questions from all sources
            console.print("[dim]Step 1: Generating eval questions...[/dim]")

            # 1a. Seed + doc questions
            if seed or docs:
                seed_q_count = min(10, questions // 3) if seed else 0
                doc_sample = min(15, questions - seed_q_count) if docs else 0

                base_questions = await generate_questions(
                    seed_path=seed,
                    docs_dir=docs,
                    target_count=questions,
                    seed_questions=seed_q_count,
                    docs_sample_size=doc_sample,
                    api_key=llm_key,
                )
                eval_questions.extend(base_questions)

            # 1b. Persona completeness checks
            if personas and seed:
                persona_qs = await generate_persona_questions(
                    seed_path=seed,
                    config_path=persona_config,
                    existing_questions=eval_questions,
                    api_key=llm_key,
                )
                eval_questions.extend(persona_qs)

            # 1c. Work items (DDC)
            if work_items:
                wi_questions = load_work_items(work_items)
                eval_questions.extend(wi_questions)

        # Summary of question sources
        source_counts: dict[str, int] = {}
        for q in eval_questions:
            source_counts[q.source] = source_counts.get(q.source, 0) + 1
        parts = [f"{count} {src}" for src, count in sorted(source_counts.items())]
        verb = "Loaded" if questions_file else "Generated"
        console.print(f"  {verb} [bold]{len(eval_questions)}[/bold] questions ({', '.join(parts)})")

        # Dry run: print questions and exit
        if dry_run:
            console.print(f"\n[bold]Generated Questions (dry run — no retrieval)[/bold]\n")
            current_source = ""
            for i, q in enumerate(eval_questions):
                # Print source header when it changes
                header = q.persona or q.source
                if header != current_source:
                    current_source = header
                    console.print(f"\n  [bold underline]{current_source}[/bold underline]")
                layer_tag = f" [{q.layer_hint}]" if q.layer_hint else ""
                # Show topic for work items (full content is long), question for others
                display = q.topic if q.source == "work-item" else q.question
                console.print(f"  {i+1:3d}. {display}{layer_tag}")

            # Save questions as JSON for review
            questions_path = output / "eval-questions.json"
            questions_data = [
                {
                    "question": q.question,
                    "source": q.source,
                    "source_file": q.source_file,
                    "persona": q.persona,
                    "layer_hint": q.layer_hint,
                    "topic": q.topic,
                }
                for q in eval_questions
            ]
            questions_path.write_text(json.dumps(questions_data, indent=2), encoding="utf-8")
            console.print(f"\n  Questions saved to: {questions_path}")
            console.print(f"  Review, edit if needed, then run without --dry-run to evaluate.\n")
            return

        # Always save questions for reproducibility
        if not questions_file:
            questions_path = output / "eval-questions.json"
            questions_data = [
                {
                    "question": q.question,
                    "source": q.source,
                    "source_file": q.source_file,
                    "persona": q.persona,
                    "layer_hint": q.layer_hint,
                    "topic": q.topic,
                }
                for q in eval_questions
            ]
            questions_path.write_text(json.dumps(questions_data, indent=2), encoding="utf-8")
            console.print(f"  Saved to: {questions_path}")

        # Step 2: Load KB + embeddings
        console.print("\n[dim]Step 2: Loading KB and embeddings...[/dim]")
        backend = InMemoryBackend()
        backend.load_from_entity_dir(entity_dir)
        console.print(f"  Loaded [bold]{backend.entity_count()}[/bold] entities")

        openai_key = os.environ.get("OPENAI_API_KEY")
        emb = get_embedder(provider=embedder, api_key=openai_key)
        count = await index_entities(backend, emb)
        console.print(f"  Embedded [bold]{count}[/bold] entities")

        synth = get_synthesizer(provider=provider, api_key=llm_key)
        pipeline = RetrievalPipeline(backend, embed_fn=emb.embed, synthesize_fn=synth)

        # Step 3: Run eval
        console.print(f"\n[dim]Step 3: Running {len(eval_questions)} questions through retrieval pipeline...[/dim]\n")
        results = await run_eval(eval_questions, pipeline)

        # Show progress inline
        for i, r in enumerate(results):
            icon = {"CLEAN": "✅", "INCOMPLETE": "⚠️ ", "MISSING": "❌"}.get(r.ddc_class, "")
            src_tag = f"[{r.question.source}]" if r.question.source in ("persona", "work-item") else ""
            console.print(
                f"  [{i+1:2d}/{len(results)}] {icon} {r.ddc_class:12s} "
                f"({r.total_ms:4d}ms, {r.entities_retrieved:2d} entities) "
                f"{src_tag} {r.question.question[:55]}"
            )

        # Step 4: Build report
        total_time = time.time() - overall_start
        report = build_coverage_report(results, total_time)

        # Write outputs
        report_path = output / "eval-report.md"
        json_path = output / "eval-results.json"
        write_eval_report(report, report_path)
        write_eval_json(results, json_path)

        # Summary
        console.print(f"\n[bold]Coverage Summary[/bold]\n")
        console.print(f"  ✅ CLEAN (answerable):       {report.clean_count:3d}  ({report.clean_pct}%)")
        console.print(f"  ⚠️  INCOMPLETE (partial):     {report.incomplete_count:3d}  ({report.incomplete_pct}%)")
        console.print(f"  ❌ MISSING (not answerable):  {report.missing_count:3d}  ({report.missing_pct}%)")

        if report.per_persona:
            console.print(f"\n  [bold]Per Persona:[/bold]")
            for persona, counts in sorted(report.per_persona.items()):
                total = sum(counts.values())
                pct = round(counts["CLEAN"] / total * 100) if total > 0 else 0
                console.print(f"    {persona:20s}  {pct:3d}% CLEAN  ({counts['CLEAN']}/{total})")

        console.print()
        console.print(f"  Time: {report.total_time_s}s | Est. cost: ${report.total_cost_estimate:.2f}")
        console.print(f"  Report: {report_path}")
        console.print(f"  JSON:   {json_path}")
        console.print()

    try:
        asyncio.run(_eval())
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted. Partial results may have been saved.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[red]Eval failed: {e}[/red]")
        console.print("[dim]Check your API keys and try again.[/dim]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# cb report
# ---------------------------------------------------------------------------
@app.command()
def report(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory with eval-results.json"),
    block: str = typer.Option(None, "--block", "-b", help="Context block name (overrides --output)"),
    dest: Path = typer.Option(None, "--dest", "-d", help="Output HTML file path (default: <output>/gap-report.html)"),
    open_browser: bool = typer.Option(True, "--open/--no-open", help="Open report in browser after generation"),
) -> None:
    """Generate a shareable HTML gap report from eval results."""
    from context_blocks.report import generate_report

    output = _resolve_output(block, output)
    eval_json = output / "eval-results.json"
    if not eval_json.exists():
        console.print(f"[red]Eval results not found: {eval_json}[/red]")
        console.print("Run 'cb eval' first to generate eval results.")
        raise typer.Exit(1)

    report_path = dest or (output / "gap-report.html")
    block_name = block or output.name

    console.print(f"\n[bold]Context Blocks — Gap Report[/bold]\n")
    console.print(f"  Eval data: {eval_json}")
    console.print(f"  Output:    {report_path}")
    console.print()

    stats = generate_report(eval_json, report_path, block_name)

    console.print(f"[bold green]Done![/bold green]")
    console.print(f"  Questions: {stats['total']}")
    console.print(f"  CLEAN: {stats['clean']} | INCOMPLETE: {stats['incomplete']} | MISSING: {stats['missing']}")
    console.print(f"  Personas: {stats['personas']}")
    console.print(f"  Gaps detected: {stats['gaps']}")
    console.print(f"  Report: {report_path}")
    console.print()

    if open_browser:
        import webbrowser

        webbrowser.open(f"file://{report_path.resolve()}")


# ---------------------------------------------------------------------------
# cb health-check
# ---------------------------------------------------------------------------
@app.command("health-check")
def health_check(
    docs: Path = typer.Argument(..., help="Directory of documents to analyze"),
    seed: Path = typer.Option(None, "--seed", "-s", help="Seed context file (improves extraction + questions)"),
    output: Path = typer.Option(Path("health-check-output"), "--output", "-o", help="Output directory for entities + report"),
    threshold: int = typer.Option(70, "--threshold", "-t", help="Minimum CLEAN coverage %% for exit code 0"),
    questions: int = typer.Option(30, "--questions", "-q", help="Target number of eval questions"),
    max_docs: int | None = typer.Option(None, "--max", "-m", help="Max documents to process"),
    provider: str = typer.Option("anthropic", "--provider", "-p", help="LLM provider for synthesis (anthropic/none)"),
    embedder: str = typer.Option("auto", "--embedder", "-e", help="Embedding provider (openai/fastembed/auto)"),
    open_browser: bool = typer.Option(True, "--open/--no-open", help="Open HTML report after generation"),
) -> None:
    """Run a full knowledge health check in one command: extract -> eval -> gap report.

    Takes a folder of documents and produces a complete knowledge health report — no prior
    'cb init' required. Exit code 0 if CLEAN coverage >= threshold, else 1.
    """
    import os

    from dotenv import load_dotenv

    load_dotenv()

    if not docs.exists() or not docs.is_dir():
        console.print(f"[red]Documents directory not found: {docs}[/red]")
        raise typer.Exit(1)

    output.mkdir(parents=True, exist_ok=True)

    # Extraction requires a seed context; synthesize a minimal one if none was provided.
    seed_path = seed
    if seed_path is None:
        seed_path = output / "_generated-seed.md"
        seed_path.write_text(
            "# Domain Knowledge Base\n\n"
            "General domain knowledge extracted for a health check. "
            "No seed context was provided.\n",
            encoding="utf-8",
        )
    elif not seed_path.exists():
        console.print(f"[red]Seed context file not found: {seed_path}[/red]")
        raise typer.Exit(1)

    console.print("\n[bold]Context Blocks — Knowledge Health Check[/bold]\n")
    console.print(f"  Documents: {docs}")
    console.print(f"  Output:    {output}")
    console.print(f"  Threshold: {threshold}% CLEAN")
    console.print()

    async def _health_check() -> None:
        from context_blocks.pipeline import run_phase1
        from context_blocks.report import generate_report
        from context_blocks.retrieval.evals import (
            generate_persona_questions,
            generate_questions,
            run_coverage_eval,
        )

        llm_key = os.environ.get("LLM_API_KEY", "")
        openai_key = os.environ.get("OPENAI_API_KEY")

        # ── Step 1: Extract ──
        console.print("[dim]Step 1/3: Extracting entities...[/dim]")

        def _on_progress(current: int, total: int, filename: str) -> None:
            console.print(f"  [{current}/{total}] {filename}")

        extraction = await run_phase1(
            docs_dir=docs,
            seed_context_path=seed_path,
            output_dir=output,
            max_documents=max_docs,
            on_progress=_on_progress,
        )
        total_entities = sum(len(r.entities) for r in extraction)
        console.print(f"  Extracted [bold]{total_entities}[/bold] entities from {len(extraction)} docs")

        entity_dir = output / "entities"
        if not entity_dir.exists() or total_entities == 0:
            console.print("[red]No entities extracted — cannot run health check.[/red]")
            raise typer.Exit(1)

        # ── Step 2: Generate questions + run coverage eval ──
        console.print("\n[dim]Step 2/3: Generating questions + evaluating coverage...[/dim]")
        eval_questions = await generate_questions(
            seed_path=seed_path,
            docs_dir=docs,
            target_count=questions,
            seed_questions=min(10, questions // 3),
            docs_sample_size=min(15, questions),
            api_key=llm_key,
        )
        persona_qs = await generate_persona_questions(
            seed_path=seed_path,
            config_path=None,
            existing_questions=eval_questions,
            api_key=llm_key,
        )
        eval_questions.extend(persona_qs)
        console.print(f"  Generated [bold]{len(eval_questions)}[/bold] questions")

        report = await run_coverage_eval(
            entity_dir=entity_dir,
            questions=eval_questions,
            output_dir=output,
            llm_provider=provider,
            embedder_provider=embedder,
            llm_api_key=llm_key,
            openai_api_key=openai_key,
        )

        # ── Step 3: HTML gap report ──
        console.print("\n[dim]Step 3/3: Generating gap report...[/dim]")
        html_path = output / "health-check-report.html"
        generate_report(output / "eval-results.json", html_path, "health-check")

        # ── Summary ──
        console.print("\n[bold]Knowledge Health Summary[/bold]\n")
        console.print(f"  Entities:  {total_entities}")
        console.print(
            f"  Coverage:  [bold]{report.clean_pct}%[/bold] CLEAN  "
            f"({report.incomplete_pct}% partial, {report.missing_pct}% missing)"
        )

        if report.per_persona:
            console.print("\n  [bold]Per persona:[/bold]")
            for persona, counts in sorted(report.per_persona.items()):
                total = sum(counts.values())
                pct = round(counts.get("CLEAN", 0) / total * 100) if total else 0
                console.print(f"    {persona:20s} {pct:3d}% CLEAN ({counts.get('CLEAN', 0)}/{total})")

        if report.all_gaps:
            console.print("\n  [bold]Top gaps:[/bold]")
            sev_rank = {"high": 0, "medium": 1, "low": 2}
            top = sorted(report.all_gaps, key=lambda g: sev_rank.get(g.severity, 3))[:5]
            for g in top:
                console.print(f"    [{g.severity:6s}] {g.description[:70]}")

        console.print()
        console.print(f"  Time: {report.total_time_s}s | Est. eval cost: ${report.total_cost_estimate:.2f}")
        console.print(f"  Report: {html_path}")

        if open_browser:
            import webbrowser

            webbrowser.open(f"file://{html_path.resolve()}")

        # Deployment gate: exit code reflects whether coverage met the threshold.
        if report.clean_pct >= threshold:
            console.print(f"\n[bold green]PASS[/bold green] — coverage {report.clean_pct}% >= threshold {threshold}%\n")
        else:
            console.print(
                f"\n[bold yellow]BELOW THRESHOLD[/bold yellow] — coverage {report.clean_pct}% < {threshold}%\n"
            )
            raise typer.Exit(1)

    try:
        asyncio.run(_health_check())
    except typer.Exit:
        raise
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[red]Health check failed: {e}[/red]")
        console.print("[dim]Check your API keys and try again.[/dim]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# cb export-obsidian
# ---------------------------------------------------------------------------
@app.command("export-obsidian")
def export_obsidian(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory with entities/"),
    block: str = typer.Option(None, "--block", "-b", help="Context block name (overrides --output)"),
    dest: Path = typer.Option(None, "--dest", "-d", help="Destination vault directory (default: <output>/obsidian-vault/)"),
) -> None:
    """Export KB entities as an Obsidian vault with wikilinks and a Map of Content."""
    from context_blocks.export_obsidian import export_obsidian as _export
    from context_blocks.ontology import set_active_ontology

    output = _resolve_output(block, output)
    set_active_ontology(_resolve_ontology(block))
    entity_dir = output / "entities"
    if not entity_dir.exists():
        console.print(f"[red]Entity directory not found: {entity_dir}[/red]")
        console.print("Run 'cb extract' first to extract entities.")
        raise typer.Exit(1)

    vault_dir = dest or (output / "obsidian-vault")

    console.print(f"\n[bold]Context Blocks — Obsidian Export[/bold]\n")
    console.print(f"  Source:      {entity_dir}")
    console.print(f"  Destination: {vault_dir}")
    console.print()

    stats = _export(entity_dir, vault_dir)

    console.print(f"[bold green]Done![/bold green]")
    console.print(f"  Entities exported: {stats['entities']}")
    console.print(f"  Relationships linked: {stats['relationships_linked']}")
    console.print(f"  Entity types: {stats['types']}")
    console.print(f"  Map of Content: {vault_dir / 'MOC.md'}")
    console.print(f"\nOpen in Obsidian: File → Open folder as vault → {vault_dir}")
    console.print()


# ---------------------------------------------------------------------------
# cb export-skill
# ---------------------------------------------------------------------------
@app.command("export-skill")
def export_skill_cmd(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory with entities/"),
    block: str = typer.Option(None, "--block", "-b", help="Context block name (overrides --output)"),
    dest: Path = typer.Option(None, "--dest", "-d", help="Output file path (default: <output>/domain-kb.md)"),
    title: str = typer.Option("Domain Knowledge Base", "--title", "-t", help="Title for the exported file"),
    max_tokens: int = typer.Option(None, "--max-tokens", help="Approximate token budget (truncates low-confidence entities)"),
) -> None:
    """Export KB as a single portable markdown file for AI agent context windows."""
    from context_blocks.export_skill import export_skill
    from context_blocks.ontology import set_active_ontology

    output = _resolve_output(block, output)
    set_active_ontology(_resolve_ontology(block))
    entity_dir = output / "entities"
    if not entity_dir.exists():
        console.print(f"[red]Entity directory not found: {entity_dir}[/red]")
        console.print("Run 'cb extract' first to extract entities.")
        raise typer.Exit(1)

    out_file = dest or (output / "domain-kb.md")

    console.print(f"\n[bold]Context Blocks — Skill Factory Export[/bold]\n")
    console.print(f"  Source:     {entity_dir}")
    console.print(f"  Output:     {out_file}")
    if max_tokens:
        console.print(f"  Max tokens: ~{max_tokens:,}")
    console.print()

    stats = export_skill(entity_dir, out_file, title=title, max_tokens=max_tokens)

    console.print(f"[bold green]Done![/bold green]")
    console.print(f"  Entities: {stats['entities']}")
    console.print(f"  Types: {stats['types']}")
    console.print(f"  Size: {stats['total_chars']:,} chars (~{stats['estimated_tokens']:,} tokens)")
    console.print(f"\nDrop {out_file.name} into your agent's system prompt or context window.")
    console.print()


@app.command("mcp")
def mcp_serve(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output directory with entities/"),
    block: str = typer.Option(None, "--block", "-b", help="Serve a single block (omit to serve all blocks)"),
    transport: str = typer.Option(None, "--transport", "-t", help="Transport: stdio (default), streamable-http, sse. Env: CB_MCP_TRANSPORT"),
    host: str = typer.Option(None, "--host", help="Host for HTTP transport. Env: CB_MCP_HOST"),
    port: int = typer.Option(None, "--port", "-p", help="Port for HTTP transport. Env: CB_MCP_PORT"),
) -> None:
    """Start the MCP server for AI agents to query the KB.

    Without --block: serves all blocks, agents discover them via list_blocks().
    With --block: serves a single block directly.

    Transport defaults to stdio. For remote agents (Copilot, web tools), use:
        cb mcp --transport streamable-http

    Configure via env vars: CB_MCP_TRANSPORT, CB_MCP_HOST, CB_MCP_PORT.
    """
    try:
        from context_blocks.mcp_server import run_server
    except ImportError:
        console.print("[red]MCP dependencies not installed.[/red]")
        console.print("Install with: pip install 'context-blocks[mcp]'")
        raise typer.Exit(1)

    kwargs = {}
    if transport:
        kwargs["transport"] = transport
    if host:
        kwargs["host"] = host
    if port:
        kwargs["port"] = port

    if block:
        output = _resolve_output(block, output)
        entity_dir = output / "entities"
        if not entity_dir.exists():
            console.print(f"[red]Entity directory not found: {entity_dir}[/red]")
            console.print("Run 'cb extract' first to extract entities.")
            raise typer.Exit(1)
        run_server(output_dir=str(output), **kwargs)
    else:
        run_server(**kwargs)


if __name__ == "__main__":
    app()
