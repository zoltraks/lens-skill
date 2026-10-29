"""Regression tests for multi-project section-boundary and counting fixes."""

from __future__ import annotations

import unittest

from tests import load_script


def _project_block(project: str) -> str:
    return f"""## {project}

### Structure Conformance

| Component | Surface | Convention | Observed | Status | Evidence |
|-----------|---------|------------|----------|--------|----------|
| pkg       | files   | PascalCase | yes      | PASS   | EVD-001  |

### Technical Findings

| Finding | Pillar | Severity | Title | Result | Status | Change | Verification |
|---------|--------|----------|-------|--------|--------|--------|--------------|
| FND-SEC-001 | Security & Compliance | High | T | FAIL | Open | New | |

### FND-SEC-001: T ({project})

Body.

* **Pillar:** Security & Compliance
* **Severity:** High
* **Type:** Concern
* **Criteria:** SEC-AUTHZ - x
* **Evidence:** EVD-001
* **Recommendation:** fix it

"""


class MultiProjectBoundaries(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    def test_conformance_scan_ignores_sibling_status_tables(self):
        # A findings summary table carries `Status: Open`, a lifecycle token
        # that is not a conformance token. Inside a multi-project `##` block
        # the conformance check must stop at the next `###` section, not run
        # into it.
        text = _project_block("alpha") + _project_block("beta")
        failures = self.validator.check_structure_and_naming(text)
        self.assertFalse(
            [f for f in failures if "status 'Open'" in f],
            msg="sibling-section Status tables leaked into conformance scan",
        )

    def test_fresh_audit_comparison_baseline_not_flagged(self):
        lines = [
            "- [Vite guide](https://vite.dev/guide/) - bundler comparison baseline.",
        ]
        failures = self.validator.check_fresh_audit_claims(lines, [False])
        self.assertEqual(failures, [])

    def test_classification_counts_first_cell_only(self):
        text = """### Recommendation Classification

| Rec | Recommendation | Class | Basis |
|-----|----------------|-------|-------|
| REC-001 | a | Recommended | b |
| REC-002 | c | Optional | follows REC-001 |

### REC-001: a

x

### REC-002: c

x
"""
        failures = self.validator.check_rec_classification(text)
        self.assertEqual(
            failures,
            [],
            msg="a REC cited in a Basis cell must not double-count",
        )


if __name__ == "__main__":
    unittest.main()
