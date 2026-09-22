"""Documentation generation.

``README.md``, ``STATUS.md``, ``VERIFICATION.md`` and ``IRREGULARITIES.md`` are
all generated from the same objects the site is generated from, so the prose and
the site cannot disagree.  Every number in them is read out of the ledger, the
library, the register or the registry — a figure that cannot be read from one of
those is not printed.

The ``AUTO:COUNTS`` block at the top of ``README.md`` is machine-regenerated on
every cycle and is the only place a number should be quoted from.
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List, Optional

from . import config
from .evidence import Ledger
from .irregularities import ORDER, Register
from .pipeline import CycleReport
from .sources import (INTEREST_CATEGORIES_WITHOUT_A_SOURCE, KEYED_SOURCES_EXCLUDED,
                      REGISTRY)
from .topics import FAMILIES, Library

BEGIN = "<!-- AUTO:COUNTS:BEGIN — regenerated every cycle, do not edit -->"
END = "<!-- AUTO:COUNTS:END -->"


def render_all(d: pathlib.Path, now: str, rep: CycleReport, ledger: Ledger,
               library: Library, memory: Dict[str, Any], register: Register,
               lb: Dict[str, Any], docs_dir: Optional[pathlib.Path] = None) -> None:
    """Regenerate the four markdown documents.

    ``d`` is the data directory (read for ideas.json); ``docs_dir`` is where the
    markdown is written, which is the repository root — these are documents about
    the project, not cycle state, and GitHub renders them on the repo front page.
    """
    out = pathlib.Path(docs_dir or config.ROOT)
    out.mkdir(parents=True, exist_ok=True)
    ac = rep.auto_counts()
    _write_readme(out, d, now, rep, ac, ledger, library, memory, register, lb)
    _write_status(out, now, rep, ac, ledger, library, memory, register)
    _write_verification(out, now, rep, ac, ledger, library, register)
    _write_irregularities(out, now, rep, register)


def _counts_table(ac: Dict[str, Any]) -> str:
    rows = [
        ("Cycle", f"**{ac['cycle']}**"),
        ("Verified claims in the ledger", f"**{ac['claims']:,}**"),
        ("— captured from live payloads", f"{ac['claims'] - ac['derivedClaims']:,}"),
        ("— derived by recorded arithmetic", f"{ac['derivedClaims']:,}"),
        ("Claims rejected by the evidence gate", f"**{ac['claimsRejectedByGate']:,}**"),
        ("Derived claims rechecked this cycle", f"{ac['derivedRechecks']:,}"),
        ("Derived claims that no longer recompute", f"**{ac['derivedDrifts']}**"),
        ("Topics in the library", f"**{ac['topics']:,}** (new this cycle: {ac['newTopics']})"),
        ("Published insights", f"{ac['insights']:,}"),
        ("Forecasts issued this cycle", f"{ac['forecastsIssued']:,}"),
        ("Forecasts scored against outcomes", f"{ac['forecastsScored']:,}"),
        ("Ideas in the competition", f"**{ac['ideas']:,}** (promoted: {ac['ideasPromoted']})"),
        ("Open irregularities", f"**{ac['irregularitiesOpen']:,}** (new: {ac['irregularitiesNew']})"),
        ("Sources registered", f"{ac['sourcesRegistered']}"),
        ("— verified by a recorded live read", f"{ac['sourcesVerified']}"),
        ("— currently blocked", f"{ac['sourcesBlocked']}"),
        ("— never read (not broken, just unprobed)", f"{ac['sourcesNeverRead']}"),
        ("Reads this cycle (ok / failed)", f"{ac['fetchOk']} / {ac['fetchFailed']}"),
        ("Bytes read this cycle", f"{ac['bytesIn']:,}"),
        ("Manual inputs required", "**0**"),
    ]
    return "\n".join(f"| {k} | {v} |" for k, v in rows)


def _write_readme(out: pathlib.Path, d: pathlib.Path, now: str, rep: CycleReport,
                  ac: Dict[str, Any], ledger: Ledger, library: Library,
                  memory: Dict[str, Any], register: Register,
                  lb: Dict[str, Any]) -> None:
    counts = register.counts()
    ranked = lb.get("ranked", [])
    top_ideas = []
    p = d / "ideas.json"
    if p.exists():
        try:
            top_ideas = json.loads(p.read_text(encoding="utf-8")).get("items", [])[:5]
        except (json.JSONDecodeError, OSError):
            top_ideas = []

    auto = f"""{BEGIN}
| Metric | Value |
|---|---|
{_counts_table(ac)}

Generated `{now}` by `msl/pipeline.py`. Quoting any figure outside this block
means quoting something the next cycle has already superseded.
{END}"""

    fam_rows = "\n".join(
        f"| [{f.title}](library.html#{f.slug}) | {f.category} | {f.question} | "
        f"{', '.join(f'`{s}`' for s in f.sources)} |"
        for f in FAMILIES)

    ranked_rows = "\n".join(
        f"| {i} | `{r['strategyId']}` | {r['name']} | {r['scored']} | "
        f"{(r['accuracy'] or 0)*100:.1f}% | {(r['skill'] or 0)*100:+.1f} pts |"
        for i, r in enumerate(ranked, 1)) or \
        "| — | — | *No persona has enough scored forecasts to rank yet. That is the correct state on cycle 1, not a failure.* | — | — | — |"

    unranked_rows = "\n".join(
        f"| `{u['strategyId']}` | {u['name']} | {u.get('unrankedReason','')} |"
        for u in lb.get("unranked", [])) or "| — | — | — |"

    idea_rows = "\n".join(
        f"| {i} | {it['title']} | {it['robustness']:.3f} | {it['kind']} | {len(it['lineage'])} |"
        for i, it in enumerate(top_ideas, 1)) or \
        "| — | *No idea has a verified lineage yet.* | — | — | — |"

    lessons = memory.get("lessons", [])
    lesson_rows = "\n".join(
        f"| `{l['id']}` | {l['statement']} |" for l in lessons) or \
        "| — | *No lesson has enough supporting counts yet.* |"

    readme = f"""# MasterSelfLearn

An autonomous, evidence-first research engine. It runs on a timer, reads official
public data, builds an expanding library of topics, makes each of a set of
competing personas predict what happens next, scores them against what actually
happened, and writes the whole thing up — with a link a human can open for every
number it prints.

**Live site:** <{config.SITE_URL}> · **Repository:** <{config.REPO_URL}>

It requires **no manual input**. Every cycle is triggered by
`.github/workflows/think.yml` on `{config.CYCLE_CRON}` and commits its own output.

---

{auto}

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
{fam_rows}

## The competition

Personas issue falsifiable forecasts about the next observation of a tracked
metric, and are scored the following cycle. The headline number is **skill** —
accuracy minus the accuracy of `S10_Persistence`, which always predicts "no
change". A persona with positive accuracy but non-positive skill has demonstrated
nothing, and the table says so.

| # | Persona | Name | Scored | Accuracy | Skill vs null |
|---|---|---|---|---|---|
{ranked_rows}

### Unranked

| Persona | Name | Why it is not ranked |
|---|---|---|
{unranked_rows}

A persona is ranked only with ≥{config.MIN_SCORED_FORECASTS_TO_RANK} scored
forecasts *and* a scored null model. Below that it is reported `UNRANKED` with the
reason — never shown as 0%, which would present an untested design as a losing one.

## The idea competition

Ideas are generated by a fixed rule set over verified claims, scored for
robustness (evidence, corroboration, breadth, freshness, reproducibility), and
carried forward. An idea whose support disappears sinks; one that keeps gaining
corroboration is promoted.

| # | Idea | Robustness | Kind | Verified claims behind it |
|---|---|---|---|---|
{idea_rows}

## What the engine has learned about itself

These are counted, not reflected. Each lesson carries the integers behind it.

| | Lesson |
|---|---|
{lesson_rows}

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
python3 -m unittest discover -s tests # {len(_test_names(d))} tests, standard library only
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

{counts['total']} registered — {counts.get('critical', 0)} critical,
{counts.get('warn', 0)} warn, {counts.get('info', 0)} info;
{counts.get('open', 0)} open, {counts.get('resolved', 0)} resolved,
{counts.get('standing', 0)} standing (structural limits that do not auto-resolve).

Full register: [`IRREGULARITIES.md`](IRREGULARITIES.md) or
[`irregularities.html`](irregularities.html).

## Sources

{ac['sourcesRegistered']} registered, {ac['sourcesVerified']} verified by a recorded
live read, {ac['sourcesBlocked']} blocked, {ac['sourcesNeverRead']} never read.
**"Never read" is not "broken"**: it means no recorded probe has reached the
endpoint yet, which is a fact about this project, not a claim about the service.
A source is promoted to `verified-live-read` only by `msl/probe.py`, which writes
`data/source_health.json` and nothing else — the registry itself hard-codes no
status.

{len(KEYED_SOURCES_EXCLUDED)} excluded for requiring an API key, each with the
reason recorded in `msl/sources.py`. {len(INTEREST_CATEGORIES_WITHOUT_A_SOURCE)}
interest categories have no registered source that can serve them, and no claim
is made about them.

Full registry and the last recorded probe: [`sources.html`](sources.html).
"""
    (out / "README.md").write_text(readme, encoding="utf-8")


def _write_status(out: pathlib.Path, now: str, rep: CycleReport, ac: Dict[str, Any],
                  ledger: Ledger, library: Library, memory: Dict[str, Any],
                  register: Register) -> None:
    counts = register.counts()
    crit = [i for i in register.items.values() if i.severity == "critical" and i.status == "open"]
    hist = memory.get("history", [])[-10:]
    hist_rows = "\n".join(
        f"| {h['cycle']} | {h['at']} | {h['claims']:,} | {h['topics']} | {h['newTopics']} | "
        f"{h['forecasts']} | {h['scored']} | {h['ideas']} | {h['irregularities']} | "
        f"{'ok' if h['ok'] else 'ERROR'} |" for h in hist) or "| — | — | — | — | — | — | — | — | — | — |"
    crit_rows = "\n".join(
        f"| `{i.id}` | {i.title} | cycle {i.first_seen_cycle} | `{i.repro}` |" for i in crit) or \
        "| — | *No critical irregularity is open.* | — | — |"

    doc = f"""# STATUS — cycle {rep.cycle}

Generated `{now}` by `msl/docs.py`. Every figure here is read from the same
objects the site is built from.

## Last cycle

| | |
|---|---|
| Cycle | {rep.cycle} |
| Mode | `{rep.mode}` |
| Duration | {rep.duration_ms} ms |
| Reads (ok / failed) | {rep.fetch_ok} / {rep.fetch_failed} |
| Bytes read | {rep.net.get('bytesIn', 0):,} |
| Facts extracted | {rep.facts:,} |
| New claims | {rep.claims_new:,} |
| Claims rejected by the gate | {rep.claims_rejected:,} |
| Derived / rechecked / drifted | {rep.derived} / {rep.rechecks} / {rep.drift} |
| Topics (new) | {rep.topics_total} ({rep.new_topics}) |
| Insights published | {rep.insights} |
| Forecasts issued / scored | {rep.forecasts_issued} / {rep.forecasts_scored} |
| Ideas (promoted) | {rep.ideas} ({rep.ideas_promoted}) |
| Irregularities open (new) | {rep.irregularities_open} ({rep.irregularities_new}) |
| Pipeline errors | {len(rep.errors)} |

{('**Errors:** ' + '; '.join(rep.errors)) if rep.errors else 'No pipeline stage raised.'}

## Open critical irregularities

| Id | Title | First seen | Reproduce |
|---|---|---|---|
{crit_rows}

## Register totals

{counts['total']} registered — {counts.get('critical', 0)} critical,
{counts.get('warn', 0)} warn, {counts.get('info', 0)} info;
{counts.get('open', 0)} open, {counts.get('resolved', 0)} resolved,
{counts.get('standing', 0)} standing.

## Recent cycles

| Cycle | At (UTC) | Claims | Topics | New | Forecasts | Scored | Ideas | Irr open | Result |
|---|---|---|---|---|---|---|---|---|---|
{hist_rows}

## What runs next

`.github/workflows/think.yml` fires on `{config.CYCLE_CRON}` and needs no input.
`probe.yml` live-reads every registered source daily and publishes the health
ledger. `tests.yml` runs the suite on every push and pull request.
"""
    (out / "STATUS.md").write_text(doc, encoding="utf-8")


def _write_verification(out: pathlib.Path, now: str, rep: CycleReport, ac: Dict[str, Any],
                        ledger: Ledger, library: Library, register: Register) -> None:
    rows = []
    for i, s in enumerate(sorted(REGISTRY, key=lambda x: x.id), 1):
        rows.append(
            f"| {i} | `{s.id}` | {s.name} | {s.operator} | `{s.status}` | {s.live_reads} | "
            f"{s.last_read_at or '—'} | {s.last_status if s.last_status is not None else '—'} | "
            f"[docs]({s.docs_url}) · [probe]({s.probe_url}) |")
    table = "\n".join(rows)

    ev = ledger.evidence[-60:]
    ev_rows = "\n".join(
        f"| `{e.id}` | `{e.source_id}` | {e.status if e.status is not None else '—'} | "
        f"{e.captured_at} | `{(e.payload_sha256 or e.projection_sha256)[:16]}` | "
        f"{e.raw_bytes:,} | `{e.capture_mode}` | {'yes' if e.wire_hash_verifiable else '**no**'} | "
        f"[open]({e.url}) |" for e in ev) or "| — | — | — | — | — | — | — | — | — |"

    kinds = ledger.counts()
    doc = f"""# VERIFICATION — line-by-line audit ledger

Generated `{now}` at cycle {rep.cycle}. Read-only verifiers:
`python3 -m msl.cli verify-claims` and `python3 tools/probe_sources.py`.

## 1. Claim ledger composition

| Kind | Count | What it means |
|---|---|---|
| `captured` | {kinds.get('captured', 0):,} | A value lifted from a payload this project read |
| `documented` | {kinds.get('documented', 0):,} | A value from the operator's own published record |
| `negative` | {kinds.get('negative', 0):,} | Proof that something does **not** exist |
| `derived` | {kinds.get('derived', 0):,} | Arithmetic over claims above, formula recorded |
| **Total accepted** | **{len(ledger.claims):,}** | |
| Rejected by the gate | {len(ledger.rejections):,} | Published, not swallowed |

## 2. Source registry

{len(REGISTRY)} sources. `status` is written only by the probe.

| # | Id | Name | Operator | Status | Live reads | Last read (UTC) | HTTP | Links |
|---|---|---|---|---|---|---|---|---|
{table}

## 3. Most recent evidence rows

Every row is one outbound read, with the hash of what came back.

| Id | Source | HTTP | Captured (UTC) | SHA-256 (16) | Bytes | Capture mode | Wire-hash verifiable | URL |
|---|---|---|---|---|---|---|---|---|
{ev_rows}

`wire-hash verifiable = no` means the body was recorded by an interactive agent
read rather than by the pipeline, so the stored hash covers the recorded body and
not the bytes on the wire. Those rows are re-read by the next probe.

## 4. Library accounting

| | |
|---|---|
| Topics tracked | {len(library.topics):,} |
| Topics with ≥1 verified claim | {len(ledger.topics_with_claims()):,} |
| Topics with 0 verified claims | {len(library.topics) - len(ledger.topics_with_claims()):,} |
| Candidate / active / retired / blocked | {library.counts().get('candidate', 0)} / {library.counts().get('active', 0)} / {library.counts().get('retired', 0)} / {library.counts().get('blocked-no-source', 0)} |
| Families | {len(library.counts()) and sum(1 for f in {t.family for t in library.topics.values()})} |

## 5. Reproducing any number on the site

```bash
python3 -m msl.cli cycle --offline   # rebuild every artifact from data/seed/, no network
python3 -m msl.cli verify-claims     # recheck every derived claim, report drift
python3 tools/probe_sources.py       # live-read every registered source
python3 -m unittest discover -s tests
```

A number on the site that you cannot reproduce with one of those four commands is
a defect. Report it as an irregularity rather than editing the number.
"""
    (out / "VERIFICATION.md").write_text(doc, encoding="utf-8")


def _write_irregularities(out: pathlib.Path, now: str, rep: CycleReport,
                          register: Register) -> None:
    items = sorted(register.items.values(),
                   key=lambda i: (ORDER.get(i.severity, 3), -i.last_seen_cycle, i.id))
    counts = register.counts()
    sections = []
    for sev in ("critical", "warn", "info"):
        rows = [i for i in items if i.severity == sev]
        if not rows:
            continue
        body = "\n".join(
            f"### `{i.id}` — {i.title}\n\n"
            f"*{i.severity.upper()}* · first seen cycle {i.first_seen_cycle} "
            f"({i.first_seen_at}) · last seen cycle {i.last_seen_cycle} "
            f"({i.last_seen_at}) · {i.occurrences} occurrence(s) · "
            f"**{i.status}**{ ' · standing' if i.standing else ''}"
            f"{f' · source `{i.source_id}`' if i.source_id else ''}"
            f"{f' · topic `{i.topic}`' if i.topic else ''}\n\n"
            f"{i.detail}\n\n"
            + (f"**Reproduce:** `{i.repro}`\n" if i.repro else "")
            for i in rows)
        sections.append(f"## {sev.upper()} ({len(rows)})\n\n{body}")
    body = "\n\n".join(sections) or "*No irregularity is registered.*"

    doc = f"""# IRREGULARITIES

Generated `{now}` at cycle {rep.cycle}.

{counts['total']} registered — {counts.get('critical', 0)} critical,
{counts.get('warn', 0)} warn, {counts.get('info', 0)} info.
{counts.get('open', 0)} open, {counts.get('resolved', 0)} resolved,
{counts.get('standing', 0)} standing.

**Standing** entries are structural limits of this project, not transient
failures: they do not auto-resolve, because the owner needs to keep seeing them.
A non-standing entry that stops recurring is marked `resolved` rather than
deleted, so the register keeps its history.

---

{body}
"""
    (out / "IRREGULARITIES.md").write_text(doc, encoding="utf-8")


def _test_names(d: pathlib.Path) -> List[str]:
    tests = config.ROOT / "tests"
    if not tests.exists():
        return []
    out = []
    for p in sorted(tests.glob("test_*.py")):
        out.append(p.stem)
    return out


def _write(p: pathlib.Path, text: str) -> None:
    p.write_text(text, encoding="utf-8")
