# API Contract Conformance

## Purpose

> **Scope:** API specification conformance, schema validation, error standardization, versioning,
> spec-to-code agreement
> **Key items:** OpenAPI/contract presence, request and response schema enforcement, RFC 9457 error
> format, versioning strategy, OWASP API Security Top 10 (2023)

This file guides assessment of whether a system that exposes an API conforms to its own contract and
to API design standards, and whether a system that consumes a documented API contract calls it
conformantly. It complements `assessment/security-review.md` and
`assessment/threat-model.md` for the security dimension and `assessment/documentation-review.md` for
the docs dimension.

Apply `principles/evaluation-rules.md` throughout. Assess only what the spec and code show. Treat a
spec that contradicts the code as a drift finding.

## When This Applies

This assessment applies when the system defines, exposes, or consumes an API contract: REST,
GraphQL, gRPC, MCP, or a similar contract-driven interface.

A consumer such as a CLI, agent, or client library qualifies when a documented contract exists for
the API it calls, for example an OpenAPI spec in the same repository or a published contract it
targets. For a consumer, assess request and response conformance to that contract: whether the
calls match documented endpoints, payloads, and error shapes. Mark provider-side dimensions such
as contract presence and schema enforcement `N/A` for a pure consumer.

It does not apply to a system with no API surface and no documented contract consumption, for
example a pure CLI with no server calls, a library, or a batch job. In that case, mark the
section `N/A` with a one-line justification. Do not invent an API-spec section for a project
that has no API.

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

Render this as a standalone section, as described in `process/report-format.md`, only when the
system exposes an API. Present a conformance table across the evaluated dimensions, then describe
each gap with evidence and its linked `FND-XXX`.

## Rules

- Anchor every conformance gap to a specific endpoint, schema, or spec line.
- When the spec contradicts the code, record it as a drift finding citing both sides.
- Map each API security gap to its OWASP API Security Top 10 (2023) code where one applies.
- Do not assume a control is present because the spec mentions it, confirm enforcement in code.
