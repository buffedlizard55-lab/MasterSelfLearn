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
| Cycle | **16** |
| Verified claims in the ledger | **13,388** |
| — captured from live payloads | 9,031 |
| — derived by recorded arithmetic | 4,357 |
| — negative (proof of absence) | 0 |
| Claims rejected by the evidence gate | **0** |
| Derived claims rechecked this cycle | 40 |
| Derived claims that no longer recompute | **0** |
| Topics in the library | **109** (new this cycle: 6) |
| Published insights | 357 |
| Forecasts issued this cycle | 1,036 |
| Forecasts scored against outcomes | 620 |
| Ideas in the competition | **14** (promoted: 0) |
| Open irregularities | **30** (new: 1) |
| Sources registered | 30 |
| — verified by a recorded live read | 23 |
| — currently blocked | 5 |
| — never read (not broken, just unprobed) | 2 |
| Reads this cycle (ok / failed) | 63 / 7 |
| Reads planned / refused by the cap | not recorded / not recorded |
| Forecasts waiting for an observation | not recorded |
| Forecasts that can never be scored | not recorded |
| Bytes read this cycle | 1,804,907 |
| Manual inputs required | **0** |

Generated `2026-09-22T12:45:18Z` by `msl/pipeline.py`. Quoting any figure outside this block
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
| 5. Reason | `msl/reason.py` | Deterministic arithmetic over verified claims, plus a recheck of every previously published derivation |
| 6. Compete | `msl/strategies.py`, `msl/ideas.py` | Personas forecast the next observation; ideas are scored for robustness and carried forward |
| 7. Learn & publish | `msl/learn.py`, `msl/sitegen.py` | Skill and reliability folded into memory; site and docs regenerated |

## The anti-hallucination contract

1. **No evidence, no claim.** `Ledger.accept` raises unless a `captured`,
   `documented` or `negative` claim cites an evidence row, and unless a `derived`
   claim cites the claim ids and formula it came from. Rejections are counted and
   published, not swallowed.
2. **Unreadable is not unknown.** A source that fails produces a recorded failure
   with its HTTP status and a reproduction command. It never produces a
   substitute value, and it is marked `blocked` so no claim can be built from it.
3. **Yesterday's arithmetic is re-checked today.** Every derived claim is
   recomputed from its recorded inputs each cycle; a mismatch is a drift
   irregularity and both numbers are shown.
4. **Nothing is inferred from a model's memory.** There is no language model in
   the loop and no API key anywhere. Every sentence on the site is a template
   whose slots come from claim values. See `METHODOLOGY.md` §3.
5. **Gaps are printed.** Topics with no verified claims, families with no source
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
| 1 | `S10_Persistence` | Persistence (null model) | 1450 | 87.8% | +0.0 pts |
| 2 | `S05_EvidenceDensity` | Evidence density | 101 | 68.3% | -19.5 pts |
| 3 | `S01_MomentumPersist` | Momentum persistence | 101 | 68.3% | -19.5 pts |
| 4 | `S03_Acceleration` | Acceleration | 164 | 30.5% | -57.3 pts |
| 5 | `S04_ConsensusFade` | Consensus fade | 164 | 28.0% | -59.7 pts |
| 6 | `S06_MemoryWeighted` | Skill-weighted memory | 274 | 26.3% | -61.5 pts |
| 7 | `S02_MeanRevert` | Mean reversion | 268 | 1.1% | -86.7 pts |

### Unranked

| Persona | Name | Why it is not ranked |
|---|---|---|
| — | — | — |

A persona is ranked only with ≥3 scored
forecasts *and* a scored null model. Below that it is reported `UNRANKED` with the
reason — never shown as 0%, which would present an untested design as a losing one.

## The idea competition

Ideas are generated by a fixed rule set over verified claims, scored for
robustness (evidence, corroboration, breadth, freshness, reproducibility), and
carried forward. An idea whose support disappears sinks; one that keeps gaining
corroboration is promoted.

| # | Idea | Robustness | Kind | Verified claims behind it |
|---|---|---|---|---|
| 1 | Watch for research lagging rulemaking on “artificial intelligence” | 0.400 | regulatory-lead | 12 |
| 2 | Replicate what made NandhaKishorM/laya grow | 0.400 | velocity-outlier | 10 |
| 3 | Watch for research lagging rulemaking on “reasoning” | 0.325 | regulatory-lead | 9 |
| 4 | Watch for research lagging rulemaking on “agent” | 0.325 | regulatory-lead | 9 |
| 5 | Watch for research lagging rulemaking on “model” | 0.325 | regulatory-lead | 9 |

## What the engine has learned about itself

These are counted, not reflected. Each lesson carries the integers behind it.

| | Lesson |
|---|---|
| `L1` | Topics backed by two or more independent sources have averaged 1.00 signals against 1.00 for single-source topics — a ratio of 1.00×. |
| `L2` | The evidence gate has rejected 0 of 13388 attempted claims (0.00%). |
| `L3` | 12 of 109 tracked topics (11.0%) have at least one verified claim. |
| `L4` | Of 2 idea kinds, “velocity-outlier” holds the highest mean robustness (0.333 over 3 ideas). |
| `L5` | 23 of 28 registered sources are reading reliably (EMA ≥ 0.8); 4 are effectively unreadable (EMA < 0.2). |

## Site

| Page | What is on it |
|---|---|
| [`index.html`](index.html) | Today's briefing — the daily page |
| [`library.html`](library.html) | The expanding topic library, family by family |
| [`leaderboard.html`](leaderboard.html) | Persona competition, forecasts and outcomes |
| [`ideas.html`](ideas.html) | The idea competition, ranked by robustness |
| [`evidence.html`](evidence.html) | Every claim with its source URL, hash and capture time |
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
python3 -m unittest discover -s tests # 293 tests in 12 modules, standard library only
node tools/render_check.js            # render all 9 pages headlessly
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

105 registered — 6 critical,
58 warn, 41 info;
30 open, 75 resolved,
15 standing (structural limits that do not auto-resolve).

Full register: [`IRREGULARITIES.md`](IRREGULARITIES.md) or
[`irregularities.html`](irregularities.html).

## Sources

30 registered, 23 verified by a recorded
live read, 5 blocked, 2 never read.
**"Never read" is not "broken"**: it means no recorded probe has reached the
endpoint yet, which is a fact about this project, not a claim about the service.
A source is promoted to `verified-live-read` only by `msl/probe.py`, which writes
`data/source_health.json` and nothing else — the registry itself hard-codes no
status.

6 excluded for requiring an API key, each with the
reason recorded in `msl/sources.py`. 4
interest categories have no registered source that can serve them, and no claim
is made about them.

Full registry and the last recorded probe: [`sources.html`](sources.html).
