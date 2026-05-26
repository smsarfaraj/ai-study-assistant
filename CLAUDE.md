# AI Study Assistant — Agent Context

This project uses Spec-Driven Development. Always read `.specify/memory/constitution.md` before making any architectural decisions.

## Project Structure
- `src/config.py` — all settings via Pydantic BaseSettings
- `src/ingestion/` — document parsing, chunking, embedding, ingestion pipeline
- `src/retrieval/` — retriever, LLM providers, cache, query pipeline
- `src/vector_store/` — VectorStoreProtocol + ChromaDB/InMemory adapters
- `src/api/` — FastAPI app with ingest/query/manage routes
- `src/cli/` — Typer CLI (`study` command)
- `src/mcp/` — fastmcp server exposing RAG tools
- `tests/unit/` — unit tests (use InMemoryAdapter, mock LLM calls)
- `tests/integration/` — integration tests (real pipelines, mock external APIs)
- `specs/001-rag-qa-bot/` — spec.md, plan.md, tasks.md

## Current Task
See `specs/001-rag-qa-bot/tasks.md` for the ordered task list. Always implement the lowest-numbered incomplete task.

## Running the project
```bash
uv sync
uv run study serve        # Start web server
uv run study ask "..."    # Query via CLI
uv run pytest             # Run tests
uv run ruff check src/    # Lint
uv run mypy src/          # Type-check
```

## Key Rules
- Run `pytest` before marking any task complete
- Never hardcode API keys — always use Settings from src/config.py
- Never break the VectorStoreProtocol or LLMProvider abstractions
- Structured output: all LLM responses must be validated against Pydantic schema

## Spec Kit Commands
- `/speckit.specify` — update the feature spec
- `/speckit.plan` — update the technical plan
- `/speckit.tasks` — regenerate task breakdown
- `/speckit.analyze` — cross-artifact consistency check
- `/speckit.implement` — implement next task from tasks.md
