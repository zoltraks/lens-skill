# Deployment Strategy

## Purpose

> **Scope:** Build pipeline, release process, release frequency, manual steps
> **Key items:** reproducible builds, automation, release cadence, manual intervention points

This file guides assessment of how the system goes from source to a running release.

Apply `principles/evaluation-rules.md` throughout. Reverting a release is assessed separately in
`assessment/rollback-review.md`.

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

## Delivery Performance

When production delivery history is available, use the current
[DORA delivery metrics](https://dora.dev/guides/dora-metrics/) at the application/service level.

The consulted guide defines five metrics:

- Change lead time, from commit to production deployment.
- Deployment frequency, deployments per period or time between deployments.
- Failed deployment recovery time, recovery after a deployment requiring immediate intervention.
- Change fail rate, the share of deployments requiring immediate intervention.
- Deployment rework rate, the share of deployments unplanned due to a production incident.

Record the definition, data sources, observation window, sample size, calculation, and exclusions.

Use deployment and incident records, Git commits or release tags alone do not establish these
metrics.

Mark unavailable measurements `UNKNOWN` and zero-denominator ratios as undefined, not zero.

Do not equate failed deployment recovery time with recovery from every type of incident.

If comparing with an older four-metric audit, disclose definition changes before comparing values.

Do not impose historical "elite" bands as universal targets or rank individual contributors.

Use comparable service-level trends to assess change over time.

## Status Criteria

- `PASS`: Builds are automated and reproducible, releases follow a defined automated path, and
  manual steps are minimal and documented.
- `PARTIAL`: Automation exists but key steps are manual, undocumented, or inconsistent across
  environments.
- `FAIL`: Releases are entirely manual and undocumented where automation is clearly required, with
  evidence.
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
