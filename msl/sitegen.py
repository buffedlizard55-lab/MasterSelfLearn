"""Site data generation.

Writes ``data/site.js`` — one JSON object assigned to ``window.MSLDATA``.  The
pages are static and read nothing but this file, so there is no build step, no
framework and no runtime dependency, and the whole site works from
``file://`` too.

Every value in the object comes from the ledger, the library, the register or the
registry.  Nothing here formats a number the pipeline did not produce.
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List, Optional

from . import config
from .evidence import Ledger
from .ideas import Idea
from .irregularities import ORDER, Register
from .pipeline import CycleReport, load_seeds
from .sources import (INTEREST_CATEGORIES_WITHOUT_A_SOURCE, KEYED_SOURCES_EXCLUDED,
                      REGISTRY)
from .topics import FAMILY_BY_SLUG, FAMILIES, Library


def _read_json(p: pathlib.Path) -> Dict[str, Any]:
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def render(d: pathlib.Path, now: str, rep: CycleReport, ledger: Ledger,
           library: Library, memory: Dict[str, Any], register: Register) -> pathlib.Path:
    lb = _read_json(d / "leaderboard.json")
    ideas_doc = _read_json(d / "ideas.json")
    insights_doc = _read_json(d / "insights.json")
    sources_doc = _read_json(d / "sources.json")
    profile = _read_json(d / "profile.json")

    cycles: List[Dict[str, Any]] = []
    cp = d / "cycles.jsonl"
    if cp.exists():
        for line in cp.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                cycles.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    topics = []
    claim_counts = ledger.topics_with_claims()
    for t in sorted(library.topics.values(),
                    key=lambda x: (-x.interest_score, -x.signals, x.slug)):
        fam = FAMILY_BY_SLUG.get(t.family)
        topics.append({
            **t.as_dict(),
            "familyTitle": fam.title if fam else t.family,
            "category": fam.category if fam else "",
            "question": fam.question if fam else "",
            "verifiedClaims": claim_counts.get(t.slug, 0),
            "interest": (memory.get("topicInterest") or {}).get(t.slug, {}),
        })

    irr = sorted(register.items.values(),
                 key=lambda i: (ORDER.get(i.severity, 3), -i.last_seen_cycle, i.id))

    # Evidence rows are published once, keyed by id; claims reference them by id.
    # Inlining a copy of the same handful of reads into every claim row duplicated
    # the payload ~40x for no gain.
    ev_ids = {e.id for e in ledger.evidence}
    evidence_rows = {
        e.id: {
            "id": e.id, "url": e.url, "status": e.status,
            "capturedAt": e.captured_at, "sha256": e.payload_sha256 or e.projection_sha256,
            "rawBytes": e.raw_bytes, "captureMode": e.capture_mode,
            "wireHashVerifiable": e.wire_hash_verifiable,
        }
        for e in ledger.evidence
    }
    # The site publishes a WINDOW of the ledger, not all of it.  At ~500 claims per
    # cycle and 48 cycles a day, shipping every claim ever made would make the page
    # unloadable within a fortnight.  The append-only JSONL on disk stays the record;
    # the page says plainly that it is showing a window.
    window = 1500
    claim_rows = [{**c.as_dict(),
                   "evidenceIds": [i for i in c.evidence if i in ev_ids]}
                  for c in ledger.claims[-window:]]

    forecasts_doc = _read_json(d / "forecasts.json")
    fc = forecasts_doc.get("items", [])

    data = {
        "meta": {
            "generatedAt": now,
            "cycle": rep.cycle,
            "mode": rep.mode,
            "repoUrl": config.REPO_URL,
            "siteUrl": config.SITE_URL,
            "masterSiteUrl": config.MASTER_SITE_URL,
            "owner": config.REPO_OWNER,
            "cron": config.CYCLE_CRON,
            "intervalMinutes": config.CYCLE_INTERVAL_MINUTES,
            "version": _version(),
        },
        "autoCounts": rep.auto_counts(),
        "report": rep.summary(),
        "claimKindCounts": ledger.counts(),
        "families": [{
            "slug": f.slug, "title": f.title, "category": f.category,
            "question": f.question, "sources": f.sources,
            "blockedReason": f.blocked_reason,
            "topics": sum(1 for t in library.topics.values() if t.family == f.slug),
            "verifiedClaims": sum(claim_counts.get(t.slug, 0) for t in library.topics.values()
                                  if t.family == f.slug),
        } for f in FAMILIES],
        "topics": topics,
        "insights": sorted(insights_doc.get("items", []),
                           key=lambda i: -float(i.get("importance", 0)))[:120],
        "ideas": ideas_doc.get("items", []),
        "leaderboard": lb,
        "forecasts": fc[-600:],
        "sources": sources_doc.get("sources", [s.as_dict() for s in REGISTRY]),
        "keyedExcluded": KEYED_SOURCES_EXCLUDED,
        "categoriesWithoutSource": INTEREST_CATEGORIES_WITHOUT_A_SOURCE,
        "irregularities": [i.as_dict() for i in irr],
        "irregularityCounts": register.counts(),
        "evidence": claim_rows,
        "evidenceRows": evidence_rows,
        "evidenceTotal": len(ledger.evidence),
        "claimTotal": len(ledger.claims),
        "claimWindow": len(claim_rows),
        "gateRejections": ledger.rejections[-200:],
        "cycles": cycles[-120:],
        "cyclesTotal": len(cycles),
        "memory": {
            "cyclesRun": memory.get("cyclesRun", 0),
            "strategyWeights": memory.get("strategyWeights", {}),
            "sourceReliability": memory.get("sourceReliability", {}),
            "lessons": memory.get("lessons", []),
            "consecutiveCycleFailures": memory.get("consecutiveCycleFailures", 0),
        },
        "profile": profile,
        "seedCaptures": [{"file": r.get("_file", ""), "url": r.get("url", ""),
                          "capturedAt": r.get("capturedAt", ""),
                          "payloadSha256": r.get("payloadSha256", ""),
                          "httpStatus": r.get("httpStatus"),
                          "rawBytes": r.get("rawBytes"),
                          "captureMode": r.get("captureMode", ""),
                          "wireHashVerifiable": r.get("wireHashVerifiable", True)}
                         for r in load_seeds().values()],
    }

    out = d / "site.js"
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    out.write_text("// GENERATED by msl/sitegen.py — do not edit by hand.\n"
                   f"// cycle {rep.cycle} @ {now}\n"
                   "window.MSLDATA = " + body + ";\n", encoding="utf-8")
    return out


def _version() -> str:
    try:
        from . import __version__
        return __version__
    except Exception:  # noqa: BLE001
        return "0.1.0"
