═══════════════════════════════════════════════════════════════════════
BEGIN BRICK 1 SPEC — 
═══════════════════════════════════════════════════════════════════════

Brick 1 — Repository Skeleton
You are implementing Brick 1 of the Soda-Streams project.

Context
Read these documents before starting:

docs/DESIGN.md — vision, principles, scope

docs/BLUEPRINT.md — architecture (especially §2 repository structure, §11 build order)

docs/DEVELOPMENT.md — methodology, coding standards

docs/DEVOPS.md — documentation standards, licensing, security defaults

Soda-Streams is a shared repository of AI workflows for a creative technology school. Brick 0 established the provenance infrastructure. Brick 1 establishes the repository skeleton: the root documentation, the licensing, and the top-level directory structure.

Current Repository State
Already present and must not be modified:

.gitignore — repo hygiene

pyproject.toml — pytest and ruff config

.opencode/ — OpenCode config (Brick 0)

tools/provenance/ — provenance helper (Brick 0)

prompts/ — prompt archive (Brick 0, add new entries only)

logs/ — session logs (Brick 0)

tests/test_archive_prompt.py — Brick 0 tests

docs/ — the four core specification documents

Deliverables
Create exactly the following files. Do not create anything else. Do not modify any existing file except DEVLOG.md and ROADMAP.md (updates described below).

Root documentation
1. README.md

Content outline:

Title: # Soda-Streams

Tagline: > A shared repository of AI workflows and processes — by SODA, for SODA — that makes sincere experimentation possible across teaching, research, and knowledge exchange.

Status line: **Status:** Prototype — under active development.

What this is — 2–3 sentences drawn from docs/DESIGN.md §1 Problem Statement. The unit is the workflow, not the output. The repository is the sandbox.

Design principles — the three from docs/DESIGN.md §2 (porous edges, defined boundaries, prepared cleanup) plus "make the meal, not the menu."

Repository structure — brief overview. Not the full tree; just the top-level folders and what each contains.

Three tiers — a small table showing Curated / Community / Experimental, drawn from docs/BLUEPRINT.md §4.

Quick start — aspirational for now. Note that the sandbox CLI will exist after Brick 3. For now: "Clone the repo, read a workflow's README.md, follow the guide."

Contributing — link to CONTRIBUTING.md.

Governance — link to GOVERNANCE.md.

Licence — MIT for code, CC-BY 4.0 for content. See LICENSE and LICENSE-content.

Acknowledgements — "Built as part of a technical development initiative at the School of Digital Arts."

Keep it readable in under two minutes. No badges, no build status, no CI banners — this is a prototype.

2. CONTRIBUTING.md

Content outline:

How to contribute a workflow — the three-tier process from docs/BLUEPRINT.md §5.

What every workflow needs — metadata (with a link to docs/BLUEPRINT.md §3 for the schema), README.md, guide.md (curated only), the workflow code itself, and examples where relevant.

The PR process — fork, branch, commit, PR, review.

Commit message conventions — brief summary pointing at docs/DEVELOPMENT.md §9.

Code of conduct — link to CODE_OF_CONDUCT.md.

Questions — open an issue.

Keep it practical. A first-time contributor should be able to follow it end to end.

3. GOVERNANCE.md

Content outline:

Tier system — curated / community / experimental, drawn from docs/BLUEPRINT.md §4. Include the review and support expectations for each.

Review process — who reviews what, at what tier.

Escalation path — the four-step path from docs/BLUEPRINT.md §9.

Incident response — a short summary of the process in docs/DEVOPS.md §10, or a link to it.

Alignment with institutional policy — a short statement that Soda-Streams references and complements MMU AI guidance and data protection policy, without replacing them.

Boundary-pushing posture — one paragraph. Soda-Streams is a creative-technical school's repository; it should be more experimental than central IT would sanction for enterprise use, but it documents what it does so the institution can learn from it.

Do not name individuals. Refer to roles only.

4. LICENSE

Standard MIT licence text. Copyright year: 2026. Copyright holder: Git-Lister.

5. LICENSE-content

Short declaration that all non-code content (documentation, guides, examples, workflow metadata) is licensed under Creative Commons Attribution 4.0 International (CC-BY 4.0). Include the canonical link: https://creativecommons.org/licenses/by/4.0/.

6. SECURITY.md

Content outline:

Reporting a security issue — how (private issue or email placeholder).

Scope — what counts as a security issue (secrets committed, dependency vulnerabilities, harmful workflow code, unexpected data exfiltration).

What is out of scope — model outputs being "wrong" or "biased" are governance concerns, not security issues; direct them to GOVERNANCE.md.

Response expectations — no SLA, but a commitment to acknowledge and address.

7. CODE_OF_CONDUCT.md

Adopt the Contributor Covenant, version 2.1 (https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Include the standard text. Replace the placeholder contact with: Open an issue with the label "conduct".

Configuration files
8. .editorconfig

Content exactly as specified in docs/DEVELOPMENT.md §11:

ini
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
9. sandbox.config.yaml

Content exactly as specified in docs/BLUEPRINT.md §7:

yaml
llm:
  provider: "ollama"
  model: "llama3.2:3b"
  base_url: "http://localhost:11434"
  api_key_env: "SANDBOX_LLM_API_KEY"
  temperature: 0.3
  max_tokens: 2048

assistant:
  enabled: true
  grounding: true
  allow_external: false
  log_queries: true
  log_path: "./logs/assistant/"

embeddings:
  model: "all-MiniLM-L6-v2"
  vector_store: "chromadb"
  persist_path: "./.chroma/"
Directory placeholders
Create the following directories. Each must contain a single .gitkeep file (empty) so the directory is tracked by Git.

workflows/

guides/

provenance/

sandbox-ui/

tests/fixtures/

tests/workflows/

docs/adr/

Do not pre-create subdirectories inside workflows/ — those are created by their respective workflow bricks (Bricks 4–7).

Updates to existing files
10. DEVLOG.md — append a new entry at the top of the entries section:

markdown
## YYYY-MM-DD — Brick 1: Repository skeleton

**Built:** Root documentation (README, CONTRIBUTING, GOVERNANCE, SECURITY,
CODE_OF_CONDUCT), licensing (MIT + CC-BY 4.0), config files
(.editorconfig, sandbox.config.yaml), and top-level directory structure
with .gitkeep placeholders.

**Learned:** To be filled in after review.

**Changed:** To be filled in after review.

**Next:** Brick 2 (metadata schema and validator).
Use today's date in ISO format.

11. ROADMAP.md — mark repository skeleton as built:

markdown
## Built
- [x] Provenance infrastructure
- [x] Repository skeleton

## Next
- [ ] Metadata schema
...
Rules
Do not run tests. Do not run pytest. Do not report test results. You are writing files only. Verification is done by the maintainer.

Do not modify .gitignore, pyproject.toml, docs/, prompts/, logs/, .opencode/, tools/, tests/test_archive_prompt.py, or any file not listed in Deliverables.

Follow the naming conventions in docs/BLUEPRINT.md §2.

No individual names. Refer to roles only (Technical Specialist, Technical Manager, Maintainer).

Markdown style per docs/DEVELOPMENT.md §9: ATX headings, one sentence per line where practical, no trailing whitespace.

Verification (maintainer will run)
After OpenCode returns, the maintainer will run:

bash
# 1. Confirm all deliverables exist
dir
dir workflows guides provenance sandbox-ui
dir tests docs\adr

# 2. Confirm sandbox.config.yaml parses
python -c "import yaml; yaml.safe_load(open('sandbox.config.yaml')); print('OK')"

# 3. Confirm no unintended changes
git status

# 4. Confirm no secrets or PII
findstr /S /I "api_key password secret" *.md *.yaml
Expected results:

All listed files present.

OK printed.

Only the expected files show as new or modified.

No hits in committed files (only the environment variable reference in sandbox.config.yaml, which is by design).

Output
Report:

A list of every file created.

A list of every file modified.

Confirmation that no other files were touched.

Do not run tests. Do not report test results.

Commit Message
text
chore(repo): initialize Soda-Streams repository skeleton

- Root documentation: README, CONTRIBUTING, GOVERNANCE, SECURITY,
  CODE_OF_CONDUCT
- Licensing: MIT (code) and CC-BY 4.0 (content)
- Config: .editorconfig, sandbox.config.yaml
- Directory placeholders for workflows, guides, provenance,
  sandbox-ui, tests, ADRs
- DEVLOG and ROADMAP updated

Generated with OpenCode (Nemotron 3 Ultra)
Prompt: prompts/brick-01-repository-skeleton/01-initial-prompt.md
═══════════════════════════════════════════════════════════════════════
END BRICK 1 SPEC
═══════════════════════════════════════════════════════════════════════