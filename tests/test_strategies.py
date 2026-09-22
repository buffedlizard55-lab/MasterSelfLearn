"""The competition.  The properties that matter: nothing is scored that was not
forecast in advance, and nothing is ranked that has not earned a rank."""
from __future__ import annotations

import unittest

from msl import config
from msl.evidence import KIND_CAPTURED, Ledger
from msl.strategies import (Context, Forecast, leaderboard, score, tracked_metrics,
                            update_weights, STRATEGY_BY_ID, STRATEGIES)
from tests.helpers import TmpDirCase, NOW1, NOW2, NOW3, ev


def series(l: Ledger, e, field: str, topic: str, values, cycles, source="wikimedia_pageviews"):
    out = []
    for v, cyc in zip(values, cycles):
        out.append(l.accept(topic, KIND_CAPTURED, f"{field} obs", source,
                            NOW1, cyc, value=float(v), unit="x", evidence=[e.id],
                            field=field, tags=["wikipedia", "attention", "Art"]))
    return out


class TrackedMetrics(TmpDirCase):
    def test_a_field_with_one_observation_is_not_tracked(self):
        l = Ledger(self.dir)
        e = ev(l)
        series(l, e, "wiki[Art].views.2026-09-14", "t", [100], [1])
        m, _ = tracked_metrics(l)
        self.assertEqual(m, {})

    def test_a_field_with_two_observations_is_tracked(self):
        l = Ledger(self.dir)
        e = ev(l)
        series(l, e, "wiki[Art].views.2026-09-14", "t", [100, 120], [1, 2])
        m, topics = tracked_metrics(l)
        self.assertIn("wiki[Art].views.2026-09-14", m)
        self.assertEqual(topics["wiki[Art].views.2026-09-14"], "t")

    def test_derived_claims_are_not_treated_as_observations(self):
        l = Ledger(self.dir)
        e = ev(l)
        series(l, e, "wiki[Art].views.2026-09-14", "t", [100, 120], [1, 2])
        a, b = l.claims[0], l.claims[1]
        l.accept("t", "derived", "trend", "derived", NOW1, 2, value=20.0,
                 computed_from=[a.id, b.id], formula="last.value - first.value",
                 field="wiki[Art].views.2026-09-14")
        m, _ = tracked_metrics(l)
        self.assertEqual(len(m["wiki[Art].views.2026-09-14"]), 2)


class ForecastingAndScoring(TmpDirCase):
    def _ctx(self, l, cycle, now, memory=None):
        m, t = tracked_metrics(l)
        return Context(ledger=l, cycle=cycle, now=now, memory=memory or {},
                       metrics=m, topic_of=t)

    def test_persistence_always_issues_one_forecast_per_metric(self):
        l = Ledger(self.dir)
        e = ev(l)
        series(l, e, "wiki[Art].views.2026-09-14", "t", [100, 120], [1, 2])
        fc = STRATEGY_BY_ID["S10_Persistence"].fn(self._ctx(l, 2, NOW2))
        self.assertEqual(len(fc), 1)
        self.assertEqual(fc[0].direction, "flat")
        self.assertEqual(fc[0].probability, 0.5)

    def test_momentum_follows_the_observed_direction(self):
        l = Ledger(self.dir)
        e = ev(l)
        series(l, e, "wiki[Art].views.2026-09-14", "t", [100, 120], [1, 2])
        fc = STRATEGY_BY_ID["S01_MomentumPersist"].fn(self._ctx(l, 2, NOW2))
        self.assertEqual(fc[0].direction, "up")
        self.assertGreater(fc[0].probability, 0.5)

    def test_a_forecast_is_not_scored_before_a_new_observation_exists(self):
        l = Ledger(self.dir)
        e = ev(l)
        series(l, e, "wiki[Art].views.2026-09-14", "t", [100, 120], [1, 2])
        ctx = self._ctx(l, 2, NOW2)
        fc = STRATEGY_BY_ID["S10_Persistence"].fn(ctx)
        score(fc, ctx)
        self.assertFalse(fc[0].scored, "scoring against a forecast's own cycle is cheating")

    def test_a_forecast_is_scored_once_a_later_observation_lands(self):
        l = Ledger(self.dir)
        e = ev(l)
        series(l, e, "wiki[Art].views.2026-09-14", "t", [100, 120], [1, 2])
        fc = STRATEGY_BY_ID["S10_Persistence"].fn(self._ctx(l, 2, NOW2))
        series(l, e, "wiki[Art].views.2026-09-14", "t", [120], [3])
        score(fc, self._ctx(l, 3, NOW3))
        self.assertTrue(fc[0].scored)
        self.assertEqual(fc[0].outcome, "flat")
        self.assertAlmostEqual(fc[0].brier, 0.25)

    def test_brier_is_computed_against_the_realised_direction(self):
        l = Ledger(self.dir)
        e = ev(l)
        series(l, e, "wiki[Art].views.2026-09-14", "t", [100, 120], [1, 2])
        fc = STRATEGY_BY_ID["S01_MomentumPersist"].fn(self._ctx(l, 2, NOW2))
        series(l, e, "wiki[Art].views.2026-09-14", "t", [90], [3])   # it fell
        score(fc, self._ctx(l, 3, NOW3))
        self.assertEqual(fc[0].outcome, "down")
        self.assertGreater(fc[0].brier, 0.25, "a confident wrong call must score badly")

    def test_probabilities_are_clamped_into_the_open_interval(self):
        l = Ledger(self.dir)
        e = ev(l)
        series(l, e, "wiki[Art].views.2026-09-14", "t", [1, 100000], [1, 2])
        fc = STRATEGY_BY_ID["S01_MomentumPersist"].fn(self._ctx(l, 2, NOW2))
        self.assertGreater(fc[0].probability, 0.0)
        self.assertLess(fc[0].probability, 1.0)

    def test_memory_weighted_issues_nothing_before_any_persona_is_scored(self):
        """S06 may only weight personas that have actually earned a number."""
        l = Ledger(self.dir)
        e = ev(l)
        series(l, e, "wiki[Art].views.2026-09-14", "t", [100, 120], [1, 2])
        fc = STRATEGY_BY_ID["S06_MemoryWeighted"].fn(self._ctx(l, 2, NOW2, memory={}))
        self.assertEqual(fc, [])


class LeaderboardQualification(unittest.TestCase):
    def _fc(self, sid, n, correct):
        out = []
        for i in range(n):
            f = Forecast(sid, 1, "t", "m", "up", 0.6, [], "x")
            f.scored = True
            f.outcome = "up" if i < correct else "down"
            f.brier = 0.16
            out.append(f)
        return out

    def test_a_persona_below_the_threshold_is_unranked_not_zero(self):
        fcs = self._fc("S10_Persistence", 5, 5) + self._fc("S01_MomentumPersist", 1, 1)
        lb = leaderboard(fcs)
        self.assertEqual([r["strategyId"] for r in lb["ranked"]], ["S10_Persistence"])
        unranked = {u["strategyId"]: u for u in lb["unranked"]}
        self.assertIn("S01_MomentumPersist", unranked)
        self.assertIn("1 scored forecast", unranked["S01_MomentumPersist"]["unrankedReason"])

    def test_no_persona_is_ranked_when_the_null_model_is_unscored(self):
        fcs = self._fc("S01_MomentumPersist", 10, 9)
        lb = leaderboard(fcs)
        self.assertEqual(lb["ranked"], [])
        self.assertTrue(all("null model" in u["unrankedReason"] for u in lb["unranked"]
                            if u["strategyId"] == "S01_MomentumPersist"))

    def test_skill_is_accuracy_minus_the_null_models_accuracy(self):
        fcs = self._fc("S10_Persistence", 10, 5) + self._fc("S01_MomentumPersist", 10, 8)
        lb = leaderboard(fcs)
        row = next(r for r in lb["ranked"] if r["strategyId"] == "S01_MomentumPersist")
        self.assertAlmostEqual(row["accuracy"], 0.8)
        self.assertAlmostEqual(row["skill"], 0.3)
        null = next(r for r in lb["ranked"] if r["strategyId"] == "S10_Persistence")
        self.assertEqual(null["skill"], 0.0, "the null model's skill is zero by definition")

    def test_accuracy_without_skill_does_not_earn_a_top_rank(self):
        """A persona that only ever predicts 'no change' on a static series looks
        accurate while demonstrating nothing."""
        fcs = self._fc("S10_Persistence", 10, 10) + self._fc("S01_MomentumPersist", 10, 5)
        lb = leaderboard(fcs)
        self.assertEqual(lb["ranked"][0]["strategyId"], "S10_Persistence")
        worse = next(r for r in lb["ranked"] if r["strategyId"] == "S01_MomentumPersist")
        self.assertLess(worse["skill"], 0)

    def test_issued_is_counted_separately_from_scored(self):
        fcs = self._fc("S10_Persistence", 4, 4)
        fcs.append(Forecast("S10_Persistence", 5, "t", "m", "up", 0.5, [], "pending"))
        lb = leaderboard(fcs)
        row = next(r for r in lb["all"] if r["strategyId"] == "S10_Persistence")
        self.assertEqual(row["issued"], 5)
        self.assertEqual(row["scored"], 4)


class WeightLearning(unittest.TestCase):
    def test_weights_fold_skill_in_and_skip_the_null_model(self):
        memory = {"strategyWeights": {}}
        lb = {"all": [{"strategyId": "S01_MomentumPersist", "skill": 0.4},
                      {"strategyId": "S10_Persistence", "skill": 0.0},
                      {"strategyId": "S02_MeanRevert", "skill": None}]}
        out = update_weights(lb, memory)
        w = out["strategyWeights"]
        self.assertIn("S01_MomentumPersist", w)
        self.assertNotIn("S10_Persistence", w, "the null model must not be weighted")
        self.assertNotIn("S02_MeanRevert", w, "an unscored persona has no weight")
        self.assertAlmostEqual(w["S01_MomentumPersist"], 0.5 * 0.75 + 0.9 * 0.25)

    def test_a_weight_never_goes_negative(self):
        """Skill is bounded below by -1, so 0.5 + skill must be floored at 0."""
        memory = {"strategyWeights": {"S01_MomentumPersist": 0.5}}
        lb = {"all": [{"strategyId": "S01_MomentumPersist", "skill": -1.0}]}
        w = update_weights(lb, memory)["strategyWeights"]
        self.assertEqual(w["S01_MomentumPersist"], 0.5 * 0.75 + 0.0 * 0.25)
        self.assertGreaterEqual(w["S01_MomentumPersist"], 0.0)


class RegistryIntegrity(unittest.TestCase):
    def test_every_persona_is_addressable(self):
        for s in STRATEGIES:
            self.assertIn(s.id, STRATEGY_BY_ID)

    def test_the_null_model_exists_and_is_named_as_such(self):
        self.assertIn("S10_Persistence", STRATEGY_BY_ID)
        self.assertIn("null", STRATEGY_BY_ID["S10_Persistence"].name.lower())

    def test_threshold_matches_the_config_the_site_quotes(self):
        self.assertEqual(config.MIN_SCORED_FORECASTS_TO_RANK, 3)


if __name__ == "__main__":
    unittest.main()


def change_series(l: Ledger, e, field: str, topic: str, values, cycles,
                  source="pypi_json"):
    """A categorical series: a version string is an identity, not a magnitude."""
    out = []
    for v, cyc in zip(values, cycles):
        out.append(l.accept(topic, KIND_CAPTURED, f"{field} read", source, NOW1, cyc,
                            value=str(v), unit="version", evidence=[e.id], field=field,
                            tags=["pypi", "release"]))
    return out


class ChangeTargets(TmpDirCase):
    """A version has no up or down; the question is whether it moved."""

    FIELD = "pypi[requests].version"

    def _ctx(self, l, cycle, now):
        from msl.strategies import tracked_changes
        c, topic_of, kind_of = tracked_changes(l)
        return Context(ledger=l, cycle=cycle, now=now, memory={},
                       metrics={}, topic_of={}, changes=c, change_topic_of=topic_of,
                       change_kind=kind_of)

    def test_a_one_observation_version_is_not_tracked(self):
        from msl.strategies import tracked_changes
        l = Ledger(self.dir)
        e = ev(l)
        change_series(l, e, self.FIELD, "t", ["2.34.2"], [1])
        c, _, _ = tracked_changes(l)
        self.assertEqual(c, {})

    def test_a_version_that_changed_is_scored_as_a_change(self):
        l = Ledger(self.dir)
        e = ev(l)
        change_series(l, e, self.FIELD, "t", ["2.34.2", "2.35.0"], [1, 2])
        ctx = self._ctx(l, 2, NOW2)
        f = Forecast("S10_Persistence", 1, "t", self.FIELD, "flat", 0.5,
                     metric_kind="change")
        score([f], ctx)
        self.assertTrue(f.scored)
        self.assertEqual(f.outcome, "up")
        self.assertEqual(f.outcome_value, "2.35.0")
        self.assertAlmostEqual(f.brier, 0.25)

    def test_a_version_that_stayed_the_same_is_a_flat_outcome(self):
        l = Ledger(self.dir)
        e = ev(l)
        change_series(l, e, self.FIELD, "t", ["2.34.2", "2.34.2"], [1, 2])
        ctx = self._ctx(l, 2, NOW2)
        f = Forecast("S10_Persistence", 1, "t", self.FIELD, "flat", 0.5,
                     metric_kind="change")
        score([f], ctx)
        self.assertEqual(f.outcome, "flat")
        self.assertAlmostEqual(f.brier, 0.25)

    def test_change_hazard_is_laplace_smoothed_never_certain(self):
        """A subject that has never changed has not earned a probability of zero."""
        l = Ledger(self.dir)
        e = ev(l)
        change_series(l, e, self.FIELD, "t", ["1", "1", "1"], [1, 2, 3])
        ctx = self._ctx(l, 3, NOW3)
        f = next(x for x in STRATEGY_BY_ID["S07_ChangeHazard"].fn(ctx)
                 if x.metric == self.FIELD)
        self.assertGreater(f.probability, 0.0)
        self.assertLess(f.probability, 0.5)          # "no change" is still the call
        self.assertEqual(f.direction, "flat")
        self.assertEqual(f.metric_kind, "change")

    def test_change_hazard_leans_to_change_when_it_usually_changes(self):
        l = Ledger(self.dir)
        e = ev(l)
        change_series(l, e, self.FIELD, "t", ["1", "2", "3", "4"], [1, 2, 3, 4])
        ctx = self._ctx(l, 4, NOW3)
        f = next(x for x in STRATEGY_BY_ID["S07_ChangeHazard"].fn(ctx)
                 if x.metric == self.FIELD)
        self.assertGreater(f.probability, 0.5)
        self.assertEqual(f.direction, "up")

    def test_the_null_model_covers_change_targets(self):
        l = Ledger(self.dir)
        e = ev(l)
        change_series(l, e, self.FIELD, "t", ["1", "2"], [1, 2])
        ctx = self._ctx(l, 2, NOW2)
        f = next(x for x in STRATEGY_BY_ID["S10_Persistence"].fn(ctx)
                 if x.metric == self.FIELD)
        self.assertEqual(f.direction, "flat")
        self.assertEqual(f.metric_kind, "change")

    def test_numeric_personas_do_not_forecast_change_targets(self):
        """A momentum persona reads magnitudes; a version is not one."""
        l = Ledger(self.dir)
        e = ev(l)
        change_series(l, e, self.FIELD, "t", ["1", "2", "3"], [1, 2, 3])
        ctx = self._ctx(l, 3, NOW3)
        for sid in ("S01_MomentumPersist", "S02_MeanRevert", "S03_Acceleration"):
            issued = STRATEGY_BY_ID[sid].fn(ctx)
            self.assertEqual([f.metric for f in issued if f.metric == self.FIELD], [],
                             f"{sid} issued a magnitude forecast on a version string")

    def test_one_observation_per_cycle_is_what_gets_scored(self):
        """Two reads of one field inside one cycle are one moment, not two."""
        from msl.strategies import tracked_changes
        l = Ledger(self.dir)
        e = ev(l)
        change_series(l, e, self.FIELD, "t", ["1", "1", "2"], [1, 1, 2])
        c, _, _ = tracked_changes(l)
        self.assertEqual([x.cycle for x in c[self.FIELD]], [1, 2],
                         "a duplicate read inside cycle 1 must not become an observation")
        self.assertEqual([x.value for x in c[self.FIELD]], ["1", "2"])

    def test_a_retracted_field_is_not_forecast(self):
        """Retraction must reach the competition, not only the site."""
        from msl.strategies import tracked_changes
        l = Ledger(self.dir)
        e = ev(l)
        field = "github.release[old/name].tag"
        change_series(l, e, field, "t", ["v1", "v2"], [1, 2])
        self.assertIn(field, tracked_changes(l)[0])
        from msl import retractions
        retractions.RETRACTIONS.append({"fieldPrefix": field, "reason": "test",
                                        "firstSeenCycle": "1", "fixedInCycle": "2"})
        try:
            self.assertNotIn(field, tracked_changes(l)[0])
        finally:
            retractions.RETRACTIONS.pop()
