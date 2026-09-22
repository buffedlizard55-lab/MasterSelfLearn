#!/usr/bin/env python3
"""Read-only verifier: recompute every derived claim and report drift.

Never writes anything.  Exit code 1 when a published derivation no longer
recomputes, so CI can fail on it.

    python3 tools/verify_claims.py
"""
from __future__ import annotations

import sys
import time
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from msl.evidence import Ledger                             # noqa: E402
from msl.reason import recheck_derived                      # noqa: E402
from msl.sources import REGISTRY                            # noqa: E402
from msl.topics import Library                              # noqa: E402


def main() -> int:
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    ledger = Ledger()
    library = Library()
    res = recheck_derived(ledger, cycle=0, now=now)

    kinds = ledger.counts()
    print("claim ledger")
    for k in ("captured", "documented", "negative", "derived"):
        print(f"  {k:<12} {kinds.get(k, 0):>7,}")
    print(f"  {'TOTAL':<12} {len(ledger.claims):>7,}")
    print(f"  evidence rows {len(ledger.evidence):,}")

    unsupported = [c for c in ledger.claims
                   if c.kind in ("captured", "documented", "negative") and not c.evidence]
    orphan_derived = [c for c in ledger.claims
                      if c.kind == "derived" and not c.computed_from]
    print(f"\nintegrity")
    print(f"  captured/documented/negative with no evidence : {len(unsupported)}")
    print(f"  derived with no lineage                       : {len(orphan_derived)}")

    print(f"\nderived claims")
    print(f"  rechecked     : {res.rechecks}")
    print(f"  not recheckable: {res.not_recheckable}  (time-dependent formula)")
    print(f"  drift         : {len(res.drift)}")
    for d in res.drift:
        print(f"    {d.get('claimId')} {d.get('field')} "
              f"published={d.get('old')!r} recomputed={d.get('new')!r}")

    counts = ledger.topics_with_claims()
    tracked = len(library.topics)
    print(f"\nlibrary")
    print(f"  topics tracked           : {tracked}")
    print(f"  with >=1 verified claim  : {len(counts)}")
    print(f"  with 0 verified claims   : {tracked - len(counts)}")

    print(f"\nsources")
    for s in REGISTRY:
        print(f"  {s.id:<22} {s.status:<20} reads={s.live_reads:<3} "
              f"last={s.last_status if s.last_status is not None else '-'}")

    bad = bool(unsupported) or bool(orphan_derived) or bool(res.drift)
    print("\n" + ("FAIL — the ledger is not internally consistent"
                  if bad else "PASS"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
