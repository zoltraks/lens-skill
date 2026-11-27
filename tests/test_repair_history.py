"""Contract tests for the dataset registry repair in `scripts/repair-history.py`."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import SCRIPTS

TOOL = SCRIPTS / "repair-history.py"
VALIDATE = SCRIPTS / "validate-history.py"


def _version():
    return {"version": "1.0.0", "kind": "release",
            "stats": {"loc": {"total": 10}},
            "metrics": {"days": 1},
            "events": [{"type": "fix", "title": "a fix", "date": "2026-01-01",
                        "sha": "abc123"}],
            "eventCounts": {"fix": 1},
            "changelog_items": [{"subject": "1.0.0", "text": "initial"}]}


def _broken() -> dict:
    """A flat-registry dataset like the pre-repair generation produced."""
    ids = ["release", "change", "feature", "fix", "refactor", "merge",
           "chore", "test", "dependency", "plan", "implementation", "design",
           "epic", "decision", "review", "docs", "project", "reference",
           "script", "standard", "template"]
    return {
        "schema": 2,
        "project": {"name": "example-service", "head": "abc123", "commits": 1,
                    "span": {"from": "2026-01-01", "to": "2026-01-02"},
                    "grouping": "version"},
        "categories": [
            {"id": cid, "label": cid.title(), "color": "#123456",
             "order": (i + 1) * 10}
            for i, cid in enumerate(ids)],
        "versions": [_version()],
    }


def _canonical() -> dict:
    return {
        "schema": 2,
        "project": {"name": "example-service", "head": "abc123", "commits": 1,
                    "span": {"from": "2026-01-01", "to": "2026-01-02"},
                    "grouping": "version"},
        "categories": [
            {"id": "release", "label": "Releases", "color": "#c0c8d4",
             "order": -10},
            {"id": "fix", "label": "Fixes", "color": "#e64980", "order": 10},
            {"id": "changelog", "label": "Changelog", "color": "#69db7c",
             "order": 340},
        ],
        "versions": [_version()],
    }


class TestRepairHistory(unittest.TestCase):
    def _write(self, data):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        f = Path(tmp.name) / "history.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        return f

    def _run(self, *args):
        return subprocess.run([sys.executable, str(TOOL), *map(str, args)],
                              capture_output=True, text=True)

    def test_broken_registry_gets_canonical_anchors(self):
        f = self._write(_broken())
        result = self._run(f)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        cats = {c["id"]: c for c in json.loads(f.read_text())["categories"]}
        # canonical ids re-anchored inside their compacted family blocks
        self.assertEqual(cats["release"]["order"], -10)
        self.assertEqual(cats["merge"]["order"], 50)  # contract absent: tens
        self.assertEqual(cats["fix"]["color"], "#e64980")
        # changelog injected from changelog_items at its canonical seat
        self.assertEqual(cats["changelog"]["order"], 350)
        self.assertEqual(cats["changelog"]["color"], "#69db7c")
        # family gaps restored - every boundary pair jumps by 20+ where the
        # canonical blocks require it
        orders = sorted(c["order"] for c in cats.values())
        self.assertEqual(len(orders), len(set(orders)))
        self.assertIn("+ changelog added", result.stdout)
        # repaired dataset passes the validator gate
        v = subprocess.run([sys.executable, str(VALIDATE), str(f)],
                           capture_output=True, text=True)
        self.assertEqual(v.returncode, 0, v.stdout)

    def test_canonical_registry_is_clean(self):
        f = self._write(_canonical())
        result = self._run(f)
        self.assertEqual(result.returncode, 0)
        self.assertIn("already canonical", result.stdout)

    def test_check_reports_without_writing(self):
        f = self._write(_broken())
        before = f.read_text()
        result = self._run(f, "--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("would repair", result.stdout)
        self.assertEqual(f.read_text(), before)

    def test_unknown_id_appends_inside_its_order_family(self):
        data = _canonical()
        data["categories"].append({"id": "epic", "label": "Epics",
                                   "color": "#111111", "order": 30})
        f = self._write(data)
        result = self._run(f)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        cats = {c["id"]: c for c in json.loads(f.read_text())["categories"]}
        self.assertIn("epic", cats)
        self.assertEqual(cats["epic"]["order"], 20)  # after fix in code block
        self.assertEqual(cats["epic"]["color"], "#111111")
        self.assertEqual(cats["epic"]["label"], "Epics")

    def test_unregistered_event_type_gets_fallback_entry(self):
        data = _canonical()
        data["versions"][0]["events"].append(
            {"type": "deploy", "title": "ship", "date": "2026-01-02",
             "sha": "def456"})
        data["versions"][0]["eventCounts"] = {"fix": 1, "deploy": 1}
        f = self._write(data)
        result = self._run(f)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        cats = {c["id"]: c for c in json.loads(f.read_text())["categories"]}
        self.assertEqual(cats["deploy"]["color"], "#adb5bd")
        self.assertEqual(cats["deploy"]["order"], 350)  # trailing block

    def test_repair_is_idempotent(self):
        f = self._write(_broken())
        self.assertEqual(self._run(f).returncode, 0)
        result = self._run(f, "--check")
        self.assertEqual(result.returncode, 0)
        self.assertIn("already canonical", result.stdout)

    def test_out_writes_elsewhere(self):
        f = self._write(_broken())
        dst = f.parent / "fixed.json"
        result = self._run(f, "--out", dst)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(dst.exists())
        cats = {c["id"]: c for c in json.loads(dst.read_text())["categories"]}
        self.assertEqual(cats["changelog"]["order"], 350)


if __name__ == "__main__":
    unittest.main()
