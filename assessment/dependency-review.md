# Dependencies and Supply Chain

## Purpose

> **Scope:** Dependency health, known vulnerabilities, license compliance, lockfiles, provenance
> **Key items:** outdated dependencies, known CVEs, license obligations, pinning, SBOM, build provenance

This file guides assessment of third-party dependencies and the software supply chain, a primary concern for production code.

Apply `principles/evaluation-rules.md` throughout.

Assess manifests, lockfiles, and permitted tool results using the execution-safety rules below.

## What To Evaluate

- Dependency freshness: whether dependencies are current or significantly outdated.
- Known vulnerabilities: whether dependencies carry published vulnerabilities.
- License compliance: whether dependency licenses are compatible with the project's license and distribution.
- Pinning and lockfiles: whether versions are pinned and locked for reproducibility.
- Provenance: whether the origin and integrity of dependencies are verifiable.
- Bill of materials: whether an SBOM or equivalent inventory exists.

## Evidence To Look For

| Signal                 | Where It Appears                               |
|------------------------|------------------------------------------------|
| Dependency manifest    | Package or build manifest with version ranges  |
| Lockfile               | Lockfile pinning resolved versions             |
| Vulnerability scanning | Audit tooling, advisory config, scan reports   |
| License data           | Declared license, dependency license inventory |
| Vendoring or pinning   | Vendored deps, exact-version pins, hashes      |
| SBOM                   | SBOM file or generated inventory               |

## Verification And Advisory Triage

Use the safe-execution rules and evidence ledger in `process/audit-workflow.md`.

For Rust, inspect each workspace or independent manifest and its resolved lockfile.

Run `cargo audit` or `cargo deny check advisories` when available and permitted, recording the
RustSec database revision, tool version, features/targets, exit code, and sanitized output.

[Cargo audit and cargo deny](https://rustsec.org/) have different scopes, do not treat them as
interchangeable proof of application security.

For other stacks, select the existing ecosystem equivalent and state its supported scope.

For each advisory, record package and resolved version, dependency path, affected and fixed ranges,
advisory ID and aliases, advisory category, and runtime/build/dev relevance.

Distinguish vulnerable, unmaintained, yanked, outdated, and duplicate dependencies.

A pre-1.0 version or an old release is not proof of vulnerability or abandonment.

Assess reachability when evidence permits, otherwise mark it `UNKNOWN` without dismissing an
applicable advisory.

Record suppressions with their rationale, owner, and expiry, never silently add exceptions.

Do not call a replacement crate safe or maintained without checking its current provenance,
advisories, compatibility, and support signals.

## SBOM And License Evidence

For executable deliverables, check for a machine-readable component inventory tied to the audited
revision or release artifact, and generate one when safe and permitted.

Use CycloneDX or SPDX according to consumer requirements and tool support, recording the schema
version, generator/version, timestamp, target/features, and source or binary basis.

Both formats support supply-chain and licensing use cases, neither guarantees completeness.

Inspect direct and transitive components, dependency relationships, package identifiers and
versions,
license expressions, and unknown components.

State whether native libraries, vendored code, container OS packages, build dependencies, models,
and other shipped assets are included or excluded.

A source SBOM does not prove what a particular binary or container actually shipped.

For Rust, consider `cargo cyclonedx` for inventory and `cargo deny check licenses` for policy
checks.

[Cargo CycloneDX](https://github.com/CycloneDX/cyclonedx-rust-cargo) invokes Cargo and is not safe
by default on an untrusted project.

Use the existing license policy, and distinguish a scanner's default-policy rejection from an
established legal incompatibility.

[Cargo deny checks](https://embarkstudios.github.io/cargo-deny/checks/index.html) are configurable,
so record the policy and any exceptions along with the result.

Review SPDX `AND`/`OR` expressions, notices, linking, distribution, and service-use obligations
against the actual delivery model, escalating ambiguous cases for legal review.

A root MIT license does not settle transitive obligations, and a lockfile is not a license audit.

Consult [CycloneDX](https://cyclonedx.org/specification/overview/) and
[SPDX](https://spdx.dev/learn/overview/) for the selected schema and inventory limitations.

Do not claim SBOM procurement obligations without a specific applicable contract or regime.

## Container And Maintainer Risk

For an in-scope container, assess its build context, ignore rules, builder stage, published runtime
image, and exported caches separately.

Use an approved image scanner such as Trivy against an immutable image digest, recording scanners,
database age, target platform, exclusions, and results.

A final-image scan does not cover unpublished builder layers or external build caches.

Use synthetic canaries for leakage tests, never bake a real secret into a test image.

For critical dependencies, inspect release/support policy, ownership continuity, security response,
and feasible replacement or fork paths using dated primary evidence.

Do not infer maintainer competence, availability, or bus factor from stars or version numbers.

## Status Criteria

- `PASS`: Applicable support, integrity, advisory, and license requirements are evidenced for the
  resolved dependency scope, including version locking where required.
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
