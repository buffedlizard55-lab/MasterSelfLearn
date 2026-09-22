# AGENTS.md — Standing Instructions for MasterSelfLearn

Read this before editing, auditing, or regenerating anything in this repository.

---

## 1. The one rule that outranks everything else

**Nothing is published without an evidence row.**

`msl/evidence.py → Ledger.accept` is the only door into the claim ledger. It
rejects a `captured`, `documented` or `negative` claim with no evidence row, and a
`derived` claim with no `computedFrom` lineage or `formula`. Do not:

- add a second door (a direct append to `data/claims.jsonl`);
- widen the gate to accept a claim "when we are confident";
- delete the `rejections` counter — a permanent zero there is suspicious, not
  reassuring.

If a number cannot be traced to a URL that was actually read, it does not go on
the site. It goes in the irregularity register as a gap instead.

## 2. Do not "fix" the counts

`README.md` has an `AUTO:COUNTS` block between
`<!-- AUTO:COUNTS:BEGIN -->` and `<!-- AUTO:COUNTS:END -->`. It is regenerated
every cycle by `msl/docs.py`. Never edit a number inside it, and never quote a
figure from outside it — the next cycle has already superseded it.

Same for `STATUS.md`, `VERIFICATION.md` and `IRREGULARITIES.md`: all four are
generated. Edit the generator, not the output.

## 3. The data files are append-only

`data/claims.jsonl`, `data/evidence.jsonl` and `data/cycles.jsonl` are histories.
Appending is the only legal write. A derived claim that no longer recomputes gets
a **new** row plus a drift irregularity; it is never edited in place, because
"we corrected the number" is not auditable and "here are both numbers" is.

`data/library.json`, `data/memory.json`, `data/ideas.json`,
`data/leaderboard.json`, `data/irregularities.json` and `data/site.js` are
regenerated in full each cycle. They may be deleted safely; the JSONL files may
not.

`data/source_health.json` is the exception among the regenerable files: both the
live cycle and daily probe fold conclusive observations into this one shared
ledger under the same workflow writer lock. It is the sole record of endpoint
availability. `msl/sources.py` replays it at import, so deleting it does not lose
a claim — it correctly demotes every source back to `registered` until a later
recorded read.

## 4. `data/seed/` is bootstrap evidence, not fixtures

These are dated captures or canonical projections with SHA-256 integrity
metadata. Their `captureMode` and `wireHashVerifiable` fields say which; do not
call a projection a wire response. They serve two purposes:

1. the first cycle has something true to build on;
2. `--offline` and the test suite run the identical pipeline with no network.

Two rules:

- **A projection must keep the raw field names the adapter reads.** This already
  went wrong once: a projection stored `stars` where `msl/adapters.gh_search`
  reads `stargazers_count`, the adapter got `None`, and the ledger published
  "0 stars" for every repository. The adapters now refuse to record a 0 and raise
  a shape problem instead. Keep it that way.
- **An interactive or API-decoded projection is not wire-verifiable.** Such rows
  carry modes including `agent-fetch-page-transcribed` or `gh-api-projection` and
  `wireHashVerifiable: false`. Do not upgrade that flag. A later automated read
  is a new observation; it cannot retroactively prove old response bytes.

## 5. A failed response produces no fresh claim

A conclusive source-side failure is recorded with its HTTP status and reproduction
command and may mark the source `blocked`. Caller-generated 400/404/405/422,
runner egress, and the local response-size cap produce **no source-health verdict**
because they do not establish that the service is down. No value may be attributed
to the failed response.

One exception, already implemented and loudly labelled: when a source is
unreadable and a seed capture exists for that exact URL, the seed is used and
every resulting claim is marked `captureMode=seed-fallback`, plus a warn
irregularity naming the substitution. That is a bootstrap, not a fresh read.

A TLS/SSL EOF on *every* host is an egress policy, not broken data. Check that
before treating a wall of failures as a finding.

**`EgressBlocked` must never move a source's status.** `msl/http.fetch` tags a
read `EgressBlocked` when the TLS session is torn down before any HTTP status
arrives. That is a fact about the machine running the cycle, not about the
service, so:

- the probe records the row with `verdict: false` and leaves `statusAfter`
  untouched;
- the pipeline adds the source to one aggregated irregularity instead of marking
  it `blocked`, and does **not** increment `consecutive_failures` (that counter
  drives the CRITICAL escalation, so an egress blip would otherwise manufacture
  critical findings about other people's APIs);
- a conclusive HTTP failure such as 403 or 5xx still affects source health;
  caller-generated 400/404/405/422 does not. Do not widen either category without
  proving what the status says about source availability.

These behaviors are covered by `tests/test_egress.py` and pipeline health tests.

## 6. The competition's honesty rules

- A persona needs `MIN_SCORED_FORECASTS_TO_RANK` (3) scored forecasts **and** a
  scored null model before it is ranked. Below that it is `UNRANKED` **with the
  reason**. Never show an untested persona at 0% — that presents a design which
  never traded as a losing one.
- The headline number is **skill** = accuracy − accuracy of `S10_Persistence`,
  which always predicts "no change". Accuracy alone flatters any persona on a
  series dominated by no-change.
- `S06_MemoryWeighted` may only weight personas that have a recorded skill. If
  `memory.strategyWeights` is empty it issues nothing. Do not give it a default
  weight.
- A forecast is scored only against an observation from a **later** cycle.
  Scoring a forecast against its own cycle is cheating and the test suite fails
  on it.

## 7. Irregularity register

Entries are keyed by fingerprint, so the same finding keeps the same `IRR-nnn`
across cycles. A non-standing entry that stops recurring is marked `resolved`,
never deleted.

**Standing** entries are structural limits (no language model in the loop; GitHub
has no trending API; documented interest-category coverage gaps; the owner's
shared document is not machine-readable). They do not auto-resolve, because the
owner needs to keep seeing them. Do not clear them by hand.

Aggregate rather than spam: one warn naming N unsupported topics, not N warns.
A register with 400 identical rows hides the three that matter.

## 8. There is no language model in this loop, on purpose

No API key, no secret, no model client. Every sentence on the site is a template
whose slots come from claim values; every idea comes from a fixed rule set over
the ledger. That costs novelty and buys auditability. Adding a model would need a
secret, and adding a secret is manual input, which the brief rules out. If the
owner ever supplies a key, that is a deliberate change and it belongs in
`METHODOLOGY.md` §3 first.

## 9. Standard library only

No `requirements.txt`, no `pyproject.toml`, no `setup.py`. `tests.yml` fails the
build if one appears. The site has no build step either: plain
`index.html` + `styles.css` + `app.js` + one generated `data/site.js`, which is
why it works from `file://` as well as from Pages.

## 10. Verify before you claim done

```bash
python3 -m msl.cli selftest            # the gate must reject — this is not optional
python3 -m unittest discover -s tests  # full suite, offline, deterministic
python3 -m msl.cli cycle --offline     # rebuild every artifact with no network
python3 -m msl.cli publish             # re-render site+docs from committed state
python3 tools/verify_claims.py         # read-only: recheck derived claims
python3 tools/probe_sources.py         # live-read every source (needs egress)
node tools/render_check.js             # render all 10 pages headlessly
```

`tools/probe_sources.py` exits non-zero when it could not do its job — nothing
attempted, nothing reachable, or most of the registry inconclusive because the
runner had no egress. Per-source failures are *results* and do not fail it.

If you change a template, `publish` shows it without spending a cycle. It must
reproduce the counts the cycle published; if a republish ever reports zero or a
negative figure for a ledger that holds claims, it is the republish that is
broken. `tests/test_site.py::Republish` asserts exactly that.

A clean exit code is not a pass when the output is wrong. Read the counts. If
`claims new` is 0 while reads succeeded, or every star count is 0, something is
reading nothing — find it before committing.

## 11. Known traps that have already bitten

| Trap | Symptom | Fix that is already in place |
|---|---|---|
| `dataclass` field named `field` | `TypeError: 'str' object is not callable` at import | `evidence.py` / `adapters.py` call `dataclasses.field(...)` explicitly |
| Regex `[a-z_]+\[` cannot cross a dot | every derived rule silently produced nothing | `_INDEXED` allows `[A-Za-z_.]+` |
| Index-based field names | two different repositories shared one field name | fields are keyed by repository name |
| `derived` counted as a source | every entity looked corroborated by two sources | corroboration skips `source_id == "derived"` |
| Local `room` counter in `_discover` | ~108 new topics per cycle instead of 6 | budget list shared across the cycle |
| Unrounded recompute vs rounded stored value | false drift on every trend claim | `_recompute` rounds to 4 dp like `derive` |
| npm dist-tags `Accept` header | HTTP 406 with the registry's own documented media type | `Accept: application/json`, recorded as IRR |
| Two copies of the probe, both calling `fetch(accepts=…)` | `TypeError` on source #1; `probe.yml` still went green and nothing was ever probed | One loop in `msl/probe.py`; entry points delegate; `set -o pipefail` in both workflows |
| `cmd \| tee log` in a workflow step | the step's status is `tee`'s, so a crash exits 0 and looks like a pass | `set -o pipefail` before any piped command |
| Hand-typed `status="verified-live-read"` in the registry | the site advertised verified sources no code had ever read | registry hard-codes no status; `load_probe_results()` replays the shared cycle/probe health ledger |
| `EgressBlocked` treated as a source failure | 22 healthy services published as `blocked`, 3 CRITICAL findings invented | egress is a runner fact: no status change, no escalation, one aggregated finding |
| A per-cycle delta used where a total belongs | README reported 8,312 captured / 306 derived for a ledger holding 5,914 / 2,704 | `derived_total` for the breakdown, `derivedThisCycle` for the delta |
| Reflective `setattr` from a JSON row | camelCase keys vs snake_case fields matched nothing; every figure silently defaulted to 0 | map recorded keys explicitly; `republish` recomputes totals from the ledger |
| A count typed into a title ("Three categories…") | the number went stale when the list grew | compute counts from the list; pin the fingerprint so the IRR id survives |
