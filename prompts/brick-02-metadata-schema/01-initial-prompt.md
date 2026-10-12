"""Metadata validation for Soda-Streams workflows."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import jsonschema
import yaml

Status = Literal["valid", "invalid", "skipped"]

PLACEHOLDER_MARKER = "# PLACEHOLDER"
"""Files whose first non-blank line is this marker are skipped."""

SCHEMA_PATH = Path(__file__).parent / "schema.json"
"""Default location of the JSON Schema."""


@dataclass
class ValidationResult:
    """Outcome of validating one metadata file."""

    path: Path
    status: Status
    errors: list[str] = field(default_factory=list)


def load_schema(path: Path = SCHEMA_PATH) -> dict:
    """Load the JSON Schema from disk."""


def is_placeholder(path: Path) -> bool:
    """Return True if the file's first non-blank line is `# PLACEHOLDER`."""


def validate_file(path: Path, schema: dict | None = None) -> ValidationResult:
    """Validate a single metadata.yaml against the schema.

    Returns a ValidationResult with status:
    - "skipped" if the file is a placeholder or does not exist
    - "invalid" if the file fails to parse or fails schema validation
    - "valid" otherwise
    """


def validate_all(root: Path) -> list[ValidationResult]:
    """Walk `root`, find every metadata.yaml, validate each.

    Returns a list of ValidationResult, one per file found.
    """
Behaviour requirements:

load_schema reads JSON from path and returns a dict.

is_placeholder: read the file as text; strip leading whitespace and
blank lines; return True if the first non-blank line starts with
# PLACEHOLDER (exact case).

validate_file:

If path does not exist: return ValidationResult(path, "skipped", ["file not found"]).

If is_placeholder(path): return ValidationResult(path, "skipped").

Parse YAML. On yaml.YAMLError: return ValidationResult(path, "invalid", [str(exc)]).

Run jsonschema.validate(instance, schema). On jsonschema.ValidationError: collect a single error string in the form <path>: <message> (JSON Pointer path + validator message).

Otherwise return ValidationResult(path, "valid").

validate_all: use root.rglob("metadata.yaml"). Sort results by path for determinism.

No globals. Do not read env vars. Configuration is passed as arguments.

Type hints on all public functions. Google-style docstrings.

C. tools/validators/validate_all.py
Replace the placeholder with a CLI wrapper:

python
"""CLI entry point: validate all metadata.yaml files in the repository."""

from __future__ import annotations

import sys
from pathlib import Path

from tools.validators.validate import ValidationResult, validate_all


def format_result(result: ValidationResult) -> str:
    """Format a single ValidationResult for terminal output."""


def main(argv: list[str] | None = None) -> int:
    """Walk from the repository root and validate every metadata.yaml.

    Returns 0 if no invalid results, 1 otherwise.
    """
Behaviour:

Default root is the current working directory.

Print a header Validating metadata files... then one line per result:

valid: ✓ valid: <path>

skipped: - skipped: <path>

invalid: ✗ invalid: <path>, followed by one indented line per
error: - <error>

Print a summary line: Summary: N valid, M skipped, K invalid

Exit code: 0 if K == 0, 1 otherwise.

If validate_all returns nothing (no files found), print
No metadata.yaml files found. and exit 0.

D. tests/test_metadata_validation.py
Replace the placeholder with real tests. The file must remove the
module-level pytest.skip(...) call.

Import from tools.validators.validate. Use tests/fixtures/ for
fixture files. Use tmp_path for fixtures that need to be written at
runtime.

Required test cases (group into classes; aim for ~15 tests):

TestIsPlaceholder — returns True for a placeholder fixture; returns
False for a real metadata fixture.

TestValidateFile — validates each valid fixture as "valid"; skips
the placeholder fixture; returns "invalid" with a specific error for
each invalid fixture; returns "skipped" with file not found for a
non-existent path.

TestValidateAll — with a tmp_path tree containing one valid, one
placeholder, one invalid file, returns three results with correct
statuses; results are sorted by path.

TestErrorMessages — each invalid fixture produces an error message
that names the offending field or the specific schema violation.

TestMain — main() with a valid-only tree returns 0; main() with
any invalid file returns 1. Use monkeypatch.chdir and capsys.

TestSchema — loading schema.json returns a dict with "$schema"
and "title" keys.

Use pytest.mark.parametrize where it improves clarity.

E. Fixtures — 10 files in tests/fixtures/
Create exactly these. Contents are prescriptive — do not invent variations.

valid-curated.yaml

yaml
name: "Character Design with ComfyUI"
slug: "comfyui-character-design"
author: "Git-Lister"
contributors:
  - "example-contributor"
tier: "curated"
discipline:
  - "games"
  - "filmmaking"
  - "fine-art"
description: "Generate character concept art with ComfyUI using a curated Stable Diffusion workflow."
version: "1.0.0"
licence: "MIT"
tools:
  - name: "ComfyUI"
    version: ">=0.2.0"
    source: "https://github.com/comfyanonymous/ComfyUI"
    licence: "GPL-3.0"
dependencies:
  - "torch>=2.1.0"
entry_point: "workflow.py:main"
runtime: "python"
provenance:
  models:
    - name: "SDXL Base 1.0"
      source: "Stability AI"
      licence: "CreativeML-Open-RAIL++-M"
      training_data: "LAION-5B"
  ai_assistance:
    - tool: "OpenCode (Nemotron 3 Ultra)"
      role: "code generation"
created: "2026-01-15"
updated: "2026-01-15"
contributor_handle: "Git-Lister"
valid-community.yaml

yaml
name: "Storyboard Sketcher"
slug: "storyboard-sketcher"
author: "Git-Lister"
tier: "community"
discipline:
  - "filmmaking"
description: "Generate rough storyboard frames from a script excerpt."
version: "0.1.0"
licence: "MIT"
provenance: {}
valid-experimental.yaml

yaml
name: "Colour Palette Generator"
slug: "colour-palette-generator"
author: "Git-Lister"
tier: "experimental"
discipline:
  - "fine-art"
description: "Experimental palette generation from reference images."
version: "0.0.1"
licence: "CC-BY-4.0"
provenance: {}
placeholder.yaml

yaml
# PLACEHOLDER — test fixture. This file should be skipped by the validator.
# The first non-blank line is the marker.

name: "Placeholder"
slug: "placeholder"
author: "test"
tier: "experimental"
discipline:
  - "games"
description: "Should never be validated."
version: "0.0.1"
licence: "MIT"
provenance: {}
invalid-missing-name.yaml

yaml
slug: "missing-name"
author: "Git-Lister"
tier: "community"
discipline:
  - "games"
description: "Missing the required `name` field."
version: "1.0.0"
licence: "MIT"
provenance: {}
invalid-bad-tier.yaml

yaml
name: "Bad Tier"
slug: "bad-tier"
author: "Git-Lister"
tier: "super-curated"
discipline:
  - "games"
description: "Tier is not one of the allowed values."
version: "1.0.0"
licence: "MIT"
provenance: {}
invalid-bad-version.yaml

yaml
name: "Bad Version"
slug: "bad-version"
author: "Git-Lister"
tier: "community"
discipline:
  - "games"
description: "Version is not semantic."
version: "1.0"
licence: "MIT"
provenance: {}
invalid-missing-provenance.yaml

yaml
name: "Missing Provenance"
slug: "missing-provenance"
author: "Git-Lister"
tier: "community"
discipline:
  - "games"
description: "No provenance block."
version: "1.0.0"
licence: "MIT"
invalid-bad-slug.yaml

yaml
name: "Bad Slug"
slug: "Bad Slug With Spaces"
author: "Git-Lister"
tier: "community"
discipline:
  - "games"
description: "Slug is not kebab-case."
version: "1.0.0"
licence: "MIT"
provenance: {}
invalid-bad-discipline.yaml

yaml
name: "Bad Discipline"
slug: "bad-discipline"
author: "Git-Lister"
tier: "community"
discipline:
  - "basket-weaving"
description: "Discipline tag is not in the allowed set."
version: "1.0.0"
licence: "MIT"
provenance: {}
F. Updates to existing files
DEVLOG.md — prepend a new entry:

markdown
## YYYY-MM-DD — Brick 2: Metadata schema and validator

**Built:** JSON Schema for workflow metadata, Python validator
(validate.py, validate_all.py), 10 test fixtures, and full test suite
for the validator.

**Learned:** To be filled in.

**Changed:** To be filled in.

**Next:** Brick 3 (launcher CLI).
Use today's date (ISO format).

ROADMAP.md — mark metadata schema as built:

markdown
## Built
- [x] Provenance infrastructure
- [x] Repository skeleton
- [x] Full repository scaffold
- [x] Metadata schema

## Next
- [ ] Launcher CLI
...
Rules
Modify exactly the 4 files listed (schema.json, validate.py,
validate_all.py, test_metadata_validation.py) plus DEVLOG.md and
ROADMAP.md.

Create exactly the 10 fixture files listed.

Do not modify any other file.

Do not invent new fields in the schema. The schema above is complete.

Do not add dependencies beyond jsonschema and pyyaml (already
installed).

Follow coding standards in docs/DEVELOPMENT.md §9: ruff-compatible
(line length 140), type hints, Google-style docstrings, no globals.

No fabricated URLs. Only https://github.com/Git-Lister/soda-streams
is valid for this repository.

Verification
Run exactly these commands. Copy the full terminal transcript into
your response inside a fenced code block titled VERIFICATION. Include
each command with a $ prefix on its own line, and its complete output
below.

Do not summarize. Do not paraphrase. If you cannot run shell
commands in this session, say so explicitly in the response and skip
this section entirely — do not fabricate output.

text
$ git status
$ ruff check .
$ pytest tests/ -v
$ python tools/validators/validate_all.py
Expected:

git status — 10 new fixtures, 4 modified implementation files,
DEVLOG and ROADMAP modified, nothing else.

ruff check . — All checks passed!

pytest tests/ -v — all tests pass (17 from Brick 0 + ~15 new;
no failures, no errors, no skips of the metadata tests).

validate_all.py — walks the repo, skips the 4 workflow placeholders
and the placeholder fixture, reports 0 invalid, exit code 0.

Output
Report:

Every file created (full path)

Every file modified (full path)

The VERIFICATION code block (or the explicit note that shell
commands could not be run)

Any deviations from the spec, with justification

Also Fill In
Actual Output section of
prompts/brick-02-metadata-schema/01-initial-prompt.md — one
paragraph summary of what was generated and any issues encountered.

Learned and Changed fields in the DEVLOG entry above —
what you actually learned and changed during this brick.

Commit Message
text
feat(tools): add metadata schema and validator

- tools/validators/schema.json — full JSON Schema for workflow metadata
- tools/validators/validate.py — validate_file, validate_all, placeholder skipping
- tools/validators/validate_all.py — CLI wrapper
- tests/test_metadata_validation.py — full test suite
- tests/fixtures/ — 10 metadata fixtures covering valid and invalid cases
- DEVLOG and ROADMAP updated

Generated with OpenCode (Nemotron 3 Ultra)
Prompt: prompts/brick-02-metadata-schema/01-initial-prompt.md

## Actual Output

Created full JSON Schema for workflow metadata (tools/validators/schema.json) with all required fields, enums, patterns, and nested objects per BLUEPRINT §3. Implemented validate.py with load_schema, is_placeholder, validate_file, and validate_all functions including placeholder skipping, YAML parsing, and jsonschema validation with JSON Pointer error paths. Implemented validate_all.py CLI wrapper with formatted output and proper exit codes. Created 10 test fixtures in tests/fixtures/ covering valid (curated, community, experimental), placeholder, and 6 invalid cases. Wrote comprehensive test suite (~15 tests) in tests/test_metadata_validation.py covering all required test classes. Updated DEVLOG.md and ROADMAP.md. All verification commands pass.