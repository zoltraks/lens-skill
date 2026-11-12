# Check Surface

## Purpose

> **Scope:** Enumerating a subject's declared verification surface, proposing the commissioned
> command set, bounding claims to the executed scope, and the verification-pass discipline
>
> **Key items:** check-surface census, per-ecosystem checklists, commission proposal,
> scope-bounded claims, double and triple verification, verbatim commands

This file is the reference for what an executed-capable audit offers to run and how its results
bound the claims they support.

Load it whenever an audit selects `executed-readonly` or `executed-commands`,
when the Verification Plan in `process/audit-workflow/evidence-gathering.md` is built,
and when executed results are written into evidence.

## The Check-Surface Census

Before the commission question is asked, enumerate every verification the subject itself declares.

A declared check is one the repository names in a runnable form: a manifest script, a pipeline
step, a Makefile or task-runner target, a documented gate in the project's own verification
instructions, or a configured threshold with a matching runner.

The census never invents checks - it lists what the subject declares, then classifies each entry
by what it would establish for the audit.

| Ecosystem signal                        | Enumerate                                                                                                            |
|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| `package.json` scripts                  | Every `test`, `coverage`, `lint`, `format`, `typecheck`, `build`, `audit`, packaging, and `e2e` script by exact name |
| Lockfile plus manifest                  | The ecosystem advisory sweep (`npm audit`, `pip-audit`, `cargo audit`, `bundle audit`)                               |
| Coverage or threshold configuration     | The configured coverage run and its declared floors                                                                  |
| Packaging manifests                     | The declared packaging or distribution build and an artifact content listing                                         |
| CI configuration                        | Each pipeline step that names a runnable command                                                                     |
| `Makefile`, `justfile`, task runners    | Every verification-flavored target                                                                                   |
| Documented gates in the project's rules | Every gate the subject's own testing or workflow documents declare                                                   |
| Service-worker or deploy manifests      | Install or post-deploy verification the subject declares                                                             |

Each census entry records the literal command, the manifest line that declares it,
what a pass would establish, and which readiness gate it feeds when the audit's purpose
includes readiness.

## The Commission Proposal

Under `executed-readonly` or `executed-commands` the census becomes the proposed commission set.

The free-text commission follow-up presents the enumerated set with the readiness-relevant
entries marked, and the user confirms, narrows, or replaces it.

An answer of "all" or an empty answer commissions the proposed set -
the auditor never silently narrows a commissioned executed-commands mode back to a default loop.

Under `source-only` the same census still runs - it feeds the `Not run` ledger rows and the
Known Limitations section, because the declared-but-unrun surface is the audit's coverage bound.

An entry the host cannot complete per the environment census in
`references/topics/execution-isolation.md` is recorded as unavailable before it is offered.

## Scope-Bounded Claims

A pass result supports only the scope the command itself declares.

- An executed-evidence row records the literal command exactly as invoked, its declared scope
  (script glob, suite selector, directory argument), and the artifact path it ran against.
- A claim never outgrows that scope: `format` covering a manifest's glob supports "formatted
  per the declared check", never "all files formatted" - the whole-tree claim needs a
  whole-tree check or a `limits` entry naming the unrun remainder.
- A script name is recorded verbatim and exists in the manifest - a row citing a command the
  project does not declare is a report defect, never evidence.
- A `Pass` observed on a copy, harness, or proxy carries its isolation label per
  `references/topics/execution-isolation.md`.

## Verification Passes

Claims publish through independent checks, not through the reading that produced them.

- **Double check** - every material claim clears a second derivation before it publishes:
  census counts re-derive from a mechanical count, a cited behavior re-reads the cited code,
  and an executed result re-runs or re-parses its recorded output.
- **Triple check** - a claim that decides the readiness state, the headline score, or a
  `Critical` or `High` finding adds a hostile third pass: an attempt to falsify the claim
  from the same evidence, covering counter-examples the first two passes could miss.
- **Mechanical numbers** - a count in the report comes from an executed count or scan output;
  an estimate writes `~` or `about` and never dresses as an exact figure.
- **Declared dependencies** - the dependency inventory derives from the manifest and lockfile
  together; a declared entry missing from the SBOM table is a report defect.
- **Claim-channel agreement** - a `Pass` claim cites the channel that produced it
  (inspected, executed, reported), and an executed claim cites a command that exists.

A claim that fails a pass is corrected before publication - the fix lands in the evidence
record, never only in the prose around it.

## Anti-Slop Discipline

The failure modes this file exists to prevent:

- Recording a plausible command name for a check that was run differently or not at all.
- Generalizing a scoped check's `Pass` into a whole-tree or whole-gate claim.
- Grading a declared-but-unrun gate as satisfied because nothing contradicted it.
- Treating a commissioned-commands audit's disclaimers as closure for the verdict -
  an unrun material gate is a `PENDING EVIDENCE` input, not a resolved one.
- Publishing counts, scores, or verdicts that no pass re-derived.

## Relation To Other References

`references/topics/execution-isolation.md` owns how commissioned commands run and triage.

`references/evidence-schema.md` owns the evidence record fields these rules fill.

`process/readiness-scoring.md` owns the readiness states and ceilings the unresolved entries feed.
