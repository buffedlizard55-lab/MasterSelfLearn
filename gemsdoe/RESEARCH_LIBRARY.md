# RESEARCH LIBRARY — fault detection for the GEMS Prize

Annotated, linked bibliography. Every entry was reached and read (at least to
abstract/method level) on **2026-09-26** unless marked carry-forward. Nothing
here is from model memory; each takeaway is what the cited source itself says.
Entries are grouped by the method family the session brief names.

Relevance key: ★★★ = directly usable as a candidate generator for
catalogue-missing faults; ★★ = strong supporting method; ★ = context.

---

## A. Competition ground truth, data and official baseline

### A1. GEMS Prize problem statement, metric and submission format ★★★
<https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/>
(read 2026-09-26, both chunks).
Defines: GeoDAWN region; provided features = surface conductivity + depth to
conductive base, detrended elevation + its slope, dilatation rate / shear
strain rate / second invariant of strain rate, isostatic gravity anomaly +
slope, RTP magnetic anomaly, TMI, vertical & horizontal slope of TMI,
top-of-crustal magnetic source depth, earthquake density; labels = USGS
Quaternary faults + INGENIOUS; external data allowed if licensed; links
`1m_DEM_links.csv` for 1 m DEMs; metric DTI α=0.2/β=0.8, R=300 m; submission
float32 GeoTIFF EPSG:32611 100 m. **The single most consequential sentence:**
test faults are *"faults that are not contained within the current public
USGS database"*, manually identified by experts.

### A2. Official rules (full document) ★★★
<https://www.nlr.gov/docs/fy26osti/96647.pdf> (all 7 chunks read 2026-09-26).
Verbatim extracts in `FIELD_AND_METRIC.md` §4. Key dates deferred to the
competition site per §1.2. Labels described in §3.3: training features at
100 m incl. GeoDAWN + "other publicly available geospatial features";
training labels from the INGENIOUS Great Basin compilation.

### A3. Official reference solution (U-Net MC-CV) ★★★
<https://github.com/drivendataorg/gems-prize-reference-solution> — notebook
read cell-by-cell this session. U-Net via `segmentation_models_pytorch`,
TverskyLoss(α=0.2, β=0.8), 5 Monte-Carlo splits, 128 px patches, augmentation
(crop/flip/rotate30), combined prediction, suggested threshold 0.1. It trains
**only on catalogue labels** — the ceiling of this exact recipe on hidden
faults is whatever generalisation it gets; beating it means adding
new-fault evidence or better recall geometry.

### A4. INGENIOUS Great Basin Regional Dataset Compilation (label source) ★★
Ayling, B., J. Faulds, et al. 2022. doi:10.15121/1881483 (citation as printed
in rules §3.3, which names it the source of the training labels). The GBCGE
project page: <https://gbcge.org/current-projects/ingenious/> (linked from
page 967; not independently fetched this session — flagged as link-only).

### A5. USGS Quaternary Fault and Fold Database (QFFDB) (catalogue source) ★★★
<https://www.usgs.gov/programs/earthquake-hazards/faults> (read 2026-09-26).
The catalogue the new faults are *absent from*: U.S. faults with Quaternary
(<1.6 Ma) coseismic surface deformation. The same page links a **slip
tendency / dilation tendency shapefile for Great Basin Quaternary faults** —
faults oriented to slip or dilate under the ambient stress field — a direct,
official, region-specific prior for which unmapped structures are most likely
active. (Rules §2/§3.3 name the QFFDB as the other label source.)

### A6. GeoDAWN data release (the survey itself) ★★★
Glen, J.M.G., and T.E. Earney, 2024, USGS data release, doi:10.5066/P93LGLVQ
(doi as printed in rules §2). DOE Geothermal Data Repository landing:
<https://gdr.openei.org/submissions/1591> (read 2026-09-26). High-resolution
aeromagnetic + aeroradiometric surveys, flown Nov 2021–Nov 2022 by EDCON-PRJ
under USGS contract (EarthMRI + DOE GTO), two overlapping survey areas across
the Walker Lane and northwestern Great Basin.

---

## B. Potential-field edge/lineament detection (gravity & magnetics)

### B1. Tilt-angle family on magnetics — TDR and TAHG, Zanjan case study ★★
<https://jesphys.ut.ac.ir/article_58910.html?lang=en> (read 2026-09-26).
Tilt angle = arctan(vertical-derivative / total-horizontal-derivative):
depth-insensitive, edges at zero crossings; TAHG (tilt of the total
horizontal gradient) equalises shallow/deep sources and puts maxima on edges;
used to map **basement faults hidden under thick sedimentary cover** — the
"buried fault" regime of Basin-and-Range basins.

### B2. Gravity lineaments via second horizontal derivative, Central Anatolia ★★
<https://link.springer.com/article/10.5047/eps.2011.04.003> (read 2026-09-26).
Edge operator from the second horizontal derivative of the truncated-plate
model; non-maximum suppression + double threshold; explicitly *"useful for
detecting deep faults even in the presence of shallower features."*

### B3. Method comparison — SVD vs tilt angle on gravity ★
<https://www.irejournals.com/formatedpaper/1703006.pdf> (read 2026-09-26).
Second vertical derivative enhances shallow edges; tilt balances depths; both
place edges at the same cardinal points in their test area. Useful for
choosing which derivative layers to stack.

### B4. Fault identification suite, Anza Basin (Kenya) — incl. iTilt ★★
<https://link.springer.com/article/10.1007/s44195-025-00085-x> (read 2026-09-26).
Compares 2nd-VDR, THDR, analytic signal, NVDR-THDR, Tilt-Euler and
**iTilt-Euler**; iTilt (Liu et al. 2015) divides VDR by the analytic-signal
amplitude to stabilise derivatives over stacked sources — the practical
choice where multiple fault generations overlap.

### B5. Integrated satellite-lineament + gravity edges, Gongola Basin ★
<https://www.sciencedirect.com/science/article/abs/pii/S2352938519303684>
(read 2026-09-26, abstract level).
Concordance of directional-filtered imagery lineaments (NW-SE, NE-SW) with
second-horizontal-derivative gravity edges; template for the multi-evidence
intersection approach in D5 of our metric analysis.

---

## C. DEM / LiDAR scarp detection

### C1. Regional scarp extraction by curvature template matching ★★★
Sare, B., et al. 2019, *JGR: Solid Earth*, doi:10.1029/2018JB016886.
<https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018JB016886>
(read 2026-09-26).
The most directly usable DEM method found: convolve directional DEM
curvature with the **curvature template of the diffusive scarp-degradation
model** (Hanks 2000 / Hilley et al. 2010), yielding per-pixel scarp amplitude
and misfit on ≤2 m DEMs over ≥100 km regions; validated against field-dated
scarps. Its in-paper context even reports that up to ~85% of swath pixels are
unmapped in the Q-faults DB around real scarps — the same completeness gap
this prize scores.

### C2. Utah Geological Survey — LiDAR as the fault-mapping tool ★★
<https://geology.utah.gov/map-pub/survey-notes/lidar-tool-for-geologists/>
(read 2026-09-26).
0.5 m bare-earth DEMs + slopeshade/hillshade reveal *"many previously unmapped
fault traces"*, incl. under vegetation and for non-N-S trends; slope-shade
manipulation is the practical trick for small scarps.

### C3. Scarps beneath dense canopy — Seattle fault zone ★★
<https://pugetsoundlidar.ess.washington.edu/harding.pdf> (read 2026-09-26).
1.5–10 m scarps invisible in the field/air photos, found in leaf-off LiDAR;
ground-return density is the resolving constraint. Justifies DEM-first
scanning in vegetated parts of the GeoDAWN footprint.

### C4. Active-trace identification from LiDAR DEM, Yangsan fault (Korea) ★
<https://www.mdpi.com/2072-4292/14/19/4838> (read 2026-09-26).
Scarp + deflected-stream signatures on 20 cm DEMs; distinguishes fault
valleys from fluvial valleys by linear continuity and connectivity — the
false-positive discipline a scarp miner needs.

### C5. ML scarp detection — review of U-Net-style approaches ★★
<https://www.ijres.org/papers/Volume-13/Issue-5/13052644.pdf> (read 2026-09-26).
Reviews automated scarp detection incl. a U-Net-like network for scarps
(cites Su et al. 2023) and VHSR-image rupture detection; positions DEM
morphometry + ML as the emerging standard. (Cited-paper details not fetched;
the review itself is the source of record here.)

---

## D. Geothermal fault-mapping methodology (official programme literature)

### D1. Play-fairway analysis, Brady's & Astor Pass (Great Basin) ★★★
Siler, D.L., and J.E. Faulds, 2013 (OSTI record; Science.gov landing:
<https://www.science.gov/topicpages/g/geothermal+system+exploration>, record
retrieved 2026-09-26). Permeability-potential model from **fault zone, minor
faults, and micro-earthquake activity**; heat model from gradients, springs,
alteration, He isotopes, magnetics. This is the DOE-blessed factor stack for
"where do fluids flow along faults" — the geothermal relevance filter the
prize cares about.

### D2. Great Basin play-fairway model — the 9-factor permeability/heat map ★★★
Faulds, J.E., et al. 2016, Stanford Geothermal Workshop paper:
<https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2016/Faulds1.pdf>
(read 2026-09-26).
Factors: recency of faulting, fault intersection/step-over geometry,
stress-field orientation (slip/dilation tendency), **earthquake density**,
gravity, 3 km temperature, geochemistry; fuzzy-logic + weights-of-evidence
integration; Quaternary faults = "intermediate permeability" tier. Note the
overlap with the competition's *provided* bands (strain rates, earthquake
density, gravity, conductivity): the feature stack was chosen to reproduce
exactly this methodology.

### D3. Blind-system discovery, southern Gabbs Valley (validation case) ★★★
<https://publications.mygeoenergynow.org/grc/1033921.pdf> (read 2026-09-26).
A **blind** (>130 °C, no surface expression in the catalogue) system found at
*multiple fault intersections in a displacement transfer zone*, flagged by
gravity + magnetic + MT, then confirmed by 2 m temperature holes (~120 °C at
150 m). Template for a high-value prediction: intersection/transfer-zone
candidates absent from the catalogue.

### D4. BRIDGE project — GeoDAWN magnetics + LiDAR fault picks, Hawthorne NV ★★★
<https://gdr.openei.org/files/1682/BRIDGE_README.pdf> (read 2026-09-26).
DOE GDR readme: **LiDAR fault picks + fault-ball dip directions, 2 m
temperature surveys, MT, gravity, GeoDAWN aeromagnetic derivatives, 3D joint
inversion**, and an explicit "geophysics sketchbook" correlating gravity,
magnetics, 2 m temperature, **LiDAR fault scarps** and HTEM resistivity.
Published inside the competition's own study region; the closest thing to an
official worked example of multi-physics fault discovery there.

### D5. GeoDAWN/GeoFlight survey programme — official DOE page ★★
<https://www.energy.gov/hgeo/geothermal/geoflight> (read 2026-09-26). DOE's
own framing: GeoDAWN data constrain *"geologic conditions and stress
regimes"* of the Salton Sea region, Walker Lane trough and western Great
Basin for geothermal discovery; GeoFlight continues it.

### D6. GeoDAWN GRC paper — young hidden faults in the magnetics ★★★
<https://publications.mygeoenergynow.org/grc/1034804.pdf> (read 2026-09-26).
USGS authors: near Battle Mountain, **young basin faults mapped from LiDAR
displace weakly magnetic basin fill, producing subtle anomalies visible in
GeoDAWN residual magnetics** (regional removed). Direct published evidence
that GeoDAWN magnetics + LiDAR see faults the existing compilation misses —
the exact class this prize scores.

---

## E. Method gaps still open (printed, not filled)

1. No published source yet located that scores **against this competition's
   private set** (by construction none exists); all transfer inferences above
   are ours and are labelled D1–D6 in `FIELD_AND_METRIC.md`.
2. The INGENIOUS project page (A4) is link-only this session; fetch next pass.
3. DrivenData community forum (<https://community.drivendata.org/c/gems-prize-challenge/111>)
   not yet read — likely contains official clarifications; fetch next session.
4. No peer-reviewed scarp-detection study *inside the GeoDAWN footprint*
   found this session (D6 is the nearest, Battle Mountain). Search again.
5. Competition data files themselves are behind the participant login of the
   confirmed account — nothing in this repo can yet run models (see README).
