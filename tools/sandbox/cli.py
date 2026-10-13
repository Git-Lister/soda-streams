"""Soda-Streams launcher CLI."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from tools.validators.validate import (
    is_placeholder,
    validate_file,
)

DEFAULT_WORKFLOWS_ROOT = Path("workflows")
"""Directory searched for workflow folders."""


@dataclass
class WorkflowRef:
    """A discovered workflow."""

    slug: str
    path: Path
    metadata: dict


def find_workflows(root: Path) -> list[WorkflowRef]:
    """Walk `root`, return a WorkflowRef for each folder containing a
    metadata.yaml whose first line is not `# PLACEHOLDER`.

    Sort results by slug for determinism.
    """
    workflows = []
    for metadata_path in sorted(root.rglob("metadata.yaml")):
        if is_placeholder(metadata_path):
            continue
        try:
            metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if metadata is None:
            continue
        slug = metadata.get("slug")
        if not slug:
            continue
        workflows.append(
            WorkflowRef(
                slug=slug,
                path=metadata_path.parent,
                metadata=metadata,
            )
        )
    return sorted(workflows, key=lambda w: w.slug)


def filter_workflows(
    workflows: list[WorkflowRef],
    tier: str | None = None,
    discipline: str | None = None,
) -> list[WorkflowRef]:
    """Filter workflows by tier and/or discipline. Both filters are
    inclusive. If both are None, returns the input unchanged.
    """
    if tier is None and discipline is None:
        return workflows
    result = []
    for w in workflows:
        if tier is not None and w.metadata.get("tier") != tier:
            continue
        if discipline is not None:
            disciplines = w.metadata.get("discipline", [])
            if discipline not in disciplines:
                continue
        result.append(w)
    return result


def format_workflow_line(ref: WorkflowRef) -> str:
    """Format one workflow for `list` output:

    `<slug>  [<tier>]  <discipline-comma-separated>`

    If discipline is empty, use `(none)`.
    """
    tier = ref.metadata.get("tier", "unknown")
    disciplines = ref.metadata.get("discipline", [])
    discipline_str = ",".join(disciplines) if disciplines else "(none)"
    return f"{ref.slug}  [{tier}]  {discipline_str}"


def cmd_list(args: argparse.Namespace) -> int:
    """Handle `sandbox list`."""
    root = Path(args.root) if args.root else DEFAULT_WORKFLOWS_ROOT
    workflows = find_workflows(root)
    workflows = filter_workflows(workflows, args.tier, args.discipline)

    print("SLUG  TIER  DISCIPLINE")
    if not workflows:
        print("No workflows found.")
        return 0

    for w in workflows:
        print(format_workflow_line(w))
    return 0


def cmd_info(args: argparse.Namespace, root: Path | None = None) -> int:
    """Handle `sandbox info <slug>`."""
    search_root = root or DEFAULT_WORKFLOWS_ROOT
    workflows = find_workflows(search_root)
    match = next((w for w in workflows if w.slug == args.slug), None)

    if match is None:
        print(f"Workflow not found: {args.slug}", file=sys.stderr)
        return 1

    m = match.metadata
    name = m.get("name", "")
    slug = m.get("slug", "")
    tier = m.get("tier", "")
    disciplines = m.get("discipline", [])
    discipline_str = ",".join(disciplines) if disciplines else "(none)"
    description = m.get("description", "")
    version = m.get("version", "")
    licence = m.get("licence", "")

    print(f"Name: {name}")
    print(f"Slug: {slug}")
    print(f"Tier: {tier}")
    print(f"Discipline: {discipline_str}")
    print(f"Description: {description}")
    print(f"Version: {version}")
    print(f"Licence: {licence}")
    return 0


def cmd_run(args: argparse.Namespace, root: Path | None = None) -> int:
    """Handle `sandbox run <slug>`."""
    search_root = root or DEFAULT_WORKFLOWS_ROOT
    workflows = find_workflows(search_root)
    match = next((w for w in workflows if w.slug == args.slug), None)

    if match is None:
        print(f"Workflow not found: {args.slug}", file=sys.stderr)
        return 1

    print(f"Running {args.slug}...")
    workflow_py = match.path / "workflow.py"

    if not workflow_py.exists():
        print(f"Workflow failed: {args.slug}", file=sys.stderr)
        return 3

    try:
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        if spec is None or spec.loader is None:
            print(f"Workflow failed: {args.slug}", file=sys.stderr)
            return 3
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        main_func = getattr(module, "main", None)
        if main_func is None:
            print(f"Workflow failed: {args.slug}", file=sys.stderr)
            return 3
        main_func()
    except NotImplementedError:
        print(f"Workflow is a placeholder: {args.slug}")
        return 2
    except Exception:
        print(f"Workflow failed: {args.slug}", file=sys.stderr)
        return 3

    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Handle `sandbox validate <path>`."""
    path = Path(args.path)
    result = validate_file(path)

    print(f"{result.status}: {path}")
    if result.status == "invalid":
        for error in result.errors:
            print(f"  {error}")

    return 0 if result.status != "invalid" else 1


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argparse parser."""
    parser = argparse.ArgumentParser(prog="sandbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--tier", choices=["curated", "community", "experimental"])
    list_parser.add_argument("--discipline")
    list_parser.add_argument("--root", type=str)

    # info
    info_parser = subparsers.add_parser("info")
    info_parser.add_argument("slug", type=str)

    # run
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("slug", type=str)

    # validate
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("path", type=str)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point. If argv is None, uses sys.argv[1:]."""
    if argv is None:
        argv = sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list":
        return cmd_list(args)
    if args.command == "info":
        return cmd_info(args, DEFAULT_WORKFLOWS_ROOT)
    if args.command == "run":
        return cmd_run(args, DEFAULT_WORKFLOWS_ROOT)
    if args.command == "validate":
        return cmd_validate(args)

    return 1


if __name__ == "__main__":
    sys.exit(main())