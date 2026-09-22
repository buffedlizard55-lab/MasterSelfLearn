"""Shared source-health recording for the daily probe and research cycle.

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

``verified-live-read``  a complete 2xx body was recorded
``registered``          endpoint + docs recorded; no conclusive success yet
``blocked``             the last conclusive read failed (a stale exact-URL seed may
                        still be shown only as an explicit seed-fallback)
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional

from . import config
from .http import FetchResult, fetch, health_inconclusive_reason
from .sources import REGISTRY, Source, render_probe_url


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
    inconclusiveReason: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)


@dataclass
class ProbeReport:
    generatedAt: str = ""
    mode: str = ""
    ok: int = 0
    failed: int = 0
    #: reads that reached no source-health verdict (runner, caller, or local cap)
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
                "A failed response produces no fresh claim. Rows with verdict=false "
                "reached NO source-health conclusion: runner egress, a caller-generated "
                "request error, or a local response cap says nothing about whether the "
                "service is down, so statusAfter is unchanged. Status comes only from "
                "conclusive reads folded into this ledger by the probe or live cycle."
            ),
            "results": [r.as_dict() for r in self.rows],
        }


def apply_result(src: Source, r: FetchResult, at: str, egress_blocked: bool = False) -> None:
    """Fold one read into the registry entry.  Mutates ``src`` in place.

    ``egress_blocked`` is the legacy parameter name for any no-verdict read:
    runner egress, a caller-generated URL error, or the local response cap. None
    establishes that a healthy endpoint is blocked, so status and failure streak
    are left untouched; the row records the specific reason.
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
        # The probe URL template is rendered against this read's own clock, so a
        # date-windowed probe (GitHub created:>=, USGS starttime, MLB date) always
        # asks about the current window instead of the day the registry was edited.
        url = render_probe_url(s.probe_url, at)
        try:
            r = fetch(url, accept=s.accepts, retries=retries)
        except Exception as e:  # noqa: BLE001 - one bad source must not abort 27
            # msl.http.fetch is documented never to raise, so reaching here means
            # something unexpected (a bad probe_url, a DNS failure inside the
            # resolver, a programming error).  Record it as a failed read and
            # carry on: a probe that stops at the first bad entry reports nothing
            # about the rest, which is exactly how the original TypeError bug hid.
            r = FetchResult(url=url, status=None, body=b"", attempts=1,
                            error_kind=type(e).__name__, error=str(e)[:300])
        # Runner egress, a caller-generated request error, and our own response
        # cap say nothing about source availability. Cycle and probe share this
        # classifier so one writer cannot block what the other calls inconclusive.
        inconclusive_reason = health_inconclusive_reason(r)
        blocked = inconclusive_reason == "runner-egress"
        no_verdict = bool(inconclusive_reason)
        apply_result(s, r, at, egress_blocked=no_verdict)
        rep.rows.append(ProbeRow(
            id=s.id, name=s.name, operator=s.operator, docsUrl=s.docs_url,
            probeUrl=url, httpStatus=r.status, ok=r.ok, bytes=r.size,
            elapsedMs=r.elapsed_ms, attempts=r.attempts,
            error="" if r.ok else r.describe_error(),
            sha256=r.sha256[:16] if r.body else "", checkedAt=at,
            statusAfter=s.status, liveReads=s.live_reads,
            consecutiveFailures=s.consecutive_failures,
            egressBlocked=blocked, verdict=not no_verdict,
            inconclusiveReason=inconclusive_reason,
        ))
        if r.ok:
            rep.ok += 1
        elif no_verdict:
            rep.inconclusive += 1
        else:
            rep.failed += 1
        if verbose:
            flag = "OK " if r.ok else ("NO-VRD" if no_verdict else "ERR")
            status = r.status if r.status is not None else "---"
            print(f"{flag:<6} {status:>3} {r.elapsed_ms:>5}ms {r.size:>8}B  "
                  f"{s.id:<22} {'' if r.ok else r.describe_error()}")

    return rep


def summary_line(rep: ProbeReport) -> str:
    parts = [f"{rep.ok} ok", f"{rep.failed} failed"]
    if rep.inconclusive:
        parts.append(f"{rep.inconclusive} inconclusive (no source verdict)")
    line = " / ".join(parts)
    if rep.egress_blocked:
        line += (" — each TLS/EOF row is a runner-egress observation and proves "
                 "nothing about that source")
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
    """Merge probe rows into the shared health ledger and return its path.

    A targeted ``--only`` probe must not erase the last recorded observation for
    every source it did not inspect. The daily full probe naturally replaces all
    rows; a partial diagnostic replaces only its selected ids.
    """
    import pathlib as _pl

    p = (_pl.Path(config.DATA / "source_health.json") if path is None
         else _pl.Path(path))
    fresh = rep.payload()
    rows: Dict[str, Dict[str, Any]] = {}
    valid_ids = {source.id for source in REGISTRY}
    if p.exists():
        try:
            old = json.loads(p.read_text(encoding="utf-8"))
            rows = {r.get("id"): r for r in old.get("results", [])
                    if r.get("id") in valid_ids}
        except (OSError, ValueError):
            rows = {}
    rows.update({r.get("id"): r for r in fresh["results"] if r.get("id")})
    merged = sorted(rows.values(), key=lambda r: r.get("id") or "")
    fresh.update({
        "lastWriter": "probe",
        "lastWriteCounts": {"ok": rep.ok, "failed": rep.failed,
                            "inconclusive": rep.inconclusive},
        "attempted": len(merged),
        "ok": sum(1 for r in merged if r.get("ok")),
        "failed": sum(1 for r in merged
                      if not r.get("ok") and r.get("verdict", True)),
        "inconclusive": sum(1 for r in merged if not r.get("verdict", True)),
        "egressBlocked": any(r.get("egressBlocked") for r in merged),
        "results": merged,
    })
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(fresh, indent=1, allow_nan=False) + "\n",
                   encoding="utf-8")
    tmp.replace(p)
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

    ``reads`` rows are ``(source, FetchResult, at, egress_blocked)`` with an
    optional fifth ``inconclusive_reason``. Caller mistakes and local safety caps,
    like egress blocks, produce no verdict about source health.
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
            valid_ids = {source.id for source in REGISTRY}
            existing = {r.get("id"): r for r in doc.get("results", [])
                        if r.get("id") in valid_ids}
            meta = doc
        except (OSError, ValueError):
            existing, meta = {}, {}

    ok = failed = inconclusive = 0
    for read in reads:
        if len(read) == 4:
            src, r, at, blocked = read
            inconclusive_reason = "runner-egress" if blocked else ""
        else:
            src, r, at, blocked, inconclusive_reason = read
        no_verdict = bool(inconclusive_reason)
        if apply:
            apply_result(src, r, at, egress_blocked=no_verdict)
        existing[src.id] = {
            "id": src.id, "name": src.name, "operator": src.operator,
            "docsUrl": src.docs_url, "probeUrl": src.probe_url,
            "url": r.url, "httpStatus": r.status, "ok": r.ok, "bytes": r.size,
            "elapsedMs": r.elapsed_ms, "attempts": r.attempts,
            "error": "" if r.ok else r.describe_error(),
            "sha256": r.sha256[:16] if r.body else "", "checkedAt": at,
            "statusAfter": src.status, "liveReads": src.live_reads,
            "consecutiveFailures": src.consecutive_failures,
            "egressBlocked": bool(blocked), "verdict": not no_verdict,
            "inconclusiveReason": inconclusive_reason, "via": mode,
        }
        if r.ok:
            ok += 1
        elif no_verdict:
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
        "failed": sum(1 for r in rows
                      if not r.get("ok") and r.get("verdict", True)),
        "inconclusive": sum(1 for r in rows if not r.get("verdict", True)),
        "egressBlocked": any(r.get("egressBlocked") for r in rows),
        "note": (
            "One ledger, two writers: rows with via='probe' come from "
            "tools/probe_sources.py, rows with via='cycle' from a cycle read. "
            "verdict=false means no source-health verdict was reached (runner "
            "egress, a caller-generated request error, or a local safety cap), so "
            "statusAfter is unchanged and must not be read as 'this is broken'."
        ),
        "results": rows,
    }
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=1, allow_nan=False) + "\n",
                   encoding="utf-8")
    tmp.replace(p)
    return p
