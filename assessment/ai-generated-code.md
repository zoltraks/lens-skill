# AI-Generated Code & Provenance

## Purpose

> **Scope:** Evidence of code origin and the controls used to validate generated artifacts
> **Key items:** provenance, review records, reproducibility, SDLC controls, uncertainty

Assess observable development artifacts and validation controls, not the abilities or intent of
contributors.

Apply `principles/evaluation-rules.md` throughout.

| Out of scope       | See instead                       |
|--------------------|-----------------------------------|
| Test effectiveness | `assessment/testing-review.md`    |
| Source licensing   | `assessment/copyright-review.md`  |
| Change governance  | `assessment/change-management.md` |

## Establish Provenance

Use explicit attribution, generation manifests, linked review records, or supplied stakeholder
statements to establish the provenance of particular artifacts.

AI instruction files establish that an agent workflow is supported, not that any specific file was
generated or that review was absent.

Record the provenance source, its scope, and whether it is inspected or reported evidence.

Keep code origin `UNKNOWN` when it cannot be established.

Do not estimate the percentage of AI-generated code from style.

Uniform formatting, round test values, synchronized versions, rapid commits, verbose prose, and
absence of TODOs or abandoned code are not reliable authorship evidence.

Generated code is not inherently lower quality, and unknown origin is not evidence of infringement.

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

SSDF 1.1 is the final baseline consulted for this guidance, while 1.2 is listed as a draft in the
[NIST publications index](https://csrc.nist.gov/projects/ssdf/publications).

Recheck publication status at audit time and do not present draft requirements as adopted controls.

Use [OWASP SAMM](https://owaspsamm.org/model/) to organize evidenced governance, design,
implementation, verification, and operations practices when process maturity is in scope.

Identify the exact practices assessed and missing evidence.

Do not claim an SSDF certification or SAMM maturity level from repository inspection alone.
