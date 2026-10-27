# .NET Application And Library Baseline

## Purpose

> **Scope:** Checkable constraints for non-web .NET codebases - console tools, class
> libraries, desktop utilities, and multi-project solutions
> **Key items:** solution/project hierarchy, namespace-directory mirroring, file naming,
> test-project conventions, role-directory patterns

This file distills the Microsoft program-organization and C# coding-convention sources listed
in `references/source-catalog.md`, plus the maintainer's C# engineering standards
(`csharp-general`, `csharp-cli`, `csharp-mcp`, `csharp-automation`, `csharp-refactoring`,
`automation-general`, `automation-web`, `automation-windows`) into constraints an audit can
verify from repository source.

Snapshot date: 2026-10-27.

Feeds `assessment/structure-review.md`, `assessment/code-style.md`,
`assessment/best-practices.md`, `assessment/testing-review.md`, and
`assessment/baseline-conformance.md` for .NET subjects.

`references/stacks/dotnet-aspnet.md` covers the web-service surface and its security baseline -
this file carries the shared .NET naming floor plus the non-web project shapes.

## Naming And Layout

From the Microsoft program-organization guide at
https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/program-structure/program-organization,
https://learn.microsoft.com/en-us/dotnet/core/tutorials/testing-with-cli, and the maintainer's
C# engineering standards.

- The organizational hierarchy is solution, project, assembly, namespace, type: a `.sln`/`.slnx`
  groups related `.csproj` files, each project produces one assembly, and the root namespace
  matches the assembly name.
- A typical solution keeps projects under `src/<Name>/<Name>.csproj` with test projects under
  `test/<Name>.Test` or `test/<Name>.Tests`, sharing settings through root
  `Directory.Build.props` and `Directory.Packages.props` and style through `.editorconfig`.
- Small projects may stay flat (Microsoft's own guidance allows a flat layout while a project
  is small) - a single-project console tool without `src/` is not a defect.
- Namespaces mirror the directory structure under the project root. A type at
  `src/MyApp/Service/EntityService.cs` in namespace `MyApp.Service` is canonical, and drift
  between path and namespace is a structural finding.
- One public top-level type per `PascalCase.cs` file named for the type. Files approaching
  roughly 300-500 lines split along responsibility seams into `Type.<Area>.cs` partials.
- Test projects mirror the production directory structure, name test classes
  `<TypeUnderTest>Tests` in `*Tests.cs` files, and keep shared helpers in `TestHelpers/` or a
  dedicated `*.TestShared` project rather than copies in each project.
- MSBuild items such as `InternalsVisibleTo` belong in an `ItemGroup` - an item element inside
  `PropertyGroup` fails the build with MSB4066.
- Automation-utility layouts name domain folders for the surface the tool drives (the external
  system or window), not after the tool itself - `Providers/` is reserved for the provider seam
  and `Platform/` for OS backends.
- Role-directory patterns by project kind: CLI tools separate `Commands/`, `Models/`,
  `Formatting/`, `Infrastructure/` under a thin `Program.cs` (`*Command` suffixes,
  `--kebab-case` options), MCP servers separate `Tools/`, `Resources/`, `Prompts/`,
  `Infrastructure/` (`*Tools` classes, `snake_case` tool names, `*Arguments` records), and
  automation projects separate `Probes/`, `Executors`/`Scenarios/`, `Interop/`, `Common/`
  (`*Probe`, `*Action`, `*Window`, `*Element` suffixes).

## Identifier Naming

- `PascalCase` for namespaces, types, methods, properties, public fields, constants, and enum
  values, `camelCase` for parameters and locals, `_camelCase` for private fields, `I` prefix
  for interfaces, `T` prefix for type parameters, `Async` suffix for async methods.
- Full words over truncations in type, file, and project names (`Configuration` not `Conf`,
  `Definition` not `Def`), while ecosystem-idiomatic parameter names such as `args` stay.
- Boolean names read as claims (`IsReadonly`, `HasPendingWork`), and no type encoding in names
  (`strTitle`, `listItems`) - Hungarian-style prefixes outside Win32 interop are findings.
- Test methods read `MethodName_Scenario_ExpectedBehavior` (`GetEntity_MissingId_Throws`),
  so a failing test names the defect in the report.

## Code Quality And Error Handling

From the maintainer's C# engineering standards
(https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
as the base convention).

- `sealed` is the honest class default (the runtime devirtualizes sealed calls), every member
  carries an explicit access modifier, and an interface at a component boundary is contract -
  an interface with one internal implementation is indirection without benefit.
- `record` for immutable data carriers and DTOs, `readonly record struct` for small hot-path
  values, and a primary constructor only when initialization is straight dependency
  assignment - captured parameters live for the instance's lifetime.
- Guards use the framework helpers (`ArgumentNullException.ThrowIfNull`,
  `ArgumentOutOfRangeException.ThrowIfNegative`) for consistent parameter names and messages.
- Categorized error surfaces: one domain exception carrying a failure kind maps to the host's
  exit code or status - parallel exception families per failure kind are duplication.
- Lazy enumerables throw inside `MoveNext`, not at the call - a `try`/`catch` around
  `Directory.EnumerateFiles` guards nothing; guard the iteration site or pass
  `EnumerationOptions` with `IgnoreInaccessible`.
- A `using` declaration disposes at the end of its block - a resource a consumer still needs
  after the block (a shared `HttpClient`) is disposed out from under it; give the consumer
  ownership or create short-lived instances per operation.
- `async` code passes `CancellationToken` through the whole chain, never calls `.Result`/
  `.Wait()` (deadlock + wasted thread), never uses `Thread.Sleep` in async paths, and prefers
  `System.Threading.Channels` for producer/consumer over hand-written locks.
- Forbidden-pattern floor: `dynamic`, `null!` without a `// REASON:` comment, `#pragma warning
  disable` without one, `async void` outside event handlers, static mutable state, empty
  `catch`, `Contains` used as a prefix test (anchor positionally instead), hardcoded secrets.
- XML documentation covers every public API member (`<summary>`, `<param>`, `<returns>`,
  deliberate `<exception>`); `<GenerateDocumentationFile>` makes the compiler report `CS1591`,
  and an orphaned `///` block (member inserted between doc and declaration) reports `CS1572`.
- `.editorconfig` is the single source for style and analyzer severity; the checkable analyzer
  posture is `EnableNETAnalyzers` + `AnalysisLevel=latest` + `AnalysisMode=Recommended` +
  `EnforceCodeStyleInBuild` - without the last, `IDExxxx` rules run only in the IDE and CI
  silently disagrees.

## CLI Surface Contract

From the maintainer's `csharp-cli` engineering standard.

- Exit codes are semantic and defined once in a shared constants class: `0` success, `1`
  unexpected failure only (the code an unhandled exception produces), `2` usage, `3`
  not-found, `4` blocked, `5` unsupported - domain failures map through one categorized
  exception to `error[kind]: message` on stderr (JSON error object on stdout under `--json`).
- The help gate runs before the argument-error gate - `tool --bogus --help` still prints usage
  and exits `0`.
- Option names form one flat namespace across all commands - a command-local meaning on a
  shared name silently hijacks it; use scoped names (`--out`, `--session`).
- A literal `--` terminates flag parsing; raw-arg scans (`--version`/`--help` shortcuts) must
  stop at `--` too or a child's flag hijacks the parent's gate.
- Resource-root resolution precedence: explicit `--root`, then environment variable, then
  walk-up marker-file discovery - a sidecar resource (cache, note store) degrades to a warning,
  the payload resource fails `not-found`.
- Layered settings merge recursively (baseline scope, then profile scope; `null` inherits the
  lower layer), explicit command-line options always outrank configured defaults, credentials
  live in a version-control-excluded secrets file referenced by `secrets:key` indirection, and
  spawned sibling tools receive the resolved root and scope flags.
- Sibling/external invocation goes through one shared runner returning a result record - never
  ad-hoc `Process.Start`: drain stdout and stderr before waiting, bound the wait with a
  timeout that kills the process tree, surface the child's stderr on nonzero exit, resolve the
  executable to an absolute path (`UseShellExecute=false` does not search relative paths), and
  hold stdin open until every expected reply line arrives for stdio protocols (JSON-RPC, LSP,
  MCP).
- A GUI launch is verified on the process tree or window title, never on the launch handle -
  launcher-style apps exit the spawned process while the real tree keeps running.
- Forbidden: progress or banners on `Console.Out`, stack traces on stdout, `Console.ReadLine`
  in batch mode.

## Platform And API Hazards

Recurring .NET defect and portability patterns an audit can confirm from source.

Each probe is a search pattern plus what the result bounds - a hit is a candidate confirmed
by reading, per `assessment/correctness-review.md`.

| Probe                        | Pattern                                                              | What it bounds                                                                                                     |
|------------------------------|----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Forced thread termination    | `Thread.Abort(` calls                                                | Throws `PlatformNotSupportedException` off .NET Framework - declared multi-target surface fails on modern runtimes |
| Binary serialization         | `BinaryFormatter` usage                                              | Obsolete and unsafe deserialization (`SYSLIB0011`), removed from modern .NET                                       |
| Legacy web APIs              | `WebRequest.Create`, `ServicePointManager`, `WebClient`              | Obsolete networking surface (`SYSLIB0014`) and global mutable TLS state                                            |
| Obsolete cryptography        | `DESCryptoServiceProvider`, `MD5.Create`, `SHA1.Create`, `RC2`       | Legacy primitives exposed without warnings (`SYSLIB0021` family)                                                   |
| Explicit-layout overlays     | `[FieldOffset]` overlapping reference-typed and value-typed members  | `TypeLoadException` at type load - managed refs cannot overlap                                                     |
| Value-type null comparisons  | Non-nullable `struct` compared to `null` (`DateTime`, `TimeSpan`)    | Always-false condition hiding a missing branch (compiler `CS8073`)                                                 |
| Uncached XML serializer      | `new XmlSerializer(type, new XmlRootAttribute(...))` in shared paths | Dynamic-assembly leak per construction - serializer instances must be cached                                       |
| Unguarded platform interop   | `[DllImport]` on `kernel32`/`user32`/`psapi` in multi-target code    | Windows-only entry points without platform guards break other targets                                              |
| Non-cryptographic randomness | `System.Random` feeding tokens, keys, or salts                       | Predictable values in security-sensitive flows                                                                     |

## Testing And Build Discipline

From the maintainer's C# engineering standards and
https://learn.microsoft.com/en-us/dotnet/core/tutorials/testing-with-cli.

- One test framework per solution (xUnit, MSTest, or NUnit - all on Microsoft.Testing.Platform);
  test classes are `sealed`, assert one thing, and test observable behavior rather than private
  steps.
- Analyzer-clean assertion forms matter under warnings-as-errors - the xUnit analyzers fail the
  build on LINQ-shaped assertions (xUnit2031), so `Assert.Single(collection, predicate)` over
  `Assert.Single(collection.Where(...))`.
- Process-global swaps (`Console.Out`, culture, environment variables) serialize through a
  shared xUnit `[Collection]` name and always restore in `finally` - the runner executes
  collections in parallel.
- Tests stay free of the file system, network, and clock - `TimeProvider` replaces
  `DateTime.Now`, and string fixtures interpolate a captured `DateTimeOffset` rather than
  hardcoding a calendar date. A test needing a guaranteed zero-exit child spawns the host's
  shell (`%ComSpec%` or `/bin/sh`), never `Environment.ProcessPath` (the testhost apphost exits
  nonzero bare).
- Portable-assembly tests do not assume Windows host semantics (no `cmd.exe`, no `\\`-only
  splits, no registry); host-shaped fixtures branch on `OperatingSystem.IsWindows()` or move to
  a Windows-TFM test assembly, which compiles anywhere but executes only on Windows.
- The documented verification set is evidence for tooling presence: `dotnet build -c Release`
  with warnings-as-errors, `dotnet test`, `dotnet format --verify-no-changes`, zero `CA`/`IDE`/
  `CS1591`/`CS86xx` diagnostics, `dotnet list package --vulnerable --include-transitive`, and a
  `PublishAot` publish free of `IL2xxx`/`IL3xxx` warnings for AOT projects.
- Build hygiene: `global.json` pins the SDK band, `Directory.Build.props` holds shared
  properties (repeated per-project settings drift), `bin/`/`obj/` are never committed, one
  `dotnet` verb takes one project (MSB1008 on multi-project invocations), and
  `EnableWindowsTargeting=true` applies on foreign hosts - as an environment assignment for
  `dotnet format`, not a `-p:` flag.
- Dependency floor: framework API before package, already-used package before a second library
  for the same job, exact pins or Central Package Management (`Directory.Packages.props`),
  floating `*`/`latest` ranges are a reproducibility finding, and a vulnerable transitive
  package is a defect.

## Live Check

When web fetch is available, verify the naming floor against the Microsoft program-organization
and identifier-names documents and record the drift window.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
