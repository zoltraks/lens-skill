#!/usr/bin/env python3
"""Continue a history dataset from a previously generated visualisation.

A prior artifact - a packed single-file HTML visualisation, a `history.json`,
or a `history.js` shim - already carries every era up to its last version.
Repository history may since have been truncated by retention, archiving,
or a rewrite, so a fresh full gather can lose eras the prior artifact still
holds. Continuation keeps those eras and re-gathers only the last included
version and anything newer.

Two subcommands:

  plan   Read the prior dataset and the repository, pick the anchor - the
         last non-planned version of the prior dataset - and report what is
         kept, where gathering starts, and which prior commits still resolve.
  merge  Splice a dataset gathered from the anchor onward onto the kept prior
         eras, carrying the prior settings (view, project identity, category
         registry), and write the continued dataset.

Usage:
  python scripts/continue-history.py plan --prior old.html --repo path/to/repo [--ref HEAD]
  python scripts/continue-history.py merge --prior old.html --update new-history.json \
      --out history.json [--plan plan.json]

The repository is read with `git` only - nothing is written to it. The prior
artifact is never modified.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

MARKER = "window.HISTORY_DATA = "
CARRIED_PROJECT = ("name", "description", "repository")


def vkey(version: str) -> tuple:
    numbers = re.findall(r"\d+", version or "")
    return tuple(int(n) for n in numbers[:3]) or (0,)


def load_dataset(path: Path) -> dict:
    """Read `history.json`, a `history.js` shim, or a packed HTML visualisation."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        pos = 0
        while True:
            start = text.find(MARKER, pos)
            if start == -1:
                raise SystemExit(f"continue-history: no embedded dataset in {path}")
            start += len(MARKER)
            if text[start:start + 1] == "{":
                break
            pos = start
        end = text.find("</script>", start) if path.suffix.lower() in (".html", ".htm") \
            else len(text)
        payload = text[start:end].strip().rstrip(";")
        data = json.loads(payload)
    if not isinstance(data.get("versions"), list) or not isinstance(data.get("categories"), list):
        raise SystemExit(f"continue-history: {path} is not a history dataset")
    return data


def anchor_of(prior: dict) -> int:
    """Index of the last prior version with code evidence - the first one to re-gather."""
    for index in range(len(prior["versions"]) - 1, -1, -1):
        version = prior["versions"][index]
        if version.get("kind") not in ("planned", "changelog") and version.get("range"):
            return index
    raise SystemExit("continue-history: the prior dataset has no version with a commit range")


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def exists(repo: Path, sha: str) -> bool:
    return bool(sha) and git(repo, "cat-file", "-e", f"{sha}^{{commit}}").returncode == 0


def plan(prior: dict, repo: Path, ref: str) -> dict:
    versions = prior["versions"]
    anchor = anchor_of(prior)
    head = git(repo, "rev-parse", ref).stdout.strip()
    previous = versions[anchor - 1] if anchor else None
    start = (previous or {}).get("range", {}).get("to")
    start_ok = exists(repo, start) if start else False
    anchor_from = versions[anchor].get("range", {}).get("from")
    result = {
        "anchor": versions[anchor]["version"],
        "anchor_index": anchor,
        "kept": [v["version"] for v in versions[:anchor]],
        "dropped": [v["version"] for v in versions[anchor:]],
        "prior_generated": prior.get("project", {}).get("generated"),
        "prior_head": prior.get("project", {}).get("head"),
        "prior_head_found": exists(repo, prior.get("project", {}).get("head", "")),
        "first_commit_found": exists(repo, (versions[0].get("range") or {}).get("from", "")),
        "ref": ref, "head": head,
        "gather_from": start if start_ok else None,
        "gather_range": f"{start}..{head}" if start_ok else head,
        "anchor_from_found": exists(repo, anchor_from) if anchor_from else False,
    }
    if start_ok:
        count = git(repo, "rev-list", "--count", f"{start}..{head}").stdout.strip()
        result["commits_to_gather"] = int(count or 0)
    result["truncated_history"] = not result["first_commit_found"]
    result["settings"] = {
        "view": prior.get("view", {}),
        "project": {k: prior.get("project", {})[k] for k in CARRIED_PROJECT
                    if k in prior.get("project", {})},
        "categories": len(prior["categories"]),
        "grouping": prior.get("project", {}).get("grouping"),
    }
    if not start_ok:
        result["warning"] = ("the boundary before the anchor no longer resolves - gather the "
                             "anchor version by its version signal or fall back to a full run")
    return result


def days_between(earlier: str, later: str) -> int:
    a = datetime.fromisoformat(earlier[:10])
    b = datetime.fromisoformat(later[:10])
    return max(0, (b - a).days)


def merge(prior: dict, update: dict) -> tuple[dict, dict]:
    anchor = anchor_of(prior)
    anchor_version = prior["versions"][anchor]["version"]
    kept = prior["versions"][:anchor]
    fresh = [v for v in update["versions"]
             if v.get("kind") == "planned" or vkey(v["version"]) >= vkey(anchor_version)]
    if not fresh:
        raise SystemExit(f"continue-history: the update holds no version from {anchor_version} on")
    offset = 0
    last_span = next((v["commit_span"] for v in reversed(kept) if v.get("commit_span")), None)
    first_fresh = next((v["commit_span"] for v in fresh if v.get("commit_span")), None)
    if last_span and first_fresh:
        offset = last_span[1] + 1 - first_fresh[0]
    merged_fresh = []
    for version in fresh:
        version = json.loads(json.dumps(version))
        if version.get("commit_span"):
            version["commit_span"] = [version["commit_span"][0] + offset,
                                      version["commit_span"][1] + offset]
        merged_fresh.append(version)
    previous = next((v for v in reversed(kept) if v.get("dates")), None)
    first = next((v for v in merged_fresh if v.get("dates")), None)
    if previous and first:
        first["gapDays"] = days_between(previous["dates"]["to"], first["dates"]["from"])
    categories = list(prior["categories"])
    known = {c["id"] for c in categories}
    used = {e["type"] for v in merged_fresh for e in v.get("events", [])}
    for category in update["categories"]:
        if category["id"] not in known and category["id"] in used:
            categories.append(category)
    project = dict(update.get("project", {}))
    for key in CARRIED_PROJECT:
        if key in prior.get("project", {}):
            project[key] = prior["project"][key]
    kept_commits = sum((v.get("stats") or {}).get("commits", 0) for v in kept)
    fresh_commits = sum((v.get("stats") or {}).get("commits", 0) for v in merged_fresh)
    if kept_commits or fresh_commits:
        project["commits"] = kept_commits + fresh_commits
    span_from = (prior.get("project", {}).get("span") or {}).get("from")
    if span_from and project.get("span"):
        project["span"] = {"from": span_from, "to": project["span"]["to"]}
    data = {"schema": update.get("schema", prior.get("schema", 2)),
            "view": prior.get("view") or update.get("view", {}),
            "project": project, "categories": categories,
            "versions": kept + merged_fresh}
    provenance = {"mode": "continuation", "anchor": anchor_version,
                  "kept": len(kept), "regathered": len(merged_fresh),
                  "prior_generated": prior.get("project", {}).get("generated"),
                  "prior_head": prior.get("project", {}).get("head"),
                  "commit_span_offset": offset}
    return data, provenance


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_plan = sub.add_parser("plan", help="pick the anchor and the gather range")
    p_plan.add_argument("--prior", required=True)
    p_plan.add_argument("--repo", required=True)
    p_plan.add_argument("--ref", default="HEAD")
    p_plan.add_argument("--out")
    p_merge = sub.add_parser("merge", help="splice re-gathered eras onto the kept prior eras")
    p_merge.add_argument("--prior", required=True)
    p_merge.add_argument("--update", required=True)
    p_merge.add_argument("--out", required=True)
    p_merge.add_argument("--provenance", help="write the continuation record to this file")
    args = parser.parse_args()

    prior = load_dataset(Path(args.prior))
    if args.command == "plan":
        result = plan(prior, Path(args.repo), args.ref)
        text = json.dumps(result, indent=2, ensure_ascii=False)
        if args.out:
            Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(text)
        return 0
    data, provenance = merge(prior, load_dataset(Path(args.update)))
    Path(args.out).write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n",
                              encoding="utf-8", newline="\n")
    if args.provenance:
        Path(args.provenance).write_text(json.dumps(provenance, indent=2) + "\n",
                                         encoding="utf-8")
    print(f"continued -> {args.out} ({provenance['kept']} kept + {provenance['regathered']} "
          f"re-gathered from {provenance['anchor']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
