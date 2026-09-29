# JSON Parameter Exchange

## Purpose

> **Scope:** Emit and consume machine-readable parameter documents in place of, or alongside,
> the question surfaces in `process/audit-workflow.md`
> **Key items:** emission trigger, diagnostic output, emitted document, parameter catalog,
> returned document, authority

This file defines how Lens exposes its intake questions as JSON and how it consumes JSON answers.

## When to Emit

When the request asks for the questions, settings, or parameters "in JSON", "as JSON", or another
machine-readable format, emit a parameter document instead of the question menus and checkbox
lists.

Repository discovery and the blocking-gate conditions still run first: the document contains only
the questions that are actually pending in this session.

Emit the document where the request directs - inline in the response by default.

## Diagnostic Output

When the request names a debugging mode, a diagnostic mode, or asks for detailed or verbose
information, emit the parameter document for information purposes only.

The emission order is fixed: the JSON document first, then a text description of the pending
decisions, then the question menus.

The question menus still run - the emitted document does not replace the question flow.

Answers may still arrive as menu selections, natural-language responses, or a returned document.

The same emission applies when diagnostics are implied: a malformed returned document, an
unresolved parameter conflict, or an intake validation failure may accompany the parameter
document and a text note, while the menus proceed.

## Emitted Document

The document carries a `description`, context fields (`project`, `mode`, `date`, `time`), and an
`intake` array.

- `project` - the audited subject or directory name.
- `mode` - `audit` or `review`, per the report type resolved at intake.
- `date` - the current day in `YYYY-MM-DD` format.
- `time` - the local time in `hh:mm:ss` followed by the timezone offset, for example
  `13:45:21 GMT+2`.

Each parameter object keeps a fixed key order: `id`, `question`, `answer`, `description`, `type`,
`menu`, `open`, `default` - the `default` key is always the last key of the object.

- `id` - a stable kebab-case identifier for the parameter.
- `question` - the literal question wording presented to the answering side.
- `answer` - emitted as an empty string (an empty array for `selection`), to be filled by the
  answering side.
- `description` - what the parameter controls and the discovery evidence behind its default.
- `type` - `choice` for a single-option answer, `selection` when multiple options may be chosen,
  or `text` for free input.
- `menu` - required for `choice` and `selection` types and omitted for `text`, letter-keyed (`A`,
  `B`, `C`, ...), and the recommended option label carries "(recommended)".
- `open` - whether the answer is open to free text beyond the listed options.
- `default` - the option letter or suggested text applied when the answer stays empty; for
  `selection`, the array of letters that are pre-checked.

Routine prompts' trailing `Use default: <value>` and `Use defaults for all remaining questions`
options do not become `menu` entries - the `default` key and the returned document's "use
defaults" semantics cover them.

```json
{
    "description": "Intake parameters for <project>",
    "project": "<name>",
    "mode": "audit",
    "date": "2026-09-30",
    "time": "13:45:21 GMT+2",
    "intake": [
        {
            "id": "audit-mode",
            "question": "A previous report AUDIT-1.0.md was found - which audit mode should this run use?",
            "answer": "",
            "description": "Controls baseline comparison and identifier continuity; the found report appears to cover the same subject.",
            "type": "choice",
            "menu": {
                "A": "Re-audit - compare against AUDIT-1.0.md (recommended)",
                "B": "Re-audit with changed parameters - compare but reconfigure",
                "C": "Fresh audit - ignore the previous report's content"
            },
            "open": false,
            "default": "A"
        },
        {
            "id": "project-inclusion",
            "question": "Multiple projects were found - which should the audit include?",
            "answer": [],
            "description": "One option per discovered project; installed or external entries are listed but unchecked by default.",
            "type": "selection",
            "menu": {
                "A": "`src/service/` - application",
                "B": "`skills/search/` - authored skill",
                "C": "`.claude/skills/vendor-tool/` - skill (installed/external)"
            },
            "open": false,
            "default": ["A", "B"]
        },
        {
            "id": "detail-level",
            "question": "Which detail level should the report use?",
            "answer": "",
            "description": "Controls section breadth; Detailed is the recommended default.",
            "type": "choice",
            "menu": {
                "A": "Brief",
                "B": "Standard",
                "C": "Detailed (recommended)"
            },
            "open": false,
            "default": "C"
        }
    ]
}
```

## Parameter Catalog

Every pending question surface emits with a stable kebab-case `id`:

| Parameter               | Type        | Surface in `process/audit-workflow.md`                                     |
|-------------------------|-------------|----------------------------------------------------------------------------|
| `audit-mode`            | `choice`    | Re-audit, changed-parameters, or fresh-audit gate and its confirm variants |
| `skills-scope`          | `choice`    | Assess embedded skills as components or independent projects               |
| `project-inclusion`     | `selection` | Checkbox list of discovered projects, recommended set pre-checked          |
| `cancel-confirmation`   | `choice`    | Emitted only when a returned or selected all-unchecked answer cancels      |
| `parameters-acceptance` | `choice`    | Accept default parameters or configure                                     |
| `parameters-to-change`  | `selection` | Re-audit-with-changed-parameters follow-up naming core parameters          |
| `report-delivery`       | `choice`    | Delivery and output-file prompt                                            |
| `detail-level`          | `choice`    | Brief, Standard, or Detailed                                               |
| `evaluation-scale`      | `choice`    | All five scale options in their fixed order                                |

Thin-input clarifications emit as `text` or `choice` parameters as they arise, with `open: true`
when free input is appropriate.

## Returned Document

The answering side returns a document keeping a `response` key - either an array of entry objects
or a condensed object keyed by parameter `id`.

Each array entry requires only `id` and `answer` - an option letter for `choice`, an array of
letters for `selection`, or free text for `text`.

Other keys may be echoed or omitted.

In the condensed form, each key is a parameter `id` and each value is its `answer`.

An empty or missing `answer` - including an `id` absent from the condensed object - applies the
parameter's `default`.

Entries or keys with an unknown `id` are ignored.

Answering "use defaults" applies every `default` value.

A returned document is accepted whenever it appears - on any question surface, on its own or
embedded inside a natural-language reply.

Answers are applied from the `response` value; natural language surrounding the document is
treated as supplementary context, not as part of the answers.

```json
{
    "response": [
        {
            "id": "audit-mode",
            "answer": "A"
        },
        {
            "id": "project-inclusion",
            "answer": ["A", "B"]
        },
        {
            "id": "detail-level",
            "answer": "C"
        }
    ]
}
```

The same answers in the condensed form:

```json
{
    "response": {
        "audit-mode": "A",
        "project-inclusion": ["A", "B"],
        "detail-level": "C"
    }
}
```

## Authority

The JSON format is a presentation format, not an authority change.

Every gate still follows `process/audit-workflow.md`: blocking gates still wait for an answer,
and returned documents answer the same questions the menus would have asked.

An orchestrating agent may emit and consume these documents without human interaction, and every
automated decision is still recorded as answered through the exchange.
