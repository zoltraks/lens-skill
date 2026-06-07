# Observability

## Purpose

> **Scope:** Logging, metrics, tracing, alerting
> **Key items:** structured logs, meaningful metrics, request tracing, actionable alerts

This file guides assessment of how well the system can be understood while running.

Apply `principles/evaluation-rules.md` throughout. Operational use of observability data is assessed in `assessment/operational-readiness.md`.

## What To Evaluate

- Logging: whether logs are present, structured, and at useful levels.
- Metrics: whether key system and business metrics are collected.
- Tracing: whether requests can be followed across components.
- Alerting: whether conditions trigger actionable notifications.

## Evidence To Look For

| Signal                       | Where It Appears                                   |
|------------------------------|----------------------------------------------------|
| Logging                      | Logging libraries, log format, log levels          |
| Metrics                      | Metrics instrumentation, dashboards, counters      |
| Tracing                      | Trace context propagation, span instrumentation    |
| Alerting                     | Alert rules, thresholds, notification routing      |
| Correlation                  | Request or trace identifiers across components      |

## Status Criteria

- `PASS`: Structured logs, meaningful metrics, request tracing, and actionable alerts are present, with evidence.
- `PARTIAL`: Some signals exist but are unstructured, incomplete, or lack alerting.
- `FAIL`: No usable observability where it is clearly required, with evidence.
- `UNKNOWN`: Observability artifacts were not provided.

## Common Risks

- Incidents cannot be diagnosed because logs are absent or unstructured.
- Degradation goes unnoticed because no metric captures it.
- Failures cannot be traced across services without correlation identifiers.
- Alerts are missing or noisy, so real problems are not acted upon.

## What Raises Confidence

- Structured logs with consistent levels and correlation identifiers.
- Metrics that cover the system's key health and business signals.
- Distributed tracing across component boundaries.
- Alerts tied to clear thresholds and routed to an owner.

Mark each missing signal explicitly rather than inferring its presence.
