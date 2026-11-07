"""Function-level tests for the Set B (policy 3) report-side checks in
validate-report.py: the `headline disclosure` and `requirements table`
checks plus the `--model` extension of `model consistency` to the three
headline records and the requirements registry."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tests import load_script


DOC_INFO = """## Document Information

| Field | Value |
|-------|-------|
| Report Style | audit |
"""

SCORECARD = """## Health Dashboard

**Scorecard Summary**

| Dimension              | Score   | Notes |
|------------------------|---------|-------|
| Functional Suitability | 6/10    | x     |
| Testability            | 4/10    | x     |
| Design Soundness       | 6/10    | x     |
| Code Quality           | 7/10    | x     |
| Code Style             | 9/10    | x     |
| Stack Alignment        | 8/10    | x     |
| Dependency Health      | 8/10    | x     |
| Maintainability        | 4/10    | x     |
| Structure              | 8/10    | x     |
| Scalability            | 8/10    | x     |
| Security               | 8/10    | x     |
| Compliance             | 8/10    | x     |
| Observability          | 7/10    | x     |
| Operational Safety     | 9/10    | x     |
| Delivery & Continuity  | 6/10    | x     |
| Originality & Licensing| Unknown | x     |
"""

HEADLINE = """## Executive Summary

| Field         | Value                |
|---------------|----------------------|
| **Overall score** | **6.0/10 (Average)** |

| Score               | Value            | Basis                                                                 |
|---------------------|------------------|-----------------------------------------------------------------------|
| Product Quality     | 7.0/10 (Good)    | Tier-weighted mean of 14 product dimensions, lowest Testability 4/10  |
| Engineering Process | Not published    | 1 of 2 applicable process dimensions scored                           |

The overall score is the product value alone (Product-only).

The overall is capped at ceiling 6: readiness NOT READY.
"""

REPORT = DOC_INFO + "\n" + HEADLINE + "\n" + SCORECARD

PROCESS_PUBLISHED_SCORECARD = SCORECARD.replace(
    "| Originality & Licensing| Unknown | x     |\n",
    "| Originality & Licensing| 8/10    | x     |\n"
    "| Skill Definition       | 7/10    | x     |\n",
)

PROCESS_PUBLISHED_HEADLINE = """## Executive Summary

| Field         | Value             |
|---------------|-------------------|
| **Overall score** | **7.0/10 (Good)** |

| Score               | Value            | Basis                                            |
|---------------------|------------------|--------------------------------------------------|
| Product Quality     | 7.0/10 (Good)    | Tier-weighted mean, lowest Testability 4/10      |
| Engineering Process | 7.0/10 (Good)    | Equal-weight mean, lowest Delivery & Continuity  |

The overall score blends product quality (0.7) and engineering process (0.3).
"""


class TestHeadlineDisclosure(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    def test_consistent_headline_passes(self):
        self.assertEqual(self.validator.check_headline_disclosure(REPORT), [])

    def test_missing_rows_fail(self):
        text = REPORT.replace(
            "| **Overall score** | **6.0/10 (Average)** |\n",
            "",
        )
        fails = self.validator.check_headline_disclosure(text)
        self.assertTrue(
            any("lacks the Overall score row" in f for f in fails), fails
        )
        text = REPORT.replace(
            "| Product Quality     | 7.0/10 (Good)    | "
            "Tier-weighted mean of 14 product dimensions, lowest "
            "Testability 4/10  |\n",
            "",
        )
        fails = self.validator.check_headline_disclosure(text)
        self.assertTrue(
            any("lacks the Product Quality row" in f for f in fails), fails
        )
        fails = self.validator.check_headline_disclosure(
            DOC_INFO + "\n## Executive Summary\n\nProse only.\n"
        )
        joined = "\n".join(fails)
        self.assertIn("lacks the Product Quality row", joined)
        self.assertIn("lacks the Engineering Process row", joined)
        self.assertIn("lacks the Overall score row", joined)

    def test_score_table_overall_row_duplicates(self):
        text = REPORT.replace(
            "| Engineering Process | Not published    | "
            "1 of 2 applicable process dimensions scored                           |\n",
            "| Engineering Process | Not published    | "
            "1 of 2 applicable process dimensions scored                           |\n"
            "| Overall Score       | 6.0/10 (Average) | Product-only, ceiling 6  |\n",
        )
        fails = self.validator.check_headline_disclosure(text)
        self.assertTrue(
            any("duplicates the overall" in f for f in fails), fails
        )

    def test_numeric_product_needs_lowest_nearby(self):
        text = REPORT.replace("lowest Testability 4/10", "tier-weighted blend")
        fails = self.validator.check_headline_disclosure(text)
        self.assertTrue(
            any(
                "Product Quality" in f and "lowest-dimension floor" in f
                for f in fails
            ),
            fails,
        )

    def test_numeric_process_needs_lowest_nearby(self):
        text = (
            DOC_INFO
            + "\n"
            + PROCESS_PUBLISHED_HEADLINE.replace(
                "lowest Delivery & Continuity", "equal-weight blend"
            )
            + "\n"
            + PROCESS_PUBLISHED_SCORECARD
        )
        fails = self.validator.check_headline_disclosure(text)
        self.assertTrue(
            any(
                "Engineering Process" in f and "lowest-dimension floor" in f
                for f in fails
            ),
            fails,
        )

    def test_process_published_recompute_and_blend(self):
        text = (
            DOC_INFO
            + "\n"
            + PROCESS_PUBLISHED_HEADLINE
            + "\n"
            + PROCESS_PUBLISHED_SCORECARD
        )
        self.assertEqual(self.validator.check_headline_disclosure(text), [])
        swapped = text.replace(
            "| Engineering Process | 7.0/10 (Good)",
            "| Engineering Process | 7.4/10 (Good)",
        )
        fails = self.validator.check_headline_disclosure(swapped)
        self.assertTrue(
            any(
                "headline Engineering Process" in f
                and "does not recompute" in f
                and "(7.0/10)" in f
                for f in fails
            ),
            fails,
        )
        swapped = text.replace(
            "| **Overall score** | **7.0/10 (Good)**",
            "| **Overall score** | **7.2/10 (Good)**",
        )
        fails = self.validator.check_headline_disclosure(swapped)
        self.assertTrue(
            any(
                "headline Overall Score" in f
                and "does not recompute" in f
                and "(7.0/10)" in f
                for f in fails
            ),
            fails,
        )

    def test_product_only_must_be_named(self):
        text = REPORT.replace(" (Product-only)", "")
        fails = self.validator.check_headline_disclosure(text)
        self.assertTrue(
            any("does not name Product-only" in f for f in fails), fails
        )

    def test_ceiling_must_be_named(self):
        text = REPORT.replace(
            "\nThe overall is capped at ceiling 6: readiness NOT READY.\n", ""
        )
        fails = self.validator.check_headline_disclosure(text)
        self.assertTrue(
            any("does not name ceiling" in f for f in fails), fails
        )

    def test_product_value_must_recompute(self):
        text = REPORT.replace(
            "| Product Quality     | 7.0/10 (Good)",
            "| Product Quality     | 7.5/10 (Good)",
        )
        fails = self.validator.check_headline_disclosure(text)
        self.assertTrue(
            any(
                "headline Product Quality" in f
                and "does not recompute from the displayed scores (7.0/10)"
                in f
                for f in fails
            ),
            fails,
        )

    def test_unjustified_not_published_fails(self):
        text = REPORT.replace(
            "| Product Quality     | 7.0/10 (Good)    | "
            "Tier-weighted mean of 14 product dimensions, lowest "
            "Testability 4/10  |",
            "| Product Quality     | Not published    | withheld             "
            "                                                            |",
        )
        fails = self.validator.check_headline_disclosure(text)
        self.assertTrue(
            any(
                "headline Product Quality Not published does not recompute"
                in f
                for f in fails
            ),
            fails,
        )

    def test_product_unpublished_overall_is_not_published(self):
        scorecard = SCORECARD.replace(
            "| Testability            | 4/10    | x     |",
            "| Testability            | Unknown | x     |",
        )
        headline = """## Executive Summary

| Field         | Value         |
|---------------|---------------|
| **Overall score** | Not published |

| Score               | Value         | Basis                                  |
|---------------------|---------------|--------------------------------------|
| Product Quality     | Not published | tier weight short of half            |
| Engineering Process | Not published | 1 of 2 applicable dimensions scored  |

The overall score is Not published.
"""
        text = DOC_INFO + "\n" + headline + "\n" + scorecard
        self.assertEqual(self.validator.check_headline_disclosure(text), [])
        numeric = text.replace(
            "| **Overall score** | Not published",
            "| **Overall score** | **5.0/10 (Average)**",
        )
        fails = self.validator.check_headline_disclosure(numeric)
        self.assertTrue(
            any(
                "headline Overall Score" in f
                and "does not recompute from the displayed scores "
                "(Not published)" in f
                for f in fails
            ),
            fails,
        )


class TestExecutiveSummaryShape(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    BODY = """## Document Information

| Field | Value |
|-------|-------|
| Report Style | audit |

## Executive Summary

| Field | Value |
|-------|-------|
| System type | Codebase |
| Scope | x |
| Source basis | x |
| Maturity level | Pre-production |
| Overall score | **5.0/10** |
"""

    def test_legend_absent_passes(self):
        fails = self.validator.check_executive_summary(self.BODY)
        self.assertFalse(any("legend" in f for f in fails), fails)

    def test_legend_in_summary_fails(self):
        text = self.BODY.replace(
            "## Executive Summary\n",
            "## Executive Summary\n\n1-3 Poor · 4-6 Average · 7-8 Good · 9-10 Excellent\n",
        )
        fails = self.validator.check_executive_summary(text)
        self.assertTrue(any("Health Dashboard" in f for f in fails), fails)

    def test_subscore_row_in_kv_table_fails(self):
        text = self.BODY.replace(
            "| Overall score | **5.0/10** |\n",
            "| Overall score | **5.0/10** |\n"
            "| Product Quality | 5.0/10 - lowest x |\n",
        )
        fails = self.validator.check_executive_summary(text)
        self.assertTrue(
            any("Field/Value table" in f and "Product Quality" in f for f in fails),
            fails,
        )


class TestRequirementsTable(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    SECTION = """## Requirements Conformance

| Requirement | Obligation | Status  | Evidence |
|-------------|------------|---------|----------|
| A-01        | mandatory  | Pass    | -        |
| A-02        | mandatory  | Partial | -        |
"""

    def test_clean_table_passes(self):
        text = DOC_INFO + "\n" + self.SECTION
        self.assertEqual(self.validator.check_requirements_table(text), [])

    def test_range_rows_rejected(self):
        for merged in ("A-01 through A-11", "A-01..A-11", "A-01 - A-11"):
            text = DOC_INFO + "\n" + self.SECTION.replace(
                "| A-01        ", f"| {merged} "
            )
            fails = self.validator.check_requirements_table(text)
            self.assertTrue(
                any(
                    f"requirements table row {merged!r} merges several "
                    "requirements - one row per requirement" in f
                    for f in fails
                ),
                (merged, fails),
            )

    def test_header_signature_located_without_section(self):
        text = (
            DOC_INFO
            + "\n## Appendix\n\n"
            + "| Requirement | Obligation | Status |\n"
            + "|-------------|------------|--------|\n"
            + "| A-01 through A-11 | mandatory | Pass |\n"
        )
        fails = self.validator.check_requirements_table(text)
        self.assertTrue(any("merges several requirements" in f for f in fails))

    def test_non_audit_style_skips(self):
        text = DOC_INFO.replace("audit", "hunt") + "\n" + self.SECTION.replace(
            "| A-01        ", "| A-01..A-11 "
        )
        self.assertEqual(self.validator.check_requirements_table(text), [])


class TestModelHeadline(unittest.TestCase):
    def setUp(self):
        self.validator = load_script("validate-report.py")

    REPORT = REPORT

    def _model(self) -> dict:
        return {
            "scope": {"projects": [{"name": None}]},
            "criteria": [
                {
                    "id": "CPR-LIC",
                    "dimension": "originality_licensing",
                    "outcome": "PASS",
                }
            ],
            "requirements": [
                {"id": "A-01", "obligation": "mandatory", "status": "PASS"},
                {"id": "A-02", "obligation": "mandatory", "status": "PARTIAL"},
            ],
            "evidence": [],
            "findings": [],
            "risks": [],
            "recommendations": [],
            "scores": {
                "scale_max": 10,
                "dimensions": {
                    "functional_suitability": {"score": 6},
                    "testability": {"score": 4},
                    "design_soundness": {"score": 6},
                    "code_quality": {"score": 7},
                    "code_style": {"score": 9},
                    "stack_alignment": {"score": 8},
                    "dependency_health": {"score": 8},
                    "maintainability": {"score": 4},
                    "structure": {"score": 8},
                    "scalability": {"score": 8},
                    "security": {"score": 8},
                    "compliance": {"score": 8},
                    "observability": {"score": 7},
                    "operational_safety": {"score": 9},
                    "delivery_continuity": {"score": 6},
                    "originality_licensing": {"score": None},
                },
                "product": {
                    "score": 7.0,
                    "interval": None,
                    "published": True,
                    "eligible_weight": 29,
                    "applicable_weight": 29,
                    "lowest": ["testability", "maintainability"],
                },
                "process": {
                    "score": None,
                    "interval": None,
                    "published": False,
                    "scored": 1,
                    "applicable": 2,
                    "lowest": [],
                },
                "single": {
                    "score": 6.0,
                    "raw": 7.0,
                    "interval": None,
                    "flag": "product-only",
                    "ceiling": {
                        "limit": 6,
                        "reasons": ["readiness:NOT READY"],
                    },
                    "band": "Average",
                },
            },
        }

    REQUIREMENTS = """## Requirements Conformance

| Requirement | Obligation | Status  | Evidence |
|-------------|------------|---------|----------|
| A-01        | mandatory  | Pass    | -        |
| A-02        | mandatory  | Partial | -        |
"""

    def _check(self, text=None, model=None):
        return self.validator.check_model_consistency(
            self.REPORT if text is None else text,
            self._model() if model is None else model,
            "audit",
        )

    def test_consistent_headline_and_requirements_pass(self):
        text = self.REPORT + "\n" + self.REQUIREMENTS
        self.assertEqual(self._check(text), [])

    def test_headline_value_differs(self):
        model = self._model()
        model["requirements"] = []
        text = self.REPORT.replace(
            "| Product Quality     | 7.0/10 (Good)",
            "| Product Quality     | 7.5/10 (Good)",
        )
        fails = self._check(text, model)
        self.assertTrue(
            any(
                "headline Product Quality 7.5/10 differs from the model 7/10"
                in f
                for f in fails
            ),
            fails,
        )

    def test_headline_not_published_differs(self):
        model = self._model()
        model["requirements"] = []
        model["scores"]["process"] = {
            "score": 7.0,
            "published": True,
            "scored": 2,
            "applicable": 2,
        }
        fails = self._check(model=model)
        self.assertTrue(
            any(
                "headline Engineering Process Not published differs from "
                "the model 7/10" in f
                for f in fails
            ),
            fails,
        )

    def test_product_only_marker_required(self):
        model = self._model()
        model["requirements"] = []
        text = self.REPORT.replace(" (Product-only)", "")
        fails = self._check(text, model)
        self.assertTrue(
            any(
                "headline Overall Score" in f and "differs from the model" in f
                and "Product-only" in f
                for f in fails
            ),
            fails,
        )

    def test_ceiling_marker_required(self):
        model = self._model()
        model["requirements"] = []
        model["scores"]["single"]["score"] = 7.0
        model["scores"]["single"]["ceiling"] = None
        text = self.REPORT.replace(
            "\nThe overall is capped at ceiling 6: readiness NOT READY.\n", ""
        ).replace(
            "**6.0/10 (Average)**", "**7.0/10 (Average)**"
        )
        self.assertEqual(self._check(text, model), [])
        extra = text.replace(
            "The overall score is the product value alone (Product-only).",
            "The overall score is the product value alone (Product-only), ceiling 6.",
        )
        fails = self._check(extra, model)
        self.assertTrue(
            any(
                "headline Overall Score 7.0/10 differs from the model "
                "7/10 (Product-only)" in f
                for f in fails
            ),
            fails,
        )

    def test_multi_project_per_project_headline(self):
        model = self._model()
        model["requirements"] = []
        model["criteria"] = []
        model["scope"]["projects"] = [
            {"name": "api", "path": "a"},
            {"name": "cli", "path": "c"},
        ]
        for key in ("product", "process", "single"):
            del model["scores"][key]
        headline = {
            "product": {"score": 7.0, "published": True},
            "process": {"score": None, "published": False},
            "single": {
                "score": 6.0,
                "flag": "product-only",
                "ceiling": {"limit": 6},
            },
        }
        model["scores"]["per_project"] = {
            "api": dict(headline),
            "cli": dict(headline),
        }
        text = (
            DOC_INFO
            + "\n## Project `api`\n\n### Executive Summary\n\n"
            + "| Field | Value |\n|---|---|\n"
            + "| **Overall score** | **6.0/10** |\n\n"
            + "| Score | Value | Basis |\n|---|---|---|\n"
            + "| Product Quality | 7.0/10 (Good) | lowest x |\n"
            + "| Engineering Process | Not published | - |\n\n"
            + "The overall score is the product value alone (Product-only), ceiling 6.\n"
            + "\n## Project `cli`\n\n### Executive Summary\n\n"
            + "| Field | Value |\n|---|---|\n"
            + "| **Overall score** | **6.0/10** |\n\n"
            + "| Score | Value | Basis |\n|---|---|---|\n"
            + "| Product Quality | 7.0/10 (Good) | lowest x |\n"
            + "| Engineering Process | Not published | - |\n\n"
            + "The overall score is the product value alone (Product-only), ceiling 6.\n"
        )
        self.assertEqual(self._check(text, model), [])
        head, sep, tail = text.rpartition("## Project `cli`")
        swapped = head + sep + tail.replace("6.0/10", "9.0/10", 1)
        fails = self._check(swapped, model)
        self.assertTrue(
            any(
                "headline Overall Score cli 9.0/10 differs from the model "
                "6/10 (Product-only, ceiling 6)" in f
                for f in fails
            ),
            fails,
        )

    def test_requirements_rows_match_model(self):
        text = self.REPORT + "\n" + self.REQUIREMENTS.replace(
            "| A-02        | mandatory  | Partial | -        |",
            "| A-02        | mandatory  | Fail    | -        |",
        )
        fails = self._check(text)
        self.assertTrue(
            any(
                "requirements table A-02: report Fail differs from the "
                "model PARTIAL" in f
                for f in fails
            ),
            fails,
        )

    def test_requirements_id_presence_and_count(self):
        model = self._model()
        model["requirements"].append(
            {"id": "A-03", "obligation": "optional", "status": "UNKNOWN"}
        )
        text = self.REPORT + "\n" + self.REQUIREMENTS
        fails = self._check(text, model)
        joined = "\n".join(fails)
        self.assertIn("requirements table lists 2 rows, model has 3", joined)
        self.assertIn(
            "A-03 appears in the model but not in the report", joined
        )
        text = self.REPORT + "\n" + self.REQUIREMENTS.replace(
            "| A-02        | mandatory  | Partial | -        |",
            "| B-99        | mandatory  | Partial | -        |",
        )
        fails = self._check(text)
        self.assertTrue(
            any("B-99 appears in the report but not in the model" in f for f in fails),
            fails,
        )

    def test_requirements_status_normalization(self):
        model = self._model()
        model["requirements"] = [
            {"id": "A-01", "obligation": "mandatory", "status": "NOT_APPLICABLE"}
        ]
        text = self.REPORT + "\n" + self.REQUIREMENTS.replace(
            "| A-02        | mandatory  | Partial | -        |\n", ""
        ).replace(
            "| A-01        | mandatory  | Pass    | -        |",
            "| A-01        | mandatory  | N/A     | -        |",
        )
        self.assertEqual(self._check(text, model), [])

    def test_main_model_flag_reports_consistency(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "AUDIT-1.0.md"
            model = Path(tmp) / "audit-model.json"
            report.write_text(
                self.REPORT + "\n" + self.REQUIREMENTS, encoding="utf-8"
            )
            model.write_text(json.dumps(self._model()), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = self.validator.main(
                    str(report), None, str(model), None
                )
            printed = out.getvalue()
            self.assertIn("[PASS] model consistency", printed)
            self.assertIn("[PASS] headline disclosure", printed)
            self.assertIn("[PASS] requirements table", printed)
            self.assertEqual(rc, 1)  # fragment report fails other checks
            model.write_text(
                json.dumps(
                    {
                        **self._model(),
                        "scores": {
                            **self._model()["scores"],
                            "product": {
                                **self._model()["scores"]["product"],
                                "score": 5.0,
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = self.validator.main(
                    str(report), None, str(model), None
                )
            self.assertIn("[FAIL] model consistency", out.getvalue())
            self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
