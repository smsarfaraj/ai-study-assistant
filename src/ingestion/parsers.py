"""
Document parsers for PDF, Markdown, and URL sources.

Each parser implements the DocumentParser protocol and returns a ParsedDocument
containing a list of ParsedPage objects with text and metadata.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import fitz  # PyMuPDF


@dataclass
class ParsedPage:
    """A single page extracted from a document."""

    page_number: int          # 1-indexed
    text: str
    section_header: str | None = None  # nearest heading found on this page


@dataclass
class ParsedDocument:
    """A fully parsed document with all pages."""

    source_path: Path
    pages: list[ParsedPage] = field(default_factory=list)


class PDFParser:
    """Parses PDF files using PyMuPDF (fitz)."""

    def parse(self, source: Path) -> ParsedDocument:
        """Parse a PDF file into pages with text and metadata.

        Args:
            source: Path to the PDF file.

        Returns:
            ParsedDocument with one ParsedPage per page.

        Raises:
            ValueError: If file doesn't exist or cannot be parsed as a PDF.
        """
        if not source.exists() or not source.is_file():
            raise ValueError(f"Cannot parse: file does not exist: {source}")

        try:
            with fitz.open(str(source)) as doc:
                parsed_pages = []
                for page in doc:
                    parsed_pages.append(
                        ParsedPage(
                            page_number=page.number + 1,
                            text=page.get_text(),
                            section_header=None,
                        )
                    )
                return ParsedDocument(source_path=source, pages=parsed_pages)
        except Exception as e:
            raise ValueError(
                f"Cannot parse: {source} is not a valid PDF. {e}"
            ) from e
