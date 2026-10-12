# BLUEPRINT.md

# Soda-Streams — System Blueprint

> Architecture specification for the Soda-Streams repository.
> This document describes the target architecture. Implementation proceeds
> in bricks (see §11), but the structure is designed for the end state.

## 1. Design Context

Soda-Streams is a shared repository of AI workflows and processes for SODA.
The unit of content is the **workflow**, not the output. Users discover,
fork, run, and contribute workflows. The repository is the sandbox.

See `DESIGN.md` for the full rationale.

## 2. Repository Structure

```
soda-streams/
├── README.md                    # Vision, quick start
├── CONTRIBUTING.md              # How to contribute
├── GOVERNANCE.md                # Tiers, review, incident response
├── LICENSE                      # MIT (code), CC-BY 4.0 (content)
├── SECURITY.md                  # How to report issues
├── CODE_OF_CONDUCT.md           # Community standards
├── sandbox.config.yaml          # LLM + runtime configuration
├── DEVLOG.md                    # Development narrative
├── ROADMAP.md                   # Forward look
├── .gitignore
├── .editorconfig
│
├── /workflows/                  # The heart of the repository
│   ├── /image-generation/
│   │   └── /comfyui-character-design/
│   ├── /motion-capture/
│   │   └── /webcam-previs/
│   ├── /text/
│   │   └── /rag-research-assistant/
│   └── /audio/
│       └── /voice-synthesis/
│
├── /tools/                      # The launcher and runtime
│   ├── /sandbox/                # CLI + launcher
│   ├── /assistant/              # LLM assistant (RAG over repo)
│   ├── /validators/             # Metadata schema validation
│   └── /provenance/             # Development provenance automation
│       └── archive_prompt.py    # Prompt archiving helper
│
├── /sandbox-ui/                 # NiceGUI front-end
│   ├── /pages/
│   ├── /components/
│   └── app.py
│
├── /guides/                     # Discipline-specific guidance
│   ├── filmmaking.md
│   ├── games.md
│   ├── vr-immersive.md
│   ├── animation.md
│   ├── fine-art.md
│   └── research.md
│
├── /provenance/                 # Attribution patterns, licence templates
│   ├── model-licences.md
│   ├── dataset-provenance.md
│   └── attribution-template.md
│
├── /docs/                       # Project documentation
│   ├── DESIGN.md
│   ├── BLUEPRINT.md
│   ├── DEVOPS.md
│   ├── DEVELOPMENT.md
│   └── /adr/                    # Architecture Decision Records
│       ├── README.md
│       ├── 0001-use-nicegui-for-frontend.md
│       ├── 0002-metadata-schema-design.md
│       ├── 0003-three-tier-system.md
│       ├── 0004-llm-configuration-approach.md
│       ├── 0005-mediapipe-workflow-scope.md
│       ├── 0006-tiers-as-labels-not-branches.md
│       └── 0007-opencode-with-provenance-layer.md
│
├── /prompts/                    # OpenCode prompt archive (COMMITTED)
│   ├── README.md
│   ├── /brick-00-provenance-infrastructure/
│   ├── /brick-01-repo-skeleton/
│   ├── /brick-02-metadata-schema/
│   └── ...
│
├── /logs/                       # Development logs (GITIGNORED except README)
│   ├── README.md
│   └── /opencode/
│       └── README.md
│
├── /tests/                      # Test suite
│   ├── test_metadata_validation.py
│   ├── test_launcher.py
│   ├── test_assistant_rag.py
│   ├── /fixtures/
│   └── /workflows/
│
├── /.opencode/                  # OpenCode project configuration (COMMITTED)
│   ├── config.json
│   ├── /agents/
│   │   ├── brick-implementer.md
│   │   └── reviewer.md
│   └── /commands/
│       └── new-brick.md
│
└── /.github/                    # CI/CD, templates
    ├── /workflows/
    │   └── validate.yml
    ├── /ISSUE_TEMPLATE/
    │   ├── bug-report.md
    │   ├── workflow-submission.md
    │   └── tier-promotion.md
    └── PULL_REQUEST_TEMPLATE.md
```

### Naming conventions

- **Directories:** kebab-case (`image-generation`, `webcam-previs`)
- **Python files:** snake_case (`metadata_validator.py`)
- **Workflow folders:** descriptive, discipline-prefixed where useful
  (`comfyui-character-design`)
- **Metadata files:** always `metadata.yaml`
- **Guides:** always `guide.md` (per-workflow) or `<discipline>.md` (in `/guides/`)
- **Prompts:** `<NN>-<description>.md` (e.g., `01-initial-prompt.md`)
- **ADRs:** `<NNNN>-<kebab-title>.md` (e.g., `0001-use-nicegui-for-frontend.md`)

## 3. Metadata Schema

Every workflow must have a `metadata.yaml` conforming to this schema. This
is what makes the repository machine-readable, searchable, and governable.

```yaml
# Required fields
name: string                    # Human-readable name
slug: string                    # Directory-safe identifier (matches folder)
author: string                  # Primary author (name or handle)
tier: enum                      # curated | community | experimental
discipline: list[string]        # filmmaking, games, vr, animation, audio, fine-art, research, teaching
description: string             # One-paragraph summary (what it does, who it's for)
version: string                 # Semantic version (1.0.0)
licence: string                 # SPDX identifier or "proprietary" with explanation

# Tools and dependencies
tools:                          # Named tools the workflow uses
  - name: string
    version: string
    source: string              # URL or "bundled"
    licence: string
dependencies: list[string]      # pip-style dependencies (for Python workflows)

# Provenance (critical for governance)
provenance:
  models:                       # If AI models are used
    - name: string
      source: string            # URL or organisation
      licence: string
      training_data: string     # "Not applicable" if pre-trained only
  datasets:                     # If custom datasets are used
    - name: string
      source: string
      licence: string
  ai_assistance:                # If AI was used to create the workflow itself
    - tool: string              # e.g. "OpenCode with Nemotron 3 Ultra"
      role: string              # e.g. "code generation"

# Optional fields
related_workflows: list[string] # Slugs of related workflows
risk_assessment: string         # Path to risk assessment doc (for curated tier)
output_examples: list[string]   # Paths to example outputs (screenshots, files)
readiness:                      # Optional self-assessment
  documentation: int            # 1-5
  testing: int                  # 1-5
  provenance: int               # 1-5

# Auto-generated (do not edit manually)
created: date                   # ISO 8601
updated: date                   # ISO 8601
contributor_handle: string      # Git handle
```

A **JSON Schema** implementation lives in `/tools/validators/schema.json`
and is enforced in CI.

## 4. Tier System

Three tiers, defined by review status and support level. **Tiers are
metadata fields and GitHub labels — not git branches.** All workflows live
on `main`.

| Tier | Reviewed | Supported | Who governs | Who contributes |
|---|---|---|---|---|
| **Curated** | Yes — by Technical Specialist + discipline staff | Yes | Institution | Staff, advanced students (by invitation) |
| **Community** | No — but metadata validated | No — best effort | Contributors | Anyone at SODA |
| **Experimental** | No | No | No one | Anyone (with warnings) |

### Tier requirements

**Curated workflows must:**
- Have complete metadata (all required fields)
- Have a `README.md` with what/who/how
- Have a `guide.md` with discipline-specific adaptation
- Pass all tests in `/tests/workflows/`
- Have a risk assessment (if applicable)
- Be licensed under MIT or CC-BY

**Community workflows must:**
- Have complete metadata
- Have a `README.md` (may be brief)
- Pass metadata validation in CI

**Experimental workflows must:**
- Have `metadata.yaml` with `tier: experimental`
- Pass metadata validation in CI
- Display a clear warning in the UI

### Labels, not branches

All workflows live on `main`. Tiers are:

1. **Declared in metadata** (`tier: curated` in `metadata.yaml`)
2. **Applied as GitHub labels** (`tier: curated`, `tier: community`,
   `tier: experimental`)
3. **Filterable in the launcher and UI** (`sandbox list --tier curated`)

This keeps the repository simple (one branch), makes contribution
frictionless (no branch targeting), and lets governance evolve without
git operations.

**Promoting a workflow** from community to curated means:
1. Update `tier` in `metadata.yaml`
2. Update the GitHub label
3. Complete any missing requirements (guide.md, tests, risk assessment)
4. Commit with message: `promote(workflows): <slug> to curated tier`

No branch merges. No cherry-picks. Just a metadata change and a review.

## 5. Contribution Workflow

### For curated tier
1. Fork the repository
2. Create a workflow folder under `/workflows/<discipline>/<slug>/`
3. Add `metadata.yaml` (with `tier: curated`), `README.md`, `guide.md`,
   workflow code, `examples/`
4. Open a PR to `main` with the workflow submission template
5. Reviewer applies `tier: curated` label and requests review from
   discipline staff
6. Review by Technical Specialist + discipline staff
7. Merge if approved

### For community tier
1. Fork the repository
2. Create a workflow folder as above (may omit `guide.md`)
3. Set `tier: community` in `metadata.yaml`
4. Open a PR to `main` with the workflow submission template
5. Metadata validation runs automatically
6. Reviewer applies `tier: community` label
7. Merge if validation passes

### For experimental tier
1. Fork the repository
2. Create a workflow folder as above
3. Set `tier: experimental` in `metadata.yaml`
4. Open a PR to `main` with a brief description
5. Metadata validation runs automatically
6. Reviewer applies `tier: experimental` label
7. Merge if validation passes

## 6. Runtime Convention

### The launcher (`sandbox` CLI)

The launcher is the primary way to interact with workflows from the
command line.

```bash
sandbox list                        # List all available workflows
sandbox list --tier curated         # Filter by tier
sandbox list --discipline games     # Filter by discipline
sandbox info <workflow-slug>        # Show metadata and description
sandbox run <workflow-slug>         # Run a workflow
sandbox run <workflow-slug> --ui    # Launch the workflow's UI (if it has one)
sandbox validate <path>             # Validate a metadata.yaml
sandbox assistant                   # Launch the LLM assistant (CLI mode)
```

### Environment isolation

Each workflow declares its dependencies in `metadata.yaml`. The launcher:

1. Reads metadata
2. Checks if a venv exists at `.venvs/<workflow-slug>/`
3. If not, creates it and installs dependencies
4. Activates the venv and runs the workflow's entry point

For heavier workflows (ComfyUI), the launcher can defer to Docker:
```yaml
runtime: docker
docker_image: "soda-streams/comfyui:latest"
```

### Entry point convention

Each workflow must declare an entry point:
```yaml
entry_point: "workflow.py:main"    # Python
# or
entry_point: "workflow.json"       # ComfyUI (launcher wraps it)
# or
entry_point: "workflow.sh"         # Shell script
```

The launcher handles the calling convention based on the entry point type.

## 7. LLM Assistant Architecture

The Soda-Streams Assistant is a grounded RAG pipeline over the repository's
own contents.

### Grounding sources
- All `metadata.yaml` files (structured data)
- All `README.md` and `guide.md` files (narrative documentation)
- All workflow code (for explaining how things work)

### Pipeline

```
User query
    ↓
[Embed query]  ← sentence-transformers (local, e.g. all-MiniLM-L6-v2)
    ↓
[Retrieve top-k]  ← ChromaDB vector store, built from repo contents
    ↓
[Augment prompt]  ← system prompt + retrieved context
    ↓
[LLM]  ← configurable provider (Ollama default, cloud opt-in)
    ↓
[Answer + citations]  ← always cite source files
```

### Configuration (`sandbox.config.yaml`)

```yaml
llm:
  provider: "ollama"                    # ollama | openai | anthropic | groq | custom
  model: "llama3.2:3b"
  base_url: "http://localhost:11434"    # for local/custom providers
  api_key_env: "SANDBOX_LLM_API_KEY"    # for cloud providers
  temperature: 0.3
  max_tokens: 2048

assistant:
  enabled: true
  grounding: true                       # if true, only answers from repo contents
  allow_external: false                 # if false, blocks cloud providers
  log_queries: true                     # for transparency
  log_path: "./logs/assistant/"

embeddings:
  model: "all-MiniLM-L6-v2"            # local, no API
  vector_store: "chromadb"              # local
  persist_path: "./.chroma/"
```

### Institutional override

Environment variables override config:
- `SANDBOX_FORCE_LOCAL=true` — blocks all external providers
- `SANDBOX_DISABLE_ASSISTANT=true` — disables assistant entirely
- `SANDBOX_ADMIN_MODE=true` — allows admin to lock config

This is the alignment hook for MMU governance. The assistant defaults to
local, logs its actions, and can be locked down centrally.

## 8. Front-End (NiceGUI)

### Pages

- **`/` — Home**: vision statement, quick start, featured workflows
- **`/browse`** — Browse all workflows (filter by discipline, tier, tool)
- **`/workflow/<slug>`** — Workflow detail: metadata, README, guide, run button
- **`/contribute`** — How to contribute (links to CONTRIBUTING.md)
- **`/assistant`** — Chat interface for the LLM assistant
- **`/settings`** — LLM configuration (provider, model, API key)
- **`/about`** — Governance, licences, provenance

### Accessibility

- WCAG 2.1 AA compliance
- Keyboard navigation
- Alt text for all images
- Colour contrast minimum 4.5:1
- Screen-reader tested

## 9. Governance Model

Light-touch, ground-up, aligned with MMU policy.

### Principles
- **Default to open.** Community and experimental tiers require no approval.
- **Curated requires review.** Staff and advanced students only.
- **Escalation is documented.** Who to contact when something goes wrong.
- **Incidents are logged.** `/docs/incidents/` (private repo if needed).

### Escalation path
1. Contributor (for their own workflow)
2. Technical Specialist (for curated workflows, or cross-cutting issues)
3. SODA Technical Manager
4. MMU central IT (for security incidents)

### Alignment with institutional policy
- References (but doesn't replace) MMU AI guidance
- References (but doesn't replace) MMU data protection policy
- Uses `sandbox.config.yaml` institutional override to enforce local-only
  if required
- Documents all AI usage (assistant queries, model provenance)

### Boundary-pushing posture
Soda-Streams is a creative-technical school's repository. It should be
*more experimental* than central IT would sanction for enterprise use —
that's the point of a sandbox. But it documents what it does, so the
institution can learn from it. This is the "aligned, not kowtowed" position.

## 10. Development Tooling & Provenance Layer

Development uses **OpenCode** as the primary AI implementation environment,
with a custom provenance layer built into the repository.

### OpenCode configuration

Project-level configuration lives in `/.opencode/` (committed):

```
.opencode/
├── config.json              # Model, temperature, permissions, agents
├── /agents/
│   ├── brick-implementer.md # Agent for implementing a single brick
│   └── reviewer.md          # Agent for reviewing generated code
└── /commands/
    └── new-brick.md         # Custom command to start a new brick
```

### Provenance layer

Because no existing AI coding tool provides the provenance we need, we
build it:

- **`/prompts/`** — Prompt archive (committed). Every prompt used to
  generate code is stored here with date, model, expected output, and
  actual output.
- **`/logs/opencode/`** — Session logs (gitignored except README). Working
  notes for each OpenCode session.
- **`/tools/provenance/archive_prompt.py`** — Helper script that automates
  prompt archiving and generates the commit message footer.

The helper script means provenance is *automated*, not manual bookkeeping.
One command before a session creates the archive; the commit footer is
generated automatically.

### Tool decision

OpenCode was chosen for: model flexibility (local + cloud), privacy-first
design, configurability, and existing familiarity. Aider is the documented
fallback if OpenCode's free tier proves unreliable — the provenance layer
is tool-agnostic and portable.

See `/docs/adr/0007-opencode-with-provenance-layer.md` for the full
rationale.

## 11. Build Order (Brick Execution Order)

Implementation proceeds in bricks. Each brick is testable and commits cleanly.

**Brick 0: Provenance infrastructure**
- `.opencode/` configuration (config.json, agents, commands)
- `tools/provenance/archive_prompt.py` (helper script)
- `/prompts/` directory + README
- `/logs/opencode/` directory + README
- Commit: "feat(tools): add provenance infrastructure and OpenCode config"

**Brick 1: Repository skeleton**
- Directory structure (all empty dirs with .gitkeep)
- README.md, CONTRIBUTING.md, GOVERNANCE.md, LICENSE, SECURITY.md,
  CODE_OF_CONDUCT.md
- `.gitignore`, `.editorconfig`, `sandbox.config.yaml`
- DEVLOG.md, ROADMAP.md
- Commit: "chore(repo): initialize Soda-Streams repository skeleton"

**Brick 2: Metadata schema + validator**
- `/tools/validators/schema.json` (JSON Schema)
- `/tools/validators/validate.py` (validation script)
- Example metadata file
- Tests in `/tests/test_metadata_validation.py`
- Commit: "feat(tools): add metadata schema and validator"

**Brick 3: Launcher CLI**
- `/tools/sandbox/cli.py` (argparse or click)
- Commands: list, info, run, validate
- Tests in `/tests/test_launcher.py`
- Commit: "feat(tools): add sandbox CLI launcher"

**Brick 4: First workflow — ComfyUI image generation**
- `/workflows/image-generation/comfyui-character-design/`
- metadata.yaml, README.md, guide.md, workflow.json, examples/
- Adapted from existing ComfyUI integration work
- Commit: "feat(workflows): add ComfyUI character design workflow (curated)"

**Brick 5: RAG research assistant workflow**
- `/workflows/text/rag-research-assistant/`
- Adapted from existing RAG pipeline work
- Commit: "feat(workflows): add RAG research assistant workflow (curated)"

**Brick 6: Audio/voice synthesis workflow**
- `/workflows/audio/voice-synthesis/`
- Adapted from existing audio work
- Commit: "feat(workflows): add voice synthesis workflow (curated)"

**Brick 7: MediaPipe motion capture workflow**
- `/workflows/motion-capture/webcam-previs/`
- MediaPipe Holistic (pose + hand + face)
- Recording + export (BVH, JSON)
- Skeleton overlay visualisation
- Commit: "feat(workflows): add webcam motion capture workflow (curated)"

**Brick 8: LLM Assistant**
- `/tools/assistant/` — RAG pipeline over repo
- ChromaDB vector store
- Configurable LLM provider
- CLI mode
- Tests in `/tests/test_assistant_rag.py`
- Commit: "feat(tools): add grounded LLM assistant"

**Brick 9: NiceGUI front-end**
- `/sandbox-ui/` — pages, components
- Browse, workflow detail, assistant, settings
- Accessibility pass
- Commit: "feat(ui): add NiceGUI front-end"

**Brick 10: CI/CD pipeline**
- `/.github/workflows/validate.yml` — metadata + tests
- Issue and PR templates
- Commit: "ci: add validation pipeline and contribution templates"

**Brick 11: Documentation polish + demo prep**
- Discipline guides (`/guides/`)
- ADRs (`/docs/adr/`) — finalise all decision records
- DEVLOG.md and ROADMAP.md final pass
- Demo script
- Commit: "docs: polish documentation and add demo script"

## 12. Testing Strategy

- **Metadata validation:** every `metadata.yaml` validated against JSON
  Schema in CI
- **Launcher:** unit tests for CLI commands
- **Assistant:** RAG retrieval tests (known query → expected workflow
  retrieved)
- **Workflows:** smoke tests (import + run without error); one deep test
  per curated workflow
- **Front-end:** Playwright tests for navigation, accessibility (future)
- **No GPU tests in CI** — GPU workflows tested locally

## 13. Provenance and Licensing

- **Code:** MIT
- **Content (guides, examples):** CC-BY 4.0
- **Workflows:** contributor's choice, declared in metadata
- **Models:** licence tracked in metadata `provenance.models[].licence`
- **Development:** OpenCode prompts archived in `/prompts/` as development
  provenance

## 14. What This Blueprint Is Not

- It is not a finished implementation. It is the architecture.
- It is not a production system. It is a prototype that scales.
- It is not a platform. It is a repository and a convention.
- It is not a replacement for institutional AI platforms. It is a
  complement.
- It is not top-down. It is by SODA, for SODA.

---

## Related Documents

- `DESIGN.md` — What Soda-Streams is and why
- `DEVOPS.md` — How it is maintained
- `DEVELOPMENT.md` — How we build it
- `/docs/adr/` — Architecture Decision Records
```
