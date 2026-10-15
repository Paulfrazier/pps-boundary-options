# build/data: data foundation for the PPS boundary options (Phase 1a)

Built 2026-10-11/12. Everything here can be regenerated with `scripts/01..10` (run in numeric order, with the kit's `.venv`). The Census key is read at run time from `the CENSUS_API_KEY environment variable` and is never written to disk.

## Deliverables

| File | What it is |
|---|---|
| `schools.csv` | 83 rows: every K-5, K-8, 6-8 and 9-12 neighborhood school plus focus and alternative programs (Winterhaven, da Vinci, Richmond, Odyssey, ACCESS, MLC, Benson, Alliance). Columns: ids, lat/lon, capacity, 2025-26 enrollment by grade, the PSU neighborhood/DLI split, DLI strands, the modeled neighborhood kids, and PPS's 2031-32 projections under No change, A and B. |
| `boundaries/current_K-5_K-8.geojson`, `current_6-8.geojson`, `current_9-12.geojson`, `current_cells_all_levels.geojson` | Today's attendance areas. In the 9-12 file, the Jefferson dual-assignment zones are separate features with a `cluster_2025_26` field. |
| `blocks.parquet` / `blocks.csv` | The 9,295 blocks from `pps-model.json`, in the same order (`idx` = BL index, so `NB` adjacency still applies). Each block has: current schools at each level; calibrated kids by band (`k5`, `m68`, `h912`); the old `s_model`; the raw Census counts; the calibration factors; and assignments under the Status Quo 2027-28, A and B maps at every level, each with a `*_how` method flag. |
| `focus_dli.csv` | 41 programs: 35 DLI strands, plus Winterhaven, da Vinci, Odyssey, ACCESS, MLC and Benson. Each row has 2025-26 enrollment, an estimated by-grade split, the host building and the home-location assumption. |
| `focus_dli_homes.parquet` | Block x program matrix of estimated home locations (each column sums to the program's enrollment). |
| `scenarios.json` | Scenarios A and B at every level: closures and receivers, K-8 conversions, middle and high school changes, DLI and program moves with 2025-26 counts, renames, and block-level flows (from → to, kids). It also holds PPS's own per-school projections for 2027-28 to 2031-32 from the 82 Family Guides. |
| `scenario_maps/{status_quo,scenario_A,scenario_B}_{K-5,6-8,9-12}.geojson` | Labeled polygons digitized from PPS's 2027-28 map PDFs, including `scenario_A_6-8.geojson`. |
| `backtest.md` | The gate: modeled vs actual by school at every level. |
| `raw/` | Downloaded sources (listed below). `work/` holds intermediates. `scripts/` holds the code. |

## Sources (all downloaded 2026-10-11)

| Source | Used for | Vintage |
|---|---|---|
| `data/pps-map/pps-model.json` (read only) | Block universe (GEOID, centroid, pop, hu, `a`, `s`, NB) | Built Oct 2026 from 2020 Census |
| US Census 2020 DHC, API `api.census.gov/data/2020/dec/dhc`: P12 (sex by 5-year age) at **block** level and PCT12 (single year of age) at **tract** level, counties 41051/41067/41005 → `raw/census/` | Age bands | Census day 2020-04-01 |
| ODE Fall Membership 2025-26 (PPS Data Explorer, `data/raw/fall_membership_2025_26.xlsx`, sheet "School 20252026", Portland SD 1J) | Enrollment by school and grade | Oct 1 2025 |
| PSU Population Research Center, *PPS Enrollment Forecasts 2026-27 to 2035-36* (July 2026), Table 5.5 (PPS Data Explorer `pps_enrollment_forecast_2026.pdf` / `.csv`) | **Neighborhood vs DLI-program split by school** (2025-26), Odyssey/ACCESS counts, 10-year forecast | Historic 2025-26 |
| PPS *Enrollment Details for Language Immersion Schools*, Oct 2025 (PPS Data Explorer `pps_immersion_details_2526.json`) | Cross-check of DLI counts (it matches PRC within a few students) | Oct 2025 |
| PPS Data Explorer, `data/pps_schools.csv` (commit 80ec323, 2026-10-05) | NCES ids, lat/lon, LRFP 2021 functional capacity (and the "model" variant), seismic/URM, DLI languages | Mixed; capacity is 2021 |
| City of Portland `School_Boundaries` FeatureServer (`services.arcgis.com/quVN97tn06YNGj9s/.../School_Boundaries/FeatureServer/0`, 59 PPS cells, lastEdit 2025-11-03) → `raw/boundaries/` | **Current attendance areas** at all 3 levels | Identical in area (ratio 0.99992) to PPS's `PPS_Boundaries_All_Grades_22_23_DRAFT` service, whose layer is "PPS_Boundaries_All_Grades_23_24_FINAL" (board-approved SEGC lines in effect 2023-24 through 2025-26). Also saved. |
| PPS board memo *Rightsizing Update: Scenario Release* (Oct 5 2026) and 4 regional summaries (PPS Data Explorer `pps_rightsizing_board_2026-10-06/`) | Scenario structure | Oct 3-5 2026 |
| PPS **Family Guides**, one PDF per school (82), reached through the Awesome Table on `pps.net/.../rightsize/how-could-your-school-be-impacted`. Google Drive ids are in `raw/family_guides/index.tsv`. | Per-school proposals and PPS projections (No change / A / B, 2027-28 to 2031-32) | Oct 2026 |
| PPS attendance-area **map PDFs** (Status Quo/A/B x K-5/6-8/9-12, "School Year 2027-28"), BoardBook org 915, files 14505795-14505805, via `meetings.boardbook.org/Documents/DownloadPDF/<id>?org=915`. The A 6-8 map is also the user's Downloads copy. → `raw/scenario_maps/` | Digitized scenario lines | Model 2026-09-24, version 10/03/2026 |

The scenario-page Drive links (overview and regional) are the same documents as the BoardBook memo and summaries.

## Method

### Age bands (2020 DHC)
- P12 gives each block 5-9, 10-14 and 15-17. PCT12 single-year ages at the **tract** level split each band into single years.
- **Grade mapping.** On Census day (Apr 1), with a Sept 1 cutoff, grade g is 5/12 age g+5 and 7/12 age g+6. That gives these weights:
  - **K-5** = 5/12·age5 + ages 6-10 + 7/12·age11
  - **6-8** = 5/12·age11 + ages 12-13 + 7/12·age14
  - **9-12** = 5/12·age14 + ages 15-17 + 7/12·age18
  - Age 18 is not in the under-18 tables, so it is approximated by the age-17 count.
- **Smoothing.** Block-level DHC ages carry differential-privacy noise. Each block's raw count is therefore `block pop × (block-group band count ÷ block-group pop)`. This is the same smoothing the first-generation model's per-block student estimate (column `s` in `pps-model.json`) used, which we reverse-engineered: that estimate matches pop × the block-group under-18 rate within 0.8% dissimilarity.
- These are *where kids of grade age lived in 2020*, used as the spatial pattern for 2025-26. Cohorts are not aged forward, because families move as children age. Totals come from enrollment, so Census levels don't matter, only the spatial pattern.

### Targets (2025-26 neighborhood-program enrollment)
- **K-5 area.** The PRC Table 5.5 "Neighborhood" row where PRC splits out a DLI program. Otherwise ODE grades K-5. Special cases:
  - Hayhurst = 290. ODE's 508 includes Odyssey.
  - Cesar Chavez = 143 neighborhood K-8 × 273/443 = 88.
  - **Lent and Rigler**, whole-school Spanish DLI with their own areas, use their full K-5 enrollment (256, 291), as the old model did.
  - Bridger, Sunnyside and Buckman include their focus-lottery students. PPS doesn't publish that share.
- **6-8 area.** The PRC Neighborhood row for middle schools (Beaumont 315, George 249, Tubman 354, Harrison Park 308, Kellogg 330, Lane 411, Mt Tabor 208, Ockley Green 397, Roseway 415, West Sylvan 567). Otherwise ODE grades 6-8 (Gray, Hosford, Jackson, Sellwood, and the K-8s; Cesar Chavez = 55).
- **9-12.** PRC Neighborhood rows: Cleveland 1336, Franklin 1578, Grant 1809, Jefferson 377, Lincoln 1469, McDaniel 1325, Roosevelt 1082, Wells 1574 (total; Wells has no program split). Benson, MLC, Alliance and PISA are excluded.
  - In 2025-26 the "Jefferson / X" zones could choose Jefferson or X. Each X is therefore calibrated as a **cluster** (X-only cells plus Jefferson/X cells). Jefferson's 377 is spread across the three dual zones in proportion to their raw 9-12 counts and added to the cluster targets.
- **Calibration.** Each block's band count = raw × (area target ÷ area raw sum). The "capture factor" (`f_es`, `f_ms`, `f_hs`) stays with the block when lines move. Totals: K-5 14,372, 6-8 7,218, 9-12 10,550.

### K-5: why `k5` replaces `s` (and `s` is kept as `s_model`)
1. **2025-26 targets instead of 2024-25 NCES totals, and the published PRC neighborhood/DLI split instead of hand estimates.** The clear error this fixes: `s` gave **Hayhurst 451**, but 161 of those are Odyssey students (Odyssey is reported inside Hayhurst), so the right figure is 290. Clark's DLI was 72 in `s`; the actual is 91.
2. **Grade-specific ages (5-11) instead of all under-18 for the within-area distribution.** This is a small gain: uniform-rate MAPE 21.1% vs 21.4%.
- Net effect: total 14,372 vs 14,897. Areas differ from `s` by 6.6% MAPE, mostly the 2024-25 → 2025-26 decline.

### Digitizing the scenario maps
- **The PDFs are vector, so no raster tracing was needed.** Boundary lines are distinct styled paths: K-5 gold 3pt, 6-8 teal 3pt, 9-12 blue 11pt. K-8 lines are dashed maroon.
- **Georeferencing.** One affine PDF→EPSG:2913 transform for all nine maps, which share the identical sheet layout:
  - Start from 24 school-label positions matched to school coordinates.
  - Refine by ICP of the Status-Quo 6-8 lines against today's middle-school lines.
  - Residual: median 71 ft, p90 143 ft. Scale is 27.88 ft/pt on both axes.
- **Labeling.** Each polygon is named by regex on the label words it contains ("X K-5 Neighborhood", "X Middle School", "X High School"). Whole-school DLI schools (Lent, Rigler, Cesar Chavez, Richmond) never take a neighborhood label. Two unlabeled polygons (West Sylvan and Lincoln, whose labels sit outside their own polygons) are named by the majority current school of their blocks.
- **Block assignment.** Each block goes to the smallest digitized polygon containing its centroid. Fallbacks, with the method in `*_how`:
  - `k8_rule`: K-8 areas are drawn dashed and not digitized, so those blocks keep their K-8. That means today's 9 K-8s in the Status Quo, and Astor and Skyline in A/B.
  - `bybee_rule`: in A/B, Faubion's Bybee Lake Shelter blocks → Astor.
  - `skyline_rule`: Skyline area is inset-only. 9-12 = Lincoln in SQ, Roosevelt in A/B.
  - `nearest`: 5-115 sliver blocks per map along rivers and gaps.
- **QA against today.** Status-Quo K-5 agrees with current lines on 99.9% of blocks. 6-8 agrees on 98.7%; all 100 disagreements are the Rigler K-5 area, which the 2027-28 SQ map draws in Roseway Heights while the 2023-24 layer has Beaumont. We kept Beaumont for "today" because it fits enrollment better (backtest.md). 9-12 agrees except the dual zones, which the 2027-28 map shows as Jefferson-only. That is the phase-in of Jefferson's own boundary, which the Grant family guide confirms ("ending of Dual Assignment").
- Because the maps digitized reliably, this is a real **polygon** digitization, not block-rule reconstruction. The polygon GeoJSONs omit K-8 dashed areas and the Skyline inset, so `blocks.parquet` is the authoritative assignment.

### focus_dli home locations (assumption, not published)
- Strand homes are proportional to Census band residents (`raw_*`) in the host school's **2025-26 HS cluster**. PPS gives DLI lottery priority to the neighborhood, then the cluster.
- Exceptions:
  - Japanese DLI (Richmond, Mt Tabor, Grant), Cleveland Mandarin and all focus programs are district-wide.
  - Lent and Rigler use their own area, and their students are already inside the block `k5` counts. Don't double count them.
- By-grade counts = strand total × the host school's ODE grade distribution within the band. PPS publishes DLI counts by school and program, not by grade.

## Assumptions the solver must know
1. **Block kids are neighborhood-program kids only.** DLI-strand and focus students are separate fixed populations (`focus_dli.csv`); Lent and Rigler are the exception (item 3). To close Winterhaven or da Vinci (option 3), add their `focus_dli_homes` columns to the blocks.
2. **Capture factors move with blocks.** A moved block brings its old area's enrollment propensity. The out-of-sample error of predicting a school from Census alone is about 21-23% MAPE at K-5 and about 27% at 6-8 (17% when carrying K-5 factors), so treat sizes within ~15% of 360/500/1,100 as uncertain.
3. **Lent and Rigler areas are whole-school DLI.** Their `k5` (256 and 291) is all DLI students. Under A/B, Lent's area goes to Kelly and Rigler's to Scott, but PPS's own projections imply nearly all of those students stay with the DLI program: Kelly A gains about 5, and Scott A = 512 in 2027-28, not the ~755 a naive block sum gives. Treat these blocks (`es_cur` in {Lent, Rigler}) as DLI kids that follow the program unless you deliberately model otherwise.
4. **Sunnyside, Bridger and Buckman `k5`/`m68` include focus-lottery students** (capture 0.84-1.23). Under A/B, Sunnyside's focus ends and Buckman's arts program closes, so those areas' factors are probably too high for future years.
5. **The basis is 2025-26.** PPS's projections are for 2031-32 (district K-5 down about 9%); scale by year if needed. `schools.csv` has PRC's 2031-32 forecast and PPS's 2031-32 scenario projections.
6. **9-12 "current"** is the cluster (`hs_cluster_cur`) with the dual zones pooled; `hs_zone_cur` keeps the raw zone. For future-year HS work use `sq_hs`, where Jefferson has its own area.
7. **Names.**
   - K-5 uses `pps-model.json` names; Lee = **Sunrise**.
   - Middle schools use City layer names: Lane = **Brentwood**, Tubman = Harriet Tubman, Gray = Robert Gray.
   - "Ida B. Wells" = Ida B. Wells-Barnett.
8. **Middle-school areas follow elementary areas** in the current layer, except where the City cells split Bridlemile (Gray/West Sylvan), Faubion (2 HS), Vestal, Whitman, Woodmere and Woodstock (HS splits). Feeder cleanliness can be built on whole elementary areas.

## Biggest gaps
- **Where DLI and focus students live is not published.** Their homes are an assumption (cluster- or district-proportional).
- **The focus-lottery share** at Sunnyside, Bridger and Buckman is unknown, and so are transfer in/out flows by school. That is the main driver of the 20%+ structural error.
- **DLI counts exist only by school and program, not by grade.** The grade split is estimated.
- **Capacity is the LRFP 2021 functional capacity.** PPS Data Explorer's "model" capacity differs for about 10 schools, and both are given. The family guides cite slightly different "can hold" numbers (Arleta 653 vs 696; Abernethy 441 vs 522; Hosford n/a), so PPS's current capacity model isn't public.
- **ACCESS isn't a separate ODE school** (PRC: 324), and its grade split is unknown.
- **Clark has no NCES id** in CCD 2022 because it opened in 2023.
- **K-8 dashed lines weren't digitized as polygons.** The blocks use rules instead, which matter only for Astor's Bybee Lake gain (5 blocks).
