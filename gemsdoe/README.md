# gemsdoe/ — the GEMS Prize knowledge library

The expanding, self-improving body of expertise for the DOE GEMS Prize
(DrivenData competition 306): predicting geologic faults **missing from the
training catalogue** in the GeoDAWN region of Nevada/California.

This directory is the institutional memory the session brief requires ("building
a growing knowledge library inside the repo, not just a final submission").
It is append-friendly: each session adds to `SESSION_LOG.md` and
`HYPOTHESES.md`; findings that stop holding up get a status change, never a
silent deletion.

## Index

| File | Contents |
|---|---|
| [`SESSION_LOG.md`](SESSION_LOG.md) | Per-session audit + work log. Session 1 = the 2026-09-26 stop-the-line ownership flag; session 2 = the re-audit, leaderboard pull, site study, research pass; session 3 = the executed pipeline audit; session 4 = score-quality work: D-1/D-2/D-5 patched and re-measured, the E8 rebuild + E9 gap instrument executed, E10 falsification tests run; session 5 = E11 masking-aware file built + gated, E12 stripe levelling tested (criterion not met, instrument defect D-9), D8 masked metric implemented and E9 re-run under it, the C-1↔C-6↔C-5 chain test refuted and both cond kill-ifs supported; **session 6 = sourced GeoDAWN flight geometry (it corrects the session-3 striping prior), E14 tie-stripe alignment executed (stripe question closed: 0/4 aligned), cond pillars re-measured at 5 profiles/trace + famrank_cond member attribution (24/89 depth-carried), and the whole-system holdout instrument built (`--system-holdout`) with E9 re-priced on it (the 105-ch gap win does NOT transfer at system scale)**. |
| [`PIPELINE_AUDIT.md`](PIPELINE_AUDIT.md) | **Start here for engineering.** Session 3's audit of the live pipeline against brief items 1–5, produced by *running* the code: 46/46 tests, a re-verified 13-check submission gate with a negative test, and four measured defects (D-1…D-4) with verified patches. |
| [`REBUILT_EXPERIMENTS.md`](REBUILT_EXPERIMENTS.md) | Session 4 results (the E8 experiment table re-run on a D-1/D-5-fixed feature stack — ordering reproduced, 88 > 105 > 48; E9, the agreement layer re-tested on the catalogue-gap instrument) **plus the session-5 section**: D8 implemented, E11 built/gated, E9 re-run under the mask. |
| [`CANDIDATE_GEOLOGY.md`](CANDIDATE_GEOLOGY.md) | Brief item 6: the geological reasoning behind the flagged traces, with per-candidate lookups against the USGS QFFD-sourced Nevada fault service. Ten written up in full, the three falsification tests **executed** (§5–§6), one candidate demoted (C-4), the class-level N–S striping finding (now downgraded to a physical prior after D-9), and **§7 (session 5)**: the C-1↔C-6↔C-5 chain test **refuted**, the cond cross-sections for C-8/C-4, E12/D-9, and a status-change table for C-2/C-4/C-6/C-8. |
| [`probes/`](probes/) | The runnable scripts that produced the audit's measurements, plus `probe_crossder_halo.py` (defect D-5), `e10_falsification.py` (tests (a)–(c) on raw bands), `e12_stripe_removal.py` (E12 + D-9) and `followup_chain_cond.py` (chain test, cond cross-sections). Not part of this repo's stdlib test suite; see its README. |
| [`patches/session4_d1_d2_d3_d5_e9.patch`](patches/session4_d1_d2_d3_d5_e9.patch) | The verified unified diff against `6GEMSDOE@e2fe3f41` (D-1 NaN-guard square reach, D-2 L∞ buffer, D-3 help text, D-5 cross-derivative halo, D-4 test rewrite, E9 gap scoring). **Not applied upstream** — apply in whichever repo is ratified canonical, and only there. |
| [`patches/session5_d8_e11_e13.patch`](patches/session5_d8_e11_e13.patch) | Session 5's additions to the same base: `metric.components(fp_free_mask=)` (D8), `experiment.py --fp-mask-px` (masked + unmasked aggregates in one run), `scripts/build_e11_union.py` (the E11 file builder). **Not applied upstream**, same rule. |
| [`patches/session6_system_holdout.patch`](patches/session6_system_holdout.patch) | Session 6: `experiment.py --system-holdout/--system-link-px` — the grouping key (8-connected components of the 10 px-dilated catalogue; 266 systems) and whole-system holdout scoring reusing the trace_gap/trace_seen/masked aggregates. **Applies clean on session-4+5 patches; verified in a fresh clone, 46/46 tests. Not applied upstream**, same rule. |
| [`evidence/session6/`](evidence/session6/) | The raw JSON outputs behind every session-6 number: `e14_results.json` (E14), `cond6_results.json` (multi-profile + member attribution), `followup_results_s6.json` (chain/cond reproduction on this rebuild), `experiments_e14sys.json` (88-vs-105 under whole-system holdout). |
| [`SESSION_PROMPT.md`](SESSION_PROMPT.md) | The recurring session prompt, embedded verbatim (finding F6). Moves to the canonical repo's `README.md` once ratified. |
| [`FIELD_AND_METRIC.md`](FIELD_AND_METRIC.md) | The verified scoring metric (distance-weighted Tversky, α=0.2/β=0.8, 300 m kernel), its strategic consequences, and the fresh 2026-09-26 leaderboard state vs our tracked rows. **§1b adds the official staff clarification that known-fault pixels are masked from scoring** (forum 11516) — read it before any budget or placement decision. |
| [`RESEARCH_LIBRARY.md`](RESEARCH_LIBRARY.md) | Annotated, linked bibliography: potential-field edge detection, DEM/LiDAR scarp detection, geothermal play-fairway methodology, official datasets. Every entry names where it came from. |
| [`HYPOTHESES.md`](HYPOTHESES.md) | The hypothesis register: what was tested (and how it was scored), what was falsified, and the open ranked queue of next angles. Session 3 falsified HE (4–5 px spacing, at matched budget) and HG (the `--n-channels` rationale); session 4 decided E10 and added HI (masking), E11 (catalogue hedge), E12 (stripe removal); session 5 tested D8/E11/E12/E13 (E11 built + gated, E12 criterion not met with defect D-9, E13 flip survives the mask) and added the session-5 additions table (D-9, chain refuted, cond kill-ifs supported). |
| [`../GEMSDOE_OWNERSHIP_FLAG.md`](../GEMSDOE_OWNERSHIP_FLAG.md) | The standing ownership/one-repo audit (session 1) + addendum (session 2). Read before touching anything submission-related. |

## Standing guardrails (from the session brief — non-negotiable)

1. **One repo, one account, one submission per prize round, for us.** Never
   create a new GEMSDOE repo, site, or DrivenData registration. Eleven
   GEMSDOE repos currently exist on our GitHub account — that violation is
   flagged in `../GEMSDOE_OWNERSHIP_FLAG.md` and consolidation awaits a human
   decision; none of them may be treated as a parallel experiment arm here.
2. **No hallucinations.** Every claim links to an official, verifiable source,
   or is labelled as our own derivation/interpretation. Gaps are printed, not
   filled.
3. **The target is faults MISSING from the training catalogue.** Both prize
   rounds score the experts' new-fault set (rules §1.1; competition page 967).
   Reproducing the USGS/INGENIOUS catalogue is only worth credit where the
   experts' new labels happen to coincide with it.
4. **No submissions from this repo without human ratification** of which
   DrivenData registration is the ONE account and which repo is canonical.

## Current state (2026-09-26, session 6)

- Ownership violation **open, sixth session**: 11 GEMSDOE repos on our
  account, all with Pages sites. No new repo since session 2 (newest
  `created_at` 2026-09-25T18:33:56Z); **parallel arms were active DURING this
  session** (`7GEMSDOE` merged 22:53/22:58Z, `8GEMSDOE` pushed 23:15:58Z with
  Pages building). Consolidation still blocked on human ratification.
- **The three "unconfirmed ownership" sites are ours** — re-verified session 6
  with fresh API calls; all six reference sites visited again and unchanged
  (6GEMSDOE's F4 canonical-entry conflict stands upstream). The
  *registrations* behind the leaderboard rows remain unverifiable (F5);
  `wbg1` fell off the publicly visible board (static render ends at #50).
- **The pipeline is not in this repo.** It lives in `6GEMSDOE`
  (`src/gems/*.py`), executed read-only in a scratch checkout: session 6
  rebuilt the stack (1,031.8 s, valid mask byte-consistent with sessions 4/5),
  re-ran the gate (13/13 + negative test), reproduced session 5's chain/cond
  probe exactly, and ran E14/E14-SYS — see
  [`SESSION_LOG.md`](SESSION_LOG.md) session 6.
- **The stripe question is CLOSED for the written-up set.** The GeoDAWN
  flight geometry is now sourced (USGS DR 10.5066/P93LGLVQ): flight lines
  E–W at 200/400 m, tie lines N–S at 2000/4000 m — session 3's "N–S =
  flight-line" prior was wrong for GeoDAWN. E14 (tie-scale crest alignment,
  trace self-masked, 300-draw nulls): **0/4 near-N–S traces are stripe-locked**
  (`CANDIDATE_GEOLOGY.md` §8; `probes/e14_alignment.py`).
- **Cond pillars re-measured**: C-8/C-9 kill-ifs stand on 5 profiles/trace;
  C-4 refined to "inconclusive" (2/5 noise-level local-max, never a raw
  high). **famrank_cond member attribution: 24 of 89 high-cond candidates
  (27%) are carried by `depth_to_base_surf` alone** — sediment thickness,
  not conductivity; recommend reporting two sub-signals (§8.3).
- **Whole-system holdout now exists** (`--system-holdout`, grouping = 266
  systems at 10 px link radius; session-6 patch, verified, not upstream).
  E9 re-priced on it: the 105-ch gap win shrinks ~10× to +0.0000…+0.0017
  (fold-inconsistent) — a **trace-level effect**, see
  [`REBUILT_EXPERIMENTS.md`](REBUILT_EXPERIMENTS.md) §6. Recommendation
  downgraded accordingly in [`HYPOTHESES.md`](HYPOTHESES.md).
- **E11 file exists, gate-passing, unsubmitted**: `gems6_hgb88topk03_hedge105topk02_984e11e4d7.tif`
  (202,951 px; all 60,988 catalogue px free under the staff mask; off-mask
  2.75%). E14-SYS says its 105-ch component is neither helped nor hurt;
  submission still blocked on ratification + human go-ahead.
- Best score attributable to our tracked rows: **0.1563** (`extradr19`, #24;
  `SDCF9` also 0.1563 at #25 — other registrations, per the brief not our
  data). Field high **0.3049**, pay line **0.2589**, unchanged six sessions.
- **The brief's "~4–5 px spacing" placement premise stays falsified** (HE) and
  the spacing machinery is intact-but-unadopted.
- This repo holds **no competition data files** (they live in the scratch
  checkout and the `6GEMSDOE` bridge). No GEMSDOE repo was written to this
  session.
