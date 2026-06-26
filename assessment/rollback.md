# Rollback Strategy

## Purpose

> **Scope:** Rollback mechanism, deployment safety, versioning strategy, recovery
> **Key items:** revert path, safe-deploy patterns, version pinning, data migration reversibility

This file guides assessment of how the system recovers from a bad release.

Apply `principles/evaluation-rules.md` throughout. Forward deployment is assessed in `assessment/deployment.md`.

## What To Evaluate

- Rollback mechanism: how a previous known-good version is restored.
- Deployment safety: patterns that limit blast radius, such as staged, canary, or blue-green releases.
- Versioning strategy: how versions are identified and pinned for revert.
- Data reversibility: whether schema and data migrations can be undone safely.

## Evidence To Look For

| Signal                 | Where It Appears                                   |
|------------------------|----------------------------------------------------|
| Revert procedure       | Runbooks, deploy tooling, documented steps         |
| Safe-deploy pattern    | Canary, blue-green, staged rollout configuration   |
| Version pinning        | Immutable tags, release identifiers, artifact pins |
| Migration tooling      | Migration framework, up and down migrations        |
| Backups before release | Backup steps tied to release procedure             |


## Status Criteria

- `PASS`: A defined, tested rollback path exists, deployments limit blast radius, and migrations are reversible or guarded.
- `PARTIAL`: A rollback path exists for code but not data, or safe-deploy patterns are absent, or the path is untested.
- `FAIL`: No rollback path where one is clearly required, with evidence of absence.
- `UNKNOWN`: Rollback and versioning details were not provided.

## Common Risks

- A bad release cannot be reverted quickly, extending incident duration.
- Irreversible migrations make rollback impossible without data loss.
- Lack of staged rollout exposes all users to a defect at once.
- Mutable artifacts make it unclear which version to revert to.

## What Raises Confidence

- A documented and rehearsed rollback procedure.
- Reversible migrations or a forward-fix strategy that is explicitly stated.
- Staged, canary, or blue-green deployment configuration.
- Immutable, pinned versions that map to a known-good state.

Mark each missing signal explicitly rather than inferring its presence.
