# Operation Timing

## Purpose

> **Scope:** Elapsed-time and context reporting for operations, armed by default on every
> operation the skill answers.

> **Key items:** default arming, reporting modes, closing report, breakdown, heartbeat, identity

This file defines how Lens closes an operation with its time and context report.

## Trigger

Timing is armed by default on every operation the skill answers - local activation and task
execution alike. Naming `no timing`, `without timing`, or an equivalent opt-out disarms it for that
request only.

| Mode            | Adds to the closing report                                        |
|-----------------|-------------------------------------------------------------------|
| `timing`        | Operations table                                                  |
| `context usage` | Context line, then the operations table                           |
| `verbose`       | Operations table, and the parameter document for pending surfaces |
| `diagnostic`    | Same as `verbose`                                                 |
| `informational` | Nothing beyond the timing sentence                                |

`timing` and `context usage` never load `process/json-exchange.md` - only `verbose`, `diagnostic`,
or an explicit JSON request emit the parameter document, which that file owns.

A mode named on a request without a task stays armed for the session and closes every later
operation. A mode named on a task request applies to that request only.
Modes are named in the request text, never resolved from environment variables.

## Timing

The agent notes the system clock before starting the operation's work.

## Report

The closing elements print in this order, each a separate block divided by exactly one blank line:

1. Context line - `context usage` only: `Context in use: <n>k tokens`, with the window share when
   the window size is known.
2. Breakdown table - operations past three minutes only, per Performance Analysis.
3. Operations table - `timing`, `context usage`, `verbose`, and `diagnostic` only,
   one row per operation the session has run:

   | Operation | Time     | Context  |
   |-----------|----------|----------|
   | `<name>`  | `<m:ss>` | `+<n>k`  |

   `Context` is what the operation consumed, in tokens or as a window share.
4. Timing sentence - `<description> operation took <m:ss>`, the last sentence of the response,
   where `<description>` names the operation the last request asked for.

Counters come from the host - a token counter it reports, or one it records in its own session store
or logs. An estimate is marked `~`. A counter the environment does not expose is omitted entirely,
never reported as `unknown` or another placeholder.
Context usage never rides along on a response whose request armed no such mode.

## Performance Analysis

An operation that runs longer than three minutes closes with a breakdown table placed before the
operations table and the timing sentence.

| Stage    | Elapsed  | Share  | Note                            |
|----------|----------|--------|---------------------------------|
| `<name>` | `<m:ss>` | `<n>%` | what consumed or saved the time |

Stage times come from command-reported elapsed values, recorded clock captures, or output timestamps.
When none exists, the note says so instead of guessing.

## Progress Heartbeat

While a backgrounded command runs past about a minute, the agent reports progress roughly every
60 seconds in one short line - current stage, items done of the total, and warnings seen.
A poll that finds no new output still earns a brief "still in <stage>" line.

## Agent Identity

The driving agent and model are named once per session - on the first report carrying an operations
table - and again whenever a request asks for them, as a separate paragraph.
Detection follows a ladder: an explicit value in the request, the tool's own namespace variables,
known environment markers (`AI_AGENT` carrying `devin` proves Devin,
`CLAUDECODE` and `CLAUDE_CODE_*` prove Claude Code, `CODEX_*` proves Codex,
`CURSOR_TRACE_ID` proves Cursor, `ANTIGRAVITY_*` proves AntiGravity, `GEMINI_CLI` proves Gemini,
`QWEN_CODE` proves Qwen, a `windsurf` `ACP_BACKEND` proves a Windsurf-family host),
configured settings keys, then agent self-declaration. An unresolved value reports `unset`.

## Coverage

Bare activation times readiness and the update check when it runs.
Task requests time the task work.
