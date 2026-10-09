# MCP Server Baseline

## Purpose

> **Scope:** Checkable constraints for servers that expose tools to agents over the Model
> Context Protocol
> **Key items:** stdio stream ownership, tool manifest single-sourcing, input schemas,
> permission gating, bounded invocation, structured results, surface parity

This file distills the Model Context Protocol specification and the official C# and Rust SDK
sources listed in `references/source-catalog.md` into constraints an audit can verify from
repository source.

Snapshot date: 2026-10-09.

Feeds `assessment/baseline-conformance.md`, `assessment/api-contract.md`, and
`assessment/security-review.md` for subjects classified `agent-tooling` in
`references/domain-profiles.md`.

## Transport Ownership

From https://modelcontextprotocol.io/specification/latest and the transport documentation of
the official SDKs.

- On the stdio transport, stdout belongs to the JSON-RPC protocol stream. Any log line,
  banner, or diagnostic written to stdout corrupts the protocol - all logging is redirected
  to stderr or a file before the server starts.
- Transport, session bookkeeping, and JSON-RPC dispatch live outside the tool layer. A tool
  handler must not know which transport delivered it.
- Shutdown drains: the server stops accepting calls, lets in-flight handlers finish within a
  bounded timeout, then runs application cleanup.

## Tool Surface Contract

- Tool names are stable identifiers (`snake_case` verb-noun form). Renaming a tool breaks
  every configured client, so names are chosen once and renames are treated as breaking
  changes.
- The tool description is the only context the calling agent receives. It must state what the
  tool returns, its provider or target, and every side effect - a state-changing parameter
  that is not disclosed is a contract defect.
- A single authoritative registry or manifest binds each tool's name, description, permission,
  input schema, and handler in one place, so adding a tool is a one-line change and the listed
  surface cannot drift from the implemented surface.
- Feature-gated tools still appear in the manifest and return a descriptive error at call
  time, so clients see a stable surface instead of a shape that changes with configuration.

## Input And Execution

- The embedded JSON Schema is the source of truth for a tool's arguments. Deserialized
  arguments validate against it - or schema-shaped types make drift impossible - and unknown
  fields are rejected rather than ignored.
- Shared argument shapes are parsed through shared helpers, not hand-rolled per handler,
  because per-handler extraction drifts error messages and defaults.
- Permission checks run at dispatch before the handler. A principal lacking the tool's
  permission receives a descriptive protocol-level error, never a generic failure.
- Every invocation that reaches external state is bounded by a timeout with a kill fallback -
  the caller cannot cancel a wedged child process any other way.
- Failures map to protocol-level errors (`isError` results or equivalent exceptions), never a
  successful payload carrying an error field. A wrapped service's own stderr or error JSON is
  the better message than an invented one.

## Surface Parity

- Where the same capability is exposed over several surfaces (a CLI plus MCP tools, or REST
  plus MCP), each handler delegates to the same domain port and returns the same contract,
  so the surfaces cannot diverge in behavior.
- A CLI-wrapping server passes the machine-format flag unconditionally, builds arguments as a
  list rather than a shell string, resolves sibling executables beside the running process
  (not a bundled extraction directory), and pins cwd-relative defaults through the
  environment only where the child would not resolve them itself.
- Argument construction is a pure function a test can pin to an exact argv, so a flag added
  to one surface fails the test until it lands on the other.
- Help text and tool descriptions are authored for the same audience and kept in sync -
  drift between them produces wrong agent behavior.

## Verification

- A stdio server is smoke-checked by sending `initialize`, `tools/list`, and one `tools/call`
  on stdin and confirming protocol responses on stdout with nothing else writing there.
- Manifest tests assert every tool name is unique, every schema validates, and gated tools
  still appear. Permission tests assert dispatch rejects an under-privileged principal.

## Live Check

When web fetch is available, compare the pinned SDK's implemented spec revision against
https://modelcontextprotocol.io/specification/latest and record the pairing.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
