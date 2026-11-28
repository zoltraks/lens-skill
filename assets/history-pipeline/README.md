# History Pipeline

## Purpose

> **Scope:** The reference extraction pipeline for `process/history-visualisation.md`.

> **Key items:** stages, configuration, continuation, adaptation

Copy the four scripts into `<workspace>/gathering/scripts/` and run them in order from there.

The scripts are standard library only and read the target through `git`.

They never write to the target repository.

## Stages

| Script             | Output under `gathering/out/`                                                          |
|--------------------|----------------------------------------------------------------------------------------|
| `common.py`        | Shared helpers - configuration, buckets, modules, commit classifier                    |
| `extract_git.py`   | `commits.json`, `commit-events.json`, `eras.json`, `churn.json`, `dependencies.json`   |
| `extract_docs.py`  | `records.json`, `changelog.json`, and `gathering/notes/inventory.json`                 |
| `build_history.py` | `<workspace>/out/history.json`, `history.js`, `manifest.json`, `notes/unassigned.json` |

## Configuration

The scripts read `gathering/config.json`:

| Key                 | Meaning                                                                   |
|---------------------|---------------------------------------------------------------------------|
| `repo`              | Target repository, absolute or relative to `gathering/`                   |
| `ref`               | Ref to gather, `HEAD` by default                                          |
| `prior`             | Prior dataset whose view, project identity, and categories carry forward  |
| `view`, `project`   | Explicit presentation and identity values, winning over the prior dataset |
| `from_version`      | Continuation scope - eras before this version are skipped                 |
| `version_manifests` | Manifest paths to read, discovered from history when absent               |
| `docs_families`     | `root`, `top`, and `dirs` maps from paths to record families              |
| `categories`        | Registry to use when no prior dataset exists                              |

## Continuation

Set `from_version` to the anchor `scripts/continue-history.py plan` reports.

The output then starts at the anchor, and `scripts/continue-history.py merge` splices it onto the
prior dataset.

## Adaptation

Edit the header line of each copied script to name the actual target.

Adjust `docs_families` to the target's documentation layout before editing code.

Change the scripts only for evidence the configuration cannot express, and record the change in
the workspace steps log.
