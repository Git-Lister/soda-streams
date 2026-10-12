"""Tests for the archive_prompt.py helper script."""

import datetime
import os
import time
from pathlib import Path

import pytest

from tools.provenance.archive_prompt import (
    create_prompt_file,
    create_session_log,
    main,
    pad_brick_number,
    print_footer,
    slugify,
)


class TestSlugify:
    """Tests for the slugify function."""

    def test_simple_title(self) -> None:
        """Test slugification of a simple title."""
        assert slugify("Provenance infrastructure") == "provenance-infrastructure"

    def test_title_with_punctuation(self) -> None:
        """Test slugification handles punctuation."""
        assert slugify("Hello, World!") == "hello-world"

    def test_title_with_multiple_spaces(self) -> None:
        """Test slugification handles multiple spaces."""
        assert slugify("Multiple   spaces") == "multiple-spaces"

    def test_title_with_leading_trailing_spaces(self) -> None:
        """Test slugification strips leading/trailing hyphens."""
        assert slugify("  Leading and trailing  ") == "leading-and-trailing"

    def test_title_already_slugified(self) -> None:
        """Test slugification of an already slugified string."""
        assert slugify("already-slugified") == "already-slugified"

    def test_title_with_numbers(self) -> None:
        """Test slugification preserves numbers."""
        assert slugify("Brick 42 Test") == "brick-42-test"


class TestPadBrickNumber:
    """Tests for the pad_brick_number function."""

    def test_zero(self) -> None:
        """Test padding of zero."""
        assert pad_brick_number(0) == "00"

    def test_single_digit(self) -> None:
        """Test padding of single digit."""
        assert pad_brick_number(4) == "04"

    def test_double_digit(self) -> None:
        """Test padding of double digit."""
        assert pad_brick_number(12) == "12"

    def test_larger_number(self) -> None:
        """Test padding of larger number (no truncation)."""
        assert pad_brick_number(99) == "99"


class TestCreatePromptFile:
    """Tests for the create_prompt_file function."""

    def test_creates_prompt_file(self, tmp_path: Path) -> None:
        """Test that the prompt file is created with correct content."""
        today = datetime.date.today().isoformat()
        prompt_file = create_prompt_file(
            brick_slug="brick-00-provenance-infrastructure",
            padded_number="00",
            original_title="Provenance infrastructure",
            model="Nemotron 3 Ultra",
            today_iso=today,
            base_path=tmp_path,
        )

        assert prompt_file.exists()
        content = prompt_file.read_text(encoding="utf-8")
        assert "Brick 00 — Provenance infrastructure" in content
        assert f"**Date:** {today}" in content
        assert "**Model:** Nemotron 3 Ultra" in content
        assert "logs/opencode/" in content

    def test_does_not_overwrite_existing(self, tmp_path: Path) -> None:
        """Test that existing prompt file is not overwritten."""
        today = datetime.date.today().isoformat()
        # Create first
        create_prompt_file(
            brick_slug="brick-00-provenance-infrastructure",
            padded_number="00",
            original_title="Provenance infrastructure",
            model="Nemotron 3 Ultra",
            today_iso=today,
            base_path=tmp_path,
        )
        # Modify the file
        prompt_file = tmp_path / "prompts" / "brick-00-provenance-infrastructure" / "01-initial-prompt.md"        
        prompt_file.write_text("MODIFIED CONTENT", encoding="utf-8")

        # Call again
        result = create_prompt_file(
            brick_slug="brick-00-provenance-infrastructure",
            padded_number="00",
            original_title="Provenance infrastructure",
            model="Nemotron 3 Ultra",
            today_iso=today,
            base_path=tmp_path,
        )

        # Should return the existing file
        assert result == prompt_file
        # Content should remain modified (not overwritten)
        assert prompt_file.read_text(encoding="utf-8") == "MODIFIED CONTENT"


class TestCreateSessionLog:
    """Tests for the create_session_log function."""

    def test_creates_session_log(self, tmp_path: Path) -> None:
        """Test that the session log file is created with correct content."""
        today = datetime.date.today().isoformat()
        log_file = create_session_log(
            brick_slug="brick-00-provenance-infrastructure",
            padded_number="00",
            original_title="Provenance infrastructure",
            model="Nemotron 3 Ultra",
            today_iso=today,
            base_path=tmp_path,
        )

        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "Session: Brick 00 — Provenance infrastructure" in content
        assert f"**Date:** {today}" in content
        assert "**Model:** Nemotron 3 Ultra" in content
        assert "prompts/brick-00-provenance-infrastructure/01-initial-prompt.md" in content

    def test_does_not_overwrite_existing(self, tmp_path: Path) -> None:
        """Test that existing session log file is not overwritten."""
        today = datetime.date.today().isoformat()
        # Create first
        create_session_log(
            brick_slug="brick-00-provenance-infrastructure",
            padded_number="00",
            original_title="Provenance infrastructure",
            model="Nemotron 3 Ultra",
            today_iso=today,
            base_path=tmp_path,
        )
        # Modify the file
        log_file = tmp_path / "logs" / "opencode" / f"{today}-brick-00.md"
        log_file.write_text("MODIFIED CONTENT", encoding="utf-8")

        # Call again
        result = create_session_log(
            brick_slug="brick-00-provenance-infrastructure",
            padded_number="00",
            original_title="Provenance infrastructure",
            model="Nemotron 3 Ultra",
            today_iso=today,
            base_path=tmp_path,
        )

        # Should return the existing file
        assert result == log_file
        # Content should remain modified (not overwritten)
        assert log_file.read_text(encoding="utf-8") == "MODIFIED CONTENT"


class TestPrintFooter:
    """Tests for the print_footer function."""

    def test_prints_footer(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that the footer is printed correctly."""
        prompt_file = tmp_path / "prompts" / "brick-00-provenance-infrastructure" / "01-initial-prompt.md"
        log_file = tmp_path / "logs" / "opencode" / "2026-10-12-brick-00.md"
        prompt_file.parent.mkdir(parents=True, exist_ok=True)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        prompt_file.write_text("", encoding="utf-8")
        log_file.write_text("", encoding="utf-8")

        print_footer(prompt_file, log_file, "Nemotron 3 Ultra", tmp_path)

        captured = capsys.readouterr()
        # Use pathlib to normalize paths for cross-platform comparison
        expected_prompt = str(prompt_file.relative_to(tmp_path))
        expected_log = str(log_file.relative_to(tmp_path))
        assert f"Created: {expected_prompt}" in captured.out
        assert f"Created: {expected_log}" in captured.out
        assert "Commit footer:" in captured.out
        assert "Generated with OpenCode (Nemotron 3 Ultra)" in captured.out
        assert f"Prompt: {expected_prompt}" in captured.out


class TestMain:
    """Tests for the main function."""

    def test_main_creates_files(self, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that main creates the expected files and prints footer."""
        monkeypatch.chdir(tmp_path)

        # Mock sys.argv
        import sys
        original_argv = sys.argv
        sys.argv = ["archive_prompt.py", "--brick", "0", "--prompt", "Provenance infrastructure", "--model", "Nemotron 3 Ultra"]

        try:
            exit_code = main()
        finally:
            sys.argv = original_argv

        assert exit_code == 0

        # Check files created
        prompt_file = tmp_path / "prompts" / "brick-00-provenance-infrastructure" / "01-initial-prompt.md"
        log_file = tmp_path / "logs" / "opencode" / f"{datetime.date.today().isoformat()}-brick-00.md"

        assert prompt_file.exists()
        assert log_file.exists()

        # Check stdout
        captured = capsys.readouterr()
        expected_prompt = "prompts/brick-00-provenance-infrastructure/01-initial-prompt.md".replace("/", os.sep)
        expected_log_prefix = f"logs{os.sep}opencode{os.sep}"
        assert f"Created: {expected_prompt}" in captured.out
        assert f"Created: {expected_log_prefix}" in captured.out
        assert "Generated with OpenCode (Nemotron 3 Ultra)" in captured.out

    def test_main_skips_existing_files(self, tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that main skips files that already exist."""
        monkeypatch.chdir(tmp_path)

        # Pre-create the files
        today = datetime.date.today().isoformat()
        prompt_dir = tmp_path / "prompts" / "brick-00-provenance-infrastructure"
        prompt_dir.mkdir(parents=True, exist_ok=True)
        prompt_file = prompt_dir / "01-initial-prompt.md"
        prompt_file.write_text("EXISTING", encoding="utf-8")

        log_dir = tmp_path / "logs" / "opencode"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{today}-brick-00.md"
        log_file.write_text("EXISTING", encoding="utf-8")

        # Ensure mtime is old enough for the "existed" check (1 second threshold)
        time.sleep(1.1)

        import sys
        original_argv = sys.argv
        sys.argv = ["archive_prompt.py", "--brick", "0", "--prompt", "Provenance infrastructure", "--model", "Nemotron 3 Ultra"]

        try:
            exit_code = main()
        finally:
            sys.argv = original_argv

        assert exit_code == 0

        captured = capsys.readouterr()
        expected_prompt = "prompts/brick-00-provenance-infrastructure/01-initial-prompt.md".replace("/", os.sep)
        expected_log = f"logs{os.sep}opencode{os.sep}{today}-brick-00.md"
        assert f"Skipped (exists): {expected_prompt}" in captured.out
        assert f"Skipped (exists): {expected_log}" in captured.out
        assert "All target files exist. No action needed." in captured.out