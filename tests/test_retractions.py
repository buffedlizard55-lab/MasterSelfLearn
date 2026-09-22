"""Retracted claims: withdrawn from reasoning and the site, kept in the ledger.

A verified read of the wrong subject is the one failure the evidence gate cannot
catch, because the evidence is genuine.  These tests pin the three behaviours
that follow from it: stop reasoning from it, keep the row, and say so loudly.
"""
from __future__ import annotations

import pathlib
import tempfile
import unittest

from msl.evidence import Ledger
from msl.irregularities import Register
from msl.reason import derive
from msl.retractions import RETRACTIONS, is_retracted, reason_for
from tests.helpers import NOW1, NOW2, ev


class FieldMatching(unittest.TestCase):
    def test_the_retracted_prefixes_match_only_what_they_name(self):
        self.assertTrue(is_retracted("wiki[artificial_intelligence].views.2026-09-09"))
        self.assertTrue(is_retracted("trend[wiki:artificial_intelligence]"))
        # the canonical title must never be caught by the retraction
        self.assertFalse(is_retracted("wiki[Artificial_intelligence].views.2026-09-09"))
        self.assertFalse(is_retracted("trend[wiki:Artificial_intelligence]"))
        self.assertFalse(is_retracted("wiki[large_language_model].views.2026-09-09"))
        self.assertFalse(is_retracted(""))

    def test_every_retraction_carries_a_reason_and_a_replacement(self):
        for r in RETRACTIONS:
            self.assertTrue(r["reason"], f"{r['fieldPrefix']} has no recorded reason")
            self.assertTrue(r["supersededBy"], f"{r['fieldPrefix']} names no replacement")
            self.assertEqual(reason_for(r["fieldPrefix"] + ".x"), r["reason"])


class ReasoningSkipsRetracted(unittest.TestCase):
    def setUp(self):
        self.dir = pathlib.Path(tempfile.mkdtemp())
        self.ledger = Ledger(self.dir)

    def _views(self, article, day, value):
        e = ev(self.ledger, source_id="wikimedia_pageviews")
        return self.ledger.try_accept(
            "public-attention", "captured",
            f"Wikipedia article \u201c{article}\u201d received {value} views on {day}.",
            "wikimedia_pageviews", NOW1, 1, value=value, unit="views/day",
            field=f"wiki[{article}].views.{day}", evidence=[e.id], tags=["wikipedia", article])

    def test_no_insight_is_derived_from_a_retracted_claim(self):
        """The defect this exists for: a genuine read of the wrong page produced
        'moved from 2 views to 1, a change of -50%' on the front page, and the
        reasoning stage re-derived it on every later cycle."""
        self._views("artificial_intelligence", "2026-09-09", 2)
        self._views("artificial_intelligence", "2026-09-14", 1)
        res = derive(self.ledger, 2, NOW2, [0])
        self.assertEqual(
            [i for i in res.insights if "artificial_intelligence" in i.text
             and "Artificial_intelligence" not in i.text],
            [], "a retracted claim was reasoned from")

    def test_the_canonical_article_is_still_reasoned_about(self):
        self._views("Artificial_intelligence", "2026-09-14", 21659)
        self._views("Artificial_intelligence", "2026-09-20", 14954)
        derive(self.ledger, 2, NOW2, [0])
        self.assertTrue(
            [c for c in self.ledger.claims if c.field.startswith("trend[wiki:Artificial")],
            "the canonical article should still produce a trend")

    def test_retracted_rows_survive_in_the_ledger(self):
        c = self._views("artificial_intelligence", "2026-09-09", 2)
        self.assertIsNotNone(c, "the claim itself was valid and must be recorded")
        derive(self.ledger, 2, NOW2, [0])
        on_disk = [l for l in (self.dir / "claims.jsonl").read_text().splitlines() if l.strip()]
        self.assertTrue(any("artificial_intelligence" in l for l in on_disk),
                        "the ledger is append-only; a retraction must not erase a row")


if __name__ == "__main__":
    unittest.main()
