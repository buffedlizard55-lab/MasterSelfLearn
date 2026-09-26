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

| Id | Hypothesis | Why it could move the score | Test | Blocked on |
|---|---|---|---|---|
| E1 | Mining the 1 m DEM for scarp-template matches **outside** the catalogue adds true hidden-fault recall | D5: scarps are the richest young-fault evidence; C1 gives a published per-pixel method; the GEMSDOE inventory already confirmed 716 1 m tiles over the footprint | Run Sare-et-al.-style curvature-template matching per tile; emit candidates with distance-to-catalogue > 300 m; score surrogate overlap + public-board A/B | competition data + DEM tiles (confirmed account), a GPU-class runner |
| E2 | A soft 1–2 px probability halo around high-confidence traces beats the binary skeleton on the real metric (geolocation insurance) | D3/D4: kernel credit falls 1 → 2/3 → 1/3 over 3 px; a halo hedges predictor offset at near-zero FP cost near the trace | Public-leaderboard A/B vs `ens12-adopted-floor0.1-w0`, same candidates | one of the 3 weekly submissions of the confirmed account; explicit human go-ahead |
| E3 | Magnetic-edge candidates (tilt/iTilt/THDR on the GeoDAWN bands) intersected with strain/seismicity anomalies predict catalogue-gap faults | D5 + B1/B2/B4 + D6: GeoDAWN residuals already show young basin faults; the provided stack ships the derivative bands | Derive edge layers from provided bands; rank catalogue-gap pixels; validate against any held-out expert traces if obtainable, else board A/B | competition feature stack |
| E4 | Trace extensions and step-over/intersection pixels (PFA sweet spots) are over-represented in the expert new-fault set | D2/D3 of the research library: Faulds-type factors treat intersections/step-overs as permeability maxima; experts extending traces is the most plausible "new" geometry | Generate tip-rays + intersection candidates from the catalogue geometry; compare density of hits vs random traces on whatever scored feedback is available | catalogue vectors (data tab) |
| E5 | Emission budget should be raised above 3% of valid area — recall-priced metric tolerates more candidates | D1: FP tax is 0.2 per far miss vs 0.8 per recovered truth; break-even P(capture) ≈ 0.2 | Budget sweep on surrogate, then the smallest board-confirming step | both populations |
| E6 | Stress-loaded candidates (slip/dilation tendency of Great Basin Q-faults, USGS official shapefile) prioritise which unmapped structures to emit | A5: official, region-specific, free; complements the provided dilatation-rate band | Join tendency shapefile to catalogue-gap candidates; use as ranking prior | data tab access to emit |
| E7 | Phase-2 upside: defensible-only candidates outscore recall-maxed noise once experts expand labels | D6: Phase 2 rescoring uses experts' review of every submission | Not directly testable before Phase 1 closes; adopted as a design principle (no indefensible mass) | n/a — principle |
| **E8** | **Rebuild the feature stack with the NaN-guard defect (D-1) fixed and re-run the whole experiment table** | Session 3 measured 32,461 footprint px (0.63%) at σ=1.5 and 78,319 (1.52%) at σ=3.0 sitting in the filter stencil's reach of a NaN yet reported as valid — 0.5×–1.3× the size of the entire 60,988-px label set. Every number in `data/evidence/experiments*.json` was computed on those channels, so **the current feature ranking is unknown, not merely suboptimal** | Apply the verified patch (`PIPELINE_AUDIT.md` §5), re-run `build_features.py` (917 s last time), re-run the experiment table, diff the ordering | a runner with the 419 MB feature bridge; ~1 h of compute |
| **E9** | **Re-test the agreement layer on a catalogue-*gap* instrument, not the catalogue proxy** | HF lost by 0.0019–0.0027 on the catalogue. Those 17 channels are the only ones whose information is independent of mapping history, so the catalogue proxy is the one instrument that cannot see their value. They are also what makes the top candidates geologically legible (`CANDIDATE_GEOLOGY.md` §4) | Blocked folds scoring only catalogue-gap pixels; or the `cross-catalogue` instrument. Compare 88 ch vs 88+agreement at identical budget | E8 first, else the comparison inherits D-1 |
| **E10** | **Kill the three falsification risks that dominate the top candidates** | `CANDIDATE_GEOLOGY.md` §4: (a) N–S aeromagnetic flight-line striping in `tmi_hg` threatens every azimuth ≈ 0–13° candidate; (b) smoothed regional gradient inherited by `geod_shearrate` threatens the highest-strain candidate C-7; (c) gravity *sign* (basement high vs basin fill) threatens C-1/C-5, whose ranks are 1.00/0.99. None is answerable from magnitude-ranked `famrank` | Read raw band values along each of the six written-up traces; check striping periodicity, strain-band gradient, and gravity sign | the feature stack (same access as E8) |

## What killed (or would kill) each open entry

- E1 dies if template matches outside the catalogue convert to board score at
  ≤ the rate of random traces (one A/B decides it).
- E2 dies if the halo A/B loses to the skeleton by more than the public-split
  noise (~±0.005, our rough read of sibling-score spreads — labelled as such).
- E3 dies if edge layers merely re-express catalogue structure (high overlap,
  low gap-density).
- E5 dies if the board punishes the raised budget (FP tax realised).
- E8 cannot die, only cost: if the rebuilt table reproduces the current ordering,
  the contamination was immaterial and that is itself a result worth recording.
- E9 dies if the agreement channels also lose on the gap population — at which
  point they stay out and the brief's priority-3 axis is closed with evidence
  rather than with an assumption.
- E10 dies the candidates, not the hypothesis: a candidate killed by (a), (b) or
  (c) is removed from the written-up set and the reason is recorded here.
