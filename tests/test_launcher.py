"""Tests for the sandbox CLI."""

from pathlib import Path

import pytest

from tools.sandbox.cli import (
    WorkflowRef,
    build_parser,
    cmd_info,
    cmd_list,
    cmd_run,
    cmd_validate,
    filter_workflows,
    find_workflows,
    format_workflow_line,
)


class TestFindWorkflows:
    """Tests for find_workflows function."""

    def test_empty_root(self, tmp_path: Path) -> None:
        """Empty root returns empty list."""
        result = find_workflows(tmp_path)
        assert result == []

    def test_single_valid_workflow(self, tmp_path: Path) -> None:
        """Root with one valid workflow returns one ref."""
        wf_dir = tmp_path / "test-workflow"
        wf_dir.mkdir()
        metadata = wf_dir / "metadata.yaml"
        metadata.write_text(
            """name: "Test Workflow"
slug: "test-workflow"
author: "Git-Lister"
tier: "experimental"
discipline:
  - "games"
description: "A test workflow"
version: "0.0.1"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )

        result = find_workflows(tmp_path)
        assert len(result) == 1
        assert result[0].slug == "test-workflow"
        assert result[0].path == wf_dir
        assert result[0].metadata["name"] == "Test Workflow"

    def test_placeholder_workflow_skipped(self, tmp_path: Path) -> None:
        """Root with one placeholder workflow returns empty list."""
        wf_dir = tmp_path / "placeholder-workflow"
        wf_dir.mkdir()
        metadata = wf_dir / "metadata.yaml"
        metadata.write_text(
            "# PLACEHOLDER\nname: Placeholder\n",
            encoding="utf-8",
        )

        result = find_workflows(tmp_path)
        assert result == []

    def test_mixed_valid_and_placeholder(self, tmp_path: Path) -> None:
        """Root with mixed returns only valid ones."""
        # Valid workflow
        valid_dir = tmp_path / "valid-workflow"
        valid_dir.mkdir()
        metadata = valid_dir / "metadata.yaml"
        metadata.write_text(
            """name: "Valid Workflow"
slug: "valid-workflow"
author: "Git-Lister"
tier: "experimental"
discipline:
  - "games"
description: "A valid workflow"
version: "0.0.1"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )

        # Placeholder workflow
        placeholder_dir = tmp_path / "placeholder-workflow"
        placeholder_dir.mkdir()
        metadata = placeholder_dir / "metadata.yaml"
        metadata.write_text(
            "# PLACEHOLDER\nname: Placeholder\n",
            encoding="utf-8",
        )

        result = find_workflows(tmp_path)
        assert len(result) == 1
        assert result[0].slug == "valid-workflow"

    def test_sorted_by_slug(self, tmp_path: Path) -> None:
        """Results are sorted by slug."""
        for slug in ["zebra-workflow", "alpha-workflow", "beta-workflow"]:
            wf_dir = tmp_path / slug
            wf_dir.mkdir()
            metadata = wf_dir / "metadata.yaml"
            yaml_content = (
                f'name: "{slug}"\n'
                f'slug: "{slug}"\n'
                'author: "Git-Lister"\n'
                'tier: "experimental"\n'
                'discipline:\n'
                '  - "games"\n'
                'description: "A workflow"\n'
                'version: "0.0.1"\n'
                'licence: "MIT"\n'
                'provenance: {}\n'
            )
            metadata.write_text(yaml_content, encoding="utf-8")

        result = find_workflows(tmp_path)
        slugs = [w.slug for w in result]
        assert slugs == ["alpha-workflow", "beta-workflow", "zebra-workflow"]


class TestFilterWorkflows:
    """Tests for filter_workflows function."""

    def make_ref(self, slug: str, tier: str, disciplines: list[str]) -> WorkflowRef:
        """Helper to create a WorkflowRef."""
        return WorkflowRef(
            slug=slug,
            path=Path("dummy"),
            metadata={"tier": tier, "discipline": disciplines},
        )

    def test_tier_filter(self) -> None:
        """Tier filter matches and excludes correctly."""
        workflows = [
            self.make_ref("a", "curated", ["games"]),
            self.make_ref("b", "community", ["games"]),
            self.make_ref("c", "experimental", ["games"]),
        ]
        result = filter_workflows(workflows, tier="community")
        assert len(result) == 1
        assert result[0].slug == "b"

    def test_discipline_filter(self) -> None:
        """Discipline filter matches and excludes correctly."""
        workflows = [
            self.make_ref("a", "experimental", ["games"]),
            self.make_ref("b", "experimental", ["filmmaking"]),
            self.make_ref("c", "experimental", ["games", "filmmaking"]),
        ]
        result = filter_workflows(workflows, discipline="filmmaking")
        assert len(result) == 2
        assert {r.slug for r in result} == {"b", "c"}

    def test_both_filters(self) -> None:
        """Both filters together apply conjunctively."""
        workflows = [
            self.make_ref("a", "curated", ["games"]),
            self.make_ref("b", "curated", ["filmmaking"]),
            self.make_ref("c", "community", ["games"]),
        ]
        result = filter_workflows(workflows, tier="curated", discipline="games")
        assert len(result) == 1
        assert result[0].slug == "a"

    def test_no_filters(self) -> None:
        """No filters returns input unchanged."""
        workflows = [
            self.make_ref("a", "curated", ["games"]),
            self.make_ref("b", "community", ["filmmaking"]),
        ]
        result = filter_workflows(workflows)
        assert result == workflows


class TestFormatWorkflowLine:
    """Tests for format_workflow_line function."""

    def test_with_disciplines(self) -> None:
        """Formats correctly with disciplines."""
        ref = WorkflowRef(
            slug="test-workflow",
            path=Path("dummy"),
            metadata={"tier": "curated", "discipline": ["games", "filmmaking"]},
        )
        line = format_workflow_line(ref)
        assert line == "test-workflow  [curated]  games,filmmaking"

    def test_empty_discipline(self) -> None:
        """Formats correctly with empty discipline (prints (none))."""
        ref = WorkflowRef(
            slug="test-workflow",
            path=Path("dummy"),
            metadata={"tier": "experimental", "discipline": []},
        )
        line = format_workflow_line(ref)
        assert line == "test-workflow  [experimental]  (none)"


class TestCmdList:
    """Tests for cmd_list function."""

    def test_empty_root(self, tmp_path: Path, capsys) -> None:
        """Empty root prints No workflows found."""
        from argparse import Namespace

        args = Namespace(tier=None, discipline=None, root=str(tmp_path))
        exit_code = cmd_list(args)
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "No workflows found." in captured.out

    def test_valid_root(self, tmp_path: Path, capsys) -> None:
        """Valid root prints header and one line per workflow."""
        from argparse import Namespace

        wf_dir = tmp_path / "test-workflow"
        wf_dir.mkdir()
        metadata = wf_dir / "metadata.yaml"
        metadata.write_text(
            """name: "Test Workflow"
slug: "test-workflow"
author: "Git-Lister"
tier: "experimental"
discipline:
  - "games"
description: "A test workflow"
version: "0.0.1"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )

        args = Namespace(tier=None, discipline=None, root=str(tmp_path))
        exit_code = cmd_list(args)
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "SLUG  TIER  DISCIPLINE" in captured.out
        assert "test-workflow  [experimental]  games" in captured.out


class TestCmdInfo:
    """Tests for cmd_info function."""

    def test_nonexistent_slug(self, tmp_path: Path, capsys) -> None:
        """Non-existent slug returns 1 and prints to stderr."""
        from argparse import Namespace

        args = Namespace(slug="nonexistent")
        exit_code = cmd_info(args)
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Workflow not found: nonexistent" in captured.err

    def test_existing_slug(self, tmp_path: Path, capsys) -> None:
        """Existing slug returns 0 and prints expected key/value lines."""
        from argparse import Namespace

        wf_dir = tmp_path / "test-workflow"
        wf_dir.mkdir()
        metadata = wf_dir / "metadata.yaml"
        metadata.write_text(
            """name: "Test Workflow"
slug: "test-workflow"
author: "Git-Lister"
tier: "curated"
discipline:
  - "games"
  - "filmmaking"
description: "A test workflow"
version: "1.0.0"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )

        args = Namespace(slug="test-workflow")
        exit_code = cmd_info(args, tmp_path)
        assert exit_code == 0
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert lines[0] == "Name: Test Workflow"
        assert lines[1] == "Slug: test-workflow"
        assert lines[2] == "Tier: curated"
        assert lines[3] == "Discipline: games,filmmaking"
        assert lines[4] == "Description: A test workflow"
        assert lines[5] == "Version: 1.0.0"
        assert lines[6] == "Licence: MIT"


class TestCmdRun:
    """Tests for cmd_run function."""

    def test_nonexistent_slug(self, tmp_path: Path, capsys) -> None:
        """Non-existent slug returns 1."""
        from argparse import Namespace

        args = Namespace(slug="nonexistent")
        exit_code = cmd_run(args, tmp_path)
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Workflow not found: nonexistent" in captured.err

    def test_valid_workflow(self, tmp_path: Path, capsys) -> None:
        """Workflow whose main() returns cleanly returns 0."""
        from argparse import Namespace

        wf_dir = tmp_path / "test-workflow"
        wf_dir.mkdir()
        metadata = wf_dir / "metadata.yaml"
        metadata.write_text(
            """name: "Test Workflow"
slug: "test-workflow"
author: "Git-Lister"
tier: "experimental"
discipline:
  - "games"
description: "A test workflow"
version: "0.0.1"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )
        workflow_py = wf_dir / "workflow.py"
        workflow_py.write_text(
            """def main() -> None:
    print("Hello from workflow")
""",
            encoding="utf-8",
        )

        args = Namespace(slug="test-workflow")
        exit_code = cmd_run(args, tmp_path)
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Running test-workflow..." in captured.out
        assert "Hello from workflow" in captured.out

    def test_placeholder_workflow(self, tmp_path: Path, capsys) -> None:
        """Workflow whose main() raises NotImplementedError returns 2."""
        from argparse import Namespace

        wf_dir = tmp_path / "test-workflow"
        wf_dir.mkdir()
        metadata = wf_dir / "metadata.yaml"
        metadata.write_text(
            """name: "Test Workflow"
slug: "test-workflow"
author: "Git-Lister"
tier: "experimental"
discipline:
  - "games"
description: "A test workflow"
version: "0.0.1"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )
        workflow_py = wf_dir / "workflow.py"
        workflow_py.write_text(
            """def main() -> None:
    raise NotImplementedError("Filled in Brick 4.")
""",
            encoding="utf-8",
        )

        args = Namespace(slug="test-workflow")
        exit_code = cmd_run(args, tmp_path)
        assert exit_code == 2
        captured = capsys.readouterr()
        assert "Running test-workflow..." in captured.out
        assert "Workflow is a placeholder: test-workflow" in captured.out

    def test_failing_workflow(self, tmp_path: Path, capsys) -> None:
        """Workflow whose main() raises another exception returns 3."""
        from argparse import Namespace

        wf_dir = tmp_path / "test-workflow"
        wf_dir.mkdir()
        metadata = wf_dir / "metadata.yaml"
        metadata.write_text(
            """name: "Test Workflow"
slug: "test-workflow"
author: "Git-Lister"
tier: "experimental"
discipline:
  - "games"
description: "A test workflow"
version: "0.0.1"
licence: "MIT"
provenance: {}
""",
            encoding="utf-8",
        )
        workflow_py = wf_dir / "workflow.py"
        workflow_py.write_text(
            """def main() -> None:
    raise ValueError("Something went wrong")
""",
            encoding="utf-8",
        )

        args = Namespace(slug="test-workflow")
        exit_code = cmd_run(args, tmp_path)
        assert exit_code == 3
        captured = capsys.readouterr()
        assert "Running test-workflow..." in captured.out
        assert "Workflow failed: test-workflow" in captured.err


class TestCmdValidate:
    """Tests for cmd_validate function."""

    def test_valid_fixture(self, capsys) -> None:
        """Valid fixture returns 0, prints valid."""
        from argparse import Namespace

        args = Namespace(path="tests/fixtures/valid-curated.yaml")
        exit_code = cmd_validate(args)
        assert exit_code == 0
        captured = capsys.readouterr()
        # Handle Windows path separators
        expected = "valid: " + str(Path("tests/fixtures/valid-curated.yaml"))
        assert expected in captured.out

    def test_invalid_fixture(self, capsys) -> None:
        """Invalid fixture returns 1, prints invalid and error."""
        from argparse import Namespace

        args = Namespace(path="tests/fixtures/invalid-missing-name.yaml")
        exit_code = cmd_validate(args)
        assert exit_code == 1
        captured = capsys.readouterr()
        expected = "invalid: " + str(Path("tests/fixtures/invalid-missing-name.yaml"))
        assert expected in captured.out
        assert "name" in captured.out.lower()

    def test_placeholder_fixture(self, capsys) -> None:
        """Placeholder fixture returns 0, prints skipped."""
        from argparse import Namespace

        args = Namespace(path="tests/fixtures/placeholder.yaml")
        exit_code = cmd_validate(args)
        assert exit_code == 0
        captured = capsys.readouterr()
        expected = "skipped: " + str(Path("tests/fixtures/placeholder.yaml"))
        assert expected in captured.out


class TestBuildParser:
    """Tests for build_parser function."""

    def test_subcommands_exist(self) -> None:
        """Parser has the expected subcommands."""
        parser = build_parser()
        # Parse each subcommand to verify they exist
        for cmd in ["list", "info", "run", "validate"]:
            args = parser.parse_args([cmd] + (["dummy"] if cmd != "list" else []))
            assert args.command == cmd

    def test_list_defaults(self) -> None:
        """List command has correct defaults."""
        parser = build_parser()
        args = parser.parse_args(["list"])
        assert args.tier is None
        assert args.discipline is None
        assert args.root is None

    def test_info_requires_slug(self) -> None:
        """Info command requires slug argument."""
        parser = build_parser()
        args = parser.parse_args(["info", "test-slug"])
        assert args.slug == "test-slug"

    def test_run_requires_slug(self) -> None:
        """Run command requires slug argument."""
        parser = build_parser()
        args = parser.parse_args(["run", "test-slug"])
        assert args.slug == "test-slug"

    def test_validate_requires_path(self) -> None:
        """Validate command requires path argument."""
        parser = build_parser()
        args = parser.parse_args(["validate", "tests/fixtures/valid-curated.yaml"])
        assert args.path == "tests/fixtures/valid-curated.yaml"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])