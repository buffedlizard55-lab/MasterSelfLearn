"""The evidence ledger and the anti-hallucination gate.

Two append-only JSONL files are the whole memory of the project:

``data/evidence.jsonl``  one row per outbound read that succeeded or failed
``data/claims.jsonl``    one row per statement the library is allowed to make

``Ledger.accept`` is the only way a claim enters the library.  It rejects, and
counts the rejection, when a ``captured``/``documented``/``negative`` claim has no
evidence, or when a ``derived`` claim has no ``computedFrom`` lineage.  A rejected
claim becomes an irregularity rather than a quiet omission.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import dataclasses
from dataclasses import dataclass, asdict

from typing import Any, Dict, Iterable, List, Optional

from . import config

# claim kinds.  These four, and only these, are legal.
KIND_DOCUMENTED = "documented"   # read from the operator's own published record
KIND_CAPTURED = "captured"       # a number lifted from a live payload
KIND_NEGATIVE = "negative"       # proof something does NOT exist (404, 0 results)
KIND_DERIVED = "derived"         # arithmetic over claims that already passed the gate

KINDS_REQUIRING_EVIDENCE = {KIND_DOCUMENTED, KIND_CAPTURED, KIND_NEGATIVE}


def _next_id(prefix: str, n: int) -> str:
    return f"{prefix}{n:06d}"


@dataclass
class Evidence:
    """One read.  ``payloadSha256`` is over the bytes this process received."""

    id: str
    source_id: str
    url: str
    captured_at: str
    status: Optional[int] = None
    payload_sha256: str = ""
    raw_bytes: int = 0
    elapsed_ms: int = 0
    attempts: int = 1
    error: Optional[str] = None
    error_kind: Optional[str] = None
    rate_limited: bool = False
    capture_mode: str = "pipeline"
    #: False when the body was recorded by an interactive agent read rather than by
    #: this process, so the hash covers the recorded body and not the wire bytes.
    wire_hash_verifiable: bool = True
    projection_sha256: str = ""
    note: str = ""

    def as_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return {
            "id": d["id"], "sourceId": d["source_id"], "url": d["url"],
            "capturedAt": d["captured_at"], "status": d["status"],
            "payloadSha256": d["payload_sha256"], "rawBytes": d["raw_bytes"],
            "elapsedMs": d["elapsed_ms"], "attempts": d["attempts"],
            "error": d["error"], "errorKind": d["error_kind"],
            "rateLimited": d["rate_limited"], "captureMode": d["capture_mode"],
            "wireHashVerifiable": d["wire_hash_verifiable"],
            "projectionSha256": d["projection_sha256"], "note": d["note"],
        }


@dataclass
class Claim:
    """A single statement the site is allowed to publish."""

    id: str
    cycle: int
    topic: str
    kind: str
    statement: str
    source_id: str
    retrieved_at: str
    value: Any = None
    unit: str = ""
    field: str = ""            # JSON/Atom path inside the payload
    evidence: List[str] = dataclasses.field(default_factory=list)
    computed_from: List[str] = dataclasses.field(default_factory=list)
    formula: str = ""
    url: str = ""
    #: derived claims are recomputed every cycle; this is the check result
    recheck: str = ""
    tags: List[str] = dataclasses.field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id, "cycle": self.cycle, "topic": self.topic,
            "kind": self.kind, "statement": self.statement,
            "sourceId": self.source_id, "retrievedAt": self.retrieved_at,
            "value": self.value, "unit": self.unit, "field": self.field,
            "evidence": self.evidence, "computedFrom": self.computed_from,
            "formula": self.formula, "url": self.url, "recheck": self.recheck,
            "tags": self.tags,
        }

    @property
    def fingerprint(self) -> str:
        """Identity of the statement, ignoring the value.  Used to detect drift."""
        key = f"{self.topic}|{self.kind}|{self.field}|{self.formula}|{self.source_id}"
        return hashlib.sha256(key.encode()).hexdigest()[:16]


class RejectedClaim(Exception):
    """Raised when a claim fails the gate.  The caller logs it as an irregularity."""


class Ledger:
    """Append-only claim + evidence store with the single acceptance gate."""

    def __init__(self, data_dir: Optional[pathlib.Path] = None):
        self.dir = pathlib.Path(data_dir or config.DATA)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.evidence_path = self.dir / "evidence.jsonl"
        self.claims_path = self.dir / "claims.jsonl"
        self.evidence: List[Evidence] = []
        self.claims: List[Claim] = []
        self.rejections: List[Dict[str, Any]] = []
        self._e_seq = itertools.count(1)
        self._c_seq = itertools.count(1)
        self._by_fingerprint: Dict[str, Claim] = {}
        self.load()

    # ------------------------------------------------------------------ io
    def load(self) -> None:
        for line in _read_lines(self.evidence_path):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            e = Evidence(
                id=d["id"], source_id=d.get("sourceId", ""), url=d.get("url", ""),
                captured_at=d.get("capturedAt", ""), status=d.get("status"),
                payload_sha256=d.get("payloadSha256", ""), raw_bytes=d.get("rawBytes", 0),
                elapsed_ms=d.get("elapsedMs", 0), attempts=d.get("attempts", 1),
                error=d.get("error"), error_kind=d.get("errorKind"),
                rate_limited=bool(d.get("rateLimited")),
                capture_mode=d.get("captureMode", "pipeline"),
                wire_hash_verifiable=bool(d.get("wireHashVerifiable", True)),
                projection_sha256=d.get("projectionSha256", ""), note=d.get("note", ""),
            )
            self.evidence.append(e)
            self._e_seq = itertools.count(_num_suffix(e.id) + 1)
        for line in _read_lines(self.claims_path):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            c = Claim(
                id=d["id"], cycle=d.get("cycle", 0), topic=d.get("topic", ""),
                kind=d.get("kind", ""), statement=d.get("statement", ""),
                source_id=d.get("sourceId", ""), retrieved_at=d.get("retrievedAt", ""),
                value=d.get("value"), unit=d.get("unit", ""), field=d.get("field", ""),
                evidence=d.get("evidence", []) or [], computed_from=d.get("computedFrom", []) or [],
                formula=d.get("formula", ""), url=d.get("url", ""),
                recheck=d.get("recheck", ""), tags=d.get("tags", []) or [],
            )
            self.claims.append(c)
            self._by_fingerprint[c.fingerprint] = c
            self._c_seq = itertools.count(_num_suffix(c.id) + 1)

    # -------------------------------------------------------------- evidence
    def add_evidence(self, source_id: str, url: str, captured_at: str, status: Optional[int],
                     body: bytes = b"", error: Optional[str] = None,
                     error_kind: Optional[str] = None, elapsed_ms: int = 0, attempts: int = 1,
                     rate_limited: bool = False, capture_mode: str = "pipeline",
                     wire_hash_verifiable: bool = True, projection: Any = None,
                     note: str = "") -> Evidence:
        e = Evidence(
            id=_next_id("E", next(self._e_seq)), source_id=source_id, url=url,
            captured_at=captured_at, status=status,
            payload_sha256=hashlib.sha256(body).hexdigest() if body else "",
            raw_bytes=len(body), elapsed_ms=elapsed_ms, attempts=attempts,
            error=error, error_kind=error_kind, rate_limited=rate_limited,
            capture_mode=capture_mode, wire_hash_verifiable=wire_hash_verifiable,
            projection_sha256=(hashlib.sha256(
                json.dumps(projection, sort_keys=True).encode()).hexdigest()
                if projection is not None else ""),
            note=note,
        )
        self.evidence.append(e)
        _append(self.evidence_path, e.as_dict())
        return e

    # ----------------------------------------------------------------- gate
    def accept(self, topic: str, kind: str, statement: str, source_id: str,
               retrieved_at: str, cycle: int, **kw: Any) -> Claim:
        """Validate and persist one claim.  Raises ``RejectedClaim`` on failure."""
        if kind not in (KIND_DOCUMENTED, KIND_CAPTURED, KIND_NEGATIVE, KIND_DERIVED):
            raise RejectedClaim(f"unknown claim kind {kind!r}")
        if not statement or not statement.strip():
            raise RejectedClaim("empty statement")
        evidence_ids = list(kw.pop("evidence", []) or [])
        computed_from = list(kw.pop("computed_from", []) or [])
        if kind in KINDS_REQUIRING_EVIDENCE and not evidence_ids:
            raise RejectedClaim(
                f"{kind} claim has no evidence row: {statement[:90]}")
        if kind == KIND_DERIVED and (not computed_from or not kw.get("formula")):
            raise RejectedClaim(
                f"derived claim has no lineage/formula: {statement[:90]}")
        known = {e.id for e in self.evidence}
        bad = [i for i in evidence_ids if i not in known]
        if bad:
            raise RejectedClaim(f"unknown evidence id(s) {bad[:3]}")
        known_c = {c.id for c in self.claims}
        bad_c = [i for i in computed_from if i not in known_c]
        if bad_c:
            raise RejectedClaim(f"unknown computedFrom id(s) {bad_c[:3]}")

        c = Claim(id=_next_id("C", next(self._c_seq)), cycle=cycle, topic=topic,
                  kind=kind, statement=statement, source_id=source_id,
                  retrieved_at=retrieved_at, evidence=evidence_ids,
                  computed_from=computed_from, **kw)
        self.claims.append(c)
        self._by_fingerprint[c.fingerprint] = c
        _append(self.claims_path, c.as_dict())
        return c

    def reject(self, reason: str, statement: str, kind: str, source_id: str) -> None:
        self.rejections.append({"reason": reason, "statement": statement[:200],
                                "kind": kind, "sourceId": source_id})

    def try_accept(self, *a: Any, **kw: Any) -> Optional[Claim]:
        """``accept`` that records the rejection instead of raising."""
        try:
            return self.accept(*a, **kw)
        except RejectedClaim as e:
            self.reject(str(e), kw.get("statement", "") or (a[2] if len(a) > 2 else ""),
                        kw.get("kind", "") or (a[1] if len(a) > 1 else ""),
                        kw.get("source_id", "") or (a[3] if len(a) > 3 else ""))
            return None

    # --------------------------------------------------------------- queries
    def by_topic(self, topic: str) -> List[Claim]:
        return [c for c in self.claims if c.topic == topic]

    def latest(self, topic: str, field: str) -> Optional[Claim]:
        hits = [c for c in self.claims if c.topic == topic and c.field == field]
        return hits[-1] if hits else None

    def series(self, topic: str, field: str) -> List[Claim]:
        return [c for c in self.claims if c.topic == topic and c.field == field]

    def previous(self, fingerprint: str) -> Optional[Claim]:
        return self._by_fingerprint.get(fingerprint)

    def counts(self) -> Dict[str, int]:
        out: Dict[str, int] = {KIND_DOCUMENTED: 0, KIND_CAPTURED: 0,
                               KIND_NEGATIVE: 0, KIND_DERIVED: 0}
        for c in self.claims:
            out[c.kind] = out.get(c.kind, 0) + 1
        return out

    def topics_with_claims(self) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for c in self.claims:
            out[c.topic] = out.get(c.topic, 0) + 1
        return out


def _num_suffix(cid: str) -> int:
    try:
        return int(cid.lstrip("CE"))
    except ValueError:
        return 0


def _read_lines(p: pathlib.Path) -> Iterable[str]:
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8") as fh:
        return [ln for ln in (l.rstrip("\n") for l in fh) if ln.strip()]


def _append(p: pathlib.Path, obj: Dict[str, Any]) -> None:
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, sort_keys=True, ensure_ascii=False) + "\n")
