# Project Health Baseline

## Purpose

> **Scope:** Checkable signals for open-source project hygiene and community files
> **Key items:** OpenSSF best-practices criteria, community-health file conventions,
> SECURITY.md semantics, gitignore coverage

This file distills the OpenSSF Best Practices criteria, GitHub community-health docs, and the
gitignore template collection listed in `references/source-catalog.md` into constraints an
audit can verify from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/documentation-review.md`, `assessment/operational-readiness.md`, and the
project-health pillar of multi-file subjects.

## OpenSSF Best Practices

From https://www.bestpractices.dev/en/criteria (bare `bestpractices.dev` URLs fold into this
row).

- The criteria levels (passing -> silver -> gold) map to a checklist of practices. The
  source-verifiable subset: `LICENSE` file present and OSI-recognized, `README` present,
  versioning scheme used, public issue tracker implied by repo hosting, `SECURITY.md` or
  vulnerability-report channel, tests exist, CI exists, static/dynamic analysis configured.
- A `bestpractices.dev` badge in README is `Reported` evidence. The criteria file the badge
  claims is verifiable in-repo.

## Community Files

From https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions
and https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository.

- The health files: `README`, `LICENSE`, `CODE_OF_CONDUCT`, `CONTRIBUTING`, `SECURITY.md`,
  issue/PR templates, `CODEOWNERS` - each carries a documented role. `SECURITY.md` is where
  GitHub surfaces the vulnerability-report path and supported versions.
- `SECURITY.md` semantics: a `## Supported Versions` table and a private reporting channel
  (email/advisory form), not just "report issues".
- `CONTRIBUTING.md` defines the pre-merge bar. Absent contribution rules plus claims of
  review practice is a docs-to-code drift finding.
- `CODEOWNERS` expresses review ownership. It only matters when branch protection enforces
  it - the file alone is intent.

## Ignore Coverage

From https://github.com/github/gitignore.

- `.gitignore` should cover the stack's artifacts (`node_modules`, `__pycache__`, `target/`,
  `vendor/`, `dist/`, `*.log`, `.env`, OS noise). An empty or stack-mismatched `.gitignore`
  plus committed artifacts is a defect.
- Committed noise (`.DS_Store`, `Thumbs.db`, editor swap files, `*.log`) in tracked files is
  a direct finding regardless of `.gitignore` content.
- Secret-file patterns (`.env`, `*.pem`, `credentials.json`, `id_rsa`) should be ignored
  before they can be committed. A tracked file matching a secret pattern is a finding.

## Live Check

When web fetch is available, spot-check one criterion against bestpractices.dev and one file
name against the GitHub community-health docs.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
