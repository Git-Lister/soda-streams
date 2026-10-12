"""Tests for the metadata validator."""

from pathlib import Path

import pytest

from tools.validators.validate import (
    is_placeholder,
    load_schema,
    validate_all,
    validate_file,
)


class TestIsPlaceholder:
    """Tests for is_placeholder function."""

    def test_placeholder_fixture(self) -> None:
        """Returns True for a placeholder fixture."""
        path = Path("tests/fixtures/placeholder.yaml")
        assert is_placeholder(path) is True

    def test_valid_metadata_fixture(self) -> None:
        """Returns False for a real metadata fixture."""
        path = Path("tests/fixtures/valid-curated.yaml")
        assert is_placeholder(path) is False

    def test_non_existent_file(self) -> None:
        """Returns False for a non-existent file."""
        path = Path("tests/fixtures/does-not-exist.yaml")
        assert is_placeholder(path) is False


class TestLoadSchema:
    """Tests for load_schema function."""

    def test_loads_schema_with_required_keys(self) -> None:
        """Loading schema.json returns a dict with $schema and title keys."""
        schema = load_schema()
        assert isinstance(schema, dict)
        assert "$schema" in schema
        assert "title" in schema
        assert schema["title"] == "Soda-Streams workflow metadata"


class TestValidateFile:
    """Tests for validate_file function."""

    @pytest.mark.parametrize(
        "fixture",
        [
            "valid-curated.yaml",
            "valid-community.yaml",
            "valid-experimental.yaml",
        ],
    )
    def test_valid_fixtures(self, fixture: str) -> None:
        """Valid fixtures return 'valid' status."""
        path = Path(f"tests/fixtures/{fixture}")
        result = validate_file(path)
        assert result.status == "valid"
        assert result.errors == []

    def test_placeholder_fixture_skipped(self) -> None:
        """Placeholder fixture returns 'skipped' status."""
        path = Path("tests/fixtures/placeholder.yaml")
        result = validate_file(path)
        assert result.status == "skipped"
        assert result.errors == []

    @pytest.mark.parametrize(
        "fixture,expected_error_substring",
        [
            ("invalid-missing-name.yaml", "name"),
            ("invalid-bad-tier.yaml", "tier"),
            ("invalid-bad-version.yaml", "version"),
            ("invalid-missing-provenance.yaml", "provenance"),
            ("invalid-bad-slug.yaml", "slug"),
            ("invalid-bad-discipline.yaml", "discipline"),
        ],
    )
    def test_invalid_fixtures(
        self, fixture: str, expected_error_substring: str
    ) -> None:
        """Invalid fixtures return 'invalid' with specific error."""
        path = Path(f"tests/fixtures/{fixture}")
        result = validate_file(path)
        assert result.status == "invalid"
        assert len(result.errors) == 1
        assert expected_error_substring in result.errors[0].lower()

    def test_non_existent_file(self) -> None:
        """Non-existent file returns 'skipped' with file not found error."""
        path = Path("tests/fixtures/does-not-exist.yaml")
        result = validate_file(path)
        assert result.status == "skipped"
        assert "file not found" in result.errors[0].lower()


class TestValidateAll:
    """Tests for validate_all function."""

    def test_validate_all_with_mixed_files(
        self, tmp_path: Path
    ) -> None:
        """Returns three results with correct statuses, sorted by path."""
        # Create test tree with metadata.yaml files in subdirectories
        valid_dir = tmp_path / "valid"
        valid_dir.mkdir()
        valid_file = valid_dir / "metadata.yaml"
        valid_file.write_text(
            """name: "Test"
slug: "test"
author: "Git-Lister"
tier: "experimental"
discipline:
  - "games"
description: "Test"
version: "0.0.1"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )

        placeholder_dir = tmp_path / "placeholder"
        placeholder_dir.mkdir()
        placeholder_file = placeholder_dir / "metadata.yaml"
        placeholder_file.write_text(
            "# PLACEHOLDER\nname: Test\n",
            encoding="utf-8",
        )

        invalid_dir = tmp_path / "invalid"
        invalid_dir.mkdir()
        invalid_file = invalid_dir / "metadata.yaml"
        invalid_file.write_text(
            """slug: "missing-name"
author: "Git-Lister"
tier: "community"
discipline:
  - "games"
description: "Missing name"
version: "1.0.0"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )

        results = validate_all(tmp_path)

        assert len(results) == 3
        # Results should be sorted by path
        assert results[0].path == invalid_file
        assert results[1].path == placeholder_file
        assert results[2].path == valid_file

        statuses = [r.status for r in results]
        assert statuses == ["invalid", "skipped", "valid"]


class TestErrorMessages:
    """Tests that error messages name the offending field."""

    def test_missing_name_error(self) -> None:
        """Error message mentions 'name' field."""
        path = Path("tests/fixtures/invalid-missing-name.yaml")
        result = validate_file(path)
        assert "name" in result.errors[0].lower()

    def test_bad_tier_error(self) -> None:
        """Error message mentions 'tier' field."""
        path = Path("tests/fixtures/invalid-bad-tier.yaml")
        result = validate_file(path)
        assert "tier" in result.errors[0].lower()

    def test_bad_version_error(self) -> None:
        """Error message mentions 'version' field."""
        path = Path("tests/fixtures/invalid-bad-version.yaml")
        result = validate_file(path)
        assert "version" in result.errors[0].lower()

    def test_missing_provenance_error(self) -> None:
        """Error message mentions 'provenance' field."""
        path = Path("tests/fixtures/invalid-missing-provenance.yaml")
        result = validate_file(path)
        assert "provenance" in result.errors[0].lower()

    def test_bad_slug_error(self) -> None:
        """Error message mentions 'slug' field."""
        path = Path("tests/fixtures/invalid-bad-slug.yaml")
        result = validate_file(path)
        assert "slug" in result.errors[0].lower()

    def test_bad_discipline_error(self) -> None:
        """Error message mentions 'discipline' field."""
        path = Path("tests/fixtures/invalid-bad-discipline.yaml")
        result = validate_file(path)
        assert "discipline" in result.errors[0].lower()


class TestMain:
    """Tests for validate_all.py main() function."""

    def test_main_valid_only(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """main() with valid-only tree returns 0."""
        # Create valid file
        valid_dir = tmp_path / "valid"
        valid_dir.mkdir()
        valid_file = valid_dir / "metadata.yaml"
        valid_file.write_text(
            """name: "Test"
slug: "test"
author: "Git-Lister"
tier: "experimental"
discipline:
  - "games"
description: "Test"
version: "0.0.1"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )

        monkeypatch.chdir(tmp_path)
        import tools.validators.validate_all as validate_all_module

        exit_code = validate_all_module.main(["validate_all.py"])

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "✓ valid:" in captured.out
        assert "Summary: 1 valid, 0 skipped, 0 invalid" in captured.out

    def test_main_with_invalid(self, tmp_path: Path, monkeypatch, capsys) -> None:
        """main() with any invalid file returns 1."""
        # Create valid and invalid files
        valid_dir = tmp_path / "valid"
        valid_dir.mkdir()
        valid_file = valid_dir / "metadata.yaml"
        valid_file.write_text(
            """name: "Test"
slug: "test"
author: "Git-Lister"
tier: "experimental"
discipline:
  - "games"
description: "Test"
version: "0.0.1"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )

        invalid_dir = tmp_path / "invalid"
        invalid_dir.mkdir()
        invalid_file = invalid_dir / "metadata.yaml"
        invalid_file.write_text(
            """slug: "missing-name"
author: "Git-Lister"
tier: "community"
discipline:
  - "games"
description: "Missing name"
version: "1.0.0"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )

        monkeypatch.chdir(tmp_path)
        import tools.validators.validate_all as validate_all_module

        exit_code = validate_all_module.main(["validate_all.py"])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "✗ invalid:" in captured.out
        assert "Summary: 1 valid, 0 skipped, 1 invalid" in captured.out


class TestSchema:
    """Tests for the schema itself."""

    def test_schema_has_required_structure(self) -> None:
        """Schema has required top-level keys."""
        schema = load_schema()
        assert "$schema" in schema
        assert "title" in schema
        assert "type" in schema
        assert schema["type"] == "object"
        assert "required" in schema
        assert "properties" in schema
        assert "additionalProperties" in schema
        assert schema["additionalProperties"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])