# Agent Configuration Format Corpus

## Purpose

> **Scope:** Checkable constraints for agent-facing configuration formats other than `SKILL.md`,
> used as the conformance baseline for the Skill Definition Conformance assessment
> **Key items:** memory files, rules directories, plugin manifests, subagent definitions,
> instruction files, MCP configuration, per-format baselines, live-check procedure

This file distills the documented constraints of each agent-facing configuration format into what
an audit can check mechanically.

`references/agent-skills.md` covers `SKILL.md` itself.

This file covers every other format discovered during agent-facing artifact discovery.

`assessment/skill-definition.md` consumes this file.

## Sources And Baselines

Each format section names its authoritative documentation.

Record which baseline was used for each format in the report's evidence: the snapshot below or a
live fetch of the named source.

Snapshot date: 2026-09-27.

When web fetch is available during the audit, retrieve the named source and compare its headline
constraints against the snapshot.

When the fetched source differs, record the live constraints as that format's baseline and note
the drift in the report's Limitations and Unknowns.

The check is best-effort and never executes anything against the audited subject.

## AGENTS.md

Authoritative source: `https://agents.md/`, stewarded by the Agentic AI Foundation.

An `AGENTS.md` file is standard Markdown with no required fields or fixed sections.

Checkable constraints:

- Location: repository root, or nested inside a package directory, where the nearest file to the
  edited path takes precedence.
- Content is plain Markdown, free-form headings.
- Recommended coverage: project overview, setup and test commands, code style, and contribution
  or review instructions. Missing coverage is a quality observation, not a violation.
- Legacy spelling `AGENT.md` is a deviation: the convention is to rename to `AGENTS.md` and keep
  a compatibility symlink.
- Every file path referenced inside the file must resolve.

## CLAUDE.md And Memory Files

Authoritative source: `https://code.claude.com/docs/en/memory`.

`CLAUDE.md` is the Claude Code memory file, plain Markdown.

Checkable constraints:

- Location: repository root or `.claude/CLAUDE.md`. A `~/.claude/` file is user-level and outside
  repository scope.
- Imports use `@path/to/file` syntax, resolve relative to the file containing the import, allow
  absolute paths, and recurse to a maximum depth of 5 hops. Every import path must resolve.
- `CLAUDE.local.md` is deprecated: its presence is a conformance finding recommending migration
  to `CLAUDE.md` or imports.
- `.claude/rules/*.md` files are path-scoped rules with optional `paths:` frontmatter, discovered
  recursively. A `paths:` pattern that matches no file in the repository is a dead rule worth a
  finding.

## Cursor Rules

Authoritative source: `https://cursor.com/docs/rules`.

Cursor project rules live in `.cursor/rules/` as `.mdc` files.

Checkable constraints:

- A rule file must use the `.mdc` extension. A plain `.md` file inside `.cursor/rules/` is ignored
  by the rules engine, a conformance finding.
- Frontmatter fields: `description`, `globs`, `alwaysApply`.
- `alwaysApply: true` ignores `description` and `globs`. Setting them anyway is dead configuration.
- `alwaysApply: false` with `globs` attaches the rule on matching files. `alwaysApply: false`
  with only `description` defers to agent judgment. `alwaysApply: false` with neither field makes
  the rule manual-only.
- A `globs` pattern that matches no repository file is a dead rule.
- Legacy `.cursorrules` at the repository root is deprecated: recommend migration to `.mdc` files.

## Windsurf And Devin Rules

Authoritative source: `https://docs.devin.ai/windsurf/plugins/cascade/memories`.

Workspace rules are Markdown files with frontmatter, stored per file.

Checkable constraints:

- Location: `.devin/rules/*.md` is the current location, `.windsurf/rules/*.md` is the backward-
  compatible fallback. Both in one repository is a duplication finding.
- Required frontmatter field `trigger`, one of `always_on`, `model_decision`, `glob`, `manual`.
- `trigger: glob` requires a `globs` field. `trigger: model_decision` should carry a `description`.
- A `globs` pattern matching no repository file is a dead rule.
- Each workspace rule file is limited to 12,000 characters. A file over the limit is truncated.
- Legacy `.windsurfrules` at the repository root is deprecated: recommend migration to rule files.
- `~/.codeium/windsurf/memories/global_rules.md` is user-level and outside repository scope.

## Claude Plugin Manifests

Authoritative source: `https://code.claude.com/docs/en/plugins-reference`.

A plugin is a directory that may carry `.claude-plugin/plugin.json`.

Checkable constraints:

- The manifest is optional. When absent, components are auto-discovered from `skills/`,
  `agents/`, `hooks/`, `commands/`, and `.mcp.json`, and the plugin name derives from the
  directory name.
- When present, `plugin.json` must be valid JSON and must contain `name`. `version`,
  `description`, `author`, `homepage`, `repository`, `license`, and `keywords` are optional.
- Component-path fields (`skills`, `commands`, `agents`, `hooks`, `mcpServers`, `outputStyles`,
  `lspServers`) are strings or string arrays whose paths must resolve.
- `commands/` is a legacy format: new functionality belongs in `skills/`.
- Portable references inside the plugin use `${CLAUDE_PLUGIN_ROOT}`, never absolute paths.
- A `marketplace.json` under `.claude-plugin/` describes a plugin catalog, not a plugin.

## Claude Subagent Definitions

Authoritative source: `https://code.claude.com/docs/en/subagents`.

Subagents are Markdown files with YAML frontmatter under `.claude/agents/`, discovered
recursively.

Checkable constraints:

- `name` and `description` are required frontmatter fields.
- Optional fields: `tools`, `disallowedTools`, `model`, `skills`, `memory`, `background`,
  `isolation`. The only valid `isolation` value is `worktree`.
- `hooks`, `mcpServers`, and `permissionMode` are not supported on plugin-shipped agents.
- The `description` drives delegation and should state when to use the agent.
- Duplicate `name` values across `.claude/agents/` directories make the nearest definition win,
  which hides the others.

## Copilot Instructions

Authoritative source: `https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions`.

Checkable constraints:

- Repository-wide instructions live at `.github/copilot-instructions.md`.
- Path-specific instructions live under `.github/instructions/` as `*.instructions.md` files
  whose frontmatter `applyTo` carries the path glob. A missing `applyTo` or a glob matching no
  repository file is a dead instruction.
- `excludeAgent` may scope a file away from a specific Copilot surface.
- Copilot also reads `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as agent instructions, so their
  constraints apply unchanged.

## MCP Server Configuration

Authoritative source: the Model Context Protocol documentation at `https://modelcontextprotocol.io`.

Checkable constraints:

- MCP server definitions live in `.mcp.json` (or the client-specific equivalent) as a
  `mcpServers` map keyed by server name.
- A stdio server entry carries `command`, optional `args`, and optional `env`. The `command`
  must name an executable the project documents or vendors.
- A remote server entry carries `url` and a transport `type` such as `http` or `sse`.
- `env` blocks must not embed plaintext secrets. A literal token value is a security finding,
  an environment-variable reference such as `${VAR}` is the expected form.

## Best-Practice Signals

Signals that apply across formats:

- Every agent-facing file references only paths that resolve.
- Deprecated flat files are migrated rather than left alongside the modern layout.
- Agent-facing configuration kept out of version control (`CLAUDE.local.md`, user-level files)
  is documented as intentional when it appears inside the repository.
- Instructions that conflict across formats for the same scope are a finding, regardless of
  which file an agent happens to load first.
