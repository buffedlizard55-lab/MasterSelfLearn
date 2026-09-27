#!/usr/bin/env python3
"""E14 — crest-ALIGNMENT test for the striping question (session 6).

Why this probe exists. E10's test (a) asked whether narrowband E–W
periodicity is *present* under a near-N–S trace; E12 showed its threshold has
no baseline contrast (defect D-9) and that no global levelling subtraction
removes the statistic. What was never tested is the question that actually
matters for artefact suspicion: does the trace SIT ON a stripe crest?

This probe implements the alignment test proposed in CANDIDATE_GEOLOGY.md
§7.3, now with the flight geometry SOURCED rather than assumed (session 6,
USGS Science Data Catalog entry for the GeoDAWN data release, DOI
10.5066/P93LGLVQ, fetched this session — see FIELD_AND_METRIC.md/RESEARCH_LIBRARY
for the quote):

  * GeoDAWN flight lines: azimuth 90deg (E-W), spaced 200 m (Area 1 /
    Clayton Valley block) / 400 m (Area 2, the geothermal block that covers
    the study area) -> at 100 m sampling the flight-line stripe direction is
    E-W with a 2-4 px N-S period.
  * Tie lines: azimuth 180deg (N-S), spaced 2000 m / 4000 m -> the N-S stripe
    direction has a 20-40 px E-W period.
  * The contractor already applied tie-line leveling AND micro-leveling
    (quoted on the same page), so any residual is a *residual* artefact, not
    an unprocessed one.

Consequence: a near-N-S candidate trace is artefact-consistent only if it is
locked to a TIE-SCALE N-S stripe; the "classic flight-line direction = N-S"
prior in CANDIDATE_GEOLOGY.md does not hold for GeoDAWN (flight lines are
E-W), and this probe tests the geometry that is actually sourced.

Test design (pre-registered before running)
-------------------------------------------
Windows are +/-45 px (4.5 km) per side — wider than E10/E12's +/-25 px,
deliberately: the instrument needs >= 2 cycles of the LONGEST tie period
(45 px) inside every window, and the shortest written-up trace (12 px)
leaves a 62 px window at +/-25 px, which cannot hold two 45 px cycles.
The window change is stated, not hidden; E14's statistics are not
comparable to E10's shares, only to its own nulls.

For each written-up candidate window:

  (TIE) tie-scale N-S stripe test, primary band `tmi_hg`:
    1. Mask the trace's own pixels (Chebyshev +/-1) out of the window and
       take the column-mean profile of what is left (linear interpolation
       across the masked columns). The trace therefore cannot create its
       own crest.
    2. FFT band-pass the profile to 12-45 px period (covers both sourced tie
       spacings with margin, and E10's 10-18 px window observations).
    3. Crests = local maxima of the band-passed profile, >= 12 px apart.
    4. A_x = share of the trace's per-row x-positions whose nearest crest is
       within TOL_X = 2 px.
    5. Null: N_NULL random segments per window, same length as the trace,
       azimuth uniform in the +/-15deg N-S band (0/180), centre uniform over
       the inner half of the window, scored against the SAME trace-masked
       profile. Verdict "tie-stripe-aligned" iff A_x >= the null's 95th
       percentile AND A_x >= the maximum A_x of the oblique written-up
       controls in their own windows.

  (LINE) line-scale E-W stripe test (the sourced flight-line direction):
    symmetric test on the row-mean profile, band-pass 2-6 px, tolerance
    TOL_Y = 1 px, crests >= 3 px apart, null = the near-N-S written-up
    candidates themselves (a N-S trace crosses the E-W stripes and provides
    the chance level for a trace that is NOT an E-W stripe). Reported for
    the oblique candidates: an E-W-trending artefact candidate would show
    A_y ~ 1 (all rows on one crest); none of the written-up oblique set
    trends E-W, so this arm is a geometry check, not a demotion instrument.

Bands: `tmi_hg` (primary, as in E10/E12) plus `tmi` and `rtp` as robustness
replicates (HGM/derived channels are downstream of these three).

Class verdict (pre-registered): the near-N-S emission class is "tie-stripe
locked" only if >= 3 of 4 near-N-S candidates are tie-stripe-aligned on
`tmi_hg` AND the median near-N-S A_x exceeds the median oblique A_x.

Self-alignment guard: the trace's own pixels are masked before any profile
is taken, and band edges are checked to be within the FFT support of each
window (window widths 51-83 px; 12-45 px band -> >= 2 cycles at the short
edge; the 2-6 px band has k = N/p >= 8 bins in every window).

Run:
  GEMS_SRC=/path/to/src python3 e14_alignment.py \
      --features data/training_features.tif \
      --candidates data/evidence/candidates.json --out e14_results.json

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

NEAR_NS = {3552: "C-2", 1618: "C-4", 872: "C-8", 4323: "C-10"}
NON_NS = {548: "C-1", 622: "C-3", 240: "C-5", 4383: "C-7"}
REPLICATE_BANDS = ("tmi", "rtp")

TIE_BAND = (12.0, 45.0)    # px periods: sourced tie spacings 20 / 40 px +- margin
LINE_BAND = (2.0, 6.0)     # px periods: sourced flight-line spacings 2 / 4 px
TOL_X = 2.0                # crest tolerance, tie test
TOL_Y = 1.0                # crest tolerance, line test
MIN_CREST_SEP_TIE = 12     # >= short edge of TIE_BAND
MIN_CREST_SEP_LINE = 3
N_NULL = 300
NULL_SEED = 20260926
WINDOW_HALF = 45           # px; >= 2 cycles of TIE_BAND[1] in every window


def bandpass(profile: np.ndarray, pmin: float, pmax: float) -> np.ndarray | None:
    """FFT band-pass keeping periods in [pmin, pmax] px. profile must be finite."""
    n = profile.size
    if n < 2 * pmax:
        return None
    p = profile - profile.mean()
    spec_f = np.fft.rfft(p)
    freqs = np.fft.rfftfreq(n, d=1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        periods = 1.0 / freqs
    keep = (periods >= pmin) & (periods <= pmax)
    out = np.fft.irfft(spec_f * keep, n=n)
    return out


def crests(signal: np.ndarray, min_sep: int) -> np.ndarray:
    """Local maxima of a 1-D signal, greedily enforcing min separation."""
    if signal.size < 2 * min_sep + 1:
        return np.empty(0, dtype=int)
    loc = []
    for i in range(1, signal.size - 1):
        if signal[i] >= signal[i - 1] and signal[i] > signal[i + 1]:
            loc.append(i)
    if not loc:
        return np.empty(0, dtype=int)
    loc = np.asarray(loc)
    order = np.argsort(-signal[loc])
    kept: list[int] = []
    for idx in loc[order]:
        if all(abs(idx - k) >= min_sep for k in kept):
            kept.append(int(idx))
    return np.asarray(sorted(kept), dtype=int)


def masked_profile(win: np.ndarray, rows: np.ndarray, cols: np.ndarray,
                   axis: str) -> np.ndarray | None:
    """Column- or row-mean profile with the trace's own pixels masked (+/-1).

    axis="x" -> profile over columns (each entry = nanmean over rows, with the
    trace pixels removed); axis="y" -> profile over rows. Masked positions are
    linearly interpolated across, so the FFT sees a finite series.
    """
    w = win.astype(np.float64).copy()
    h, wd = w.shape
    rr = np.clip(rows, 0, h - 1)
    cc = np.clip(cols, 0, wd - 1)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            r2 = np.clip(rr + dy, 0, h - 1)
            c2 = np.clip(cc + dx, 0, wd - 1)
            w[r2, c2] = np.nan
    with np.errstate(all="ignore"):
        prof = np.nanmean(w, axis=0) if axis == "x" else np.nanmean(w, axis=1)
    x = np.arange(prof.size)
    m = np.isfinite(prof)
    if m.sum() < max(8, prof.size // 2):
        return None
    return np.interp(x, x[m], prof[m])


def alignment_share(positions: np.ndarray, crest_pos: np.ndarray, tol: float) -> float | None:
    """Share of `positions` whose nearest crest is within `tol`."""
    if crest_pos.size == 0 or positions.size == 0:
        return None
    d = np.abs(positions[:, None].astype(float) - crest_pos[None, :].astype(float))
    return float((d.min(axis=1) <= tol).mean())


def random_ns_segments(length_px: int, win_shape: tuple[int, int], n: int,
                       seed: int) -> list[tuple[np.ndarray, np.ndarray]]:
    """(rows, cols) int pixel lists of random N-S-band straight segments."""
    rng = np.random.default_rng(seed)
    h, w = win_shape
    out = []
    for _ in range(n):
        az = np.deg2rad(rng.uniform(-15.0, 15.0))
        # azimuth measured from N (y): dx = sin, dy = cos (flips allowed)
        if rng.random() < 0.5:
            az += np.pi
        t = (np.arange(length_px) - (length_px - 1) / 2.0)
        cy = rng.uniform(h * 0.25, h * 0.75)
        cx = rng.uniform(w * 0.25, w * 0.75)
        rows = np.clip(np.round(cy + t * np.cos(az)), 0, h - 1).astype(int)
        cols = np.clip(np.round(cx + t * np.sin(az)), 0, w - 1).astype(int)
        out.append((rows, cols))
    return out


def tie_test(win: np.ndarray, rows: np.ndarray, cols: np.ndarray,
             n_null: int = N_NULL) -> dict:
    """The (TIE) arm: does the trace sit on a tie-scale N-S stripe crest?"""
    h, w = win.shape
    prof = masked_profile(win, rows, cols, axis="x")
    if prof is None:
        return {"ok": False, "reason": "profile unusable"}
    bp = bandpass(prof, *TIE_BAND)
    if bp is None:
        return {"ok": False, "reason": f"window width {w} < 2 x {TIE_BAND[1]:g}"}
    cr = crests(bp, MIN_CREST_SEP_TIE)
    # unique per-row x of the trace (its column coordinate along the line)
    order = np.argsort(rows)
    xs = cols[order].astype(float)
    a_x = alignment_share(xs, cr, TOL_X)
    # null: random N-S segments of the same length against the same profile
    nulls = []
    for r2, c2 in random_ns_segments(len(rows), (h, w), n_null, NULL_SEED + len(rows)):
        a = alignment_share(c2.astype(float), cr, TOL_X)
        if a is not None:
            nulls.append(a)
    null_arr = np.asarray(nulls)
    p95 = float(np.percentile(null_arr, 95)) if null_arr.size else None
    # empirical p: share of null segments scoring >= the trace's own A_x.
    # With short near-vertical segments the null is nearly bimodal (on-crest
    # -> ~1, off-crest -> ~0), so this is the informative tail probability,
    # not the percentile bar alone.
    emp_p = (float((null_arr >= a_x).mean()) if null_arr.size and a_x is not None
             else None)
    # analytic chance coverage: expected share of random positions landing
    # within TOL_X of a crest, given the measured crest density. Reported so
    # the instrument cannot quietly sit at chance level.
    chance = min(1.0, cr.size * (2.0 * TOL_X + 1.0) / prof.size)
    return {
        "ok": True, "n_crests": int(cr.size), "A_x": a_x,
        "chance_coverage_analytic": round(chance, 4),
        "null_mean": float(null_arr.mean()) if null_arr.size else None,
        "null_p50": float(np.percentile(null_arr, 50)) if null_arr.size else None,
        "null_p95": p95,
        "null_empirical_p_ge_trace": emp_p,
        "trace_exceeds_null_p95": bool(a_x is not None and p95 is not None
                                       and a_x >= p95),
        "profile_len": int(prof.size),
        "band_px": list(TIE_BAND),
    }


def line_test(win: np.ndarray, rows: np.ndarray, cols: np.ndarray) -> dict:
    """The (LINE) arm: does the trace sit on a line-scale E-W stripe crest?"""
    prof = masked_profile(win, rows, cols, axis="y")
    if prof is None:
        return {"ok": False, "reason": "profile unusable"}
    bp = bandpass(prof, *LINE_BAND)
    if bp is None:
        return {"ok": False, "reason": f"window height < 2 x {LINE_BAND[1]:g}"}
    cr = crests(bp, MIN_CREST_SEP_LINE)
    order = np.argsort(cols)
    ys = rows[order].astype(float)
    a_y = alignment_share(ys, cr, TOL_Y)
    # analytic chance coverage: with crests ~3-6 px apart and TOL_Y = 1, the
    # instrument's chance level is intrinsically high — reported, and this arm
    # is therefore comparative only, never a verdict by itself.
    chance = min(1.0, cr.size * (2.0 * TOL_Y + 1.0) / prof.size)
    return {"ok": True, "n_crests": int(cr.size), "A_y": a_y,
            "chance_coverage_analytic": round(chance, 4),
            "band_px": list(LINE_BAND)}


def window_of(rows: np.ndarray, cols: np.ndarray) -> tuple[slice, slice]:
    minr, maxr = int(rows.min()), int(rows.max())
    minc, maxc = int(cols.min()), int(cols.max())
    r0 = max(0, minr - WINDOW_HALF)
    r1 = min(spec.HEIGHT, maxr + WINDOW_HALF + 1)
    c0 = max(0, minc - WINDOW_HALF)
    c1 = min(spec.WIDTH, maxc + WINDOW_HALF + 1)
    return (slice(r0, r1), slice(c0, c1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", default="data/training_features.tif")
    ap.add_argument("--candidates", default="data/evidence/candidates.json")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    import rasterio
    cands = {c["id"]: c for c in json.load(open(args.candidates))["candidates"]}
    ids = {**NEAR_NS, **NON_NS}

    report: dict = {
        "design": {
            "tie_band_px": list(TIE_BAND), "line_band_px": list(LINE_BAND),
            "tol_x": TOL_X, "tol_y": TOL_Y, "n_null": N_NULL,
            "geometry_source": "USGS data release 10.5066/P93LGLVQ: flight "
                               "lines az 90 (E-W) 200/400 m; tie lines az 180 "
                               "(N-S) 2000/4000 m -> at 100 m sampling: E-W "
                               "stripes 2-4 px period, N-S stripes 20-40 px",
        },
        "candidates": {},
    }

    with rasterio.open(args.features) as src:
        band_data: dict[str, np.ndarray] = {}
        for name in ("tmi_hg",) + REPLICATE_BANDS:
            a = src.read(spec.BAND_INDEX[name]).astype(np.float32)
            a[a < spec.FEATURE_INVALID_BELOW] = np.nan
            band_data[name] = a

        for cid, label in ids.items():
            c = cands[cid]
            near_ns = min(abs(c["azimuth_deg"] % 180.0),
                          180.0 - abs(c["azimuth_deg"] % 180.0)) <= 15.0
            rows_g, cols_g = centerline_pixels(c["utm_bbox"], c["azimuth_deg"],
                                               c["length_m"])
            sl = window_of(rows_g, cols_g)
            rows = rows_g - sl[0].start
            cols = cols_g - sl[1].start
            rec: dict = {"azimuth_deg": c["azimuth_deg"], "near_n_s": bool(near_ns),
                         "length_px": int(len(rows_g))}
            for bname, full in band_data.items():
                win = full[sl]
                t = tie_test(win, rows, cols)
                ln = line_test(win, rows, cols)
                rec[bname] = {"tie": t, "line": ln}
            report["candidates"][label] = rec
            t = rec["tmi_hg"]["tie"]
            print(f"{label} (az {c['azimuth_deg']:7.1f}, "
                  f"{'N-S' if near_ns else 'obl'}): "
                  f"A_x={t.get('A_x')} vs null_p95={t.get('null_p95')} "
                  f"-> tie-aligned={t.get('trace_exceeds_null_p95')}; "
                  f"A_y(line)={rec['tmi_hg']['line'].get('A_y')}")

    # verdicts, primary band only (replicates reported, not decided on)
    oblique_max_ax = 0.0
    for label, rec in report["candidates"].items():
        if not rec["near_n_s"]:
            a = rec["tmi_hg"]["tie"].get("A_x")
            if a is not None:
                oblique_max_ax = max(oblique_max_ax, a)
    n_aligned = 0
    near_shares, obl_shares = [], []
    for label, rec in report["candidates"].items():
        t = rec["tmi_hg"]["tie"]
        if not t.get("ok"):
            continue
        aligned = bool(t["trace_exceeds_null_p95"] and t["A_x"] >= oblique_max_ax)
        rec["tmi_hg"]["tie"]["verdict_tie_stripe_aligned"] = aligned
        if rec["near_n_s"]:
            n_aligned += int(aligned)
            near_shares.append(t["A_x"])
        else:
            obl_shares.append(t["A_x"])
    report["summary"] = {
        "oblique_control_max_A_x": oblique_max_ax,
        "near_ns_tie_aligned": n_aligned,
        "near_ns_median_A_x": float(np.median(near_shares)) if near_shares else None,
        "oblique_median_A_x": float(np.median(obl_shares)) if obl_shares else None,
        "class_verdict_tie_stripe_locked": bool(
            n_aligned >= 3
            and near_shares and obl_shares
            and np.median(near_shares) > np.median(obl_shares)),
    }
    print("\nsummary:", json.dumps(report["summary"], indent=2))

    if args.out:
        with open(args.out, "w") as f:
            json.dump(report, f, indent=2, default=float)
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
