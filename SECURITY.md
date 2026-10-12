# Security

## Reporting Security Issues

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, report them directly to the maintainers via:

- **Email:** security@soda-streams.example (placeholder — update with real contact)
- **GitHub Security Advisories:** Use the "Report a vulnerability" tab in the Security section

We will acknowledge receipt within 48 hours and provide a timeline for
investigation and fix.

## Supported Versions

| Version | Supported |
|---|---|
| Main branch | Yes (prototype) |

As a prototype, only the latest `main` branch receives security updates.

## Security Practices

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

### Model Licences

Every model declared in `metadata.yaml` must have its licence recorded.
Some model licences restrict commercial use, require attribution, or
prohibit certain applications. The validator checks that the `licence`
field is present and non-empty.

### Code Execution

- Workflows run in isolated environments (`venv` or Docker).
- The launcher does not run workflows as root.
- Network access is workflow-specific — the launcher does not expose
  network by default.

## Disclosure Policy

When a security issue is confirmed:

1. We will work on a fix privately
2. We will coordinate disclosure with the reporter
3. We will publish a security advisory after the fix is released
4. We will credit the reporter (unless they prefer anonymity)

## Institutional Alignment

This security policy aligns with (but does not replace) MMU's:
- IT Acceptable Use Policy
- Data Protection Policy
- Incident Response Procedures

For institutional security incidents, escalate to MMU Central IT per the
[Governance](GOVERNANCE.md) escalation path.