# Governance

> Light-touch, ground-up governance aligned with MMU policy.

## Principles

- **Default to open.** Community and experimental tiers require no approval.
- **Curated requires review.** Staff and advanced students only.
- **Escalation is documented.** Who to contact when something goes wrong.
- **Incidents are logged.** `/docs/incidents/` (private repo if needed).

## Three-Tier System

Three tiers defined by review status and support level. **Tiers are metadata
fields and GitHub labels — not git branches.** All workflows live on `main`.

| Tier | Reviewed | Supported | Who governs | Who contributes |
|---|---|---|---|---|
| **Curated** | Yes — by Technical Specialist + discipline staff | Yes | Institution | Staff, advanced students (by invitation) |
| **Community** | No — but metadata validated | No — best effort | Contributors | Anyone at SODA |
| **Experimental** | No | No | No one | Anyone (with warnings) |

### Tier Requirements

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

### Labels, Not Branches

All workflows live on `main`. Tiers are:

1. **Declared in metadata** (`tier: curated` in `metadata.yaml`)
2. **Applied as GitHub labels** (`tier: curated`, `tier: community`,
   `tier: experimental`)
3. **Filterable in the launcher and UI** (`sandbox list --tier curated`)

This keeps the repository simple (one branch), makes contribution
frictionless (no branch targeting), and lets governance evolve without
git operations.

### Promoting a Workflow

Promoting a workflow from community to curated means:

1. Update `tier` in `metadata.yaml`
2. Update the GitHub label
3. Complete any missing requirements (guide.md, tests, risk assessment)
4. Commit with message: `promote(workflows): <slug> to curated tier`

No branch merges. No cherry-picks. Just a metadata change and a review.

## Escalation Path

1. **Contributor** (for their own workflow)
2. **Technical Specialist** (for curated workflows, or cross-cutting issues)
3. **SODA Technical Manager**
4. **MMU central IT** (for security incidents)

## Alignment with Institutional Policy

- References (but doesn't replace) MMU AI guidance
- References (but doesn't replace) MMU data protection policy
- Uses `sandbox.config.yaml` institutional override to enforce local-only
  if required
- Documents all AI usage (assistant queries, model provenance)

## Boundary-Pushing Posture

Soda-Streams is a creative-technical school's repository. It should be
*more experimental* than central IT would sanction for enterprise use —
that's the point of a sandbox. But it documents what it does, so the
institution can learn from it. This is the "aligned, not kowtowed" position.

## Incident Response

See [DEVOPS.md §10](docs/DEVOPS.md#10-incident-response) for the full
incident response process.

### What Counts as an Incident

- A workflow causes harm (data loss, security issue, harmful output)
- A workflow is found to use a model with an inappropriate licence
- A contributor violates the code of conduct
- A security vulnerability is found in a dependency
- Sensitive data is accidentally committed

### Response Process

1. **Document.** Create an issue with the `incident` label. Include what
   happened, when, and who was affected.
2. **Contain.** If necessary, remove the offending workflow from `main`
   (revert commit or remove folder).
3. **Notify.** Escalate according to severity.
4. **Resolve.** Fix the issue. If a workflow, re-review before restoring.
   If a dependency, update and test.
5. **Review.** Write a brief incident review in `/docs/incidents/` (private
   repo if needed). What happened, what was fixed, what will prevent
   recurrence.
6. **Learn.** If the incident reveals a gap in governance, update
   `GOVERNANCE.md`.

## Roles

| Role | Responsibility |
|---|---|
| **Contributor** | Creates workflows, follows tier requirements |
| **Reviewer** | Validates metadata, applies tier labels, requests reviews |
| **Technical Specialist** | Reviews curated workflows, cross-cutting issues |
| **SODA Technical Manager** | Escalation point, governance decisions |
| **MMU Central IT** | Security incidents, institutional policy |

## Governance Evolution

Governance is not static. As the repository grows, this document will be
updated through the normal PR process. Significant changes should be
documented as ADRs in `/docs/adr/`.

## Related Documents

- [Contributing](CONTRIBUTING.md) — How to submit workflows
- [Code of Conduct](CODE_OF_CONDUCT.md) — Community standards
- [Security](SECURITY.md) — How to report issues
- [DEVOPS.md](docs/DEVOPS.md) — Operational practices
- [DEVELOPMENT.md](docs/DEVELOPMENT.md) — Development methodology