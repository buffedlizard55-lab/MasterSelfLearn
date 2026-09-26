# REBUILT EXPERIMENTS — session 4 (2026-09-26): E8 and E9, executed

The two experiments `HYPOTHESES.md` E8/E9 queued: rebuild the feature stack
with the NaN-guard defect (D-1) fixed and re-run the experiment table, then
re-test the 17-channel agreement layer on a catalogue-*gap* instrument. Both
were executed this session on a scratch checkout of `6GEMSDOE@e2fe3f41` with
[`patches/session4_d1_d2_d3_d5_e9.patch`](patches/session4_d1_d2_d3_d5_e9.patch)
applied. **Nothing here is a leaderboard value** — every number is blocked-CV
surrogate DTI, and the population it is measured on is named in each table.

Environment: Python 3.11.2, numpy 2.4.6, scipy 1.17.1, rasterio 1.4.4 (GDAL
3.10.3), scikit-learn 1.9.1, pytest 9.1.1. Hardware: 2 CPU / 4 GB class host.

Provenance (all re-measured this session):

| Object | Value |
|---|---|
| `data/training_features.tif` (assembled from the 5 pinned bridge parts) | sha256 `4371c82e3b8339b807bdffcf4ef59a225520fe2988d521be208ae33743123bc5` — **matches `spec.PINS`** |
| `data/labels.tif` / `data/sample_submission.tif` | from the repo; gate re-verified against `spec.PINS` (template `2176d08e…`, footprint 5,167,373 px) |
| Rebuilt features (`features.f32.npy`, 3730×3292×105) | built 2026-09-26T19:05:36Z in 956.7 s; invalid/valid masks identical to the committed meta (7,113,320 / 5,165,840) |
| Pipeline test suite on the patched tree | **46/46 pass** (the buffer test is strengthened: it now asserts against `metric.kernel_offsets()`, not against the implementation's own helper) |
| `validate_submission.py` on the shipped file | **13/13 PASS** incl. `NAN-INSIDE-FOOTPRINT`; negative test (one NaN injected at (936, 1221), inside the footprint) → `values-in-0-1` still passes, `NAN-INSIDE-FOOTPRINT` FAILS, **exit 1** |

Patched-and-probed defect counts (before → after): D-1 leaked px 95/345 → **0**;
D-2 unexcluded kernel offsets 4 → **0**, 6/4-layout leak 100 px → **0**; D-5
leaked cross-derivative px per NaN 4 → **0** (new defect found this session —
`second_derivatives`' mixed-derivative stencil taps diagonal neighbours its
4-connected halo never covered).

---

## 1. E8 — the experiment table on the fixed stack

`scripts/experiment.py --configs baseline,extended,agreement --max-train-px
400000 --iters 300` — the exact settings of the reference run
(`data/evidence/experiments_agreement.json`, generated 2026-09-25T23:44:57Z on
the contaminated stack). Same folds (4×4 blocks, 3 px buffer), same seeds.
Output: `data/evidence/experiments_e8_d1fix.json` in the scratch checkout.

Mean blocked-CV DTI vs the **full catalogue** ground truth (`gt_full`):

| config | ch | topk@0.03 old → new | topk@0.05 old → new | hard@0.2 old → new |
|---|---|---|---|---|
| baseline | 48 | 0.16283 → 0.15876 (−0.0041) | 0.16940 → 0.16411 (−0.0053) | 0.16676 → 0.16013 (−0.0066) |
| **extended (shipped)** | **88** | **0.16978 → 0.16973 (−0.0001)** | 0.17502 → 0.17274 (−0.0023) | 0.17022 → 0.16914 (−0.0011) |
| agreement | 105 | 0.16704 → 0.16170 (−0.0053) | 0.17056 → 0.16698 (−0.0036) | 0.16739 → 0.16267 (−0.0047) |

**Verdict (the pre-registered reading in `HYPOTHESES.md` E8: "if the rebuilt
table reproduces the current ordering, the contamination was immaterial and
that is itself a result worth recording"):**

1. **The ordering reproduces: 88 > 105 > 48 on every column, before and
   after.** The D-1 contamination did not distort the feature-set ranking.
   The session-3 fear ("the current feature ranking is unknown") resolves to:
   the ranking is *known* and stable under the fix.
2. **Magnitudes moved down slightly** (−0.000 to −0.007). The contaminated
   boundary band was mildly *score-inflating*, not score-suppressing — the
   wrong-pixels problem was real (0.63–1.52% of the footprint) but its effect
   on this instrument was small and slightly flattering.
3. The shipped 88-channel axis is essentially unchanged at the shipped budget
   (0.16978 → 0.16973 at topk@0.03). **The shipped file does not need to be
   rebuilt for correctness of its selection** — but see E9 for the selection
   question that does change.

Caveats: (a) the rank-table file hash drifted between the original build
(`64a62c3b…`) and this rebuild (`9368d6a9…`) from the same pinned raster —
bit-stability of `build_rank_tables.py` across environments is **not**
confirmed (irregularity, flagged); this affects only the 17 agreement channels,
so the 48/88 rows are clean and the 105 row carries the drift on top of the
D-1/D-5 change. (b) n = 4 folds; fold spread at topk@0.03 is wide (88ch:
0.131–0.197) — the means are what the earlier table used, same yardstick.

---

## 2. E9 — the agreement layer on a catalogue-GAP instrument

Design (implemented in the delivered patch as `trace_gap` / `trace_seen`
scoring under `--trace-holdout`): hold out **960 whole fault traces (30%,
18,116 gt px) from training in every fold** — the model has never seen them as
positives — then score the held-out traces alone (`trace_gap`) against the
same fixed placement set. This is the `cross-catalogue` instrument of
`HYPOTHESES.md` E9: the closest honest proxy carrying ground truth for "faults
missing from the training catalogue", which is what both prize rounds score
(rules §1.1). `trace_seen` (the complement) and `gt_full` are reported beside
it. Same folds, same budget (400k neg / 300 iters), same seeds.

Run: `scripts/experiment.py --configs extended,agreement --trace-holdout 0.3
--max-train-px 400000 --iters 300` → `data/evidence/experiments_e9_gap.json`.
Gap gt per fold: 4,164 / 7,574 / 4,950 / 1,428 px.

Mean DTI — **88 ch vs 105 ch at identical placement budget**:

| placement | gap 88 → 105 (Δ) | seen 88 → 105 (Δ) | gt_full 88 → 105 (Δ) |
|---|---|---|---|
| topk_hard@0.01 | 0.0712 → **0.0750 (+0.0038)** | 0.1126 → 0.1088 (−0.0038) | 0.1168 → 0.1157 (−0.0011) |
| topk_hard@0.02 | 0.0744 → **0.0780 (+0.0036)** | 0.1345 → 0.1296 (−0.0049) | 0.1468 → 0.1450 (−0.0018) |
| topk_hard@0.03 | 0.0713 → **0.0736 (+0.0023)** | 0.1397 → 0.1362 (−0.0035) | 0.1578 → 0.1567 (−0.0012) |
| topk_hard@0.05 | 0.0659 → 0.0663 (+0.0004) | 0.1401 → 0.1339 (−0.0062) | 0.1662 → 0.1615 (−0.0047) |
| hard@0.2 | 0.0717 → 0.0702 (−0.0014) | 0.1338 → 0.1286 (−0.0052) | 0.1529 → 0.1487 (−0.0041) |
| hard@0.3 | 0.0646 → **0.0708 (+0.0062)** | 0.1049 → 0.1051 (+0.0002) | 0.1119 → 0.1152 (+0.0034) |

**Verdict — the sign of the agreement-layer effect flips with the population,
exactly as HF/E9 pre-registered:**

1. **On gap truth, 105 ch wins 5 of 6 placements** (+0.0023 to +0.0062;
   +3% to +10% relative). It is also more robust at the tight budgets: at
   topk@0.01 the 105-ch worst fold (0.0580) beats the 88-ch worst fold
   (0.0439), and at topk@0.02 likewise (0.0640 vs 0.0557).
2. **On seen and full-catalogue truth, 105 ch loses 5 of 6 / 4 of 6** — the
   same numbers that made the earlier sessions drop the layer (HF) are
   reproduced, and they are now explained: the catalogue proxy rewards
   re-expressing mapping history, and the agreement channels carry the
   information *independent* of mapping history. The one instrument the
   decision was made on is the one instrument that cannot see their value.
3. **For the actual target ("faults missing from the catalogue"), the gap
   instrument is the relevant one**, so the brief's priority-3 axis
   (strain × conductivity × seismicity cross-reference) should be
   **re-enabled in target-oriented builds**. HF's status splits: falsified on
   the catalogue proxy (unchanged), **supported on the gap population**.

Caveats, stated rather than smoothed:

- **The gap population is still catalogue-character.** Held-out traces are
  faults *like* the mapped ones the model never saw; the hidden expert set is
  faults the mappers missed. If those differ systematically (shorter, subtler,
  different geology), the effect size transfers only as a direction, not as a
  number. The sign flip is the finding; the +0.003 is a lower bound on nothing.
- **Rank-table hash drift** (see E8 caveat (a)) rides on the 105-ch rows.
- Restricted-GT scoring charges FP for predictions on the *other* population
  (fixed across configs — both pay it), and the local metric does not implement
  the official known-fault **mask** (D8, `FIELD_AND_METRIC.md` §1b) — also
  fixed across configs. Both blur absolute values; neither can create a sign
  flip between two configs scored on identical machinery.
- n = 4 folds with 1,428–7,574 gap px per fold; the consistency across
  placements is the strength of the result, not any single cell.

---

## 3. What this changes about the shipped file (recommendation, not action)

The shipped `gems6_hgb88-topk03_33cec71ff0.tif` was selected with the
catalogue proxy. Two session-4 findings bear on the next build:

1. **Include the agreement channels for gap discovery (E9).** A natural next
   build is a *union* placement: the 88-ch surface where it is strong
   (catalogue-adjacent, seen-type structure) plus 105-ch gap-priority
   candidates — or simply the 105-ch surface at topk@0.02, where it wins its
   largest robust margin. Nothing was built or submitted this session (no
   sanctioned slot; no ratified account).
2. **Catalogue emission is free under the official mask (HI/D7).** The next
   file should contain the catalogue union regardless of budget (the
   5GEMSDOE "S5-A catalogue hedge" form) — it cannot score lower under either
   reading of the mask, and Phase-2 experts review the file's coverage of
   known structure favourably in any case (D6).

Both are board-testable with one sanctioned submission (HYPOTHESES E11).

## 4. Reproduction

```bash
# scratch checkout + patch (never a write to a GEMSDOE repo)
git clone --depth 1 https://github.com/buffedlizard55-lab/6GEMSDOE.git pipeline
cd pipeline && git apply ../gemsdoe/patches/session4_d1_d2_d3_d5_e9.patch
cat data/bridge/gems-geodawn-numerical-features.tif.part-00{0,1,2,3,4} \
    > data/training_features.tif           # sha256 4371c82e… (spec.PINS)
python3 -m pytest tests/ -q                # 46 passed
python3 scripts/build_rank_tables.py       # 124 s  (hash drift caveat applies)
python3 scripts/build_features.py          # 957 s
python3 scripts/experiment.py --configs baseline,extended,agreement \
    --max-train-px 400000 --iters 300 --out data/evidence/experiments_e8_d1fix.json
python3 scripts/experiment.py --configs extended,agreement --trace-holdout 0.3 \
    --max-train-px 400000 --iters 300 --out data/evidence/experiments_e9_gap.json
python3 scripts/validate_submission.py downloads/gems6_hgb88-topk03_33cec71ff0.tif
```
