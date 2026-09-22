"""Topic model and the interest profile.

The interest profile is **derived**, not asserted: ``build_interest_profile`` reads
``data/seed/owner_repos.json`` (a hashed capture of the owner's own public corpus)
and scores a fixed vocabulary against the repository names and descriptions it
finds there.  Nothing in the profile is written by hand, so a change in the
owner's published work changes the profile on the next cycle with no input.
"""
from __future__ import annotations

import json
import pathlib
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import config

STATUS_CANDIDATE = "candidate"
STATUS_ACTIVE = "active"
STATUS_RETIRED = "retired"
STATUS_BLOCKED = "blocked-no-source"


@dataclass
class TopicFamily:
    """A fixed branch of the library, bound to the sources that can feed it."""

    slug: str
    title: str
    category: str
    sources: List[str]
    question: str
    keywords: List[str] = field(default_factory=list)
    #: set when no registered source can answer the question at all
    blocked_reason: str = ""


FAMILIES: List[TopicFamily] = [
    TopicFamily("ai-research-frontier", "AI research frontier", "Science & ML Research",
                ["arxiv", "openalex", "crossref", "europepmc", "huggingface", "federal_register"],
                "Which research directions are gaining published evidence fastest?",
                ["llm", "reasoning", "agent", "model", "transformer", "retrieval", "alignment", "evaluation"]),
    TopicFamily("open-source-momentum", "Open-source momentum", "Science & ML Research",
                ["github_search", "github_repo", "github_releases", "pypi_json",
                 "npm_registry", "stackexchange"],
                "Which new software is attracting maintainers and stars fastest?",
                ["agent", "framework", "runtime", "toolkit", "sdk", "compiler", "inference"]),
    TopicFamily("public-attention", "Public attention", "Social & Creator Data",
                ["wikimedia_pageviews", "hn_firebase"],
                "What is the public reading about, and is that attention rising or falling?",
                []),
    TopicFamily("regulatory-flow", "Regulatory flow", "Elections & Civic Data",
                ["federal_register"],
                "Which policy areas are generating federal rulemaking activity?",
                ["artificial intelligence", "data", "health", "energy", "security", "finance"]),
    TopicFamily("macro-signals", "Macro signals", "Markets & Trading Research",
                ["ecb_sdmx", "frankfurter", "worldbank", "bls"],
                "What are the official macro series doing?",
                ["inflation", "exchange rate", "gdp", "employment"]),
    TopicFamily("geohazards", "Geohazards", "Science & ML Research",
                ["usgs_fdsn"],
                "How active is the planet this week, by the survey's own count?",
                ["earthquake", "magnitude"]),
    TopicFamily("sf-local", "San Francisco local conditions", "SF Local Guides",
                ["nws_alerts", "census_acs"],
                "What are the official agencies saying about conditions in San Francisco?",
                ["san francisco", "california", "alert", "weather"]),
    TopicFamily("clinical-evidence", "Clinical evidence", "Health & Personal Guides",
                ["clinicaltrials", "pubmed", "europepmc"],
                "Which clinical questions are being actively investigated?",
                ["trial", "therapy", "shoulder", "musculoskeletal", "pain"]),
    TopicFamily("public-health-policy", "Public health policy", "Health & Personal Guides",
                ["pubmed", "federal_register"],
                "Where are public-health agencies directing attention?",
                ["cdc", "public health", "surveillance", "data exchange"]),
    TopicFamily("sports-signals", "Sports signals", "Sports Data & Scoreboards",
                ["mlb_statsapi", "nhl_web", "nba_cdn", "kalshi_public"],
                "What do the leagues' own public feeds report?",
                ["mlb", "nhl", "nba", "nfl", "schedule", "scoreboard"]),
    TopicFamily("market-lab-ecosystem", "Market-lab ecosystem", "Markets & Trading Research",
                ["kalshi_public", "sec_edgar", "github_search"],
                "How is the prediction-market and paper-trading research ecosystem moving?",
                ["kalshi", "prediction market", "paper trading", "backtest"]),
    TopicFamily("owner-corpus", "Owner corpus", "Directory & Meta",
                ["github_repos"],
                "How is the owner's own published research corpus growing?",
                []),
    TopicFamily("travel-korea", "Travel & Korea", "Travel & Korea Trip",
                ["nominatim"],
                "What can official sources say about Korea travel planning?",
                ["seoul", "busan", "korea"],
                blocked_reason=("No official keyless API for lodging or airfare pricing is "
                                "registered; nominatim can geocode a place but cannot price it. "
                                "No pricing claim is made. See ROADMAP.md.")),
]

FAMILY_BY_SLUG: Dict[str, TopicFamily] = {f.slug: f for f in FAMILIES}


@dataclass
class Topic:
    """One node of the library.  Families are nodes; discovered entities are nodes."""

    slug: str
    title: str
    family: str
    status: str = STATUS_CANDIDATE
    created_cycle: int = 0
    first_seen_at: str = ""
    last_signal_cycle: int = 0
    last_seen_at: str = ""
    signals: int = 0
    claims: int = 0
    interest_score: float = 0.0
    parent: str = ""
    lineage: List[str] = field(default_factory=list)
    origin: str = ""          # which discovery rule created it
    origin_url: str = ""
    notes: str = ""
    history: List[Dict[str, Any]] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "slug": self.slug, "title": self.title, "family": self.family,
            "status": self.status, "createdCycle": self.created_cycle,
            "firstSeenAt": self.first_seen_at, "lastSignalCycle": self.last_signal_cycle,
            "lastSeenAt": self.last_seen_at, "signals": self.signals,
            "claims": self.claims, "interestScore": round(self.interest_score, 4),
            "parent": self.parent, "lineage": self.lineage, "origin": self.origin,
            "originUrl": self.origin_url, "notes": self.notes, "history": self.history[-60:],
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Topic":
        return cls(slug=d["slug"], title=d["title"], family=d["family"],
                   status=d.get("status", STATUS_CANDIDATE),
                   created_cycle=d.get("createdCycle", 0),
                   first_seen_at=d.get("firstSeenAt", ""),
                   last_signal_cycle=d.get("lastSignalCycle", 0),
                   last_seen_at=d.get("lastSeenAt", ""), signals=d.get("signals", 0),
                   claims=d.get("claims", 0), interest_score=d.get("interestScore", 0.0),
                   parent=d.get("parent", ""), lineage=d.get("lineage", []) or [],
                   origin=d.get("origin", ""), origin_url=d.get("originUrl", ""),
                   notes=d.get("notes", ""), history=d.get("history", []) or [])


class Library:
    """The expanding topic library, persisted to ``data/library.json``."""

    def __init__(self, data_dir: Optional[pathlib.Path] = None):
        self.dir = pathlib.Path(data_dir or config.DATA)
        self.path = self.dir / "library.json"
        self.topics: Dict[str, Topic] = {}
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return
        try:
            d = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        for t in d.get("topics", []):
            topic = Topic.from_dict(t)
            self.topics[topic.slug] = topic

    def save(self, generated_at: str) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "generatedAt": generated_at,
            "counts": self.counts(),
            "topics": sorted((t.as_dict() for t in self.topics.values()),
                             key=lambda x: (-x["signals"], x["slug"])),
        }
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(json.dumps(payload, indent=1, ensure_ascii=False,
                                  allow_nan=False) + "\n", encoding="utf-8")
        tmp.replace(self.path)

    def get(self, slug: str) -> Optional[Topic]:
        return self.topics.get(slug)

    def ensure(self, slug: str, title: str, family: str, now: str, cycle: int,
               origin: str = "", origin_url: str = "", parent: str = "",
               notes: str = "", status: str = STATUS_CANDIDATE) -> Topic:
        t = self.topics.get(slug)
        if t is None:
            lineage = ([parent] if parent else [])
            t = Topic(slug=slug, title=title, family=family, status=status,
                      created_cycle=cycle, first_seen_at=now, last_signal_cycle=cycle,
                      last_seen_at=now, signals=1, origin=origin,
                      origin_url=origin_url, parent=parent, lineage=lineage, notes=notes)
            self.topics[slug] = t
        else:
            t.signals += 1
            t.last_signal_cycle = cycle
            t.last_seen_at = now
            if t.status == STATUS_CANDIDATE and t.signals >= config.MIN_SIGNALS_TO_PROPOSE_TOPIC:
                t.status = STATUS_ACTIVE
        return t

    def touch(self, slug: str, now: str, cycle: int, claims_delta: int = 0) -> None:
        t = self.topics.get(slug)
        if t is None:
            return
        t.last_seen_at = now
        t.last_signal_cycle = cycle
        t.claims += claims_delta

    def retire_stale(self, cycle: int) -> List[str]:
        retired: List[str] = []
        for t in self.topics.values():
            if t.status in (STATUS_RETIRED, STATUS_BLOCKED):
                continue
            if cycle - t.last_signal_cycle >= config.CYCLES_BEFORE_RETIREMENT:
                t.status = STATUS_RETIRED
                retired.append(t.slug)
        return retired

    def counts(self) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for t in self.topics.values():
            out[t.status] = out.get(t.status, 0) + 1
        out["total"] = len(self.topics)
        fams: Dict[str, int] = {}
        for t in self.topics.values():
            fams[t.family] = fams.get(t.family, 0) + 1
        out["families"] = len(fams)
        return out


_TOKEN = re.compile(r"[a-z][a-z0-9]{2,}")
_STOP = {
    "the", "and", "for", "with", "from", "that", "this", "your", "you", "are", "was",
    "has", "have", "not", "all", "one", "its", "our", "new", "any", "get", "use",
    "app", "api", "web", "com", "www", "http", "https", "github", "git", "src", "docs",
    "project", "projects", "repo", "code", "tool", "tools", "data", "json", "python",
    "javascript", "typescript", "official", "simple", "fast", "easy", "just", "more",
    "other", "into", "out", "over", "under", "per", "via", "using", "used", "uses",
}


def keywords_from_text(text: str, limit: int = 40) -> List[str]:
    toks = [t for t in _TOKEN.findall((text or "").lower()) if t not in _STOP]
    seen: Dict[str, int] = {}
    for t in toks:
        seen[t] = seen.get(t, 0) + 1
    return [k for k, _ in sorted(seen.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]]


def build_interest_profile(seed_dir: Optional[pathlib.Path] = None) -> Dict[str, Any]:
    """Score interest categories against the owner's own published corpus.

    Reads ``data/seed/owner_repos.json`` (a hashed capture) and returns per-category
    scores plus the keywords that produced them.  Returns ``available: False`` with
    a reason if the capture is missing — it never invents a profile.
    """
    d = pathlib.Path(seed_dir or config.SEED)
    p = d / "owner_repos.json"
    if not p.exists():
        return {"available": False, "reason": f"missing capture {p}",
                "categories": {}, "keywords": [], "repoCount": 0}
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return {"available": False, "reason": f"unreadable capture: {e}",
                "categories": {}, "keywords": [], "repoCount": 0}
    # The projection is the raw GitHub array (so msl/adapters.gh_repos can read it
    # directly); an older capture shape wrapped it as {"repos": [...]}.  Accept both
    # rather than crashing the cycle on a shape change.
    proj = rec.get("projection")
    if isinstance(proj, list):
        repos = [r for r in proj if isinstance(r, dict)]
    elif isinstance(proj, dict):
        repos = [r for r in (proj.get("repos") or []) if isinstance(r, dict)]
    else:
        repos = []
    text = " ".join((r.get("name") or "") + " " + (r.get("description") or "") for r in repos)
    kws = keywords_from_text(text, 60)
    kwset = set(kws)

    scores: Dict[str, float] = {}
    hits: Dict[str, List[str]] = {}
    for fam in FAMILIES:
        n = 0
        found: List[str] = []
        for k in fam.keywords:
            for tok in re.findall(r"[a-z0-9]+", k.lower()):
                if tok in kwset:
                    n += 1
                    found.append(tok)
                    break
        # repository-name corroboration: does the corpus contain a repo for this family?
        corpus_hits = 0
        for r in repos:
            name = (r.get("name") or "").lower()
            if any(tok in name for tok in found[:6]) or any(
                    k.split()[0] in name for k in fam.keywords[:6] if k):
                corpus_hits += 1
        scores[fam.slug] = round(n + corpus_hits * 0.25, 3)
        hits[fam.slug] = sorted(set(found))

    return {
        "available": True,
        "source": "data/seed/owner_repos.json",
        "sourceUrl": rec.get("url", ""),
        "payloadSha256": rec.get("payloadSha256", ""),
        "capturedAt": rec.get("capturedAt", ""),
        "repoCount": len(repos),
        "keywords": kws,
        "categories": scores,
        "categoryKeywords": hits,
    }
