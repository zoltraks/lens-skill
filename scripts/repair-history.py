#!/usr/bin/env python3
"""Repair a history.json dataset's category registry against the canonical
anchors in references/history-schema.md.

Usage: python3 repair-history.py <history.json> [--out <path>] [--check]

Older or hand-produced datasets can carry a broken registry - flat order
sequences with no family gaps, scattered colors, or a missing `changelog`
entry while versions still carry `changelog_items`. This tool rewrites the
`categories` array to the canonical contract:

- Known ids get their canonical `color` and a family-compacted `order` -
  each family's present members take tens from the family base in canonical
  sequence, so jumps of 20 or more land only at family boundaries (a
  dataset's own `label` is kept when present).
- Registry entries with unknown ids keep their fields and join the family
  block their declared `order` falls into, appended after canonical members.
- Rendered kinds missing from the registry - an event `type`, an
  `eventCounts` key, or `changelog` from `changelog_items` - gain an entry:
  the canonical seat for a known id, otherwise a gray entry in a trailing
  block.

`--check` lists the proposed changes and exits 1 when any are needed, 0 when
the registry is already canonical. Without `--check` the repaired dataset is
written back (in place or to `--out`) and every applied change is listed.
Only the `categories` array is touched - rerun `validate-history.py` after.

Exits 1 on unparseable input.
"""

import json
import sys

# Canonical registry: ordered family blocks, each (name, base order, member
# ids in canonical sequence). Present members compact by tens from the family
# base - a family only grows into the slots its ids occupy, so a jump of 20 or
# more between consecutive orders happens only at a family boundary, which is
# where interfaces draw filter group gaps. Colors and labels are per-id.
FAMILIES = [
    ("releases", -10, ["release"]),
    ("code", 10, ["change", "feature", "fix", "refactor", "contract",
                  "merge", "chore", "test", "dependency"]),
    ("process", 120, ["plan", "concept", "spec", "proposal", "preparation",
                      "decision", "prompt", "lesson", "discard"]),
    ("quality", 240, ["review", "audit", "hunt", "assessment", "report",
                      "comparison"]),
    ("docs", 340, ["docs", "changelog", "reference", "standard",
                   "template"]),
]
COLORS = {
    "release": "#c0c8d4", "change": "#339af0", "feature": "#14b8a6",
    "fix": "#e64980", "refactor": "#5c7cfa", "contract": "#66d9e8",
    "merge": "#94a3b8", "chore": "#364fc7", "test": "#1098ad",
    "dependency": "#74c0fc", "plan": "#6741d9", "concept": "#845ef7",
    "spec": "#5f3dc4", "proposal": "#b197fc", "preparation": "#9775fa",
    "decision": "#e599f7", "prompt": "#da77f2", "lesson": "#f783ac",
    "discard": "#9d8ec7", "review": "#f06595", "audit": "#d9480f",
    "hunt": "#fd7e14", "assessment": "#ffa94d", "report": "#ffd8a8",
    "comparison": "#748ffc", "docs": "#40c057", "changelog": "#69db7c",
    "reference": "#8ce99a", "standard": "#2b8a3e", "template": "#d3f9d8",
}
LABELS = {
    "release": "Releases", "change": "Changes", "feature": "Features",
    "fix": "Fixes", "refactor": "Refactoring", "contract": "Contracts",
    "merge": "Merges", "chore": "Chores", "test": "Tests",
    "dependency": "Dependencies", "plan": "Plans", "concept": "Concepts",
    "spec": "Specs", "proposal": "Proposals", "preparation": "Preparations",
    "decision": "Decisions", "prompt": "Prompts", "lesson": "Lessons",
    "discard": "Discards", "review": "Reviews", "audit": "Audits",
    "hunt": "Hunts", "assessment": "Assessments", "report": "Reports",
    "comparison": "Comparisons", "docs": "Documentation",
    "changelog": "Changelog", "reference": "References",
    "standard": "Standards", "template": "Templates",
}
FAMILY_OF = {cid for _, _, members in FAMILIES for cid in members}
FALLBACK_COLOR = "#adb5bd"  # the interface's unregistered-category gray


def rendered_kinds(h):
    """Every category id the interface will draw, from the version data."""
    kinds = set()
    for v in h.get("versions") or []:
        if not isinstance(v, dict):
            continue
        for e in v.get("events") or []:
            if isinstance(e, dict) and e.get("type"):
                kinds.add(e["type"])
        for k in (v.get("eventCounts") or {}):
            kinds.add(k)
        if v.get("changelog_items"):
            kinds.add("changelog")
    return kinds


def label_for(cid):
    return cid.replace("-", " ").replace("_", " ").title()


def family_of_order(order):
    """Bucket an unknown id's declared order into a family range."""
    fam = FAMILIES[0]
    for f in FAMILIES:
        if order >= f[1]:
            fam = f
    return fam


def repair(h):
    """Return (changes, repaired_categories). Pure - does not mutate `h`.

    Families compact by tens from their canonical base over present members;
    unknown ids append inside the family their declared order falls into,
    and rendered kinds with no registry entry gain one - a canonical seat or
    a gray entry in a trailing block.
    """
    changes = []
    cats = [c for c in (h.get("categories") or []) if isinstance(c, dict)]
    by_id, declared = {}, []
    for c in cats:
        cid = c.get("id")
        if cid in by_id:
            changes.append("%s: duplicate registry entry dropped" % cid)
            continue
        by_id[cid] = c
        declared.append(cid)
    present = set(by_id) | rendered_kinds(h)
    used, out = set(), []

    def seat(cid, order, color, label):
        c = by_id.get(cid)
        if c is None:
            out.append({"id": cid, "label": label, "color": color,
                        "order": order})
            changes.append("+ %s added (order %s, %s)" % (cid, order, color))
        else:
            if c.get("order") != order:
                changes.append("%s: order %r -> %s" % (cid, c.get("order"), order))
            if c.get("color") != color:
                changes.append("%s: color %r -> %s" % (cid, c.get("color"), color))
            out.append(dict(c, order=order, color=color,
                            label=c.get("label") or label))
        used.add(order)

    # unknown registry ids keep their declared order's family, then append
    # after that family's canonical members in declared sequence
    extras, stray = {}, []
    for cid in declared:
        if cid in FAMILY_OF:
            continue
        order = by_id[cid].get("order")
        if isinstance(order, int):
            extras.setdefault(family_of_order(order)[0], []).append(cid)
        else:
            stray.append(cid)

    for name, base, members in FAMILIES:
        ids = [m for m in members if m in present]
        for rank, cid in enumerate(ids):
            seat(cid, base + 10 * rank, COLORS[cid], LABELS[cid])
        order = base + 10 * len(ids)
        for cid in extras.get(name, []):
            while order in used:
                order += 10
            c = by_id[cid]
            entry = dict(c)
            entry["label"] = entry.get("label") or label_for(str(cid))
            entry["color"] = entry.get("color") or FALLBACK_COLOR
            if c.get("order") != order:
                changes.append("%s: order %r -> %s" % (cid, c.get("order"), order))
            entry["order"] = order
            used.add(order)
            out.append(entry)
            order += 10

    # rendered kinds never registered, plus unknown ids with no usable order
    for cid in stray + sorted(present - set(by_id) - set(FAMILY_OF)):
        order = (max(used) + 10) if used else 10
        while order in used:
            order += 10
        seat(cid, order, COLORS.get(cid, FALLBACK_COLOR),
             LABELS.get(cid, label_for(str(cid))))

    out.sort(key=lambda e: e["order"])
    return changes, out


def main(argv):
    if len(argv) < 2 or "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 2
    src = argv[1]
    out = None
    dry = "--check" in argv
    if "--out" in argv:
        i = argv.index("--out")
        out = argv[i + 1]
    try:
        h = json.loads(open(src, encoding="utf-8").read())
    except Exception as e:
        print("FAIL: cannot parse %s: %s" % (src, e))
        return 1
    changes, cats = repair(h)
    if not changes:
        print("OK: %s registry already canonical (%d categories)" %
              (src, len(cats)))
        return 0
    head = "would repair" if dry else "repaired"
    print("%s: %d change(s) to %s" % (head, len(changes), src))
    for ch in changes:
        print("  - " + ch)
    if dry:
        return 1
    h["categories"] = cats
    dst = out or src
    open(dst, "w", encoding="utf-8").write(json.dumps(h, indent=1))
    print("wrote %s" % dst)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
