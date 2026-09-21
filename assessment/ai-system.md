# AI System Assessment

## Purpose

> **Scope:** AI and machine-learning system risk, provenance, evaluation, safety, privacy, and
> operational controls
> **Key items:** model and data provenance, evaluation, misuse resistance, monitoring, rollback

This file guides assessment of a software project that trains, fine-tunes, serves, or materially
depends on an AI or machine-learning model.

Apply `principles/evaluation-rules.md` throughout.

| Out of scope                 | See instead                       |
|------------------------------|-----------------------------------|
| Code authorship or origin    | `assessment/ai-generated-code.md` |
| General application security | `assessment/security-review.md`   |
| Personal-data obligations    | `assessment/compliance-review.md` |
| Dependency inventory         | `assessment/dependency-review.md` |

## When This Applies

Include this assessment when the repository contains model weights, training or fine-tuning code,
model-serving code, prompt or agent orchestration, retrieval-augmented generation, AI evaluation
harnesses, or documentation that makes AI behavior a material system function.

Do not include it because a project used an AI coding assistant.

When the system only contains ordinary generated source and no AI runtime or model lifecycle, use
`assessment/ai-generated-code.md` instead.

## What To Evaluate

- Model and dataset provenance, versioning, licensing, and integrity.
- Evaluation objectives, test data, acceptance criteria, and documented limitations.
- Safety, misuse, abuse, privacy, and security controls appropriate to the use case.
- Input and output boundaries, prompt or tool injection controls, and authorization context.
- Model change management, rollback, monitoring, and incident response.
- Human oversight, escalation, user disclosure, and decision-impact controls.
- Resource, cost, latency, and availability controls for model use.

## Evidence To Look For

| Signal              | Where It Appears                                     |
|---------------------|------------------------------------------------------|
| Model identity      | Model manifest, pinned artifact, registry reference  |
| Dataset provenance  | Data card, source inventory, license, lineage record |
| Evaluation coverage | Evaluation code, datasets, metrics, reports          |
| Safety controls     | Policy filters, refusal tests, abuse controls        |
| Input boundaries    | Prompt templates, retrieval filters, tool policies   |
| Output controls     | Validation, redaction, human review, constraints     |
| Monitoring          | Drift, quality, safety, cost, and incident metrics   |
| Change control      | Model release notes, approvals, rollback procedure   |
| User disclosure     | Product documentation and user-facing notices        |

## Provenance And Reproducibility

Record the model, data, code, configuration, dependency, and artifact revisions that determine the
assessed behavior.

Distinguish declared provenance from verified provenance.

A model name without a digest, version, source, or retrieval date is incomplete provenance evidence.

A dataset name without collection scope, license, and transformation history is incomplete data
provenance evidence.

Do not reproduce sensitive training data, prompts, credentials, or model artifacts in the report.

## Evaluation And Safety

Assess whether evaluation criteria match the system's stated purpose and risk.

Look for positive, negative, boundary, abuse, regression, and out-of-distribution cases where the
use case makes them relevant.

Do not invent a universal accuracy, safety, or fairness threshold.

Mark proposed thresholds as proposed until an owner confirms them.

A benchmark score does not prove production safety, robustness, or suitability for every user group.

Record the evaluation dataset, metric definition, model revision, exclusions, and result basis when
reported results are present.

## Security And Authorization Boundaries

Trace untrusted input through model prompts, retrieval, tool calls, structured output, and side
effects.

Check whether model output is treated as data or as an authorization decision.

Check whether tool access is independently authorized rather than granted because a model requested
it.

Assess prompt injection, indirect instruction injection, sensitive-data disclosure, unsafe tool use,
resource exhaustion, and untrusted output handling when the architecture exposes those surfaces.

Do not perform adversarial exploitation against a live system.

## Operations And Change Management

Assess model and prompt versioning, release approval, rollback, monitoring, incident response, and
cost controls.

For hosted inference, distinguish target latency or cost from measured results.

For local inference, assess resource limits, model loading failures, update safety, and recovery
from partial or corrupted artifacts.

A model registry or deployment manifest shows intended control, not successful rollback or runtime
monitoring.

## Framework References

Use selected practices from the [NIST AI Risk Management Framework 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
when AI risk management is in scope.

Use [ISO/IEC 42001](https://www.iso.org/standard/42001) only as a management-system reference
when organizational AI governance is explicitly relevant.

Neither reference creates a conformance claim from repository inspection alone.

Record the exact practices or outcomes assessed and list unassessed areas.

## Status Criteria

- `PASS`: Applicable AI lifecycle and operational controls are present and supported by evidence.
- `PARTIAL`: Some controls or evaluations exist, but material lifecycle or evidence gaps remain.
- `FAIL`: A required control is absent or defeated, with evidence.
- `UNKNOWN`: The AI system scope, artifacts, or evaluation evidence cannot be determined.
- `N/A`: No AI or machine-learning system is in scope, with a deployment-model justification.

## What Raises Confidence

- Pinned model and dataset artifacts with provenance and license records.
- Evaluation results tied to the assessed model revision and declared use case.
- Independent authorization around retrieval, tools, and consequential actions.
- Documented safety, privacy, abuse, and incident-response controls.
- Monitored releases with rollback and residual-risk handling.

## How To Present

Render this assessment as a conditional section or as findings in the appropriate technical pillars,
according to `process/report-format.md`.

Keep AI-system risks separate from AI-generated-code provenance findings.

Link every material gap to `FND-SEC-XXX`, `FND-ARC-XXX`, `FND-INF-XXX`, or another pillar where the
fix lives.
