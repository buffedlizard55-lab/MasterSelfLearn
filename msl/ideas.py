"""Idea synthesis — the "free thinking" stage, kept honest.

Every idea is a template whose slots are filled from claims that already passed
the evidence gate, and every idea carries the ids of those claims.  An idea that
cannot point at a verified claim is not produced.  There is no language model
here: the generator is a fixed rule set, which is what makes it repeatable and
auditable, and it is stated plainly on the site (see ``METHODOLOGY.md``).

Ideas persist.  Each cycle the previous set is re-scored against the *current*
ledger, so an idea that keeps gaining corroboration climbs and one whose support
disappears sinks.  That carry-forward is the "learning from previous ideas" part.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from . import config
from .evidence import Claim, Ledger
from .reason import Insight, days_between, split_indexed

ROBUSTNESS_WEIGHTS = {
    "evidence": 0.30,       # how many verified claims stand behind it
    "corroboration": 0.30,  # how many independent sources
    "breadth": 0.15,        # how many topic families
    "freshness": 0.15,      # how recent the newest supporting claim is
    "reproducibility": 0.10  # can a reader re-fetch it right now
}


@dataclass
class Idea:
    id: str
    cycle: int
    kind: str
    title: str
    statement: str
    lineage: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    families: List[str] = field(default_factory=list)
    urls: List[str] = field(default_factory=list)
    first_seen_cycle: int = 0
    last_seen_cycle: int = 0
    appearances: int = 1
    robustness: float = 0.0
    components: Dict[str, float] = field(default_factory=dict)
    status: str = "new"
    fingerprint: str = ""
    history: List[Dict[str, Any]] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "cycle": self.cycle, "kind": self.kind, "title": self.title,
                "statement": self.statement, "lineage": self.lineage, "sources": self.sources,
                "families": self.families, "urls": self.urls[:4],
                "firstSeenCycle": self.first_seen_cycle, "lastSeenCycle": self.last_seen_cycle,
                "appearances": self.appearances, "robustness": round(self.robustness, 4),
                "components": {k: round(v, 4) for k, v in self.components.items()},
                "status": self.status, "fingerprint": self.fingerprint,
                "history": self.history[-24:]}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Idea":
        return cls(id=d["id"], cycle=d["cycle"], kind=d["kind"], title=d["title"],
                   statement=d["statement"], lineage=d.get("lineage", []) or [],
                   sources=d.get("sources", []) or [], families=d.get("families", []) or [],
                   urls=d.get("urls", []) or [], first_seen_cycle=d.get("firstSeenCycle", 0),
                   last_seen_cycle=d.get("lastSeenCycle", 0),
                   appearances=d.get("appearances", 1), robustness=d.get("robustness", 0.0),
                   components=d.get("components", {}) or {}, status=d.get("status", "new"),
                   fingerprint=d.get("fingerprint", ""), history=d.get("history", []) or [])


def _fp(kind: str, key: str) -> str:
    import hashlib
    return hashlib.sha256(f"{kind}|{key}".encode()).hexdigest()[:16]


@dataclass
class IdeaResult:
    ideas: List[Idea] = field(default_factory=list)
    promoted: int = 0
    retired: int = 0
    rejected_no_lineage: int = 0


def score_idea(idea: Idea, ledger: Ledger, now: str, blocked_sources: set) -> None:
    """Recompute robustness from current terminal evidence, never stored scores.

    Derived claims are useful lineage nodes, but they are not fresh independent
    evidence. Recursing to their captured inputs prevents a newly re-run formula
    from making a week-old observation look new or corroborated.
    """
    by_id = {c.id: c for c in ledger.claims}
    terminal: Dict[str, Claim] = {}
    visiting: set = set()

    def visit(claim_id: str) -> None:
        if claim_id in visiting:
            return
        claim = by_id.get(claim_id)
        if claim is None:
            return
        visiting.add(claim_id)
        if claim.kind == "derived" and claim.computed_from:
            for parent in claim.computed_from:
                visit(parent)
        else:
            terminal[claim.id] = claim

    for claim_id in idea.lineage:
        visit(claim_id)
    claims = list(terminal.values())
    if not claims:
        idea.components = {"evidence": 0.0, "corroboration": 0.0, "breadth": 0.0,
                           "freshness": 0.0, "reproducibility": 0.0}
        idea.robustness = 0.0
        idea.sources = []
        idea.families = []
        return
    srcs = {c.source_id for c in claims if c.source_id != "derived"}
    fams = {c.topic for c in claims}
    newest = max(c.retrieved_at for c in claims)
    measured_age = days_between(newest, now)
    age_days = max(0.0, measured_age) if measured_age is not None else 999.0
    evidence_by_id = {e.id: e for e in ledger.evidence}

    def reproducible(c: Claim) -> bool:
        if c.source_id in blocked_sources or not c.url or not c.evidence:
            return False
        for evidence_id in c.evidence:
            evidence = evidence_by_id.get(evidence_id)
            if (evidence is not None and evidence.successful
                    and evidence.has_integrity_hash
                    and evidence.source_id == c.source_id
                    and c.url in (evidence.url, evidence.final_url)):
                return True
        return False

    live = [c for c in claims if reproducible(c)]
    comp = {
        "evidence": min(len(claims) / 12.0, 1.0),
        "corroboration": min(max(len(srcs) - 1, 0) / 3.0, 1.0),
        "breadth": min(max(len(fams) - 1, 0) / 3.0, 1.0),
        # days_between returns days. The old divisor was 7*24, accidentally
        # granting full freshness over 168 days instead of one week.
        "freshness": max(0.0, 1.0 - age_days / 7.0),
        "reproducibility": len(live) / len(claims),
    }
    idea.components = comp
    idea.robustness = sum(comp[k] * ROBUSTNESS_WEIGHTS[k] for k in ROBUSTNESS_WEIGHTS)
    idea.sources = sorted(srcs)
    idea.families = sorted(fams)


def synthesize(ledger: Ledger, cycle: int, now: str, previous: List[Idea],
               insights: List[Insight], blocked_sources: set) -> IdeaResult:
    res = IdeaResult()
    by_fp: Dict[str, Idea] = {i.fingerprint: i for i in previous if i.fingerprint}
    fresh: List[Idea] = []
    seq = [0]

    def add(kind: str, key: str, title: str, statement: str, lineage: List[str],
            urls: List[str]) -> Optional[Idea]:
        lineage = [i for i in dict.fromkeys(lineage) if i]
        if not lineage:
            res.rejected_no_lineage += 1
            return None
        fp = _fp(kind, key)
        # dedupe inside this cycle too: three search tasks can surface the same
        # subject, and one idea should not be published three times
        already = next((x for x in fresh if x.fingerprint == fp), None)
        if already is not None:
            # Multiple rules for the same fingerprint in this cycle may each add
            # current support. Do not mix in support from earlier cycles here.
            already.lineage = list(dict.fromkeys(already.lineage + lineage))
            already.urls = list(dict.fromkeys(already.urls + urls))[:4]
            return already
        prev = by_fp.get(fp)
        seq[0] += 1
        if prev is not None:
            prev.cycle = cycle
            prev.last_seen_cycle = cycle
            prev.appearances += 1
            # A recurring idea is rescored from this cycle's support, not an
            # ever-growing bag of every claim it has seen since birth.
            prev.lineage = lineage
            prev.urls = list(dict.fromkeys(urls))[:4]
            prev.status = "carried"
            fresh.append(prev)
            return prev
        idea = Idea(id=f"ID{cycle:04d}-{seq[0]:03d}", cycle=cycle, kind=kind, title=title,
                    statement=statement, lineage=lineage, urls=urls[:4],
                    first_seen_cycle=cycle, last_seen_cycle=cycle, status="new",
                    fingerprint=fp)
        fresh.append(idea)
        return idea

    claims = ledger.claims
    by_id = {c.id: c for c in claims}

    # 1. convergence — an entity several independent sources report on
    # "derived" is our own arithmetic, not a second witness.  Counting it made
    # every single-source entity look corroborated by two sources.
    ent_src: Dict[str, Dict[str, List[Claim]]] = {}
    for c in claims:
        if c.source_id == "derived":
            continue
        entities = c.subjects or [t for t in c.tags if "/" in t]
        for entity in entities:
            ent_src.setdefault(entity, {}).setdefault(c.source_id, []).append(c)
    for ent, per_src in sorted(ent_src.items()):
        if len(per_src) < 2:
            continue
        ids = [lst[-1].id for lst in per_src.values()]
        urls = [by_id[i].url for i in ids if by_id[i].url]
        add("convergence", ent,
            f"Track “{ent}” as a multi-source subject",
            f"“{ent}” is independently reported by {len(per_src)} sources "
            f"({', '.join(sorted(per_src))}).  A monitor built on all of them can be "
            f"cross-checked; one built on any single one cannot.", ids, urls)

    # 2. velocity outlier — the fastest new repository in the current ledger
    repos: Dict[str, Tuple[Optional[Claim], Optional[Claim]]] = {}
    for c in claims:
        if not c.field.startswith("github.repo["):
            continue
        parts = split_indexed(c.field)
        if not parts:
            continue
        name = next((t for t in c.tags if "/" in t), None)
        if not name:
            continue
        slot = repos.setdefault(name, (None, None))
        if c.field.endswith(".stars"):
            slot = (c, slot[1])
        elif c.field.endswith(".created"):
            slot = (slot[0], c)
        repos[name] = slot
    vel: List[Tuple[float, str, Claim, Claim]] = []
    for name, (stars, created) in repos.items():
        if stars is None or created is None or not isinstance(stars.value, (int, float)):
            continue
        age = days_between(str(created.value), now)
        if age is None or age <= 0:
            continue
        vel.append((float(stars.value) / max(age, 1.0), name, stars, created))
    if len(vel) >= 3:
        vel.sort(key=lambda x: -x[0])
        median = sorted(v[0] for v in vel)[len(vel) // 2] or 1.0
        for v, name, stars, created in vel[:3]:
            if v < median * 2.0:
                continue
            add("velocity-outlier", name,
                f"Replicate what made {name} grow",
                f"{name} reached {int(stars.value):,} stars in "
                f"{days_between(str(created.value), now) or 0:.1f} days "
                f"({v:,.1f}/day), against a median of {median:,.1f}/day across the "
                f"{len(vel)} tracked repositories.  Testable claim: its growth is "
                f"explained by something in its first-week release, not by its topic.",
                [stars.id, created.id], [stars.url] if stars.url else [])

    # 3. regulatory lead — rulemaking outrunning published research
    newest_regulatory: Dict[str, Claim] = {}
    newest_research: Dict[str, Claim] = {}
    for claim in claims:
        if (claim.field.startswith("fedreg.documents[")
                and isinstance(claim.value, (int, float))):
            newest_regulatory[claim.field] = claim
        if claim.kind == "derived" and claim.field.startswith("trend[wiki:"):
            newest_research[claim.field] = claim
    for field_name, c in sorted(newest_regulatory.items()):
        term = field_name[len("fedreg.documents["):-1]
        if term in ("newest", "*", ""):
            continue
        research = newest_research.get(f"trend[wiki:{term}]")
        lineage = [c.id] + ([research.id] if research is not None else [])
        add("regulatory-lead", term,
            f"Watch for research lagging rulemaking on “{term}”",
            f"The Federal Register holds {int(c.value):,} documents matching “{term}”. "
            f"If published-research attention on the same term stays flat while that "
            f"count rises, rulemaking is leading and the literature will follow.",
            lineage, [c.url] if c.url else [])

    # 4. contradiction — the same field, two sources, two answers
    by_field: Dict[str, Dict[str, Claim]] = {}
    for c in claims:
        if c.kind == "captured" and isinstance(c.value, (int, float)):
            # Ledger order is append-only; assignment keeps the latest value from
            # each source rather than freezing the contradiction at cycle one.
            by_field.setdefault(c.field, {})[c.source_id] = c
    for fld, per_src in sorted(by_field.items()):
        if len(per_src) < 2:
            continue
        vals = {float(c.value) for c in per_src.values()}
        if len(vals) < 2:
            continue
        ids = [c.id for c in per_src.values()]
        add("contradiction", fld,
            f"Reconcile the disagreement on {fld}",
            f"{len(per_src)} sources report different values for {fld} "
            f"({', '.join(f'{s}={c.value}' for s, c in sorted(per_src.items()))}). "
            f"Until that is explained, neither number should be quoted alone.",
            ids, [c.url for c in per_src.values() if c.url])

    # 5. decay — attention that is falling
    for ins in insights:
        if ins.kind != "trend":
            continue
        m = re.search(r"trend\[wiki:(?P<art>[^\]]+)\]",
                      next((c.field for c in claims if c.id in ins.claim_ids), ""))
        art = m.group("art") if m else None
        if not art or "fell" not in ins.text and "−" not in ins.text:
            continue
        add("attention-decay", art,
            f"Explain the fall in attention to “{art}”",
            f"{ins.text}  Distinguish a seasonal dip from a genuine end of interest "
            f"before acting on either reading.", ins.claim_ids,
            [c.url for c in claims if c.id in ins.claim_ids and c.url])

    # 6. honest gap — a family with no verified claims
    fam_claims: Dict[str, int] = {}
    for c in claims:
        fam_claims[c.topic] = fam_claims.get(c.topic, 0) + 1
    from .topics import FAMILIES
    for fam in FAMILIES:
        n = fam_claims.get(fam.slug, 0)
        if n > 0:
            continue
        add("gap", fam.slug,
            f"No verified evidence yet for “{fam.title}”",
            f"{cycle - 1} cycles in, the question “{fam.question}” has {n} verified "
            f"claims behind it.  Either find an official source that can answer it or "
            f"drop the family — do not fill the gap with prose.",
            [], [])
        # gaps deliberately have no lineage; they are reported, not scored

    # score everything against the current ledger
    for idea in fresh:
        score_idea(idea, ledger, now, blocked_sources)
        idea.history.append({"cycle": cycle, "robustness": idea.robustness,
                             "lineageSize": len(idea.lineage)})

    # carry forward ideas that were not regenerated but still have support
    kept_fp = {i.fingerprint for i in fresh}
    for prev in previous:
        if prev.fingerprint in kept_fp:
            continue
        score_idea(prev, ledger, now, blocked_sources)
        if prev.robustness <= 0.0:
            prev.status = "retired"
            res.retired += 1
            continue
        prev.status = "carried"
        prev.history.append({"cycle": cycle, "robustness": prev.robustness,
                             "lineageSize": len(prev.lineage)})
        fresh.append(prev)

    fresh.sort(key=lambda i: -i.robustness)
    for i in fresh:
        if i.status == "carried" and i.robustness >= 0.55 and i.appearances >= 2:
            i.status = "promoted"
            res.promoted += 1
    res.ideas = fresh
    return res
