"""Unit tests for src/config.py."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.config import Settings


def _base_settings(**overrides: object) -> Settings:
    """Create a Settings instance with valid defaults, apply overrides."""
    defaults = {
        "google_api_key": "fake-google-key",
        "anthropic_api_key": "fake-anthropic-key",
        "llm_provider": "gemini",
    }
    defaults.update(overrides)
    return Settings(**defaults)  # type: ignore[arg-type]


class TestDefaults:
    def test_default_llm_provider(self) -> None:
        s = _base_settings()
        assert s.llm_provider == "gemini"

    def test_default_chunk_size(self) -> None:
        s = _base_settings()
        assert s.chunk_size == 512

    def test_default_chunk_overlap(self) -> None:
        s = _base_settings()
        assert s.chunk_overlap == 64

    def test_default_retrieval_top_k(self) -> None:
        s = _base_settings()
        assert s.retrieval_top_k == 5

    def test_default_retrieval_min_score(self) -> None:
        s = _base_settings()
        assert s.retrieval_min_score == 0.7

    def test_default_cache_ttl(self) -> None:
        s = _base_settings()
        assert s.cache_ttl_seconds == 3600

    def test_chroma_collection_name(self) -> None:
        s = _base_settings()
        assert s.chroma_collection_name == "study_materials"


class TestDerivedProperties:
    def test_upload_max_size_bytes(self) -> None:
        s = _base_settings(upload_max_size_mb=50)
        assert s.upload_max_size_bytes == 50 * 1024 * 1024

    def test_upload_max_size_bytes_custom(self) -> None:
        s = _base_settings(upload_max_size_mb=10)
        assert s.upload_max_size_bytes == 10 * 1024 * 1024


class TestValidation:
    def test_chunk_overlap_must_be_less_than_chunk_size(self) -> None:
        with pytest.raises(ValidationError, match="chunk_overlap"):
            _base_settings(chunk_size=100, chunk_overlap=100)

    def test_chunk_overlap_equal_to_chunk_size_fails(self) -> None:
        with pytest.raises(ValidationError):
            _base_settings(chunk_size=256, chunk_overlap=256)

    def test_chunk_overlap_less_than_chunk_size_passes(self) -> None:
        s = _base_settings(chunk_size=256, chunk_overlap=32)
        assert s.chunk_size == 256
        assert s.chunk_overlap == 32

    def test_gemini_provider_requires_google_key(self) -> None:
        with pytest.raises(ValidationError, match="GOOGLE_API_KEY"):
            Settings(llm_provider="gemini", google_api_key="")  # type: ignore[call-arg]

    def test_claude_provider_requires_anthropic_key(self) -> None:
        with pytest.raises(ValidationError, match="ANTHROPIC_API_KEY"):
            Settings(llm_provider="claude", anthropic_api_key="", google_api_key="fake")  # type: ignore[call-arg]

    def test_google_embedding_requires_google_key(self) -> None:
        with pytest.raises(ValidationError, match="GOOGLE_API_KEY"):
            Settings(  # type: ignore[call-arg]
                llm_provider="gemini",
                google_api_key="",
                embedding_provider="google",
            )

    def test_invalid_llm_provider_rejected(self) -> None:
        with pytest.raises(ValidationError):
            _base_settings(llm_provider="openai")  # type: ignore[arg-type]

    def test_retrieval_min_score_out_of_range(self) -> None:
        with pytest.raises(ValidationError):
            _base_settings(retrieval_min_score=1.5)

    def test_chunk_size_below_minimum(self) -> None:
        with pytest.raises(ValidationError):
            _base_settings(chunk_size=10)


class TestEnvOverride:
    def test_claude_provider_with_key(self) -> None:
        # When using Claude as LLM + nomic for embeddings, no Google key is needed.
        s = _base_settings(
            llm_provider="claude",
            anthropic_api_key="real-key",
            google_api_key="",
            embedding_provider="nomic",
        )
        assert s.llm_provider == "claude"
        assert s.anthropic_api_key == "real-key"

    def test_custom_models(self) -> None:
        s = _base_settings(
            gemini_model="gemini-2.0-flash",
            claude_model="claude-opus-4-6",
        )
        assert s.gemini_model == "gemini-2.0-flash"
        assert s.claude_model == "claude-opus-4-6"
