"""The evidence gate.  If any of these pass when they should fail, the project
can publish a hallucination, so they are written to fail loudly."""
from __future__ import annotations

import unittest

from msl.evidence import KIND_CAPTURED, KIND_DERIVED, KIND_NEGATIVE, Ledger, RejectedClaim
from tests.helpers import TmpDirCase, ev


class GateRejectsUnsupportedClaims(TmpDirCase):
    def test_captured_claim_without_evidence_is_rejected(self):
        l = fresh = Ledger(self.dir)
        with self.assertRaises(RejectedClaim):
            fresh.accept("t", KIND_CAPTURED, "no evidence behind this", "src",
                         "2026-01-01T00:00:00Z", 1)
        self.assertEqual(len(fresh.claims), 0)
        self.assertEqual(len(fresh.rejections), 0)   # accept() raises; try_accept records

    def test_try_accept_records_the_rejection_instead_of_raising(self):
        l = Ledger(self.dir)
        c = l.try_accept("t", KIND_CAPTURED, "no evidence", "src",
                         "2026-01-01T00:00:00Z", 1)
        self.assertIsNone(c)
        self.assertEqual(len(l.rejections), 1)
        self.assertIn("no evidence row", l.rejections[0]["reason"])

    def test_derived_claim_without_lineage_is_rejected(self):
        l = Ledger(self.dir)
        c = l.try_accept("t", KIND_DERIVED, "arithmetic with no inputs", "derived",
                         "2026-01-01T00:00:00Z", 1, formula="a + b")
        self.assertIsNone(c)
        self.assertEqual(len(l.rejections), 1)

    def test_derived_claim_without_formula_is_rejected(self):
        l = Ledger(self.dir)
        e = ev(l)
        base = l.accept("t", KIND_CAPTURED, "an observation", "src",
                        "2026-01-01T00:00:00Z", 1, evidence=[e.id], value=1)
        c = l.try_accept("t", KIND_DERIVED, "no formula", "derived",
                         "2026-01-01T00:00:00Z", 1, computed_from=[base.id])
        self.assertIsNone(c)

    def test_unknown_evidence_id_is_rejected(self):
        l = Ledger(self.dir)
        c = l.try_accept("t", KIND_CAPTURED, "cites an evidence row that does not exist",
                         "src", "2026-01-01T00:00:00Z", 1, evidence=["E999999"])
        self.assertIsNone(c)
        self.assertIn("unknown evidence id", l.rejections[0]["reason"])

    def test_unknown_computedfrom_id_is_rejected(self):
        l = Ledger(self.dir)
        c = l.try_accept("t", KIND_DERIVED, "cites a claim that does not exist", "derived",
                         "2026-01-01T00:00:00Z", 1, evidence=[], formula="x",
                         computed_from=["C999999"])
        self.assertIsNone(c)
        self.assertIn("unknown computedFrom", l.rejections[0]["reason"])

    def test_empty_statement_is_rejected(self):
        l = Ledger(self.dir)
        e = ev(l)
        c = l.try_accept("t", KIND_CAPTURED, "   ", "src", "2026-01-01T00:00:00Z", 1,
                         evidence=[e.id])
        self.assertIsNone(c)

    def test_unknown_kind_is_rejected(self):
        l = Ledger(self.dir)
        c = l.try_accept("t", "inferred", "a kind that does not exist", "src",
                         "2026-01-01T00:00:00Z", 1)
        self.assertIsNone(c)
        self.assertIn("unknown claim kind", l.rejections[0]["reason"])


class GateAcceptsSupportedClaims(TmpDirCase):
    def test_captured_claim_with_evidence_is_accepted(self):
        l = Ledger(self.dir)
        e = ev(l)
        c = l.accept("t", KIND_CAPTURED, "browser-use/jev-ultrafast has 15,573 stars.",
                     "github_search", "2026-01-01T00:00:00Z", 1,
                     value=15573, unit="stars", evidence=[e.id],
                     field="github.repo[browser-use/jev-ultrafast].stars")
        self.assertEqual(len(l.claims), 1)
        self.assertEqual(c.evidence, [e.id])
        self.assertTrue(c.id.startswith("C"))

    def test_negative_claim_needs_evidence_too(self):
        l = Ledger(self.dir)
        e = ev(l)
        c = l.accept("t", KIND_NEGATIVE, "no such market exists", "kalshi_public",
                     "2026-01-01T00:00:00Z", 1, evidence=[e.id])
        self.assertEqual(c.kind, KIND_NEGATIVE)
        self.assertIsNone(l.try_accept("t", KIND_NEGATIVE, "absence with no proof",
                                       "x", "2026-01-01T00:00:00Z", 1))

    def test_derived_claim_with_lineage_and_formula_is_accepted(self):
        l = Ledger(self.dir)
        e = ev(l)
        a = l.accept("t", KIND_CAPTURED, "first", "s", "2026-01-01T00:00:00Z", 1,
                     value=100.0, evidence=[e.id], field="f.1")
        b = l.accept("t", KIND_CAPTURED, "last", "s", "2026-01-01T00:00:00Z", 1,
                     value=150.0, evidence=[e.id], field="f.2")
        d = l.accept("t", KIND_DERIVED, "rose 50%", "derived", "2026-01-01T00:00:00Z", 1,
                     value=50.0, computed_from=[a.id, b.id],
                     formula="(last - first) / first * 100", field="delta")
        self.assertEqual(d.computed_from, [a.id, b.id])

    def test_evidence_rows_are_append_only_and_hashed(self):
        l = Ledger(self.dir)
        e1 = ev(l, url="https://example.test/1")
        e2 = ev(l, url="https://example.test/2")
        self.assertNotEqual(e1.id, e2.id)
        self.assertEqual(len(e1.payload_sha256), 64)
        lines = (self.dir / "evidence.jsonl").read_text().strip().split("\n")
        self.assertEqual(len(lines), 2)

    def test_fingerprint_ignores_the_value_so_drift_is_detectable(self):
        l = Ledger(self.dir)
        e = ev(l)
        a = l.accept("t", KIND_CAPTURED, "s", "s", "2026-01-01T00:00:00Z", 1,
                     value=1, evidence=[e.id], field="f")
        b = l.accept("t", KIND_CAPTURED, "s", "s", "2026-01-01T00:00:00Z", 2,
                     value=2, evidence=[e.id], field="f")
        self.assertEqual(a.fingerprint, b.fingerprint)


class LedgerPersistence(TmpDirCase):
    def test_ledger_reloads_from_disk(self):
        l = Ledger(self.dir)
        e = ev(l)
        l.accept("t", KIND_CAPTURED, "kept", "s", "2026-01-01T00:00:00Z", 1,
                 value=7, evidence=[e.id], field="f")
        again = Ledger(self.dir)
        self.assertEqual(len(again.claims), 1)
        self.assertEqual(len(again.evidence), 1)
        self.assertEqual(again.claims[0].value, 7)

    def test_ids_do_not_restart_after_reload(self):
        l = Ledger(self.dir)
        e = ev(l)
        first = l.accept("t", KIND_CAPTURED, "a", "s", "2026-01-01T00:00:00Z", 1,
                         value=1, evidence=[e.id], field="f")
        again = Ledger(self.dir)
        e2 = again.add_evidence("s", "https://example.test/2", "2026-01-01T00:00:00Z",
                                200, body=b"{}")
        second = again.accept("t", KIND_CAPTURED, "b", "s", "2026-01-01T00:00:00Z", 1,
                              value=2, evidence=[e2.id], field="g")
        self.assertNotEqual(first.id, second.id)


if __name__ == "__main__":
    unittest.main()
