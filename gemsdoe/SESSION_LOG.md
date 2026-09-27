# SESSION LOG — GEMS Prize work in MasterSelfLearn

Append-only. Newest session first. Every row of evidence carries its capture
method (`gh api`, research fetch, …) and timestamp. Runner fact: direct
`curl`/`urllib` egress from this sandbox is TLS-blocked (every probe returns
an SSL EOF); all live reads use the GitHub API (`gh`) or the research fetch
tool. That is a fact about this runner, never a claim that a target is down.

---

# SESSION LOG — GEMS Prize work in MasterSelfLearn

Append-only. Newest session first. Every row of evidence carries its capture
method (`gh api`, research fetch, …) and timestamp. Runner fact: direct
`curl`/`urllib` egress from this sandbox is TLS-blocked (every probe returns
an SSL EOF); all live reads use the GitHub API (`gh`) or the research fetch
tool. That is a fact about this runner, never a claim that a target is down.

---

## Session 6 — 2026-09-26 (UTC, ~23:10–00:30) · branch `arena/01a0dffd-masterselflearn`

### 0. Mandate check

Read session 5's carry-forward (§8 of that entry) and the standing brief
before anything new. Carry-forward order: (1) human ratification,
(2) E11 submission decision, (3) apply session-4+5 patches in the ratified
repo, (4) E12 as an alignment test + GeoDAWN flight-line metadata,
(5) cond multi-profile follow-ups + famrank_cond member decision,
(6) whole-system holdout, (7) engine-side F10. Items 1–3 remain blocked on a
human; **items 4, 5 AND 6 were all executed** (6 needed a grouping key that
did not exist — this session built it). The brief's own items 1–7 were
verified against fresh runs, not cited. Outputs: two new probes, one new
experiment instrument (`--system-holdout`), one verified patch, the sourced
flight-geometry correction, and the write-ups below. Raw outputs committed at
[`gemsdoe/evidence/session6/`](evidence/session6/).

### 1. Guardrail check first: one account, one repo (brief guardrail 1)

| Check | Method (this session, ~23:16Z) | Result |
|---|---|---|
| GEMSDOE repo inventory | `gh api search/repositories?q=GEMSDOE+in:name` | `total_count: 11`, all `owner_id 309556078`. Newest `created_at` still 2026-09-25T18:33:56Z — **no new repo created**. |
| New pushes since session 5 | `pushed_at` + commit logs | **YES — during this session**: `7GEMSDOE` merged PRs #7/#8 at 22:53:02Z and 22:58:49Z (branch `arena/01a0dfad-7gemsdoe`), `8GEMSDOE.pushed_at` 23:15:58Z with Pages `building` (its Pages was caught mid-deploy). F12 pattern continues, now mid-session, not just between sessions. |
| Stub status | `created_at`/`pushed_at` on `GEMSDOE9`, `GEMSDOE10`, `11GEMSDOE` | All three still `pushed_at == created_at` (untouched stubs, Pages built). |
| Secondary account | `gh api users/kanlerxz87-cyber` | Still 0 public repos (id 312694378). |
| Pages status ×11 | `gh api repos/<r>/pages` | 10 **built**, `8GEMSDOE` **building** (a deploy was in progress at 23:16Z). |
| DrivenData registrations | fresh leaderboard pull (§2) | Unverifiable from public data (F5, unchanged). No registration treated as ours. |

**Verdict, not smoothed:** the "ONE repo" condition remains **violated**
(standing since session 1; consolidation still blocked on human ratification,
sixth session). No new repo/registration was created; two parallel arms were
provably active *during* this session. This session created nothing, treated
no other entrant's registration or score as our data or as an arm, and wrote
to no GEMSDOE repository (scratch checkout in `/tmp` only).

### 2. Fresh leaderboard — pulled ≈23:16Z via research fetch (brief item 7)

Source: <https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/>
(static render through #50 = 0.0878; the board got denser at the bottom).

| Rank | Participant | Score | Subs | Last activity | Note |
|---|---|---|---|---|---|
| #1 | DARD | **0.3049** | 10 | 4d | field high, **unchanged across six sessions** |
| #5 | joeyfezster | 0.2589 | 12 | 1d 5h | **pay line**, unchanged |
| #24 | extradr19 | 0.1563 | 2 | 1d 22h | brief row: GEMSDOE |
| #25 | SDCF9 | 0.1563 | 2 | **5h 20m** | brief row: GEMSDOE3; activity without count change |
| #26 | smashi34 | 0.1560 | 1 | 1d 5h | brief row: GEMSDOE2 |
| #42 | smrtdoog5 | 0.1193 | 1 | 1d 5h | brief row: GEMSDOE3 |
| >#50 | wbg1 | 0.0830 (session-5 value) | 2 | — | **fell off the visible board**: #50 is now tarabird90 0.0878 |

All five tracked rows exact-match session 5's scores; no new attributable
registration appeared in the visible ranks. Field reading: gap from the best
tracked row (0.1563) to the pay line = **0.1026** (unchanged); to field high
0.1486. **Flagged:** wbg1's row is now untraceable from public data — the
static render ends at #50 and rows below load via JavaScript, so any future
score changes below 0.0878 are invisible to this runner. We plausibly sit
mid-pack: best tracked row at #24 of 50 visible.

### 3. Ownership of the three "unconfirmed" sites — RESOLVED again, this session's own calls (brief item 7)

Fresh `gh api repos/...` calls at ~23:16Z: `5GEMSDOE`, `GEMSDOE4`, `6GEMSDOE`
all return `owner.login = buffedlizard55-lab`, `owner_id = 309556078` —
identical to every other GEMSDOE repo. **They are ours as repositories**
(confirmed for the fifth time, always with the session's own API calls).
All three sites were **visited this session** plus GEMSDOE1/2/3 and the
6GEMSDOE root site: GEMSDOE1 `7f00890a…` (unchanged), GEMSDOE2 dual-family
union `f68e590f…` + the three-arm week plan (unchanged; still attributing
"0.1563 = the recall-union's board score" across sites), GEMSDOE3 Pindrop v4
(unchanged), 5GEMSDOE `7f00890a…` + its S5-A hedge candidate 227,507 px
(unchanged), GEMSDOE4 `237f0063…` k=3-of-5 union 264,247 px (unchanged),
6GEMSDOE shipped file + 13-check table + its own canonical claim
(unchanged — F4 conflict stands upstream). What remains unverified (F5):
which DrivenData *registrations* the scores belong to; none is treated as
our own.

### 4. Brief items 1–5, re-verified this session (fresh runs, not citations)

Environment: fresh scratch clone `6GEMSDOE@e2fe3f41` (HEAD = pin) + session-4
patch + session-5 patch (both `git apply --check` clean again); Python 3.11.2,
numpy 2.4.6, scipy 1.17.1, rasterio 1.4.4, sklearn 1.9.1, pytest 9.1.1.
Bridge reassembled, sha256 `4371c82e…` matches `spec.PINS` (plus labels
`7ba308cc…`, template `2176d08e…`, shipped file `33cec71f…` — all four
pins exact). Rank tables 129.2 s; feature build 1,031.8 s; valid mask
**5,165,840** — byte-consistent with sessions 4/5 rebuilds.

| Brief item | Verdict |
|---|---|
| 1. Feature engineering vs the priorities | Re-derived from the rebuilt `features_meta.json`: 105 channels; HGM/tilt on mag+grav = 26 channels, curvature/slope-break on DEM = 14 — **all inside the shipped 88**; the strain×cond×seis cross-reference block (famrank/agree, indices 88–104) is the 17-channel block excluded by `--n-channels 88` (only the three `x_*` products survive inside). Evidence for/against that exclusion: E9/E13 (gap-population win for 105) is now **weakened by E14-SYS** — see §5.4: the whole-system holdout, the harder instrument, shrinks the 105-ch gap advantage to ≈0–0.0017. |
| 2. Spatially blocked + buffered CV | **Confirmed on the patched tree**: `probe_cv_buffer.py` → 0/29 unexcluded kernel offsets; 0.000% leakage at every layout incl. 6-blocks/4-folds; `probe_feature_guard.py` → 0 affected-but-finite px at σ=1.5/3.0; `probe_crossder_halo.py` → 0. The only randomness anywhere is negative subsampling inside already-blocked masks; standardisation train-only. **No random pixel split.** 46/46 tests pass. |
| 3. Metric-aware placement intact | **Intact** — `thin_keep`/`_skeleton`/`skeleton_spaced4`/`topk_mask`/`gated_topk`/`breakeven_posterior` all present; 17 metric/placement tests pass. The ~4–5 px spacing premise stays **falsified** (HE, session 3, budget-matched); intactness ≠ adopted and that's unchanged. |
| 4. Submission generator + gate | **Re-verified end to end this session**: shipped file sha `33cec71ff0…` matches pin; gate **13/13 PASS** incl. `NAN-INSIDE-FOOTPRINT`, exit 0; negative test (one NaN injected at (936,1221) inside the footprint, on a copy): `values-in-0-1` still passes, `NAN-INSIDE-FOOTPRINT` **fails**, exit **1**. Hard-gate requirement met. |
| 5. Executive summary / how-to-submit | Checkable claims still accurate: file name/sha/1,652,883 bytes, 155,021 px = 3.00%, {0,1} values, model string, the DTI-monotonicity argument, the 13-check list, the minimax table; the "one-entry record" in SUBMISSION_GUIDE.md is still correctly blank. **Standing upstream flags unchanged** (session 5): both guides pre-date forum-11516 masking; `EXECUTIVE_SUMMARY.md`/`ACCOUNT_STATUS.md`/README assert the "designated single entry" designation as fact while F4 records it was never ratified; the "what did NOT work" framing treats the agreement channels on the catalogue proxy only, now fully superseded by E9/E13/E14-SYS. Nothing written upstream. |
| 6. Geological reasoning | Extended — `CANDIDATE_GEOLOGY.md` **§8**: E14 stripe-closure, cond multi-profiles + member attribution, per-candidate status-change table. |
| 7. Field standing + ownership | §2–§3. Mid-pack; ownership of the three sites resolved ours (fifth confirmation). |

### 5. What was executed (carry-forward 4, 5, 6)

#### 5.1 Sourced flight metadata (carry 4b) — the physical prior was wrong for GeoDAWN

USGS Science Data Catalog, GeoDAWN data release (Glen & Earney 2024,
DOI 10.5066/P93LGLVQ,
<https://data.usgs.gov/datacatalog/data/USGS:657e1d85d34e23d3533209f7>,
fetched verbatim this session): Area 1 flight lines **200 m at azimuth
90°**, ties 2000 m az 180°; **Area 2** (the geothermal block covering the
study area — interpretation from the page's own area descriptions, stated)
flight lines **400 m at azimuth 90°**, ties **4000 m az 180°**. Magnetic
processing includes "tie-line leveling, **micro-leveling**" (already
applied by the contractor). Session 3's prior ("N–S = classic flight-line
direction") is therefore wrong for GeoDAWN: flight lines are **E–W**; N–S is
the tie direction (20–40 px E–W period at 100 m sampling). Recorded verbatim
in `CANDIDATE_GEOLOGY.md` §8.1.

#### 5.2 E14 — the alignment test (carry 4a), executed

New probe `gemsdoe/probes/e14_alignment.py` (design pre-registered in the
probe's header before the first run): trace-self-masked 12–45 px band-pass
crest alignment in ±45 px windows; null = 300 random N–S segments/window;
verdict bar A_x ≥ null p95 AND ≥ oblique max. First run caught and fixed an
instrument insufficiency **by its own output**: at E10's ±25 px window the
shortest trace's window (62 px) could not hold two cycles of the 45 px tie
edge — the window was widened to ±45 px and the change stated in the probe,
not hidden. Results (raw: `evidence/session6/e14_results.json`):

- **C-2, C-8, C-10: A_x = 0.000 on all three bands (emp. p 1.00)** —
  decisively not tie-stripe locked.
- **C-4: A_x = 0.938 on `tmi_hg` only; emp. p = 0.22; replicates `tmi`/`rtp`
  = 0.000** — below the pre-registered bar (null p95 = 1.0) and
  non-replicating: recorded as an anomaly, not a detection.
- **Class verdict: 0/4 aligned; near-N–S median 0.000 vs oblique median
  0.254 → NOT tie-stripe locked.**
- Line arm (E–W stripes 2–6 px, the sourced flight direction): per-candidate
  A_y 0.38–0.78 against analytic chance coverage 0.48–0.61 (min/max over
  candidates × the three bands) — at chance everywhere; comparative-only
  instrument, stated.

**The stripe question is closed for the written-up set; the "N–S emission
class is artefact-suspect" framing is retired** (`CANDIDATE_GEOLOGY.md`
§8.2/§8.4). C-4's magnetics return to neutral standing; the demoted-status
basis (D-9) is now invalidated on two independent legs.

#### 5.3 Cond multi-profiles + member attribution (carry 5), executed

New probe `gemsdoe/probes/followup_cond_multiprofile.py`, pre-registered
verdict rules (raw: `evidence/session6/cond6_results.json`):

- **C-8: 0/5 profiles local-max → kill-if stands (regional)** — session 5's
  single-profile conclusion confirmed beyond its own caveat.
- **C-9: 0/5 → kill-if stands**, measured for the first time (session 5 had
  rank-check only). Its cond pillar is regional.
- **C-4: 2/5 local-max (fracs 0.70/0.85) on MAD-scale residuals, all five
  raw trace means below window medians → "inconclusive" per the
  pre-registered rule** — refined from session 5's "kill-if supported"; the
  multi-profile extension does not support the conductor story anywhere
  either (trace never a raw high). Flagged precisely, not resolved into a
  cleaner-sounding verdict.
- **Member attribution over 260 candidates**: `famrank_cond` = max of the
  two member ranks, NO inversion on `depth_to_base_surf` (verified in
  `build_features.py`). 89 candidates ≥ 0.75; **24/89 (27%) carried by
  `depth_to_base_surf` alone** (e.g. id 4176: fam 0.991 = max(cond **0.097**,
  d2b 0.991)) — sediment thickness, not subsurface conductivity, under the
  official band descriptions. Written-up set: 9/10 fire on cond_surf
  (C-2's 0.431 the exception, always its weak family).
- **Decision recorded (recommendation level)**: report `famrank_cond` as two
  sub-signals; the drop-the-depth-member ablation is queued but was not run.

#### 5.4 Whole-system holdout (carry 6) — grouping key built, instrument implemented, experiment run

Session 5 noted this was blocked on "a grouping key that does not exist
yet". This session built it: **8-connected components of the catalogue after
Euclidean dilation by a link radius**. Radius scan (this session): r=10 px →
**266 systems** (median 3 traces, largest 10.8% of labels); r=25 px → 39
systems (largest 36.6%); r=50 px → 3 (degenerate). Default link radius 10 px
(nearest-pixel merge distance 2 km). Single-valuedness asserted: **0 of
3,199 traces span >1 component** (chain argument verified numerically, not
assumed). Implemented as `--system-holdout/--system-link-px` in
`experiment.py` (mutually exclusive with `--trace-holdout`; reuses the
`trace_excl` train-exclusion and the whole trace_gap/trace_seen/masked
reporting), 46/46 tests pass with it in place, patch delivered:
[`patches/session6_system_holdout.patch`](patches/session6_system_holdout.patch)
— **not applied upstream**, same rule as sessions 4/5.

Run (exactly E13's recipe, system holdout replacing trace holdout):
`experiment.py --configs extended,agreement --system-holdout 0.3
--max-train-px 400000 --iters 300 --fp-mask-px 0` →
`evidence/session6/experiments_e14sys.json`. Holdout: **80 of 266 systems =
787 traces = 14,128 gt px** (23.2% of labels).

**E14-SYS result — the E9/E13 gap win does *not* transfer at whole-system
scale.** Mean blocked-CV DTI, system-gap truth, 88 vs 105 channels
(masked = FP side of forum-11516 at width-0):

| placement | gap 88 | gap 105 | Δ | gap masked 88 | gap masked 105 | Δ masked |
|---|---|---|---|---|---|---|
| topk_hard@0.01 | 0.0462 | 0.0447 | −0.0014 | 0.0475 | 0.0459 | −0.0016 |
| topk_hard@0.02 | 0.0470 | 0.0473 | +0.0003 | 0.0483 | 0.0485 | +0.0002 |
| topk_hard@0.03 | 0.0445 | 0.0460 | +0.0015 | 0.0457 | 0.0471 | +0.0014 |
| topk_hard@0.05 | 0.0406 | 0.0416 | +0.0010 | 0.0416 | 0.0426 | +0.0010 |
| topk_hard@0.1 | 0.0336 | 0.0353 | +0.0017 | 0.0343 | 0.0359 | +0.0017 |
| hard@0.2 | 0.0434 | 0.0436 | +0.0001 | 0.0446 | 0.0446 | +0.0000 |
| hard@0.3 | 0.0447 | 0.0444 | −0.0003 | 0.0459 | 0.0455 | −0.0004 |

vs E13's trace-holdout flip of +0.0023…+0.0062 (5/6 placements). Fold-level
at topk@0.02: 105 wins folds 0/1/3 but **loses fold 2** (0.0391 → 0.0273).
`trace_seen`/`gt_full` orderings unchanged (88 > 105 everywhere, as always).

**Verdicts (flagged, not smoothed):**

1. **The agreement layer's gap advantage is a trace-level effect.** At
   system level it shrinks ~10× to +0.0000…+0.0017 (6/9 placements positive,
   fold-inconsistent at the reference placement). Most of what E9 measured
   was rediscovery of strands next to mapped systems — which may still be
   board-relevant (the hidden set is unknown), but "weak gap evidence", not
   "the 105-ch case". The recommendation is **downgraded**: from
   "re-enable in gap-oriented builds" to "neutral-to-slightly-positive at
   system scale; the E11 file's 10.5k-px 105-ch marginal addition is neither
   helped nor hurt by this instrument".
2. **Absolute gap scores drop ~35–40% from trace- to system-holdout**
   (topk@0.02 masked: 0.0482 vs 0.0780) — a measurement of how much harder
   whole-system discovery is than strand rediscovery, i.e. the true size of
   the generalisation the hidden set demands, insofar as the labels proxy it.
3. The instrument itself is the deliverable that outlasts this session's
   number: every future build claim can now be priced on three populations
   (catalogue / held traces / held systems) with one flag.

### 6. Irregularities flagged this session (guardrail 4)

1. **F13 — parallel arms active DURING this session** (§1): `7GEMSDOE` two
   merges 22:53/22:58Z, `8GEMSDOE` pushed 23:15:58Z with Pages caught
   mid-deploy. Eleven repos, eleven Pages sites (one building), three stubs
   untouched; zero consolidation decisions; human ratification now blocked
   for a sixth session.
2. **wbg1 fell off the visible leaderboard** (§2) — sub-#50 rows are no
   longer publicly trackable from this runner; recorded, not guessed.
3. **Session 3's striping prior corrected by sourced metadata** (§5.1) — the
   "N–S flight-line" basis of E10(a)'s candidate-set suspicion was wrong
   for GeoDAWN; corrected in the library with a verbatim official quote.
4. **Session 5's C-4 cond verdict refined** (§5.3): "kill-if supported"
   became "inconclusive" under the multi-profile rule — the extension showed
   the single centre profile did not generalise, even though no profile
   supports a conductor either.
5. **E9/E13 over-reading risk** (§5.4): the 105-ch gap win was priced in
   session 4/5 recommendations at full strength; the harder instrument says
   it is a trace-level effect. Downgrade recorded in `HYPOTHESES.md`.
6. **`famrank_cond` max-rule materially mislabels** 24/89 cond-strong
   candidates (§5.3) — recommendation recorded; upstream unchanged.
7. **Probe-comment staleness**: `probe_real_footprint.py` part (b) hard-codes
   the legacy guard and calls it "what the code uses" — true only of the
   unpatched upstream; documented in `probes/README.md` rather than silently
   edited (probes are the evidence record).
8. **Engine-side F10 unchanged**: this repo's own suite is **350/350 green**
   this session; the quoted-prose blind spot in `tools/render_check.js` is
   latent, remains the owner's call, and was not touched.
9. Runner facts re-confirmed: `gh api` fine; direct TLS egress still
   blocked; the `probe_sources.py` live pass not run (documented runner
   fact, not a source verdict).

### 7. Three-pass review notes

1. **Implement.** Every number above came from this session's own runs, API
   calls or fetches: all four pins re-hashed; gate 13/13 and the negative
   test **executed** (not cited); E14 run twice (the ±25 px window was
   judged insufficient by the instrument's own output and replaced with
   ±45 px, stated in the probe header); cond probe run once (its arm-B LUT
   re-implements `build_features.py`'s exact bin rule); the system grouping
   was probed at three radii before wiring it in; the E14-SYS run used
   E13's recipe verbatim (80/266 systems = 787 traces / 14,128 px verified
   in the log before interpreting anything) and the session-5 chain/cond
   probe **reproduced session 5's numbers exactly** on this session's
   rebuild (instrument-chain regression check).
2. **Review for bugs/gaps.** The null-empirical-p was added to E14 after
   review showed the p95 bar alone was uninformative on a bimodal null; the
   per-trace system assignment was re-written vectorised after review
   (the naive loop would have scanned the full grid per trace); C-4's
   "2/5 local-max" profiles were re-inspected and reported as MAD-scale
   residual classes rather than conductor evidence; the analytic chance
   coverage was added to both E14 arms so no instrument can quietly sit at
   chance. **Patch verified in a fresh clone** (the session-5 discipline):
   `6GEMSDOE@e2fe3f41` → s4 applies clean → s5 applies clean → s6 applies
   clean → `scripts/experiment.py` byte-identical to the tested state →
   pytest **46/46** → `--system-holdout` present in `--help`. Every number
   quoted in §2–§5 was re-extracted from the committed JSONs and matched.
3. **Re-check vs prompt + rules.** Guardrail 1 executed first (§1); nothing
   created, nothing submitted, nothing consolidated, no GEMSDOE repo
   written to. The rules were not re-quoted this session (session 2's
   verbatim full read stands; no submission was made or planned); the one
   newly cited external document (the GeoDAWN flight specs) is an official
   USGS .gov page fetched verbatim. Brief items 1–7 all executed or
   explicitly scoped; guardrails 2–4 honoured (links on every sourced
   claim; fully autonomous; nine irregularities flagged, including two that
   weakened earlier sessions' findings).

### 8. Carry-forward (next session, in order)

1. **Human ratification — sixth session running, and the arms are now
   merging mid-session.** Canonical repo/site, THE DrivenData registration,
   fate of the eleven sites (three stubs left). F13: parallel arms pushed
   during this very session. Until this lands: no submission, no
   consolidation.
2. **E11 submission decision** (needs 1 + go-ahead): the file exists and
   gates (`gems6_hgb88topk03_hedge105topk02_984e11e4d7.tif`); E14-SYS says
   its 105-ch component is neither helped nor hurt; record the weekly state
   on the confirmed account first (F5).
3. **Apply session-4, session-5 AND session-6 patches in the ratified
   canonical repo only** — all three verified this session (46/46 on the
   fully patched tree in a fresh clone).
4. **famrank_cond ablation**: `agreement-minus-depth-member` config on the
   E9/E13/E14-SYS machinery; the member-attribution measurement (24/89)
   says the max-rule is load-bearing for the wrong reason on a quarter of
   the cond-strong population.
5. **Extend the written-up set past 10** — unchanged queue item; use the
   session-6 status table so the new write-ups inherit the closed stripe
   question and the cond member attribution automatically.
6. **Engine-side latent F10**: quoted-prose blind spot in
   `tools/render_check.js`; suite green; owner's call, unchanged.

---

## Session 5 — 2026-09-26 (UTC, ~21:02–22:30) · branch `arena/01a0df86-masterselflearn`

### 0. Mandate check

Read session 4's carry-forward (§9 of that entry) and the standing brief in
[`SESSION_PROMPT.md`](SESSION_PROMPT.md) **before anything new**, as the brief
requires. Carry-forward order: (1) human ratification, (2) apply the session-4
patch in the ratified repo only, (3) E11 build, (4) E12 stripe pass, (5) E9
under the masked metric (D8) + system holdout, (6) chain test + cond
cross-section for id 872, (7) F10 owner's call. Items 1, 2 and the submission
half of 3 are blocked on a human; everything else was executed. This session's
own output: two runnable probes, one builder script, one metric extension, one
verified patch, and the write-ups below.

### 1. Guardrail check first: one account, one repo (brief guardrail 1)

| Check | Method | Result |
|---|---|---|
| GEMSDOE repo inventory | `gh api search/repositories?q=GEMSDOE+in:name` | `total_count: 11`, all `owner_id 309556078`. Newest `created_at` still 2026-09-25T18:33:56Z — **no new repo**. |
| New site activity since session 4 | `pushed_at` + commit logs | **YES — both stub-turned-sites pushed again**: `8GEMSDOE` merged PR #7 at 20:10:58Z, `7GEMSDOE` merged "Session 4: region-wide 1 m lidar scarp pipeline…" at 20:54:28Z (after session 4's log closed ~20:20Z). F11 pattern continues. |
| Secondary account | `gh api users/kanlerxz87-cyber` | Still 0 public repos (id 312694378). |
| Pages status ×12 | `gh api repos/<r>/pages` | all **built** (11 GEMSDOE + MasterSelfLearn). |
| DrivenData registrations | leaderboard pull (§2) | Unverifiable from public data (F5, unchanged). No registration treated as ours. |

**Verdict, not smoothed:** the brief's "ONE repo" condition is **still
violated** (standing, flagged since session 1, consolidation blocked on human
ratification). No new *repo* or *registration* was created; two *sites* were
pushed to by parallel arms between sessions. This session created no site and
no account, treated no other entrant's registration or score as our data or as
a test arm, and wrote to no GEMSDOE repository (scratch checkout only).

### 2. Fresh leaderboard — pulled ≈21:05Z via research fetch (brief item 7)

Source: <https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/>
(static render through #50).

| Rank | Participant | Score | Subs | Last activity | Note |
|---|---|---|---|---|---|
| #1 | DARD | **0.3049** | 10 | 3d 22h | field high, unchanged across five sessions |
| #5 | joeyfezster | 0.2589 | 12 | 1d 3h | **pay line**, unchanged |
| #24 | **extradr19** | 0.1563 | 2 | 1d 20h | brief row: GEMSDOE |
| #25 | **SDCF9** | 0.1563 | 2 | 3h 11m | brief row: GEMSDOE3 — no score change since session 4's jump |
| #26 | smashi34 | 0.1560 | 1 | 1d 2h | brief row: GEMSDOE2 |
| #41 | smrtdoog5 | 0.1193 | 1 | 1d 3h | brief row: GEMSDOE3 |
| #50 | wbg1 | 0.0830 | 2 | 1d 2h | brief row: GEMSDOE3 |

All five tracked rows exact-match session 4's scores; no movement among them.
New faces above our band since session 4: #22 Scotty77 0.1590, #23 fishnchips
0.1587, #27 hudsonenterprises 0.1543 — other entrants, recorded as field data
only. Gap to pay line: **0.1026** (unchanged). Flagged observation (not ours):
GEMSDOE2's site now runs a published "three submissions, one hypothesis each"
week plan and cites **0.1563** as "the recall-union's board score" — i.e. the
GEMSDOE-family sites attribute the extradr19 row to each other across sites.
Per the brief none of that is our data (F5); recorded as attribution drift.

### 3. Ownership of the three "unconfirmed" sites — resolved again, this session's own calls (brief item 7)

`5GEMSDOE`, `GEMSDOE4`, `6GEMSDOE`: fresh `gh api repos/...` calls at
21:05–21:06Z return `owner_id 309556078` (`buffedlizard55-lab`) on all three —
identical to every other GEMSDOE repo. **They are ours as repositories**
(confirming sessions 1/3/4 with this session's own API calls). All three sites
were **visited this session**: `5GEMSDOE` (same site family as GEMSDOE1, pins
`7f00890a…`, now advertising its "S5-A catalogue hedge" candidate file,
227,507 px, as the next upload), `GEMSDOE4` (pins `237f0063…`, k=3-of-5 union,
now branded "the new-fault-first line" with SGMC-derived proxy labels), and
`6GEMSDOE` (our pipeline's own site: shipped file, 13-check gate table, and
its own "This repository is the one canonical entry" banner — the F4
designation conflict, unratified, unchanged). What remains unverified (F5):
which DrivenData registrations the sites' scores belong to. Per the brief the
GEMSDOE3 trio's rows stay attributed "three different entrants"; none of the
rows is treated as our own.

### 4. Brief items 1–5, re-verified on the freshly rebuilt stack

Environment: fresh scratch checkout `6GEMSDOE@e2fe3f41` + session-4 patch;
Python 3.11.2, numpy 2.4.6, scipy 1.17.1, rasterio 1.4.4, sklearn 1.9.1,
pytest 9.1.1. Bridge reassembled: `training_features.tif` sha256
`4371c82e…` matches `spec.PINS`. Rank tables 110.3 s; feature build
**949.2 s** (valid mask 5,165,840 — byte-consistent with session 4's
rebuild).

| Brief item | Verdict |
|---|---|
| 1. Feature engineering vs the three research priorities | Unchanged from session 3's F-1 map, re-derived from the rebuilt `features_meta.json`: HGM/tilt on mag+grav and curvature/slope-break on DEM are in the shipped 88; the strain×cond×seis cross-reference layer is channels 88–104. E9's gap-population win (session 4) + this session's E13 (§6) are the evidence for gap-oriented builds. |
| 2. Spatially blocked + buffered CV | **Confirmed on the patched tree**: `cv.py` blocks rows/cols, buffer = L∞ square ⊇ L2 kernel disk (D-2 fix), train excludes buffer, `sample_pixels` only samples inside blocked masks, standardisation train-only. **No random pixel split anywhere.** 46/46 tests pass incl. the strengthened kernel-offset assertion. |
| 3. Metric-aware placement intact | **Intact** — `thin_keep`/`skeleton_spaced4`/`topk_mask`/`gated_topk`/`breakeven_posterior` all present and pinned by the suite. The "~4–5 px spacing" premise stays falsified (HE); re-confirming intactness is not a reason to re-open it (SESSION_PROMPT standing note). |
| 4. Generator + `validate_submission.py` | **Re-verified end to end, this session**: shipped file sha `33cec71ff0…` matches pin; gate **13/13 PASS** (EPSG:32611, 100 m, shape/geotransform, values [0,1], NaN-outside only), exit 0. Negative test (one NaN injected inside the footprint): `values-in-0-1` still passes, `NAN-INSIDE-FOOTPRINT` fails, **exit 1**. Hard-gate requirement met. |
| 5. Executive summary / how-to-submit | Checkable claims still accurate (file name/sha/bytes, 155,021 px = 3.00%, model string, 13-check list, minimax table, blank one-entry record — gate re-run this session confirms the live claims). **Flagged, not smoothed:** (a) both guides pre-date the forum-11516 masking rule — their budget/rationale sections do not reflect D7, which now lives only in this library; (b) `EXECUTIVE_SUMMARY.md` §6 ("The single outstanding risk to eligibility") states as fact "**This repository is the designated single entry**" while F4 records that the designation was never verified/ratified and all eleven sites are still up; (c) the "what did NOT work" list still frames the agreement channels on the catalogue proxy only, superseded by E9/E13. All three are upstream-document findings; nothing was written to `6GEMSDOE`. |
| 6. Geological reasoning | Extended — §6 below + `CANDIDATE_GEOLOGY.md` §7 (chain test, cond cross-sections, E12). |
| 7. Field standing + ownership | §2–§3. Mid-pack: best tracked row 0.1563 ≈ #24 of 50 visible; ownership of the three sites resolved: ours. |

### 5. What was executed (carry-forward items 3, 4, 5, 6)

Detail in [`REBUILT_EXPERIMENTS.md`](REBUILT_EXPERIMENTS.md) §5 (session 5)
and [`CANDIDATE_GEOLOGY.md`](CANDIDATE_GEOLOGY.md) §7.

| Carry-forward | Result |
|---|---|
| **3. E11 — masking-aware file** | **BUILT and GATED, not submitted.** `scripts/build_e11_union.py`: file A = shipped ∪ catalogue (192,404 px, 3.72%, gate 13/13 PASS, `gems6_hgb88topk03_hedge_dada4435cd.tif`); file B = A ∪ 105-ch topk@0.02 (202,951 px, 3.93%, PASS, `gems6_hgb88topk03_hedge105topk02_984e11e4d7.tif`). Accounting: catalogue adds 37,383 free px over the shipped field; the 105-ch gap set is 88% already inside the shipped field → marginal addition 10,547 px; file B's **off-mask emission is 141,963 px = 2.75%**, inside the 3% minimax budget on the taxable side while covering 100% of the free zone. **Weekly-submission state recorded first: unverifiable from here (F5)**; one-entry record left blank; no upload (needs ratified account + human go-ahead). |
| **4. E12 — stripe-removal pass** | **EXECUTED; pre-registered criterion NOT MET; instrument defect found.** Two levellers (global column median; y-aware 256-row block medians) on the six raw magnetic bands, E10 test (a) re-run on the same windows: flags 3/4 → 4/4 → 4/4; near-N–S E–W shares never exceed the **non-N–S baseline** (raw 0.445–0.691 vs near-N–S 0.233–0.526), so the ≥0.25 threshold has no contrast (**D-9**); the x-only field's own dominant period is 823 px, not the 10–18 px seen in windows — no column-constant flight-line component at the E10 periods. Consequences: session 4's class finding downgraded to a physical prior; C-4's demotion basis invalidated (status: unresolved on magnetics, not restored); the follow-up is an *alignment* test (crest-position vs trace) plus official flight-line metadata. Signal preservation r ≥ 0.897 everywhere. |
| **5a. E9 under the masked metric (D8 → E13)** | `metric.components(fp_free_mask=)` implemented (FP side of forum 11516; conservative pin = the 60,988 label px; TP/FN deliberately untouched, documented); `experiment.py --fp-mask-px` scores every placement masked **and** unmasked in one run. Re-ran E9 (same folds/seeds/960 held traces/18,116 px — **unmasked numbers reproduce session 4's table to 4 dp**) → `experiments_e13_masked.json`. **Result: the sign flip survives the mask** — 105 ch wins gap 5/6 placements with deltas within ±0.0002 of unmasked; mask lifts gap ≈ +0.002 for both configs (measures the restricted-GT FP wash) and is a no-op on gt_full (implementation validated by the proximity discount). Full tables in `REBUILT_EXPERIMENTS.md` §5.3. |
| **5b. whole-system holdout** | **Still not implemented** (only `--trace-holdout` exists) — carried forward again with an estimate: it needs a grouping key in `candidates.json`/labels that does not exist yet. |
| **6. Chain test + cond cross-section** | **Both executed** (`probes/followup_chain_cond.py`): (i) C-1↔C-6↔C-5 **REFUTED** — lateral line offsets 34.9/56.1 px (3.5/5.6 km) vs a 3 px kernel, 53 km facing gap on C-6→C-1, gravity cross-sections ramp-like on the critical leg (C-6's own kill-if); 3 intermediate candidates on the C-6–C-1 leg, 0 on C-1–C-5. The "one ~17 km Humboldt system" claim — session 4's strongest — is dead. (ii) `cond_surf` cross-sections for **id 872 (C-8)** and id 1618 (C-4): cond_surf global ranks at the trace are 0.984/0.886 (real, and driven by `cond_surf` itself, not `depth_to_base_surf` — checked against `rank_tables.json`), but trace-vs-window is **−0.044σ / −0.108σ with no local high** → **both kill-ifs supported**: the cond pillars are regional basin-fill highs, not trace-local conductors. C-8's case restated on seis/strain/sourced-Holocene; C-4's on grav/seis. |

### 6. Irregularities flagged this session (guardrail 4)

1. **F12** — parallel arms pushed both converted stubs again between sessions:
   `8GEMSDOE` PR #7 merged 20:10:58Z, `7GEMSDOE` "Session 4: region-wide 1 m
   lidar scarp pipeline…" merged 20:54:28Z (after session 4 closed). Eleven
   repos, twelve Pages sites, zero consolidation decisions.
2. **D-9** — E10 test (a)'s threshold has no baseline contrast (3/4 non-N–S
   windows exceed it, up to 0.691). Session 4's class-level finding ("N–S
   class artefact-suspect as a class") was computed without the baseline and
   is **not identified by the instrument** — downgraded to a physical prior,
   not deleted (status change recorded in `HYPOTHESES.md` + §7 of
   `CANDIDATE_GEOLOGY.md`).
3. **Session 4's strongest claim reversed by its own pre-registered test**: the
   C-1↔C-6↔C-5 chain is not continuous (offsets 35–56 px, 53 km gap).
4. **Both cond kill-ifs supported** — the famrank_cond pillars of C-4/C-8 are
   regional, not local; earlier write-ups had them as "confirmation pending".
5. **Cross-site attribution drift**: GEMSDOE2's site cites 0.1563 (the
   extradr19 row per the brief's attribution) as "the recall-union's board
   score" — sibling sites treating one row's score as shared history. Not our
   data per F5; recorded.
6. **E11's economics surprise**: the 105-ch gap surface at topk@0.02 is 88%
   inside the shipped field — the agreement layer's marginal emission is
   10.5k px, much smaller than E9's sign-flip implied the surfaces differ.
   Not an error; a measurement that changes how "different" the gap surface
   is.
7. **F10 status change (engine-side)**: the render-check failure no longer
   reproduces after this session's `cycle --offline` + `publish` — suite is
   350/350 green and `render_check.js` passes all 10 pages. The quoted
   `"undefined MPT-Flawless"` string **still exists** in `data/site.js` and
   `data/claims.jsonl`; it simply no longer renders into any page (claim
   rotation after +484 offline claims). The underlying limitation (checker
   cannot distinguish quoted prose from a template slot) is **latent, not
   fixed** — reported, not claimed as a fix.
8. **Session 4's rank-table hash-drift irregularity (its item 3) is
   confounded.** `rank_tables.json` embeds `built_utc`, so *file* sha256
   differs on every rebuild regardless of content. Measured this session:
   two consecutive builds in the same environment → file hashes differ,
   content hashes (JSON sans `built_utc`) **identical**
   (`3af5745d11470d66…`). So (a) same-environment content bit-stability is
   now upheld, (b) the 64a62c3b→9368d6a9 "drift" session 4 reported was
   never diagnostic of numeric drift, and (c) cross-environment content
   drift remains **untested** (no second environment here). Recorded, not
   smoothed: the original irregularity stands only in its weakened form.
9. Runner facts re-confirmed: `gh api` public endpoints fine; direct TLS
   egress still blocked (live reads via `gh` + research fetch); the
   `probe_sources.py` live pass was therefore not run (its egress failure is
   the documented runner fact, not a source verdict).

### 7. Three-pass review notes

1. **Implement.** Every number in §2–§6 came from this session's own runs,
   API calls, or fetches: gate runs and the negative test re-executed (not
   cited); E11 files built from scratch (train 94 s, full build 272 s); E12
   run three times (twice to add the y-aware leveller, once after a print
   bug); the chain/cond probe run twice (first run crashed on a print — the
   bug was fixed and the whole probe re-run, not patched around); E13 launched
   with the exact E9 recipe and its holdout count (960/18,116) verified in
   the log before interpreting anything.
2. **Review for bugs/gaps.** `metric.components` gained a shape check on the
   mask and a bit-identity assertion for unmasked calls (46/46 tests pass
   with the extension in place). E12's first method was judged insufficient
   *by its own output* and extended rather than reported as a conclusion; the
   (a)-instrument critique was checked against the non-N–S baseline before
   being called D-9. The cond ranks were re-derived from `rank_tables.json`
   to rule out the depth-member alternative before writing "regional".
   **The doc pass itself caught five errors, all fixed before commit:**
   §7.3's r-range (0.976–0.998 → 0.976–0.9997 col) and "block eats 25–40%"
   (actually 42–47%, recomputed from the JSON); the session-log's paraphrase
   of `EXECUTIVE_SUMMARY.md` §6 (now the exact sentence); probes/README's
   `--ids` note (e10-only) and its "falls back to raw bands" claim (the probe
   *omits* the derived surface when absent — raw always runs); and
   `followup_chain_cond.py`'s hardcoded verdict string, which labelled the
   C-1–C-5 leg "C-6's kill-if fires" (strings fixed; numbers never depended
   on it). **And the session-5 patch itself was rebuilt after review caught
   it contaminated**: it had been generated with `git diff` in the scratch
   checkout while session-4's patch was still uncommitted, so its
   `experiment.py` hunks carried session-4's E9 code and it failed
   `git apply --check` on top of the session-4 patch (the exact delivery
   order in the README). Rebuilt against a committed session-4 base; now
   verified in a fresh clone: s4 applies clean, s5 applies clean on top, the
   three files land byte-identical to the tested state, pytest 46/46,
   `--fp-mask-px` present. Every number quoted in §2–§6 and
   `CANDIDATE_GEOLOGY.md` §7 was re-extracted from `e12_results.json` /
   `followup_results.json` / `experiments_e13_masked.json` and matched.
   Caveats left in place:
   single-profile cond sections; centreline-approximation traces; E13's
   effect sizes inherit session 4's E9 caveats plus the D8 asymmetry (FP
   side only).
3. **Re-check vs prompt + rules.** Guardrail 1 executed first (§1); nothing
   created, nothing submitted, nothing consolidated, no GEMSDOE repo written
   to. Rules unchanged from session 2's verbatim full read (3/week §3.4; one
   final §3.5/§3.6.2; US eligibility §1.3) — no rule re-read was needed this
   session because no submission was made or planned from this repo. Brief
   items 1–7 all executed or explicitly scoped (§4); guardrails 2–4 honoured
   (official sources only with links; fully autonomous; nine irregularities
   flagged, none smoothed — including three that reversed session-4 claims).

### 8. Carry-forward (next session, in order)

1. **Human ratification — fifth session running.** Canonical repo/site, THE
   DrivenData registration, fate of the other twelve sites (three stubs left).
   F12: both converted stubs pushed again after session 4 closed. Until this
   lands: no submission, no consolidation.
2. **E11 submission decision** (needs 1 + human go-ahead): the file exists and
   gates (`gems6_hgb88topk03_hedge105topk02_984e11e4d7.tif`); record the
   weekly-submission state *on the confirmed account* first (still F5). One
   slot tests the masking rule's board reading directly.
3. **Apply session-4 + session-5 patches in the ratified canonical repo only**
   (`patches/session4_d1_d2_d3_d5_e9.patch`, `patches/session5_d8_e11_e13.patch`)
   — both verified locally (46/46), neither applied upstream.
4. **Re-run E12 as an alignment test** (crest positions of a 5–30 px
   band-passed x-only field vs trace x-positions, oblique traces as control)
   and fetch official GeoDAWN flight-line metadata (line orientation/spacing)
   from the data documentation — turning the physical prior into a sourced
   fact before any N–S candidate decision rests on it.
5. **Cond follow-ups**: re-check C-8/C-4/C-9 with multi-profile (not
   centreline-single) `cond_surf` sections; decide whether `famrank_cond`
   should drop `depth_to_base_surf`'s non-inverted rank or be reported as two
   sub-signals (the max-rule hides which member fired).
6. **Whole-system holdout** (6GEMSDOE NEXT_STEPS item 6) still unimplemented;
   blocked on a grouping key that does not exist in the data yet.
7. **Engine-side latent F10**: the quoted-prose blind spot in
   `tools/render_check.js` remains; the suite is green only because the claim
   stopped rendering. Fix is the owner's call.

---

## Session 4 — 2026-09-26 (UTC, ~18:30–20:20) · branch `arena/01a0def8-masterselflearn`

### 0. Mandate check

Re-read the session prompt (now embedded in [`SESSION_PROMPT.md`](SESSION_PROMPT.md) —
F6 cured) and session 3's carry-forward (§9 of that entry), in order: E8, E9,
E10, the D-1/D-2/D-3 patches, F6. This session's brief said "focus on genuinely
improving score quality, not just re-confirming the pipeline works" — the work
below is two executed experiments (E8/E9), an executed falsification pass
(E10), and a strategy-changing verified rule find (the scoring mask), with the
format/CV/placement items re-verified only as far as the brief demanded.

### 1. Guardrail check first: one account, one repo (brief guardrail 1)

| Check | Method | Result |
|---|---|---|
| GEMSDOE repo inventory | `gh api search/repositories?q=GEMSDOE+in:name` | `total_count: 11`, all `owner_id 309556078`. **No new repo created** since 2026-09-25T18:33:56Z (`11GEMSDOE`). |
| New live sites since session 3? | `pushed_at` + commit log on the stubs | **YES — `8GEMSDOE` was stood up at 18:10–18:17Z today** (PRs #1/#2: "8GEMSDOE strategy line…", "apex geothermal discovery system, GitHub Pages site, data pipeline, and conformant submission deliverable"), mirroring `7GEMSDOE`'s 17:38–17:43Z stand-up during session 3. `7GEMSDOE` also took a further merge at 18:16–18:17Z. **The stub→site conversion rate is now one per session.** |
| Secondary account | `gh api users/kanlerxz87-cyber` | Still 0 public repos (id 312694378). |
| Pages status ×11 | `gh api repos/<r>/pages` | all **built** (so: 11 repos, 12–13 live sites in effect — `MasterSelfLearn`'s own site plus the GEMSDOE family). |
| DrivenData registrations | fresh leaderboard pull (§4) | Unverifiable from public data (F5, unchanged). No registration treated as ours. |

**Verdict, not smoothed:** the brief's "ONE repo" condition is **still
violated** (standing, flagged since session 1, consolidation blocked on human
ratification). No new *repo* or *registration* was created since session 3, but
a new *site* (`8GEMSDOE`) went live today and parallel arms were pushing at
18:17Z. This session created no site and no account, treated no other entrant's
registration or score as our data or as an experiment arm, and wrote to no
GEMSDOE repository. Flagged as F11 below.

### 2. NEW FINDING F11 — the stubs are being consumed one session at a time

Session 3's F9 (`7GEMSDOE` stood up mid-session) is now a pattern: `8GEMSDOE`
(empty since 2026-09-25) received a complete site + pipeline + "conformant
submission deliverable" at 18:10–18:17Z today, branch `arena/01a0dedb-8gemsdoe`.
Remaining stubs with Pages built: `GEMSDOE9`, `GEMSDOE10`, `11GEMSDOE`. On the
current rate they become live sites within the next three sessions unless a
human stops the arms or ratifies a canonical repo. **This is the escalation of
F8/F9 and remains the item most needing human intervention.**

### 3. Ownership of the three "unconfirmed" sites — RESOLVED again, this session's own calls (brief item 7)

`5GEMSDOE`, `GEMSDOE4`, `6GEMSDOE` — all `owner_id 309556078`
(`buffedlizard55-lab`), identical to every other GEMSDOE repo. They are **ours
as repositories** (confirming session 1 F3 and session 3 §1 with fresh calls).
All three were visited this session: `5GEMSDOE` and `GEMSDOE4` serve the
same site family as `GEMSDOE`/`GEMSDOE2` (in-browser GeoTIFF builder, pinned
artifacts — `5GEMSDOE` pins `7f00890a…` and adds an "S5-A catalogue hedge"
candidate; `GEMSDOE4` pins `237f0063…`, "union k=3 of 5" policy); `6GEMSDOE`
is the pipeline repo (read locally). What remains unverified (F5): which
DrivenData *registrations* the sites' scores belong to. Per the brief, the
GEMSDOE3 trio's rows stay attributed "three different entrants" and none of
the rows is treated as our own.

### 4. Fresh leaderboard — pulled ≈18:55Z via research fetch (brief item 7)

Source: <https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/>
(static render through #50).

| Rank | Participant | Score | Subs | Last activity | Note |
|---|---|---|---|---|---|
| #1 | DARD | **0.3049** | 10 | 3d 19h | field high, unchanged all session |
| #5 | joeyfezster | 0.2589 | 12 | 1d | **pay line**, unchanged |
| #6 | GrigorSargsyan | 0.2504 | 5 | 1d 18h | new near the top since session 3 |
| #9 | hiii12345 | 0.2262 | 6 | 5h 45m | new since session 3 |
| #24 | **extradr19** | 0.1563 | 2 | 1d 18h | brief row: GEMSDOE |
| #25 | **SDCF9** | **0.1563** | **2** | **35 min** | brief row: GEMSDOE3 — **moved 0.1152 → 0.1563 during this session** |
| #26 | smashi34 | 0.1560 | 1 | 1d | brief row: GEMSDOE2 |
| #41 | smrtdoog5 | 0.1193 | 1 | 1d | brief row: GEMSDOE3 |
| #50 | wbg1 | 0.0830 | 2 | 1d | brief row: GEMSDOE3 |

**Flagged, not smoothed:** `SDCF9` — one of the three *different entrants* the
brief attributes to the GEMSDOE3 site — submitted a second file and jumped
+0.0411 within the hour. Session 3's counter discrepancy (extradr19/wbg1 1→2
subs) is now matched by observed activity on SDCF9's row. Per guardrail 1 none
of this is our data; recorded as field movement only. Gap from the best tracked
row to the pay line: **0.1026** (unchanged); field high 0.3049 (unchanged).

### 5. The strategy-changing verified find: the scorer MASKS known faults

Not found by experiment — found by source discipline (guardrail 2). DrivenData
staff reply (chrisk-dd, 2026-09-16) in forum thread 11516
(<https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516>,
fetched this session):

> Pixels corresponding to known USGS/INGENIOUS faults are masked / excluded
> from evaluation, so they do not count towards penalty terms. […] Re-evaluation
> will also mask/exclude the existing USGS/INGENIOUS faults.

Implications recorded in [`FIELD_AND_METRIC.md`](FIELD_AND_METRIC.md) §1b as
D7/D8: catalogue emission is **free** (the 3%-budget minimax analysis
double-counts its cost), our local `metric.py` implements **no mask** (every
local number charges FP the board never charges), and the concrete hedge forms
(5GEMSDOE S5-A, GEMSDOE2 extension arm) become first-class candidates
(HYPOTHESES E11). Mask width unspecified — flagged. The thread is the source
`exposed`'s question and staff's answer; no inference added to the quote.

### 6. What was executed (brief items 1–6)

Detail in [`REBUILT_EXPERIMENTS.md`](REBUILT_EXPERIMENTS.md) and
[`CANDIDATE_GEOLOGY.md`](CANDIDATE_GEOLOGY.md) §5–§6.

| Brief item | Verdict |
|---|---|
| 1. Feature engineering vs the three research priorities | HGM/tilt (mag+grav) and curvature/slope-break (DEM) present and in the shipped model (session 3's F-1 map, unchanged). **The priority-3 cross-reference layer: re-tested on the right instrument (E9) and it WINS there** — +0.0023…+0.0062 on never-seen-trace truth at 5 of 6 placements, while losing on the catalogue proxy exactly as before. The sign flips with the population; the earlier "drop it" decision was made on the one instrument blind to its value. Recommendation: re-enable it in gap-oriented builds. |
| 2. Spatially blocked + buffered CV | Confirmed (no random pixel split anywhere). **D-2 patched** (buffer now L∞ square ⊇ the L2 kernel disk) and **D-4's dead/circular test replaced** with an assertion against `metric.kernel_offsets()` across six block layouts. 46/46 tests pass; probes: 4→0 unexcluded offsets, 100→0 leaks. |
| 3. Metric-aware placement intact | **Intact** — `placement.thin_keep`/`skeleton_spaced4`/`breakeven_posterior` all present and pinned by tests (46/46). The "~4–5 px spacing" premise stays **falsified** (HE, session 3): at matched budget spacing loses 19–42% on our folds. The live placement question this session is instead the masking-driven hedge (E11). |
| 4. Submission generator + `validate_submission.py` | **Re-verified end to end**: shipped file sha `33cec71ff0…` matches its pin, gate **13/13 PASS** incl. `NAN-INSIDE-FOOTPRINT`; negative test (NaN injected inside the footprint) → `values-in-0-1` still passes, `NAN-INSIDE-FOOTPRINT` fails, exit 1. The hard-gate requirement is met. |
| 5. Executive summary / how-to-submit | Re-checked against evidence: file name/sha/bytes (1,652,883), 155,021 px = 3.00% of 5,167,373, values {0,1}, model string, metric formula string (0.8·n_gt + 0.2·FP_w + 0.2·TP_w), 13-check list, minimax-regret table shape, blank one-entry record — all accurate or correctly blank. The one stale rationale (D-3, "multi-scale channels did not improve") lives in `build_submission.py`'s help text and is **fixed in the delivered patch**. New §1b fact (masking) post-dates the guide and is recorded in our library; `6GEMSDOE`'s guide is upstream and untouched. |
| 6. Geological reasoning per candidate | **E10 executed** (striping / strain-inheritance / gravity-sign on raw bands): **C-4 demoted** (striping artefact present — pre-registered rule applied), **C-7 flagship risk dead** (strain earned locally, plane R² 0.29), **C-5 kill hypothesis refuted** (basement-high/shallow), C-2 survived marginally. **Write-ups extended from 6 to 10**, including the rank-6 candidate (id 1991) session 3's "top six" had skipped (selection inconsistency, flagged), plus id 872 (cond rank 0.98) and id 4323 (strain rank 0.98) with live QFFD lookups (Granite Springs Valley **Holocene** segment, Paradise Range <130,000, Bluewing Mountains, Agai Pah Hills). **Class finding: 3/3 near-N–S traces striping-flagged + C-2 marginal — the N–S emission class is artefact-suspect as a class** (E12). New data defect: `geod_shearrate` has holes (C-3/C-4 windows <30 finite px in ±2.5 km). |
| 7. Field standing + ownership | §3–§4. We plausibly sit mid-pack (best tracked row 0.1563 ≈ #24–25 of 50 visible, ~51% of the pay line, ~35% above the blanket-coverage floor 0.0956 on the surrogate scale). Ownership of the three unconfirmed sites **resolved: ours**. |

Also executed: **E8** — full feature rebuild on the D-1/D-5-fixed stack (956.7
s) and the 48/88/105 experiment table at the reference settings. Ordering
**reproduced** (88 > 105 > 48 on every column) — the contamination did not
distort the ranking (the pre-registered "immaterial" outcome, recorded as a
result); magnitudes shifted ≤0.007 downward (the wrong band was mildly
score-inflating). New defect **D-5** found and patched along the way
(`second_derivatives` mixed-derivative halo missed diagonal stencil taps; 4
leaked px per NaN → 0). Verified patch for D-1/D-2/D-3/D-5/D-4 + the E9
machinery delivered at
[`patches/session4_d1_d2_d3_d5_e9.patch`](patches/session4_d1_d2_d3_d5_e9.patch)
against `6GEMSDOE@e2fe3f41` — **not applied upstream**, per carry-forward 5
(apply in the ratified canonical repo, and only there).

### 7. Irregularities flagged this session (guardrail 4)

1. **F11** — `8GEMSDOE` stood up as a new live site at 18:10–18:17Z (§2).
2. **SDCF9's +0.0411 move during the session** on an unverifiable registration (§4) — field data, not ours.
3. **`rank_tables.json` hash drift** from the same pinned raster
   (`64a62c3b…` → `9368d6a9…`, numpy 2.4.6 vs the original builder
   environment): `build_rank_tables.py`'s bit-stability claim is **not** upheld
   across environments. Affects only the 17 agreement channels; recorded in
   `REBUILT_EXPERIMENTS.md` §1 caveats.
4. **Session 3's "top six" skipped rank 6** (id 1991) — selection inconsistency in the previous write-up set; corrected in `CANDIDATE_GEOLOGY.md` §6.
5. **`geod_shearrate` data holes** at C-3/C-4 — famrank_strain there is computed from family `max` over sparse members.
6. **Engine-side, unchanged:** F10's false-positive render-check failure still
   red at HEAD (350 tests, 1 failure — the quoted-English "undefined" case).
   Re-confirmed pre-existing; deliberately not fixed (owner's call).
7. Runner fact re-noted: `gh api user` returns 403 on this integration token
   (public endpoints fine); direct `curl` egress remains TLS-blocked — live
   reads used `gh` and the research fetcher.

### 8. Three-pass review notes

1. **Implement:** every figure in §4–§6 came from this session's own runs,
   API calls or fetches. E8/E9 numbers were diffed programmatically against the
   committed `experiments_agreement.json`, not retyped.
2. **Review for bugs/gaps:** the strengthened buffer test was run against the
   *patched* tree (46/46) and the patches were re-probed after application
   (three probes exit 0). The E9 effect size carries three stated caveats
   (catalogue-character gap population, rank-table drift, restricted-GT FP
   wash) — any of which could shrink +0.003, none of which can manufacture a
   sign flip between two configs on identical machinery. The negative test was
   re-run rather than cited.
3. **Re-check vs prompt + rules:** guardrail 1 first (§1); nothing created,
   nothing submitted, nothing consolidated, no GEMSDOE repo written to. Rules
   re-checked through primary sources only: the masking quote is staff's own
   words on the official forum; eligibility/submission-budget rules unchanged
   from session 2's verbatim read (3/week §3.4, one final §3.5/§3.6.2).
   Brief items 1–7 all executed or explicitly scoped; guardrails 2–4 honoured
   (links on every sourced claim; fully autonomous; seven irregularities
   flagged, none smoothed).

### 9. Carry-forward (next session, in order)

1. **Human ratification — fourth session running, and now with a measured
   cost.** Canonical repo/site, THE DrivenData registration, fate of the other
   twelve sites (three stubs left). F11 shows what the delay costs: another
   full site went live this session.
2. **Apply `patches/session4_d1_d2_d3_d5_e9.patch` in the ratified canonical
   repo** (and only there): D-1/D-2/D-3/D-5 fixes, the real buffer test, and
   the E9 gap-scoring machinery. 46/46 verified on the patched tree.
3. **E11 — build and sanction the masking-aware file**: catalogue union (free
   under the staff-confirmed mask) ∪ gap-priority candidates from the 105-ch
   surface (E9 winner at topk@0.02), i.e. the S5-A hedge form plus the
   agreement layer. One board slot, spent only with the confirmed account and
   human go-ahead. Record the weekly-submission state first.
4. **E12 — stripe-removal pass over `tmi_hg`/`mag_*`** (class finding: 3/3
   N–S traces flagged). Until it exists, re-statement on gravity/strain/seis/
   cond is mandatory for every near-N–S candidate (C-4/C-8/C-10 already are).
5. Re-run the E9 comparison with the **masked** local metric (D8) and, if time
   allows, whole-system holdout (6GEMSDOE NEXT_STEPS item 6 — only the
   diagnostic `--trace-holdout` exists; system grouping is not implemented).
6. Extend the written-up set past 10: the C-1↔C-6↔C-5 chain test and the
   `cond_surf` cross-section for id 872 are the two highest-value measurements
   named in `CANDIDATE_GEOLOGY.md`.
7. Engine-side owner's call, unchanged: F10's render-check false positive.

---

## Session 3 — 2026-09-26 (UTC, ~17:50–18:30) · branch `arena/01a0ded7-masterselflearn`

### 0. Mandate check and what was actually done differently this session

Re-read the session prompt (still not embedded in `README.md` — carry-forward
F6, third session running) and session 2's carry-forward list (§9 of that
entry). This session **did not** re-confirm that the pipeline works. It
installed a real scientific stack, pulled the pipeline read-only, and executed
it — 46/46 of its tests, the submission gate, and three purpose-built probes —
then reported what came back, including two premises in the brief that the
evidence contradicts. Full detail in [`PIPELINE_AUDIT.md`](PIPELINE_AUDIT.md)
and [`CANDIDATE_GEOLOGY.md`](CANDIDATE_GEOLOGY.md).

### 1. Guardrail check first: one account, one repo (brief guardrail 1)

| Check | Method | Result |
|---|---|---|
| GEMSDOE repo inventory | `gh api search/repositories?q=GEMSDOE+in:name` | `total_count: 11`, all `owner_id 309556078` (`buffedlizard55-lab`). No third-party GEMSDOE repo anywhere on GitHub. |
| New repo since session 2? | `created_at` on all 11 | newest is **2026-09-25T18:33:56Z** (`11GEMSDOE`). **No new repo created.** The literal stop trigger is not tripped. |
| Secondary account | — | not re-queried this session (session 2: `kanlerxz87-cyber`, 0 public repos). Carried forward. |
| Pages | `gh api repos/<r>/pages` ×11 | all 11 **built**. |
| DrivenData registrations | fresh leaderboard pull (§4) | unverifiable from public data, unchanged. |

**Ownership of the three sites the brief lists as "unconfirmed" — RESOLVED.**
`5GEMSDOE`, `GEMSDOE4` and `6GEMSDOE` all return `owner_id 309556078`, the same
owner as every other GEMSDOE repo on the account. They are **ours**. This
confirms session 1's F3 independently, with this session's own API calls rather
than by trusting the earlier note. They may therefore be used as our own
history; they still may not be treated as parallel arms of one experiment,
because the DrivenData registrations behind them are a separate question and
remain unverified.

### 2. NEW FINDING F9 — a brand-new site was stood up on our account *during* this session

`7GEMSDOE` was an empty stub (`size: 0`) on 2026-09-25. Today:

| time (UTC) | event |
|---|---|
| 17:38:36 | `c4f4a223` "GEMS v1: verified data + official metric + blind-fault model + format-gated submission + site" |
| 17:39:24 | PR #1 merged (`83da7128`) |
| 17:42:23 | `fd7082de` "Serve the site from the repo root (Pages source is legacy '/' on main)" |
| 17:43:03 | PR #2 merged (`96b0f056`) |
| 17:43:14 | `pushed_at` |

Both PRs are from branch `arena/01a0de9c-7gemsdoe` — another Arena session on
the same account. The repo now holds 18 top-level entries including
`index.html`, `how-to-submit.html`, `metric.html`, `strategy.html`,
`research.html`, `results.html`, `data.html`, `scripts/`, `tests/`,
`knowledge/`, `downloads/`, and a `requirements.txt`. Pages reports **built**.
(GitHub's cached `size` field still read 0 at 17:51Z; the contents API returns
the full tree. The `size` field lags, the tree does not.)

Also today: `5GEMSDOE` PR #5 merged 17:28:42Z (`a36e1aaf` "Session 4:
geothermal prior measured and rejected as an instrument; scarp channel measured
and adopted; S5-D corridor + S5-F flagship ship"), `GEMSDOE4` pushed 06:10:35Z,
`6GEMSDOE` pushed 04:28:31Z.

**This is an escalation of session 2's F8, and it is the item most needing human
intervention.** Session 2 flagged parallel arms *committing* to two existing
repos. This session a previously-empty repo was turned into a **twelfth live
GEMSDOE site**, ~10 minutes before this audit started. No new *repo* was
created, so the literal stop trigger ("no duplicate repos, sites, or
registrations of our own have been created") is arguable — the repo existed, the
site did not. Reading it in the spirit it was written, a new public site is a
new duplicate site. It is flagged, not actioned: this session cannot stop other
runners and created nothing itself.

### 3. The pipeline is not in this repo (correcting a brief premise)

Verified: `find . -name "*.py"` returns 37 files, all `msl/`, `tests/`,
`tools/`. There is no `features.py`, `cv.py`, `metric.py`, `placement.py` or
`validate_submission.py` here. Brief items 1–5 have no artefact in the repo the
brief points at. The pipeline the brief describes exists in **`6GEMSDOE`** and
was audited there, read-only via `gh api`, in a scratch checkout outside this
repository. **Nothing was written to any GEMSDOE repo this session.**

That this is the third session to have to *locate* the pipeline before improving
it is itself the strongest practical argument for the consolidation that is
still blocked on a human decision.

### 4. Fresh leaderboard (brief step 7) — pulled 17:53Z via research fetch

Source: <https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/>

| Rank | Participant | Score | Subs | Last activity | Note |
|---|---|---|---|---|---|
| #1 | DARD | **0.3049** | 10 | 3d 18h | field high unchanged |
| #5 | joeyfezster | 0.2589 | 12 | 1d | **Phase-1 pay line (top 5, $10K each)** |
| #15 | ndavis7 | 0.1797 | 2 | 21h 38m | was 1 sub in session 2 |
| #20 | hall4jm | 0.1642 | 7 | **57m** | actively moving |
| #21 | VictorCallejas | 0.1629 | 1 | 1d 3h | new single-submission entrant above us |
| #24 | **extradr19** | 0.1563 | **2** | 1d 17h | brief row: site `GEMSDOE` |
| #25 | **smashi34** | 0.1560 | 1 | 23h 44m | brief row: site `GEMSDOE2` |
| #40 | **smrtdoog5** | 0.1193 | 1 | 23h 47m | brief row: `GEMSDOE3` nodes |
| #41 | **SDCF9** | 0.1152 | 1 | 23h 35m | brief row: `GEMSDOE3` ridge control |
| #50 | **wbg1** | 0.0830 | **2** | 23h 38m | brief row: `GEMSDOE3` discovery |

**Record discrepancy, flagged not smoothed.** Session 2 logged `extradr19` and
`wbg1` at **1** submission each; the board now reads **2** for both. Every one
of the five tracked rows' last-activity timestamps (23h35m–1d17h ago) predates
session 1's flag merge at 2026-09-26T00:19:13Z, and matches the timestamps
session 2 itself recorded — so **no submission event postdates the flag**. The
count change is therefore either a session-2 misread or a counter that moves
without an activity timestamp. Not resolvable from public data. Recorded as a
discrepancy; the session-2 numbers are not edited, per `AGENTS.md` §3.

Ranks #22→#24 and #39/#40/#49→#40/#41/#50 are other entrants arriving above us,
not our scores moving. All five of our tracked rows are exact-match on score.

### 5. Rules re-verification (brief guardrail 2 — official sources only)

Session 2 cited <https://www.nlr.gov/docs/fy26osti/96647.pdf>. That domain was
worth doubting, so it was checked rather than inherited: it **resolves** and
serves *"Geologic Enhanced Mapping System (GEMS) Prize Official Rules"*,
**SEPTEMBER 2026**, U.S. Department of Energy, governed by 15 U.S.C. § 3719,
redirecting to `docs.nlr.gov`. `nlr.gov` is the sponsor's own domain — the
competition home page gives the organiser contact as `gemsprize@nlr.gov`. The
citation is genuine and official; the earlier sessions were right.

Eligibility (the brief's "for US") re-read verbatim this session: rules §1.3 —
*"Institutions, companies, nonprofit organizations, and individuals based in the
United States (U.S.) are eligible to compete (Section 1.3)"*; and the
competition home page — *"Individual competitors must be U.S. citizens or
permanent residents. Teams must have a captain who is a U.S. citizen or
permanent resident."* Also re-confirmed: *"you may use the provided set of
faults for training purposes. Participants will be evaluated based on their
performance predicting faults contained in a newly labeled, private set of
faults."*

### 6. What was executed (brief steps 1–5) — summary; detail in `PIPELINE_AUDIT.md`

Environment: Python 3.11.2, numpy 2.4.6, scipy 1.17.1, rasterio 1.4.4
(GDAL 3.10.3), pytest 9.1.1 — installed with `--break-system-packages`, all
outside this repo.

| Brief item | Verdict |
|---|---|
| 1. Feature engineering vs the three research priorities | HGM and tilt on magnetics/gravity: **present and in the shipped model**. Curvature and slope-break on the DEM: **present and in the shipped model**. Strain × conductivity × seismicity cross-reference: **built, measured, and excluded** — `--n-channels 88` drops exactly the 17 agreement channels and nothing else (finding **F-1**). The flag's own help text misstates which channels it drops (**D-3**). |
| 2. Spatially blocked, buffered CV | **Yes** — blocked, buffered, no random pixel split, train-only standardisation. But the buffer is an L1 diamond while the kernel is an L2 disk: 4 of 29 in-kernel offsets are not excluded (**D-2**), each fold is one contiguous full-height stripe rather than scattered blocks (**D-2b**), and the test that should catch this is built from the same helper it tests, plus a dead `assert … or True` (**D-4**). |
| 3. Metric-aware ~4–5 px placement | Code **intact** and tested. **Not adopted, and it should not be** — at an exactly matched budget (27,875 vs 27,877 px) thinning loses 19.0% / 28.9% / 42.2% at spacing 3 / 5 / 9, monotone (**HE, falsified**). The brief's premise is wrong and our own data says so. |
| 4. Submission generator + `validate_submission.py` | **Re-verified end to end.** File sha256 matches its pin; gate 13/13 PASS, exit 0. Negative test: one NaN injected inside the footprint → `values-in-0-1` still **passes** while `NAN-INSIDE-FOOTPRINT` **fails** and the script exits 1. It catches the exact platform condition, not a proxy. Fail-closed on a missing or hash-mismatched template. 46/46 tests pass. |
| 5. Executive summary / how-to-submit | **Accurate on every checkable claim**: file name, sha256, byte count, 155,021 px = 3.00%, model string, gate result, the DTI monotonicity argument, and the 3%-vs-5% minimax-regret reasoning all reproduce from the evidence files. The "one-entry record" table is correctly left blank rather than invented. One stale justification (D-3) lives in `build_submission.py`, not in the guide. |
| 6. Geological reasoning per candidate | Written for the top six `new_to_catalogue` candidates with live QFFD lookups — `CANDIDATE_GEOLOGY.md`. |
| 7. Standing vs the field | §4. Our best tracked row is 0.1563 at #24; field high 0.3049; pay line 0.2589. The gap to the pay line is 0.1026. |

**New defect D-1, the largest measured one.** `nan_gaussian`'s NaN guard
invalidates an L1 diamond of radius `ceil(3σ)` while `scipy.ndimage.gaussian_filter`
reaches a *square* of radius `int(4σ+0.5)`. Measured by single-NaN injection:
95 affected-but-still-finite pixels at σ=1.5, 345 at σ=3.0, worst offset 12 px
away. Scaled to the **real official footprint**: **32,461 px (0.63%)** at σ=1.5
and **78,319 px (1.52%)** at σ=3.0 lie in the stencil's reach of a NaN yet are
reported valid — 0.5×–1.3× the size of the entire 60,988-px label set, landing
exactly on the curvature, slope-break and lineament channels the brief
prioritises. Every blocked-CV number in the evidence directory inherits it.

Patches for D-1 and D-2 were written, **applied to a scratch copy, and
verified**: 46/46 tests still pass, unexcluded kernel offsets 4 → 0, the
`n_blocks=6/n_folds=4` leak 100 → 0, affected-but-finite pixels 95 → 0 and
345 → 0. They have **not** been applied to `6GEMSDOE` — nothing was written to
any GEMSDOE repo this session.

### 7. Geological reasoning (brief step 6)

`CANDIDATE_GEOLOGY.md`. Of 1,380 candidate components, only 260 are
`new_to_catalogue` (>300 m) and can score at all. Six were written up in full,
each with a live query this session against the Nevada Bureau of Mines and
Geology Quaternary-fault service
(<https://gisweb.unr.edu/nbmg/rest/services/Geology/Faults/MapServer/0/query>),
whose layer is documented as adapted from NBMG M167 and the **USGS Quaternary
Fault and Fold Database**, and whose records carry
`Source = "USGS Q Fault & Fold Database"`.

Sourced result: five of the six land within a ~4 km window of a named QFFD
structure while being 412–2,059 m from the catalogue's own pixels — the shape
expected if the hidden set is strands, extensions and transverse structures
next to known systems. Two evidence archetypes separate cleanly
(gravity/topography-led with low strain vs strain/seismicity-led), and three
falsification tests dominate: N–S aeromagnetic flight-line striping, smoothed
strain-band inheritance, and gravity *sign* (basement high vs basin fill). None
is answerable from magnitude-ranked `famrank`.

Search-window caveat is stated in the file: the lookups used ±0.05° envelopes
with `returnGeometry=false`, so exact trace-to-trace separation was **not**
computed and is the first follow-up.

### 8. Three-pass review notes

1. **Implement & verify.** Every number above came from a `gh api` call, a
   research fetch, or a command run this session. No figure is inherited from a
   previous session's prose without being re-derived or explicitly labelled
   carry-forward (the secondary account, the GeoDAWN DOI, and the Wesnousky /
   Hreinsdóttir regional citations are so labelled).
2. **Self-review for bugs and gaps.** Two of my own working hypotheses were
   falsified mid-session and the write-up follows the evidence, not the
   hypothesis: the cross-reference channels are *not* simply "missing" (they
   were measured and rejected), and the spacing comparison is *not* confounded
   by budget (it is matched to within 5 px). The buffer defect is latent, not
   live, in every recorded run — stated as such rather than as a live leak.
   Probe exit codes were checked, not assumed.
3. **Re-check against the prompt and the rules.** Guardrail 1 executed first
   (§1) and before any other work; nothing created, nothing submitted, nothing
   consolidated, no GEMSDOE repo written to. Guardrail 2: the rules PDF's domain
   was doubted and verified rather than trusted (§5). Guardrail 3: no manual
   input requested. Guardrail 4: four irregularities flagged (§2, §4, HE's
   instrument conflict, D-3) instead of smoothed over. `AGENTS.md` respected —
   no generated file (`README.md` AUTO:COUNTS, `STATUS.md`, `VERIFICATION.md`,
   `IRREGULARITIES.md`) was hand-edited; no dependency manifest was added to a
   stdlib-only repo; the probes live outside `tests/` so CI does not collect
   them.

### 9. Carry-forward (next session, in order) Which repo is
   canonical, which DrivenData registration is THE account, and the fate of the
   other ten repos. F9 makes this time-critical: a new site went live *during*
   this session, and more will while the question is open.
2. **E8 — rebuild features with D-1 fixed and re-run the experiment table.**
   Until then the feature ranking is unknown, not merely suboptimal. Patch is
   written and verified; it needs a runner with the feature bridge.
3. **E9 — re-test the agreement layer on a catalogue-gap instrument.** This is
   the brief's priority-3 axis and it is currently switched off on the strength
   of an instrument that cannot see its value.
4. **E10 — the three candidate falsification tests** in `CANDIDATE_GEOLOGY.md`
   §4, and extend the written-up set past six of 260.
5. Apply the verified D-1/D-2 patches and the D-3 help-text fix in whichever
   repo is ratified canonical — and only there.
6. Embed the session prompt in the canonical repo's `README.md` (F6).

---

## Session 2 — 2026-09-26 (UTC, ~00:40–01:10) · branch `arena/01a0db24-masterselflearn`

### 0. Mandate check (brief step 1)

Re-read the session prompt (delivered inline; **still not embedded in
`README.md`** — carry-forward of session-1 finding F6). Re-read
`GEMSDOE_OWNERSHIP_FLAG.md` (session 1's output, merged as `c6c8350`,
PR #11, 2026-09-26T00:19:13Z). This session is the mandated re-verification.

### 1. Priority verification — duplicates created since the last session?

| Check | Method | Result |
|---|---|---|
| Repo inventory (created/pushed/pages) | `gh api users/buffedlizard55-lab/repos?sort=created` | **11 GEMSDOE repos, same set as session 1.** No new GEMSDOE repo created since the flag. |
| Global search | `gh api search/repositories?q=GEMSDOE` | `total_count: 11`, all under `buffedlizard55-lab`. No third-party GEMSDOE repos anywhere on GitHub. |
| Secondary account | `gh api users/kanlerxz87-cyber` | Still **0 public repos** (id 312694378). |
| Pages status, all 11 | `gh api repos/<r>/pages` ×11 | All **built**. |
| DrivenData registrations | fresh leaderboard pull (below) | 5 tracked accounts all still 1 submission, scores unchanged. Zero-submission registrations remain **not publicly enumerable** (carry-forward F5.2). |

**Verdict: no NEW duplicate repo/site/registration was *created* since the
last session.** The standing 11-way duplication remains unresolved (that was
already flagged; it is not re-flagged as "new").

### 2. NEW FINDING F8 — parallel arms were actively worked AFTER the stop flag

`gh api repos/buffedlizard55-lab/GEMSDOE4/commits` and `…/pulls` show, after
session 1's flag merged (00:19:13Z):

- `858bcb6e` 00:16:14Z `feat(union): adopt k=2-of-5 new-fault union (+0.0150 on the untouched fold, P=0.957) and close the session-30 queue`
- PR #5 merged 00:18:49Z "adopt k=2-of-5 new-fault union (session 31)"
- two failing-CI log commits 00:21:30/00:21:38Z, then PR #6 merged 00:36:16Z
  "fix(ci): track the deep-ensemble raster the field-selection tests score against"

`GEMSDOE4.pushed_at = 2026-09-26T00:36:16Z`; `6GEMSDOE.pushed_at =
2026-09-26T00:39:45Z` and **again 00:41:09Z** — i.e. **another session was
pushing to 6GEMSDOE during this audit**, pushes ~1–2 min apart. Sessions are
self-numbering ("session 30/31" in commit text).
Per the brief these are **not** adopted as parallel experiment arms; their
numbers are not folded into ours. This session cannot stop other runners —
the finding is flagged for the account holder. §5 carries the decision.

### 3. Fresh leaderboard (brief step 3) — pulled ~00:41Z via research fetch

Source: <https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/>
(static render covers through ≈#50; deeper rows load via JS and are not visible from here).

| Rank | Participant | Score | Subs | Last activity | Note |
|---|---|---|---|---|---|
| #1 | DARD | **0.3049** | 10 | 3d 1h | field high unchanged |
| #2 | alexoktaba | 0.2993 | 13 | 1d | |
| #3 | HardcoreTechGod | 0.2854 | 6 | 1w | |
| #4 | mzoorob | 0.2843 | 15 | 23h 48m | |
| #5 | joeyfezster | 0.2589 | 12 | 7h 1m | **Phase-1 pay line (top 5, $10K each)** |
| #8 | exposed | 0.2340 | 12 | 37m | was 0.2262 in session-1 snapshot → board is moving |
| #14 | doegemsDrivendata | 0.1847 | 5 | 5d 20h | likely organizer baseline account (not verified) |
| #15 | ndavis7 | 0.1797 | 1 | 4h 27m | new single-submission entrant near our band |
| #22 | **extradr19** | 0.1563 | 1 | 1d | brief row: site GEMSDOE |
| #23 | **smashi34** | 0.1560 | 1 | 6h 33m | brief row: site GEMSDOE2 |
| #39 | **smrtdoog5** | 0.1193 | 1 | 6h 36m | brief row: GEMSDOE3 "SUBMIT FIRST" |
| #40 | **SDCF9** | 0.1152 | 1 | 6h 24m | brief row: GEMSDOE3 "CONTROL, UPLOAD LAST" |
| #49 | **wbg1** | 0.0830 | 1 | 6h 27m | brief row: GEMSDOE3 "SUBMIT SECOND" |

Deltas vs session-1 snapshot: five tracked rows **exact-match, still 1
submission each** (no new uploads by them); `exposed` improved 0.2262→0.2340;
four of the five tracked accounts show **login/activity ~2026-09-26T01:2xZ**
(~6½h before the pull) without submitting. No new account in the visible
ranks is identifiable as ours (identifying is impossible from public data —
flagged, not guessed).

### 4. Reference-site study (brief step 3, ownership = ours per session 1 §4)

**`GEMSDOE/docs/index.html`** (fetched this session): the "extradr19" line.
Measured facts it publishes: grid 3,292×3,730 px · EPSG:32611 · 100 m ·
19 feature bands; 60,988 labelled fault pixels = 1.18% of valid area; 716
1-m DEM tiles confirmed against the USGS 3DEP bucket; **blanket-coverage
floor DTI 0.0956** on the supplied labels (the number any model must beat);
adopted artifact `ens12-adopted-floor0.1-w0` = 172,974 px at 1.0, 4,994,399
px at 0.0, 7,111,787 NaN (total 12,279,160 = 3292×3730 ✔); in-browser
GeoTIFF builder with round-trip self-check; 29 verbatim rules quotes
machine-verified against the PDF. Its own stated policy: **thinned skeleton,
width 0 px, floor 0.1**, because its width sweep on the surrogate peaked at
0 px. Its own caveat (quoted): *"every DTI printed elsewhere on this site is
a monitor against the wrong population."* — the surrogate scores against the
catalogue, not the hidden new faults.

**`GEMSDOE3/docs/index.html`** (fetched this session): the "Pindrop" line,
three files at fixed budget **155,021 px = 3.00%** of valid area (consistent
with GEMSDOE's valid-area count ≈5.17M): `pindrop-v4-nodes` (spacing k=4 px,
sha8 f347b70daa), `pindrop-v4-discovery` ("arm trained only on catalogue
pixels the supplied labels do not contain"), `pindrop-v4-ridge` (spacing 1,
dense control). Thesis: *"placement beats mass"* — each truth pixel is
credited from its single best prediction inside the 300 m kernel, so
predictions spaced ≤5 px cover without redundant FP cost; published spacing
4 px (worst-case gap 2 px < R=3 px); 288 candidate policies / 12 budgets
swept. Leaderboard attribution: nodes 0.1193 (`smrtdoog5`), discovery 0.0830
(`wbg1`), ridge 0.1152 (`SDCF9`) — i.e. nodes beat the dense control by
+0.0041 at equal budget.

**Not fetched this session** (spot-checked session 1): `5GEMSDOE/docs/`,
`GEMSDOE4/`; `GEMSDOE2` (its `SUBMISSION_READY.md` documented session 1),
`6GEMSDOE` (mid-push during this audit; fetching would capture a moving
target). Carry-forward, not a gap in ownership — all six verified ours in
session 1 §4.

**Our own live site (brief step 2).** This repo publishes
<https://buffedlizard55-lab.github.io/MasterSelfLearn/> (root-level site, no
`docs/`). Re-read this session: it is the autonomous research-engine briefing
(cycle 27, 24,393 accepted claims, 175 topics, persona table) and contains
**no GEMSDOE methodology** — the brief's "our live site (docs/index.html)"
matches the GEMSDOE-family layout, not this repo's. Finding F6 stands: the
"one canonical GEMSDOE site" is precisely what is undesignated (§5).
Engine-side anomaly noticed while reading: the site claims the owner's public
repo count moved 53 → 1 (claims C024205/C024206), contradicting the live
inventory (~90 repos incl. all 11 GEMSDOE sites) — the engine's owner-corpus
source is evidently reading a stale or filtered snapshot. Engine backlog, not
a GEMS finding; logged here so it is not lost (AGENTS.md §2 forbids
hand-editing the generated register).

### 5. Decision this session

The brief's stop trigger is *"no duplicate repos, sites, or registrations of
OUR OWN have been created since the last session. If one is found, stop and
flag it."* Fresh evidence: **none created**. Therefore the literal stop
trigger is not re-tripped, and the session proceeds with the parts of the
mission that are safe under every reading of the guardrails: fresh
leaderboard/rules verification, reference-site study, deep sourced research,
and this knowledge library — all inside this repo, all read-only everywhere
else. **Still not done (blocked on human ratification, unchanged from session
1):** picking/cementing the one canonical repo+site, consolidating/archiving
the other ten GEMSDOE repos, resolving the one-account posture of the five
DrivenData registrations, and any submission. The post-flag activity in §2 is
flagged as the item needing human intervention most urgently.

### 6. Rules re-verification (full document read this session)

All 7 chunks of <https://www.nlr.gov/docs/fy26osti/96647.pdf> read verbatim
(serves from docs.nlr.gov). Session 1 had left A.3/A.16 unverified; now
closed. Extracts in `FIELD_AND_METRIC.md` §4; highlights: §3.4 *"Each
participating entity (team, organization, or individual prize competitor not
on a team) is allowed to have one final submission; individuals participating
on a team will not be allowed to submit a separate final submission."* A.3:
*"The prize administrator will award a single dollar amount to the designated
primary submitter, whether consisting of a single entity or multiple
entities."* A.2: registration disputes resolve to the *"authorized account
holder of the email address used to register."* A.16: funds clawback if the
prize was made on *"fraudulent or inaccurate information."* §1.3 perjury
certification re-read verbatim.

### 7. Research pass (brief step 4) and knowledge library

Bibliography assembled in `RESEARCH_LIBRARY.md` (19 linked entries across
potential-field edge detection, DEM/LiDAR scarp detection, play-fairway
methodology, official datasets, and the official reference solution). New
hypotheses and re-scored old ones in `HYPOTHESES.md`.

### 8. Three-pass review notes (this session)

1. **Implement & verify:** every table above re-derived from a `gh api` call
   or fetch made this session; leaderboard numbers cross-checked chunk-by-chunk.
2. **Self-review:** owner id re-confirmed implicitly via `gh api` owner scope
   on every repo call; credentials never used/printed; the "activity ~6½h ago"
   rows are leaderboard "last activity" fields, not submission events — kept
   distinct; GEMSDOE4's "+0.0150" is a surrogate claim in a commit message,
   **not** a leaderboard fact — labelled as such; `doegemsDrivendata` is
   *suspected* organizer account, unverified — labelled as such.
3. **Prompt/rules re-check:** brief steps 1–6 all executed or explicitly
   blocked-with-reason; guardrails honoured (nothing created, nothing
   submitted, nothing consolidated, no site edited); metric constants
   (α=0.2, β=0.8, R=300 m) re-read from page 967 this session.

### 8b. Engine-side finding F10 — the repo's own CI is red at HEAD, and it is a false positive

Found while running this repo's own check suite (`AGENTS.md` §10), not while
editing GEMS content. Recorded because the next session will hit it too.

```
$ python3 -m msl.cli selftest          -> PASS
$ python3 -m unittest discover -s tests -> Ran 350 tests, FAILED (failures=1)
FAIL: test_every_page_renders (test_site.RenderCheck)
BADVAL projects.html: {"undefined":1}
  e.g. "...the >=$600 wire-only payment rail (IR-29) and the undefined
        MPT-Flawless names (IR-36) were re-confirmed..."
```

**Verified pre-existing**: `git stash push -u` back to HEAD `8453777` and
re-run → same single failure. It is not caused by this session's changes.

**Root cause, diagnosed rather than guessed.** `tools/render_check.js:111`
scans rendered page text with
`/\b(NaN|undefined|Infinity|\[object Object\])\b/g` to catch unrendered JS
template slots. Here the token is **not** a template leak: it is the English
word "undefined" inside a *captured* description string — claim `C023901`,
`field = mastersite.project[tradingviewtheleap].record`, whose `value.description`
quotes another repository's own README audit banner verbatim, and that banner
says "the undefined MPT-Flawless names (IR-36)". The capture is correct; the
checker cannot tell quoted evidence prose from an unrendered slot.

**Deliberately not fixed here.** Narrowing the checker would be editing a
validation gate in the same commit as unrelated work, and the right fix is a
judgement about the engine's contract — sanitise captured prose, or teach the
checker to scope its match to template output rather than to quoted evidence.
That is the owner's call, and `AGENTS.md` §2 requires the generator to change
rather than the output. Left red, reported, and reproducible.

### 9. Carry-forward (next session, in order)

1. **Human ratification, now urgent for a third session running.**

1. Human ratification still outstanding: canonical repo/site, which
   DrivenData registration is THE account, fate of the other ten repos
   (five stubs first). Until then: no consolidation, no submission.
2. Stop/contain the parallel arms still running on `GEMSDOE4` / `6GEMSDOE`
   (§2) — only the account holder can.
3. Obtain competition data access through the confirmed account so model
   experiments can run (this repo currently holds none).
4. Top open experiments per `HYPOTHESES.md`: E1 1-m-DEM scarp template
   mining outside the catalogue, E2 recall-oriented emission A/B vs skeleton,
   E3 magnetic-edge candidates on GeoDAWN bands.
5. Embed this session prompt in the canonical repo's README (F6) once the
   canonical repo is ratified.

---

## Session 1 — 2026-09-26 (earlier, UTC) · branch `arena/01a0db08-masterselflearn`

**Output:** `../GEMSDOE_OWNERSHIP_FLAG.md` (merged via PR #11 at
`c6c8350`, 2026-09-26T00:19:13Z). **Mission was stopped that session.**
Findings, abbreviated (full text and repro in the flag file):

- **F1:** 11 GEMSDOE repos on our account (id 309556078), all with Pages
  built: `GEMSDOE`, `GEMSDOE2`, `GEMSDOE3`, `GEMSDOE4`, `5GEMSDOE`,
  `6GEMSDOE`, `7GEMSDOE`, `8GEMSDOE`, `GEMSDOE9`, `GEMSDOE10`, `11GEMSDOE`.
- **F2:** five of them (7/8/9/10/11) were created in a scripted burst on
  2026-09-25 18:22–18:33Z, after the brief's inventory froze — the stop
  trigger that session.
- **F3:** the three "unconfirmed-ownership" sites are **OURS** (owner id
  309556078 on each backing repo).
- **F4:** five repos each claim operational primacy (three-way designation
  conflict with the brief pointing at MasterSelfLearn).
- **F5:** DrivenData registration ownership unverifiable from public data;
  five tracked accounts, 1 submission each, scores 0.1563/0.1560/0.1193/
  0.1152/0.0830; field high 0.3049 unchanged.
- **F6:** the session prompt is not in this repo's README and there is no
  GEMSDOE knowledge library here (defect now cured by this directory).
