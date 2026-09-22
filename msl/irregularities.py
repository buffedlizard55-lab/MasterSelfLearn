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
import urllib.parse
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import config
from .sources import (INTEREST_CATEGORIES_WITHOUT_A_SOURCE, KEYED_SOURCES_EXCLUDED,
                      REGISTRY)

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

    # The count and the list are derived from the registry, never typed here:
    # this title used to read "Three interest categories..." and stayed at three
    # after a fourth gap was found, so the register understated the gap it exists
    # to report.  A pinned fingerprint keeps the existing IRR-036 identity while
    # the wording is corrected — standing entries never auto-resolve, so a title
    # change without a pinned fingerprint would strand the old entry open forever
    # with a stale count and mint a duplicate alongside it.
    _gaps = INTEREST_CATEGORIES_WITHOUT_A_SOURCE
    _names = ", ".join(g["category"] for g in _gaps)
    _detail = " ".join(f"• {g['category']}: {g['gap']}" for g in _gaps)
    out.append({
        "severity": WARN,
        "title": (f"{len(_gaps)} interest categories have documented missing or "
                  f"partial coverage"),
        "detail": (f"{_names} appear in the owner's verified corpus "
                   f"({config.MASTER_SITE_URL}), but the registered official/keyless "
                   f"surface cannot answer important parts of their questions. Partial "
                   f"signals are retained where available; no claim is made beyond that "
                   f"surface. Per category: {_detail} "
                   f"See KEYED_SOURCES_EXCLUDED and "
                   f"INTEREST_CATEGORIES_WITHOUT_A_SOURCE in msl/sources.py and "
                   f"ROADMAP.md."),
        "repro": ("python3 -c \"import msl.sources as s; "
                  "[print(g['category'], '::', g['gap']) for g in "
                  "s.INTEREST_CATEGORIES_WITHOUT_A_SOURCE]\""),
        "standing": True,
        "topic": "travel-korea",
        # Pinned to the fingerprint the entry was minted with (IRR-036).
        "fingerprint": "db11cd28e56a",
    })

    # Both titles below used to hard-code their own counts ("Six", "Three"), which
    # is the same staleness bug the category finding above had: the number is a
    # function of a list defined elsewhere, so it has to be computed from it.
    _keyed = KEYED_SOURCES_EXCLUDED
    _undoc = [s for s in REGISTRY if "UNDOCUMENTED" in (s.notes or "")
              or "UNDOCUMENTED" in (s.docs_note or "")]
    out.append({
        "severity": INFO,
        "title": f"{len(_keyed)} useful sources are excluded because they need an API key",
        "detail": (f"{', '.join(x['name'] for x in _keyed)} were all rejected. Obtaining a "
                   f"key is manual input, which the brief rules out. Each is listed with "
                   f"the reason in msl/sources.py → KEYED_SOURCES_EXCLUDED so the omission "
                   f"is a decision on the record, not a gap."),
        "repro": ("python3 -c \"import msl.sources as s; "
                  "[print(x['id'], x['reason']) for x in s.KEYED_SOURCES_EXCLUDED]\""),
        "standing": True,
        "fingerprint": "cbaa30023f8d",
    })
    out.append({
        "severity": INFO,
        "title": f"{len(_undoc)} sports feeds are undocumented public endpoints",
        "detail": (f"{', '.join(urllib.parse.urlsplit(s.probe_url).netloc for s in _undoc)} "
                   f"are the leagues' own hosts and the same feeds the owner's sibling "
                   f"labs already read, but no official public documentation page was "
                   f"located for any of them. They are registered with an explicit "
                   f"UNDOCUMENTED marker, and any claim built from one carries that "
                   f"marker too, so nothing on the site implies a contract exists."),
        "repro": "grep -n 'UNDOCUMENTED' msl/sources.py",
        "standing": True,
        "topic": "sports-signals",
        "fingerprint": "90ae5e67e77d",
    })

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

    add(WARN, "Cycles 1–18 retained projection hashes, not response-byte hashes",
        "An audit of the 817 historical evidence rows found 795 with rawBytes=0 and no "
        "payloadSha256; 777 of those also carried the old wireHashVerifiable=true flag. "
        "Every one has a canonical projection hash, but that cannot prove the bytes that "
        "arrived over HTTP. The loader now classifies them as integrity=projection rather "
        "than retroactively upgrading them. Schema-v2 live reads hash the exact "
        "decompressed body handed to the adapter and retain final URL, content type, and "
        "truncation state.",
        repro="python3 tools/verify_claims.py | sed -n '/evidence integrity/,/claim trace/p'",
        topic="evidence-integrity")

    add(INFO, "GitHub's half-hour schedule is best effort, not a nonstop SLA",
        "think.yml requests a cycle every 30 minutes, but GitHub documents that scheduled "
        "workflows can be delayed or dropped during high load. The generated timestamp and "
        "cycle history expose gaps, and writer workflows are serialized, but a repository "
        "running on hosted Actions cannot guarantee hard real-time continuous execution.",
        repro=("open https://docs.github.com/en/actions/reference/workflows-and-actions/"
               "events-that-trigger-workflows#schedule"),
        topic="source-health")

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
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(json.dumps(payload, indent=1, ensure_ascii=False,
                                  allow_nan=False) + "\n", encoding="utf-8")
        tmp.replace(self.path)

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
            # A pinned fingerprint deliberately keeps identity across a wording
            # correction. Update every display field; otherwise the stale title
            # that motivated the pin survives forever while only its detail moves.
            existing.title = title
            existing.detail = detail
            existing.repro = repro
            existing.standing = standing
            existing.source_id = source_id
            existing.topic = topic
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
                     source_id=f.get("source_id", ""), topic=f.get("topic", ""),
                     # A finding may pin its fingerprint to keep its identity
                     # (and so its IRR id) across a wording change.
                     fingerprint=f.get("fingerprint"))


def _num(iid: str) -> int:
    try:
        return int(iid.split("-")[-1])
    except ValueError:
        return 0
