"""Regression tests for multi-project section-boundary and counting fixes."""

from __future__ import annotations

import unittest

from tests import load_script


def _project_block(project: str, number: int) -> str:
    return f"""## {project}

### Structure Conformance

| Component | Surface | Convention | Observed | Status | Evidence |
|-----------|---------|------------|----------|--------|----------|
| pkg       | files   | PascalCase | yes      | Pass   | EVD-001  |

### Technical Findings

| Finding | Pillar | Severity | Title | Result | Status | Change | Verification |
|---------|--------|----------|-------|--------|--------|--------|--------------|
| FND-SEC-{number:03d} | Security & Compliance | High | T | Fail | Open | New | |

### FND-SEC-{number:03d}: T ({project})

Body.

- **Pillar:** Security & Compliance
- **Severity:** High
- **Type:** Concern
- **Criteria:** SEC-AUTHZ - x
- **Evidence:** EVD-001
- **Recommendation:** fix it

"""


class MultiProjectBoundaries(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    def test_conformance_scan_ignores_sibling_status_tables(self):
        # A findings summary table carries `Status: Open`, a lifecycle token
        # that is not a conformance token. Inside a multi-project `##` block
        # the conformance check must stop at the next `###` section, not run
        # into it.
        text = _project_block("alpha", 1) + _project_block("beta", 2)
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

### REC-001 a

x

### REC-002 c

x
"""
        failures = self.validator.check_rec_classification(text)
        self.assertEqual(
            failures,
            [],
            msg="a REC cited in a Basis cell must not double-count",
        )


class CombinedLayoutProjectColumns(unittest.TestCase):
    """Combined multi-project reports carry a leading `Project` column
    instead of `## Project <name>` sections - model consistency must
    attribute scorecard rows from that column."""

    def setUp(self):
        self.validator = load_script("validate-report.py")
        self.names = {"alpha", "beta"}

    def test_project_cell_name_forms(self):
        for cell, expected in (
            ("Project `alpha`", "alpha"),
            ("alpha", "alpha"),
            ("`alpha`", "alpha"),
            ("[Project `beta`](#project-beta)", "beta"),
        ):
            self.assertEqual(
                self.validator.project_cell_name(cell, self.names), expected
            )
        self.assertIsNone(
            self.validator.project_cell_name(
                "Project `alpha` + Project `beta`", self.names
            )
        )
        self.assertIsNone(
            self.validator.project_cell_name("gamma", self.names)
        )

    def test_combined_scorecard_rows_verify_per_project(self):
        text = (
            "# T\n\nDocument Information\n\n"
            "## Health Dashboard\n\n"
            "| Project | Dimension | Score |\n"
            "|---------|-----------|-------|\n"
            "| Project `alpha` | Functional Suitability | 7/10 |\n"
            "| Project `beta` | Functional Suitability | 3/10 |\n"
        )
        model = {
            "scope": {
                "projects": [{"name": "alpha"}, {"name": "beta"}]
            },
            "scores": {
                "scale_max": 10,
                "dimensions": {
                    "alpha.functional_suitability": {"score": 7},
                    "beta.functional_suitability": {"score": 3},
                },
            },
            "criteria": [],
            "requirements": [],
            "findings": [],
            "risks": [],
            "recommendations": [],
            "evidence": [],
        }
        failures = self.validator.check_model_consistency(text, model, "audit")
        scorecard_failures = [f for f in failures if f.startswith("scorecard")]
        self.assertEqual(scorecard_failures, [])

    def test_combined_scorecard_mismatch_is_flagged(self):
        text = (
            "# T\n\nDocument Information\n\n"
            "## Health Dashboard\n\n"
            "| Project | Dimension | Score |\n"
            "|---------|-----------|-------|\n"
            "| Project `alpha` | Functional Suitability | 7/10 |\n"
            "| Project `beta` | Functional Suitability | 9/10 |\n"
        )
        model = {
            "scope": {
                "projects": [{"name": "alpha"}, {"name": "beta"}]
            },
            "scores": {
                "scale_max": 10,
                "dimensions": {
                    "alpha.functional_suitability": {"score": 7},
                    "beta.functional_suitability": {"score": 3},
                },
            },
            "criteria": [],
            "requirements": [],
            "findings": [],
            "risks": [],
            "recommendations": [],
            "evidence": [],
        }
        failures = self.validator.check_model_consistency(text, model, "audit")
        self.assertTrue(
            any("beta" in f and "Functional Suitability" in f for f in failures),
            msg=f"expected a beta scorecard mismatch, got {failures}",
        )


if __name__ == "__main__":
    unittest.main()
