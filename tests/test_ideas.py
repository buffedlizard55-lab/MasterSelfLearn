"""Idea synthesis.  An idea with no verified claim behind it must not exist."""
from __future__ import annotations

import unittest

from msl.evidence import KIND_CAPTURED, Ledger
from msl.ideas import Idea, score_idea, synthesize
from msl.reason import Insight
from tests.helpers import TmpDirCase, NOW1, NOW2, ev


def repo_claims(l, e, name, stars, created, source="github_search", url="https://example.test/q"):
    l.accept("open-source-momentum", KIND_CAPTURED, f"{name} stars", source, NOW1, 1,
             value=stars, unit="stars", evidence=[e.id], url=url,
             field=f"github.repo[{name}].stars", tags=["github", "repo", name])
    l.accept("open-source-momentum", KIND_CAPTURED, f"{name} created", source, NOW1, 1,
             value=created, unit="iso8601", evidence=[e.id], url=url,
             field=f"github.repo[{name}].created", tags=["github", "repo", name])


class NoIdeaWithoutALineage(TmpDirCase):
    def test_an_empty_ledger_produces_no_ideas(self):
        l = Ledger(self.dir)
        res = synthesize(l, 1, NOW2, [], [], set())
        self.assertEqual(res.ideas, [])

    def test_ideas_only_appear_with_claim_ids_attached(self):
        l = Ledger(self.dir)
        e = ev(l)
        for n, s, c in [("a/fast", 5000, "2026-09-19T00:00:00Z"),
                        ("b/mid", 500, "2026-08-01T00:00:00Z"),
                        ("c/slow", 10, "2026-01-01T00:00:00Z")]:
            repo_claims(l, e, n, s, c)
        res = synthesize(l, 1, NOW2, [], [], set())
        self.assertTrue(res.ideas)
        for i in res.ideas:
            self.assertTrue(i.lineage, f"idea {i.id} has no verified lineage")
            for cid in i.lineage:
                self.assertTrue(any(c.id == cid for c in l.claims))

    def test_a_coverage_gap_is_reported_but_never_scored_as_an_idea(self):
        l = Ledger(self.dir)
        e = ev(l)
        repo_claims(l, e, "a/fast", 5000, "2026-09-19T00:00:00Z")
        repo_claims(l, e, "b/mid", 500, "2026-08-01T00:00:00Z")
        repo_claims(l, e, "c/slow", 10, "2026-01-01T00:00:00Z")
        res = synthesize(l, 1, NOW2, [], [], set())
        gaps = [i for i in res.ideas if i.kind == "gap"]
        self.assertEqual(gaps, [], "gaps have no lineage, so they are not ideas")


class ConvergenceNeedsTwoRealSources(TmpDirCase):
    def test_the_same_source_twice_is_not_convergence(self):
        l = Ledger(self.dir)
        e1 = ev(l, url="https://example.test/q1")
        e2 = ev(l, url="https://example.test/q2")
        repo_claims(l, e1, "x/y", 100, "2026-09-01T00:00:00Z")
        repo_claims(l, e2, "x/y", 100, "2026-09-01T00:00:00Z")
        res = synthesize(l, 1, NOW2, [], [], set())
        self.assertEqual([i for i in res.ideas if i.kind == "convergence"], [])

    def test_derived_claims_do_not_count_as_a_second_witness(self):
        """This was a real defect: every entity looked corroborated because our own
        arithmetic had source_id='derived' and was counted as a source."""
        l = Ledger(self.dir)
        e = ev(l)
        for n, s, c in [("a/fast", 5000, "2026-09-19T00:00:00Z"),
                        ("b/mid", 500, "2026-08-01T00:00:00Z"),
                        ("c/slow", 10, "2026-01-01T00:00:00Z")]:
            repo_claims(l, e, n, s, c)
        l.accept("open-source-momentum", "derived", "velocity", "derived", NOW2, 1,
                 value=1000.0, computed_from=[l.claims[0].id, l.claims[1].id],
                 formula="stars / max(age_days, 1)", field="velocity[a/fast]",
                 tags=["github", "velocity", "a/fast"])
        res = synthesize(l, 1, NOW2, [], [], set())
        conv = [i for i in res.ideas if i.kind == "convergence"]
        self.assertEqual(conv, [], "one real source plus our own arithmetic is not two sources")

    def test_two_genuine_sources_do_produce_convergence(self):
        l = Ledger(self.dir)
        e1 = ev(l, source_id="github_search", url="https://example.test/q1")
        e2 = ev(l, source_id="stackexchange", url="https://example.test/q2")
        repo_claims(l, e1, "x/y", 100, "2026-09-01T00:00:00Z")
        l.accept("open-source-momentum", KIND_CAPTURED, "x/y discussed", "stackexchange",
                 NOW1, 1, value=7, evidence=[e2.id], field="stackexchange.q[0].score",
                 tags=["stackexchange", "x/y"])
        res = synthesize(l, 1, NOW2, [], [], set())
        conv = [i for i in res.ideas if i.kind == "convergence"]
        self.assertEqual(len(conv), 1)
        self.assertEqual(sorted(conv[0].sources), ["github_search", "stackexchange"])


class VelocityOutliers(TmpDirCase):
    def test_a_fast_grower_is_flagged_against_the_median(self):
        l = Ledger(self.dir)
        e = ev(l)
        repo_claims(l, e, "zai-org/zcode", 5548, "2026-09-20T00:00:00Z")
        repo_claims(l, e, "b/mid", 500, "2026-08-01T00:00:00Z")
        repo_claims(l, e, "c/slow", 10, "2026-01-01T00:00:00Z")
        res = synthesize(l, 1, NOW2, [], [], set())
        out = [i for i in res.ideas if i.kind == "velocity-outlier"]
        self.assertTrue(out)
        self.assertIn("zai-org/zcode", out[0].title)
        self.assertIn("5,548", out[0].statement)


class PersistenceAndScoring(TmpDirCase):
    def _three_repos(self):
        l = Ledger(self.dir)
        e = ev(l)
        repo_claims(l, e, "zai-org/zcode", 5548, "2026-09-20T00:00:00Z")
        repo_claims(l, e, "b/mid", 500, "2026-08-01T00:00:00Z")
        repo_claims(l, e, "c/slow", 10, "2026-01-01T00:00:00Z")
        return l

    def test_an_idea_seen_again_is_carried_not_re_minted(self):
        l = self._three_repos()
        first = synthesize(l, 1, NOW2, [], [], set())
        second = synthesize(l, 2, NOW2, first.ideas, [], set())
        ids = [i.id for i in second.ideas]
        self.assertEqual(len(ids), len(set(ids)), "no duplicate idea ids within a cycle")
        carried = [i for i in second.ideas if i.status in ("carried", "promoted")]
        self.assertTrue(carried)
        self.assertTrue(all(i.appearances >= 2 for i in carried))

    def test_the_same_subject_found_by_two_tasks_yields_one_idea(self):
        l = Ledger(self.dir)
        e1 = ev(l, url="https://example.test/q1")
        e2 = ev(l, url="https://example.test/q2")
        repo_claims(l, e1, "zai-org/zcode", 5548, "2026-09-20T00:00:00Z")
        repo_claims(l, e2, "zai-org/zcode", 5548, "2026-09-20T00:00:00Z")
        repo_claims(l, e1, "b/mid", 500, "2026-08-01T00:00:00Z")
        repo_claims(l, e1, "c/slow", 10, "2026-01-01T00:00:00Z")
        res = synthesize(l, 1, NOW2, [], [], set())
        titles = [i.title for i in res.ideas]
        self.assertEqual(len(titles), len(set(titles)), "one subject must not be published twice")

    def test_robustness_falls_to_zero_when_the_lineage_disappears(self):
        l = self._three_repos()
        res = synthesize(l, 1, NOW2, [], [], set())
        idea = res.ideas[0]
        self.assertGreater(idea.robustness, 0)
        idea.lineage = ["C999999"]
        score_idea(idea, l, NOW2, set())
        self.assertEqual(idea.robustness, 0.0)

    def test_an_idea_whose_sources_are_all_blocked_loses_reproducibility(self):
        l = self._three_repos()
        res = synthesize(l, 1, NOW2, [], [], set())
        idea = res.ideas[0]
        before = idea.components["reproducibility"]
        score_idea(idea, l, NOW2, {"github_search"})
        self.assertLess(idea.components["reproducibility"], before)

    def test_round_trip_through_dict(self):
        l = self._three_repos()
        res = synthesize(l, 1, NOW2, [], [], set())
        back = Idea.from_dict(res.ideas[0].as_dict())
        self.assertEqual(back.id, res.ideas[0].id)
        self.assertEqual(back.fingerprint, res.ideas[0].fingerprint)
        self.assertEqual(back.lineage, res.ideas[0].lineage)


class FederalRegisterIdeas(TmpDirCase):
    def test_a_topical_term_produces_a_leading_indicator_idea(self):
        l = Ledger(self.dir)
        e = ev(l, source_id="federal_register",
               url="https://www.federalregister.gov/api/v1/documents.json")
        l.accept("regulatory-flow", KIND_CAPTURED, "1573 documents", "federal_register",
                 NOW1, 1, value=1573, unit="documents", evidence=[e.id],
                 field="fedreg.documents[artificial intelligence]",
                 tags=["federal-register", "regulatory"])
        res = synthesize(l, 1, NOW2, [], [], set())
        lead = [i for i in res.ideas if i.kind == "regulatory-lead"]
        self.assertEqual(len(lead), 1)
        self.assertIn("artificial intelligence", lead[0].title)

    def test_the_health_probe_is_not_mistaken_for_a_term(self):
        l = Ledger(self.dir)
        e = ev(l, source_id="federal_register", url="https://example.test/probe")
        l.accept("source-health", KIND_CAPTURED, "newest documents", "federal_register",
                 NOW1, 1, value=1000, unit="documents", evidence=[e.id],
                 field="fedreg.documents[newest]", tags=["federal-register"])
        res = synthesize(l, 1, NOW2, [], [], set())
        self.assertEqual([i for i in res.ideas if i.kind == "regulatory-lead"], [])


if __name__ == "__main__":
    unittest.main()
