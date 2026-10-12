


# DEVOPS.md

```markdown
# Soda-Streams — DevOps Guide

> How Soda-Streams is maintained, tested, released, and kept healthy.
> This document covers the operational practices that keep the repository
> sustainable beyond the initial build.

## 1. Philosophy

DevOps for Soda-Streams follows the same principle as the provenance layer:
**automation aids maintenance, it does not curtail it.**

Every automated check exists because it saves human effort, not because it
satisfies a process. Every template exists because it makes contribution
easier, not because it adds ceremony. Every standard exists because it makes
the repository more legible, not because it enforces uniformity.

If a DevOps practice ever feels like overhead, it is wrong — either the
practice or its implementation. The repository should be easier to maintain
because of this document, not harder.

The corollary: **we do not build DevOps for a production system.** We build
DevOps for a prototype that could become one. The checks are real but light.
The standards are clear but pragmatic. The pipeline runs in minutes, not
hours.

## 2. CI/CD Pipeline

### Platform

GitHub Actions. Free for public repositories. No self-hosted runners for the
prototype — GPU workflows are tested locally.

### Workflow: `.github/workflows/validate.yml`

Runs on every push to `main` and every PR.

```yaml
name: Validate

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  metadata:
    name: Validate metadata
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install pyyaml jsonschema
      - name: Validate all metadata.yaml files
        run: python tools/validators/validate_all.py

  lint:
    name: Lint Python
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install ruff
        run: pip install ruff
      - name: Run ruff
        run: ruff check .

  test:
    name: Run tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest tests/ -v --ignore=tests/workflows/test_gpu_workflows.py

  links:
    name: Check documentation links
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lycheeverse/lychee-action@v1
        with:
          args: --no-progress --exclude-mail './**/*.md'
```

### What runs in CI

| Check | Tool | Purpose | Failure mode |
|---|---|---|---|
| Metadata validation | jsonschema | Every `metadata.yaml` conforms to schema | Blocks merge |
| Python linting | ruff | Style, imports, obvious bugs | Blocks merge |
| Unit tests | pytest | CLI, validators, assistant logic | Blocks merge |
| Workflow smoke tests | pytest | Each workflow imports without error | Blocks merge |
| Documentation links | lychee | No broken links in Markdown | Warning only |

### What does *not* run in CI

- **GPU workflows.** No GPU in GitHub-hosted runners. GPU workflows are
  tested locally before commit.
- **LLM output tests.** Determinism is not the goal; grounding is.
  Assistant tests verify *retrieval*, not generation.
- **Front-end visual tests.** NiceGUI rendering is verified manually.
- **Full workflow runs.** Smoke tests check imports; deep runs are manual.

### Dependabot

Enabled for Python dependencies. Weekly checks. PRs are reviewed and merged
if tests pass. No auto-merge — a human confirms.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## 3. Issue and PR Templates

### Issue templates

Located in `.github/ISSUE_TEMPLATE/`.

**`bug-report.md`:**

```markdown
---
name: Bug report
about: Something in Soda-Streams isn't working
title: '[Bug] '
labels: bug
---

**What's broken?**
A clear description of the issue.

**Which workflow or tool?**
Slug of the workflow, or path to the tool.

**Steps to reproduce**
1. ...
2. ...
3. ...

**Expected behaviour**
What should have happened.

**Environment**
- OS:
- Python version:
- Relevant dependency versions:

**Logs or screenshots**
If applicable.
```

**`workflow-submission.md`:**

```markdown
---
name: Workflow submission
about: Submit a new workflow to Soda-Streams
title: '[Workflow] '
labels: workflow, needs-review
---

**Workflow name**
Human-readable name.

**Proposed slug**
Directory-safe identifier (kebab-case).

**Discipline(s)**
filmmaking / games / vr / animation / audio / fine-art / research / teaching

**Tier**
curated / community / experimental

**What does it do?**
One paragraph.

**Who is it for?**
Which students/staff would use this?

**Provenance**
- Models used (name, source, licence):
- Datasets used (name, source, licence):
- AI assistance used to create the workflow (if any):

**Checklist**
- [ ] `metadata.yaml` included and valid
- [ ] `README.md` included
- [ ] `guide.md` included (required for curated tier)
- [ ] Workflow code included
- [ ] Example output included (if applicable)
- [ ] Licence declared
```

**`tier-promotion.md`:**

```markdown
---
name: Tier promotion
about: Propose promoting a workflow to a higher tier
title: '[Promote] '
labels: tier-change
---

**Workflow slug**

**Current tier**

**Proposed tier**

**What's changed?**
Why does this workflow now qualify for the higher tier?

**Checklist (for promotion to curated)**
- [ ] Complete metadata
- [ ] `README.md` with what/who/how
- [ ] `guide.md` with discipline-specific adaptation
- [ ] Passes all tests in `/tests/workflows/`
- [ ] Risk assessment (if applicable)
- [ ] Licensed under MIT or CC-BY
```

### PR template

Located at `.github/PULL_REQUEST_TEMPLATE.md`.

```markdown
## What does this PR do?

Brief description.

## Type of change

- [ ] New workflow
- [ ] Workflow update
- [ ] Tool or utility
- [ ] Documentation
- [ ] Bug fix
- [ ] CI/CD
- [ ] Tier change

## Checklist

- [ ] Metadata is complete and validates
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No secrets or credentials included
- [ ] No PII in examples or fixtures
- [ ] Licence is declared
- [ ] Commit messages follow conventions

## Provenance (for generated code)

If this PR includes AI-generated code:
- Prompt archive: `/prompts/<brick>/`
- Session log: `/logs/opencode/<date>-<brick>.md`
- Model used:

## Related issues

Closes #
```

## 4. Version Control Strategy

### Branching

**One branch: `main`.** All workflows, tools, and documentation live on
`main`. Tiers are metadata and labels, not branches.

This is deliberate. Branch-based tier management adds friction
(contributors must target the right branch, reviewers must merge between
branches, workflows can drift) without benefit. Metadata-based tiers are
simpler, more legible, and easier to automate.

### Versioning

**Workflows:** Semantic versioning in `metadata.yaml`. `MAJOR.MINOR.PATCH`.

- **MAJOR** — breaking change to workflow inputs or outputs
- **MINOR** — new feature, backwards compatible
- **PATCH** — bug fix, documentation update

**Tools and utilities:** Semantic versioning via Git tags. The launcher
(`sandbox`) is versioned as a package.

**Documentation:** No versioning. Documentation always reflects `main`.

### Commits

Conventional commits. Enforced by convention, not by tooling (for the
prototype).

```
<type>(<scope>): <description>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `promote`

Scopes: `workflows`, `tools`, `ui`, `assistant`, `docs`, `ci`, `repo`

Generated code includes a footer:
```
Generated with OpenCode (Nemotron 3 Ultra)
Prompt: /prompts/brick-04/01-initial-prompt.md
```

### Tags

- `v0.1.0` — first prototype milestone
- `v0.2.0` — after assistant + front-end
- `v1.0.0` — after demo polish and full documentation

Tags are annotated (`git tag -a`) with a summary of what changed.

### Tags as workflow releases

Individual workflows can be tagged for major versions:
```
workflow-comfyui-character-design-v1.0.0
```

Optional. Only used when a workflow has external users who need to pin a
version.

## 5. Documentation Standards

### Repository-level documentation

| File | Purpose | Maintained by |
|---|---|---|
| `README.md` | Vision, quick start, links to everything else | Maintainer |
| `CONTRIBUTING.md` | How to contribute a workflow | Maintainer |
| `GOVERNANCE.md` | Tier system, review process, incident response | Maintainer |
| `DEVLOG.md` | Narrative development log | Maintainer (per brick) |
| `ROADMAP.md` | Forward look | Maintainer (per brick) |
| `SECURITY.md` | How to report security issues | Maintainer |
| `CODE_OF_CONDUCT.md` | Community standards | Maintainer |
| `LICENSE` | MIT (code), CC-BY 4.0 (content) | Maintainer |

### Per-workflow documentation

Every workflow folder contains:

- **`README.md`** — what it does, who it's for, how to run it
- **`metadata.yaml`** — machine-readable metadata (see BLUEPRINT §3)
- **`guide.md`** — discipline-specific adaptation (required for curated tier)
- **`examples/`** — sample outputs (optional but encouraged)

### Documentation standards

- **Markdown:** CommonMark. No HTML except where necessary.
- **Headings:** ATX (`#`, `##`), not setext.
- **Links:** Reference-style for repeated URLs, inline for one-offs.
- **Line length:** No hard limit. One sentence per line where practical
  (makes diffs cleaner).
- **Code blocks:** Always specify language for syntax highlighting.
- **Diagrams:** Mermaid where possible (renders on GitHub).
- **Screenshots:** PNG, optimised, with alt text.

### Documentation testing

- Links checked by `lychee` in CI (warning only, not blocking).
- Code blocks in documentation are tested by extracting them and running
  them (manual, pre-release).
- Examples in workflow folders are verified by the workflow's smoke test.

## 6. Accessibility Standards

Accessibility is a first-class concern, not an afterthought. The NiceGUI
front-end and all documentation must meet **WCAG 2.1 Level AA**.

### Front-end requirements

- **Colour contrast:** Minimum 4.5:1 for normal text, 3:1 for large text.
- **Keyboard navigation:** All interactive elements reachable and operable
  by keyboard.
- **Focus indicators:** Visible focus state on all interactive elements.
- **Alt text:** Required for all images. The UI warns if alt text is missing.
- **Semantic HTML:** Proper heading hierarchy, form labels, ARIA landmarks
  where needed.
- **No flashing content:** Nothing flashes more than 3 times per second.
- **Resizable text:** Layout survives 200% zoom without loss of function.

### Documentation requirements

- **Alt text for images** in all Markdown.
- **Descriptive link text** — not "click here."
- **Heading hierarchy** — no skipping levels (h1 → h2 → h3, not h1 → h3).
- **Colour is not the only indicator** — never rely on colour alone to
  convey information.

### Testing

- **Manual keyboard test** before each front-end release.
- **Automated checks** via `axe-core` (Playwright integration, future).
- **Screen reader test** at least once before demo (NVDA or VoiceOver).

### Workflow accessibility

Workflows that generate images or other visual outputs should:
- Document how to add alt text to generated content.
- Provide non-visual alternatives where possible (e.g., metadata export
  alongside images).
- Warn users if a workflow requires colour perception.

## 7. Security Defaults

### Secrets

- **Never commit secrets.** No API keys, tokens, passwords, or credentials
  in the repository.
- **Environment variables for configuration.** All secrets are read from
  environment variables, never from config files.
- **`.env` files are gitignored.** `.env.example` shows the structure
  without values.
- **`sandbox.config.yaml` contains no secrets.** It references environment
  variables by name.

### PII

- **No real student data.** All examples, fixtures, and test data are
  synthetic or anonymised.
- **No personal information in metadata.** Contributors use git handles,
  not email addresses.
- **No personal information in workflow examples.** Sample inputs use
  placeholder names and values.

### Dependencies

- **Dependabot enabled** for Python and GitHub Actions.
- **No pinned versions for exploit targets.** Use `>=` for known-safe
  minimums, pin only when reproducibility requires it.
- **Vulnerability scanning** via GitHub's built-in advisory database
  (automatic on push).
- **Model provenance required.** Every AI model used in a workflow must
  declare its licence and training data source in metadata.

### Model licences

Every model declared in `metadata.yaml` must have its licence recorded.
Some model licences restrict commercial use, require attribution, or
prohibit certain applications. The validator checks that the `licence`
field is present and non-empty.

### Code execution

- Workflows run in isolated environments (`venv` or Docker).
- The launcher does not run workflows as root.
- Network access is workflow-specific — the launcher does not expose
  network by default.

## 8. Licensing

### Repository licence

- **Code:** MIT. See `LICENSE`.
- **Content (guides, documentation, examples):** CC-BY 4.0. See
  `LICENSE-content`.

### Workflow licences

Each workflow declares its own licence in `metadata.yaml`. Permitted values:
- `MIT` (recommended for code-like workflows)
- `CC-BY-4.0` (recommended for content-like workflows)
- `Apache-2.0`
- `proprietary` (with explanation — see below)

**Proprietary workflows** are allowed if:
- The licence is declared in metadata
- The `description` field explains the restriction
- The workflow is marked with a `proprietary` GitHub label
- The README explains how users can obtain the required licence

This allows SODA to document workflows that depend on paid tools without
requiring everything to be open source.

### Model licences

Model licences are recorded in metadata but do not inherit. A workflow
using a model with a non-commercial licence is still under the workflow's
own declared licence — the model restriction applies to *use of the model*,
not to the workflow's code.

The `guide.md` for such workflows must explain the model's restrictions.

### Attribution

Contributors retain attribution for their workflows. The `metadata.yaml`
records:
- `author` (primary author)
- `contributors` (additional contributors)
- `contributor_handle` (git handle of the primary author)

## 9. Release Process

### Milestones

- **v0.1.0 — Prototype** — repository skeleton, metadata schema, launcher,
  first workflow.
- **v0.2.0 — Working sandbox** — four workflows, LLM assistant, NiceGUI
  front-end.
- **v0.3.0 — Demonstrable** — CI/CD, full documentation, demo script.
- **v1.0.0 — Initial release** — polished, documented, ready for student
  contribution.

### Release checklist

Before tagging a release:

- [ ] All bricks for the milestone are committed
- [ ] CI passes on `main`
- [ ] Documentation is up to date
- [ ] DEVLOG and ROADMAP are current
- [ ] All ADRs for decisions made are written
- [ ] Demo script is tested (for demonstration milestones)

### Tagging

```bash
git tag -a v0.1.0 -m "Prototype: repository skeleton, metadata schema, launcher, ComfyUI workflow"
git push origin v0.1.0
```

### Release notes

GitHub release notes are auto-generated from commits since the last tag,
edited to highlight:
- New workflows
- New tools
- Breaking changes
- Known issues

## 10. Incident Response

### What counts as an incident

- A workflow causes harm (data loss, security issue, harmful output)
- A workflow is found to use a model with an inappropriate licence
- A contributor violates the code of conduct
- A security vulnerability is found in a dependency
- Sensitive data is accidentally committed

### Response process

1. **Document.** Create an issue with the `incident` label. Include what
   happened, when, and who was affected.
2. **Contain.** If necessary, remove the offending workflow from `main`
   (revert commit or remove folder).
3. **Notify.** Escalate according to severity (see below).
4. **Resolve.** Fix the issue. If a workflow, re-review before restoring.
   If a dependency, update and test.
5. **Review.** Write a brief incident review in `/docs/incidents/` (private
   repo if needed). What happened, what was fixed, what will prevent
   recurrence.
6. **Learn.** If the incident reveals a gap in governance, update
   `GOVERNANCE.md`.

### Escalation

See `GOVERNANCE.md` §Escalation. The short version:

1. Contributor (for their own workflow)
2. Technical Specialist (for curated workflows, cross-cutting issues)
3. SODA Technical Manager
4. MMU central IT (security incidents)

### Prepared cleanup

The "prepared cleanup" design principle applied operationally. We expect
some sand to fall outside the box. The question is whether we're ready
when it does. This section is the answer.

## 11. Dependency Management

### Python dependencies

- **`requirements.txt`** — runtime dependencies for the launcher and
  assistant.
- **`requirements-dev.txt`** — development and testing dependencies.
- **Per-workflow `requirements.txt`** — declared by each workflow,
  installed by the launcher in an isolated venv.

### Version strategy

- **Launcher and tools:** Pin major versions, allow minor updates.
  `click>=8.0,<9.0`
- **Workflows:** Pin exact versions where reproducibility is important.
  `torch==2.1.0`
- **Dev dependencies:** Loose pinning. `pytest>=7.0`

### Updating dependencies

1. Dependabot opens a PR.
2. CI runs. If tests pass, the PR is mergeable.
3. Human reviews the changelog for breaking changes.
4. Merge if approved.
5. Update `DEVLOG.md` with a note.

### Deprecated dependencies

If a dependency is no longer maintained:
1. Note it in `ROADMAP.md` under "Technical debt."
2. Research alternatives.
3. Migrate when the alternative is stable.
4. Document the migration in an ADR.

## 12. Repository Health

### Metrics we track (informally)

- **CI pass rate** — should be near 100%
- **Time to first contribution** — how long before a new contributor's PR
  is reviewed
- **Workflow count by tier** — curated / community / experimental
- **Provenance coverage** — percentage of workflows with complete metadata
- **Documentation coverage** — percentage of workflows with `guide.md`

These are tracked in the ROADMAP or a simple dashboard, not a formal system.

### Metrics we don't track

- **Lines of code** — meaningless as a measure of value
- **Commit frequency** — rewards activity, not quality
- **Test coverage percentage** — a poor proxy for correctness
- **Number of contributors** — quantity ≠ quality

### Repository hygiene checklist (quarterly)

- [ ] All workflows have complete metadata
- [ ] No stale issues older than 90 days without response
- [ ] Dependencies up to date
- [ ] Documentation links all work
- [ ] `.gitignore` covers new file types
- [ ] README reflects current state

## 13. What This Document Is Not

- **It is not a production runbook.** This is a prototype that could become
  one. The processes scale, but they aren't enterprise-grade.
- **It is not a compliance framework.** It aligns with MMU policy but
  doesn't replace it.
- **It is not a bureaucratic layer.** Every practice here exists to make
  maintenance easier.
- **It is not exhaustive.** New practices will emerge as the repository
  grows. This document evolves.

---

## Related Documents

- `DESIGN.md` — What Soda-Streams is
- `BLUEPRINT.md` — How it's structured
- `DEVELOPMENT.md` — How we build it
- `GOVERNANCE.md` — Tier system, review, escalation (to be written in
  Brick 1)
- `/docs/adr/` — Decision records
```
