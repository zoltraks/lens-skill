# AI-Generated Code & Provenance

## Purpose

> **Scope:** Evidence of code origin and the controls used to validate generated artifacts
> **Key items:** provenance, review records, reproducibility, SDLC controls, uncertainty

Assess observable development artifacts and validation controls, not the abilities or intent of
contributors.

Apply `principles/evaluation-rules.md` throughout.

`references/methodology/ai-provenance.md` holds the attribution signature table, the
provenance-document vocabulary, the erasure rules, and the detection-research basis for the
constraints below.

| Out of scope       | See instead                       |
|--------------------|-----------------------------------|
| Test effectiveness | `assessment/testing-review.md`    |
| Source licensing   | `assessment/copyright-review.md`  |
| Change governance  | `assessment/change-management.md` |

## Establish Provenance

Establish provenance from artifacts, never from style.

Assign each scoped artifact or change set a `Provenance basis` from the evidence tiers:

- `Declared` - an explicit attribution artifact exists in the repository: an agent commit
  trailer, a bot author or committer identity, a generation manifest, a session-log link,
  or a documented AI policy whose declared artifacts are consistent with the tree.
- `Attested` - a verifiable or signed provenance record exists: a platform-signed bot
  commit, an in-toto or SLSA source-track attestation, an SPDX `createdBy`/`createdUsing`
  record, or a CycloneDX `declarations`/`formulation` entry naming the producing agent.
- `Supplied` - a stakeholder statement or other reported evidence asserts the origin and
  nothing contradicts it.
- `Indicated` - only circumstantial artifacts exist: agent configuration or guidance
  files, committed settings that govern (or suppress) attribution, or an agent workflow
  the repository clearly supports without per-artifact attribution.
- `Undetermined` - no evidence either way.

The tiers describe the strength of evidence for agent involvement, in descending order.

`Declared` and `Attested` support a positive provenance finding; `Indicated` and
`Supplied` support provenance language only with the limitation named; `Undetermined`
supports no provenance claim at all.

The asymmetry rule applies: human authorship is never a report conclusion - a clean
attribution census is `Undetermined`, not evidence of human authorship.

AI instruction files establish that an agent workflow is supported, not that any specific
file was generated or that review was absent - they ground `Indicated` at most.

Record the provenance source, its scope, and whether it is inspected or reported evidence.

Run the attribution census from `references/census-commands.md` when git history is in
scope, and treat erased or suppressed attribution per the digest's erasure rules - an
opt-out configuration is `Indicated` evidence about the workflow, not about the code.

Keep code origin `UNKNOWN` when it cannot be established.

Do not estimate the percentage of AI-generated code from style, and do not run or cite
statistical authorship detectors - the digest's research section documents why their
output is not audit evidence.

Uniform formatting, round test values, synchronized versions, rapid commits, verbose
prose, and absence of TODOs or abandoned code are not reliable authorship evidence.

Generated code is not inherently lower quality, and unknown origin is not evidence of
infringement.

## Evaluate Validation Controls

- Check whether generated changes have requirement links and review evidence.
- Inspect tests for actual behavior, boundary conditions, and failure paths.
- Verify referenced APIs against the declared or pinned dependency versions.
- Inspect whether generated datasets record source, generator version, and validation method.
- Check how generation inputs containing sensitive data are governed when such use is evidenced.
- Assess how defects are tracked, corrected, and prevented from recurring.

Do not infer a contributor's understanding from comments or the absence of comments.

Evaluate missing review or provenance controls against the system's adopted requirements and
exposure, rather than assigning an automatic severity based on file size.

## Separate Origin From Quality

Record stub tests under Code Quality, unsafe authorization under Security, and missing decision
rationale under Architecture, regardless of who or what produced the code.

Cross-reference those findings from this category only when explicit provenance links them.

Do not duplicate the same defect under multiple pillars to penalize AI involvement twice.

Use "unverified generated artifact" only when generation is evidenced and validation is unknown.

Use "missing validation evidence" when origin itself is unknown.

## Status Criteria

- `PASS`: Applicable provenance and validation requirements are evidenced for the reviewed scope.
- `PARTIAL`: Some required controls are evidenced, but specific validation gaps remain.
- `FAIL`: A required provenance or validation control is demonstrably absent or defeated.
- `UNKNOWN`: Origin or validation history cannot be determined from available artifacts.
- `N/A`: No generated artifacts or AI workflow are in scope, with a stated justification.

Keep provenance uncertainty separate from independently evidenced quality defects.

Prototype status changes applicable controls, but does not make provenance automatically irrelevant.

## Process Frameworks

Use selected [NIST SSDF practices](https://csrc.nist.gov/pubs/sp/800/218/final) for review, testing,
artifact protection, and vulnerability response when process evidence is available.

SSDF 1.1 is the current core SSDF baseline for this guidance.

Recheck the NIST publications index at audit time because supplemental profiles and revisions may
change the applicable reference set.

When generative-AI or foundation-model development is in scope, consider the applicable
[SSDF AI community profile](https://csrc.nist.gov/pubs/sp/800/218/a/final) separately from the
core SSDF practices.

Do not present draft requirements or supplemental profiles as adopted controls.

Use [OWASP SAMM](https://owaspsamm.org/model/) to organize evidenced governance, design,
implementation, verification, and operations practices when process maturity is in scope.

Identify the exact practices assessed and missing evidence.

Do not claim an SSDF certification or SAMM maturity level from repository inspection alone.
