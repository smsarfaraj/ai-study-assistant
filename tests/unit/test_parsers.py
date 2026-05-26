# tests/unit/test_parsers.py
from pathlib import Path
import pytest
from pathlib import Path
from src.ingestion.parsers import PDFParser


FIXTURES = Path(__file__).parent.parent / "fixtures"

class TestPDFParser:

    def test_parse_returns_pages_with_text(self):
        # Arrange
        from src.ingestion.parsers import PDFParser
        parser = PDFParser()
        
        # Act
        doc = parser.parse(FIXTURES / "sample-test.pdf")
        
        # Assert
        assert len(doc.pages) > 0
        assert all(len(p.text) > 0 for p in doc.pages)

    def test_parse_returns_page_numbers(self):
        from src.ingestion.parsers import PDFParser
        parser = PDFParser()
        doc = parser.parse(FIXTURES / "sample-test.pdf")
        
        # Page numbers should start at 1 and be sequential
        page_nums = [p.page_number for p in doc.pages]
        assert page_nums[0] == 1
        assert page_nums == list(range(1, len(doc.pages) + 1))

    def test_parse_corrupt_file_raises_cleanly(self):
        from src.ingestion.parsers import PDFParser
        parser = PDFParser()
        
        with pytest.raises(ValueError, match="Cannot parse"):
            parser.parse(Path("nonexistent.pdf"))

    def test_parse_invalid_pdf_raises_cleanly(self, tmp_path):
        fake = tmp_path / "fake.pdf"
        fake.write_text("not a pdf")
        
        with pytest.raises(ValueError, match="Cannot parse"):
            PDFParser().parse(fake)