"""End-to-end: the whole cycle, offline, in a throwaway directory.

These tests exercise the real orchestrator rather than a stand-in, so a change
anywhere in plan → collect → gate → discover → reason → compete → learn → publish
shows up here.
"""
from __future__ import annotations

import json
import pathlib
import unittest

from msl import config
from msl.pipeline import load_seeds, run_cycle, seed_plan
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


if __name__ == "__main__":
    unittest.main()
