# FIELD & METRIC — what is scored, and what the field is doing

Everything in §1–§2 was re-read from the primary sources on 2026-09-26
(session 2); §3 is the same-day leaderboard; §4 is verbatim rules text;
§5 is **our own analysis** and is labelled as such.

---

## 1. The scoring metric (verified against page 967, 2026-09-26)

Source: <https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/#performance-metric>

Submission: one GeoTIFF, EPSG:32611 (UTM 11N), 100 m resolution, same bounds
as the training data, single band float32, values in [0,1] = per-pixel fault
confidence, NaN outside the footprint.

Distance-weighted Tversky index with triangular kernel k(d) = max(1 − d/R, 0),
R = 300 m (= 3 px at 100 m):

- `TP_w = Σ_{g∈G} max_{x: d(x,g)≤R} p(x)·k(d(x,g))` — each ground-truth pixel
  is credited from its **single best** prediction inside the kernel.
- `FP_w = Σ_{x: p(x)>0} p(x)·[1 − max_{g∈G} k(d(x,g))]` — each predicted pixel
  pays, discounted by proximity to the nearest truth pixel.
- `FN_w = Σ_{g∈G} [1 − max_{x: d(x,g)≤R} p(x)·k(d(x,g))]` — each truth pixel
  pays for how little of it was covered.

`DTI(α,β) = TP_w / (TP_w + α·FP_w + β·FN_w + ε)`, with **α = 0.2** (false
positives), **β = 0.8** (false negatives). Quote: *"we set α=0.2 and β=0.8,
which reduces the penalty for false positive predictions and increases the
penalty for false negative predictions."*

Kernel credits at 100 m pixels: distance 0 → 1.0; 1 px → 2/3; 2 px → 1/3;
≥3 px → 0.

Both rounds score the **new-fault** population: Phase 1 a private subset of
expert-labelled faults absent from the USGS catalogue; Phase 2 the expanded
label set after experts review every team's predictions (rules §1.1; page
967). One submission, chosen blind, scores in both rounds.

### 1b. Official staff clarification: known-fault pixels are MASKED from scoring (verified 2026-09-26)

Source: DrivenData community forum, thread 11516, reply by **chrisk-dd
(DrivenData Staff)** on Sep 16 —
<https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516>
(fetched 2026-09-26, session 4; the question was asked by entrant `exposed`):

> 1. Pixels corresponding to known USGS/INGENIOUS faults are masked / excluded
>    from evaluation, so they do not count towards penalty terms.
> 2. Re-evaluation will also mask/exclude the existing USGS/INGENIOUS faults.
>
> We'll consider changing the description, but for scoring purposes it should
> not matter whether these known faults are included with predictions or not.

This is an official, on-platform statement by the prize administrator and it
**outranks any inference from the metric formula alone**:

- `TP_w`, `FP_w` and `FN_w` are computed on the **masked** grid: pixels at
  known USGS/INGENIOUS faults contribute to *no* term, in *either* round.
- Emitting predictions on (or, subject to the mask's unknown width, near) the
  supplied catalogue is therefore **free** — no penalty, no credit.
- **Irregularity, flagged not smoothed:** the mask's spatial extent is not
  specified ("pixels corresponding to known faults" — the 60,988 label pixels
  themselves? a buffer?). Staff wrote "it should not matter whether these known
  faults are included with predictions or not", which is consistent with a
  mask at least as wide as the label pixels. The conservative free move is
  emission *on* catalogue pixels; corridor widths beyond that are a measured
  bet, not a rule.
- **Our local metric does not implement the mask.** `6GEMSDOE/src/gems/metric.py`
  scores against `labels.tif` as ground truth with no exclusion zone, so every
  local DTI in the evidence files charges FP_w for catalogue-adjacent emission
  the real scorer never sees. Local numbers remain valid as *relative* monitors
  on the catalogue population, and are wrong as absolute predictors of board
  values in a second way (in addition to the wrong-population problem below).

## 2. What the reference baseline does (verified, official)

Source: <https://github.com/drivendataorg/gems-prize-reference-solution>
(notebook read this session via `gh api`; author Prof. John Lipor, Portland
State University; repo created 2026-06-16, single notebook
`unet-mc-cv-reference-solution.ipynb`):

- U-Net (`segmentation_models_pytorch`) on the 100 m feature stack, channels
  min-max normalised to [0,1]; labels binarised (`y<1 → 0`).
- **TverskyLoss with alpha=0.2, beta=0.8** — the competition metric as loss.
- Monte-Carlo cross-validation: **5 random train/test patch splits**
  (patch 128 px, test_proportion 0.5, train step 32 → overlapping),
  batch 32, epochs 5, lr 1e-4; augmentations: random resized crop, flips,
  ±30° rotation. Predictions of the splits are combined; the notebook notes
  *"it may be advantageous to threshold this map for better scoring"* and
  shows a >0.1 threshold.

Implication: the official floor is a supervised U-Net ensemble on the
catalogue labels. Every score above it on the hidden new faults must come
from generalisation **beyond** the catalogue (new geometries, new locations,
better recall), since the test set is by construction not in the catalogue.

## 3. Field state — fresh pull 2026-09-26T≈18:55Z (session 4)

Source: <https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/>
(full table in `SESSION_LOG.md` session 4 §4). Summary:

- Field high **0.3049** (DARD, #1, 10 subs) — unchanged across all four
  sessions. Phase-1 pay line (top five, $10K each) sits at **0.2589**
  (#5 joeyfezster) — also unchanged.
- The board is dense and active through #50 (50 rows visible; new entrants
  `GrigorSargsyan` #6 0.2504 and `hiii12345` #9 0.2262 appeared near the top
  since session 3).
- The five tracked rows (attribution per the brief; registration ownership
  still unverifiable from public data — flag F5): **0.1563** (#24 extradr19,
  2 subs), **0.1563** (#25 SDCF9, **2 subs, activity 35 min before the pull**),
  0.1560 (#26 smashi34), 0.1193 (#41 smrtdoog5), 0.0830 (#50 wbg1).
- **Movement flagged:** `SDCF9` (one of the three GEMSDOE3-site rows) moved
  0.1152 → **0.1563** with a second submission *during session 4*. Per the
  brief these registrations are not treated as our data or as experiment arms
  of ours; recorded as field movement only.
- Gap from the best tracked row to the pay line: **+0.1026**; to field high:
  +0.1486.

## 4. Rules text that constrains us (verbatim, read 2026-09-26)

Source: <https://www.nlr.gov/docs/fy26osti/96647.pdf> — full document read
all 7 chunks this session (session 1 had A.3/A.16 outstanding; now closed).

- §1.1: *"Participants will submit a single entry, which will be evaluated in
  two prize phases using a distance-weighted Tversky index."*
- §3.2: three submissions per week; generative-AI use allowed but must be
  disclosed in the narrative; the competitor *"is responsible for the
  accuracy, authenticity, and authorship representations"* of AI-assisted
  content.
- §3.4: *"Multiple finalized submissions are not allowed. Each participating
  entity (team, organization, or individual prize competitor not on a team)
  is allowed to have one final submission; individuals participating on a
  team will not be allowed to submit a separate final submission."*
- §3.6.2: the single scored submission must be chosen **without knowledge of
  private-set scores**.
- §1.3 / A.1: perjury certification of eligibility (U.S. citizen/permanent
  resident for individuals; 18 U.S.C. § 1001 and § 287 exposure).
- A.2: *"If a dispute arises related to any registration, the authorized
  account holder of the email address used to register will be considered the
  competitor."*
- A.3: *"The prize administrator will award a single dollar amount to the
  designated primary submitter, whether consisting of a single entity or
  multiple entities."*
- A.12: DOE may cancel for fraud; *"All applications submitted to DOE are
  subject to a due diligence review"* incl. a foreign-interference risk review.
- A.16: funds returned if the prize *"was made based on fraudulent or
  inaccurate information."*

## 5. Strategic consequences — OUR analysis (derivation, not citation)

From the metric in §1. Labelled D1–D6; each states its assumption.

- **D1 — the metric is recall-priced with a cheap, proximity-discounted FP
  tax.** A predicted pixel at confidence 1 far from any truth costs α·1 = 0.2;
  a truth pixel fully missed costs β·1 = 0.8; a truth pixel covered at
  distance 0 by p=1 gains ~1 TP while zeroing that FN term. Marginal
  break-even (first-order, holding the denominator fixed): emit at a candidate
  pixel when P(it covers an otherwise-uncovered truth pixel) ≳ α/(α+β) = 0.2.
  Assumption: the candidate would otherwise not be covered; denominator
  effects are second order here.
- **D2 — placement accuracy is worth more than mass.** Credit per truth pixel
  is `max`, not sum, inside the kernel: piling pixels along an already-covered
  trace adds TP_w ≈ 0 and FP_w > 0. This matches the one clean live A/B we
  have: GEMSDOE3's equal-budget nodes-vs-ridge (0.1193 vs 0.1152, +0.0041).
- **D3 — the 300 m kernel forgives registration error only up to ~2 px.**
  Credit at 1 px = 2/3, at 2 px = 1/3. A trace located 300 m off an expert
  trace earns nothing from it. Any candidate source with better-than-100 m
  geolocation is a direct scoring asset; the problem page itself notes parts
  of the existing fault data may be misaligned from the true surface fault.
- **D4 — the skeleton-vs-halo question is unresolved on the real population.**
  GEMSDOE's surrogate sweep found width 0 optimal — but against the catalogue,
  where the labels are already 1-px lines, a tautological setting. On the
  hidden expert traces the same geometry likely holds, yet D3's forgiveness
  window argues for a *soft* halo (decaying p) rather than binary 0/1, since
  a halo is a hedge against the predictor's own geolocation error at near-zero
  FP cost near the trace. This is a live contradiction between two of our own
  measurements; only a public-leaderboard A/B can settle it (costs one of the
  3 weekly submissions of the confirmed account).
- **D5 — the 0.15 → 0.30 gap is a recall gap on the unmapped population.**
  An entry that only re-expresses catalogue-adjacent structure is capped by
  how much the experts' new set coincides with it. Entries near 0.30 must be
  emitting substantially more *true* hidden-trace pixels: i.e. they are
  finding candidate faults from evidence the catalogue lacks — 1 m DEM scarps,
  magnetic/radiometric lineaments, strain and seismicity concentrations,
  trace extensions, step-overs and intersections — exactly the families in
  `RESEARCH_LIBRARY.md`.
- **D6 — Phase 2 rewards defensible candidates.** Experts expand the label set
  by reviewing **every team's** predictions. A prediction that flags a real,
  previously-unlabelled fault can gain Phase-2 credit even if it did not
  overlap Phase-1 labels — but the same file is chosen blind for both rounds,
  so the rational posture is: high recall over candidates with *geologically
  defensible* evidence, and no mass spent on indefensible noise (it pays FP
  tax in Phase 1 and earns nothing in Phase 2).
- **D7 (session 4, from §1b) — the catalogue is a free emission zone, and the
  budget calculus changes with it.** The 3%-vs-5% minimax-regret analysis
  assumed every off-truth pixel pays α·p. Under the staff-confirmed mask,
  catalogue pixels pay nothing, so the optimal file is (catalogue ∪ confident
  candidates): the union can only help where expert "new" labels coincide with
  the catalogue (corrections/registrations) and cannot hurt on the masked
  pixels. The 5GEMSDOE "S5-A catalogue hedge" (field + the 54,533 missing
  catalogue px) and GEMSDOE2's "extension arm" (union + 300 m corridor) are
  the concrete forms of this; the hedge is safe under either reading of the
  mask width, the corridor is a measured bet on extensions. Assumption: the
  mask covers at least the label pixels themselves.
- **D8 (session 4) — our surrogate instruments double-count FP near the
  catalogue.** Because `metric.py` has no mask, a candidate whose pixels ride
  next to known faults is under-ranked locally relative to its board value,
  and the gap between our 0.17-class CV numbers and board-class numbers is
  not only the wrong-population gap (D5) but also the unmasked-FP gap. Any
  future local experiment claiming board relevance should implement the
  §1b mask as far as it can be pinned (mask ≥ the 60,988 label px) and report
  both masked and unmasked numbers.

### What a higher-scoring approach must therefore be doing differently

1. Mining the **1 m DEM** (716 tiles confirmed in the GEMSDOE inventory
   against the USGS 3DEP bucket) for scarp-like curvature signatures outside
   the catalogue — the single richest source for young, unmapped surface
   faults (see Sare et al. 2019 in the research library).
2. Deriving **edge fields from the GeoDAWN magnetic bands** (the provided
   stack already ships RTP anomaly, TMI, and the vertical/horizontal slope of
   TMI; tilt-type filters add depth-balanced edges) and intersecting them
   with other evidence rather than using any single layer.
3. Stacking the **provided strain-rate, seismicity-density, and conductivity
   bands** as a fault-likelihood prior focused on catalogue gaps — the same
   ingredients Great Basin play-fairway studies use for permeability.
4. **Extending** catalogue traces (tips, splays, step-overs, intersections) —
   Faulds-type PFA factor maps treat those settings as permeability sweet
   spots, and experts extending known traces is the most likely "new fault"
   geometry.
5. Emitting with **metric-aware geometry**: near-binary confidence on
   high-evidence traces, soft 1–2 px halos as geolocation insurance, budget
   spent on covering *more distinct traces* rather than thickening covered ones.

## 6. Known baselines and floors

| Quantity | Value | Source |
|---|---|---|
| Blanket-coverage floor (predict-everything) DTI vs supplied labels | 0.0956 | GEMSDOE site (its measured value; surrogate population) |
| Catalogue-trained U-Net MC-CV (official reference) | not publicly scored | reference-solution repo; no public leaderboard row attached |
| Our tracked best (public board) | 0.1563 (#22) | leaderboard pull 2026-09-26 |
| Phase-1 pay line at pull time | 0.2589 (#5) | same pull |
| Field high | 0.3049 (#1) | same pull |
