# lens-skill Software Audit Report

## Document Information

|                    |                                                                            |
|--------------------|----------------------------------------------------------------------------|
| Report Revision    | 1.0                                                                        |
| Report Date        | 2026-09-27                                                                 |
| Detail Level       | Detailed                                                                   |
| Evaluation Scale   | 1-10                                                                       |
| Language           | English                                                                    |
| Audit Purpose      | Engineering improvement                                                    |
| Target Environment | Agent runtime loading `SKILL.md` plus bundled resources, local `git` clone |
| Verification Scope | source-only                                                                |
| Subject Revision   | `495a15b87cd682df7987bd099aaecb61b134f332`                                 |
| Skill Version      | 1.5                                                                        |
| Time taken         | 17:00                                                                      |

## Audit Type Coverage & Assurance Matrix

|  | Report type                                              | Status         | Rationale                                                                           |
|--|----------------------------------------------------------|----------------|-------------------------------------------------------------------------------------|
|  | Software Architecture Review                             | Covered        | Structure, routing, layering, and data flow were inspected from source              |
|  | Code Quality Audit                                       | Covered        | All Python scripts and rule documents were inspected                                |
|  | Security Vulnerability Assessment                        | Covered        | Update-path boundary and script write contracts assessed at source level            |
|  | Open Source License Compliance Review                    | Covered        | License file, notices, and originality evidence inspected                           |
|  | Penetration Test                                         | Not done       | Source-only audit, live exploitation is a separately commissioned engagement        |
|  | Performance Audit                                        | Partially      | Context-budget design inspected, no load or latency measurement performed           |
|  | Cloud Infrastructure Audit                               | Not Applicable | No cloud infrastructure or deployable service in the subject                        |
|  | AI Governance Audit                                      | Not Applicable | The subject is agent instructions, not an [AI](#glossary) runtime or model artifact |
|  | Technical Due Diligence                                  | Partially      | Engineering and delivery dimensions covered, business inputs not supplied           |
|  | [SBOM](#sbom) / Software Composition Analysis            | Covered        | Source-derived inventory produced, no manifests exist to enumerate                  |
|  | Compliance Certification (SOC 2, [ISO](#glossary) 27001) | Not done       | Standards appear only as scoring rubrics, not certification evidence                |

## Glossary

| Term              | Definition                                                    |
|-------------------|---------------------------------------------------------------|
| ADR               | Architecture Decision Record, a recorded design decision      |
| AI                | Artificial Intelligence                                       |
| [API](#api)       | Application Programming Interface                             |
| ASCII             | American Standard Code for Information Interchange            |
| CI                | Continuous Integration                                        |
| CVSS              | Common Vulnerability Scoring System                           |
| [CWE](#cwe)       | Common Weakness Enumeration                                   |
| [DORA](#dora)     | DevOps Research and Assessment                                |
| [EVD](#evd)       | Evidence identifier used by this report                       |
| [FND](#fnd)       | Finding identifier used by this report                        |
| HTTP(S)           | Hypertext Transfer Protocol (Secure)                          |
| IP                | Intellectual Property                                         |
| ISO               | International Organization for Standardization                |
| JSON              | JavaScript Object Notation                                    |
| MIT               | Massachusetts Institute of Technology (license name)          |
| NFR               | Non-Functional Requirement                                    |
| NIST              | National Institute of Standards and Technology                |
| OWASP             | Open Worldwide Application Security Project                   |
| P1-P4             | Remediation priority bands, P1 immediate through P4 long-term |
| [PAR](#par)       | Parity checklist row identifier used by this report           |
| [REC](#rec)       | Recommendation identifier used by this report                 |
| RPO               | Recovery Point Objective                                      |
| [RSK](#rsk)       | Risk identifier used by this report                           |
| RTO               | Recovery Time Objective                                       |
| [SBOM](#sbom)     | Software Bill of Materials                                    |
| SLO               | Service Level Objective                                       |
| SOC               | System and Organization Controls (audit framework)            |
| [STRIDE](#stride) | Threat classification mnemonic                                |
| TDR               | Technical Debt Register entry identifier                      |
| UTF-8             | Unicode Transformation Format, 8-bit                          |
| YAML              | YAML Ain't Markup Language, used for `SKILL.md` frontmatter   |

### API

Application Programming Interface.

In this report it covers contract surfaces such as the `SKILL.md` frontmatter schema and script
verdict protocols.

### CWE

Common Weakness Enumeration.

Security findings cite a [CWE](#cwe) number or a justified `N/A`.

### DORA

DevOps Research and Assessment.

The delivery metrics family (lead time, deployment frequency, recovery, fail rate, rework)
approximated here from Git history as source-derived proxies.

### EVD

Evidence identifier.

`EVD-XXX` rows in the Verification And Evidence Ledger anchor claims to inspected sources.

### FND

Finding identifier.

`FND-[pillar]-XXX` indexes detailed findings per engineering pillar.

### PAR

Parity checklist row identifier.

`PAR-N` rows in the Validation Record attest the mandatory core checklist.

### REC

Recommendation identifier.

`REC-XXX` rows in the remediation roadmap resolve specific findings.

### RSK

Risk identifier.

`RSK-XXX` rows in the Unified Risk Register trace back to findings.

### SBOM

Software Bill of Materials.

Here it means a source-derived component inventory, not a generated or shipped artifact.

### STRIDE

Threat enumeration framework.

Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.

## Executive Summary

Lens is a routed Agent Skill: `SKILL.md` frontmatter plus Markdown instruction resources
(assessment, process, synthesis, references), one translation file, behavioral evaluation prompts,
and six self-contained Python 3 maintenance and report-production scripts.

The audit covered repository structure, frontmatter and specification conformance, the update
path, scripting quality, delivery practice, licensing, and the skill's own maintenance controls.

Overall score: 7.3 / 10.

Lowest applicable dimension: Testability 3 / 10.

Score confidence is `MEDIUM`: structure and documents were fully inspected, while no build,
test, lint, scan, or runtime execution was performed per the source-only scope.

Maturity: `Pre-production`.

The skill is distributed at version 1.5 with a deployable shape, but readiness gates such as
automated verification and a broader ownership base remain open (FND-INF-001, FND-ARC-001).

Readiness state: `Not assessed`.

The audit purpose is engineering improvement, not a release decision.

Two `MEDIUM` findings dominate: internal drift between rule documents and the enforced report
contract (FND-CQY-001), and the absence of any automated test or [CI](#glossary) gate for the
maintenance scripts (FND-INF-001).

## System Context

The subject is the `lens-skill` repository at revision `495a15b`.

It is a single-project Agent Skill, not an application, service, or library.

There is no network listener, no database, no user interface, and no build step.

At audit time an agent loads `SKILL.md`, follows its router to read only the applicable Markdown
resources, and may run the bundled Python scripts as report-production or maintenance tools.

The `scripts/check-update.py` tool is the only component that touches the network: it runs
`git fetch` against `origin/main` over [HTTPS](#glossary) and, after explicit user confirmation, applies
`git pull --ff-only` to update the skill clone.

Report-production scripts are copied into the audited repository under a `.tmp.` name, run only
on report artifacts, and removed afterward.

### Technology Stack

| Layer             | Technology                                      | Evidence |
|-------------------|-------------------------------------------------|----------|
| Skill definition  | `SKILL.md` with [YAML](#glossary) frontmatter   | EVD-007  |
| Instruction rules | Markdown (51 files across 7 directories)        | EVD-001  |
| Tooling           | Python 3, standard library only (7 `.py` files) | EVD-023  |
| Evaluations       | `evals/evals.json`, 22 behavioral prompts       | EVD-016  |
| Translations      | `translations/polish-language.md`               | EVD-001  |
| VCS               | `git`, remote `origin` on GitHub                | EVD-005  |

Detected stacks: Markdown and Python 3.

No package manifests, lockfiles, or build configuration exist.

## Software Bill of Materials

No dependency manifests or lockfiles exist in the repository (EVD-023).

This is a source-derived inventory, not a generated or shipped [SBOM](#sbom).

No third-party packages are vendored or declared.

The Python scripts use only the standard library per `scripts/README.md` and `MAINTENANCE.md`.

| Component | Version        | Ecosystem / purl    | Relationship | Scope   | Integrity  | License   | License Risk | Advisory Checked | Source File       |
|-----------|----------------|---------------------|--------------|---------|------------|-----------|--------------|------------------|-------------------|
| Python 3  | `>= 3.8` (min) | system interpreter  | required     | runtime | n/a system | `Unknown` | Low          | N                | `scripts/*.py`    |
| `git`     | system         | command-line client | required     | runtime | n/a system | `Unknown` | Low          | N                | `check-update.py` |

The `>= 3.8` floor is inferred from the walrus operator in `check-contents.py` (EVD-017), not
declared anywhere in the repository.

No manifest or lockfile means no pinned versions, hashes, or advisory feeds to evaluate.

## License & IP Compliance Review

`LICENSE` is the MIT License, copyright 2026 Filip Golewski (EVD-022).

Every tracked file is original project content.

No vendored code, embedded third-party snippets, or copied upstream assets were found by
inspection (EVD-023).

`CONTRIBUTING.md` requires disclosure of meaningful [AI](#glossary) assistance via commit
trailers.

Two of 67 commits carry a `Co-Authored-By` trailer (EVD-021).

Contributor IP assignment or CLA documents are `NOT SPECIFIED` in the repository.

The single-author history and MIT License grant keep license risk low.

## Health Dashboard

**Risk Map**

| Impact   | LOW              | MEDIUM                    | HIGH |
|----------|------------------|---------------------------|------|
| CRITICAL |                  |                           |      |
| HIGH     | RSK-006          |                           |      |
| MEDIUM   |                  | RSK-001, RSK-004, RSK-007 |      |
| LOW      | RSK-003, RSK-005 | RSK-002                   |      |

**Scorecard Summary**

Bands: `Excellent` 9-10, `Good` 7-8, `Average` 4-6, `Poor` 1-3.

| Dimension               | Score | Notes                                                          |
|-------------------------|-------|----------------------------------------------------------------|
| Testability             | 3/10  | No automated tests, behavioral eval prompts only               |
| Design Soundness        | 8/10  | Routed progressive disclosure, clear directory roles           |
| Code Quality            | 7/10  | Consistent stdlib scripts, known contract drift items          |
| Stack Alignment         | 8/10  | Markdown + stdlib Python per documented conventions            |
| Dependency Health       | 8/10  | Zero package dependencies, runtime floor undocumented          |
| Maintainability         | 8/10  | Registration contract and validators hold, single owner        |
| Deployability           | 7/10  | Git-clone distribution, gated update path, no tags             |
| Scalability             | 8/10  | Line budgets and routing keep the context cost bounded         |
| Security                | 7/10  | Documented threat posture, update integrity rests on user gate |
| Compliance              | 8/10  | MIT License, security policy, no regulated obligations         |
| Observability           | 7/10  | Deterministic verdict output on all tools                      |
| Operational Safety      | 7/10  | Bounded timeouts, ff-only pull, rollback by commit hash        |
| Delivery & Continuity   | 6/10  | Active delivery, single-author concentration is `High`         |
| AI Provenance           | 7/10  | Disclosure policy exists, trailer usage is sparse              |
| Originality & Licensing | 9/10  | Original content, MIT License, no vendored code                |
| Skill Definition        | 9/10  | Frontmatter, routing, and budgets conform to the spec          |
| API Compatibility       | N/A   | Not a reusable library or package                              |

**Team & Continuity**

One author accounts for 100% of the 66 non-merge commits over about 3.7 months, with no tags
and a documented single-maintainer model plus a fork or handoff continuity statement
(EVD-002, EVD-003, EVD-004, EVD-020).

## Delivery Practice & Team Continuity

Git history is available and in scope.

67 total commits, 66 non-merge commits, 1 merge commit.

History span: 2026-06-07 to 2026-09-27.

All 66 non-merge commits share one author, so contributor concentration is `High`
(a single-author project is always `High` per the rubric).

Concentration is a continuity-risk fact, not a judgment of any person.

|  | [DORA](#dora) metric            | Result          | Basis                                      |
|--|---------------------------------|-----------------|--------------------------------------------|
|  | Change lead time                | `NOT SPECIFIED` | Proxy needs tags, commits are not releases |
|  | Deployment frequency            | `NOT SPECIFIED` | No tags or release markers exist           |
|  | Failed deployment recovery time | `NOT SPECIFIED` | Requires incident and deployment data      |
|  | Change fail rate                | `NOT SPECIFIED` | Requires incident and rollback data        |
|  | Deployment rework rate          | `NOT SPECIFIED` | Requires production incident data          |

Four commit subjects mention fix or revert work (EVD-021), but commit subjects are not a
rework metric.

`VERSIONING.md` documents a deliberate no-tag release model: the commit that bumps
`metadata.version` is the release anchor, and consumers pin by commit hash (EVD-022).

Two `Co-Authored-By` trailers appear in history (EVD-021).

Support, cost, and supplier-obligation evidence is `UNKNOWN` (none supplied).

## High-Level Observations

The repository is internally consistent at the mechanical level: every `SKILL.md` router
reference resolves, every Contents table in files over 300 lines is in sync, and frontmatter
conforms to the bundled Agent Skills specification snapshot (EVD-007, EVD-008, EVD-009).

Three documentation-vs-validator drift defects exist inside the report contract itself
(FND-CQY-001), which is the most consequential finding because this skill generates and
validates audit reports from those rules.

There is no automated test or [CI](#glossary) gate anywhere in the project (FND-INF-001).

Every quality gate the project documents is manual and maintainer-run.

Delivery is steady but concentrated in a single author, which is openly documented with a
fork/handoff continuity statement (FND-ARC-001).

The update path is the only trust boundary that touches the network, and it is gated by an
explicit user-confirmation step rather than automatic pulling (FND-SEC-001).

## Auditing Methodology

This audit is source-only.

No builds, tests, linters, scanners, generators, package installation, or runtime execution
were performed against the subject.

Inspection consisted of file census (`git ls-files`), `git log`/`git tag` history queries,
`git status`, and direct reading of all rule documents, scripts, and evaluation data.

`scripts/check-update.py` was executed once as the skill's own bootstrap step (it checks the
skill repository, never the audited subject) and reported `UP-TO-DATE` at tip `495a15b`,
2026-09-27 (EVD-024).

The subject's maintenance validators (`validate-skill.py`, `check-references.py`,
`check-contents.py`) were `NOT RUN` because running the subject's own linters is a scanner
execution against the audited project, outside source-only scope.

Structural claims that those validators encode (reference resolution, Contents-table sync,
frontmatter limits) were instead re-derived manually from source and are recorded as
`Inspected` evidence.

Git commit history was reviewed across the full 67-commit span.

**Reference standards**

- Agent Skills specification, bundled snapshot dated 2026-09-27, for skill conformance.
- `ISO/IEC 25010:2023` product-quality crosswalk, as a scorecard mapping only.
- [CWE](#cwe), for the security-finding weakness classification.
- NIST SP 800-30, for the risk-register process.
- [STRIDE](#stride), for threat-model enumeration.
- [ISO](#glossary) 19011 and the NIST Risk Management Framework monitor step, for the re-audit plan.
- [DORA](#dora) metric definitions, for delivery proxies.

**Verification And Evidence Ledger**

| Evidence ID | Project    | Check / Source                                       | Execution | Result                                                                                                        | Type        | Artifact                                        |
|-------------|------------|------------------------------------------------------|-----------|---------------------------------------------------------------------------------------------------------------|-------------|-------------------------------------------------|
| EVD-001     | lens-skill | `git ls-files` census                                | `N/A`     | 68 tracked files, md/py/json/LICENSE/.gitignore                                                               | Observation | file inventory                                  |
| EVD-002     | lens-skill | `git rev-list --count HEAD` and `--no-merges`        | `N/A`     | 67 total, 66 non-merge commits                                                                                | Observation | revision `495a15b`                              |
| EVD-003     | lens-skill | `git log --no-merges --format=%an` census            | `N/A`     | 66/66 commits by one author (100%)                                                                            | Observation | concentration `High`                            |
| EVD-004     | lens-skill | `git tag -l` and `git log` span                      | `N/A`     | 0 tags, span 2026-06-07 to 2026-09-27                                                                         | Observation | HEAD `495a15b`                                  |
| EVD-005     | lens-skill | `git status -sb`, `git remote -v`                    | `N/A`     | clean tree, `main` == `origin/main`, GitHub remote                                                            | Observation | `zoltraks/lens-skill`                           |
| EVD-006     | lens-skill | `git branch -a`, `git for-each-ref`                  | `N/A`     | single local + remote branch pair, no stashes                                                                 | Observation | ref set                                         |
| EVD-007     | lens-skill | `SKILL.md` frontmatter measurement                   | `N/A`     | name matches dir, description 771/1024, compatibility 360/500, 471/500 lines, `metadata.version` 1.5          | Observation | `SKILL.md:1-24`                                 |
| EVD-008     | lens-skill | router reference resolution scan                     | `N/A`     | 59 backticked references resolve, all resource files registered                                               | Observation | `SKILL.md` router                               |
| EVD-009     | lens-skill | Contents-table re-derivation, 8 files over 300 lines | `N/A`     | every recorded line within tolerance of actual `##` headings                                                  | Observation | Contents tables                                 |
| EVD-010     | lens-skill | baseline-section count comparison                    | `N/A`     | prose lists 17 sections, enforced set has 21                                                                  | Concern     | `report-format.md:342-361`                      |
| EVD-011     | lens-skill | PAR-row bound comparison                             | `N/A`     | text and validator stop at PAR-16, PAR-17 defined                                                             | Concern     | `report-parity.md:37`, `validate-report.py:260` |
| EVD-012     | lens-skill | Pre-Delivery Checklist row inspection                | `N/A`     | `Glossary` row contains stray `587` instead of a rule                                                         | Concern     | `report-format.md:2725`                         |
| EVD-013     | lens-skill | validator glossary rule inspection                   | `N/A`     | SLO/RPO/RTO required unconditionally, not stated in format rules                                              | Concern     | `validate-report.py:408-410`                    |
| EVD-014     | lens-skill | script entry-point comparison                        | `N/A`     | `format-table.py` lacks the argc guard its siblings have                                                      | Concern     | `format-table.py:69`                            |
| EVD-015     | lens-skill | [CI](#glossary) configuration search                 | `N/A`     | no `.github/` or workflow files, validators are manual                                                        | Concern     | `CONTRIBUTING.md:24-33`                         |
| EVD-016     | lens-skill | test-asset census                                    | `N/A`     | no test suite, `evals/evals.json` holds 22 behavioral prompts                                                 | Concern     | `evals/evals.json`                              |
| EVD-017     | lens-skill | language-feature census                              | `N/A`     | walrus operator implies Python >= 3.8, floor undocumented                                                     | Concern     | `check-contents.py:61`                          |
| EVD-018     | lens-skill | `check-update.py` + update-flow inspection           | `N/A`     | bounded 15s timeouts, user-gated ff-only pull, ahead count ignored on `UP-TO-DATE`                            | Observation | `check-update.py`, `SKILL.md:73-95`             |
| EVD-019     | lens-skill | `SECURITY.md` inspection                             | `N/A`     | private advisory channel, covered risks named                                                                 | Observation | `SECURITY.md:11-28`                             |
| EVD-020     | lens-skill | `CONTRIBUTING.md` inspection                         | `N/A`     | single-maintainer model, PR review, AI-disclosure policy                                                      | Observation | `CONTRIBUTING.md:10-45`                         |
| EVD-021     | lens-skill | `git log` trailer and subject scan                   | `N/A`     | 2 `Co-Authored-By` trailers, 4 fix-titled subjects                                                            | Observation | commit messages                                 |
| EVD-022     | lens-skill | `LICENSE` + `VERSIONING.md` inspection               | `N/A`     | MIT License, commit-anchored releases, no tags, no changelog                                                  | Observation | `LICENSE`, `VERSIONING.md`                      |
| EVD-023     | lens-skill | manifest, secret, and vendor census                  | `N/A`     | no manifests, vendored code, or secrets found                                                                 | Observation | tracked-file set                                |
| EVD-024     | lens-skill | `scripts/check-update.py` run (bootstrap)            | `N/A`     | `UP-TO-DATE`, tip `495a15b` dated 2026-09-27                                                                  | Observation | executed once                                   |
| EVD-025     | lens-skill | bundled specification snapshot                       | `N/A`     | conformance baseline recorded, live fetch not run                                                             | Observation | `agent-skills-specification.md:15`              |
| EVD-026     | lens-skill | subject maintenance validators                       | `NOT RUN` | documented checks exist but scanner execution is out of scope                                                 | Observation | `scripts/README.md`                             |
| EVD-027     | lens-skill | builds, tests, lints, runtime execution              | `NOT RUN` | excluded by source-only verification scope                                                                    | Observation | audit scope                                     |
| EVD-028     | lens-skill | formatter vs validator column-width comparison       | `N/A`     | `format-table.py` emits `---` for empty columns, `validate-report.py` expects `--` per the canonical template | Concern     | `format-table.py:47`, `validate-report.py:163`  |

Ledger notes: revision `495a15b87cd682df7987bd099aaecb61b134f332`, clean working tree,
audit date 2026-09-27.

Every row is re-derivable from the named command or file range.

EVD-024 records the skill's own update check, which ran per the skill contract, it is not a
verification of the subject.

**Severity definitions**

| Severity | Meaning                  | Readiness Treatment       |
|----------|--------------------------|---------------------------|
| CRITICAL | Critical contextual risk | Gate resolution           |
| HIGH     | Major contextual risk    | Gate resolution           |
| MEDIUM   | Material contained risk  | Track and plan            |
| LOW      | Limited contextual risk  | Proportionate improvement |

Severity derives from the impact/likelihood matrix, not [CVSS](#glossary).

## Scoring Rubrics

Scale: `1-10` integers, selected at parameter configuration.

| Band      | Score Range | Definition                                                   |
|-----------|-------------|--------------------------------------------------------------|
| Excellent | 9-10        | Capability is comprehensive and verified by strong evidence  |
| Good      | 7-8         | Capability is solid overall, minor or noticeable gaps exist  |
| Average   | 4-6         | Capability is present but uneven, limited, or inconsistent   |
| Poor      | 1-3         | Capability is minimal, fragmentary, or absent where required |

Per-score meanings follow the same matrix in `synthesis/project-scorecard.md`.

`UNKNOWN` and `N/A` are not scores and are excluded from aggregation.

Overall aggregation: arithmetic mean of applicable dimensions, 1 decimal place.

Applicable dimensions: 16 of 17 (`API Compatibility` is `N/A`).

117 / 16 = 7.3125, reported as 7.3 / 10.

The overall score is a descriptive summary, never a production approval.

The [ISO/IEC](#glossary) 25010:2023 coverage crosswalk is applied as a dimension mapping only, not as a
conformance claim.

## Architectural Assessment

The architecture is a three-level routed instruction set.

`SKILL.md` holds spec-conformant frontmatter plus a router that names every resource file and
when to load it.

Resources are partitioned by responsibility into `assessment/` (audit categories),
`process/` (workflow and report contract), `synthesis/` (report sections), `references/`
(taxonomies and schemas), `principles/` (evidence rules), `translations/`, `scripts/`, and
`evals/`, matching the documented directory roles in `MAINTENANCE.md`.

Scripts are split into two classes: self-contained report-production tools (copied into the
audited repository, single-file, no shared imports) and skill-maintenance tools that may
share `scripts/common.py`.

Coupling is low.

The Markdown rule files reference each other by relative path only, and scripts depend on
nothing outside the standard library.

The main structural weakness is duplication between the human-readable contract and the
validator that enforces it: the same section lists, checklist bounds, and table rules live in
prose and in code, and three of those pairs have drifted (FND-CQY-001).

### Design Principles

Single responsibility holds at the file level: each rule document covers one topic, and each
script is one verb-object tool.

Dependency direction is clean: rule documents describe contracts, `validate-report.py` and the
maintenance validators enforce them, and nothing executes the audited project.

The fail-closed choices are consistent: unknown evidence stays `UNKNOWN`, the update path
requires a clean tree, and verdict functions return explicit failure rows instead of silent
passes.

The weakest principle conformance is DRY between prose contracts and validator code, which
produced the drift findings.

### Data Flow Diagram

```
+------------------+        HTTPS git fetch/pull         +-------------------+
| origin/main      | ----------------------------------> | lens-skill clone  |
| (GitHub remote)  |   user-confirmed, ff-only, 15s cap  | (skill files)     |
+------------------+                                     +-------------------+
                                                                  |
                                                          agent loads SKILL.md
                                                          + router resources
                                                                  v
+------------------+        read-only inspection         +-------------------+
| audited repo     | ----------------------------------> | agent context     |
+------------------+                                     +-------------------+
                                                                  |
                                          .tmp. script copies ->  v
                                                         +-------------------+
                                                         | AUDIT-*.md report |
                                                         | (written artifact)|
                                                         +-------------------+
```

Two trust boundaries exist: the upstream remote to clone update path, and the skill clone to
agent instruction load.

The audited repository is read-only to the skill, only the report artifact and `.tmp.` script
copies are written into it.

### Design Patterns

The codebase uses a small set of recurring patterns by convention rather than by framework.

The router pattern in `SKILL.md` is a registry: every resource is listed with load conditions,
and the registration contract in `MAINTENANCE.md` keeps it in sync (verified, EVD-008).

The verdict-line pattern in scripts (`STATUS ...` / `[PASS]` output with a nonzero exit on
issues) is a shared command protocol, partially factored through `scripts/common.py` for the
maintenance tools.

The self-contained single-file constraint on report-production tools is a documented
compensation for the copy-into-subject delivery model.

No anti-patterns beyond the documented duplication were identified.

## Trade-off Analysis

| Decision                                 | Chosen approach                              | Gained                                      | Accepted cost                             |
|------------------------------------------|----------------------------------------------|---------------------------------------------|-------------------------------------------|
| Source-only verification                 | Inspect files only, never build or execute   | Determinism, safety, reproducibility        | No behavioral or runtime verification     |
| Stdlib-only self-contained scripts       | Single-file tools with no shared imports     | Copy into any audited repo works            | Duplicated parsing/formatting logic       |
| Prose contract plus mechanical validator | Rules in Markdown plus `validate-report.py`  | Human clarity plus enforcement              | Drift risk, realized as FND-CQY-001       |
| Commit-anchored releases, no tags        | `metadata.version` bump commit is the anchor | Simple history, hash pinning works          | No tag namespace, weaker discoverability  |
| User-gated skill updates                 | Confirm before `git pull --ff-only`          | Update cannot silently rewrite instructions | Update depends on user presence           |
| Single-maintainer review model           | All changes through one maintainer           | Consistent voice and review quality         | `High` concentration rating (FND-ARC-001) |

Embedded reasoning appears inside the affected findings.

## Threat Model

The attack surface is narrow: one network boundary (the update path) and one content boundary
(skill Markdown becoming agent instructions).

| Boundary           | [STRIDE](#stride) class | Exposure                                                 | Existing control                        | Linked finding |
|--------------------|-------------------------|----------------------------------------------------------|-----------------------------------------|----------------|
| Upstream remote    | Spoofing                | Remote configured by clone, [HTTPS](#glossary) transport | TLS to `origin/main`                    | FND-SEC-001    |
| Upstream remote    | Tampering               | Pulled content becomes agent instructions                | User confirmation + `ff-only` + review  | FND-SEC-001    |
| Upstream remote    | Repudiation             | Commit authorship attribution                            | Git history preserved                   | none           |
| Skill clone        | Tampering               | Local edits alter instructions before load               | Clean-tree gate on update path          | none           |
| Audited repository | Tampering               | `.tmp.` scripts write into the subject tree              | Scoped `.tmp.` names, removal after use | none           |
| Update fetch       | Denial of Service       | Unresponsive remote stalls the check                     | 15s fetch timeout, `FETCH-FAILED`       | none           |
| Report artifact    | Information Disclosure  | Report may carry subject file contents                   | `REDACTED` rule for secrets             | none           |

The dominant threat is supply-chain tampering through the update path.

Its control is a human gate, not cryptographic verification: there are no signed commits or
tags, and the documented release model pins by commit hash (EVD-022).

That gap is recorded as FND-SEC-001.

## Skill Definition Conformance

Baseline: the bundled specification snapshot in `references/agent-skills-specification.md`,
snapshot date 2026-09-27 (EVD-025).

The live specification was not fetched, conformance runs against the bundled snapshot.

| Check                                 | Result | Evidence                                                             |
|---------------------------------------|--------|----------------------------------------------------------------------|
| `name` required, valid, matches dir   | PASS   | `lens-skill`, kebab-case, dir match (EVD-007)                        |
| `description` required, <= 1024 chars | PASS   | 771 chars, states what and when (EVD-007)                            |
| Only allowed frontmatter fields       | PASS   | name, description, license, compatibility, metadata, allowed-tools   |
| `compatibility` <= 500 chars          | PASS   | 360 chars (EVD-007)                                                  |
| `SKILL.md` <= 500 lines               | PASS   | 471 lines (EVD-007)                                                  |
| Progressive disclosure routing        | PASS   | every resource registered with load conditions (EVD-008)             |
| All root references resolve           | PASS   | 59/59 resolve (EVD-008)                                              |
| Contents tables in files > 300 lines  | PASS   | 8 files, all anchors verified (EVD-009)                              |
| `evals/evals.json` shape              | PASS   | valid [JSON](#glossary), `skill_name` match, 22 unique ids (EVD-016) |
| Single `SKILL.md`                     | PASS   | one root file, no nested skills (EVD-001)                            |

Structural conformance holds against the bundled snapshot.

This does not verify that future agents will follow the instructions, which the repository
itself flags as a separate behavioral-verification step (`README.md` verification section).

The maintenance validators that encode these rules were `NOT RUN` (EVD-026), the same checks
were re-derived manually instead.

## Standards Conformance

The project carries documented development standards: `STYLE.md` (prose, tables, encoding),
`MAINTENANCE.md` (directory roles, naming, registration contract), `VERSIONING.md` (release
anchors), `CONTRIBUTING.md` (review and disclosure), and `scripts/README.md` (tool safety).

| Standard area                | Conformance | Evidence                                                     |
|------------------------------|-------------|--------------------------------------------------------------|
| Resource naming (kebab-case) | Conforms    | all file names match the pattern (EVD-001)                   |
| Registration contract        | Conforms    | every resource file registered (EVD-008)                     |
| Contents-table maintenance   | Conforms    | all anchors in sync (EVD-009)                                |
| Prose/table style            | Conforms    | spot-checked documents follow `STYLE.md`                     |
| Versioning policy            | Conforms    | `metadata.version` 1.5 with anchor commits (EVD-022)         |
| Report-contract consistency  | Deviates    | drift items FND-CQY-001 (EVD-010, EVD-011, EVD-012, EVD-028) |
| Script entry-point UX        | Deviates    | `format-table.py` lacks the argc guard (EVD-014)             |
| Update-verdict completeness  | Deviates    | `UP-TO-DATE` ignores local-ahead state (EVD-018)             |

## Strengths & What's Working

- Specification conformance is real, not claimed: frontmatter limits, routing, and budgets
  were measured against the bundled baseline and pass (EVD-007, EVD-008, EVD-009).
- The registration contract is enforced in practice: every resource file is registered, and
  no reference is dangling.
- Six self-contained maintenance and report-production scripts implement the documented
  contracts, including source-width table formatting and report validation, with deterministic
  verdict output.
- The update path is conservative by design: bounded timeouts, a clean-tree gate, `ff-only`
  pulls, explicit user confirmation, and it never touches the audited repository (EVD-018).
- Governance documents exist where most small projects have none: `SECURITY.md` private
  reporting, `CONTRIBUTING.md` AI-disclosure policy, `VERSIONING.md` release anchoring, and a
  Polish translation file with rendering rules.
- `evals/evals.json` encodes 22 behavioral regression prompts covering edge cases such as
  re-audit modes, multi-project reports, and embedded skills.
- Git history is clean and linear with descriptive commit messages, making releases
  traceable by hash even without tags.

## Detailed Technical Findings

| Finding ID  | Pillar                      | Severity | Title                                                             | Status  | Remediation Status |
|-------------|-----------------------------|----------|-------------------------------------------------------------------|---------|--------------------|
| FND-CQY-001 | Code Quality                | MEDIUM   | Contract drift between rule documents and validator               | FAIL    | Open               |
| FND-CQY-002 | Code Quality                | LOW      | Glossary validator enforces a rule prose does not state           | PARTIAL | Open               |
| FND-CQY-003 | Code Quality                | LOW      | `format-table.py` crashes on missing argument                     | PARTIAL | Open               |
| FND-INF-001 | Infrastructure & CI/CD      | MEDIUM   | No automated test or [CI](#glossary) gate anywhere in the project | FAIL    | Open               |
| FND-INF-002 | Infrastructure & CI/CD      | LOW      | Python runtime floor is undocumented                              | PARTIAL | Open               |
| FND-SEC-001 | Security & Compliance       | LOW      | Update-path integrity rests on user gate, not signing             | PARTIAL | Open               |
| FND-ARC-001 | Architecture & Design       | LOW      | Single-author contributor concentration is `High`                 | N/A     | Open               |
| FND-AIP-001 | AI Provenance & Code Origin | LOW      | AI-assistance disclosure is sparse against the policy             | PARTIAL | Open               |
| FND-CQY-004 | Code Quality                | LOW      | `UP-TO-DATE` verdict ignores local-ahead commits                  | PARTIAL | Open               |

### FND-CQY-001: Contract drift between rule documents and validator

* **Pillar:** Code Quality
* **Severity:** Medium
* **Type:** Concern
* **Target Files/Modules:** `process/report-format.md`, `process/report-parity.md`, `scripts/validate-report.py`
* **Requirement Basis:** the registration contract in `MAINTENANCE.md` requires report-format, parity, navigation, and validation material to change together
* **Evidence:** EVD-010, EVD-011, EVD-012, EVD-028, all `Inspected`
* **Confidence:** HIGH - all three defects are directly citable lines
* **Verification State:** observed in source
* **Counter-check:** the parity file was checked for a 16-row bound and defines PAR-17 explicitly, so the drift is real, not a template artifact
* **Security Classification:** N/A - documentation consistency defect, not a weakness
* **Description:** four inconsistencies between prose and enforced contract.

`report-format.md:342` says "seventeen baseline sections" and lists 17, omitting the Coverage
Matrix, [SBOM](#sbom), License and [IP](#glossary), and Delivery Practice sections that
`validate-report.py` enforces and `README.md:49` counts as twenty-one.

`report-format.md:2642` bounds the Validation Record at PAR-1 through PAR-16 while
`report-parity.md:37` defines PAR-17 and `validate-report.py:260` checks only PAR-1..16.

`report-format.md:2725` holds the literal string `587` where the Glossary checklist rule belongs.

`format-table.py:47` seeds a minimum column width of 1, so it emits `---` for an empty column,
while `validate-report.py` expects the canonical `--` that the report template itself uses.
* **Impact:** an agent following the prose produces a report missing enforced sections or checklist rows, which then fails the validator or silently under-validates, the newest parity check (PAR-17, skills inventory) is never mechanically enforced
* **Remediation Recommendation:** update the Standard-mode list to all 21 sections, change the Validation Record bound to PAR-1 through PAR-17, extend `check_par_rows` to cover PAR-17, and restore the Glossary checklist rule text
* **Verification Method:** run `scripts/validate-report.py` on a conforming report containing a PAR-17 row and confirm zero issues, re-read the three corrected lines
* **Exploitability Narrative:** N/A - not a security finding

### FND-CQY-002: Glossary validator enforces a rule prose does not state

* **Pillar:** Code Quality
* **Severity:** Low
* **Type:** Concern
* **Target Files/Modules:** `scripts/validate-report.py`
* **Requirement Basis:** `process/report-format.md` glossary rules state the index covers acronyms used in the report
* **Evidence:** EVD-013, `Inspected`
* **Confidence:** HIGH - the unconditional requirement is three explicit lines
* **Verification State:** observed in source
* **Counter-check:** format rules were searched for the unconditional terms and do not contain them
* **Security Classification:** N/A - validator behavior defect
* **Description:** `validate-report.py:408-410` requires [SLO](#glossary), [RPO](#glossary), and [RTO](#glossary) glossary terms in every report regardless of whether the report uses them, a rule stricter than the documented "index every acronym used" contract
* **Impact:** reports for subjects with no service-level vocabulary fail validation or must carry glossary terms for unused acronyms, and the divergence between code and prose is invisible to maintainers
* **Remediation Recommendation:** either gate the requirement on actual term usage in the report body, or document the mandatory terms explicitly in `process/report-format.md` so the contract is single-sourced
* **Verification Method:** validate a report with no SLO/RPO/RTO usage and confirm the result matches the documented rule
* **Exploitability Narrative:** N/A - not a security finding

### FND-CQY-003: `format-table.py` crashes on missing argument

* **Pillar:** Code Quality
* **Severity:** Low
* **Type:** Concern
* **Target Files/Modules:** `scripts/format-table.py`
* **Requirement Basis:** sibling scripts print a usage line and exit nonzero on missing arguments
* **Evidence:** EVD-014, `Inspected`
* **Confidence:** HIGH - the call site is unconditional
* **Verification State:** observed in source
* **Counter-check:** `validate-report.py`, `validate-skill.py`, and `check-update.py` all guard `sys.argv`
* **Security Classification:** N/A - robustness defect
* **Description:** `format-table.py:69` calls `main(sys.argv[1])` with no argument-count guard, so invoking the script without a path raises `IndexError` instead of the usage line every sibling script prints
* **Impact:** misuse produces an unhandled traceback inconsistent with the documented tool UX, report-production runs could surface a raw error inside an audit session
* **Remediation Recommendation:** add the same `len(sys.argv) != 2` guard with a usage message used by the other scripts
* **Verification Method:** run `python format-table.py` with no arguments and confirm a usage line and exit code 1
* **Exploitability Narrative:** N/A - not a security finding

### FND-INF-001: No automated test or [CI](#glossary) gate anywhere in the project

* **Pillar:** Infrastructure & CI/CD
* **Severity:** Medium
* **Type:** Concern
* **Target Files/Modules:** repository root, `scripts/`, `evals/evals.json`
* **Requirement Basis:** `CONTRIBUTING.md` and `MAINTENANCE.md` define a documented validation procedure, and the scripts enforce correctness for every report the skill produces
* **Evidence:** EVD-015, EVD-016, `Inspected`
* **Confidence:** HIGH - absence verified by full file census
* **Verification State:** observed in source
* **Counter-check:** `evals/evals.json` provides behavioral prompts for an agent harness, but it is not an executable test suite and cannot run in [CI](#glossary) as-is
* **Security Classification:** N/A - process gap, not a weakness
* **Description:** there is no `.github/` workflow, no test directory, no unit tests for the seven Python scripts, and no automated gate for the documented validators, every check in `CONTRIBUTING.md:24-33` is a manual maintainer step
* **Impact:** regressions in validators, formatters, or rule text land undetected until a human runs the manual procedure, the drift defects in FND-CQY-001 are exactly the class of bug a mechanical gate would catch
* **Remediation Recommendation:** add a [CI](#glossary) workflow that runs `validate-skill.py`, `check-references.py`, `check-contents.py`, and `git diff --check` on each pull request, add minimal unit coverage for the script argument and verdict paths
* **Verification Method:** confirm the workflow file exists and a pushed change triggers it on the platform
* **Exploitability Narrative:** N/A - not a security finding

### FND-INF-002: Python runtime floor is undocumented

* **Pillar:** Infrastructure & CI/CD
* **Severity:** Low
* **Type:** Concern
* **Target Files/Modules:** `scripts/check-contents.py`, `scripts/README.md`, `SKILL.md`
* **Requirement Basis:** `SKILL.md` `compatibility` declares interpreter, `git`, and file access but no Python version
* **Evidence:** EVD-017, `Inspected`
* **Confidence:** MEDIUM - the floor is inferred from one language feature, other features may raise it further
* **Verification State:** observed in source
* **Counter-check:** `from __future__ import annotations` defers the PEP-604-style annotations, so 3.8 is the binding feature, not 3.10
* **Security Classification:** N/A - documentation gap
* **Description:** `check-contents.py:61` uses the walrus operator, requiring Python >= 3.8, but no manifest, `compatibility` text, or script README declares a minimum interpreter version
* **Impact:** consumers on older interpreters hit a `SyntaxError` at runtime rather than a clear requirement statement
* **Remediation Recommendation:** declare `Python >= 3.8` in `scripts/README.md` and the `SKILL.md` `compatibility` field, or add a `requires-python` note where the scripts are documented
* **Verification Method:** confirm the declared floor matches the newest language feature used across `scripts/`
* **Exploitability Narrative:** N/A - not a security finding

### FND-SEC-001: Update-path integrity rests on user gate, not signing

* **Pillar:** Security & Compliance
* **Severity:** Low
* **Type:** Concern
* **Target Files/Modules:** `scripts/check-update.py`, `SKILL.md` update flow, `VERSIONING.md`
* **Requirement Basis:** `SECURITY.md` declares skill content integrity a security issue and lists the update path as a covered risk
* **Evidence:** EVD-018, EVD-022, `Inspected`
* **Confidence:** MEDIUM - the trust model is documented and the absence of signing is verified, but the residual risk depends on upstream account security
* **Verification State:** observed in source
* **Counter-check:** [HTTPS](#glossary) transport, the user-confirmation gate, `ff-only` pulls, and divergence detection all bound the exposure, hash pinning gives consumers a manual integrity anchor
* **Security Classification:** CWE-494 - download of code without integrity check, partially mitigated
* **Description:** the skill update path fetches remote content that becomes agent instructions on next load. Integrity relies on [HTTPS](#glossary) transport to `origin/main` plus an explicit user-confirmation and diff-review step. There are no signed commits or tags, and the documented release model pins by commit hash rather than a verifiable signature
* **Impact:** a compromised upstream account could ship malicious instruction content, the user gate reduces but does not eliminate silent acceptance risk
* **Remediation Recommendation:** optionally sign release commits or tags, or publish the release-anchor hash list so consumers can verify before pulling, keep the existing user gate as the primary control
* **Verification Method:** attempt `git verify-tag` or `git log --show-signature` on a release anchor and confirm a signature, or confirm the published hash list matches the tip
* **Exploitability Narrative:** N/A - LOW severity, narrative required only for HIGH/CRITICAL

### FND-ARC-001: Single-author contributor concentration is `High`

* **Pillar:** Architecture & Design
* **Severity:** Low
* **Type:** Observation
* **Target Files/Modules:** repository history, `CONTRIBUTING.md`
* **Requirement Basis:** delivery-practice rubric rates a single-author project `High` concentration
* **Evidence:** EVD-002, EVD-003, EVD-020, `Inspected`
* **Confidence:** HIGH - direct census of all 66 non-merge commits
* **Verification State:** observed in source
* **Counter-check:** `CONTRIBUTING.md` openly documents the single-maintainer model and names fork or handoff as the continuity path, so the risk is acknowledged, not hidden
* **Security Classification:** N/A - continuity fact, not a weakness
* **Description:** one author accounts for 100% of non-merge commits across the project's 3.7-month history, yielding a `High` contributor-concentration rating under the delivery rubric
* **Impact:** maintainer unavailability halts review, merge, and release until a fork or handoff occurs
* **Remediation Recommendation:** nominate a backup reviewer or record an organizational fork owner so the documented handoff path has a named party
* **Verification Method:** confirm a second maintainer or documented owner exists in `CONTRIBUTING.md` or repository settings
* **Exploitability Narrative:** N/A - not a security finding

### FND-AIP-001: AI-assistance disclosure is sparse against the policy

* **Pillar:** AI Provenance & Code Origin
* **Severity:** Low
* **Type:** Observation
* **Target Files/Modules:** `CONTRIBUTING.md`, git history
* **Requirement Basis:** `CONTRIBUTING.md:36-40` asks that meaningful [AI](#glossary) involvement be disclosed via commit trailers
* **Evidence:** EVD-020, EVD-021, `Inspected`
* **Confidence:** LOW - the count of trailers is verifiable, but whether other commits involved undisclosed [AI](#glossary) assistance cannot be determined from source
* **Verification State:** observed in source
* **Counter-check:** code style is not reliable authorship evidence and none was used, the low trailer count may reflect genuinely low [AI](#glossary) usage rather than non-disclosure
* **Security Classification:** N/A - provenance fact
* **Description:** an explicit AI-assistance disclosure policy exists, and 2 of 67 commits carry `Co-Authored-By` trailers, policy compliance cannot be measured from history because undisclosed assistance leaves no trace
* **Impact:** code and content provenance is only partially traceable to tooling, which matters for a skill whose content becomes agent instructions
* **Remediation Recommendation:** continue the existing policy, no structural change is indicated by the evidence
* **Verification Method:** N/A - policy conformance is not mechanically verifiable
* **Exploitability Narrative:** N/A - not a security finding

### FND-CQY-004: `UP-TO-DATE` verdict ignores local-ahead commits

* **Pillar:** Code Quality
* **Severity:** Low
* **Type:** Observation
* **Target Files/Modules:** `scripts/check-update.py`
* **Requirement Basis:** the verdict protocol claims to describe the local-to-upstream state
* **Evidence:** EVD-018, `Inspected`
* **Confidence:** HIGH - the verdict logic only inspects the `behind` count
* **Verification State:** observed in source
* **Counter-check:** being ahead is not an update concern for the check's purpose, so the gap is informational rather than functional
* **Security Classification:** N/A - reporting gap
* **Description:** `check-update.py` reports `UP-TO-DATE` whenever `behind` is 0, regardless of the `ahead` count, so a clone carrying unpushed local commits reports the same verdict as an identical tree
* **Impact:** a caller cannot distinguish "identical to upstream" from "ahead of upstream" from the verdict alone
* **Remediation Recommendation:** include the ahead count in the `UP-TO-DATE` detail output, or emit a distinct status when the clone is ahead
* **Verification Method:** run the checker on a clone one commit ahead of upstream and confirm the output reports the ahead state
* **Exploitability Narrative:** N/A - not a security finding

## Unified Risk Register

| Risk ID | Risk                                                                | Source Finding | Impact | Likelihood | Severity | Mitigation                                |
|---------|---------------------------------------------------------------------|----------------|--------|------------|----------|-------------------------------------------|
| RSK-001 | Prose contract and enforced validator disagree on report structure  | FND-CQY-001    | MEDIUM | MEDIUM     | MEDIUM   | Single-source the contract bounds         |
| RSK-002 | Reports without SLO/RPO/RTO vocabulary fail validation unexpectedly | FND-CQY-002    | LOW    | MEDIUM     | LOW      | Align validator with documented rule      |
| RSK-003 | Script misuse produces a raw traceback inside an audit session      | FND-CQY-003    | LOW    | LOW        | LOW      | Add the standard usage guard              |
| RSK-004 | Script or rule regressions merge without detection                  | FND-INF-001    | MEDIUM | MEDIUM     | MEDIUM   | Add CI running the maintenance validators |
| RSK-005 | Consumers on older interpreters hit an undocumented runtime floor   | FND-INF-002    | LOW    | LOW        | LOW      | Declare the Python >= 3.8 floor           |
| RSK-006 | Malicious upstream content becomes agent instructions via update    | FND-SEC-001    | HIGH   | LOW        | MEDIUM   | Sign release anchors, keep user gate      |
| RSK-007 | Maintainer unavailability halts all project delivery                | FND-ARC-001    | MEDIUM | MEDIUM     | MEDIUM   | Name a backup reviewer or fork owner      |

### RSK-001: Prose contract and enforced validator disagree on report structure

* **Source Finding:** FND-CQY-001
* **Description:** the rule documents and the report validator disagree on baseline section count and parity-row bounds, an agent following prose produces a non-conforming report
* **Impact:** invalid or under-validated reports delivered to users of the skill
* **Likelihood:** MEDIUM - any audit run through the affected paths can hit it
* **Severity:** MEDIUM
* **Confidence:** HIGH - both sides of each drift are citable
* **Triggering Condition:** generating or validating a report under the drifted rules
* **Existing Controls:** the validator catches part of the drift but not PAR-17
* **Mitigation:** reconcile the three drifted texts and extend the validator bound
* **Residual Risk:** LOW after reconciliation
* **Treatment State:** Open
* **Owner:** `NOT SPECIFIED`
* **Closure Trigger:** validator accepts a PAR-17-conforming report

### RSK-002: Reports without SLO/RPO/RTO vocabulary fail validation unexpectedly

* **Source Finding:** FND-CQY-002
* **Description:** the validator hard-requires three glossary terms the format rules do not state
* **Impact:** spurious validation failures or mandatory dead glossary rows
* **Likelihood:** MEDIUM - affects any subject lacking service-level terms
* **Severity:** LOW
* **Confidence:** HIGH - the code path is unconditional
* **Triggering Condition:** validating a report whose subject has no service-level vocabulary
* **Existing Controls:** none
* **Mitigation:** align the validator with the documented rule or document the requirement
* **Residual Risk:** LOW
* **Treatment State:** Open
* **Owner:** `NOT SPECIFIED`
* **Closure Trigger:** validation outcome matches the documented contract

### RSK-003: Script misuse produces a raw traceback inside an audit session

* **Source Finding:** FND-CQY-003
* **Description:** `format-table.py` lacks the argc guard its siblings carry
* **Impact:** unhelpful error output, inconsistent tool UX
* **Likelihood:** LOW - normal report production always passes a path
* **Severity:** LOW
* **Confidence:** HIGH - direct code inspection
* **Triggering Condition:** invoking the formatter without a path argument
* **Existing Controls:** none
* **Mitigation:** add the standard usage guard
* **Residual Risk:** LOW
* **Treatment State:** Open
* **Owner:** `NOT SPECIFIED`
* **Closure Trigger:** usage line and exit 1 on missing argument

### RSK-004: Script or rule regressions merge without detection

* **Source Finding:** FND-INF-001
* **Description:** no automated gate runs the maintenance validators or any test on change
* **Impact:** correctness of every report the skill validates depends on manual diligence
* **Likelihood:** MEDIUM - manual-only gates are routinely skipped under time pressure
* **Severity:** MEDIUM
* **Confidence:** HIGH - absence verified by census
* **Triggering Condition:** a change that breaks a validator or rule file
* **Existing Controls:** documented manual procedure, behavioral eval prompts
* **Mitigation:** add a [CI](#glossary) workflow plus minimal script unit tests
* **Residual Risk:** MEDIUM until the gate exists
* **Treatment State:** Open
* **Owner:** `NOT SPECIFIED`
* **Closure Trigger:** the workflow runs on a pull request

### RSK-005: Consumers on older interpreters hit an undocumented runtime floor

* **Source Finding:** FND-INF-002
* **Description:** Python >= 3.8 is required by the walrus operator but undeclared
* **Impact:** opaque `SyntaxError` for under-version consumers
* **Likelihood:** LOW - Python 3.8 is old enough that most environments exceed it
* **Severity:** LOW
* **Confidence:** MEDIUM - floor inferred, not verified end-to-end
* **Triggering Condition:** running scripts on Python < 3.8
* **Existing Controls:** none
* **Mitigation:** declare the floor in `scripts/README.md` and `compatibility`
* **Residual Risk:** LOW
* **Treatment State:** Open
* **Owner:** `NOT SPECIFIED`
* **Closure Trigger:** declared floor matches actual language features

### RSK-006: Malicious upstream content becomes agent instructions via update

* **Source Finding:** FND-SEC-001
* **Description:** pulled skill content becomes agent instructions, integrity rests on transport and a human gate rather than signatures
* **Impact:** instruction-content compromise affecting every audit run after a poisoned pull
* **Likelihood:** LOW - requires upstream account compromise and user acceptance
* **Severity:** MEDIUM
* **Confidence:** MEDIUM - trust model verified, residual exposure depends on external factors
* **Triggering Condition:** `git pull` of a compromised `origin/main`
* **Existing Controls:** [HTTPS](#glossary) transport, user confirmation, `ff-only`, clean-tree gate, hash pinning
* **Mitigation:** sign release anchors or publish a verifiable hash list
* **Residual Risk:** MEDIUM - the user gate remains the primary control
* **Treatment State:** Open
* **Owner:** `NOT SPECIFIED`
* **Closure Trigger:** a verifiable signature or hash list covers release anchors

### RSK-007: Maintainer unavailability halts all project delivery

* **Source Finding:** FND-ARC-001
* **Description:** 100% contributor concentration with review and merge gated on one maintainer
* **Impact:** development, review, and release stop until a fork or handoff occurs
* **Likelihood:** MEDIUM - single point of contact by design
* **Severity:** MEDIUM
* **Confidence:** HIGH - census is exact
* **Triggering Condition:** extended maintainer unavailability
* **Existing Controls:** documented fork/handoff continuity statement
* **Mitigation:** name a backup reviewer or organizational fork owner
* **Residual Risk:** MEDIUM until a second party exists
* **Treatment State:** Open
* **Owner:** `NOT SPECIFIED`
* **Closure Trigger:** a second maintainer or named owner exists

## Actionable Remediation Roadmap

| Rec ID  | Priority        | Finding     | Recommendation                                                                                    | Impact | Effort | Complexity | Verification                                    |
|---------|-----------------|-------------|---------------------------------------------------------------------------------------------------|--------|--------|------------|-------------------------------------------------|
| REC-001 | [P2](#glossary) | FND-CQY-001 | Reconcile prose contract with the enforced validator (sections, [PAR](#par) bound, checklist row) | High   | Low    | Low        | Validator accepts a PAR-17-conforming report    |
| REC-002 | [P2](#glossary) | FND-INF-001 | Add CI running the maintenance validators plus `git diff --check`, and add script unit tests      | High   | Medium | Medium     | Workflow passes on a pull request               |
| REC-003 | [P3](#glossary) | FND-ARC-001 | Name a backup reviewer or organizational fork owner                                               | Medium | Low    | Low        | Second party recorded in `CONTRIBUTING.md`      |
| REC-004 | [P3](#glossary) | FND-CQY-002 | Align glossary enforcement with the documented rule                                               | Medium | Low    | Low        | Validation matches the stated contract          |
| REC-005 | [P4](#glossary) | FND-CQY-003 | Add the standard argc guard to `format-table.py`                                                  | Low    | Low    | Low        | Usage line and exit 1 on missing argument       |
| REC-006 | [P4](#glossary) | FND-INF-002 | Declare the Python >= 3.8 floor in docs and `compatibility`                                       | Low    | Low    | Low        | Declared floor matches newest language feature  |
| REC-007 | [P4](#glossary) | FND-SEC-001 | Sign release anchors or publish a verifiable hash list                                            | Medium | Medium | Medium     | Signature or hash list verifies the release tip |
| REC-008 | [P4](#glossary) | FND-CQY-004 | Report the ahead count on `UP-TO-DATE` verdicts                                                   | Low    | Low    | Low        | Verdict reports ahead state on an ahead clone   |

### REC-001: Reconcile prose contract with the enforced validator

* **Priority:** [P2](#glossary)
* **Finding:** FND-CQY-001
* **Description:** fix the 17-vs-21 section list in `report-format.md`, raise the Validation Record bound to PAR-17 in the same file and in `validate-report.py`'s `check_par_rows`, and restore the Glossary checklist rule text that was replaced by `587`, and align the formatter's empty-column width with the canonical template
* **Impact:** removes the highest-consequence consistency defect in the skill's core contract
* **Effort:** Low - four localized edits
* **Complexity:** Low - single-file changes plus one code bound
* **Verification:** validate a conforming report containing a PAR-17 row and confirm zero issues

### REC-002: Add CI running the maintenance validators and script unit tests

* **Priority:** [P2](#glossary)
* **Finding:** FND-INF-001
* **Description:** create a workflow that runs `validate-skill.py`, `check-references.py`, `check-contents.py`, and `git diff --check` on pull requests, and add minimal unit coverage for script argument handling and verdict paths
* **Impact:** converts the manual gate into a mechanical one, catching the drift class of FND-CQY-001
* **Effort:** Medium - workflow file plus a small test harness
* **Complexity:** Medium - the eval prompts are behavioral and cannot run as [CI](#glossary) assertions without an agent harness, so scope the gate to the deterministic checks
* **Verification:** the workflow executes on a pull request and fails on an injected violation

### REC-003: Name a backup reviewer or organizational fork owner

* **Priority:** [P3](#glossary)
* **Finding:** FND-ARC-001
* **Description:** record a second party in `CONTRIBUTING.md` or repository settings so the documented fork/handoff continuity path has an owner
* **Impact:** reduces the single point of delivery failure
* **Effort:** Low - documentation and permission change
* **Complexity:** Low - organizational, not technical
* **Verification:** the named party exists and has merge rights

### REC-004: Align glossary enforcement with the documented rule

* **Priority:** [P3](#glossary)
* **Finding:** FND-CQY-002
* **Description:** either gate the SLO/RPO/RTO requirement on actual usage or write the unconditional requirement into `process/report-format.md` so prose and code agree
* **Impact:** eliminates spurious validation failures and a hidden rule
* **Effort:** Low - one code path or one documentation line
* **Complexity:** Low
* **Verification:** validate a report without service-level vocabulary and confirm the outcome matches the written rule

### REC-005: Add the standard argc guard to `format-table.py`

* **Priority:** [P4](#glossary)
* **Finding:** FND-CQY-003
* **Description:** add `len(sys.argv) != 2` handling that prints usage and returns 1, matching every sibling script
* **Impact:** consistent tool UX, no raw tracebacks on misuse
* **Effort:** Low - a three-line guard
* **Complexity:** Low
* **Verification:** run the script with no arguments and observe the usage line and exit code 1

### REC-006: Declare the Python >= 3.8 floor

* **Priority:** [P4](#glossary)
* **Finding:** FND-INF-002
* **Description:** document the minimum interpreter version in `scripts/README.md` and the `SKILL.md` `compatibility` field
* **Impact:** consumers see the requirement before hitting a syntax error
* **Effort:** Low - documentation-only
* **Complexity:** Low
* **Verification:** confirm the declared floor covers every language feature used in `scripts/`

### REC-007: Sign release anchors or publish a verifiable hash list

* **Priority:** [P4](#glossary)
* **Finding:** FND-SEC-001
* **Description:** sign the `metadata.version` bump commits (or add lightweight signed tags), or maintain a published list of release-anchor hashes consumers can verify before pulling
* **Impact:** adds a cryptographic integrity check to the instruction-content update path
* **Effort:** Medium - signing setup and release-process documentation
* **Complexity:** Medium - touches the documented no-tag release model
* **Verification:** `git verify-tag` or a published hash list confirms the tip at the current release anchor

### REC-008: Report the ahead count on `UP-TO-DATE` verdicts

* **Priority:** [P4](#glossary)
* **Finding:** FND-CQY-004
* **Description:** include the `ahead` count in the `UP-TO-DATE` output (or emit a distinct status) so callers can distinguish identical from ahead-of-upstream
* **Impact:** more precise update-state reporting
* **Effort:** Low - one output line change
* **Complexity:** Low
* **Verification:** run the checker on an ahead-of-upstream clone and confirm the ahead count appears

## Scope Exclusions

- Penetration test: not performed, live exploitation is a separately commissioned engagement
  (coverage-matrix `Not done`).
- Compliance certification ([SOC](#glossary) 2, [ISO](#glossary) 27001): not performed, standards appear only as
  scoring rubrics (`Not done`).
- Cloud infrastructure audit: no cloud resources or deployable service exist in the subject
  (`Not Applicable`).
- [AI](#glossary) governance audit: the subject is an instruction set for an agent, not a trained, served,
  or model-dependent [AI](#glossary) system (`Not Applicable`).
- Performance audit beyond design inspection: no load or latency measurement is possible under
  source-only scope (`Partially`).
- Technical due diligence business inputs (cost, support, ownership obligations): not supplied
  (`Partially`, recorded as `UNKNOWN` where applicable).
- API Contract Conformance: omitted - the subject defines, exposes, or consumes no [API](#api)
  contract.
- AI System Assessment: omitted - the subject does not train, serve, or materially depend on
  an [AI](#glossary) runtime, being consumed by an agent is not a runtime dependency of the artifact.
- API Compatibility & Versioning Discipline: omitted - the subject is not a reusable library
  or package, versioning discipline is covered under delivery and standards conformance.
- Architecture Decision Records: omitted - decisions are recorded in policy documents rather
  than [ADR](#glossary) files, and the subject is not a production-bound service.
- Technical Debt Register: omitted - no structural debt distinct from the risk findings was
  surfaced.
- Changes Since Previous Audit: omitted - no previous audit report exists (fresh audit).
- Project Inventory / Skills Inventory: omitted - single project, single skill.
- Any builds, tests, linters, scanners, generators, package installs, or runtime execution of
  the subject: excluded by the source-only verification scope.
- The subject's maintenance validators (`validate-skill.py`, `check-references.py`,
  `check-contents.py`): `NOT RUN` because they are the subject's own scanners.

## Limitations and Unknowns

- All findings rest on static source inspection at revision `495a15b` with a clean tree.
- No behavioral verification exists: whether agents actually follow the routed instructions is
  outside what source inspection can establish, and `evals/evals.json` prompts were reviewed,
  not executed.
- The Python >= 3.8 floor (FND-INF-002) is inferred from one language feature and was not
  verified against an actual interpreter.
- The Agent Skills specification was checked against the bundled snapshot dated 2026-09-27.
  the live specification was not fetched, so any upstream spec drift is `UNKNOWN` (EVD-025).
- AI-authorship compliance is `UNKNOWN` beyond the 2 disclosed trailers, source cannot detect
  undisclosed assistance (FND-AIP-001).
- No committed scanner, coverage, or [CI](#glossary) output exists to cite as `Reported` evidence.
- The skill-maintenance validators were not run, their encoded checks were re-derived manually
  instead, which bounds the claim to spot-level equivalence.
- Business inputs (cost, supplier obligations, support model) were never provided and remain
  `UNKNOWN`.
- Secrets or credential material were not found by inspection, but no secret-scanning tool was
  run, hidden material outside the tracked tree is `UNKNOWN`.

## Re-audit And Follow-up Plan

| Finding     | Priority        | Verification Owner | Closure Evidence                                  | Target Re-audit Trigger              |
|-------------|-----------------|--------------------|---------------------------------------------------|--------------------------------------|
| FND-CQY-001 | [P2](#glossary) | `NOT SPECIFIED`    | Validator accepts a PAR-17-conforming report      | On merge of the reconciliation edits |
| FND-INF-001 | [P2](#glossary) | `NOT SPECIFIED`    | [CI](#glossary) workflow passes on a pull request | On workflow creation                 |

Sign-off gates tied to risk register rows:

- RSK-001 closes when the prose contract and validator agree and a conforming report validates.
- RSK-004 closes when the [CI](#glossary) workflow runs the maintenance validators on pull requests.
- RSK-006 remains open with the user gate as the standing control, a signed release anchor
  would reduce it further.
- RSK-007 closes when a second maintainer or named fork owner exists.

The standard SBOM-drift trigger is not currently armed because no manifests or lockfiles
exist, if a manifest is added later, re-audit on its change.

No HIGH or CRITICAL network-facing finding remains `Theoretical`, so the pentest-escalation
trigger does not apply.

Proposed roles above are not assignments, unknown owners keep sign-off pending even though the
report is final.

## Validation Record

| Check                       | Result     | Evidence / Justification                                                                                                                                                                         |
|-----------------------------|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PAR-1                       | Applied    | FND-SEC-001 carries CWE-494, no other security findings                                                                                                                                          |
| PAR-2                       | Applied    | Severity note states impact/likelihood matrix, not [CVSS](#glossary)                                                                                                                             |
| PAR-3                       | Applied    | [ISO/IEC](#glossary) 25010 crosswalk cited as mapping in Scoring Rubrics                                                                                                                         |
| PAR-4                       | N/A        | Technical Debt Register omitted, no structural debt distinct from risks                                                                                                                          |
| PAR-5                       | Applied    | Team & Continuity line present, anchored to EVD-002..EVD-004                                                                                                                                     |
| PAR-6                       | Applied    | Source-derived inventory produced, no manifests exist                                                                                                                                            |
| PAR-7                       | Applied    | Limitations lists every unrun execution-class check                                                                                                                                              |
| PAR-8                       | Applied    | This table carries all [PAR](#par) rows plus consistency checks                                                                                                                                  |
| PAR-9                       | Applied    | Standards derived from bundled taxonomy and reference files                                                                                                                                      |
| PAR-10                      | Applied    | Glossary indexes every acronym, body occurrences link                                                                                                                                            |
| PAR-11                      | Applied    | Coverage matrix matches Scope Exclusions                                                                                                                                                         |
| PAR-12                      | Applied    | All inventory rows carry `Unknown` license cells, manifest-sourced                                                                                                                               |
| PAR-13                      | Applied    | Every ledger row and finding carries Observation/Concern                                                                                                                                         |
| PAR-14                      | N/A        | No HIGH/CRITICAL security findings exist                                                                                                                                                         |
| PAR-15                      | Applied    | Delivery section present, non-proxy metrics `NOT SPECIFIED`                                                                                                                                      |
| PAR-16                      | N/A        | English report, translation-verbatim rule does not apply                                                                                                                                         |
| PAR-17                      | Applied    | Single-skill conformance recorded, bundled baseline named                                                                                                                                        |
| Cross-reference consistency | PASS       | Every [RSK](#rsk) and [REC](#rec) cites a defined [FND](#fnd)                                                                                                                                    |
| Count reconciliation        | PASS       | 9 findings, 7 risks, 8 recommendations agree across tables                                                                                                                                       |
| Conditional-section check   | PASS       | Included: Data Flow Diagram, Design Patterns, Threat Model, Skill Definition Conformance, Standards Conformance, Re-audit And Follow-up Plan, Glossary, all others justified in Scope Exclusions |
| Formatting rules            | PASS       | No semicolons, [ASCII](#glossary) hyphens only, no `####`, aligned tables                                                                                                                        |
| Parity baseline             | none found | Fresh audit at revision 1.0, no prior AUDIT-*.md exists                                                                                                                                          |

## References

| Reference                                             | Publisher or Author            | Used In                             |
|-------------------------------------------------------|--------------------------------|-------------------------------------|
| Agent Skills specification (snapshot 2026-09-27)      | agentskills.io                 | Skill Definition Conformance        |
| `SKILL.md`, rule documents, and scripts               | zoltraks/lens-skill repository | all sections                        |
| [ISO/IEC](#glossary) 25010:2023 product quality model | [ISO/IEC](#glossary)           | Scoring Rubrics                     |
| Common Weakness Enumeration                           | MITRE                          | FND-SEC-001 classification          |
| NIST SP 800-30 risk assessment                        | [NIST](#glossary)              | Unified Risk Register               |
| [STRIDE](#stride) threat classification               | Microsoft                      | Threat Model                        |
| [ISO](#glossary) 19011 audit follow-up                | [ISO](#glossary)               | Re-audit And Follow-up Plan         |
| NIST Risk Management Framework monitor step           | [NIST](#glossary)              | Re-audit And Follow-up Plan         |
| [DORA](#dora) delivery metrics                        | DevOps Research and Assessment | Delivery Practice & Team Continuity |
| MIT License                                           | Open Source Initiative text    | License & IP Compliance Review      |
| `references/audit-taxonomy.md` source corpus          | zoltraks/lens-skill repository | Coverage matrix canonical types     |
