# GitHub Actions Baseline

## Purpose

> **Scope:** Checkable constraints for GitHub Actions workflows
> **Key items:** SHA pinning, permission floors, script-injection rules, OIDC and secrets,
> workflow-syntax conformance

This file distills the GitHub Actions security-hardening guide and workflow-syntax reference
listed in `references/source-catalog.md` into constraints an audit can verify from workflow
YAML.

Snapshot date: 2026-09-30.

Feeds `assessment/security-review.md` (CI pin discipline), `assessment/deployment-review.md`,
and `assessment/baseline-conformance.md` for CI/CD subjects.

## Action Pinning

From https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions.

- Third-party actions and reusable workflows should be pinned to a full commit SHA
  (`uses: actions/checkout@<40-hex>`). A floating tag (`@v4`) or branch (`@main`) is mutable
  and is the supply-chain pin-discipline finding.
- A trailing `# vX.Y.Z` comment preserves human readability of a SHA pin.
- First-party actions (`actions/*`, `github/*`) carry lower risk but pinning them is still
  the documented hardening posture.
- `GITHUB_TOKEN` defaults must be minimized: `permissions:` declared at workflow or job level
  with least privilege (`contents: read` baseline). Absent `permissions:` means the token
  falls back to permissive repository defaults.
- `pull_request_target` runs with write tokens and secrets on forked PRs - its presence on
  checkout-of-PR-code patterns is the classic privilege-escalation finding.

## Injection And Secrets

- `${{ github.event.* }}` and other untrusted contexts interpolated into `run:` blocks are
  script-injection vectors. The hardened form assigns them to env vars and uses shell quoting,
  or passes them as action inputs.
- Secrets referenced in `if:` or `env:` are safer than inline. `secrets.*` must never appear
  in `run:` echo or artifact paths.
- `pull_request` events don't expose secrets. A workflow that needs secrets on PRs needs
  `pull_request_target` (with checkout restrictions) or `workflow_run` - flag the pairing.
- OIDC (`id-token: write` + `aws-actions/configure-aws-credentials` or similar) replaces
  stored cloud keys. Static AWS keys in secrets are an observation when OIDC is available.

## Workflow Syntax Conformance

From https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax.

- `on:` triggers, `jobs.<id>.runs-on`, and `steps` with `uses:` or `run:` are the required
  skeleton. A job with no `runs-on` or no `steps` is malformed.
- `defaults.run.shell`, `env` scoping, `timeout-minutes`, and `concurrency` groups are the
  operability knobs. Absent `timeout-minutes` lets a hung job burn the default limit.
- `workflow_dispatch` inputs are strings by default. Typed inputs (`number`, `boolean`,
  `choice`) are the checkable form.
- Reusable workflows (`workflow_call`) and matrix strategies are advanced but stable syntax.
  `if:` conditions evaluate without `${{ }}` inside `if:` contexts (the braces are still
  legal but redundant).

## Live Check

When web fetch is available, spot-check the SHA-pinning recommendation and one syntax key
against docs.github.com.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
