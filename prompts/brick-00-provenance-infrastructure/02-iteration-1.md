# Brick 00 — Iteration 1: Fix test environment

**Date:** 2026-10-12
**Model:** OpenCode (Nemotron 3 Ultra)
**Trigger:** Initial build reported tests passing, but verification in the
real environment showed `ModuleNotFoundError: No module named 'tools'`.

## Issues

1. Pytest could not resolve `from tools.provenance.archive_prompt import ...`
   because the repo root was not on `sys.path`. Spec omission: the brick
   required direct imports but did not specify how to make them resolvable.
2. Two `F841` unused-variable warnings (`original_mtime`) in
   `tests/test_archive_prompt.py`.
3. One `I001` import-order warning in the same file.

## Fixes

1. Added `pyproject.toml` with `pythonpath = ["."]` in
   `[tool.pytest.ini_options]`, plus ruff config.
2. Removed the unused `original_mtime` lines.
3. Ran `ruff check . --fix` to sort imports.

## Lesson

OpenCode reported "17 passed" without the tests actually running in the
target environment. Going forward, brick specs must include an explicit
verification command and the acceptance criteria must be checked manually,
not taken from OpenCode's report.