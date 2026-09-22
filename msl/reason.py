"""Reasoning: arithmetic over verified claims, and re-checking yesterday's arithmetic.

Two halves, both deterministic:

**Derive.**  Each rule takes claims that already passed the evidence gate and
emits a new ``derived`` claim carrying the ids it came from and the formula used.
A derived claim is never a new observation — it is a computation the reader can
redo.

**Recheck.**  On every cycle the rules are re-run over the same inputs and the
result is compared with what was published before.  A mismatch is a drift
irregularity: either the arithmetic is wrong or an input moved.  Either way the
site says so rather than quietly showing the new number.

There is no language model in this loop and no free-text generation.  Every
sentence on the site is a template whose slots are filled from claim values.
"""
from __future__ import annotations

import re
import dataclasses
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from .retractions import is_retracted

from . import config
from .evidence import KIND_DERIVED, Claim, Ledger

# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
_INDEXED = re.compile(r"^(?P<base>[A-Za-z_.]+\[)(?P<i>[^\]]+)(?P<rest>\]\..+)$")


def parse_iso(s: str) -> Optional[datetime]:
    if not s or not _ISO.match(s):
        return None
    try:
        return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def days_between(a: str, b: str) -> Optional[float]:
    da, db = parse_iso(a), parse_iso(b)
    if da is None or db is None:
        return None
    return (db - da).total_seconds() / 86400.0


def split_indexed(field_name: str) -> Optional[Tuple[str, str, str]]:
    """Split ``base[key].rest`` into its parts.

    ``key`` is whatever identifies the observation — a repository name, a document
    number, a date — not necessarily an integer.  Returning the raw string is what
    keeps two different subjects from being merged into one series.
    """
    m = _INDEXED.match(field_name)
    if not m:
        return None
    return m.group("base"), m.group("i"), m.group("rest")


@dataclass
class Insight:
    """A published sentence.  Every slot is a verified number."""

    id: str
    cycle: int
    topic: str
    kind: str                 # trend | velocity | corroboration | growth | anomaly
    text: str
    claim_ids: List[str] = field(default_factory=list)
    importance: float = 0.0

    def as_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "cycle": self.cycle, "topic": self.topic,
                "kind": self.kind, "text": self.text, "claimIds": self.claim_ids,
                "importance": round(self.importance, 4)}


@dataclass
class ReasonResult:
    insights: List[Insight] = field(default_factory=list)
    derived: int = 0
    rechecks: int = 0
    not_recheckable: int = 0
    drift: List[Dict[str, Any]] = field(default_factory=list)


# --------------------------------------------------------------------------- #
# rule implementations
# --------------------------------------------------------------------------- #
def _repo_groups(claims: List[Claim]) -> Dict[str, Dict[str, Claim]]:
    """Group ``github.repo[i].*`` claims by the repository full name in their tags."""
    out: Dict[str, Dict[str, Claim]] = {}
    for c in claims:
        if not c.field.startswith("github.repo["):
            continue
        parts = split_indexed(c.field)
        if not parts:
            continue
        _base, _i, rest = parts
        name = next((t for t in c.tags if "/" in t), None)
        if not name:
            continue
        out.setdefault(name, {})[rest.lstrip("].")] = c
        # keep the newest cycle's value
        store = out[name]
        key = rest.lstrip("].")
        prev = store.get(key)
        if prev is None or (c.cycle, ) >= (prev.cycle,):
            store[key] = c
    return out


def derive(ledger: Ledger, cycle: int, now: str,
           seq: List[int]) -> ReasonResult:
    res = ReasonResult()
    ins_n = [0]

    def insight(topic: str, kind: str, text: str, ids: List[str], importance: float) -> None:
        ins_n[0] += 1
        res.insights.append(Insight(id=f"I{cycle:04d}-{ins_n[0]:03d}", cycle=cycle,
                                    topic=topic, kind=kind, text=text,
                                    claim_ids=ids, importance=importance))

    def emit(topic: str, statement: str, field_name: str, value: Any, unit: str,
             formula: str, computed_from: List[str], tags: List[str],
             importance: float = 0.0, kind: str = "trend") -> Optional[Claim]:
        seq[0] += 1
        c = ledger.try_accept(
            topic, KIND_DERIVED, statement, "derived", now, cycle,
            value=value, unit=unit, field=field_name, formula=formula,
            computed_from=computed_from, tags=tags)
        if c is not None:
            res.derived += 1
            insight(topic, kind, statement, [c.id], importance)
        return c

    # Retracted claims stay in the append-only ledger but are not inputs.  Without
    # this the reasoning stage recomputes the same wrong conclusion every cycle
    # from claims that are genuine reads of the wrong subject.
    claims = [c for c in ledger.claims if not is_retracted(c.field)]

    # ---- R1/R5/R6  repository age and star velocity -----------------------
    for name, g in sorted(_repo_groups(claims).items()):
        stars = g.get("stars")
        created = g.get("created")
        if stars is None or created is None:
            continue
        s = stars.value
        if not isinstance(s, (int, float)):
            continue
        age = days_between(str(created.value), now)
        if age is None or age <= 0:
            continue
        age = max(age, 1.0)
        emit(stars.topic,
             f"{name} is {age:.1f} days old and has {int(s):,} stars, "
             f"a rate of {s / age:,.1f} stars per day.",
             f"velocity[{name}]", round(s / age, 4), "stars/day",
             "stars / max(age_days, 1)", [stars.id, created.id],
             ["github", "velocity", name], importance=min(s / age / 500.0, 1.0),
             kind="velocity")

    # ---- R3  corroboration across independent sources ---------------------
    # A derived claim's source_id is "derived": it is our own arithmetic, not a
    # second witness.  Counting it as one made every single-source entity look
    # corroborated (observed: 104 of 104).
    by_entity: Dict[str, Dict[str, List[Claim]]] = {}
    for c in claims:
        if c.source_id == "derived":
            continue
        for t in c.tags:
            if "/" in t or t.startswith(("wiki:", "repo:")):
                by_entity.setdefault(t, {}).setdefault(c.source_id, []).append(c)
    for ent, per_src in sorted(by_entity.items()):
        if len(per_src) < 2:
            continue
        ids = [lst[-1].id for lst in per_src.values()]
        topic = next(iter(per_src.values()))[0].topic
        emit(topic,
             f"“{ent}” is independently reported by {len(per_src)} sources "
             f"({', '.join(sorted(per_src))}).",
             f"corroboration[{ent}]", len(per_src), "sources",
             "count(distinct sourceId mentioning entity)", ids,
             ["corroboration", ent], importance=min(len(per_src) / 4.0, 1.0),
             kind="corroboration")

    # ---- R1  daily-series trend (Wikipedia pageviews, any *.views.YYYY-MM-DD)
    series: Dict[Tuple[str, str], List[Claim]] = {}
    for c in claims:
        m = re.match(r"^wiki\[(?P<art>[^\]]+)\]\.views\.(?P<day>\d{4}-\d{2}-\d{2})$", c.field)
        if m and isinstance(c.value, (int, float)):
            series.setdefault((c.topic, m.group("art")), []).append((m.group("day"), c))
    for (topic, art), pairs in sorted(series.items()):
        pairs.sort(key=lambda x: x[0])
        # de-duplicate by day, keeping the latest cycle's reading
        by_day: Dict[str, Claim] = {}
        for day, c in pairs:
            by_day[day] = c
        days = sorted(by_day)
        if len(days) < 2:
            continue
        first, last = by_day[days[0]], by_day[days[-1]]
        a, b = float(first.value), float(last.value)
        if a == 0:
            continue
        pct = (b - a) / a * 100.0
        emit(topic,
             f"Wikipedia article “{art}” moved from {int(a):,} views on {days[0]} to "
             f"{int(b):,} on {days[-1]}, a change of {pct:+.1f}% over {len(days) - 1} days.",
             f"trend[wiki:{art}]", round(pct, 4), "percent",
             "(last - first) / first * 100", [first.id, last.id],
             ["wikipedia", "trend", art], importance=min(abs(pct) / 50.0, 1.0),
             kind="trend")

    # ---- R8/R9  counters moving between cycles ----------------------------
    for fld, label, unit in [
        ("owner.public_repos", "the owner's public repository count", "repositories"),
        ("owner.pages_repos", "the owner's Pages-enabled repository count", "repositories"),
        ("hn.topstories.length", "the Hacker News topstories list length", "stories"),
    ]:
        hist = [c for c in claims if c.field == fld and isinstance(c.value, (int, float))]
        if len(hist) < 2:
            continue
        a, b = hist[0], hist[-1]
        d = float(b.value) - float(a.value)
        if d == 0:
            continue
        emit(b.topic,
             f"Between cycles {a.cycle} and {b.cycle}, {label} moved "
             f"{int(a.value):,} → {int(b.value):,} ({d:+,.0f} {unit}).",
             f"delta[{fld}]", round(d, 4), unit,
             "last.value - first.value", [a.id, b.id],
             ["delta", fld], importance=min(abs(d) / 10.0, 1.0), kind="growth")

    for c in claims:
        if not c.field.startswith("fedreg.documents[") or not isinstance(c.value, (int, float)):
            continue
        hist = [h for h in claims if h.field == c.field and isinstance(h.value, (int, float))]
        if len(hist) < 2:
            continue
        a, b = hist[0], hist[-1]
        d = float(b.value) - float(a.value)
        term = c.field[len("fedreg.documents["):-1]
        if term in ("newest", "*", ""):
            continue
        emit(b.topic,
             f"Federal Register documents matching “{term}” moved "
             f"{int(a.value):,} → {int(b.value):,} ({d:+,.0f}) between cycles {a.cycle} and {b.cycle}.",
             f"delta[fedreg:{term}]", round(d, 4), "documents",
             "last.value - first.value", [a.id, b.id],
             ["federal-register", "delta", term], importance=min(abs(d) / 20.0, 1.0),
             kind="growth")

    # ---- R10  cross-family presence ---------------------------------------
    fams: Dict[str, Dict[str, int]] = {}
    for c in claims:
        if c.source_id == "derived":
            continue
        for t in c.tags:
            if "/" in t:
                fams.setdefault(t, {}).setdefault(c.topic, 0)
                fams[t][c.topic] += 1
    for ent, per_fam in sorted(fams.items()):
        if len(per_fam) < 2:
            continue
        ids = [next(c.id for c in reversed(claims) if ent in c.tags and c.topic == f)
               for f in sorted(per_fam)]
        emit(sorted(per_fam)[0],
             f"“{ent}” appears in {len(per_fam)} topic families "
             f"({', '.join(sorted(per_fam))}), so it is not confined to one line of research.",
             f"crossfamily[{ent}]", len(per_fam), "families",
             "count(distinct topic containing entity)", ids,
             ["cross-family", ent], importance=min(len(per_fam) / 3.0, 1.0),
             kind="corroboration")

    return res


# --------------------------------------------------------------------------- #
# recheck
# --------------------------------------------------------------------------- #
def recheck_derived(ledger: Ledger, cycle: int, now: str) -> ReasonResult:
    """Recompute previously published derived claims and flag any that moved.

    Append-only: the recheck writes a fresh claim marked ``recheck`` rather than
    editing history, so the site can show both the old and the new number.
    """
    res = ReasonResult()
    by_id = {c.id: c for c in ledger.claims}
    seen: set = set()
    for c in ledger.claims:
        if c.kind != KIND_DERIVED or not c.computed_from or not c.formula:
            continue
        if c.fingerprint in seen:
            continue
        seen.add(c.fingerprint)
        inputs = [by_id[i] for i in c.computed_from if i in by_id]
        if len(inputs) != len(c.computed_from):
            res.drift.append({"claimId": c.id, "reason": "missing input claim",
                              "old": c.value, "new": None, "field": c.field})
            continue
        newv = _recompute(c.formula, inputs)
        if newv is None:
            res.not_recheckable += 1
            continue
        res.rechecks += 1
        old = c.value
        same = (isinstance(old, (int, float)) and isinstance(newv, (int, float))
                and abs(float(old) - float(newv)) <= config.DERIVED_RECHECK_TOLERANCE)
        if same:
            continue
        res.drift.append({"claimId": c.id, "reason": "recomputed value differs",
                          "old": old, "new": newv, "field": c.field,
                          "formula": c.formula, "inputs": c.computed_from})
    return res


def _recompute(formula: str, inputs: List[Claim]) -> Optional[float]:
    """Re-evaluate a recorded formula from its recorded inputs.

    Only the formulas this module itself writes are recognised.  An unrecognised
    formula returns ``None`` — "not rechecked" — rather than being guessed at.
    """
    vals = [i.value for i in inputs]
    raw: Optional[float]
    try:
        if formula == "last.value - first.value" and len(vals) == 2:
            raw = float(vals[1]) - float(vals[0])
        elif formula == "(last - first) / first * 100" and len(vals) == 2:
            a, b = float(vals[0]), float(vals[1])
            raw = (b - a) / a * 100.0 if a else None
        elif formula == "count(distinct sourceId mentioning entity)":
            raw = float(len(vals))
        elif formula == "count(distinct topic containing entity)":
            raw = float(len(vals))
        else:
            # Not a formula this module can re-evaluate.  Returning None means
            # "not rechecked", which is reported separately rather than silently
            # counted as a pass.
            return None
    except (TypeError, ValueError):
        return None
    if raw is None:
        return None
    # derive() stores values rounded to 4 dp; the recheck must round identically
    # or it reports drift that is only a display artifact.
    return round(raw, 4)
