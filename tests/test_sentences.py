"""The defective-sentence detector must count history without crying wolf.

These sentences are in the append-only ledger and cannot be deleted.  The detector
is what keeps them visible; if it matched a *correct* sentence it would turn a real
finding into noise, so the false-positive cases are tested as carefully as the true
ones.
"""
from __future__ import annotations

import pathlib
import unittest

from msl.evidence import Ledger
from msl.sentences import DEFECTS, find_defects

ROOT = pathlib.Path(__file__).resolve().parent.parent


class SentenceDetector(unittest.TestCase):
    def test_the_real_counts_match_what_was_found_by_hand(self):
        """The numbers quoted in the fix's own documentation.

        Read from the published ledger, so this test fails loudly if the detector
        stops seeing rows that are really there.
        """
        found = find_defects(Ledger(ROOT / "data").claims)
        counts = {k: len(v) for k, v in found.items()}
        self.assertEqual(counts.get("SENT-DOUBLED-PHRASE"), 80,
                         "the Federal Register template published 80 doubled sentences")
        self.assertEqual(counts.get("SENT-EMPTY-SUBJECT"), 16,
                         "16 rows name no subject at all")
        self.assertGreaterEqual(counts.get("SENT-PLACEHOLDER-ARGUMENT", 0), 39,
                                "at least the 39 placeholder-argument rows")

    def test_every_defect_id_is_unique_and_has_a_fix(self):
        ids = [d["id"] for d in DEFECTS]
        self.assertEqual(len(ids), len(set(ids)))
        for d in DEFECTS:
            self.assertTrue(d["symptom"] and d["fix"], d["id"])

    def test_correct_sentences_are_not_matched(self):
        """The repaired templates' output, which is what the next cycle publishes."""

        class Row:
            id = "C1"

        good = [
            "The U.S. Federal Register holds 1,573 documents matching “artificial intelligence”.",
            "The U.S. Federal Register holds 1,573 documents in total. The API describes this "
            "query as “Documents matching 'artificial intelligence'”.",
            "USGS counts 41 earthquakes between 2026-09-09 and 2026-09-15, at magnitude 5.0 "
            "and above.",
            "USGS counts 40 earthquakes from 2026-09-14 to the time of this read, at "
            "magnitude 5.0 and above.",
            "BLS reports series CUUR0000SA0 at 334.98 for August 2026.",
            "Nominatim returns 1 place result(s) for “Seoul”.",
            "GitHub Search reports 52,142 repositories matching the seeded GitHub query "
            "“AI agents created:>=2026-08-22”.",
            "The GitHub Releases API lists no release for browser-use/jev-ultrafast.",
        ]
        for text in good:
            rows = []
            for t in [text]:
                r = Row()
                r.statement = t
                rows.append(r)
            self.assertEqual(find_defects(rows), {}, f"false positive on: {text}")

    def test_the_known_bad_sentences_are_matched(self):
        class Row:
            id = "C2"

        bad = [
            "The U.S. Federal Register holds 1,573 documents matching Documents matching "
            "'artificial intelligence'.",
            "BLS reports series ? at 334.98 for August 2026.",
            "USGS counts 40 earthquakes the configured window.",
            "GitHub Search reports 3,667,127 repositories matching .",
            "Nominatim returns 1 place result(s) for the query.",
        ]
        matched = []
        for text in bad:
            r = Row()
            r.statement = text
            matched.append(bool(find_defects([r])))
        self.assertEqual(matched, [True] * len(bad), "a known-bad sentence went unnoticed")


if __name__ == "__main__":
    unittest.main()
