# Operations Catalog

## Purpose

> **Scope:** Response contract for requests that ask what the skill can do - the complete
> operations list or one slice of it
>
> **Key items:** catalog triggers, partial questions, canonical operations table, inline delivery

This file defines the answer produced when the request asks what operations the skill
performs or assists with.

Follow it when the request says "list all operations", "show all capabilities",
"what operations can this skill perform", "list everything this skill can do", or an equivalent.

## When This Applies

The request names the skill and asks for the complete list of its operations.

A partial question - "can lens audit dependencies" - is not a catalog request.

Answer it per Partial Questions below instead of reproducing the table.

The catalog is a query surface, not an audit - no intake classification, parameter resolution,
or subject discovery runs.

When it follows an activation or another task, the check is not repeated.

## The Catalog

Answer with the operations table below, reproduced inline and re-aligned to source width when the
request's language changes the cell text.

| Operation             | Family      | What it covers                                                                  |
|-----------------------|-------------|---------------------------------------------------------------------------------|
| audit                 | Report      | full governance report across the assessment categories                         |
| hunt                  | Report      | defect and health register over the same evidence base                          |
| hunt (legacy)         | Report      | preserved pre-redesign verdict/domain hunt layout                               |
| brief                 | Report      | compact status-driven decision brief over the same evidence base                |
| review (legacy)       | Report      | preserved execution-register review layout                                      |
| structure review      | Report      | the structure-review variant                                                    |
| re-audit              | Report      | revisioned report compared against a previous baseline                          |
| security review       | Focused     | vulnerability and control-verification assessment                               |
| dependency audit      | Focused     | supply chain, SBOM, and license review                                          |
| code quality review   | Focused     | quality, style, naming, and design-principle assessment                         |
| testing review        | Focused     | TDD, coverage, and testability assessment                                       |
| operational readiness | Focused     | observability, rollback, and deployment-strategy review                         |
| maintainability       | Focused     | maintainability and documentation assessment                                    |
| standards conformance | Focused     | coding-standards and convention conformance review                              |
| skill audit           | Skill       | Agent Skill spec and agent-guidance conformance                                 |
| inline analysis       | Descriptive | evidence-based description, no report artifact                                  |
| audit request         | Generate    | generalized prompt commissioning an external-agent audit                        |
| history visualisation | Generate    | development-history `history.json` dataset for lifecycle interfaces, named-only |
| enablement            | Enable      | bare-activation standby with version and operations table                       |
| self-update check     | Enable      | upstream check on working modes or explicit request                             |
| operations catalog    | Enable      | this table                                                                      |
| skill maintenance     | Maintain    | changes to this skill repository                                                |
| session review        | Maintain    | session lessons harvested into the rule corpus                                  |
| report benchmark      | Maintain    | external-report comparison feeding skill improvement                            |
| stack feed            | Maintain    | external standards-source intake extending the corpus                           |

## Response

Deliver the catalog inline.

Write the response in the language of the request - family and operation names render in that
language while the `Family` column keeps its canonical grouping.

Close with one line inviting a task request.

## Partial Questions

A partial capability question asks about one slice of the skill rather than the complete
operation list - "can lens audit dependencies", "what report types does lens produce".

Answer it from the loaded router and this file with no further rule-file loads.

Open with a one- or two-sentence summary.

When the answer enumerates a fixed set - report styles, detail levels,
or operation families - render it as a compact table, one row per item,
aligned by source width.

A shared parameter that applies to every item, such as a detail-level or language list,
follows the table in one line rather than repeating inside cells.

Keep the answer brief - no audit framing, no section walkthrough,
and no prose restatement of the table.

Write the answer in the language of the request.

## What Does Not Apply

- No intake classification, parameter resolution,
  or subject discovery runs - the request named a query.
- No rule files beyond the router and this file load.
  The catalog table is canonical and is not rebuilt by rescanning the repository.
- No file is written and no target is surveyed.
