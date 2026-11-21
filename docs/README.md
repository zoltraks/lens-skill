# Governance Documents

## Purpose

> **Scope:**Index of the repository-governance documents under `docs/`. **Key items:** style,
> maintenance, versioning, contributing, security.

These documents govern the Lens repository itself, not the audit reports the skill produces.

| File                               | Owns                                                              | Read when                                            |
|------------------------------------|-------------------------------------------------------------------|------------------------------------------------------|
| [STYLE.md](STYLE.md)               | Prose, tables, headings, and encoding for shipped documents       | Editing any shipped document                         |
| [MAINTENANCE.md](MAINTENANCE.md)   | Directory roles, file naming, registration, validation procedures | Structural, naming, registration, or layout changes  |
| [VERSIONING.md](VERSIONING.md)     | Version format, bump rules, and the release procedure             | Version bumps and release anchoring                  |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Maintainer model, pre-merge validation, commit convention         | Preparing a change set or reporting an issue         |
| [SECURITY.md](SECURITY.md)         | Vulnerability reporting path and covered risks                    | Vulnerability reports and content-integrity concerns |

`AGENTS.md` at the root is the agent-facing entry point and summarizes the same contract.

Root `docs/` holds repository governance only.
It is unrelated to the `docs/audit/` report location convention that audits may find in
subject repositories.
