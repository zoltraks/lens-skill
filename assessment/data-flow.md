# Data Flow Modeling

## Purpose

> **Scope:** Data flow diagrams, trust boundaries, data stores, inter-process flows
> **Key items:** Level-0 context diagram, Level-1 decomposition, external entities, processes, data stores, trust boundaries

This file guides construction of a data flow model that makes the system's data movement and trust boundaries explicit. It is the foundation for the threat model in `assessment/threat-model.md` and enriches the Architectural Assessment.

Apply `principles/evaluation-rules.md` throughout. Model only what the input shows. Mark inferred flows as inferred.

## When This Applies

This assessment applies when the system moves data across one or more trust boundaries, for example: a network service, an API, a multi-process system, a system that reads or writes external stores, or a system that integrates with third-party services.

It does not apply to a pure library, a single-file script with no external I/O, or a system with no trust boundary. In those cases, mark the section `N/A` with a one-line justification anchored to the deployment model.

## What To Model

A data flow diagram (DFD) uses exactly four element types. Use these consistently:

| Element | Meaning | Notation in prose |
|---------|---------|-------------------|
| External entity | An actor or system outside the boundary that produces or consumes data | `[Entity]` |
| Process | A unit inside the system that transforms data | `(Process)` |
| Data store | A place where data rests | `{Store}` |
| Data flow | A directional movement of data between the above | `-->` |

Model two levels:

- **Level-0 (context diagram)**: the entire system as a single process, surrounded by its external entities and the data flows between them. This shows the system boundary and scope.
- **Level-1 (decomposition)**: the main process broken into its major internal processes, with the data stores and the flows between them. This shows the internal structure and the trust boundaries.

## Trust Boundaries

A trust boundary is a line where the level of trust changes, for example between an unauthenticated client and an authenticated handler, or between application code and the filesystem.

Mark each boundary explicitly. Every flow that crosses a boundary is a candidate for threat analysis in `assessment/threat-model.md`.

## Evidence To Look For

| Signal | Where It Appears |
|--------|------------------|
| External entities | Clients, third-party services, Git remotes, message queues named in code or config |
| Processes | Request handlers, background workers, sync loops, watchers |
| Data stores | Databases, caches, file systems, in-memory state |
| Data flows | Function calls across modules, network calls, file reads and writes |
| Trust boundaries | Authentication middleware, authorization checks, deserialization points, process boundaries |

## How To Present

Render the model in the Architectural Assessment section as described in `process/report-format.md`. Present the Level-0 and Level-1 diagrams as fenced ASCII blocks or as a flow table, then list the trust boundaries in a table.

Tie every node and flow to a concrete file path, module, or config key. Do not invent flows that the input does not show.

## Rules

- Use only the four DFD element types. Do not introduce custom shapes.
- Mark every trust boundary explicitly; the threat model depends on it.
- Mark inferred flows as inferred rather than presenting them as confirmed.
- When the system has no trust boundary, mark the section `N/A` rather than forcing a diagram.
