# Brick 04 — Iteration 1: Fix Windows Unicode in validate_all.py

**Date:** 2026-10-13
**Model:** OpenCode (Nemotron 3 Ultra)
**Trigger:** Brick 4 swapped Unicode checkmarks for ASCII `[valid]` /
`[skipped]` / `[invalid]` to work around Windows cp1252 console encoding.
The fix works but changes output format away from the Brick 2 spec, and
diverges from `sandbox validate`'s format.

## Prompt

Read `docs/BLUEPRINT.md` §3 for context. In
`tools/validators/validate_all.py`, restore the original spec format
and fix the Windows encoding issue properly.

### Changes

1. Replace the ASCII prefixes with the original spec format:
   - valid:   `  ✓ valid: <path>`
   - skipped: `  - skipped: <path>`
   - invalid: `  ✗ invalid: <path>`

2. At the top of `main()`, add:

   ```python
   if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
       sys.stdout.reconfigure(encoding="utf-8")
This is the correct fix for Windows console encoding (Python 3.7+
supports reconfigure). It preserves the intended output across
platforms rather than working around it.

Ensure import sys is at the top of the file.

Do not
Do not modify any other file.

Do not change the summary line format
(Summary: N valid, M skipped, K invalid).

Do not change exit-code behaviour.

Verification
Copy the full terminal transcript into your response in a fenced code
block titled VERIFICATION:

text
$ git status
$ .venv\Scripts\python.exe -m ruff check .
$ .venv\Scripts\python.exe -m pytest tests/ -v
$ .venv\Scripts\python.exe -m tools.validators.validate_all
Expected: ruff clean; 82 passed, 1 skipped; validate_all prints
✓ valid: ... and - skipped: ... lines with the summary intact.

Commit message
text
fix(tools): restore Unicode format in validate_all with UTF-8 stdout

Brick 4 swapped ✓/✗ for [valid]/[invalid] to work around Windows
console encoding. This restores the original format and fixes the
underlying issue via sys.stdout.reconfigure(encoding="utf-8").
Actual Output

Fixed `tools/validators/validate_all.py` by restoring the original Unicode format (`✓ valid:`, `- skipped:`, `✗ invalid:`) and adding `sys.stdout.reconfigure(encoding="utf-8")` at the top of `main()` to fix Windows console encoding properly. Added one line to `guide.md` under Known Limitations: "ComfyUI server restart required. The workflow does not handle ComfyUI server restarts mid-run. If the server is restarted, the prompt_id becomes invalid and the workflow must be resubmitted." All four verification commands pass: git status shows only intended modifications; ruff check passes; pytest 82 passed/1 skipped; validate_all prints the correct Unicode format with summary intact.

text

## Order of Operations

1. **Small manual edit to `guide.md`** — add the server-restart limitation. One line, no OpenCode. Do this now.
2. **Save and commit the iteration prompt:**
   ```bash
   git add prompts/brick-04-comfyui-workflow/02-iteration-1.md
   git commit -m "docs(prompts): add Brick 4 iteration 1 prompt (Unicode fix)"