# API Contract Conformance

## Purpose

> **Scope:** API specification conformance, schema validation, error standardization, versioning, spec-to-code agreement
> **Key items:** OpenAPI/contract presence, request and response schema enforcement, RFC 7807 error format, versioning strategy, OWASP API Security Top 10 (2023)

This file guides assessment of whether a system that exposes an API conforms to its own contract and to API design standards. It complements `assessment/security.md` and `assessment/threat-model.md` for the security dimension and `assessment/documentation.md` for the docs dimension.

Apply `principles/evaluation-rules.md` throughout. Assess only what the spec and code show. Treat a spec that contradicts the code as a drift finding.

## When This Applies

This assessment applies when the system exposes an API: REST, GraphQL, gRPC, MCP, or a similar contract-driven interface.

It does not apply to a system with no external API surface, for example a pure CLI with no server, a library, or a batch job. In that case, mark the section `N/A` with a one-line justification. Do not invent an API-spec section for a project that has no API.

## What To Evaluate

- **Contract presence**: whether an API specification exists (OpenAPI, AsyncAPI, Protobuf, JSON Schema) and whether it is generated from code or maintained by hand.
- **Schema validation**: whether request bodies are validated against the schema and rejected when malformed.
- **Response consistency**: whether responses use a consistent envelope and types across endpoints.
- **Error standardization**: whether errors follow a standard such as RFC 7807 (Problem Details for HTTP APIs) with `type`, `title`, `status`, `detail`, and `instance` fields, rather than ad hoc bodies.
- **Versioning**: whether the API has a versioning strategy (path, header, or media type).
- **Spec-to-code agreement**: whether the specification matches the implemented behavior, including auth requirements per endpoint.
- **OWASP API Security Top 10 (2023)**: whether the contract guards against the API-specific risk categories.

## OWASP API Security Top 10 (2023) Reference

Use these category codes when an API security gap maps to one:

| Code | Category |
|------|----------|
| API1:2023 | Broken Object Level Authorization |
| API2:2023 | Broken Authentication |
| API3:2023 | Broken Object Property Level Authorization |
| API4:2023 | Unrestricted Resource Consumption |
| API5:2023 | Broken Function Level Authorization |
| API6:2023 | Unrestricted Access to Sensitive Business Flows |
| API7:2023 | Server-Side Request Forgery |
| API8:2023 | Security Misconfiguration |
| API9:2023 | Improper Inventory Management |
| API10:2023 | Unsafe Consumption of APIs |

## Evidence To Look For

| Signal | Where It Appears |
|--------|------------------|
| API specification | `openapi.yaml`, `*.proto`, schema files, generated docs |
| Schema enforcement | Validation middleware, typed deserialization, rejected-input tests |
| Error format | Centralized error responses, problem-details types |
| Versioning | Version in path, header, or media type |
| Spec drift | Spec declarations that differ from implemented behavior |

## Status Criteria

- `PASS`: A specification exists, is enforced, errors are standardized, versioning is defined, and the spec matches the code, with evidence.
- `PARTIAL`: A specification exists but enforcement, error standardization, versioning, or spec-to-code agreement is incomplete.
- `FAIL`: No specification where the API surface clearly requires one, or the spec broadly contradicts the code, with evidence.
- `UNKNOWN`: API artifacts were not provided.
- `N/A`: The system exposes no API, with justification.

## How To Present

Render this as a standalone section, as described in `process/report-format.md`, only when the system exposes an API. Present a conformance table across the evaluated dimensions, then describe each gap with evidence and its linked `FND-XXX`.

## Rules

- Anchor every conformance gap to a specific endpoint, schema, or spec line.
- When the spec contradicts the code, record it as a drift finding citing both sides.
- Map each API security gap to its OWASP API Security Top 10 (2023) code where one applies.
- Do not assume a control is present because the spec mentions it; confirm enforcement in code.
