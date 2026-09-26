# HYPOTHESIS REGISTER — GEMS Prize

Status vocabulary:
- **TESTED-LIVE** — scored on the real public leaderboard (evidence: row + score).
- **TESTED-SURROGATE** — scored only against the supplied catalogue labels
  (the wrong population; every such number carries that caveat).
- **FALSIFIED-LIVE** — the leaderboard contradicted it.
- **OPEN** — not yet testable from here, with what it would take.

Every entry names the experiment that decided it. Nothing is silently edited:
a status change gets a new line with the date.

---

## Decided entries

| Id | Hypothesis | Status (2026-09-26) | Evidence |
|---|---|---|---|
| HA | Skeleton emission (width 0 px, floor 0.1) is optimal among widths | TESTED-SURROGATE only | GEMSDOE site's width sweep (its published measurement): width curve peaks at 0 px on every ensemble *against the catalogue*. Unresolved on the hidden population — see D4 in `FIELD_AND_METRIC.md`. |
| HB | At a fixed pixel budget, spacing nodes at the kernel's own scale beats a dense ridge | TESTED-LIVE, direction confirmed, magnitude small | GEMSDOE3 Pindrop A/B on the real board: nodes 0.1193 (`smrtdoog5`) vs dense-ridge control 0.1152 (`SDCF9`), same 155,021 px budget → +0.0041. |
| HC | An arm trained only on catalogue-gap ("unmapped") pixels generalises better to the hidden labels than one trained on everything | FALSIFIED-LIVE (as built) | Pindrop discovery arm scored 0.0830 (`wbg1`) — the worst of the three. Caveat: it was the second, independently trained system, so construction is confounded with the training-set change; the lesson is "gap-only training as implemented lost 0.036 vs the sibling", not that the idea is dead. |
| HD | k=2-of-5 union of new-fault detectors adds +0.0150 | TESTED-SURROGATE, UNVERIFIED | Claim appears only in GEMSDOE4 commit `858bcb6e` / PR #5 (2026-09-26): "+0.0150 on the untouched fold, P=0.957". No leaderboard row is attributable to it, and its surrogate is the catalogue population. Carried as a claim, not a result. |
| HE | **At an exactly matched pixel budget, thinning to ~4–5 px spacing beats dense emission** | **FALSIFIED-SURROGATE (2026-09-26, session 3)** | The session brief carries this as a live design premise. It is not. `experiments_agreement.json` config `extended` (88 ch), fold 0, `gt_full`, budgets matched to within 5 px of 27,875: `topk_hard@0.03` **0.13579** vs `line3` 0.11005 (**−19.0%**), `line5` 0.09658 (**−28.9%**), `line9` 0.07847 (**−42.2%**); `mix3/5/9` 0.12086/0.11449/0.10907. Monotone in spacing. Caveat: catalogue population. See `PIPELINE_AUDIT.md` §3. |
| HF | The 17-channel cross-signal agreement layer (strain × conductivity × seismicity) improves the model | **FALSIFIED-SURROGATE on the catalogue proxy; OPEN on the gap population** | Measured twice on identical blocked folds, 400k neg / 300 iters: 88 ch vs 105 ch = 0.16978 vs 0.16704 (`experiments_agreement.json`, full catalogue) and 0.16497 vs 0.16309 (`experiments_itrace.json`, trace-thinned). So it lost. But both instruments score the *catalogue*, which is structurally blind to information that is independent of mapping history — the one thing those channels carry. Re-test on block-holdout / cross-catalogue. See `PIPELINE_AUDIT.md` §1. |
| HG | The `--n-channels 88` subset is justified by "the multi-scale channels did not improve the score" | **FALSIFIED (documentation defect D-3)** | The help text at `build_submission.py:134-137` says this. The multi-scale channels are indices 48–87 and *are* included in 88; they *did* improve (88 ch 0.16978 vs 48 ch 0.16283, +0.0070). The 17 channels 88 actually removes are the agreement block. The flag works; its stated rationale is wrong. |

## Open queue — ranked by expected leverage on the 0.15 → 0.26+ gap

(Ranking rationale = our D-analysis in `FIELD_AND_METRIC.md` §5; each entry
names the test that would decide it and what blocks that test here.)

**Queue revision 2026-09-26 (session 4):** the DrivenData staff clarification
that known-fault pixels are **masked from scoring** (`FIELD_AND_METRIC.md` §1b,
forum 11516) reorders this queue. Catalogue emission is free, so hedges and
corridors along known traces (E11) jump to the top of the cheap experiments,
and every surrogate number below must be re-read with the unmasked-FP caveat
(D8).

| Id | Hypothesis | Why it could move the score | Test | Blocked on |
|---|---|---|---|---|
| E1 | Mining the 1 m DEM for scarp-template matches **outside** the catalogue adds true hidden-fault recall | D5: scarps are the richest young-fault evidence; C1 gives a published per-pixel method; the GEMSDOE inventory already confirmed 716 1 m tiles over the footprint | Run Sare-et-al.-style curvature-template matching per tile; emit candidates with distance-to-catalogue > 300 m; score surrogate overlap + public-board A/B | competition data + DEM tiles (confirmed account), a GPU-class runner |
| E2 | A soft 1–2 px probability halo around high-confidence traces beats the binary skeleton on the real metric (geolocation insurance) | D3/D4: kernel credit falls 1 → 2/3 → 1/3 over 3 px; a halo hedges predictor offset at near-zero FP cost near the trace | Public-leaderboard A/B vs `ens12-adopted-floor0.1-w0`, same candidates | one of the 3 weekly submissions of the confirmed account; explicit human go-ahead |
| E3 | Magnetic-edge candidates (tilt/iTilt/THDR on the GeoDAWN bands) intersected with strain/seismicity anomalies predict catalogue-gap faults | D5 + B1/B2/B4 + D6: GeoDAWN residuals already show young basin faults; the provided stack ships the derivative bands | Derive edge layers from provided bands; rank catalogue-gap pixels; validate against any held-out expert traces if obtainable, else board A/B | competition feature stack |
| E4 | Trace extensions and step-over/intersection pixels (PFA sweet spots) are over-represented in the expert new-fault set | D2/D3 of the research library: Faulds-type factors treat intersections/step-overs as permeability maxima; experts extending traces is the most plausible "new" geometry | Generate tip-rays + intersection candidates from the catalogue geometry; compare density of hits vs random traces on whatever scored feedback is available | catalogue vectors (data tab) |
| E5 | Emission budget should be raised above 3% of valid area — recall-priced metric tolerates more candidates | D1: FP tax is 0.2 per far miss vs 0.8 per recovered truth; break-even P(capture) ≈ 0.2 | Budget sweep on surrogate, then the smallest board-confirming step | both populations |
| E6 | Stress-loaded candidates (slip/dilation tendency of Great Basin Q-faults, USGS official shapefile) prioritise which unmapped structures to emit | A5: official, region-specific, free; complements the provided dilatation-rate band | Join tendency shapefile to catalogue-gap candidates; use as ranking prior | data tab access to emit |
| E7 | Phase-2 upside: defensible-only candidates outscore recall-maxed noise once experts expand labels | D6: Phase 2 rescoring uses experts' review of every submission | Not directly testable before Phase 1 closes; adopted as a design principle (no indefensible mass) | n/a — principle |
| **E8** | **Rebuild the feature stack with the NaN-guard defect (D-1) fixed and re-run the whole experiment table** | Session 3 measured 32,461 footprint px (0.63%) at σ=1.5 and 78,319 (1.52%) at σ=3.0 sitting in the filter stencil's reach of a NaN yet reported as valid — 0.5×–1.3× the size of the entire 60,988-px label set. Every number in `data/evidence/experiments*.json` was computed on those channels, so **the current feature ranking is unknown, not merely suboptimal** | Apply the verified patch (`PIPELINE_AUDIT.md` §5), re-run `build_features.py` (917 s last time), re-run the experiment table, diff the ordering | a runner with the 419 MB feature bridge; ~1 h of compute — **UNBLOCKED and executed session 4 in a scratch checkout; results in `REBUILT_EXPERIMENTS.md`** |
| **E9** | **Re-test the agreement layer on a catalogue-*gap* instrument, not the catalogue proxy** | HF lost by 0.0019–0.0027 on the catalogue. Those 17 channels are the only ones whose information is independent of mapping history, so the catalogue proxy is the one instrument that cannot see their value. They are also what makes the top candidates geologically legible (`CANDIDATE_GEOLOGY.md` §4) | Blocked folds scoring only catalogue-gap pixels; or the `cross-catalogue` instrument. Compare 88 ch vs 88+agreement at identical budget | E8 first, else the comparison inherits D-1 — **sequenced after E8 and executed session 4 as `--trace-holdout 0.3` + `trace_gap` scoring (the cross-catalogue instrument); results in `REBUILT_EXPERIMENTS.md`** |
| **E10** | **Kill the three falsification risks that dominate the top candidates** | `CANDIDATE_GEOLOGY.md` §4: (a) N–S aeromagnetic flight-line striping in `tmi_hg` threatens every azimuth ≈ 0–13° candidate; (b) smoothed regional gradient inherited by `geod_shearrate` threatens the highest-strain candidate C-7; (c) gravity *sign* (basement high vs basin fill) threatens C-1/C-5, whose ranks are 1.00/0.99. None is answerable from magnitude-ranked `famrank` | Read raw band values along each of the six written-up traces; check striping periodicity, strain-band gradient, and gravity sign | the feature stack (same access as E8) |

## What killed (or would kill) each open entry

- E1 dies if template matches outside the catalogue convert to board score at
  ≤ the rate of random traces (one A/B decides it).
- E2 dies if the halo A/B loses to the skeleton by more than the public-split
  noise (~±0.005, our rough read of sibling-score spreads — labelled as such).
- E3 dies if edge layers merely re-express catalogue structure (high overlap,
  low gap-density).
- E5 dies if the board punishes the raised budget (FP tax realised). **Re-opened
  in part by the masking rule (D7):** budget spent *on/near the catalogue* is
  tax-free, so the 3% ceiling applies only to off-mask emission.
- E8 cannot die, only cost: if the rebuilt table reproduces the current ordering,
  the contamination was immaterial and that is itself a result worth recording.
- E9 dies if the agreement channels also lose on the gap population — at which
  point they stay out and the brief's priority-3 axis is closed with evidence
  rather than with an assumption.
- E10 dies the candidates, not the hypothesis: a candidate killed by (a), (b) or
  (c) is removed from the written-up set and the reason is recorded here.

## Session-4 additions and status changes (2026-09-26)

| Id | Hypothesis | Status | Evidence |
|---|---|---|---|
| **E10** | The three artefact risks that dominate the top candidates can be killed with raw-band tests | **DECIDED — tests executed; one candidate demoted, two strengthened, one class-level finding** | `gemsdoe/probes/e10_falsification.py` on the pinned raster; results in `CANDIDATE_GEOLOGY.md` §5–§6. (a) flags C-4 and 3/3 near-N–S traces tested (class finding); (b) clears C-7's flagship risk (strain earned locally, R² 0.29) and exposes `geod_shearrate` data holes at C-3/C-4; (c) refutes C-5's graben-fill kill (both C-1/C-5 are density-high/shallow-basement). **(a) later invalidated by E12's baseline test — see the session-5 table below.** |
| **HI** | Known USGS/INGENIOUS fault pixels are masked out of scoring in both rounds | **RULE-VERIFIED (official staff, forum 11516, 2026-09-16)** — not our experiment | DrivenData staff reply quoted in `FIELD_AND_METRIC.md` §1b: masked pixels "do not count towards penalty terms", in both rounds. Mask width unspecified (flagged). Our local `metric.py` does not implement it (D8) — **the FP side is now implemented** (session 5, below). |
| **E11** | The score-safe, possibly score-raising file is `catalogue ∪ confident new-fault candidates` (and a 1-px corridor along the catalogue is a cheap bet on expert extensions) | **BUILT + GATED LOCALLY (session 5) — not submitted (blocked on ratified account + human go-ahead)** | `scripts/build_e11_union.py` on the D-1/D-5-fixed stack: file A `gems6_hgb88topk03_hedge_dada4435cd.tif` = shipped ∪ catalogue, 192,404 px (3.72%), gate 13/13 PASS; file B (the E11 form) `gems6_hgb88topk03_hedge105topk02_984e11e4d7.tif` = A ∪ 105-ch topk@0.02, 202,951 px (3.93%), gate PASS. All 60,988 catalogue px free under the mask (width-0 pin); off-mask emission 141,963 px = 2.75% — **inside the 3% minimax budget on the taxable side**. The 105-ch gap set overlaps the shipped field by 91,321/103,347 px (88%), so the agreement layer's marginal addition is only 10,547 px. Weekly-submission state of the confirmed account: unverifiable from here (F5); one-entry record left blank. |
| **E12** | A stripe-removal (flight-line levelling) pass over `tmi_hg`/`mag_*` recovers trustworthy N–S edge evidence | **TESTED — criterion NOT MET; instrument defect D-9 found; class finding downgraded to a physical prior** | `gemsdoe/probes/e12_stripe_removal.py`: two levellers (global column median; y-aware 256-row block medians) on the six raw magnetic bands, E10 test (a) re-run on the same windows. Flags 3/4 → 4/4; near-N–S shares never exceed the non-N–S baseline (which itself exceeds the 0.25 threshold in 3/4 windows raw — the flag reduces to the azimuth gate). The x-only field's own dominant period is 823 px (`tmi_hg`), not 10–18 px — no column-constant flight-line component at the E10 periods. Details + the alignment-test proposal: `CANDIDATE_GEOLOGY.md` §7.3. |
| **E13** | E9's gap-population sign flip (105 ch wins 5/6) persists under the D8 board-like mask | **TESTED — criterion MET (weak sense): flip unchanged** | `data/evidence/experiments_e13_masked.json`; unmasked aggregates reproduce session 4's E9 table to 4 dp (doubles as the reproduction check). Masked: 105 ch wins gap 5/6 with deltas within ±0.0002 of unmasked (topk@0.02: 0.0765→0.0801); mask ≈ +0.002 on gap for both configs (measures E9's restricted-GT FP wash); no-op on gt_full (proximity discount already zeroes on-trace FP — implementation validation). Tables: `REBUILT_EXPERIMENTS.md` §5.3. |

## Session-5 additions and status changes (2026-09-26)

| Id | Hypothesis | Status | Evidence |
|---|---|---|---|
| **D8** | Local experiments claiming board relevance must implement the §1b mask and report masked + unmasked numbers | **IMPLEMENTED (FP side), re-run executed** | `metric.components(..., fp_free_mask=)` (conservative pin: the 60,988 label px; TP/FN deliberately not zeroed — every local gt pixel is a known fault, documented in the docstring) + `experiment.py --fp-mask-px`; run `experiments_e13_masked.json` = E9 comparison with masked **and** unmasked aggregates side by side (results: `REBUILT_EXPERIMENTS.md` session-5 section). |
| **D-9** | (defect, found by E12) test (a)'s E–W-share threshold has no baseline contrast | **MEASURED** | 3/4 non-N–S written-up windows exceed 0.25 (0.445–0.691 raw); the class finding of E10/(a) is not identified by the instrument. `CANDIDATE_GEOLOGY.md` §7.3. |
| **chain test** | C-1 ↔ C-6 ↔ C-5 are one ~17 km system | **REFUTED** | Lateral offsets 34.9/56.1 px (3.5/5.6 km), facing gap 53 km on C-6→C-1; gravity cross-sections ramp-like on the critical leg (C-6's own kill-if). `CANDIDATE_GEOLOGY.md` §7.1. |
| **cond kill-ifs** | C-8's/C-4's cond pillars are fault-local fluid paths | **KILL-IFS SUPPORTED** | cond_surf rank at trace = 0.984/0.886 globally but trace-vs-window −0.044σ/−0.108σ locally (regional basin-fill high, no local expression). `CANDIDATE_GEOLOGY.md` §7.2. |
