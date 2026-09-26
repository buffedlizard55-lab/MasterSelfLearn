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
3. Run falsification tests (a)–(c) above along each trace.
4. Extend this file past the top six: there are 260 `new_to_catalogue`
   candidates and only 6 have written reasoning. The generator
   (`scripts/candidate_writeup.py`) should emit the SOURCED lookup per candidate
   automatically rather than have it done by hand.
