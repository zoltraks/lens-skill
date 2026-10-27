# Java, Kotlin, And Spring Baseline

## Purpose

> **Scope:** Checkable constraints for JVM services built with Java or Kotlin, Spring, Maven,
> and Gradle
> **Key items:** filter-chain authorization, TLS/password storage, metrics surface, build
> verification, API-compatibility tools, Oracle secure-coding rules

This file distills the Spring Security, Spring Boot, Micrometer, Gradle, Oracle secure-coding,
FindSecBugs, japicmp/Revapi, and Kotlin sources listed in `references/source-catalog.md` into
constraints an audit can verify from repository source.

Snapshot date: 2026-10-27.

Feeds `assessment/security-review.md`, `assessment/dependency-review.md`,
`assessment/api-compatibility.md`, `assessment/best-practices.md`, and
`assessment/baseline-conformance.md` for JVM subjects.

## Spring Security

From
https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html,
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

## Compatibility, Layout, And Naming

From https://github.com/siom79/japicmp, https://revapi.org/,
https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html,
https://docs.oracle.com/javase/specs/jls/se17/html/jls-6.html,
https://docs.spring.io/spring-boot/reference/using/structuring-your-code.html, and
https://kotlinlang.org/docs/coding-conventions.html.

- Maven and Gradle standard directory layout separates `src/main/java`, `src/main/resources`,
  and `src/test/java`. Every directory path under `src/main/java` must match the `package`
  declaration in lowercase reverse-DNS form (`com.example.orderapp.service`), and each public
  top-level type lives in its own `PascalCase.java` file.
- Java naming and code division: classes, records, enums, and interfaces use `PascalCase` with
  no `I` prefix on interfaces (`OrderService`, `OrderRepository`), concrete implementations
  name their role or backing strategy (`DefaultOrderService`, `InMemoryOrderRepository`,
  `JpaOrderRepository`), methods, fields, and parameters use `camelCase`, constants and enum
  values use `UPPER_SNAKE_CASE`, DTOs use Java 17+ `record` types under `api/dto/`, and JUnit 5
  test classes use `<Class>Test.java` or `<Class>Tests.java`.
- Spring Boot code structure places the `@SpringBootApplication` entry class at the root
  package (`com.example.orderapp.OrderApplication`) above `api`, `config`, `domain`, `service`,
  and `repository` subpackages, never in the default (unnamed) package.
- japicmp and Revapi are the API-diff tools for released libraries. A release without an
  API-diff report can't claim semver compliance mechanically.
- Kotlin coding conventions are the style floor: camelCase properties/functions, PascalCase
  classes, `val` preferred over `var`, named arguments for multi-parameter calls.
- Kotlin null-safety is the language contract. `!!` operators and platform-type leaks across
  Java interop are reviewable.
- Spring role-suffix naming from the maintainer's engineering standard: `*Controller`,
  `*Service`, `*Repository`, `*Config`/`*Configuration`, `*Entity`, `*Filter`, `*Properties`,
  `*Client`, and `*Request`/`*Response` DTOs - a `*Manager` or `*Helper` catch-all name is an
  observation that the class hides a role.
- Maven module conventions: `artifactId` is `kebab-case` and the module's directory name
  equals its `artifactId`, the aggregator `pom.xml` lists modules in build order, and
  `groupId` is the reverse-DNS owner (`com.example`).
- Database migrations follow the tool's own scheme - Flyway `V<n>__<snake_case_desc>.sql`,
  Liquibase `kebab-case` change-sets - and a migration file renamed after application is a
  history defect.
- Package-by-feature (`com.example.order.OrderController`, `Order`, `OrderService`,
  `OrderRepository` grouped under one `order` package) is the Spring-endorsed alternative to
  layered packages - the audit checks which model the project follows, never prescribes one.

## Persistence And Transactions

From https://jakarta.ee/specifications/persistence/ and
https://docs.spring.io/spring-framework/reference/data-access/transaction.html.

- `@Transactional` belongs on the service boundary, not the repository or controller. A
  transaction spanning a network call or `.await`-equivalent widens the lock window.
- Lazy fetching is the default for collections: `FetchType.EAGER` on a `@OneToMany` is a
  reviewable choice, and the N+1 pattern it produces is the checkable defect.
- `ddl-auto` outside `validate`/`none` on a non-disposable environment is a finding - real
  schema changes go through versioned migrations (Flyway/Liquibase), and a released migration
  is never edited.
- Tests run against the real engine through Testcontainers or the declared equivalent - an
  H2 substitute accepts DDL and dialect the target rejects.
- `@Version` optimistic locking is the default answer to concurrent writes - destructive
  concurrent updates are a finding.
- The shared contract lives in `references/topics/data-persistence.md` - this section only
  carries the JVM-specific shape.

## Maintainer-Standard Floor

From the maintainer's Java, Maven, and Spring engineering standards.

- The defect floor: raw types (`List` without parameters), checked exceptions in new code,
  swallowed `catch` blocks, `System.out.println` diagnostics (SLF4J is the channel), `null`
  returns from public methods (`Optional`, empty collection, or throw), raw `Thread.sleep`
  where virtual threads apply, and pooled virtual threads
  (`Executors.newVirtualThreadPerTaskExecutor()` per task, never pooled).
- Spring specifics: constructor injection only (field and setter injection are defects), no
  stack traces in HTTP responses, externalized configuration, and no repository logic inside
  entities or controllers.
- Persistence floor: every entity declares its key strategy (`@GeneratedValue` explicit),
  `FetchType.EAGER` on a to-many association is a defect, `ddl-auto` is disabled outside
  disposable environments, and schema change goes through migrations.
- Maven/Gradle floor: the build succeeds from a clean checkout, dependency versions are pinned
  (no `*`/unbounded ranges), `target/` and `build/` stay gitignored, a `-SNAPSHOT` in a tagged
  release is a defect, and `mvn package`/`gradle build` is the packaging entry point - a custom
  script bypassing the lifecycle is a finding.

## Live Check

When web fetch is available, spot-check one Spring authorization rule against the reference
and one FindSecBugs pattern name against the catalog.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
