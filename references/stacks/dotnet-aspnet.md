# .NET And ASP.NET Core Baseline

## Purpose

> **Scope:** Checkable constraints for .NET libraries and ASP.NET Core services
> **Key items:** naming/design rules, security analyzers, TLS enforcement, authentication
> middleware, rate limiting, NuGet lockfiles, constant-time comparison

This file distills the Microsoft Learn design, security-analysis, ASP.NET Core, and NuGet
sources listed in `references/source-catalog.md` into constraints an audit can verify from
repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/best-practices.md`, `assessment/security-review.md`, and
`assessment/api-compatibility.md` for .NET subjects.

## Design And Compatibility

From https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/ and
https://learn.microsoft.com/en-us/dotnet/core/compatibility/.

- Framework Design Guidelines naming: `PascalCase` for types and public members,
  `camelCase` for parameters and locals, `I` prefix for interfaces, no `snake_case` in the
  public surface.
- The breaking-change taxonomy distinguishes binary compatibility (drop-in replacement) from
  source compatibility (recompiles) and behavioral changes. A major-version claim needs a
  compatibility assessment against that taxonomy.
- `Obsolete` attributes carry messages and flag error escalation. Removing an API without an
  `Obsolete` period is a breaking-change finding for libraries.

## Security Analyzers

From https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/security-warnings.

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
  unauthenticated endpoints without a limiter are a resource-exhaustion observation.
- `CryptographicOperations.FixedTimeEquals`
  (https://learn.microsoft.com/dotnet/api/system.security.cryptography.cryptographicoperations.fixedtimeequals)
  is the constant-time comparison for secrets. `==`/`SequenceEqual` on MACs and tokens is a
  timing finding.

## NuGet And Locking

From https://learn.microsoft.com/nuget/consume-packages/package-references-in-project-files.

- `PackageReference` in the project file is the modern form. `packages.config` is legacy.
- `packages.lock.json` is opt-in via `RestorePackagesWithLockFile`. With
  `RestoreLockedMode` the build fails when the lockfile and project disagree - the CI
  reproducibility control.
- Floating versions (`*`, `1.*`) resolve nondeterministically and defeat lockfile intent.
  floating references in a committed build are a reproducibility finding.
- Central Package Management (`Directory.Packages.props`) is the monorepo convention for
  version consistency.

## Live Check

When web fetch is available, spot-check one CA security rule against the Microsoft Learn
catalog and one middleware name against the ASP.NET Core docs.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
