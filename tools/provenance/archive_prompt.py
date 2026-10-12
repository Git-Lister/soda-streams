#!/usr/bin/env python3
"""Helper script for archiving OpenCode prompts and creating session logs.

This script automates the creation of prompt archive files and development
session logs for the Soda-Streams provenance infrastructure.
"""

import argparse
import datetime
import re
import sys
from pathlib import Path


def slugify(title: str) -> str:
    """Convert a title to a URL-friendly slug.

    Args:
        title: The title string to slugify.

    Returns:
        A slugified version of the title: lowercase, spaces and non-alphanumerics
        become hyphens, leading/trailing hyphens stripped.

    Examples:
        >>> slugify("Provenance infrastructure")
        'provenance-infrastructure'
        >>> slugify("Hello, World!  ")
        'hello-world'
    """
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def pad_brick_number(number: int) -> str:
    """Pad a brick number to two digits.

    Args:
        number: The brick number (0-99).

    Returns:
        The brick number as a zero-padded two-digit string.

    Examples:
        >>> pad_brick_number(0)
        '00'
        >>> pad_brick_number(4)
        '04'
        >>> pad_brick_number(12)
        '12'
    """
    return f"{number:02d}"


def create_prompt_file(
    brick_slug: str,
    padded_number: str,
    original_title: str,
    model: str,
    today_iso: str,
    base_path: Path,
) -> Path:
    """Create the initial prompt markdown file.

    Args:
        brick_slug: The full brick slug (e.g., "brick-00-provenance-infrastructure").
        padded_number: The zero-padded brick number (e.g., "00").
        original_title: The original human-readable title.
        model: The model name used.
        today_iso: Today's date in ISO format (YYYY-MM-DD).
        base_path: The repository root path.

    Returns:
        The path to the created prompt file.
    """
    prompt_dir = base_path / "prompts" / brick_slug
    prompt_dir.mkdir(parents=True, exist_ok=True)

    prompt_file = prompt_dir / "01-initial-prompt.md"

    if prompt_file.exists():
        return prompt_file

    template = (
        f"# Brick {padded_number} — {original_title}\n\n"
        f"**Date:** {today_iso}\n"
        f"**Model:** {model}\n"
        f"**Session:** logs/opencode/{today_iso}-brick-{padded_number}.md\n\n"
        "## Prompt\n\n"
        "[To be filled]\n\n"
        "## Expected Output\n\n"
        "[To be filled]\n\n"
        "## Actual Output\n\n"
        "[To be filled after session]\n"
    )

    prompt_file.write_text(template, encoding="utf-8")
    return prompt_file


def create_session_log(
    brick_slug: str,
    padded_number: str,
    original_title: str,
    model: str,
    today_iso: str,
    base_path: Path,
) -> Path:
    """Create the session log markdown file.

    Args:
        brick_slug: The full brick slug (e.g., "brick-00-provenance-infrastructure").
        padded_number: The zero-padded brick number (e.g., "00").
        original_title: The original human-readable title.
        model: The model name used.
        today_iso: Today's date in ISO format (YYYY-MM-DD).
        base_path: The repository root path.

    Returns:
        The path to the created session log file.
    """
    log_dir = base_path / "logs" / "opencode"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"{today_iso}-brick-{padded_number}.md"

    if log_file.exists():
        return log_file

    template = (
        f"# Session: Brick {padded_number} — {original_title}\n\n"
        f"**Date:** {today_iso}\n"
        f"**Duration:** [start] – [end]\n"
        f"**Model:** {model}\n\n"
        "## Prompts Used\n"
        f"- prompts/{brick_slug}/01-initial-prompt.md\n\n"
        "## Summary\n"
        "[What was generated]\n\n"
        "## Issues\n"
        "[Any problems encountered]\n\n"
        "## Resolution\n"
        "[How they were fixed]\n\n"
        "## Human Review Notes\n"
        "[Maintainer notes]\n"
    )

    log_file.write_text(template, encoding="utf-8")
    return log_file


def print_footer(
    prompt_file: Path,
    log_file: Path,
    model: str,
    base_path: Path,
) -> None:
    """Print the commit footer to stdout.

    Args:
        prompt_file: The path to the prompt file.
        log_file: The path to the session log file.
        model: The model name used.
        base_path: The repository root path.
    """
    rel_prompt = prompt_file.relative_to(base_path)
    rel_log = log_file.relative_to(base_path)

    print(f"Created: {rel_prompt}")
    print(f"Created: {rel_log}")
    print("Commit footer:")
    print(f"Generated with OpenCode ({model})")
    print(f"Prompt: {rel_prompt}")


def main() -> int:
    """Main entry point for the archive_prompt script.

    Parses command-line arguments, creates the prompt archive and session log
    files, and prints the commit footer.

    Returns:
        Exit code 0 on success, non-zero on error.
    """
    parser = argparse.ArgumentParser(
        description="Archive an OpenCode prompt and create a session log."
    )
    parser.add_argument(
        "--brick",
        type=int,
        required=True,
        help="Brick number (e.g., 0, 4, 12)",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Prompt title (e.g., 'Provenance infrastructure')",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model name (e.g., 'Nemotron 3 Ultra')",
    )

    args = parser.parse_args()

    today_iso = datetime.date.today().isoformat()
    padded_number = pad_brick_number(args.brick)
    slugified_title = slugify(args.prompt)
    brick_slug = f"brick-{padded_number}-{slugified_title}"

    base_path = Path.cwd()

    prompt_file = create_prompt_file(
        brick_slug=brick_slug,
        padded_number=padded_number,
        original_title=args.prompt,
        model=args.model,
        today_iso=today_iso,
        base_path=base_path,
    )

    log_file = create_session_log(
        brick_slug=brick_slug,
        padded_number=padded_number,
        original_title=args.prompt,
        model=args.model,
        today_iso=today_iso,
        base_path=base_path,
    )

    prompt_existed = prompt_file.exists() and prompt_file.stat().st_mtime < (
        datetime.datetime.now().timestamp() - 1
    )
    log_existed = log_file.exists() and log_file.stat().st_mtime < (
        datetime.datetime.now().timestamp() - 1
    )

    if prompt_existed:
        rel_prompt = prompt_file.relative_to(base_path)
        print(f"Skipped (exists): {rel_prompt}")
    if log_existed:
        rel_log = log_file.relative_to(base_path)
        print(f"Skipped (exists): {rel_log}")

    if not prompt_existed and not log_existed:
        print_footer(prompt_file, log_file, args.model, base_path)
    elif prompt_existed and log_existed:
        print("All target files exist. No action needed.")

    return 0


if __name__ == "__main__":
    sys.exit(main())