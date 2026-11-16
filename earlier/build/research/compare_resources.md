# Our PPS boundary kit vs. four public rightsizing resources

Compiled 2026-10-12. Each site was read as data. I fetched the pages, their embedded JSON and their GitHub repos where public. "Ours" means this kit: `build/data/schools.csv`, `blocks.parquet`, `build/routing/walk_miles.parquet` and `build/solver/out/`. Scratch extracts were kept out of the repo.

## The four resources

| Name you gave | Identified as | URL | Made by (as stated) | Last updated |
|---|---|---|---|---|
| Portland Public Schools Data Explorer | **PPS Data Explorer** | https://ppsdata.info/ (source: https://github.com/meub/pps-data) | "independent personal project" | Not shown on the page. HTTP Last-Modified 2026-10-12 16:17 UTC; last repo commit 2026-10-12 |
| PPS School Explorer | **PPS School Explorer: PPS attendance boundaries** | https://pps-explorer.codedaily.workers.dev/ | Independent; author named on the site | Not shown. Its data JS is current with the Oct 6 memo |
| PPS Closure Commutes | **PPS Closure Commutes: How much farther is school?** | https://chrisloer.github.io/pps-closures/ (Felt maps linked from the page) | No name on the page ("Independent analysis"). "Made with Felt ... driven by Claude through the Felt MCP server" | Not shown. HTTP Last-Modified 2026-10-11 16:39 UTC |
| rightsizepdx.com | **Right Size Portland** (scenario explorer) | https://rightsizepdx.com/ → `rightsizing-scenario-explorer.html` (source: https://github.com/southie/ppsrightsize) | "an independent project"; contact@rightsizepdx.com | Not shown. HTTP Last-Modified 2026-10-12 16:52 UTC |

| *(added 2026-10-12, Paul's follow-up)* PPS DLI explorer | **PPS Dual Language Immersion & Rightsizing** (Quarto site, English and Spanish) | https://pps-dli-explorer.netlify.app/ (source: https://github.com/jminnier/pps-dli-explorer, no license file) | No name on the site ("an independent analysis, not a PPS publication"). Its README says it builds on pps-explorer | Not shown. Last repo commit 2026-10-12 02:53 UTC |

All five are confidently identified.
- Right Size Portland's "Related" links name three of the others ("ppsdata.info (PPS Data Explorer) · pps-explorer (attendance-boundary explorer) · PPS Closure Commutes (walk, bike and drive time by closure)").
- Closure Commutes, the School Explorer and the DLI explorer all credit ppsdata.info / PPS Data Explorer.
- The DLI explorer uses the PPS School Explorer's tracings and memo transcription.

**All five share one data spine (PPS Data Explorer plus the School Explorer's traced maps), and so do we** (PPS Data Explorer plus our own independent tracing).

**URL re-check (2026-10-12).** Each URL Paul gave returns HTTP 200:
- https://ppsdata.info/
- https://pps-explorer.codedaily.workers.dev/#s=sq&g=k5 (the hash only sets the view to Status quo, K-5)
- https://chrisloer.github.io/pps-closures/
- https://rightsizepdx.com/ (redirects with JavaScript and meta-refresh to `rightsizing-scenario-explorer.html`, keeping `#custom=` links)
- https://pps-dli-explorer.netlify.app/

---

## Headline findings

1. **The Chávez question is already answered by PPS text we hold.** PLAN.md "Open items" says no PPS text says Chávez becomes immersion-only. It does. The Oct 6 board memo, which we already have at `build/data/raw/meub-pps-data/data/raw/pps_rightsizing_board_2026-10-06/Rightsizing_Update_Scenario_Release_Board_Memo.pdf`, p. 3, says: *"César Chávez would become a K–5 Spanish immersion hub, with non-immersion K–5 students assigned to Rosa Parks and middle grades to George."* Our extracted family guide (`build/pps-texts/family-guide-cesar-chavez.md`) also says: *"César Chávez would change from a K-8 to a focused K-5 regional Spanish DLI school ... Neighborhood (non-DLI) K-5 students would move to Rosa Parks K-5."* The map's "immersion only" label is therefore correct. Only the "≈645" count needs replacing (PPS A 2031-32 = 527; ours = 558).
2. **Our traced Scenario A/B lines agree with the PPS School Explorer's independent tracing on 99.6-99.9% of kids** at every level and scenario. I point-in-polygon tested all 9,295 block centroids against its 9 GeoJSONs. The one material difference, 524 K-5 kids, is a label rather than a line: PPS draws Kelly and Lent (and Scott and Rigler) inside one shared polygon. He names it "Lent" with `unclear_between: [Kelly, Lent]`; we give it to Kelly. That gives us strong independent validation of `scenario_maps/`.
3. **The biggest number gaps come from definitions, not errors.**
   - Closure Commutes counts only students who **live in the area and attend its neighborhood program**: Sabin 215 vs our 270, Irvington 212 vs 259, Peninsula 195 vs 239, Buckman 133 vs 283, Woodmere 141 vs 226. Ours is the school's whole neighborhood-program enrollment, including transfers in.
   - Our Scenario A 2031-32 sizes for **Hosford (669 vs PPS 557, +20%)**, **Roseway Heights (746 vs 628, +19%)** and **Sunnyside (417 vs 235)** are off from PPS. Right Size Portland lands near PPS on Hosford (548) and Roseway (643). Likely causes: we carry Sunnyside's focus-lottery capture into its moved 6-8 kids, and we may double-count DLI at Roseway.
4. **Closure walk distances agree.** On closure-area walks, all three routed sources (ours on OSRM, Right Size Portland on an OSM 40 m grid, Closure Commutes on Valhalla/H3) are within about 10% on average walk. The only >10% gap is Closure Commutes' "% beyond 1 mile" for Peninsula (58% vs our 75%). It uses Valhalla minutes, which it says itself run about 14% shorter than OSRM.
5. **Update (follow-up): the PPS capture-rate reports are found.** They are already parsed (Oct 2019 → Oct 2025) in the DLI explorer's public repo, along with PPS 2025-26 capacities, DLI by grade and the family-guide "within 1 mile" figures. See §5 and the conclusions table below.
6. **Data worth adding:**
   - PPS's **capture-rate / "Enrollment Summary by K-12 Students' Neighborhood and Type of School Attended"** reports. These are in-area residents by where they attend, the thing our backtest says is our main error source.
   - PSU low/high forecast bands.
   - The **Lent-area → Marysville** non-immersion flow (115 students).
   - Right Size Portland's busing, staffing and building-cost layers, if we want cost metrics.

---

## 1. PPS Data Explorer (ppsdata.info)

**What it is.** A dashboard of the 74 in-scope PPS schools. It has a Scenarios tab (A/B closures and receivers), a utilization map, enrollment trends from 2018, a PRC 2035-36 forecast, seismic data, a "Transportation" tab, DLI shares, a "Students per grade at a receiving school" model, a sortable table and charters. Methodology: https://ppsdata.info/#section-methodology.

**Data sources (as listed on the site and in the repo)**
- Enrollment: ODE Fall Membership 2025-26, with 2022-23 to 2024-25 now added (`data/exports/pps_enrollment_by_grade_2022-23_to_2025-26.csv`), and NCES CCD 2018-2023. Hayhurst and Odyssey use PSU's split (Hayhurst 290, Odyssey 217).
- DLI: PPS *Enrollment Details for Language Immersion Schools*, Oct 2025, now with `dli_by_language` (Franklin Spanish 173 / Russian 29, for example).
- Capacity: LRFP 2021 functional capacity, plus "functional_capacity_model" from a recovered PPS utilization workbook. Since our snapshot it has a `capacity_source` column, and MLC now takes its capacity from the workbook.
- Forecast: PSU PRC July 2026, Table 5.5, medium. Low/high per school are **synthesized** as medium × the district low/medium ratio for the grade band (K-5 ×0.93 / ×1.11; 6-8 ×0.90 / ×1.07).
- Boundaries: City of Portland attendance areas.
- Scenarios: PPS scenario comparison (Oct 4) and board memo receivers (`data/exports/pps_rightsizing_receiving_schools.csv`, new).
- Distance: OSRM **driving** distance and time to the nearest same-level school, for the 20 lowest-enrollment schools only.
- Demographics: CRDC, ODE At-a-Glance and OSAS.
- Housing: Metro BLI 2045, the Oregon affordable-housing inventory and BDS permits.
- Seismic: Holmes 2024 assessment.

**Scenario model.** `scripts/rightsizing_model.py` holds fall-2025 ODE enrollment fixed and moves whole closing schools to the memo's receivers by strand. Sellwood MS splits 50/50 to Hosford/Lane. It does **not** model attendance-boundary changes. Its `EXTRA_FLOWS` has "César Chávez non-immersion K-5 students to Rosa Parks (board memo)".

**Overlap with ours.** Near total: we built on its commit 80ec323 (Oct 5). Since then it has changed:
- `pps_schools.csv`: a new `capacity_source` column; values unchanged for our schools.
- `pps_immersion_details_2526.json`: adds a per-language split.
- Three earlier ODE years, which could give us a trend-based check on capture.
- A receivers CSV.
- Synthesized per-school low/high forecast bands.

None changes a number we use. The multi-year ODE file and the per-language DLI split are cheap upgrades.

**Spot checks.** Identical to ours wherever both have the number: 2025-26 totals, PSU neighborhood/DLI split, LRFP capacity, utilization and PSU 2031-32 (table below). Its "nearest alternative" is a **drive** to the nearest school, not to the receiver: Sabin → Alameda 0.86 mi, Irvington → Sabin 0.97 mi, Peninsula → Rosa Parks 1.09 mi / 4.6 min. It is not comparable to our walk metrics.

**PPS district measures it republishes** (PPS, 2031-32): schools above threshold SQ 26% / A 67% / B 57%; students in such schools 48% / 80% / 73%; "students who would change schools" A 27% / B 24%.
- **Our official-line baselines reproduce these closely:** buildings at or above floor SQ 28% / A 71% / B 58%; students in them 50% / 82% / 74%.
- Ours counts every zoned and program building in `baselines/*/schools.csv`, so the denominators differ slightly.

**Chávez/Lent/Rigler.**
- Chávez: "Program move: Spanish: Beach, James John, and Sitton to Cesar Chavez; Program move: Chavez 6–8 and Ockley Green MS to George MS; Grade change: Chavez 6-8 to George". The model moves non-immersion K-5 to Rosa Parks.
- Lent: neighborhood 0 / DLI 256 ("Program move: Atkinson to Lent; Attendance boundary changes").
- Rigler: neighborhood 2 / DLI 289 ("Program move: Scott to Rigler").
- Source: https://ppsdata.info/data.json.

**Worth borrowing / avoid**
- Borrow: the class-count view at receiving schools (strand × grade ÷ class-size target), a concrete "does it fit" check our scorecard lacks, and the synthesized low/high bands as a robustness check.
- Avoid: its scenario model ignores boundary changes. Its own caveat: "a receiving school that also loses area will look fuller here than it would be".

---

## 2. PPS School Explorer

**What it is.** An address-lookup map of Status Quo / A / B attendance areas at K-5, 6-8 and 9-12. It has a today's-lines overlay, "where students from closing schools go" arrows, immersion rings with a "Spanish immersion: 1-mile reach" layer, and six languages. URL: https://pps-explorer.codedaily.workers.dev/.

**Data sources**
- Boundaries: traced from the vector paths of PPS's Oct 6 2027-28 scenario map PDFs (BoardBook agenda item 8), "placed ... using the map coordinates inside those PDFs, so lines are accurate to a few meters". It checks against City of Portland data: "Today's areas match City of Portland data for 98% of the district."
- School changes: the Oct 6 board memo, each tagged `source:"memo"`.
- No enrollment, capacity or forecast. The only numbers are PPS's district measures, such as "PPS expects 48% of students to be in a school big enough to stay strong by 2031–32."
- DLI reach: straight-line 1-mile circles around Spanish K-5 DLI sites.
- Data: `/data/{sq,a,b}_{k5,68,912}.geojson`, `/data/dli_reach.json`.

**Overlap.**
- Same source PDFs as our `scenario_maps/`, digitized independently.
- **Agreement with our block assignments (kid-weighted):**
  - SQ: K-5 99.8%, 6-8 99.9%, 9-12 99.9%
  - A: K-5 96.3% (99.9% excluding the Kelly/Lent label), 6-8 99.8%, 9-12 99.9%
  - B: K-5 96.2% (likewise), 6-8 99.8%, 9-12 99.9%
- Residual differences are 1-10 kids, mostly Duniway/Lewis and Lincoln/Wells slivers.
- Method: block centroids in its polygons vs `blocks.parquet` `sq_*`, `A_*`, `B_*`.

**Sources we don't have.** None for numbers. Its DLI reach layer is a new metric (`dli_reach.json`): Spanish K-5 DLI sites go from 10 (2022) to 9 (today) to **4 under A and B** (Ainsworth, César Chávez, Lent, Rigler). The share of PPS land within 1 straight-line mile of one drops from 16.4% to **8.5%**.

**Chávez/Lent/Rigler (verbatim, https://pps-explorer.codedaily.workers.dev/, JS bundle `assets/index-CzMeLJCe.js`):**
- Legend: "Immersion only: no neighborhood area"
- K-5 note: "Rigler, Kelly and César Chávez do not close. César Chávez's area goes to Rosa Parks. PPS's maps put Rigler and Scott, and Kelly and Lent, inside shared boundaries. PPS has not said which school serves each area."
- Change list (source: memo): "César Chávez becomes the main K–5 Spanish immersion school. Its K–5 students who are not in immersion go to Rosa Parks."
- DLI note: "PPS does not share where immersion students live. An older PPS note says immersion buses outside a school's own area are only for native Spanish speakers. Bridger's Spanish immersion moved to Lent in fall 2023."
- Polygon properties: Lent `unclear_between: ["Kelly","Lent"]`; Scott `unclear_between: ["Rigler","Scott"]`.

**Worth borrowing.**
- The DLI-reach metric. Option 2 ("DLI stays put") could report "% of homes within 1 mi of a Spanish K-5 DLI site", ideally network-based, using our walk matrix.
- Flagging ambiguous shared polygons explicitly, as `unclear_between` does, rather than silently picking one school.
- Multilingual UI for the final map.

---

## 3. PPS Closure Commutes

**What it is.** Per-closure change in walk, bike and drive time for families in each closing school's area. It covers K-5 closures plus the middle-school moves, under PPS's lines and four alternative boundary rules. URL: https://chrisloer.github.io/pps-closures/ (data: `data.json`, `boundaries.json`).

**Data sources (from its "How this was built")**
- Boundaries: PPS Oct 6 map PDFs, georeferenced to the City School Boundaries service (edited Nov 3 2025) by labels then ICP (median 0.6 ft). Erased and new lines are applied to current GIS polygons.
  - Receivers come from the memo; two-way splits go by shorter average walk.
  - Checked against the memo's splits: Maplewood 66/34 (memo 70/30), Stephenson 72/28 (70/30), Buckman 56/44 (50/50).
  - Only 2 of the ~30 open-school boundary shifts are modeled (Duniway → Llewellyn in A, Whitman → Lewis in B).
- Students: **"PPS's October 2025 enrollment summary counts, for every school, the students who live in its own neighborhood and attend its neighborhood program ... they leave out students who transfer in from other neighborhoods and students in immersion programs."** K-8s are split by ODE grade enrollment.
- Spatial spread: 2020 DHC P12 blocks (K-5 = 5-9 + 1/5 of 10-14; 6-8 = 3/5 of 10-14), on H3 res-9 hexes (~0.1 km²).
- Travel: Felt `isochrone()` on self-hosted Valhalla, about 4,100 nested isochrones.
  - Walk at about 5.1 km/h (19 min/mi). The 1-mile and 1.5-mile bus thresholds are proxied as 18.9 and 28.4 minutes.
  - Drive is free-flow and stands in for the bus.
  - Cross-checks: vs OSRM drive r = 0.96 (Valhalla about 19% shorter); walk/bike vs OSRM r = 0.996 / 0.994 (Valhalla about 14% shorter).
- Capacity: LRFP 2021. **Year: 2025-26 only, no forecast** ("PPS's own figures use 2031–32 projections and will differ").

**Overlap.** Same Census table and same City layer. It uses PPS Data Explorer for roster, capacity and DLI. Like us, it routes on the OSM network.

**Sources we don't have.**
- (a) The PPS **in-area / own-neighborhood-program counts** by school. We use total neighborhood-program enrollment.
- (b) A Lent-area fact: "non-immersion students from the Lent area attend Marysville today (115 of them in October 2025), and the slides send them to Kelly."

**Alternative boundary rules it tests** (all close the same schools):
- PPS plan
- PPS rules, shortest trips (at most 2 receivers, near capacity)
- Shortest walks within capacity (an LP at 95% of functional capacity, any number of receivers)
- Nearest open school (capacity ignored)
- Whole school to one receiver

This parallels our options 1/4. Its headline numbers (A, PPS plan, 2025-26 in-area students):
- K-5: 2,710 students move; average walk 13.7 → 22.4 min; 1,174 newly over the 1-mile walk proxy.
- 6-8: 1,720 move; 23.2 → 38.2 min; 635 newly over 1.5 mi.
- B: K-5 2,068 move; 6-8 1,720.
- Schools at threshold on 2025-26 loads: now K-5 14/53, MS 6/23 → A K-5 28/40, MS 12/15.

**Chávez/Lent/Rigler (verbatim, https://chrisloer.github.io/pps-closures/, "Special cases"):**
> "Lent enrolls only Spanish immersion students; non-immersion students from the Lent area attend Marysville today (115 of them in October 2025), and the slides send them to Kelly. Rigler is also a whole-school Spanish immersion program, but most of its students live in its neighborhood, so it is treated as that neighborhood's school. César Chávez becomes a Spanish immersion hub, so its neighborhood K–5 students go to Rosa Parks."

Its data has Chávez as a closure-like source: 61 K-5 students → Rosa Parks (walk 11.8 → 14.1 min), and 38 6-8 students → George.

> "At the closing schools alone, 238 immersion students live in the school's own neighborhood (73 at Beach, 96 at James John, 69 at Rose City Park)"

**Worth borrowing / avoid**
- Borrow: its alternative-rule ladder (especially "nearest open school, capacity ignored" as a floor and "whole school to one receiver" as a cohesion benchmark). It is a cheap way to bracket our options.
- Borrow: the memo-split check (rebuilt shares vs the memo's 70/30 and 50/50). We should report the same for our A baseline.
- Borrow: the "student-minutes" weighting.
- Avoid: treating Rigler-area kids as neighborhood kids. PSU (2 neighborhood / 289 DLI) and the Rigler family guide ("Rigler's non-DLI neighborhood boundary would shift to Scott K-5") both say otherwise. Our `lr_nbhd_share` = 2% matches PSU.
- Avoid: drive time as a bus-time proxy. Its own text says "Real bus rides are longer."

---

## 4. Right Size Portland (rightsizepdx.com)

**What it is.** The most complete of the four. It has a scenario explorer with a **year-by-year enrollment model 2025-26 → 2035-36** for SQ, A, B and user-built custom scenarios (closing or keeping schools via right-click, with shareable `#custom=` links), PPS's published measures reproduced by region, commute distributions, a yellow-bus route model and busing cost, a staffing-formula model, building and repair costs, assessor land values, and private, homeschool and virtual school context. URL: https://rightsizepdx.com/rightsizing-scenario-explorer.html.

**Data sources (its NOTES and assumptions, verbatim where quoted)**
- Map, receivers and shares: "come from the pps-data repository".
- Published measures: "PPS regional summaries (Status Quo, A, B for 2031-32) and the district scenario overview (October 4, 2026)."
- SQ enrollment: "PSU 2026-27 enrollment forecast, Table 5.5 (medium scenario); 2025-26 is actual."
- Scenario enrollment: "the feeder model built from the scenario feeder files, applied from 2027-28. Tested at 2031-32 against PPS's published measures: it matches the district and most regions exactly."
  - K-8 → K-5 keeps the school's own ODE K-5 share.
  - Immersion moves with PSU Table 5.5 program rows.
  - 6-8 reassignment is by each feeder's share of K-5 neighborhood enrollment.
  - A "Census boundary adjustment" applies the 2020-Census share of residents in moved areas to the sender's neighborhood students.
  - "Not modelled (no published size): Duniway southern boundary to Llewellyn, Lent non-DLI students to Kelly, Lewis receiving part of Whitman (B), Creston Deaf and Hard of Hearing to Glencoe, MLC 9-12 ..."
- Capacity: "PPS 2021 Long-Range Facility Plan ... Harrison Park uses the LRFP figure (PPS's operational model differs)". That is 1,006; we use 890.
- Boundaries: the PPS School Explorer's tracings (above).
- Getting to school: OSM shortest paths from Census residents on a 40 m grid, at walk 3 mph and bike 10 mph. Drive is scaled ×1.24 to match OSRM. Bus distance follows ORS 327.043, 1 mi K-5 and 1.5 mi 6-12, "measured along the walking route".
- Also:
  - an OR-Tools bus-route model (293 routes, 449 runs, 129 buses)
  - the PPS 2026-27 staffing formula
  - LRFP FCI and Holmes seismic costs (Turner-indexed)
  - Multnomah assessor RMV
  - NCES PSS private schools
  - ODE homeschool registrations, ODE virtual enrollment
  - PSU Table 3.2 private share and Table 5.2 by grade
  - the OSRM public drive matrix

**Overlap.** The same PSU Table 5.5, LRFP capacity, ODE and DLI counts. Its 2031-32 SQ numbers are identical to our `forecast_2031_32_prc`. It also traces boundaries and uses DHC P12 for spatial spread.

**Sources we don't have (candidates):**
- PSU Table 5.2 by **grade** to 20 years, and Table 3.2 private-school share.
- The 2026-27 adopted budget: Student Transportation (function 2550), O&M of plant ($72.4M, about $8.05/sq ft) and the staffing formula.
- Posted PPS bus routes and stops.
- Holmes 2024 per-campus seismic costs (PPS Data Explorer has these) and LRFP FCI.
- Assessor land values.
- PPS 2026-27 bell times.

**Chávez/Lent/Rigler.**
- Lent: "Not modelled ... Lent non-DLI students to Kelly". Its Kelly A 2031-32 stays at 391, while PPS says 401.
- Its Chávez A 2031-32 = **578**, util 98% (PPS 527; ours 558). It lists no Chávez → Rosa Parks receiver, so Chávez's neighborhood K-5 appear to stay at Chávez in its model.
- Rigler A = 544, matching ours exactly; Lent A = 457, also matching ours exactly. Both of us use the same PSU program rows; PPS has 505 and 421.

Source: embedded `const D` in https://rightsizepdx.com/rightsizing-scenario-explorer.html. I found no prose about Chávez being immersion-only.

**Worth borrowing / avoid**
- Borrow: **year-by-year sizes 2025-26 → 2035-36 per school under each scenario**. We only have district-level PSU ratios for durability. The same per-school-by-year logic (PSU Table 5.5 annual rows, which stop at 2035-36) would make our durability check per-area rather than uniform.
- Borrow: the "matches PPS's published measures" test, district and region. We already match district-level within 1-4 points and should add the regional breakdown.
- Borrow: bus distance measured along the walking route, as we do. Also its note that at a 1-mile 6-8 threshold "about 2,900 more 6-8 residents would count", a useful sensitivity for our bus-eligible metric.
- Borrow (stretch): bus-cost and staffing-formula models, if the trade-off write-up wants dollars.
- Avoid: no Chávez → Rosa Parks flow and no Lent → Kelly flow (stated). Rosa Parks and Kelly are therefore slightly undercounted, and Chávez overcounted.

---

## 5. PPS Dual Language Immersion & Rightsizing (pps-dli-explorer)

**What it is.** A DLI-focused analysis site, in English and Spanish. URL: https://pps-dli-explorer.netlify.app/. Pages:
- Overview
- Demand & scorecard (`scorecard.html`)
- Equity (`equity.html`)
- School changes (`schools.html`)
- Lent & Chávez (`history.html`)
- Whole-school vs strand research (`research.html`)
- Sources & methods (`methods.html`)

It is reproducible from its repo: R and Python parsers, with every source PDF saved in `data-raw/` and cleaned tables in `data/`.

**Data sources** (repo README and methods page). It adds a lot of PPS primary data we don't have:
- **PPS Neighborhood Capture Rate Metrics**, Oct 2019 → Oct 2025 (`data/capture_rate.csv`): "Enrollment Summary by K-12 Students' Neighborhood and Type of School Attended". This is the report we looked for and couldn't reach on the old pps.net URLs. The 2024-25 and 2025-26 editions are on PPS's Data & Reporting page, earlier years on its archive page.
- PPS *School Enrollment by Neighborhood of Residence*, Oct 2023 → Oct 2025.
- **PPS *Enrollment by Grade and Program Type*, Oct 2024 and Oct 2025.** This gives **DLI enrollment by grade** (`enrollment_by_program_grade.csv`). Our README lists that as a gap; we estimate it.
- PPS *Language Immersion Track Profiles*, Oct 2021 → Oct 2025, and *Enrollment by Language and School*.
- PPS kindergarten lottery results 2022-23 → 2026-27: applications, offers and waitlists by program.
- **PPS School Profiles 2025-26** (Power BI): current functional capacity, utilization, capture rate (`school_profiles_2025.csv`, retrieved Oct 9 2026).
- PPS family guides, parsed (`guide_school.csv`, `guide_enrollment.csv`), including PPS's per-school "Students living within 1 mile" and "meets space use goal".
- PPS Enrollment Summary by Race and Ethnicity (program rows), class size detail, and board slide 44 (subgroup move rates).
- PSU forecasts (2022-23, 2023-24 and 2026-27 editions).
- ACS 2020-24 C16001/B16007 (language spoken at home) spread to 2020 blocks.
- LRFP 2021 capacity (via PPS Data Explorer), Title I and SUN school lists, and an unofficial 2026-27 SPED allocation sheet.
- Scenario maps and memo transcription from pps-explorer.
- Distance: **straight-line** (1-mile reach of a K-5 Spanish site; home-to-school distance estimates).

**Overlap with ours.**
- **DLI strand totals match `build/data/focus_dli.csv` exactly** for all 32 strand rows (Ainsworth 287, Atkinson 178, Beach 155, Beaumont 101, Chávez 300, Kelly Russian 143, Scott 222, Sitton 138, and so on). Their program-and-grade file treats Lent, Rigler and Richmond as "Whole School" rows.
- **Their DLI move list matches targets.md "Scenario-A facts" item 6 one for one:** Scott→Rigler; Beaumont 6-8→Roseway; Clark→Woodstock; Atkinson→Lent; Beach, James John and Sitton→Chávez; Ockley Green 6-8→George; MLK→Boise-Eliot/Humboldt; RCP Vietnamese→Vestal (A only); Chávez 6-8→George.

**Spot checks vs ours (flags >10%)**

| Item | Theirs (PPS source) | Ours | Flag / reason |
|---|---|---|---|
| Chávez Spanish DLI split, Oct 2025 | K-5 **195** / 6-8 **105** (PPS Enrollment by Grade and Program Type) | K-5 ≈185 / 6-8 ≈115 (split by ODE grade mix, METHOD §1); targets.md gap #8 guessed "≈1/3 of 295" | Within 10%. The actual split is now published |
| Chávez neighborhood program, Oct 2025 | K-5 **78** / 6-8 **65** (total 143) | K-5 **88** / 6-8 **55** | 6-8 −15%, K-5 +13%: we split 143 by the whole school's grade mix; the actual neighborhood program is older-skewed |
| Students in moving DLI programs, Scenario A | **1,586** (Oct 2025, grades that move) | **1,567** DLI kids moved (2031-32 basis: 473 building closes + 1,094 program moves) | Agree (−1%) despite different years |
| Lent capacity | **798** (PPS School Profiles 2025-26) | 707 (LRFP 2021) | +13% |
| Rigler capacity | 621 | 589 | +5% |
| Chávez capacity | 564 | 589 | −4% |
| Rosa Parks capacity | **499** | 594 | **−16%** |
| Beverly Cleary capacity | **531** | 783 | **−32%** (receives Irvington under A) |
| Sabin / Irvington / Peninsula capacity | 621 / 618 / 539 | 559 / 547 / 613 | +11% / +13% / −12% |
| Marysville / Chief Joseph / Abernethy | 410 / 444 / 441 | 533 / 499 / 522 | −23% / −11% / −16% (Abernethy 441 is the "can hold" figure our README noted from its family guide) |
| Sabin capture, 2025-26 | **215** live in Sabin's area and attend Sabin (68% of 318 PPS K-5 residents) | Sabin neighborhood target 270 | This is where Closure Commutes' 215 comes from (also the "215" in the early fact check that started this project) |
| Lent area | 254 PPS students live in Lent's area; **80** attend Lent (31%); **117** attend another neighborhood school (Marysville by design) | Our Lent-area `k5` = 256, all treated as DLI | Confirms the Lent→Marysville flow we don't model (Closure Commutes says 115) |
| Rigler area | 438 PPS K-5 residents; **215** attend Rigler (49%); 152 attend another neighborhood school. "Rigler enrolled 50 [immersion kindergartners] with no lottery at all" | `lr_nbhd_share` = 2% (PSU: 2 neighborhood / 289 DLI) | No numeric conflict: Rigler's students are DLI by program but mostly local by residence. Under A/B, Rigler's area goes to Scott, so new local families would lose walk-in access |
| PPS DLI follow rate | "PPS's own school projections now expect only **80–84%** of students in a moved program to follow it" | We hold 100% of PSU program rows at the new host | **Likely explains our Rigler 544 vs PPS 505 and Lent 457 vs PPS 421 (+8–9%)** |
| PPS space-use goal | "PPS's space-use goal is 70–100% of available room (school guides)" | targets.md §1.3: "Utilization band 70–100%: **Not found in any PPS source**" | The family guides we already extracted say "The district aims to use 70%-100% of a school's available room for students" (`build/pps-texts/family-guide-*.md`, glossary). targets.md is out of date on this point |

**PPS's own "students living within 1 mile" (family guides, enrolled students) vs ours** (2025-26 calibrated area kids, OSRM walk / straight line):

| School | PPS SQ | Ours SQ walk / straight | PPS A | Ours A walk / straight |
|---|---|---|---|---|
| MLK Jr | 100% | 100 / 100 | 64.7% | 69 / 91 |
| Rosa Parks | 100% | 100 / 100 | 55.2% | 63 / 82 |
| Beverly Cleary | 93.5% | 96 / 100 | 74.2% | 71 / 82 |
| Scott | 91.9% | 97 / 100 | 46.7% (B 91.9%) | 47 / 62 (B 61) |
| Sitton | 70.6% | 84 / 98 | 45.6% | 54 / 69 |
| Chief Joseph | 78.8% | 76 / 86 | 59.4% | 59 / 73 |
| Alameda | 59.7% | 63 / 71 | 59.7% | 63 / 71 |
| Arleta | 87.6% | 81 / 90 | 63.5% | 62 / 90 |
| Markham | 47.2% | 37 / 87 | 29.5% | 24 / 70 |
| Kelly | 58.2% | 89 / 100 | 58.2% | 62 / 86 |

**PPS's figures track our network-walk numbers, not straight line,** often within 5 points. So PPS likely measures along streets.
- Gaps over 10 points: Sitton (−13 SQ), Markham SQ (+10) and Kelly SQ (−31). PPS counts enrolled students at their real addresses; we count area residents.
- Kelly, Lent and Atkinson (A) all print an identical **58.2%** in the PPS guides, which looks like a copy error in the PPS documents.

**What it concludes or emphasizes** (verbatim from https://pps-dli-explorer.netlify.app/ and `/equity.html`):
- "9 → 4 elementary Spanish immersion sites, today → Scenario A or B"
- "57% of Spanish kindergarten lottery applications went to programs that would move (2022-23 to 2026-27)"
- "52% → 36% of school-age Spanish speakers live within 1 mile of a K-5 Spanish site (estimate; allowing for survey error, the drop is 11–20 points)"
- "Scenario A would move 1,586 students in dual language immersion (DLI) programs out of their schools. They are 29% of the students who would have to change schools"
- "Schools that lose an immersion program are 51% historically underserved and 44% low-income; the schools closing outright are 61% white"
- "Moving a program loses the families who would have joined it ... The 2023 plan had projected 527 students at Lent; it has 256."
- "Lent's problem is not a shortage of families who want Spanish. Its problem is that it no longer serves its own neighborhood, and the plan would do the same to Rigler"
- Research page: "We found no study that compares the two [whole-school vs strand] on student outcomes."

**Chávez/Lent/Rigler (verbatim, https://pps-dli-explorer.netlify.app/history.html)**
> "César Chávez is the plan's main new hub ... In both scenarios, PPS would make it a regional Spanish immersion school for kindergarten through fifth grade (K-5). It would take in the immersion programs from Beach, Sitton and James John. Its neighborhood students would move to Rosa Parks, and its middle grades would move to George."

> "César Chávez would have 541 students, all in Spanish immersion, compared with 413 with no changes. That is 96% of its capacity of 564."

> "In 2023-24 Bridger's Spanish program moved to Lent and Lent's neighborhood program moved to Marysville."

> "PPS projects that Lent would grow to 401 students in 2027-28 once Atkinson's program arrives ... Even so, Lent would fill only 50% of its capacity of 798 students"

From `/equity.html`: "moving César Chávez's neighborhood program out so the school can be immersion-only. That program is 34% Black."

**Strand sizes vs our DLI rule** (targets.md §2.3: viable ≥22/grade K-5, healthy ≥44).
- Their Lent precedent table gives per-grade sizes: Bridger + Lent 56.2 per grade (2021-22); Lent alone 42.7 per grade (2024-25 and 2025-26), with 43 immersion kindergartners in 2025-26.
- On our rule, Lent sits just below "healthy". It is a precedent that a consolidated strand ended up smaller than its parts.
- They report Atkinson at "121 kindergarten applications a year for about 24 seats" and Beach "96 for 23". That is about one class per grade offered against demand for four or more, a demand view our size-only rule doesn't capture.

**Worth borrowing.**
- The capture-rate and residence tables, to recalibrate block capture, fix transfer-in inflation and model the Lent→Marysville flow.
- DLI by grade.
- PPS 2025-26 capacities as a second ceiling.
- A DLI follow-rate parameter (PPS implies 80–84%) for option 2.
- Lottery demand as a DLI "healthy strand" signal.
- Network-based Spanish-speaker access instead of their straight-line 1 mi.

**Avoid.**
- Straight-line reach. Their own note says it overstates walkable access.
- Reading "whole-school vs strand" as settled either way. They found no outcome study.

---

## Spot-check tables (side by side)

### A. 2025-26 enrollment (total; neighborhood where the source gives it)

| School | Ours: ODE total | Ours: neighborhood (K-5 or 6-8 area target) | ppsdata.info total (nbhd / DLI) | Right Size Portland total | Closure Commutes neighborhood (in-area, own program) | Flag |
|---|---|---|---|---|---|---|
| Sabin | 270 | 270 | 270 | 269 | **215** | CC −20%: excludes transfers in |
| MLK Jr (King) | 319 | 126 | 319 (126 / 193) | 319 | n/a (not a source) | |
| Alameda | 515 | 515 | 515 | 513 | 515 (enroll) | |
| Tubman | 403 | 354 | 403 (355 / 48) | 402 | n/a | |
| Beaumont | 416 | 315 | 416 (315 / 101) | 416 | n/a | |
| Jackson | 688 | 688 | 688 | 689 | n/a | |
| da Vinci | 429 | (focus) | 429 | not modeled | n/a | |
| Winterhaven | 316 | (focus) | 316 | 316 | n/a | |
| Rosa Parks | 160 | 160 | 160 | 160 | 160 (enroll) | |
| César Chávez | 443 | K-5 88 / 6-8 55 | 443 (143 / 300) | 443 | **K-5 61 / 6-8 38** | CC −31% |
| Scott | 477 | 254 | 477 (255 / 222) | 476 | n/a | |
| Irvington | 259 | 259 | 259 | 259 | **212** | CC −18% |
| Peninsula | 239 | 239 | 239 | 239 | **195** | CC −18% |
| Other closures | Buckman 283; Woodmere 226; Lewis 262; Creston 219 | same | same | same | **133; 141; 180; 162** | CC −53%, −38%, −31%, −26% |

ODE/PSU totals agree to within ±2 students everywhere, so it is one data spine. The >10% gaps are all Closure Commutes, and all have one cause: its counts are *in-area residents who attend their own neighborhood program*, from a PPS October 2025 enrollment summary.
- The gap is largest at schools that draw transfers or have focus programs: Buckman's arts focus, and Woodmere and Lewis transfer-ins.
- This is the **capture** quantity our backtest flags as the main error source. For a closing school, the transfer-in kids don't live in the area, so our block model, which spreads all 283 Buckman kids over Buckman's blocks, overstates how many land at the receivers.

### B. Capacity and utilization (2025-26)

| School | Ours LRFP 2021 / "model" | ppsdata.info | Right Size Portland | Closure Commutes | Util 2025-26 (all sources) |
|---|---|---|---|---|---|
| Sabin | 559 / **635.5** | 559 / 635.5 | 559 | 559 | 48% |
| Rosa Parks | 594 | 594 | 594 | 594 | 27% |
| Winterhaven | 261 | 261 | 261 | — | 121% |
| da Vinci | 714 | 714 | — | — | 60% |
| Jackson | 908 / 931 | 908 / 931 | 908 | 908 | 76% |
| Harrison Park | 1,006 / **890** (we use 890) | 1,006 / 890 | **1,006** | — | — |
| Creston | 558 / **282** | same | 558 | — | — |

Everyone uses LRFP 2021. The flags are the model-vs-LRFP conflicts: Sabin +14%, Creston −49% and Harrison Park −12%. Right Size Portland uses 1,006 for Harrison Park and we use 890, an 11.5% difference, so a Harrison Park ceiling result depends on it.

### C. PSU 2031-32 and PPS Scenario A 2031-32

| School | PSU 2031-32 SQ (ours = ppsdata = Right Size Portland) | PPS family guide A | Ours A (official lines) | Right Size Portland A | Flag (>10%) |
|---|---|---|---|---|---|
| Alameda | 492 | 493 | 490 | 492 | |
| MLK Jr | 337 | 383 | 377 | 376 | |
| Rosa Parks | 168 | 472 | 464 | 470 | |
| César Chávez | 392 | 527 | 558 | **578** | RSP +10% (keeps the neighborhood K-5) |
| Scott | 470 | 470 (B 301) | 413 (B 253) | 407 (B 247) | ours −12%, RSP −13% vs PPS; B −16 to −18% |
| Rigler | 321 | 505 | 544 | 544 | ours and RSP +8% |
| Lent | 274 | 421 | 457 | 457 | ours and RSP +9% |
| Kelly | 391 | 401 | 396 | 391 | |
| Beverly Cleary | 389 | 484 | 451 | 489 | |
| Beaumont | 418 | 498 | 449 | 475 | ours −10% |
| Tubman | 374 | 455 | 423 | 438 | |
| Jackson | 515 | 404 | 409 | 406 | |
| Hosford | 374 | 557 | **669** | 548 | **ours +20%** |
| Roseway Heights | 498 | 628 | **746** | 643 | **ours +19%** |
| George | 390 | 636 | 673 | 651 | |
| Sunnyside | 475 | **235** | 417 | 444 | ours and RSP ~+80% |
| Winterhaven / da Vinci | 310 / 419 | unchanged | fixed | 310 / — | |

**Likely reasons for the flags**
- **Sunnyside, and through it Hosford.** PPS ends Sunnyside's focus option. The School Explorer says: "It takes no new lottery students. Current lottery students can stay through 5th grade." PPS's 235 evidently drops the lottery share. We, like Right Size Portland, carry Sunnyside's capture factor (1.18 at 6-8) into its moved 6-8 kids, which inflates Hosford. Fix: cap Sunnyside, Bridger and Buckman capture at the area's peers when they lose focus status (README Assumption 4 already warns of this).
- **Roseway Heights.** Ours = 451 neighborhood + **295 program**. Right Size Portland is 643 with the same PSU program rows, so check whether our Roseway program total double-counts. Possible causes: Beaumont 6-8 Spanish plus Roseway's own DLI plus the Rigler/Scott pathway, or our Rigler-area 6-8 assignment (Beaumont vs Roseway).
- **Scott B / Rigler / Lent.** We and Right Size Portland agree to the student, so the gap to PPS is PPS's own program-move assumptions, not our lines. PPS's Rigler 505 < 544 suggests PPS doesn't move all of Scott's 2031 DLI.

### D. Closure-area walks (K-5 kids living in the closing area, to the receiver)

| Move | Ours (OSRM walk, calibrated 2025-26 kids) | Right Size Portland (OSM walk, Census 40 m grid) | Closure Commutes (Valhalla, 19 min/mi; miles = min ÷ 19) | Building to building |
|---|---|---|---|---|
| Sabin → MLK Jr | avg 0.45 → **0.93 mi**; >1 mi 0% → **46%** (123 of 270) | 0.48 → **1.01 mi**; 0% → **53%** | 8.1 → 17.4 min (≈0.43 → **0.92 mi**); 0% → **46.5%** | straight 0.68 mi; our walk ≈0.88; RSP drive 0.91 mi / 3.2 min |
| Irvington → Beverly Cleary | 0.54 → **1.07 mi**; 7% → **56%** (146 of 259) | 0.55 → **1.15 mi**; 9% → **63%** | 9.6 → 20.4 min (≈0.51 → **1.07 mi**); 6% → **61%** | straight 1.02; walk ≈1.23; drive 1.27 / 4.9 min |
| Peninsula → Rosa Parks | 0.55 → **1.26 mi**; 8% → **75%** (178 of 239) | 0.58 → **1.30 mi**; 9% → **74%** | 9.6 → 22.6 min (≈0.51 → **1.19 mi**); 4% → **58%** | straight 0.73; walk ≈1.15; drive 1.09 / 4.6 min (ppsdata same) |

Average walks agree within 8%. The only >10% gap is Closure Commutes' Peninsula share over 1 mile (58% vs our 75%, −17 points). Its minute-based proxy on Valhalla runs about 14% shorter than OSRM by its own cross-check. Many Peninsula homes sit just over 1 mile, so a small distance bias flips them.

Straight-line vs network: Peninsula → Rosa Parks is 0.73 mi straight but about 1.1-1.15 mi on the network, +55%. Never quote straight-line for this pair.

### E. Students affected by Scenario A / B

| Measure | Source | A | B |
|---|---|---|---|
| "Students who would change schools" (share, 2031-32) | PPS (via ppsdata / Right Size Portland) | 27% | 24% |
| Same, recreated by its model | Right Size Portland | 20% | — |
| K-5 / 6-8 students moving (2025-26 in-area own-program students; closures, K-8 conversions, Sellwood and 2 boundary shifts) | Closure Commutes | 2,710 / 1,720 | 2,068 / 1,720 |
| K-5 / 6-8 / 9-12 neighborhood kids reassigned vs SQ 2027-28 (2031-32 basis, all traced line changes) + DLI kids moved | Ours | 3,135 / 2,116 / 388 + 1,567 DLI | 2,502 / 2,116 / 355 + 1,357 DLI |

These are not directly comparable:
- different years (2025-26 vs 2031-32)
- different populations (in-area only vs whole neighborhood program)
- scope: Closure Commutes skips ~30 open-school boundary edits, which we include from the traced maps
- PPS's denominator isn't published

Our K-5 count is higher than Closure Commutes' by +16% (A) and +21% (B). That fits: we include the boundary edits and transfer-in kids.

### F. Schools at the size threshold

| | SQ | A | B |
|---|---|---|---|
| PPS, % of schools at or above threshold (2031-32) | 26% | 67% | 57% |
| Ours, buildings ≥ floor, official lines (2031-32) | 28% | 71% | 58% |
| PPS, % of students in such schools | 48% | 80% | 73% |
| Ours | 50% | 82% | 74% |
| Closure Commutes, K-5 at 360 / MS at 500 (2025-26 loads) | 14/53, 6/23 | 28/40, 12/15 | 23/43, 12/15 |

Ours is consistently 1-4 points above PPS: within noise, and in the expected direction, since we count program-only buildings that PPS may group differently. Closure Commutes' MS count is lower than ours on 2025-26 (6 vs our 11 in-range at 6-8) because we judge K-8s on their K-8 total and count exempt Astor and Skyline as in range.

---

## César Chávez, Lent and Rigler: what each source says

| | Chávez | Lent | Rigler |
|---|---|---|---|
| **PPS memo (we hold it)** | "César Chávez would become a K–5 Spanish immersion hub, with non-immersion K–5 students assigned to Rosa Parks and middle grades to George." | "Atkinson's Spanish immersion program would move to Lent" | "Scott's Spanish immersion program would move to Rigler" |
| **PPS family guides (`build/pps-texts/`)** | "focused K-5 regional Spanish DLI school ... Neighborhood (non-DLI) K-5 students would move to Rosa Parks K-5." Students within 1 mile under A/B: "N/A" | "Lent remains a focused K-5 Spanish DLI school serving the area ... Lent's neighborhood boundary would move to Kelly K-5." Kelly: "Kelly would welcome neighborhood students from Lent (previously assigned to Marysville)." | "Rigler would remain open as a focused regional Spanish DLI K-5 school ... Rigler's non-DLI neighborhood boundary would shift to Scott K-5." Students within 1 mile: "Not applicable" |
| ppsdata.info | Program moves; model sends non-immersion K-5 to Rosa Parks | nbhd 0 / DLI 256 | nbhd 2 / DLI 289 |
| School Explorer | "Immersion only: no neighborhood area"; "César Chávez's area goes to Rosa Parks" | Shared polygon with Kelly, `unclear_between` | Shared polygon with Scott, `unclear_between` |
| Closure Commutes | "becomes a Spanish immersion hub, so its neighborhood K–5 students go to Rosa Parks" (61 kids) | "non-immersion students from the Lent area attend Marysville today (115 ...), and the slides send them to Kelly" | Treated as a neighborhood school ("most of its students live in its neighborhood") |
| Right Size Portland | No Chávez → Rosa Parks flow (Chávez A 578) | "Not modelled ... Lent non-DLI students to Kelly" | Program move only |
| DLI explorer | "regional Spanish immersion school ... Its neighborhood students would move to Rosa Parks"; neighborhood program 143 (78 K-5 / 65 6-8), "34% Black"; A = 541, 96% of capacity 564 | Precedent: 2023 conversion; capture 63% → 31%; 256 vs 527 projected; A 401 (2027-28), 50% of 798 | "the plan would do the same to Rigler" (area goes to Scott); 50 immersion kindergartners with no lottery |
| **Ours** | Program-only marker, no area; 88 neighborhood K-5 (2025-26) → Rosa Parks | Area → Kelly; kids follow the program (`lr_nbhd_share` 2%) | Area → Scott; kids follow the program (2%) |

**Implications for us**
1. Close the PLAN.md open item: the "immersion only" label is supported by the memo (p. 3) and the family guide. Replace "≈645" with 2031-32 A numbers (PPS 527 / ours 558).
2. **Lent → Marysville is a real flow we don't model.** About 115 Lent-area non-immersion kids enroll at Marysville. Our calibration counts them in Marysville's 304 but spreads them over Marysville's blocks, which likely explains part of Marysville's −35% backtest miss (capture 0.78).
   - Under A, PPS sends them to Kelly; we send Marysville's area to Arleta.
   - Possible fix: give the Lent-area blocks a non-DLI neighborhood count of about 115 that goes to Marysville today and Kelly under A/B, and take the same amount off Marysville's blocks.
   - Find the exact count first, in PPS's capture-rate report or by asking the Closure Commutes author.
3. Rigler: keep our treatment, which matches PSU and the family guide. Closure Commutes' choice is the outlier.

---

## Data we should consider adding

| Data | Why | Where |
|---|---|---|
| **PPS "Enrollment Summary by K-12 Students' Neighborhood and Type of School Attended" / capture-rate reports**, Oct 2019 → Oct 2025 | Gives in-area residents attending their own neighborhood school, another neighborhood school, alternative or charter. That replaces Census-based capture guesses and fixes transfer-in inflation for closing schools (Buckman, Woodmere, Lewis). It shows Lent-area residents at another neighborhood school (117). | **Found:** already parsed in https://github.com/jminnier/pps-dli-explorer `data/capture_rate.csv` (PDFs in `data-raw/pps_reports/capture_rate/`). Primary: PPS Data & Reporting page (2024-25, 2025-26) and archive page. The old `pps.net/cms/lib/...` URLs 404 |
| **PPS School Profiles 2025-26 functional capacity** | PPS's *current* capacity differs from LRFP 2021 by >10% at many schools (Beverly Cleary 531 vs 783; Rosa Parks 499 vs 594; Marysville 410 vs 533; Lent 798 vs 707). It changes ceilings and utilization | DLI explorer `data/school_profiles_2025.csv` (scraped from PPS Power BI, Oct 9 2026) |
| **DLI enrollment by grade** (PPS Enrollment by Grade and Program Type, Oct 2024/2025) | Replaces our estimated grade split (README "Biggest gaps") | DLI explorer `data/enrollment_by_program_grade.csv` |
| PPS family-guide per-school "% within 1 mile", "meets space use goal" | Direct PPS benchmark for our distance metric; the 70–100% space-use goal | DLI explorer `data/guide_school.csv`; also our own `build/pps-texts/` |
| PPS DLI follow rate (80–84%) and K lottery demand by program | Option 2 realism; "healthy strand" signal | DLI explorer equity §5, `lottery_results.csv` |
| PSU low/high (Tables 5.3/5.4) | Robustness for durability. ppsdata.info's synthesized per-school bands are K-5 ×0.93/×1.11 and 6-8 ×0.90/×1.07 | PSU forecast PDF (already in PPS Data Explorer raw) |
| PSU Table 5.5 annual per-school rows (2026-27 → 2035-36) | Per-area durability in place of a uniform district ratio (METHOD §3b gap) | Right Size Portland embeds `series` per school per year; PPS Data Explorer has `enrollment_forecast_20xx` columns. **We already have this in `pps_schools.csv`; we just don't use it.** |
| ODE 2022-23 → 2024-25 by grade | Trend check on capture; cohort aging | PPS Data Explorer `data/exports/` (new since our snapshot) |
| DLI by language at multi-language schools | Franklin Spanish 173 / Russian 29 | PPS Data Explorer `pps_immersion_details_2526.json` (updated) |
| Spanish-DLI reach metric | Quantifies the access cost of A/B consolidation (16.4% → 8.5% of land within 1 mi) | Compute ourselves from the walk matrix |
| Busing cost / staffing / building costs (stretch) | Dollars for the trade-off write-up | Right Size Portland's sources: 2026-27 adopted budget, posted bus routes, LRFP FCI, Holmes 2024 |

## Methods worth borrowing, and errors to avoid

**Borrow**
- Alternative-rule bracketing from Closure Commutes ("nearest open, capacity ignored" as the floor; "whole school to one receiver"). Report these next to our options so readers see the feasible range.
- A memo-split check for our traced A baseline (Maplewood 70/30, Stephenson 70/30, Buckman 50/50).
- A regional measures check against PPS's four regional summaries, as Right Size Portland does.
- Receiving-school class counts by grade and strand (ppsdata.info).
- `unclear_between` flags for Kelly/Lent and Scott/Rigler in our map data and on the map.
- Bus-eligibility sensitivity: Right Size Portland finds about 2,900 more 6-8 residents if 6-8 used 1 mile instead of 1.5.

**Avoid**
- Treating straight-line distance as a walk; it is off by up to 55% for Peninsula → Rosa Parks.
- Using a drive or isochrone proxy as bus time.
- Scenario models that skip open-school boundary changes (ppsdata.info, and partly Closure Commutes and Right Size Portland). Our traced-polygon approach is the stronger one, and now independently corroborated.
- Carrying focus-lottery capture into areas that lose focus status (our Sunnyside/Hosford issue).

## Conclusions: what each resource emphasizes, and whether we agree

| Resource | What it concludes or emphasizes |
|---|---|
| ppsdata.info | **Sustainability and size.** It emphasizes decline ("PRC expects enrollment to fall from 42,622 (2025-26) to 36,763 (2035-36 medium), a 14% decline"), building utilization, seismic risk and condition. It republishes PPS's measures (students in sustainable schools 48% → 80% under A). Its rough receiving-school model (2025-26 students, no boundary changes) puts Hosford, César Chávez and Duniway (A) over 2021 capacity, and it flags that this overstates. It takes no position on the scenarios. |
| PPS School Explorer | **Information access.** It shows what changes at an address. Its analytic emphasis is **DLI access** (Spanish K-5 1-mile reach 16% → 9% of PPS land) and **ambiguity** (Rigler/Scott, Kelly/Lent shared areas; "PPS has not said which school serves each area"). |
| Closure Commutes | **Commute burden for displaced families.** Under A with PPS's lines, closure-area K-5 walks rise from 13.7 to 22.4 min, and 1,174 children newly pass the 1-mile walk proxy. A capacity-limited shortest-walk rule cuts that to 667, but with **fewer schools at 360 (25 vs 28)**. It frames this as "Shorter trips, or fuller schools?", a trade-off. Middle grades are hit hardest (Vernon → Tubman +42 min walk; Sellwood → Hosford +50 min). |
| Right Size Portland | **Full cost and consequence accounting.** It covers year-by-year size (A: 43/64 buildings at threshold in 2031-32, falling to 39/64 by 2035-36), commute (K-5 beyond 1 mi 28.7% → 41.1% under A), busing cost, staffing-formula positions, avoided repair costs, land value, and private, homeschool and virtual alternatives. It lets users build custom scenarios. It reproduces PPS's measures. |
| DLI explorer | **DLI access and equity.** The plan "relies on moving immersion programs" (1,586 students). Burdens fall on Latino and Asian immersion families and on César Chávez's neighborhood program (34% Black). The schools closing outright are 61% white. Program moves lose families (the Lent precedent; PPS's own 80–84% follow rate). Spanish-speaker access within 1 mile falls from 52% to 36%. Lottery demand is concentrated at the programs that move. |

### Side-by-side key claims

| Claim (ours) | Our number (source) | Theirs | Verdict | Why any difference |
|---|---|---|---|---|
| Scenario A sends K-5 kids past a closer open school | **2,575** (official-line A, map/letter basis, PLAN.md). Solver scorecard (2031-32, ≥0.25 mi further rule): **1,997** vs 1,855 SQ (compare.md) | Closure Commutes: "Nearest open school" rule would put 657 closure-area kids newly over 1 mi vs **1,174** under PPS's lines | **Agree in direction** (PPS's lines are not nearest-school lines); not the same metric | They measure only closure areas, by newly-over-threshold, in 2025-26 in-area students. Ours covers all K-5 blocks. Note our two figures differ (2,575 vs 1,997) by basis and definition: reconcile before quoting |
| % of K-5 within 1 mile falls under A | **72.2% → 62.7%** (B 65.3%), OSRM walk, 2031-32, model v2 scorecards `levels.K-5.pct_within_1.0mi`, Status Quo → A (earlier model: 73.5% → 63.0%, B 65.6%) | RSP: **71.3% → 58.9%** (B 61.9%), OSM walk, Census residents. PPS per-school guide figures track our walk numbers (table in §5) | **Agree** (−9.5 vs −12.4 pts) | RSP weights by Census residents, so it doesn't apply our per-area capture; different routing graph; scenario years differ |
| Average K-5 walk rises | 0.854 → **0.968 mi** | RSP 0.87 → **1.00 mi**; Closure Commutes, closure areas only, 13.7 → 22.4 min | **Agree** | Same as above |
| Middle schools: only 7 of 13 zoned non-exempt at ≥500 in A (2031-32) | **7 of 13** (compare.md durability) | Closure Commutes: MS at 500 = **12/15** under A (2025-26 loads). PPS slide (targets.md): 15 schools → 2-8 at 500+ depending on closures | **Differ** | Closure Commutes uses 2025-26 enrollment (pre-decline; 6-8 PSU 2031 ratio down to 0.62 at Sellwood) and counts building loads including DLI and K-8s. Ours is 2031-32 PSU-scaled, neighborhood plus hosted programs, Astor/Skyline exempt |
| A redraw can keep ~70% within a mile while hitting size targets | Option 1 (2031-only) **69.5%**, Option 1-durable **67.7%**, with **every** school in range in 2031-32 (compare.md) | Closure Commutes: shorter-walk rules **reduce** schools at 360 (28 → 24–25). Nobody else redraws open-school lines | **Differ** (they find a trade-off; we find both are achievable) | **Scope**: Closure Commutes only reassigns closing areas and holds every other line fixed. We redraw all lines with a size-constrained solver. Year: their sizes are 2025-26, ours 2031-32 |
| Schools sized only to 2031 fall below target by 2032-33 | Option 1 (2031-only): K-5 35/35 → **12** in 2032-33; Scenario A K-5 24 → 21 by 2036-37 | RSP (PSU Table 5.5 per school, all levels): A **43/64** at threshold in 2031-32 → **39/64** in 2035-36; SQ 20/78 → 19/78 | **Agree** that A erodes after 2031. Nobody else tests a 2031-tuned redraw | RSP uses PSU per-school annual rows; we scale by PSU district ratios (Table 5.2) |
| Scenario A sharply raises schools at threshold | Buildings ≥ floor: 28% → **71%** (B 58%); students in them 50% → 82% | PPS: 26% → **67%** (B 57%); 48% → 80%. RSP reproduces PPS exactly | **Agree** (within 1–4 pts) | Our denominator includes program-only buildings |
| DLI disruption | **1,567** DLI kids moved under A (2031-32) | DLI explorer **1,586** (Oct 2025); School Explorer 1-mi reach 16% → 9% | **Agree** | Year |
| Diversity is roughly unchanged by A and by our redraw | Dissimilarity 0.209 → 0.198 (A), 0.197 (Option 1-durable); kids of color are ~42% of movers | DLI explorer: moving **DLI** programs are 45% Latino / 13% Asian; César Chávez neighborhood 34% Black; closing schools 61% white | **Not covered the same way** | We measure school-level segregation of neighborhood kids; they measure *who moves* by program. Their DLI-specific burden is outside our neighborhood-kid metric |
| Closure-area walks (Sabin→King, Irvington→Beverly Cleary, Peninsula→Rosa Parks) roughly double | §D: 0.45→0.93, 0.54→1.07, 0.55→1.26 mi | RSP 0.48→1.01, 0.55→1.15, 0.58→1.30; Closure Commutes ≈0.43→0.92, 0.51→1.07, 0.51→1.19 | **Agree** (≤8% on averages) | Routing engine |
| Busing cost, staffing, building costs | Not computed (we report bus-eligible counts only: K-5 3,452 → 4,819 under A) | RSP models dollars | **Not covered** by us | Scope |

---

## Data-sharing with PPS School Explorer

**Is the traced data downloadable?** Yes.
- The live site serves plain GeoJSON at `/data/{sq,a,b}_{k5,68,912}.geojson`, `*_schools.geojson`, `{a,b}_*_changed.geojson`, `dli_reach.json` and `index.json`. These are fetched by the app, and I downloaded all nine area layers.
- The **public GitHub repo https://github.com/browniefed/pps-explorer** (last push 2026-10-10) has the same files under `public/data/` and the full extraction pipeline (`scripts/pipeline/`: extract.py, gpts.py, build.py, qa.py, verify_city.py, dli.py), plus the source PDFs in `public/maps`.

**License and terms.**
- The repo has **no license file**: the GitHub API returns `license: null`. Without a license, default copyright applies, so redistribution needs the author's permission.
- The DLI explorer's README says the same: "The upstream pps-explorer repository has no license; its author is credited throughout, and reuse terms have not yet been confirmed."
- The site states no terms. It says: "This site is not part of PPS."

**Contact routes.**
- The site's footer gives a contact email for boundary questions.
- GitHub issues are enabled on the repo (none filed yet).

**Compatibility with ours.**
- Format: WGS84 GeoJSON polygons, one feature per area, with `name`, `school_label` (PPS's map label), `cluster`, `clusters` (with shares), `level`, `area_sqmi` and, where relevant, `unclear_between`. That is directly joinable to our `scenario_maps/*.geojson` and `blocks.parquet` after a name crosswalk (Brentwood↔Lane, Sunrise↔Lee, Wells-Barnett↔Ida B. Wells, MLK).
- **Agreement:** 99.6–99.9% of kids at all 9 level/scenario combinations, apart from the Kelly/Lent label. Line-to-line offset between the two tracings is median 37–39 ft, p90 83–98 ft, with 90–94% of our boundary within 100 ft of his.
- **Its georeferencing is likely more precise than ours.** It reads the GeoPDF `/VP /GPTS` tags embedded in PPS's PDFs (corner residuals 3 m main map, 9 m inset). We fitted an affine transform from label positions plus ICP (median 71 ft, p90 143 ft residual; data README). The ~40 ft offset is consistent with our transform being the looser one.
- Status-quo differences against the City layer are the same on both sides: its `verify_city.py` finds the same Beaumont/Roseway (Cully/airport strip) disagreement we found in our 6-8 QA (backtest "Rigler question").

**What each side could offer the other**

| We could offer | It could offer |
|---|---|
| Block-level calibrated kids by band (K-5/6-8/9-12) on both tracings, to put student counts behind any area, change or "where students go" | GeoPDF-tag georeferencing (`gpts.py`), a few-meter accuracy upgrade we could adopt or check against |
| OSRM walk and bike matrices, block → school (9,295 × 86) | Its `_changed.geojson` diff layers and the memo transcription (`changes-data.mjs`) with Spanish and other translations |
| Official-line baselines (Today, SQ, A, B scorecards: distance, size, durability 2031-41) | Six-language UI text and plain-language style guide, if our map adds languages |
| An independent cross-check: the agreement statistics above, plus the specific sliver disagreements (Duniway/Lewis 10 kids, Lincoln/Wells 10, Beverly Cleary/Alameda 4) | The DLI reach layer and site list |
| A resolution proposal for the shared polygons: under A/B we assign the Kelly/Lent area to Kelly and Scott/Rigler to Scott, per the family guides ("Lent's neighborhood boundary would move to Kelly K-5"; "Rigler's non-DLI neighborhood boundary would shift to Scott K-5"). Both sides could cite those lines | His confirmation of how the PDFs label those shared areas |

**Ambiguous shared areas.**
- On the A/B K-5 maps, PPS draws Kelly+Lent and Scott+Rigler as single polygons.
- The School Explorer names them "Lent" and "Scott" and flags `unclear_between`. We name them Kelly and Scott.
- The family guides (quoted above) say the neighborhood area belongs to Kelly and Scott respectively. Lent and Rigler stay as immersion-only buildings.
- That resolves the naming. The remaining open question for both projects is whether any non-DLI kids still walk in to Rigler or Lent; PPS hasn't said.

---

## Sources

- PPS DLI explorer: https://pps-dli-explorer.netlify.app/ (pages `/history.html`, `/equity.html`, `/scorecard.html`, `/methods.html`) ; repo https://github.com/jminnier/pps-dli-explorer (`data/capture_rate.csv`, `data/school_profiles_2025.csv`, `data/enrollment_by_program_grade.csv`, `data/guide_school.csv`, `data/dli_moves.csv`)
- PPS School Explorer repo: https://github.com/browniefed/pps-explorer
- PPS Data & Reporting (capture rate, enrollment by program and grade): https://www.pps.net/departments/dataaccountability/data-and-accountability/data-strategy-and-insights/data-and-reporting ; archive https://www.pps.net/departments/dataaccountability/data-and-accountability/data-strategy-and-insights/archives
- PPS Data Explorer: https://ppsdata.info/ ; data https://ppsdata.info/data.json ; repo https://github.com/meub/pps-data (HEAD 2026-10-12; we use 80ec323)
- PPS School Explorer: https://pps-explorer.codedaily.workers.dev/ ; data `/data/{sq,a,b}_{k5,68,912}.geojson`, `/data/dli_reach.json`
- PPS Closure Commutes: https://chrisloer.github.io/pps-closures/ ; data `data.json`, `boundaries.json` ; Felt maps https://felt.com/map/PPS-school-closures-travel-time-impact-eRA1FAMvSHSebm5FQg9AcNA and https://felt.com/map/PPS-closures-travel-time-workbench-c6as0xMdQ3utb9AoiMhEBcC
- Right Size Portland: https://rightsizepdx.com/rightsizing-scenario-explorer.html ; repo https://github.com/southie/ppsrightsize
- PPS board memo, Oct 6 2026 (memo link used by Closure Commutes): https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14509719 ; agenda https://meetings.boardbook.org/Public/Agenda/915?meeting=769955
- PPS capture-rate report, Oct 2025 (current PPS link): https://www.pps.net/fs/resource-manager/view/d65fc69c-e9b5-4c13-8199-545d12deb541 . Earlier years' reports were on PPS's old website and are no longer online.
