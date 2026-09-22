"""Reasoning: the arithmetic must be right, and yesterday's arithmetic must be
re-checked against today's inputs."""
from __future__ import annotations

import unittest

from msl.evidence import KIND_CAPTURED, KIND_DERIVED, Ledger
from msl.reason import (_recompute, days_between, derive, parse_iso, recheck_derived,
                        split_indexed)
from tests.helpers import TmpDirCase, NOW1, NOW2, ev


def two_point_series(l: Ledger, e, field_base: str, topic: str, a: float, b: float):
    first = l.accept(topic, KIND_CAPTURED, f"{field_base} day 1", "wikimedia_pageviews",
                     NOW1, 1, value=a, unit="views/day", evidence=[e.id],
                     field=f"{field_base}.2026-09-14", tags=["wikipedia", "attention", "Art"])
    last = l.accept(topic, KIND_CAPTURED, f"{field_base} day 2", "wikimedia_pageviews",
                    NOW1, 2, value=b, unit="views/day", evidence=[e.id],
                    field=f"{field_base}.2026-09-20", tags=["wikipedia", "attention", "Art"])
    return first, last


class FieldParsing(unittest.TestCase):
    def test_split_indexed_accepts_identity_keys(self):
        base, key, rest = split_indexed("github.repo[browser-use/jev-ultrafast].stars")
        self.assertEqual(base, "github.repo[")
        self.assertEqual(key, "browser-use/jev-ultrafast")
        self.assertEqual(rest, "].stars")

    def test_split_indexed_accepts_integer_keys(self):
        base, key, rest = split_indexed("github.repo[0].stars")
        self.assertEqual(key, "0")

    def test_split_indexed_rejects_unindexed_fields(self):
        self.assertIsNone(split_indexed("owner.public_repos"))

    def test_iso_parsing(self):
        self.assertIsNotNone(parse_iso("2026-09-16T21:30:12Z"))
        self.assertIsNone(parse_iso("not a date"))
        self.assertIsNone(parse_iso(""))

    def test_days_between(self):
        d = days_between("2026-09-16T00:00:00Z", "2026-09-21T00:00:00Z")
        self.assertAlmostEqual(d, 5.0)
        self.assertIsNone(days_between("bad", "2026-09-21T00:00:00Z"))


class Recompute(unittest.TestCase):
    """Only formulas this module wrote may be re-evaluated.  An unrecognised
    formula must return None — 'not rechecked' — never a guess."""

    class _C:
        def __init__(self, v):
            self.value = v

    def test_delta(self):
        self.assertEqual(_recompute("last.value - first.value",
                                    [self._C(100), self._C(150)]), 50.0)

    def test_percent_change(self):
        raw = (14954 - 21659) / 21659 * 100
        self.assertEqual(_recompute("(last - first) / first * 100",
                                    [self._C(21659), self._C(14954)]), round(raw, 4))

    def test_percent_change_never_divides_by_zero(self):
        self.assertIsNone(_recompute("(last - first) / first * 100",
                                     [self._C(0), self._C(5)]))

    def test_counts(self):
        self.assertEqual(_recompute("count(distinct sourceId mentioning entity",
                                    [self._C(1)]) if False else
                         _recompute("count(distinct sourceId mentioning entity)",
                                    [self._C(1), self._C(2), self._C(3)]), 3.0)

    def test_unknown_formula_returns_none(self):
        self.assertIsNone(_recompute("something nobody wrote", [self._C(1)]))

    def test_time_dependent_formula_is_not_recheckable(self):
        self.assertIsNone(_recompute("stars / max(age_days, 1)", [self._C(100)]))

    def test_result_is_rounded_the_way_derive_stores_it(self):
        """derive() stores round(x, 4); an unrounded recompute reports false drift."""
        raw = (14954 - 21659) / 21659 * 100
        self.assertNotEqual(raw, round(raw, 4))
        self.assertEqual(_recompute("(last - first) / first * 100",
                                    [self._C(21659), self._C(14954)]), round(raw, 4))


class Derivation(TmpDirCase):
    def test_trend_rule_computes_the_right_percentage(self):
        l = Ledger(self.dir)
        e = ev(l, source_id="wikimedia_pageviews")
        two_point_series(l, e, "wiki[Art].views", "public-attention", 21659.0, 14954.0)
        seq = [0]
        res = derive(l, 3, NOW2, seq)
        trend = [c for c in l.claims if c.field == "trend[wiki:Art]"]
        self.assertEqual(len(trend), 1)
        self.assertEqual(trend[0].value, round((14954 - 21659) / 21659 * 100, 4))
        self.assertEqual(trend[0].kind, KIND_DERIVED)
        self.assertEqual(len(trend[0].computed_from), 2)
        self.assertTrue(trend[0].formula)
        self.assertTrue(res.insights)

    def test_a_single_observation_produces_no_trend(self):
        l = Ledger(self.dir)
        e = ev(l, source_id="wikimedia_pageviews")
        l.accept("public-attention", KIND_CAPTURED, "one point", "wikimedia_pageviews",
                 NOW1, 1, value=100.0, evidence=[e.id],
                 field="wiki[Art].views.2026-09-14", tags=["wikipedia", "attention", "Art"])
        derive(l, 2, NOW2, [0])
        self.assertEqual([c for c in l.claims if c.field.startswith("trend[")], [])

    def test_velocity_rule_uses_real_age(self):
        l = Ledger(self.dir)
        e = ev(l)
        name = "browser-use/jev-ultrafast"
        l.accept("open-source-momentum", KIND_CAPTURED, "stars", "github_search", NOW1, 1,
                 value=15573, unit="stars", evidence=[e.id],
                 field=f"github.repo[{name}].stars", tags=["github", "repo", name])
        l.accept("open-source-momentum", KIND_CAPTURED, "created", "github_search", NOW1, 1,
                 value="2026-09-16T21:30:12Z", unit="iso8601", evidence=[e.id],
                 field=f"github.repo[{name}].created", tags=["github", "repo", name])
        derive(l, 2, "2026-09-21T21:30:12Z", [0])
        vel = [c for c in l.claims if c.field == f"velocity[{name}]"]
        self.assertEqual(len(vel), 1)
        self.assertAlmostEqual(vel[0].value, round(15573 / 5.0, 4), places=3)

    def test_corroboration_needs_two_real_sources(self):
        """'derived' is our own arithmetic, not a second witness."""
        l = Ledger(self.dir)
        e1 = ev(l, source_id="github_search", url="https://example.test/a")
        e2 = ev(l, source_id="github_search", url="https://example.test/b")
        name = "some/repo"
        for e in (e1, e2):
            l.accept("open-source-momentum", KIND_CAPTURED, "stars", "github_search",
                     NOW1, 1, value=10, evidence=[e.id],
                     field=f"github.repo[{name}].stars", tags=["github", "repo", name])
        derive(l, 2, NOW2, [0])
        corr = [c for c in l.claims if c.field.startswith("corroboration[")]
        self.assertEqual(corr, [], "one source reported twice is not corroboration")

        e3 = ev(l, source_id="stackexchange", url="https://example.test/c")
        l.accept("open-source-momentum", KIND_CAPTURED, "mentions", "stackexchange",
                 NOW1, 1, value=3, evidence=[e3.id],
                 field="stackexchange.q[0].score", tags=["stackexchange", name])
        derive(l, 3, NOW2, [0])
        corr = [c for c in l.claims if c.field.startswith("corroboration[")]
        self.assertEqual(len(corr), 1)
        self.assertEqual(corr[0].value, 2)


    def test_federal_register_delta_is_emitted_once_per_field(self):
        ledger = Ledger(self.dir)
        evidence = ev(ledger, source_id="federal_register")
        for cycle, value in ((1, 10), (2, 11), (3, 12), (4, 13)):
            ledger.accept("regulatory-flow", KIND_CAPTURED, "count",
                          "federal_register", NOW1, cycle, value=value,
                          evidence=[evidence.id],
                          field="fedreg.documents[artificial intelligence]",
                          tags=["federal-register", "artificial intelligence"])
        result = derive(ledger, 5, NOW2, [0])
        deltas = [c for c in ledger.claims
                  if c.field == "delta[fedreg:artificial intelligence]"]
        self.assertEqual(len(deltas), 1)
        self.assertEqual(result.derived, 1)
        repeated = derive(ledger, 6, NOW2, [100])
        self.assertEqual(len([c for c in ledger.claims
                              if c.field == "delta[fedreg:artificial intelligence]"]), 1)
        self.assertEqual(repeated.derived, 0)
        self.assertEqual(len(repeated.insights), 1)



class Recheck(TmpDirCase):
    def test_every_derived_row_is_rechecked_even_when_fingerprints_match(self):
        ledger = Ledger(self.dir)
        evidence = ev(ledger)
        a = ledger.accept("t", KIND_CAPTURED, "a", "github_search", NOW1, 1,
                          value=1, evidence=[evidence.id], field="a")
        b = ledger.accept("t", KIND_CAPTURED, "b", "github_search", NOW1, 1,
                          value=3, evidence=[evidence.id], field="b")
        for _ in range(2):
            ledger.accept("t", KIND_DERIVED, "delta", "derived", NOW2, 2,
                          value=2.0, field="delta[x]",
                          formula="last.value - first.value",
                          computed_from=[a.id, b.id])
        result = recheck_derived(ledger, 3, NOW2)
        self.assertEqual(result.rechecks, 2)
        self.assertEqual(result.drift, [])

    def test_recheck_passes_when_inputs_are_unchanged(self):
        l = Ledger(self.dir)
        e = ev(l, source_id="wikimedia_pageviews")
        two_point_series(l, e, "wiki[Art].views", "public-attention", 100.0, 150.0)
        derive(l, 2, NOW2, [0])
        res = recheck_derived(l, 3, NOW2)
        self.assertGreaterEqual(res.rechecks, 1)
        self.assertEqual(res.drift, [])

    def test_recheck_reports_drift_when_an_input_moves(self):
        l = Ledger(self.dir)
        e = ev(l, source_id="wikimedia_pageviews")
        two_point_series(l, e, "wiki[Art].views", "public-attention", 100.0, 150.0)
        derive(l, 2, NOW2, [0])
        published = next(c for c in l.claims if c.field == "trend[wiki:Art]")
        published.value = 99.0                     # simulate a wrong published figure
        res = recheck_derived(l, 3, NOW2)
        self.assertEqual(len(res.drift), 1)
        self.assertEqual(res.drift[0]["old"], 99.0)
        self.assertEqual(res.drift[0]["new"], 50.0)

    def test_time_dependent_claims_are_counted_not_recheckable(self):
        l = Ledger(self.dir)
        e = ev(l)
        name = "a/b"
        l.accept("t", KIND_CAPTURED, "stars", "github_search", NOW1, 1, value=100,
                 evidence=[e.id], field=f"github.repo[{name}].stars",
                 tags=["github", "repo", name])
        l.accept("t", KIND_CAPTURED, "created", "github_search", NOW1, 1,
                 value="2026-09-16T00:00:00Z", evidence=[e.id],
                 field=f"github.repo[{name}].created", tags=["github", "repo", name])
        derive(l, 2, NOW2, [0])
        res = recheck_derived(l, 3, NOW2)
        self.assertGreaterEqual(res.not_recheckable, 1)
        self.assertEqual(res.drift, [])


if __name__ == "__main__":
    unittest.main()
