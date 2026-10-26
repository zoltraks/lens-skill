# Operations Catalog

## Purpose

> **Scope:** Response contract for requests that ask for the skill's complete
> list of operations
> **Key items:** catalog triggers, canonical operations table, inline delivery

This file defines the answer produced when the request asks what operations the
skill performs or assists with.

Follow it when the request says "list all operations", "show all capabilities",
"what operations can this skill perform", "list everything this skill can do",
or an equivalent.

## When This Applies

The request names the skill and asks for the complete list of its operations.

A partial question - "can lens audit dependencies" - is not a catalog request.

Answer it directly instead of reproducing the table.

The catalog is a query surface, not an audit - no intake classification,
parameter resolution, or subject discovery runs.

When the catalog request is the session's first action, the once-per-session
Skill Update Check from `SKILL.md` runs first.

When it follows an activation or another task, the check is not repeated.

## The Catalog

Answer with the operations table below, reproduced inline and re-aligned to
source width when the request's language changes the cell text.

| Family      | Operation             | What it covers                                            |
|-------------|-----------------------|-----------------------------------------------------------|
| Report      | audit                 | full governance report across the assessment categories   |
| Report      | hunt                  | defect-hunt verdict over the same evidence base           |
| Report      | review                | execution-register review                                 |
| Report      | structure review      | the structure-review variant                              |
| Report      | re-audit              | revisioned report compared against a previous baseline    |
| Focused     | security review       | vulnerability and control-verification assessment         |
| Focused     | dependency audit      | supply chain, SBOM, and license review                    |
| Focused     | code quality review   | quality, style, naming, and design-principle assessment   |
| Focused     | testing review        | TDD, coverage, and testability assessment                 |
| Focused     | operational readiness | observability, rollback, and deployment-strategy review   |
| Focused     | maintainability       | maintainability and documentation assessment              |
| Focused     | standards conformance | coding-standards and convention conformance review        |
| Skill       | skill audit           | Agent Skill spec and agent-guidance conformance           |
| Descriptive | inline analysis       | evidence-based description, no report artifact            |
| Enable      | enablement            | bare-activation standby with version and operations table |
| Enable      | self-update check     | once-per-session upstream check                           |
| Enable      | operations catalog    | this table                                                |
| Maintain    | skill maintenance     | changes to this skill repository                          |
| Maintain    | session review        | session lessons harvested into the rule corpus            |

## Response

Deliver the catalog inline.

Write the response in the language of the request - family and operation names
render in that language while the `Family` column keeps its canonical
grouping.

Close with one line inviting a task request.

## What Does Not Apply

- No intake classification, parameter resolution, or subject discovery runs -
  the request named a query.
- No rule files beyond the router and this file load. The catalog table is
  canonical and is not rebuilt by rescanning the repository.
- No file is written and no target is surveyed.
