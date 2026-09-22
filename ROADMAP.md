# ROADMAP — completed scope, remaining work, and blockers

This is a limitations ledger, not a wish list presented as a result. Current
cycle counts live in [`STATUS.md`](STATUS.md); claim and source details live in
[`VERIFICATION.md`](VERIFICATION.md). Both are regenerated from state so this
file does not duplicate figures that will be stale after the next scheduled run.

---

## Delivered and mechanically checked

| Requirement | Implemented result | Where to verify |
|---|---|---|
| Run without manual input | A serialized GitHub Actions writer runs every 30 minutes; a daily probe shares the same lock | `.github/workflows/think.yml`, `.github/workflows/probe.yml` |
| Research new and trending subjects | Date-relative official/public searches, scholarly feeds, registries, government data, sports feeds, and public-attention signals | `msl/tasks.py`, `msl/sources.py`, `cycles.html` |
| Build an expanding expert library | Payload entities become candidate topics, repeated signals promote them, accepted claims credit them, and later plans deepen them | `msl/topics.py`, `library.html` |
| Learn from previous cycles and ideas | Source reliability, persona skill, topic interest, lessons, forecasts, and idea lineage persist and affect later cycles | `msl/learn.py`, `msl/ideas.py`, `data/memory.json` |
| Run competing strategies | Eight deterministic personas, including a persistence null, issue falsifiable forecasts; ranking uses paired same-target skill | `msl/strategies.py`, `leaderboard.html` |
| Evaluate idea robustness | Evidence, independent corroboration, breadth, seven-day freshness, and reproducibility are rescored each cycle from terminal evidence | `msl/ideas.py`, `ideas.html` |
| Verify before publishing | Schema-v2 captured claims require a complete successful evidence row, matching source and URL, integrity hash, stable field, exact declared source path, and strict JSON value | `msl/evidence.py`, `tests/test_gate.py` |
| Preserve line-level review links | The site publishes a recent claim window with URL, path, time, lineage, and integrity class; the complete append-only record remains in JSONL | `evidence.html`, `data/claims.jsonl`, `data/evidence.jsonl` |
| Flag irregularities | Failures, malformed payloads, coverage gaps, drift, stale fallbacks, and structural limitations receive persistent IDs and reproduction steps | `irregularities.html`, `IRREGULARITIES.md` |
| Reflect the owner's interests | The readable MasterSite catalog is decoded through the evidence gate, Git blob SHA checked, and shown as 52 linked projects across its categories | `projects.html`, `data/seed/master_site_catalog.json` |
| Provide a daily one-stop site | Ten dependency-free, accessible static pages render from one generated payload and work without runtime API calls | root HTML files, `app.js`, `tools/render_check.js` |
| Bound unattended execution | Reads are paced by host, response size and task growth are capped, HTTP 4xx is not hammered, and a cycle defers work after its network budget rather than dying mid-write | `msl/http.py`, `msl/config.py`, `msl/pipeline.py` |

## The three cumulative review passes

### Pass 1 — implementation and baseline verification

The engine, evidence gate, library, reasoning, competition, generated site, source
registry, and unattended workflows were exercised end to end. An isolated offline
cycle proved that every fixture could pass through plan → collect → gate → reason
→ compete → publish with no network or manual input.

### Pass 2 — adversarial bug and edge-case review

The review corrected, among other findings:

- historical projection hashes that had been labelled as wire-verifiable;
- duplicate derived conclusions and derivations duplicated across cycles;
- malformed-success responses that could be mistaken for usable collections;
- caller-generated 4xx, local response caps, and runner egress being misreported
  as evidence that somebody else's service was down;
- competing personas compared with a differently mixed null-model sample;
- idea freshness inflated by derived rows rather than terminal observations;
- stale or hard-coded dates, a non-owner-local MLB date, and quota-bypassing BLS
  probes;
- wrong ECB and NHL payload assumptions;
- generated-file races between the half-hour cycle and daily probe;
- accepted/strict/legacy counts that described different populations as one; and
- a project catalog that had previously been imported by the browser rather than
  accepted as evidence.

Each corrected behavior has a regression test or a read-only verifier check.

### Pass 2b — the 2026-09-22 continuity audit

A second adversarial review of the *published artefacts* (not just the code)
found and fixed five defects, each verified against the committed ledger before
the fix was written:

1. **Probe/survey URL collision.** Probes were planned before surveys and the
   dedup keyed on `source_id|url`, so for nominatim, nws_alerts, census_acs and
   nhl_web — whose availability probe and only family survey are the same GET —
   the probe won and every fact was filed under the maintenance topic
   `source-health`. The `travel-korea` and `sf-local` families spent all 22
   cycles at zero claims while being read every cycle, and the register kept
   flagging them as unsupported. Surveys now win the collision and the probe
   stands down for that URL (`msl/tasks.py`); source health is folded from
   every read of a registered source, so no availability signal was lost.
2. **Blended claim counts.** The Library published
   `max(persisted credit, row-provable count)` per topic — a number that is
   neither population and whose total (23,049) matched no auditable quantity.
   It now publishes `verifiedClaims` (recomputes from `claims.jsonl`) and
   `creditedClaims` (pre-schema-v2 history) separately, with the difference
   disclosed on the page and in one aggregated irregularity.
3. **Self-contradicting register.** IRR-042 computed "unsupported" from
   row-provable counts while its own repro command counted persisted credit —
   two different populations, so it named topics with up to 62 claim credits as
   having "zero verified claims". Both now call
   `pipeline.unsupported_topic_report`, exposed as
   `python3 -m msl.cli unsupported-topics`; the truly-unsupported list fell
   from 25 to 6 and the 19 credit-only topics are disclosed as their own class.
4. **Vacuous lesson.** L1 bucketed corroboration by `c.topic` alone; only
   family slugs matched, every family has one signal, and the README published
   "1.00 signals against 1.00 signals — a ratio of 1.00×" as a learned rule.
   L1 now buckets by topic+subjects (derived excluded) and reports what the
   counts actually show: corroborated topics hold ~17× more claim rows but not
   more signals.
5. **Frozen dates in registry probe URLs** (`created:>=2026-09-14`,
   `starttime=2026-09-14`, `date=2026-09-20`). The MLB probe re-read one
   fixed day's schedule every cycle. Probe URLs are now date templates
   rendered against the read's own clock, owner-timezone-aware for MLB, and a
   test sweeps every planned URL for dates the plan did not compute.

Additionally the Library detail panel now matches claims by topic **or**
subject (127 of 132 entity topics previously showed "no accepted claim" under a
badge carrying 60+ claims), and Travel & Korea is honestly *active with
disclosed partial coverage* instead of `blocked-no-source` while nominatim
reads it every cycle. Sixteen new regression tests cover all of the above.

### Pass 3 — original-request and publication audit

The final audit checked all ten rendered pages and the complete written request.
It additionally corrected negative library accounting, stale source-health
wording, partial-interest coverage presented as wholly unserved, pinned
irregularity titles that could never update, HTTP 4xx retry hammering, generic 403
responses falsely called rate limits, and unbounded collection time. Documentation
now distinguishes a fresh live read, an explicitly stale seed fallback, exact wire
integrity, projection-only integrity, strict schema-v2 claims, and legacy claims.

---

## Remaining work and blockers, in priority order

### 1. Historical evidence cannot be upgraded retroactively

Cycles before the strict capture contract usually retained a canonical projection
hash but not the exact response bytes. Those rows remain accepted legacy evidence
and are labelled `projection`; they are **not** relabelled as wire-verifiable. A
future read can establish integrity for a new observation, but it cannot prove the
bytes received in an old cycle. The verifier reports strict and legacy populations
separately.

**Recommendation:** let strict schema-v2 observations grow naturally and never
rewrite old rows. If long-term storage becomes available, retain compressed raw
bodies for new reads under an explicit size/retention policy.

### 2. The shared ChatGPT transcript is not machine-readable here

The supplied share URL exposes only an HTML shell and the title “Design Autonomous
Research System”; its transcript could not be retrieved. No unseen requirement is
claimed as reviewed. The written request and the readable MasterSite corpus are the
only owner requirements used.

**Blocker:** only the share service or the owner can make that transcript available
as readable text. Importing it would be manual input, so the autonomous engine does
not wait for it.

### 3. Live availability is point-in-time, not a service SLA

The source ledger reports what a particular runner conclusively read. Some prior
reads returned 403 from ClinicalTrials.gov, the NBA CDN, or SEC EDGAR while an
independent read of at least some of those endpoints later succeeded. A 403 is
therefore reported as that request's result, not a universal claim that the service
is down. Runner egress, malformed caller requests, and local response caps produce
an explicit **no verdict** instead.

**Recommendation:** inspect the first post-merge daily probe and subsequent live
cycles. Do not hand-edit a source to “verified”; only a complete recorded read may
move it there.

### 4. Four interest areas still have missing or partial official/keyless coverage

- **Travel & Korea Trip:** place geocoding is available; airfare and lodging prices
  are not available from a confirmed official keyless API.
- **Social & Creator Data:** Wikimedia and Hacker News cover public attention;
  official creator-platform metrics require approved/keyed APIs.
- **Elections & Civic Data:** federal rulemaking is covered; election results are
  jurisdiction-specific and major federal interfaces are keyed.
- **Gaming & Guides:** no sufficiently documented, confirmed source has been
  registered.

The site shows those as coverage gaps rather than filling them with scraped or
invented values.

**Recommendation:** prefer honest partial coverage. Add a source only after a live
read and documentation review; otherwise leave the gap open.

### 5. GitHub's scheduler is best effort

The workflow requests a run every 30 minutes, but GitHub documents that scheduled
runs may be delayed or dropped under load. Repository code cannot provide a hard
real-time or “never stops” SLA on a hosted scheduler. The cycle timeline makes gaps
visible, and the state-writer lock prevents overlapping writes.

**Recommendation:** if a hard SLA becomes necessary, mirror the same keyless CLI on
a supervised external runner. That is infrastructure work, not a claim this
repository can satisfy by itself.

### 6. Some public feeds have weaker contracts

MLB, NHL, and NBA public feeds are operator-hosted but lack a located stable public
contract; Frankfurter is a third-party ECB mirror; GitHub has no official trending
API. Every affected source is assigned an explicit provenance/trust tier and the
substitution is disclosed.

**Recommendation:** keep adapter shape tests and the daily probe. Retire a feed if
its operator contract or provenance can no longer be stated honestly.

### 7. The forecast problem can become more substantive

Direction-of-next-observation is falsifiable but often rewards “flat.” Paired skill
prevents that baseline from looking impressive, yet stronger targets would improve
research value.

Suggested additions, only after an official outcome route is confirmed:

1. package release within a fixed forward window;
2. Federal Register publication-date outcomes;
3. USGS counts in a predeclared future window; and
4. sports outcomes tied to a documented league record.

Each new target must define its outcome before issuance, score only against a later
cycle, and include a same-target null forecast.

---

## Deliberate non-goals

- **No unsupported scraping.** An attractive number without stable provenance is
  worse than a visible gap.
- **No invented history.** The ledger starts where observations start.
- **No secret-dependent model.** The current “reasoning” is deterministic,
  testable rule execution. A language model would require a key, add nondeterminism,
  and need a separate evidence-constrained design; it is not silently simulated.
- **No manual source-status edits.** Availability comes from recorded reads.
- **No absolute hallucination claim.** The verifier can prove schema, lineage,
  integrity metadata, and deterministic arithmetic within the retained record. It
  cannot reconstruct response bytes that old cycles did not save or prove that an
  external source itself was correct. Those limits remain visible.

## Next-session checklist

1. Review Actions and Pages after several scheduled live cycles. In particular,
   confirm the first live cycle after the 2026-09-22 fixes credits
   `travel-korea` and `sf-local` with claim rows (the survey now wins the
   probe/survey URL collision) and that IRR-042's unsupported list shrinks to
   the honest remainder.
2. Investigate any new open critical irregularity before adding sources or ideas.
3. Watch strict-v2 and wire-integrity proportions grow; never “upgrade” legacy
   rows, and never blend `verifiedClaims` with `creditedClaims` (see AGENTS.md
   trap table).
4. Add a stronger forecast target only with an official, later-cycle outcome.
5. Re-run the full suite, render check, strict JSON/JSONL parse, claim verifier,
   and an isolated offline cycle before the next merge.
