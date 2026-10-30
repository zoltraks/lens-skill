# API Contract Conformance

## Purpose

> **Scope:** API specification conformance, schema validation, error standardization, versioning,
> spec-to-code agreement
> **Key items:** OpenAPI/contract presence, request and response schema enforcement, RFC 9457 error
> format, versioning strategy, OWASP API Security Top 10 (2023)

This file guides assessment of whether a system that exposes an API conforms to its own contract and
to API design standards, and whether a system that consumes a documented API contract calls it
conformantly.

It complements `assessment/security-review.md` and `assessment/threat-model.md` for the security
dimension and `assessment/documentation-review.md` for the docs dimension.

Apply `principles/evaluation-rules.md` throughout.

Assess only what the spec and code show.

Treat a spec that contradicts the code as a drift finding.

## When This Applies

This assessment applies when the system defines, exposes, or consumes an API contract: REST,
GraphQL, gRPC, MCP, or a similar contract-driven interface.

A consumer such as a CLI, agent, or client library qualifies when a documented contract exists for
the API it calls, for example an OpenAPI spec in the same repository or a published contract it
targets.

For a consumer, assess request and response conformance to that contract:
whether the calls match documented endpoints, payloads, and error shapes.

Mark provider-side dimensions such as contract presence and schema enforcement `N/A` for a pure
consumer.

A system with no API surface still has contract surfaces. See Contract Surfaces Beyond APIs.

In that case mark the API rows `N/A` with a one-line justification and assess the surfaces
that do exist.

Do not invent an API-spec section for a project that has no API.

## What To Evaluate

- **Contract presence**: whether an API specification exists (OpenAPI, AsyncAPI, Protobuf, JSON
  Schema) and whether it is generated from code or maintained by hand.
- **Schema validation**: whether request bodies are validated against the schema and rejected when
  malformed.
- **Response consistency**: whether responses use a consistent envelope and types across endpoints.
- **Error standardization**: whether errors follow a standard such as RFC 9457 (Problem Details for
  HTTP APIs) with `type`, `title`, `status`, `detail`, and `instance` fields, rather than ad hoc
  bodies.
- **Versioning**: whether the API has a versioning strategy (path, header, or media type).
- **Spec-to-code agreement**: whether the specification matches the implemented behavior, including
  auth requirements per endpoint.
- **OWASP API Security Top 10 (2023)**: whether the contract guards against the API-specific risk
  categories.

## Protocol-Specific Requirements

[RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) obsoletes RFC 7807 for HTTP Problem Details.

It is an optional format, not a universal requirement for every API or every error response.

Assess its member semantics and media type only when adopted by the contract, and do not require
all five standard members indiscriminately.

Use JSON-RPC/MCP, gRPC, or GraphQL error conventions for those protocols rather than forcing an
HTTP Problem Details envelope onto them.

Compare actual endpoints, schemas, auth rules, compatibility promises, and failure behavior.

An OpenAPI `info.version` need not equal the binary package version unless the project requires it.

A version mismatch alone does not demonstrate schema drift or require URL versioning.

Apply the stub-detection recipe from `references/topics/evidence-recipes.md` to the endpoint
surface: a handler returning a fixed payload, raising `NotImplementedError`, or delegating to a
simulated service is a stub finding, and the spec entry it satisfies is spec drift, not an
implemented contract.

Diff authentication requirements per endpoint between the spec (`security` blocks, documented
auth rules) and the code (middleware, decorators, guards): an endpoint the spec marks
authenticated but the code serves without a check is a contract violation, and the reverse
direction - code-enforced auth the spec never declares - is a documentation gap.

## Contract Surfaces Beyond APIs

Contract conformance is wider than network APIs - every interface the subject promises to
consumers is a contract surface, and each one gets the same spec-versus-code drift check.

| Surface                 | Contract artifact                                    | Drift check                                               |
|-------------------------|------------------------------------------------------|-----------------------------------------------------------|
| Event/message schema    | AsyncAPI, schema registry export, documented payload | Emitted or consumed payload versus the declared schema    |
| CLI surface             | `--help` text, man page, documented exit codes       | Parsed flags, subcommands, and exit codes versus docs     |
| Configuration schema    | Env-var list, config file spec, JSON Schema          | Accepted keys, types, and defaults versus the spec        |
| File/persistence format | Format spec, migration docs, schema DDL              | Written layout and migrations versus the declared format  |
| Plugin/extension point  | Extension guide, SPI/interface docs                  | Discovered hooks and signatures versus the documented set |
| Library public surface  | API docs, changelog, semver promise                  | Exported symbols and signatures versus the documented API |

For each surface that exists, apply the same sequence as for APIs: locate the declared contract,
locate the implementing code, diff them, and record drift as a finding citing both sides.

A surface the subject never declares is `NOT_ASSESSED` for contract purposes - an undocumented
interface is a documentation finding, not spec drift.

### Coupled-Client Reconciliation

When the repository contains a consumer of the subject's API - frontend service modules,
static control pages, CLI callers - the client's call set is the declared contract even
when no written spec exists.

Enumerate the client call sites and the server routes, then reconcile in both directions:
every client call must land on a served route, and every served route should have a caller
or a documented external consumer.

Classify each pair:

| Class            | Meaning                                                         |
|------------------|-----------------------------------------------------------------|
| `matched`        | Client call and server route agree on path, method, and shape   |
| `phantom call`   | Client calls an endpoint the server does not implement          |
| `dead endpoint`  | Server route with no client call and no documented consumer     |
| `shape mismatch` | Both sides exist but disagree on payload, method, or parameters |

Present the reconciliation as a matrix of call sites against routes.

A `phantom call` or `shape mismatch` is a finding citing both the call site and the route.

A `dead endpoint` is a finding unless a documented external consumer justifies it.

## OWASP API Security Top 10 (2023) Reference

Use these category codes when an API security gap maps to one:

| Code       | Category                                        |
|------------|-------------------------------------------------|
| API1:2023  | Broken Object Level Authorization               |
| API2:2023  | Broken Authentication                           |
| API3:2023  | Broken Object Property Level Authorization      |
| API4:2023  | Unrestricted Resource Consumption               |
| API5:2023  | Broken Function Level Authorization             |
| API6:2023  | Unrestricted Access to Sensitive Business Flows |
| API7:2023  | Server-Side Request Forgery                     |
| API8:2023  | Security Misconfiguration                       |
| API9:2023  | Improper Inventory Management                   |
| API10:2023 | Unsafe Consumption of APIs                      |

## Evidence To Look For

| Signal             | Where It Appears                                                   |
|--------------------|--------------------------------------------------------------------|
| API specification  | `openapi.yaml`, `*.proto`, schema files, generated docs            |
| Schema enforcement | Validation middleware, typed deserialization, rejected-input tests |
| Error format       | Centralized error responses, problem-details types                 |
| Versioning         | Version in path, header, or media type                             |
| Spec drift         | Spec declarations that differ from implemented behavior            |

## Status Criteria

- `PASS`: A specification exists, is enforced, errors are standardized, versioning is defined, and
  the spec matches the code, with evidence.
- `PARTIAL`: A specification exists but enforcement, error standardization, versioning, or
  spec-to-code agreement is incomplete.
- `FAIL`: No specification where the API surface clearly requires one, or the spec broadly
  contradicts the code, with evidence.
- `UNKNOWN`: API artifacts were not provided.
- `N/A`: The system exposes no API and consumes no documented contract, with justification.

## How To Present

Render this as a standalone section, as described in
`process/report-format/conditional-conformance.md`, only when the system exposes an API.

Present a conformance table across the evaluated dimensions,
then describe each gap with evidence and its linked `FND-XXX`.

## Rules

- Anchor every conformance gap to a specific endpoint, schema, or spec line.
- When the spec contradicts the code, record it as a drift finding citing both sides.
- Map each API security gap to its OWASP API Security Top 10 (2023) code where one applies.
- Do not assume a control is present because the spec mentions it, confirm enforcement in code.
