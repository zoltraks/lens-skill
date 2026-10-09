# Closing Sections

## Purpose

> **Scope:** Scope exclusions, limitations, re-audit plan, validation record, and references
> **Key items:** exclusions, unknowns, closure evidence, validation record, consulted sources

## Scope Exclusions

Explicitly define the limits of the analysis.

List components or environments that were not inspected unless they were explicitly provided in the
input scope.

Format each exclusion as a bullet with a bold label, followed by an empty line,
then the explanation.

Example:

```markdown
- **SQL database schema and stored procedures**.

The database layer was assessed only from the API side. The actual tables, views, triggers, and
stored procedures were not provided.
```

Typical exclusions include:

- Operational runtime infrastructure (live servers, VMs, containers)
- Live network topologies and firewall rules
- Third-party authentication provider implementations
- Physical deployment environments
- End-user devices or browser clients
- Data backups or disaster-recovery procedures
- Penetration-test results or security audits performed by external firms

Mark each item as `NOT INSPECTED` or `EXCLUDED BY SCOPE`.

If the user provided some of these, list them as `INCLUDED`.

State any extrapolations made from sampled code to the whole system.

**Standard engagement-type exclusions**

Every report carries these statements in the same register, matching the `NOT DONE` rows of
the Audit Type Coverage table:

- **Dynamic/runtime penetration testing** - `NOT PERFORMED` by default. Security findings on
  network-facing surfaces carry a `Theoretical`-tier `Exploitability` narrative only. A scoped, live
  penetration test is a distinct, separately-commissioned engagement.
- **Organizational and team interviews, business-fit assessment** - `NOT PERFORMED` by default.
  The report covers the engineering dimensions of a technical due diligence (architecture, code,
  security, licensing, delivery-practice proxies) but not the interview-based team, leadership,
  and problem-fit pillars a formal TDD engagement adds.
- **Compliance certification and attestation** - the report is not an ISO/IEC 27001
  certification and not a SOC 2 attestation examination, nor a PCI-DSS conformance
  assessment. Referenced standards such as ISO/IEC 25010, OWASP ASVS, and NIST SP 800-30 are used
  as scoring rubrics and coverage checklists only.

When the engagement scope explicitly lifts one of these defaults, state that here and update the
matrix status to match.

**Standard coverage statement**

When the audit referenced security standards, state which categories were in scope and which were
not, so the reader does not assume full coverage.

For a web application, name the OWASP Top 10 (2025) categories (`A01`-`A10`) that were and were not
assessed.
For an API, name the OWASP API Security Top 10 (2023) categories (`API1`-`API10`).
For a full audit, use the nine ISO/IEC 25010:2023 characteristics in the scorecard crosswalk to
identify coverage and justify exclusions.

Do not present Lens dimension names such as Operational Safety as ISO characteristic names.
Mark categories that could not be assessed from the provided input as `NOT ASSESSED` with a one-line
reason.

**Omitted conditional sections**

When a conditional section was omitted because it does not apply (for example,
the API Contract Conformance section for a system with no API,
or the Threat Model for a single-user local utility),
state the omission here with a one-line justification so the reader knows it was deliberate.

The Changes Since Previous Audit section is the exception,
a first audit has no previous report to compare and a fresh audit ignores it,
so its absence needs no note in either case.

## Limitations and Unknowns

List every check that would require execution and was therefore not performed, plus every
unresolved unknown the report carries.

This section exists because the audit is source-only.

An unrun check is a limitation of the report, never a defect of the subject.

Use a table:

| Item               | Type        | Reason                                 | Resolution                                |
|--------------------|-------------|----------------------------------------|-------------------------------------------|
| <check or unknown> | Unrun check | Requires execution, out of audit scope | <command or artifact that would run it>   |
| <check or unknown> | Unknown     | <why the evidence was unavailable>     | <input or artifact that would resolve it> |

Rows come from two sources:

- Every `NOT RUN` row of the verification plan and evidence ledger in
  `process/audit-workflow.md`, with the verification method that would have run it.
- Every unresolved `UNKNOWN`, `NOT SPECIFIED`, or `INSUFFICIENT INFORMATION` token from the
  findings and registers, with the input that would resolve it.

Typical unresolved inputs include telemetry-dependent delivery metrics that stayed
`NOT SPECIFIED`, missing cost, support, ownership, or supplier-obligation evidence,
underivable SBOM fields such as `Unknown` licenses, and `Theoretical` attack paths that no
live validation has confirmed.

For multi-project reports, qualify each row with the project identifier.

## Operator Verification Handoff

This section turns the source-only boundary into an actionable follow-up.

It is always present under `source-only` evidence mode.

Under `executed-readonly` or `executed-commands` it lists only the checks outside the
commissioned set - for a `review`-style report those deferred rows live in the Execution
Register instead, so this section appears only when deferred checks need their own
follow-up register.

Each row names one material claim the audit could not resolve from source, the exact check
that resolves it, and the finding, risk, or rating the check would confirm or close:

| Claim              | Command / Procedure          | Pass Criteria               | Resolves         |
|--------------------|------------------------------|-----------------------------|------------------|
| <unresolved claim> | <exact command or procedure> | <observable pass condition> | FND-XXX / rating |

Commands come from the project's documented tooling where it exists.

A claim with no proposed check is a defect of the audit, not of the subject.

## Executed Evidence Log

Present under `executed-readonly` or `executed-commands` evidence mode in `audit` and `hunt`
reports - a `review` report records the same provenance in its Execution Register instead.

One row per commissioned execution:

| Check | Tool & Version | Command | Timestamp | Result | Resolves |
|-------|----------------|---------|-----------|--------|----------|

Each row records the exact command, the tool and advisory-database or ruleset revision, the
exit status or outcome, and a retained-output reference (sanitized artifact path or digest)
when output exists.

Result cells take the check-status vocabulary - `PASS`, `FAIL`, `ERROR`, `BLOCKED`,
`SKIPPED`, `NOT RUN`, `N/A` - where `ERROR` and `BLOCKED` describe the runner, never the
product.

Rows are `Executed` evidence. Under `executed-readonly` they describe analyzer output and
never imply a build, test, or run of the subject occurred. Under `executed-commands` they may
describe commissioned non-mutating commands - tests, builds, isolated reproductions - and
still never imply the subject was deployed, mutated, or connected to live systems.

## Re-audit And Follow-up Plan

Include this section only when the Actionable Remediation Roadmap contains at least one P1 or P2
recommendation, per `synthesis/reaudit-plan.md`.

It precedes the Validation Record and References sections.

This section makes the report actionable in a governance sense.

It borrows the follow-up-audit practice of ISO 19011:2026 (guidelines for auditing
management systems, applied here as supporting principles only)
and the monitor step of the NIST Risk Management Framework.

Present a table mapping findings to verification ownership and closure evidence.

Include one row per P1 and P2 finding at minimum.

| Finding | Priority | Verification Owner        | Closure Evidence      | Target Re-audit Trigger        |
|---------|----------|---------------------------|-----------------------|--------------------------------|
| FND-XXX | P1       | <role or `NOT SPECIFIED`> | <verifiable artifact> | <milestone or `NOT SPECIFIED`> |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

After the table, state sign-off gates tied to project-qualified `RSK-XXX` IDs and an evidenced
re-audit schedule.

Include the two standard triggers from `synthesis/reaudit-plan.md` when they apply: an SBOM-drift
re-audit on manifest or lockfile change, and a pentest-escalation trigger naming a scoped live
penetration test when a `HIGH` or `CRITICAL` network-facing finding remains `Theoretical` after
remediation planning.

Apply `synthesis/reaudit-plan.md` for confirmed ownership, revision-specific closure evidence,
residual risk, and the separation of final-report state from production sign-off.

Unknown owners or missing required verification leave sign-off pending, proposed roles are not
assignments.

## Validation Record

Close the analysis with a self-check table verifying the report's internal consistency.

This section renders the report's capability set so a future report can diff it mechanically,
per `process/report-parity.md`.

Use a table:

| Check | Result  | Evidence / Justification          |
|-------|---------|-----------------------------------|
| PAR-1 | APPLIED | <evidence or `N/A` justification> |

Rows appear in this order:

1. One row per Mandatory Core Checklist item, `PAR-1` through `PAR-19`, in fixed order.
2. Internal consistency checks: `FND-XXX`/`RSK-XXX`/`REC-XXX` cross-referencing, count
   reconciliation across summary tables and registers, conditional-section evaluation, and
   formatting rules.
3. A `Parity baseline` row naming the report diffed against, or `none found`.

Result values are `APPLIED`, `PASS`, or `N/A`.

An `N/A` always carries a justification in the Evidence / Justification column.

The `State` row in Document Information is removed only after this record is complete and the
consistency gate in `process/report-parity.md` passes - removal is the last structural edit,
before the final timestamp is written, so a report that still shows `Draft` has not passed its
own gate.

For multi-project reports, qualify per-project checks with the project identifier.

## References

This section lists every external source referenced during the audit.

It is always the final section of the report.

Collect references from all sections of the report.

Sources include the standards named in Auditing Methodology,
the external best practices cited in Standards Conformance,
and any documentation consulted during any assessment category.

Present the references as a table:

| Reference | Publisher or Author   | Used In         |
|-----------|-----------------------|-----------------|
| <title>   | <publisher or author> | <section names> |

When the report language is not English, apply the column header translations from the matching
`translations/` file.

Only list sources actually consulted during the audit.

Do not invent references.

For each source, record edition/version, publisher, access date, applied controls or claims, and any
access limitation in the supporting paragraph.

Prefer primary standards and tool documentation over marketing summaries.

Verify publication status at audit time, distinguishing released editions, drafts, and legacy
baselines, and avoid claiming full conformance from sampled coverage.

Offline audits should identify dated cached sources and leave current advisory status unknown when
it cannot be checked.

After the table, add one paragraph per reference that has a URL.

Format each link as a Markdown link: `[<title>](<url>)`.

Do not put URLs in the table itself, because long URLs make the table unreadable in plain text.

Group rows by section when the same source is used in multiple sections,
or list one row per source with all sections in the Used In column separated by commas.

Keep the order stable: methodology standards first, then standards-conformance best practices,
then any other sources in the order they first appear in the report.
