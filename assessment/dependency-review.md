# Dependencies and Supply Chain

## Purpose

> **Scope:** Dependency health, known vulnerabilities, license compliance, lockfiles, provenance
> **Key items:** outdated dependencies, known CVEs, license obligations, pinning, SBOM, build provenance

This file guides assessment of third-party dependencies and the software supply chain, a primary concern for production code.

Apply `principles/evaluation-rules.md` throughout.

Assess manifests, lockfiles, committed scan reports, and generated inventories by inspection.
The audit never runs audit or generation tools.

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

Use the evidence ledger and the no-execution rule in `process/audit-workflow.md`.

For Rust, inspect each workspace or independent manifest and its resolved lockfile.

Do not run `cargo audit`, `cargo deny check advisories`, or an ecosystem equivalent. Look for
committed scan reports, CI pipeline steps that run them, or documented advisory reviews. When a
report exists, record the advisory database revision, tool version, and scope from the artifact
as `Reported` evidence.

[Cargo audit and cargo deny](https://rustsec.org/) have different scopes, do not treat them as
interchangeable proof of application security.

For other stacks, note the existing ecosystem equivalent and state its supported scope.

When no scan report exists and advisory status cannot be checked from repository contents, mark
vulnerability status `UNKNOWN` and recommend the scan as a roadmap item rather than treating
freshness as clearance.

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
revision or release artifact. The audit does not generate one.

When no SBOM exists, derive a source-level component list from the manifests and lockfiles using
the readers in `references/dependency-manifests.md`. The derived list is `Inspected` evidence of
the declared and resolved dependency set at the audited revision. It partially closes the
inventory gap without claiming to be a shipped-artifact SBOM.

When an SBOM exists, record the CycloneDX or SPDX schema version, generator, timestamp, and
source or binary basis.

Both formats support supply-chain and licensing use cases, neither guarantees completeness.

Inspect direct and transitive components, dependency relationships, package identifiers and
versions,
license expressions, and unknown components.

State whether native libraries, vendored code, container OS packages, build dependencies, models,
and other shipped assets are included or excluded.

A source SBOM does not prove what a particular binary or container actually shipped.

For Rust, `cargo cyclonedx` for inventory and `cargo deny check licenses` for policy checks are
typical documented tooling, assess their configuration and committed output rather than running
them.

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

Do not run image scanners such as Trivy. Assess the container from its build context and inspect
committed scan reports when present, recording the scanner, database age, target platform,
exclusions, and results as `Reported` evidence.

A final-image scan does not cover unpublished builder layers or external build caches.

Check Dockerfiles and image build contexts for copied secrets, never suggest baking a real
secret into a test image.

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
