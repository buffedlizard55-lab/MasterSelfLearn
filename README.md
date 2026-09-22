# MasterSelfLearn

An autonomous, evidence-first research engine. It runs on a timer, reads official
public data, builds an expanding library of topics, makes each of a set of
competing personas predict what happens next, scores them against what actually
happened, and writes the whole thing up — with a link a human can open for every
number it prints.

**Live site:** <https://buffedlizard55-lab.github.io/MasterSelfLearn/> · **Repository:** <https://github.com/buffedlizard55-lab/MasterSelfLearn>

It requires **no manual input**. Every cycle is triggered by
`.github/workflows/think.yml` on `*/30 * * * *` and commits its own output.

---

<!-- AUTO:COUNTS:BEGIN — regenerated every cycle, do not edit -->
| Metric | Value |
|---|---|
| Cycle | **23** |
| Accepted claims in the ledger | **19,851** |
| — schema-v2 strict trace contract | 4,744 |
| — legacy trace contract (reported, not upgraded) | 15,107 |
| — captured from accepted source reads | 13,121 |
| — derived by recorded arithmetic | 6,713 |
| — negative (proof of absence) | 17 |
| Claims rejected by the evidence gate | **0** |
| Derived claims rechecked this cycle | 1,953 |
| Derived claims that no longer recompute | **0** |
| Topics in the library | **151** (new this cycle: 6) |
| Published insights | 408 |
| Forecasts issued this cycle | 1,116 |
| Forecasts scored against outcomes | 684 |
| Ideas in the competition | **28** (promoted: 0) |
| Open irregularities | **27** (new: 0) |
| Sources registered | 31 |
| — verified by a recorded live read | 28 |
| — currently blocked | 3 |
| — never read (not broken, just unprobed) | 0 |
| Reads this cycle (ok / failed) | 64 / 4 |
| Reads planned / refused by the cap | 68 / 0 |
| Forecasts waiting for an observation | 2,552 |
| Forecasts that can never be scored | 0 |
| Bytes read this cycle | 2,231,352 |
| Manual inputs required | **0** |

Generated `2026-09-22T23:28:37Z` by `msl/pipeline.py`. Quoting any figure outside this block
means quoting something the next cycle has already superseded.
<!-- AUTO:COUNTS:END -->

---

## What it actually does

A cycle is seven stages. Each one is a separate module and each one can fail
without stopping the others — a failed stage becomes an entry in the irregularity
register and the cycle still publishes.

| Stage | Module | What it does |
|---|---|---|
| 1. Plan | `msl/tasks.py` | Derives this cycle's reading list from the *current* library, so last cycle's topics get deeper reads now |
| 2. Collect | `msl/http.py` | Reads each URL. Returns bytes or a recorded failure — never a silent empty |
| 3. Verify | `msl/evidence.py` | The gate. A claim without an evidence row, or a derived claim without a lineage, is rejected and the rejection is logged |
| 4. Discover | `msl/topics.py` | Entities found in the payloads become candidate topics; two signals promote a candidate |
| 5. Reason | `msl/reason.py` | Deterministic arithmetic over accepted claims, plus a recheck of every previously published derivation |
| 6. Compete | `msl/strategies.py`, `msl/ideas.py` | Personas forecast the next observation; ideas are scored for robustness and carried forward |
| 7. Learn & publish | `msl/learn.py`, `msl/sitegen.py` | Skill and reliability folded into memory; site and docs regenerated |

## The anti-hallucination contract

1. **No evidence, no claim.** `Ledger.accept` raises unless a `captured`,
   `documented` or `negative` claim cites an evidence row, and unless a `derived`
   claim cites the claim ids and formula it came from. Rejections are counted and
   published, not swallowed.
2. **Unreadable is not unknown.** A conclusive source failure is recorded with
   its HTTP status and reproduction command; no value is attributed to that
   failed response. When an exact-URL hashed seed exists, the engine may publish
   the older projection only as `seed-fallback`, with its original capture time
   and an irregularity — never as a fresh observation.
3. **Yesterday's arithmetic is re-checked today.** Every derived claim is
   recomputed from its recorded inputs each cycle; a mismatch is a drift
   irregularity and both numbers are shown.
4. **Nothing is inferred from a model's memory.** There is no language model in
   the loop and no API key anywhere. Every sentence on the site is a template
   whose slots come from claim values. See `METHODOLOGY.md` §3.
5. **Gaps are printed.** Topics with no accepted claims, families with no source
   that can answer their question, and sources excluded for needing a key are all
   listed on the site with the reason.

## Topic families

| Family | Category | The question it answers | Sources |
|---|---|---|---|
| [AI research frontier](library.html#ai-research-frontier) | Science & ML Research | Which research directions are gaining published evidence fastest? | `arxiv`, `openalex`, `crossref`, `europepmc`, `huggingface`, `federal_register` |
| [Open-source momentum](library.html#open-source-momentum) | Science & ML Research | Which new software is attracting maintainers and stars fastest? | `github_search`, `github_repo`, `github_releases`, `pypi_json`, `npm_registry`, `stackexchange` |
| [Public attention](library.html#public-attention) | Social & Creator Data | What is the public reading about, and is that attention rising or falling? | `wikimedia_pageviews`, `hn_firebase` |
| [Regulatory flow](library.html#regulatory-flow) | Elections & Civic Data | Which policy areas are generating federal rulemaking activity? | `federal_register` |
| [Macro signals](library.html#macro-signals) | Markets & Trading Research | What are the official macro series doing? | `ecb_sdmx`, `frankfurter`, `worldbank`, `bls` |
| [Geohazards](library.html#geohazards) | Science & ML Research | How active is the planet this week, by the survey's own count? | `usgs_fdsn` |
| [San Francisco local conditions](library.html#sf-local) | SF Local Guides | What are the official agencies saying about conditions in San Francisco? | `nws_alerts`, `census_acs` |
| [Clinical evidence](library.html#clinical-evidence) | Health & Personal Guides | Which clinical questions are being actively investigated? | `clinicaltrials`, `pubmed`, `europepmc` |
| [Public health policy](library.html#public-health-policy) | Health & Personal Guides | Where are public-health agencies directing attention? | `pubmed`, `federal_register` |
| [Sports signals](library.html#sports-signals) | Sports Data & Scoreboards | What do the leagues' own public feeds report? | `mlb_statsapi`, `nhl_web`, `nba_cdn`, `kalshi_public` |
| [Market-lab ecosystem](library.html#market-lab-ecosystem) | Markets & Trading Research | How is the prediction-market and paper-trading research ecosystem moving? | `kalshi_public`, `sec_edgar`, `github_search` |
| [Owner corpus](library.html#owner-corpus) | Directory & Meta | How is the owner's own published research corpus growing? | `github_repos` |
| [Travel & Korea](library.html#travel-korea) | Travel & Korea Trip | What can official sources say about Korea travel planning? | `nominatim` |

## The competition

Personas issue falsifiable forecasts about the next observation of a tracked
metric, and are scored the following cycle. The headline number is **skill** —
accuracy minus the accuracy of `S10_Persistence`, which always predicts "no
change". A persona with positive accuracy but non-positive skill has demonstrated
nothing, and the table says so.

| # | Persona | Name | Scored | Accuracy | Skill vs null |
|---|---|---|---|---|---|
| 1 | `S05_EvidenceDensity` | Evidence density | 286 | 52.1% | +11.5 pts |
| 2 | `S01_MomentumPersist` | Momentum persistence | 253 | 50.6% | +9.5 pts |
| 3 | `S07_ChangeHazard` | Change hazard | 69 | 97.1% | +0.0 pts |
| 4 | `S10_Persistence` | Persistence (null model) | 2165 | 87.0% | +0.0 pts |
| 5 | `S06_MemoryWeighted` | Skill-weighted memory | 612 | 32.4% | -25.3 pts |
| 6 | `S04_ConsensusFade` | Consensus fade | 382 | 28.3% | -25.4 pts |
| 7 | `S03_Acceleration` | Acceleration | 386 | 18.7% | -34.7 pts |
| 8 | `S02_MeanRevert` | Mean reversion | 531 | 8.9% | -50.3 pts |

### Unranked

| Persona | Name | Why it is not ranked |
|---|---|---|
| — | — | — |

A persona is ranked only with ≥3 scored
forecasts *and* a scored null model. Below that it is reported `UNRANKED` with the
reason — never shown as 0%, which would present an untested design as a losing one.

## The idea competition

Ideas are generated by a fixed rule set over accepted claims, scored for
robustness (evidence, corroboration, breadth, freshness, reproducibility), and
carried forward. An idea whose support disappears sinks; one that keeps gaining
corroboration is promoted.

| # | Idea | Robustness | Kind | Accepted claims behind it |
|---|---|---|---|---|
| 1 | Track “repo:brayonpi/hexstellar” as a multi-source subject | 0.525 | convergence | 3 |
| 2 | Track “repo:browser-use/jev-ultrafast” as a multi-source subject | 0.525 | convergence | 3 |
| 3 | Track “repo:zai-org/zcode” as a multi-source subject | 0.525 | convergence | 3 |
| 4 | Track “brayonpi/hexstellar” as a multi-source subject | 0.520 | convergence | 3 |
| 5 | Track “browser-use/jev-ultrafast” as a multi-source subject | 0.520 | convergence | 3 |

## What the engine has learned about itself

These are counted, not reflected. Each lesson carries the integers behind it.

| | Lesson |
|---|---|
| `L1` | Topics backed by two or more independent sources have averaged 1.00 signals against 1.00 for single-source topics — a ratio of 1.00×. |
| `L2` | The evidence gate has rejected 0 of 19851 attempted claims (0.00%). |
| `L3` | 133 of 151 tracked topics (88.1%) have at least one accepted claim credit. |
| `L4` | Of 4 idea kinds, “convergence” holds the highest mean robustness (0.491 over 8 ideas). |
| `L5` | 28 of 31 registered sources are reading reliably (EMA ≥ 0.8); 3 are effectively unreadable (EMA < 0.2). |

## Site

| Page | What is on it |
|---|---|
| [`index.html`](index.html) | Today's briefing — the daily page |
| [`library.html`](library.html) | The expanding topic library, family by family |
| [`projects.html`](projects.html) | The evidence-backed MasterSite project catalog and interest map |
| [`leaderboard.html`](leaderboard.html) | Persona competition, forecasts and outcomes |
| [`ideas.html`](ideas.html) | The idea competition, ranked by robustness |
| [`evidence.html`](evidence.html) | Recent claim window with source URL, path, hash and capture time; full history stays in `data/claims.jsonl` |
| [`sources.html`](sources.html) | The source registry, health, and what is excluded and why |
| [`irregularities.html`](irregularities.html) | The flagged-irregularity register |
| [`cycles.html`](cycles.html) | Cycle history and network accounting |
| [`methodology.html`](methodology.html) | How it reasons, and the limits of that |

## Running it

```bash
python3 -m msl.cli cycle              # one full cycle, live network
python3 -m msl.cli cycle --offline    # identical pipeline against data/seed/, no network
python3 -m msl.cli probe              # live-read every registered source, report health
python3 -m msl.cli publish            # re-render site + docs from committed state
python3 -m msl.cli verify-claims      # read-only: recheck derived claims, report drift
python3 -m msl.cli gate-report        # read-only: show what the evidence gate rejected
python3 -m unittest discover -s tests # 334 tests in 13 modules, standard library only
node tools/render_check.js            # render all 10 pages headlessly
```

Python 3.9+, standard library only. No `pip install`, no build step, no keys.

## Repository layout

| Path | Purpose |
|---|---|
| `msl/` | The engine — planning, fetching, the evidence gate, reasoning, competition, learning |
| `data/` | Generated state: ledger, library, memory, leaderboard, ideas, `site.js` |
| `data/seed/` | Hashed first captures. Bootstrap evidence and the offline test corpus |
| `tests/` | `unittest` suite; runs offline against `data/seed/` |
| `tools/` | Read-only verifiers: `probe_sources.py`, `verify_claims.py` |
| `.github/workflows/` | `think.yml` (the timer), `tests.yml`, `probe.yml` |
| `AGENTS.md` | Standing instructions for the next session |
| `METHODOLOGY.md` | The reasoning model and its limits |
| `ROADMAP.md` | What is still to be done, and what is blocking it |
| `VERIFICATION.md` | **Generated** line-by-line audit ledger |
| `IRREGULARITIES.md` | **Generated** register, severity-ordered |
| `STATUS.md` | **Generated** current state of the last cycle |

## Current irregularities

120 registered — 6 critical,
70 warn, 44 info;
27 open, 93 resolved,
21 standing (structural limits that do not auto-resolve).

Full register: [`IRREGULARITIES.md`](IRREGULARITIES.md) or
[`irregularities.html`](irregularities.html).

## Sources

31 registered, 28 verified by a recorded
live read, 3 blocked, 0 never read.
**"Never read" is not "broken"**: it means no recorded probe has reached the
endpoint yet, which is a fact about this project, not a claim about the service.
A source is promoted to `verified-live-read` only by a conclusive complete read
from the cycle or daily probe. Both fold observations into
`data/source_health.json`; the registry itself hard-codes no status.

6 excluded for requiring an API key, each with the
reason recorded in `msl/sources.py`. 4
interest categories have documented missing or partial coverage; no claim is made
beyond the registered source surface.

Full registry and the last recorded probe: [`sources.html`](sources.html).
