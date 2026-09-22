"""Adapters must project real values and must never invent a fact from a payload
whose shape has changed."""
from __future__ import annotations

import json
import unittest

from msl import adapters
from msl.adapters import ADAPTERS, adapter_for
from msl.sources import BY_ID, REGISTRY

CTX = {"topic": "open-source-momentum", "query": "agents", "query_label": "agents"}


class AdapterContract(unittest.TestCase):
    def test_every_registered_source_has_an_adapter(self):
        missing = [s.id for s in REGISTRY if adapter_for(s.id) is None]
        self.assertEqual(missing, [], f"sources with no adapter: {missing}")

    def test_no_adapter_registered_for_an_unregistered_source(self):
        orphans = sorted(set(ADAPTERS) - set(BY_ID))
        self.assertEqual(orphans, [], f"adapters with no source: {orphans}")

    def test_a_bad_payload_yields_problems_and_zero_facts(self):
        """The core anti-hallucination property of the adapter layer."""
        for sid, fn in ADAPTERS.items():
            if sid == "arxiv":
                continue                       # atom is parsed from bytes, tested below
            xr = fn({"unexpected": "shape"}, dict(CTX))
            self.assertEqual(xr.facts, [], f"{sid} invented facts from a bad payload")
            self.assertTrue(xr.problems, f"{sid} said nothing about a bad payload")

    def test_none_payload_is_survivable(self):
        for sid, fn in ADAPTERS.items():
            if sid == "arxiv":
                continue
            xr = fn(None, dict(CTX))
            self.assertEqual(xr.facts, [])


class GitHubSearch(unittest.TestCase):
    PAYLOAD = {
        "total_count": 3636291,
        "incomplete_results": False,
        "items": [
            {"full_name": "browser-use/jev-ultrafast", "stargazers_count": 15573,
             "forks_count": 970, "created_at": "2026-09-16T21:30:12Z",
             "pushed_at": "2026-09-21T01:00:00Z", "description": "Fastest web agent",
             "topics": ["agent", "browser"], "language": "Python",
             "open_issues_count": 12, "html_url": "https://github.com/browser-use/jev-ultrafast",
             "license": "MIT"},
            {"full_name": "zai-org/ZCode", "stargazers_count": 5548, "forks_count": 100,
             "created_at": "2026-09-20T00:00:00Z", "pushed_at": "2026-09-21T00:00:00Z",
             "description": "Coding agent", "topics": ["agent"], "language": "TypeScript",
             "open_issues_count": 1, "html_url": "https://github.com/zai-org/ZCode",
             "license": None},
        ],
    }

    def test_star_counts_are_the_real_ones(self):
        xr = adapters.gh_search(self.PAYLOAD, dict(CTX))
        stars = {f.field: f.value for f in xr.facts if f.field.endswith(".stars")}
        self.assertEqual(stars["github.repo[browser-use/jev-ultrafast].stars"], 15573)
        self.assertEqual(stars["github.repo[zai-org/zcode].stars"], 5548)

    def test_field_names_are_keyed_by_identity_not_position(self):
        """Two queries returning different repos at index 0 must not collide."""
        a = adapters.gh_search(self.PAYLOAD, dict(CTX))
        other = json.loads(json.dumps(self.PAYLOAD))
        other["items"] = other["items"][::-1]
        b = adapters.gh_search(other, dict(CTX))
        fa = {f.field for f in a.facts if f.field.endswith(".stars")}
        fb = {f.field for f in b.facts if f.field.endswith(".stars")}
        self.assertEqual(fa, fb, "field names must not depend on result position")

    def test_total_count_is_namespaced_by_query(self):
        xr = adapters.gh_search(self.PAYLOAD, dict(CTX))
        f = next(f for f in xr.facts if f.field.startswith("github.total_count"))
        self.assertEqual(f.field, "github.total_count[agents]")
        self.assertEqual(f.value, 3636291)

    def test_missing_star_field_records_zero_explicitly_not_silently(self):
        """A payload without stargazers_count must be a shape problem, not a 0.

        This is the exact defect that shipped once: the seed projection used
        shortened keys, the adapter read None, and every repository was published
        as having 0 stars.
        """
        bad = json.loads(json.dumps(self.PAYLOAD))
        for it in bad["items"]:
            it.pop("stargazers_count")
        xr = adapters.gh_search(bad, dict(CTX))
        stars = [f for f in xr.facts if f.field.endswith(".stars")]
        self.assertTrue(all(f.value == 0 for f in stars))
        self.assertTrue(xr.problems, "a payload missing stargazers_count must be reported")

    def test_incomplete_results_is_flagged(self):
        bad = json.loads(json.dumps(self.PAYLOAD))
        bad["incomplete_results"] = True
        xr = adapters.gh_search(bad, dict(CTX))
        self.assertTrue(any("incomplete_results" in p for p in xr.problems))

    def test_entities_are_emitted_for_discovery(self):
        xr = adapters.gh_search(self.PAYLOAD, dict(CTX))
        slugs = [e[0] for e in xr.entities]
        self.assertIn("repo:browser-use/jev-ultrafast", slugs)
        self.assertIn("tag:agent", slugs)

    def test_facts_credit_the_entity_topics_they_support(self):
        xr = adapters.gh_search(self.PAYLOAD, dict(CTX))
        per_field = {f.field: f.entities for f in xr.facts
                     if f.field.startswith("github.repo[")}
        self.assertTrue(per_field)
        for field, ents in per_field.items():
            self.assertTrue(ents, f"{field} credits no entity topic")
        self.assertIn("repo:browser-use/jev-ultrafast",
                      per_field["github.repo[browser-use/jev-ultrafast].stars"])
        self.assertIn("tag:agent",
                      per_field["github.repo[browser-use/jev-ultrafast].stars"])
        self.assertIn("repo:zai-org/zcode",
                      per_field["github.repo[zai-org/zcode].stars"])


class WikipediaPageviews(unittest.TestCase):
    PAYLOAD = {"items": [
        {"project": "en.wikipedia", "article": "Artificial_intelligence",
         "granularity": "daily", "timestamp": "2026091400", "access": "all-access",
         "agent": "user", "views": 21659},
        {"project": "en.wikipedia", "article": "Artificial_intelligence",
         "granularity": "daily", "timestamp": "2026092000", "access": "all-access",
         "agent": "user", "views": 14954},
    ]}

    def test_views_are_the_real_numbers(self):
        xr = adapters.wiki_pageviews(self.PAYLOAD, {"topic": "public-attention"})
        vals = {f.field: f.value for f in xr.facts}
        self.assertEqual(vals["wiki[Artificial_intelligence].views.2026-09-14"], 21659)
        self.assertEqual(vals["wiki[Artificial_intelligence].views.2026-09-20"], 14954)

    def test_statement_names_the_article_and_the_day(self):
        xr = adapters.wiki_pageviews(self.PAYLOAD, {"topic": "public-attention"})
        self.assertIn("Artificial_intelligence", xr.facts[0].statement)
        self.assertIn("2026-09-14", xr.facts[0].statement)


class FederalRegister(unittest.TestCase):
    PAYLOAD = {
        "description": "Documents matching 'artificial intelligence'",
        "count": 1573, "total_pages": 50,
        "results": [
            {"title": "Data Intermediaries and Approaches To Strengthen Public Health Data Exchange",
             "type": "Notice", "document_number": "2026-19271",
             "html_url": "https://www.federalregister.gov/documents/2026-09-21/2026-19271/x",
             "publication_date": "2026-09-21",
             "agencies": [{"name": "Health and Human Services Department", "id": 221},
                          {"name": "Centers for Disease Control and Prevention", "id": 44}]},
        ],
    }

    def test_count_is_the_real_number(self):
        xr = adapters.federal_register(self.PAYLOAD, {"topic": "regulatory-flow",
                                                      "term": "artificial intelligence"})
        f = next(f for f in xr.facts if f.field.startswith("fedreg.documents["))
        self.assertEqual(f.value, 1573)
        self.assertEqual(f.field, "fedreg.documents[artificial intelligence]")

    def test_the_health_probe_is_labelled_not_called_a_term(self):
        xr = adapters.federal_register(self.PAYLOAD, {"topic": "source-health"})
        f = next(f for f in xr.facts if f.field.startswith("fedreg.documents["))
        self.assertEqual(f.field, "fedreg.documents[newest]")
        self.assertNotIn("*", f.field)

    def test_document_and_agency_entities_are_emitted(self):
        xr = adapters.federal_register(self.PAYLOAD, {"topic": "regulatory-flow",
                                                      "term": "artificial intelligence"})
        slugs = [e[0] for e in xr.entities]
        self.assertIn("frdoc:2026-19271", slugs)
        self.assertIn("agency:centers-for-disease-control-and-prevention", slugs)


class OtherAdapters(unittest.TestCase):
    def test_usgs_reports_the_count_and_the_cap(self):
        xr = adapters.usgs_count({"count": 40, "maxAllowed": 20000},
                                 {"topic": "geohazards", "window": "7d", "label": "the week"})
        vals = {f.field: f.value for f in xr.facts}
        self.assertEqual(vals["usgs.events[7d]"], 40)
        self.assertEqual(vals["usgs.maxAllowed"], 20000)

    def test_usgs_flags_when_the_cap_is_hit(self):
        xr = adapters.usgs_count({"count": 20000, "maxAllowed": 20000},
                                 {"topic": "geohazards", "window": "7d"})
        self.assertTrue(any("maxAllowed cap" in p for p in xr.problems))

    def test_hn_prefix_is_described_as_a_prefix(self):
        xr = adapters.hn_top([49792730, 49791939], {"topic": "public-attention"})
        f = next(f for f in xr.facts if f.field == "hn.topstories.length")
        self.assertEqual(f.value, 2)
        self.assertIn("2 story ids", f.statement)

    def test_pypi_release_count_survives_a_keys_only_projection(self):
        payload = {"info": {"name": "requests", "version": "2.34.2",
                            "requires_python": ">=3.9", "summary": "HTTP for Humans"},
                   "releases": {f"2.{i}.0": [] for i in range(63)}}
        xr = adapters.pypi_json(payload, {"topic": "open-source-momentum"})
        vals = {f.field: f.value for f in xr.facts}
        self.assertEqual(vals["pypi[requests].version"], "2.34.2")
        self.assertEqual(vals["pypi[requests].releases"], 63)

    def test_npm_reads_name_and_version(self):
        xr = adapters.npm_latest({"name": "next", "version": "16.3.5"},
                                 {"topic": "open-source-momentum"})
        f = next(f for f in xr.facts if f.field == "npm[next].version")
        self.assertEqual(f.value, "16.3.5")

    def test_arxiv_atom_is_parsed_from_bytes(self):
        atom = (b'<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">'
                b'<opensearch:totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">'
                b'12345</opensearch:totalResults>'
                b'<entry><title>On Reasoning</title><id>http://arxiv.org/abs/2609.00001v1</id>'
                b'<published>2026-09-20T00:00:00Z</published></entry></feed>')
        xr = adapters.arxiv_atom(atom, {"topic": "ai-research-frontier",
                                        "query_label": "cs.AI"})
        vals = {f.field: f.value for f in xr.facts}
        self.assertEqual(vals["arxiv.totalResults"], 12345)
        self.assertEqual(vals["arxiv.entry[0].published"], "2026-09-20T00:00:00Z")

    def test_arxiv_unparseable_body_is_a_problem_not_a_guess(self):
        xr = adapters.arxiv_atom(b"<not xml", {"topic": "ai-research-frontier"})
        self.assertEqual(xr.facts, [])
        self.assertTrue(xr.problems)

    def test_worldbank_skips_the_pagination_element(self):
        payload = [{"pages": 1}, [{"date": "2023", "value": 27357800000000,
                                    "indicator": {"value": "GDP (current US$)"}}]]
        xr = adapters.worldbank(payload, {"topic": "macro-signals",
                                          "indicator": "NY.GDP.MKTP.CD"})
        self.assertEqual(len(xr.facts), 1)
        self.assertEqual(xr.facts[0].value, 27357800000000)

    def test_frankfurter_is_labelled_third_party_in_the_statement_itself(self):
        xr = adapters.frankfurter({"date": "2026-09-19", "rates": {"EUR": 0.85, "KRW": 1380.2}},
                                  {"topic": "macro-signals"})
        for f in xr.facts:
            self.assertIn("Not an official ECB endpoint", f.statement)
            self.assertIn("third-party", f.tags)

    def test_bls_non_success_status_is_a_problem(self):
        xr = adapters.bls({"status": "REQUEST_NOT_PROCESSED",
                           "message": ["Too many series"]}, {"topic": "macro-signals"})
        self.assertEqual(xr.facts, [])
        self.assertTrue(xr.problems)

    def test_stackexchange_reports_its_own_quota(self):
        xr = adapters.stackexchange({"items": [{"title": "q", "score": 5}],
                                     "quota_remaining": 297},
                                    {"topic": "open-source-momentum"})
        f = next(f for f in xr.facts if f.field == "stackexchange.quota_remaining")
        self.assertEqual(f.value, 297)

    def test_low_quota_is_flagged(self):
        xr = adapters.stackexchange({"items": [], "quota_remaining": 3},
                                    {"topic": "open-source-momentum"})
        self.assertTrue(any("quota_remaining=3" in p for p in xr.problems))


if __name__ == "__main__":
    unittest.main()
