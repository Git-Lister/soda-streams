# Soda-Streams

> A shared repository of AI workflows and processes — by SODA, for SODA —
> that makes sincere experimentation possible across teaching, research,
> and knowledge exchange.

## Vision

SODA has the culture, the people, and the infrastructure for creative
technology. It has VR labs, virtual production studios, motion capture,
and a community of staff and students who are already experimenting with AI.

What's missing is the **connective tissue** — a way to share *processes*,
not just outputs. Right now, if a student figures out a ComfyUI workflow
for character design, that knowledge lives in their head, in a Discord
message, or in a file on their laptop. It doesn't become part of SODA's
shared capability.

AI is the connective tissue. Soda-Streams is the repository that makes it
visible, versioned, and co-creatable. It's not a platform. It's not a
service. It's a convention — a way of working that makes SODA's AI practice
legible and shareable.

## Quick Start
> **Note:** The `sandbox` CLI commands below are the target interface, coming in Brick 3. Until then, browse workflows by reading their `README.md` files directly.
### Prerequisites

- Python 3.11+
- Git
- (Optional) Ollama for local LLM inference

### Installation

```bash
git clone https://github.com/Git-Lister/soda-streams.git
cd soda-streams
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
```

### Browse Workflows

```bash
# List all workflows
python -m tools.sandbox.cli list

# List curated workflows only
python -m tools.sandbox.cli list --tier curated

# List by discipline
python -m tools.sandbox.cli list --discipline games
```

### Run a Workflow

```bash
# Show workflow info
python -m tools.sandbox.cli info comfyui-character-design

# Run a workflow
python -m tools.sandbox.cli run comfyui-character-design

# Run with UI (if available)
python -m tools.sandbox.cli run comfyui-character-design --ui
```

### Validate Metadata

```bash
# Validate a specific metadata.yaml
python -m tools.sandbox.cli validate workflows/image-generation/comfyui-character-design/metadata.yaml

# Validate all workflows
python tools/validators/validate_all.py
```

## Repository Structure

```
soda-streams/
├── README.md                    # This file
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
│
├── /prompts/                    # OpenCode prompt archive (COMMITTED)
│   ├── README.md
│   ├── /brick-00-provenance-infrastructure/
│   ├── /brick-01-repo-skeleton/
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

## Design Principles

- **Porous edges.** Low-friction access. GitHub-based contribution. No maze
  of permissions. Anyone at SODA can browse, run, and fork a workflow
  without asking.
- **Defined boundaries.** A metadata schema. A three-tier system. A
  governance framework. Not to prevent exploration, but to make it safe.
- **Prepared cleanup.** Provenance tracking. Incident response. Clear
  escalation paths. We expect some sand to fall outside the box — the
  question is whether we're ready when it does.
- **Make the meal, not the menu.** Every workflow is a complete, runnable
  thing — not a tutorial, not a diagram, not a link to a tool. The user can
  run it, modify it, and extend it.

## Three-Tier System

All workflows live on `main`. Tiers are metadata fields and GitHub labels —
not git branches.

| Tier | Reviewed | Supported | Who governs |
|---|---|---|---|
| **Curated** | Yes — by Technical Specialist + discipline staff | Yes | Institution |
| **Community** | No — but metadata validated | No — best effort | Contributors |
| **Experimental** | No | No | No one |

## Links

- [Contributing](CONTRIBUTING.md)
- [Governance](GOVERNANCE.md)
- [Licence](LICENSE)
- [Security](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Blueprint](docs/BLUEPRINT.md)
- [DevOps](docs/DEVOPS.md)
- [Design](docs/DESIGN.md)