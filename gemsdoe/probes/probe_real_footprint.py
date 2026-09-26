#!/usr/bin/env python3
"""D-1 on official bytes, and D-2 across fold layouts.

(a) scales the nan_gaussian guard gap from a synthetic raster to the REAL
    scored footprint, read from the sha256-verified official sample submission.
(b) sweeps fold layouts to show whether the CV buffer gap is latent or live.

Run:
  GEMS_SRC=/path/to/6GEMSDOE/src \
  GEMS_TEMPLATE=/path/to/6GEMSDOE/data/sample_submission.tif \
      python3 probe_real_footprint.py
Needs: numpy, scipy, rasterio.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import rasterio
from scipy import ndimage

SRC = os.environ.get("GEMS_SRC", "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from gems import cv, metric, raster, spec  # noqa: E402

SQ8 = np.ones((3, 3), dtype=bool)


def fold_layouts() -> None:
    print("=" * 72)
    print("(a) fold-layout leakage: scored pixels with a TRAINING pixel inside R")
    print("=" * 72)
    shape = (373, 329)
    for nb, nf in ((4, 4), (5, 5), (6, 4), (8, 4), (3, 3), (4, 2)):
        folds = cv.make_folds(n_blocks=nb, n_folds=nf, buffer_px=3)
        scored = leaky = 0
        for k in range(nf):
            train, score = folds.train_test_masks(shape, k)
            d = ndimage.distance_transform_edt(~train, sampling=1.0)
            leaky += int((score & (d <= metric.RADIUS_PX + 1e-9)).sum())
            scored += int(score.sum())
        _, sc0 = folds.train_test_masks(shape, 0)
        print(f"  n_blocks={nb} n_folds={nf}: {leaky}/{scored} = "
              f"{100.0*leaky/scored:.3f}%   fold-0 components = "
              f"{int(ndimage.label(sc0)[1])}")


def footprint(template: str) -> None:
    print()
    print("=" * 72)
    print("(b) real official footprint: pixels inside the nan_gaussian guard gap")
    print("=" * 72)
    got = raster.sha256_file(template)
    pin = spec.PINS["sample_submission.tif"]["sha256"]
    if got != pin:
        raise SystemExit(f"template sha256 mismatch: {got} != {pin} — refusing")
    print(f"  template sha256 verified: {got[:16]}...")

    with rasterio.open(template) as src:
        arr = src.read(1)
    finite = np.isfinite(arr)
    print(f"  grid {arr.shape}  finite (footprint) = {int(finite.sum()):,}  "
          f"(spec pins {spec.FOOTPRINT_PIXELS:,})")
    if int(finite.sum()) != spec.FOOTPRINT_PIXELS:
        print("  !! footprint count disagrees with spec.FOOTPRINT_PIXELS")

    for sigma in (1.5, 3.0):
        r_guard = int(np.ceil(3 * sigma))       # what the code uses (L1 diamond)
        r_true = int(4.0 * sigma + 0.5)         # scipy's actual square reach
        zone_code = ndimage.binary_dilation(~finite, iterations=r_guard)
        zone_true = ndimage.binary_dilation(~finite, structure=SQ8, iterations=r_true)
        under = int((finite & zone_true & ~zone_code).sum())
        zone_sq = ndimage.binary_dilation(~finite, structure=SQ8, iterations=r_guard)
        lower = int((finite & zone_true & ~zone_sq).sum())
        print(f"  sigma={sigma}: guard r={r_guard} (L1, as coded) vs stencil r={r_true} (square)")
        print(f"     unguarded footprint pixels: {under:,} "
              f"({100.0*under/finite.sum():.2f}%)   [radius-only lower bound: {lower:,}]")
    print(f"\n  the features' all-19-band valid footprint is smaller still "
          f"({spec.FEATURES_ALL_BAND_VALID_PIXELS:,} px), so the true boundary "
          f"band is larger than these figures.")
    print(f"  for scale: the whole label set is {spec.LABEL_POSITIVE_PIXELS:,} px.")


def main() -> int:
    template = os.environ.get("GEMS_TEMPLATE", "data/sample_submission.tif")
    fold_layouts()
    if not os.path.exists(template):
        print(f"\nskipping (b): no template at {template!r} — set GEMS_TEMPLATE")
        return 0
    footprint(template)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
