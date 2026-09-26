#!/usr/bin/env python3
"""D-2 — does the blocked-CV buffer cover the metric's kernel support?

The scoring kernel is a Euclidean DISK of radius R = 300 m = 3.0 px on the
official 100 m grid (`gems.metric.kernel_offsets`). `gems.cv._dilate` dilates
with 4-connectivity, i.e. an L1 DIAMOND. A diamond of radius 3 does not contain
a disk of radius 3, so some in-kernel offsets are not held out of training.

Run:  GEMS_SRC=/path/to/6GEMSDOE/src python3 probe_cv_buffer.py
Needs: numpy, scipy.
"""
from __future__ import annotations

import os
import sys

import numpy as np
from scipy import ndimage

SRC = os.environ.get("GEMS_SRC", "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from gems import cv, metric  # noqa: E402


def main() -> int:
    dy, dx, k = metric.kernel_offsets()
    print(f"metric kernel: {len(dy)} integer offsets with d <= {metric.RADIUS_PX} px")

    # a single held-out pixel, buffered exactly the way cv.py does it
    single = np.zeros((61, 61), dtype=bool)
    single[30, 30] = True
    buf = cv._dilate(single, 3)

    missed = []
    for a, b, kk in zip(dy, dx, k):
        if kk <= 0.0:
            continue
        if not bool(buf[30 + a, 30 + b]):
            missed.append((int(a), int(b), float(np.hypot(a, b)), float(kk)))

    print(f"\nkernel offsets (k>0) NOT excluded by cv._dilate(mask, 3): {len(missed)}")
    for a, b, d, kk in missed:
        print(f"   offset (dy,dx)=({a:+d},{b:+d})  d={d:.4f} px  k={kk:.4f}")

    # what that costs on real fold geometry: scored pixels reachable by a
    # training pixel at k>0, i.e. folds that are not independent under the metric
    print("\nfold-geometry leakage: scored pixels with a TRAINING pixel inside R")
    shape = (373, 329)  # 1/10 scale of the official 3730x3292 grid
    for nb, nf in ((4, 4), (5, 5), (6, 4), (8, 4), (3, 3), (4, 2)):
        folds = cv.make_folds(n_blocks=nb, n_folds=nf, buffer_px=3)
        scored = leaky = 0
        for k_ in range(nf):
            train, score = folds.train_test_masks(shape, k_)
            d = ndimage.distance_transform_edt(~train, sampling=1.0)
            leaky += int((score & (d <= metric.RADIUS_PX + 1e-9)).sum())
            scored += int(score.sum())
        _, sc0 = folds.train_test_masks(shape, 0)
        ncomp = int(ndimage.label(sc0)[1])
        print(f"  n_blocks={nb} n_folds={nf}: {leaky}/{scored} = "
              f"{100.0*leaky/scored:.3f}%   fold-0 connected components = {ncomp}")

    f4 = cv.make_folds(4, 4, 3)
    print(f"\n  make_folds(4,4,3).fold_of_block =\n{f4.fold_of_block}")
    print("  -> with n_blocks == n_folds the fold id is the block COLUMN index, so")
    print("     each fold is one contiguous full-height stripe. That is why the")
    print("     missing diagonal offsets never straddle a train/score boundary in")
    print("     the default layout - the gap is latent, not absent.")
    return 1 if missed else 0


if __name__ == "__main__":
    raise SystemExit(main())
