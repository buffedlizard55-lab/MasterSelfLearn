#!/usr/bin/env python3
"""Read-only verifier for every accepted claim and every derived computation.

The verifier never writes. It distinguishes legacy rows (schema version 1,
created before the strict trace contract) from schema-v2 rows. Legacy limitations
are counted and printed; a new schema-v2 violation or arithmetic drift exits 1.

    python3 tools/verify_claims.py
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys
import time
from typing import Any, Dict, List

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from msl.evidence import Ledger                             # noqa: E402
from msl.reason import recheck_derived                      # noqa: E402
from msl.sources import REGISTRY                            # noqa: E402
from msl.topics import Library                              # noqa: E402


def _strict_json(value: Any) -> bool:
    try:
        json.dumps(value, allow_nan=False)
        return True
    except (TypeError, ValueError):
        return False


def _trace_problems(ledger: Ledger) -> Dict[str, List[str]]:
    """Return strict-contract failures split into new and historical rows."""
    evidence = {e.id: e for e in ledger.evidence}
    claims = {c.id: c for c in ledger.claims}
    out: Dict[str, List[str]] = {"strict": [], "legacy": []}

    for c in ledger.claims:
        problems: List[str] = []
        if not _strict_json(c.value):
            problems.append("value is not strict JSON")
        if c.kind in ("captured", "documented", "negative"):
            if not c.evidence:
                problems.append("no evidence id")
            if not c.field:
                problems.append("no stable field")
            if not c.source_path:
                problems.append("no sourcePath")
            if not c.url:
                problems.append("no source URL")
            for evidence_id in c.evidence:
                e = evidence.get(evidence_id)
                if e is None:
                    problems.append(f"unknown evidence {evidence_id}")
                    continue
                if not e.successful:
                    problems.append(f"evidence {evidence_id} is not a complete 2xx read")
                if not e.has_integrity_hash:
                    problems.append(f"evidence {evidence_id} has no integrity hash")
                if e.source_id != c.source_id:
                    problems.append(f"evidence {evidence_id} source mismatch")
                if c.url and c.url not in (e.url, e.final_url):
                    problems.append(f"evidence {evidence_id} URL mismatch")
        elif c.kind == "derived":
            if c.source_id != "derived":
                problems.append("derived sourceId is not 'derived'")
            if not c.formula:
                problems.append("derived claim has no formula")
            if not c.computed_from:
                problems.append("derived claim has no lineage")
            unknown = [i for i in c.computed_from if i not in claims]
            if unknown:
                problems.append(f"unknown lineage {unknown[:3]}")
        else:
            problems.append(f"unknown kind {c.kind!r}")

        if problems:
            bucket = "strict" if c.schema_version >= 2 else "legacy"
            out[bucket].append(f"{c.id}: " + "; ".join(problems))
    return out


def main() -> int:
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    ledger = Ledger()
    library = Library()
    res = recheck_derived(ledger, cycle=0, now=now)

    kinds = ledger.counts()
    print("claim ledger")
    for kind in ("captured", "documented", "negative", "derived"):
        print(f"  {kind:<12} {kinds.get(kind, 0):>7,}")
    print(f"  {'TOTAL':<12} {len(ledger.claims):>7,}")
    print(f"  evidence rows {len(ledger.evidence):,}")
    print(f"  gate rejections {len(ledger.rejections):,}")

    integrity = collections.Counter(e.integrity_level for e in ledger.evidence)
    complete = sum(1 for e in ledger.evidence if e.successful)
    traces = _trace_problems(ledger)
    print("\nevidence integrity")
    print(f"  complete successful reads : {complete:,}")
    print(f"  wire hashes               : {integrity.get('wire', 0):,}")
    print(f"  projection-only hashes    : {integrity.get('projection', 0):,}")
    print(f"  missing hashes            : {integrity.get('missing', 0):,}")
    print("  note: projection-only is explicitly not a retained wire-byte hash")

    print("\nclaim trace contract")
    print(f"  schema-v2 violations      : {len(traces['strict']):,}")
    print(f"  legacy limitations        : {len(traces['legacy']):,}")
    for problem in traces["strict"][:30]:
        print(f"    STRICT {problem}")
    for problem in traces["legacy"][:10]:
        print(f"    LEGACY {problem}")
    if len(traces["legacy"]) > 10:
        print(f"    ... {len(traces['legacy']) - 10:,} more legacy rows; not retroactively upgraded")

    exact = collections.Counter(
        (c.field, c.formula, tuple(c.computed_from),
         json.dumps(c.value, sort_keys=True, ensure_ascii=False, allow_nan=False))
        for c in ledger.claims if c.kind == "derived" and _strict_json(c.value)
    )
    duplicate_rows = sum(n - 1 for n in exact.values() if n > 1)
    print("\nderived claims")
    print(f"  rechecked                 : {res.rechecks:,}")
    print(f"  not recheckable           : {res.not_recheckable:,}")
    print(f"  drift                     : {len(res.drift):,}")
    print(f"  historical exact duplicates: {duplicate_rows:,}")
    for drift in res.drift[:50]:
        print(f"    {drift.get('claimId')} {drift.get('field')} "
              f"published={drift.get('old')!r} recomputed={drift.get('new')!r} "
              f"reason={drift.get('reason')}")

    # Two support populations, reported separately and never blended: the
    # row-provable count (a claim row names the topic) and the pre-schema-v2
    # credit accumulator (history the rows can no longer prove).  This used to
    # print only the credit number, which overstated what the ledger can
    # re-prove for entity topics.
    row_counts = ledger.topics_with_claims()
    tracked = len(library.topics)
    row_provable = sum(1 for slug in library.topics if row_counts.get(slug, 0) > 0)
    credit_only = sum(1 for slug, topic in library.topics.items()
                      if row_counts.get(slug, 0) == 0 and topic.claims > 0)
    print("\nlibrary")
    print(f"  topics tracked                     : {tracked}")
    print(f"  with >=1 claim row naming them     : {row_provable}")
    print(f"  with only pre-v2 credit (unproven) : {credit_only}")
    print(f"  with neither                       : {tracked - row_provable - credit_only}")

    print("\nsources")
    for source in REGISTRY:
        print(f"  {source.id:<22} {source.status:<20} "
              f"trust={source.trust_tier:<29} reads={source.live_reads:<3} "
              f"last={source.last_status if source.last_status is not None else '-'}")

    bad = bool(traces["strict"]) or bool(res.drift)
    print("\n" + ("FAIL — a schema-v2 claim or derivation is inconsistent"
                  if bad else "PASS (legacy limitations are reported above, not upgraded)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
