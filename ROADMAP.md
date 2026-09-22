# ROADMAP — what is left, and what is blocking it

Everything here is either verified against something that was actually read, or
labelled as an assumption. Nothing on this page is a plan presented as a result.

---

## Done and verified

| | |
|---|---|
| Autonomous cycle on a timer | `.github/workflows/think.yml`, cron `*/30 * * * *`, commits its own output, no manual input |
| Evidence gate with a single door | `msl/evidence.py → Ledger.accept`; rejections counted and published |
| Derived-claim recheck | `msl/reason.py → recheck_derived`; drift becomes an irregularity |
| Source registry with health states | 28 sources, statuses written only by the probe |
| Persona competition scored on skill | 7 personas, null model, qualification rule, forecast log |
| Idea competition with persistence | 6 generator rules, robustness scoring, carry-forward and retirement |
| Memory that changes behaviour | skill weights, source reliability, counted lessons |
| Site | 9 pages, zero dependencies, works from `file://` |
| Test suite | standard library only, runs offline and deterministically |

## Fixed in the 2026-09-22 session

Each of these was found by running the project's own documented checks and
reading what came back, not by inspection. Each has a test that fails when the
defect is reintroduced.

| Defect | How it hid | Fix |
|---|---|---|
| **The probe had never run.** Both copies called `fetch(..., accepts=...)` against a signature taking `accept=`, so both raised `TypeError` on the first source | `probe.yml` ran `... \| tee data/probe.log` with no `pipefail`; a pipeline's status is its last command's, so `tee` succeeded and the step went **green** while the probe read nothing | One shared loop in `msl/probe.py`; both entry points delegate. `set -o pipefail` in `probe.yml` and `think.yml`. 26 tests in `tests/test_probe.py` |
| **Eight sources were advertised as `verified-live-read` from values typed into `msl/sources.py`**, contradicting that module's own "promoted only by the probe, never by hand" | The site rendered them as verified; nothing cross-checked the claim against a recorded read | The registry now hard-codes no probe state. `load_probe_results()` replays `data/source_health.json`, written only by the probe |
| **An egress wall published 22 healthy sources as `blocked`** and minted 38 near-identical irregularities, including 3 CRITICAL escalations against `federal_register` | `EgressBlocked` was folded into the same branch as a real HTTP failure, and `consecutive_failures` (which drives CRITICAL) counted our own outage | Egress is now a *runner* fact: no status change, no escalation, one aggregated finding naming all affected hosts. 7 tests in `tests/test_egress.py` |
| **The README's captured/derived breakdown was wrong**: it reported 8,312 / 306 when the ledger held 5,914 / 2,704 | `derivedClaims` was fed `rep.derived` — this cycle's derivation *delta* — while the template uses it as the ledger *total*, so ~2,400 arithmetic claims were labelled "captured from live payloads" | `derived_total` added and used for the breakdown; the delta is published separately as `derivedThisCycle` |
| **A fourth interest category was missing entirely** | The owner's master directory publishes 10 categories; 9 were represented here, so "Gaming & Guides" was neither served nor reported as a gap — an omission that is not written down is invisible | Added to `INTEREST_CATEGORIES_WITHOUT_A_SOURCE`. All three count-bearing irregularity titles are now computed from their lists, not typed |

`python3 -m msl.cli publish` was added so a template change can be seen without
burning a cycle. Its first version replayed the recorded cycle row reflectively
over camelCase keys against snake_case fields, matched almost nothing, and
published "0 verified claims" with a clean exit code — caught and fixed before
commit, and now guarded by a test that fails on it.

## Next session, in priority order

### 1. Probe every source from a runner with unrestricted egress — *still open*

The probe now runs (it did not before: see "Fixed this session" below), but this
repository's own probe was executed from a sandbox whose egress allowlist reached
only 4 of 28 hosts. The recorded ledger says so explicitly: `egressBlocked: true`,
24 rows with `verdict: false`. **Those 24 sources are unproven, not broken.**

The first `probe.yml` run on a GitHub runner does this automatically. Expect
failures; the likely ones are unchanged from the previous revision of this file:

- `ecb_sdmx` — the `jsondata` structure format nests observations differently
  from the flat shape `adapters.ecb_sdmx` expects. Budget time for this one.
- `arxiv` — Atom namespace handling; `opensearch:totalResults` is easy to miss.
- `sec_edgar` — requires a User-Agent declaring a contact; the engine sends one,
  but SEC returns 403 to generic agents.
- `bls` — keyless use is capped at 25 queries/day per IP; a shared Actions runner
  IP may already be exhausted.
- `kalshi_public`, `mlb_statsapi`, `nhl_web`, `nba_cdn` — undocumented endpoints
  with no contract, so a shape change is silent until it is not.

Do not mark a source `verified-live-read` by hand, and do not "fix" the 24
`registered` rows by editing `msl/sources.py` — the registry now hard-codes no
status at all, and `load_probe_results()` replays `data/source_health.json` at
import. The only way to move a status is to run the probe.

**Adapters for the 24 unprobed sources have still never met a real payload.**
They are unit-tested against hand-built payloads only. This is the single most
important open item and it cannot be closed from a sandbox.

### 2. Give the competition something that actually moves

On the static seed corpus every metric is unchanged, so the null model scores
100% and every other persona scores ≤ 0. That is honest but it is not a
competition. Two live cycles with moving series are needed before any skill number
means anything. Until then the leaderboard page should keep saying "no persona
qualifies yet", and it does.

### 3. Backfill the attention signal

Only one Wikipedia article is tracked (`Artificial_intelligence`), because that
is the only pageview capture in the seed set. `msl/tasks.py` already expands to
every tracked `wiki:` topic, so this grows on its own — but the discovery stage
does not currently *propose* new Wikipedia articles. Add a rule that maps a
high-signal GitHub repository or Federal Register agency to a Wikipedia article
title, then verify the article exists before adding it. An article that 404s must
produce a `negative` claim, not a silent drop.

### 4. Close or formally drop the three unserved interest categories

Travel & Korea Trip, Social & Creator Data and Elections & Civic Data appear in
the owner's verified corpus and have no source that can serve them. Each needs a
decision:

- **Travel** — no official keyless pricing API exists. Realistic options: publish
  only what `nominatim` can verify (that a place exists and where it is) and
  retire the pricing question, or accept a keyed source as manual input.
- **Social/creator** — every official API is keyed. There is no honest path
  without a key. Recommend retiring the category rather than scraping.
- **Elections** — `federal_register` covers federal rulemaking. State results are
  per-jurisdiction; the FEC API needs a key for most routes. Partial coverage is
  achievable and should be labelled partial.

### 5. Retire topics that never earn evidence

`CYCLES_BEFORE_RETIREMENT` is 96 cycles (~2 days). The discovery stage proposes up
to 6 candidate topics a cycle, so without retirement the library fills with
candidates that never produce a claim. Verify the retirement path actually fires
after a few days of live running — it has never been exercised on real data.

### 6. Add a real forecast target with a knowable outcome

The current target is "does this metric move up or down next cycle", which is
weak: on most series the honest answer is "no". Stronger targets, in rough order
of value:

- **Federal Register publication dates.** A document's `publication_date` is
  known in advance from `public_inspection_pdf_url`. Predicting it is falsifiable
  against a fixed official record.
- **PyPI/npm next release within N days.** Verifiable from the registry.
- **USGS event counts in a forward window.** Verifiable from the same endpoint.

Each needs an adapter change and a scoring rule. None exists yet.

## Limitations that are not fixable without manual input

| Limitation | Why |
|---|---|
| No language model in the reasoning loop | A model needs an API key; a key is manual input |
| Six useful sources excluded | FRED, NFL Game API, Google Trends, X, YouTube Data, TikTok/Instagram — all keyed |
| No creator/social signal at all | Every official creator API requires an approved developer application |
| The owner's ChatGPT transcript is not machine-readable | Client-side rendered; only the `<title>` is served. Any requirement in it that is missing here is missing |
| No live execution proof in this repository | The sandbox egress allowlist blocked every source except GitHub, PyPI and npm. The first Actions run is the proof |

## Deliberate non-goals

- **No scraping.** If there is no official endpoint, the topic has no signal. A
  scraped number cannot be traced to a contract, which defeats the whole design.
- **No backfilled history.** The ledger starts at the first cycle. Inventing a
  plausible past would be the exact failure mode this project exists to avoid.
- **No manual data entry.** `tools/overlay.json`-style hand-authored narrative, as
  used by the sibling `MasterSite`, is deliberately absent here. Every sentence
  the site prints is generated from the ledger.
