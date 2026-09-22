"""Command line entry point.  ``python3 -m msl.cli <command>``."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
from typing import Any, Dict, List

from . import config
from .evidence import Ledger
from .http import fetch
from .irregularities import Register
from .pipeline import run_cycle
from .reason import recheck_derived
from .sources import REGISTRY
from .topics import Library


def cmd_cycle(args: argparse.Namespace) -> int:
    rep = run_cycle(offline=args.offline, max_tasks=args.max_tasks,
                    publish=not args.no_publish,
                    seed_dir=pathlib.Path(args.seed_dir) if args.seed_dir else None)
    ac = rep.auto_counts()
    print(f"cycle {rep.cycle} @ {rep.at}  mode={rep.mode}  {rep.duration_ms}ms")
    print(f"  reads      ok={ac['fetchOk']} failed={ac['fetchFailed']} "
          f"bytes={ac['bytesIn']:,}")
    print(f"  claims     total={ac['claims']:,} new={ac['claimsNewThisCycle']:,} "
          f"rejected={ac['claimsRejectedByGate']:,} derived={ac['derivedClaims']:,}")
    print(f"  recheck    {ac['derivedRechecks']} checked, {ac['derivedDrifts']} drifted, "
          f"{ac['derivedNotRecheckable']} not recheckable")
    print(f"  topics     {ac['topics']} (new {ac['newTopics']})")
    print(f"  compete    {ac['forecastsIssued']} issued, {ac['forecastsScored']} scored")
    print(f"  ideas      {ac['ideas']} (promoted {ac['ideasPromoted']})")
    print(f"  flags      {ac['irregularitiesOpen']} open (new {ac['irregularitiesNew']})")
    print(f"  sources    {ac['sourcesVerified']}/{ac['sourcesRegistered']} verified, "
          f"{ac['sourcesBlocked']} blocked")
    if rep.errors:
        print("  ERRORS:")
        for e in rep.errors:
            print(f"    - {e}")
    return 0 if rep.ok else 1


def cmd_probe(args: argparse.Namespace) -> int:
    """Live-read every registered source.  Writes data/source_health.json."""
    out: List[Dict[str, Any]] = []
    ok = failed = 0
    for s in REGISTRY:
        if args.only and s.id != args.only:
            continue
        r = fetch(s.probe_url, accepts=s.accepts, retries=1)
        row = {"id": s.id, "name": s.name, "operator": s.operator,
               "docsUrl": s.docs_url, "probeUrl": s.probe_url,
               "status": r.status, "ok": r.ok, "bytes": r.size,
               "elapsedMs": r.elapsed_ms, "error": r.describe_error() if not r.ok else "",
               "sha256": r.sha256[:16] if r.body else "",
               "checkedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        out.append(row)
        if r.ok:
            ok += 1
            s.status = "verified-live-read"
            s.live_reads += 1
            s.consecutive_failures = 0
            s.last_read_at = row["checkedAt"]
            s.last_status = r.status
            s.last_error = ""
        else:
            failed += 1
            s.consecutive_failures += 1
            s.status = "blocked"
            s.last_error = r.describe_error()
            s.last_read_at = row["checkedAt"]
            s.last_status = r.status
        print(f"{'OK ' if r.ok else 'ERR'} {r.status or '---'} {r.elapsed_ms:>5}ms "
              f"{r.size:>8}B  {s.id:<22} {r.describe_error() if not r.ok else ''}")
    payload = {"generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "ok": ok, "failed": failed, "results": out}
    p = config.DATA / "source_health.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    print(f"\n{ok} ok / {failed} failed → {p}")
    return 0


def cmd_verify_claims(args: argparse.Namespace) -> int:
    """Read-only: recompute every derived claim and report drift."""
    ledger = Ledger()
    res = recheck_derived(ledger, cycle=0,
                          now=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print(f"derived claims rechecked : {res.rechecks}")
    print(f"not recheckable          : {res.not_recheckable}")
    print(f"drift detected           : {len(res.drift)}")
    for d in res.drift:
        print(f"  {d.get('claimId')} {d.get('field')} "
              f"published={d.get('old')!r} recomputed={d.get('new')!r} "
              f"({d.get('reason')})")
    return 1 if res.drift else 0


def cmd_gate_report(args: argparse.Namespace) -> int:
    """Read-only: what the evidence gate has rejected, and why."""
    ledger = Ledger()
    counts = ledger.counts()
    print("accepted by kind:")
    for k, v in sorted(counts.items()):
        print(f"  {k:<12} {v:,}")
    print(f"  {'TOTAL':<12} {len(ledger.claims):,}")
    print(f"rejected this run: {len(ledger.rejections)}")
    for r in ledger.rejections[-40:]:
        print(f"  - [{r.get('kind','?')}/{r.get('sourceId','?')}] {r['reason']}")
    return 0


def cmd_topic(args: argparse.Namespace) -> int:
    """Read-only: dump one topic and its verified claims."""
    library = Library()
    t = library.get(args.slug)
    if t is None:
        print(f"no such topic: {args.slug}")
        print("topics: " + ", ".join(sorted(library.topics)[:40]))
        return 1
    print(json.dumps(t.as_dict(), indent=1, ensure_ascii=False))
    ledger = Ledger()
    claims = ledger.by_topic(args.slug)
    print(f"\n{len(claims)} verified claims:")
    for c in claims[-60:]:
        print(f"  {c.id} [{c.kind}] {c.statement}")
        for e in c.evidence:
            print(f"      evidence {e}")
    return 0


def cmd_sources(args: argparse.Namespace) -> int:
    from .sources import KEYED_SOURCES_EXCLUDED
    print(f"{len(REGISTRY)} registered sources")
    for s in REGISTRY:
        print(f"  {s.id:<22} {s.status:<20} reads={s.live_reads:<3} {s.name}")
        print(f"      docs: {s.docs_url}")
    print(f"\n{len(KEYED_SOURCES_EXCLUDED)} excluded for requiring a key:")
    for x in KEYED_SOURCES_EXCLUDED:
        print(f"  {x['id']:<18} {x['reason'][:110]}")
    return 0


def cmd_selftest(args: argparse.Namespace) -> int:
    """The gate must actually reject.  If this prints PASS the gate is wired."""
    ledger = Ledger("/tmp/msl-selftest-nonexistent")
    bad = ledger.try_accept("t", "captured", "a claim with no evidence", "s",
                            "2026-01-01T00:00:00Z", 1)
    bad2 = ledger.try_accept("t", "derived", "a derivation with no lineage", "derived",
                             "2026-01-01T00:00:00Z", 1, formula="x")
    ok = bad is None and bad2 is None and len(ledger.rejections) == 2
    print("gate rejects unsupported captured claim :", bad is None)
    print("gate rejects lineage-less derived claim :", bad2 is None)
    print("both rejections recorded                :", len(ledger.rejections) == 2)
    print("PASS" if ok else "FAIL — THE GATE IS NOT WIRED")
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 -m msl.cli",
                                description="MasterSelfLearn autonomous research engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("cycle", help="run one full cycle")
    c.add_argument("--offline", action="store_true",
                   help="run the identical pipeline against data/seed/ with no network")
    c.add_argument("--max-tasks", type=int, default=None)
    c.add_argument("--no-publish", action="store_true",
                   help="do not regenerate the site and docs")
    c.add_argument("--seed-dir", default=None,
                   help="offline only: read this seed corpus instead of data/seed/")
    c.set_defaults(fn=cmd_cycle)

    pr = sub.add_parser("probe", help="live-read every registered source")
    pr.add_argument("--only", default=None)
    pr.set_defaults(fn=cmd_probe)

    v = sub.add_parser("verify-claims", help="read-only derived-claim recheck")
    v.set_defaults(fn=cmd_verify_claims)

    g = sub.add_parser("gate-report", help="read-only evidence-gate report")
    g.set_defaults(fn=cmd_gate_report)

    t = sub.add_parser("topic", help="dump one topic and its verified claims")
    t.add_argument("slug")
    t.set_defaults(fn=cmd_topic)

    s = sub.add_parser("sources", help="list the source registry")
    s.set_defaults(fn=cmd_sources)

    st = sub.add_parser("selftest", help="prove the evidence gate rejects")
    st.set_defaults(fn=cmd_selftest)
    return p


def main(argv: List[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
