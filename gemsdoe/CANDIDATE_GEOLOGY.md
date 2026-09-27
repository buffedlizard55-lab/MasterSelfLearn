# CANDIDATE GEOLOGY — the reasoning behind the flagged traces

Session-brief item 6: *"For any candidate fault the model flags, write down the
geological reasoning behind it, not just the pixel mask."*

This file supplies the missing half of `6GEMSDOE/CANDIDATES.md`, which is a
geometry-and-statistics table. For each candidate it records: what the model
says (measured), what the official fault database says is nearby (sourced), the
geological interpretation, and **what observation would confirm or kill it**.

Source discipline used here:

- **MEASURED** — from `data/evidence/candidates.json`, provenance-pinned to
  submission `gems6_hgb88-topk03_33cec71ff0.tif`
  (sha256 `33cec71ff00b3f32…`), prob surface `89ee392338929292…`,
  features `4371c82e3b8339b8…`.
- **SOURCED** — live query this session (2026-09-26) against the Nevada Bureau
  of Mines and Geology Quaternary-fault ArcGIS REST service,
  <https://gisweb.unr.edu/nbmg/rest/services/Geology/Faults/MapServer/0/query>,
  whose own service description states the layer is *"adapted and modified from
  the Nevada Bureau of Mines and Geology M167 Quaternary Faults in Nevada and
  the U.S. Geological Survey Quaternary Fault and Fold Database"*, and whose
  records carry `Source = "USGS Q Fault & Fold Database"`. Upstream:
  <https://www.usgs.gov/programs/earthquake-hazards/faults>.
- **INTERPRETATION** — our reasoning. Labelled as such, never mixed into the two
  above.

**Search-window caveat, stated up front.** Each lookup was a
±0.05° envelope (≈ ±4.3 km N–S, ±4.2 km E–W at these latitudes) around the
candidate's ring centroid, `returnGeometry=false`. So "X fault zone is in the
window" is a sourced statement about a ~4 km box. **Exact trace-to-trace
separation was not computed** — that needs `returnGeometry=true` plus a distance
transform, and it is listed as the first follow-up in §4. Do not read a named
fault in the window as "the candidate *is* that fault".

---

## 1. What the model flagged, in aggregate (MEASURED)

From `candidates.json`: 1,380 components ≥ 8 px, 14,625,500 m (14,626 km) of
candidate line, split:

| class | rule | count |
|---|---|---|
| `on_catalogue` | ≤ 100 m from a catalogue pixel | 1,032 |
| `near_catalogue` | ≤ 300 m | 88 |
| **`new_to_catalogue`** | **> 300 m** | **260** |

Only the 260 `new_to_catalogue` candidates can earn score in either prize round,
because both rounds score faults **missing from the training catalogue**
(competition home page: *"Participants will be evaluated based on their
performance predicting faults contained in a newly labeled, private set of
faults"*). So 260 of 1,380 components — 19% — are the ones that need a
geological argument. The other 1,120 restate the catalogue.

`famrank` below is the median per-family evidence rank along the trace
(0 = weakest pixel in the feature domain, 1 = strongest), in the order
mag / grav / strain / seis / cond / topo; `agree4` is the median number of the
six families simultaneously in their global top 25%.

---

## 2. The regional frame — what the sourced records themselves show

Before the per-candidate reasoning, one sourced observation that constrains all
of it. Across the five windows queried this session, the QFFD-derived records
are **not** uniformly normal-slip:

| window | structures returned | `Type` values | youngest `Age` |
|---|---|---|---|
| 40.50°N 118.11°W | Eastern Humboldt Range fault zone | N | <130,000 |
| 40.62°N 118.10°W | Western + Eastern Humboldt Range fault zone | N | <1,800,000 |
| 40.48°N 116.86°W | Shoshone Range fault zone | N | **<15,000** |
| 40.15°N 116.73°W | Cortez Mountains fault zone, SW section | N | <750,000 |
| 39.31°N 119.46°W | Carson lineament | **N and SS** | **<15,000** |
| 38.70°N 118.38°W | Indian Head fault; Gumdrop Hills fault zone | **SS** (and N) | **<15,000** |

Two things follow directly, without importing any regional model:

1. **Holocene (`<15,000`) structures are present in at least three of the six
   windows.** Holocene faulting means scarps that have not been degraded away —
   which is exactly what the `det_elev` curvature and `slope_of_slope` channels
   can see at 100 m sampling. Candidates near these windows have a
   geomorphic-visibility argument that candidates elsewhere do not.
2. **Strike-slip (`SS`) is documented in the two western/southern windows**
   (Carson lineament; Indian Head fault and Gumdrop Hills fault zone), alongside
   normal slip. So a candidate with an oblique trend in those windows is not
   automatically an artefact of a normal-fault-only reading of the region.
   (The wider Walker Lane / eastern California shear zone framing quoted in
   `6GEMSDOE/CANDIDATES.md` is **carried forward unverified this session** — the
   Wesnousky 2005 and Hreinsdóttir citations there were not re-read. Treat that
   paragraph as unconfirmed until someone re-reads it.)

---

## 3. Per-candidate reasoning — top six `new_to_catalogue` by median probability

> **Session-4 status (2026-09-26):** the three falsification tests of §4 have
> now been run on raw bands — see §5 for the per-candidate outcomes. Net:
> **C-4 demoted** (N–S striping artefact present in `tmi_hg`), **C-7 and C-5
> strengthened** (their kill tests failed to kill), C-2 survived its striping
> test marginally. Read §5 alongside each block below.

### C-1 · 40.5042°N, 118.1105°W · 1,200 m · azimuth 34.3° · p̃ 0.577 · 412 m from catalogue
**MEASURED** famrank 0.70 / **1.00** / 0.28 / **0.93** / 0.72 / 0.72; agree4 = 2.0
**SOURCED** Eastern Humboldt Range fault zone (N; <130,000 and <1,800,000; slip <0.2 mm/yr) in the window.

**INTERPRETATION.** Gravity rank 1.00 is the single strongest value in the
whole top-12 set, and seismicity 0.93 is high; strain 0.28 is low. That
combination — a density contrast and seismicity, without a geodetic strain
signal — is what an **older, range-bounding normal fault with a large accumulated
throw** looks like: enough displacement to offset the basement density
interface, enough Holocene-to-late-Quaternary activity to sit near
seismicity, but no measurable present-day strain because the slip rate is low
(the sourced record says <0.2 mm/yr). The NE trend (34°) is consistent with the
range front rather than cutting it. At only 412 m from the catalogue this is
most plausibly an **unmapped parallel or antithetic strand** of the Eastern
Humboldt Range zone, or a step basinward of the mapped trace.
**Confirm with:** the 1 m DEM (716 tiles confirmed over the footprint) for a
linear scarp/facet run continuous with the mapped zone; a fault-plane solution
or epicentre alignment along the trend.
**Kill it if:** the 34° trend is the mapped trace's own trend offset by a
constant amount everywhere — that is a rasterisation/georeference bias, not a
new fault.

### C-2 · 39.3113°N, 119.4628°W · 1,900 m · azimuth 2.0° · p̃ 0.575 · 1,903 m from catalogue
**MEASURED** famrank **0.91** / 0.86 / **0.88** / 0.73 / 0.42 / 0.74; agree4 = 3.0
**SOURCED** Carson lineament (N **and** SS; <15,000 on some segments; slip <0.2) in the window.

**INTERPRETATION.** This is the best-balanced candidate in the set: magnetics
0.91, gravity 0.86 and strain 0.88 all high, conductivity the only weak family
(0.42). A near-pure N–S trace (azimuth 2.0°) 1.9 km from any catalogue pixel,
beside a **Holocene** structure that the database records as both normal and
strike-slip. High strain rank next to a documented Holocene fault, with no
conductivity anomaly, reads as a **through-going brittle structure in
crystalline basement** — fluid-poor, so it does not light up conductivity, but
actively deforming. That is a plausible geothermal-relevant target precisely
because permeability on such a fault is structural rather than alteration-controlled.
**Confirm with:** the strike-slip component implied by the sourced record should
show as en-échelon segmentation or a Riedel pattern in the magnetics HGM/tilt
channels — check `mag_tilt` and `tmi_hgm_computed` along the trace for
systematic stepping.
**Kill it if:** the N–S trace is a survey-line artefact. N–S azimuth is the
classic aeromagnetic flight-line direction; check `tmi_hg` for striping parallel
to the trace before believing it. **This is the most important falsification
test in the list** and it applies to every N–S candidate here (C-2, and the
azimuth ≈ 0–13° group).

### C-3 · 40.4790°N, 116.8569°W · 3,300 m · azimuth 32.3° · p̃ 0.574 · 500 m from catalogue
**MEASURED** famrank 0.60 / 0.80 / 0.34 / 0.64 / 0.73 / **0.87**; agree4 = 2.0
**SOURCED** Shoshone Range fault zone (N; **<15,000**; slip <0.2) in the window.

**INTERPRETATION.** Topography rank 0.87 is the highest of the six families and
strain 0.34 the lowest — the **opposite** profile to C-1. A strong geomorphic
expression with weak present-day strain, next to a fault zone the database dates
to the Holocene. That is the signature of a **young, well-preserved range-front
scarp** whose slip is episodic rather than continuous: enough of a scarp to
survive 100 m-pixel detection, low enough average rate that geodetic strain does
not resolve it. Longest trace in the top six at 3.3 km and only 500 m off the
catalogue, so an **along-strike extension** of the mapped Shoshone Range zone is
the first hypothesis — and trace extension is exactly the geometry an expert
reviewer adding "new" faults is most likely to produce.
**Confirm with:** `slope_of_slope_s1.5` / `curv_profile` cross-sections
perpendicular to the trace; a scarp with a convex break at the same position on
both flanks is a fault, a single-sided break is a bedding or erosional edge.
**Kill it if:** the topography rank is carried by a drainage line. Check whether
the trace follows a valley axis (concave in plan) rather than crossing one.

### C-4 · 40.1515°N, 116.7315°W · 1,500 m · azimuth 172.0° · p̃ 0.571 · **1,628 m** from catalogue
**MEASURED** famrank 0.70 / **0.90** / 0.55 / **0.93** / **0.88** / 0.78; agree4 = 4.0
**SOURCED** Cortez Mountains fault zone, southwest section (N; <750,000 and <1,800,000; slip <0.2) in the window.

**INTERPRETATION.** Four of six families in the top quartile (agree4 = 4.0), the
second-highest in the top six, and the trace is a genuinely long way from the
catalogue (1.6 km). Azimuth 172° is N–S but south-dipping-sense, i.e. it does
*not* parallel the NE-trending Cortez Mountains zone in the window — so this is
not a simple strand of it. Gravity 0.90 + conductivity 0.88 + seismicity 0.93
together is the most geothermally interesting profile in the list: a density
contrast, a conductive zone, and earthquakes on the same 1.5 km line. Read
together that is a **transverse structure cutting the range front, with fluids
along it** — the classic setting for an upflow zone where a transverse fault
intersects a range-bounding normal fault.
**Confirm with:** whether the conductivity high (0.88) is a narrow linear
conductor along the trace (structural, fluids in the damage zone) or a broad
basin fill (stratigraphic, uninformative). `cond_surf` cross-section settles it.
**Kill it if:** the conductivity high is the basin centre and the trace is just
the basin edge — then the "conductive anomaly" is sediment thickness, not a
fault-controlled fluid path. Note `depth_to_base_surf` is the channel that
separates those two cases, and the shipped model does have `x_cond_surf__depth_to_base_surf`.

### C-5 · 40.6208°N, 118.1008°W · **6,900 m** · azimuth 35.0° · p̃ 0.564 · 671 m from catalogue
**MEASURED** famrank **0.92** / **0.99** / 0.25 / **0.93** / 0.83 / 0.80; **agree4 = 5.0**
**SOURCED** Western **and** Eastern Humboldt Range fault zone (both N; <1,800,000; slip <0.2) in the window.

**INTERPRETATION.** The strongest candidate in the set on every axis except
strain: highest agree4 (5 of 6 families in the top quartile), gravity 0.99,
magnetics 0.92, seismicity 0.93, and at 6.9 km the second-longest trace in the
top twelve. It sits ~13 km north of C-1, in the same Humboldt Range system, and
the window returns **both** range-bounding zones — so this is a
**graben-margin structure between two opposed range-front normals**, i.e. the
fault system that bounds a half-graben. Paired range-front normals with a
conductive, seismically active structure between them is a textbook geothermal
play: the transverse/interior structure is where cross-flow can occur.
Strain 0.25 is the one weak family and it is consistent with a system whose slip
is concentrated on the mapped range fronts while the interior structure moves
slowly.
**Confirm with:** whether the 35° trend is continuous with C-1's 34° trend over
the 13 km between them. If C-1 and C-5 are the same structure, the pair is one
~15 km candidate and should be assessed as one, not two — and a 15 km
unmapped structure is a much stronger claim than two short ones.
**Kill it if:** the two Humboldt zones in the window are being detected as one
because the model is responding to the *graben fill* (a density low) rather than
to either fault. Gravity rank 0.99 on a *high* versus a *low* is the difference
between a basement uplift and a basin; the sign is not in `famrank` (which is
magnitude-ranked) and must be read off `iso_grav_anom` directly.

### C-7 · 38.6997°N, 118.3778°W · 2,200 m · azimuth 159.0° · p̃ 0.552 · **2,059 m** from catalogue
**MEASURED** famrank 0.81 / 0.73 / **0.97** / **0.91** / 0.81 / 0.82; **agree4 = 5.0**
**SOURCED** Indian Head fault (**SS**; **<15,000**); Gumdrop Hills fault zone (N and SS; <130,000) in the window.

**INTERPRETATION.** The most distinctive candidate here, and the one whose
geology is best supported by the sourced records. It has the **highest strain
rank in the entire top twelve (0.97)** with seismicity 0.91, all six families
above 0.73, agree4 = 5.0, and it is 2.1 km from the catalogue — far enough that
"unmapped strand" is less likely than "structure the catalogue does not have at
all". Its azimuth (159°, i.e. SSE) is oblique to a pure N–S normal fault, and
the window contains a **Holocene strike-slip** fault plus a zone the database
records in *both* normal and strike-slip modes. High geodetic strain + high
seismicity + oblique trend beside documented Holocene strike-slip is a coherent
picture of an **active oblique-slip structure within a transpressional/transtensional
transfer zone** — the kind of structure that transfers strain between
range-front normals and is systematically under-mapped, because it does not
present as a clean range front.
**Confirm with:** the strike-slip prediction is testable from the data we
already have — an oblique-slip fault in a transfer zone should show
**en-échelon segment offsets** rather than one straight trace. Check
`lin_elev_cos2theta_s1`/`sin2theta_s1` for a consistent orientation that steps
along the trace. Also: the sourced `Indian Head fault` is a named, Holocene,
strike-slip structure — a candidate 2 km from the catalogue that lands next to
it should be compared against the *full* QFFD record for that fault, not just
its presence in a box.
**Kill it if:** the 0.97 strain rank is an artefact of the `geod_shearrate` /
`geod_dilaterate` bands' own interpolation. Strain-rate products are smoothed
over large footprints; a narrow 2.2 km trace inheriting 0.97 from a broad
regional gradient is not evidence about the trace. **Cross-check the strain
rank against the band's own spatial gradient** before treating this as the
flagship candidate.

---

## 4. Cross-cutting conclusions

1. **The candidates are not random.** Five of the six land within ~4 km of a
   named QFFD structure while being >300 m from the catalogue's own pixels. That
   is the expected shape of the answer for this prize: the hidden set is
   "faults the experts added", and experts add strands, extensions and
   transverse structures adjacent to known systems — not structures in geology
   that has never been looked at. **INTERPRETATION, but a strong one.**
2. **Two distinct evidence archetypes appear, and they should be ranked
   separately.** C-1/C-3/C-5 are *gravity-and-topography-led with low strain* —
   older, large-throw, geomorphically expressed. C-2/C-4/C-7 are
   *strain-and-seismicity-led* — younger, actively deforming, and in C-4/C-7
   conductivity-positive. Geothermal relevance is not the same for the two
   groups, and neither is falsification risk (the strain-led group is exposed
   to the smoothed-strain-band artefact in §3 C-7; the gravity-led group is
   exposed to basin-vs-uplift sign ambiguity in §3 C-5).
3. **Three falsification tests dominate the list**, in order:
   (a) N–S aeromagnetic flight-line striping in `tmi_hg` (threatens C-2 and the
   whole azimuth ≈ 0–13° group);
   (b) smoothed regional gradient inherited by `geod_shearrate` (threatens C-7,
   the highest-strain candidate);
   (c) gravity *sign* — basement high vs basin fill (threatens C-1 and C-5,
   whose 1.00 and 0.99 ranks are the strongest in the set).
   None of these is answerable from `famrank`, which is magnitude-ranked. All
   three need the raw band values along the trace.
4. **The agreement channels that produced `agree4` and the `famrank` columns are
   the same 17 channels the shipped model does not use**
   (`PIPELINE_AUDIT.md` §1, finding F-1). So the evidence that makes these six
   candidates legible to a geologist was computed and then excluded from the
   prediction. That is the single most actionable inconsistency in the pipeline:
   the reasoning layer and the scoring layer disagree about whether this
   information is useful.

### Follow-ups, in order

1. Re-run every lookup with `returnGeometry=true` and compute exact
   trace-to-trace separation, so "in the window" becomes a distance.
2. Pull the **full** QFFD record (not just name/age/type) for the Eastern
   Humboldt Range, Shoshone Range, Cortez Mountains SW, Carson lineament,
   Indian Head and Gumdrop Hills zones — dip, sense, and any published slip-rate
   estimate — and check each candidate's azimuth against the documented dip
   direction.
3. Run falsification tests (a)–(c) above along each trace. **DONE — session 4,
   see §5.**
4. Extend this file past the top six: there are 260 `new_to_catalogue`
   candidates and only 6 have written reasoning. The generator
   (`scripts/candidate_writeup.py`) should emit the SOURCED lookup per candidate
   automatically rather than have it done by hand.

---

## 5. Session-4 falsification results (E10, 2026-09-26)

**MEASURED** — `gemsdoe/probes/e10_falsification.py` against the sha-pinned
official raster (`training_features.tif`, sha256 `4371c82e…`) this session.
Raw bands only (`tmi_hg`, `geod_shearrate`, `geod_dilaterate`, `iso_grav_anom`,
`det_elev`, `depth_to_base_surf`) — never `famrank`, which cannot answer any
of these. Trace geometry: `candidates.json` stores bbox + azimuth + length but
not pixel lists, so each trace is sampled on its **bbox-centerline segment**
(exact for straight traces; stated approximation). Window = ±25 px (±2.5 km).

| candidate | (a) N–S striping in `tmi_hg` | (b) strain-gradient inheritance | (c) gravity sign | session-4 verdict |
|---|---|---|---|---|
| C-1 (id 548) | not near-N–S — n/a | shear clear (R² 0.75); **dilatation FLAG** (R² 0.90, residual −0.08σ) | **+0.54σ basement HIGH** (trace 14.5 vs window 11.7) | **STRENGTHENED** on the kill-it-that-mattered; strain rank was always low (0.28) and is now doubly uninformative |
| C-2 (id 3552) | near-N–S but **clear** — E–W power share 0.233 < 0.25 threshold (control N–S share 0.490); period 10.4 px | clear on both bands (R² 0.77/0.78, residual 0.18/0.28σ) | −0.38σ mild low; det_elev −0.52σ (basin floor), basement deeper (+0.25σ) | **SURVIVED its main kill test** — the N–S trace is not sitting on a stripe artefact (marginal: 0.233 is near the flag threshold; keep watching) |
| C-3 (id 622) | not near-N–S — n/a | **`geod_shearrate` is data-sparse here (plane fit undefined, <30 finite px)**; dilatation FLAG (R² 0.95) | no contrast (+0.14σ) | **STRENGTHENED on its own terms** (topo-led, 0.87); its strain rank 0.34 is now known to be computed from a hole in the strain bands — uninformative either way |
| **C-4 (id 1618)** | near-N–S (172°) and **FLAGGED** — narrowband **E–W periodicity, 18 px period, power share 0.463** under the trace (control N–S share 0.202) | `geod_shearrate` sparse (fit undefined); dilatation FLAG (R² 0.90) | no contrast (+0.21σ) | **DEMOTED from the written-up flagship set.** The exact artefact the kill-it-if named is present in the band that gives the trace its edge evidence. Restated case: grav/seis/cond-only (0.90/0.93/0.88) — a fluids-bearing transverse structure *if* those families survive independent inspection; the magnetics/trend evidence is contaminated until someone subtracts the stripe field |
| C-5 (id 240) | not near-N–S — n/a | FLAG on both bands (R² 0.87/0.91) — but its strain rank is 0.25 (already the weak family) | **+0.27σ gravity HIGH**, **det_elev +0.86σ** (range front), **basement shallow (−0.70σ)** | **STRENGTHENED** — the kill-it-if (model responding to graben *fill*, a density low) is **refuted**: the trace sits on the dense/high/shallow-basement side. Coherent range-front reading |
| C-7 (id 4383) | not near-N–S (159°) — n/a | **CLEAR, and this was the flagship risk**: `geod_shearrate` plane R² only **0.29** in-window, trace residual −0.53σ — the 0.97 strain rank is a **local departure**, not a smoothed-gradient inheritance | −0.62σ gravity LOW but **basement deep (+0.92σ)**, det_elev high-ish | **STRENGTHENED** — the single most important kill test failed to kill it. Gravity-low + deep section + high strain + high seismicity is the transtensional transfer-zone reading, now with the strain artefact excluded at the window scale |

### What changed in the reasoning (INTERPRETATION, following the measurements)

1. **One candidate (C-4) is demoted** by test (a), exactly as the pre-registered
   rule in `HYPOTHESES.md` E10 ("a candidate killed by (a), (b) or (c) is
   removed from the written-up set and the reason is recorded") required. The
   test flagged rather than strictly proved the artefact (the model responds to
   ten other channels too), so C-4 is *demoted and restated on non-magnetic
   evidence* rather than deleted — the distinction is recorded so the next
   reader can re-promote it if the stripe field is subtracted.
2. **The flagship risk to C-7 is dead at the window scale.** The strain rank is
   earned locally (R² 0.29, residual −0.53σ). Combined with the sourced Holocene
   strike-slip neighbours, C-7 is now the best-supported candidate in the set.
3. **The gravity-sign test separates the gravity-led pair cleanly**: C-1 and
   C-5 are both density-HIGH / basement-shallow — basement structures, not
   basin-fill artefacts. C-5's graben-fill kill hypothesis is refuted outright.
4. **New finding, not in any earlier brief: `geod_shearrate` has data holes.**
   In the C-3 and C-4 windows the band has fewer than 30 finite pixels in the
   ±2.5 km window — the plane fit is undefined. Their `famrank_strain` values
   (0.34 / 0.55) are computed by the `max`-over-family-members rule from
   `geod_2ndinv` / `geod_dilaterate` alone. Any reading of a "strain rank" at
   those two locations must state this. **FLAGGED.**
5. **The (b) FLAG on `geod_dilaterate` is frequent (4 of 6) and mostly
   uninformative** — the dilatation-rate band is smooth almost everywhere
   (R² ≥ 0.9 in 4 windows), so "sits on the regional field" is the null case
   for that band. The discriminative test is the *shear*-rate R², which is low
   only at C-7 (0.29) and moderate at C-1/C-2 (0.75/0.77). Recorded so the
   next reader does not over-flag from the dilatation column.

### Still open per candidate (in priority order)

- C-2's 0.233 E–W power share is *near* the 0.25 flag threshold — re-test after
  any detrended/levelled `tmi_hg` becomes available.
- C-4's conductivity question (narrow linear conductor vs basin fill) is
  untouched by these three tests — `cond_surf` cross-sections are the next
  measurement before any re-promotion.
- All six: exact trace-to-trace QFFD separation (follow-up 1 above) is still
  outstanding.

---

## 6. Extension set — four more written up (session 4, task 6)

The brief asks for reasoning per candidate, not per pixel mask; the written-up
set now covers **ten** of the 260 `new_to_catalogue` components. Selection:
the previous session's "top six" **skipped rank 6 (id 1991, p̃ 0.558)** — its
"C-7" is rank 7 — so id 1991 is written up first (flagged as a selection
inconsistency in session 3, not silently absorbed). Then the two most
distinctive remaining profiles (id 872: cond rank **0.98**; id 4323: strain
rank **0.98**) and id 4209 (cond 0.93). QFFD windows queried live 2026-09-26
with `outFields=Name,Age,Type,Source` (session 3's field set; a `Slip_Rate`
attempt returns HTTP 400 from the service — the field does not exist there).

### C-6 · id 1991 · 40.0588°N, 118.4222°W · 4,400 m · az 24.6° · p̃ 0.558 · 1,000 m from catalogue
**MEASURED** famrank 0.81 / 0.97 / 0.60 / 0.75 / 0.59 / 0.80; agree 3.0. E10: shear
**inherited** (plane R² 0.95, residual −0.07σ); dilatation *departs* (+1.03σ);
gravity no contrast.
**SOURCED** Western Humboldt Range fault zone (N; <1,800,000) plus an unnamed
N section dated <130,000 in the window.
**INTERPRETATION.** The longest trace after C-5 (4.4 km) on the same Humboldt
system as C-1/C-5, at 24.6° — sub-parallel to C-1/C-5's ~34–35° but rotated
toward the range-front trend. Gravity 0.97 is second only to C-1/C-5, but the
E10 inheritance flag says its 0.60 strain rank is **carried by the smoothed
regional field, not earned locally** — treat the strain column as uninformative
here. What survives: gravity + magnetics + a sourced late-Quaternary unnamed
segment. Read as the **central segment linking C-1 and C-5 along the Western
Humboldt front** — if the three connect at trace resolution, the Humboldt
structure becomes a ~17 km system, the strongest single claim in the set.
**Confirm with:** the C-1 ↔ C-6 ↔ C-5 chain test (trend continuity over the
full latitude span 40.05–40.62°N).
**Kill it if:** the connecting trend is the gravity *gradient* of the basin
margin rather than a discrete structure — check `grav_hgm_computed` for a
single narrow ridge vs a broad ramp along the chain.

### C-8 · id 872 · 40.3677°N, 118.9505°W · 800 m · az 12.8° · p̃ 0.545 · 1,005 m from catalogue
**MEASURED** famrank 0.51 / 0.94 / 0.66 / 0.93 / **0.98** / 0.88; agree 4.0. E10:
**(a) FLAGGED** — near-N–S, E–W periodicity 17.3 px, power share **0.526**;
(b) strain **departs locally on both bands** (+0.64/+0.66σ on top of a smooth
field, R² 0.87/0.89); (c) no gravity contrast.
**SOURCED** Unnamed fault zone along Bluewing Mountains (N; <1,800,000);
**Granite Springs Valley fault zone with a <15,000 (Holocene) segment** (N).
**INTERPRETATION.** The highest conductivity rank in the whole top-12 (0.98)
with seismicity 0.93 and a Holocene neighbour — on non-magnetic evidence this
is the most geothermally pointed candidate after C-4's demotion: a conductive,
seismically active structure beside a Holocene fault. The (a) flag contaminates
its *magnetics/trend* evidence (az 12.8° sits in the stripe-suspect class), so
the case is **restated on cond/seis/strain only**, exactly as C-4's is. The
strain result here is the mirror image of C-6's: the trace is a *local*
maximum riding a smooth field — earned, not inherited.
**Confirm with:** `cond_surf` cross-section (narrow conductor = structural
fluid path; broad = basin fill — the C-4 kill test, applied here where cond is
even stronger) and the Holocene segment's mapped trace geometry from QFFD with
`returnGeometry=true`.
**Kill it if:** the conductivity high is the Granite Springs Valley fill
itself (`depth_to_base_surf` at the trace reads 18.8 m vs 21.2 m window —
shallow everywhere; if `cond_surf` maps the valley axis, the anomaly is
stratigraphic).

### C-9 · id 4209 · 38.8782°N, 117.9021°W · 1,000 m · az 24.7° · p̃ 0.542 · 412 m from catalogue
**MEASURED** famrank 0.53 / 0.81 / 0.74 / 0.72 / **0.93** / 0.72; agree 3.0. E10:
shear inherited (R² 0.92) but dilatation departs (−0.37σ); gravity mild (+0.22σ).
**SOURCED** Paradise Range fault zone (N; **<130,000**) in the window.
**INTERPRETATION.** Only 412 m from the catalogue — the nearest of the
extension set — beside a late-Quaternary normal zone. Cond 0.93 with modest
everything-else is the profile of a **basin-margin structure with fluid in the
damage zone**; at 412 m this is most plausibly a mapped-trace splay or step-over
(the PFA sweet-spot geometry of `HYPOTHESES.md` E4).
**Confirm with:** tip-ray/step-over geometry against the nearby catalogue
trace (E4's test); if the candidate is collinear with a catalogue trace tip,
it is an extension, which is exactly the population the experts' "new" set is
most likely to contain.
**Kill it if:** the cond high is valley fill along the Paradise Range front
(same cond_surf cross-section test).

### C-10 · id 4323 · 38.7578°N, 118.6216°W · 800 m · az 1.5° · p̃ 0.534 · 2,786 m from catalogue
**MEASURED** famrank 0.72 / 0.55 / **0.98** / 0.91 / 0.28 / 0.85; agree 3.0. E10:
**(a) FLAGGED** — near-N–S, E–W periodicity 13 px, share **0.456**; (b) strain
**departs on both bands** (−0.13/−0.40σ, R² 0.83/0.88); (c) **gravity HIGH
+0.67σ with basement very shallow (−1.07σ: depth_to_base 4 m vs 59 m window)
and det_elev high (+0.25σ)**.
**SOURCED** Agai Pah Hills fault zone (N; <1,800,000) in the window — and it
sits ~11 km north of C-7's Indian Head/Gumdrop Hills window, the same
southwestern corridor.
**INTERPRETATION.** The highest strain rank anywhere (0.98) with seismicity
0.91 — and, unlike C-7's, the E10 test says the strain is **earned locally,
not inherited** (the second candidate with that property). It stands on a
**shallow-basement gravity high** — a footwall/uplift setting, the opposite of
C-7's deep basin. C-10 and C-7 are 11 km apart in the same transtensional
corridor: one on the uplift side, one in the deep basin — the two flanks of
one transfer zone would look exactly like this pair. The az 1.5° trend is in
the stripe-suspect class (flagged), so the *orientation* is untrusted while
the *evidence stack* (strain+seis local maxima on a basement high beside a
named zone) survives.
**Confirm with:** whether C-10 and C-7 share a connecting structure (en-échelon
stepping between 38.70 and 38.76°N); magnetic edge map with the stripe field
subtracted before trusting the N–S trend.
**Kill it if:** the shallow basement high is the Agai Pah Hills range front
itself and the candidate merely traces the topographic break (`slope_of_slope`
vs `curv_profile` cross-sections decide).

### Class-level finding (INTERPRETATION over §5 + §6 measurements)

> **Session-5 status correction (see §7): this finding is DOWNGRADED to a
> physical prior.** The E12 baseline test (`e12_stripe_removal.py`, session 5)
> showed that test (a)'s threshold (E–W power share ≥ 0.25) is exceeded by
> 3/4 *non*-N–S written-up windows as well (raw shares 0.445–0.691), i.e. the
> "3/3 near-N–S flagged" contrast does not exist in the measurement — the flag
> reduces to the azimuth gate alone (instrument defect **D-9**, §7). Two
> levelling passes (global column median; y-aware 256-row block medians)
> changed the statistic but left flags at 4/4 while the baseline shares stayed
> equal or higher. What survives: the *physical* concern that N–S is the
> standard aeromagnetic flight-line direction (a prior, not a measurement
> about these traces). What does not: any claim that the (a) test *detected*
> striping under these particular traces.

**Every near-N–S trace tested with the striping probe has now flagged (3/3) or
sat at the threshold (C-2, 0.233).** The azimuth ≈ 0–17° emission class is
artefact-suspect as a class, not case by case. Practical consequence for the
next model build: N–S-oriented evidence from `tmi_hg`/`mag_*` channels should
carry a prior discount (or a detrended/levelled magnetic stack should replace
those channels) until a stripe-removal pass exists. Gravity, strain, seismicity
and conductivity evidence is unaffected by this class risk and is what the
demoted candidates are re-stated on.

---

## 7. Session-5 measurements: the chain test, the cond cross-sections, and the E12 instrument (2026-09-26)

**MEASURED** this session by `gemsdoe/probes/followup_chain_cond.py` and
`gemsdoe/probes/e12_stripe_removal.py` against the pinned official raster and
the D-1/D-5-fixed derived stack (same provenance as §5). Raw outputs: the
probes' `--out` JSON (reproduction commands in `probes/README.md`). These are
the two highest-value open measurements carry-forward 6 named.

### 7.1 The C-1 ↔ C-6 ↔ C-5 chain test — **REFUTED at trace resolution**

| link | facing endpoint gap | min lateral line offset | continuous (≤5 px)? |
|---|---|---|---|
| C-6 → C-1 | **53,363 m** | **34.91 px = 3,491 m** | **no** |
| C-1 → C-5 | 9,774 m | **56.08 px = 5,608 m** | **no** |

The three Humboldt candidates' extended centrelines pass kilometres apart, not
pixels: 35–56 px of lateral offset against a 3 px scoring kernel, and a 53 km
facing gap on the critical C-6→C-1 link. Gravity cross-sections along the legs
(a narrow central ridge vs a broad ramp, C-6's own stated kill-if):

| leg | narrow-ridge fraction (`iso_grav_anom_hg`) | (`grav_hgm_computed`) | verdict |
|---|---|---|---|
| C-6–C-1 | 0.241 | 0.414 | broad/ramp-like — **kill-if fires** |
| C-1–C-5 | 0.286 (median prominence −0.28 MAD) | 0.571 | mixed; raw band says ramp |

Intermediate candidates within 2 km of the legs: 3 on C-6–C-1 (ids 1758, 1794,
970), 0 on C-1–C-5.

**INTERPRETATION.** C-6's write-up condition — "if the three connect at trace
resolution, the Humboldt structure becomes one ~17 km system, the strongest
single claim in the set" — is **killed by its own pre-registered test**. The
three remain separate candidates; C-6 loses the chain-extension claim and
keeps only its own case (gravity + magnetics + the sourced unnamed <130,000
segment in its window). The §3 C-5 "confirm with: is the 35° trend continuous
with C-1's 34° trend over the 13 km between them?" is answered **no** — the
trends are sub-parallel but laterally offset by kilometres. The three
candidates' individual evidence profiles are unchanged; only the "one system"
story is gone. Flagged, not smoothed: this reverses the strongest claim
session 4's write-up set contained.

### 7.2 `cond_surf` cross-sections for id 872 (C-8) and id 1618 (C-4) — **both kill-ifs supported**

Single perpendicular profile (±25 px) through the bbox centre, plus the global
percentile ranks of both `cond`-family members computed from
`rank_tables.json` (the family is `max(rank(cond_surf),
rank(depth_to_base_surf))` — verified in `build_features.py`):

| candidate | famrank_cond cited | cond_surf global rank at trace | depth_to_base rank | cond_surf trace vs window | shape |
|---|---|---|---|---|---|
| **C-8** (id 872) | 0.984 | **0.984** | 0.111 | 4.316 vs 4.321 = **−0.044σ**; profile flat at its minimum across the centre, max at the window edge | **no conductor at the trace** |
| **C-4** (id 1618) | 0.884 | **0.886** | 0.758 | 3.504 vs 3.528 = **−0.108σ**; monotone decline across the trace | **no conductor at the trace** |
| C-9 (id 4209) | 0.930 | 0.930 | 0.156 | (rank check only) | same regional pattern |

**INTERPRETATION.** The 0.98/0.88 cond ranks are *real global ranks of
`cond_surf` itself* (not the depth member doing the lifting), but they are
**regional**, not trace-local: the whole ±2.5 km window sits in the globally
high regime and the trace itself is not a local maximum — for C-8 it is the
flat floor of the profile (4.316 vs an edge max of 4.608). That is exactly the
kill-if both write-ups named: C-8's "the conductivity high is the Granite
Springs Valley fill itself" and C-4's "the conductivity high is the basin
centre and the trace is just the basin edge". The cond evidence supports
*"this is a basin with conductive fill"* and does **not** support *"fluids are
along this fault"*. C-4's and C-8's cases therefore rest on their remaining
families (C-4: grav 0.90 / seis 0.93; C-8: seis 0.93 + strain earned-local
+ the sourced Holocene neighbour), with the cond pillar demoted from
"confirmation pending" to **measured-not-localised**.

*Caveat, stated:* one profile per candidate through the bbox centre; a hooked
or offset trace could hide a local high off the centreline. The ranks are
computed along the same centreline approximation §5 uses.

### 7.3 E12 executed — stripe levelling does **not** clear test (a), and test (a) has no baseline

`e12_stripe_removal.py`: levelling the six raw magnetic bands by (1) the
per-column nanmedian (global flight-line offset) and (2) y-aware 256-row-block
column medians (along-line drift), then re-running E10's test (a) on the same
windows, same 0.25 threshold:

| window | raw share (flag) | col-lev (flag) | block-lev (flag) |
|---|---|---|---|
| C-2 (N–S) | 0.233 (no) | 0.260 (**yes**) | 0.345 (**yes**) |
| C-4 (N–S) | 0.463 (yes) | 0.474 (yes) | 0.354 (yes) |
| C-8 (N–S) | 0.526 (yes) | 0.303 (yes) | 0.371 (yes) |
| C-10 (N–S) | 0.456 (yes) | 0.480 (yes) | 0.498 (yes) |
| **C-1/C-3/C-5/C-7 (non-N–S baseline)** | **0.691 / 0.246 / 0.596 / 0.445** | 0.678 / 0.180 / 0.609 / 0.426 | 0.581 / 0.183 / 0.486 / 0.347 |

- **Criterion (pre-registered: flag rate falls below the non-N–S baseline):
  NOT MET.** Flags 3/4 → 4/4 (both methods); near-N–S mean share 0.419 →
  0.379 → 0.392 against baseline means 0.494 → 0.473 → 0.399. The near-N–S
  class is never *more* periodic than the baseline — it is usually less.
- **The x-only stripe field s(x) itself carries no flight-line-scale
  periodicity**: its dominant E–W period is 823 px for `tmi_hg` (470 px for
  `tmi`; shares 0.10–0.16), not the 10–18 px E10 measured in windows. A
  column-constant component at flight-line spacing is therefore absent from
  these bands; what the window statistic sees is within-window structure
  (real E–W-wavelength geology, trace geometry, or along-line-varying noise
  that no global subtraction can remove).
- **Instrument defect D-9:** test (a)'s threshold does not discriminate:
  3/4 non-N–S windows exceed 0.25 too (up to 0.691). The class finding in §6
  was computed without this baseline and is therefore not identified by the
  instrument. The physical flight-line prior stands; the detection claim does
  not.
- Signal preservation: r(raw, levelled) 0.976–0.9997 (col) and 0.897–0.9984
  (block); block-levelling eats 42–47% of the trace-vs-window contrast at
  C-4/C-8 (0.547→0.291, −0.491→−0.284), col-levelling barely changes it
  (0.547→0.530; C-8 even gains, −0.491→−0.52) — so the y-aware pass is the
  more destructive one and still fails the criterion.

**What would settle it (proposal, next session):** an *alignment* test, not a
presence test — band-pass the x-only field at 5–30 px in the window and
measure whether each near-N–S trace's x-positions sit on its crests more often
than oblique/random traces do; plus the official GeoDAWN flight-line metadata
(orientation and line spacing) from the data documentation, which would turn
the physical prior into a sourced fact.

### Status changes this section forces

| candidate | before (session 4) | after (session 5) |
|---|---|---|
| **C-4** | demoted by test (a) | **demotion basis invalidated** (D-9): test (a) cannot detect what it was applied for. C-4 returns to *unresolved on magnetics* — neither proven contaminated nor proven clean — and its cond pillar is now measured-not-localised (§7.2). Grav/seis case unchanged. |
| **C-6** | "central segment of a ~17 km system" | chain **refuted** (§7.1); standalone candidate; kill-if fired on the critical leg. |
| **C-8** | cond 0.98 = confirmation pending | cond **measured regional, not trace-local** (§7.2) — kill-if supported; case restated on seis/strain/sourced-Holocene. |
| **C-2** | "survived (a) marginally, re-test after levelled tmi_hg" | re-test **executed and uninformative** (§7.3): levelling does not change the instrument; (a) cannot answer the question either way. Survival status vacuous; physical prior remains. |
| **C-1 / C-3 / C-5 / C-7 / C-9 / C-10** | as §5–§6 | unchanged; C-1/C-5 lose the chain narrative only (§7.1), C-4's sibling C-10 unaffected. |

---

## 8. Session-6 measurements: the stripe question closed on sourced geometry (E14), and the cond pillars re-measured properly (2026-09-26)

**MEASURED** this session by `gemsdoe/probes/e14_alignment.py` and
`gemsdoe/probes/followup_cond_multiprofile.py` against the pinned official
raster and the D-1/D-5-fixed derived stack (same provenance as §5; the §7
chain/cond probe was also re-run this session and **reproduces session 5's
numbers exactly** — offsets 34.91/56.08 px, 53,363 m gap, cond −0.044/−0.108σ,
ridge fractions 0.241/0.414 and 0.286/0.571 — instrument-chain stability
across rebuilds is now verified, not assumed).

### 8.1 The flight geometry is now SOURCED, and the session-3 prior was wrong for GeoDAWN

Source: USGS Science Data Catalog entry for the GeoDAWN data release
(Glen, J.M., and Earney, T.E., 2024, *GeoDAWN: Airborne magnetic and
radiometric surveys of the northwestern Great Basin, Nevada and California*,
U.S. Geological Survey data release, DOI https://doi.org/10.5066/P93LGLVQ :
<https://data.usgs.gov/datacatalog/data/USGS:657e1d85d34e23d3533209f7> —
fetched verbatim this session):

> "Area 1 … Flight lines were spaced 200 m apart at an azimuth of 90 degrees,
> and tie lines were spaced 2000 m apart at an azimuth of 180 degrees." ·
> "Area 2 … was flown with flight lines spaced 400 m apart at an azimuth of
> 90 degrees, and tie lines spaced 4000 m apart at an azimuth of 180 degrees."
> · "Magnetic data … include corrections for diurnal variations of the Earth's
> magnetic field, magnetic field of the aircraft, **tie-line leveling,
> micro-leveling**, and an International Geomagnetic Reference …"

Area 2 is "the remainder of the GeoDAWN extent, … selected primarily with a
focus on geothermal resources"; Area 1 is "centered over Clayton Valley in
western Nevada" (~37.8°N, Silver Peak). All ten written-up candidates sit at
38.70–40.62°N, far north of Clayton Valley, so **Area 2 specifications are
the relevant ones** (400 m flight lines / 4000 m tie lines — INTERPRETATION,
from the same page's area descriptions; the four acquisition blocks
Winnemucca/Fallon/Hawthorne/Tonopah are also named there).

**Consequences (this corrects §6's class-level prior):**

1. Session 3's prior — "N–S azimuth is the classic aeromagnetic flight-line
   direction" — does **not** hold for GeoDAWN: the flight lines run **E–W**
   (azimuth 90°). At 100 m sampling, flight-line striping would appear as
   E–W stripes with a 2–4 px N–S period — mostly sub-Nyquist and doubly
   smoothed (gridding plus the contractor's *micro-leveling*, which is the
   standard destriping step, quoted above as already applied).
2. N–S is the **tie-line** direction: residual tie-to-line levelling
   artefacts would appear as N–S stripes with a **20–40 px E–W** period
   (2000/4000 m). E10's 10–18 px window-FFT observations sit at half to full
   the tie scale — and E10/E12 were therefore testing a geometry the sourced
   metadata does not predict, on top of the D-9 baseline-contrast defect.
3. The physically adequate question for a near-N–S trace is: *is it locked
   to a tie-scale N–S stripe crest?* That is E14.

### 8.2 E14 executed — crest alignment, not presence (tie scale; trace self-masked)

`e14_alignment.py`, pre-registered before running. Per candidate, ±45 px
windows (wider than E10/E12's ±25 px, deliberately: the instrument needs
≥2 cycles of the 45 px tie edge in every window — stated in the probe).
The trace's own pixels are masked (±1) before the column-mean profile is
taken, so the trace cannot create its own crest; the profile is FFT
band-passed to 12–45 px; crests = local maxima ≥12 px apart; **A_x** =
share of the trace's per-row x-positions within ±2 px of a crest; null = 300
random N–S-band segments of the same length per window against the same
trace-masked profile; empirical p = share of nulls scoring ≥ the trace.
Verdict bar (pre-registered): A_x ≥ null p95 AND ≥ the oblique-control max.

| candidate | band | A_x | emp. p | tmi/rtp replicate A_x | verdict per rule |
|---|---|---|---|---|---|
| **C-2** (id 3552, az 2.0°) | tmi_hg | **0.000** | 1.00 | 0.000 / 0.000 | NOT tie-stripe aligned |
| **C-4** (id 1618, az 172.0°) | tmi_hg | 0.938 | **0.22** | **0.000 / 0.000** | NOT aligned (bar unmet, non-replicating) — anomaly recorded |
| **C-8** (id 872, az 12.8°) | tmi_hg | **0.000** | 1.00 | 0.000 / 0.000 | NOT tie-stripe aligned |
| **C-10** (id 4323, az 1.5°) | tmi_hg | **0.000** | 1.00 | 0.000 / 0.000 | NOT tie-stripe aligned |
| C-1/C-3/C-5/C-7 (oblique controls) | tmi_hg | 0.000–0.435 | 0.14–1.00 | — | within null |

**Class verdict (pre-registered: ≥3/4 near-N–S aligned AND median_Ax(near-N-S)
> median_Ax(oblique)): NOT MET** — 0/4 near-N–S traces are tie-stripe locked;
medians 0.000 (near-N–S) vs 0.254 (oblique). C-4's tmi_hg-only 0.938 is the
one anomaly: 15 of 16 trace-row x-positions sit on one band-passed crest, but
22% of random N–S segments score as high in the same window (bivariate null:
short vertical segments are either fully on or fully off a crest), it never
replicates on `tmi`/`rtp`, and it misses the pre-registered bar (null p95 =
1.0). It is recorded as a curiosity below every bar, not a detection.

Line arm (the sourced flight-line direction, E–W stripes at 2–6 px):
per-candidate A_y 0.38–0.78 against an analytic chance coverage 0.48–0.61
(min/max over candidates × the three bands) — at chance everywhere, and the
instrument is comparative-only by construction (stated in the probe); no
written-up candidate trends E–W, so no candidate structure has the
flight-line-stripe geometry in any case.

**What this closes.** The E10(a) → E12/D-9 arc is closed on the sourced
geometry: (i) the striping prior's direction was wrong for GeoDAWN (§8.1);
(ii) on the correct geometry (tie-scale N–S crests), no written-up near-N–S
trace is stripe-locked (this section); (iii) the E12 levelling result (no
removable column-constant field at the 10–18 px periods; x-only field period
823 px) stands as the third, consistent leg. **The "azimuth ≈ 0–17° emission
class is artefact-suspect as a class" framing is retired** — first downgraded
to a physical prior by D-9 (session 5), now with the prior itself corrected
and the alignment test negative. Magnetics evidence at the four near-N–S
candidates returns to neutral standing: neither discounted nor specially
endorsed. C-4's demotion basis (already invalidated by D-9) stays
invalidated, for a second, independent reason.

### 8.3 Cond pillars re-measured: five profiles per trace, and which family member actually fires

`followup_cond_multiprofile.py`, pre-registered verdicts before running
(≥3/5 profiles local-max-at-trace ⇒ locally supported; ≤1/5 with
|centre z| < 0.5 ⇒ kill-if stands; else inconclusive):

| candidate | profiles local-max | centre z(win) | verdict | vs session 5 |
|---|---|---|---|---|
| **C-8** (id 872) | **0/5** | 0.000 | **kill-if stands (regional)** | confirms §7.2 beyond the single-profile caveat |
| **C-9** (id 4209) | **0/5** | 0.000 | **kill-if stands (regional)** | §7.2 had rank-check only → now MEASURED; cond pillar demoted from "confirmation pending" to regional |
| **C-4** (id 1618) | 2/5 (fracs 0.70/0.85) | −0.092 | **inconclusive** (per rule) | refines §7.2: the southern half of the trace carries two local-max classifications — but on MAD-scale residuals, ALL five raw trace means stay below their window medians (z −0.009…−0.159) and every profile's maximum sits at the profile edge. The multi-profile extension does not support the conductor story anywhere; the honest verdict is "inconclusive", with the trace never a raw high |

**Member attribution over all 260 `new_to_catalogue` candidates**
(carry-forward 5's second half). `famrank_cond =
max(rank(cond_surf), rank(depth_to_base_surf))`, **no inversion on either
member** (verified in `build_features.py`: only `deq_n100a15` is inverted,
in the seis family). Median trace ranks recomputed from `rank_tables.json`
with the identical bin rule:

- 89/260 candidates have `famrank_cond ≥ 0.75`;
- **24 of those 89 (27%) are carried by `depth_to_base_surf` alone**
  (cond_surf itself < 0.75) — under the official band descriptions
  (`cond_surf` = "electrical conductivity of subsurface";
  `depth_to_base_surf` = "depth to basement surface — thickness of
  sedimentary cover") those candidates' "cond pillar" is **sediment
  thickness, not a subsurface conductor**. Example: id 4176 —
  famrank_cond 0.991 = max(cond_surf **0.097**, depth 0.991).
- Overall firing splits 135 cond_surf / 125 depth_to_base / 0 tie.
- **The written-up set is clean on this**: 9 of 10 fire on cond_surf itself
  (C-8's 0.984, C-9's 0.930, C-4's 0.886 are all cond_surf-real; C-7's 0.821
  too). Only C-2 (0.431) fires on depth — and cond was always its weak
  family, so no written reasoning rests on it.

**Decision this feeds (recommendation, recorded for the next build):** report
`famrank_cond` as two sub-signals — `cond_surf` rank and
`depth_to_base_surf` rank — instead of / alongside the max, because a
quarter of the cond-strong candidate population is depth-carried and the
max-rule materially mislabels them as conductivity evidence. Whether the
depth member should be *dropped* from the channel in gap-oriented builds is
a build question (measurably testable with the E9/E13/E14-SYS machinery:
an ablation `agreement-minus-depth-member` config); it was not run this
session.

### 8.4 Status changes this section forces

| candidate | before (session 5) | after (session 6) |
|---|---|---|
| **C-2 / C-8 / C-10** | "striping: test (a) uninformative either way; physical prior remains" | **stripe question CLOSED, negative**: prior corrected (§8.1) and no tie-scale crest lock on any band (§8.2). Magnetics standing: neutral. |
| **C-4** | "demotion basis invalidated (D-9); unresolved on magnetics" | **also NOT tie-stripe locked per E14** (the tmi_hg anomaly is below the pre-registered bar and non-replicating); magnetics no longer discounted. Cond pillar: single-profile "no conductor" refined to **multi-profile inconclusive** — never a raw high in any of 5 profiles (§8.3). Case still rests on grav/seis (0.90/0.93). |
| **C-8** | cond measured regional (single profile) | cond regional **confirmed on 5 profiles**; case rests on seis/strain/sourced-Holocene, unchanged in strength but now caveat-free. |
| **C-9** | cond rank-check only | cond regional **measured**; its "splay/step-over with fluids in the damage zone" reading (§6) loses the cond leg and rests on proximity + the sourced <130,000 Paradise Range zone. Tip-ray/step-over geometry check (E4) stays its open test. |
| **class framing** | "N–S class artefact-suspect" downgraded to physical prior | **retired** (§8.2); the E10(a)/E12/E14 chain lives in this file and `HYPOTHESES.md` as the record. |
