"""The source-health probe.

These tests exist because of a real defect: the probe was duplicated in
``msl/cli.py`` and ``tools/probe_sources.py``, both copies called
``fetch(..., accepts=...)`` against a signature that takes ``accept=``, both
raised ``TypeError`` on the very first source, and the probe had therefore never
run — while the registry still advertised eight sources as ``verified-live-read``
from values typed into ``msl/sources.py`` by hand.  A broken verification tool is
worse than no verification tool, because it looks like the check passed.

Everything here is offline: ``msl.probe.fetch`` is patched, no network is used,
and the global ``REGISTRY`` is snapshotted and restored so a test cannot leak a
status change into the next one.
"""
from __future__ import annotations

import ast
import contextlib
import io
import json
import pathlib
import tempfile
import unittest
from unittest import mock

from msl import probe as probe_mod
from msl.pipeline import run_cycle
from tests.helpers import TmpDirCase
from msl.http import FetchResult
from msl.sources import REGISTRY, Source, load_probe_results


def _called_func_name(node) -> str:
    """The function name a Call node invokes, for Name or Attribute forms."""
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def _calls(tree, name: str) -> bool:
    return any(isinstance(n, ast.Call) and _called_func_name(n) == name
               for n in ast.walk(tree))


def _assigns_status(tree, value: str) -> bool:
    for n in ast.walk(tree):
        if not isinstance(n, ast.Assign):
            continue
        if not (isinstance(n.value, ast.Constant) and n.value.value == value):
            continue
        if any(isinstance(t, ast.Attribute) and t.attr == "status" for t in n.targets):
            return True
    return False


def _snapshot():
    return [(s.id, s.status, s.live_reads, s.last_read_at, s.last_status,
             s.last_error, s.consecutive_failures) for s in REGISTRY]


def _restore(snap):
    by_id = {s.id: s for s in REGISTRY}
    for sid, st, lr, lra, ls, le, cf in snap:
        s = by_id[sid]
        s.status, s.live_reads, s.last_read_at = st, lr, lra
        s.last_status, s.last_error, s.consecutive_failures = ls, le, cf


def _ok(url="", size=10):
    return FetchResult(url=url, status=200, body=b"x" * size, attempts=1,
                       elapsed_ms=5, final_url=url, content_type="application/json")


def _http_error(url="", code=403):
    return FetchResult(url=url, status=code, body=b"", attempts=1, elapsed_ms=5,
                       error_kind="HTTPError", error=f"HTTP {code} Forbidden")


def _ok_json(url, obj):
    body = json.dumps(obj).encode()
    return FetchResult(url=url, status=200, body=body, attempts=1, elapsed_ms=8,
                       final_url=url, content_type="application/json")


def _egress_blocked(url=""):
    return FetchResult(url=url, status=None, body=b"", attempts=1, elapsed_ms=2,
                       error_kind="EgressBlocked",
                       error="TLS/SSL connection has been closed (EOF)")


class ProbeSignature(unittest.TestCase):
    """The exact bug that stopped the probe from ever running."""

    def setUp(self):
        self.snap = _snapshot()
        self.addCleanup(_restore, self.snap)

    def test_probe_calls_fetch_with_the_real_keyword(self):
        """``msl.http.fetch`` takes ``accept``, not ``accepts``.

        This asserts on the call, not on the outcome: an ``accepts=`` typo raises
        ``TypeError`` before any assertion about results could ever run, so the
        regression has to be caught at the call site.
        """
        seen = {}

        def fake_fetch(url, accept=None, retries=None, **kw):
            seen["accept"] = accept
            seen["kw"] = kw
            return _ok(url)

        with mock.patch.object(probe_mod, "fetch", side_effect=fake_fetch):
            rep = probe_mod.probe_registry(only=["github_search"], verbose=False)

        self.assertEqual(rep.ok, 1)
        self.assertEqual(seen["accept"], "application/json")
        self.assertEqual(seen["kw"], {}, "unexpected extra kwargs reached fetch")

    def test_fetch_rejects_the_old_keyword_so_the_typo_cannot_return_silently(self):
        """Guards the guard: if ``fetch`` ever grows ``accepts``, the test above
        would stop proving anything."""
        import inspect

        params = inspect.signature(probe_mod.fetch).parameters
        self.assertIn("accept", params)
        self.assertNotIn("accepts", params)

    def test_every_registry_source_can_be_probed_without_a_typeerror(self):
        """A per-source crash used to abort the whole probe on the first entry."""
        with mock.patch.object(probe_mod, "fetch", side_effect=lambda u, **kw: _ok(u)):
            rep = probe_mod.probe_registry(verbose=False)
        self.assertEqual(rep.attempted, len(REGISTRY))
        self.assertEqual(rep.ok, len(REGISTRY))


class ProbeStatusTransitions(unittest.TestCase):
    def setUp(self):
        self.snap = _snapshot()
        self.addCleanup(_restore, self.snap)

    def test_a_successful_read_is_the_only_thing_that_verifies(self):
        src = REGISTRY[0]
        src.status, src.live_reads = "registered", 0
        probe_mod.apply_result(src, _ok(), "2026-09-22T00:00:00Z")
        self.assertEqual(src.status, "verified-live-read")
        self.assertEqual(src.live_reads, 1)
        self.assertEqual(src.consecutive_failures, 0)
        self.assertEqual(src.last_error, "")

    def test_a_genuine_http_failure_blocks_the_source(self):
        """The *transition* is what is under test, so the counter starts at zero.

        It used to read the counter the registry had replayed from the health ledger,
        so an unattended cycle recording more failures for whichever source happens
        to be first in the registry made this test fail for the wrong reason.
        """
        src = REGISTRY[0]
        src.consecutive_failures = 0
        probe_mod.apply_result(src, _http_error(code=403), "2026-09-22T00:00:00Z")
        self.assertEqual(src.status, "blocked")
        self.assertEqual(src.last_status, 403)
        self.assertEqual(src.consecutive_failures, 1)
        self.assertIn("403", src.last_error)

    def test_egress_failure_does_not_block_the_source(self):
        """A runner with no egress says nothing about the source.  Marking a
        healthy endpoint ``blocked`` because *we* could not leave the building
        would publish a false claim about someone else's service."""
        src = REGISTRY[0]
        src.status, src.last_error = "registered", ""
        probe_mod.apply_result(src, _egress_blocked(), "2026-09-22T00:00:00Z",
                               egress_blocked=True)
        self.assertEqual(src.status, "registered", "egress wall must not block")
        self.assertIn("inconclusive", src.last_error)

    def test_egress_failure_does_not_count_as_a_live_read(self):
        src = REGISTRY[0]
        src.live_reads = 3
        probe_mod.apply_result(src, _egress_blocked(), "2026-09-22T00:00:00Z",
                               egress_blocked=True)
        self.assertEqual(src.live_reads, 3)

    def test_egress_failure_does_not_touch_last_read_at(self):
        src = REGISTRY[0]
        src.last_read_at = "2026-01-01T00:00:00Z"
        probe_mod.apply_result(src, _egress_blocked(), "2026-09-22T00:00:00Z",
                               egress_blocked=True)
        self.assertEqual(src.last_read_at, "2026-01-01T00:00:00Z",
                         "no read happened, so no read may be recorded")

    def test_report_separates_failed_from_inconclusive(self):
        seq = iter([_ok("a"), _http_error("b"), _egress_blocked("c")])
        with mock.patch.object(probe_mod, "fetch", side_effect=lambda u, **k: next(seq)):
            rep = probe_mod.probe_registry(only=[REGISTRY[0].id, REGISTRY[1].id,
                                                 REGISTRY[2].id], verbose=False)
        self.assertEqual((rep.ok, rep.failed, rep.inconclusive), (1, 1, 1))
        self.assertEqual(rep.attempted, 3)

    def test_egress_blocked_is_detected_only_when_every_failure_is_egress(self):
        seq = iter([_egress_blocked("a"), _egress_blocked("b")])
        with mock.patch.object(probe_mod, "fetch", side_effect=lambda u, **k: next(seq)):
            rep = probe_mod.probe_registry(only=[REGISTRY[0].id, REGISTRY[1].id],
                                           verbose=False)
        self.assertTrue(rep.egress_blocked)

        seq = iter([_egress_blocked("a"), _http_error("b")])
        with mock.patch.object(probe_mod, "fetch", side_effect=lambda u, **k: next(seq)):
            rep = probe_mod.probe_registry(only=[REGISTRY[0].id, REGISTRY[1].id],
                                           verbose=False)
        self.assertFalse(rep.egress_blocked,
                         "one real HTTP failure means the wall is not uniform")

    def test_a_crashing_fetch_does_not_abort_the_probe(self):
        """One source raising must not stop the rest from being reported.

        ``msl.http.fetch`` is documented never to raise, so this is belt and
        braces — but the original defect was exactly a raise on the first entry,
        which silently reported nothing about the other 27 sources.
        """
        ids = [REGISTRY[0].id, REGISTRY[1].id, REGISTRY[2].id]
        calls = {"n": 0}

        def flaky(url, **kw):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RuntimeError("boom")
            return _ok(url)

        with mock.patch.object(probe_mod, "fetch", side_effect=flaky):
            rep = probe_mod.probe_registry(only=ids, verbose=False)

        self.assertEqual(rep.attempted, 3, "every source was still probed")
        self.assertEqual(rep.ok, 2)
        self.assertEqual(rep.failed, 1)
        bad = [r for r in rep.rows if not r.ok][0]
        self.assertIn("boom", bad.error)
        self.assertEqual(bad.httpStatus, None)
        self.assertEqual(bad.statusAfter, "blocked",
                         "a raise is a failed read, so it blocks; egress would not")


class ProbeExitCode(unittest.TestCase):
    """The scheduled job has to go red when the probe did not do its job."""

    def test_nothing_attempted_is_a_failure(self):
        self.assertEqual(probe_mod.exit_code(probe_mod.ProbeReport()), 1)

    def test_zero_reachable_is_a_failure(self):
        rep = probe_mod.ProbeReport(rows=[mock.Mock(ok=False)])
        rep.failed = 1
        self.assertEqual(probe_mod.exit_code(rep), 1)

    def test_mostly_inconclusive_is_a_failure(self):
        rep = probe_mod.ProbeReport(ok=4, inconclusive=24,
                                    rows=[mock.Mock() for _ in range(28)])
        self.assertEqual(probe_mod.exit_code(rep), 1)

    def test_a_fully_informative_probe_passes_even_with_failures(self):
        """Per-source failures are *results*.  Failing the probe for finding them
        would punish the tool for working."""
        rep = probe_mod.ProbeReport(ok=20, failed=8,
                                    rows=[mock.Mock() for _ in range(28)])
        self.assertEqual(probe_mod.exit_code(rep), 0)

    def test_summary_names_the_inconclusive_rows(self):
        rep = probe_mod.ProbeReport(ok=4, inconclusive=24,
                                    rows=[mock.Mock(ok=False, egressBlocked=True)
                                          for _ in range(24)]
                                    + [mock.Mock(ok=True, egressBlocked=False)
                                       for _ in range(4)])
        line = probe_mod.summary_line(rep)
        self.assertIn("24 inconclusive", line)
        self.assertIn("proves nothing", line)


class ProbePersistence(unittest.TestCase):
    def setUp(self):
        self.snap = _snapshot()
        self.addCleanup(_restore, self.snap)
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="msl-probe-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(self.dir, ignore_errors=True))

    def test_round_trip_from_report_to_registry(self):
        """The ledger the probe writes must be the ledger the registry replays."""
        src = next(s for s in REGISTRY if s.id == "github_search")
        with mock.patch.object(probe_mod, "fetch", side_effect=lambda u, **k: _ok(u)):
            rep = probe_mod.probe_registry(only=["github_search"], verbose=False)
        recorded = rep.rows[0].liveReads
        path = probe_mod.write_report(rep, self.dir / "health.json")
        self.assertTrue(path.exists())

        # Pretend a fresh process: wipe the in-memory state, then replay.
        src.status, src.live_reads, src.last_read_at = "registered", 0, ""
        applied = load_probe_results(path)
        self.assertEqual(applied, 1)
        self.assertEqual(src.status, "verified-live-read")
        self.assertEqual(src.live_reads, recorded,
                         "replay must restore the recorded count, not recount")
        self.assertEqual(src.last_read_at, rep.rows[0].checkedAt)

    def test_missing_ledger_applies_nothing_and_verifies_nothing(self):
        """The honest default: no recorded read means no verified source."""
        self.assertEqual(load_probe_results(self.dir / "absent.json"), 0)

    def test_corrupt_ledger_applies_nothing_rather_than_raising(self):
        p = self.dir / "bad.json"
        p.write_text("{not json", encoding="utf-8")
        self.assertEqual(load_probe_results(p), 0)

    def test_unknown_source_ids_are_ignored_not_invented(self):
        p = self.dir / "h.json"
        p.write_text(json.dumps({"results": [
            {"id": "no_such_source", "statusAfter": "verified-live-read",
             "liveReads": 9, "checkedAt": "2026-09-22T00:00:00Z"}]}), encoding="utf-8")
        self.assertEqual(load_probe_results(p), 0)
        self.assertNotIn("no_such_source", {s.id for s in REGISTRY})

    def test_payload_records_the_egress_distinction(self):
        rep = probe_mod.ProbeReport(ok=1, inconclusive=1,
                                    rows=[mock.Mock(ok=True, egressBlocked=False,
                                                    as_dict=lambda: {"ok": True})])
        payload = rep.payload()
        for key in ("generatedAt", "attempted", "ok", "failed", "inconclusive",
                    "egressBlocked", "results"):
            self.assertIn(key, payload)


class EntryPointEndToEnd(unittest.TestCase):
    """Drive both entry points through their real ``main()``.

    The original defect was invisible to every existing test because the tests
    covered ``msl.*`` while the bug lived in the two entry points.  Executing
    ``main()`` with ``fetch`` patched exercises argument parsing, the shared
    loop, the ledger write and the exit code in one go — the path a human or a
    scheduled job actually takes.
    """

    def setUp(self):
        self.snap = _snapshot()
        self.addCleanup(_restore, self.snap)
        # Both entry points print their per-source table; keep the test log clean.
        quiet = contextlib.redirect_stdout(io.StringIO())
        quiet.__enter__()
        self.addCleanup(quiet.__exit__, None, None, None)
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="msl-ep-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(self.dir, ignore_errors=True))
        self.health = pathlib.Path(probe_mod.__file__).resolve().parent.parent \
            / "data" / "source_health.json"
        if self.health.exists():
            # The tests overwrite the real ledger; put it back afterwards.
            self._saved_health = self.health.read_text(encoding="utf-8")
            self.addCleanup(lambda: self.health.write_text(
                self._saved_health, encoding="utf-8"))
        else:
            self.addCleanup(self.health.unlink, True)

    def test_tools_probe_sources_runs_end_to_end(self):
        import importlib.util

        path = (pathlib.Path(probe_mod.__file__).resolve().parent.parent
                / "tools" / "probe_sources.py")
        spec = importlib.util.spec_from_file_location("_probe_tool", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        with mock.patch.object(probe_mod, "fetch", side_effect=lambda u, **k: _ok(u)):
            rc = mod.main(["tools/probe_sources.py", "github_search", "pypi_json"])

        self.assertEqual(rc, 0)
        payload = json.loads(self.health.read_text(encoding="utf-8"))
        self.assertEqual(payload["ok"], 2)
        self.assertEqual(payload["attempted"], 2)
        self.assertEqual({r["id"] for r in payload["results"]},
                         {"github_search", "pypi_json"})

    def test_cli_probe_runs_end_to_end(self):
        from msl.cli import main as cli_main

        with mock.patch.object(probe_mod, "fetch", side_effect=lambda u, **k: _ok(u)):
            rc = cli_main(["probe", "--only", "github_search"])

        self.assertEqual(rc, 0)
        payload = json.loads(self.health.read_text(encoding="utf-8"))
        self.assertEqual(payload["ok"], 1)

    def test_cli_probe_goes_red_when_the_runner_has_no_egress(self):
        """The daily job must not report success for a probe that proved nothing."""
        from msl.cli import main as cli_main

        with mock.patch.object(probe_mod, "fetch",
                               side_effect=lambda u, **k: _egress_blocked(u)):
            rc = cli_main(["probe", "--only", "github_search"])
        self.assertEqual(rc, 1)

    def test_both_entry_points_agree_on_the_exit_code(self):
        """They used to be two implementations; now they must be one behaviour."""
        import importlib.util

        from msl.cli import main as cli_main
        path = (pathlib.Path(probe_mod.__file__).resolve().parent.parent
                / "tools" / "probe_sources.py")
        spec = importlib.util.spec_from_file_location("_probe_tool2", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        for responder in (lambda u, **k: _ok(u),
                          lambda u, **k: _egress_blocked(u),
                          lambda u, **k: _http_error(u)):
            with mock.patch.object(probe_mod, "fetch", side_effect=responder):
                a = cli_main(["probe", "--only", "github_search"])
            _restore(self.snap)
            with mock.patch.object(probe_mod, "fetch", side_effect=responder):
                b = mod.main(["probe_sources.py", "github_search"])
            _restore(self.snap)
            self.assertEqual(a, b, f"entry points disagreed for {responder}")


class RegistryHonesty(unittest.TestCase):
    """Nothing may claim a source is verified by hand."""

    def test_no_source_hardcodes_a_probe_state(self):
        """The registry's own docstring says these fields are probe-written.

        Eight entries used to carry ``status="verified-live-read"`` typed in by
        hand, so the site advertised verified sources that no code in this
        repository had ever read.  Read the source text, not the live objects,
        because ``load_probe_results`` legitimately mutates them at import.
        """
        text = (pathlib.Path(probe_mod.__file__).resolve().parent
                / "sources.py").read_text(encoding="utf-8")
        # Report the offending line, not the whole 400-line module: assertNotIn
        # prints its haystack, which is unreadable at this file size.
        for needle in ('status="verified-live-read"', "last_status=200"):
            hits = [f"  L{i}: {ln.strip()}" for i, ln in enumerate(text.splitlines(), 1)
                    if needle in ln]
            self.assertEqual(hits, [], f"{needle} is hand-set in msl/sources.py:\n"
                                       + "\n".join(hits))

    def test_sources_module_declares_the_ledger_it_replays(self):
        text = (pathlib.Path(probe_mod.__file__).resolve().parent
                / "sources.py").read_text(encoding="utf-8")
        self.assertIn("load_probe_results", text)
        self.assertIn("source_health.json", text)

    def test_only_the_probe_module_moves_status(self):
        """Guards against a second copy of the probe appearing.

        Status may be *assigned* in ``msl/probe.py`` and in the pipeline (which
        records a real read during a cycle).  The two entry points must only
        delegate — that is where the duplicated-and-broken copies used to live.
        The check looks for assignment, not for the string, because the entry
        points legitimately *describe* the status names in their docstrings.
        """
        repo = pathlib.Path(probe_mod.__file__).resolve().parent.parent
        for rel in ("msl/cli.py", "tools/probe_sources.py"):
            text = (repo / rel).read_text(encoding="utf-8")
            tree = ast.parse(text)

            # Walk the AST rather than the text: both files legitimately *describe*
            # fetch() and the status names in their docstrings, and a substring
            # check on prose produces a test that fails for the wrong reason.
            self.assertFalse(_assigns_status(tree, "verified-live-read"),
                             f"{rel} assigns status itself; call msl.probe instead")
            self.assertFalse(_calls(tree, "fetch"),
                             f"{rel} must not implement its own read loop")
            self.assertIn("probe_registry", text,
                          f"{rel} must call the shared probe loop")

    def test_the_probe_loop_exists_exactly_once(self):
        """The defect was duplication.  Assert there is one loop to break."""
        repo = pathlib.Path(probe_mod.__file__).resolve().parent.parent
        needle = "def probe_registry"
        defs = []
        for py in sorted(repo.rglob("*.py")):
            # tests/ is excluded: this file necessarily names the function it is
            # guarding, and so would always match itself.
            if ".git" in py.parts or "tests" in py.parts:
                continue
            if needle in py.read_text(encoding="utf-8"):
                defs.append(str(py.relative_to(repo)))
        self.assertEqual(defs, ["msl/probe.py"],
                         f"probe loop duplicated in {defs}")

    def test_source_dataclass_defaults_are_honest(self):
        s = Source(id="x", name="x", operator="o", docs_url="d", probe_url="p")
        self.assertEqual(s.status, "registered")
        self.assertEqual(s.live_reads, 0)
        self.assertEqual(s.last_read_at, "")
        self.assertIsNone(s.last_status)


if __name__ == "__main__":
    unittest.main()


class MergedHealthLedger(unittest.TestCase):
    """One ledger, two writers.

    The probe and a cycle both read sources.  When only the probe wrote
    data/source_health.json, the file went stale between the daily probe runs and
    the Sources page showed a probe table saying "4 ok / 24 inconclusive"
    directly above a registry table saying "23 verified" — two honest records
    that visibly contradicted each other.
    """

    def setUp(self):
        self.snap = _snapshot()
        self.addCleanup(_restore, self.snap)
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="msl-merge-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(self.dir, ignore_errors=True))
        self.ledger = self.dir / "source_health.json"

    def _write_initial(self):
        self.ledger.write_text(json.dumps({
            "generatedAt": "2026-09-22T00:00:00Z", "mode": "local",
            "attempted": 2, "ok": 1, "failed": 0, "inconclusive": 1,
            "egressBlocked": True, "note": "old", "results": [
                {"id": "github_search", "ok": True, "httpStatus": 200, "bytes": 10,
                 "sha256": "aa" * 8, "checkedAt": "2026-09-22T00:00:00Z",
                 "statusAfter": "verified-live-read", "egressBlocked": False,
                 "verdict": True, "via": "probe"},
                {"id": "arxiv", "ok": False, "httpStatus": None, "bytes": 0,
                 "sha256": "", "checkedAt": "2026-09-22T00:00:00Z",
                 "statusAfter": "registered", "egressBlocked": True,
                 "verdict": False, "via": "probe"},
            ]}), encoding="utf-8")

    def test_reads_not_made_this_cycle_are_preserved(self):
        """A cycle reading 1 of 28 sources must not erase the other 27."""
        self._write_initial()
        src = next(s for s in REGISTRY if s.id == "pypi_json")
        probe_mod.record_reads([(src, _ok("u"), "2026-09-22T01:00:00Z", False)],
                               path=self.ledger, mode="cycle-9", apply=False)
        rows = json.loads(self.ledger.read_text(encoding="utf-8"))["results"]
        ids = {r["id"] for r in rows}
        self.assertIn("arxiv", ids, "a source not read this cycle was erased")
        self.assertIn("github_search", ids)
        self.assertIn("pypi_json", ids)

    def test_a_cycle_read_replaces_the_stale_probe_row(self):
        self._write_initial()
        src = next(s for s in REGISTRY if s.id == "arxiv")
        probe_mod.record_reads([(src, _ok("u"), "2026-09-22T01:00:00Z", False)],
                               path=self.ledger, mode="cycle-9", apply=False)
        rows = {r["id"]: r for r in
                json.loads(self.ledger.read_text(encoding="utf-8"))["results"]}
        self.assertTrue(rows["arxiv"]["ok"], "the stale inconclusive row survived")
        self.assertEqual(rows["arxiv"]["via"], "cycle-9")
        self.assertFalse(rows["arxiv"]["egressBlocked"])

    def test_apply_false_does_not_double_count(self):
        """The cycle already folds results into the registry inline."""
        src = next(s for s in REGISTRY if s.id == "github_search")
        src.live_reads, src.consecutive_failures = 5, 2
        probe_mod.record_reads([(src, _ok("u"), "2026-09-22T01:00:00Z", False)],
                               path=self.ledger, mode="cycle-9", apply=False)
        self.assertEqual(src.live_reads, 5, "live_reads was double-counted")
        self.assertEqual(src.consecutive_failures, 2,
                         "consecutive_failures was double-counted; it drives CRITICAL")

    def test_apply_true_does_count(self):
        src = next(s for s in REGISTRY if s.id == "github_search")
        src.live_reads, src.status = 5, "registered"
        probe_mod.record_reads([(src, _ok("u"), "2026-09-22T01:00:00Z", False)],
                               path=self.ledger, mode="probe", apply=True)
        self.assertEqual(src.live_reads, 6)
        self.assertEqual(src.status, "verified-live-read")

    def test_totals_span_the_merged_rows_not_just_this_write(self):
        self._write_initial()
        src = next(s for s in REGISTRY if s.id == "pypi_json")
        probe_mod.record_reads([(src, _ok("u"), "2026-09-22T01:00:00Z", False)],
                               path=self.ledger, mode="cycle-9", apply=False)
        doc = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertEqual(doc["attempted"], 3)
        self.assertEqual(doc["ok"], 2, "github_search + pypi_json")
        self.assertEqual(doc["inconclusive"], 1, "arxiv was never re-read")
        self.assertEqual(doc["lastWriter"], "cycle-9")
        self.assertEqual(doc["lastWriteCounts"]["ok"], 1, "this write read one source")

    def test_a_corrupt_existing_ledger_is_replaced_not_fatal(self):
        self.ledger.write_text("{not json", encoding="utf-8")
        src = next(s for s in REGISTRY if s.id == "github_search")
        probe_mod.record_reads([(src, _ok("u"), "2026-09-22T01:00:00Z", False)],
                               path=self.ledger, mode="cycle-9", apply=False)
        doc = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertEqual(doc["attempted"], 1)


class CycleWritesTheLedger(TmpDirCase):
    """The cycle and the probe must leave one coherent record behind."""

    def setUp(self):
        super().setUp()
        self.snap = _snapshot()

        def restore():
            by_id = {s.id: s for s in REGISTRY}
            for sid, st, lr, lra, ls, le, cf in self.snap:
                s = by_id[sid]
                s.status, s.live_reads, s.last_read_at = st, lr, lra
                s.last_status, s.last_error, s.consecutive_failures = ls, le, cf
        self.addCleanup(restore)

    def test_a_live_cycle_records_its_reads(self):
        with mock.patch("msl.pipeline.fetch",
                        side_effect=lambda u, **k: _ok_json(u, {"items": []})):
            run_cycle(offline=False, data_dir=self.dir, now_override="2026-09-22T09:00:00Z",
                      docs_dir=self.dir, max_tasks=4)
        p = self.dir / "source_health.json"
        self.assertTrue(p.exists(), "a live cycle wrote no health ledger")
        doc = json.loads(p.read_text(encoding="utf-8"))
        self.assertTrue(doc["lastWriter"].startswith("cycle-"))
        self.assertGreater(doc["ok"], 0)
        for r in doc["results"]:
            self.assertIn("via", r)

    def test_an_offline_cycle_records_nothing(self):
        """A fixture is not evidence that a service is reachable."""
        self.seed_into(self.dir)
        self.cycle("2026-09-22T09:00:00Z")
        p = self.dir / "source_health.json"
        if p.exists():
            doc = json.loads(p.read_text(encoding="utf-8"))
            self.assertFalse(doc["lastWriter"].startswith("cycle-"),
                             "an offline run claimed to have read live endpoints")
