"""Merge stage: history.json, the history.js shim, and manifest.json from the git and docs
extracts, carrying the prior visualisation's settings (view, project identity, categories).

With `from_version` set, the output starts at that version - splice it onto the prior dataset
with `scripts/continue-history.py merge`.
Target: the repository named in gathering/config.json - edit this line to name it.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone

from common import CONFIG, NOTES, OUT, REPO, WORKSPACE, read, vkey, write

CODE_CATS = {"feature", "change", "fix", "refactor", "chore", "release"}
REPORT_CATS = {"audit", "hunt", "review", "assessment", "proposal", "report", "comparison"}
GOD_FILE = 800


def iso_day(value: str) -> datetime:
    return datetime.fromisoformat(value[:10])


def clean_record(r: dict) -> dict:
    event = {"type": r["type"], "title": r["title"], "date": r["date"] or r["committed"][:10],
             "ref": r["ref"]}
    for key in ("archived", "summary", "score", "verdict", "findings", "revision",
                "subject_version"):
        if r.get(key):
            event[key] = r[key]
    return event


def prior_settings() -> dict:
    path = WORKSPACE / CONFIG["prior"]
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def assign_records(records, eras, commits) -> tuple[dict, list, list]:
    index = {c["sha"]: i for i, c in enumerate(commits)}
    by_version = {e["version"]: n for n, e in enumerate(eras)}
    last = eras[-1]["version"]
    assigned, planned, unassigned = defaultdict(list), defaultdict(list), []
    for r in records:
        version = r.get("version_dir")
        since = CONFIG.get("from_version")
        if since and version and vkey(version) < vkey(since):
            continue
        if version and version in by_version:
            assigned[by_version[version]].append(r)
            continue
        if version and vkey(version) > vkey(last):
            planned[version].append(r)
            continue
        position = index.get(r.get("add_sha"))
        if position is None or position < eras[0]["first"]:
            if position is None:
                unassigned.append(r)
            continue
        era = next((n for n, e in enumerate(eras) if e["first"] <= position <= e["last"]), None)
        if era is None:
            unassigned.append(r)
        else:
            assigned[era].append(r)
    return assigned, planned, unassigned


def churn_for(era, churn, buckets=None):
    total = [0, 0]
    modules = defaultdict(lambda: [0, 0])
    for i in range(era["first"], era["last"] + 1):
        for mod, per in churn[i].items():
            for kind, (ins, dele) in per.items():
                if buckets is None or kind in buckets:
                    total[0] += ins
                    total[1] += dele
                    modules[mod][0] += ins
                    modules[mod][1] += dele
    return total, modules


def aspects(stats, events, fixes, findings):
    s = stats
    out = {}
    ratio = round(s["loc"]["test"] / s["loc"]["src"], 3) if s["loc"]["src"] else 0
    out["testability"] = {"ratio": ratio, "files": s["test"]["files"], "cases": s["test"]["cases"],
                          "summary": f"test/source ratio {ratio}; {s['test']['files']} test files; "
                                     f"{s['test']['cases']} cases"}
    sizes = s["all_sizes"]
    if sizes:
        avg, top, god = round(sum(sizes) / len(sizes)), max(sizes), sum(1 for n in sizes if n > GOD_FILE)
        out["maintainability"] = {"avgFile": avg, "maxFile": top, "godFiles": god,
                                  "summary": f"avg file {avg} LOC, largest {top}, {god} god files"}
    if s["api"]:
        out["api"] = {"paths": s["api"]["paths"], "operations": s["api"]["operations"],
                      "summary": f"{s['api']['paths']} paths, {s['api']['operations']} operations"}
        if s["api"]["schemes"] or s.get("auth_deps"):
            out["security"] = {"schemes": s["api"]["schemes"], "authDeps": s.get("auth_deps", 0),
                               "summary": f"{s['api']['schemes']} security schemes; "
                                          f"{s.get('auth_deps', 0)} auth-family deps"}
    code = s["loc"]["src"] + s["loc"]["test"]
    records = sum(1 for e in events if "ref" in e)
    if code:
        doc_ratio = round(s["loc"]["docs"] / code, 3)
        out["documentation"] = {"ratio": doc_ratio, "loc": s["loc"]["docs"], "records": records,
                                "summary": f"docs {doc_ratio * 100:.1f}% of code LOC; "
                                           f"{s['loc']['docs']} doc LOC; {records} records"}
    out["problems"] = {"findings": findings, "fixes": fixes,
                       "summary": f"{findings} findings, {fixes} fix commits"}
    return out


def category_detail(order, events, era, churn, stats, items):
    detail = {}
    era_churn = {kind: churn_for(era, churn, buckets) for kind, buckets in
                 (("code", {"src", "test"}), ("docs", {"docs"}), ("test", {"test"}))}
    mods = stats["modules"]
    for cat in order:
        own = [e for e in events if e["type"] == cat]
        block = {"events": len(own)}
        ins = sum(e.get("ins", 0) for e in own)
        dele = sum(e.get("del", 0) for e in own)
        if ins:
            block["ins"] = ins
        if dele:
            block["del"] = dele
        slice_key = "code" if cat in CODE_CATS else cat if cat in ("docs", "test") else None
        if slice_key and (own or cat in ("docs", "test")):
            (tins, tdel), per = era_churn[slice_key]
            buckets = ["src", "test"] if slice_key == "code" else [slice_key]
            if tins or tdel:
                block["churn"] = {"ins": tins, "del": tdel}
                block["modules"] = {m: {"ins": v[0], "del": v[1],
                                        "loc": sum(mods.get(m, {}).get(b, 0) for b in buckets)}
                                    for m, v in sorted(per.items(), key=lambda kv: -sum(kv[1]))
                                    if v[0] or v[1]}
            block["loc"] = {b: stats["loc"][b] for b in buckets}
        facts = {}
        if cat == "dependency" and own:
            actions = Counter(e["dep"]["action"] for e in own)
            facts = {a: actions.get(a, 0) for a in ("added", "bumped", "removed")}
            facts["names"] = {a: sorted({e["dep"]["name"] for e in own if e["dep"]["action"] == a})
                              for a in actions}
            facts.update(stats["deps"])
        elif cat == "test":
            facts = {"cases": stats["test"]["cases"], "files": stats["test"]["files"],
                     "ratio": round(stats["loc"]["test"] / stats["loc"]["src"], 3)
                     if stats["loc"]["src"] else 0}
        elif cat in REPORT_CATS and own:
            facts = {"records": len(own)}
            archived = sum(1 for e in own if e.get("archived"))
            if archived:
                facts["archived"] = archived
            for key, name in (("score", "scores"), ("verdict", "verdicts"),
                              ("subject_version", "subjects")):
                values = sorted({e[key] for e in own if e.get(key)})
                if values:
                    facts[name] = values
            found = sum(e.get("findings", 0) for e in own)
            if found:
                facts["findings"] = found
        elif cat == "changelog" and items:
            facts = {"items": len(items)}
        elif own and any("ref" in e for e in own):
            facts = {"records": sum(1 for e in own if "ref" in e)}
        if facts:
            block["facts"] = facts
        if not own and "churn" not in block and not (cat == "changelog" and items):
            continue
        parts = []
        if own or cat == "changelog":
            parts.append(f"{len(own)} events" if cat in CODE_CATS or cat == "dependency"
                         else f"{len(own)} records" if own else f"{len(items)} changelog items")
        if "churn" in block:
            top = ", ".join(list(block["modules"])[:3])
            parts.append(f"+{block['churn']['ins']}/-{block['churn']['del']} across {top}")
        if cat == "test":
            parts.append(f"{facts['cases']} cases in {facts['files']} files")
        block["summary"] = "; ".join(parts)
        detail[cat] = block
    return detail


def main() -> None:
    commits, events_git = read("commits.json"), read("commit-events.json")
    eras, churn, deps = read("eras.json"), read("churn.json"), read("dependencies.json")
    records, changelog, ref = read("records.json"), read("changelog.json"), read("ref.json")
    prior = prior_settings()
    categories = prior.get("categories") or CONFIG.get("categories", [])
    known = {c["id"] for c in categories}
    assigned, planned, unassigned = assign_records(records, eras, commits)
    sha_era = {}
    for n, e in enumerate(eras):
        for i in range(e["first"], e["last"] + 1):
            sha_era[commits[i]["sha"]] = n
    dep_by_era = defaultdict(list)
    for d in deps:
        if d["sha"] in sha_era:
            dep_by_era[sha_era[d["sha"]]].append(d)
    versions, previous_modules, previous_end = [], set(), None
    for n, era in enumerate(eras):
        span = commits[era["first"]:era["last"] + 1]
        evs = events_git[era["first"]:era["last"] + 1] + dep_by_era[n] + \
            [clean_record(r) for r in assigned.get(n, [])]
        evs.sort(key=lambda e: (e["date"][:19], e.get("sha", ""), e.get("ref", "")))
        stats = era["stats"]
        total, per_module = churn_for(era, churn)
        start, end = iso_day(span[0]["date"]), iso_day(span[-1]["date"])
        touched = Counter(f for c in span for f, _, _ in c["files"])
        mix = Counter(e["type"] for e in events_git[era["first"]:era["last"] + 1]
                      if "ins" in e or "del" in e)
        modules = {}
        for mod, loc in stats["modules"].items():
            entry = {k: loc.get(k, 0) for k in ("src", "test", "docs", "other", "files")}
            entry["total"] = sum(loc.get(k, 0) for k in ("src", "test", "docs", "other"))
            entry["ins"], entry["del"] = per_module.get(mod, [0, 0])
            if mod in stats["module_deps"]:
                entry["deps"] = stats["module_deps"][mod]
            if previous_modules and mod not in previous_modules:
                entry["added"] = True
            modules[mod] = entry
        previous_modules = set(stats["modules"])
        fixes = mix.get("fix", 0)
        findings = sum(e.get("findings", 0) for e in evs if "ref" in e)
        items = changelog.get(era["version"], [])
        record = {
            "version": era["version"], "kind": era["kind"],
            "range": {"from": span[0]["sha"], "to": span[-1]["sha"]},
            "dates": {"from": span[0]["date"], "to": span[-1]["date"]},
            "stats": {"loc": stats["loc"], "files": stats["files"], "deps": stats["deps"],
                      "delta": {"ins": total[0], "del": total[1]}, "commits": len(span)},
            "metrics": {
                "days": (end - start).days,
                "testRatio": round(stats["loc"]["test"] / stats["loc"]["src"], 3)
                if stats["loc"]["src"] else 0,
                "modules": modules,
                "hotspots": [{"file": f, "commits": c} for f, c in touched.most_common(8)],
                "authors": dict(Counter(c["author"] for c in span).most_common()),
                "commitMix": dict(mix.most_common()),
                "files": stats["largest"],
                "aspects": aspects(stats, evs, fixes, findings),
            },
            "commit_span": [era["first"], era["last"]],
            "events": evs,
        }
        counts = Counter(e["type"] for e in evs)
        top = ", ".join(f"{k} {v}" for k, v in counts.most_common(3))
        record["summary"] = (f"{len(span)} commits over {record['metrics']['days']} days, "
                             f"+{total[0]}/-{total[1]} lines; most active: {top}.")
        if items:
            record["changelog_items"] = items
        record["eventCounts"] = dict(counts)
        record["gapDays"] = max(0, (start - previous_end).days) if previous_end else 0
        previous_end = end
        order = [c["id"] for c in sorted(categories, key=lambda c: c["order"])]
        detail = category_detail(order, evs, era, churn, stats, items)
        if detail:
            record["categoryDetail"] = detail
        versions.append(record)
    for version in sorted(planned, key=vkey):
        evs = sorted((clean_record(r) for r in planned[version]), key=lambda e: e["date"])
        versions.append({"version": version, "kind": "planned", "events": evs,
                         "eventCounts": dict(Counter(e["type"] for e in evs)), "gapDays": 0,
                         "planned": True})
    missing = sorted({e["type"] for v in versions for e in v["events"]} - known)
    next_order = max((c["order"] for c in categories), default=0) + 10
    for cat in missing:
        categories.append({"id": cat, "label": cat.title(), "color": "#94a3b8",
                           "order": next_order})
        next_order += 10
    project = {k: prior["project"][k] for k in ("name", "description", "repository")
               if k in prior.get("project", {})}
    project.update(CONFIG.get("project", {}))
    project.setdefault("name", REPO.name)
    project.setdefault("repository", REPO.name)
    project.update({
        "generated": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "head": ref["sha"], "commits": len(commits),
        "span": {"from": commits[0]["date"], "to": commits[-1]["date"]},
        "grouping": "version"})
    dataset = {"schema": 2, "view": CONFIG.get("view") or prior.get("view", {}),
               "project": project, "categories": categories, "versions": versions}
    target = WORKSPACE / "out"
    target.mkdir(exist_ok=True)
    text = json.dumps(dataset, ensure_ascii=False, indent=1)
    (target / "history.json").write_text(text + "\n", encoding="utf-8", newline="\n")
    (target / "history.js").write_text(f"window.HISTORY_DATA = {text};\n", encoding="utf-8",
                                       newline="\n")
    NOTES.mkdir(exist_ok=True)
    (NOTES / "unassigned.json").write_text(json.dumps(unassigned, indent=1), encoding="utf-8")
    write("manifest.json", {"generated": project["generated"], "ref": ref["ref"],
                            "sha": ref["sha"], "local_head": ref["local_head"], "behind": 0,
                            "commits": len(commits), "versions": len(versions),
                            "records": len(records), "unassigned": len(unassigned),
                            "new_categories": missing, "landing": str(target)})
    print(f"versions={len(versions)} events={sum(len(v['events']) for v in versions)} "
          f"unassigned={len(unassigned)} new_categories={missing}")


if __name__ == "__main__":
    main()
