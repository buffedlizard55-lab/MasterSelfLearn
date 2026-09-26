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

## What killed (or would kill) each open entry

- E1 dies if template matches outside the catalogue convert to board score at
  ≤ the rate of random traces (one A/B decides it).
- E2 dies if the halo A/B loses to the skeleton by more than the public-split
  noise (~±0.005, our rough read of sibling-score spreads — labelled as such).
- E3 dies if edge layers merely re-express catalogue structure (high overlap,
  low gap-density).
- E5 dies if the board punishes the raised budget (FP tax realised).
