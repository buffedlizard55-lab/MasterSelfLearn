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
| [`SESSION_LOG.md`](SESSION_LOG.md) | Per-session audit + work log. Session 1 = the 2026-09-26 stop-the-line ownership flag; session 2 = the re-audit, leaderboard pull, site study, research pass; session 3 = the executed pipeline audit. |
| [`PIPELINE_AUDIT.md`](PIPELINE_AUDIT.md) | **Start here for engineering.** Session 3's audit of the live pipeline against brief items 1–5, produced by *running* the code: 46/46 tests, a re-verified 13-check submission gate with a negative test, and four measured defects (D-1…D-4) with verified patches. |
| [`CANDIDATE_GEOLOGY.md`](CANDIDATE_GEOLOGY.md) | Brief item 6: the geological reasoning behind the flagged traces, with per-candidate lookups against the USGS QFFD-sourced Nevada fault service. Six written up in full, three falsification tests named. |
| [`probes/`](probes/) | The three runnable scripts that produced the audit's measurements. Not part of this repo's stdlib test suite; see its README. |
| [`FIELD_AND_METRIC.md`](FIELD_AND_METRIC.md) | The verified scoring metric (distance-weighted Tversky, α=0.2/β=0.8, 300 m kernel), its strategic consequences, and the fresh 2026-09-26 leaderboard state vs our tracked rows. |
| [`RESEARCH_LIBRARY.md`](RESEARCH_LIBRARY.md) | Annotated, linked bibliography: potential-field edge detection, DEM/LiDAR scarp detection, geothermal play-fairway methodology, official datasets. Every entry names where it came from. |
| [`HYPOTHESES.md`](HYPOTHESES.md) | The hypothesis register: what was tested (and how it was scored), what was falsified, and the open ranked queue of next angles. Session 3 falsified HE (4–5 px spacing, at matched budget) and HG (the `--n-channels` rationale). |
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

## Current state (2026-09-26, session 3)

- Ownership violation **open and now 12 sites wide in effect**: 11 GEMSDOE
  repos on our account, all with Pages built. No *new repo* was created since
  session 2 (newest `created_at` is 2026-09-25T18:33:56Z), but `7GEMSDOE` — an
  empty stub since 2026-09-25 — was populated with a complete new site at
  **17:38–17:43Z today**, and `5GEMSDOE`, `GEMSDOE4` and `6GEMSDOE` all took
  pushes today. Consolidation is still blocked on human ratification.
- **The pipeline is not in this repo.** It lives in `6GEMSDOE`
  (`src/gems/*.py`). Session 3 audited it read-only by executing it: 46/46
  tests pass, the submission gate passes 13/13 and fails correctly on an
  injected NaN, and four defects were measured — see
  [`PIPELINE_AUDIT.md`](PIPELINE_AUDIT.md).
- Best score attributable to our tracked accounts: **0.1563** (`extradr19`,
  #24). Field high **0.3049** (DARD, #1), unchanged. Phase-1 pay line (top 5)
  at **0.2589**.
- **The brief's "~4–5 px spacing" placement premise is falsified** at an exactly
  matched pixel budget on our own spatially blocked folds (−19% to −42%,
  monotone in spacing). The shipped placement is a dense top-3% budget, which
  the measurement supports. See `HYPOTHESES.md` HE.
- This repo holds **no competition data files**. Model experimentation is
  blocked on access through the confirmed account; the audit and the research
  library are not.
