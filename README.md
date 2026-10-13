
# Soda-Streams

> An open, versioned repository of AI workflows and processes that
> makes sincere experimentation possible across teaching, research,
> and knowledge exchange.

## The problem

Creative technology disciplines already have the infrastructure —
studios, labs, capture spaces, exhibition spaces — and the community
that knows how to use it. What they often lack is **connective tissue**:
a way to share the *processes* that make the work happen, not just
the outputs.

A student figures out a ComfyUI workflow for character design. A
lecturer builds a RAG pipeline for research. A researcher trains a
webcam-based motion capture model. Each is real, useful, hard-won.
But the knowledge lives in a head, in a chat message, in a folder on
a laptop. It doesn't become part of the community's shared capability.

Soda-Streams is the connective tissue.

## What it is

Soda-Streams is a repository of **workflows** — not outputs, not
prompts, not screenshots. A workflow is a complete, runnable thing:
the code, the metadata, the provenance, the guidance. The unit of
content is the *process*, not the product.

Every workflow lives in its own folder:

```
workflows/
└── image-generation/
    └── comfyui-character-design/
        ├── README.md          # What it does, who it's for, how to run it
        ├── metadata.yaml      # Tools, dependencies, provenance
        ├── guide.md           # Discipline-specific adaptation
        ├── workflow.py        # The workflow itself
        └── examples/          # Sample outputs
```

When you browse the repository, you're browsing recipes. When you
fork a workflow, you're adapting a recipe. When you contribute your
own, you're adding a recipe others can build on. The repository grows
by accretion, from the work already happening.

## What it isn't

- It isn't a platform or a service. It's a repository and a convention.
- It isn't a replacement for institutional AI tools. It's a specialist
  complement for creative, discipline-specific work.
- It isn't a physical space. It's a shared working environment.
- It isn't a collection of outputs. It's a collection of processes.
- It isn't top-down. It's built by its community, for its community.
- It isn't proprietary. Open-source first, pragmatic about paid tools.

## Design principles

- **Porous edges.** Low-friction access. Git-based contribution. No
  maze of permissions. Anyone in the community can browse, run, and
  fork a workflow without asking.
- **Defined boundaries.** A metadata schema. A three-tier system. A
  governance framework. Not to prevent exploration, but to make it safe.
- **Prepared cleanup.** Provenance tracking. Incident response. Clear
  escalation paths. We expect some sand to fall outside the box — the
  question is whether we're ready when it does.
- **Make the meal, not the menu.** Every workflow is a complete,
  runnable thing — not a tutorial, not a diagram, not a link to a tool.
  The user can run it, modify it, and extend it.

## Three-tier system

All workflows live on `main`. Tiers are metadata fields and Git
labels — not branches.

| Tier | Reviewed | Supported | Who governs |
|---|---|---|---|
| **Curated** | Yes — reviewed for safety, licensing, and provenance | Yes | Community maintainers |
| **Community** | No — metadata validated only | Best-effort | Contributors |
| **Experimental** | No | No | No one |

## Repository structure

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
│
├── workflows/                   # The heart of the repository
│   ├── image-generation/
│   │   └── comfyui-character-design/
│   ├── motion-capture/
│   │   └── webcam-previs/
│   ├── text/
│   │   └── rag-research-assistant/
│   └── audio/
│       └── voice-synthesis/
│
├── tools/                       # The launcher and runtime
│   ├── sandbox/                 # CLI + launcher
│   ├── assistant/               # LLM assistant (RAG over repo)
│   ├── validators/              # Metadata schema validation
│   └── provenance/              # Development provenance automation
│
├── sandbox-ui/                  # NiceGUI front-end
│
├── guides/                      # Discipline-specific guidance
│   ├── filmmaking.md
│   ├── games.md
│   ├── vr-immersive.md
│   ├── animation.md
│   ├── fine-art.md
│   └── research.md
│
├── provenance/                  # Attribution patterns, licence templates
│
├── docs/                        # Project documentation
│   ├── DESIGN.md
│   ├── BLUEPRINT.md
│   ├── DEVOPS.md
│   ├── DEVELOPMENT.md
│   └── adr/                     # Architecture Decision Records
│
├── prompts/                     # Development provenance (committed)
├── logs/                        # Development logs (gitignored)
├── tests/                       # Test suite
├── .opencode/                   # OpenCode project configuration
└── .github/                     # CI/CD, templates
```

## Quick start

### Prerequisites

- Python 3.11+
- Git
- (Optional) [Ollama](https://ollama.com) for local LLM inference

### Installation

```bash
git clone https://github.com/Git-Lister/soda-streams.git
cd soda-streams
python -m venv .venv
source .venv/bin/activate      # or .venv\Scripts\activate on Windows
pip install pyyaml jsonschema ruff pytest
```

### Browse workflows

```bash
# List all available workflows
python -m tools.sandbox.cli list

# Filter by tier
python -m tools.sandbox.cli list --tier curated

# Filter by discipline
python -m tools.sandbox.cli list --discipline games
```

### Inspect a workflow

```bash
python -m tools.sandbox.cli info comfyui-character-design
```

### Run a workflow

```bash
python -m tools.sandbox.cli run comfyui-character-design
```

### Validate metadata

```bash
# Validate a specific workflow's metadata
python -m tools.sandbox.cli validate workflows/image-generation/comfyui-character-design/metadata.yaml

# Validate every workflow in the repository
python tools/validators/validate_all.py
```

## Contributing

Workflows come in three tiers — curated, community, and experimental.
Each has different requirements. See [CONTRIBUTING.md](CONTRIBUTING.md)
for the full process, and [GOVERNANCE.md](GOVERNANCE.md) for the
tier definitions.

Every workflow must include a `metadata.yaml` that validates against
the schema in `tools/validators/schema.json`. The schema is enforced
in CI.

## Governance

Governance is light-touch and ground-up. Community and experimental
workflows require no approval. Curated workflows are reviewed for
safety, licensing, and provenance.

See [GOVERNANCE.md](GOVERNANCE.md) for the tier system, review
process, escalation path, and incident response.

## Licensing

- **Code:** MIT — see [LICENSE](LICENSE)
- **Content (guides, documentation, examples):** CC-BY 4.0
- **Workflows:** contributor's choice, declared in `metadata.yaml`
- **Models and datasets:** licence recorded per workflow in `provenance`

## Provenance

Every workflow declares its provenance: models used, datasets used,
licences, and (where applicable) the AI assistance used to build the
workflow itself. This isn't decoration — it's the foundation of the
repository's approach to responsible AI.

## Links

- [Contributing](CONTRIBUTING.md)
- [Governance](GOVERNANCE.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security](SECURITY.md)
- [Design](docs/DESIGN.md)
- [Blueprint](docs/BLUEPRINT.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [DevOps](docs/DEVOPS.md)
- [Roadmap](ROADMAP.md)
- [Development Log](DEVLOG.md)
```

---
