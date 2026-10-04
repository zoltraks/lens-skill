# Domain Profiles

## Purpose

> **Scope:** Project-nature classification and the mandatory evidence probes each nature
> activates
> **Key items:** nature classification, advertised-workflow discovery, probe selection,
> completeness rules

This file defines how an audit classifies what the subject IS before it assesses what the
subject does well.

Apply `principles/evaluation-rules.md` throughout.

A project nature is derived from evidence - manifests, entry points, protocols, persisted data,
and documentation claims - never assumed from the repository name or the user's phrasing.

## Classification

During Scope Definition, assign one primary nature and any number of secondary natures per
project:

| Nature          | Recognized by                                                                   |
|-----------------|---------------------------------------------------------------------------------|
| `service`       | Long-running process, network listeners, request handlers, deployment artifacts |
| `library`       | Public API surface, packaging manifest, no entry point                          |
| `cli`           | Command entry point, argument parsing, terminal output                          |
| `pipeline`      | Batch or streaming transformation of inputs to outputs                          |
| `retrieval`     | Indexing, embedding, search or ranking over stored content                      |
| `agent-tooling` | Skill definitions, tool schemas, protocol bridges such as MCP                   |
| `frontend`      | Rendered UI, routing, client-side state                                         |
| `unclassified`  | None of the above fits. Record the closest profile used as a fallback           |

The classification records which documentation claims count as advertised workflows.

A capability named in README, specifications, or contract surfaces is an advertised workflow
even when the implementation is thin.

A root `SKILL.md` does not by itself make the subject `agent-tooling` primary: distinguish a
repository that IS the skill - `SKILL.md` is the product entry and the payload is instructions -
from a software repository that ships a `SKILL.md` capability catalog alongside compiled or
runtime payloads, which classifies by its deliverable and keeps `agent-tooling` secondary.
Cross-reference the authored-versus-installed rules in `assessment/skill-definition.md` so a
catalog of the project's own utilities is not misfiled as a separate skill project.

## Mandatory Probes

Each nature activates its probe set during Evidence Gathering.

A probe produces evidence rows. It never produces a finding by itself.

| Nature          | Mandatory probes                                                                                                                                                                                         |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `service`       | Session/request lifecycle (issuance, expiry, revocation, eviction). Rate and size limits per endpoint. Graceful shutdown path. Request concurrency bounds                                                |
| `library`       | Public-surface inventory. Compatibility and versioning discipline. Consumer-visible error taxonomy                                                                                                       |
| `cli`           | Credential and token persistence (store, permissions, rotation). Argument and exit-code contract. CWD versus config-location resolution. Proxy/stdio bridges                                             |
| `pipeline`      | Idempotency and partial-failure resume. Input validation. Ordering and backpressure bounds                                                                                                               |
| `retrieval`     | Index-path and identifier producer/consumer trace across ingest, query, fetch, watch, and sync paths. Embedding pipeline reality (real inference versus stub). Stale-row handling on deletes and renames |
| `agent-tooling` | Protocol conformance per declared spec version. Tool registry consistency across transports. Attribution fields the caller controls                                                                      |
| `frontend`      | Route and state boundary checks. Secret-bearing surface in shipped bundles                                                                                                                               |
| `unclassified`  | Closest profile's probes plus an explicit Scope Exclusions note                                                                                                                                          |

## Cross-Cutting Probes

Every nature also activates these probes:

- **Identifier trace** - for every value crossing a component boundary (paths, IDs, tokens,
  claims, config keys, error shapes), a producer/consumer matrix naming each site and the
  representation it emits or expects.
- **Journey trace** - for each advertised workflow, the declared path through its hops with
  conforming and failing hops recorded.
- **Stub census** - uniform-return functions, `unimplemented!`/`todo!` bodies, cfg-gated or
  never-called modules, and feature-flagged fallbacks behind advertised capabilities.
- **Lifecycle completeness** - for credentials, tokens, sessions, and synced state:
  revocation, expiry, rotation, and post-removal behavior.
- **Defaults sweep** - shipped ports, addresses, credentials, debug endpoints, transport
  security, and file permissions against least-privilege expectations.
- **Toolchain compatibility** - manifest edition/MSRV, builder images, and documented
  prerequisites against the language features and APIs the code uses.

## Recording

Record the profile assignment and activated probes in the Auditing Methodology section.

A skipped probe requires a recorded reason. An unprobeable item is a `NOT ASSESSED` evidence
row, not silence.
