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
| [`SESSION_LOG.md`](SESSION_LOG.md) | Per-session audit + work log. Session 1 = the 2026-09-26 stop-the-line ownership flag; session 2 = this session's re-audit, leaderboard pull, site study, and research pass. |
| [`FIELD_AND_METRIC.md`](FIELD_AND_METRIC.md) | The verified scoring metric (distance-weighted Tversky, α=0.2/β=0.8, 300 m kernel), its strategic consequences, and the fresh 2026-09-26 leaderboard state vs our tracked rows. |
| [`RESEARCH_LIBRARY.md`](RESEARCH_LIBRARY.md) | Annotated, linked bibliography: potential-field edge detection, DEM/LiDAR scarp detection, geothermal play-fairway methodology, official datasets. Every entry names where it came from. |
| [`HYPOTHESES.md`](HYPOTHESES.md) | The hypothesis register: what was tested (and how it was scored), what was falsified, and the open ranked queue of next angles. |
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

## Current state (2026-09-26, session 2)

- Ownership violation **open**: 11 GEMSDOE repos/sites on our account; active
  parallel sessions observed on `GEMSDOE4` and `6GEMSDOE` after the stop flag
  (details in the flag addendum). Consolidation blocked on human ratification.
- Best score attributable to our tracked accounts: **0.1563** (`extradr19`,
  #22). Field high **0.3049** (DARD, #1). Phase-1 pay line (top 5) at
  **0.2589** at pull time.
- This repo holds **no competition data files** (they sit behind the
  DrivenData login of whichever registration is confirmed as ours). Model
  experimentation is blocked on that access; the research library is not.
