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
   or `negative` claim without an evidence row, and a `derived` claim without a
   lineage and a formula. Rejections are counted and published.
   → `tests/test_gate.py`
2. **Unreadable is not unknown.** A failed read produces a recorded failure with
   its HTTP status and a reproduction command, and marks the source `blocked`.
   No substitute value is invented.
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
| Plan | `msl/tasks.py` | Reading list is derived from the *current* library, so last cycle's topics get deeper reads now. Capped at 70 tasks |
| Collect | `msl/http.py` | Returns bytes or a recorded failure. Never a silent empty |
| Verify | `msl/evidence.py` | The gate. One door in |
| Discover | `msl/topics.py` | Entities become candidate topics; 2 signals promote; capped at 6 new topics per cycle |
| Reason | `msl/reason.py` | Arithmetic + recheck of every previous derivation |
| Compete | `msl/strategies.py`, `msl/ideas.py` | Personas forecast; ideas scored for robustness and carried forward |
| Learn | `msl/learn.py` | Skill and reliability folded into memory; lessons counted from the ledger |
| Publish | `msl/sitegen.py`, `msl/docs.py` | Site and docs regenerated from the same objects |

A stage that raises becomes an irregularity; the cycle still publishes.

## 4. Why the competition is scored the way it is

The headline number is **skill**, not accuracy:

```
skill = accuracy − accuracy(S10_Persistence)
```

`S10_Persistence` always predicts "no change". Most daily series are dominated by
no-change, so a persona can post respectable accuracy while demonstrating nothing
at all. Skill removes that flattering baseline. On the offline seed corpus — a
static snapshot, where nothing moves — the null model scores 100% and every other
persona scores at or below zero. That is the correct reading, and it is exactly
the situation the metric exists to expose.

**Qualification.** A persona is ranked only with ≥3 scored forecasts *and* a
scored null model. Below that it is reported `UNRANKED` with the reason. It is
never shown at 0%, which would present an untested design as a losing one.

**Scoring discipline.** A forecast may only be scored against an observation from
a *later* cycle. `tests/test_strategies.py` fails if a forecast is scored against
its own cycle.

## 5. How ideas compete

An idea is produced by one of six rules over verified claims, and carries the ids
of the claims behind it. An idea with no lineage is not produced — coverage gaps
are reported separately, never dressed as ideas.

Robustness is a weighted sum, recomputed every cycle from the *current* ledger:

| Component | Weight | Meaning |
|---|---|---|
| `evidence` | 0.30 | how many verified claims stand behind it |
| `corroboration` | 0.30 | how many independent sources report it |
| `breadth` | 0.15 | how many topic families it spans |
| `freshness` | 0.15 | how recent the newest supporting claim is |
| `reproducibility` | 0.10 | whether a reader can re-fetch the source now |

Ideas persist. One that keeps gaining corroboration climbs and is promoted; one
whose support disappears sinks to zero and is retired. That carry-forward is the
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
3. **Three interest categories are unserved.** Travel & Korea Trip, Social &
   Creator Data and Elections & Civic Data have no registered source that can
   answer their question. No claim is made about them.
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
8. **Seed captures taken by an interactive read are not wire-verifiable.** Those
   rows carry `wireHashVerifiable: false`; the first automated probe re-reads the
   endpoint and reports whether the values still match.
9. **The owner's shared document could not be read by a machine.** The brief
   points at a ChatGPT share URL whose body is rendered client-side; the only
   server-supplied content is its `<title>`, "Design Autonomous Research System".
   No requirement in this repository is sourced from that transcript.

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
