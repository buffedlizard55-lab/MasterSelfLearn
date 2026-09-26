#!/usr/bin/env python3
"""Follow-ups named in CANDIDATE_GEOLOGY.md §4–§6 (session-5 carry-forward 6).

Two measurements, both from the written-up set's own "confirm with" lines:

1. THE C-1 ↔ C-6 ↔ C-5 CHAIN TEST (§6 C-6, §3 C-5)
   C-6's confirmation line: "trend continuity over the full latitude span
   40.05–40.62°N" — if the three Humboldt candidates connect at trace
   resolution the system is one ~17 km (actually ~63 km latitude span)
   structure. Measured as:
     (i)   lateral offset of each segment from the neighbour's extended line
           (px, at 100 m/px) — "continuous" needs the offset inside a few
           pixels, i.e. the trends must actually meet;
     (ii)  intermediate-candidate scan: how many other `new_to_catalogue`
           components sit within 2 km of the connecting legs (steps in the
           chain vs an empty corridor);
     (iii) C-6's stated kill-if: is the connecting trend a gravity-gradient
           BROAD RAMP or a NARROW RIDGE? Along each leg, cross-sections of
           `grav_hgm_computed` (derived) and `iso_grav_anom_hg` (raw
           provider band) are scored for a central narrow peak
           (local max within +/-3 px of the leg, prominence >= 1 window MAD
           on the detrended profile). A chain of narrow ridges = discrete
           structure; mostly broad = basin-margin gradient (kill).

2. cond_surf CROSS-SECTIONS FOR id 872 (C-8) — and id 1618 (C-4), the same
   open question (§5 "still open")
   C-8's kill-if: "the conductivity high is the Granite Springs Valley fill
   itself". Measured as: perpendicular profile of `cond_surf` and
   `depth_to_base_surf` across the trace, reporting trace-vs-window contrast,
   the width of the elevated region around the trace (narrow linear conductor
   = structural fluid path; broad = basin fill), and peak offset from the
   trace.

Run:
  GEMS_SRC=/path/to/src python3 followup_chain_cond.py \
      --features data/training_features.tif \
      --candidates data/evidence/candidates.json

Needs: numpy, rasterio. Reads `grav_hgm_computed` from the DERIVED stack
(data/evidence/features.f32.npy + features_meta.json) when present, and
falls back to the raw provider band only for the cross-sections.
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
from e10_falsification import centerline_pixels, to_rowcol  # noqa: E402

CHAIN = [("C-6", 1991), ("C-1", 548), ("C-5", 240)]  # south -> north
COND_IDS = [("C-8", 872), ("C-4", 1618)]
CORRIDOR_M = 2000.0          # intermediate-candidate search half-width
LEG_SAMPLE_M = 2000.0         # cross-section spacing along each leg
CROSS_HALF_PX = 10            # cross-section half-width (1 km)
CENTRAL_PX = 3                # "narrow" = peak within 3 px of the leg
PROMINENCE_MAD = 1.0          # peak prominence threshold, in window MADs


def unit_dir(rows: np.ndarray, cols: np.ndarray) -> tuple[float, float]:
    dr, dc = float(rows[-1] - rows[0]), float(cols[-1] - cols[0])
    n = float(np.hypot(dr, dc))
    return (dr / n, dc / n)


def point_line_dist(pr, pc, r0, c0, dr, dc) -> float:
    """Perpendicular distance from (pr, pc) to the infinite line
    (r0,c0) + t*(dr,dc), in pixels."""
    v_r, v_c = pr - r0, pc - c0
    proj = v_r * dr + v_c * dc
    return float(np.hypot(v_r - proj * dr, v_c - proj * dc))


def leg_points(r0, c0, r1, c1, step_px: float):
    n = max(2, int(np.hypot(r1 - r0, c1 - c0) / step_px) + 1)
    t = np.linspace(0.0, 1.0, n)
    return r0 + t * (r1 - r0), c0 + t * (c1 - c0)


def narrow_peak(profile: np.ndarray) -> tuple[bool, float]:
    """Is there a central narrow peak? (bool, prominence in MAD units)."""
    p = profile.astype(float)
    m = np.isfinite(p)
    if m.sum() < 7:
        return False, float("nan")
    # detrend with a line fit over the section
    x = np.arange(len(p), dtype=float)
    coef = np.polyfit(x[m], p[m], 1)
    d = p - np.polyval(coef, x)
    d[~m] = np.nan
    c = len(d) // 2
    lo, hi = c - CENTRAL_PX, c + CENTRAL_PX + 1
    central = d[lo:hi]
    if not np.isfinite(central).any():
        return False, float("nan")
    mad = float(np.nanmedian(np.abs(d - np.nanmedian(d)))) or 1e-12
    peak = float(np.nanmax(central))
    rest = np.concatenate([d[:lo], d[hi:]])
    is_peak = bool(peak >= np.nanmax(rest)) and peak >= PROMINENCE_MAD * mad
    return is_peak, round(peak / mad, 3)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", default="data/training_features.tif")
    ap.add_argument("--candidates", default="data/evidence/candidates.json")
    ap.add_argument("--derived", default="data/evidence/features.f32.npy")
    ap.add_argument("--meta", default="data/evidence/features_meta.json")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    import rasterio
    cands = {c["id"]: c for c in json.load(open(args.candidates))["candidates"]}
    report: dict = {"chain": {}, "cond_cross_sections": {}}

    # ------------------------------------------------------------ geometry
    segs = {}
    for label, cid in CHAIN:
        c = cands[cid]
        rows, cols = centerline_pixels(c["utm_bbox"], c["azimuth_deg"],
                                       c["length_m"])
        segs[label] = (rows, cols)
        report["chain"].setdefault("segments", {})[label] = {
            "id": cid, "azimuth_deg": c["azimuth_deg"],
            "length_m": c["length_m"],
            "start_rowcol": [int(rows[0]), int(cols[0])],
            "end_rowcol": [int(rows[-1]), int(cols[-1])],
        }

    offsets = {}
    for (la, lb) in (("C-6", "C-1"), ("C-1", "C-5")):
        ra, ca = segs[la]
        rb, cb = segs[lb]
        # direction of A extended; distance of B's endpoints to A's line and
        # distance of A's nearest endpoint to B's line
        d_ar, d_ac = unit_dir(ra, ca)
        d_br, d_bc = unit_dir(rb, cb)
        dist_b_start_on_a = point_line_dist(rb[0], cb[0], ra[0], ca[0], d_ar, d_ac)
        dist_b_end_on_a = point_line_dist(rb[-1], cb[-1], ra[0], ca[0], d_ar, d_ac)
        dist_a_end_on_b = point_line_dist(ra[-1], ca[-1], rb[0], cb[0], d_br, d_bc)
        # along-strike gap between the facing endpoints (projected)
        facing_gap = float(np.hypot(ra[-1] - rb[0], ca[-1] - cb[0]))
        offsets[f"{la}->{lb}"] = {
            "facing_endpoint_gap_px": round(facing_gap, 1),
            "facing_endpoint_gap_m": round(facing_gap * spec.PIXEL_SIZE_M, 0),
            "B_on_A_line_min_offset_px": round(
                min(dist_b_start_on_a, dist_b_end_on_a), 2),
            "A_end_on_B_line_offset_px": round(dist_a_end_on_b, 2),
            "continuous_at_trace_resolution": bool(
                min(dist_b_start_on_a, dist_b_end_on_a, dist_a_end_on_b) <= 5.0),
        }
    report["chain"]["lateral_offsets"] = offsets

    # ------------------------------------------- intermediate candidates
    def dist_point_to_leg(px_r, px_c, r0, c0, r1, c1) -> float:
        dr, dc = r1 - r0, c1 - c0
        n2 = dr * dr + dc * dc
        if n2 == 0:
            return float(np.hypot(px_r - r0, px_c - c0))
        t = ((px_r - r0) * dr + (px_c - c0) * dc) / n2
        t = min(1.0, max(0.0, t))
        return float(np.hypot(px_r - (r0 + t * dr), px_c - (c0 + t * dc)))

    legs = {}
    for (la, lb) in (("C-6", "C-1"), ("C-1", "C-5")):
        ra, ca = segs[la]
        rb, cb = segs[lb]
        # leg between the centroids of the two candidates
        r0 = float(np.mean([ra[0], ra[-1]])); c0 = float(np.mean([ca[0], ca[-1]]))
        r1 = float(np.mean([rb[0], rb[-1]])); c1 = float(np.mean([cb[0], cb[-1]]))
        legs[f"{la}-{lb}"] = (r0, c0, r1, c1)
        hits = []
        for c in cands.values():
            if c["class"] != "new_to_catalogue":
                continue
            if c["id"] in (1991, 548, 240):
                continue
            minx, miny, maxx, maxy = c["utm_bbox"]
            mr, mc = to_rowcol((minx + maxx) / 2.0, (miny + maxy) / 2.0)
            d = dist_point_to_leg(mr, mc, r0, c0, r1, c1)
            if d * spec.PIXEL_SIZE_M <= CORRIDOR_M:
                hits.append({"id": c["id"],
                             "dist_to_leg_m": round(d * spec.PIXEL_SIZE_M, 0),
                             "azimuth_deg": c["azimuth_deg"]})
        hits.sort(key=lambda h: h["dist_to_leg_m"])
        legs[f"{la}-{lb}_intermediates"] = hits
    report["chain"]["intermediate_candidates_within_2km"] = {
        k: v for k, v in legs.items() if k.endswith("_intermediates")}
    leg_geoms = {k: v for k, v in legs.items() if not k.endswith("_intermediates")}

    # ------------------------------------ (iii) narrow-ridge vs broad-ramp
    with rasterio.open(args.features) as src:
        raw_hg = src.read(spec.BAND_INDEX["iso_grav_anom_hg"]).astype(np.float32)
        raw_hg[raw_hg < spec.FEATURE_INVALID_BELOW] = np.nan

        derived_idx = None
        mm = None
        if os.path.exists(args.derived) and os.path.exists(args.meta):
            channels = json.load(open(args.meta))["channels"]
            if "grav_hgm_computed" in channels:
                derived_idx = channels.index("grav_hgm_computed")
                mm = np.load(args.derived, mmap_mode="r")

        for leg_name, (r0, c0, r1, c1) in leg_geoms.items():
            pr, pc = leg_points(r0, c0, r1, c1, LEG_SAMPLE_M / spec.PIXEL_SIZE_M)
            dr, dc = unit_dir(np.array([r0, r1]), np.array([c0, c1]))
            # cross-section direction = perpendicular to the leg
            xr, xc = -dc, dr
            stats = {"n_sections": len(pr), "raw_iso_grav_anom_hg": {},
                     "derived_grav_hgm_computed": {}}
            for tag, getter in (
                    ("raw_iso_grav_anom_hg",
                     lambda R, C: raw_hg[int(R), int(C)]),
                    ("derived_grav_hgm_computed",
                     (lambda R, C: np.asarray(
                         mm[int(R), int(C), derived_idx], dtype=np.float64))
                     if mm is not None else None)):
                if getter is None:
                    continue
                n_flags, proms = 0, []
                for i in range(len(pr)):
                    ts = np.arange(-CROSS_HALF_PX, CROSS_HALF_PX + 1)
                    rr = np.clip(np.round(pr[i] + ts * xr).astype(int),
                                 0, spec.HEIGHT - 1)
                    cc = np.clip(np.round(pc[i] + ts * xc).astype(int),
                                 0, spec.WIDTH - 1)
                    prof = np.array([getter(rr[j], cc[j]) for j in range(len(ts))])
                    ok, prom = narrow_peak(prof)
                    n_flags += int(ok)
                    if np.isfinite(prom):
                        proms.append(prom)
                stats[tag] = {
                    "narrow_ridge_sections": n_flags,
                    "narrow_ridge_fraction": round(n_flags / max(1, len(pr)), 3),
                    "median_prominence_mad": (round(float(np.median(proms)), 3)
                                              if proms else None),
                    "verdict": ("narrow ridge — discrete structure along the leg"
                                if n_flags / max(1, len(pr)) >= 0.5 else
                                "broad/ramp-like — narrow-ridge fraction "
                                "below 0.5"),
                }
            report["chain"].setdefault("gravity_cross_sections", {})[leg_name] = stats

        # ------------------------------------------- cond cross-sections
        for label, cid in COND_IDS:
            c = cands[cid]
            rows, cols = centerline_pixels(c["utm_bbox"], c["azimuth_deg"],
                                           c["length_m"])
            minr, maxr = int(rows.min()), int(rows.max())
            minc, maxc = int(cols.min()), int(cols.max())
            r0 = max(0, minr - 25); r1 = min(spec.HEIGHT, maxr + 26)
            c0 = max(0, minc - 25); c1 = min(spec.WIDTH, maxc + 26)
            # cross-section through the bbox centre, perpendicular to azimuth
            cr, cc_ = (rows[0] + rows[-1]) // 2, (cols[0] + cols[-1]) // 2
            az = np.deg2rad(c["azimuth_deg"])
            # perpendicular in (row, col): azimuth from north, clockwise
            xr, xc = np.cos(az), -np.sin(az)  # right-hand perpendicular
            out = {}
            for band in ("cond_surf", "depth_to_base_surf"):
                a = src.read(spec.BAND_INDEX[band]).astype(np.float32)
                a[a < spec.FEATURE_INVALID_BELOW] = np.nan
                w = a[r0:r1, c0:c1]
                ts = np.arange(-25, 26)
                rr = np.clip(np.round(cr + ts * xr).astype(int) - r0, 0, r1 - r0 - 1)
                cc2 = np.clip(np.round(cc_ + ts * xc).astype(int) - c0, 0, c1 - c0 - 1)
                prof = w[rr, cc2]
                center = 25
                win_med = float(np.nanmedian(w))
                win_std = float(np.nanstd(w)) or np.nan
                trc = float(np.nanmean(prof[center - 3:center + 4]))
                # width of contiguous elevated run around the centre
                thr = win_med + 0.5 * win_std
                lo = center
                while lo > 0 and np.isfinite(prof[lo - 1]) and prof[lo - 1] >= thr:
                    lo -= 1
                hi = center
                while hi < len(prof) - 1 and np.isfinite(prof[hi + 1]) and prof[hi + 1] >= thr:
                    hi += 1
                pk = int(np.nanargmax(np.where(np.isfinite(prof), prof, -np.inf)))
                out[band] = {
                    "trace_mean": round(trc, 3),
                    "window_median": round(win_med, 3),
                    "trace_minus_window_std": round((trc - win_med) / win_std, 3)
                    if win_std == win_std else None,
                    "elevated_width_px": int(hi - lo + 1),
                    "elevated_width_m": int((hi - lo + 1) * spec.PIXEL_SIZE_M),
                    "peak_offset_from_trace_px": int(pk - center),
                    "profile": [None if not np.isfinite(v) else round(float(v), 3)
                                for v in prof],
                }
            cond = out["cond_surf"]
            ctz = cond["trace_minus_window_std"]
            if ctz is not None and ctz >= 1.0:
                shape = ("conductive high ON the trace — "
                         + ("narrow (structural)" if cond["elevated_width_px"] <= 7
                            else "broad (basin-fill-like)"))
            elif ctz is not None and ctz >= 0.5:
                shape = "marginal conductive high at the trace"
            else:
                shape = ("NO conductor at the trace in cond_surf — the "
                         "kill-if is NOT cleared (the cond evidence, if any, "
                         "is elsewhere or offset from the trace)")
            report["cond_cross_sections"][label] = {
                "id": cid, "azimuth_deg": c["azimuth_deg"],
                "verdict_shape": shape, **out,
            }
            print(f"{label} (id {cid}) cond_surf: trace {cond['trace_mean']} vs "
                  f"window {cond['window_median']} "
                  f"({ctz}σ), elevated width "
                  f"{cond['elevated_width_px']} px, peak offset "
                  f"{cond['peak_offset_from_trace_px']} px -> {shape}")

    for leg, s in report["chain"].get("gravity_cross_sections", {}).items():
        print(f"\n{leg}:")
        for band, v in s.items():
            if not isinstance(v, dict):
                continue
            print(f"  {band}: {v['narrow_ridge_fraction']} narrow sections "
                  f"(median prominence {v['median_prominence_mad']} MAD) "
                  f"-> {v['verdict']}")
    print("\nlateral offsets:")
    for k, v in offsets.items():
        print(f"  {k}: facing gap {v['facing_endpoint_gap_m']:.0f} m, "
              f"min line offset {v['B_on_A_line_min_offset_px']} px, "
              f"continuous={v['continuous_at_trace_resolution']}")
    for k, v in report["chain"]["intermediate_candidates_within_2km"].items():
        print(f"  intermediates on {k}: {len(v)} "
              f"{[h['id'] for h in v]}")

    if args.out:
        with open(args.out, "w") as f:
            json.dump(report, f, indent=2, default=float)
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
