"""CLI entry point: validate all metadata.yaml files in the repository."""

from __future__ import annotations

import sys
from pathlib import Path

from tools.validators.validate import ValidationResult, validate_all


def format_result(result: ValidationResult) -> str:
    """Format a single ValidationResult for terminal output.

    Args:
        result: The validation result to format.

    Returns:
        A formatted string for terminal output.
    """
    if result.status == "valid":
        return f"✓ valid: {result.path}"
    if result.status == "skipped":
        return f"- skipped: {result.path}"
    # invalid
    lines = [f"✗ invalid: {result.path}"]
    for error in result.errors:
        lines.append(f"  - {error}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Walk from the repository root and validate every metadata.yaml.

    Args:
        argv: Command-line arguments. argv[1] is the root directory
            (default: current working directory).

    Returns:
        0 if no invalid results, 1 otherwise.
    """
    if argv is None:
        argv = sys.argv

    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()

    print("Validating metadata files...")
    results = validate_all(root)

    if not results:
        print("No metadata.yaml files found.")
        return 0

    for result in results:
        print(format_result(result))

    valid_count = sum(1 for r in results if r.status == "valid")
    skipped_count = sum(1 for r in results if r.status == "skipped")
    invalid_count = sum(1 for r in results if r.status == "invalid")

    print(f"Summary: {valid_count} valid, {skipped_count} skipped, {invalid_count} invalid")

    return 0 if invalid_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())