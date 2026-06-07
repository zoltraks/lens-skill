# Dependencies and Supply Chain

## Purpose

> **Scope:** Dependency health, known vulnerabilities, license compliance, lockfiles, provenance
> **Key items:** outdated dependencies, known CVEs, license obligations, pinning, SBOM, build provenance

This file guides assessment of third-party dependencies and the software supply chain, a primary concern for production code.

Apply `principles/evaluation-rules.md` throughout. Report the supply-chain posture from available manifests and lockfiles; do not run untrusted tooling as part of the audit.

## What To Evaluate

- Dependency freshness: whether dependencies are current or significantly outdated.
- Known vulnerabilities: whether dependencies carry published vulnerabilities.
- License compliance: whether dependency licenses are compatible with the project's license and distribution.
- Pinning and lockfiles: whether versions are pinned and locked for reproducibility.
- Provenance: whether the origin and integrity of dependencies are verifiable.
- Bill of materials: whether an SBOM or equivalent inventory exists.

## Evidence To Look For

| Signal                       | Where It Appears                                   |
|------------------------------|----------------------------------------------------|
| Dependency manifest          | Package or build manifest with version ranges      |
| Lockfile                     | Lockfile pinning resolved versions                 |
| Vulnerability scanning       | Audit tooling, advisory config, scan reports       |
| License data                 | Declared license, dependency license inventory     |
| Vendoring or pinning         | Vendored deps, exact-version pins, hashes          |
| SBOM                         | SBOM file or generated inventory                   |

## Status Criteria

- `PASS`: Dependencies are current, locked, scanned for vulnerabilities, and license-compatible, with evidence.
- `PARTIAL`: Dependencies are managed but outdated, unscanned, or license posture is unclear.
- `FAIL`: Dependencies carry known unaddressed vulnerabilities or incompatible licenses, with evidence.
- `UNKNOWN`: Manifests, lockfiles, or license data were not provided.

## Common Risks

- Outdated dependencies accumulate known vulnerabilities and migration debt.
- Unscanned dependencies hide published vulnerabilities in the supply chain.
- Incompatible or unreviewed licenses create legal and distribution risk.
- Unlocked version ranges make builds non-reproducible and allow silent drift.
- Absence of an inventory makes incident response to a dependency advisory slow.

## What Raises Confidence

- A lockfile pinning resolved versions for reproducible builds.
- Automated vulnerability scanning tied to the dependency manifest.
- A reviewed, recorded license posture compatible with the project license.
- An SBOM or generated dependency inventory.

Mark each missing signal explicitly rather than inferring its presence. Do not claim a dependency is safe merely because it is current.
