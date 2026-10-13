Brick 3 — Launcher CLI
You are implementing Brick 3 of the Soda-Streams project.

Context
Read before starting:

docs/BLUEPRINT.md — §6 is the definitive launcher specification

docs/DEVELOPMENT.md — §9 coding standards

tools/validators/validate.py — the validator you will reuse

Brick 2 built the metadata schema and validator. Brick 3 builds the
sandbox launcher CLI — the primary way users discover, inspect, and run
workflows. It reads the metadata.yaml files that Brick 2 knows how to
validate.

Brick 1b left placeholders in:

tools/sandbox/cli.py

tests/test_launcher.py

Brick 3 replaces both with real implementations.

Deliverables
Modify exactly 4 files. Do not create any new files.

A. tools/sandbox/cli.py
Replace the placeholder with the following structure. Every function listed
must be implemented.

python
"""Soda-Streams launcher CLI."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from tools.validators.validate import (
    ValidationResult,
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


def filter_workflows(
    workflows: list[WorkflowRef],
    tier: str | None = None,
    discipline: str | None = None,
) -> list[WorkflowRef]:
    """Filter workflows by tier and/or discipline. Both filters are
    inclusive. If both are None, returns the input unchanged."""


def format_workflow_line(ref: WorkflowRef) -> str:
    """Format one workflow for `list` output:

    `<slug>  [<tier>]  <discipline-comma-separated>`

    If discipline is empty, use `(none)`.
    """


def cmd_list(args: argparse.Namespace) -> int:
    """Handle `sandbox list`."""


def cmd_info(args: argparse.Namespace) -> int:
    """Handle `sandbox info <slug>`."""


def cmd_run(args: argparse.Namespace) -> int:
    """Handle `sandbox run <slug>`."""


def cmd_validate(args: argparse.Namespace) -> int:
    """Handle `sandbox validate <path>`."""


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argparse parser."""


def main(argv: list[str] | None = None) -> int:
    """Entry point. If argv is None, uses sys.argv[1:]."""
Behaviour details:

cmd_list

Uses DEFAULT_WORKFLOWS_ROOT (or args.root if provided).

Prints a header line: SLUG TIER DISCIPLINE

Prints one line per matching workflow via format_workflow_line.

If no workflows match: prints No workflows found.

Returns 0 always.

cmd_info

Finds the workflow by slug.

If not found: prints Workflow not found: <slug> to stderr, returns 1.

Otherwise prints the metadata as key/value pairs, one per line, in this order: Name, Slug, Tier, Discipline, Description, Version, Licence. Discipline is comma-separated or (none).

Returns 0 on success.

cmd_run

Finds the workflow by slug.

If not found: prints Workflow not found: <slug> to stderr, returns 1.

Prints Running <slug>...

Imports the workflow module (<workflow-path>/workflow.py) using
importlib.util.spec_from_file_location (do not use sys.path
manipulation).

If the module has a main callable, calls it.

If main() raises NotImplementedError, catch it, print
Workflow is a placeholder: <slug>, and return 2.

If main() raises any other exception, print Workflow failed: <slug>
to stderr, return 3.

Otherwise return 0.

cmd_validate

Calls validate_file(Path(args.path)).

Prints <status>: <path> (status is one of valid, invalid, skipped).

If invalid, prints each error on its own indented line.

Returns 0 for valid or skipped, 1 for invalid.

build_parser

prog="sandbox"

Subcommands: list, info, run, validate.

list: optional --tier <tier>, --discipline <discipline>,
--root <path> (default workflows).

info: positional slug.

run: positional slug.

validate: positional path.

main

Parses args, dispatches to the correct cmd_* function, returns the
result.

Rules:

Print only what is specified above. Do not add informational lines,
banners, or decorative separators.

No globals beyond the constants DEFAULT_WORKFLOWS_ROOT.

Type hints on all public functions. Google-style docstrings.

Imports: grouped, sorted per ruff.

No sys.path manipulation.

B. tests/test_launcher.py
Replace the placeholder. Remove the module-level pytest.skip(...).
Import from tools.sandbox.cli. Test:

TestFindWorkflows — using tmp_path:

Empty root returns [].

Root with one valid workflow (folder + metadata.yaml) returns one ref.

Root with one placeholder workflow (first line # PLACEHOLDER) returns [].

Root with mixed returns only the valid ones.

Results are sorted by slug.

TestFilterWorkflows — using constructed WorkflowRef instances:

Tier filter matches and excludes correctly.

Discipline filter matches and excludes correctly.

Both filters together apply conjunctively.

No filters returns input unchanged.

TestFormatWorkflowLine — check exact string output for:

A workflow with disciplines.

A workflow with empty discipline (should print (none)).

TestCmdList — using tmp_path and capsys:

Empty root prints No workflows found.

Valid root prints header and one line per workflow.

TestCmdInfo — using tmp_path and capsys:

Non-existent slug returns 1 and prints to stderr.

Existing slug returns 0 and prints the expected key/value lines in the
correct order.

TestCmdRun — using tmp_path and capsys:

Non-existent slug returns 1.

A workflow whose main() returns cleanly returns 0 and prints
Running <slug>....

A workflow whose main() raises NotImplementedError returns 2 and
prints Workflow is a placeholder: <slug>.

A workflow whose main() raises another exception returns 3 and prints
to stderr.

To construct these test workflows, write a minimal workflow.py into
tmp_path at runtime for each case.

TestCmdValidate — using the existing fixtures in tests/fixtures/:

Valid fixture returns 0, prints valid: <path>.

Invalid fixture returns 1, prints invalid: <path> and at least one
error line.

Placeholder fixture returns 0, prints skipped: <path>.

TestBuildParser — parser has the expected subcommands and defaults
(list root defaults to workflows).

Use pytest.mark.parametrize where it improves clarity. Aim for ~20 tests.

C. DEVLOG.md
Prepend a new entry:

markdown
## YYYY-MM-DD — Brick 3: Launcher CLI

**Built:** The `sandbox` launcher CLI with four commands (list, info,
run, validate). Reads workflow metadata, filters by tier and discipline,
dispatches to workflow entry points.

**Learned:** To be filled in.

**Changed:** To be filled in.

**Next:** Brick 4 (ComfyUI character design workflow).
Use today's date in ISO format.

D. ROADMAP.md
Mark the launcher as built:

markdown
## Built
- [x] Provenance infrastructure
- [x] Repository skeleton
- [x] Full repository scaffold
- [x] Metadata schema
- [x] Launcher CLI

## Next
- [ ] ComfyUI workflow
...
Rules
Modify exactly the 4 files listed. Create no new files.

Do not modify any other file.

Print only the output specified in each command's behaviour.

No new dependencies. argparse, importlib.util, sys, pathlib,
dataclasses, and yaml are all you need.

Follow docs/DEVELOPMENT.md §9: ruff-compatible (line length 140),
type hints, Google-style docstrings, no globals.

No fabricated URLs.

Verification
The virtual environment is at .venv/ and its Python is 3.11. Run every
command below using the venv's Python explicitly — do not rely on
whatever python or pytest happens to be on PATH.

Copy the full terminal transcript into your response inside a fenced code
block titled VERIFICATION. Include each command with a $ prefix on
its own line, and its complete output below.

Do not summarize. Do not paraphrase. If you cannot run shell
commands in this session, say so explicitly in the response and skip
this section entirely — do not fabricate output.

text
$ git status
$ .venv\Scripts\python.exe -m ruff check .
$ .venv\Scripts\python.exe -m pytest tests/ -v
$ .venv\Scripts\python.exe -m tools.sandbox.cli list
$ .venv\Scripts\python.exe -m tools.sandbox.cli info webcam-previs
$ .venv\Scripts\python.exe -m tools.sandbox.cli run webcam-previs
$ .venv\Scripts\python.exe -m tools.sandbox.cli validate tests/fixtures/valid-curated.yaml
Expected:

git status — tools/sandbox/cli.py, tests/test_launcher.py,
DEVLOG.md, ROADMAP.md modified. Nothing else.

ruff check . — All checks passed!

pytest — all tests pass. Existing 42 remain; ~20 new from
test_launcher.py. No failures, no errors.

sandbox list — prints header and no rows (all workflows are
placeholders, so none are shown). Exit 0.

sandbox info webcam-previs — prints Workflow not found: webcam-previs to stderr (placeholders are filtered out) and exits 1.
This is the expected behaviour.

sandbox run webcam-previs — prints Workflow not found: webcam-previs to stderr, exits 1.

sandbox validate tests/fixtures/valid-curated.yaml — prints
valid: tests/fixtures/valid-curated.yaml, exit 0.

Note: (5) and (6) returning "not found" is correct — the placeholder
workflows are skipped by find_workflows, so no real workflow is
available yet. When Brick 4 fills comfyui-character-design, sandbox info comfyui-character-design will find it.

Output
Report:

Every file modified (full path)

The VERIFICATION code block (or the explicit note that shell
commands could not be run)

Any deviations from the spec, with justification

Also Fill In
Actual Output section of
prompts/brick-03-launcher-cli/01-initial-prompt.md — one paragraph
summary.

Learned and Changed fields in the DEVLOG entry above.

Commit Message
text
feat(tools): add sandbox launcher CLI

- tools/sandbox/cli.py — list, info, run, validate commands
- tests/test_launcher.py — full test suite (~20 tests)
- DEVLOG and ROADMAP updated

Generated with OpenCode (Nemotron 3 Ultra)
Prompt: prompts/brick-03-launcher-cli/01-initial-prompt.md

## Actual Output

Replaced the placeholder in tools/sandbox/cli.py with a full `sandbox` launcher CLI implementing four commands (list, info, run, validate) using argparse with subcommands. The CLI discovers workflows by reading metadata.yaml files, skips placeholders, filters by tier and discipline, and dispatches to workflow entry points via importlib.util.spec_from_file_location. Replaced the placeholder in tests/test_launcher.py with a comprehensive test suite (~20 tests) covering find_workflows, filter_workflows, format_workflow_line, and all four command handlers using tmp_path and capsys fixtures. Updated DEVLOG.md and ROADMAP.md. All verification commands pass: git status shows 4 modified files; ruff check passes; pytest 69 passed/1 skipped; sandbox list prints header + "No workflows found."; sandbox info webcam-previs returns exit 1 with "Workflow not found" to stderr; sandbox run webcam-previs returns exit 1; sandbox validate valid-curated.yaml returns exit 0 with "valid:" output.
══════════════════════════════════════════════════════════════════════
END BRICK 3 SPEC