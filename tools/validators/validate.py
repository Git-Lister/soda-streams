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
    """Load the JSON Schema from disk.

    Args:
        path: Path to the JSON Schema file.

    Returns:
        The parsed JSON Schema as a dictionary.

    Raises:
        FileNotFoundError: If the schema file does not exist.
        json.JSONDecodeError: If the schema file is not valid JSON.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def is_placeholder(path: Path) -> bool:
    """Return True if the file's first non-blank line is `# PLACEHOLDER`.

    Args:
        path: Path to the metadata file.

    Returns:
        True if the file starts with the placeholder marker, False otherwise.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False

    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped:  # first non-blank line
            return stripped.startswith(PLACEHOLDER_MARKER)
    return False


def validate_file(path: Path, schema: dict | None = None) -> ValidationResult:
    """Validate a single metadata.yaml against the schema.

    Args:
        path: Path to the metadata.yaml file.
        schema: Optional JSON Schema dict. If not provided, loads from
            SCHEMA_PATH.

    Returns:
        A ValidationResult with status:
        - "skipped" if the file is a placeholder or does not exist
        - "invalid" if the file fails to parse or fails schema validation
        - "valid" otherwise
    """
    if not path.exists():
        return ValidationResult(path, "skipped", ["file not found"])

    if is_placeholder(path):
        return ValidationResult(path, "skipped")

    if schema is None:
        schema = load_schema()

    try:
        instance = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return ValidationResult(path, "invalid", [str(exc)])

    if instance is None:
        return ValidationResult(path, "invalid", ["empty file"])

    try:
        jsonschema.validate(instance, schema)
    except jsonschema.ValidationError as exc:
        # Format error as JSON Pointer path + message
        pointer = " -> ".join(str(p) for p in exc.absolute_path)
        error_msg = f"{pointer}: {exc.message}" if pointer else exc.message
        return ValidationResult(path, "invalid", [error_msg])

    return ValidationResult(path, "valid")


def validate_all(root: Path) -> list[ValidationResult]:
    """Walk `root`, find every metadata.yaml, validate each.

    Args:
        root: Root directory to search for metadata.yaml files.

    Returns:
        A list of ValidationResult, one per file found, sorted by path
        for determinism.
    """
    results = []
    for path in sorted(root.rglob("metadata.yaml")):
        results.append(validate_file(path))
    return results