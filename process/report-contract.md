# Report Contract

## Purpose

> **Scope:**The mechanically enforced surface of every Lens report**Key items:** required sections,
> field syntax, token vocabularies, style-specific rules

This file lists only what `scripts/validate-report.py` enforces - nothing more.

The same contract is available as JSON through `python3 scripts/validate-report.py --dump-contract`,
generated from the live constants, so an agent can load it without reading this file.

Rationale and detail live in the section specs under `process/report-format/` and `synthesis/` -
this page is the fast check, not the specification.

## Every Report

- Headings never go deeper than `###`, and every heading is followed by exactly one blank line.
- No semicolons in prose outside code spans and link targets - use a comma or split the sentence.
- No em dash, en dash, or Unicode arrow outside code spans - use `-` and `->`.
- Table cells carry tokens and short phrases,
  not sentences - a cell over roughly 80 characters is a defect. Narrative, rationale,
  and file:line detail live in the block or paragraph around the table, not inside a cell.
  Link markup counts toward cell width, which is why register titles stay terse.
- Every table's separator widths match its header cell widths and all pipes align vertically - run
  `scripts/format-table.py` rather than aligning by hand.
  Column widths count the full `[text](target)` markup - brackets, text, and target together.
- Every register identifier (`EVD`, `FND`, `RSK`, `REC`, `TDR`, `PAR`)
  cited outside its defining location links to its definition - `### <ID>:` heading anchors for
  block registers, the register's section anchor for `EVD` / `PAR` rows - and every such link
  resolves to a real heading anchor, and `scripts/link-references.py` applies the pass.
- No trailing whitespace, and the closing line `End of audit report` is never written.
- Document Information carries `Report Style`, `Evidence Mode`,
  and a `Subject Revision` snapshot anchor.
- A report under `Evidence Mode: source-only` carries a `Further Verification` - under
  `executed-readonly` or `executed-commands` an `Executed Evidence` replaces it,
  and an executed `review` -style report additionally carries an Artifact Manifest.
- The Audit Coverage table keeps only `Covered`, `Partially`,
  and `Not done` status cells - `Not Applicable` rows are omitted entirely.
- The Validation Protocol is a run-internal record reported inline during the run - rows `PAR-1`
  through `PAR-33` in fixed order - and enters the report only when the request asks for it.
- At `Detail Level: Detailed`, when `## Glossary Index` is present,
  it carries a separate `**Identifier triplets**` table (`Triplet | Scope | Description`)
  after the alphabetical `Term | Definition` index table, starting with `FND` and `EVD`,
  followed by the other register triplets (`TDR`, `RSK`, `REC`, `PAR`)
  and every three-letter criteria prefix and finding-pillar triplet used in the report.
- The `Structure Review` section carries the five verdict rows (`Directory organization`,
  `Naming conventions`, `Component placement`, `Supporting-artifact layout`, `Consistency`)
  with verdict tokens `Passed`, `Partially`, `Failed`, `Unknown`, or `N/A`,
  and when the conditional `Structure Conformance` section is present its conformance tables carry
  valid status tokens, and when the conditional `Code Style` section is present its lens sub-score
  table and census rows carry valid status tokens.
- The closing Reference Sources section lists external authoritative sources only - each linked
  source renders a `[title](url)` link paragraph and an unlinked source renders its title without a
  link, `No external sources consulted` replaces the table,
  and repository paths never appear as references.
- `FND`, `RSK`, and `REC` references must resolve to defined entries - a `REC-XXX` or `RSK-XXX` cite
  of a nonexistent `FND-` fails.
- Reports carry no `State` row: every generated report is a final artifact,
  and gate outcomes are recorded in run state and the inline protocol instead of
  an in-progress marker.

## Field Blocks

- The only parsed field syntax is `* **Field:** value` - an asterisk bullet, a bold field name,
  a colon outside the bold.
- Every register block (`FND`, `RSK`, `REC`, `TDR`)
  opens with a description paragraph directly under its `### ` heading,
  before the field list - the paragraph may span multiple sentences or paragraphs and carries no
  `Description` field label.
- Finding blocks require, in order: `Pillar`, `Severity`, `Type`, `Targets`, `Basis`, `Criteria`,
  `Impact`, `Method`, `Confidence`, `Mitigating factors`, `Evidence`, `Recommendation`.
- `Verification` appears only when the finding was verified - a `Yes` / `No` lead with a title-cased
  qualifier, never a lowercase `yes` / `no` prefix.
  `Runtime` appears only when execution confirmed the behavior.
- `Status` appears only when it differs from `Open`,
  and `Change` only when it differs from `New` - both are lifecycle defaults and carry no
  information at the default value.
- Risk blocks require: `Severity`, `Likelihood`, `Residual`, `Impact`, `Trigger`, `Controls`,
  `Closure`, `Source`, `Confidence`, `Mitigation`.
- Recommendation blocks require: `Priority`, `Finding`, `Condition`, `Impact`, `Effort`,
  `Complexity`, `Verification`.
- Debt blocks require: `Category`, `Source` - `Cost` and `Delay` appear only when they carry a real
  estimate or qualitative note, and never an `Insufficient information` token a value with no
  estimable basis omits the field entirely.
- A risk block's `Source` names a defined `FND-`,
  a recommendation block's `Finding` names a defined `FND-` and its `Depends on` names defined
  `REC-` identifiers or `none`, and a debt block's `Source` is a defined `FND-` or
  `Direct observation`.
- Recommendation `Priority` starts with `P1` - `P4`. Debt `Category` is `Reliability`,
  `Performance Efficiency`, `Security`, or `Maintainability`, and debt `Status` is `Open`,
  `In progress`, or `Resolved`.
- Finding identifiers match `FND-<pillar>-NNN` with pillar `ARC`, `CQY`, `SEC`, `INF`, `AIP`,
  `CPR`, `API`, or `STR`.
- `Type` is `Observation` or `Concern`. `Runtime` appears only when the reported behavior was
  confirmed by execution - never a lowercase `yes` / `no` / `not applicable` prefix.
  `Breaking change` starts with `None`, `Internal`, or `Public API`.
  `Applicability` starts with `applicable`, `conditional`, `inapplicable`, or `unverified`.
- `Provenance basis` starts with `Declared`, `Attested`, `Supplied`, `Indicated`,
  or `Undetermined` - required on `FND-AIP-` blocks, omitted on other pillars.
- A `Criteria` value never renders `N/A` or a placeholder,
  and each cited criteria entry resolves to a declared row of the report's `**Criteria table**` with
  a three-letter prefix and no redundant `-01` suffix - `audit` -style findings naming criteria
  without a declared table fail.
- A field whose value would be `N/A` or empty is omitted, never rendered blank.
- Legacy field names such as `Verification State` or `Remediation Status` are rejected - the current
  names are the ones above.

## Token Casing

English renders title case where the vocabulary lists give canonical uppercase names.

- Finding `Status`: `Open`, `Closed`, `Pass`. Finding `Change`: `New`, `Unchanged`, `Reopened`,
  `Closed`. Summary `Verification`: `Verified`, `Confirmed`, `Reported`, or empty for `New`.
- Risk `Status`: `Open`, `Accepted`, `Transferred`, `Monitoring`, `Closed`.
- Classification `Class`: `Recommended`, `Optional`, `Not recommended`.
- `Absence`: `No documented rationale`, `Deliberate - recorded decision`, `Undetermined`.
- A summary row's `Verification` / `Confirmed` claim must agree with the block's `Verification`
  and `Runtime` fields.

## Scorecard And Overall Score

- `**Scorecard Summary**` rows carry numeric `n/m` Score cells - the validator recomputes the mean
  and compares it to every stated `Overall score` row in `hunt` and `review` reports,
  and they must agree.
- `Overall score` never appears inside the scorecard table - it lives in the Executive Summary
  key-value table, where its value renders bold.
- An audit Executive Summary carries `Product Quality` and `Engineering Process` rows in the
  headline score table and states the overall once,
  in the key-value `Overall score` row - a numeric sub-score value names `lowest` within six lines,
  a paragraph below the headline table names `Product-only` when `Engineering Process` is
  `Not published` and names `ceiling` when the overall sits below the value recomputed from the
  displayed sub-scores, and every headline value recomputes from the displayed scorecard cells under
  the catalogue tier weights.
- An audit `Requirements Conformance` table keeps one row per requirement - a merged range row such
  as `A-01 through A-11` or `A-01..A-11` fails.
- Every `Dimension | Score` table - each `**Scorecard Summary**` table and every table inside a
  `Health Dashboard` section - uses only the 19 canonical dimension names,
  in canonical order with `N/A` rows omitted, and each Score cell renders `n/m`, a star bar,
  or `Unknown` with an optional `[lo-hi]` interval.
- Every `Health Dashboard` section - single-project or per-project - carries a `Risk Map`,
  a `Scorecard Summary`, and a `Team & Continuity` marker (bold label or heading).
- Document Information rows come from the canonical field list in
  `process/report-format/report-opening.md`, mirrored in the generated contract below:
  `Skill Version` renders the bare version string (for example `2.6.5`),
  never prefixed with the skill name, and no row carries an empty or `Not specified` value.
- In `hunt` and `review` reports every line stating an overall `x.y/n` score needs the word
  `lowest` within six lines.
- `N/A` scorecard rows are omitted, never rendered.
- A Score cell's `n/m` value leads the cell,
  and an optional `[lo-hi]` uncertainty interval follows it - the validator's scorecard checks read
  the `n/m` value, and a rendered interval must contain the point score, stay within the scale,
  and be non-degenerate.

## Multi-Project

- A report with a `Project Inventory` never uses `both`, `either`,
  or `the projects` as a table cell - rows name each project explicitly.
- Register identifiers stay bare - `FND-SEC-001` - in shared sections and project blocks alike.
  Every register family numbers report-globally, so the bare identifier is unambiguous.
- The `Project` column appears only in shared tables - a single-project evidence
  ledger must not carry one.
- The `Remediation Roadmap` renders once at level 2 - immediately before `Reference Sources` -
  carrying `Recommendation Classification` and `Follow-up Plan` only as `###` subsections,
  never as standalone sections or per-project blocks.

## Hunt Style

Under `Report Style: hunt` the required sections are Document Information, Audit Type Coverage,
Verdict, System Context, Methodology And Evidence, Journey Traces, Domain Findings, Risk Register,
Remediation Phases, Scope Exclusions, Known Limitations, Reference Sources - plus Glossary,
Contradiction Register, and the handoff or executed-log section when conditional.

- The Verdict section carries a `Verdict:` token (`Ready`, `Conditionally ready`, `Not ready`),
  a domain ratings table, a gates table, a top-five actions list citing `REC-` / `FND-` identifiers,
  and at most five strengths.
- Domain ratings cover the fixed set Correctness, Security, Reliability, Performance, Dependencies,
  Deployment, Testability, Documentation, Maintainability, Provenance with values `Red`, `Amber`,
  `Green`, `Not assessed`. A `Red` or `Amber` row cites an `FND-` in its Basis.
- Journey hop tables use `Hop | Status | Evidence` with `conforming`, `failing`,
  or `not assessable` - a `failing` hop cites a defined `FND-`.
- The producer/consumer `Representation match` column takes `conforming`, `partially conforming`,
  `failing`, or `not assessable`.
- Domain Findings replaces Technical Findings for the summary-table and count checks - `###` domain
  headings sit inside the section and end only at the next `##`.
- Every `### FND-` block maps to a remediation phase or an `Accepted - no action` row,
  and multi-project findings match by the `(<project>)` heading qualifier.
- A `Recommendation Classification` section is forbidden under hunt - phases carry the disposition.
- Every `High` or `Critical` finding carries a `Defect scenario` field - initial conditions, steps,
  expected result, observed result, confirmation level.
  The requirement binds `audit` and `hunt` styles alike,
  and `Source` -level confirmation satisfies it.

## Review Style

Under `Report Style: review` the required sections are Document Information, Audit Type Coverage,
Verdict, System Context, Check Plan And Methodology, Execution Register, Domain Findings,
Risk Register, Improvement Plan, Scope Exclusions, Known Limitations,
Reference Sources - plus the conditional Retest Register, Metrics Snapshot, Artifact Manifest,
Glossary, Contradiction Register, and the handoff section.

- The Verdict carries the same verdict token, domain ratings, gates, top-five,
  and strengths rules as hunt.
- The Execution Register table carries `Check`, `Command`, and `Result` columns,
  and `Result` cells take `Pass`, `Fail`, `Error`, `Blocked`, `Skipped`, `Not run`, or `N/A`,
  and every non- `Pass` row states an `Interpretation`.
- Every `### FND-` block carries an `Evidence level` field valued `Source`, `Model`, `App`,
  `Deployed`, or `Unknown`.
- A `Fail`, `Error`, or `Blocked` register row requires a Retest Register section
  covering the failed check.
- Improvement Plan `Disposition` cells take `Planned`, `Deferred`,
  `Accepted - no action`, or `Unresolved`.
- Every `### FND-` block maps to a phase or an explicit disposition,
  and a `Recommendation Classification` section is forbidden.
- A `Review Scope: Structure` row in Document Information selects the structure-review variant
  contract in `process/report-format/structure-review.md` instead: Document Information,
  Project Context, Structural Overview, Findings, Positive Practices, Recommendations,
  Prioritization, and Limitations and Assumptions.

## Generated Contract

The enumerations below render mechanically from `scripts/validate-report.py` via
`scripts/render-contract.py` - prose rules stay in the sections above, canonical lists stay here.

<!-- contract:begin -->

Generated by `scripts/render-contract.py` - edit `scripts/validate-report.py`,
then rerun the renderer. Do not edit inside the markers.

### Canonical Dimensions

Scorecard display names in canonical order and the `audit-model.json`
dimension key each maps to:

| #  | Scorecard name        | Model id              |
|----|-----------------------|-----------------------|
| 1  | Functional Suitability | functional_suitability |
| 2  | Testability           | testability           |
| 3  | Design Soundness      | design_soundness      |
| 4  | Code Quality          | code_quality          |
| 5  | Code Style            | code_style            |
| 6  | Stack Alignment       | stack_alignment       |
| 7  | Dependency Health     | dependency_health     |
| 8  | Maintainability       | maintainability       |
| 9  | Structure             | structure             |
| 10 | Deployability         | deployability         |
| 11 | Scalability           | scalability           |
| 12 | Security              | security              |
| 13 | Compliance            | compliance            |
| 14 | Observability         | observability         |
| 15 | Operational Safety    | operational_safety    |
| 16 | Documentation         | documentation         |
| 17 | API Compatibility     | api_compatibility     |
| 18 | Delivery & Continuity | delivery_continuity   |
| 19 | Originality & Licensing | originality_licensing |
| 20 | Skill Definition      | skill_definition      |

Multi-project models prefix each key - `<project>.security`.

### Document Information Fields

Required rows: `Detail Level`, `Evaluation Scale`, `Evidence Mode`, `Report Date`, `Report Revision`, `Report Style`, `Skill Version`, `Subject Revision`, `Time taken`, `Verification Scope`.

Optional rows: `Audit Purpose`, `Dirty-Tree State`, `Language`, `Previous Report`, `Projects`, `Review Scope`, `Sentence breaks`, `Target Environment`, `Translations`.

### Health Dashboard Markers

Every Health Dashboard section carries: `Risk Map`, `Scorecard Summary`, `Team & Continuity`.

### Run State

`work/audit-state.json` carries `state_version` 1 and
this vocabulary:

- Phases in order: `intake`, `parameter-configuration`, `scope-definition`, `evidence-gathering`, `category-assessment`, `synthesis`, `validation`.
- Gate tiers: `explicit`, `convention`, `discovered`, `default`, `automated`, `unknown`.
- Required gates: `audit-mode`, `project-inclusion`, `parameters-acceptance`, `report-delivery`.
- Artifact kinds: `params`, `model`, `state`, `part`, `report`, `translation`.

### Validation Protocol

Rows `PAR-1` through `PAR-33` in fixed order.

<!-- contract:end -->
