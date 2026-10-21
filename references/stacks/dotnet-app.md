# .NET Application And Library Baseline

## Purpose

> **Scope:** Checkable constraints for non-web .NET codebases - console tools, class
> libraries, desktop utilities, and multi-project solutions
> **Key items:** solution/project hierarchy, namespace-directory mirroring, file naming,
> test-project conventions, role-directory patterns

This file distills the Microsoft program-organization and C# coding-convention sources listed
in `references/source-catalog.md`, plus the maintainer's C# engineering standards
(`csharp-general`, `csharp-cli`, `csharp-mcp`, `csharp-automation`, `automation-general`,
`automation-web`, `automation-windows`) into constraints an audit can verify from repository
source.

Snapshot date: 2026-10-21.

Feeds `assessment/structure-review.md`, `assessment/code-style.md`,
`assessment/best-practices.md`, and `assessment/baseline-conformance.md` for .NET subjects.

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

## Live Check

When web fetch is available, verify the naming floor against the Microsoft program-organization
and identifier-names documents and record the drift window.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
