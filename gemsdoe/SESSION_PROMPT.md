# The session prompt — embedded verbatim (finding F6)

Finding F6 (session 1): the recurring session prompt was never stored in the
repository, so every session had to re-derive its mandate from a transient
message. The canonical home is the ratified repo's `README.md`; until
ratification (still outstanding — see `SESSION_LOG.md` session 3 §9.1) it lives
here. **Session 4's prompt, verbatim** (the first to carry the full standing
brief; earlier sessions' prompts are summarised in `SESSION_LOG.md`):

---

> Review this repo and our one live GEMSDOE site. Pick up from where the previous
> session's "next steps" left off — read them before starting anything new.
>
> Reference sites (visit for context; confirm ownership before treating any as
> our own history):
>
>   - GEMSDOE1 — https://buffedlizard55-lab.github.io/GEMSDOE/docs/index.html — 0.1563
>   - GEMSDOE2 — https://buffedlizard55-lab.github.io/GEMSDOE2/docs/index.html — 0.1560
>   - GEMSDOE3 — https://buffedlizard55-lab.github.io/GEMSDOE3/docs/index.html — 0.1193 / 0.0830 / 0.1152
>     (three different entrants submitting to the same GEMSDOE3 site)
>
>   - Ownership unconfirmed — check before using as our own data:
>     - https://buffedlizard55-lab.github.io/5GEMSDOE/docs/index.html
>     - https://buffedlizard55-lab.github.io/GEMSDOE4/
>     - https://buffedlizard55-lab.github.io/6GEMSDOE/
>
>   - Field high (last checked): 0.3049
>   - Live leaderboard: https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/
>
> This session, focus on genuinely improving score quality, not just re-confirming
> the pipeline works:
>
> 1. Study our current feature engineering against the research priorities:
>    horizontal gradient magnitude / tilt derivative on the magnetic and gravity
>    layers, curvature and slope-break analysis on the DEM, and cross-referencing
>    strain-rate, conductivity anomalies, and earthquake density.
> 2. Confirm cross-validation is spatially-blocked and buffered, never a random
>    pixel split.
> 3. Confirm the metric-aware placement step (~4-5 pixel spacing) is intact.
> 4. Re-verify the submission generator still passes every format check
>    (EPSG:32611, 100m resolution, correct shape/geotransform, values in [0,1],
>    NaN only outside the valid footprint), with `validate_submission.py`
>    hard-gating on NaN-inside-footprint.
> 5. Check the executive summary / "how to submit" page is still accurate.
> 6. For any candidate fault the model flags, write down the geological
>    reasoning behind it, not just the pixel mask.
> 7. Visit the reference sites above and sanity-check where we plausibly sit
>    against the field. Explicitly resolve ownership of the three unconfirmed
>    sites this session if it hasn't been resolved yet, and report the finding.
>
> Guardrails carried over every session:
>
> - Verify we are still operating as ONE DrivenData account and ONE repo, for
>   US, before doing anything else. Do not create a second site or account of
>   our own. Do not treat another entrant's registration or score as our own
>   data or as a test arm of our own experiment.
> - No hallucinations — official, verified sources only, links included.
> - Work line by line, autonomously, no manual input required.
> - Flag irregularities rather than smoothing over them.
>
> Run this in three passes (implement → review for bugs/gaps → re-check against
> this prompt and the competition rules), then end with: what changed, what's
> still unverified, what's blocking further progress, and what to do first next
> session. Open a PR with the changes and merge to main once verified.

---

Standing-note for future sessions: item 3's "~4-5 pixel spacing" premise was
falsified at equal budget (session 3, hypothesis HE) and the spacing code is
intact but deliberately unadopted; see `PIPELINE_AUDIT.md` §3 and
`REBUILT_EXPERIMENTS.md` for the live status of that question. Re-confirming
"the placement step is intact" is not a reason to re-open the spacing decision
without new evidence from the hidden population.
