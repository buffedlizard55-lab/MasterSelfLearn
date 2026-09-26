#!/usr/bin/env python3
"""D-1 — does features.nan_gaussian's NaN guard cover the filter's stencil?

`gems.features._guarded_filter` re-invalidates an L1 DIAMOND of radius
`ceil(3*sigma)` around every NaN. `scipy.ndimage.gaussian_filter` has a SQUARE
support of radius `int(truncate*sigma + 0.5)`, truncate defaulting to 4.0.
Two mismatches: wrong shape, and too small.

This measures it directly: inject one NaN, then find every output pixel whose
value changed. Any such pixel that stays finite was not invalidated.

Run:  GEMS_SRC=/path/to/6GEMSDOE/src python3 probe_feature_guard.py
Needs: numpy, scipy.
"""
from __future__ import annotations

import os
import sys

import numpy as np

SRC = os.environ.get("GEMS_SRC", "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from gems import features  # noqa: E402

N = 81
C = N // 2


def main() -> int:
    rng = np.random.default_rng(0)
    worst_any = 0
    for sigma in (1.5, 3.0):
        base = rng.normal(size=(N, N)).astype(np.float32)
        clean = features.nan_gaussian(base, sigma)

        holed = base.copy()
        holed[C, C] = np.nan
        out = features.nan_gaussian(holed, sigma)

        r_guard = int(np.ceil(3 * sigma))          # what the code uses
        r_true = int(4.0 * sigma + 0.5)            # what scipy actually uses
        diff = ~np.isclose(np.nan_to_num(clean, nan=-9e9),
                           np.nan_to_num(out, nan=-9e9))
        ys, xs = np.nonzero(diff)
        affected = set(zip((ys - C).tolist(), (xs - C).tolist()))
        leaked = [(a, b) for a, b in affected
                  if (abs(a) + abs(b)) > r_guard and np.isfinite(out[C + a, C + b])]
        worst_any = max(worst_any, len(leaked))

        print(f"sigma={sigma}: guard r=ceil(3*sigma)={r_guard} (L1 diamond); "
              f"scipy stencil r=int(4*sigma+0.5)={r_true} (square)")
        print(f"   pixels affected by the single NaN: {len(affected)}")
        print(f"   affected but NOT invalidated (still finite): {len(leaked)}")
        if leaked:
            worst = max(leaked, key=lambda t: abs(t[0]) + abs(t[1]))
            print(f"   worst-case missed offset: (dy,dx)={worst} "
                  f"(L1={abs(worst[0])+abs(worst[1])} > {r_guard})")
        print()

    print("recommended guard: Chebyshev (8-connected) dilation of radius "
          "int(truncate*sigma+0.5) - the filter's own reach.")
    return 1 if worst_any else 0


if __name__ == "__main__":
    raise SystemExit(main())
