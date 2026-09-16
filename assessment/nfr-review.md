# Non-Functional Requirements

## Purpose

> **Scope:** Performance, scalability, availability, reliability, resilience
> **Key items:** stated targets, measured evidence, scaling model, failure tolerance

This file guides assessment of the qualities a system must exhibit beyond its functions.

Apply `principles/evaluation-rules.md` throughout. Distinguish a stated target from a measured result, and mark unstated targets as `NOT SPECIFIED`.

## What To Evaluate

- Performance: latency and throughput against stated targets.
- Scalability: how the system handles increased load, and whether scaling is horizontal or vertical.
- Availability: uptime targets and the architecture that supports them.
- Reliability: correctness and consistency of results over time.
- Resilience: behavior under partial failure, including degradation and recovery.

## Evidence To Look For

| Signal               | Where It Appears                                |
|----------------------|-------------------------------------------------|
| Stated NFR targets   | Requirements, SLAs, SLOs, design docs           |
| Performance evidence | Benchmarks, load test results, profiling data   |
| Scaling model        | Autoscaling config, statelessness, partitioning |
| Redundancy           | Replication, multi-zone setup, failover         |
| Resilience patterns  | Timeouts, circuit breakers, bulkheads, retries  |

## Status Criteria

- `PASS`: Targets are stated and met with measured evidence, and the architecture supports the required scale and resilience.
- `PARTIAL`: Targets are stated but only partly evidenced, or the architecture supports some qualities but not others.
- `FAIL`: Required NFRs are clearly unmet, with evidence.
- `UNKNOWN`: NFR targets or measurements were not provided.

## Common Risks

- Performance degrades under load that was never tested.
- A stateful design blocks horizontal scaling when demand rises.
- A single point of failure undermines stated availability targets.
- Partial failures cascade because no resilience patterns contain them.

## What Raises Confidence

- Explicit NFR targets tied to measured results.
- A scaling model that matches the expected load profile.
- Redundancy that matches the stated availability target.
- Resilience patterns that contain and recover from partial failure.

Mark each missing signal explicitly rather than inferring its presence.
