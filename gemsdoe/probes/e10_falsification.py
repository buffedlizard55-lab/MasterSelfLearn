#!/usr/bin/env python3
"""E10 — falsification tests on raw band values along flagged candidate traces.

Session-4 implementation of `gemsdoe/CANDIDATE_GEOLOGY.md` §4 follow-up 3. For
each written-up `new_to_catalogue` candidate, three artefact risks are tested
directly on the official raw bands (NOT on `famrank`, which is magnitude-ranked
and cannot answer any of these):

  (a) N-S aeromagnetic flight-line striping in `tmi_hg`
      — threatens C-2 and every near-N-S candidate. A flight-line artefact is a
      narrowband EAST-WEST periodicity (N-S stripes) that the trace simply
      follows. Measured as: dominant period + power share of the column-mean
      `tmi_hg` profile in a window around the trace (linear trend removed),
      with the row-mean profile as the control direction.

  (b) smoothed regional gradient inherited by `geod_shearrate`
      — threatens C-7 (the 0.97 strain rank). If a plane fitted to the strain
      band in the window explains the field (high R^2) and the trace sits on
      that plane (small residual), the rank is inherited from a broad regional
      gradient, not earned by the trace. Also measured on `geod_dilaterate`.

  (c) gravity SIGN at the trace: basement high vs basin fill
      — threatens C-1/C-5 (famrank grav 1.00/0.99). `famrank` ranks |anomaly|
      magnitude; the sign distinguishes a dense uplift (real structure) from a
      basin-fill low (sediment thickness). Read `iso_grav_anom` along the trace
      against the window, with `det_elev` and `depth_to_base_surf` as context.

Trace geometry: `candidates.json` stores each component's UTM bounding box and
azimuth but not its pixel list, so the trace is taken as the bbox-centerline
segment of length `length_m` along `azimuth_deg`. This is an APPROXIMATION,
stated as such: it is exact for a straight trace through the bbox (these all
are, by construction of the azimuth), but a hooked trace would be sampled on
its principal axis only.

Run:
  GEMS_SRC=/path/to/src python3 e10_falsification.py \
      --features data/training_features.tif \
      --candidates data/evidence/candidates.json

Needs: numpy, rasterio.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

SRC = os.environ.get("GEMS_SRC", "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from gems import spec  # noqa: E402

# the six written-up candidates (CANDIDATE_GEOLOGY.md §3), by candidates.json id
SIX = {
    548: "C-1", 3552: "C-2", 622: "C-3",
    1618: "C-4", 240: "C-5", 4383: "C-7",
}
WINDOW_PX = 25          # analysis window half-width, pixels (2.5 km)
STRIPING_MIN_SHARE = 0.25   # power-share flag threshold for (a)
PLANE_R2_FLAG = 0.85        # inheritance flag threshold for (b)


def to_rowcol(x: float, y: float) -> tuple[float, float]:
    col = (x - spec.ORIGIN_X) / spec.PIXEL_SIZE_M
    row = (spec.ORIGIN_Y - y) / spec.PIXEL_SIZE_M   # ORIGIN_Y is the TOP edge
    return row, col


def centerline_pixels(bbox, azimuth_deg: float, length_m: float):
    minx, miny, maxx, maxy = bbox
    cx, cy = (minx + maxx) / 2.0, (miny + maxy) / 2.0
    az = np.deg2rad(azimuth_deg)
    ux, uy = np.sin(az), np.cos(az)   # azimuth from north, clockwise
    half = length_m / 2.0 / spec.PIXEL_SIZE_M   # in pixels
    pts = []
    n = max(3, int(2 * half) + 1)
    for t in np.linspace(-half, half, n):
        pts.append(to_rowcol(cx + ux * t * spec.PIXEL_SIZE_M,
                             cy + uy * t * spec.PIXEL_SIZE_M))
    rc = np.array(pts)
    rows = np.clip(np.round(rc[:, 0]).astype(int), 0, spec.HEIGHT - 1)
    cols = np.clip(np.round(rc[:, 1]).astype(int), 0, spec.WIDTH - 1)
    return rows, cols


def fit_plane(window: np.ndarray) -> tuple[float, float]:
    """Least-squares z = a + b*col + c*row over finite pixels. Returns (R2, rms)."""
    h, w = window.shape
    rr, cc = np.mgrid[0:h, 0:w]
    m = np.isfinite(window)
    if m.sum() < 30:
        return float("nan"), float("nan")
    A = np.stack([np.ones(int(m.sum())), cc[m].astype(float), rr[m].astype(float)], axis=1)
    z = window[m].astype(float)
    coef, *_ = np.linalg.lstsq(A, z, rcond=None)
    pred = A @ coef
    ss_res = float(((z - pred) ** 2).sum())
    ss_tot = float(((z - z.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return r2, float(np.sqrt(ss_res / len(z)))


def periodicity(profile: np.ndarray) -> dict:
    """Dominant period (px) and its power share of a detrended 1-D profile."""
    y = profile.astype(float)
    m = np.isfinite(y)
    if m.sum() < 12:
        return {"period_px": None, "power_share": None, "n": int(m.sum())}
    x = np.arange(len(y), dtype=float)
    coef = np.polyfit(x[m], y[m], 1)
    y = y - np.polyval(coef, x)
    y[~m] = 0.0
    y = y - y.mean()
    if not np.any(y):
        return {"period_px": None, "power_share": 0.0, "n": int(m.sum())}
    spec_ = np.abs(np.fft.rfft(y)) ** 2
    spec_[0] = 0.0
    # ignore periods longer than the window itself
    freqs = np.fft.rfftfreq(len(y))
    valid = freqs > 1.0 / len(y)
    if not valid.any():
        return {"period_px": None, "power_share": 0.0, "n": int(m.sum())}
    i = int(np.argmax(np.where(valid, spec_, 0.0)))
    share = float(spec_[i] / spec_[valid].sum()) if spec_[valid].sum() > 0 else 0.0
    period = float(1.0 / freqs[i]) if freqs[i] > 0 else None
    return {"period_px": period, "power_share": share, "n": int(m.sum())}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", default="data/training_features.tif")
    ap.add_argument("--candidates", default="data/evidence/candidates.json")
    ap.add_argument("--out", default="")
    ap.add_argument("--ids", default="",
                    help="comma list of candidates.json ids to test "
                         "(default: the SIX written-up candidates)")
    args = ap.parse_args()

    import rasterio
    cands = {c["id"]: c for c in json.load(open(args.candidates))["candidates"]}
    if args.ids:
        ids = {int(x): f"id{x}" for x in args.ids.split(",") if x.strip()}
    else:
        ids = SIX
    report = {}

    with rasterio.open(args.features) as src:
        def read_band(name, rows, cols):
            a = src.read(spec.BAND_INDEX[name]).astype(np.float32)
            a[a < spec.FEATURE_INVALID_BELOW] = np.nan
            return a[rows, cols]

        for cid, label in ids.items():
            c = cands.get(cid)
            if c is None:
                print(f"{label}: id {cid} MISSING from candidates.json", file=sys.stderr)
                continue
            rows, cols = centerline_pixels(c["utm_bbox"], c["azimuth_deg"],
                                           c["length_m"])
            minr, maxr = int(rows.min()), int(rows.max())
            minc, maxc = int(cols.min()), int(cols.max())
            r0, r1 = max(0, minr - WINDOW_PX), min(spec.HEIGHT, maxr + WINDOW_PX + 1)
            c0, c1 = max(0, minc - WINDOW_PX), min(spec.WIDTH, maxc + WINDOW_PX + 1)

            full_tmi_hg = src.read(spec.BAND_INDEX["tmi_hg"]).astype(np.float32)
            full_tmi_hg[full_tmi_hg < spec.FEATURE_INVALID_BELOW] = np.nan
            win = full_tmi_hg[r0:r1, c0:c1]

            rec: dict = {"candidates_json_id": cid, "azimuth_deg": c["azimuth_deg"],
                         "length_m": c["length_m"], "dist_to_catalogue_m":
                             c["dist_to_catalogue_m"],
                         "trace_px": int(len(rows))}

            # ---- (a) flight-line striping in tmi_hg ------------------------
            col_prof = np.nanmean(win, axis=0)   # varies along E-W if N-S stripes
            row_prof = np.nanmean(win, axis=1)
            ew = periodicity(col_prof)   # stripe periodicity shows up HERE
            ns = periodicity(row_prof)   # control direction
            near_ns = min(abs(c["azimuth_deg"] % 180.0),
                          180.0 - abs(c["azimuth_deg"] % 180.0)) <= 15.0
            stripe_flag = bool(near_ns and ew["power_share"] is not None
                               and ew["power_share"] >= STRIPING_MIN_SHARE
                               and ew["period_px"] and ew["period_px"] <= win.shape[1] / 2)
            rec["striping"] = {
                "near_n_s": bool(near_ns),
                "e_w_profile": ew, "n_s_profile": ns,
                "verdict": ("FLAG — narrowband E-W periodicity under a N-S trace"
                            if stripe_flag else
                            "clear — no dominant stripe periodicity"),
            }

            # ---- (b) strain-band gradient inheritance ----------------------
            gb = {}
            for name in ("geod_shearrate", "geod_dilaterate"):
                gwin = src.read(spec.BAND_INDEX[name]).astype(np.float32)
                gwin[gwin < spec.FEATURE_INVALID_BELOW] = np.nan
                gwin = gwin[r0:r1, c0:c1]
                r2, rms = fit_plane(gwin)
                vals = read_band(name, rows, cols)
                wstd = float(np.nanstd(gwin))
                resid = float(np.nanmean(vals)) - float(np.nanmean(gwin))
                inherited = bool(np.isfinite(r2) and r2 >= PLANE_R2_FLAG
                                 and wstd > 0 and abs(resid) < 0.25 * wstd)
                gb[name] = {
                    "plane_r2": round(float(r2), 4), "plane_rms": round(rms, 5),
                    "window_std": round(wstd, 5),
                    "trace_mean": round(float(np.nanmean(vals)), 5),
                    "window_mean": round(float(np.nanmean(gwin)), 5),
                    "trace_minus_window_std": round(resid / wstd, 3) if wstd > 0 else None,
                    "inherited_from_regional_gradient": inherited,
                }
            rec["strain_inheritance"] = gb
            rec["strain_verdict"] = (
                "FLAG — trace sits on the smoothed regional field"
                if any(v["inherited_from_regional_gradient"] for v in gb.values())
                else "clear — trace departs from the fitted regional plane")

            # ---- (c) gravity sign ------------------------------------------
            ctx = {}
            for name, invert_context in (("iso_grav_anom", False),
                                         ("det_elev", False),
                                         ("depth_to_base_surf", False)):
                w = src.read(spec.BAND_INDEX[name]).astype(np.float32)
                w[w < spec.FEATURE_INVALID_BELOW] = np.nan
                w = w[r0:r1, c0:c1]
                vals = read_band(name, rows, cols)
                wmed = float(np.nanmedian(w))
                wstd = float(np.nanstd(w))
                tmean = float(np.nanmean(vals))
                ctx[name] = {
                    "trace_mean": round(tmean, 3),
                    "window_median": round(wmed, 3),
                    "trace_minus_window_std": round((tmean - wmed) / wstd, 3)
                    if wstd > 0 else None,
                }
            gz = ctx["iso_grav_anom"]["trace_minus_window_std"]
            sign = ("basement/density HIGH side" if (gz is not None and gz > 0.5)
                    else "basin-fill/low side" if (gz is not None and gz < -0.5)
                    else "no strong local contrast")
            rec["gravity_sign"] = ctx
            rec["gravity_verdict"] = sign

            report[label] = rec

            # ---- print -----------------------------------------------------
            print(f"\n=== {label} (id {cid}) · az {c['azimuth_deg']}° · "
                  f"{c['length_m']:.0f} m · {rec['trace_px']} px sampled ===")
            s = rec["striping"]
            print(f"  (a) striping: near-N/S={s['near_n_s']}  "
                  f"E-W period={s['e_w_profile']['period_px']} px "
                  f"share={s['e_w_profile']['power_share']}  "
                  f"[control N-S share={s['n_s_profile']['power_share']}]")
            print(f"  -> {s['verdict']}")
            for name, v in gb.items():
                print(f"  (b) {name}: plane R²={v['plane_r2']}  "
                      f"trace−window={v['trace_minus_window_std']}σ  "
                      f"inherited={v['inherited_from_regional_gradient']}")
            print(f"      -> {rec['strain_verdict']}")
            print(f"  (c) gravity: trace−window={gz}σ  -> {sign}")
            for name, v in ctx.items():
                print(f"      {name}: trace {v['trace_mean']} vs window "
                      f"{v['window_median']} ({v['trace_minus_window_std']}σ)")

    if args.out:
        with open(args.out, "w") as f:
            json.dump(report, f, indent=2, default=float)
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
