# Java, Kotlin, And Spring Baseline

## Purpose

> **Scope:** Checkable constraints for JVM services built with Java or Kotlin, Spring, Maven,
> and Gradle
> **Key items:** filter-chain authorization, TLS/password storage, metrics surface, build
> verification, API-compatibility tools, Oracle secure-coding rules

This file distills the Spring Security, Spring Boot, Micrometer, Gradle, Oracle secure-coding,
FindSecBugs, japicmp/Revapi, and Kotlin sources listed in `references/source-catalog.md` into
constraints an audit can verify from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/security-review.md`, `assessment/dependency-review.md`,
`assessment/api-compatibility.md`, and `assessment/best-practices.md` for JVM subjects.

## Spring Security

From https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html,
https://docs.spring.io/spring-boot/reference/features/ssl.html, and
https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html.

- Authorization is filter-chain ordered: `authorizeHttpRequests` rules evaluate top-down and
  the first match wins, so a broad `permitAll()` before a restrictive rule defeats it -
  read rule order, not just presence.
- `anyRequest().authenticated()` or an equivalent catch-all is the safe default. Endpoints
  missing from explicit matchers fall through to whatever `anyRequest` allows.
- `@PreAuthorize`/`@EnableMethodSecurity` enforce at the method layer. A controller with no
  URL-level rule and no method-level annotation is unprotected by default.
- CSRF protection is enabled by default for browser-facing flows. Disabling it is justified
  only for token-authenticated stateless APIs and is a reviewable deviation.
- Password storage goes through `PasswordEncoder` (`BCryptPasswordEncoder` or
  `DelegatingPasswordEncoder`). Plaintext or single-hash comparisons are findings.
- Spring Boot SSL config (`server.ssl.*`) terminates TLS at the app. Behind a proxy,
  `server.forward-headers-strategy` controls trust of `X-Forwarded-*`.

## Observability

From https://micrometer.io/docs registry documentation (canonical page:
https://docs.micrometer.io/micrometer/reference/implementations/prometheus.html).

- Micrometer is the metrics facade. The Prometheus registry exposes `/actuator/prometheus`
  in Spring Boot - an absent metrics endpoint on a service claiming observability is a gap.
- Actuator endpoints (`/actuator/health`, `/actuator/env`, `/actuator/heapdump`) must be
  exposure-scoped. `management.endpoints.web.exposure.include=*` on a public port is a
  security finding.

## Build And Dependency Verification

From https://docs.gradle.org/current/userguide/dependency_verification.html and
https://github.com/chains-project/maven-lockfile.

- Gradle dependency verification writes `gradle/verification-metadata.xml` with checksums and
  key pins. Its presence turns dependency resolution into a verifiable step.
- `maven-lockfile` produces `lockfile.json` recording resolved versions and checksums for
  Maven builds that need reproducibility.
- `mvn -o`/offline or `gradle --offline` behavior is evidence of vendored builds, not a defect
  by itself.
- `SNAPSHOT` dependencies in a release path are findings: snapshots are mutable artifacts.

## Secure Coding And Analysis

From https://www.oracle.com/java/technologies/javase/seccodeguide.html and
https://find-sec-bugs.github.io/bugs.htm.

- Oracle Secure Coding Guidelines checkable subset: validate inputs at trust boundaries,
  avoid `Runtime.exec` with untrusted strings, never deserialize untrusted data with native
  `ObjectInputStream`, use `SecureRandom` for security purposes, and do not log secrets.
- Deserialization of attacker-controlled streams is a critical finding class. JDK allowlist
  filters (`jdk.serialFilter`) mitigate but do not eliminate it.
- FindSecBugs (SpotBugs plugin) rule names feed `references/cwe-analyzer.md`: SQL injection,
  command injection, path traversal, XXE, weak crypto (`WEAK_MESSAGE_DIGEST`,
  `DES_USAGE`), `PREDICTABLE_RANDOM`, hardcoded passwords.

## Compatibility And Kotlin

From https://github.com/siom79/japicmp, https://revapi.org/, and
https://kotlinlang.org/docs/coding-conventions.html.

- japicmp and Revapi are the API-diff tools for released libraries. A release without an
  API-diff report can't claim semver compliance mechanically.
- Kotlin coding conventions are the style floor: camelCase properties/functions, PascalCase
  classes, `val` preferred over `var`, named arguments for multi-parameter calls.
- Kotlin null-safety is the language contract. `!!` operators and platform-type leaks across
  Java interop are reviewable.

## Live Check

When web fetch is available, spot-check one Spring authorization rule against the reference
and one FindSecBugs pattern name against the catalog.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
