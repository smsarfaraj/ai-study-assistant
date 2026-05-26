# Project Constitution
> Governing principles — every agent command must respect this file

## Project: AI Study Assistant
RAG-based Q&A bot for AI certification study materials (Google AI Professional, Google AI Leader, AWS AI Practitioner, Claude Certified Architect CCA-F, GitHub Copilot GH-300, GitHub Foundations GH-900).

## Technology Stack (Non-Negotiable)
- Language: Python 3.11+
- Web Framework: FastAPI
- Vector Store: ChromaDB (behind VectorStoreProtocol abstraction)
- LLM: Google Gemini 1.5 Flash AND Claude claude-haiku-4-5-20251001 (both co-primary, switchable via LLM_PROVIDER env var)
- Embeddings: Google text-embedding-004
- MCP Server: fastmcp (first-class interface, not optional)
- CLI: Typer + Rich
- Testing: pytest + pytest-asyncio
- CI/CD: GitHub Actions
- Package Manager: uv

## Architecture Constraints
1. VectorStore behind VectorStoreProtocol — no direct ChromaDB calls in business logic
2. LLM behind LLMProvider protocol — model switch = config change only
3. MCP server is required — exposes query/ingest/list_sources/stats as MCP tools
4. All LLM responses validated against Pydantic JSON schema (structured output)
5. Ingestion is atomic — rollback all chunks if any step fails
6. Async all the way — no blocking calls in async paths
7. GitHub flow — feature branches + PRs, no direct commits to main

## Coding Standards
- Type hints everywhere, Google-style docstrings on all public functions
- No magic strings — all config via src/config.py Settings
- Explicit error handling — no bare Exception catches
- Tests required — every public function has at least one unit test

## RAG Constraints
- Chunk size: 512 tokens, overlap: 64 tokens
- Retrieval top-K: 5, min score: 0.7
- Every answer must include source citations tagged with which cert they're relevant to
- Hallucination guard: if no relevant context, say so explicitly
