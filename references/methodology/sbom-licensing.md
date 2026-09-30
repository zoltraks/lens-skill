# SBOM And Licensing Baseline

## Purpose

> **Scope:** Checkable anchors for SBOM content, license identification, and license-file
> placement
> **Key items:** CISA minimum elements, SPDX identifiers, CycloneDX component model, REUSE
> per-file convention, OSI classification

This file distills the CISA, SPDX, CycloneDX, REUSE, and OSI sources listed in
`references/source-catalog.md` into constraints an audit can verify from repository source.

Snapshot date: 2026-09-30.

Feeds `references/sbom-schema.md`, `references/license-compliance.md`, and
`assessment/dependency-review.md`.

## CISA Minimum Elements

From https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom
(the older `minimum-requirements` URL is the alternate form of this row).

- The minimum data fields per component: supplier, component name, version, unique
  identifiers (purl/CPE), dependency relationships, SBOM author, timestamp.
- Automation support, distribution practices, and accommodation phases are process fields
  beyond the data model. The audit checks only the data fields against
  `references/sbom-schema.md`.
- A source-derived inventory (never an executed SBOM) records what the manifests prove and
  marks underivable fields `Unknown` per the schema file.

## SPDX

From https://spdx.org/licenses/ and https://spdx.github.io/spdx-spec/v2.3/.

- SPDX License IDs are the canonical identifiers (`MIT`, `Apache-2.0`, `GPL-3.0-only`,
  `BSD-3-Clause`, `EUPL-1.2`). `-only`/`-or-later` split replaced the deprecated `+`
  operator.
- `license` fields and `LicenseRef` comments should use SPDX IDs. Free-text license names
  are a normalization finding.
- `LICENSE`/`COPYING`/`NOTICE` files plus package `license` fields form the evidence set.
  `NOASSERTION` is the SPDX value for undetermined licenses, not `Unknown`.
- SPDX documents (`documentName`, `spdxVersion`, `packages[]` with `SPDXID`,
  `downloadLocation`, `licenseConcluded`/`licenseDeclared`, `copyrightText`) are the
  document shape when a repo ships one.

## CycloneDX

From https://cyclonedx.org/specification/overview/ and
https://ecma-tc54.github.io/ECMA-424/ (the ECMA-424 standard form).

- CycloneDX is a BOM standard covering components, services, dependencies, vulnerabilities,
  and licenses. `bomFormat`, `specVersion`, `serialNumber`, `components[]` are the top-level
  shape.
- Components carry `type`, `name`, `version`, `purl`, `licenses`, `hashes`, and
  `externalReferences`. `purl` (package URL) is the canonical identifier scheme.
- A shipped `sbom.json`/`cdx.json` artifact is `Reported` evidence - the audit reads it,
  never regenerates it.

## REUSE

From https://reuse.software/spec/ (the bare root URL is folded into this row).

- REUSE declares per-file licensing: every file carries an `SPDX-License-Identifier` comment
  and an `SPDX-FileCopyrightText`, or inherits via `REUSE.toml`/dep5 bulk coverage.
- `LICENSES/` directory holds full license texts for each declared ID.
- `reuse lint` compliance is a verifiable claim. A repo claiming REUSE conformance should
  pass it - absent per-file headers is the finding.

## OSI Cross-Check

From https://opensource.org/licenses.

- OSI-approved status is the classification cross-check: permissive (MIT, BSD, Apache-2.0),
  weak copyleft (LGPL, MPL-2.0, EPL), strong copyleft (GPL, AGPL), and non-OSI source
  licenses (SSPL, BUSL, CC-BY-NC) each carry different downstream obligations that
  `references/license-compliance.md` consumes.

## Live Check

When web fetch is available, spot-check the CISA element list and the SPDX `-only`/`-or-later`
convention.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
