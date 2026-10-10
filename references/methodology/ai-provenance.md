# AI Provenance Baseline

## Purpose

> **Scope:** Checkable anchors for determining whether a coding agent produced repository
> artifacts - attribution conventions, provenance-document vocabulary, erasure rules, and
> the evidence behind the style-inference ban
> **Key items:** per-tool attribution signatures, commit trailers, bot identities,
> provenance documents, suppression and erasure, detector-research limits, legal context

This file distills the vendor documentation, supply-chain specifications, legal references,
and detection research listed in `references/source-catalog.md` into the anchors an audit
uses to establish code authorship.

Snapshot date: 2026-10-09.

Feeds `assessment/generated-code.md`, the attribution census in
`references/census-commands.md`, and the `Provenance basis` field vocabulary in
`process/report-format/findings-registers.md`.

## The Asymmetry Rule

Agent involvement can be proven: an attribution artifact either exists or it does not.

Human authorship cannot be proven: every attribution mechanism is opt-out, removable, or
rewriteable, so a clean history says only that no agent-attribution evidence was found.

The audit therefore never writes `human-authored` as a conclusion.

The honest negative is `Undetermined` - no agent-attribution evidence observed in the
inspected scope.

## Attribution Signatures

Per-tool conventions for explicit attribution, recorded from vendor documentation and
observed repository output.

| Tool         | Commit trailer                                                               | Author/committer identity                                              | Session and PR artifacts                                                                |
|--------------|------------------------------------------------------------------------------|------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| Claude Code  | `Co-Authored-By: Claude <model> <noreply@anthropic.com>`                     | -                                                                      | `Claude-Session` trailer (remote sessions), `Generated with Claude Code` PR body marker |
| Copilot      | `Co-authored-by: Copilot <copilot@github.com>` (VS Code `git.addAICoAuthor`) | `Copilot`, `copilot-swe-agent[bot]` - commits may be signed `Verified` | `Agent-Logs-Url` trailer                                                                |
| Cursor       | `Made-with: Cursor`                                                          | `cursor[bot]`, `cursoragent@cursor.com`                                | -                                                                                       |
| Devin        | `Co-Authored-By: Devin`                                                      | `devin-ai-integration[bot]`                                            | PR body attribution                                                                     |
| OpenAI Codex | `Co-authored-by: Codex <noreply@openai.com>`                                 | `codex` bot identity per workspace policy                              | -                                                                                       |
| Gemini CLI   | `Co-Authored-By: Gemini`                                                     | `gemini-bot` identity                                                  | -                                                                                       |
| Aider        | `aider (model) <aider@aider.chat>` co-author                                 | -                                                                      | `aider:` subject prefix when attribution enabled                                        |

Signal precedence: an author or committer identity outranks a trailer (trailers survive
squash merges poorly and can be typed by hand), a signed bot commit outranks an unsigned
one (the signature binds identity to the platform), and a repository-internal artifact
outranks a PR-body marker (the PR surface is `Reported` evidence).

Automation identities are not AI attribution: `github-actions[bot]`, `dependabot[bot]`,
`renovate[bot]`, and release bots mark machine-driven changes, not generative authorship.

A trailer or identity names the tool, not the share of work it did - one attributed commit
does not make the repository agent-built.

## Suppression And Erasure

Attribution is opt-out in every major tool: Claude Code's `attribution.commit`/
`attribution.pr` settings (the `includeCoAuthoredBy` form is deprecated), VS Code's
`git.addAICoAuthor` (`off`, `chatAndAgent`, `all`), and per-tool equivalents let a user
suppress the markers.

A committed settings file that disables attribution is itself observable evidence of a
deliberate de-attribution decision - record it under `Indicated` provenance for the
workflow, never as proof that specific files were generated.

History rewrites erase trailers: squash merges drop co-author trailers unless the merger
preserves them, rebases and `filter-repo` runs can strip them entirely, and purpose-built
scrubbing tools exist.

Absence of attribution therefore carries zero evidentiary weight toward human authorship.

## Provenance Documents

Structured provenance records, when a project ships them, outrank convention signals.

- SPDX 3.0 `creationInfo` records `createdBy` (an Agent, which may be an AI agent) and
  `createdUsing` (a Tool) per element - the only widely-adopted machine-readable
  authorship vocabulary for shipped files.
- CycloneDX `formulation` describes declared and observed manufacturing processes
  (workflows, tasks, steps), `declarations` carries signed attestations and evidence, and
  `metadata.tools` names the generating toolchain - `externalReferences` of type
  `attestation` link supporting claims.
- SLSA v1.2 source-track provenance attestations (in-toto predicate naming how a source
  revision was produced, including review enforcement) are the supply-chain form of
  authorship evidence.
- in-toto attestations in CI workflows or release artifacts (`*.intoto.jsonl`,
  attestation steps) bind claims to signed envelopes.
- Signed commits and tags bind an author identity to a key - a `Verified` bot commit is a
  platform-attested agent contribution, and a signed human commit attests the keyholder,
  not the authorship.

## Detection Research Reality Check

Academic detectors classify code as human- or machine-written from lexical, syntactic,
perplexity, or learned features.

The published record shows they are not audit evidence:

- Real-world robustness is poor - DIMVA'25 ("Hiding in Plain Sight") found existing tools
  fragile and inaccurate under realistic prompt and training-set variation.
- Detection has a half-life - accuracy depends on the generator model and prompting
  strategy, so a detector validated on one generation degrades on the next.
- Benchmarks keep showing the gap - AICD Bench and empirical studies report strong
  in-domain scores that collapse out-of-distribution, with severe prediction bias in some
  tools.
- Perplexity methods generalize best but trade away accuracy and speed and fail on
  high-level languages; general-purpose LLM judges beat dedicated detectors yet remain
  unreliable and prompt-sensitive.

Style therefore never establishes provenance.

Uniform formatting, conventional naming, dense comments, round test values, synchronized
version bumps, rapid commit cadence, and absent TODOs each have human explanations and are
excluded from the evidence base.

## Context Anchors

Legal and governance references that explain why attribution records matter - context for
findings, not conformance checks.

- EU AI Act Article 50(2) requires providers of AI systems generating synthetic text
  (among other modalities) to mark outputs in a machine-readable, detectable format;
  obligations apply from 2 August 2026 and sit on the AI provider, with exceptions for
  assistive editing and some business-to-business uses. Expect vendor attribution
  conventions to strengthen, not weaken.
- The US Copyright Office's Part 2 report on copyrightability (January 2025) reaffirms
  the human-authorship requirement: purely AI-generated material lacks protection, and
  prompting alone does not confer authorship - provenance records are what let a rights
  holder evidence the human contribution.
- NIST AI RMF and ISO/IEC 42001 frame the organizational controls around AI use, consumed
  by `assessment/ai-system.md` and `assessment/generated-code.md` as process vocabulary.

## Live Check

When web fetch is available, spot-check one tool's attribution convention against its
vendor documentation and the SLSA source-track requirements against slsa.dev - the
conventions table drifts fastest.

Record whichever baseline - this snapshot or the live pages - the audit used, and note
drift in Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
