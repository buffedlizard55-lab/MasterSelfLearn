#!/usr/bin/env python3
"""D-5 — does `second_derivatives`' NaN halo cover the mixed-derivative stencil?

`features.second_derivatives` computes s = d2/dxdy from the FOUR DIAGONAL
neighbours of each output pixel. Its NaN halo was a 4-connected (L1 diamond)
radius-1 dilation, which covers the orthogonal neighbours used by r = d2/dx2
and t = d2/dy2 but NOT the diagonals used by s. A single NaN one diagonal step
away therefore contaminates s (and everything built from it: curv_gaussian,
profile/plan curvature mixes) while the output pixel stays finite.

Measured exactly like probe_feature_guard: inject one NaN, find every output
pixel that changed, and count those that stayed finite (the leak).

Run:  GEMS_SRC=/path/to/6GEMSDOE/src python3 probe_crossder_halo.py
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

N = 41
C = N // 2


def leak_count(clean_s: np.ndarray, out_s: np.ndarray) -> list[tuple[int, int]]:
    diff = ~np.isclose(np.nan_to_num(clean_s, nan=-9e9),
                       np.nan_to_num(out_s, nan=-9e9))
    ys, xs = np.nonzero(diff)
    leaked = []
    for a, b in zip((ys - C).tolist(), (xs - C).tolist()):
        if np.isfinite(out_s[C + a, C + b]):
            leaked.append((a, b))
    return leaked


def main() -> int:
    rng = np.random.default_rng(1)
    base = rng.normal(size=(N, N)).astype(np.float32)
    clean = features.second_derivatives(base)[2]  # s = d2/dxdy

    worst = 0
    for pos, label in (((C, C), "centre (orthogonal+diagonal taps)"),
                       ((C + 1, C + 1), "one diagonal step away")):
        holed = base.copy()
        holed[pos] = np.nan
        out = features.second_derivatives(holed)[2]
        leaked = leak_count(clean, out)
        worst = max(worst, len(leaked))
        print(f"NaN at {pos} relative to output — {label}")
        print(f"   s-pixels changed by the single NaN and STILL FINITE: "
              f"{len(leaked)}")
        if leaked:
            print(f"   leaked offsets e.g. {leaked[:6]}")
        print()

    print("correct guard: 8-connected (structure=np.ones((3,3))) radius-1 "
          "dilation — covers the diagonal taps of s.")
    return 1 if worst else 0


if __name__ == "__main__":
    raise SystemExit(main())
