"""A runner that cannot reach the network must not be reported as broken sources.

This is the same class of false claim the probe used to make, in the main cycle
path: an ``EgressBlocked`` transport failure (TLS session closed before any HTTP
status arrives) was folded into ``src.status = "blocked"``, so a sandboxed or
filtered runner published "this service is down" for every source it simply was
not allowed to reach — and incremented ``consecutive_failures``, which feeds the
CRITICAL escalation, so an egress blip could manufacture critical findings about
other people's APIs.

It also minted one irregularity per unreachable source: 38 near-identical rows
for a single egress allowlist, which is the register spam AGENTS.md §7 forbids.
"""
from __future__ import annotations

import json
import unittest
from unittest import mock

from msl.http import FetchResult
from msl.pipeline import run_cycle
from msl.sources import REGISTRY

from tests.helpers import TmpDirCase

NOW = "2026-09-22T12:00:00Z"


def _egress(url):
    return FetchResult(url=url, status=None, body=b"", attempts=3, elapsed_ms=2,
                       error_kind="EgressBlocked",
                       error="TLS/SSL connection has been closed (EOF)")


def _ok_json(url, obj):
    body = json.dumps(obj).encode()
    return FetchResult(url=url, status=200, body=body, attempts=1, elapsed_ms=8,
                       final_url=url, content_type="application/json")


def _real_http_error(url, code=500):
    return FetchResult(url=url, status=code, body=b"", attempts=3, elapsed_ms=40,
                       error_kind="HTTPError", error=f"HTTP {code} Server Error")


class EgressIsNotAFinding(TmpDirCase):
    """An egress wall is a fact about us, never about the source."""

    def setUp(self):
        super().setUp()
        self._snap = [(s.id, s.status, s.consecutive_failures, s.live_reads)
                      for s in REGISTRY]

        def restore():
            by_id = {s.id: s for s in REGISTRY}
            for sid, st, cf, lr in self._snap:
                s = by_id[sid]
                s.status, s.consecutive_failures, s.live_reads = st, cf, lr
        self.addCleanup(restore)

    def _register(self):
        return json.loads((self.dir / "irregularities.json").read_text())["items"]

    def test_no_source_is_marked_blocked_by_an_egress_wall(self):
        """The headline assertion: blocked is a claim about someone else's service.

        Compared against the baseline rather than against zero, because the
        registry legitimately starts with sources already blocked by real HTTP
        failures recorded in a previous cycle.  What an egress wall must not do is
        ADD to that set.
        """
        baseline = {sid for sid, st, _, _ in self._snap if st == "blocked"}
        with mock.patch("msl.pipeline.fetch", side_effect=lambda u, **k: _egress(u)):
            run_cycle(offline=False, data_dir=self.dir, now_override=NOW,
                      docs_dir=self.dir, max_tasks=8)
        blocked = {s.id for s in REGISTRY if s.status == "blocked"}
        self.assertEqual(blocked - baseline, set(),
                         f"egress wall newly marked these blocked: {blocked - baseline}")

    def test_an_egress_wall_does_not_escalate_consecutive_failures(self):
        """consecutive_failures drives CRITICAL, so it must not count our outage."""
        before = {s.id: s.consecutive_failures for s in REGISTRY}
        with mock.patch("msl.pipeline.fetch", side_effect=lambda u, **k: _egress(u)):
            run_cycle(offline=False, data_dir=self.dir, now_override=NOW,
                      docs_dir=self.dir, max_tasks=8)
        changed = {s.id: (before[s.id], s.consecutive_failures) for s in REGISTRY
                   if before[s.id] != s.consecutive_failures}
        self.assertEqual(changed, {},
                         f"egress wall moved consecutive_failures: {changed}")

    def test_egress_failures_are_aggregated_into_one_finding(self):
        """N unreachable sources must not become N register rows."""
        with mock.patch("msl.pipeline.fetch", side_effect=lambda u, **k: _egress(u)):
            run_cycle(offline=False, data_dir=self.dir, now_override=NOW,
                      docs_dir=self.dir, max_tasks=8)
        items = self._register()
        egress = [i for i in items if "could not egress" in i["title"]]
        self.assertEqual(len(egress), 1, f"expected one aggregated row, got {len(egress)}")
        per_source = [i for i in items if i["title"].endswith("could not be read")]
        self.assertEqual(per_source, [],
                         "an egress failure must not be filed as a source failure")

    def test_the_aggregated_finding_says_it_proves_nothing_about_the_source(self):
        with mock.patch("msl.pipeline.fetch", side_effect=lambda u, **k: _egress(u)):
            run_cycle(offline=False, data_dir=self.dir, now_override=NOW,
                      docs_dir=self.dir, max_tasks=8)
        row = [i for i in self._register() if "could not egress" in i["title"]][0]
        self.assertEqual(row["severity"], "warn")
        self.assertIn("NONE of them is marked blocked", row["detail"])
        self.assertIn("not of those services", row["detail"])

    def test_a_real_http_failure_still_blocks_the_source(self):
        """The fix must not neuter genuine failure detection."""
        with mock.patch("msl.pipeline.fetch",
                        side_effect=lambda u, **k: _real_http_error(u, 500)):
            run_cycle(offline=False, data_dir=self.dir, now_override=NOW,
                      docs_dir=self.dir, max_tasks=8)
        items = self._register()
        self.assertTrue(any(i["title"].endswith("could not be read") for i in items),
                        "a 500 must still be filed against the source")
        self.assertTrue(any(s.status == "blocked" for s in REGISTRY),
                        "a 500 must still block the source")
        self.assertFalse(any("could not egress" in i["title"] for i in items),
                         "an HTTP 500 is not an egress problem")

    def test_a_mixed_cycle_blocks_only_the_genuinely_failing_source(self):
        """One real failure plus an egress wall: exactly one source is blocked."""
        seen = {"n": 0}

        def responder(url, **kw):
            seen["n"] += 1
            # The first read succeeds so stats.ok > 0, which is the evidence that
            # distinguishes an allowlist from a total outage.
            if seen["n"] == 1:
                return _ok_json(url, {"items": []})
            if seen["n"] == 2:
                # A 500 is the source failing.  A 404 would be a caller-fault status
                # (msl/pipeline.CALLER_FAULT_STATUSES): it says the addressed thing
                # does not exist, which is a fact about the URL, not an outage — see
                # CallerFaultIsNotASourceOutage in tests/test_pipeline.py.
                return _real_http_error(url, 500)
            return _egress(url)

        with mock.patch("msl.pipeline.fetch", side_effect=responder):
            run_cycle(offline=False, data_dir=self.dir, now_override=NOW,
                      docs_dir=self.dir, max_tasks=8)
        items = self._register()
        self.assertTrue(any("could not egress" in i["title"] for i in items))
        self.assertTrue(any(i["title"].endswith("could not be read") for i in items))
        baseline = {sid for sid, st, _, _ in self._snap if st == "blocked"}
        newly = {s.id for s in REGISTRY if s.status == "blocked"} - baseline
        self.assertEqual(len(newly), 1,
                         f"exactly one source should be newly blocked, got {newly}")

    def test_no_claim_is_produced_from_an_unreachable_source(self):
        """The whole point: no evidence, no claim — and no invented substitute."""
        with mock.patch("msl.pipeline.fetch", side_effect=lambda u, **k: _egress(u)):
            rep = run_cycle(offline=False, data_dir=self.dir, now_override=NOW,
                            docs_dir=self.dir, max_tasks=8)
        self.assertEqual(rep.fetch_ok, 0)
        claims = (self.dir / "claims.jsonl")
        captured = [json.loads(l) for l in claims.read_text().splitlines() if l.strip()] \
            if claims.exists() else []
        self.assertEqual([c for c in captured if c.get("kind") == "captured"], [],
                         "an unreachable source produced a captured claim")


if __name__ == "__main__":
    unittest.main()
