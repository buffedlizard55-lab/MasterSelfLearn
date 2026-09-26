# gemsdoe/probes — the audit's runnable evidence

Three small scripts. They produced every measurement quoted in
[`../PIPELINE_AUDIT.md`](../PIPELINE_AUDIT.md); they exist so the next session
can re-derive those numbers instead of trusting the write-up.

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
```

Probe 3 re-verifies the template's sha256 against `spec.PINS` before using it
and raises if it does not match, so it cannot silently measure the wrong grid.

| Probe | Finding | Result on the code as it stands | After the recommended patch |
|---|---|---|---|
| `probe_cv_buffer.py` | D-2 | 4 of 29 kernel offsets not excluded by the buffer | 0 |
| `probe_feature_guard.py` | D-1 | 95 affected-but-finite px at σ=1.5, 345 at σ=3.0 | 0 and 0 |
| `probe_real_footprint.py` | D-1 + D-2 | 32,461 px (0.63%) / 78,319 px (1.52%) unguarded on the official footprint; 100 leaked scored px at 6 blocks / 4 folds | 0 leaked px |

Every "after the recommended patch" figure above was measured this session by
applying the patch to a scratch copy and re-running — **46/46 of the pipeline's
own tests still passed** on the patched copy. The patches are in
`PIPELINE_AUDIT.md` §2 and §5; they have **not** been applied to `6GEMSDOE`,
because nothing was written to any GEMSDOE repo this session.
