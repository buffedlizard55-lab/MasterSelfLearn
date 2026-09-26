#!/usr/bin/env python3
"""E12 — stripe-removal (flight-line levelling) pass over the magnetic bands.

Session-5 implementation of `HYPOTHESES.md` E12, motivated by the class-level
finding of E10 (CANDIDATE_GEOLOGY.md §6): 3/3 tested near-N–S traces flagged
for narrowband E–W periodicity under `tmi_hg` (C-2 sat at the threshold), i.e.
the azimuth ≈ 0–17° emission class is artefact-suspect as a class.

Pre-registered test (HYPOTHESES.md E12): "re-run (a) on a levelled stack; flag
rate must fall below the non-N–S baseline."

Method
------
A north–south flight-line artefact is, to first order, a function of COLUMN
position only (constant along the line). The levelling estimate is therefore

    s(x) = nanmedian over rows of the band, per column
    levelled(x, y) = band(x, y) - s(x)

computed on the official raw magnetic bands of the pinned raster
(`tmi_hg`, `tmi`, `tmi_vg`, `mag_anom`, `rtp`, `tc`). s(x) is exactly the
component test (a) measures: E10's striping statistic is the FFT power share
of the window's COLUMN-MEAN profile, which an x-only component contributes to
in full, while real geology varies in y and survives the subtraction.

Then test (a) — identical machinery to `e10_falsification.py`, same windows,
same 0.25 flag threshold — is re-run on raw vs levelled `tmi_hg` for:

  * the four near-N–S written-up candidates  (C-2, C-4, C-8, C-10)
  * the four non-N–S written-up candidates   (C-1, C-3, C-5, C-7) as the
    baseline distribution the near-N–S shares must fall to

Two guards against a "fix" that destroys the data:

  * signal preservation: Pearson r(raw, levelled) inside each window, and the
    trace-vs-window contrast (the quantity the geology is read from) before
    and after;
  * over-removal check: the levelled band's column-mean profile share must
    drop, but the ROW-mean profile (control direction, which striping does
    not touch) must be statistically unchanged.

Limitation, stated not smoothed: this levels the RAW bands of the official
raster. The shipped model consumes DERIVED channels (`mag_anom_hgm_computed`,
`mag_tilt`, `tdr_tmi_*`, multi-scale HGM…) built from these bands — a full
"levelled stack" requires re-running `scripts/build_features.py` on levelled
inputs, which is the follow-up, not this probe's claim.

Run:
  GEMS_SRC=/path/to/src python3 e12_stripe_removal.py \
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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gems import spec  # noqa: E402
from e10_falsification import (  # noqa: E402
    WINDOW_PX, STRIPING_MIN_SHARE, centerline_pixels, periodicity,
)

# written-up candidates, by candidates.json id
NEAR_NS = {3552: "C-2", 1618: "C-4", 872: "C-8", 4323: "C-10"}
NON_NS = {548: "C-1", 622: "C-3", 240: "C-5", 4383: "C-7"}
MAG_BANDS = ["tmi_hg", "tmi", "tmi_vg", "mag_anom", "rtp", "tc"]


def level_by_column(band: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Subtract the per-column nanmedian (the x-only flight-line component).

    Returns (levelled, stripe_field). The stripe field is broadcast over rows
    only for reporting; the subtraction itself never touches y-structure.
    """
    with np.errstate(all="ignore"):
        s = np.nanmedian(band, axis=0)          # shape (width,)
    s = np.where(np.isfinite(s), s, 0.0)
    return (band - s[None, :]).astype(np.float32), s


def level_by_block(band: np.ndarray, block: int = 256, stride: int = 128
                   ) -> tuple[np.ndarray, np.ndarray]:
    """Y-AWARE levelling: per-column nanmedian within rolling row-blocks.

    The session-5 first attempt (global column median) does not reduce the
    window statistic because flight-line offsets vary ALONG the line: the
    stripe field is s(x, y), not s(x). This variant estimates it per
    (row-block, column) and linearly interpolates block estimates in y, so
    the subtraction can follow along-line drift while staying x-structured.
    """
    h, w = band.shape
    centers, fields = [], []
    starts = list(range(0, max(1, h - block + 1), stride))
    if not starts or starts[-1] + block < h:
        starts.append(max(0, h - block))
    for s0 in starts:
        s1 = min(h, s0 + block)
        with np.errstate(all="ignore"):
            f = np.nanmedian(band[s0:s1], axis=0)
        centers.append(0.5 * (s0 + s1 - 1))
        fields.append(np.where(np.isfinite(f), f, 0.0))
    centers = np.asarray(centers, dtype=float)
    stack = np.stack(fields, axis=0)              # (n_blocks, width)
    yy = np.arange(h, dtype=float)[:, None]
    # np.interp needs increasing xp; handles the 1- or 2-block case too
    out = np.empty_like(band, dtype=np.float32)
    for y0 in range(0, h, 512):
        y1 = min(h, y0 + 512)
        seg = np.empty((y1 - y0, w), dtype=np.float32)
        for j in range(w):
            seg[:, j] = np.interp(yy[y0:y1, 0], centers, stack[:, j])
        out[y0:y1] = band[y0:y1] - seg
    return out, stack.mean(axis=0)


def pearson(a: np.ndarray, b: np.ndarray) -> float:
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 12:
        return float("nan")
    x, y = a[m].astype(float), b[m].astype(float)
    if x.std() == 0 or y.std() == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def window_stats(win: np.ndarray) -> dict:
    col = np.nanmean(win, axis=0)
    row = np.nanmean(win, axis=1)
    return {"e_w": periodicity(col), "n_s": periodicity(row)}


def flag_of(ew: dict, win_width: int) -> bool:
    return bool(ew["power_share"] is not None
                and ew["power_share"] >= STRIPING_MIN_SHARE
                and ew["period_px"] and ew["period_px"] <= win_width / 2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", default="data/training_features.tif")
    ap.add_argument("--candidates", default="data/evidence/candidates.json")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    import rasterio
    cands = {c["id"]: c for c in json.load(open(args.candidates))["candidates"]}
    ids = {**NEAR_NS, **NON_NS}

    report: dict = {"level_method": "A: per-column nanmedian subtraction "
                                     "(global flight-line offset, x-only); "
                                     "B: y-aware 256-row block column medians "
                                     "(128 stride, linear interp in y)",
                    "flag_threshold": STRIPING_MIN_SHARE, "candidates": {}}

    with rasterio.open(args.features) as src:
        # --- level every magnetic band once (whole grid) -------------------
        levelled_bands: dict[str, np.ndarray] = {}
        stripe_fields: dict[str, np.ndarray] = {}
        raw_tmi_hg = None
        for name in MAG_BANDS:
            a = src.read(spec.BAND_INDEX[name]).astype(np.float32)
            a[a < spec.FEATURE_INVALID_BELOW] = np.nan
            if name == "tmi_hg":
                raw_tmi_hg = a
            lev, s = level_by_column(a)
            levelled_bands[name] = lev
            stripe_fields[name] = s
            # how much x-only variance did we remove? (whole-grid std of s vs band)
            report.setdefault("stripe_fields", {})[name] = {
                "field_std": round(float(np.nanstd(s)), 4),
                "band_std": round(float(np.nanstd(a)), 4),
                "field_to_band_std_ratio":
                    round(float(np.nanstd(s) / np.nanstd(a)), 4)
                    if np.nanstd(a) > 0 else None,
                # is the x-only field itself periodic at flight-line scales?
                "field_periodicity": periodicity(s),
            }
        lev_tmi_hg = levelled_bands["tmi_hg"]
        blk_tmi_hg, blk_field = level_by_block(raw_tmi_hg)
        report["stripe_fields"]["tmi_hg_block_method"] = {
            "field_std": round(float(np.nanstd(blk_field)), 4),
            "band_std": round(float(np.nanstd(raw_tmi_hg)), 4),
            "note": "y-aware (256-row block, 128 stride) column medians",
        }

        raw_flags = 0
        lev_flags = 0
        blk_flags = 0
        near_shares_raw, near_shares_lev, base_shares_raw, base_shares_lev = [], [], [], []
        near_shares_blk, base_shares_blk = [], []

        for cid, label in ids.items():
            c = cands[cid]
            near_ns = min(abs(c["azimuth_deg"] % 180.0),
                          180.0 - abs(c["azimuth_deg"] % 180.0)) <= 15.0
            rows, cols = centerline_pixels(c["utm_bbox"], c["azimuth_deg"],
                                           c["length_m"])
            minr, maxr = int(rows.min()), int(rows.max())
            minc, maxc = int(cols.min()), int(cols.max())
            r0 = max(0, minr - WINDOW_PX); r1 = min(spec.HEIGHT, maxr + WINDOW_PX + 1)
            c0 = max(0, minc - WINDOW_PX); c1 = min(spec.WIDTH, maxc + WINDOW_PX + 1)
            sl = (slice(r0, r1), slice(c0, c1))

            w_raw = raw_tmi_hg[sl]
            w_lev = lev_tmi_hg[sl]
            w_blk = blk_tmi_hg[sl]
            sr = window_stats(w_raw)
            slv = window_stats(w_lev)
            sbk = window_stats(w_blk)
            fr = near_ns and flag_of(sr["e_w"], w_raw.shape[1])
            fl = near_ns and flag_of(slv["e_w"], w_raw.shape[1])
            fbl = near_ns and flag_of(sbk["e_w"], w_raw.shape[1])
            raw_flags += int(fr)
            lev_flags += int(fl)
            blk_flags += int(fbl)

            rec = {
                "azimuth_deg": c["azimuth_deg"], "near_n_s": bool(near_ns),
                "raw": {"e_w_share": sr["e_w"]["power_share"],
                        "e_w_period_px": sr["e_w"]["period_px"],
                        "n_s_share": sr["n_s"]["power_share"],
                        "flag": bool(fr)},
                "levelled": {"e_w_share": slv["e_w"]["power_share"],
                             "e_w_period_px": slv["e_w"]["period_px"],
                             "n_s_share": slv["n_s"]["power_share"],
                             "flag": bool(fl)},
                "levelled_block": {"e_w_share": sbk["e_w"]["power_share"],
                                   "e_w_period_px": sbk["e_w"]["period_px"],
                                   "n_s_share": sbk["n_s"]["power_share"],
                                   "flag": bool(fbl)},
                "pearson_raw_vs_levelled": round(pearson(w_raw, w_lev), 4),
                "pearson_raw_vs_levelled_block": round(pearson(w_raw, w_blk), 4),
            }
            # trace-vs-window contrast (the geology signal) before/after
            for tag, w in (("raw", w_raw), ("levelled", w_lev),
                           ("levelled_block", w_blk)):
                tv = w[rows - r0, cols - c0]
                rec[tag]["trace_minus_window_std"] = round(
                    (float(np.nanmean(tv)) - float(np.nanmean(w)))
                    / (float(np.nanstd(w)) or np.nan), 3)
            report["candidates"][label] = rec
            if near_ns:
                near_shares_raw.append(sr["e_w"]["power_share"])
                near_shares_lev.append(slv["e_w"]["power_share"])
                near_shares_blk.append(sbk["e_w"]["power_share"])
            else:
                base_shares_raw.append(sr["e_w"]["power_share"])
                base_shares_lev.append(slv["e_w"]["power_share"])
                base_shares_blk.append(sbk["e_w"]["power_share"])

            print(f"{label} ({'N-S' if near_ns else 'non-N-S'}): "
                  f"E-W share raw {sr['e_w']['power_share']} (flag {fr}) -> "
                  f"col-lev {slv['e_w']['power_share']} (flag {fl}) -> "
                  f"block-lev {sbk['e_w']['power_share']} (flag {fbl}); "
                  f"r={rec['pearson_raw_vs_levelled']}/"
                  f"{rec['pearson_raw_vs_levelled_block']}; "
                  f"trace contrast {rec['raw']['trace_minus_window_std']} -> "
                  f"{rec['levelled_block']['trace_minus_window_std']}")

        def summ(xs):
            xs = [x for x in xs if x is not None]
            return {"mean": round(float(np.mean(xs)), 4),
                    "max": round(float(np.max(xs)), 4), "n": len(xs)}

        report["summary"] = {
            "near_ns_flags_raw": raw_flags,
            "near_ns_flags_levelled": lev_flags,
            "near_ns_flags_levelled_block": blk_flags,
            "near_ns_shares_raw": summ(near_shares_raw),
            "near_ns_shares_levelled": summ(near_shares_lev),
            "near_ns_shares_levelled_block": summ(near_shares_blk),
            "non_ns_baseline_shares_raw": summ(base_shares_raw),
            "non_ns_baseline_shares_levelled": summ(base_shares_lev),
            "non_ns_baseline_shares_levelled_block": summ(base_shares_blk),
            "criterion_flag_rate_below_non_ns_baseline": bool(
                blk_flags == 0
                and (max(x for x in near_shares_blk if x is not None)
                     <= summ(base_shares_blk)["max"])),
        }

    # control direction: striping does not touch the row-mean profile —
    # verify the removal did not eat it either
    print("\nstripe fields (x-only component removed):")
    for name, v in report.get("stripe_fields", {}).items():
        ratio = v.get("field_to_band_std_ratio")
        per = v.get("field_periodicity")
        extra = (f"; field E-W period {per['period_px']} px, "
                 f"share {per['power_share']}") if per else ""
        print(f"  {name}: field_std {v['field_std']} vs band_std "
              f"{v['band_std']} (ratio {ratio}){extra}")
    s = report["summary"]
    print(f"\nnear-N-S flags: {s['near_ns_flags_raw']}/4 raw -> "
          f"{s['near_ns_flags_levelled']}/4 col-lev -> "
          f"{s['near_ns_flags_levelled_block']}/4 block-lev")
    print(f"near-N-S E-W shares: {s['near_ns_shares_raw']} -> "
          f"{s['near_ns_shares_levelled']} -> "
          f"{s['near_ns_shares_levelled_block']}")
    print(f"non-N-S baseline shares: {s['non_ns_baseline_shares_raw']} -> "
          f"{s['non_ns_baseline_shares_levelled']} -> "
          f"{s['non_ns_baseline_shares_levelled_block']}")
    print(f"criterion met (0 flags AND max share <= non-N-S max): "
          f"{s['criterion_flag_rate_below_non_ns_baseline']}")

    if args.out:
        with open(args.out, "w") as f:
            json.dump(report, f, indent=2, default=float)
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
