"""Append-only evidence, claim, and rejection ledgers.

``data/evidence.jsonl`` records one successful read, including the SHA-256 of the
exact response bytes when this process received them. ``data/claims.jsonl`` holds
only claims accepted by :meth:`Ledger.accept`. ``data/rejections.jsonl`` keeps every
failed gate attempt; a rejection is evidence that the gate is exercised and must
not disappear when the process exits.

The gate is intentionally stricter than "an evidence id exists": a captured,
documented, or negative claim must cite a successful, hashed read by the same
source and URL, and must name both its stable metric field and the path used inside
the payload. Derived claims must cite existing claims and a recorded formula.
"""
from __future__ import annotations

import dataclasses
import hashlib
import itertools
import json
import math
import pathlib
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Optional

from . import config

KIND_DOCUMENTED = "documented"
KIND_CAPTURED = "captured"
KIND_NEGATIVE = "negative"
KIND_DERIVED = "derived"

KINDS_REQUIRING_EVIDENCE = {KIND_DOCUMENTED, KIND_CAPTURED, KIND_NEGATIVE}
LEGAL_KINDS = KINDS_REQUIRING_EVIDENCE | {KIND_DERIVED}


def _next_id(prefix: str, n: int) -> str:
    return f"{prefix}{n:06d}"


@dataclass
class Evidence:
    """One successful read and its integrity metadata.

    ``payload_sha256`` is over the exact decompressed bytes handed to the adapter.
    ``projection_sha256`` is over canonical JSON and is useful for seed captures,
    but it is not a wire hash. Historical rows written before cycle 19 can have only
    a projection hash; the verifier reports that limitation rather than upgrading it.
    """

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
    wire_hash_verifiable: bool = True
    projection_sha256: str = ""
    note: str = ""
    final_url: str = ""
    content_type: str = ""
    truncated: bool = False
    schema_version: int = 2

    @property
    def successful(self) -> bool:
        return (self.status is not None and 200 <= self.status < 300
                and not self.error and not self.truncated)

    @property
    def has_integrity_hash(self) -> bool:
        return bool(self.payload_sha256 or self.projection_sha256)

    @property
    def integrity_level(self) -> str:
        if self.wire_hash_verifiable and self.payload_sha256 and self.raw_bytes > 0:
            return "wire"
        if self.projection_sha256:
            return "projection"
        return "missing"

    def as_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return {
            "id": d["id"], "sourceId": d["source_id"], "url": d["url"],
            "finalUrl": d["final_url"], "capturedAt": d["captured_at"],
            "status": d["status"], "contentType": d["content_type"],
            "payloadSha256": d["payload_sha256"], "rawBytes": d["raw_bytes"],
            "elapsedMs": d["elapsed_ms"], "attempts": d["attempts"],
            "error": d["error"], "errorKind": d["error_kind"],
            "rateLimited": d["rate_limited"], "captureMode": d["capture_mode"],
            "wireHashVerifiable": d["wire_hash_verifiable"],
            "projectionSha256": d["projection_sha256"], "truncated": d["truncated"],
            "integrityLevel": self.integrity_level, "note": d["note"],
            "schemaVersion": self.schema_version,
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
    # Stable identity of the measured series (not a JSON path).
    field: str = ""
    # Exact JSON/XML path or projection expression used by the adapter.
    source_path: str = ""
    evidence: List[str] = dataclasses.field(default_factory=list)
    computed_from: List[str] = dataclasses.field(default_factory=list)
    formula: str = ""
    url: str = ""
    recheck: str = ""
    tags: List[str] = dataclasses.field(default_factory=list)
    # Entity-topic slugs this family-level claim directly supports.
    subjects: List[str] = dataclasses.field(default_factory=list)
    schema_version: int = 2

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id, "cycle": self.cycle, "topic": self.topic,
            "kind": self.kind, "statement": self.statement,
            "sourceId": self.source_id, "retrievedAt": self.retrieved_at,
            "value": self.value, "unit": self.unit, "field": self.field,
            "sourcePath": self.source_path, "subjects": self.subjects,
            "evidence": self.evidence, "computedFrom": self.computed_from,
            "formula": self.formula, "url": self.url, "recheck": self.recheck,
            "tags": self.tags, "schemaVersion": self.schema_version,
        }

    @property
    def fingerprint(self) -> str:
        key = f"{self.topic}|{self.kind}|{self.field}|{self.formula}|{self.source_id}"
        return hashlib.sha256(key.encode()).hexdigest()[:16]


class RejectedClaim(Exception):
    """Raised when a claim fails the gate."""


class Ledger:
    """Append-only evidence, claim, and rejection store with one acceptance gate."""

    def __init__(self, data_dir: Optional[pathlib.Path] = None):
        self.dir = pathlib.Path(data_dir or config.DATA)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.evidence_path = self.dir / "evidence.jsonl"
        self.claims_path = self.dir / "claims.jsonl"
        self.rejections_path = self.dir / "rejections.jsonl"
        self.evidence: List[Evidence] = []
        self.claims: List[Claim] = []
        self.rejections: List[Dict[str, Any]] = []
        self._e_seq = itertools.count(1)
        self._c_seq = itertools.count(1)
        self._r_seq = itertools.count(1)
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
                final_url=d.get("finalUrl", ""), captured_at=d.get("capturedAt", ""),
                status=d.get("status"), content_type=d.get("contentType", ""),
                payload_sha256=d.get("payloadSha256", ""), raw_bytes=d.get("rawBytes", 0),
                elapsed_ms=d.get("elapsedMs", 0), attempts=d.get("attempts", 1),
                error=d.get("error"), error_kind=d.get("errorKind"),
                rate_limited=bool(d.get("rateLimited")),
                capture_mode=d.get("captureMode", "pipeline"),
                wire_hash_verifiable=bool(d.get("wireHashVerifiable", True)),
                projection_sha256=d.get("projectionSha256", ""),
                truncated=bool(d.get("truncated", False)), note=d.get("note", ""),
                schema_version=int(d.get("schemaVersion", 1) or 1),
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
                source_path=d.get("sourcePath", ""),
                subjects=d.get("subjects", []) or [],
                evidence=d.get("evidence", []) or [],
                computed_from=d.get("computedFrom", []) or [],
                formula=d.get("formula", ""), url=d.get("url", ""),
                recheck=d.get("recheck", ""), tags=d.get("tags", []) or [],
                schema_version=int(d.get("schemaVersion", 1) or 1),
            )
            self.claims.append(c)
            self._by_fingerprint[c.fingerprint] = c
            self._c_seq = itertools.count(_num_suffix(c.id) + 1)
        for line in _read_lines(self.rejections_path):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            self.rejections.append(r)
            self._r_seq = itertools.count(_num_suffix(r.get("id", "")) + 1)

    # -------------------------------------------------------------- evidence
    def add_evidence(self, source_id: str, url: str, captured_at: str,
                     status: Optional[int], body: bytes = b"",
                     error: Optional[str] = None, error_kind: Optional[str] = None,
                     elapsed_ms: int = 0, attempts: int = 1,
                     rate_limited: bool = False, capture_mode: str = "pipeline",
                     wire_hash_verifiable: bool = True, projection: Any = None,
                     note: str = "", final_url: str = "", content_type: str = "",
                     truncated: bool = False) -> Evidence:
        canonical = (json.dumps(projection, sort_keys=True, ensure_ascii=False,
                                separators=(",", ":"), allow_nan=False).encode("utf-8")
                     if projection is not None else b"")
        e = Evidence(
            id=_next_id("E", next(self._e_seq)), source_id=source_id, url=url,
            final_url=final_url or url, captured_at=captured_at, status=status,
            content_type=content_type,
            payload_sha256=hashlib.sha256(body).hexdigest() if body else "",
            raw_bytes=len(body), elapsed_ms=elapsed_ms, attempts=attempts,
            error=error, error_kind=error_kind, rate_limited=rate_limited,
            capture_mode=capture_mode, wire_hash_verifiable=wire_hash_verifiable,
            projection_sha256=hashlib.sha256(canonical).hexdigest() if canonical else "",
            truncated=truncated, note=note,
        )
        self.evidence.append(e)
        _append(self.evidence_path, e.as_dict())
        return e

    # ----------------------------------------------------------------- gate
    def accept(self, topic: str, kind: str, statement: str, source_id: str,
               retrieved_at: str, cycle: int, **kw: Any) -> Claim:
        """Validate and persist one claim. Raises :class:`RejectedClaim` on failure."""
        if kind not in LEGAL_KINDS:
            raise RejectedClaim(f"unknown claim kind {kind!r}")
        if not statement or not statement.strip():
            raise RejectedClaim("empty statement")
        if not topic or not source_id or not retrieved_at:
            raise RejectedClaim("topic, source_id and retrieved_at are required")

        evidence_ids = list(dict.fromkeys(kw.pop("evidence", []) or []))
        computed_from = list(dict.fromkeys(kw.pop("computed_from", []) or []))
        field_name = str(kw.get("field", "") or "").strip()
        source_path = str(kw.get("source_path", "") or "").strip()
        claim_url = str(kw.get("url", "") or "").strip()

        if kind in KINDS_REQUIRING_EVIDENCE and not evidence_ids:
            raise RejectedClaim(f"{kind} claim has no evidence row: {statement[:90]}")
        if kind == KIND_DERIVED:
            if not computed_from or not kw.get("formula"):
                raise RejectedClaim(
                    f"derived claim has no lineage/formula: {statement[:90]}")
            if source_id != "derived":
                raise RejectedClaim("derived claim must use source_id='derived'")

        by_evidence = {e.id: e for e in self.evidence}
        bad = [i for i in evidence_ids if i not in by_evidence]
        if bad:
            raise RejectedClaim(f"unknown evidence id(s) {bad[:3]}")
        # Unit tests use an explicit test-fixture capture mode so they can focus on
        # one gate property at a time. Production, seed, and offline-fixture rows
        # receive no such exemption: they must carry complete line-level trace data.
        test_fixture = bool(evidence_ids) and all(
            by_evidence[i].capture_mode == "test-fixture" for i in evidence_ids)
        if kind in KINDS_REQUIRING_EVIDENCE and not test_fixture:
            if not field_name:
                raise RejectedClaim(f"{kind} claim has no stable field identifier")
            if not source_path:
                raise RejectedClaim(f"{kind} claim has no source path")
            if not claim_url:
                raise RejectedClaim(f"{kind} claim has no source URL")
        for eid in evidence_ids:
            e = by_evidence[eid]
            if not test_fixture and e.source_id != source_id:
                raise RejectedClaim(
                    f"evidence {eid} belongs to {e.source_id!r}, not {source_id!r}")
            if not e.url or not e.captured_at:
                raise RejectedClaim(f"evidence {eid} is missing URL or capture time")
            if not e.successful:
                raise RejectedClaim(f"evidence {eid} is not a successful complete read")
            if not e.has_integrity_hash:
                raise RejectedClaim(f"evidence {eid} has no integrity hash")
            if (not test_fixture and claim_url
                    and claim_url != e.url and claim_url != e.final_url):
                raise RejectedClaim(f"claim URL does not match evidence {eid}")

        by_claim = {c.id: c for c in self.claims}
        bad_c = [i for i in computed_from if i not in by_claim]
        if bad_c:
            raise RejectedClaim(f"unknown computedFrom id(s) {bad_c[:3]}")
        if kind == KIND_DERIVED and not field_name:
            raise RejectedClaim("derived claim has no stable field identifier")

        value = kw.get("value")
        if isinstance(value, float) and not math.isfinite(value):
            raise RejectedClaim("claim value is not finite")
        # Refuse values Python can emit but strict JSON readers cannot parse.
        try:
            json.dumps(value, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise RejectedClaim(f"claim value is not strict JSON: {exc}") from exc

        c = Claim(
            id=_next_id("C", next(self._c_seq)), cycle=cycle, topic=topic,
            kind=kind, statement=statement, source_id=source_id,
            retrieved_at=retrieved_at, evidence=evidence_ids,
            computed_from=computed_from, **kw)
        self.claims.append(c)
        self._by_fingerprint[c.fingerprint] = c
        _append(self.claims_path, c.as_dict())
        return c

    def reject(self, reason: str, statement: str, kind: str, source_id: str,
               topic: str = "", cycle: int = 0, rejected_at: str = "") -> None:
        row = {
            "id": _next_id("R", next(self._r_seq)), "reason": reason,
            "statement": (statement or "")[:200], "kind": kind,
            "sourceId": source_id, "topic": topic, "cycle": cycle,
            "rejectedAt": rejected_at,
        }
        self.rejections.append(row)
        _append(self.rejections_path, row)

    def try_accept(self, *a: Any, **kw: Any) -> Optional[Claim]:
        """``accept`` that persists the rejection instead of raising."""
        try:
            return self.accept(*a, **kw)
        except RejectedClaim as exc:
            self.reject(
                str(exc),
                kw.get("statement", "") or (a[2] if len(a) > 2 else ""),
                kw.get("kind", "") or (a[1] if len(a) > 1 else ""),
                kw.get("source_id", "") or (a[3] if len(a) > 3 else ""),
                topic=kw.get("topic", "") or (a[0] if a else ""),
                rejected_at=(a[4] if len(a) > 4 else kw.get("retrieved_at", "")),
                cycle=int(a[5] if len(a) > 5 else kw.get("cycle", 0) or 0),
            )
            return None

    # --------------------------------------------------------------- queries
    def by_topic(self, topic: str) -> List[Claim]:
        return [c for c in self.claims if c.topic == topic or topic in c.subjects]

    def latest(self, topic: str, field: str) -> Optional[Claim]:
        hits = [c for c in self.by_topic(topic) if c.field == field]
        return hits[-1] if hits else None

    def series(self, topic: str, field: str) -> List[Claim]:
        return [c for c in self.by_topic(topic) if c.field == field]

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
            for slug in dict.fromkeys([c.topic] + list(c.subjects)):
                if slug:
                    out[slug] = out.get(slug, 0) + 1
        return out

    def evidence_integrity_counts(self) -> Dict[str, int]:
        out = {"wire": 0, "projection": 0, "missing": 0,
               "successful": 0, "invalid": 0}
        for e in self.evidence:
            out[e.integrity_level] += 1
            out["successful" if e.successful else "invalid"] += 1
        return out


def _num_suffix(cid: str) -> int:
    try:
        return int("".join(ch for ch in str(cid) if ch.isdigit()) or "0")
    except ValueError:
        return 0


def _read_lines(p: pathlib.Path) -> Iterable[str]:
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8") as fh:
        return [ln for ln in (line.rstrip("\n") for line in fh) if ln.strip()]


def _append(p: pathlib.Path, obj: Dict[str, Any]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                            allow_nan=False) + "\n")
