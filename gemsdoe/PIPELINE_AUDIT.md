# PIPELINE AUDIT — 2026-09-26 (session 3)

Audit of the live GEMS pipeline against session-brief items 1–5.

**Everything in this file was produced by running code this session**, not by
reading it. Where a claim is a measurement, the command that produced it is
named. Where something could not be run here, it is marked **UNVERIFIED**.

---

## 0. Where the pipeline actually is (correcting a premise in the brief)

The brief asks to "study our current feature engineering", "confirm
cross-validation is spatially-blocked", "confirm the metric-aware placement
step is intact", and "re-verify the submission generator with
`validate_submission.py`". **None of that code is in this repository.**

Verified this session:

```
$ find . -path ./.git -prune -o -name "*.py" -print     # 37 files
./msl/*.py  (21)  ./tests/*.py (14)  ./tools/*.py (2)
$ find . -path ./.git -prune -o -iname "*gems*" -print
./GEMSDOE_OWNERSHIP_FLAG.md   ./gemsdoe
```

`MasterSelfLearn` contains the autonomous research engine and this knowledge
library — no `features.py`, no `cv.py`, no `metric.py`, no `placement.py`, no
`validate_submission.py`, no rasterio anywhere. So items 1–5 have no artefact
in the repo the brief points at.

The pipeline the brief describes exists in **`6GEMSDOE`**, and only there in
this shape:

```
src/gems/{__init__,spec,features,cv,metric,placement,raster}.py
scripts/{validate_submission,build_submission,experiment,analysis,
         build_features,candidate_writeup,…}.py
tests/{conftest,test_gate,test_metric,test_spec_and_cv}.py
EXECUTIVE_SUMMARY.md  SUBMISSION_GUIDE.md  CANDIDATES.md  NEXT_STEPS.md
```

It was pulled read-only via `gh api` into a scratch checkout outside this repo
and audited there. **Nothing was written to any GEMSDOE repo this session.**

> **Flagged, not smoothed over.** Auditing a sibling repository's code from here
> is read-only and safe, but it is also the third session in a row that has had
> to *locate* the pipeline before it could improve it. That is a cost of the
> eleven-repo duplication, and it is the strongest practical argument for the
> consolidation that is still blocked on human ratification.

Environment used for every execution below: Python 3.11.2, numpy 2.4.6,
scipy 1.17.1, rasterio 1.4.4 (GDAL 3.10.3), pytest 9.1.1.

---

## 1. Feature engineering vs the three research priorities

The stack is built by `scripts/build_features.py` into a 105-channel memmap;
`data/evidence/features_meta.json` names all 105 and pins
`features_sha256 = 4371c82e3b8339b807bdffcf4ef59a225520fe2988d521be208ae33743123bc5`
— which matches `spec.PINS["training_features.tif"]` exactly.

| Brief priority | Channels present | In the shipped model? |
|---|---|---|
| **HGM on magnetic + gravity** | `tmi_hgm_computed`, `rtp_hgm_computed`, `mag_anom_hgm_computed`, `grav_hgm_computed`, `det_elev_hgm_computed`, multi-scale `hgm_{tmi,rtp,mag_anom,iso_grav_anom,det_elev}_s{1.5,3,6}` | **yes** (indices 21–24, 48–62) |
| **Tilt derivative** | `mag_tilt`, `grav_tilt`, `tdr_tmi_s{1.5,3}`, `tdr_iso_grav_anom_s{1.5,3}`, plus provider `tc` | **yes** (indices 20, 26, 69–75) |
| **Curvature + slope-break on DEM** | `curv_total/profile/plan/gaussian`, `slope_computed`, `slope_of_slope`, `curv_total_s{1.5,3}`, `curv_plan_s{1.5,3}`, `slope_of_slope_s{1.5,3}`, `std_det_elev_s3` | **yes** (indices 28–34, 76–83) |
| **Strain-rate × conductivity × earthquake density cross-reference** | `x_geod_shearrate__geod_dilaterate`, `x_cond_surf__depth_to_base_surf`, `x_ieq_n100a15__deq_n100a15`, `famrank_{mag,grav,strain,seis,cond,topo}`, `n_avail_fam`, `{max,mean,min}_famrank`, `n_agree_top{10,25,50}`, `agree_{strain_seis,strain_cond,seis_cond,strain_seis_cond}` | **only the three `x_*` products** |

### Finding F-1 — the shipped model drops the whole cross-reference layer

The shipped file was built with `--n-channels 88`, and that flag means *"use
only the first N channels of the stack"* (`build_submission.py:134`). Measured:

```
INCLUDED  (last of the 88):  [82] std_det_elev_s3 … [87] lin_rtp_coherence_s2
EXCLUDED  (indices 88..104):  famrank_mag … agree_strain_seis_cond
excluded = 17 channels; cross-signal agreement/family-rank = 17 of 17
```

So **100% of the excluded channels are exactly the brief's priority-3
cross-reference layer.** The three `x_*` products survive; the family ranks and
agreement counts — the channels that say "magnetics, gravity, strain,
seismicity, conductivity and topography all rank this pixel in their top 25%" —
do not reach the model.

This is a *measured* exclusion, not an oversight. On identical blocked folds:

| Run (blocked folds 4×4, buf 3 px, 400k neg, 300 iters) | 48 ch | 88 ch | 105 ch |
|---|---|---|---|
| `experiments_agreement.json` (2026-09-25T23:44:57Z), `topk_hard@0.03`, full-catalogue GT | 0.16283 | **0.16978** | 0.16704 |
| `experiments_itrace.json` (2026-09-26T00:15:13Z), trace-thinned GT | — | **0.16497** | 0.16309 |

105 channels loses 0.0027 and 0.0019 respectively. The decision is defensible
**on that instrument** — and that is the caveat (see §6).

### Finding D-3 — the flag's own help text is wrong about what it drops

`build_submission.py:134-137` reads:

> "use only the first N channels of the stack (0 = all). The blocked-CV
> comparison found the extra **multi-scale channels** did not improve the score,
> so the shipped model uses the validated subset."

Both halves are contradicted by the repo's own evidence:

- the multi-scale channels are indices 48–87 and **are included** in 88;
- they **did** improve the score: 88 ch = 0.16978 vs 48 ch = 0.16283 (+0.0070).

The channels 88 actually removes are the agreement block. A future session
reading this help text will draw the wrong conclusion about which features were
tested. Documentation defect; one-line fix, no behavioural change.

---

## 2. Cross-validation: spatially blocked and buffered — yes, but the buffer geometry is wrong

`src/gems/cv.py` is genuinely spatial: `make_folds()` cuts the grid into
`n_blocks × n_blocks` rectangles, deals them to folds, and
`train_test_masks()` returns `train = ~dilate(test, buffer_px)` and
`score = test`. No random pixel split anywhere; `sample_pixels()` only samples
*negatives inside an already-blocked mask*. `standardize()` in `features.py`
fits `mu`/`sd` on train only. That part is correct and worth stating plainly.

### Finding D-2 — the buffer is an L1 diamond, the kernel is an L2 disk

The metric kernel is a Euclidean disk of radius R = 300 m = 3.0 px
(`metric.kernel_offsets()`). `cv._dilate()` dilates with 4-connectivity, i.e. an
L1 diamond of radius 3. A diamond of radius 3 does not contain a disk of
radius 3. Measured with `probe_cv_buffer.py`:

```
metric kernel: 29 integer offsets with d <= 3.0 px
kernel offsets (k>0) NOT excluded by cv._dilate(mask, 3): 4
   offset (dy,dx)=(-2,-2)  d=2.8284 px  k=0.0572
   offset (dy,dx)=(-2,+2)  d=2.8284 px  k=0.0572
   offset (dy,dx)=(+2,-2)  d=2.8284 px  k=0.0572
   offset (dy,dx)=(+2,+2)  d=2.8284 px  k=0.0572
```

Is it live? **No — and that is luck, not design.** Measured leakage (scored
pixels having ≥1 training pixel within R = 3 px) across fold layouts, 373×329:

| `n_blocks`/`n_folds` | leakage before | after patch | fold-0 connected components |
|---|---|---|---|
| 4/4 (the shipped default) | 0 / 122,717 = 0.000% | 0.000% | **1** |
| 5/5 | 0.000% | 0.000% | 1 |
| **6/4** | **100 / 122,717 = 0.081%** | **0.000%** | 9 |
| 8/4 | 0.000% | 0.000% | 2 |
| 3/3 | 0.000% | 0.000% | 1 |
| 4/2 | 0.000% | 0.000% | 2 |

Every recorded run in `data/evidence/experiments*.json` used `n_folds ==
n_blocks`, which is why no published number is contaminated. The moment anyone
runs `n_blocks=6, n_folds=4` (a natural thing to try), the folds leak.

### Finding D-2b — each fold is one contiguous vertical stripe, not scattered blocks

```
make_folds(4,4,3).fold_of_block =
[[0 1 2 3]
 [0 1 2 3]
 [0 1 2 3]
 [0 1 2 3]]
```

`counter % n_folds` over a row-major walk gives **fold = block-column index**.
Each fold is therefore a single connected full-height slab, and
`ndimage.label` confirms `fold-0 connected components = 1`. `cv.py`'s own
docstring claims folds are dealt "in a strided pattern so that each fold's
blocks are spread over the region rather than clustered" — with
`n_blocks == n_folds` that is not what happens. A contiguous slab is a *weaker*
independence assumption than scattered blocks (it shares two long boundaries
with training data instead of eight short ones), and it is also what makes the
D-2 gap latent.

### Finding D-4 — the buffer test cannot catch any of this

`tests/test_spec_and_cv.py:49-61`:

```python
dilated = cv._dilate(score, 3)
assert not (train & dilated).any()
```

The assertion is built from the same `_dilate` the implementation uses, so it
verifies "train excludes whatever `_dilate` returns" — true by construction,
and silent on whether `_dilate` covers the kernel. Two lines above it, a dead
assertion:

```python
for r in rows:
    assert not train[r].any() or True      # always True; asserts nothing
```

### Patch (verified this session)

```python
# src/gems/cv.py
from scipy import ndimage
_SQ8 = np.ones((3, 3), dtype=bool)

def _dilate(mask, iterations):
    if iterations <= 0:
        return mask
    return ndimage.binary_dilation(mask, structure=_SQ8, iterations=iterations)
```

The L∞ square of radius 3 is a strict superset of the L2 disk of radius 3, so
this buffer can never be too small. **Applied to a scratch copy: 46/46 tests
still pass; unexcluded kernel offsets 4 → 0; the 6/4 leakage 100 → 0.**

The test should be rewritten to assert against `metric.kernel_offsets()`
directly, not against `_dilate`.

---

## 3. Metric-aware placement: intact, and the "~4–5 px spacing" premise is falsified at equal budget

The code is intact: `placement.thin_keep(mask, spacing)` (default 4),
`skeleton_spaced4` in `strategies()`, `get_strategy()` dispatch, Zhang–Suen
`_skeleton()`, `topk_mask()`, `gated_topk()`, and
`breakeven_posterior(k) = α(1−k)/(k(1+β)+α(1−k))` with `q*(2/3) = 0.052632`
pinned by `test_breakeven_posterior_matches_the_closed_form`. All 17
placement/spec tests pass.

But it is **not** the adopted placement, and it should not be. The brief's
premise is that ~4–5 px spacing is a good idea. Our own blocked folds say
otherwise, and — unlike the earlier fold-0 comparison in `cv.json` — this
comparison is **budget-matched**. From `experiments_agreement.json`, config
`extended` (88 ch), fold 0, `gt_full`:

| strategy | `n_pos_pred` | DTI | vs plain |
|---|---|---|---|
| `topk_hard@0.03` (shipped) | 27,875 | **0.13579** | — |
| `line3/topk_hard@0.03` | 27,877 | 0.11005 | **−19.0%** |
| `line5/topk_hard@0.03` | 27,880 | 0.09658 | **−28.9%** |
| `line9/topk_hard@0.03` | 27,878 | 0.07847 | **−42.2%** |
| `mix3/topk_hard@0.03` | 27,875 | 0.12086 | −11.0% |
| `mix5/topk_hard@0.03` | 27,875 | 0.11449 | −15.7% |
| `mix9/topk_hard@0.03` | 27,875 | 0.10907 | −19.7% |

Budgets agree to within 5 pixels out of ~27,875 (0.02%), so the loss is
attributable to spacing alone and it is **monotone in spacing**. `placement.py`
already derived why from the metric algebra; this is the measurement.

The shipped placement is `topk_hard@0.03` — dense top-3% of the footprint
written as 1.0 — which is a *budget* choice, not a geometry choice. Note the
nominal CV optimum is `topk_hard@0.05` (0.17502 vs 0.16978 at 88 ch); the
3% figure is a deliberate minimax-regret deviation documented in
`EXECUTIVE_SUMMARY.md` §3 against thinned ground truth. That reasoning is sound
and is left standing.

### Irregularity I-1 — two of our own instruments disagree on the sign of the spacing effect

`GEMSDOE3`'s published live-board pair reads the other way: `pindrop-v4-nodes`
(spacing 4) 0.1193 vs `pindrop-v4-ridge` (spacing 1, dense control) 0.1152 at
the same 155,021-px budget → **+0.0041 for spacing on the real board**, while
our blocked folds give **−0.019 to −0.042 for spacing against the catalogue**.

Not resolved here, and deliberately not explained away:

- the DrivenData registrations behind those rows are **not verifiably ours**
  (see `../GEMSDOE_OWNERSHIP_FLAG.md`), so this is not a controlled arm of our
  own experiment;
- the catalogue proxy rewards dense coverage of *contiguous known* traces,
  whereas the board scores *hidden* faults, which may be shorter and more
  isolated — a real reason for the signs to differ;
- the two files may differ in more than spacing. Their construction is
  documented on that site, not here.

Carried as an open instrument conflict, not as a result.

---

## 4. Submission generator: re-verified end to end, including a negative test

`scripts/validate_submission.py` → `gems.raster.check_submission()` enforces 13
checks. Re-run this session on the file the site actually offers:

```
$ sha256sum downloads/gems6_hgb88-topk03_33cec71ff0.tif
33cec71ff00b3f32d0d59c81c156f3f1488ffef46baa4b6499094e24ea1875ab   # matches the pin

$ python3 scripts/validate_submission.py downloads/gems6_hgb88-topk03_33cec71ff0.tif
SUBMISSION FORMAT GATE: PASS
[PASS] single-band … dtype-float32 … crs-epsg32611 … resolution-100m
[PASS] shape: (3730, 3292), expected (3730, 3292)
[PASS] geotransform: (100.0, 0.0, 243350.0, 0.0, -100.0, 4508550.0)
[PASS] nodata-nan: nan
[PASS] values-in-0-1: finite range = [0.0, 1.0]
[PASS] no-inf / template-verified (footprint = 5167373 px)
[PASS] NAN-INSIDE-FOOTPRINT: 0 non-finite pixels inside the scored footprint
[PASS] footprint-matches-official: 0 finite pixels outside the official footprint
stats: total=12279160 finite=5167373 nan=7111787 positive=155021
EXIT CODE: 0
```

**The negative test — the one that proves the gate catches the right thing.**
One NaN injected at (936, 1221), inside the footprint, on a copy:

```
[PASS] values-in-0-1: finite range = [0.0, 1.0]     <-- still passes!
[FAIL] NAN-INSIDE-FOOTPRINT: 1 non-finite pixels inside the scored footprint
HARD GATE FAILED — do NOT upload this file.
EXIT CODE: 1
```

This reproduces the platform's misleading `"Predicted values must be in range
[0, 1]"` condition exactly: every finite value is legal, the range check passes,
and only the footprint-aware check fails. The gate is catching the real
condition, not a proxy. Fail-closed behaviour is also correct: a missing or
hash-mismatched template produces a hard `template-verified` FAIL and exit 1
rather than silently skipping rule 9.

Independent re-verification of the spec, from official bytes:
`data/sample_submission.tif` sha256 = `2176d08e485aa2cd2860ce8df539db4faf4d76163b38a4dd8c30a40454d35cbc`
(matches `spec.PINS`), finite pixels = **5,167,373** (matches
`spec.FOOTPRINT_PIXELS` exactly).

**Test suite:** `python3 -m pytest tests/ -q` → **46 passed** (12 gate +
17 metric + 17 spec/cv).

Minor: `raster.py`'s module docstring lists rule 9 as "the file's own nodata
declaration is NaN", but the code accepts `nodata is None` as well. Harmless
for our file (declared `nan`); the docstring overstates the check.

---

## 5. Feature-boundary contamination — the largest measured defect

### Finding D-1 — `nan_gaussian`'s NaN guard does not cover the filter's stencil

`features._guarded_filter()` re-invalidates an L1 **diamond** of radius
`ceil(3σ)` around every NaN. But `scipy.ndimage.gaussian_filter` has a **square**
support of radius `int(truncate·σ + 0.5)` (truncate defaults to 4.0). Two
mismatches at once: wrong shape, and too small. Measured by injecting a single
NaN and finding every output pixel that changed (`probe_feature_guard.py`):

| σ | guard radius as coded | scipy stencil radius | affected-but-still-finite | worst missed offset |
|---|---|---|---|---|
| 1.5 | 5 (L1 diamond) | 6 (square) | **95** | (6, 5), L1 = 11 |
| 3.0 | 9 (L1 diamond) | 12 (square) | **345** | (9, −12), L1 = 21 |

So a single NaN up to **12 px away** changes a smoothed value and the result is
still reported as a finite, valid measurement.

Scaled to the **real official footprint** (sha-verified sample submission,
`probe_real_footprint.py`):

| σ | footprint pixels in the stencil reach of a NaN but *not* invalidated | share of footprint |
|---|---|---|
| 1.5 | **32,461** | 0.63% |
| 3.0 | **78,319** | 1.52% |

For scale, the entire label set is 60,988 pixels — the contaminated band is
**0.5×–1.3× the size of all the training truth there is.** And it lands exactly
where the brief's priorities live: `curvature_at_scale()` calls `nan_gaussian`
first, and `structure_tensor()` calls it three times, so the curvature,
slope-break and lineament channels are the most exposed. With 7,111,787 NaN
pixels the footprint boundary is everywhere, not an edge case.

This is a **precision** defect, not a crash: the channels are silently wrong
near boundaries, so the model is learning partly from filter artefacts. It
biases every blocked-CV number in `data/evidence/`, in an unknown direction.

### Patch (verified this session)

```python
# src/gems/features.py
_SQ8 = np.ones((3, 3), dtype=bool)

def _filter_reach(sigma: float, truncate: float = 4.0) -> int:
    """scipy.ndimage.gaussian_filter's own stencil half-width."""
    return int(truncate * sigma + 0.5)

# in _guarded_filter:
grown = ndimage.binary_dilation(bad, structure=_SQ8, iterations=radius)
# in nan_gaussian / local_std:
r = _filter_reach(sigma)          # was int(np.ceil(3 * sigma))
```

`nan_uniform` needs the same square structure (`uniform_filter` is also a
square stencil of radius `size//2`).

**Applied to a scratch copy: 46/46 tests still pass; affected-but-finite pixels
95 → 0 at σ=1.5 and 345 → 0 at σ=3.0.**

**Consequence:** the feature stack must be rebuilt and the whole experiment
table re-run before any of it is trusted again. `build_features.py` took
917.1 s last time; the experiment runs are the expensive part.

---

## 6. What this means for score quality

Ranked by expected effect, each with the test that decides it:

1. **Rebuild features with D-1 fixed, re-run the CV table.** Every number in
   `data/evidence/experiments*.json` was computed on boundary-contaminated
   channels. Until this is re-run we do not actually know which feature set is
   best — we know which was best *given the contamination*. Highest priority
   because it invalidates the ordering of everything else.
2. **Re-test the agreement layer (F-1) on the right instrument.** It lost by
   0.0019–0.0027 on the *catalogue* proxy. That proxy is the one instrument
   structurally blind to what those channels are for: strain/conductivity/
   seismicity agreement carries information independent of the catalogue's
   mapping history, so its value should show up on catalogue-*gap* populations,
   not on the catalogue itself. Test on the block-holdout / cross-catalogue
   instrument. This is the brief's priority-3 axis and it is currently
   switched off.
3. **Fix D-2/D-2b before trying any new fold layout.** Two-line patch, already
   verified. Cheap insurance against a silent leak in the next experiment.
4. **Drop the spacing question.** Settled at equal budget (§3). Spend the
   effort on E1/E3/E4 in `HYPOTHESES.md` instead.
5. **Fix the D-3 help text** so the next session does not re-derive a false
   conclusion about which features were tested.

---

## Reproducing this audit

```bash
# read-only pull of the pipeline under audit (never a write)
gh api -H "Accept: application/vnd.github.raw" \
  "repos/buffedlizard55-lab/6GEMSDOE/contents/<path>" > <path>

pip install --break-system-packages numpy scipy rasterio pytest
python3 -m pytest tests/ -q                     # 46 passed
python3 scripts/validate_submission.py downloads/gems6_hgb88-topk03_33cec71ff0.tif
python3 gemsdoe/probes/probe_cv_buffer.py       # D-2
python3 gemsdoe/probes/probe_feature_guard.py   # D-1
python3 gemsdoe/probes/probe_real_footprint.py  # D-1 on official bytes + D-2 layouts
```

The probes need `GEMS_SRC` (default `src`) pointing at a checkout of the
pipeline repo; they are **not** part of this repo's stdlib-only test suite and
are not collected by `python3 -m unittest discover -s tests`.
