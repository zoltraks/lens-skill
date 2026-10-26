# Execution Isolation

## Purpose

> **Scope:** Session-proven procedure for commissioned non-mutating execution under the
> `executed-readonly` and `executed-commands` evidence modes
> **Key items:** environment census, isolation recipe, bounded inputs, proxy labeling,
> adaptation harnesses, failure-output mining, result triage

This file defines how commissioned checks run without touching the audited tree and how their
results become reliable evidence.

Snapshot date: 2026-10-27.

No external sources.

The rules are distilled from audit sessions that ran commissioned builds and test suites.

Feeds the evidence-mode paragraphs and the Verification Plan in `process/audit-workflow.md`,
and the `EXECUTED` record fields in `references/evidence-schema.md`.

Every rule keeps the evidence-mode contract: the subject is never deployed, mutated, or
connected to live systems, and nothing runs that the user did not commission.

## Pre-Flight Environment Census

Before the verification matrix is built, record what the environment can actually run.

- Enumerate the relevant toolchains: SDK and runtime listings (`dotnet --list-sdks`,
  `java -version`, `node --version`, `rustc --version`), compiler and analyzer versions,
  package-manager caches, and whether the network is reachable.
- The verification matrix selects only checks the census says can run.
- A toolchain the subject declares but the environment lacks is recorded in `limits` or
  `unavailable` on the evidence record - it is an audit limitation, never a subject defect.
- Record the host platform when it differs from the subject's declared targets, since
  platform differences shape which results are meaningful.

## Isolation Recipe

Commissioned commands run against a copy, never against the audited tree.

- Copy the audited tree into the audit's work or scratch area and run every commissioned
  command inside the copy.
- Redirect tool caches, package downloads, build output, and test artifacts into the copy so
  nothing writes back into the audited tree.
- Record the isolation root in the evidence record's `procedure` block.
- When the audit finishes, the audited tree's `git status --porcelain` output must match the
  intake snapshot - any delta beyond audit artifacts is reported.

## Bounded Inputs

Respect the environment's limits instead of working around them.

- No tool, package, or dependency is installed or fetched unless the user commissioned it.
- When a restore or resolution fails because packages are unavailable offline, record the
  missing inputs as an environment limitation on the evidence record, not as a defect of the
  subject.
- A partially completed run still produces `EXECUTED` evidence: the record carries what ran,
  what failed to provision, and the `limits` of what the result can establish.

## Proxy-Verification Labeling

A check that runs against a substitute target proves less than the declared target.

- When the declared toolchain is unavailable, a commissioned check may run against an
  available substitute - a different framework profile, SDK band, or analyzer set - but the
  result is labeled proxy evidence.
- The evidence record states what the proxy cannot establish: compiling under a modern
  framework profile never verifies the legacy targets the subject also declares.
- Findings resting on proxy evidence name the proxy in their evidence and `limits`, so a
  reader cannot mistake a substitute verification for a target one.

## Adaptation Harnesses

An audit-created shim is audit tooling, never subject source.

- A compatibility shim, adapter, or stripped fixture that makes a commissioned check run
  against available dependencies is an audit artifact - for example a bridge that maps a
  test framework's assertion surface onto a locally available version.
- The harness and its delta from subject source are disclosed in the evidence record.
- Results produced through a harness are labeled harness-assisted: they verify behavior under
  the adaptation, never the subject's unmodified build.
- Harness files live in the isolation copy or the audit work area and never land in the
  audited tree.

## Failure-Output Mining

A non-zero exit status still produces evidence.

- Capture the emitted diagnostic set - compiler warnings, analyzer diagnostics, failed test
  names - as retained output with a sanitized artifact path or digest.
- A build that fails still yields its warning inventory; a suite that fails still yields its
  per-test results.
- `FAIL` and `ERROR` describe the runner outcome per `principles/evaluation-rules.md` - the
  mined diagnostics become `Observation` rows that feed findings on their own evidence.

## Result Triage

Every failing executed result is classified before it becomes a finding or a limitation.

| Class                    | Meaning                                                           | Lands as                                |
|--------------------------|-------------------------------------------------------------------|-----------------------------------------|
| `subject defect`         | The product code produced the failure                             | A `FND-XXX` finding                     |
| `harness defect`         | Test, fixture, or harness code produced the failure               | A test-quality finding or a suite note  |
| `environment limitation` | Toolchain, platform, or package availability produced the failure | A `limits` entry and a Limitations row  |
| `inconclusive`           | The failure cannot be attributed from the output                  | An `UNKNOWN` and a verification request |

Record the classification basis - the diagnostic text or reproduced mechanism - in the
evidence record.

The class decides where the result lands: an environment failure is never reported as a
subject defect, and a subject defect is never dismissed as an environment quirk.

## Live Check

These rules are session-derived and not backed by a live source.

No live check applies.

The file updates when audit sessions produce new execution-isolation patterns.
