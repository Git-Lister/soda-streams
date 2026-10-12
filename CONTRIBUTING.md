# Contributing to Soda-Streams

Thank you for contributing to Soda-Streams! This guide explains how to submit
workflows, propose improvements, and participate in the community.

## Ways to Contribute

1. **Submit a workflow** — Share a complete, runnable AI workflow
2. **Improve existing workflows** — Fix bugs, add features, improve documentation
3. **Add tooling** — Enhance the launcher, validator, or assistant
4. **Document** — Write guides, improve READMEs, add examples
5. **Governance** — Review workflows, participate in tier promotions

## Workflow Submission

### Before You Start

- Check if a similar workflow already exists in `/workflows/`
- Read the [Governance](GOVERNANCE.md) document to understand the tier system
- Choose the appropriate tier: **curated**, **community**, or **experimental**

### Submission Process

#### For Curated Tier

1. Fork the repository
2. Create a workflow folder under `/workflows/<discipline>/<slug>/`
3. Add required files:
   - `metadata.yaml` (with `tier: curated`)
   - `README.md` (what/who/how)
   - `guide.md` (discipline-specific adaptation)
   - Workflow code
   - `examples/` (sample outputs)
4. Open a PR to `main` with the workflow submission template
5. Reviewer applies `tier: curated` label and requests review from discipline staff
6. Review by Technical Specialist + discipline staff
7. Merge if approved

#### For Community Tier

1. Fork the repository
2. Create a workflow folder as above (may omit `guide.md`)
3. Set `tier: community` in `metadata.yaml`
4. Open a PR to `main` with the workflow submission template
5. Metadata validation runs automatically
6. Reviewer applies `tier: community` label
7. Merge if validation passes

#### For Experimental Tier

1. Fork the repository
2. Create a workflow folder as above
3. Set `tier: experimental` in `metadata.yaml`
4. Open a PR to `main` with a brief description
5. Metadata validation runs automatically
6. Reviewer applies `tier: experimental` label
7. Merge if validation passes

### Required Files

Every workflow must include:

| File | Curated | Community | Experimental |
|---|---|---|---|
| `metadata.yaml` | ✓ | ✓ | ✓ |
| `README.md` | ✓ | ✓ | ✓ |
| `guide.md` | ✓ | Optional | Optional |
| Workflow code | ✓ | ✓ | ✓ |
| `examples/` | Encouraged | Encouraged | Encouraged |

### Metadata Requirements

The `metadata.yaml` must conform to the schema in `/tools/validators/schema.json`.
See [BLUEPRINT.md §3](docs/BLUEPRINT.md#3-metadata-schema) for the full schema.

Key fields:
- `name`, `slug`, `author`, `tier`, `discipline`, `description`, `version`, `licence`
- `tools`, `dependencies`
- `provenance` (models, datasets, AI assistance)

## Development Workflow

### Brick Model

Development proceeds in **bricks** — self-contained units of work. See
[DEVELOPMENT.md §3](docs/DEVELOPMENT.md#3-the-brick-model).

### Coding Standards

- **Python:** ruff (linting + formatting), type hints on public functions,
  Google-style docstrings, no globals
- **YAML:** Two-space indent, no tabs
- **Markdown:** ATX headings, one sentence per line, reference-style links
- **Commits:** Conventional commits with provenance footer

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_archive_prompt.py -v

# Lint
ruff check .
```

## Provenance

All AI-assisted development must be documented:

1. Use the helper script before an OpenCode session:
   ```bash
   python tools/provenance/archive_prompt.py --brick N --prompt "Title" --model "Model"
   ```
2. The script creates the prompt archive and session log
3. Include the generated commit footer in your commit message

See [DEVELOPMENT.md §4](docs/DEVELOPMENT.md#4-development-tooling) for details.

## Code of Conduct

All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Licensing

By contributing, you agree that your contributions will be licensed under:

- **Code:** MIT
- **Content (guides, documentation, examples):** CC-BY 4.0
- **Workflows:** Your choice, declared in `metadata.yaml`

See [LICENSE](LICENSE) and [DEVOPS.md §8](docs/DEVOPS.md#8-licensing) for details.

## Getting Help

- Open a [GitHub Issue](https://github.com/soda-streams/soda-streams/issues) for bugs or questions
- Check existing [Issues](https://github.com/Git-Lister/soda-streams/soda-streams/issues)
- Read the [docs/](docs/) for architecture and methodology

## Recognition

Contributors are credited in:
- `metadata.yaml` (`author`, `contributors`, `contributor_handle`)
- Git commit history
- GitHub release notes

Thank you for making Soda-Streams better!