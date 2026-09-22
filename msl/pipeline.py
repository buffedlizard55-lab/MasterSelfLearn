"""The cycle: discover → collect → verify → reason → compete → learn → publish.

``run_cycle`` is the whole engine.  It is idempotent-ish by construction (the
ledger is append-only and every stage recomputes from it), it never raises to the
caller — a failed stage becomes an irregularity and the cycle still publishes —
and it never prompts for input.

Offline mode (``--offline`` / ``MSL_OFFLINE=1``) runs the identical pipeline
against the hashed seed captures in ``data/seed/`` with no network at all.  That
is what the test suite exercises, and it is why the tests are deterministic.
"""
from __future__ import annotations

import json
import pathlib
import re
import time
import traceback
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from . import config, tasks as taskmod
from .adapters import ExtractResult, adapter_for
from .evidence import Ledger, RejectedClaim
from .http import FetchResult, FetchStats, fetch
from .ideas import Idea, synthesize
from .irregularities import CRITICAL, INFO, WARN, Register
from .learn import (derive_lessons, empty_memory, load as load_memory, record_cycle,
                    save as save_memory, update_source_reliability, update_topic_interest)
from .reason import derive, recheck_derived
from .retractions import RETRACTIONS
from .sentences import DEFECTS, find_defects
from .sources import BY_ID, REGISTRY
from .strategies import (Context, Forecast, issue, leaderboard, score, tracked_changes,
                         tracked_metrics, update_weights)
from .topics import (FAMILIES, FAMILY_BY_SLUG, STATUS_ACTIVE, STATUS_BLOCKED,
                     STATUS_CANDIDATE, STATUS_RETIRED, Library, build_interest_profile)


@dataclass
class CycleReport:
    cycle: int = 0
    at: str = ""
    ok: bool = True
    fetches: int = 0
    fetch_ok: int = 0
    fetch_failed: int = 0
    #: Facts projected out of the payloads this cycle.  ``None`` on a republish of a
    #: row that predates this field: the cycle extracted 680 facts and the row has no
    #: record of it, so the docs must say "not recorded" rather than "0".
    facts: Optional[int] = None
    claims_new: int = 0
    claims_total: int = 0
    claims_rejected: int = 0
    #: derivations produced *this cycle* (a delta; goes in STATUS.md's
    #: "Derived / rechecked / drifted" row)
    derived: int = 0
    #: derived claims currently *in the ledger* (a total; it is one half of the
    #: "captured vs derived" breakdown of `claims_total`, so it must be a total)
    derived_total: int = 0
    #: ``negative`` claims currently in the ledger: proof of absence.  A separate
    #: kind from captured, so the captured/derived breakdown must subtract it.
    negative_total: int = 0
    rechecks: int = 0
    not_recheckable: int = 0
    drift: int = 0
    topics_total: int = 0
    new_topics: int = 0
    retired_topics: int = 0
    insights: int = 0
    forecasts_issued: int = 0
    forecasts_scored: int = 0
    ideas: int = 0
    ideas_promoted: int = 0
    #: Reads the plan asked for, and how many the per-cycle cap refused.  A task the
    #: cap drops is work this engine decided not to do, so it is published rather
    #: than left to look like a plan that was exactly this size.  ``None`` means the
    #: cycle row does not record it — which is not the same as zero, and a republish
    #: must not turn "not recorded" into a number.
    tasks_planned: Optional[int] = None
    tasks_dropped: Optional[int] = None
    #: tracked wiki topics whose recorded title is not a title (it starts lower-case,
    #: which MediaWiki never produces).  Nothing is read from such a topic.
    wiki_titles_skipped: int = 0
    #: forecasts issued but still waiting for an observation, and forecasts that can
    #: never be scored because their metric stopped being observed.
    forecasts_pending: Optional[int] = None
    forecasts_abandoned: Optional[int] = None
    #: pending forecasts dropped by the size cap rather than by staleness.  Both are
    #: reported: a forecast that disappears without a word is a result nobody checked.
    forecasts_dropped_pending: Optional[int] = None
    irregularities_open: int = 0
    irregularities_new: int = 0
    net: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    duration_ms: int = 0
    mode: str = ""

    def summary(self) -> Dict[str, Any]:
        return {
            "cycle": self.cycle, "at": self.at, "ok": self.ok, "mode": self.mode,
            "facts": self.facts,
            "claimsTotal": self.claims_total, "claimsNew": self.claims_new,
            "claimsRejected": self.claims_rejected, "derived": self.derived,
            "derivedTotal": self.derived_total, "negativeClaims": self.negative_total,
            "rechecks": self.rechecks, "notRecheckable": self.not_recheckable,
            "drift": self.drift,
            "topicsTotal": self.topics_total, "newTopics": self.new_topics,
            "tasksPlanned": self.tasks_planned, "tasksDropped": self.tasks_dropped,
            "wikiTitlesSkipped": self.wiki_titles_skipped,
            "forecastsIssued": self.forecasts_issued,
            "forecastsScored": self.forecasts_scored,
            "forecastsPending": self.forecasts_pending,
            "forecastsAbandoned": self.forecasts_abandoned,
            "forecastsDroppedByCap": self.forecasts_dropped_pending,
            "ideas": self.ideas, "ideasPromoted": self.ideas_promoted,
            "insights": self.insights,
            "irregularitiesOpen": self.irregularities_open,
            "irregularitiesNew": self.irregularities_new,
            "fetches": self.fetches, "fetchOk": self.fetch_ok,
            "fetchFailed": self.fetch_failed, "errors": self.errors,
            "durationMs": self.duration_ms, "net": self.net,
        }

    def auto_counts(self) -> Dict[str, Any]:
        """The machine-regenerated counts block.  Never hand-edited."""
        return {
            "generatedAt": self.at,
            "cycle": self.cycle,
            "claims": self.claims_total,
            "claimsNewThisCycle": self.claims_new,
            "claimsRejectedByGate": self.claims_rejected,
            # A breakdown of `claims` into captured vs derived must use ledger
            # TOTALS.  This used to be `self.derived` — the count produced this
            # cycle — so the README published the cycle delta as if it were the
            # ledger's derived total and silently mislabelled every older derived
            # claim as "captured from live payloads".  With 8,618 claims it
            # reported 8,312 captured / 306 derived when the ledger actually held
            # 5,914 / 2,704.
            "derivedClaims": self.derived_total,
            # `negative` is a claim kind of its own — proof that something does not
            # exist, e.g. "this repository publishes no release" — and it is neither
            # captured nor derived.  Published separately because the breakdown in
            # README.md is rendered as a remainder, and until this existed the
            # remainder silently counted negative claims as captured readings.
            "negativeClaims": self.negative_total,
            "derivedThisCycle": self.derived,
            "derivedRechecks": self.rechecks,
            "derivedNotRecheckable": self.not_recheckable,
            "derivedDrifts": self.drift,
            "topics": self.topics_total,
            "newTopics": self.new_topics,
            "insights": self.insights,
            "tasksPlanned": self.tasks_planned,
            "tasksDroppedByCap": self.tasks_dropped,
            "wikiTitlesSkipped": self.wiki_titles_skipped,
            "forecastsIssued": self.forecasts_issued,
            "forecastsScored": self.forecasts_scored,
            "forecastsPending": self.forecasts_pending,
            "forecastsAbandoned": self.forecasts_abandoned,
            "forecastsDroppedByCap": self.forecasts_dropped_pending,
            "ideas": self.ideas,
            "ideasPromoted": self.ideas_promoted,
            "irregularitiesOpen": self.irregularities_open,
            "irregularitiesNew": self.irregularities_new,
            "sourcesRegistered": len(REGISTRY),
            "sourcesVerified": sum(1 for s in REGISTRY if s.status == "verified-live-read"),
            "sourcesBlocked": sum(1 for s in REGISTRY if s.status == "blocked"),
            # Reported separately because "not verified" and "broken" are
            # different claims.  A source here has simply never been read by a
            # recorded probe — which says nothing about whether it works.
            "sourcesNeverRead": sum(1 for s in REGISTRY if s.status == "registered"),
            "fetches": self.fetches, "fetchOk": self.fetch_ok,
            "fetchFailed": self.fetch_failed, "bytesIn": self.net.get("bytesIn", 0),
        }


# --------------------------------------------------------------------------- #
# seed handling
# --------------------------------------------------------------------------- #
def load_seeds(seed_dir: Optional[pathlib.Path] = None) -> Dict[str, Dict[str, Any]]:
    """URL → recorded seed capture.  Used for bootstrap and for offline runs."""
    d = pathlib.Path(seed_dir or config.SEED)
    out: Dict[str, Dict[str, Any]] = {}
    if not d.exists():
        return out
    for p in sorted(d.glob("*.json")):
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        url = rec.get("url")
        if url:
            rec["_file"] = p.name
            out[url] = rec
    return out


def seed_plan(seeds: Dict[str, Dict[str, Any]]) -> List[taskmod.Task]:
    """Turn the seed captures into tasks so offline runs exercise the real path."""
    out: List[taskmod.Task] = []
    for url, rec in seeds.items():
        sid = _source_for_url(url)
        if sid is None:
            continue
        topic = "source-health"
        if BY_ID[sid].topics:
            topic = BY_ID[sid].topics[0]
        ctx: Dict[str, Any] = {"topic": topic, "source": sid}
        if "search/repositories" in url:
            q = urllib.parse.unquote_plus(url.split("q=", 1)[-1].split("&")[0])
            ctx["query"] = q
            ctx["query_label"] = f"the seeded GitHub query “{q}”"
        if "federalregister.gov/api/v1/documents" in url and "conditions%5Bterm%5D=" in url:
            ctx["term"] = urllib.parse.unquote_plus(
                url.split("conditions%5Bterm%5D=", 1)[-1].split("&")[0])
        out.append(taskmod.Task(sid, url, sid, topic, "seed", ctx,
                                accepts=BY_ID[sid].accepts))
    return out


#: URL shapes that identify a source whose reads are not just its probe URL: another
#: package on PyPI, another search on GitHub, another window on USGS.
_URL_VARIANTS: List[Tuple[str, str]] = [
    ("api.github.com/search/repositories", "github_search"),
    ("api.github.com/users/", "github_repos"),
    ("pypi.org/pypi/", "pypi_json"),
    ("registry.npmjs.org", "npm_registry"),
    ("wikimedia.org/api/rest_v1/metrics/pageviews", "wikimedia_pageviews"),
    ("federalregister.gov/api/v1/documents", "federal_register"),
    ("earthquake.usgs.gov/fdsnws/event", "usgs_fdsn"),
    ("hacker-news.firebaseio.com", "hn_firebase"),
]


def _url_rules() -> List[Tuple[str, str]]:
    """Variant shapes first, then every registered source's own probe URL.

    The registry-derived half matters more than it looks: this function is what turns
    a stored capture into an offline task, and a URL it does not recognise is a read
    that disappears without a message (``seed_plan`` skips it).  Twenty of the thirty
    probe URLs used to fall through here — every arXiv, PubMed, Crossref, OpenAlex,
    NWS, World Bank, ECB, SEC, BLS, Census, Europe PMC, Kalshi, MLB, NHL and NBA
    read — so a capture of any of them would have been silently dropped.  Longest
    base first, so ``/releases`` is decided before the repository URL it sits under.
    """
    rules = list(_URL_VARIANTS)
    derived = []
    for s in REGISTRY:
        base = s.probe_url.split("?", 1)[0]
        if base:
            derived.append((base, s.id))
    derived.sort(key=lambda x: -len(x[0]))
    rules.extend(derived)
    return rules


_URL_RULES: List[Tuple[str, str]] = _url_rules()


def _source_for_url(url: str) -> Optional[str]:
    # /releases has to be decided before the bare /repos/ rule, or every release read
    # would be attributed to the single-repository endpoint.
    if "api.github.com/repos/" in url:
        return "github_releases" if "/releases" in url else "github_repo"
    for needle, sid in _URL_RULES:
        if needle in url:
            return sid
    return None


#: Query parameters that identify *what was asked for*, as opposed to how to answer
#: it.  Every read carries these into its adapter context so the resulting field name
#: and the published sentence describe the request the URL actually made.  Without
#: this a probe read published "GitHub Search reports 3,667,127 repositories
#: matching ." under the field ``github.total_count[]``, and a Nominatim answer said
#: "1 place result(s) for the query" with the field ``nominatim.results[?]``.
#: Mapped name → context key; a task may still set the key itself, and then its value
#: wins because the plan knows the label a human wants to read.
_URL_CONTEXT_PARAMS: Dict[str, str] = {
    "q": "query", "query": "query", "area": "area", "starttime": "starttime",
    "endtime": "endtime", "minmagnitude": "minmagnitude",
    "indicator": "indicator", "series": "series",
}


def url_context(url: str) -> Dict[str, str]:
    """Identifying parameters of a read, taken from the URL that will be read."""
    out: Dict[str, str] = {}
    split = urllib.parse.urlsplit(url or "")
    for key, value in urllib.parse.parse_qsl(split.query, keep_blank_values=False):
        target = _URL_CONTEXT_PARAMS.get(key)
        if target and value:
            out[target] = value
    # ``conditions[term]`` is how the Federal Register spells "full-text search".
    m = re.search(r"[?&]conditions(?:%5B|\[)term(?:%5D|\])=([^&]+)", url or "")
    if m and "term" not in out:
        out["term"] = urllib.parse.unquote_plus(m.group(1))
    # /repos/{owner}/{repo}[/releases] — the subject lives in the path, not the query.
    m = re.match(r"^https?://api\.github\.com/repos/([^/]+/[^/]+)(?:/|$)", url or "")
    if m:
        out.setdefault("repo", m.group(1))
    return out


def task_context(task: Any) -> Dict[str, Any]:
    """The adapter context for a task: what the plan said, completed by the URL."""
    ctx: Dict[str, Any] = dict(task.ctx or {})
    for key, value in url_context(task.url).items():
        ctx.setdefault(key, value)
    return ctx


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def run_cycle(offline: bool = False, max_tasks: Optional[int] = None,
              publish: bool = True, data_dir: Optional[pathlib.Path] = None,
              now_override: Optional[str] = None,
              seed_dir: Optional[pathlib.Path] = None,
              docs_dir: Optional[pathlib.Path] = None) -> CycleReport:
    t0 = time.monotonic()
    rep = CycleReport()
    rep.mode = "offline-fixtures" if offline else config.runtime_mode()
    now = now_override or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rep.at = now

    d = pathlib.Path(data_dir or config.DATA)
    d.mkdir(parents=True, exist_ok=True)
    ledger = Ledger(d)
    library = Library(d)
    register = Register(d)
    memory = load_memory(d)
    cycle = int(memory.get("cyclesRun", 0)) + 1
    rep.cycle = cycle
    stats = FetchStats()

    # dates for windowed queries
    end_dt = datetime.strptime(now[:10], "%Y-%m-%d")
    start_dt = end_dt - timedelta(days=7)
    end_day = start_dt.strftime("%Y%m%d")      # pageviews lag ~2 days; stay inside the window
    start_day = (start_dt - timedelta(days=6)).strftime("%Y%m%d")
    window_label = f"{(start_dt - timedelta(days=6)).strftime('%Y-%m-%d')} to {start_dt.strftime('%Y-%m-%d')}"

    # ---------------------------------------------------------------- seed the library
    _seed_library(library, cycle, now, d, register)

    # ---------------------------------------------------------------- plan
    # Seeds live beside the data they bootstrap.  Fall back to the repository's
    # own corpus only for the *default* data dir — an explicit data_dir (tests,
    # dry runs) must not be silently rescued by seeds it does not own, or an
    # isolated run cannot prove what happens with nothing to read.
    seeds = load_seeds(seed_dir or (d / "seed"))
    if not seeds and seed_dir is None and d.resolve() == config.DATA.resolve():
        seeds = load_seeds()
    plan_stats: Dict[str, int] = {}
    if offline:
        plan = seed_plan(seeds)
    else:
        plan = taskmod.build_plan(library, now, start_day, end_day, window_label,
                                  stats=plan_stats)
    rep.tasks_planned = plan_stats.get("planned", len(plan))
    rep.tasks_dropped = plan_stats.get("dropped", 0)
    rep.wiki_titles_skipped = plan_stats.get("wikiTitlesSkipped", 0)
    if max_tasks:
        plan = plan[:max_tasks]

    # ---------------------------------------------------------------- collect + verify
    outcomes: Dict[str, bool] = {}
    shape_problems: List[str] = []
    fetch_log: List[Dict[str, Any]] = []
    gh_totals: List[Tuple[int, str]] = []
    discovery_budget = [config.MAX_NEW_TOPICS_PER_CYCLE]   # shared across all tasks
    # Sources this runner could not reach at the TLS layer.  That is a fact about
    # the runner, not about the source, so they are collected and reported as ONE
    # aggregated finding instead of blocking 22 healthy endpoints and minting 38
    # near-identical irregularities — which is both a false claim about those
    # services and the register spam AGENTS.md §7 warns against.
    egress_failures: List[str] = []
    # Every read this cycle, for the shared health ledger.  Collecting them here
    # and writing once at the end keeps the ledger a single record of "last
    # recorded read per source" instead of two files that disagree.
    cycle_reads: List[Tuple[Any, Any, str, bool]] = []

    for task in plan:
        # An unattended loop cannot afford to die.  Anything unexpected on one
        # task is recorded as an irregularity and the cycle carries on; the
        # failure is visible on the site instead of being a dead cron job.
        try:
            src = BY_ID.get(task.source_id)
            adapter = adapter_for(task.adapter)
            # What was asked for comes from the URL that is about to be read as well
            # as from the plan: a field name and a published sentence must describe
            # the request this read actually made.
            ctx = task_context(task)
            if adapter is None:
                register.add(WARN, f"No adapter registered for source {task.source_id}",
                             f"The task plan produced a read for {task.source_id} but no "
                             f"adapter can project its payload, so the read was skipped "
                             f"rather than stored uninterpreted.", cycle, now,
                             repro=f"grep -n {task.source_id!r} msl/adapters.py",
                             source_id=task.source_id)
                continue

            rec = seeds.get(task.url)
            result: Optional[FetchResult] = None
            payload: Any = None
            capture_mode = "pipeline"
            wire_verifiable = True
            used_seed = False

            if offline and rec is not None:
                payload = rec.get("projection")
                capture_mode = "offline-fixture"
                wire_verifiable = bool(rec.get("wireHashVerifiable", True))
                used_seed = True
                outcomes[task.source_id] = True
            else:
                result = fetch(task.url, accept=task.accepts)
                stats.record(result)
                if src is not None:
                    cycle_reads.append((src, result, now,
                                        (not result.ok)
                                        and result.error_kind == "EgressBlocked"))
                if result.ok:
                    try:
                        if src and src.payload_kind == "atom":
                            payload = result.body          # adapters parse the XML themselves
                        else:
                            payload = result.json()
                    except (json.JSONDecodeError, ValueError) as e:
                        payload = None
                        shape_problems.append(f"{task.source_id}: body was not parseable "
                                              f"({type(e).__name__}: {e}) for {task.url}")
                else:
                    outcomes[task.source_id] = False
                    if rec is not None:
                        # bootstrap: use the hashed seed capture and say so loudly
                        payload = rec.get("projection")
                        capture_mode = "seed-fallback"
                        wire_verifiable = False
                        used_seed = True
                        register.add(WARN, f"{task.source_id} unreadable; seed capture substituted",
                                     f"{result.describe_error()} on GET {task.url}. The recorded "
                                     f"seed capture from {rec.get('capturedAt')} was used instead so "
                                     f"the cycle still produces claims, and every claim from it is "
                                     f"marked captureMode=seed-fallback. This is a substitute, not a "
                                     f"fresh read.", cycle, now, repro=f"curl -sS -o /dev/null -w '%{{http_code}}' '{task.url}'",
                                     source_id=task.source_id, topic=task.topic)
                if result.ok or used_seed:
                    outcomes.setdefault(task.source_id, result.ok if result else True)

            if payload is None:
                if result is not None and not result.ok:
                    if result.error_kind == "EgressBlocked":
                        # This runner could not open a TLS session to the host, so
                        # nothing was learned about the source.  Marking it blocked
                        # would publish "this service is down" for a service that
                        # may be perfectly healthy, and consecutive_failures feeds
                        # the CRITICAL escalation, so an egress blip would
                        # manufacture critical findings about other people's APIs.
                        if task.source_id not in egress_failures:
                            egress_failures.append(task.source_id)
                        continue
                    register.add(CRITICAL if (src and src.consecutive_failures >=
                                              config.SOURCE_FAILS_BEFORE_CRITICAL) else WARN,
                                 f"{task.source_id} could not be read",
                                 f"{result.describe_error()} on GET {task.url} after "
                                 f"{result.attempts} attempt(s). No claim was produced and no "
                                 f"substitute value was invented.", cycle, now,
                                 repro=f"curl -sS -o /dev/null -w '%{{http_code}}\\n' '{task.url}'",
                                 source_id=task.source_id, topic=task.topic)
                    if src is not None:
                        src.consecutive_failures += 1
                        src.status = "blocked"
                        src.last_error = result.describe_error()
                        src.last_read_at = now
                        src.last_status = result.status
                    if result.rate_limited:
                        register.add(WARN, f"{task.source_id} rate-limited this cycle",
                                     f"HTTP {result.status} on {task.url}. The engine backs off "
                                     f"rather than retrying, and produces no claim from this "
                                     f"source this cycle.", cycle, now,
                                     repro=f"curl -sSI '{task.url}' | head -5",
                                     source_id=task.source_id)
                continue

            # record the read
            ev = ledger.add_evidence(
                source_id=task.source_id, url=task.url,
                captured_at=(rec.get("capturedAt", now) if used_seed else now),
                status=(rec.get("httpStatus") if used_seed else (result.status if result else 200)),
                body=(b"" if used_seed or payload is None or not isinstance(payload, bytes)
                      else payload),
                error=None, error_kind=None,
                elapsed_ms=(result.elapsed_ms if result else 0),
                attempts=(result.attempts if result else 1),
                rate_limited=bool(result.rate_limited if result else False),
                capture_mode=capture_mode, wire_hash_verifiable=wire_verifiable,
                projection=(None if isinstance(payload, bytes) else payload),
                note=(f"seed capture {rec.get('_file')}" if used_seed else ""))

            if src is not None and result is not None and result.ok:
                src.consecutive_failures = 0
                src.status = "verified-live-read"
                src.live_reads += 1
                src.last_read_at = now
                src.last_status = result.status
                src.last_error = ""

            # extract
            try:
                xr: ExtractResult = adapter(payload, ctx)
            except Exception as e:  # noqa: BLE001
                xr = ExtractResult()
                shape_problems.append(f"{task.source_id}: adapter raised "
                                      f"{type(e).__name__}: {e} for {task.url}")
                register.add(WARN, f"{task.source_id} adapter failed",
                             f"The adapter raised {type(e).__name__}: {e} while projecting "
                             f"{task.url}. The payload shape probably changed. Zero facts were "
                             f"produced; nothing was guessed.", cycle, now,
                             repro=f"python3 -m msl.cli probe --only {task.source_id}",
                             source_id=task.source_id, topic=task.topic)

            for prob in xr.problems:
                shape_problems.append(f"{task.source_id}: {prob}")
                register.add(WARN, f"{task.source_id} payload shape problem",
                             f"{prob}  Zero facts were taken from the affected part of the "
                             f"payload.", cycle, now,
                             repro=f"curl -sS '{task.url}' | head -c 400",
                             source_id=task.source_id, topic=task.topic)

            rep.facts = (rep.facts or 0) + len(xr.facts)
            for f in xr.facts:
                c = ledger.try_accept(f.topic, f.kind, f.statement, task.source_id,
                                      ev.captured_at, cycle, value=f.value, unit=f.unit,
                                      field=f.field, evidence=[ev.id], url=task.url,
                                      tags=f.tags)
                if c is not None:
                    rep.claims_new += 1
                    library.touch(f.topic, now, cycle, claims_delta=1)
                    # credit the entity topics this fact is evidence for, so a
                    # discovered topic accumulates real support instead of signals only
                    for slug in f.entities:
                        if library.get(slug) is not None:
                            library.touch(slug, now, cycle, claims_delta=1)
                if f.field == "github.total_count" and isinstance(f.value, int):
                    gh_totals.append((f.value, task.url))
            # discovery seeds
            _discover(library, xr.entities, cycle, now, task.source_id, task.url,
                      register, discovery_budget, task.topic)

            fetch_log.append({"sourceId": task.source_id, "url": task.url,
                              "facts": len(xr.facts), "evidenceId": ev.id,
                              "captureMode": capture_mode,
                              "status": ev.status, "problems": len(xr.problems)})

        except Exception as e:  # noqa: BLE001
            rep.errors.append(f"{task.source_id}: {type(e).__name__}: {e}")
            register.add(CRITICAL, f"{task.source_id} raised an unhandled error",
                         f"{type(e).__name__}: {e} while processing {task.url}. The "
                         f"task was abandoned and the rest of the cycle continued. "
                         f"No claim was produced and none was guessed.", cycle, now,
                         repro=f"python3 -m msl.cli cycle --offline  # then read the "
                               f"irregularity register",
                         source_id=task.source_id, topic=task.topic)
            continue
    rep.fetches = len(fetch_log)
    # count what actually produced an evidence row, not what was attempted
    rep.fetch_ok = len(fetch_log)
    rep.fetch_failed = len(plan) - len(fetch_log)
    if not offline:
        rep.fetch_ok = stats.ok
        rep.fetch_failed = stats.failed
    rep.net = stats.as_dict()

    # One aggregated finding for a wall of egress failures, never N per-source ones.
    # The tell that it is an egress policy rather than 22 simultaneous outages is
    # uniformity: every failure is the same TLS-layer error, and some other host
    # in the same cycle was read successfully.
    if egress_failures:
        hosts = sorted({urllib.parse.urlsplit(BY_ID[s].probe_url).netloc
                        for s in egress_failures if s in BY_ID})
        tell = ("Some other host was read successfully in this same cycle, which is "
                "what distinguishes an egress allowlist from an outage."
                if stats.ok else
                "Nothing at all was read this cycle, so the wall may be total.")
        register.add(
            WARN, "This runner could not egress to some sources",
            f"{len(egress_failures)} source(s) could not be reached because the TLS "
            f"session was closed before any HTTP status arrived: "
            f"{', '.join(egress_failures)}. Hosts: {', '.join(hosts)}. "
            f"This is a property of the machine running the cycle, not of those "
            f"services, so NONE of them is marked blocked and no claim is made that "
            f"any of them is down. No claim was produced from them and no substitute "
            f"value was invented. {tell}",
            cycle, now,
            repro=(f"python3 tools/probe_sources.py {' '.join(egress_failures[:4])}"
                   "   # from a runner with unrestricted egress"),
            source_id=egress_failures[0])

    # GitHub's search index moves while you watch: two reads of the same query in one
    # cycle can legitimately disagree.  That is worth recording, not hiding.
    by_query: Dict[str, List[int]] = {}
    for v, u in gh_totals:
        by_query.setdefault(u.split("q=", 1)[-1].split("&")[0], []).append(v)
    for q, vals in by_query.items():
        if len(set(vals)) > 1:
            register.add(INFO, "GitHub search total_count moved within one cycle",
                         f"The same query “{q}” returned total_count values "
                         f"{sorted(set(vals))} inside a single cycle. GitHub's search index "
                         f"is eventually consistent, so a quoted total is a point-in-time "
                         f"reading and not a stable fact. Both values are in the ledger.",
                         cycle, now,
                         repro=f"curl -sS 'https://api.github.com/search/repositories?q={q}&per_page=1' | grep total_count",
                         source_id="github_search", topic="open-source-momentum")

    for prob in shape_problems[:20]:
        pass  # already registered individually above

    # ---------------------------------------------------------------- reason
    seq = [0]
    try:
        rr = derive(ledger, cycle, now, seq)
        rep.derived = rr.derived
        rep.insights = len(rr.insights)
        rc = recheck_derived(ledger, cycle, now)
        rep.rechecks = rc.rechecks
        rep.not_recheckable = rc.not_recheckable
        rep.drift = len(rc.drift)
        if rc.not_recheckable:
            register.add(INFO, "Some derived claims cannot be re-checked",
                         f"{rc.not_recheckable} derived claim(s) use a formula whose value "
                         f"depends on the wall clock at read time — a repository's "
                         f"stars-per-day, for example, has 'now' in its denominator. They "
                         f"are counted as NOT RECHECKED rather than as passing, because a "
                         f"check that cannot be repeated is not a check.", cycle, now,
                         repro="python3 -m msl.cli verify-claims", topic="derived",
                         standing=True)
        for dft in rc.drift:
            register.add(WARN, f"Derived claim {dft.get('claimId')} no longer recomputes",
                         f"Field {dft.get('field')}: published value {dft.get('old')!r}, "
                         f"recomputed {dft.get('new')!r} using formula "
                         f"{dft.get('formula','?')} over inputs {dft.get('inputs')}. "
                         f"Either an input moved or the arithmetic was wrong; the site "
                         f"shows both numbers.", cycle, now,
                         repro="python3 -m msl.cli verify-claims", topic="derived")
    except Exception as e:  # noqa: BLE001
        rep.errors.append(f"reason: {type(e).__name__}: {e}")
        rep.ok = False
        register.add(CRITICAL, "The reasoning stage raised",
                     f"{type(e).__name__}: {e}\n\n{traceback.format_exc()[-1500:]}",
                     cycle, now, repro="python3 -m msl.cli cycle --offline")

    # ---------------------------------------------------------------- compete
    metrics, topic_of = tracked_metrics(ledger)
    changes, change_topic_of, change_kind = tracked_changes(ledger)
    ctx = Context(ledger=ledger, cycle=cycle, now=now, memory=memory,
                  metrics=metrics, topic_of=topic_of, changes=changes,
                  change_topic_of=change_topic_of, change_kind=change_kind)
    try:
        forecasts = _load_forecasts(d)
        scored_before = sum(1 for f in forecasts if f.scored)
        score(forecasts, ctx)
        rep.forecasts_scored = sum(1 for f in forecasts if f.scored) - scored_before
        lb = leaderboard(forecasts)
        new = issue(ctx)
        rep.forecasts_issued = len(new)
        forecasts.extend(new)
        memory = update_weights(lb, memory)
        kept = _save_forecasts(d, forecasts, cycle,
                               set(metrics) | set(changes))
        rep.forecasts_pending = kept["pending"]
        rep.forecasts_abandoned = kept["abandoned"]
        rep.forecasts_dropped_pending = kept["pendingDropped"]
    except Exception as e:  # noqa: BLE001
        rep.errors.append(f"compete: {type(e).__name__}: {e}")
        rep.ok = False
        lb = {"ranked": [], "unranked": [], "all": [], "nullAccuracy": None,
              "nullScored": 0, "qualification": {}}
        register.add(CRITICAL, "The competition stage raised",
                     f"{type(e).__name__}: {e}\n\n{traceback.format_exc()[-1500:]}",
                     cycle, now, repro="python3 -m msl.cli cycle --offline")

    # ---------------------------------------------------------------- ideas
    blocked = {s.id for s in REGISTRY if s.status == "blocked"}
    try:
        prev_ideas = _load_ideas(d)
        ir = synthesize(ledger, cycle, now, prev_ideas,
                        rr.insights if 'rr' in dir() else [], blocked)
        rep.ideas = len(ir.ideas)
        rep.ideas_promoted = ir.promoted
        _save_ideas(d, ir.ideas)
    except Exception as e:  # noqa: BLE001
        rep.errors.append(f"ideas: {type(e).__name__}: {e}")
        rep.ok = False
        ir = None
        register.add(CRITICAL, "The idea-synthesis stage raised",
                     f"{type(e).__name__}: {e}\n\n{traceback.format_exc()[-1500:]}",
                     cycle, now, repro="python3 -m msl.cli cycle --offline")

    # ---------------------------------------------------------------- learn
    memory = update_source_reliability(memory, outcomes)
    signals = {t.slug: t.signals for t in library.topics.values()}
    memory = update_topic_interest(memory, signals, cycle)
    profile = build_interest_profile(d / "seed")
    for t in library.topics.values():
        fam_score = (profile.get("categories") or {}).get(t.family, 0.0) if profile.get("available") else 0.0
        t.interest_score = round(t.signals * 0.6 + fam_score * 0.4, 4)

    retired = library.retire_stale(cycle)
    rep.retired_topics = len(retired)
    rep.topics_total = len(library.topics)
    rep.new_topics = sum(1 for t in library.topics.values() if t.created_cycle == cycle)
    rep.claims_total = len(ledger.claims)
    rep.claims_rejected = len(ledger.rejections)
    rep.derived_total = sum(1 for c in ledger.claims if c.kind == "derived")
    rep.negative_total = sum(1 for c in ledger.claims if c.kind == "negative")

    # ---------------------------------------------------------------- irregularities
    _auto_flags(register, cycle, now, ledger, library, lb, rep, profile,
                len(plan))
    register.register_standing(cycle, now)
    seen_fps = {i.fingerprint for i in register.items.values()
                if i.last_seen_cycle == cycle}
    register.resolve_absent(seen_fps, cycle)
    counts = register.counts()
    rep.irregularities_open = counts.get("open", 0)
    rep.irregularities_new = sum(1 for i in register.items.values()
                                 if i.first_seen_cycle == cycle)

    # Measured HERE, before the cycle row is written, so the recorded row, the site
    # and the docs all quote one number.  The assignment used to sit after the row
    # was appended, so all fourteen recorded rows say durationMs=0 while the docs
    # published a real duration — two numbers for one cycle.  The writing and
    # rendering that follows is excluded from the figure, which is why this is a
    # lower bound on the wall clock and not a claim about it.
    rep.duration_ms = int((time.monotonic() - t0) * 1000)

    memory = derive_lessons_and_record(memory, ledger, library,
                                       ir.ideas if ir else [], cycle, now, rep)

    # ---------------------------------------------------------------- persist
    library.save(now)
    save_memory(memory, d)
    register.save(now, cycle)
    _append_jsonl(d / "cycles.jsonl", {**rep.summary(),
                                       "autoCounts": rep.auto_counts()})
    _write_json(d / "insights.json", {"generatedAt": now, "cycle": cycle,
                                      "items": [i.as_dict() for i in (rr.insights if 'rr' in dir() else [])]})
    _write_json(d / "leaderboard.json", {"generatedAt": now, "cycle": cycle, **lb})
    _write_json(d / "sources.json", {"generatedAt": now, "cycle": cycle,
                                     "sources": [s.as_dict() for s in REGISTRY],
                                     "keyedExcluded": _keyed_excluded(),
                                     "categoriesWithoutSource": _categories_without_source()})
    _write_json(d / "profile.json", profile)

    # One health ledger, two writers.  The cycle folds its reads in here so the
    # Sources page cannot show a probe table that contradicts the registry table
    # above it.  apply=False: the cycle already folded these results into the
    # registry inline, and re-applying would double-count live_reads and
    # consecutive_failures.  Offline runs read fixtures, not endpoints, so they
    # record nothing — a fixture is not evidence that a service is reachable.
    if cycle_reads and not offline:
        try:
            from .probe import record_reads
            # Pass the cycle's own data dir: the default is config.DATA, which
            # would make every test and dry run write the repository's real
            # ledger instead of its own.
            record_reads(cycle_reads, path=d / "source_health.json",
                         mode=f"cycle-{cycle}", apply=False)
        except Exception as e:  # noqa: BLE001 - bookkeeping must not fail a cycle
            rep.errors.append(f"health ledger: {type(e).__name__}: {e}")

    if publish:
        try:
            from . import docs as docsgen
            from . import sitegen
            sitegen.render(d, now, rep, ledger, library, memory, register)
            docsgen.render_all(d, now, rep, ledger, library, memory, register, lb,
                           docs_dir=docs_dir)
        except Exception as e:  # noqa: BLE001
            rep.errors.append(f"publish: {type(e).__name__}: {e}")
            rep.ok = False
            traceback.print_exc()
    return rep


#: How a republish recovers each per-cycle number ``CycleReport.summary()`` writes:
#: ``_REPLAYED`` restores it from the recorded cycle row, ``RECOMPUTED`` rebuilds it
#: from the objects on disk.  A key in neither map is a number that silently becomes
#: 0 the next time the docs are rendered — which is how STATUS.md came to publish
#: "Facts extracted 0" and "Derived 0" for a cycle that extracted 680 facts and
#: derived 330 claims.  ``tests/test_pipeline.py`` asserts the union covers every
#: key ``summary()`` writes, so a new field cannot be added without deciding.
_REPLAYED: Dict[str, str] = {
    "claims_new": "claimsNew", "rechecks": "rechecks",
    "not_recheckable": "notRecheckable", "drift": "drift",
    "new_topics": "newTopics", "forecasts_issued": "forecastsIssued",
    "forecasts_scored": "forecastsScored", "irregularities_new": "irregularitiesNew",
    "fetches": "fetches", "fetch_ok": "fetchOk", "fetch_failed": "fetchFailed",
    "tasks_planned": "tasksPlanned", "tasks_dropped": "tasksDropped",
    "wiki_titles_skipped": "wikiTitlesSkipped",
    "forecasts_pending": "forecastsPending",
    "forecasts_abandoned": "forecastsAbandoned",
    "forecasts_dropped_pending": "forecastsDroppedByCap",
    "facts": "facts", "derived": "derived", "duration_ms": "durationMs",
    "ideas_promoted": "ideasPromoted",
}
#: ``ok`` and ``errors`` are replayed by hand inside republish (a bool and a list,
#: not counts) and count as covered here.
REPLAYED_CYCLE_KEYS = frozenset(list(_REPLAYED.values()) + ["ok", "errors"])
#: Cumulative state: recomputed from the ledger, the library and the register, so a
#: stale number cannot survive a corrected ledger.
RECOMPUTED_CYCLE_KEYS = frozenset({
    "at", "cycle", "mode", "net", "claimsTotal", "claimsRejected", "derivedTotal",
    "negativeClaims", "topicsTotal", "insights", "ideas", "irregularitiesOpen",
    "sourcesRegistered", "sourcesVerified", "sourcesBlocked", "sourcesNeverRead",
})


def republish(data_dir: Optional[pathlib.Path] = None,
              docs_dir: Optional[pathlib.Path] = None) -> CycleReport:
    """Re-render the site and docs from the state already on disk.

    No read, no new claim, no new cycle row.

    Two different kinds of number appear on the site and they must be sourced
    differently, which is where the first version of this function went wrong:

    * **Cumulative state** (claims in the ledger, topics in the library, open
      irregularities) is *recomputed* from the objects on disk.  Replaying a
      recorded figure for these would let a stale number survive a corrected
      ledger.
    * **Per-cycle deltas** (claims new *this* cycle, forecasts scored, drift
      found) cannot be recomputed after the fact, so they are *replayed* from
      the recorded cycle row — explicitly mapped, key by key.

    The mapping is explicit because ``CycleReport.summary()`` writes camelCase
    (``claimsTotal``) while the dataclass fields are snake_case
    (``claims_total``).  A first attempt used ``hasattr(rep, key)`` over the
    recorded dict, which matched almost nothing, so every cumulative figure
    silently fell back to its default and the regenerated README published
    "0 verified claims" and a negative claim delta.  A republish that prints
    confident wrong numbers is worse than no republish.
    """
    d = pathlib.Path(data_dir or config.DATA)
    ledger = Ledger(d)
    library = Library(d)
    register = Register(d)
    memory = load_memory(d)

    cycles: List[Dict[str, Any]] = []
    cp = d / "cycles.jsonl"
    if cp.exists():
        for line in cp.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    cycles.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    last = cycles[-1] if cycles else {}
    rep = CycleReport()
    rep.cycle = int(last.get("cycle", memory.get("cyclesRun", 0)))
    rep.at = last.get("at", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    rep.mode = last.get("mode", config.runtime_mode())
    rep.duration_ms = last.get("durationMs", 0)   # the last *cycle's* duration, replayed

    # --- replayed per-cycle deltas: explicit, never reflective -----------------
    for attr, key in _REPLAYED.items():
        if key in last:
            setattr(rep, attr, last[key])
    # `errors` is a list, not a count: a republished cycle that raised must keep
    # saying so, or the site's "the last cycle reported errors" note disappears
    # whenever the docs are re-rendered.
    if "errors" in last and isinstance(last["errors"], list):
        rep.errors = list(last["errors"])
    if "ok" in last:
        rep.ok = bool(last["ok"])
    if isinstance(last.get("net"), dict):
        rep.net = last["net"]

    # --- recomputed cumulative state: read from the objects on disk ------------
    rep.claims_total = len(ledger.claims)
    rep.claims_rejected = len(ledger.rejections)
    rep.topics_total = len(library.topics)
    rep.retired_topics = sum(1 for t in library.topics.values()
                             if t.status == STATUS_RETIRED)
    rep.derived_total = sum(1 for c in ledger.claims if c.kind == "derived")
    rep.negative_total = sum(1 for c in ledger.claims if c.kind == "negative")
    counts = register.counts()
    rep.irregularities_open = counts.get("open", 0)

    for name, attr, key in (("insights.json", "insights", "items"),
                            ("ideas.json", "ideas", "items")):
        doc = {}
        p = d / name
        if p.exists():
            try:
                doc = json.loads(p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                doc = {}
        setattr(rep, attr, len(doc.get(key, [])))

    from . import docs as docsgen
    from . import sitegen
    sitegen.render(d, rep.at, rep, ledger, library, memory, register)
    docsgen.render_all(d, rep.at, rep, ledger, library, memory, register,
                       _read_json_or_empty(d / "leaderboard.json"),
                       docs_dir=docs_dir)
    return rep


def _read_json_or_empty(p: pathlib.Path) -> Dict[str, Any]:
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def derive_lessons_and_record(memory, ledger, library, ideas, cycle, now, rep) -> Dict[str, Any]:
    memory["lessons"] = derive_lessons(memory, ledger, library, ideas)
    return record_cycle(memory, cycle, now, rep.summary())


# --------------------------------------------------------------------------- #
# discovery
# --------------------------------------------------------------------------- #
def _seed_library(library: Library, cycle: int, now: str, d: pathlib.Path,
                  register: Register) -> None:
    """Create one topic per family, on the first cycle only."""
    for fam in FAMILIES:
        if library.get(fam.slug) is None:
            t = library.ensure(fam.slug, fam.title, fam.slug, now, cycle,
                               origin="family-seed", status=STATUS_ACTIVE,
                               notes=fam.question)
            t.claims = 0
            if fam.blocked_reason:
                t.status = STATUS_BLOCKED
                t.notes = fam.blocked_reason
                register.add(INFO, f"“{fam.title}” has no source that can answer its question",
                             fam.blocked_reason, cycle, now,
                             repro=f"python3 -c \"from msl.topics import FAMILY_BY_SLUG; "
                                   f"print(FAMILY_BY_SLUG['{fam.slug}'].blocked_reason)\"",
                             topic=fam.slug, standing=True)


def _discover(library: Library, entities: List[tuple], cycle: int, now: str,
              source_id: str, url: str, register: Register,
              budget: Optional[List[int]] = None,
              family_hint: str = "") -> None:
    """Turn extracted entities into candidate topics.

    ``budget`` is a one-element list shared across every task in the cycle.  It
    used to be a local counter, which meant MAX_NEW_TOPICS_PER_CYCLE applied per
    task rather than per cycle and the library grew by dozens of topics a run.
    """
    if not entities:
        return
    agg: Dict[str, Tuple[str, float, str]] = {}
    for slug, title, weight, ent_url in entities:
        prev = agg.get(slug)
        # tuple is (title, weight, url) — compare weights, not urls
        if prev is None or weight > prev[1]:
            agg[slug] = (title, weight, ent_url)
    ranked = sorted(agg.items(), key=lambda kv: -kv[1][1])
    room = config.MAX_NEW_TOPICS_PER_CYCLE if budget is None else budget[0]
    for slug, (title, weight, ent_url) in ranked:
        if len(library.topics) >= config.MAX_TOPICS_TRACKED:
            break
        existing = library.get(slug)
        if existing is None:
            if room <= 0:
                continue
            room -= 1
            if budget is not None:
                budget[0] = room
            fam = family_hint if (family_hint in FAMILY_BY_SLUG) else _family_for(source_id)
            library.ensure(slug, title, fam, now, cycle, origin=f"discovery:{source_id}",
                           origin_url=ent_url, status=STATUS_CANDIDATE,
                           notes=f"Proposed from {source_id}; promoted to active at "
                                 f"{config.MIN_SIGNALS_TO_PROPOSE_TOPIC} signals.")
        else:
            library.ensure(slug, title, existing.family, now, cycle,
                           origin=existing.origin, origin_url=existing.origin_url)


def _family_for(source_id: str) -> str:
    for fam in FAMILIES:
        if source_id in fam.sources:
            return fam.slug
    return "open-source-momentum"


def _auto_flags(register: Register, cycle: int, now: str, ledger: Ledger,
                library: Library, lb: Dict[str, Any], rep: CycleReport,
                profile: Dict[str, Any], plan_size: int = 0) -> None:
    # Sentences a buggy template published.  The ledger keeps them, the template is
    # fixed, and this is the only place that keeps the old rows visible: one
    # aggregated finding per defect class, with a count computed from the ledger
    # rather than typed into the message.
    defects = find_defects(ledger.claims)
    by_id = {c.id: c for c in ledger.claims}
    for defect_id in sorted(defects):
        ids = defects[defect_id]
        spec = next(x for x in DEFECTS if x["id"] == defect_id)
        cycles_seen = [by_id[i].cycle for i in ids if i in by_id]
        span = (f"published in cycles {min(cycles_seen)}–{max(cycles_seen)}"
                if cycles_seen else "of unknown cycle")
        register.add(
            WARN, "Published sentences came from a template that is now fixed",
            f"Defect {defect_id} — {len(ids)} row(s), {span}. {spec['symptom']}  "
            f"Fix in place: {spec['fix']}  The ledger is append-only, so those rows "
            f"keep the wording they were published with; no new claim can be written "
            f"by that template, and the count in this message is recomputed from the "
            f"ledger every cycle rather than remembered.",
            cycle, now,
            repro=f"python3 -c \"from msl.evidence import Ledger; from msl.sentences "
                  f"import find_defects; print(len(find_defects(Ledger('data').claims)"
                  f".get('{defect_id}', [])))\"",
            topic="ledger", standing=True, fingerprint=defect_id)

    for rej in ledger.rejections:
        register.add(WARN, "The evidence gate rejected a claim",
                     f"{rej['reason']}  Rejected text: “{rej['statement']}”.  The claim was "
                     f"not published and no substitute was written.", cycle, now,
                     repro="python3 -m msl.cli gate-report",
                     source_id=rej.get("sourceId", ""), topic=rej.get("topic", ""))

    counts = ledger.topics_with_claims()
    unsupported = sorted(
        (t for slug, t in library.topics.items()
         if t.status not in (STATUS_RETIRED, STATUS_BLOCKED)
         and counts.get(slug, 0) == 0 and cycle - t.created_cycle >= 2),
        key=lambda t: t.created_cycle)
    if unsupported:
        names = ", ".join(t.slug for t in unsupported[:12])
        more = "" if len(unsupported) <= 12 else f" (+{len(unsupported) - 12} more)"
        register.add(WARN, "Topics with no verified claims behind them",
                     f"{len(unsupported)} tracked topic(s) were proposed at least two cycles "
                     f"ago and still have zero verified claims: {names}{more}.  They are "
                     f"listed as unsupported rather than described, and each will be retired "
                     f"after {config.CYCLES_BEFORE_RETIREMENT} cycles without a signal. If a "
                     f"topic matters, the fix is to register a source that can answer it — "
                     f"not to write prose about it.",
                     cycle, now,
                     repro="python3 -c \"import json;[print(t['slug']) for t in json.load(open('data/library.json'))['topics'] if t['claims']==0]\"",
                     topic="library")

    for row in lb.get("unranked", []):
        register.add(INFO, f"Persona {row['strategyId']} is UNRANKED",
                     f"{row['name']}: {row.get('unrankedReason','')}  It is excluded from the "
                     f"ranked table rather than shown at 0%, because a persona that has not "
                     f"been scored has not been beaten.", cycle, now,
                     repro="python3 -c \"import json;print(json.load(open('data/leaderboard.json'))['qualification'])\"",
                     topic="competition")

    for s in REGISTRY:
        if s.status == "registered":
            register.add(INFO, f"Source {s.id} has never been read",
                         f"{s.name} ({s.operator}) is registered with a documentation URL but "
                         f"no successful read has been recorded yet. No claim has been built "
                         f"from it. The next probe will either verify it or record why it "
                         f"failed.", cycle, now, repro=f"curl -sS -o /dev/null -w '%{{http_code}}\\n' '{s.probe_url}'",
                         # not standing: once the probe reads this source the entry
                         # stops recurring and resolve_absent() clears it
                         source_id=s.id, standing=False)
        if s.docs_note and "UNDOCUMENTED" in s.docs_note:
            register.add(INFO, f"{s.id} is an undocumented public endpoint",
                         f"{s.docs_note}  Claims built from it carry the same marker.",
                         cycle, now, repro=f"curl -sS -o /dev/null -w '%{{http_code}}\\n' '{s.probe_url}'",
                         source_id=s.id, standing=True)

    if profile.get("available") is False:
        register.add(WARN, "The interest profile could not be built",
                     f"{profile.get('reason','')}  Without the owner-corpus capture the engine "
                     f"cannot derive interest weights, so it uses signal counts alone. No "
                     f"profile was invented.", cycle, now,
                     repro="ls -l data/seed/owner_repos.json", topic="owner-corpus")

    for rt in RETRACTIONS:
        hits = sum(1 for c in ledger.claims if c.field.startswith(rt["fieldPrefix"]))
        if not hits:
            continue
        register.add(WARN, f"Retracted: {rt['fieldPrefix']}",
                     f"{hits} claim(s) in the append-only ledger match this retracted "
                     f"field prefix and are no longer published or reasoned from. "
                     f"{rt['reason']} Superseded by `{rt['supersededBy']}`. The rows are "
                     f"kept, with their hashes, because the ledger is a record and not a "
                     f"view; deleting them would make the original error unauditable. "
                     f"First seen cycle {rt['firstSeenCycle']}, corrected in cycle "
                     f"{rt['fixedInCycle']}.", cycle, now,
                     repro="grep -n '" + rt["fieldPrefix"] + "' data/claims.jsonl | head",
                     standing=True, fingerprint=rt["irregularity"])
    if rep.fetch_failed and rep.fetch_ok:
        register.add(WARN, f"{rep.fetch_failed} of {plan_size} planned reads failed",
                     f"{rep.fetch_failed} read(s) failed while {rep.fetch_ok} succeeded. Each "
                     f"failure is listed separately with its HTTP status or transport error and "
                     f"a reproduction command. A partial cycle is still published, but every "
                     f"figure that would have come from a failed source is absent rather than "
                     f"carried forward silently.", cycle, now,
                     repro="python3 tools/probe_sources.py")
    if rep.fetch_ok == 0:
        reason = ("The task plan was empty — there was nothing to read, which in "
                  "offline mode means no seed capture matched a registered source."
                  if not plan_size else
                  f"{rep.fetch_failed} of {plan_size} planned read(s) attempted, "
                  f"0 succeeded.")
        register.add(CRITICAL, "No successful read this cycle",
                     f"{reason}  The usual cause is egress being blocked (a TLS/SSL EOF "
                     f"on every host is a network policy, not a data problem) or "
                     f"credentials having expired. A cycle that read nothing still "
                     f"publishes, and publishes nothing new.", cycle, now,
                     repro="python3 tools/probe_sources.py")

    # A cap that quietly refuses work is a hidden gap.  The task list is capped so
    # this engine cannot abuse somebody's API; when the cap is reached, the reads it
    # refused are named here instead of looking like a plan that happened to be that
    # size.  Observed 2026-09-22: the cap was 70 and the plan was exactly 70, so one
    # deepening read was being dropped every cycle with nothing said about it.
    if rep.tasks_dropped:
        register.add(WARN, "Planned reads were refused by the per-cycle cap",
                     f"The plan asked for {(rep.tasks_planned or 0) + (rep.tasks_dropped or 0)} "
                     f"reads and "
                     f"{rep.tasks_dropped} were refused by MAX_TASKS_PER_CYCLE="
                     f"{taskmod.MAX_TASKS_PER_CYCLE}. Those reads did not happen, so no "
                     f"claim came from them. Raising the cap is a deliberate decision — it "
                     f"costs somebody's API budget — so the count is published instead of "
                     f"the plan being silently shortened.", cycle, now,
                     repro="python3 -c \"from msl.topics import Library;"
                           "from msl.tasks import build_plan,MAX_TASKS_PER_CYCLE;"
                           "s={};build_plan(Library(),'2026-01-01T00:00:00Z','20260101',"
                           "'20260107','x',stats=s);print(s,MAX_TASKS_PER_CYCLE)\"",
                     topic="plan", fingerprint="IRR-TASK-CAP")

    if rep.wiki_titles_skipped:
        register.add(INFO, "A wiki topic carries a title that is not a title",
                     f"MediaWiki capitalises the first letter of every article title, so a "
                     f"tracked topic whose recorded title starts lower-case is the slug read "
                     f"back rather than an article name. Those topics were not read: asking "
                     f"for the lowercased form returns a different page, which is the "
                     f"retracted wiki-case defect. Fix the topic's recorded title rather than "
                     f"the reader.", cycle, now,
                     repro="python3 -c \"import json;[print(t['slug'],repr(t['title'])) for t in "
                           "json.load(open('data/library.json'))['topics'] if t['slug'].startswith('wiki:')]\"",
                     topic="public-attention", fingerprint="IRR-WIKI-TITLE")

    if rep.forecasts_abandoned:
        register.add(WARN, "Forecasts can never be scored",
                     f"{rep.forecasts_abandoned} forecast(s) have waited "
                     f"{FORECASTS_PENDING_ABANDON_AFTER} cycles or more for a metric that has "
                     f"produced no observation since, so nothing will ever score them. They "
                     f"are dropped from the forecast log and counted here: a forecast that "
                     f"disappears without a word is a result that was never checked. The "
                     f"cause is usually a topic that stopped being read — the fix is a source "
                     f"that keeps observing it, not a longer wait.", cycle, now,
                     repro="python3 -c \"import json;d=json.load(open('data/forecasts.json'));"
                           "print(sum(1 for f in d['items'] if not f['scored']),'pending')\"",
                     topic="competition", fingerprint="IRR-FORECAST-UNSCOREABLE")

    if rep.forecasts_dropped_pending:
        register.add(WARN, "Forecasts hit the log size cap before they could be scored",
                     f"{rep.forecasts_dropped_pending} pending forecast(s) were dropped by the "
                     f"{FORECASTS_PENDING_KEPT}-row pending cap. Each one named an observation "
                     f"that has not arrived yet, so dropping it is a lost score, not history "
                     f"being trimmed. Raise FORECASTS_PENDING_KEPT, or stop issuing forecasts "
                     f"on metrics that update more slowly than the cap allows.",
                     cycle, now,
                     repro="python3 -c \"import json;print(len(json.load(open("
                           "'data/forecasts.json'))['items']))\"",
                     topic="competition", fingerprint="IRR-FORECAST-CAP")

    if rep.claims_new == 0 and rep.fetch_ok > 0:
        register.add(WARN, "Reads succeeded but produced no new claims",
                     f"{rep.fetch_ok} successful read(s) yielded 0 new claims. Either every "
                     f"observation was already in the ledger, or the adapters stopped matching "
                     f"the payload shapes. Both explanations are checked before this is "
                     f"dismissed.", cycle, now, repro="python3 -m msl.cli gate-report")


# --------------------------------------------------------------------------- #
# persistence helpers
# --------------------------------------------------------------------------- #
def _load_forecasts(d: pathlib.Path) -> List[Forecast]:
    p = d / "forecasts.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return [Forecast.from_dict(x) for x in data.get("items", [])]


#: Scored forecasts are history for the leaderboard and for anyone re-checking a
#: score; pending ones are live.  The two are capped separately because a single
#: ``forecasts[-4000:]`` window is enough to throw away a forecast that has been
#: issued but not yet scored — which is the only state in which a forecast can never
#: be scored, and it used to happen in silence.
FORECASTS_SCORED_KEPT = 4000
FORECASTS_PENDING_KEPT = 6000
#: A pending forecast whose metric has produced no observation for this many cycles
#: is not waiting for anything: nothing will ever score it.  It is dropped from the
#: file and the count is published, because a forecast that vanished quietly is the
#: same defect as a claim that was never checked.
FORECASTS_PENDING_ABANDON_AFTER = 6


def _save_forecasts(d: pathlib.Path, forecasts: List[Forecast], cycle: int = 0,
                    tracked: Optional[set] = None) -> Dict[str, int]:
    """Persist the forecast log, keeping everything that can still be scored.

    Returns the counts the cycle report publishes: how many forecasts are pending,
    how many were abandoned as unscoreable, and how many pending rows the size cap
    dropped (which is also reported, not swallowed).
    """
    scored = [f for f in forecasts if f.scored]
    pending = [f for f in forecasts if not f.scored]
    tracked = tracked or set()

    keep: List[Forecast] = []
    abandoned = 0
    for f in pending:
        if f.metric and tracked and f.metric not in tracked and \
                cycle and (cycle - f.cycle) >= FORECASTS_PENDING_ABANDON_AFTER:
            abandoned += 1
            continue
        keep.append(f)

    dropped = 0
    if len(keep) > FORECASTS_PENDING_KEPT:
        dropped = len(keep) - FORECASTS_PENDING_KEPT
        keep = keep[dropped:]          # oldest first: those are the stale ones

    # Written oldest-first so ``items[-600:]`` — the window the site renders — is
    # still the newest work, exactly as before this change.
    items = sorted(keep + scored[-FORECASTS_SCORED_KEPT:], key=lambda f: f.cycle)
    _write_json(d / "forecasts.json", {"items": [f.as_dict() for f in items]})
    return {"pending": len(keep), "abandoned": abandoned, "pendingDropped": dropped,
            "scored": min(len(scored), FORECASTS_SCORED_KEPT)}


def _load_ideas(d: pathlib.Path) -> List[Idea]:
    p = d / "ideas.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return [Idea.from_dict(x) for x in data.get("items", [])]


def _save_ideas(d: pathlib.Path, ideas: List[Idea]) -> None:
    _write_json(d / "ideas.json",
                {"items": [i.as_dict() for i in ideas[:600]]})


def _write_json(p: pathlib.Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                 encoding="utf-8")


def _append_jsonl(p: pathlib.Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, sort_keys=True, ensure_ascii=False) + "\n")


def _keyed_excluded() -> List[Dict[str, str]]:
    from .sources import KEYED_SOURCES_EXCLUDED
    return KEYED_SOURCES_EXCLUDED


def _categories_without_source() -> List[Dict[str, str]]:
    from .sources import INTEREST_CATEGORIES_WITHOUT_A_SOURCE
    return INTEREST_CATEGORIES_WITHOUT_A_SOURCE
