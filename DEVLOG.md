# Development Log

## 2026-10-13 — Brick 5: RAG research assistant workflow

**Built:** Second content workflow. PDF ingestion, chunking, embedding
(sentence-transformers), storage (ChromaDB), retrieval, and Ollama-backed
generation with citations.

**Learned:** Lazy imports are essential for heavy dependencies —
sentence_transformers pulls in PyTorch, chromadb has its own overhead.
Putting them inside embed_and_store and retrieve lets tests run without
the full stack. The Chunk dataclass carrying source/page/chunk_id makes
citation reconstruction trivial.

**Changed:** None — implementation follows the spec exactly.

**Next:** Brick 6 (voice synthesis workflow).

## 2026-10-13 — Brick 4: ComfyUI character design workflow

**Built:** First content workflow. ComfyUI + SDXL character design with
a real workflow.json, a Python HTTP client, discipline guide, and smoke
tests. Metadata validates as curated tier with full provenance.

**Learned:** The separation between workflow.py (client logic) and
workflow.json (ComfyUI graph) is clean — the Python side only needs to
know the prompt node IDs. The metadata validator's placeholder skipping
means the repo can mix real and placeholder workflows without false
positives.

**Changed:** None — implementation follows the spec exactly.

**Next:** Brick 5 (RAG research assistant workflow).

## 2026-10-12 — Brick 3: Launcher CLI

**Built:** The `sandbox` launcher CLI with four commands (list, info,
run, validate). Reads workflow metadata, filters by tier and discipline,
dispatches to workflow entry points.

**Learned:** The find_workflows + filter pattern cleanly separates
discovery from filtering. importlib.util.spec_from_file_location is the
correct way to load workflow modules without sys.path manipulation.
Placeholder workflows are skipped at discovery time, so info/run correctly
return "not found" until Brick 4 fills them.

**Changed:** None — implementation follows the spec exactly.

**Next:** Brick 4 (ComfyUI character design workflow).

## 2026-10-12 — Brick 2: Metadata schema and validator

**Built:** JSON Schema for workflow metadata, Python validator
(validate.py, validate_all.py), 10 test fixtures, and full test suite
for the validator.

**Learned:** The placeholder skipping mechanism is critical — it lets the
validator run on a partially populated repo without false positives. The
JSON Schema pattern for semantic versioning is stricter than expected
(rejects "1.0" without patch). The discipline enum must exactly match
the BLUEPRINT list.

**Changed:** None — implementation follows the spec exactly.

**Next:** Brick 3 (launcher CLI).

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