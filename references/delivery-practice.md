# Delivery Practice Methodology

## Purpose

> **Scope:** Git-derived delivery-practice proxies and the contributor-concentration rubric for
> the Delivery Practice & Team Continuity section
> **Key items:** five-metric DORA model, source-only proxies, bus-factor rubric, NOT SPECIFIED
> discipline

This file defines how a source-only audit approximates delivery health.

Technical due diligence weighs the team's delivery habits alongside the code itself,
and delivery health is measured with the DORA metrics.

A repository alone cannot supply most of them,
so this file states exactly which proxies are computable and which fields must stay `NOT SPECIFIED`
rather than be omitted or invented.

Apply `principles/evaluation-rules.md` throughout.

Proxy figures are derived evidence about the repository, not measurements of a production pipeline.

## DORA Metrics Under A Source-Only Audit

The distilled DORA model, SLO definitions, and NIST SSDF practice anchors live in
`references/methodology/delivery-metrics.md`.

Consult that digest before citing the live DORA source.

The current DORA model has five metrics.

Two are approximable from Git history, three are not:

| DORA metric                     | Source-only proxy                                     | Reporting rule                              |
|---------------------------------|-------------------------------------------------------|---------------------------------------------|
| Change lead time                | Median interval between a commit and its first tagged | Computed proxy, labeled as a proxy estimate |
|                                 | release                                               |                                             |
| Deployment frequency            | Tag or release cadence over the observed window       | Computed proxy, labeled as a proxy estimate |
| Failed deployment recovery time | None, requires incident and deployment data           | `NOT SPECIFIED` with the reason             |
| Change fail rate                | None, requires incident and rollback data             | `NOT SPECIFIED` with the reason             |
| Deployment rework rate          | None, requires production incident data               | `NOT SPECIFIED` with the reason             |

## Computing The Proxies

Use the canonical census commands in `references/census-commands.md` so a re-audit reproduces
the figures.

- **Deployment frequency proxy.** List tags (`git tag`) with creation dates, count tags per
  observed month or quarter. A project with no tags gets `NOT SPECIFIED`, not a commit-cadence
  substitution, commits are not deployments.
- **Change lead time proxy.** For each tag, take the earliest commit it contains, compute the
  interval between that commit's date and the tag's date. Report the median interval and the
  window it covers. State that this measures release lag, not true production lead time.
- **Reviewer diversity.** Pull-request review data does not live in the repository. Merge-author
  vs commit-author overlap in `git log` is the only proxy available, label it as such or mark
  `NOT SPECIFIED`.

## Bus-Factor Rubric

Score contributor concentration from `git log --no-merges --format="%an"` per
`references/census-commands.md`.

Agent-bot author identities (`copilot-swe-agent[bot]`, `devin-ai-integration[bot]`, and the
other signatures in `references/methodology/ai-provenance.md`) are excluded from the
contributor count and reported separately through the attribution census - a bot is not a
bus-factor contributor and not a second active contributor.

| Share of commits from the top author | Concentration rating |
|--------------------------------------|----------------------|
| >= 80%                               | HIGH                 |
| 50-79%                               | MODERATE             |
| < 50% with >= 2 active contributors  | LOW                  |

"Active" means commits in the observed window, not lifetime contributors.

A single-author project is always `HIGH`.

Record the top-author share, the active-contributor count, and the window.

Concentration is a continuity-risk fact, not a judgment of any person.

Report it in aggregate form only, never as a personal assessment.

## Boundary With Deployment Review

`assessment/deployment-review.md` assesses declared pipeline and deployment evidence:
CI configuration, release mechanisms, gates, rollback design.

This file covers only the git-derived delivery metrics and contributor concentration.

Do not duplicate pipeline findings into the Delivery Practice section, reference them.

When no pipeline exists at all, the absence assessment lives in `assessment/deployment-review.md`
per `principles/evaluation-rules.md`, not here.

## Rules

- A proxy is never presented as a measured DORA metric. Label each computed value as a proxy.
- `NOT SPECIFIED` fields stay in the table with their reason. Omitting them implies they were
  measured.
- Non-Git subjects mark the whole section `NOT COLLECTED`, mirroring the PAR-5 rule for the
  Team & Continuity line.
- Concentration figures anchor to `EVD-XXX` rows.
