# API Compatibility And Versioning Discipline

## Purpose

> **Scope:** Public API stability, versioning practice, and breaking-change tracking for reusable libraries and packages
> **Key items:** API compatibility gates, versioning scheme consistency, deprecation policy, tracked breaking changes

This file guides assessment of whether a reusable library or package protects its consumers from
unplanned breaking changes. It is a conditional pillar: include it whenever the audit subject is a
reusable library or package, and omit it for deployable services and applications. For services,
the adjacent concern is API Contract Conformance (`assessment/api-contract.md`), which covers
whether an exposed contract behaves as documented, not whether the public surface stays stable
across versions.

Apply `principles/evaluation-rules.md` throughout.

## What To Evaluate

- **Public surface definition**: whether the project defines and tracks what counts as public API
  (explicit baselines, exports lists, or visibility conventions).
- **Compatibility gate**: whether an API-compatibility tool or gate exists and is configured, for
  example ApiCompat or PublicApiAnalyzers for .NET, `cargo-semver-checks` for Rust, `gorelease`
  or `apidiff` for Go, japicmp or Revapi for Java, API Extractor for TypeScript, `griffe` for
  Python, or `abidiff` for C and C++. Tool configuration is evidence of intent, not proof of
  execution.
- **Versioning consistency**: whether the declared versioning scheme matches observed practice.
  Compare documented scheme, manifest versions, tags, changelog entries, and release notes.
- **Breaking-change management**: whether known future-breaking items, such as public mutable
  fields or planned removals, are tracked against a specific future major version rather than
  left open-ended.
- **Deprecation signals**: whether obsolete or deprecated members are marked, documented, and
  scheduled for removal on a stated timeline.
- **Version semantics**: whether pre-1.0 semantics, if applicable, are stated, since minor
  versions may break under SemVer before 1.0.

## Evidence To Look For

| Signal                      | Where It Appears                                                                                                                                   |
|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| API surface baseline        | `PublicAPI.Shipped.txt`/`PublicAPI.Unshipped.txt`, `*.api.md` reports, exports manifests                                                           |
| Compatibility gate config   | `EnablePackageValidation`, `PackageValidationBaselineVersion`, `api-extractor.json`, `cargo-semver-checks` config, japicmp or revapi build plugins |
| Versioning scheme           | `VERSIONING.md`, contributing docs, release policy, SemVer statement                                                                               |
| Declared vs tagged versions | Manifest version, `PackageVersion`, `Cargo.toml` version, `package.json` version vs `git tag` list                                                 |
| Deprecation markers         | `[Obsolete]`, `#[deprecated]`, `@Deprecated`, `@deprecated` doc tags                                                                               |
| Breaking-change tracking    | Changelog "breaking changes" entries, milestones, issues naming a future major version                                                             |
| Release practice            | Tag history, release notes, prerelease labels                                                                                                      |

## Per-Stack Tooling

Consult `references/stack-standards.md` for canonical links. The table below names the common
gate mechanisms so absence can be assessed, not so the tools are run.

| Stack             | Compatibility Gates                                                                        |
|-------------------|--------------------------------------------------------------------------------------------|
| .NET / NuGet      | `EnablePackageValidation` with baseline, ApiCompat, PublicApiAnalyzers (`RS0016`/`RS0017`) |
| Rust              | `cargo-semver-checks`, `cargo-public-api`                                                  |
| Go                | `gorelease`, `apidiff`                                                                     |
| Java / JVM        | japicmp, Revapi, `binary-compatibility-validator` for Kotlin                               |
| TypeScript        | API Extractor `*.api.md` reports                                                           |
| Python            | `griffe check`                                                                             |
| C / C++           | `abidiff` (libabigail), ABI Compliance Checker                                             |
| PHP               | Roave BackwardCompatibilityCheck                                                           |
| Other / unmanaged | No ecosystem gate, assess manually and record the gap                                      |

## Status Criteria

- `PASS`: The public surface is tracked, a compatibility gate or equivalent discipline is
  configured, versioning practice matches the declared scheme, and known breaking changes are
  bound to named future versions.
- `PARTIAL`: Some discipline exists, for example versioned releases and a changelog, but the
  surface is untracked, no gate is configured, or breaking-change items lack a target version.
- `FAIL`: Evidence shows breaking changes shipped in non-major versions, or the declared scheme
  is contradicted by practice.
- `UNKNOWN`: Version history, manifests, or tags were not inspectable.
- `N/A`: The subject is a deployable service or application. Omit the category and note the
  omission in Scope Exclusions.

## Common Risks

- An untracked public surface lets breaking changes ship silently in minor or patch releases.
- Public mutable fields and similar exposed members constrain every future refactor. Without a
  tracked breaking-change list, they stay open-ended.
- A declared scheme contradicted by tags or changelogs misleads consumers about upgrade safety.
- Pre-1.0 packages that do not state their instability invite consumers to assume SemVer
  guarantees that do not apply.
- A configured gate that is not evidenced as run provides reassurance without verification.

## What Raises Confidence

- A committed API baseline file or generated API report under version control.
- A compatibility gate configured in build or CI files, with its enablement evidenced.
- A documented versioning scheme whose tags, manifests, and changelogs agree with it.
- A deprecation policy naming how and when members are removed.
- A maintained list of known breaking changes bound to the next major version.

Mark each missing signal explicitly rather than inferring its presence. Anchor every judgement to
a specific file, tag, or documented policy.

## Cross-References

- `assessment/api-contract.md` for whether an exposed API behaves as documented.
- `assessment/change-management.md` for release process and versioning workflow evidence.
- `assessment/standards-conformance.md` for whether documented standards cover versioning.
- `references/stack-standards.md` for canonical versioning and compatibility references per stack.
