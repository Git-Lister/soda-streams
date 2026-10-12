# Development Log

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