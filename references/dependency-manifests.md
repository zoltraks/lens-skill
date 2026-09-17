# Dependency Manifest Inventories

## Purpose

> **Scope:** Source-derivable component inventories from dependency manifests and lockfiles
> **Key items:** per-ecosystem extraction procedures, component list format, evidence labeling

This file defines a family of text-only manifest readers. Each procedure reads a manifest or
lockfile as text and produces a lightweight component list in the style of a CycloneDX or SPDX
inventory. No tool is installed, no package manager is invoked, and nothing is generated.

Apply `principles/evaluation-rules.md` throughout. The derived inventory is `Inspected` evidence
about the source, not a report from a generation tool.

## Output Contract

Every reader produces the same component list shape.

| Field        | Content                                                                                                                                                                       |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Component    | Package name as declared                                                                                                                                                      |
| Version      | Resolved or declared version. `UNKNOWN` when not derivable                                                                                                                    |
| Ecosystem    | `purl` type: `pkg:cargo/…`, `pkg:nuget/…`, `pkg:npm/…`, `pkg:pypi/…`, `pkg:golang/…`, `pkg:maven/…`, `pkg:gem/…`, `pkg:composer/…`, `pkg:pub/…`, `pkg:hex/…`, `pkg:generic/…` |
| Relationship | `direct` or `transitive`, where derivable, else `UNKNOWN`                                                                                                                     |
| Scope        | `runtime`, `dev`, `build`, `test`, `optional`, or `UNKNOWN`                                                                                                                   |
| Integrity    | Lockfile checksum or hash when present                                                                                                                                        |
| Source File  | The manifest or lockfile the entry was read from                                                                                                                              |

License fields are rarely present in manifests. Record them only when the file actually declares
them, otherwise mark `UNKNOWN` rather than copying registry assumptions.

## Reading Rules

- The inventory reflects the manifests at the audited revision. It is a source-derived component
  list, not a shipped-artifact SBOM. State that distinction wherever the inventory is used.
- A lockfile entry proves resolution intent, not what a released binary or container contains.
- Count direct and transitive components separately and report both totals.
- Record manifest-lockfile drift: a declared dependency missing from the lockfile, or a locked
  component with no declared path, is a finding input.
- Deduplicate by (ecosystem, name, version). Note repeated versions of the same component.
- Cap the displayed inventory when it is long. Show direct components in full, summarize
  transitive components by count and notable entries, and record full totals in the evidence
  ledger.
- Record each manifest and lockfile read in the evidence ledger with `Inspected` labels.

## Rust

| File         | What To Extract                                                                                                                                                                                                                                              |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Cargo.toml` | `[dependencies]`, `[dev-dependencies]`, `[build-dependencies]` give direct components and declared ranges. `[workspace.dependencies]` gives inherited declarations. Feature-gated and target-gated sections qualify scope.                                   |
| `Cargo.lock` | Each `[[package]]` block gives `name`, `version`, `source`, `checksum`. Entries also declared in a workspace manifest are `direct`, the rest are `transitive`. Workspace members have no `source`. Per-package `dependencies` lists give relationship paths. |

## .NET / NuGet

| File                  | What To Extract                                                                                                                                                          |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `*.csproj`            | `<PackageReference Include Version>` entries are `direct`. `PrivateAssets` and `IncludeAssets` qualify scope. `<ProjectReference>` entries are internal, not components. |
| `packages.config`     | Each `<package id version>` entry is a direct component (legacy projects).                                                                                               |
| `packages.lock.json`  | Per-target objects list `resolved` versions with `type` of `Direct` or `Transitive` and `contentHash`. Multi-target projects produce one list per target.                |
| `project.assets.json` | `libraries` lists all resolved components with `type`; `targets` records the resolved graph per target framework.                                                        |
| `*.nuspec`            | `<dependencies><dependency id version>` declares the package's own runtime dependencies.                                                                                 |

## Node / npm

| File                | What To Extract                                                                                                                                                                                                                                        |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `package.json`      | `dependencies`, `devDependencies`, `peerDependencies`, `optionalDependencies` give direct components with declared ranges.                                                                                                                             |
| `package-lock.json` | The `packages` map keys `node_modules/<name>` entries give resolved `version`, `dev` scope flag, `resolved` URL, and `integrity` hash. Nested `node_modules` paths indicate transitive placement. The root `""` entry repeats the declared direct set. |
| `yarn.lock`         | Each `name@range:` stanza gives resolved `version`, `resolved`, `integrity`.                                                                                                                                                                           |
| `pnpm-lock.yaml`    | `importers` lists direct dependencies per workspace package; `packages` or `snapshots` lists the resolved set.                                                                                                                                         |

## Python

| File               | What To Extract                                                                                                                                         |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `requirements.txt` | `name==version` lines give pinned components. `-r` and `--requirement` lines recurse into further files. Unpinned lines give `UNKNOWN` versions.        |
| `pyproject.toml`   | `[project] dependencies` and `optional-dependencies` give direct components. `[tool.poetry.dependencies]` and `[tool.uv]` serve their respective tools. |
| `Pipfile.lock`     | `default` (runtime) and `develop` (dev) objects give resolved versions and hashes.                                                                      |
| `poetry.lock`      | Each `[[package]]` gives `name`, `version`, and dependency relationships.                                                                               |
| `uv.lock`          | Each `[[package]]` gives `name`, `version`, `source`, and hashes.                                                                                       |

Relationship is usually `UNKNOWN` for Python unless a lockfile marks it. State that explicitly.

## Go

| File     | What To Extract                                                                                                                                                                |
|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `go.mod` | `require` blocks give direct components; entries commented `// indirect` are transitive. `toolchain` and `go` lines are toolchain pins, not dependencies.                      |
| `go.sum` | Module-plus-hash lines give integrity data, including hashes for transitive and test dependencies. Each module typically has two lines: the module hash and the `go.mod` hash. |

## Java / JVM

| File                        | What To Extract                                                                                                                                                                                                                                                 |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `pom.xml`                   | `<dependencies>` entries give direct components. `<scope>` maps to runtime (`compile`, `runtime`), `test`, `provided`, or `system`. `<dependencyManagement>` pins versions without implying use. Properties in `<version>` need resolution from `<properties>`. |
| `build.gradle` / `.kts`     | `dependencies {}` entries are direct. Configuration names map to scope: `implementation`/`api` are runtime, `testImplementation` is dev, `compileOnly` is build.                                                                                                |
| `gradle.lockfile`           | Resolved versions per configuration with `=configuration` suffixes.                                                                                                                                                                                             |
| `verification-metadata.xml` | Checksums and signatures for resolved artifacts.                                                                                                                                                                                                                |

Transitive resolution is not derivable from `pom.xml` or `build.gradle` alone. Mark relationship
`UNKNOWN` without a lockfile.

## PHP / Ruby / Dart / Elixir / Zig

| Ecosystem | Files                            | What To Extract                                                                                                                             |
|-----------|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| PHP       | `composer.json`, `composer.lock` | `require` and `require-dev` are direct. `composer.lock` `packages` and `packages-dev` give resolved versions and `dist` references.         |
| Ruby      | `Gemfile`, `Gemfile.lock`        | `Gemfile` entries are direct. `Gemfile.lock` `DEPENDENCIES` lists the declared set, `GEM` `specs` lists the resolved graph.                 |
| Dart      | `pubspec.yaml`, `pubspec.lock`   | `dependencies` and `dev_dependencies` are direct. `pubspec.lock` entries carry `dependency: "direct main"` or `"transitive"` and `version`. |
| Elixir    | `mix.exs`, `mix.lock`            | `deps` are direct. `mix.lock` hex entries give resolved versions and hashes.                                                                |
| Zig       | `build.zig.zon`                  | `.dependencies` entries give name, URL, and hash. All are direct and pinned.                                                                |

## C / C++ And Vendored Code

| File                      | What To Extract                                                                                                |
|---------------------------|----------------------------------------------------------------------------------------------------------------|
| `conanfile.txt` / `.py`   | `[requires]` entries give components with versions.                                                            |
| `vcpkg.json`              | `dependencies` entries give components with version constraints.                                               |
| `vendor/`, `third_party/` | Vendored directories count as components. Version is `UNKNOWN` unless a nested manifest or header declares it. |

## Delphi And Unmanaged Stacks

Delphi and similar ecosystems have no standard manifest. Record components from vendored source
directories, GetIt package metadata when committed, and documented dependency lists. Mark version
and relationship `UNKNOWN` when not derivable.

## Using The Inventory

- The inventory feeds Dependencies and Supply Chain (`assessment/dependency-review.md`), license
  review, and supply-chain findings.
- It partially closes an "no SBOM" finding: the audit demonstrates what a manifest-derived
  component list looks like, while still noting that no shipped-artifact SBOM exists.
- It never substitutes for advisory checking. Resolved versions with no vulnerability evidence
  remain `UNKNOWN` for advisory status, per `assessment/dependency-review.md`.
