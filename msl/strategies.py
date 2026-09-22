"""The competition: deterministic strategy personas that must beat a null model.

Each persona reads only the verified ledger and issues *forecasts* — falsifiable
predictions about the next observation of a tracked metric.  The following cycle
the engine looks up what actually happened and scores them.  Nothing is scored
that was not forecast in advance, and nothing is ranked that has not been scored
enough times to mean anything (``MIN_SCORED_FORECASTS_TO_RANK``): a persona that
never traded is reported ``UNRANKED`` with the reason, never as "0%".

The headline metric is **skill**, not accuracy: ``accuracy - accuracy of
S10_Persistence``.  S10 always predicts "no change", so it is the null hypothesis,
and a persona with positive accuracy but non-positive skill has demonstrated
nothing.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from . import config
from .evidence import Claim, Ledger
from .retractions import is_retracted

DIRECTION_UP = "up"
DIRECTION_DOWN = "down"
DIRECTION_FLAT = "flat"


#: Two kinds of target, and they are scored by the same rule.
#:
#: ``numeric``  a magnitude: up, down, or unchanged.
#: ``change``   an identity: a version string, a release tag, a primary language, a
#:              repository state.  A version has no magnitude, so "up" there means
#:              "different from the last observation" and "flat" means "the same".
#:              That is the honest form of the question "will the next release land
#:              before the next cycle?", and its outcome is knowable one cycle later
#:              in exactly the same way.
METRIC_NUMERIC = "numeric"
METRIC_CHANGE = "change"


@dataclass
class Forecast:
    strategy_id: str
    cycle: int
    topic: str
    metric: str                  # the claim field being predicted
    direction: str               # up | down | flat
    probability: float           # P(up); for a change target, P(the value differs)
    basis: List[str] = field(default_factory=list)
    reason: str = ""
    scored: bool = False
    outcome: str = ""
    outcome_value: Any = None
    scored_at_cycle: int = 0
    brier: Optional[float] = None
    metric_kind: str = METRIC_NUMERIC

    def as_dict(self) -> Dict[str, Any]:
        return {"strategyId": self.strategy_id, "cycle": self.cycle, "topic": self.topic,
                "metric": self.metric, "direction": self.direction,
                "metricKind": self.metric_kind,
                "probability": round(self.probability, 4), "basis": self.basis,
                "reason": self.reason, "scored": self.scored, "outcome": self.outcome,
                "outcomeValue": self.outcome_value, "scoredAtCycle": self.scored_at_cycle,
                "brier": self.brier}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Forecast":
        return cls(strategy_id=d["strategyId"], cycle=d["cycle"], topic=d["topic"],
                   metric=d["metric"], direction=d["direction"],
                   probability=d["probability"], basis=d.get("basis", []) or [],
                   reason=d.get("reason", ""), scored=bool(d.get("scored")),
                   outcome=d.get("outcome", ""), outcome_value=d.get("outcomeValue"),
                   scored_at_cycle=d.get("scoredAtCycle", 0), brier=d.get("brier"),
                   metric_kind=d.get("metricKind", METRIC_NUMERIC))


@dataclass
class StrategyScore:
    strategy_id: str
    name: str
    thesis: str
    issued: int = 0
    scored: int = 0
    correct: int = 0
    brier_sum: float = 0.0
    skill: Optional[float] = None
    status: str = "unranked"
    unranked_reason: str = ""

    @property
    def accuracy(self) -> Optional[float]:
        return self.correct / self.scored if self.scored else None

    @property
    def mean_brier(self) -> Optional[float]:
        return self.brier_sum / self.scored if self.scored else None

    def as_dict(self) -> Dict[str, Any]:
        return {"strategyId": self.strategy_id, "name": self.name, "thesis": self.thesis,
                "issued": self.issued, "scored": self.scored, "correct": self.correct,
                "accuracy": self.accuracy, "meanBrier": self.mean_brier,
                "skill": self.skill, "status": self.status,
                "unrankedReason": self.unranked_reason}


@dataclass
class Strategy:
    id: str
    name: str
    thesis: str
    fn: Callable[["Context"], List[Forecast]]
    #: personas that are allowed to learn from the memory
    adaptive: bool = False


@dataclass
class Context:
    ledger: Ledger
    cycle: int
    now: str
    memory: Dict[str, Any]
    metrics: Dict[str, List[Claim]]     # numeric metric field -> ordered claims
    topic_of: Dict[str, str]            # metric field -> topic slug
    #: Categorical series, same shape.  ``__post_init__`` fills them when a caller
    #: does not, so nobody can construct a context that quietly sees only half of the
    #: observable world and then report that the other half never moves.
    changes: Dict[str, List[Claim]] = field(default_factory=dict)
    change_topic_of: Dict[str, str] = field(default_factory=dict)
    change_kind: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.changes:
            self.changes, self.change_topic_of, self.change_kind = tracked_changes(self.ledger)


# --------------------------------------------------------------------------- #
# metric extraction
# --------------------------------------------------------------------------- #
_VIEWS = re.compile(r"^wiki\[[^\]]+\]\.views\.\d{4}-\d{2}-\d{2}$")
# keyed by repository name, not by position — see msl/adapters.gh_search
_STARS = re.compile(r"^github\.repo\[[^\]]+\]\.stars$")
_FORKS = re.compile(r"^github\.repo\[[^\]]+\]\.forks$")
_COUNTS = {"owner.public_repos", "owner.pages_repos", "owner.total_kb",
           "hn.topstories.length"}
#: Rates and counters that are re-read every cycle, so "where is this next cycle?"
#: has a knowable answer rather than a rhetorical one.  Deliberately a curated list
#: and not "any numeric field": a target that is constant by construction (the size
#: of a page we asked for) would fill the forecast log with noise and flatter
#: whichever persona happened to predict it.
_NUMERIC_SERIES = (
    re.compile(r"^fx\[[^\]]+\]\.vsUSD$"),
    re.compile(r"^ecb\[[^\]]+\]\.latest$"),
    re.compile(r"^bls\[[^\]]+\]\.latest$"),
    re.compile(r"^worldbank\[[^\]]+\]\.latest$"),
    re.compile(r"^usgs\.events\[[^\]]+\]$"),
    re.compile(r"^nws\.alerts\[[^\]]+\]$"),
    re.compile(r"^clinicaltrials\.totalCount$"),
    re.compile(r"^pubmed\.hits\[[^\]]+\]$"),
    re.compile(r"^crossref\.totalResults$"),
    re.compile(r"^openalex\.count$"),
    re.compile(r"^arxiv\.totalResults$"),
    re.compile(r"^europepmc\.hitCount$"),
    re.compile(r"^nhl\.games_today$"),
    re.compile(r"^nba\.games_today$"),
    re.compile(r"^sec\[[^\]]+\]\.recent_filings$"),
)
#: Categorical series: subjects whose *identity* is the observation.  A version
#: string cannot be bigger or smaller than the last one, so the only question that
#: means anything is whether it changed.  Every entry here names the kind of thing
#: that changed, which is what the published reason says out loud.
CHANGE_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"^pypi\[[^\]]+\]\.version$"), "release version"),
    (re.compile(r"^npm\[[^\]]+\]\.version$"), "release version"),
    (re.compile(r"^github\.release\[[^\]]+\]\.tag$"), "release tag"),
    (re.compile(r"^github\.repo\[[^\]]+\]\.language$"), "primary language"),
    (re.compile(r"^github\.repo\[[^\]]+\]\.state$"), "repository state"),
]


def _by_cycle(claims: List[Claim]) -> List[Claim]:
    """One observation per cycle, keeping the last read inside that cycle.

    A cycle reads the same field more than once whenever two planned reads overlap
    (a family survey and a follow-up query both describing one repository, a probe
    and a survey reading one count).  Those are two reads of one moment, not two
    moments: scored as a series they let a persona "forecast" the difference between
    two readings taken minutes apart.  193 field/cycle pairs in the ledger have more
    than one observation, one of them a star count that moved by 1 inside a single
    cycle.  The comparison a forecast makes is *cycle to cycle*, so that is the
    series it is given.
    """
    latest: Dict[int, Claim] = {}
    for c in sorted(claims, key=lambda c: (c.retrieved_at, c.cycle)):
        latest[c.cycle] = c
    return [latest[k] for k in sorted(latest)]


def tracked_metrics(ledger: Ledger) -> Tuple[Dict[str, List[Claim]], Dict[str, str]]:
    """Every numeric field that has at least two one-per-cycle observations."""
    buckets: Dict[str, List[Claim]] = {}
    for c in ledger.claims:
        if c.kind != "captured" or not isinstance(c.value, (int, float)):
            continue
        # A retracted field is withdrawn from reasoning as well as from the site.
        # It used to be withdrawn from msl/reason.py only, so the competition kept
        # issuing forecasts on the retracted lowercased-Wikipedia series — forecasts
        # that could never be scored, because nothing observes that series any more.
        if is_retracted(c.field):
            continue
        if (_VIEWS.match(c.field) or _STARS.match(c.field) or _FORKS.match(c.field)
                or c.field in _COUNTS
                or c.field.startswith("fedreg.documents[")
                or c.field.startswith("github.total_count[")
                or any(p.match(c.field) for p in _NUMERIC_SERIES)):
            buckets.setdefault(c.field, []).append(c)
    metrics: Dict[str, List[Claim]] = {}
    topic_of: Dict[str, str] = {}
    for k, v in buckets.items():
        series = _by_cycle(v)
        if len(series) < 2:
            continue
        metrics[k] = series
        topic_of[k] = series[-1].topic
    return metrics, topic_of


def tracked_changes(ledger: Ledger) -> Tuple[Dict[str, List[Claim]], Dict[str, str], Dict[str, str]]:
    """Every categorical field with at least two one-per-cycle observations.

    Returns the series, the topic each belongs to, and what kind of thing it is
    ("release version", "release tag", ...) so the published reason can name it.
    """
    buckets: Dict[str, List[Claim]] = {}
    kind_of: Dict[str, str] = {}
    for c in ledger.claims:
        if c.kind != "captured" or not isinstance(c.value, str):
            continue
        if is_retracted(c.field):
            continue
        for pattern, label in CHANGE_PATTERNS:
            if pattern.match(c.field):
                buckets.setdefault(c.field, []).append(c)
                kind_of.setdefault(c.field, label)
                break
    changes: Dict[str, List[Claim]] = {}
    topic_of: Dict[str, str] = {}
    for k, v in buckets.items():
        series = _by_cycle(v)
        if len(series) < 2:
            continue
        changes[k] = series
        topic_of[k] = series[-1].topic
    return changes, topic_of, kind_of


def _direction(a: float, b: float) -> str:
    if b > a:
        return DIRECTION_UP
    if b < a:
        return DIRECTION_DOWN
    return DIRECTION_FLAT


def _clamp(p: float) -> float:
    return min(max(p, 0.02), 0.98)


# --------------------------------------------------------------------------- #
# personas
# --------------------------------------------------------------------------- #
def _persist(ctx: Context) -> List[Forecast]:
    """S10 — the null model.  Predicts the next observation repeats this one.

    It covers both kinds of target, which is what makes the null model a fair
    baseline for both: on a numeric series "flat" means the same value, on a
    categorical one it means the same version or tag.
    """
    out = []
    for m, series in ctx.metrics.items():
        out.append(Forecast("S10_Persistence", ctx.cycle, ctx.topic_of[m], m,
                            DIRECTION_FLAT, 0.5, [series[-1].id],
                            "Null model: assume the last observation repeats."))
    for m, series in ctx.changes.items():
        out.append(Forecast("S10_Persistence", ctx.cycle, ctx.change_topic_of[m], m,
                            DIRECTION_FLAT, 0.5, [series[-1].id],
                            f"Null model: assume the {ctx.change_kind.get(m, 'value')} "
                            f"does not change.", metric_kind=METRIC_CHANGE))
    return out


def _momentum(ctx: Context) -> List[Forecast]:
    """S01 — the observed trend continues."""
    out = []
    for m, series in ctx.metrics.items():
        a, b = float(series[-2].value), float(series[-1].value)
        d = _direction(a, b)
        if d == DIRECTION_FLAT:
            continue
        mag = abs(b - a) / max(abs(a), 1e-9)
        p = _clamp(0.5 + min(mag, 1.0) * 0.35)
        out.append(Forecast("S01_MomentumPersist", ctx.cycle, ctx.topic_of[m], m, d,
                            p if d == DIRECTION_UP else 1 - p, [series[-2].id, series[-1].id],
                            f"Last move was {a:,.0f}→{b:,.0f} ({mag*100:.1f}%); assume it continues."))
    return out


def _mean_revert(ctx: Context) -> List[Forecast]:
    """S02 — the observed trend reverses toward the series mean."""
    out = []
    for m, series in ctx.metrics.items():
        vals = [float(c.value) for c in series]
        a, b = vals[-2], vals[-1]
        mean = sum(vals) / len(vals)
        d = DIRECTION_UP if b < mean else (DIRECTION_DOWN if b > mean else DIRECTION_FLAT)
        if d == DIRECTION_FLAT:
            continue
        gap = abs(b - mean) / max(abs(mean), 1e-9)
        p = _clamp(0.5 + min(gap, 1.0) * 0.30)
        out.append(Forecast("S02_MeanRevert", ctx.cycle, ctx.topic_of[m], m, d,
                            p if d == DIRECTION_UP else 1 - p,
                            [series[-1].id],
                            f"Last value {b:,.0f} sits {gap*100:.1f}% from the series mean {mean:,.0f}."))
    return out


def _acceleration(ctx: Context) -> List[Forecast]:
    """S03 — forecast the second difference: is the trend speeding up?"""
    out = []
    for m, series in ctx.metrics.items():
        if len(series) < 3:
            continue
        v = [float(c.value) for c in series[-3:]]
        d1, d2 = v[1] - v[0], v[2] - v[1]
        acc = d2 - d1
        if acc == 0:
            continue
        d = DIRECTION_UP if acc > 0 else DIRECTION_DOWN
        scale = abs(acc) / max(abs(v[2]), 1e-9)
        p = _clamp(0.5 + min(scale, 1.0) * 0.30)
        out.append(Forecast("S03_Acceleration", ctx.cycle, ctx.topic_of[m], m, d,
                            p if d == DIRECTION_UP else 1 - p,
                            [c.id for c in series[-3:]],
                            f"Successive changes {d1:+,.0f} then {d2:+,.0f}; acceleration {acc:+,.0f}."))
    return out


def _consensus_fade(ctx: Context) -> List[Forecast]:
    """S04 — contrarian: fade whatever every other persona agrees on."""
    agree: Dict[str, Dict[str, int]] = {}
    for s in (STRATEGY_BY_ID["S01_MomentumPersist"], STRATEGY_BY_ID["S02_MeanRevert"],
              STRATEGY_BY_ID["S03_Acceleration"]):
        for f in s.fn(ctx):
            agree.setdefault(f.metric, {}).setdefault(f.direction, 0)
            agree[f.metric][f.direction] += 1
    out = []
    for m, tally in agree.items():
        top = max(tally.items(), key=lambda kv: kv[1])
        if top[1] < 2:
            continue
        opp = DIRECTION_DOWN if top[0] == DIRECTION_UP else DIRECTION_UP
        p = _clamp(0.5 + 0.10 * top[1])
        out.append(Forecast("S04_ConsensusFade", ctx.cycle, ctx.topic_of[m], m, opp,
                            p if opp == DIRECTION_UP else 1 - p, [],
                            f"{top[1]} personas predicted {top[0]}; fade the consensus."))
    return out


def _evidence_density(ctx: Context) -> List[Forecast]:
    """S05 — the metric with the most independent evidence behind it keeps moving."""
    out = []
    for m, series in ctx.metrics.items():
        srcs = {c.source_id for c in series}
        d = _direction(float(series[-2].value), float(series[-1].value))
        if d == DIRECTION_FLAT:
            continue
        p = _clamp(0.5 + min(len(srcs), 3) * 0.12)
        out.append(Forecast("S05_EvidenceDensity", ctx.cycle, ctx.topic_of[m], m, d,
                            p if d == DIRECTION_UP else 1 - p, [series[-1].id],
                            f"Series is backed by {len(srcs)} source(s) and {len(series)} observations."))
    return out


def _memory_weighted(ctx: Context) -> List[Forecast]:
    """S06 — the adaptive persona.  Votes are weighted by realised skill.

    This is the only persona that changes its own behaviour over time, and it can
    only do so from numbers the ledger already contains: the per-persona skill
    recorded in ``data/memory.json`` by previous scoring runs.
    """
    weights = (ctx.memory.get("strategyWeights") or {})
    votes: Dict[str, Dict[str, float]] = {}
    basis: Dict[str, List[str]] = {}
    for sid in ("S01_MomentumPersist", "S02_MeanRevert", "S03_Acceleration", "S05_EvidenceDensity"):
        w = weights.get(sid)
        if w is None:
            continue                      # never weight an unscored persona
        w = max(w, 0.0)
        for f in STRATEGY_BY_ID[sid].fn(ctx):
            votes.setdefault(f.metric, {}).setdefault(f.direction, 0.0)
            votes[f.metric][f.direction] += w * f.probability
            basis.setdefault(f.metric, []).extend(f.basis)
    out = []
    for m, tally in votes.items():
        if not tally:
            continue
        best = max(tally.items(), key=lambda kv: kv[1])
        total = sum(tally.values()) or 1.0
        p = _clamp(best[1] / total)
        out.append(Forecast("S06_MemoryWeighted", ctx.cycle, ctx.topic_of[m], m, best[0],
                            p if best[0] == DIRECTION_UP else 1 - p,
                            basis.get(m, [])[:6],
                            f"Skill-weighted vote over {len(weights)} previously scored personas."))
    return out


def _change_hazard(ctx: Context) -> List[Forecast]:
    """S07 — how often does this subject change?  Straight from its own history.

    A release version, a release tag, a primary language and a repository state all
    share one property: their own recorded history contains the only base rate worth
    using.  A package that shipped in three of the last ten cycles has an estimated
    chance of shipping again this cycle, and that estimate is checkable against the
    ledger the forecast is scored against.
    """
    out = []
    for m, series in ctx.changes.items():
        vals = [str(c.value) for c in series]
        transitions = len(vals) - 1
        if transitions < 1:
            continue
        changed = sum(1 for a, b in zip(vals, vals[1:]) if a != b)
        # Laplace smoothing with the null model's prior: one imagined unchanged
        # transition, one imagined change.  Without it a series that has never moved
        # would be issued at p=0, which is a claim no finite history supports.
        p = _clamp((changed + 1) / (transitions + 2))
        direction = DIRECTION_UP if p > 0.5 else DIRECTION_FLAT
        kind = ctx.change_kind.get(m, "value")
        out.append(Forecast(
            "S07_ChangeHazard", ctx.cycle, ctx.change_topic_of[m], m, direction, p,
            [c.id for c in series[-3:]],
            f"The {kind} changed in {changed} of the last {transitions} cycle-to-cycle "
            f"observations, so it is forecast to "
            f"{'change' if direction == DIRECTION_UP else 'stay the same'}.",
            metric_kind=METRIC_CHANGE))
    return out


STRATEGIES: List[Strategy] = [
    Strategy("S01_MomentumPersist", "Momentum persistence",
             "A metric that moved last cycle moves the same way next cycle.", _momentum),
    Strategy("S02_MeanRevert", "Mean reversion",
             "A metric away from its own series mean moves back toward it.", _mean_revert),
    Strategy("S03_Acceleration", "Acceleration",
             "The second difference, not the first, predicts the next move.", _acceleration),
    Strategy("S04_ConsensusFade", "Consensus fade",
             "When the other personas agree, the crowd is already positioned; fade it.",
             _consensus_fade),
    Strategy("S05_EvidenceDensity", "Evidence density",
             "Metrics corroborated by more independent sources have more reliable trends.",
             _evidence_density),
    Strategy("S06_MemoryWeighted", "Skill-weighted memory",
             "Combine the personas in proportion to the skill they have actually earned.",
             _memory_weighted, adaptive=True),
    Strategy("S07_ChangeHazard", "Change hazard",
             "How often a release version, tag, language or repository state has "
             "changed in its own recorded history is the best available estimate of "
             "whether it changes next cycle.", _change_hazard),
    Strategy("S10_Persistence", "Persistence (null model)",
             "Nothing changes.  Every other persona must beat this to be worth keeping.",
             _persist),
]
STRATEGY_BY_ID: Dict[str, Strategy] = {s.id: s for s in STRATEGIES}


# --------------------------------------------------------------------------- #
# issue / score
# --------------------------------------------------------------------------- #
def issue(ctx: Context) -> List[Forecast]:
    out: List[Forecast] = []
    for s in STRATEGIES:
        if s.adaptive and not ctx.memory.get("strategyWeights"):
            continue          # nothing to weight yet; issuing would be noise
        try:
            out.extend(s.fn(ctx))
        except Exception as e:  # noqa: BLE001 - one bad persona must not kill the cycle
            out.append(Forecast(s.id, ctx.cycle, "", "", DIRECTION_FLAT, 0.5, [],
                                f"PERSONA ERROR {type(e).__name__}: {e}"))
    return out


def score(forecasts: List[Forecast], ctx: Context) -> List[Forecast]:
    """Score every unscored forecast against the newest observation.

    Both kinds of target are realised here, and a forecast is only ever scored
    against an observation from a *later* cycle.  For a numeric series the outcome is
    the observed direction; for a categorical one it is "changed" or "unchanged",
    which is what the persona was asked to call.
    """
    for f in forecasts:
        if f.scored or not f.metric:
            continue
        series = ctx.metrics.get(f.metric)
        kind = f.metric_kind or METRIC_NUMERIC
        if series is None:
            # A forecast issued before this cycle, or by a persona that named the
            # other kind, still has to find its series rather than be silently
            # skipped: unlike a numeric series, a categorical one never leaves the
            # scoreable set.
            series = ctx.changes.get(f.metric)
            kind = METRIC_CHANGE if series is not None else kind
        if not series:
            continue
        newest = series[-1]
        if newest.cycle <= f.cycle:
            continue                      # no new observation since the forecast
        prev = None
        for c in reversed(series[:-1]):
            if c.cycle <= f.cycle:
                prev = c
                break
        if prev is None:
            continue
        if kind == METRIC_CHANGE:
            realized = (DIRECTION_FLAT if str(newest.value) == str(prev.value)
                        else DIRECTION_UP)
            f.outcome_value = newest.value
        else:
            a, b = float(prev.value), float(newest.value)
            realized = _direction(a, b)
            f.outcome_value = b
        f.outcome = realized
        f.scored = True
        f.scored_at_cycle = ctx.cycle
        # P(up), whatever "up" means for this target: a rise, or a change.
        y = 1.0 if realized == DIRECTION_UP else 0.0
        f.brier = (f.probability - y) ** 2
    return forecasts


def leaderboard(forecasts: List[Forecast]) -> Dict[str, Any]:
    scores: Dict[str, StrategyScore] = {}
    for s in STRATEGIES:
        scores[s.id] = StrategyScore(s.id, s.name, s.thesis)
    for f in forecasts:
        sc = scores.get(f.strategy_id)
        if sc is None:
            sc = StrategyScore(f.strategy_id, f.strategy_id, "")
            scores[f.strategy_id] = sc
        sc.issued += 1
        if not f.scored or not f.outcome:
            continue
        sc.scored += 1
        if f.outcome == f.direction:
            sc.correct += 1
        if f.brier is not None:
            sc.brier_sum += f.brier

    null = scores.get("S10_Persistence")
    null_acc = null.accuracy if null and null.scored else None
    for sc in scores.values():
        if sc.scored < config.MIN_SCORED_FORECASTS_TO_RANK:
            sc.status = "unranked"
            sc.unranked_reason = (
                f"{sc.scored} scored forecast(s); {config.MIN_SCORED_FORECASTS_TO_RANK} "
                f"required before a rank means anything.")
            continue
        if null_acc is None:
            sc.status = "unranked"
            sc.unranked_reason = "The null model has no scored forecasts to compare against yet."
            continue
        sc.skill = round(sc.accuracy - null_acc, 4)
        sc.status = "ranked"
    ranked = sorted([s for s in scores.values() if s.status == "ranked"],
                    key=lambda s: (-(s.skill or 0), s.mean_brier or 1, s.strategy_id))
    for i, sc in enumerate(ranked, 1):
        sc.skill_rank = i  # type: ignore[attr-defined]
    return {
        "nullAccuracy": null_acc,
        "nullScored": null.scored if null else 0,
        "ranked": [s.as_dict() for s in ranked],
        "unranked": [s.as_dict() for s in scores.values() if s.status == "unranked"],
        "all": [s.as_dict() for s in scores.values()],
        "qualification": {
            "minScoredForecasts": config.MIN_SCORED_FORECASTS_TO_RANK,
            "rule": ("A persona is ranked only when it has at least "
                     f"{config.MIN_SCORED_FORECASTS_TO_RANK} scored forecasts AND the null "
                     "model does too.  Skill = accuracy − null accuracy, so a persona must "
                     "beat 'nothing changes' to appear in the ranked table at all."),
        },
    }


def update_weights(lb: Dict[str, Any], memory: Dict[str, Any]) -> Dict[str, Any]:
    """Fold this cycle's skill into the memory weights (EMA, α = 0.25)."""
    w = dict(memory.get("strategyWeights") or {})
    alpha = 0.25
    for row in lb.get("all", []):
        sid = row["strategyId"]
        if row["skill"] is None or sid == "S10_Persistence":
            continue
        prev = max(w.get(sid, 0.5), 0.0)
        # skill is bounded below by -1, so 0.5 + skill can go negative.  Floor the
        # TARGET at 0: a persona that is maximally wrong earns zero weight, not a
        # negative one that would make S06 vote against its own past judgement.
        target = max(0.5 + row["skill"], 0.0)
        w[sid] = round(prev * (1 - alpha) + target * alpha, 6)
    memory["strategyWeights"] = w
    return memory
