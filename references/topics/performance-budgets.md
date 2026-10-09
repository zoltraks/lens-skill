# Performance Budget Baseline

## Purpose

> **Scope:** Checkable constraints for performance budgets, their measurement discipline, and
> CI enforcement across frontend, service, CLI, and database surfaces
> **Key items:** budget tables by surface, percentile discipline, regression gates, detection
> signals

This file distills the Core Web Vitals, Lighthouse CI, k6, and hyperfine sources listed in
`references/source-catalog.md` into constraints an audit can verify from repository source.

Snapshot date: 2026-10-09.

Feeds `assessment/baseline-conformance.md` and `assessment/nfr-review.md`.

## Measurement Discipline

From https://web.dev/vitals/ and https://k6.io/docs/.

- Budgets are enforced in CI, not documented aspirationally: a regression fails the build.
  A budget file with no consuming pipeline step is an unenforced declaration.
- Tail percentiles (p95/p99) are the unit of account. Mean or median budgets hide the tail
  latency users actually hit.
- Cold start is part of the contract for serverless handlers and CLIs: first-invocation
  latency counts, not only warm-loop numbers.
- Memory budgets cover RSS and heap together, with a soak window (a 24-hour leak check or a
  declared equivalent) rather than a snapshot.
- Synthetic runs approximate production-like conditions: a benchmark that cannot plausibly
  represent the deployed environment is weaker evidence and the audit says so.

## Surface Budgets

Representative thresholds widely adopted per surface - a project's own declared budget
overrides these, and the audit checks presence and enforcement before magnitude:

| Surface         | Representative budgets                                                                   |
|-----------------|------------------------------------------------------------------------------------------|
| Frontend        | LCP <= 2.5 s, INP <= 200 ms, CLS <= 0.1, TTFB <= 800 ms, JS <= 200 KB gzipped            |
| Frontend assets | CSS <= 50 KB gzipped, total transfer <= 500 KB, third-party requests <= 10               |
| HTTP API        | p99 <= 100 ms simple read, <= 300 ms complex read, <= 500 ms write, error rate <= 0.1%   |
| API operations  | Cold start <= 1 s, connection-pool utilization <= 80%, RSS <= 100 MB idle                |
| CLI             | Cold start <= 500 ms, warm <= 100 ms, single-command p99 <= 2 s, binary <= 20-30 MB      |
| Database        | p99 <= 10 ms simple query, <= 100 ms complex, <= 20 ms single-row write, acquire <= 5 ms |

## Detection Signals

| Signal in repository                               | Inferred posture                   |
|----------------------------------------------------|------------------------------------|
| `lighthouse`/`lighthouse-ci` config or budget file | Frontend budgets enforced          |
| `k6`, `artillery`, `wrk` scripts or CI steps       | Backend load testing in place      |
| `hyperfine` invocations or benchmark scripts       | CLI benchmarking in place          |
| Bundle-analyzer tooling in the build               | Bundle size tracked                |
| Latency assertions in integration tests            | Database budgets checked per query |
| None of the above on a production-bound subject    | No declared performance contract   |

## Regression Comparison

- A regression gate compares against the baseline branch, not absolute numbers alone: a
  threshold such as "no more than 10% slower than main" catches drift the fixed budgets miss.
- Bundle-size budgets pair with deterministic filenames or an analyzer report, so the compared
  artifact is the one that ships.
- An absent performance posture is an observation, not a defect: report the missing contract
  where the subject's role makes latency or footprint load-bearing, and mark it
  `NOT ASSESSED` where budgets were never claimed.

## Live Check

When web fetch is available, spot-check the current Core Web Vitals thresholds against
https://web.dev/vitals/ before citing the defaults above.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
