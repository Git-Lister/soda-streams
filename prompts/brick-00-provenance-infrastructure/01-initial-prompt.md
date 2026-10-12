═══════════════════════════════════════════════════════════════════════

Brick 0 — Provenance Infrastructure
You are implementing Brick 0 of the Soda-Streams project.

Context
Read these documents before starting:

docs/BLUEPRINT.md — the system architecture (especially §2, §10, §11)

docs/DEVELOPMENT.md — the development methodology (especially §4)

Soda-Streams is a shared repository of AI workflows for a creative technology school. We are building the development provenance infrastructure before anything else, so that every subsequent brick is traceable and automated.

Current Repository State
Already present at the repository root:

.gitignore — handles Python, models, logs, secrets, IDE files

docs/ — contains DESIGN.md, BLUEPRINT.md, DEVELOPMENT.md, DEVOPS.md

prompts/brick-00-provenance-infrastructure/01-initial-prompt.md — this prompt

.venv/ — Python 3.11 environment (gitignored)

Do not modify or overwrite any of these existing files unless a deliverable below explicitly says to.

Deliverables
Create exactly the following files. Do not create anything else.

1. .opencode/config.json
json
{
  "model": "opencode/nemotron-3-ultra-free",
  "temperature": 0.2,
  "max_tokens": 8192,
  "permissions": {
    "edit": "ask",
    "bash": "ask",
    "webfetch": "allow"
  },
  "agents": {
    "default": {
      "model": "opencode/nemotron-3-ultra-free",
      "temperature": 0.2,
      "steps": 25
    }
  }
}
2. .opencode/agents/brick-implementer.md
markdown
---
description: Implement a single brick from the Soda-Streams blueprint
mode: primary
model: opencode/nemotron-3-ultra-free
temperature: 0.2
permission:
  edit: ask
  bash: ask
---

# Brick Implementer Agent

You are implementing a single brick from the Soda-Streams blueprint.

## Context
- Read `docs/BLUEPRINT.md` for the architecture
- Read `docs/DEVELOPMENT.md` for the development methodology
- Read the current brick specification in `prompts/<brick>/`

## Rules
- Implement only what the brick specifies
- Do not invent features not in the specification
- Write tests alongside code
- Document everything
- Follow the coding standards in DEVELOPMENT.md §9

## Output
- Generate the files specified in the brick
- Update DEVLOG.md
- Create a commit message following conventional commits
3. .opencode/agents/reviewer.md
markdown
---
description: Review generated code for correctness and quality
mode: subagent
model: opencode/nemotron-3-ultra-free
temperature: 0.1
permission:
  edit: deny
  bash: ask
---

# Reviewer Agent

You are reviewing code generated for Soda-Streams.

## Checklist
- Does it match the specification?
- Does it run?
- Are there obvious security issues?
- Are there obvious accessibility issues?
- Is it documented?
- Does the commit message follow conventions?

## Output
A brief review: what passes, what needs attention, what is blocking.
4. .opencode/commands/new-brick.md
markdown
---
description: Start a new brick
---

# /new-brick

Start a new brick.

1. Ask which brick number and title
2. Create `prompts/brick-NN-title/` directory
3. Create a new prompt file for the brick
4. Open the brick implementer agent
5. tools/provenance/archive_prompt.py
A Python CLI script, stdlib only (argparse, datetime, pathlib, re).

Interface:

bash
python tools/provenance/archive_prompt.py \
  --brick 0 \
  --prompt "Provenance infrastructure" \
  --model "Nemotron 3 Ultra"
Behaviour:

Pad the brick number to two digits (0 → 00, 4 → 04, 12 → 12).

Slugify the prompt title: lowercase, spaces and non-alphanumerics become hyphens, strip leading/trailing hyphens. "Provenance infrastructure" → provenance-infrastructure.

Derive brick_slug = f"brick-{padded_number}-{slugified_title}".

Create directory prompts/{brick_slug}/ if it doesn't exist.

Create prompts/{brick_slug}/01-initial-prompt.md if it doesn't exist (do not overwrite). Use this template:

markdown
# Brick {padded_number} — {original_title}

**Date:** {today_iso}
**Model:** {model}
**Session:** logs/opencode/{today_iso}-brick-{padded_number}.md

## Prompt

[To be filled]

## Expected Output

[To be filled]

## Actual Output

AMENDED BY HUMAN: OpenCode reported "17 passed" without the tests actually running in the
target environment. Going forward, brick specs must include an explicit
verification command and the acceptance criteria must be checked manually,
not taken from OpenCode's report.

markdown
# Session: Brick {padded_number} — {original_title}

**Date:** {today_iso}
**Duration:** [start] – [end]
**Model:** {model}

## Prompts Used
- prompts/{brick_slug}/01-initial-prompt.md

## Summary
[What was generated]

## Issues
[Any problems encountered]

## Resolution
[How they were fixed]

## Human Review Notes
[Maintainer notes]
Print to stdout, exactly:

text
Created: prompts/{brick_slug}/01-initial-prompt.md
Created: logs/opencode/{today_iso}-brick-{padded_number}.md
Commit footer:
Generated with OpenCode ({model})
Prompt: prompts/{brick_slug}/01-initial-prompt.md
Requirements:

If a file already exists, skip creation and print Skipped (exists): <path>.

If all target files exist, print a clear message and exit 0.

Return exit code 0 on success, non-zero on error.

Type hints on all functions. Google-style docstrings.

No globals. Configuration is passed via arguments.

6. prompts/README.md
markdown
# Prompt Archive

This directory contains the prompts used to generate Soda-Streams code.

Each brick gets a folder: `prompts/brick-NN-title/`. Each prompt file
records the date, model, prompt text, expected output, and actual output.

This is **development provenance**. The code's origin is documented, just
as workflow provenance is documented in metadata.

See `docs/DEVELOPMENT.md` §4 for the full methodology.
7. logs/README.md
markdown
# Development Logs

Working notes from development sessions.

These are **gitignored** except for this README. They are for the
maintainer's reference, not public provenance. The public provenance is
the prompt archive in `prompts/`.
8. logs/opencode/README.md
markdown
# OpenCode Session Logs

Session logs for OpenCode development sessions.

Each log records the session date, brick reference, prompts used, summary
of generated files, issues, and resolution.

Gitignored — working notes, not public provenance.
9. DEVLOG.md
markdown
# Development Log

## {today_iso} — Brick 0: Provenance infrastructure

**Built:** `.opencode/` config, `archive_prompt.py`, `prompts/` and
`logs/` structure.

**Learned:** The helper script is the key automation — one command creates
the archive and generates the commit footer.

**Changed:** Initially planned manual prompt archiving. Reframed as
automated tooling.

**Next:** Brick 1 (repository skeleton).
10. ROADMAP.md
markdown
# Roadmap

## Built
- [x] Provenance infrastructure

## Next
- [ ] Repository skeleton
- [ ] Metadata schema
- [ ] Launcher CLI
- [ ] ComfyUI workflow
- [ ] RAG workflow
- [ ] Audio workflow
- [ ] MediaPipe workflow
- [ ] LLM assistant
- [ ] NiceGUI front-end
- [ ] CI/CD pipeline

## Aspirational (12+ months)
- Shared GPU runtime
- External partner access
- Public exhibition integration
11. tests/test_archive_prompt.py
Pytest tests for archive_prompt.py. Cover:

Slugification: "Provenance infrastructure" → provenance-infrastructure; handles punctuation and multiple spaces.

Brick number padding: 0 → 00, 4 → 04, 12 → 12.

File creation: Running the script with tmp_path as the working directory creates the expected prompt and log files.

No overwrite: Running the script twice does not overwrite existing files (check mtime or content).

Commit footer: stdout contains the expected footer lines.

Use tmp_path and capsys fixtures. Import the script's functions directly — structure the script so this is possible (a slugify, pad_brick_number, create_prompt_file, create_session_log, print_footer set of functions, called from a main() guarded by if __name__ == "__main__":).

Rules
Implement only what is listed above. Do not create additional files.

Do not modify .gitignore, docs/, or prompts/brick-00-provenance-infrastructure/01-initial-prompt.md.

Follow the coding standards in docs/DEVELOPMENT.md §9: ruff-compatible, type hints on public functions, no globals.

The helper script must run before pyyaml or jsonschema are installed. Stdlib only.

Output
After generating all files, run:

bash
python tools/provenance/archive_prompt.py --brick 0 --prompt "Provenance infrastructure" --model "Nemotron 3 Ultra"
Because the prompt file already exists, it should report Skipped (exists) for 01-initial-prompt.md and create or skip the session log accordingly. Then run:

bash
pytest tests/test_archive_prompt.py -v
All tests should pass. Report:

A list of files created.

The stdout from the helper script.

The pytest summary line.

Commit Message
text
feat(tools): add provenance infrastructure and OpenCode config

- .opencode/ with config.json, agents, commands
- tools/provenance/archive_prompt.py helper script
- prompts/ and logs/ directory structure with READMEs
- DEVLOG.md and ROADMAP.md initial entries
- tests/test_archive_prompt.py

Generated with OpenCode (Nemotron 3 Ultra)
Prompt: prompts/brick-00-provenance-infrastructure/01-initial-prompt.md
═══════════════════════════════════════════════════════════════════════