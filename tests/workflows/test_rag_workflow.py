"""Smoke tests for the RAG research assistant workflow.

These tests do NOT require Ollama, Hugging Face downloads, or
network access. Test chunking, extraction, CLI parsing, and metadata —
not the heavy embedding/retrieval/generation functions.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from tools.validators.validate import validate_file

WORKFLOW_DIR = (
    Path(__file__).resolve().parents[2]
    / "workflows"
    / "text"
    / "rag-research-assistant"
)


class TestMetadata:
    """Metadata validation tests."""

    def test_metadata_validates(self) -> None:
        """Validate metadata.yaml against the schema via validate_file."""
        path = WORKFLOW_DIR / "metadata.yaml"
        result = validate_file(path)
        assert result.status == "valid"

    def test_tier_is_curated(self) -> None:
        """Tier is curated."""
        import yaml
        path = WORKFLOW_DIR / "metadata.yaml"
        metadata = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert metadata["tier"] == "curated"

    def test_discipline_includes_research(self) -> None:
        """Research in disciplines."""
        import yaml
        path = WORKFLOW_DIR / "metadata.yaml"
        metadata = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert "research" in metadata["discipline"]


class TestChunkText:
    """Tests for chunk_text using synthetic page lists."""

    def _load_module(self):
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        sys.modules["workflow"] = module
        spec.loader.exec_module(module)
        return module

    def test_single_short_page(self) -> None:
        """One page with short text → one chunk."""
        module = self._load_module()
        pages = [(1, "Short text here.")]
        chunks = module.chunk_text(pages, source="test.pdf")
        assert len(chunks) == 1
        assert chunks[0].text == "Short text here."
        assert chunks[0].page == 1
        assert chunks[0].source == "test.pdf"

    def test_long_page_produces_multiple_chunks(self) -> None:
        """One page with text longer than CHUNK_SIZE → multiple chunks."""
        module = self._load_module()
        long_text = "A" * 2500  # Longer than CHUNK_SIZE (1000)
        pages = [(1, long_text)]
        chunks = module.chunk_text(pages, source="test.pdf")
        assert len(chunks) > 1

    def test_overlap_respected(self) -> None:
        """The tail of chunk i appears at the start of chunk i+1."""
        module = self._load_module()
        text = "A" * 1500
        pages = [(1, text)]
        chunks = module.chunk_text(pages, source="test.pdf")
        assert len(chunks) >= 2
        # Check overlap: end of chunk 0 should match start of chunk 1
        overlap = module.CHUNK_OVERLAP
        assert chunks[1].text[:overlap] == chunks[0].text[-overlap:]

    def test_chunk_ids_deterministic(self) -> None:
        """Same input produces same IDs."""
        module = self._load_module()
        pages = [(1, "Deterministic test content.")]
        chunks1 = module.chunk_text(pages, source="test.pdf")
        chunks2 = module.chunk_text(pages, source="test.pdf")
        assert chunks1[0].chunk_id == chunks2[0].chunk_id

    def test_page_numbers_preserved(self) -> None:
        """Chunk page numbers come from input page list."""
        module = self._load_module()
        pages = [(1, "Page one content."), (2, "Page two content.")]
        chunks = module.chunk_text(pages, source="test.pdf")
        pages_in_chunks = {c.page for c in chunks}
        assert pages_in_chunks == {1, 2}

    def test_multiple_pages(self) -> None:
        """Chunks from page 2 have page=2."""
        module = self._load_module()
        pages = [(1, "A" * 500), (2, "B" * 500)]
        chunks = module.chunk_text(pages, source="test.pdf")
        page2_chunks = [c for c in chunks if c.page == 2]
        assert len(page2_chunks) > 0
        for c in page2_chunks:
            assert c.page == 2


class TestExtractText:
    """Tests for extract_text with a mock PdfReader."""

    def _load_module(self):
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        sys.modules["workflow"] = module
        spec.loader.exec_module(module)
        return module

    def test_returns_page_tuples(self) -> None:
        """Returns list of (page_number, text) tuples."""
        module = self._load_module()
        from unittest.mock import MagicMock, patch

        mock_reader = MagicMock()
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "Page one text"
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "Page two text"
        mock_reader.pages = [mock_page1, mock_page2]

        with patch.object(module, "PdfReader", return_value=mock_reader):
            result = module.extract_text(Path("dummy.pdf"))

        assert len(result) == 2
        assert result[0] == (1, "Page one text")
        assert result[1] == (2, "Page two text")

    def test_skips_empty_pages(self) -> None:
        """Pages whose extract_text() returns None or whitespace are excluded."""
        module = self._load_module()
        from unittest.mock import MagicMock, patch

        mock_reader = MagicMock()
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "Real content"
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = ""
        mock_page3 = MagicMock()
        mock_page3.extract_text.return_value = "   "
        mock_page4 = MagicMock()
        mock_page4.extract_text.return_value = None
        mock_page5 = MagicMock()
        mock_page5.extract_text.return_value = "More content"
        mock_reader.pages = [mock_page1, mock_page2, mock_page3, mock_page4, mock_page5]

        with patch.object(module, "PdfReader", return_value=mock_reader):
            result = module.extract_text(Path("dummy.pdf"))

        assert len(result) == 2
        assert result[0][1] == "Real content"
        assert result[1][1] == "More content"

    def test_page_numbers_are_one_indexed(self) -> None:
        """First page is number 1, not 0."""
        module = self._load_module()
        from unittest.mock import MagicMock, patch

        mock_reader = MagicMock()
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "First page"
        mock_reader.pages = [mock_page1]

        with patch.object(module, "PdfReader", return_value=mock_reader):
            result = module.extract_text(Path("dummy.pdf"))

        assert result[0][0] == 1


class TestBuildParser:
    """Tests for the CLI argument parser."""

    def _load_module(self):
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        sys.modules["workflow"] = module
        spec.loader.exec_module(module)
        return module

    def test_has_ingest_subcommand(self) -> None:
        """Parser has ingest."""
        module = self._load_module()
        parser = module.build_parser()
        args = parser.parse_args(["ingest", "--source", "test"])
        assert args.command == "ingest"
        assert args.source == "test"

    def test_has_query_subcommand(self) -> None:
        """Parser has query."""
        module = self._load_module()
        parser = module.build_parser()
        args = parser.parse_args(["query", "--question", "test"])
        assert args.command == "query"
        assert args.question == "test"

    def test_ingest_requires_source(self) -> None:
        """Parsing ingest without --source raises SystemExit."""
        module = self._load_module()
        parser = module.build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["ingest"])

    def test_query_requires_question(self) -> None:
        """Parsing query without --question raises SystemExit."""
        module = self._load_module()
        parser = module.build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["query"])


class TestCmdIngest:
    """Tests for cmd_ingest with tmp_path."""

    def _load_module(self):
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        sys.modules["workflow"] = module
        spec.loader.exec_module(module)
        return module

    def test_empty_source_returns_error(self, tmp_path: Path, capsys) -> None:
        """A directory with no PDFs → stderr contains 'No PDFs found', return 1."""
        module = self._load_module()
        from argparse import Namespace

        args = Namespace(
            source=str(tmp_path),
            index_dir=str(tmp_path / ".rag-index"),
            collection="research",
            embedding_model="all-MiniLM-L6-v2",
        )
        exit_code = module.cmd_ingest(args)
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "No PDFs found" in captured.err

    def test_nonexistent_source_returns_error(self, capsys) -> None:
        """A path that doesn't exist → return 1."""
        module = self._load_module()
        from argparse import Namespace

        args = Namespace(
            source=str(Path("nonexistent")),
            index_dir=str(Path("index")),
            collection="research",
            embedding_model="all-MiniLM-L6-v2",
        )
        exit_code = module.cmd_ingest(args)
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "does not exist" in captured.err


class TestCmdQuery:
    """Tests for cmd_query with tmp_path."""

    def _load_module(self):
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        sys.modules["workflow"] = module
        spec.loader.exec_module(module)
        return module

    def test_missing_index_returns_error(self, tmp_path: Path, capsys) -> None:
        """Index directory doesn't exist → stderr contains 'Index not found', return 1."""
        module = self._load_module()
        from argparse import Namespace

        args = Namespace(
            question="Test question",
            index_dir=str(tmp_path / "nonexistent"),
            collection="research",
            top_k=5,
            embedding_model="all-MiniLM-L6-v2",
            llm_model="llama3.2:3b",
        )
        exit_code = module.cmd_query(args)
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Index not found" in captured.err


class TestMain:
    """Tests for the main entry point."""

    def _load_module(self):
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        sys.modules["workflow"] = module
        spec.loader.exec_module(module)
        return module

    def test_no_args_prints_usage(self, capsys) -> None:
        """main([]) prints usage and returns 0."""
        module = self._load_module()
        exit_code = module.main([])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "usage" in captured.out.lower() or "ingest" in captured.out