# .NET And ASP.NET Core Baseline

## Purpose

> **Scope:** Checkable constraints for .NET libraries and ASP.NET Core services
> **Key items:** naming/design rules, security analyzers, TLS enforcement, authentication
> middleware, rate limiting, NuGet lockfiles, constant-time comparison

This file distills the Microsoft Learn design, security-analysis, ASP.NET Core, and NuGet
sources listed in `references/source-catalog.md` into constraints an audit can verify from
repository source.

Snapshot date: 2026-10-27.

Feeds `assessment/best-practices.md`, `assessment/structure-review.md`,
`assessment/security-review.md`, `assessment/api-compatibility.md`, and
`assessment/baseline-conformance.md` for .NET subjects.

## Design, Naming, And Project Structure

From https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/,
https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/naming-guidelines,
https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/names-of-namespaces,
https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions,
and https://learn.microsoft.com/en-us/dotnet/core/compatibility/.

- Framework Design Guidelines naming: `PascalCase` for namespaces, types, methods, properties,
  constants, and enum values, `camelCase` for parameters and locals, `_camelCase` for private
  fields, `I` prefix for interfaces, `*Async` suffix on asynchronous methods, and no
  `snake_case` or Hungarian prefixes in the public surface.
- Full words over abbreviations: directories, namespaces, and type names use unabbreviated
  words (`Application`, `Authentication`, `Configuration`, `Documentation`,
  `ConnectionParameters`, `EnvironmentSubstitution`) rather than truncated tokens (`App`,
  `Auth`, `Config`, `Docs`, `ConnectionParams`, `EnvSubst`) unless a project standard
  explicitly documents the short form.
- Namespace-to-directory correspondence: namespaces mirror the directory path under the project
  root (`OrderApp.Domain.Entities` in `Domain/Entities/`). Multi-layer solutions separate
  `Domain`, `Application`, `Infrastructure`, and `Api` into distinct `.csproj` projects with
  shared settings in `Directory.Build.props`.
- Code division: place one public top-level type (`class`, `interface`, `struct`, `enum`, or
  `record`) per `PascalCase.cs` file matching the type name, separate interfaces
  (`IOrderService.cs`) from their implementations (`OrderService.cs`, `NullRevocationStore.cs`),
  use `abstract class` for shared base behavior, and avoid `Misc`/`Util` catch-all classes.
- Ported-idiom checks: enum members with type-initial prefixes (`psNew`, `psConnected`),
  type-letter method suffixes (`ValueI`, `ValueB`), CLR struct names (`Boolean`, `Int32`,
  `String`) in place of C# keywords (`bool`, `int`, `string`), and Minimal API static endpoint
  classes named `*Controller` without inheriting from `ControllerBase` are naming findings.
- The breaking-change taxonomy distinguishes binary compatibility (drop-in replacement) from
  source compatibility (recompiles) and behavioral changes. A major-version claim needs a
  compatibility assessment against that taxonomy.
- `Obsolete` attributes carry messages and flag error escalation. Removing an API without an
  `Obsolete` period is a breaking-change finding for libraries.
- The non-negotiable floor: `<Nullable>enable</Nullable>` project-wide, no `dynamic`, no
  `Console.WriteLine` in production code (`ILogger<T>` is the channel), no hardcoded secrets,
  no `async void` outside event handlers, and every endpoint returns a typed result - an
  `object`/`dynamic` return is a defect.
- Configuration loads in a declared precedence - file, then prefixed environment variables, then
  command-line arguments - and a divergence between the documented order and the composition
  root is a finding.
- The startup sequence is ordered and visible: load and validate configuration, register DI
  services, configure auth middleware, map route groups, start background services, pre-load
  caches - plus a graceful-shutdown path that drains in-flight requests.
- Sensitive configuration files are permission-checked where the OS supports it, secret values
  never reach logs, and the shipped container image runs as a non-root user.

## Security Analyzers

From
https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/security-warnings.

- The CA3xxx/CA53xx security-warning set maps to `references/cwe-analyzer.md`: CA2100 SQL
  injection review, CA3001-3012 injection/XSS/open-redirect/file-injection surfaces,
  CA5350/CA5351 weak crypto (SHA1/MD5/DES), CA5360-5369 deserialization and certificate
  validation hazards, CA5390-5394 hardcoded keys, insecure randomness, insecure transport.
- Analyzers enabled (`AnalysisLevel`, `.editorconfig`, or `EnforceCodeStyleInBuild`) with
  security rules not globally suppressed is the checkable posture. A `GlobalSuppressions`
  file full of CA3xxx is a finding.

## ASP.NET Core Security

From https://learn.microsoft.com/aspnet/core/security/enforcing-ssl,
https://learn.microsoft.com/aspnet/core/security/authentication/, and
https://learn.microsoft.com/aspnet/core/performance/rate-limit.

- `UseHttpsRedirection` and HSTS (`UseHsts` outside development) enforce TLS. An app missing
  both relies on deployment, which the report must state.
- Authentication is middleware (`UseAuthentication` before `UseAuthorization`).
  `JwtBearer` options `Authority`/`Audience`/`TokenValidationParameters` define the contract -
  `ValidateIssuer = false` or `RequireSignedTokens = false` are findings.
- `[Authorize]` attributes or `RequireAuthorization()` on endpoints provide coverage.
  `AllowAnonymous` entries are the explicit exceptions to review.
- `AddRateLimiter` middleware provides fixed/sliding-window and token-bucket limiters.
  Unauthenticated endpoints without a limiter are a resource-exhaustion observation.
- `CryptographicOperations.FixedTimeEquals`
  (
  https://learn.microsoft.com/dotnet/api/system.security.cryptography.cryptographicoperations.fixedtimeequals)
  is the constant-time comparison for secrets. `==`/`SequenceEqual` on MACs and tokens is a
  timing finding.

## NuGet And Locking

From https://learn.microsoft.com/nuget/consume-packages/package-references-in-project-files.

- `PackageReference` in the project file is the modern form. `packages.config` is legacy.
- `packages.lock.json` is opt-in via `RestorePackagesWithLockFile`. With
  `RestoreLockedMode` the build fails when the lockfile and project disagree - the CI
  reproducibility control.
- Floating versions (`*`, `1.*`) resolve nondeterministically and defeat lockfile intent.
  Floating references in a committed build are a reproducibility finding.
- Central Package Management (`Directory.Packages.props`) is the monorepo convention for
  version consistency.

## Build And Analysis Floor

From https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props and
https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview.

- `TreatWarningsAsErrors` plus `EnforceCodeStyleInBuild` makes the analyzer set a gate rather
  than a suggestion - `<WarningsAsErrors>`-without-`<NoWarn>` sprawl is the checkable posture.
- A `global.json` pins the SDK band so a machine with a newer SDK does not silently shift the
  build. Its absence is an observation, not a defect.
- `dotnet format --verify-no-changes` is the CI check mode - a build that runs `format`
  without `--verify-no-changes` mutates the tree instead of checking it.
- `<Nullable>enable</Nullable>` is the reference floor. `#nullable disable` regions and
  `!` suppression on public API surfaces are reviewable per-site.
- `GenerateDocumentationFile` plus `<NoWarn>1591</NoWarn>`-free builds keep XML doc
  generation honest - an empty `<summary>` count is a signal, not a rule.
- Platform-specific code behind `SupportedOSPlatform`/CA1416-aware seams is the checkable
  shape - `OperatingSystem.IsWindows()`-style guards that callers can skip are the softer
  alternative.
- `PublishAot`/`PublishTrimmed` turns IL2xxx/IL3xxx trim/analyzer warnings into the contract:
  reflection-heavy libraries need `[DynamicallyAccessedMembers]` or source-generated
  serialization instead of runtime `JsonSerializer` defaults.

## Minimal API And Test Layout

From the maintainer's C# ASP.NET engineering standard.

- Minimal-API services organize under `Config/` (composition root plus `*Settings`),
  `Auth/` (`*Handler`, `*Extensions`), `Endpoints/` (`*Endpoints` classes, `*Request` and
  `*Response` records), `Services/` (`*Service` interfaces with `Default*Service`
  implementations), `Data/` (`*Store`, `*MappingExtensions`), and `Resources/` (JSON or static
  payloads) - a service whose `Program.cs` holds endpoint bodies past a few mappings is a
  division finding.
- Test projects follow `<ProjectName>.Tests` under `test/` (or `tests/`), mirror the source
  directory structure inside, and name classes `<TypeUnderTest>Tests` in
  `<TypeUnderTest>Tests.cs` files - integration suites add a `*Factory` fixture class.
- Web projects keep `PascalCase.cs` files named for their single public type and split
  classes approaching 300-500 lines along responsibility seams (`Type.<Area>.cs` partials) -
  a 1,000-line controller class is a cognitive-load finding, not a naming one.

## Live Check

When web fetch is available, spot-check one CA security rule against the Microsoft Learn
catalog and one middleware name against the ASP.NET Core docs.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
