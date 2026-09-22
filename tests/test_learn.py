"""Lessons — the engine's statements about its own track record.

A lesson is a sentence plus the integers behind it.  These tests pin the two
that were previously wrong:

* L1 bucketed topics by the sources seen in ``c.topic`` alone.  Only family
  slugs ever appear there and every family has one signal, so the lesson
  confidently published "1.00 signals against 1.00 signals — a ratio of 1.00×"
  as though it were a finding.  The buckets must come from topic+subjects, with
  derived claims excluded, and the sentence must say what the counts show.
* L3 counted only the persisted credit accumulator, which no ledger row can
  re-prove for entity topics created before schema-v2 subjects existed.
"""
from __future__ import annotations

import unittest

from msl.evidence import Ledger
from msl.learn import derive_lessons
from msl.topics import Library
from tests.helpers import TmpDirCase, NOW1

CYCLE = 9


class LessonCase(TmpDirCase):
    def setUp(self) -> None:
        super().setUp()
        self.ledger = Ledger(self.dir)
        self.library = Library(self.dir)

    def claim(self, topic, statement, source_id, subjects=(), value=1):
        e = self.ledger.add_evidence(source_id=source_id, url=f"https://x/{source_id}",
                                     captured_at=NOW1, status=200,
                                     body=b'{"ok":true}', capture_mode="test-fixture")
        return self.ledger.try_accept(
            topic, "captured", statement, source_id, NOW1, CYCLE,
            value=value, unit="n", field=f"f[{statement}]", source_path="ok",
            subjects=list(subjects), evidence=[e.id], url=f"https://x/{source_id}")

    def lesson(self, lid):
        got = [l for l in derive_lessons({}, self.ledger, self.library, [])
               if l["id"] == lid]
        return got[0] if got else None


class L1Corroboration(LessonCase):
    def test_buckets_come_from_subjects_not_family_topics(self):
        """Two sources naming the same entity corroborate it; the family topic
        they were filed under is not where corroboration is measured."""
        self.library.ensure("repo:a/b", "a/b", "open-source-momentum", NOW1, 1,
                            status="active").signals = 3
        self.library.ensure("repo:c/d", "c/d", "open-source-momentum", NOW1, 1,
                            status="active").signals = 2
        self.claim("open-source-momentum", "a from gh", "github_search",
                   subjects=["repo:a/b"])
        self.claim("open-source-momentum", "a from releases", "github_releases",
                   subjects=["repo:a/b"])
        self.claim("open-source-momentum", "c from gh", "github_search",
                   subjects=["repo:c/d"])
        l1 = self.lesson("L1")
        self.assertIsNotNone(l1)
        self.assertEqual(l1["counts"]["multiSourceTopics"], 1)
        self.assertEqual(l1["counts"]["singleSourceTopics"], 1)
        self.assertEqual(l1["counts"]["meanClaimRowsMulti"], 2.0)
        self.assertEqual(l1["counts"]["meanClaimRowsSingle"], 1.0)

    def test_derived_claims_are_not_a_second_witness(self):
        self.library.ensure("repo:a/b", "a/b", "open-source-momentum", NOW1, 1,
                            status="active")
        base = self.claim("open-source-momentum", "a from gh", "github_search",
                          subjects=["repo:a/b"])
        self.ledger.try_accept("open-source-momentum", "derived", "arithmetic",
                               "derived", NOW1, CYCLE, value=2,
                               field="d[repo:a/b]", formula="x+1",
                               computed_from=[base.id])
        # With no multi-source bucket there is no comparison to publish at all:
        # the lesson is absent rather than stating that our own arithmetic
        # corroborated a source.
        self.assertIsNone(self.lesson("L1"))

    def test_a_vacuous_comparison_is_not_published_as_a_finding(self):
        """Only family rows exist, every family has one signal: the old code
        printed 'a ratio of 1.00×' here.  With both buckets present the lesson
        must speak in claim rows, and with no buckets it must not exist."""
        self.library.ensure("family-x", "Family X", "family-x", NOW1, 1,
                            status="active").signals = 1
        self.library.ensure("family-y", "Family Y", "family-y", NOW1, 1,
                            status="active").signals = 1
        self.claim("family-x", "x one", "arxiv")
        self.claim("family-x", "x two", "crossref")
        self.claim("family-y", "y one", "arxiv")
        l1 = self.lesson("L1")
        self.assertIsNotNone(l1)
        self.assertIn("claim row", l1["statement"])
        self.assertNotIn("ratio of 1.00", l1["statement"])
        self.assertEqual(l1["counts"]["meanClaimRowsMulti"], 2.0)
        self.assertEqual(l1["counts"]["meanClaimRowsSingle"], 1.0)

    def test_family_only_signals_are_reported_honestly(self):
        """Multi-source families with equal signal counts must not be dressed
        up as a signal win: the sentence says 'not more discovery signals'."""
        self.library.ensure("family-x", "Family X", "family-x", NOW1, 1,
                            status="active").signals = 5
        self.library.ensure("family-y", "Family Y", "family-y", NOW1, 1,
                            status="active").signals = 5
        self.claim("family-x", "x one", "arxiv")
        self.claim("family-x", "x two", "crossref")
        self.claim("family-y", "y one", "arxiv")
        l1 = self.lesson("L1")
        self.assertIn("not more discovery signals", l1["statement"])


class L3Coverage(LessonCase):
    def test_credit_only_topics_are_disclosed_not_counted_as_verified(self):
        t = self.library.ensure("repo:old/thing", "old/thing",
                                "open-source-momentum", NOW1, 1, status="active")
        t.claims = 7          # pre-schema-v2 credit, no row names it
        self.library.ensure("repo:new/thing", "new/thing",
                            "open-source-momentum", NOW1, CYCLE, status="active")
        self.claim("open-source-momentum", "new from gh", "github_search",
                   subjects=["repo:new/thing"])
        l3 = self.lesson("L3")
        self.assertIsNotNone(l3)
        self.assertEqual(l3["counts"]["topicsWithClaimRows"], 1)
        self.assertEqual(l3["counts"]["topicsWithCreditOnly"], 1)
        self.assertEqual(l3["counts"]["topicsWithNeither"], 0)
        self.assertIn("pre-schema-v2 claim credit", l3["statement"])


if __name__ == "__main__":
    unittest.main()
