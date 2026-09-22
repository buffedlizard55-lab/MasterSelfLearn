# METHODOLOGY

How this project reasons, what it refuses to do, and where the reasoning stops.
Written to be checked, not admired.

---

## 1. What "thinks and reasons on its own" means here

The engine runs unattended on a timer and, each cycle, produces new claims, new
topics, new forecasts and new research ideas that were not present in the cycle
before. That much is literal.

What it does **not** contain is a language model. There is no API key and no
model client anywhere in the repository — `grep -rn 'openai\|anthropic' msl/`
returns nothing. The reasoning stage is a fixed rule set over the verified claim
ledger:

| Rule | Computes | Re-checkable? |
|---|---|---|
| `trend` | `(last − first) / first × 100` over a daily series | yes |
| `delta` | `last − first` for a counter between cycles | yes |
| `velocity` | `stars / max(age_days, 1)` | no — the denominator is *now* |
| `corroboration` | count of distinct **independent** sources reporting an entity | yes |
| `crossfamily` | count of distinct topic families an entity appears in | yes |

Every sentence published by the site is a template whose slots are filled from
claim values. No sentence is generated freely.

**The trade is explicit.** This costs novelty: the engine will not invent a
framing nobody wrote down. It buys auditability: any number on the site can be
recomputed from the ledger with one command. A model with an API key would need a
secret, and adding a secret is manual input — which the brief rules out. If the
owner ever supplies a key, that is a deliberate change and it must be recorded
here first.

## 2. The anti-hallucination contract

Five rules, each enforced in code with a test:

1. **No evidence, no claim.** `Ledger.accept` rejects a `captured`, `documented`
   or `negative` claim unless it cites a complete successful read with an integrity
   hash, matching source and URL, stable field identity, and exact adapter source
   path. A `derived` claim needs existing lineage, a formula, and `sourceId=derived`.
   Rejections are persisted in append-only `data/rejections.jsonl` and published.
   → `tests/test_gate.py`
2. **Unreadable is not unknown.** A failed read produces a recorded failure with
   its HTTP status and a reproduction command. A definitive source-side failure
   marks the source `blocked`; malformed requests, local response caps, and runner
   egress failures do not manufacture a claim that somebody else's service is
   down. An exact-URL hashed seed may be reused only as an explicitly stale
   `seed-fallback` with its original capture time; it is never represented as the
   failed response or as a fresh observation.
   → `tests/test_pipeline.py::FailurePaths`
3. **Yesterday's arithmetic is re-checked today.** Every derived claim is
   recomputed from its recorded inputs each cycle. A mismatch is a drift
   irregularity and both numbers are shown.
   → `tests/test_reason.py::Recheck`
4. **Silent defaults are banned.** A payload missing a field the adapter reads
   produces a shape problem and no figure — never a 0. This is not theoretical:
   a seed projection once used shortened keys, the adapter read `None`, and the
   ledger published "0 stars" for every repository.
   → `tests/test_adapters.py::GitHubSearch`
5. **Gaps are printed.** Topics with zero verified claims, families with no
   source that can answer their question, and sources excluded for needing a key
   are all listed with the reason.

## 3. The cycle

| Stage | Module | Contract |
|---|---|---|
| Plan | `msl/tasks.py` | Reading list is derived from the *current* library, so last cycle's topics get deeper reads now. Capped at 84 tasks; operator quotas and host pacing are enforced |
| Collect | `msl/http.py` | Returns complete bytes or a recorded failure. Truncated responses are unusable; redirects and content types are retained |
| Verify | `msl/evidence.py` | One gate validates evidence, integrity, source, URL, field, and source path |
| Discover | `msl/topics.py` | Entities become candidate topics; 2 signals promote; capped at 6 new topics per cycle |
| Reason | `msl/reason.py` | Arithmetic + recheck of every previous derivation |
| Compete | `msl/strategies.py`, `msl/ideas.py` | Personas forecast; ideas scored for robustness and carried forward |
| Learn | `msl/learn.py` | Skill and reliability folded into memory; lessons counted from the ledger |
| Publish | `msl/sitegen.py`, `msl/docs.py` | Site and docs regenerated from the same objects |

A stage that raises becomes an irregularity; the cycle still publishes.

## 4. Why the competition is scored the way it is

The headline number is **paired skill**, not raw accuracy:

```
paired skill = persona accuracy − persistence accuracy
               on the exact same metric/cycle targets
```

`S10_Persistence` always predicts "no change". Most daily series are dominated by
no-change, so a persona can post respectable accuracy while demonstrating nothing.
The older leaderboard subtracted the null's *global* accuracy even when a persona
forecast a different target mix; that was not a controlled comparison. The current
score joins each forecast to persistence by metric, issue cycle, and metric kind,
and excludes an unmatched pair.

**Qualification.** A persona is ranked only with ≥3 paired scored forecasts.
Below that it is reported `UNRANKED` with the reason. It is never shown at 0%,
which would present an untested design as a losing one.

**Scoring discipline.** A forecast may only be scored against an observation from
a *later* cycle. `tests/test_strategies.py` fails if a forecast is scored against
its own cycle.

## 5. How ideas compete

An idea is produced by one of six rules over verified claims, and carries the ids
of the claims behind it. An idea with no lineage is not produced — coverage gaps
are reported separately, never dressed as ideas.

Robustness is a weighted sum, recomputed every cycle from the current terminal
captured evidence. Derived lineage is recursively expanded, so rerunning arithmetic
cannot make an old source observation look fresh or independently corroborated:

| Component | Weight | Meaning |
|---|---|---|
| `evidence` | 0.30 | how many verified claims stand behind it |
| `corroboration` | 0.30 | how many independent sources report it |
| `breadth` | 0.15 | how many topic families it spans |
| `freshness` | 0.15 | how recent the newest supporting claim is |
| `reproducibility` | 0.10 | whether a reader can re-fetch the source now |

Ideas persist, but a recurring idea replaces its active lineage with the current
cycle's support instead of accumulating evidence forever. Freshness decays over seven
days. One that keeps gaining corroboration climbs and is promoted; one whose support
disappears sinks to zero and is retired. That carry-forward is the
"learning from previous ideas" part, and it is arithmetic over the ledger rather
than memory.

## 6. What the engine has learned about itself

`data/memory.json → lessons` holds rules the engine derived about its own track
record by counting. Each carries the integers behind it. A lesson with no
supporting count is not written. Current lessons:

| | Counts |
|---|---|
| `L1` | do multi-source topics persist longer than single-source ones |
| `L2` | what fraction of attempted claims the gate rejects |
| `L3` | what fraction of tracked topics actually have evidence |
| `L4` | which idea kinds hold the highest mean robustness |
| `L5` | how many sources are reading reliably |

## 7. Limits, stated plainly

1. **No language model.** See §1. The output is reproducible, not inventive.
2. **No keyed sources.** FRED, the NFL Game API, Google Trends, the X API,
   YouTube Data and TikTok/Instagram are all excluded; each is listed in
   `msl/sources.py → KEYED_SOURCES_EXCLUDED` with the reason.
3. **Four interest categories have missing or partial coverage.** Travel & Korea
   Trip has geocoding but not prices; Social & Creator Data has public-attention
   signals but no creator-platform metrics; Elections & Civic Data has federal
   rulemaking but not election results; Gaming & Guides has no confirmed source.
   No claim is made beyond those surfaces. The authoritative list is
   `msl/sources.py → INTEREST_CATEGORIES_WITHOUT_A_SOURCE`; the count in this
   sentence was correct when written and is the kind of figure that goes stale,
   so the list wins.
   (Gaming & Guides was missing from this document entirely until 2026-09-22 —
   an omission that is not written down is invisible, which is worse than a gap
   that is.)
4. **GitHub has no trending API.** The Search API sorted by stars over a
   `created:>=` window is a reproducible substitute, not the same thing. A
   trending *page* is a curated list with an undisclosed ranking.
5. **Three sports feeds are undocumented public endpoints** — `statsapi.mlb.com`,
   `api-web.nhle.com`, `cdn.nba.com`. No official contract page was located for
   any of them. Claims built from one carry the marker.
6. **Frankfurter is not an official ECB endpoint.** It is a community service
   republishing ECB reference rates, kept as a redundancy check against the
   official ECB SDMX route and labelled third-party in every statement it
   produces.
7. **Some derived claims cannot be re-checked.** A repository's stars-per-day has
   *now* in its denominator. Those are counted as NOT RECHECKED, never as passing.
8. **Historical integrity is not retroactively upgraded.** Most cycle 1–18
   evidence rows retained a canonical projection hash but not the response bytes,
   despite some carrying the old `wireHashVerifiable: true` flag. The loader now
   classifies those rows as `projection`, the site labels them, and the verifier
   reports the count. New live reads retain a hash of the exact decompressed bytes
   handed to the adapter. Interactive/CLI seed captures remain projection-only.
9. **The owner's shared document could not be read by a machine.** The brief
   points at a ChatGPT share URL whose body is rendered client-side; the only
   server-supplied content is its `<title>`, "Design Autonomous Research System".
   No requirement in this repository is sourced from that transcript.
10. **"Never read" is not "broken".** A source in the `registered` state has
    simply not been reached by a conclusive recorded read. Runner egress failure is
    a property of the runner, not evidence about a service.
11. **GitHub schedules are best effort, not a nonstop-process guarantee.** The
    workflow is requested every 30 minutes and serialized with the daily writer,
    but GitHub documents that scheduled jobs can be delayed or dropped under load.
    The generated timestamp and cycle history make a gap visible; this repository
    cannot make GitHub's hosted scheduler provide a hard real-time SLA.
12. **The MasterSite catalog is a point-in-time artifact with mixed provenance.**
    Repository, commit, and Pages fields come from its recorded GitHub API audit;
    descriptions come from MasterSite's first-party audited overlay and retain
    `verifiedBasis`. MasterSelfLearn verifies the catalog file and Git blob SHA but
    does not re-query all 52 repositories each cycle, so rows can become stale
    between MasterSite audits. The Projects page labels audit dates, treats this
    repository's pre-implementation “empty placeholder” row as superseded, and does
    not relabel narrative descriptions as current GitHub-authored facts.

## 8. Reproduce any number on the site

```bash
python3 -m msl.cli cycle --offline   # rebuild every artifact from data/seed/
python3 -m msl.cli verify-claims     # recheck every derived claim
python3 tools/probe_sources.py       # live-read every registered source
python3 -m msl.cli gate-report       # what the evidence gate rejected
python3 -m unittest discover -s tests
```

A number on the site that cannot be reproduced with one of those commands is a
defect. Report it as an irregularity rather than editing the number.
