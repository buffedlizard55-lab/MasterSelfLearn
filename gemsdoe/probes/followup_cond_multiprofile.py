#!/usr/bin/env python3
"""Cond follow-ups (session 6, carry-forward 5) — two measurements.

A. MULTI-PROFILE cond_surf CROSS-SECTIONS for C-8 (id 872), C-4 (id 1618),
   C-9 (id 4209)
   Session 5 measured ONE perpendicular profile through each trace's bbox
   centre and concluded "regional high, no trace-local conductor" (kill-if
   supported), with the stated caveat that one profile can miss a hooked or
   offset conductor. This probe removes the caveat: K=5 profiles, evenly
   spaced at 15/30/50/70/85 % along each trace, same +/-25 px half-width and
   detrending as session 5. The centre profile repeats session 5's
   measurement as a consistency check.

   Per-profile shape classes: local-max-at-trace (a local maximum within
   +/-3 px of the trace crossing), local-min-at-trace, monotone (the sign of
   the detrended end-to-end difference matches at least 90 % of the detrended
   profile's endpoint-vs-centre contrast), else flat/other.

   Pre-registered verdicts (before running):
     * "locally supported":  >= 3/5 profiles local-max-at-trace on cond_surf;
     * "kill-if supported (kill-if stands; regional)": <= 1/5 local-max AND the
       centre-profile trace-vs-window contrast |z| < 0.5;
     * otherwise "inconclusive".
   The three outcomes are exhaustive and the same rule applies to all three
   candidates; no per-candidate adjustments after the fact.

B. famrank_cond MEMBER ATTRIBUTION over every new_to_catalogue candidate
   `famrank_cond = max(rank(cond_surf), rank(depth_to_base_surf))` with NO
   inversion on either member (verified in scripts/build_features.py: only
   `deq_n100a15` is inverted, in the seis family). The members measure
   different physics (band descriptions from the official data dictionary in
   spec.py): cond_surf = "electrical conductivity of subsurface";
   depth_to_base_surf = "depth to basement surface - thickness of
   sedimentary cover". The max rule hides which member fired; a candidate
   whose famrank_cond is carried by SEDIMENT THICKNESS is being credited
   "conductivity evidence" for sitting in a deep basin.

   This arm recomputes both members' global percentile ranks from
   rank_tables.json (identical bin-rule/LUT to build_features.py) at every
   candidate's centreline pixels for ALL new_to_catalogue components, then
   reports: median member ranks per candidate, the firing member, the fire
   margin, and the count of candidates with famrank_cond >= 0.75 carried by
   depth_to_base_surf alone (cond_surf's own rank < 0.75). That count is the
   population the "drop the depth member / report two sub-signals" decision
   is about, and it is printed, not decided silently.

Run:
  GEMS_SRC=/path/to/src python3 followup_cond_multiprofile.py \
      --features data/training_features.tif \
      --candidates data/evidence/candidates.json \
      --rank-tables data/evidence/rank_tables.json --out cond6_results.json

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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gems import spec  # noqa: E402
from e10_falsification import centerline_pixels  # noqa: E402

COND_IDS = [("C-8", 872), ("C-4", 1618), ("C-9", 4209)]
PROFILE_FRACS = (0.15, 0.30, 0.50, 0.70, 0.85)
CROSS_HALF = 25
CENTRAL_PX = 3
FIRE_THR = 0.75   # "cond pillar" level used in the write-ups (top 25 %)


def read_band(src, name: str) -> np.ndarray:
    a = src.read(spec.BAND_INDEX[name]).astype(np.float32)
    a[a < spec.FEATURE_INVALID_BELOW] = np.nan
    return a


def detrend(p: np.ndarray) -> np.ndarray:
    x = np.arange(len(p), dtype=float)
    m = np.isfinite(p)
    if m.sum() < 7:
        return np.full_like(p, np.nan)
    coef = np.polyfit(x[m], p[m], 1)
    return p - np.polyval(coef, x)


def classify(prof: np.ndarray, center: int) -> str:
    """Shape class of the detrended profile at the trace crossing."""
    d = detrend(prof)
    m = np.isfinite(d)
    if m.sum() < 7:
        return "insufficient-data"
    lo, hi = center - CENTRAL_PX, center + CENTRAL_PX + 1
    central = d[lo:hi]
    if not np.isfinite(central).any():
        return "insufficient-data"
    cmax = float(np.nanmax(central))
    cmin = float(np.nanmin(central))
    rest = np.concatenate([d[:lo], d[hi:]])
    rest = rest[np.isfinite(rest)]
    if rest.size == 0:
        return "insufficient-data"
    mad = float(np.nanmedian(np.abs(d[np.isfinite(d)]
                                      - np.nanmedian(d[np.isfinite(d)])))) or 1e-12
    if cmax >= float(np.nanmax(rest)) and cmax >= 1.0 * mad:
        return "local-max-at-trace"
    if cmin <= float(np.nanmin(rest)) and cmin <= -1.0 * mad:
        return "local-min-at-trace"
    ends = 0.5 * (np.nanmean(d[:5]) + np.nanmean(d[-5:]))
    if np.isfinite(ends) and abs(ends) >= 1.5 * mad and abs(ends) > abs(cmax) and abs(ends) > abs(cmin):
        return "monotone"
    return "flat/other"


class RankTable:
    """Per-band global percentile rank, identical rule to build_features.py."""

    def __init__(self, path: str, nbins_expected: int = 65536):
        rt = json.load(open(path))
        self.nbins = int(rt["nbins"])
        self.luts: dict[str, np.ndarray] = {}
        self.ranges: dict[str, tuple[float, float]] = {}
        for name, t in rt["bands"].items():
            if t.get("degenerate") or not t.get("cdf") or t["total"] == 0:
                continue
            cdf = np.asarray(t["cdf"], dtype=np.float64)
            counts = np.diff(np.concatenate([[0.0], cdf]))
            self.luts[name] = ((cdf - 0.5 * counts) / t["total"]).astype(np.float32)
            self.ranges[name] = (float(t["vmin"]), float(t["vmax"]))

    def rank(self, name: str, arr: np.ndarray) -> np.ndarray:
        vmin, vmax = self.ranges[name]
        span = vmax - vmin
        if span <= 0:
            return np.full_like(arr, np.nan, dtype=np.float32)
        with np.errstate(all="ignore"):
            b = np.floor((arr - vmin) * self.nbins / span).astype(np.int64)
        b = np.clip(b, 0, self.nbins - 1)
        out = self.luts[name][b]
        out = np.where(np.isfinite(arr), out, np.nan)
        return out.astype(np.float32)


def profile_band(a: np.ndarray, cr: float, cc: float, xr: float, xc: float,
                 half: int = CROSS_HALF) -> np.ndarray:
    ts = np.arange(-half, half + 1)
    rr = np.clip(np.round(cr + ts * xr).astype(int), 0, a.shape[0] - 1)
    cc2 = np.clip(np.round(cc + ts * xc).astype(int), 0, a.shape[1] - 1)
    return a[rr, cc2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", default="data/training_features.tif")
    ap.add_argument("--candidates", default="data/evidence/candidates.json")
    ap.add_argument("--rank-tables", default="data/evidence/rank_tables.json")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    import rasterio
    cands = json.load(open(args.candidates))["candidates"]
    by_id = {c["id"]: c for c in cands}
    report: dict = {"multiprofile": {}, "member_attribution": {}}

    with rasterio.open(args.features) as src:
        cond = read_band(src, "cond_surf")
        d2b = read_band(src, "depth_to_base_surf")

        # ---------------- A. multi-profile cross-sections -----------------
        for label, cid in COND_IDS:
            c = by_id[cid]
            rows, cols = centerline_pixels(c["utm_bbox"], c["azimuth_deg"],
                                           c["length_m"])
            az = np.deg2rad(c["azimuth_deg"])
            xr, xc = np.cos(az), -np.sin(az)   # right-hand perpendicular
            n = len(rows)
            profs = []
            for frac in PROFILE_FRACS:
                i = min(n - 1, max(0, int(round(frac * (n - 1)))))
                p = profile_band(cond, rows[i], cols[i], xr, xc)
                w = cond[max(0, rows[i] - 25):rows[i] + 26,
                         max(0, cols[i] - 25):cols[i] + 26]
                d = detrend(p)
                fin = np.isfinite(d)
                z = None
                if fin.sum() >= 7:
                    mad = float(np.nanmedian(np.abs(d[fin] - np.nanmedian(d[fin])))) or 1e-12
                    trc = float(np.nanmean(d[CROSS_HALF - 3:CROSS_HALF + 4]))
                    # trace-vs-window contrast on the DETRENDED profile, in
                    # MAD units (session 5 used window-std of raw)
                    z = round(trc / (1.4826 * mad), 3)
                    raw_trc = float(np.nanmean(p[CROSS_HALF - 3:CROSS_HALF + 4]))
                    wstd = float(np.nanstd(w)) or np.nan
                    z_raw = round((raw_trc - float(np.nanmedian(w))) / wstd, 3) \
                        if wstd == wstd else None
                else:
                    z_raw = None
                profs.append({
                    "frac": frac,
                    "at_rowcol": [int(rows[i]), int(cols[i])],
                    "shape": classify(p, CROSS_HALF),
                    "contrast_mad_z": z,
                    "contrast_window_z": z_raw,
                    "peak_offset_px": int(
                        np.nanargmax(np.where(np.isfinite(p), p, -np.inf))
                        - CROSS_HALF) if np.isfinite(p).any() else None,
                })
            n_max = sum(1 for p in profs if p["shape"] == "local-max-at-trace")
            centre = profs[len(profs) // 2]
            centre_z = centre["contrast_window_z"]
            # pre-registered verdict rule (see module docstring)
            if n_max >= 3:
                verdict = "locally supported"
            elif n_max <= 1 and (centre_z is None or abs(centre_z) < 0.5):
                verdict = "kill-if stands (regional; no trace-local conductor)"
            else:
                verdict = "inconclusive"
            report["multiprofile"][label] = {
                "id": cid, "azimuth_deg": c["azimuth_deg"],
                "n_profiles": len(profs),
                "local_max_at_trace": n_max,
                "centre_profile": centre,
                "profiles": profs, "verdict": verdict,
            }
            shapes = [p["shape"].split("-at-trace")[0] for p in profs]
            print(f"{label} (id {cid}): {n_max}/5 local-max {shapes}; "
                  f"centre z(win)={centre_z} -> {verdict}")

        # ---------------- B. famrank_cond member attribution --------------
        rt = RankTable(args.rank_tables)
        r_cond = rt.rank("cond_surf", cond)
        r_d2b = rt.rank("depth_to_base_surf", d2b)
        rows_rr, cols_cc = np.where(np.isfinite(r_cond) & np.isfinite(r_d2b))

        stats = {"n_new_to_catalogue": 0, "famrank_ge_075": 0,
                 "carried_by_d2b_alone_ge_075": 0, "candidates": []}
        n_depth_fired = 0
        for c in cands:
            if c["class"] != "new_to_catalogue":
                continue
            stats["n_new_to_catalogue"] += 1
            rows, cols = centerline_pixels(c["utm_bbox"], c["azimuth_deg"],
                                           c["length_m"])
            rc = r_cond[rows, cols]
            rd = r_d2b[rows, cols]
            m = np.isfinite(rc) & np.isfinite(rd)
            if m.sum() < 3:
                continue
            mc, md = float(np.nanmedian(rc[m])), float(np.nanmedian(rd[m]))
            fam = max(mc, md)
            fired = "depth_to_base_surf" if md > mc else \
                    ("cond_surf" if mc > md else "tie")
            n_depth_fired += int(fired == "depth_to_base_surf")
            if fam >= FIRE_THR:
                stats["famrank_ge_075"] += 1
                if fired == "depth_to_base_surf" and mc < FIRE_THR:
                    stats["carried_by_d2b_alone_ge_075"] += 1
            stats["candidates"].append({
                "id": c["id"], "median_rank_cond_surf": round(mc, 3),
                "median_rank_depth_to_base": round(md, 3),
                "famrank_cond_median": round(fam, 3), "firing_member": fired,
                "fire_margin": round(abs(mc - md), 3),
            })
        stats["n_depth_fired_of_rankable"] = n_depth_fired
        stats["note"] = ("famrank >= 0.75 while cond_surf itself < 0.75: the "
                         "pillar is sediment-thickness evidence, not "
                         "subsurface-conductivity evidence, under the band "
                         "descriptions in spec.py")
        report["member_attribution"] = stats
        stats["candidates"].sort(key=lambda r: -r["famrank_cond_median"])
        print(f"\nmember attribution over {stats['n_new_to_catalogue']} "
              f"new_to_catalogue candidates:")
        print(f"  famrank_cond >= 0.75: {stats['famrank_ge_075']}")
        print(f"  of those carried by depth_to_base alone: "
              f"{stats['carried_by_d2b_alone_ge_075']}")
        print(f"  median firing member by candidate: "
              f"{sum(1 for r in stats['candidates'] if r['firing_member'] == 'cond_surf')} cond_surf, "
              f"{sum(1 for r in stats['candidates'] if r['firing_member'] == 'depth_to_base_surf')} depth_to_base, "
              f"{sum(1 for r in stats['candidates'] if r['firing_member'] == 'tie')} tie")
        for r in stats["candidates"][:6]:
            print(f"    id {r['id']:5d}: fam {r['famrank_cond_median']} "
                  f"= max(cond {r['median_rank_cond_surf']}, "
                  f"d2b {r['median_rank_depth_to_base']}) -> {r['firing_member']}")

    if args.out:
        with open(args.out, "w") as f:
            json.dump(report, f, indent=2, default=float)
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
