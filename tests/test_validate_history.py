"""Contract tests for the dataset validator in `scripts/validate-history.py`."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import SCRIPTS


def _dataset() -> dict:
    return {
        "schema": 2,
        "project": {"name": "example-service", "head": "abc123", "commits": 1,
                    "span": {"from": "2026-01-01", "to": "2026-01-02"},
                    "grouping": "version"},
        "categories": [
            {"id": "release", "label": "Releases", "color": "#c0c8d4", "order": -10},
            {"id": "fix", "label": "Fixes", "color": "#e64980", "order": 30},
            {"id": "changelog", "label": "Changelog", "color": "#69db7c", "order": 350},
        ],
        "versions": [
            {"version": "1.0.0", "kind": "release",
             "stats": {"loc": {"total": 10}},
             "metrics": {"days": 1},
             "events": [{"type": "fix", "title": "a fix", "date": "2026-01-01",
                         "sha": "abc123"}],
             "eventCounts": {"fix": 1},
             "changelog_items": [{"subject": "1.0.0", "text": "initial"}]},
        ],
    }


class TestValidateHistory(unittest.TestCase):
    def _run(self, data):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        f = Path(tmp.name) / "history.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "validate-history.py"), str(f)],
            capture_output=True, text=True)

    def test_clean_dataset_passes(self):
        result = self._run(_dataset())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK:", result.stdout)

    def test_changelog_items_without_registry_entry_fail(self):
        data = _dataset()
        data["categories"] = [c for c in data["categories"] if c["id"] != "changelog"]
        result = self._run(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("'changelog' is not in the registry", result.stdout)

    def test_eventcounts_key_outside_registry_fails(self):
        data = _dataset()
        data["versions"][0]["events"].append(
            {"type": "ghost", "title": "spooky", "date": "2026-01-01", "sha": "def"})
        data["versions"][0]["eventCounts"] = {"fix": 1, "ghost": 1}
        result = self._run(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("eventCounts key 'ghost' not in registry", result.stdout)

    def test_duplicate_order_fails(self):
        data = _dataset()
        data["categories"][1]["order"] = -10
        result = self._run(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate order", result.stdout)


if __name__ == "__main__":
    unittest.main()
