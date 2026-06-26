# Deployment Strategy

## Purpose

> **Scope:** Build pipeline, release process, release frequency, manual steps
> **Key items:** reproducible builds, automation, release cadence, manual intervention points

This file guides assessment of how the system goes from source to a running release.

Apply `principles/evaluation-rules.md` throughout. Reverting a release is assessed separately in `assessment/rollback.md`.

## What To Evaluate

- Build pipeline: how artifacts are produced, and whether the build is reproducible and automated.
- Release process: how artifacts reach each environment.
- Frequency: how often releases happen, and whether cadence is sustainable.
- Manual steps: which steps require human action, and where errors can enter.

## Evidence To Look For

| Signal                | Where It Appears                                     |
|-----------------------|------------------------------------------------------|
| Build definition      | Pipeline files, build scripts, container builds      |
| Artifact handling     | Registries, artifact stores, versioned outputs       |
| Environment promotion | Staging and production promotion steps               |
| Release automation    | Deploy jobs, infrastructure-as-code, release scripts |
| Manual procedures     | Runbooks, checklists, documented manual steps        |
| Release cadence       | Changelogs, tags, release history                    |

## Status Criteria

- `PASS`: Builds are automated and reproducible, releases follow a defined automated path, and manual steps are minimal and documented.
- `PARTIAL`: Automation exists but key steps are manual, undocumented, or inconsistent across environments.
- `FAIL`: Releases are entirely manual and undocumented where automation is clearly required, with evidence.
- `UNKNOWN`: Build and release artifacts were not provided.

## Common Risks

- Manual release steps introduce variance and human error.
- Non-reproducible builds make incidents hard to diagnose.
- Environment drift between staging and production hides defects until release.
- Undocumented release steps create a single point of knowledge.

## What Raises Confidence

- A pipeline definition that builds, tests, and deploys from source.
- Versioned, immutable artifacts promoted across environments.
- Documented and minimal manual steps with clear ownership.
- A consistent, observable release cadence.

Mark each missing signal explicitly rather than inferring its presence.
