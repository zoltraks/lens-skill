# License Evidence Locations

## Purpose

> **Scope:** Where license declarations live per ecosystem and what counts as evidence
> **Key items:** LICENSE/COPYING files, manifest `license` fields, header conventions,
> SPDX identifiers, NOTICE obligations

This file consolidates per-ecosystem license evidence locations proven across audit
sessions. `references/methodology/sbom-licensing.md` covers SBOM generation and obligation
classes. This file is the lookup table for where declarations physically sit.

Snapshot date: 2026-09-30.

Feeds `assessment/documentation-review.md` and `assessment/standards-conformance.md`.

## Repository-Level Files

- `LICENSE`, `LICENSE.md`, `LICENSE.txt`, `COPYING`, `COPYING.*` at repository root are the
  primary declaration. Multiple files (`LICENSE-APACHE` + `LICENSE-MIT`) signal dual
  licensing.
- `NOTICE` files carry attribution text that Apache-2.0 and similar licenses require
  redistributors to preserve. Their presence/absence is a compliance signal.
- `LICENSES/` directories (REUSE convention) hold one file per SPDX identifier used.
- `COPYING.LESSER` alongside `COPYING` is the LGPL pairing.
- A README license badge (`shields.io` license badge) is `Reported` evidence - the file
  itself is the declaration.

## Manifest Fields Per Ecosystem

| Ecosystem | File                   | Field                                                                 |
|-----------|------------------------|-----------------------------------------------------------------------|
| Node.js   | `package.json`         | `license` (SPDX string) or `licenses` array (deprecated)              |
| Python    | `pyproject.toml`       | `license = {text = "..."}` or `license = "Apache-2.0"` (PEP 639 SPDX) |
| Python    | `setup.py`/`setup.cfg` | `license=` arg, `License ::` classifiers                              |
| Rust      | `Cargo.toml`           | `license = "MIT OR Apache-2.0"` (SPDX expression)                     |
| Go        | none standard          | `LICENSE` file only.`go.mod` has no license field                     |
| PHP       | `composer.json`        | `license` (string or array, SPDX)                                     |
| Java      | `pom.xml`              | `<licenses><license><name>` + `<url>`                                 |
| Java      | `build.gradle`         | `licenses { license { name } }` in publishing block                   |
| .NET      | `.csproj`              | `<PackageLicenseExpression>` (SPDX) or `<PackageLicenseFile>`         |
| Ruby      | `*.gemspec`            | `spec.license` / `spec.licenses`                                      |
| Swift     | none standard          | `LICENSE` file. SPM has no license field                              |
| Docker    | image labels           | `org.opencontainers.image.licenses` label                             |

## Evidence Quality Classes

- `Verified`: a license file exists AND a manifest field or header agrees with it.
- `Reported`: a badge, README claim, or manifest field without a license file - or the
  reverse, a file with no manifest claim.
- `NOT SPECIFIED`: no file, no field, no headers.
- Conflict between file text and manifest field is a finding (e.g. `LICENSE` says MIT,
  `package.json` says `ISC`).

## Header Conventions

- Per-file SPDX headers (`// SPDX-License-Identifier: MIT`) are the REUSE-style convention.
  consistent headers plus a `LICENSES/` dir is the strongest posture.
- License headers that contradict the root file are per-file dual-licensing evidence, not
  necessarily defects - record which is which.

## Live Check

Session-derived. No single external source owns this table. License obligation classes are
in `references/methodology/sbom-licensing.md`.
