# Regression Scenarios

## Purpose

> **Scope:**The regression scenario table exercised when maintaining this skill**Key items:**
> scenario, expected behavior

This file is part of the audit workflow package indexed by `process/audit-workflow.md`.

Follow it when maintaining this skill.

## Regression Scenarios For Skill Changes

When maintaining this skill, exercise these scenarios and check the expected behavior.

These are reasoning checks, not proof of improvement from an independent model benchmark.

| Scenario                                       | Expected Behavior                                               |
|------------------------------------------------|-----------------------------------------------------------------|
| Changelog says tests pass                      | Reported only, readiness evidence incomplete                    |
| Committed scan report lists an advisory        | Reported evidence, finding requires triage                      |
| Documented build steps, no pipeline            | Inspected only, build outcome unknown                           |
| Old crate, no advisory data                    | Freshness concern, vulnerability status unknown                 |
| Guarded panic or excluded module               | Verify reachability, do not invent failure                      |
| Local CLI without hosted runtime               | Assess local safety, omit irrelevant hosted controls            |
| Due diligence with no cost or support data     | Retain unknowns, request artifacts                              |
| Two projects reuse FND-SEC-001                 | Project-qualified shared references                             |
| Clean code with uniform tests                  | No authorship inference, assess test behavior                   |
| Security fix proposed but not run              | Keep verification pending, no closure claim                     |
| Partial cost inputs or no telemetry            | No complete budget or numeric SLO claim                         |
| Previous report at revision 1.9 exists         | New `AUDIT-2.0.md`, previous kept, comparison added             |
| Previous report has no Revision row            | Assume 1.0, new file `AUDIT-1.1.md`                             |
| Previous report uses bold-label `Version`      | Read it as the report revision                                  |
| Previous report found, mode unstated           | Three audit-mode options asked before parameters                |
| Re-audit requested, report found               | Baseline file confirmed before reuse                            |
| Re-audit with changed parameters chosen        | Recovered values are defaults, named params re-asked            |
| Parameter differs between reports              | Capability change in Changes, not a product change              |
| Baseline predates current skill version        | Capability delta applied, named in Validation Protocol          |
| Scorecard gains a dimension on re-audit        | Mean formula restated, movement outside score delta             |
| Re-audit requested, none found                 | User asked before fresh audit at revision 1.0                   |
| Fresh audit over an existing report            | Revision increments, content ignored, fresh IDs                 |
| Reusable library without an API gate           | API Compatibility section included, absence assessed            |
| CWE-295 finding in C#                          | Finding names `CA5359` and its enablement state                 |
| Git author data collected, no finding          | Team & Continuity dashboard line still present                  |
| Mean 5.8 with Security at 4                    | Floor named next to the mean                                    |
| Lockfile present, no SBOM                      | Source-derived component inventory produced                     |
| Other-subject report has a new section         | Apply it or justify `N/A` in the Validation Protocol            |
| Checklist item silently skipped                | Consistency gate fails, named in the Validation Protocol        |
| Same issue type in two projects                | Per-project trade-off, not the combined section                 |
| Shared workspace or build decision             | Row in the combined Solution Comparison                         |
| Multi-project audit                            | Combined summary and Changes precede project blocks             |
| Prior report anchor does not resolve           | Correct anchor recorded, citation flagged                       |
| Census method differs between reports          | Canonical method restated, figure compared                      |
| Scripted edit anchors on `## frontend`         | Complete heading line matched, no `###` hit                     |
| Regex splice touches a table separator         | Whole block rewritten, formatter re-run                         |
| Validator reports more than 10 problems        | Fix and re-run up to three iterations, first-10 display limit   |
| File-mode report at any size                   | Parts written in order, concatenated, removed after gates       |
| Heredoc carries report content                 | Forbidden - part writes via the file tool only                  |
| Scratch dir unwritable by file tool            | `.tmp.` parts beside the output file, deleted after assembly    |
| Previous report confirmed at intake            | Checksum recorded, re-verified at assembly and delivery         |
| Baseline checksum mismatch at re-verify        | Stop and surface, never deliver silently                        |
| Assembly interrupted or output lost            | Resume from parts, `Time taken` keeps original start            |
| Comment-only catch bodies                      | Counted separately from empty bodies                            |
| Evaluation scale prompt shown                  | Four options: 1-10, 1-5, 1-3, Stars - count via follow-up       |
| No previous report exists                      | Default `AUDIT-1.0.md`, `AUDIT.md` as alternative               |
| `document/` exists, `docs/` does not           | Resolved base is `document/`, offered as a location             |
| Non-English request, no language statement     | `pair` output - `AUDIT-<rev>-EN.md` plus `-<LANG>.md`           |
| "Only the Polish report" request               | Single `AUDYT-<rev>.md`, English-first analysis                 |
| Document prose already wraps near 60           | Offer 60 alongside the default 100 at wrap time                 |
| Version-named subdirs under `docs/report/`     | Only the version path offered, no date alternative              |
| Full audit report generated                    | Coverage matrix present, pentest row `Not done`                 |
| Matrix row marked `Covered`                    | No Scope Exclusions bullet disclaims that type                  |
| Manifest has no license fields                 | SBOM License cells `Unknown`, gap feeds findings                |
| Committed advisory report absent               | `Advisory` stays `N` for every component                        |
| Reference Sources table lists repository paths | Defect: external sources only, `[title](url)` per row           |
| Critical finding on public endpoint            | `Exploitability` narrative present, `Theoretical` tier          |
| Narrative claims dynamic verification          | Defect: scope never lifted, tier forced down                    |
| Security finding on internal-only code         | Narrative field omitted                                         |
| Git subject, no tags                           | Deployment frequency proxy `Not specified`                      |
| Single-author repository                       | Bus-factor `High`, Team & Continuity line present               |
| Non-Git subject                                | Delivery Practice section `Not collected`                       |
| Evidence ledger written                        | Every row carries `Observation` or `Concern`                    |
| Polish-language report                         | Headings and dimension names match glossary verbatim            |
| Polish audit request                           | `AUDIT-<rev>-EN.md` and `AUDIT-<rev>-PL.md`, translation last   |
| Explicit review or check request               | `REVIEW.md` with the review-style section set                   |
| Explicit change-set review request             | `REVIEW.md` scoped to the change set                            |
| "Make a structure review" request              | `REVIEW.md` with the structure-review variant contract          |
| Full audit on a code-bearing subject           | Structure Review section before Solution Comparison             |
| Hunt report synthesized                        | No Structure Review content, the assessment was not loaded      |
| Legacy `CHECK-1.0.md` found                    | Not identified as a previous report                             |
| Legacy `REVIEW-1.0.md` lacking `Report Style`  | Legacy shape, never a baseline, name keeps the revision slot    |
| Bare "review this codebase" request            | Audit stays the default, single-dimension when scoped           |
| Existing `REVIEW-1.0.md`, new review           | `REVIEW-1.1.md` written, previous kept                          |
| Review request, `AUDIT-1.0.md` exists          | A report never baselines a report of another style              |
| Automated run requested                        | No question asked, gates resolve to defaults                    |
| Automated run, previous report found           | Re-audit resolves, parameters recovered                         |
| Automated run, update available                | Merge applies when state allows, else a brief note              |
| Audited location holds submodule members       | Fetched members are independent recommended projects            |
| Unfetched submodule member                     | Excluded `not fetched`, disclosed with init hint                |
| Root carries no project signals                | Pure container, the location is the named subject               |
| Collection subject with member skills          | Members are projects, inventory in the root project's block     |
| Automation census is `none`                    | Reduced deployment depth, Deployability bounded                 |
| Automation evidenced outside the tree          | Pointer is `Reported` evidence, no absence finding              |
| Member-internal directory structure            | Assessed inside the member's own project block                  |
| Credentials committed in an excluded project   | Tree-wide secret scan still surfaces the hit                    |
| Executed check fails on missing toolchain      | Triaged `environment limitation`, Limitations row, no finding   |
| Executed run needed a compatibility shim       | Harness disclosed, results labeled shim-assisted                |
| Proxy compile against an available profile     | Labeled proxy evidence, never claims legacy-target verification |
| Defect-census pattern match                    | Candidate confirmed by reading before it becomes a finding      |

