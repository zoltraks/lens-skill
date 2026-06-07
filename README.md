# Lens - Software Audit Skill

<p align="center">
  <b>Agent Skill</b> for Windsurf · Cursor · Claude Code · Gemini CLI · OpenCode · GitHub Copilot CLI
</p>

> Structured, evidence-based engineering audits of any software subject - prototypes, codebases under development, and already-running production systems. Drop-in skill for any AI coding agent that supports SKILL.md.

This is an [Agent Skill](https://www.mintlify.com/blog/skill-md) - a folder of instructions any compatible AI coding agent loads on demand. When you ask for a software audit, architecture audit, production code audit, technical due diligence, or readiness assessment, this skill provides a fixed process, a table-driven report format, and per-category checklists for producing a neutral, repeatable assessment.

---

## What you get

The skill produces a consistent audit report with these sections, each presented as a table: technology stack, executive summary, system context, quality assessment, risk register, project scorecard, trade-off analysis, and recommendation summary. Section headings are unnumbered.

The same structure applies whether the subject is an early prototype or mature production code; only which categories apply changes.

Every audit is governed by strict rules:

- **Evidence only** - findings must trace to a concrete fact in the input.
- **No assumptions** - missing information is marked `UNKNOWN`, `NOT SPECIFIED`, or `INSUFFICIENT INFORMATION`.
- **No personal judgement** - the report evaluates the system, never the people who built it.
- **Architectural neutrality** - choices are judged within stated constraints, not against a favored stack.
- **Contextual applicability** - categories that cannot apply to the system's deployment model are marked `N/A` with justification, not treated as failures.

When you ask for a full audit without naming an output file, the agent asks once whether to return the report inline or write it to a file you name. Name a file in your request to skip the question.

Each topic file is self-contained and follows the same structure: a purpose block, what to evaluate, evidence to look for, status criteria, common risks, and confidence signals.

---

## When to use this skill

| Situation                                        | Use this skill?                          |
|--------------------------------------------------|------------------------------------------|
| "Audit the architecture of this system"          | **Yes**                                  |
| "Audit this production codebase"                  | **Yes**                                  |
| "Review this prototype for production readiness"  | **Yes**                                  |
| "Do technical due diligence on this codebase"     | **Yes**                                  |
| "Audit our dependencies and supply chain"         | **Yes** - use `assessment/dependencies.md` |
| "Build me a risk register and scorecard"          | **Yes**                                  |
| "Review only the security posture"               | **Yes** - single-dimension audit          |
| "Compare these two architectural options"         | **Yes** - use `synthesis/trade-off-analysis.md` |
| "Write the feature for me"                        | No - this skill assesses, it does not build |
| "Tell me which team member caused this"           | No - this skill never evaluates people    |

---

## Install

### Windsurf / Cursor / VS Code (Cline, Roo Code)

Project install - committed to a repo, shared with your team:

```bash
git clone https://github.com/YOURNAME/lens-skill .windsurf/skills/lens
```

Or use the cross-tool `.agents/skills/` path:

```bash
git clone https://github.com/YOURNAME/lens-skill .agents/skills/lens
```

### Claude Code - manual clone

Personal install (available in all your projects):

```bash
git clone https://github.com/YOURNAME/lens-skill \
  ~/.claude/skills/lens
```

Project install:

```bash
git clone https://github.com/YOURNAME/lens-skill \
  .claude/skills/lens
```

### Gemini CLI

```bash
gemini skills install https://github.com/YOURNAME/lens-skill
```

Or manual:

```bash
git clone https://github.com/YOURNAME/lens-skill /tmp/lens-skill
cp -r /tmp/lens-skill ~/.gemini/skills/lens
```

### OpenCode

```bash
git clone https://github.com/YOURNAME/lens-skill ~/.config/opencode/skills/lens
```

Or use the Claude-compatible path:

```bash
git clone https://github.com/YOURNAME/lens-skill ~/.claude/skills/lens
```

### GitHub Copilot CLI

```bash
gh skill install YOURNAME/lens-skill lens
```

---

## Example prompts

**Full audit**
> Audit this production codebase. Produce a full engineering assessment with a risk register, scorecard, trade-off analysis, and recommendation options.

**Audit to a file**
> Perform lens on this service and write the audit report to AUDIT.md.

**Audit without a named file**
> Make audit report on this codebase. (The agent will ask whether to reply inline or write to a file you name.)

**Readiness assessment**
> Is this system production-ready? Assess testing, deployment, rollback, observability, and operational readiness, and state the maturity level with evidence.

**Single dimension**
> Review only the security posture of this codebase. Mark anything you cannot determine from the provided files.

**SOLID and testability**
> Assess this codebase against SOLID principles and its testing strategy: test pyramid balance, TDD signals, and how testable the code is.

**Dependency and supply-chain audit**
> Audit the dependencies of this project: flag outdated and vulnerable packages, license compatibility, and whether builds are locked and reproducible.

**Risk register**
> Build a risk register for this architecture proposal. Use Low / Medium / High / Critical severities and tie each risk to evidence.

**Trade-off analysis**
> Compare keeping in-memory state versus introducing an external store for this prototype, given a single-instance target.

**Thin input**
> Here is a one-paragraph description of a service. Audit what you can and list exactly what additional artifacts would raise confidence.

---

## What's inside

```
lens-skill/
├── SKILL.md                       # Root router - load this first
├── principles/
│   ├── evaluation-rules.md        # Evidence-only, no assumptions, neutrality, status markers, constraints
│   └── output-style.md            # Tone, fixed vocabularies, consistency, determinism
├── process/
│   ├── workflow.md                # Intake, scope, evidence, assessment, synthesis, validation
│   └── report-format.md           # The table-driven, unnumbered report template
├── assessment/
│   ├── testing.md                 # Test pyramid (unit/integration/e2e), TDD, coverage, testability
│   ├── design-principles.md       # SOLID, cohesion and coupling, DRY, separation of concerns
│   ├── code-quality.md            # Static analysis, type safety, complexity, duplication, dead code
│   ├── dependencies.md            # Dependency freshness, vulnerabilities, licenses, lockfiles, SBOM
│   ├── deployment.md              # Build pipeline, release process, frequency, manual steps
│   ├── rollback.md                # Rollback mechanism, deploy safety, versioning
│   ├── maintainability.md         # Modularity, coupling, structure, technical debt
│   ├── change-management.md       # Feature flags, ADRs, release governance
│   ├── documentation.md           # Entry, API, inline docs, onboarding, knowledge transfer
│   ├── nfr.md                     # Performance, scalability, availability, reliability, resilience
│   ├── security.md                # Auth, authorization, input validation, OWASP, data exposure
│   ├── compliance.md              # Data protection, privacy, regulatory scope, licensing, audit trail
│   ├── observability.md           # Logging, metrics, tracing, alerting
│   ├── error-handling.md          # Exceptions, retries, fallbacks, user-facing errors
│   └── operational-readiness.md   # Runbooks, on-call, capacity, backups, incident response
└── synthesis/
    ├── risk-register.md           # Risk table, impact and likelihood, severity scale
    ├── scorecard.md               # 0-5 project scorecard and rubric
    ├── trade-off-analysis.md      # Surfacing and presenting trade-offs as a table
    └── recommendations.md         # Non-prescriptive options with pros, cons, risk level
```

The skill activates automatically when you ask for a software audit, architecture audit, production code audit, technical due diligence, readiness assessment, risk register, scorecard, or trade-off analysis.

---

## License

MIT - see [LICENSE](./LICENSE).

---

## Credits

Built by Filip Golewski.

If you use this skill in a project, a link back is appreciated but not required.
