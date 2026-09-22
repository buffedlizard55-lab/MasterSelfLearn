"""Shared test scaffolding.  Everything here runs offline and deterministically."""
from __future__ import annotations

import pathlib
import shutil
import tempfile
import unittest

from msl.evidence import Ledger
from msl.pipeline import run_cycle

REPO = pathlib.Path(__file__).resolve().parent.parent
SEED = REPO / "data" / "seed"
NOW1 = "2026-09-21T12:00:00Z"
NOW2 = "2026-09-21T12:30:00Z"
NOW3 = "2026-09-21T13:00:00Z"


class TmpDirCase(unittest.TestCase):
    """Base class giving each test a throwaway data directory."""

    def setUp(self) -> None:
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="msl-test-"))
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def seed_into(self, dest: pathlib.Path) -> None:
        (dest / "seed").mkdir(parents=True, exist_ok=True)
        for p in SEED.glob("*.json"):
            shutil.copy2(p, dest / "seed" / p.name)

    def cycle(self, now: str, **kw):
        # docs_dir keeps a test from rewriting the repository's own README.md,
        # STATUS.md, VERIFICATION.md and IRREGULARITIES.md.
        kw.setdefault("docs_dir", self.dir)
        return run_cycle(offline=True, publish=kw.pop("publish", True),
                         data_dir=self.dir, now_override=now, **kw)


def fresh_ledger(tmp: pathlib.Path) -> Ledger:
    return Ledger(tmp)


def ev(ledger: Ledger, source_id: str = "github_search", url: str = "https://example.test/x"):
    return ledger.add_evidence(source_id=source_id, url=url, captured_at=NOW1,
                               status=200, body=b'{"ok":true}', capture_mode="test-fixture")
