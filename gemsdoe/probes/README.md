# gemsdoe/probes — the audit's runnable evidence

Five small scripts. They produced every measurement quoted in
[`../PIPELINE_AUDIT.md`](../PIPELINE_AUDIT.md) and
[`../CANDIDATE_GEOLOGY.md`](../CANDIDATE_GEOLOGY.md) §5–§6; they exist so the
next session can re-derive those numbers instead of trusting the write-up.

**They are deliberately not part of this repository's test suite.**
`MasterSelfLearn` is stdlib-only by rule (`AGENTS.md` §9 — `tests.yml` fails the
build if a dependency manifest appears), and these need `numpy`, `scipy` and
`rasterio`. They live outside `tests/` so `python3 -m unittest discover -s tests`
never collects them.

They also do not run against *this* repo — the pipeline under audit lives in
`6GEMSDOE`. Point them at a checkout:

```bash
pip install --break-system-packages numpy scipy rasterio
export GEMS_SRC=/path/to/6GEMSDOE/src           # default: ./src
export GEMS_TEMPLATE=/path/to/sample_submission.tif   # probe 3 only

python3 probe_cv_buffer.py       # D-2  — CV buffer vs the metric kernel
python3 probe_feature_guard.py   # D-1  — nan_gaussian NaN guard vs the stencil
python3 probe_real_footprint.py  # D-1 on official bytes, D-2 across fold layouts
python3 probe_crossder_halo.py   # D-5  — second_derivatives cross-term halo
python3 e10_falsification.py     # E10  — striping / strain-inheritance / gravity-sign
```

Probe 3 re-verifies the template's sha256 against `spec.PINS` before using it
and raises if it does not match, so it cannot silently measure the wrong grid.
`e10_falsification.py` needs `--features data/training_features.tif` and
`--candidates data/evidence/candidates.json` (see `--ids` to test specific
components).

| Probe | Finding | Result on the code as it stood | After the patch (session 4) |
|---|---|---|---|
| `probe_cv_buffer.py` | D-2 | 4 of 29 kernel offsets not excluded by the buffer | 0 |
| `probe_feature_guard.py` | D-1 | 95 affected-but-finite px at σ=1.5, 345 at σ=3.0 | 0 and 0 |
| `probe_real_footprint.py` | D-1 + D-2 | 32,461 px (0.63%) / 78,319 px (1.52%) unguarded on the official footprint; 100 leaked scored px at 6 blocks / 4 folds | 0 leaked px (all layouts) |
| `probe_crossder_halo.py` | D-5 (new, session 4) | 4 leaked `s`-px per NaN (the diagonal taps) | 0 |
| `e10_falsification.py` | E10 (a)/(b)/(c) | — (new instrument) | C-4 + 3/3 near-N–S flagged (a); C-7 cleared (b); C-1/C-5 basement-high (c) |

Every "after the patch" figure was measured on a scratch checkout with
[`../patches/session4_d1_d2_d3_d5_e9.patch`](../patches/session4_d1_d2_d3_d5_e9.patch)
applied — **46/46 of the pipeline's own tests still passed** there. The patch
has **not** been applied to `6GEMSDOE`: it is delivered for whichever repo is
ratified canonical, and only there.
