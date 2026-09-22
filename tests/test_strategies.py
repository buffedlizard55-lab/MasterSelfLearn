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
