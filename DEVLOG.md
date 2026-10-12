# Development Log

## 2026-10-12 — Brick 1b: Full repository scaffold

**Built:** Placeholder files across the entire target repository tree.
Workflow scaffolds (README, metadata, guide, entry point, examples/),
tool stubs (sandbox CLI, assistant, validators), UI stubs, discipline
guides, ADR stubs, provenance templates, test placeholders, and GitHub
templates. All placeholders marked and referenced to their filling brick.

**Learned:** Populating the target tree upfront removes scope ambiguity
for future bricks. Bricks now fill predetermined paths rather than
deciding what to create.

**Changed:** Scope model — "fill placeholders" replaces "create files."
Deviations become visible immediately.

**Next:** Brick 2 (metadata schema and validator).

## 2026-10-12 — Brick 0: Provenance infrastructure

**Built:** `.opencode/` config, `archive_prompt.py`, `prompts/` and
`logs/` structure.

**Learned:** The helper script is the key automation — one command creates
the archive and generates the commit footer.

**Changed:** Initially planned manual prompt archiving. Reframed as
automated tooling.

**Next:** Brick 1 (repository skeleton).

## 2026-10-12 — Brick 1: Repository skeleton

**Built:** Directory structure (all empty dirs with .gitkeep), root files
(README.md, CONTRIBUTING.md, GOVERNANCE.md, LICENSE, SECURITY.md,
CODE_OF_CONDUCT.md, .editorconfig, sandbox.config.yaml).

**Learned:** The repository structure from BLUEPRINT.md maps directly to
the governance and contribution model — directories are not arbitrary.

**Changed:** Added .gitkeep to all empty directories to ensure they track
in git. Split root documentation into separate concern files.

**Next:** Brick 2 (metadata schema + validator).