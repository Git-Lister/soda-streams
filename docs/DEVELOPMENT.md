# DEVELOPMENT.md

# Soda-Streams — Development Guide

> How we build Soda-Streams. This document is the contract between
> human oversight and AI implementation (OpenCode).
> It specifies how work is planned, generated, reviewed, logged, and
> committed.

## 1. Development Philosophy

Soda-Streams is built methodologically. The sequence is:

```
Thinking (design chat) → Specification (this repo's /docs) →
Implementation (OpenCode) → Review (maintainer) → Commit (GitHub)
```

No code is written before its specification is locked. No brick is started
before the previous brick is committed. No generated code is committed
without human review.

**Provenance aids automation.** The provenance layer is not administrative
overhead — it's a tool that makes development smoother. The helper script
archives prompts automatically. The commit footer is generated, not typed.
Logging is one command, not a manual journal. If provenance ever feels like
it's slowing things down, the provenance tooling is wrong, not the principle.

This is the same discipline the repository preaches: process over output,
provenance over speed, legibility over cleverness.

## 2. Roles

| Role | Who | Responsibility |
|---|---|---|
| **Architect** | Maintainer | Design decisions, specification, review, judgement |
| **Implementer** | OpenCode (Nemotron 3 Ultra) | Code generation from specifications |
| **Oversight** | Maintainer | Final review, calibration, commit approval |
| **Version control** | GitHub | Source of truth, provenance archive |

The AI does not make architectural decisions. It implements them. If a
specification is unclear, OpenCode asks — it does not invent.

## 3. The Brick Model

Development proceeds in **bricks** — self-contained units of work defined in
`BLUEPRINT.md` §11. Each brick:

- Has a clear specification (from BLUEPRINT or this document)
- Produces a testable, committable artefact
- Commits cleanly with a conventional commit message
- Does not depend on unfinished future bricks
- Leaves the repository in a working state

### Brick lifecycle

```
1. Specification reviewed and locked
2. Prompt written for OpenCode (archived via helper script)
3. OpenCode generates code
4. Session logged (via helper script or manual note)
5. Maintainer reviews generated code
6. Adjustments made (prompt iteration if needed)
7. Tests run locally
8. Committed with meaningful message (includes provenance footer)
9. DEVLOG.md updated
10. Next brick begins
```

No skipping steps. The method is the point.

## 4. Development Tooling

### Tool decision

**Primary:** OpenCode with Nemotron 3 Ultra (free tier), or local Ollama
models.

**Fallback:** Aider (if OpenCode's free tier proves unreliable).

**Why OpenCode:**
- Model-agnostic — switch between local (Ollama) and cloud providers
- Privacy-first — no code or context stored externally
- Configurable via `.opencode/` directory (committed to repo)
- Agent system allows custom agents for specific tasks
- LSP integration for Python
- Existing familiarity

**Why not other tools:**
- **Cline:** Too approval-heavy — the opposite of "provenance aids
  automation."
- **Kilo / Crush:** Pay-as-you-go or proprietary licence; less mature.
- **Aider as fallback:** Git-native, auto-commits with messages,
  battle-tested. The provenance layer is tool-agnostic and portable.

See `/docs/adr/0007-opencode-with-provenance-layer.md`.

### OpenCode configuration

Project configuration lives in `/.opencode/` (committed):

```
.opencode/
├── config.json              # Model, temperature, permissions, agents
├── /agents/
│   ├── brick-implementer.md # Agent for implementing a single brick
│   └── reviewer.md          # Agent for reviewing generated code
└── /commands/
    └── new-brick.md         # Custom command to start a new brick
```

**`config.json`:**

```json
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
```

**`agents/brick-implementer.md`:**

```markdown
# Brick Implementer Agent

You are implementing a single brick from the Soda-Streams blueprint.

## Context
- Read /docs/BLUEPRINT.md for the architecture
- Read /docs/DEVELOPMENT.md for the development methodology
- Read the current brick specification in /prompts/<brick>/

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
```

**`commands/new-brick.md`:**

```markdown
# /new-brick

Start a new brick.

1. Ask the user which brick number and title
2. Create /prompts/brick-NN-title/ directory
3. Create a new prompt file for the brick
4. Open the brick implementer agent
```

### The provenance layer

No existing AI coding tool provides the provenance we need. We build it:

- **`/prompts/`** — Prompt archive (committed)
- **`/logs/opencode/`** — Session logs (gitignored except README)
- **`/tools/provenance/archive_prompt.py`** — Helper script (automation)

### The helper script

`tools/provenance/archive_prompt.py` automates prompt archiving and session
logging. One command before an OpenCode session:

```bash
python tools/provenance/archive_prompt.py --brick 4 --prompt "Implement ComfyUI workflow"
```

Output:
```
Created: /prompts/brick-04/01-initial-prompt.md
Created: /logs/opencode/2026-01-20-brick-04.md
Commit footer:
Generated with OpenCode (Nemotron 3 Ultra)
Prompt: /prompts/brick-04/01-initial-prompt.md
```

You paste the footer into the commit message. The archive is created. The
session log is started. Provenance is automatic.

### Prompt archive structure

```
/prompts/
├── README.md                    # What this directory is
├── /brick-00-provenance-infrastructure/
│   ├── 01-initial-prompt.md
│   └── notes.md
├── /brick-01-repo-skeleton/
│   └── ...
└── /brick-NN-.../
```

Each prompt file includes date, brick reference, model, prompt text,
expected output, and actual output summary.

### Session logs

```
/logs/opencode/
├── README.md                    # What these logs are for
├── 2026-01-15-brick-00.md
├── 2026-01-16-brick-01.md
└── ...
```

Gitignored except for README — working notes, not public provenance.

### Handling OpenCode errors

If OpenCode generates broken code:

1. **Don't patch it manually.** Iterate on the prompt.
2. Archive the failed prompt in `/prompts/<brick>/` with `notes.md`
   explaining the failure.
3. Write a refined prompt.
4. Log the iteration.
5. Repeat until the output is correct.

This is slower than manual patching. It's also the point — the process
generates reusable patterns.

## 5. Architecture Decision Records (ADRs)

Significant decisions are documented as ADRs in `/docs/adr/`. Format
follows Michael Nygard's original pattern, kept short.

```
/docs/adr/
├── README.md                    # Index and explanation
├── 0001-use-nicegui-for-frontend.md
├── 0002-metadata-schema-design.md
├── 0003-three-tier-system.md
├── 0004-llm-configuration-approach.md
├── 0005-mediapipe-workflow-scope.md
├── 0006-tiers-as-labels-not-branches.md
└── 0007-opencode-with-provenance-layer.md
```

### ADR template

```markdown
# NNNN — Title

**Date:** YYYY-MM-DD
**Status:** proposed | accepted | superseded

## Context

What is the issue we're addressing?

## Decision

What did we decide?

## Consequences

What becomes easier? What becomes harder?
```

ADRs are written *when the decision is made*, not retrospectively.

## 6. Development Log (DEVLOG.md)

A running log at the repository root. Updated after each brick.

```markdown
# Development Log

## 2026-01-15 — Brick 0: Provenance infrastructure

**Built:** `.opencode/` config, `archive_prompt.py`, `/prompts/` and
`/logs/` structure.
**Learned:** The helper script is the key automation — one command creates
the archive.
**Changed:** Initially planned manual prompt archiving. Reframed as
automated tooling.
**Next:** Brick 1 (repository skeleton).

## 2026-01-16 — Brick 1: Repository skeleton
...
```

The DEVLOG is different from session logs:
- **Session logs** — what happened in OpenCode (technical)
- **DEVLOG** — what was built and learned (narrative)

## 7. Roadmap (ROADMAP.md)

Forward-looking. What's built, what's next, what's aspirational.

```markdown
# Roadmap

## Built
- [x] Provenance infrastructure
- [x] Repository skeleton
- [x] Metadata schema
- [x] Launcher CLI
- [ ] ComfyUI workflow
- [ ] RAG workflow
- [ ] Audio workflow
- [ ] MediaPipe workflow
- [ ] LLM assistant
- [ ] NiceGUI front-end
- [ ] CI/CD pipeline

## Next (6 months)
- Student contributor on-ramp
- First community-tier workflow
- Institutional governance review

## Aspirational (12+ months)
- Shared GPU runtime
- External partner access
- Public exhibition integration
```

Roadmap is updated at the end of each brick, not continuously.

## 8. Testing Strategy

### Test layers

| Layer | What | Where | When |
|---|---|---|---|
| **Unit** | CLI commands, metadata parser, RAG retrieval | `/tests/` | Every commit (CI) |
| **Workflow smoke** | Each workflow imports + runs without error | `/tests/workflows/` | Every commit (CI, CPU-only) |
| **Workflow deep** | One curated workflow runs end-to-end | Manual, local | Before tier promotion |
| **Front-end** | Playwright: navigation, accessibility | `/tests/ui/` | Before front-end commits |
| **Manual GPU** | GPU workflows (ComfyUI, etc.) | Local | Before commit |

### What is *not* tested in CI

- GPU-heavy workflows (no GPU in CI runners)
- LLM outputs (determinism is not the goal; grounding is)
- Front-end visual appearance (manual review)

### Test data

- Test fixtures live in `/tests/fixtures/`
- All fixtures are synthetic — no real student data, no PII
- Metadata fixtures cover every tier and every discipline

### Coverage target

Not a percentage. A principle: **every public function has at least one
test that verifies its contract.** Coverage percentage is a poor proxy for
correctness. Contract verification is the goal.

## 9. Coding Standards

### Python

- **Style:** ruff (linting + formatting), black-compatible
- **Typing:** type hints on all public functions
- **Docstrings:** Google style, one-line summary, params, returns
- **Imports:** grouped (stdlib, third-party, local), sorted
- **Naming:** snake_case for functions/variables, PascalCase for classes,
  SCREAMING_SNAKE for constants
- **No globals.** Configuration is passed, not read from environment
  mid-flow (except at explicit configuration boundaries).

### YAML

- Two-space indent
- No tabs
- Quoted strings where ambiguous
- Comments for non-obvious fields

### Markdown

- Reference-style links for URLs used more than once
- One sentence per line (makes diffs cleaner)
- No trailing whitespace
- ATX headings (`#`), not setext

### Commit messages

Conventional commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `promote`
Scopes: `workflows`, `tools`, `ui`, `assistant`, `docs`, `ci`, `repo`

Examples:
```
feat(workflows): add ComfyUI character design workflow
feat(tools): add metadata validator
fix(assistant): handle missing embedding model gracefully
docs(adr): add ADR-006 tiers as labels not branches
promote(workflows): comfyui-character-design to curated tier
```

Generated code commits include a footer:
```
Generated with OpenCode (Nemotron 3 Ultra)
Prompt: /prompts/brick-04/01-initial-prompt.md
```

## 10. Review Workflow

Every OpenCode output is reviewed before commit. The review checklist:

- [ ] Does it match the specification?
- [ ] Does it run?
- [ ] Do the tests pass?
- [ ] Are there any obvious security issues?
- [ ] Are there any obvious accessibility issues?
- [ ] Is it documented?
- [ ] Is the metadata complete?
- [ ] Does the commit message follow conventions?
- [ ] Is the prompt archived?
- [ ] Is the session logged?

If any box is unchecked, the brick is not done.

**Note on review scope:** Review is for *correctness and quality*, not for
*provenance bookkeeping*. Provenance is automated by the helper script. If
review is spending time on provenance, the tooling is wrong.

## 11. Repository Hygiene

### `.gitignore`

```
# Python
__pycache__/
*.py[cod]
.venv/
.venvs/
*.egg-info/
.pytest_cache/
.ruff_cache/

# Models
*.safetensors
*.ckpt
*.pth
/models/

# Data
/data/
*.db
.chroma/

# Logs (except README)
/logs/**
!/logs/README.md
!/logs/opencode/README.md

# Secrets
.env
.env.*
secrets/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
```

### `.editorconfig`

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space

[*.py]
indent_size = 4

[*.{yaml,yml,json}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

### Required root files

- `README.md` — vision, quick start
- `CONTRIBUTING.md` — how to contribute
- `GOVERNANCE.md` — tiers, review, incidents
- `LICENSE` — MIT (code), CC-BY 4.0 (content)
- `SECURITY.md` — how to report issues
- `CODE_OF_CONDUCT.md` — community standards
- `sandbox.config.yaml` — default configuration
- `DEVLOG.md` — development narrative
- `ROADMAP.md` — forward look
- `.gitignore`, `.editorconfig`

## 12. What "Done" Means

A brick is done when:

1. Code is written and matches specification
2. Tests pass locally and in CI
3. Documentation is updated
4. Metadata is complete (for workflows)
5. ADRs written (if decisions were made)
6. DEVLOG updated
7. Prompt archived (via helper script)
8. Session logged
9. Committed with conventional message (with provenance footer)
10. Repository is in a working state

Anything less is not done. Partial bricks are not committed.

## 13. The Meta Point

Soda-Streams documents provenance for its *contents* (workflows, models,
datasets) and for its *development* (prompts, logs, ADRs). This is
deliberate.

If the repository preaches provenance as a design principle, its own
development must practice it. The `/prompts/` archive is not administrative
overhead — it's a demonstration that AI-assisted development can be
transparent, traceable, and accountable.

This is the "aligned, not kowtowed" posture applied to how we work: we use
AI to build an AI repository, and we document exactly how.

---

## Related Documents

- `DESIGN.md` — What Soda-Streams is
- `BLUEPRINT.md` — How it's structured
- `DEVOPS.md` — How it's maintained
- `/docs/adr/` — Decision records
```
