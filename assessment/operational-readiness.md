# Operational Readiness

## Purpose

> **Scope:** Runbooks, on-call, capacity, backups, incident response
> **Key items:** day-two operations, recovery procedures, ownership, capacity planning

This file guides assessment of whether the system can be run and supported in production.

Apply `principles/evaluation-rules.md` throughout. Observability signals are assessed in `assessment/observability.md`; here the focus is the operational practices that consume them.

## What To Evaluate

- Runbooks: documented procedures for common operational tasks and failures.
- On-call and ownership: whether responsibility for the system is defined.
- Capacity: whether capacity is planned and headroom is known.
- Backups and recovery: whether data is backed up and recovery is tested.
- Incident response: whether there is a defined process for detecting and resolving incidents.

## Evidence To Look For

| Signal            | Where It Appears                                   |
|-------------------|----------------------------------------------------|
| Runbooks          | Operational docs, procedure guides                 |
| Ownership         | On-call rotation, escalation paths, service owners |
| Capacity planning | Capacity models, scaling thresholds, quotas        |
| Backups           | Backup schedule, retention, restore procedure      |
| Recovery testing  | Restore drills, disaster-recovery exercises        |
| Incident process  | Incident playbooks, post-incident reviews          |

## Status Criteria

- `PASS`: Runbooks, defined ownership, capacity planning, tested backups, and an incident process are present, with evidence.
- `PARTIAL`: Some operational practices exist but key procedures are undocumented, untested, or unowned.
- `FAIL`: No operational practices where production operation is clearly intended, with evidence.
- `UNKNOWN`: Operational artifacts were not provided.

## Common Risks

- Incidents take longer to resolve because no runbook exists.
- Unclear ownership delays response when the system fails.
- Unplanned capacity leads to outages under expected growth.
- Untested backups fail at the moment recovery is needed.
- Absence of an incident process means failures repeat without learning.

## What Raises Confidence

- Runbooks for common tasks and known failure modes.
- Defined ownership and an escalation path.
- Capacity planning with known headroom and scaling triggers.
- Backups with a tested, documented restore procedure.
- An incident process with post-incident review.

Mark each missing signal explicitly rather than inferring its presence.
