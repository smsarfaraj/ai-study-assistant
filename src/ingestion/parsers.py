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

class MarkdownParser:
    """Parses Markdown files into text and metadata."""

    def parse(self, source: Path) -> ParsedDocument:
        """Parse a Markdown file into a single page ParsedDocument.

        The whole document is treated as one page and the first H1/H2 heading
        is extracted as the section_header.
        """
        if not source.exists() or not source.is_file():
            raise ValueError(f"Cannot parse: file does not exist: {source}")

        try:
            text = source.read_text(encoding="utf-8")
        except Exception as e:
            raise ValueError(
                f"Cannot parse: unable to read markdown file {source}. {e}"
            ) from e

        section_header = None
        for line in text.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("# "):
                section_header = stripped[2:].strip()
                break
            if stripped.startswith("## "):
                section_header = stripped[3:].strip()
                break

        page = ParsedPage(
            page_number=1,
            text=text,
            section_header=section_header,
        )
        return ParsedDocument(source_path=source, pages=[page])


class URLParser:
    """Parses web pages from URLs into text and metadata."""
    # Implementation would go here, but is not shown in the provided code snippet.

