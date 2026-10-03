# Deployment Strategy

## Purpose

> **Scope:** Build pipeline, release process, release frequency, manual steps
> **Key items:** reproducible builds, automation, release cadence, manual intervention points,
> absent-automation assessment

This file guides assessment of how the system goes from source to a running release.

Apply `principles/evaluation-rules.md` throughout.

Reverting a release is assessed separately in `assessment/rollback-review.md`.

## What To Evaluate

- Build pipeline: how artifacts are produced, and whether the build is reproducible and automated.
- Release process: how artifacts reach each environment.
- Frequency: how often releases happen, and whether cadence is sustainable.
- Manual steps: which steps require human action, and where errors can enter.
- Absent automation: whether a missing pipeline or CI configuration appears intentional or an
  oversight, per `principles/evaluation-rules.md`.

## Evidence To Look For

| Signal                | Where It Appears                                     |
|-----------------------|------------------------------------------------------|
| Build definition      | Pipeline files, build scripts, container builds      |
| Artifact handling     | Registries, artifact stores, versioned outputs       |
| Environment promotion | Staging and production promotion steps               |
| Release automation    | Deploy jobs, infrastructure-as-code, release scripts |
| Manual procedures     | Runbooks, checklists, documented manual steps        |
| Release cadence       | Changelogs, tags, release history                    |

**Pipeline integrity**

For each CI workflow found, run the pin-discipline check from
`references/stacks/ci-github-actions.md`: every `uses:` reference is pinned to a commit SHA or
a versioned tag of a trusted publisher, mutable refs such as `@main` or floating major tags on
third-party actions are recorded, and unpinned first-party actions follow the project's own
policy.

The check reads workflow files as text - it never fetches the referenced actions.

A mutable third-party ref is a supply-chain exposure finding class, not a style note.

## Buildability And Defaults

Check toolchain compatibility statically: compare builder and CI image versions, manifest
toolchain floors, and documented prerequisites against the language features and APIs the
code uses and each dependency's declared minimum.

A builder image that predates a used feature is a build defect raised from source alone -
record the feature, its requirement evidence, and the image tag.

Census the shipped defaults: ports, bind addresses, credentials, debug endpoints, transport
security, file permissions, and healthcheck semantics, checked against least-privilege
expectations and documented operator obligations.

Check portability assumptions: path separators, shell-string construction, and
platform-specific behavior against the supported-platform claims.

## Absent Automation

When no pipeline definition or CI configuration exists in the supplied files, record the finding
anyway and classify the absence per `principles/evaluation-rules.md`.

| Signal                | Example                                                           |
|-----------------------|-------------------------------------------------------------------|
| Envisaged but missing | `CONTRIBUTING.md` or `README` prescribes checks that nothing runs |
| Envisaged but missing | `.github/` or `.gitlab/` exists without workflow definitions      |
| Envisaged but missing | Badges, pull request templates, or branch rules reference checks  |
| Envisaged but missing | Build, release, or deploy scripts exist that nothing invokes      |
| Deliberate omission   | Documentation limits the delivery model: prototype, local-only    |
| Deliberate omission   | A documented manual release process replaces automation           |
| Deliberate omission   | No delivery or release process is envisaged at all                |

State the reading plainly, for example "no CI configuration was found and the repository shows no
signal that automation was envisaged" or "the documented validation steps have no pipeline behind
them".

When the signals conflict or are absent, classify `Undetermined`.

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

When only repository evidence is available,
the git-derived proxies and contributor-concentration rubric live in the Delivery Practice & Team
Continuity section per `references/delivery-practice.md`.

Those proxies are labeled as proxies and never presented as measured DORA metrics.

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

The status records the capability state.

The absent-capability token records the intent reading alongside it, it does not change the status.

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
