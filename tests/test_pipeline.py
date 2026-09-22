"""End-to-end: the whole cycle, offline, in a throwaway directory.

These tests exercise the real orchestrator rather than a stand-in, so a change
anywhere in plan → collect → gate → discover → reason → compete → learn → publish
shows up here.
"""
from __future__ import annotations

import json
import re
import pathlib
import tempfile
import unittest

from msl import config
from msl.topics import Library
from msl.pipeline import load_seeds, run_cycle, seed_plan
from msl.strategies import Forecast
from msl.sources import BY_ID, KEYED_SOURCES_EXCLUDED, REGISTRY
from tests.helpers import SEED, TmpDirCase, NOW1, NOW2, NOW3


class OfflineCycle(TmpDirCase):
    def setUp(self):
        super().setUp()
        self.seed_into(self.dir)
        self.rep1 = self.cycle(NOW1)

    def test_the_cycle_produced_verified_claims(self):
        self.assertGreater(self.rep1.claims_total, 0)
        self.assertGreater(self.rep1.claims_new, 0)

    def test_claims_carry_real_values_not_silent_zeros(self):
        """Regression: a projection with shortened keys once made the adapter read
        None and publish every repository as having 0 stars."""
        claims = [json.loads(l) for l in
                  (self.dir / "claims.jsonl").read_text().splitlines() if l.strip()]
        stars = [c for c in claims if c["field"].endswith(".stars")]
        self.assertTrue(stars, "no star claims were produced at all")
        nonzero = [c for c in stars if c["value"] and c["value"] > 0]
        self.assertTrue(nonzero, "every star claim is 0 — the adapter is reading nothing")

    def test_every_captured_claim_cites_an_evidence_row(self):
        evidence_ids = {json.loads(l)["id"] for l in
                        (self.dir / "evidence.jsonl").read_text().splitlines() if l.strip()}
        for line in (self.dir / "claims.jsonl").read_text().splitlines():
            c = json.loads(line)
            if c["kind"] in ("captured", "documented", "negative"):
                self.assertTrue(c["evidence"], f"{c['id']} has no evidence")
                for eid in c["evidence"]:
                    self.assertIn(eid, evidence_ids)

    def test_every_derived_claim_has_a_lineage_and_a_formula(self):
        for line in (self.dir / "claims.jsonl").read_text().splitlines():
            c = json.loads(line)
            if c["kind"] == "derived":
                self.assertTrue(c["computedFrom"], f"{c['id']} derived with no lineage")
                self.assertTrue(c["formula"], f"{c['id']} derived with no formula")

    def test_field_names_are_unique_per_subject(self):
        """Two different repositories must never share a field name."""
        claims = [json.loads(l) for l in
                  (self.dir / "claims.jsonl").read_text().splitlines() if l.strip()]
        seen = {}
        for c in claims:
            if c["field"].startswith("github.repo[") and c["field"].endswith(".stars"):
                seen.setdefault(c["field"], set()).add(tuple(c["tags"][-1:]))
        dupes = {k: v for k, v in seen.items() if len(v) > 1}
        self.assertEqual(dupes, {}, "one field name is carrying two different subjects")

    def test_the_library_grew_and_families_were_seeded(self):
        lib = json.loads((self.dir / "library.json").read_text())
        self.assertGreaterEqual(lib["counts"]["total"], len(config.MIN_SIGNALS_TO_PROPOSE_TOPIC and REGISTRY and [1]))
        slugs = {t["slug"] for t in lib["topics"]}
        for fam in ("open-source-momentum", "public-attention", "regulatory-flow"):
            self.assertIn(fam, slugs)

    def test_the_travel_family_is_marked_blocked_rather_than_described(self):
        lib = json.loads((self.dir / "library.json").read_text())
        t = next(t for t in lib["topics"] if t["slug"] == "travel-korea")
        self.assertEqual(t["status"], "blocked-no-source")
        self.assertTrue(t["notes"])

    def test_discovered_topics_accumulate_verified_claims(self):
        lib = json.loads((self.dir / "library.json").read_text())
        withclaims = [t for t in lib["topics"] if t["claims"] > 0]
        self.assertTrue(withclaims, "no topic has any verified claim behind it")

    def test_the_new_topic_budget_is_per_cycle_not_per_task(self):
        """Regression: the cap used to reset for every task, so a cycle could add
        dozens of topics instead of MAX_NEW_TOPICS_PER_CYCLE."""
        rep2 = self.cycle(NOW2)
        self.assertLessEqual(rep2.new_topics, config.MAX_NEW_TOPICS_PER_CYCLE)

    def test_the_site_data_is_written_and_parseable(self):
        site = (self.dir / "site.js").read_text()
        self.assertTrue(site.startswith("// GENERATED"))
        body = site.split("window.MSLDATA = ", 1)[1].rstrip().rstrip(";")
        data = json.loads(body)
        for key in ("meta", "autoCounts", "topics", "evidence", "sources",
                    "irregularities", "leaderboard", "ideas", "memory", "families"):
            self.assertIn(key, data)

    def test_the_site_contains_no_nan_or_infinity(self):
        raw = (self.dir / "site.js").read_text()
        for bad in ("NaN", "Infinity", "undefined"):
            self.assertNotIn(bad, raw, f"site.js contains {bad}")

    def test_auto_counts_agree_with_the_ledger(self):
        site = (self.dir / "site.js").read_text()
        data = json.loads(site.split("window.MSLDATA = ", 1)[1].rstrip().rstrip(";"))
        claims = [l for l in (self.dir / "claims.jsonl").read_text().splitlines() if l.strip()]
        self.assertEqual(data["autoCounts"]["claims"], len(claims))
        self.assertEqual(data["claimTotal"], len(claims))

    def test_the_captured_derived_breakdown_uses_ledger_totals(self):
        """Regression: the README published this cycle's derivation *delta* as if
        it were the ledger's derived *total*.

        The breakdown is rendered as a remainder (`claims - derivedClaims -
        negativeClaims` captured), so feeding it a per-cycle delta silently
        reclassified every older derived claim as "captured from live payloads" —
        claiming evidence-backed reads for claims that were computed by
        arithmetic.  At 8,618 claims it reported 8,312 / 306 when the ledger held
        5,914 / 2,704.  Assert against the ledger's own kind counts.

        `negative` is the third kind — proof of absence, such as a repository that
        publishes no release — so the remainder has to subtract it too, or every
        negative claim is published as a captured reading.
        """
        site = (self.dir / "site.js").read_text()
        data = json.loads(site.split("window.MSLDATA = ", 1)[1].rstrip().rstrip(";"))
        rows = [json.loads(l)
                for l in (self.dir / "claims.jsonl").read_text().splitlines() if l.strip()]
        derived = sum(1 for r in rows if r.get("kind") == "derived")
        captured = sum(1 for r in rows if r.get("kind") == "captured")
        negative = sum(1 for r in rows if r.get("kind") == "negative")
        ac = data["autoCounts"]
        self.assertEqual(ac["derivedClaims"], derived,
                         "derivedClaims must be the ledger total, not this cycle's delta")
        self.assertEqual(ac["negativeClaims"], negative,
                         "negativeClaims must be the ledger total of that kind")
        self.assertEqual(ac["claims"] - ac["derivedClaims"] - ac["negativeClaims"],
                         captured,
                         "the captured figure is the remainder and must match the ledger")
        # The three kinds are a partition of the whole; if they do not sum to the
        # total the breakdown is not a breakdown.
        self.assertEqual(ac["derivedClaims"] + ac["negativeClaims"]
                         + (ac["claims"] - ac["derivedClaims"] - ac["negativeClaims"]),
                         ac["claims"])
        self.assertEqual(data["claimKindCounts"].get("derived"), derived)

    def test_derived_this_cycle_is_reported_separately_from_the_total(self):
        """The delta and the total are different numbers and both are published."""
        site = (self.dir / "site.js").read_text()
        data = json.loads(site.split("window.MSLDATA = ", 1)[1].rstrip().rstrip(";"))
        ac = data["autoCounts"]
        self.assertIn("derivedThisCycle", ac)
        self.assertLessEqual(ac["derivedThisCycle"], ac["derivedClaims"],
                             "a cycle cannot derive more than the ledger holds")

    def test_docs_are_generated(self):
        for name in ("README.md", "STATUS.md", "VERIFICATION.md", "IRREGULARITIES.md"):
            # docs are written to the repo root, not the temp data dir
            self.assertTrue((config.ROOT / name).exists(), f"{name} was not generated")

    def test_the_irregularity_register_is_populated_and_severity_ordered(self):
        reg = json.loads((self.dir / "irregularities.json").read_text())
        self.assertGreater(reg["counts"]["total"], 0)
        order = {"critical": 0, "warn": 1, "info": 2}
        ranks = [order[i["severity"]] for i in reg["items"]]
        self.assertEqual(ranks, sorted(ranks))

    def test_standing_findings_are_present(self):
        reg = json.loads((self.dir / "irregularities.json").read_text())
        titles = " ".join(i["title"] for i in reg["items"])
        self.assertIn("no language model", titles)
        self.assertIn("trending API", titles)

    def test_the_owner_document_gap_is_flagged(self):
        reg = json.loads((self.dir / "irregularities.json").read_text())
        self.assertTrue(any("source document could not be read" in i["title"]
                            for i in reg["items"]))


class CycleProgression(TmpDirCase):
    def setUp(self):
        super().setUp()
        self.seed_into(self.dir)
        self.cycle(NOW1)

    def test_the_second_cycle_scores_the_first_cycles_forecasts(self):
        rep2 = self.cycle(NOW2)
        rep3 = self.cycle(NOW3)
        self.assertGreater(rep2.forecasts_issued, 0)
        self.assertGreater(rep3.forecasts_scored, 0,
                           "forecasts issued in cycle 2 were never scored")

    def test_the_null_model_gets_a_real_accuracy_not_a_placeholder(self):
        self.cycle(NOW2)
        self.cycle(NOW3)
        lb = json.loads((self.dir / "leaderboard.json").read_text())
        self.assertIsNotNone(lb["nullAccuracy"])
        self.assertGreater(lb["nullScored"], 0)

    def test_memory_accumulates(self):
        self.cycle(NOW2)
        mem = json.loads((self.dir / "memory.json").read_text())
        self.assertEqual(mem["cyclesRun"], 2)
        self.assertEqual(len(mem["history"]), 2)
        self.assertTrue(mem["sourceReliability"])

    def test_lessons_are_counted_from_the_ledger(self):
        self.cycle(NOW2)
        mem = json.loads((self.dir / "memory.json").read_text())
        ids = {l["id"] for l in mem["lessons"]}
        self.assertIn("L2", ids, "the gate-rejection lesson should exist")
        for l in mem["lessons"]:
            self.assertTrue(l["counts"], f"lesson {l['id']} has no supporting counts")

    def test_cycles_jsonl_is_append_only(self):
        self.cycle(NOW2)
        self.cycle(NOW3)
        lines = [l for l in (self.dir / "cycles.jsonl").read_text().splitlines() if l.strip()]
        self.assertEqual(len(lines), 3)
        self.assertEqual([json.loads(l)["cycle"] for l in lines], [1, 2, 3])

    def test_a_topic_with_no_claims_is_flagged_once_not_per_topic(self):
        """Regression: one warn per unsupported topic buried everything else."""
        for _ in range(4):
            self.cycle(NOW2)
        reg = json.loads((self.dir / "irregularities.json").read_text())
        matches = [i for i in reg["items"]
                   if i["title"] == "Topics with no verified claims behind them"]
        self.assertLessEqual(len(matches), 1)


class FailurePaths(TmpDirCase):
    def test_a_cycle_with_no_seed_data_still_publishes_and_says_so(self):
        rep = run_cycle(offline=True, data_dir=self.dir, now_override=NOW1,
                          docs_dir=self.dir)
        self.assertEqual(rep.fetch_ok, 0)
        self.assertTrue((self.dir / "site.js").exists())
        reg = json.loads((self.dir / "irregularities.json").read_text())
        self.assertTrue(any("No successful read this cycle" in i["title"]
                            for i in reg["items"]),
                        "a cycle that read nothing must say so")
        self.assertTrue(any(i["severity"] == "critical" for i in reg["items"]),
                        "reading nothing is critical, not informational")

    def test_missing_interest_profile_is_reported_not_invented(self):
        rep = run_cycle(offline=True, data_dir=self.dir, now_override=NOW1,
                          docs_dir=self.dir)
        prof = json.loads((self.dir / "profile.json").read_text())
        self.assertFalse(prof["available"])
        self.assertTrue(prof["reason"])
        reg = json.loads((self.dir / "irregularities.json").read_text())
        self.assertTrue(any("interest profile could not be built" in i["title"]
                            for i in reg["items"]))


    def test_a_test_cycle_does_not_rewrite_the_repositorys_own_docs(self):
        before = {n: (config.ROOT / n).read_text(encoding="utf-8")
                  for n in ("README.md", "STATUS.md") if (config.ROOT / n).exists()}
        self.cycle(NOW1)
        for name, text in before.items():
            self.assertEqual((config.ROOT / name).read_text(encoding="utf-8"), text,
                             f"{name} at the repo root was rewritten by a test cycle")
        self.assertTrue((self.dir / "README.md").exists(),
                        "the cycle should have written its docs into the temp dir")

class SeedIntegrity(unittest.TestCase):
    def test_seed_captures_exist_and_are_hashed(self):
        seeds = load_seeds()
        self.assertGreater(len(seeds), 0)
        for url, rec in seeds.items():
            self.assertEqual(len(rec["payloadSha256"]), 64, f"{url} has no sha256")
            self.assertTrue(rec["capturedAt"], f"{url} has no capture time")
            self.assertIn(rec["captureMode"],
                          ("sandbox-scripted-urllib", "agent-fetch-page-transcribed"))

    def test_transcribed_captures_are_marked_not_wire_verifiable(self):
        """A body recorded by an interactive read cannot prove its own bytes."""
        seeds = load_seeds()
        transcribed = [r for r in seeds.values()
                       if r["captureMode"] == "agent-fetch-page-transcribed"]
        self.assertTrue(transcribed, "expected at least one agent-transcribed capture")
        for r in transcribed:
            self.assertFalse(r["wireHashVerifiable"],
                             f"{r['url']} claims to be wire-verifiable but was transcribed")

    def test_every_seed_maps_to_a_registered_source(self):
        from msl.pipeline import _source_for_url
        for url in load_seeds():
            sid = _source_for_url(url)
            self.assertIsNotNone(sid, f"no source for seed {url}")
            self.assertIn(sid, BY_ID)

    def test_every_seed_has_an_adapter_that_accepts_its_projection(self):
        from msl.adapters import adapter_for
        from msl.pipeline import _source_for_url
        for url, rec in load_seeds().items():
            sid = _source_for_url(url)
            fn = adapter_for(sid)
            xr = fn(rec["projection"], {"topic": "t", "query": "q", "query_label": "q",
                                        "term": "artificial intelligence", "window": "7d",
                                        "label": "the week", "owner": config.REPO_OWNER})
            self.assertTrue(xr.facts or xr.problems,
                            f"adapter {sid} neither projected nor complained for {url}")

    def test_the_offline_plan_is_derived_from_the_seeds(self):
        plan = seed_plan(load_seeds())
        self.assertGreater(len(plan), 0)
        self.assertTrue(all(t.kind == "seed" for t in plan))


class PlanBuilding(unittest.TestCase):
    def test_wikipedia_articles_keep_their_canonical_casing(self):
        """Wikipedia titles are case-sensitive past the first character.

        A live cycle once asked for "artificial_intelligence" because the article
        was rebuilt from the lowercased topic slug.  That is a different,
        near-empty page, and the engine published "moved from 2 views to 1, a
        change of -50%" with full confidence about the wrong subject.  The
        canonical title is already recorded on the topic; use it.
        """
        from msl.tasks import build_plan
        lib = Library(pathlib.Path(tempfile.mkdtemp()))
        lib.ensure("wiki:artificial_intelligence", "Artificial_intelligence",
                   "public-attention", NOW1, 1)
        lib.ensure("wiki:large_language_model", "Large_language_model",
                   "public-attention", NOW1, 1)
        urls = [t.url for t in build_plan(lib, NOW1, "20260909", "20260915", "last7")
                if t.source_id == "wikimedia_pageviews"]
        self.assertTrue(urls, "no pageview task was planned")
        joined = " ".join(urls)
        self.assertIn("/Artificial_intelligence/", joined)
        self.assertIn("/Large_language_model/", joined)
        self.assertNotIn("/artificial_intelligence/", joined)
        self.assertNotIn("/large_language_model/", joined)

    def test_the_fallback_article_is_used_when_no_wiki_topic_is_tracked(self):
        from msl.tasks import build_plan
        lib = Library(pathlib.Path(tempfile.mkdtemp()))
        urls = [t.url for t in build_plan(lib, NOW1, "20260909", "20260915", "last7")
                if t.source_id == "wikimedia_pageviews"]
        self.assertTrue(urls, "the attention survey must run even with an empty library")
        self.assertIn("/Artificial_intelligence/", " ".join(urls))


if __name__ == "__main__":
    unittest.main()


class PlanWindows(unittest.TestCase):
    """Every date in a *survey* has to come from the clock, not from the day the
    template was written.  A hard-coded date makes a published sentence false the
    moment the calendar moves past it.

    Probe URLs are the exception and deliberately so: a probe must be the same
    request every cycle or its health record compares two different things.
    """

    def _tasks(self, now, start_day, end_day, window_label="last7"):
        from msl.tasks import build_plan
        lib = Library(pathlib.Path(tempfile.mkdtemp()))
        lib.ensure("repo:browser-use/jev-ultrafast", "browser-use/jev-ultrafast",
                   "open-source-momentum", NOW1, 5,
                   origin_url="https://github.com/browser-use/jev-ultrafast")
        tasks = build_plan(lib, now, start_day, end_day, window_label)
        return ([t.url for t in tasks if t.kind != "probe"],
                [t.url for t in tasks if t.kind == "probe"])

    def test_the_usgs_window_moves_with_the_clock(self):
        urls, _ = self._tasks("2026-10-22T12:00:00Z", "20261009", "20261015")
        usgs = [u for u in urls if "earthquake.usgs.gov" in u]
        self.assertEqual(len(usgs), 1)
        self.assertIn("starttime=2026-10-09", usgs[0])
        self.assertIn("endtime=2026-10-15", usgs[0])
        self.assertNotIn("2026-09-14", " ".join(urls),
                         "a September date survived into an October plan")

    def test_the_github_created_windows_are_derived_from_now(self):
        urls, _ = self._tasks("2026-10-22T12:00:00Z", "20261009", "20261015")
        searches = [u for u in urls if "search/repositories" in u]
        joined = " ".join(searches)
        self.assertIn("created%3A%3E%3D2026-07-24", joined)   # 90 days before now
        self.assertIn("created%3A%3E%3D2026-10-15", joined)   # 7 days before now
        self.assertNotIn("2026-09-14", joined, "a frozen created:>= date survived")

    def test_the_mlb_date_is_iso_because_that_is_the_form_we_have_read(self):
        urls, _ = self._tasks("2026-10-22T12:00:00Z", "20261009", "20261015")
        mlb = [u for u in urls if "statsapi.mlb.com" in u]
        self.assertEqual(len(mlb), 1)
        self.assertIn("date=2026-10-15", mlb[0],
                      "every recorded MLB read used an ISO date; keep the proven form")
        self.assertNotIn("date=20261015", mlb[0])

    def test_the_pageview_window_is_compact_because_that_api_wants_it(self):
        urls, _ = self._tasks("2026-10-22T12:00:00Z", "20261009", "20261015")
        wiki = [u for u in urls if "pageviews" in u]
        self.assertTrue(wiki)
        self.assertIn("/20261009/20261015", wiki[0])

    def test_probes_are_stable_because_they_are_health_checks(self):
        a, probes_a = self._tasks("2026-09-22T12:00:00Z", "20260909", "20260915")
        b, probes_b = self._tasks("2026-10-22T12:00:00Z", "20261009", "20261015")
        self.assertEqual(probes_a, probes_b,
                         "a probe whose URL changes cannot be compared with last cycle")
        self.assertNotEqual(a, b, "the surveys must not be frozen")

    def test_no_survey_url_carries_a_date_that_is_not_in_this_plan(self):
        """A blunt sweep: every date in a survey URL must be one the plan computed."""
        urls, _ = self._tasks("2026-10-22T12:00:00Z", "20261009", "20261015")
        allowed = {"2026-10-09", "2026-10-15", "2026-07-24"}
        for u in urls:
            for d in re.findall(r"20\d{2}-\d{2}-\d{2}", u):
                self.assertIn(d, allowed, f"unexplained date {d} in {u}")


class PlanCapAccounting(unittest.TestCase):
    def test_a_refused_read_is_counted_not_silently_shortened(self):
        """The cap may refuse work; it may not hide that it did."""
        from msl import tasks as taskmod
        from msl.tasks import build_plan
        lib = Library(pathlib.Path(tempfile.mkdtemp()))
        lib.ensure("repo:browser-use/jev-ultrafast", "browser-use/jev-ultrafast",
                   "open-source-momentum", NOW1, 5)
        stats = {}
        plan = build_plan(lib, NOW1, "20260909", "20260915", "last7", stats=stats)
        self.assertEqual(stats["planned"], len(plan))
        self.assertEqual(stats["cap"], taskmod.MAX_TASKS_PER_CYCLE)
        self.assertEqual(stats.get("dropped", 0), 0,
                         f"the standing plan is at {len(plan)}, over the cap "
                         f"{taskmod.MAX_TASKS_PER_CYCLE}")

    def test_the_cap_counts_refusals_when_it_binds(self):
        from unittest import mock
        from msl import tasks as taskmod
        from msl.tasks import build_plan
        lib = Library(pathlib.Path(tempfile.mkdtemp()))
        stats = {}
        with mock.patch.object(taskmod, "MAX_TASKS_PER_CYCLE", 5):
            plan = build_plan(lib, NOW1, "20260909", "20260915", "last7", stats=stats)
        self.assertEqual(len(plan), 5)
        self.assertGreater(stats["dropped"], 0)
        self.assertEqual(stats["planned"], 5)

    def test_the_deepen_reads_use_the_core_api_not_the_search_bucket(self):
        """One deepen search was answered 403 rate limit exceeded (IRR register).

        The replacements are /repos/... reads, which GitHub meters in the core
        bucket this engine barely uses.
        """
        from msl.tasks import MAX_REPO_DEEPEN_PER_CYCLE, build_plan
        lib = Library(pathlib.Path(tempfile.mkdtemp()))
        for i in range(MAX_REPO_DEEPEN_PER_CYCLE + 2):
            lib.ensure(f"repo:owner{i}/name{i}", f"owner{i}/name{i}",
                       "open-source-momentum", NOW1, 10 - i,
                       origin_url=f"https://github.com/owner{i}/name{i}")
        plan = build_plan(lib, NOW1, "20260909", "20260915", "last7")
        deepen = [t for t in plan if t.kind == "deepen"]
        repos = [t for t in deepen if t.source_id == "github_repo"]
        releases = [t for t in deepen if t.source_id == "github_releases"]
        self.assertEqual(len(repos), MAX_REPO_DEEPEN_PER_CYCLE)
        self.assertEqual(len(releases), MAX_REPO_DEEPEN_PER_CYCLE)
        self.assertEqual([t.source_id for t in deepen if t.source_id == "github_search"], [],
                         "the per-repository search deepen is gone (search bucket)")
        for t in repos + releases:
            self.assertIn("/repos/", t.url)

    def test_no_task_url_left_the_registry(self):
        """Every planned read must map back to a registered source."""
        from msl.pipeline import _source_for_url
        from msl.tasks import build_plan
        lib = Library(pathlib.Path(tempfile.mkdtemp()))
        for t in build_plan(lib, NOW1, "20260909", "20260915", "last7"):
            self.assertIsNotNone(_source_for_url(t.url), t.url)
            self.assertEqual(_source_for_url(t.url), t.source_id, t.url)


class ForecastRetention(TmpDirCase):
    """A forecast waiting for an observation must not be dropped for being old."""

    def test_pending_forecasts_survive_beyond_the_scored_window(self):
        from msl.pipeline import _load_forecasts, _save_forecasts
        many = [Forecast("S10_Persistence", 1, "t", f"field[{i}].v", "flat", 0.5)
                for i in range(4500)]
        _save_forecasts(self.dir, many, cycle=1, tracked={f"field[{i}].v" for i in range(4500)})
        back = _load_forecasts(self.dir)
        self.assertEqual(len(back), 4500,
                         "unscored forecasts are the only state in which one can be "
                         "lost before it is ever scored")

    def test_a_metric_that_stopped_being_observed_is_abandoned_and_counted(self):
        from msl.pipeline import _save_forecasts
        pending = Forecast("S10_Persistence", 1, "t", "gone[1].v", "flat", 0.5)
        counts = _save_forecasts(self.dir, [pending], cycle=9, tracked={"other[1].v"})
        self.assertEqual(counts["abandoned"], 1,
                         "five cycles with no observation means nothing will score it")
        self.assertEqual(counts["pending"], 0)

    def test_a_recent_pending_forecast_is_not_abandoned(self):
        from msl.pipeline import _save_forecasts
        pending = Forecast("S10_Persistence", 8, "t", "future[1].v", "flat", 0.5)
        counts = _save_forecasts(self.dir, [pending], cycle=9, tracked={"other[1].v"})
        self.assertEqual(counts["abandoned"], 0)
        self.assertEqual(counts["pending"], 1)

    def test_an_empty_tracked_set_abandons_nothing(self):
        """Conservative on purpose: if the competition sees no metrics at all, the
        problem is upstream, and erasing the forecast log is not a diagnosis."""
        from msl.pipeline import _save_forecasts
        pending = Forecast("S10_Persistence", 1, "t", "gone[1].v", "flat", 0.5)
        counts = _save_forecasts(self.dir, [pending], cycle=9, tracked=set())
        self.assertEqual(counts["abandoned"], 0)
        self.assertEqual(counts["pending"], 1)


class CycleRecordCompleteness(unittest.TestCase):
    """Every per-cycle number must survive a republish.

    A republish re-renders STATUS.md, the README counts block and the site from the
    recorded cycle row.  A key in that row which the republish neither replays nor
    recomputes silently becomes 0 — which is how STATUS.md published "Facts
    extracted 0 / Derived 0" for a cycle that extracted 680 facts and derived 330
    claims, and how "Duration 0 ms" was printed for a 52-second run.
    """

    def test_every_recorded_key_is_replayed_or_recomputed(self):
        from msl.pipeline import (RECOMPUTED_CYCLE_KEYS, REPLAYED_CYCLE_KEYS,
                                  CycleReport)
        written = set(CycleReport().summary())
        covered = REPLAYED_CYCLE_KEYS | RECOMPUTED_CYCLE_KEYS
        self.assertEqual(sorted(written - covered), [],
                         "these keys would silently be republished as 0")

    def test_a_recorded_cycle_is_replayed_not_zeroed(self):
        """End to end: write a row, republish from it, check the numbers survive."""
        from msl.pipeline import CycleReport, republish
        d = pathlib.Path(tempfile.mkdtemp())
        report = CycleReport(cycle=7, at="2026-09-22T12:00:00Z", mode="test",
                             facts=680, claims_new=431, derived=126, rechecks=40,
                             duration_ms=52977, ok=False, errors=["boom"],
                             tasks_planned=21, tasks_dropped=3, forecasts_pending=288)
        (d / "cycles.jsonl").write_text(
            json.dumps({**report.summary(), "autoCounts": report.auto_counts()}) + "\n",
            encoding="utf-8")
        back = republish(data_dir=d, docs_dir=d)
        self.assertEqual(back.facts, 680, "the fact count was lost by the republish")
        self.assertEqual(back.derived, 126)
        self.assertEqual(back.tasks_dropped, 3)
        self.assertEqual(back.forecasts_pending, 288)
        self.assertEqual(back.errors, ["boom"], "a failed cycle must keep saying so")
        self.assertFalse(back.ok)
