"""Registry integrity: the promises the Sources page makes about itself."""
from __future__ import annotations

import pathlib
import unittest

from msl import sources as msl_sources
from msl.sources import (BY_ID, INTEREST_CATEGORIES_WITHOUT_A_SOURCE,
                         KEYED_SOURCES_EXCLUDED, REGISTRY, all_dicts, usable, verified)
from msl.topics import FAMILIES, FAMILY_BY_SLUG, build_interest_profile, keywords_from_text


class SourceRegistry(unittest.TestCase):
    def test_every_source_has_an_operator_and_a_documentation_url(self):
        for s in REGISTRY:
            self.assertTrue(s.operator, f"{s.id} has no operator")
            self.assertTrue(s.docs_url.startswith("http"), f"{s.id} has no docs url")
            self.assertTrue(s.probe_url.startswith("http"), f"{s.id} has no probe url")

    def test_ids_are_unique(self):
        ids = [s.id for s in REGISTRY]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_source_has_an_explicit_provenance_tier(self):
        allowed = {
            "primary-official-documented", "first-party-documented",
            "first-party-undocumented", "trusted-registry",
            "trusted-community-service", "third-party-mirror",
        }
        self.assertTrue(REGISTRY)
        self.assertTrue(all(s.trust_tier in allowed for s in REGISTRY))
        self.assertEqual(BY_ID["frankfurter"].trust_tier, "third-party-mirror")
        for sid in ("mlb_statsapi", "nhl_web", "nba_cdn"):
            self.assertEqual(BY_ID[sid].trust_tier, "first-party-undocumented")

    def test_no_registered_source_requires_an_api_key(self):
        """Obtaining a key would be manual input, which the project refuses."""
        keyed = {k["id"] for k in KEYED_SOURCES_EXCLUDED}
        self.assertEqual(keyed & set(BY_ID), set(),
                         "a keyed source must never appear in the registry")

    def test_every_excluded_source_states_why(self):
        for k in KEYED_SOURCES_EXCLUDED:
            self.assertTrue(k["reason"], f"{k['id']} excluded with no reason")
            self.assertTrue(k["docsUrl"].startswith("http"), f"{k['id']} has no docs url")

    def test_unserved_interest_categories_are_declared(self):
        self.assertTrue(INTEREST_CATEGORIES_WITHOUT_A_SOURCE)
        for g in INTEREST_CATEGORIES_WITHOUT_A_SOURCE:
            self.assertTrue(g["gap"], f"{g['category']} gap with no explanation")

    def test_undocumented_endpoints_carry_the_marker(self):
        """No official contract page was located for the league feeds; the registry
        must say so rather than implying one exists."""
        for s in REGISTRY:
            if s.id in ("mlb_statsapi", "nhl_web", "nba_cdn"):
                self.assertIn("UNDOCUMENTED", s.docs_note, f"{s.id} lost its marker")

    def test_every_probe_url_maps_back_to_its_own_source(self):
        """The URL router has to know the whole registry.

        ``_source_for_url`` is what turns a stored capture into an offline task.  A
        URL it does not recognise is a read that disappears with no message, and
        twenty of these thirty probe URLs used to fall through it.
        """
        from msl.pipeline import _source_for_url
        for s in REGISTRY:
            self.assertEqual(_source_for_url(s.probe_url), s.id,
                             f"{s.id}'s own probe URL maps to the wrong source")

    def test_url_variants_still_find_their_source(self):
        from msl.pipeline import _source_for_url
        cases = [
            ("https://pypi.org/pypi/pandas/json", "pypi_json"),
            ("https://registry.npmjs.org/vite/latest", "npm_registry"),
            ("https://api.github.com/repos/ollama/ollama", "github_repo"),
            ("https://api.github.com/repos/ollama/ollama/releases?per_page=1",
             "github_releases"),
            ("https://api.github.com/search/repositories?q=x&per_page=1", "github_search"),
            ("https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson"
             "&starttime=2026-10-09&endtime=2026-10-15&minmagnitude=5.0", "usgs_fdsn"),
        ]
        for url, want in cases:
            self.assertEqual(_source_for_url(url), want, url)

    def test_the_third_party_fx_mirror_is_labelled_as_such(self):
        s = BY_ID["frankfurter"]
        self.assertIn("NOT an official ECB endpoint", s.notes)
        self.assertIn("third-party", s.notes)
        self.assertIn("community project", s.docs_note)

    def test_verified_sources_record_how_they_were_verified(self):
        """A source may not claim `verified` without a recorded read behind it.

        The basis used to be a hand-written ``docs_note``, because statuses were
        hand-typed into the registry.  Statuses now come from the probe ledger, so
        the ledger is the basis and is what gets asserted: a verified source must
        have a positive read count and a matching recorded row that says the read
        succeeded.  A ``docs_note`` is still welcome but is commentary, not
        evidence — asserting it would fail every source verified by the probe.
        """
        import json

        health = {}
        p = pathlib.Path(msl_sources.__file__).resolve().parent.parent \
            / "data" / "source_health.json"
        if p.exists():
            health = {r.get("id"): r
                      for r in json.loads(p.read_text(encoding="utf-8")).get("results", [])}

        checked = 0
        for s in verified():
            self.assertGreater(s.live_reads, 0,
                               f"{s.id} is 'verified' with no recorded read count")
            row = health.get(s.id)
            if row is not None:
                checked += 1
                self.assertTrue(row.get("ok"),
                                f"{s.id} is 'verified' but its recorded read was not a 200")
                self.assertEqual(row.get("statusAfter"), "verified-live-read",
                                 f"{s.id}'s ledger row disagrees with the registry")
        self.assertGreater(checked, 0,
                           "no verified source could be cross-checked against the "
                           "health ledger; run tools/probe_sources.py")

    def test_statuses_are_from_the_legal_set(self):
        legal = {"registered", "verified-live-read", "blocked"}
        for s in REGISTRY:
            self.assertIn(s.status, legal)

    def test_usable_excludes_blocked_sources(self):
        s = BY_ID["arxiv"]
        original = s.status
        try:
            s.status = "blocked"
            self.assertNotIn(s, usable())
        finally:
            s.status = original

    def test_serialisation_round_trips(self):
        for d in all_dicts():
            self.assertEqual(d["status"], BY_ID[d["id"]].status)
            self.assertIn("docsUrl", d)


class TopicFamilies(unittest.TestCase):
    def test_slugs_are_unique(self):
        slugs = [f.slug for f in FAMILIES]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_every_family_question_is_a_question(self):
        for f in FAMILIES:
            self.assertTrue(f.question.endswith("?"), f"{f.slug} question does not end in '?'")

    def test_every_family_names_a_source_or_says_it_cannot(self):
        for f in FAMILIES:
            self.assertTrue(f.sources or f.blocked_reason,
                            f"{f.slug} has neither a source nor a stated reason")

    def test_a_blocked_family_states_its_reason(self):
        blocked = [f for f in FAMILIES if f.blocked_reason]
        self.assertTrue(blocked, "expected at least one honest coverage gap")
        for f in blocked:
            self.assertGreater(len(f.blocked_reason), 40)

    def test_sources_named_by_families_are_registered(self):
        for f in FAMILIES:
            for sid in f.sources:
                self.assertIn(sid, BY_ID, f"{f.slug} names unregistered source {sid}")

    def test_family_lookup_matches_the_list(self):
        self.assertEqual(set(FAMILY_BY_SLUG), {f.slug for f in FAMILIES})


class InterestProfile(unittest.TestCase):
    def test_a_missing_capture_is_reported_not_invented(self):
        prof = build_interest_profile(pathlib.Path("/nonexistent-seed-dir"))
        self.assertFalse(prof["available"])
        self.assertTrue(prof["reason"])
        self.assertEqual(prof["categories"], {})

    def test_the_real_capture_scores_every_family(self):
        from tests.helpers import SEED
        prof = build_interest_profile(SEED)
        if not prof["available"]:
            self.skipTest("owner-corpus capture not present")
        self.assertGreater(prof["repoCount"], 0)
        self.assertEqual(set(prof["categories"]), {f.slug for f in FAMILIES})
        self.assertTrue(prof["payloadSha256"])

    def test_keyword_extraction_drops_stopwords(self):
        kws = keywords_from_text("the quick brown fox and the lazy dog")
        self.assertNotIn("the", kws)
        self.assertNotIn("and", kws)
        self.assertIn("quick", kws)


import pathlib  # noqa: E402  (used by test_a_missing_capture_is_reported_not_invented)

if __name__ == "__main__":
    unittest.main()
