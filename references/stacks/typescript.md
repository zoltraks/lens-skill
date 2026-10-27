# TypeScript And Frontend Toolchain Baseline

## Purpose

> **Scope:** Checkable constraints for TypeScript projects and the common frontend toolchain
> (Vite, Vitest, Playwright, Jest, Testing Library, Zustand)
> **Key items:** strictness flags, compiler options, test-runner configuration, lint tiers,
> state-store conventions

This file distills the TypeScript handbook, TSConfig reference, typescript-eslint, Vitest,
Playwright, Testing Library, Vite, Zustand, and Jest documentation listed in
`references/source-catalog.md` into constraints an audit can verify from repository source.

Snapshot date: 2026-10-27.

Feeds `assessment/code-quality.md`, `assessment/testing-review.md`,
`assessment/best-practices.md`, and `assessment/baseline-conformance.md` for TypeScript and
browser-toolchain subjects.

## Compiler Strictness

From the TypeScript handbook (https://www.typescriptlang.org/docs/handbook/intro.html) and the
TSConfig reference (https://www.typescriptlang.org/tsconfig).

- `strict: true` is the conformance floor for new code. It bundles `strictNullChecks`,
  `noImplicitAny`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`,
  `noImplicitThis`, `useUnknownInCatchVariables`, and `alwaysStrict`.
- A project that sets `strict: false` or disables individual strict flags records a deliberate
  relaxation. Each disabled flag is a code-quality observation.
- `noUncheckedIndexedAccess` makes index signatures and array indexing return `T | undefined`.
  Its absence on data-heavy code is a robustness observation.
- `exactOptionalPropertyTypes` distinguishes `?:` from `| undefined`. Relevant when option
  objects cross API boundaries.
- `skipLibCheck: true` is conventional and not a defect. It silences third-party `.d.ts`
  errors only.
- `target`/`lib`/`module` must be consistent with the declared runtime floor. ES5-era targets
  in a modern-stack project are a drift observation.
- `verbatimModuleSyntax` or `importsNotUsedAsValues` discipline matters for bundlers that
  erase imports. Type-only imports should use `import type` when the toolchain erases.

## Lint Tiers, Naming, And Layout

From https://typescript-eslint.io/rules/ and
https://typescript-eslint.io/rules/naming-convention/.

- Naming and file layout: module files use `kebab-case.ts` (`order-repository.ts`,
  `in-memory-order-repository.ts`, `order-service.ts`), test files use `*.test.ts` or
  `*.spec.ts`, classes, interfaces, type aliases, and enums use `PascalCase` without a
  C#-style `I` prefix on interfaces (`OrderRepository`, not `IOrderRepository`), functions,
  methods, parameters, and properties use `camelCase`, and module-level constants or Zod
  schemas use `UPPER_SNAKE_CASE` or `PascalCase`.
- Code division: services split `src/server.ts` (listener) from `src/app.ts` (`buildApp`
  factory), keep repository interfaces (`order-repository.ts`) separate from concrete adapters
  (`in-memory-order-repository.ts`), and under `moduleResolution: "NodeNext"` write `.js`
  extensions on relative imports inside `.ts` files.
- Role-directory conventions from the maintainer's TypeScript standards: application `src/`
  groups `commands/` or `routes/` (entry actions), `services/` (use cases), `repositories/`
  or `data/` (persistence), `config/` (loading and validation), `types/` (shared contracts),
  `hooks/` and `stores/` (React-adjacent state), `workers/` (off-thread units), and `utils/`
  or `logic/` (pure modules) - a flat `src/` past roughly a dozen files, and files past
  roughly 500 lines, are the review thresholds the standards set.
- Test files use `*.test.ts`/`*.spec.ts` colocated or under a mirroring `test/`/`tests/`
  tree, and e2e suites conventionally live in `e2e/` or `tests/e2e/` with `*.spec.ts` naming
  - a project mixing `*_test.ts`, `*.test.ts`, and `tests-*.ts` across one partition is the
  consistency defect.
- TypeScript project references (composite `tsconfig.json` with `references`) split a
  multi-package build into per-package outputs (`compiler/`, `library/` as siblings with
  their own `tsconfig`), and the root `tsconfig` delegates rather than compiling - a root
  config re-listing every source file of every package defeats the reference model.
- The `recommended` tier is the floor. `recommended-type-checked` adds rules that need type
  information and catches `any` leaks, floating promises, and unsafe assignments.
- Key checkable rules: `no-floating-promises`, `no-misused-promises`,
  `no-unsafe-assignment`/`member-access`/`call`/`return`, `no-explicit-any` (warning tier),
  `consistent-type-imports`, `no-non-null-assertion`.
- A flat `eslint.config.*` that composes `typescript-eslint` configs is the current form.
  `.eslintrc.*` files are legacy but not a defect.
- Type-aware rules require `parserOptions.projectService` or `project` wiring. Their absence
  in a config that claims type-aware linting is a configuration finding.

## Vitest

From https://vitest.dev/guide/ and https://vitest.dev/config/#coverage.

- Test discovery defaults to `**/*.{test,spec}.?(c|m)[jt]s?(x)` patterns. An `include` glob that
  matches nothing yields a silent zero-test pass - census the matched files.
- `coverage.thresholds` (lines/functions/branches/statements) make coverage a gate. Thresholds
  absent from config mean coverage is reported, not enforced.
- `environment: 'node'` is the default. DOM tests need `happy-dom` or `jsdom`.
- `--run` is the CI form. Watch mode in CI scripts is a pipeline finding.

## Playwright And Testing Library

From https://playwright.dev/docs/best-practices and
https://testing-library.com/docs/guiding-principles.

- Playwright best practice: user-facing locators (`getByRole`, `getByLabel`, `getByText`) over
  CSS selectors. `test.describe` grouping. `webServer` config for dev-server lifecycle.
  No `page.waitForTimeout` fixed sleeps (use assertions/waitFor).
- Testing Library's guiding principle is testing the way users interact: queries by role and
  accessible name first, `querySelector` and `container` scraping last.
- Snapshot tests are discouraged for behavioral assertions. Brittle snapshots are a
  test-quality observation.

## Vite

From https://vite.dev/guide/ and https://vite.dev/config/build-options.

- `build.sourcemap` defaults off for production. Enabled sourcemaps ship readable source.
- `build.target` follows the browserslist/baseline floor. Esbuild handles transpilation.
- Dev-server options (`server.port`, `server.proxy`, `server.strictPort`) belong in config,
  not scattered CLI flags.
- `public/` assets are copied verbatim and never processed. Assets needing hashing belong in
  `src/` imports.

## Zustand And Jest

From https://zustand.docs.pmnd.rs/ and https://jestjs.io/docs/configuration.

- Zustand stores are hook factories created by `create`. Mutating state outside `set` breaks
  the subscription contract. Selectors should be memoized or shallow-compared to avoid
  render loops.
- Jest `collectCoverageFrom` defines what coverage counts. `coverageThreshold` enforces gates.
  `testMatch`/`testRegex` misconfiguration produces empty suites the same way Vitest's
  `include` does.
- `ts-jest` versus `babel-jest` versus `esbuild-jest` is a toolchain choice. Duplicate
  transpile paths in one repo are a consistency observation.

## Boundary Validation

From https://zod.dev/ and https://valibot.dev/.

- Types are erased at runtime: data entering over IO (HTTP bodies, env vars, file reads,
  storage) is `unknown` at the boundary and validated into a typed shape with a schema
  library (zod, valibot, typia) - an `as T` cast on inbound data is a trust finding.
- `JSON.parse` returns `any`: unchecked results flowing into typed code defeat the strict
  floor. The schema parse (`schema.parse`) or a validated wrapper is the checkable shape.
- Env var access goes through a validated config object built at startup - scattered
  `process.env.X` reads mean no startup-time validation and late failures.

## Maintainer-Standard Floor

From the maintainer's TypeScript engineering standards.

- The defect floor mirrors the JavaScript base: pinned runtime via `engines`/`.nvmrc`,
  explicit module system, committed lockfile, CI-enforced lint and format, and no floating
  dependency ranges.
- Strictness posture: `strict` (or the documented equivalent flags) enabled in `tsconfig.json`
  is the expected baseline - a project compiling with strictness disabled without a recorded
  reason is a finding.

## Live Check

When web fetch is available, spot-check one strictness flag name against the TSConfig reference
and one Vitest default against its config docs.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
