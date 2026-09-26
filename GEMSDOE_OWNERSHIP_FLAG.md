# ⛔ GEMSDOE OWNERSHIP FLAG — mission stopped, 2026-09-26

**Status: STOP-THE-LINE.** The one-account / one-repo / one-site assumption is
**violated**. Per the session brief — *"If one is found, stop and flag it; do not
treat it as a parallel experiment"* — the research mission (site study, method
derivation, literature review, hypothesis work) was **not started** this session.
This file is the flag and the audit behind it.

Every claim below was produced by a read-only command or a research-tool fetch
**this session (2026-09-26 UTC)**. Nothing is carried over from memory. The
reproduction commands are in §8. Direct `curl` egress from this runner is blocked
(TLS cut before any HTTP status; all `curl` probes returned `000`) — that is a
**runner fact, not a claim that any site is down**; live reads used the GitHub
API (`gh`) and the research fetch tool instead.

---

## 1. The rule being enforced

From the session brief (verbatim):

> "This is our ONE and ONLY GEMSDOE project, tied to ONE DrivenData account. …
> no duplicate repos, sites, or registrations of OUR OWN have been created since
> the last session. If one is found, stop and flag it; do not treat it as a
> parallel experiment."
>
> "ONE account, ONE repo, ONE chosen final submission per prize round, for US.
> Never create a second site or registration of our own."

Grounded in the official rules (both re-fetched and read this session —
<https://www.nlr.gov/docs/fy26osti/96647.pdf> (PDF), which serves from
<https://docs.nlr.gov/docs/fy26osti/96647.pdf>, and
<https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/>):

| Constraint | Source | Wording (as read this session) |
|---|---|---|
| A single entry | rules §1.1 | "Participants will submit a single entry, which will be evaluated in two prize phases using a distance-weighted Tversky index." |
| 3 submissions/week | rules §3.2 | "You can make multiple submissions, subject to the limits specified on the competition website (three submissions per week)." |
| One chosen submission, blind | competition page 967 | "Competitors must choose a **single** submission for scoring across both rounds before the deadline, without knowing their private test set performance." |
| Both rounds score NEW faults | rules §1.1 | "In Phase 1, submissions will be evaluated against a privately withheld subset of the original new fault dataset compiled by expert reviewers." |
| Prizes | rules §1.1 / page 967 | Phase 1 $50,000 split equally among top five ($10K each); Phase 2 $250,000 as $100K/$70K/$40K/$25K/$15K |
| Generative-AI disclosure | rules §3.2 | required in the narrative; the competitor is responsible for accuracy/authenticity of AI-assisted content |
| Eligibility + certification | rules §1.3 | U.S. citizen/permanent-resident requirement (team captain for teams); certification "under penalty of perjury … 18 U.S.C. § 1001 and § 287 …" |
| Single-entity award | rules A.3 (section title read in the PDF contents) | "Teams and Single-Entity Awards" — full text not yet read verbatim this session (see §11) |

Note: `buffedlizard55-lab/6GEMSDOE/ACCOUNT_STATUS.md` (a file in one of the
flagged repos, written 2026-09-25) quotes further verbatim strings (rules §3.4,
§3.5, §3.6.2, A.12, A.16). Those exact strings are **attributed to that file**,
not re-verified here; the equivalent constraints above were verified against the
primary sources this session.

## 2. Finding F1 — eleven GEMSDOE repos + eleven live sites on OUR account

GitHub user **`buffedlizard55-lab`** (id **309556078**, created 2026-07-27) —
the same account that owns this repository — holds **11** repositories named
after this one competition. GitHub Pages is enabled and **`status: "built"`** on
all 11 (read via `gh api repos/<repo>/pages` this session):

| # | Repository | Created (UTC) | Last push (UTC) | Contents (top level, this session) | Site |
|---|---|---|---|---|---|
| 1 | `GEMSDOE` | 2026-09-12T18:46:56Z | 2026-09-24T23:07:17Z | full project: `docs/`, `data/`, `scripts/`, `src/`, review files | <https://buffedlizard55-lab.github.io/GEMSDOE/> |
| 2 | `GEMSDOE2` | 2026-09-25T00:24:39Z | 2026-09-25T17:32:05Z | full project + `SUBMISSION_READY.md` | <https://buffedlizard55-lab.github.io/GEMSDOE2/> |
| 3 | `GEMSDOE3` | 2026-09-25T00:41:42Z | 2026-09-25T17:36:01Z | "Pindrop" project: `docs/`, `AGENTS.md`, `THIRD_PARTY.md`, `NEXT_STEPS.md` | <https://buffedlizard55-lab.github.io/GEMSDOE3/> |
| 4 | `GEMSDOE4` | 2026-09-25T18:16:35Z | 2026-09-25T21:03:01Z | full project, root-level site, "new-fault-first line" | <https://buffedlizard55-lab.github.io/GEMSDOE4/> |
| 5 | `5GEMSDOE` | 2026-09-25T18:21:09Z | 2026-09-25T23:44:33Z | full project + `PROJECT_BRIEF.md`, `docs/` | <https://buffedlizard55-lab.github.io/5GEMSDOE/> |
| 6 | `6GEMSDOE` | 2026-09-25T18:21:36Z | 2026-09-25T22:07:26Z | docs suite + `ACCOUNT_STATUS.md` ("the designated single entry") | <https://buffedlizard55-lab.github.io/6GEMSDOE/> |
| 7 | `7GEMSDOE` | **2026-09-25T18:22:01Z** | 2026-09-25T18:22:03Z | `README.md` stub ("# 7GEMSDOE") only | <https://buffedlizard55-lab.github.io/7GEMSDOE/> |
| 8 | `8GEMSDOE` | **2026-09-25T18:22:21Z** | 2026-09-25T18:22:23Z | `README.md` stub only | <https://buffedlizard55-lab.github.io/8GEMSDOE/> |
| 9 | `GEMSDOE9` | **2026-09-25T18:31:01Z** | 2026-09-25T18:31:02Z | `README.md` stub only | <https://buffedlizard55-lab.github.io/GEMSDOE9/> |
| 10 | `GEMSDOE10` | **2026-09-25T18:31:23Z** | 2026-09-25T18:31:25Z | `README.md` stub only | <https://buffedlizard55-lab.github.io/GEMSDOE10/> |
| 11 | `11GEMSDOE` | **2026-09-25T18:33:56Z** | 2026-09-25T18:33:58Z | `README.md` stub only | <https://buffedlizard55-lab.github.io/11GEMSDOE/> |

Disk-size readings from the API moved between endpoints during the audit
(5GEMSDOE reported 404,531 then 460,609 KB; 6GEMSDOE 3,194 KB vs "0" in its own
2026-09-25 table) — GitHub's `size` field is approximate and the repos were being
pushed to during the audit window. Sizes are therefore omitted above; creation
times, push times, contents and Pages status were stable and are the evidence.

Global GitHub search for "GEMSDOE" (`GET /search/repositories?q=GEMSDOE`)
returned `total_count: 11` — **exactly these 11, all under `buffedlizard55-lab`**.
There are no third-party GEMSDOE repos on GitHub, and the secondary account
noted in our own catalog (`kanlerxz87-cyber`, id 312694378) has **0** public
repos.

## 3. Finding F2 — the trigger: five duplicates created since the last session's inventory

The session brief's inventory knows **six** sites (GEMSDOE, GEMSDOE2, GEMSDOE3,
5GEMSDOE, GEMSDOE4, 6GEMSDOE). For the brief to list `6GEMSDOE`, the inventory
frosted no earlier than 2026-09-25T18:21:36Z. **Five further repo+site
duplicates of our own were created in the minutes after that and are absent from
the inventory:**

| Repository | Created (UTC) | Interval since previous | State |
|---|---|---|---|
| `7GEMSDOE` | 2026-09-25T18:22:01Z | +25 s after `6GEMSDOE` | empty stub, Pages built |
| `8GEMSDOE` | 2026-09-25T18:22:21Z | +20 s | empty stub, Pages built |
| `GEMSDOE9` | 2026-09-25T18:31:01Z | +8 m 40 s | empty stub, Pages built |
| `GEMSDOE10` | 2026-09-25T18:31:23Z | +22 s | empty stub, Pages built |
| `11GEMSDOE` | 2026-09-25T18:33:56Z | +2 m 33 s | empty stub, Pages built |

Creation at 20–25 second intervals is a scripted-burst signature (an
observation about the timestamps; the GitHub API does not expose which token,
user session, or automation created them — **author not established**).

**This meets the brief's stop condition.** These are duplicate repos **and**
duplicate sites of ours (Pages is built on all five), created after the last
inventory. Per the brief they are **flagged, not adopted as parallel experiment
arms**. Note the broader context in §2: even the six known repos are a standing
one-repo/one-site violation, and ten of the eleven were created on a single day
(2026-09-25) in three bursts (00:24–00:41, 18:16–18:21, 18:22–18:33).

## 4. Finding F3 — the three "unconfirmed-ownership" sites are OURS

The brief required this determination explicitly before drawing conclusions
from them. Determined this session, twice (initial + pass-2 re-check), via
`gh api repos/<repo>` returning `owner.login=buffedlizard55-lab`,
`owner.id=309556078` for each backing repository:

| Brief entry | URL | Backing repo | Owner (verified) | Verdict |
|---|---|---|---|---|
| "5GEMSDOE — ownership unconfirmed" | <https://buffedlizard55-lab.github.io/5GEMSDOE/docs/index.html> | `buffedlizard55-lab/5GEMSDOE` | id 309556078 | **OURS** |
| "GEMSDOE4 — ownership unconfirmed" | <https://buffedlizard55-lab.github.io/GEMSDOE4/> | `buffedlizard55-lab/GEMSDOE4` | id 309556078 | **OURS** |
| "6GEMSDOE — ownership unconfirmed" | <https://buffedlizard55-lab.github.io/6GEMSDOE/> | `buffedlizard55-lab/6GEMSDOE` | id 309556078 | **OURS** |

Live spot-checks this session (research fetch of the published pages):
`5GEMSDOE/docs/index.html` serves a full "Overview — GEMS Prize" submission
builder (pinned artifact `7f00890a…`, run `ens12-adopted-floor0.1-w0`); `GEMSDOE4/`
serves its own full builder (pinned artifact `932c2f30…`, "union k=1 of 4
members") plus a "GEMSDOE4 — the new-fault-first line" strategy section. These
are complete parallel builds, not placeholders.

Per the brief's guardrail, these three are therefore **deprecated past copies to
consolidate into the one live repo — NOT parallel test arms.** Their scores
(see §6) are **not** folded into our record as additional attempts.

Also confirmed ours at the GitHub level (the brief had labelled them "external
context — do NOT assume"): the repos behind `GEMSDOE`, `GEMSDOE2` and `GEMSDOE3`
likewise belong to owner id 309556078. `GEMSDOE3/THIRD_PARTY.md` documents the
copy chain: *"Upstream project: `buffedlizard55-lab/GEMSDOE`, commit
`cceebbdcf9a7d2890bb0665defcb54dfc66ae452`, copied at the repository owner's
request."* All eleven are one project replicated eleven times.

## 5. Finding F4 — five repos each claim operational primacy

Self-designations read from the repos this session (all ours, all in conflict):

| Repo | Its own claim |
|---|---|
| `GEMSDOE` | README leads with its in-browser "Build submission.tif" builder (added 2026-09-24) |
| `GEMSDOE2` | publishes `SUBMISSION_READY.md` |
| `GEMSDOE3` | "Pindrop · GEMSDOE3 … **Start every work session here.**" with a 3-card upload order |
| `GEMSDOE4` | "GEMSDOE4 — the new-fault-first line" (a competing strategy, live builder) |
| `6GEMSDOE` | "6GEMSDOE — the single canonical entry … This repository is designated the single entry" (`ACCOUNT_STATUS.md`, 2026-09-25) |

Meanwhile **this session's brief** states: *"Review this repo. This is our ONE
and ONLY GEMSDOE project"* — pointing at `MasterSelfLearn` (this repository).
That is a **three-way designation conflict** (brief → MasterSelfLearn;
`6GEMSDOE` → itself; `GEMSDOE` → the upstream original that GEMSDOE3 documents
as the copy source). Which repo is "the one live repo" to consolidate into
**requires an explicit human ratification** — this flag does not silently pick.

## 6. Finding F5 — registration surface (DrivenData): five tracked accounts, ownership UNVERIFIABLE from here

Public leaderboard **re-pulled fresh this session** (research fetch of
<https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/>,
2026-09-26). Field high **unchanged at 0.3049** (DARD, #1). The five accounts
named in the brief are all on the board, **1 submission each, scores exactly as
in the brief's snapshot** (no score drift, no new submissions by them):

| Rank | DrivenData user | Best public DW-Tversky | Submissions | Brief row |
|---|---|---|---|---|
| #22 | `extradr19` | 0.1563 | 1 | site GEMSDOE — "extradr19" |
| #23 | `smashi34` | 0.1560 | 1 | site GEMSDOE2 — "smashi34" |
| #39 | `smrtdoog5` | 0.1193 | 1 | site GEMSDOE3 — "SUBMIT FIRST", "Pindrop nodes" |
| #40 | `SDCF9` | 0.1152 | 1 | site GEMSDOE3 — "CONTROL, UPLOAD LAST", "Pindrop dense ridge control" |
| #49 | `wbg1` | 0.0830 | 1 | site GEMSDOE3 — "SUBMIT SECOND", "Pindrop catalogue-gap target" |

Top of the fresh board (context; the Phase-1 payout line is the top **five** at
$10K each): DARD 0.3049 · alexoktaba 0.2993 · HardcoreTechGod 0.2854 · mzoorob
0.2843 · joeyfezster 0.2589 · GrigorSargsyan 0.2504 · xiaofanhu 0.2367 ·
exposed 0.2262 · hiii12345 0.2255 · tchu 0.2220 … The static render covers
through ≈#50 (≈0.0811); rows below load via JavaScript.

The brief's mapping is corroborated by `GEMSDOE3/README.md`, whose three
published cards ("SUBMIT FIRST" pindrop-v4-nodes / "SUBMIT SECOND"
pindrop-v4-discovery / "CONTROL, UPLOAD LAST" pindrop-v4-ridge) match the three
GEMSDOE3 rows' notes one-to-one.

**What CANNOT be verified from this environment (flagged, not guessed):**

1. Which of the five DrivenData registrations (if any) is "the ONE account" the
   brief refers to. The brief lists the five as external context and forbids
   assuming they are ours — yet the repos that built and published their
   submission files are provably ours (§4). The registration-to-entity mapping
   must be confirmed by the account holder.
2. Whether any **new** DrivenData registration of ours was created since the
   last session. Registrations with zero submissions do not appear on the public
   leaderboard, and no public endpoint lists a competition's registrants.
3. Rules A.3 ("Teams and Single-Entity Awards") full verbatim text — only the
   section's existence (PDF contents) was confirmed this session.

Until (1) is resolved: **do not submit through any of these accounts, and do not
treat the five scores as five attempts of ours.** If the five are one entity,
that posture is what the brief's "ONE account" guardrail and the rules'
single-entry / single-entity structure (§1.1, page 967 quote above) are about —
resolve eligibility posture **before** any further upload, including the
perjury-certification exposure in rules §1.3 and the generative-AI disclosure
duty in rules §3.2.

## 7. Finding F6 — the brief's own step 1 cannot execute as written

The brief says *"Every session: 1. Re-read this prompt from the README before
doing anything else."* The prompt is **not** in `README.md` of this repo, nor in
any tracked `.md` file: `git grep -i` for `gemsdoe|gems |geodawn|drivendata|
tversky|geothermal` over `*.md` returns nothing, and `fault` appears in `.md`
files only inside the word "default". The only GEMSDOE traces in the repo are
data-layer artifacts: the `gemsdoe` keyword in `data/profile.json` /
`data/memory.json`; ten `owner-corpus` rows in `data/claims.jsonl` (e.g.
`C015523`) that quote the `GEMSDOE` repo's own catalog description ("Evidence-
backed site for the DOE GEMS Prize Challenge on DrivenData …"); the `GEMSDOE`
repo name in the `data/seed/owner_repos.json` (+`r2/`) snapshots; and their
render into `data/library.json` / `data/site.js`. There is **no GEMSDOE research
library and no session prompt** in this repository — mission step 1 and step 2
("re-derive … from what is published here") have no substrate here yet.
Likewise the brief's *"our live site (docs/index.html)"* matches the
GEMSDOE-family layout (a `docs/` site), not this repo's root-level site. Both
mismatches are consistent with the designation conflict in §5 and must be
resolved with it.

## 8. Reproduction (all read-only)

```bash
# inventory + timestamps + contents
gh api "users/buffedlizard55-lab/repos?per_page=100&sort=created&direction=desc" \
  --jq '.[] | {name, created_at, pushed_at, size, has_pages}'
gh api "search/repositories?q=GEMSDOE&per_page=50" --jq '.total_count, (.items[].full_name)'
gh api repos/buffedlizard55-lab/<repo> --jq '{full_name, owner, created_at}'
gh api "repos/buffedlizard55-lab/<repo>/contents/" --jq '.[] | .path'
gh api "repos/buffedlizard55-lab/<repo>/pages" --jq '{html_url, status}'
gh api "users/kanlerxz87-cyber" --jq '{login, public_repos}'
gh api "repos/buffedlizard55-lab/6GEMSDOE/contents/ACCOUNT_STATUS.md" --jq .content | base64 -d
gh api "repos/buffedlizard55-lab/GEMSDOE3/contents/THIRD_PARTY.md"  --jq .content | base64 -d
```

Public pages (research fetch tool; `curl` from this runner is egress-blocked):
`…/competitions/306/competition-doe-gems/leaderboard/`, `…/page/967/`,
`https://www.nlr.gov/docs/fy26osti/96647.pdf`, `…/5GEMSDOE/docs/index.html`,
`…/GEMSDOE4/`.

## 9. What was deliberately NOT done (stop compliance)

- **No mission work**: no methodology re-derivation, no reference-site study,
  no leaderboard-gap analysis, no literature research, no hypothesis logging
  beyond this audit. All deferred until the flag is resolved.
- **No changes to any GEMSDOE\* repo**: no commits, no deletions, no archives,
  no Pages disabled, no site edits. Consolidation is prepared (below), not
  executed — deleting or mutating ten repos is a destructive human decision and
  the brief said stop.
- **No submissions** to DrivenData; the credentials listed in the brief were not
  used and are not reproduced in this file (public usernames only).
- **No new repos, sites, or registrations.** Nothing was created anywhere.
- The five stub repos were **not** adopted as parallel experiment arms.

## 10. Session log — hypotheses tested this session

| # | Hypothesis | Test | Result |
|---|---|---|---|
| H1 | The three unconfirmed sites are third-party | `gh api repos/<repo>` owner fields (×2 passes) | **Falsified** — all ours (id 309556078) |
| H2 | No duplicate repos/sites of ours exist since the last session | repo inventory vs brief inventory + global search | **Falsified** — 5 new stubs (F2), 11 total (F1) |
| H3 | The five reference scores have drifted since the brief's snapshot | fresh leaderboard pull | **Falsified** — all five exact-match (0.1563 / 0.1560 / 0.1193 / 0.1152 / 0.0830) |
| H4 | Field high has moved | fresh leaderboard pull | **Falsified** — 0.3049 (DARD) unchanged |
| H5 | The brief is re-readable from this repo's README (brief step 1) | repo-wide grep + README read | **Falsified** — prompt not in repo (F6) |
| H6 | The runner can HTTP-probe the sites with curl | 12 URL probes | **Falsified as a method** — all `000`; egress policy (runner fact), switched to `gh` + research fetch |

## 11. Still unverified / needed / pick up first next session

**Pre-existing defect noted in pass 2 (unrelated to this audit, for the engine's
own backlog):** `python3 -m unittest discover -s tests` is 349/350 green; the
one failure (`test_site.RenderCheck.test_every_page_renders`) is a `BADVAL
{"undefined":1}` template slot in the **generated** `projects.html` (sample text:
"the undefined MPT-Flawless names (IR-36)"). Re-running the test with this flag
file removed reproduces the failure identically — it exists on base commit
`634739c` and is not caused by this change. Per `AGENTS.md` §2 the fix belongs
in the generator (`msl/sitegen.py` / `msl/docs.py` templates or the upstream
project-catalog data), not in the rendered page.

**Still unverified (do not guess):**
1. Which DrivenData registration is "the ONE account"; ownership of the five
   registrations (needs the account holder / DrivenData login).
2. Whether new zero-submission registrations were created since the last
   session (not publicly enumerable).
3. Who/what created the 2026-09-25 repo bursts (API does not expose actor).
4. Rules A.3 and A.16 verbatim text (A.3 only title-confirmed; A.16 quoted only
   via `6GEMSDOE/ACCOUNT_STATUS.md`).
5. Whether "the one GEMSDOE project" is `MasterSelfLearn` (this brief) or
   `6GEMSDOE` (its own designation) or `GEMSDOE` (upstream original).

**Pick up first next session (in order):**
1. **Human ratification of THE one repo/site** (§5). Until then, no consolidation.
2. **Registration due-diligence** (§6): enumerate our actual DrivenData
   registrations; fix the one-account posture against rules §1.1/page 967 before
   any upload; document the decision with rule citations.
3. **Consolidation** of the 10 non-chosen GEMSDOE repos: archive (preserve
   `GEMSDOE3`-style provenance first — its `THIRD_PARTY.md` is the right
   pattern), then disable Pages on all but the chosen one, then delete or
   archive the five stubs. The five stubs (F2) are safe to remove first.
4. **Embed the session prompt in the chosen repo's README** so brief step 1
   becomes executable (F6); keep this flag file's role as the audit record.
5. Only then resume the research program (brief steps 2–5), remembering the
   target is **faults MISSING from the training catalogue** — both prize rounds
   score the experts' new-fault set (rules §1.1, page 967 — verified above), not
   the public USGS/INGENIOUS catalogue.

---

*Audit performed 2026-09-26 UTC in `buffedlizard55-lab/MasterSelfLearn` on
branch `arena/01a0db08-masterselflearn`. Three-pass review: (1) implement &
verify — §2–§8 evidence collected and cross-checked; (2) self-review — owner
re-confirmed per repo, every brief-listed site re-mapped (§4), credentials
minimized, runner-egress vs site-down distinguished, repo-ownership vs
registration-ownership kept separate; (3) re-checked against the brief (stop
condition honored; nothing created, edited, or submitted) and the official rules
(§1.1 single entry, §3.2 3/week + AI disclosure, page 967 single blind choice,
§1.3 eligibility).*
