# Naming Conventions, Project Layout, And Code Division

## Purpose

> **Scope:** Cross-stack directory layouts, file-naming rules, language-idiomatic code
> division, and in-code identifier conventions by component purpose and technology stack
> **Key items:** component-role layout rules, cross-language naming matrices, code-division
> idioms, 11 canonical stack fixtures, fallback procedure for unlisted stacks

This reference consolidates directory-organization rules, source-file naming conventions,
language-idiomatic code division, and in-code identifier naming across supported programming
languages, frameworks, and documentation projects.

Apply `principles/evaluation-rules.md` throughout.

It feeds `assessment/structure-review.md`, `assessment/best-practices.md`,
`assessment/standards-conformance.md`, and `assessment/baseline-conformance.md`, and anchors
the `Structure Review` and `Structure Conformance` report sections.

Snapshot date: 2026-10-21.

## Contents

| Section                            | Line | What it covers                                              |
|------------------------------------|------|-------------------------------------------------------------|
| Component-Purpose Layout Rules     | 35   | How libraries, services, apps, CLIs, and docs differ        |
| Polyglot Repositories              | 82   | Per-partition baseline resolution for multi-stack repos     |
| Directory Naming Principles        | 114  | Full-word discipline, singular/plural, and catch-all bans   |
| Cross-Language Naming Matrices     | 141  | File, package, type, member, variable, and test conventions |
| Framework And Tooling Overrides    | 212  | Framework-imposed names that supersede language defaults    |
| Language-Idiomatic Code Division   | 237  | Type-to-file rules, interfaces, abstracts, and DI wiring    |
| Canonical Stack Fixtures           | 288  | Reference layouts and idioms across 11 languages/stacks     |
| Fallback For Unlisted Technologies | 750  | Auditing languages, frameworks, and docs not in the tables  |

## Component-Purpose Layout Rules

Evaluate every component in a repository independently against its own purpose (`library`,
`service`, `application`, `cli`, `test-suite`, `documentation`, or `agent-package`) per
`references/domain-profiles.md`, never as an undifferentiated tree.

A single repository often contains components of different natures - for example a reusable
core library under `src/OrderApp.Domain/`, an HTTP service under `src/OrderApp.Api/`, a CLI
migration tool under `tools/`, a test suite under `tests/`, and a documentation tree under
`docs/`.

Different structural and naming rules govern each component role:

| Component Role  | Structural Priorities                                           | Typical Layout Signals                                                     |
|-----------------|-----------------------------------------------------------------|----------------------------------------------------------------------------|
| `library`       | Public contract isolation, zero transport coupling, SemVer gate | Separate public header/package surface (`include/`, exported root module)  |
| `service`       | Transport vs domain vs persistence separation, boundary schemas | `api/` or `Controllers/`, `domain/`, `service/`, `repository/`, middleware |
| `application`   | Thin composition root, UI/host lifecycle isolated from logic    | `Program.cs`/`main.py`/`main.rs` wiring only, domain logic in submodules   |
| `cli`           | Command/flag parsing separated from core library execution      | `cmd/<app>/main.go` or `src/main.rs` calling `internal/` or `src/lib.rs`   |
| `test-suite`    | Mirrors production module tree, isolates fixtures from cases    | `tests/` mirroring `src/` folders, dedicated `conftest.py` or helpers      |
| `documentation` | Reader-task separation, single owner per topic, stable anchors  | Diataxis quadrants (`tutorials/`, `how-to/`, `reference/`, `explanation/`) |
| `agent-package` | Entry contract isolation, one directory per member or resource  | Root `SKILL.md`, conventional `scripts/`, `references/`, `assets/` dirs    |

Component-specific evaluation rules:

- **Libraries** must separate public API contracts from internal implementation (`internal/` in
  Go, `pub` vs `pub(crate)` in Rust, `public` vs `internal` assemblies/namespaces in C#,
  `include/<pkg>/` vs `src/` in C++20, exported package roots in Python/TypeScript).
- **Services** must separate wire/transport concerns (HTTP controllers, route handlers, request
  and response DTOs, auth/error middleware) from domain models and persistence adapters so
  transport types do not leak into domain logic.
- **Applications and CLIs** must keep the entry point (`main`, `Program.cs`, `__main__.py`,
  `index.php`) as a thin composition root that wires configuration and dependencies without
  embedding business rules.
- **Test suites** must mirror the component boundaries they verify and use the stack's
  discovery-compatible file naming (`test_*.py`, `*Test.java`, `*Tests.cs`, `*_test.go`,
  `*.test.ts`, `*Test.php`, `*_test.cpp`).
- **Documentation projects** and `docs/` trees are audited against
  `references/topics/markdown-standards.md` and `assessment/agent-guidance.md`: lowercase
  `kebab-case.md` topic files, uppercase root governance files (`README.md`, `AGENTS.md`,
  `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`), and clear separation between reference specs,
  how-to guides, and architecture decisions.
- **Agent packages** and skill collections follow the layout conventions distilled in
  `references/agent-skills.md` and `references/agent-configuration.md`: a root `SKILL.md`
  entry, conventional optional directories (`scripts/`, `references/`, `assets/`), and for a
  collection an index plus one separated directory per member.

## Polyglot Repositories

A repository that ships several language partitions resolves a naming and layout baseline
**per partition**, never one baseline for the whole tree.

A multi-language repository - for example a product that ships sibling C#, Go, Java, and
Node.js implementations of the same service, or a client in TypeScript beside a PHP server -
gives each partition its own baseline: the Java partition answers to the Maven/Gradle layout
and Spring suffixes, the Go partition to `cmd/`/`internal/` and `snake_case.go`, the C#
partition to solution/project/namespace mirroring, and shared infrastructure (workflows,
compose files, OpenAPI contracts, shell scripts) to its own digest.

Apply these rules:

- **Detect partitions first** - `references/stack-standards.md` detection signals identify each
  partition's stack from its own manifests (`pom.xml`, `go.mod`, `*.csproj`, `package.json`,
  `composer.json`, `Cargo.toml`, `build.zig`) before any naming judgement applies.
- **One baseline per partition** - inside one partition only that stack's matrix row, fixture,
  and `references/stacks/` digest apply. A `camelCase` helper in the Go partition and a
  `PascalCase` class in the C# partition of the same repository are both correct.
- **Cross-partition consistency is the reportable signal** - when partitions claim to mirror
  each other (parallel ports, shared protocol buffers, one OpenAPI contract generating several
  clients), divergent naming of the *same* domain concept across partitions is an observation
  under `Structure Conformance`, recorded as cross-partition drift, not as a style defect in
  either partition.
- **Root-level conventions belong to the repository role** - `README.md`, `.github/`,
  `docs/`, and `work/` follow the component-role rules above regardless of which partitions
  exist underneath.
- **No partition without a baseline** - an unlisted or hybrid partition falls through to the
  fallback procedure below for that partition only, while the rest of the repository keeps its
  resolved baselines.

## Directory Naming Principles

Directory names are the primary navigation surface of a codebase and map directly to packages
or namespaces in Java, C#, Python, Go, and PHP.

Apply these checks to every component's directory hierarchy:

- **Full words over arbitrary abbreviations** - in ecosystems whose standard libraries use
  unabbreviated words (C#/.NET, Java, Python, PHP, TypeScript), directory and namespace names
  use full domain terms (`Application`, `Authentication`, `Configuration`, `Documentation`,
  `Controllers`, `Repositories`, `Services`, `Exceptions`) rather than ad-hoc truncations
  (`App`, `Auth`, `Config`, `Docs`, `Repo`, `Svc`, `Exc`).
- **Recognized ecosystem directory tokens** - standard top-level build/layout roots (`src`,
  `tests`, `test`, `cmd`, `internal`, `pkg`, `include`, `public`, `var`, `db`, `api`, `dto`)
  are established conventions when the language or build tool prescribes them.
- **Abbreviation consistency** - when a project deliberately adopts short feature-folder names
  (`Auth/`, `Config/`, `Docs/`, `Sql/`), check whether the choice is documented as a project
  convention and whether it conflicts with the language's namespace design guidelines (such as
  Microsoft's .NET Framework Design Guidelines for namespace naming).
- **Singular versus plural consistency** - a layer-organized tree uses either plural collection
  nouns (`Controllers/`, `Services/`, `Repositories/`, `Entities/`, `Enums/`, `Exceptions/` in
  C#, Python, JS/TS, Delphi) or singular package nouns (`api/`, `domain/`, `service/`,
  `repository/` in Java, Go, Rust, C++), never an unexplained mix at the same level.
- **Ban on catch-all directories** - directories or units named `Misc`, `Util`, `Utils`,
  `Common`, `Helpers`, or `Shared` that accumulate unrelated responsibilities (for example
  mixing cryptographic hashing with HTTP context extraction) are structural findings.

## Cross-Language Naming Matrices

### Python 3.10+, Java 17+, And C# 8+

Canonical sources: [PEP 8](https://peps.python.org/pep-0008/),
[PyPA Packaging Guide](https://packaging.python.org/en/latest/),
[Java Language Specification Section 6](https://docs.oracle.com/javase/specs/jls/se17/html/jls-6.html),
[Maven Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html),
[Microsoft Framework Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/naming-guidelines),
and [C# Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions).

| Element              | Python 3.10+                        | Java 17+                                  | C# 8+ (.NET)                              |
|----------------------|-------------------------------------|-------------------------------------------|-------------------------------------------|
| Source file          | `snake_case.py` (`order_service`)   | `PascalCase.java` matching public type    | `PascalCase.cs` matching primary type     |
| Directory            | `snake_case` package dir            | lowercase package path (`com/example/…`)  | `PascalCase` matching namespace segment   |
| Package / namespace  | lowercase, short (`services`)       | lowercase reverse-DNS (`com.example.…`)   | `PascalCase` (`OrderApp.Domain.Entities`) |
| Class / record / exc | `PascalCase` (`OrderNotFoundError`) | `PascalCase` (`OrderNotFoundException`)   | `PascalCase` (`OrderNotFoundException`)   |
| Interface / protocol | `PascalCase`, no `I` (`Protocol`)   | `PascalCase`, no `I` (`OrderService`)     | `IPascalCase` (`IOrderService`)           |
| Method / function    | `snake_case`                        | `camelCase`                               | `PascalCase` (`CreateAsync`)              |
| Variable / parameter | `snake_case`                        | `camelCase`                               | `camelCase`                               |
| Constant / enum item | `UPPER_SNAKE_CASE`                  | `UPPER_SNAKE_CASE`                        | `PascalCase` (no type prefix on enums)    |
| Private field        | `_leading_underscore`               | `camelCase` (no prefix)                   | `_camelCase`                              |
| Test file            | `test_<module>.py`                  | `<Class>Test.java` or `<Class>Tests.java` | `<Class>Tests.cs`                         |
| Build manifest       | `pyproject.toml`                    | `pom.xml` or `build.gradle(.kts)`         | `*.sln` / `*.slnx`, `*.csproj`, `.props`  |

### PHP 8.3, Rust, Go 1.22+, JavaScript, TypeScript, Pascal, And C++20

Canonical sources: [PSR-1](https://www.php-fig.org/psr/psr-1/),
[PSR-4](https://www.php-fig.org/psr/psr-4/),
[PSR-12](https://www.php-fig.org/psr/psr-12/),
[Rust API Guidelines](https://rust-lang.github.io/api-guidelines/naming.html),
[Cargo Project Layout](https://doc.rust-lang.org/cargo/guide/project-layout.html),
[Effective Go](https://go.dev/doc/effective_go#names),
[Go Module Layout](https://go.dev/doc/modules/layout),
[TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html),
[Free Pascal Reference](https://www.freepascal.org/docs-html/ref/ref.html),
[Object Pascal Style Guide](https://edn.embarcadero.com/article/10280),
and [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-naming).

| Language    | Source File               | Types / Interfaces                  | Functions / Methods      | Fields / Params / Constants                    | Test Files                   |
|-------------|---------------------------|-------------------------------------|--------------------------|------------------------------------------------|------------------------------|
| PHP 8.3     | `PascalCase.php` (PSR-4)  | `PascalCase`, no `I` prefix         | `camelCase()`            | `$camelCase`, `UPPER_SNAKE`, enum `PascalCase` | `*Test.php`                  |
| Rust        | `snake_case.rs`           | `PascalCase` (`struct`/`trait`)     | `snake_case`             | `snake_case`, `UPPER_SNAKE`                    | `tests/*.rs`, `#[cfg(test)]` |
| Go 1.22+    | `snake_case.go`           | `PascalCase` exported, `camelCase`  | `PascalCase`/`camelCase` | `camelCase`, exported `PascalCase`             | `*_test.go`                  |
| JavaScript  | `kebab-case.js`           | `PascalCase` classes                | `camelCase`              | `#privateField`, `UPPER_SNAKE`                 | `*.test.js`                  |
| TypeScript  | `kebab-case.ts`           | `PascalCase`, no `I` prefix         | `camelCase`              | `camelCase`, `UPPER_SNAKE`                     | `*.test.ts`                  |
| Free Pascal | `lowercase.pas` unit file | `T` class/record, `I` intf, `E` exc | `PascalCase`             | `FField`, `AParam`, enum `osPending`           | `test*.pas`                  |
| Delphi      | `Namespace.Unit.pas`      | `T` class/record, `I` intf, `E` exc | `PascalCase`             | `FField`, `AParam`, enum `osPending`           | `*.Tests.*.pas`              |
| C++20       | `snake_case.hpp` / `.cpp` | `PascalCase` (or `snake_case` std)  | `snake_case`             | `member_`, `snake_case`, `kConst`              | `*_test.cpp`                 |

### Zig, Shell, And Assembly

Canonical sources: [Zig Style Guide](https://ziglang.org/documentation/master/#style-guide),
[Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html),
[DASM user guide](https://dasm-assembler.github.io/), and
[ca65 Users Guide](https://cc65.github.io/doc/ca65.html).

| Language | Source File                                        | Types / Interfaces          | Functions / Methods             | Fields / Params / Constants                    | Test Files            |
|----------|----------------------------------------------------|-----------------------------|---------------------------------|------------------------------------------------|-----------------------|
| Zig      | `TitleCase.zig` struct, `snake_case.zig` namespace | `TitleCase` types           | `camelCase`                     | `snake_case` fields, `SCREAMING_SNAKE` consts  | inline `test` blocks  |
| Shell    | `snake_case.sh` or `kebab-case.sh`                 | n/a                         | `snake_case`                    | `UPPER_SNAKE` env/exported, `snake_case` local | `*_test.sh`/`bats`    |
| Assembly | `.asm`/`.s`, `.inc`/`.mac` includes                | n/a - `UPPER_SNAKE` equates | `snake_case`/`lowercase` labels | `UPPER_SNAKE` constants, terse locals          | per-toolchain harness |

Zig file naming follows the official type rule (a file that *is* a struct uses `TitleCase`,
namespace files use `snake_case`), yet many projects adopt uniform `snake_case` - detect the
partition's declared or dominant rule before flagging either shape.

Assembly label casing is dialect- and project-specific: the working yardstick is the dominant
shape inside the partition, and terse labels plus dialect local-label syntax are idiomatic
rather than noise - see `references/stacks/assembly.md`.

## Framework And Tooling Overrides

A detected framework or toolchain imposes names that supersede the language defaults in the
matrices - framework-conforming names are never flagged against the language row.

| Detected signal                               | Override the language defaults with                                                                              |
|-----------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| Spring `@SpringBootApplication`               | Root-package entry class, `*Controller`/`*Service`/`*Repository`/`*Config`/`*Entity` suffixes, `application.yml` |
| ASP.NET Core (`Program.cs`, `WebApplication`) | `*Controller` or `*Endpoints` classes, `I`-prefixed interfaces, `appsettings*.json`                              |
| Electron (`main` field, `electron` dep)       | Process-split layout (`main`/`preload`/`renderer` dirs), `preload.*` bridge scripts                              |
| React / Vite (`jsx`/`tsx`, `vite.config.*`)   | `PascalCase.tsx` components, `use*` hooks, root `index.html`, `public/` static assets                            |
| Next/Nuxt/SvelteKit config                    | File-based routing dirs (`app/`/`pages/`/`routes/`) - filenames *are* URLs                                       |
| Django/Flask/FastAPI imports                  | `views.py`/`urls.py`/`routers`, `wsgi.py`/`asgi.py`, `templates/`                                                |
| Rails (`Gemfile`, `config/routes.rb`)         | `app/` role dirs (`models`, `controllers`, `views`), `snake_case` everything, `db/migrate/`                      |
| PHPUnit/Pest (`phpunit.xml`)                  | `*Test.php` mirroring `src/` namespaces under `tests/`                                                           |
| pytest (`pyproject.toml`, `conftest.py`)      | `test_*.py` modules, `test_*` functions, `conftest.py` fixtures                                                  |
| `docker-compose.yaml`/`compose.yaml`          | `kebab-case` service and volume names, `Dockerfile[.<variant>]`                                                  |
| `.github/workflows/*.yml`                     | `kebab-case.yml` filenames, `action.yml` composite actions                                                       |
| OpenAPI `openapi:` key                        | `PascalCase` schemas, `kebab-case` paths/tags, `operationId` `camelCase`                                         |
| `build.zig`/`build.zig.zon`                   | Zig type-rule file naming, `src/main.zig`/`src/lib.zig` entries                                                  |

An override applies only when its detection signal is present in that partition - a plain
TypeScript library answers to `kebab-case.ts`, while the same repository's React partition
answers to `PascalCase.tsx` components.

## Language-Idiomatic Code Division

Code division - how declarations, abstractions, implementations, and wiring are distributed
across files and directories - follows distinct idioms in each language.

Porting one language's file-splitting or prefix habits into another is a structural and
naming finding.

- **One public top-level type per file (Java, C#, PHP PSR-4)** - Java enforces one public
  top-level type per `.java` file matching the type name, PHP PSR-4 requires one class,
  interface, trait, or enum per `.php` file matching its autoloaded path, and C# convention
  places each public class, interface, struct, enum, or record group in its own `PascalCase.cs`
  file. Co-locating an interface and its implementation (such as `IRevocationStore` and
  `NullRevocationStore` in `IRevocationStore.cs`) or bundling helper classes, enums, and
  exceptions into a service file obscures discoverability.
- **Module-level cohesion (Python, Go, Rust)** - Python modules (`order_repository.py`), Go
  packages (`internal/service`), and Rust modules (`src/repository.rs`) group closely related
  types and functions in a single file (`OrderRepository` protocol beside
  `InMemoryOrderRepository`) without forcing one-class-per-file fragmentation.
- **Interface, abstract class, and implementation division**:
  - **Java**: Interfaces wear the domain noun (`OrderService`, `OrderRepository`) and concrete
    classes name the strategy or default (`DefaultOrderService`, `InMemoryOrderRepository`,
    `JpaOrderRepository`). When only one implementation exists and no seam is needed, Spring
    Boot idioms allow a concrete `@Service` class (`OrderService`) directly.
  - **C#**: Interfaces carry the `I` prefix (`IOrderService`, `IOrderRepository`) and the
    primary implementation uses the unadorned noun (`OrderService`, `OrderRepository`), while
    shared partial behavior across implementations uses an `abstract class` (`DbEngineBase` or
    framework `ControllerBase`).
  - **Go**: Interfaces are defined in the consuming package (`type Repository interface` inside
    `internal/service`) rather than exported preemptively from the producer package.
  - **Rust**: Traits (`pub trait OrderRepository: Send + Sync`) and their implementations sit in
    the domain/repository module, while `src/lib.rs` exports `build_app()` so integration tests
    in `tests/` drive the router without opening a socket.
  - **Free Pascal and Delphi**: Each unit file separates public contracts in the `interface`
    section from private helpers and method bodies in the `implementation` section. Constructors
    use `Create`, so domain creation methods on services use `CreateOrder` to avoid shadowing
    `TObject.Create`.
  - **C++20**: Public declarations live under `include/<project>/` (`.hpp` with `#pragma once`),
    definitions live in mirroring paths under `src/` (`.cpp`), and `CMakeLists.txt` compiles the
    core into a library target (`order_core`) linked by both the executable and the test binary.
- **Cross-language contamination checks**:
  - C# code using Delphi/Pascal enum-member prefixes (`psNew`, `psConnected`), type-letter
    method suffixes (`ValueI`, `ValueB`), or unit-style catch-all classes (`Misc`, `RedisMain`)
    is flagged as ported-idiom drift.
  - TypeScript or Java interfaces prefixed with `I` (`IOrderService`) or Python classes split
    one-per-file with Java-style `*Impl` suffixes are flagged when no project standard mandates
    them.
  - Static endpoint-registration classes in ASP.NET Core Minimal APIs named `*Controller`
    (when they do not inherit from `ControllerBase`) misstate the framework pattern - consistent
    `*Endpoints` or `*Handler` naming is expected.

## Canonical Stack Fixtures

All eleven reference fixtures model the same order-management HTTP API (`POST /orders` and
`GET /orders/{id}`) so directory layouts, file boundaries, and identifier conventions can be
compared directly across stacks.

The fixtures deliberately cover the service shape of each stack, and non-service shapes of the
same languages - SPAs, Electron desktops, CLI tools, library packages, workspace layouts, and
assembly partitions - carry their conventions in the per-stack digests under
`references/stacks/` rather than as parallel fixtures here.

### 1. Python 3.10+ (FastAPI)

Uses a `src/order_app/` package layout (`pyproject.toml` with `where = ["src"]`), `Protocol`
for structural repository typing, Pydantic `BaseModel` schemas in `api/schemas.py`, `Depends`
wiring in `api/dependencies.py`, and `@app.exception_handler` in `main.py`.

```
order-app/
├── pyproject.toml
├── README.md
├── .gitignore
├── src/
│   └── order_app/
│       ├── __init__.py
│       ├── __main__.py
│       ├── main.py
│       ├── config.py
│       ├── exceptions.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   ├── schemas.py
│       │   └── dependencies.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── order.py
│       │   └── order_status.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── order_service.py
│       └── repositories/
│           ├── __init__.py
│           └── order_repository.py
└── tests/
    ├── conftest.py
    ├── test_orders_api.py
    └── services/
        └── test_order_service.py
```

Key Python conventions verified from this fixture:

- Package directory uses `snake_case` (`src/order_app/`) while distribution name in
  `pyproject.toml` uses `kebab-case` (`name = "order-app"`).
- `OrderStatus(str, Enum)` uses `UPPER_SNAKE_CASE` members (`PENDING`, `PAID`, `CANCELLED`),
  `@dataclass class Order` and `OrderRepository(Protocol)` use `PascalCase`, and private
  attributes use a leading underscore (`self._repository`, `self._orders`).
- Domain exceptions end with `Error` (`OrderNotFoundError`), matching Python standard-library
  exception naming rather than Java/C# `*Exception`.

### 2. Java 17+ (Maven And Spring Boot 3)

Uses the Maven standard directory layout (`src/main/java`, `src/main/resources`,
`src/test/java`) with reverse-domain package path `com/example/orderapp/`, Java 17 `record`
types for immutable domain records and DTOs, and `@RestControllerAdvice` returning RFC 9457
`ProblemDetail`.

```
order-app/
├── pom.xml
├── README.md
├── .gitignore
└── src/
    ├── main/
    │   ├── java/
    │   │   └── com/example/orderapp/
    │   │       ├── OrderApplication.java
    │   │       ├── config/
    │   │       │   └── AppConfig.java
    │   │       ├── api/
    │   │       │   ├── OrderController.java
    │   │       │   ├── GlobalExceptionHandler.java
    │   │       │   └── dto/
    │   │       │       ├── CreateOrderRequest.java
    │   │       │       └── OrderResponse.java
    │   │       ├── domain/
    │   │       │   ├── Order.java
    │   │       │   ├── OrderStatus.java
    │   │       │   └── OrderNotFoundException.java
    │   │       ├── service/
    │   │       │   ├── OrderService.java
    │   │       │   └── DefaultOrderService.java
    │   │       └── repository/
    │   │           ├── OrderRepository.java
    │   │           └── InMemoryOrderRepository.java
    │   └── resources/
    │       ├── application.yml
    │       └── db/migration/
    │           └── V1__create_orders_table.sql
    └── test/
        └── java/
            └── com/example/orderapp/service/
                └── OrderServiceTest.java
```

Key Java conventions verified from this fixture:

- Every directory segment under `src/main/java/` matches the `package` declaration exactly, and
  every public top-level `class`, `interface`, `enum`, or `record` lives in its own
  `PascalCase.java` file.
- Package names are singular lowercase nouns (`api`, `api.dto`, `config`, `domain`, `service`,
  `repository`).
- When an interface has a single default implementation, pair `OrderService` with
  `DefaultOrderService` (or use a concrete `@Service class OrderService` when no seam is
  needed), and name technology-specific adapters by their backing store
  (`InMemoryOrderRepository`, `JpaOrderRepository`).

### 3. C# 8+ (.NET Solution And ASP.NET Core)

Uses `Directory.Build.props` at the solution root to share `TargetFramework`, `LangVersion`, and
`<Nullable>enable</Nullable>`, and separates Clean Architecture layers into distinct `.csproj`
projects so compile-time `<ProjectReference>` edges enforce dependency direction (`Application`
and `Infrastructure` depend on `Domain`, and `Api` is the composition root).

```
OrderApp/
├── OrderApp.sln
├── Directory.Build.props
├── .editorconfig
├── .gitignore
├── src/
│   ├── OrderApp.Api/
│   │   ├── OrderApp.Api.csproj
│   │   ├── Program.cs
│   │   ├── Startup.cs
│   │   ├── appsettings.json
│   │   ├── Controllers/
│   │   │   └── OrdersController.cs
│   │   ├── Contracts/
│   │   │   ├── CreateOrderRequest.cs
│   │   │   └── OrderResponse.cs
│   │   └── Middleware/
│   │       └── ExceptionHandlingMiddleware.cs
│   ├── OrderApp.Application/
│   │   ├── OrderApp.Application.csproj
│   │   ├── Interfaces/
│   │   │   └── IOrderService.cs
│   │   └── Services/
│   │       └── OrderService.cs
│   ├── OrderApp.Domain/
│   │   ├── OrderApp.Domain.csproj
│   │   ├── Entities/
│   │   │   └── Order.cs
│   │   ├── Enums/
│   │   │   └── OrderStatus.cs
│   │   ├── Exceptions/
│   │   │   └── OrderNotFoundException.cs
│   │   └── Interfaces/
│   │       └── IOrderRepository.cs
│   └── OrderApp.Infrastructure/
│       ├── OrderApp.Infrastructure.csproj
│       ├── Persistence/
│       │   └── OrderDbContext.cs
│       └── Repositories/
│           └── InMemoryOrderRepository.cs
└── tests/
    └── OrderApp.Application.Tests/
        ├── OrderApp.Application.Tests.csproj
        └── OrderServiceTests.cs
```

Key C# and .NET conventions verified from this fixture:

- Directories and namespaces use full `PascalCase` words (`Application`, `Infrastructure`,
  `Controllers`, `Contracts`, `Middleware`, `Interfaces`, `Services`, `Entities`, `Enums`,
  `Exceptions`, `Persistence`, `Repositories`), and namespaces mirror folder paths
  (`OrderApp.Domain.Entities`).
- Even in a single-project ASP.NET Core service organized by feature or technical folder, folder
  and namespace names avoid arbitrary abbreviations (`Configuration` over `Config`,
  `Authentication` over `Auth`, `Documentation` over `Docs`, `Application` or `Operations` over
  `App`) unless an explicit project standard documents the short names.
- One public top-level type per `.cs` file: `IOrderRepository.cs` holds only the interface, and
  `InMemoryOrderRepository.cs` holds the implementation.
- Interfaces start with `I` (`IOrderService`), async methods end with `Async` (`CreateAsync`,
  `GetAsync`), enum members use unadorned `PascalCase` (`Pending`, `Paid`, `Cancelled`), private
  fields use `_camelCase` (`_repository`, `_orders`), and C# keyword aliases (`bool`, `int`,
  `string`) are used instead of BCL struct names (`Boolean`, `Int32`, `String`).

### 4. PHP 8.3 (Slim 4 And PSR-4)

Maps `OrderApp\` to `src/` and `OrderApp\Tests\` to `tests/` via `composer.json` PSR-4
autoloading, keeps the web entry point isolated in `public/index.php`, and uses external
persistence (`var/orders.sqlite`) because PHP's shared-nothing execution model discards
in-memory state between requests.

```
order-app/
├── composer.json
├── public/
│   └── index.php
├── var/
├── src/
│   ├── Domain/
│   │   ├── Order.php
│   │   ├── OrderStatus.php
│   │   └── OrderNotFoundException.php
│   ├── Repository/
│   │   ├── OrderRepository.php
│   │   └── SqliteOrderRepository.php
│   ├── Service/
│   │   └── OrderService.php
│   └── Http/
│       └── OrderController.php
└── tests/
    └── OrderServiceTest.php
```

Key PHP conventions verified from this fixture:

- Every file starts with `declare(strict_types=1);` and omits the closing `?>` tag per PSR-12.
- Directory names under `src/` are `PascalCase` singular nouns (`Domain`, `Repository`,
  `Service`, `Http`) matching namespace segments (`OrderApp\Domain`), and each `.php` file
  defines exactly one `final readonly class`, `final class`, `interface`, or backed `enum`.
- Interfaces use the domain noun without an `I` prefix (`OrderRepository`), and enum cases use
  `PascalCase` (`OrderStatus::Pending`).

### 5. Rust (axum 0.8, Edition 2021)

Splits `src/lib.rs` (exporting `pub fn build_app() -> Router`) from a thin `src/main.rs` so
integration tests under `tests/orders_api.rs` exercise the full router via `tower::ServiceExt`
without binding a network port.

```
order-app/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── lib.rs
│   ├── api.rs
│   ├── domain.rs
│   ├── error.rs
│   ├── repository.rs
│   └── service.rs
└── tests/
    └── orders_api.rs
```

Key Rust conventions verified from this fixture:

- Crate name in `Cargo.toml` uses `kebab-case` (`order-app`), while module files and crate
  import identifiers use `snake_case` (`order_app`, `api.rs`, `domain.rs`).
- Wire-serialization casing (`#[serde(rename_all = "camelCase")]`) is declared on the struct or
  enum, keeping Rust fields in idiomatic `snake_case` (`customer_email`, `total_cents`).
- Domain errors use a typed `enum AppError` deriving `thiserror::Error` and implementing
  `IntoResponse` in `src/error.rs`.

### 6. Go 1.22+ (Standard Library `net/http`)

Uses `cmd/orderapp/main.go` for the binary entry point and places non-exported application
packages under `internal/` so the Go compiler enforces package privacy.

```
order-app/
├── go.mod
├── go.sum
├── cmd/
│   └── orderapp/
│       └── main.go
└── internal/
    ├── domain/
    │   └── order.go
    ├── repository/
    │   └── memory.go
    ├── service/
    │   └── order_service.go
    └── api/
        ├── handler.go
        └── handler_test.go
```

Key Go conventions verified from this fixture:

- Package names are short, lowercase, single-word nouns (`domain`, `repository`, `service`,
  `api`), and source files use `snake_case.go` with co-located `*_test.go` files.
- The `Repository` interface is defined in `internal/service/order_service.go` where it is
  consumed, while `internal/repository/memory.go` exports the concrete `Memory` struct and
  `NewMemory()` constructor.
- Exported identifiers use `PascalCase` with uniform initialism casing (`ID`, `URL`, `HTTP`,
  `writeJSON`), and domain errors are package-level sentinel values (`ErrOrderNotFound`,
  `ErrInvalidOrder`) checked via `errors.Is`.

### 7. JavaScript (ES2022 Modules, Node 20+, Express 5)

Separates the HTTP listener (`src/server.js`) from the Express application factory
(`src/app.js`) so `node:test` suites in `test/orders.test.js` can bind an ephemeral port (`0`).

```
order-app/
├── package.json
├── src/
│   ├── server.js
│   ├── app.js
│   ├── errors.js
│   ├── domain/
│   │   └── order.js
│   ├── repositories/
│   │   └── in-memory-order-repository.js
│   ├── services/
│   │   └── order-service.js
│   └── routes/
│       └── orders.js
└── test/
    └── orders.test.js
```

Key JavaScript conventions verified from this fixture:

- Source files use `kebab-case.js` (`in-memory-order-repository.js`, `order-service.js`),
  classes use `PascalCase` (`OrderService`), factory functions use `camelCase` (`createOrder`,
  `createApp`), and frozen constant objects use `UPPER_SNAKE_CASE` keys (`OrderStatus.PENDING`).
- Private class state uses native ES2022 `#private` fields (`#orders`, `#repository`).

### 8. TypeScript 5.x (Fastify 5, Zod, Vitest)

Follows the same `kebab-case.ts` module layout as Node.js while adding explicit `interface`
contracts (`src/repositories/order-repository.ts`) and Zod boundary validation in the route
layer (`CreateOrderBody.parse`).

```
order-app/
├── package.json
├── tsconfig.json
├── src/
│   ├── server.ts
│   ├── app.ts
│   ├── errors.ts
│   ├── domain/
│   │   └── order.ts
│   ├── repositories/
│   │   ├── order-repository.ts
│   │   └── in-memory-order-repository.ts
│   ├── services/
│   │   └── order-service.ts
│   └── routes/
│       └── orders.ts
└── test/
    └── orders.test.ts
```

Key TypeScript conventions verified from this fixture:

- Interfaces (`Order`, `OrderRepository`) use `PascalCase` without a C#-style `I` prefix, and
  type-only imports use `import type` (`verbatimModuleSyntax: true`).
- Under `moduleResolution: "NodeNext"`, relative imports carry the `.js` extension even inside
  `.ts` source files.

### 9. Free Pascal 3.2+ (`fcl-web` And `fpcunit`)

Places the program entry in `orderapp.lpr` at the root, unit files in `src/` with lowercase
filenames matching each `unit` declaration (`unit orderdomain;` in `src/orderdomain.pas`), and
`fpcunit` test runners under `tests/`.

```
order-app/
├── orderapp.lpr
├── src/
│   ├── ordererrors.pas
│   ├── orderdomain.pas
│   ├── orderrepository.pas
│   ├── orderservice.pas
│   └── orderapi.pas
└── tests/
    ├── orderservicetests.lpr
    └── testorderservice.pas
```

Key Free Pascal conventions verified from this fixture:

- Type prefixes distinguish roles: `T` for classes, records, and enums (`TOrder`,
  `TOrderStatus`, `TOrderService`), `I` for reference-counted interfaces (`IOrderRepository`),
  and `E` for exceptions (`EOrderNotFound`).
- Private fields use the `F` prefix (`FOrders`, `FRepository`), parameters use the `A` prefix
  (`ACustomerEmail`, `AOrder`), and enum values carry a lowercase type-initials prefix
  (`osPending`, `osPaid`, `osCancelled`) because standard Pascal enums share unit scope.
- Service creation methods use `CreateOrder` so they do not collide with the `Create`
  constructor inherited from `TObject`.

### 10. Delphi 11/12 (Horse And DUnitX)

Uses dotted namespace unit names (`OrderApp.Domain.Order.pas`,
`OrderApp.Services.OrderService.pas`) paired with `OrderApp.dpr` and `OrderApp.dproj`.

```
OrderApp/
├── OrderApp.dpr
├── OrderApp.dproj
├── src/
│   ├── OrderApp.Domain.Order.pas
│   ├── OrderApp.Domain.Errors.pas
│   ├── OrderApp.Repositories.Contracts.pas
│   ├── OrderApp.Repositories.InMemory.pas
│   ├── OrderApp.Services.OrderService.pas
│   └── OrderApp.Api.Routes.pas
└── tests/
    ├── OrderAppTests.dpr
    └── OrderApp.Tests.OrderService.pas
```

Key Delphi conventions verified from this fixture:

- Unit filenames match the dotted `unit` identifier (`unit OrderApp.Repositories.Contracts;`),
  grouping layers by dotted prefix (`OrderApp.Domain.*`, `OrderApp.Repositories.*`,
  `OrderApp.Services.*`, `OrderApp.Api.*`).
- Interfaces carry a GUID (`['{...}']`) and `I` prefix, classes/records carry `T`, exceptions
  carry `E`, fields carry `F`, and parameters carry `A`.

### 11. C++20 (CMake, `include/` And `src/` Split, Catch2)

Separates public headers under `include/order_app/` from implementation files under `src/` and
builds a static library target (`order_core`) in `CMakeLists.txt` shared by both the
`order_app` executable and the `order_tests` Catch2 binary.

```
order-app/
├── CMakeLists.txt
├── include/
│   └── order_app/
│       ├── domain/
│       │   ├── order.hpp
│       │   └── errors.hpp
│       ├── repository/
│       │   ├── order_repository.hpp
│       │   └── in_memory_order_repository.hpp
│       ├── service/
│       │   └── order_service.hpp
│       └── api/
│           └── routes.hpp
├── src/
│   ├── main.cpp
│   ├── domain/
│   │   └── order.cpp
│   ├── repository/
│   │   └── in_memory_order_repository.cpp
│   ├── service/
│   │   └── order_service.cpp
│   └── api/
│       └── routes.cpp
└── tests/
    └── order_service_test.cpp
```

Key C++20 conventions verified from this fixture:

- Header and source filenames use `snake_case.hpp` and `snake_case.cpp`, nested namespaces
  mirror the header path (`namespace order_app::domain`), and closing braces carry a
  `// namespace ...` comment.
- Types (`Order`, `OrderRepository`, `InMemoryOrderRepository`) use `PascalCase`, functions and
  methods (`register_routes`, `to_string`) use `snake_case`, `enum class` values use
  `snake_case` (`OrderStatus::pending`), and private data members use a trailing underscore
  (`mutex_`, `orders_`, `repository_`).

## Fallback For Unlisted Technologies

Lens audits any software or documentation repository, including languages, frameworks, DSLs,
and project types not listed in the matrices above.

When a partition uses a technology not covered by a bundled digest, matrix row, or
`references/stacks/` file, establish its governing naming and layout baseline in this order
(applied per partition in polyglot repositories):

1. **Project-declared standards** - inspect `AGENTS.md`, `CONTRIBUTING.md`, `STANDARDS.md`,
   `docs/standards/`, `.editorconfig`, and linter/formatter configs (`.clang-format`,
   `.rubocop.yml`, `checkstyle.xml`, `detekt.yml`, `swiftlint.yml`, `flake8`/`ruff.toml`) for
   explicit rules.
2. **Ecosystem and compiler/linter conventions** - apply the language's standard-library and
   official toolchain conventions (for example `snake_case` files and `PascalCase` modules in
   Elixir/Ruby, `PascalCase` modules in Haskell/OCaml/F#, `snake_case` in Zig/Nim, `camelCase`
   / `PascalCase` in Swift/Kotlin/Dart).
3. **Authoritative live source lookup** - when web fetch is permitted, consult the official
   language style guide or framework documentation and record its URL in the `References`
   section.
4. **Internal consistency census** - measure the dominant directory, file, and identifier
   patterns across the component itself via `scripts/scan-structure.py` and flag unexplained
   within-component deviations as `Established`-tier consistency findings.

Record which baseline governed the evaluation in `Auditing Methodology` and `Structure
Conformance`, and never invent an arbitrary rule when neither the ecosystem nor the project
defines one.

In-code identifier naming quality is governed by `assessment/code-style.md`, which uses the
naming matrices here as its T3 yardstick alongside `references/language-conventions.md`.
