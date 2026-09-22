"""The irregularity register.

Anything the engine could not resolve, anything that disagreed with itself, and
anything it refuses to claim becomes a numbered entry here with a severity, a
reproduction command or URL, and the cycle it was first seen in.  Entries are
keyed by a fingerprint so the same finding keeps the same id across cycles
instead of being re-minted, and an entry that stops recurring is marked
``resolved`` rather than deleted.

Some entries are *standing* — they are structural facts about this project (no
official keyless API exists for X; the owner's source document could not be read
by a machine) rather than transient failures.  Those are registered with
``standing: true`` and never auto-resolve, because they are limitations the owner
needs to keep seeing.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import config

CRITICAL = "critical"
WARN = "warn"
INFO = "info"
ORDER = {CRITICAL: 0, WARN: 1, INFO: 2}


@dataclass
class Irregularity:
    id: str
    fingerprint: str
    severity: str
    title: str
    detail: str
    repro: str = ""
    first_seen_cycle: int = 0
    first_seen_at: str = ""
    last_seen_cycle: int = 0
    last_seen_at: str = ""
    occurrences: int = 1
    status: str = "open"
    standing: bool = False
    source_id: str = ""
    topic: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "fingerprint": self.fingerprint, "severity": self.severity,
                "title": self.title, "detail": self.detail, "repro": self.repro,
                "firstSeenCycle": self.first_seen_cycle, "firstSeenAt": self.first_seen_at,
                "lastSeenCycle": self.last_seen_cycle, "lastSeenAt": self.last_seen_at,
                "occurrences": self.occurrences, "status": self.status,
                "standing": self.standing, "sourceId": self.source_id, "topic": self.topic}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Irregularity":
        return cls(id=d["id"], fingerprint=d["fingerprint"], severity=d["severity"],
                   title=d["title"], detail=d["detail"], repro=d.get("repro", ""),
                   first_seen_cycle=d.get("firstSeenCycle", 0),
                   first_seen_at=d.get("firstSeenAt", ""),
                   last_seen_cycle=d.get("lastSeenCycle", 0),
                   last_seen_at=d.get("lastSeenAt", ""),
                   occurrences=d.get("occurrences", 1), status=d.get("status", "open"),
                   standing=bool(d.get("standing")), source_id=d.get("sourceId", ""),
                   topic=d.get("topic", ""))


def _fp(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]


# --------------------------------------------------------------------------- #
# standing findings — verified facts about the limits of this project
# --------------------------------------------------------------------------- #
def standing_findings() -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    def add(sev: str, title: str, detail: str, repro: str = "", src: str = "",
            topic: str = "") -> None:
        out.append({"severity": sev, "title": title, "detail": detail, "repro": repro,
                    "standing": True, "source_id": src, "topic": topic})

    add(WARN, "The owner's source document could not be read by a machine",
        "The brief points at a shared ChatGPT transcript "
        "(https://chatgpt.com/share/6ab1612a-2f14-83e8-9de6-808d21a48e53). A GET of that "
        "URL returns an HTML shell whose body is rendered client-side; the only "
        "server-supplied content is the <title>, “Design Autonomous Research System”. "
        "No requirement in this repository is sourced from that transcript. The design "
        "was derived instead from the written brief and from the owner's own published "
        "corpus, which is readable. If the transcript contains requirements that are "
        "missing here, they are missing.",
        repro="curl -s https://chatgpt.com/share/6ab1612a-2f14-83e8-9de6-808d21a48e53 | grep -o '<title>[^<]*'",
        topic="owner-corpus")

    add(WARN, "GitHub publishes no trending API",
        "The obvious “trending repositories” signal has no official endpoint: "
        "https://github.com/trending returns HTML only, and GitHub's REST API exposes "
        "no trending route. The engine substitutes the official Search API sorted by "
        "stars over a created:>= window, which is reproducible and documented, and says "
        "so wherever the number appears. A trending *page* is a curated list with an "
        "undisclosed ranking; a search result is not, and the two are not equivalent.",
        repro="curl -s -o /dev/null -w '%{http_code} %{content_type}\\n' https://github.com/trending",
        src="github_search", topic="open-source-momentum")

    add(WARN, "npm's documented media type is rejected by its own dist-tags endpoint",
        "GET https://registry.npmjs.org/-/package/next/dist-tags answers 200 for "
        "Accept: application/json and HTTP 406 Not Acceptable for "
        "Accept: application/vnd.npm.install-v1+json — the media type the registry "
        "documents for package metadata. Observed 2026-09-21 from two independent "
        "hosts. The engine therefore sends Accept: application/json for this route. "
        "This is recorded rather than quietly worked around so the next reader does "
        "not rediscover it.",
        repro=("curl -s -o /dev/null -w '%{http_code}\\n' -H 'Accept: application/vnd.npm.install-v1+json' "
               "https://registry.npmjs.org/-/package/next/dist-tags   # -> 406"),
        src="npm_registry", topic="open-source-momentum")

    add(WARN, "Three interest categories have no registered source that can serve them",
        "Travel & Korea Trip, Social & Creator Data, and Elections & Civic Data appear in "
        "the owner's verified corpus, but no official keyless API is registered that can "
        "answer their questions: hotel and airfare pricing has no keyless official API at "
        "all; every creator platform API is keyed; the FEC API requires a key for most "
        "routes and state results are per-jurisdiction. No claim is made about these "
        "categories. See KEYED_SOURCES_EXCLUDED in msl/sources.py and ROADMAP.md.",
        repro="python3 -c \"import msl.sources as s; print(s.INTEREST_CATEGORIES_WITHOUT_A_SOURCE)\"",
        topic="travel-korea")

    add(INFO, "Six useful sources are excluded because they need an API key",
        "FRED, the NFL Game API, Google Trends, the X API, the YouTube Data API and the "
        "TikTok/Instagram APIs were all rejected. Obtaining a key is manual input, which "
        "the brief rules out. Each is listed with the reason in msl/sources.py → "
        "KEYED_SOURCES_EXCLUDED so the omission is a decision on the record, not a gap.",
        repro="python3 -c \"import msl.sources as s; [print(x['id'], x['reason']) for x in s.KEYED_SOURCES_EXCLUDED]\"")

    add(INFO, "Three sports feeds are undocumented public endpoints",
        "statsapi.mlb.com, api-web.nhle.com and cdn.nba.com are the leagues' own hosts and "
        "the same feeds the owner's sibling labs already read, but no official public "
        "documentation page was located for any of them. They are registered with an "
        "explicit UNDOCUMENTED marker, and any claim built from one carries that marker "
        "too, so nothing on the site implies a contract exists.",
        repro="grep -n 'UNDOCUMENTED' msl/sources.py",
        topic="sports-signals")

    add(INFO, "Frankfurter is not an official ECB endpoint",
        "frankfurter.app republishes ECB euro reference rates but is a community service. "
        "It is registered as a redundancy check against the official ECB SDMX route, and "
        "every claim it produces is labelled third-party in the statement text itself, so "
        "it can never be quoted as an ECB figure.",
        repro="grep -n 'third-party' msl/adapters.py | head",
        src="frankfurter", topic="macro-signals")

    add(INFO, "The reasoning stage contains no language model",
        "Every sentence published by this project is a template whose slots are filled "
        "from claim values, and every idea comes from a fixed rule set over the verified "
        "ledger. That is a deliberate limitation: it makes the output reproducible and "
        "auditable at the cost of novelty. A model with an API key would need a secret, "
        "and adding a secret is manual input. See METHODOLOGY.md §3.",
        repro="grep -rn 'openai\\|anthropic\\|llm_client' msl/ || echo 'no model client present'")

    add(INFO, "Seed captures taken by an interactive read are not wire-hash verifiable",
        "The first captures for wikimedia_pageviews, federal_register, usgs_fdsn and "
        "hn_firebase were read through an interactive agent fetch rather than by this "
        "process, so the stored SHA-256 covers the recorded body and not the bytes on the "
        "wire. Those evidence rows carry wireHashVerifiable=false, and the first automated "
        "probe re-reads each endpoint and reports whether the values still match.",
        repro="python3 -c \"import json;[print(json.loads(l)['id'], json.loads(l)['wireHashVerifiable']) for l in open('data/evidence.jsonl') if not json.loads(l)['wireHashVerifiable']]\"")

    return out


class Register:
    def __init__(self, data_dir: Optional[pathlib.Path] = None):
        self.dir = pathlib.Path(data_dir or config.DATA)
        self.path = self.dir / "irregularities.json"
        self.items: Dict[str, Irregularity] = {}
        self._seq = 0
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return
        try:
            d = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        for row in d.get("items", []):
            it = Irregularity.from_dict(row)
            self.items[it.fingerprint] = it
            self._seq = max(self._seq, _num(it.id))

    def save(self, generated_at: str, cycle: int) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        items = sorted(self.items.values(),
                       key=lambda i: (ORDER.get(i.severity, 3), -i.last_seen_cycle, i.id))
        payload = {
            "generatedAt": generated_at, "cycle": cycle,
            "counts": self.counts(),
            "items": [i.as_dict() for i in items],
        }
        self.path.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n",
                             encoding="utf-8")

    def counts(self) -> Dict[str, int]:
        out = {"total": len(self.items), CRITICAL: 0, WARN: 0, INFO: 0,
               "open": 0, "resolved": 0, "standing": 0}
        for i in self.items.values():
            out[i.severity] = out.get(i.severity, 0) + 1
            out[i.status] = out.get(i.status, 0) + 1
            if i.standing:
                out["standing"] += 1
        return out

    def add(self, severity: str, title: str, detail: str, cycle: int, now: str,
            repro: str = "", standing: bool = False, source_id: str = "",
            topic: str = "", fingerprint: Optional[str] = None) -> Irregularity:
        fp = fingerprint or _fp(title, source_id, topic)
        existing = self.items.get(fp)
        if existing is not None:
            existing.occurrences += 1
            existing.last_seen_cycle = cycle
            existing.last_seen_at = now
            existing.severity = severity
            existing.detail = detail
            if existing.status == "resolved":
                existing.status = "open"
            return existing
        self._seq += 1
        it = Irregularity(id=f"IRR-{self._seq:03d}", fingerprint=fp, severity=severity,
                          title=title, detail=detail, repro=repro,
                          first_seen_cycle=cycle, first_seen_at=now,
                          last_seen_cycle=cycle, last_seen_at=now,
                          status="open", standing=standing, source_id=source_id,
                          topic=topic)
        self.items[fp] = it
        return it

    def resolve_absent(self, seen_fps: set, cycle: int) -> List[str]:
        """Mark non-standing entries that did not recur this cycle as resolved."""
        resolved = []
        for fp, it in self.items.items():
            if it.standing or fp in seen_fps:
                continue
            if it.status == "open":
                it.status = "resolved"
                resolved.append(it.id)
        return resolved

    def register_standing(self, cycle: int, now: str) -> None:
        for f in standing_findings():
            self.add(f["severity"], f["title"], f["detail"], cycle, now,
                     repro=f.get("repro", ""), standing=True,
                     source_id=f.get("source_id", ""), topic=f.get("topic", ""))


def _num(iid: str) -> int:
    try:
        return int(iid.split("-")[-1])
    except ValueError:
        return 0
