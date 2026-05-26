"""
Application configuration using Pydantic BaseSettings.

All values are loaded from environment variables or .env file.
No configuration values should be hardcoded anywhere else in the codebase.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for AI Study Assistant.

    All settings are sourced from environment variables or .env file.
    See .env.example for full documentation of each variable.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── LLM Provider ─────────────────────────────────────────────────────────
    llm_provider: Literal["gemini", "claude"] = Field(
        default="gemini",
        description="Which LLM provider to use for answer generation.",
    )
    google_api_key: str = Field(
        default="",
        description="Google AI API key for Gemini and text-embedding-004.",
    )
    anthropic_api_key: str = Field(
        default="",
        description="Anthropic API key for Claude.",
    )
    gemini_model: str = Field(
        default="gemini-1.5-flash",
        description="Gemini model identifier.",
    )
    claude_model: str = Field(
        default="claude-haiku-4-5-20251001",
        description="Claude model identifier.",
    )

    # ── Embeddings ────────────────────────────────────────────────────────────
    embedding_model: str = Field(
        default="text-embedding-004",
        description="Embedding model name.",
    )
    embedding_provider: Literal["google", "nomic"] = Field(
        default="google",
        description="Embedding provider. 'nomic' uses local Ollama as fallback.",
    )

    # ── Chunking ──────────────────────────────────────────────────────────────
    chunk_size: int = Field(
        default=512,
        ge=64,
        le=2048,
        description="Maximum tokens per chunk.",
    )
    chunk_overlap: int = Field(
        default=64,
        ge=0,
        description="Token overlap between consecutive chunks.",
    )

    # ── Retrieval ─────────────────────────────────────────────────────────────
    retrieval_top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of chunks to retrieve per query.",
    )
    retrieval_min_score: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum cosine similarity score for a chunk to be included.",
    )
    context_window_limit_pct: float = Field(
        default=0.8,
        ge=0.1,
        le=1.0,
        description="Maximum fraction of the model's context window to use for retrieved chunks.",
    )

    # ── Cache ─────────────────────────────────────────────────────────────────
    cache_ttl_seconds: int = Field(
        default=3600,
        ge=0,
        description="Time-to-live for cached query results in seconds. 0 = no cache.",
    )
    cache_similarity_threshold: float = Field(
        default=0.98,
        ge=0.0,
        le=1.0,
        description="Cosine similarity threshold for a cache hit.",
    )

    # ── Storage ───────────────────────────────────────────────────────────────
    chroma_persist_dir: Path = Field(
        default=Path("./data/chroma"),
        description="Directory where ChromaDB persists its data.",
    )
    upload_max_size_mb: int = Field(
        default=50,
        ge=1,
        le=500,
        description="Maximum allowed file upload size in megabytes.",
    )

    # ── Server ───────────────────────────────────────────────────────────────
    host: str = Field(default="0.0.0.0", description="FastAPI bind host.")
    port: int = Field(default=8000, ge=1, le=65535, description="FastAPI bind port.")

    # ── Derived properties ───────────────────────────────────────────────────
    @property
    def upload_max_size_bytes(self) -> int:
        """Upload size limit in bytes for FastAPI file validation."""
        return self.upload_max_size_mb * 1024 * 1024

    @property
    def chroma_collection_name(self) -> str:
        """ChromaDB collection name (constant)."""
        return "study_materials"

    # ── Validation ────────────────────────────────────────────────────────────
    @model_validator(mode="after")
    def validate_overlap_less_than_chunk(self) -> "Settings":
        """chunk_overlap must be strictly less than chunk_size."""
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                f"chunk_overlap ({self.chunk_overlap}) must be less than "
                f"chunk_size ({self.chunk_size})"
            )
        return self

    @model_validator(mode="after")
    def validate_api_key_for_provider(self) -> "Settings":
        """Warn if the selected provider has no API key configured."""
        if self.llm_provider == "gemini" and not self.google_api_key:
            raise ValueError(
                "llm_provider is 'gemini' but GOOGLE_API_KEY is not set. "
                "Add it to your .env file."
            )
        if self.llm_provider == "claude" and not self.anthropic_api_key:
            raise ValueError(
                "llm_provider is 'claude' but ANTHROPIC_API_KEY is not set. "
                "Add it to your .env file."
            )
        return self

    @model_validator(mode="after")
    def validate_embedding_key(self) -> "Settings":
        """Google embedding provider requires a Google API key."""
        if self.embedding_provider == "google" and not self.google_api_key:
            raise ValueError(
                "embedding_provider is 'google' but GOOGLE_API_KEY is not set."
            )
        return self


# ── Singleton ────────────────────────────────────────────────────────────────
_settings: Settings | None = None


def get_settings() -> Settings:
    """Return the cached Settings singleton.

    Uses module-level caching so the .env file is read only once.
    In tests, use Settings() directly with explicit values.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
