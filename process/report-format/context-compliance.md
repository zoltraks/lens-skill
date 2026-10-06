# Context And Compliance

## Purpose

> **Scope:** System context, component inventory, and license review sections
> **Key items:** technology stack, SBOM, license classification

## System Context

Describe the system as understood from the input.

Present the factual context without critique.

| Aspect                 | Detail                           |
|------------------------|----------------------------------|
| Functional description | <what the system does>           |
| Architecture overview  | <high-level structure>           |
| Key components         | <named components or modules>    |
| External dependencies  | <services, libraries, platforms> |
| Assumptions            | <only when explicitly stated>    |

Omit a row for any aspect the input does not establish.

When no aspect is established at all, state that in one prose sentence instead of rendering an
empty table.

When the report language is not English, apply the table header and aspect name translations from
the matching `translations/` file.

### Technology Stack

Present a factual inventory of the technologies the subject uses.

Describe the stack only, do not judge it here.

Use a key-value table:

| Layer            | Technology                         |
|------------------|------------------------------------|
| Languages        | <languages and versions>           |
| Frameworks       | <application and UI frameworks>    |
| Runtime/Platform | <runtime, OS, or host platform>    |
| Build tooling    | <build system, bundler, compilers> |
| Test tooling     | <test frameworks and runners>      |
| Package manager  | <dependency and package manager>   |
| Key libraries    | <notable third-party libraries>    |
| Data stores      | <databases, caches, file formats>  |
| Target platforms | <where the software runs or ships> |

Anchor each entry to evidence, such as a manifest, lockfile, or config file.

Omit a layer row the input does not reveal.

Add or omit rows to fit the subject, but keep the layer names in this column and translate them into
the report language.

After the tables, add further subsections for major components (e.g., `### Backend`, `### Frontend`,
`### Deployment`).

Put exactly one empty line after each subsection header before the first sentence.

Separate every sentence with an empty line.

For operated systems, add a compact **Operational Objectives** table with metric, target, measured
result, window, source, and owner, using the NFR and operational-readiness guides.

Keep SLIs/SLOs, error budgets, RPO/RTO, and DORA delivery measures distinct.

Use `UNKNOWN` for missing measurements and `NOT SPECIFIED` for unapproved targets.

For technical due diligence, add a **Due Diligence Coverage** table with concern, status, evidence,
and missing artifact or next step.

Cover continuity, ownership cost, roadmap feasibility, supplier continuity, IP rights, and data
obligations using `assessment/operational-readiness.md` and its related category guides.

Add a data-lifecycle summary under Compliance findings when relevant, referencing categories,
stores, recipients, retention/deletion, and the applicable obligation basis.

## Software Bill of Materials

Present the source-derived component inventory as a structured table.

Open the section with one line stating what this is:
a manifest-derived component list at the audited revision,
not a shipped-artifact SBOM and not a claim of SPDX or CycloneDX conformance.

Build the table per `references/sbom-schema.md` from the manifests and lockfiles read per
`references/dependency-manifests.md`:

| Component | Version | Ecosystem | Relationship | License | License Risk | Advisory Checked | Source File |
|-----------|---------|-----------|--------------|---------|--------------|------------------|-------------|
| <name>    | <ver>   | <purl>    | direct       | <lic>   | <flag>       | N                | <path>      |

License values come from inspected declarations only, `Unknown` otherwise.

License Risk values are `None flagged`, `Review`, `Conflict`,
or `Unknown` per `references/license-compliance.md`.

`Advisory Checked` is `Y` only where committed advisory or scan evidence covers the component.

Close the section with the direct and transitive totals and any manifest-lockfile drift noted.
When no dependency manifest or lockfile exists in the project, state `No dependency manifests or
lockfiles found` in place of the table rather than omitting the section.

The Audit Type Coverage table claims `Covered` for SBOM or component-inventory rows only
when this section exists with its completeness statement - a module line-count inventory
is not an SBOM, and the validator rejects the mismatch. Advisory coverage likewise states
which advisories were checked (advisory ID, exact version, dependency path, reachability
or `UNKNOWN`) - a scanner's finding count is not a confirmed application-defect count.

When the report language is not English, apply the column header translations from the matching
`translations/` file.

## License Compliance Review

Summarize the license-classification pass run over the SBOM table per
`references/license-compliance.md`.

This section is a synthesis layer: the per-component detail lives in the SBOM table and the finding
detail lives in `FND-CPR` findings, this section states what the pass concluded.

Present the classification counts:

| License class   | Components | Notes                                  |
|-----------------|------------|----------------------------------------|
| Permissive      | <count>    | <notable components>                   |
| Weak-copyleft   | <count>    | <notable components>                   |
| Strong-copyleft | <count>    | <notable components, linkage evidence> |
| Proprietary     | <count>    | <notable components>                   |
| Unknown         | <count>    | share of total, hygiene implication    |

Omit a `License class` row whose `Components` count is zero.

When no components were classified at all, state that in prose instead of rendering the table.

Below the table, state in short paragraphs:

- Any `Conflict` copyleft-trap result, naming the component, its license, the project's license or
  distribution model, and the linkage evidence, cross-referenced to its `FND-CPR` finding.
- Whether the project's own license file, headers, and third-party notices are consistent with the
  component set, referencing the Copyrights & Originality assessment.
- The share of components whose license could not be determined from inspected sources, and what
  artifact (a maintained SBOM, a `THIRD-PARTY-NOTICES` file, per-package license declarations)
  would resolve it.

When the report language is not English, apply the column header translations from the matching
`translations/` file.
