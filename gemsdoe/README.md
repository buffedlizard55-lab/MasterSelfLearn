# gemsdoe/ — the GEMS Prize knowledge library

The expanding, self-improving body of expertise for the DOE GEMS Prize
(DrivenData competition 306): predicting geologic faults **missing from the
training catalogue** in the GeoDAWN region of Nevada/California.

This directory is the institutional memory the session brief requires ("building
a growing knowledge library inside the repo, not just a final submission").
It is append-friendly: each session adds to `SESSION_LOG.md` and
`HYPOTHESES.md`; findings that stop holding up get a status change, never a
silent deletion.

## Index

| File | Contents |
|---|---|
| [`SESSION_LOG.md`](SESSION_LOG.md) | Per-session audit + work log. Session 1 = the 2026-09-26 stop-the-line ownership flag; session 2 = the re-audit, leaderboard pull, site study, research pass; session 3 = the executed pipeline audit; session 4 = score-quality work: D-1/D-2/D-5 patched and re-measured, the E8 rebuild + E9 gap instrument executed, E10 falsification tests run. |
| [`PIPELINE_AUDIT.md`](PIPELINE_AUDIT.md) | **Start here for engineering.** Session 3's audit of the live pipeline against brief items 1–5, produced by *running* the code: 46/46 tests, a re-verified 13-check submission gate with a negative test, and four measured defects (D-1…D-4) with verified patches. |
| [`REBUILT_EXPERIMENTS.md`](REBUILT_EXPERIMENTS.md) | **Session 4 results:** the E8 experiment table re-run on a D-1/D-5-fixed feature stack (ordering reproduced — 88 > 105 > 48) and E9, the agreement layer re-tested on the catalogue-gap (whole-trace-holdout) instrument. |
| [`CANDIDATE_GEOLOGY.md`](CANDIDATE_GEOLOGY.md) | Brief item 6: the geological reasoning behind the flagged traces, with per-candidate lookups against the USGS QFFD-sourced Nevada fault service. Ten written up in full (six + session-4 extension), the three falsification tests **executed** (§5–§6), one candidate demoted (C-4), a class-level N–S striping finding. |
| [`probes/`](probes/) | The runnable scripts that produced the audit's measurements, plus `probe_crossder_halo.py` (defect D-5) and `e10_falsification.py` (tests (a)–(c) on raw bands). Not part of this repo's stdlib test suite; see its README. |
| [`patches/session4_d1_d2_d3_d5_e9.patch`](patches/session4_d1_d2_d3_d5_e9.patch) | The verified unified diff against `6GEMSDOE@e2fe3f41` (D-1 NaN-guard square reach, D-2 L∞ buffer, D-3 help text, D-5 cross-derivative halo, D-4 test rewrite, E9 gap scoring). **Not applied upstream** — apply in whichever repo is ratified canonical, and only there. |
| [`SESSION_PROMPT.md`](SESSION_PROMPT.md) | The recurring session prompt, embedded verbatim (finding F6). Moves to the canonical repo's `README.md` once ratified. |
| [`FIELD_AND_METRIC.md`](FIELD_AND_METRIC.md) | The verified scoring metric (distance-weighted Tversky, α=0.2/β=0.8, 300 m kernel), its strategic consequences, and the fresh 2026-09-26 leaderboard state vs our tracked rows. **§1b adds the official staff clarification that known-fault pixels are masked from scoring** (forum 11516) — read it before any budget or placement decision. |
| [`RESEARCH_LIBRARY.md`](RESEARCH_LIBRARY.md) | Annotated, linked bibliography: potential-field edge detection, DEM/LiDAR scarp detection, geothermal play-fairway methodology, official datasets. Every entry names where it came from. |
| [`HYPOTHESES.md`](HYPOTHESES.md) | The hypothesis register: what was tested (and how it was scored), what was falsified, and the open ranked queue of next angles. Session 3 falsified HE (4–5 px spacing, at matched budget) and HG (the `--n-channels` rationale); session 4 decided E10 and added HI (masking), E11 (catalogue hedge), E12 (stripe removal). |
| [`../GEMSDOE_OWNERSHIP_FLAG.md`](../GEMSDOE_OWNERSHIP_FLAG.md) | The standing ownership/one-repo audit (session 1) + addendum (session 2). Read before touching anything submission-related. |

## Standing guardrails (from the session brief — non-negotiable)

1. **One repo, one account, one submission per prize round, for us.** Never
   create a new GEMSDOE repo, site, or DrivenData registration. Eleven
   GEMSDOE repos currently exist on our GitHub account — that violation is
   flagged in `../GEMSDOE_OWNERSHIP_FLAG.md` and consolidation awaits a human
   decision; none of them may be treated as a parallel experiment arm here.
2. **No hallucinations.** Every claim links to an official, verifiable source,
   or is labelled as our own derivation/interpretation. Gaps are printed, not
   filled.
3. **The target is faults MISSING from the training catalogue.** Both prize
   rounds score the experts' new-fault set (rules §1.1; competition page 967).
   Reproducing the USGS/INGENIOUS catalogue is only worth credit where the
   experts' new labels happen to coincide with it.
4. **No submissions from this repo without human ratification** of which
   DrivenData registration is the ONE account and which repo is canonical.

## Current state (2026-09-26, session 4)

- Ownership violation **open and now 13 sites wide in effect**: 11 GEMSDOE
  repos on our account, all with Pages built. No *new repo* since session 2
  (newest `created_at` is 2026-09-25T18:33:56Z), but since session 3's
  snapshot **`8GEMSDOE` — also an empty stub — was populated with a complete
  new site at 18:10–18:17Z today** (mirroring `7GEMSDOE`'s 17:38–17:43Z
  stand-up). Parallel arms are converting stubs into live sites faster than
  sessions run. Consolidation is still blocked on human ratification.
- **The three "unconfirmed ownership" sites are ours** — re-verified session 4
  with fresh API calls: `5GEMSDOE`, `GEMSDOE4`, `6GEMSDOE` all
  `owner_id 309556078`. The *registrations* behind the leaderboard rows are a
  separate question and remain unverifiable from public data (F5).
- **The pipeline is not in this repo.** It lives in `6GEMSDOE`
  (`src/gems/*.py`). Session 4 executed it in a scratch checkout with the
  verified D-1/D-2/D-5 patch applied: 46/46 tests, gate 13/13 + negative test,
  the E8 feature rebuild, and the E9 gap-instrument run — see
  [`REBUILT_EXPERIMENTS.md`](REBUILT_EXPERIMENTS.md). The patch is delivered
  in [`patches/`](patches/) and is **not** applied upstream.
- **The official scorer masks known-fault pixels from all penalty terms**
  (DrivenData staff, forum 11516 — `FIELD_AND_METRIC.md` §1b). Catalogue
  emission is free; local surrogate numbers charge for it (D8). This is the
  single most strategy-relevant verified fact found this session.
- Best score attributable to our tracked rows: **0.1563** (`extradr19`, #24;
  `SDCF9` also reached 0.1563 at #25 with a second submission *during* this
  session — other registrations, per the brief not our data). Field high
  **0.3049** (DARD, #1), pay line **0.2589**, both unchanged.
- **The brief's "~4–5 px spacing" placement premise stays falsified** (HE) and
  the spacing machinery is intact-but-unadopted; the placement *strategy*
  question that is now live is the masking-driven catalogue hedge (E11).
- This repo holds **no competition data files** (they live in the scratch
  checkout and the `6GEMSDOE` bridge). Model experimentation ran read-only
  against those; no GEMSDOE repo was written to this session.
