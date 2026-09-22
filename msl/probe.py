"""The source-health probe — the only code allowed to move a source's ``status``.

There is exactly **one** implementation of the probe loop, here.  Both entry
points (``python3 -m msl.cli probe`` and ``tools/probe_sources.py``) call it.

Why this module exists: the probe used to be duplicated in ``msl/cli.py`` and
``tools/probe_sources.py``.  Both copies called ``fetch(..., accepts=...)`` while
``msl/http.fetch`` takes ``accept=...``.  Both raised ``TypeError`` on the first
source, so the probe had *never* run and ``data/source_health.json`` had never
been written — while ``data/sources.json`` still advertised sources as
``verified-live-read`` from values hard-coded in the registry.  Two copies of a
verification tool that both crash is worse than one, because either one looks
like a working check.  Keep the loop here and keep the two entry points thin.

A status is a fact about the last read, not an editorial opinion:

``verified-live-read``  this process just read the endpoint and recorded the bytes
``registered``          endpoint + docs recorded; no read has succeeded yet
``blocked``             the last read failed; no claim may be produced from it
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional

from . import config
from .http import FetchResult, fetch
from .sources import REGISTRY, Source


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


@dataclass
class ProbeRow:
    """One source, one read, fully recorded."""

    id: str
    name: str
    operator: str
    docsUrl: str
    probeUrl: str
    httpStatus: Optional[int]
    ok: bool
    bytes: int
    elapsedMs: int
    attempts: int
    error: str
    sha256: str
    checkedAt: str
    statusAfter: str
    liveReads: int
    consecutiveFailures: int
    #: True when the read failed because *this runner* could not get out to the
    #: network.  No verdict about the source was reached, so ``statusAfter`` is
    #: whatever it was before and must not be read as "this source is broken".
    egressBlocked: bool = False
    #: Did this probe reach a definitive verdict for this source at all?
    verdict: bool = True

    def as_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)


@dataclass
class ProbeReport:
    generatedAt: str = ""
    mode: str = ""
    ok: int = 0
    failed: int = 0
    #: reads that reached no verdict because this runner could not egress
    inconclusive: int = 0
    rows: List[ProbeRow] = field(default_factory=list)

    @property
    def attempted(self) -> int:
        return len(self.rows)

    @property
    def egress_blocked(self) -> bool:
        """True when the wall of failures is an egress policy, not broken data.

        The tell is uniformity: every unreachable host fails the same way at the
        TLS layer while at least one host works, so the runner is filtering
        destinations rather than the sources being down.
        """
        blocked = [r for r in self.rows if r.egressBlocked]
        return bool(blocked) and len(blocked) == sum(
            1 for r in self.rows if not r.ok)

    def payload(self) -> Dict[str, Any]:
        return {
            "generatedAt": self.generatedAt,
            "mode": self.mode,
            "attempted": self.attempted,
            "ok": self.ok,
            "failed": self.failed,
            "inconclusive": self.inconclusive,
            "egressBlocked": self.egress_blocked,
            "note": (
                "A blocked source produces no claims and no substitute value. Rows with "
                "egressBlocked=true reached NO verdict: this runner could not open a TLS "
                "session to the host, which says nothing about the source, so their "
                "statusAfter is unchanged and must not be read as 'this source is broken'. "
                "statusAfter is written by this probe and by nothing else."
            ),
            "results": [r.as_dict() for r in self.rows],
        }


def apply_result(src: Source, r: FetchResult, at: str, egress_blocked: bool = False) -> None:
    """Fold one read into the registry entry.  Mutates ``src`` in place.

    ``egress_blocked`` means *we* could not get out to the network.  That is a
    fact about this runner, not about the source, so it must not be allowed to
    mark a healthy endpoint ``blocked`` — publishing "blocked" for a source that
    merely could not be reached from a sandboxed runner is a false claim about
    the source, which is the one thing this project exists to avoid.  The status
    is left untouched and the row records why no verdict was reached.
    """
    if egress_blocked:
        src.last_error = f"probe inconclusive — {r.describe_error()}"
        return
    src.last_read_at = at
    src.last_status = r.status
    if r.ok:
        src.status = "verified-live-read"
        src.live_reads += 1
        src.consecutive_failures = 0
        src.last_error = ""
    else:
        src.status = "blocked"
        src.consecutive_failures += 1
        src.last_error = r.describe_error()


def probe_registry(only: Optional[Iterable[str]] = None,
                   retries: int = 1,
                   verbose: bool = True) -> ProbeReport:
    """Live-read every registered source (or only the ids in ``only``).

    Never raises on a transport failure: a failure is a *result*, recorded with
    its HTTP status or transport error, because finding the failures is the point.
    """
    want = set(only) if only else None
    rep = ProbeReport(generatedAt=_now(), mode=config.runtime_mode())

    for s in REGISTRY:
        if want and s.id not in want:
            continue
        at = _now()
        try:
            r = fetch(s.probe_url, accept=s.accepts, retries=retries)
        except Exception as e:  # noqa: BLE001 - one bad source must not abort 27
            # msl.http.fetch is documented never to raise, so reaching here means
            # something unexpected (a bad probe_url, a DNS failure inside the
            # resolver, a programming error).  Record it as a failed read and
            # carry on: a probe that stops at the first bad entry reports nothing
            # about the rest, which is exactly how the original TypeError bug hid.
            r = FetchResult(url=s.probe_url, status=None, body=b"", attempts=1,
                            error_kind=type(e).__name__, error=str(e)[:300])
        # EgressBlocked is recorded by msl.http.fetch when the TLS session is
        # torn down before any HTTP status arrives.  It is a fact about the
        # runner, so it gets no verdict about the source.
        blocked = (not r.ok) and r.error_kind == "EgressBlocked"
        apply_result(s, r, at, egress_blocked=blocked)
        rep.rows.append(ProbeRow(
            id=s.id, name=s.name, operator=s.operator, docsUrl=s.docs_url,
            probeUrl=s.probe_url, httpStatus=r.status, ok=r.ok, bytes=r.size,
            elapsedMs=r.elapsed_ms, attempts=r.attempts,
            error="" if r.ok else r.describe_error(),
            sha256=r.sha256[:16] if r.body else "", checkedAt=at,
            statusAfter=s.status, liveReads=s.live_reads,
            consecutiveFailures=s.consecutive_failures,
            egressBlocked=blocked, verdict=not blocked,
        ))
        if r.ok:
            rep.ok += 1
        elif blocked:
            rep.inconclusive += 1
        else:
            rep.failed += 1
        if verbose:
            flag = "OK " if r.ok else ("EGRESS" if blocked else "ERR")
            status = r.status if r.status is not None else "---"
            print(f"{flag:<6} {status:>3} {r.elapsed_ms:>5}ms {r.size:>8}B  "
                  f"{s.id:<22} {'' if r.ok else r.describe_error()}")

    return rep


def summary_line(rep: ProbeReport) -> str:
    parts = [f"{rep.ok} ok", f"{rep.failed} failed"]
    if rep.inconclusive:
        parts.append(f"{rep.inconclusive} inconclusive (egress blocked)")
    line = " / ".join(parts)
    if rep.egress_blocked:
        line += (" — every failure was a TLS/EOF at the runner, so this probe "
                 "proves nothing about those sources")
    return line


def exit_code(rep: ProbeReport) -> int:
    """Red when the probe did not actually do its job.

    A probe that verified nothing, or that could not reach most of the registry
    because the runner had no egress, must not exit 0: the scheduled job has to
    go red so somebody looks.  Genuine per-source failures are *results* and do
    not fail the probe — that is the whole point of running it.
    """
    if rep.attempted == 0:
        return 1                      # nothing was even attempted: misconfiguration
    if rep.ok == 0:
        return 1                      # not one source reachable: probe proved nothing
    if rep.inconclusive > rep.ok:
        return 1                      # most of the registry untested from here
    return 0


def write_report(rep: ProbeReport, path=None):
    """Write the health ledger.  Returns the path written."""
    p = config.DATA / "source_health.json" if path is None else path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rep.payload(), indent=1) + "\n", encoding="utf-8")
    return p


# --------------------------------------------------------------------------- #
# merging cycle reads into the same ledger
# --------------------------------------------------------------------------- #
def record_reads(reads, path=None, mode: str = "cycle",
                 apply: bool = True) -> Optional[pathlib.Path]:
    """Fold reads made during a cycle into the health ledger.  Returns the path.

    The probe is not the only thing that reads a source: a cycle reads most of
    them too, and promotes them on a real read.  If only the probe wrote this
    file, the ledger went stale between the daily probe runs — the Sources page
    ended up showing a probe table saying "4 ok / 24 inconclusive" directly above
    a registry table saying "23 verified", two honest records that visibly
    contradicted each other.  One ledger, two writers, each row naming which
    mechanism produced it.

    ``reads`` is an iterable of (source, FetchResult, at, egress_blocked).
    Existing rows for sources not read this cycle are preserved, so a cycle that
    only reads 20 of 28 sources does not erase the other 8.

    ``apply=False`` records the read without touching the source object.  The
    cycle already folds its own results into the registry inline, so applying
    them again here would double-count ``live_reads`` and
    ``consecutive_failures`` — and the latter drives the CRITICAL escalation.
    """
    import pathlib as _pl

    p = _pl.Path(config.DATA / "source_health.json") if path is None else _pl.Path(path)
    existing: Dict[str, Any] = {}
    meta: Dict[str, Any] = {}
    if p.exists():
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            existing = {r.get("id"): r for r in doc.get("results", [])}
            meta = doc
        except (OSError, ValueError):
            existing, meta = {}, {}

    ok = failed = inconclusive = 0
    for src, r, at, blocked in reads:
        if apply:
            apply_result(src, r, at, egress_blocked=blocked)
        existing[src.id] = {
            "id": src.id, "name": src.name, "operator": src.operator,
            "docsUrl": src.docs_url, "probeUrl": src.probe_url,
            "url": r.url, "httpStatus": r.status, "ok": r.ok, "bytes": r.size,
            "elapsedMs": r.elapsed_ms, "attempts": r.attempts,
            "error": "" if r.ok else r.describe_error(),
            "sha256": r.sha256[:16] if r.body else "", "checkedAt": at,
            "statusAfter": src.status, "liveReads": src.live_reads,
            "consecutiveFailures": src.consecutive_failures,
            "egressBlocked": bool(blocked), "verdict": not blocked,
            "via": mode,
        }
        if r.ok:
            ok += 1
        elif blocked:
            inconclusive += 1
        else:
            failed += 1

    rows = list(existing.values())
    # Sort by id so the file diffs readably cycle over cycle.
    rows.sort(key=lambda r: r.get("id") or "")
    payload = {
        "generatedAt": _now(),
        "mode": meta.get("mode") if meta.get("mode") else mode,
        "lastWriter": mode,
        "lastWriteCounts": {"ok": ok, "failed": failed, "inconclusive": inconclusive},
        "attempted": len(rows),
        "ok": sum(1 for r in rows if r.get("ok")),
        "failed": sum(1 for r in rows if not r.get("ok") and not r.get("egressBlocked")),
        "inconclusive": sum(1 for r in rows if r.get("egressBlocked")),
        "egressBlocked": any(r.get("egressBlocked") for r in rows),
        "note": (
            "One ledger, two writers: rows with via='probe' come from "
            "tools/probe_sources.py, rows with via='cycle' from a cycle read. "
            "egressBlocked=true means NO verdict was reached — the runner could "
            "not open a TLS session, which says nothing about the source, so "
            "statusAfter is unchanged and must not be read as 'this is broken'."
        ),
        "results": rows,
    }
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    return p
