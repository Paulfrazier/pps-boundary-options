# PPS boundary options: a parent's look at what else is possible

**Built with AI, directed by a person.** The analysis, data work, coding and optimization were done by AI (Claude, from Anthropic), directed and guided by Paul Frazier, a PPS parent. He set the questions, made every judgment call, checked the results against PPS's own documents, and corrected the model when it got things wrong. It is best effort and will have errors. **[Full methodology](#full-methodology)** covers every data source, method and assumption.

**Why it exists.** PPS has shared two scenarios, A and B. This project explores what other boundary lines could look like with the same closures and size targets. Using Census blocks and open street maps, it finds lines that keep more kids within walking distance and keep schools at their size targets in every year of PPS's own projection window, 2027-28 to 2031-32. It isn't meant to replace the district's work: PPS has real enrollment data and knows its schools far better than a public-data model can. We hope it adds to the conversation.

**What we hope to see from the district:**

1. **More options.** More than two scenarios, including boundary lines that keep kids closer to school and keep schools at their size targets in every year of PPS's projection window, not just in 2031-32.
2. **The data behind them,** so families can follow the trade-offs:
   - attendance boundaries for Status Quo, A and B as GIS files (shapefile or GeoJSON), not just PDFs;
   - student counts by grade and program on a small geographic grid, aggregated to protect privacy;
   - per-school projections for each scenario and year;
   - the building capacity model;
   - transfer and capture-rate data (where neighborhood kids actually attend);
   - transportation cost assumptions.

> **DISCLAIMER.** This is an independent, best-effort analysis by a PPS parent, **not an official Portland Public Schools product**. It may contain errors. Consult PPS's own materials to confirm: the [Rightsizing scenarios site](https://www.pps.net/about/portland-public-schools-information/rightsize/scenarios) and the [October 6, 2026 Board of Education meeting materials on BoardBook](https://meetings.boardbook.org/Public/Agenda/915?meeting=769955) (the 2027-28 attendance-area map PDFs are BoardBook files 14505795-14505805).

In October 2026 Portland Public Schools released two "rightsizing" scenarios (A and B) that close schools, convert K-8s, move Dual Language Immersion (DLI) programs and redraw attendance areas. PPS published maps of the new lines but not block-level detail or alternatives.

This repo asks a narrower question: **keeping PPS's own closures and size targets, how close to school can kids be, and will the result still hold up as enrollment keeps falling?** It builds one model of where neighborhood-program students live, digitizes PPS's maps into it, and uses an exact optimizer (OR-Tools CP-SAT) to draw alternative K-5, 6-8 and 9-12 lines with:

- **walkability**: real walk distances on the street network (local OSRM over OpenStreetMap), no new crossings of I-84 or the Willamette;
- **size targets** PPS uses: K-5 at least 360, 6-8/K-8 at least 500, 9-12 at least 1,100, all at or under building capacity, measured on PSU's **2031-32** forecast as PPS does;
- **durability, 2027-28 to 2031-32**: using each school's own Portland State University forecast (July 2026, Table 5.5), at least as many schools at target as PPS A (PPS's Scenario A) in every year of PPS's projection window; 2032-33 to 2035-36 are reported, not required, and nothing past 2035-36 is projected;
- **feeders**: whole elementary zones feeding one middle school, and middle zones feeding one high school, are preferred but not required; every split is reported (our redraws keep PPS A's high-school lines, so many middle zones feed more than one high school).

Everything here is **work in progress**. See [Limits](#limits) before quoting any number.

## Full methodology

- [Definitions](DEFINITIONS.md): what every number means, and how the two model versions differ.
- [Data foundation](build/data/README.md): sources, Census block calibration, traced PPS maps, assumptions; [backtest](build/data/backtest.md) of the model against real enrollment.
- [Walk and bike routing](build/routing/README.md) and its [validation](build/routing/validation.md).
- [Policy targets and scenario facts](build/research/targets.md), each with its PPS source.
- [Optimizer and scorecard method](build/solver/METHOD.md), including contiguity, feeders and the durability rule.
- Map build: scripts in [`build/map/`](build/map/) (`patch.py` rebuilds the compare map).
- [How this compares with other community models](build/research/compare_resources.md).

## Context and resources

- **Thanks to the [PPS Data Explorer](https://ppsdata.info/) project**, whose [`pps-data`](https://github.com/meub/pps-data) repo is the source we used for 2025-26 state enrollment by grade, the 2021 Long-Range Facility Plan capacities the earlier model used, and PPS's immersion enrollment details. These are public PPS and state figures the project compiled; see [SOURCES.md](SOURCES.md). The current model's building capacities come from PPS's 2025-26 school profiles, as captured by the [PPS Dual Language Immersion & Rightsizing](https://pps-dli-explorer.netlify.app/) project (second-hand). Every source we used is listed on [How we did this](pages/how.html).
- PPS's official materials: the [Rightsizing scenarios site](https://www.pps.net/about/portland-public-schools-information/rightsize/scenarios) and the October 6, 2026 Board meeting materials on [BoardBook](https://meetings.boardbook.org/Public/Agenda/915?meeting=769955). Unofficial text copies of every scenario document are in [`build/pps-texts/`](build/pps-texts/README.md).
- PPS family survey, ["Why They Stay and Leave" summary report (Jan 6, 2026)](https://drive.google.com/file/d/1inDzPET-xRxzR8xZhCssQNMGI2JwSRbO/view).
- Related community analyses: [ppsdata.info](https://ppsdata.info/), [PPS School Explorer](https://pps-explorer.codedaily.workers.dev/), [PPS Closure Commutes](https://chrisloer.github.io/pps-closures/), [Right Size Portland](https://rightsizepdx.com/), [PPS DLI & Rightsizing](https://pps-dli-explorer.netlify.app/). How our numbers compare: [`build/research/compare_resources.md`](build/research/compare_resources.md).
- Every link the project fetched or cites: [RESOURCES.md](RESOURCES.md).

## View the maps and tables

Start at [`index.html`](index.html), which links the current pages: [Options](pages/options.html), [Durability](pages/durability.html), [Map](pages/map.html), [Method](pages/method.html), [Sources](pages/sources.html) and [How we did this](pages/how.html). Earlier first-generation pages are kept offline and are not in this repo.

## Other models and how they compare

Several community projects have built public analyses of the PPS rightsizing scenarios. We compared our data and results with five of them (October 12, 2026). All of them build on public PPS, Portland State and Census data. Most draw on the PPS Data Explorer's [pps-data](https://github.com/meub/pps-data) repo, which this project also uses. Each project has strengths ours doesn't, and they're worth reading alongside this one.

**[PPS Data Explorer](https://ppsdata.info/)**, an independent project ([source](https://github.com/meub/pps-data)). A dashboard covering all 74 in-scope schools: enrollment trends, utilization against PPS's 2021 functional capacity, the PSU 10-year forecast, seismic condition, demographics, and a summary of Scenarios A and B. Its compiled data is the foundation of our school table, so enrollment, capacity and forecast figures match ours exactly. Its scenario section republishes PPS's district measures, and our official-line baselines reproduce them within a few points (for example, 82% vs PPS's 80% of students in schools at the size target under Scenario A). Its receiving-school model moves whole schools without boundary changes, so it is not directly comparable with our block-level results.

**[PPS School Explorer](https://pps-explorer.codedaily.workers.dev/)**, an independent project ([source](https://github.com/browniefed/pps-explorer)). An address-lookup map of the Status Quo, Scenario A and Scenario B attendance areas at every grade level, in six languages. It traces the boundaries from PPS's October 6 scenario maps using the georeferencing embedded in the PDFs. We traced the same maps independently. The two tracings assign the same school to 99.6–99.9% of children at every level and scenario, and the lines sit a median of about 40 feet apart. The one naming difference is the areas PPS draws as shared (Kelly/Lent and Scott/Rigler). His map flags these as unclear, and we follow the family guides in giving them to Kelly and Scott. His map also shows how far Spanish immersion reaches: the share of district land within a straight-line mile of a K-5 Spanish site drops from 16% to 9% under both scenarios. We don't measure that.

**[PPS Closure Commutes](https://chrisloer.github.io/pps-closures/)** (independent). It estimates how walk, bike and drive times change for families in each closing school's area, using routed travel-time contours and PPS's count of neighborhood students who attend their own school. Its closure-area walk distances agree with ours to within about 8% (for example, Sabin to MLK Jr, roughly 0.45 to 0.93 miles). Its student counts are lower than ours because it leaves out students who transfer in. It also tests other ways to draw the receiving lines. When only the closing areas are redrawn, it finds a trade-off between shorter walks and fuller schools. Our solver redraws every line, and it finds both can be met in 2031-32. That difference comes from scope, not a contradiction.

**[Right Size Portland](https://rightsizepdx.com/)** (independent; [source](https://github.com/southie/ppsrightsize)). A scenario explorer with year-by-year school sizes to 2035-36. It also covers walk and bus access, estimated busing and staffing costs, building repair costs, land values and private-school alternatives, and it lets users build custom scenarios. It matches PPS's published measures. Its walk figures agree closely with ours: the share of K-5 students within a mile drops about 12 points under Scenario A, against our 9.5 (72.2% to 62.7%). Its year-by-year figures, like ours, show the number of Scenario A schools at the size target slipping after 2031-32 as enrollment keeps falling. It covers costs we don't. Our 2031-32 sizes differ from its figures at a few schools, mainly where focus-program and immersion assumptions differ.

**[PPS Dual Language Immersion & Rightsizing](https://pps-dli-explorer.netlify.app/)** (independent; [source](https://github.com/jminnier/pps-dli-explorer)). A detailed look at what the scenarios mean for immersion families, in English and Spanish. It covers lottery demand, program moves, access for Spanish-speaking families, equity, the 2023 Lent conversion as a precedent, and the research on whole-school versus strand immersion. It draws on PPS reports we hadn't used: neighborhood capture rates, immersion enrollment by grade, and current building capacities. Its immersion program counts match ours exactly. Its count of students in moving immersion programs (1,586) is close to ours (1,567). It focuses on who moves and on immersion access, which our size and distance measures don't capture. We don't measure those, so we neither confirm nor dispute its conclusions there.

**Overall.** On the facts all of us measure, the results line up closely: enrollment and forecasts, traced boundaries, walk distances, and how many schools reach the size targets. That gives us confidence the shared inputs are sound. The differences trace to choices we can name: the enrollment year (2025-26 vs PPS's 2031-32 basis), whether students who transfer in are counted, and whether only the closing areas or all lines are redrawn. Several of these projects, especially the immersion and cost analyses, cover ground this project doesn't.

<!-- results:start -->
## Key results so far

Generated from the site's data file (`pages/data/site_data.json`, built from each plan's `scorecard.json`; model v2). Neighborhood-program kids on the PSU 2031-32 basis. Plans must match or beat PPS A's count of schools at target in every year 2027-28 to 2031-32 (PPS's own projection window). For PPS Status Quo, A and B, the at-target rows use PPS's own Family Guide projections (p. 4); every other number is our model. Full side-by-side tables: [Options](pages/options.html) and [Durability](pages/durability.html).

**K-5: PPS's lines vs. a walk-optimized redraw with the same closures and programs**

| K-5 | PPS Status Quo | PPS A | PPS B | Balanced middle schools | Balanced, Sellwood open | Boundary changes, same closures | Redrawn K-8 lines | Rebalanced PPS A | Close 2 focus options |
|---|---|---|---|---|---|---|---|---|---|
| Avg walk (mi) | 0.87 | 0.98 | 0.95 | 0.93 | 0.93 | 0.93 | 0.95 | 0.97 | 0.93 |
| Within 1 mi on foot | 72.2% | 62.7% | 65.3% | 67.6% | 67.6% | 67.6% | 65.7% | 63.4% | 67.7% |
| Over the 1-mi bus threshold | 3,496 | 4,703 | 4,376 | 4,117 | 4,117 | 4,117 | 4,366 | 4,655 | 4,156 |
| Assigned to a farther school, past a closer one (0.25 mi margin) | 1,861 | 1,970 | 2,144 | 932 | 932 | 932 | 1,285 | 1,838 | 1,001 |
| Schools at target, 2031-32 | 9 of 50 | 22 of 35 | 18 of 38 | 35 of 35 | 35 of 35 | 35 of 35 | 35 of 35 | 34 of 35 | 35 of 35 |
| Schools at target every year, 2027-28 to 2031-32 | 9 of 50 | 18 of 35 | 15 of 38 | 35 of 35 | 35 of 35 | 35 of 35 | 35 of 35 | 33 of 35 | 35 of 35 |
| Kids reassigned vs. PPS Status Quo | - | 2,935 | 2,305 | 4,867 | 4,867 | 4,867 | 4,914 | 3,594 | 4,888 |

*PPS Status Quo (2027-28, no closures):* Lent is all Spanish immersion, so the model counts K-5 kids living in Lent's area at Marysville; the map still draws PPS's Lent line. PPS reports 117 of 254 Lent-area students (46%) attend another neighborhood school (PPS enrollment summary, October 2025); which school is our assumption.

*Boundary changes, balanced middle schools:* The middle-school minimum is 460, not PPS's 500. Four middle schools dip below 500 in their low year: Harrison Park 461 (2030-31), Ockley Green 461 (2028-29), West Sylvan 460 (2031-32) and George 498 (2031-32). So at PPS's 500, 9 of 13 are at target every year 2027-28 to 2031-32; West Sylvan falls to 443 in 2032-33, a year PPS doesn't project. In return, only 3 elementary schools split between middle schools (best example we modeled: 13) and no middle school is over capacity (our model). One change to PPS A's high-school lines: the Skyline area (about 93 high-school students in 2031-32) stays at Lincoln, as today, instead of crossing the St. Johns Bridge to Roosevelt. It ends Roosevelt's 2027-28 crowding (1,421 students for 1,395 seats without it). The costs: Roosevelt falls below its 1,100 minimum from 2032-33 (1,075, then 1,027 by 2035-36, years reported but not required); the gap between the largest and smallest high school in 2031-32 grows from 362 to 424 students (PPS's goal: under 350); and the average high-school walk rises from 1.93 to 1.98 miles (our model).

*Balanced middle schools, Sellwood Middle open:* The best example we modeled with Sellwood Middle kept open on about its own area (PPS A and B close it in 2028). Sellwood would have about 312 students in 2031-32, below PPS's 500 minimum, so it is exempt from the minimum and not counted at target (our model). The other 13 middle schools are solved at a 460 minimum, as in the best example we modeled, and counted at PPS's 500 here. Elementary and high-school lines are the same as the best example we modeled. One change to PPS A's high-school lines: the Skyline area (about 93 high-school students in 2031-32) stays at Lincoln, as today, instead of crossing the St. Johns Bridge to Roosevelt. It ends Roosevelt's 2027-28 crowding (1,421 students for 1,395 seats without it). The costs: Roosevelt falls below its 1,100 minimum from 2032-33 (1,075, then 1,027 by 2035-36, years reported but not required); the gap between the largest and smallest high school in 2031-32 grows from 362 to 424 students (PPS's goal: under 350); and the average high-school walk rises from 1.93 to 1.98 miles (our model).

*Rebalanced PPS A:* Moves more K-5 kids than PPS A (3,594 vs 2,935): getting PPS A's 20 schools that miss their size range into range takes extra moves. Still misses three 2031-32 sizes: Forest Park K-5 101 short (PPS A: 102 short; no fix within the 2-mile walk cap), Jackson 6-8 78 short, Roseway Heights 6-8 35 short.

*Close 2 focus options (Winterhaven, da Vinci):* A what-if, not one of the example plans. Assumes every returning Winterhaven and da Vinci student attends their neighborhood school; home areas come from a per-catchment sheet of 2025-26 focus students (second-hand; per-program source not stated); 21 students living outside PPS are not placed.

Sources: [PPS Status Quo](build/solver/out_v2/status_quo/scorecard.json), [PPS A](build/solver/out_v2/scenario_A/scorecard.json), [PPS B](build/solver/out_v2/scenario_B/scorecard.json), [Balanced middle schools](build/solver/out_v2/option2_ms460/scorecard.json), [Balanced, Sellwood open](build/solver/out_v2/option2_ms460_sellwood_home/scorecard.json), [Boundary changes, same closures](build/solver/out_v2/option2/scorecard.json), [Redrawn K-8 lines](build/solver/out_v2/option1_durable/scorecard.json), [Rebalanced PPS A](build/solver/out_v2/option4/scorecard.json), [Close 2 focus options](build/solver/out_v2/option3a/scorecard.json).

- **Middle school (Balanced middle schools (the best example we modeled) vs. A):** average walk 1.71 vs. 1.76 mi; 9 of 13 zoned middle schools at target in 2031-32 (A: 7 of 13) and 9 in every required year (A: 6; all on our model). The cost is split feeders: 3 elementary zones split between middle schools vs. 1 under A.
- **High school (Balanced middle schools (the best example we modeled) vs. A):** One change to PPS A's high-school lines: the Skyline area (about 93 high-school students in 2031-32) stays at Lincoln, as today, instead of crossing the St. Johns Bridge to Roosevelt. It ends Roosevelt's 2027-28 crowding (1,421 students for 1,395 seats without it). The costs: Roosevelt falls below its 1,100 minimum from 2032-33 (1,075, then 1,027 by 2035-36, years reported but not required); the gap between the largest and smallest high school in 2031-32 grows from 362 to 424 students (PPS's goal: under 350); and the average high-school walk rises from 1.93 to 1.98 miles (our model). 6 of 8 high schools at target in every required year (A: 5 on our model). Because the middle school lines change, 40% of middle zones feed a single high school (A: 80%). Walk distance is a weak proxy for high schoolers who ride TriMet.
- **Trade-off:** the redraws move more kids than PPS's plans (K-5, Balanced middle schools: 4,867 vs. 2,935 under PPS A, vs. PPS Status Quo). That is the main cost, along with messier feeder paths. "Rebalanced PPS A" keeps PPS A's closures and changes today's lines as little as possible to bring schools into range; it still moves more K-5 kids than PPS A and leaves three schools short in 2031-32.

**Calibration.** Model v2 is checked against PPS's own 2031-32 projections: [calibration report](build/solver/out_v2/CALIBRATION_public.md).

<!-- results:end -->

## What's in the repo

| Path | Contents |
|---|---|
| `build/data/` | **Data foundation.** `README.md` (method), `backtest.md` (can the model reproduce today's enrollment?), `blocks.parquet`/`.csv` (9,295 Census 2020 blocks with calibrated K-5/6-8/9-12 kids and current/Status-Quo/A/B assignments), `schools.csv`, `focus_dli.csv` + `focus_dli_homes.parquet` (estimated DLI/focus home locations), `scenarios.json` (A/B structure + PPS's per-school projections), `scenario_maps/` (PPS 2027-28 maps traced to GeoJSON), `boundaries/` (today's attendance areas), `scripts/01..10`, `work/` (intermediates) |
| `build/routing/` | Walk and bike distance matrices (block x school, local OSRM), school points, validation, build scripts |
| `build/research/` | `targets.md`/`.json`: sourced size targets, DLI rules, transport thresholds, scenario details. `sources/README.md` links the PPS documents used |
| `build/solver/` | CP-SAT solver (`solve.py`), data layer (`common.py`), scorecard (`metrics.py`), configs, `METHOD.md`, and `out/` results: per-option block assignments (`assign_*.parquet`), per-school `schools.csv`, `scorecard.json`, infeasibility reports, `compare.md` |
| `build/map/` | Builds `pages/map.html` (official-line tracing, diffs, street labels, embedded fonts). Its street and base layers come from `pages/pps-walk-redraw.html`, an early map kept only as a build input (not linked from the site). |
| `cowork/` | Earlier K-5 walk-redraw model (Node), polygon tools and the street-following "crisp" boundary method |
| `data/csv`, `data/geojson` | Tables and polygons extracted from the first-generation pages |
| `data/pps-map/` | `pps-model.json` (block universe: centroids, populations, adjacency, zones, walk distances) and `pps-race.csv` (2020 Census race by block), inputs to everything above |
| `scripts/fetch_raw.py` | Re-downloads the raw inputs that are not redistributed here |

## Rebuild

Python 3.12+ (built with 3.14).

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

**1. Raw inputs (not redistributed).** PPS PDFs, Family Guides, the PPS Data Explorer snapshot, Census raw tables and the OSM extract are fetched, not committed (plain-text copies of the PPS documents we cite are in `build/pps-texts/`):

```sh
export CENSUS_API_KEY=...     # free: https://api.census.gov/data/key_signup.html
python scripts/fetch_raw.py   # or one step: meub | boundaries | maps | guides | census | osm
```

**2. Data foundation.** Run `build/data/scripts/01..10` in numeric order (01 needs `CENSUS_API_KEY`). The derived outputs are already committed, so you can skip this to work on the solver.

**3. Routing (optional; matrices are committed).** Local OSRM in Docker via Colima:

```sh
colima start --cpu 4 --memory 4 --disk 20
cd build/routing
mkdir -p foot bike
cp osm/portland.osm.pbf foot/map.osm.pbf && cp osm/portland.osm.pbf bike/map.osm.pbf
bash run_build.sh foot foot && bash run_build.sh bicycle bike
docker run -d --name osrm-foot -p 5001:5000 -v "$PWD/foot:/data" osrm/osrm-backend osrm-routed --algorithm mld --max-table-size 100000 /data/map.osrm
docker run -d --name osrm-bike -p 5002:5000 -v "$PWD/bike:/data" osrm/osrm-backend osrm-routed --algorithm mld --max-table-size 100000 /data/map.osrm
python build_matrices.py && python validate.py
```

**4. Solver and scorecards.**

```sh
cd build/solver
python gen_configs.py                       # configs/*.json
python metrics.py                           # baselines: today, status quo, PPS A, PPS B
python solve.py configs/option1_durable.json
python compare.py                           # out/compare.md
```

The durable K-5 model solves all 9,295 blocks at once (about 15 minutes, ~1.5 GB RAM, 6 workers).

**5. Map page.** `cd build/map && python patch.py` (needs `osmium` for street labels).

Paths: code finds `data/pps-map/` relative to the repo; set `PPS_MAP_DIR` to override. The `cowork/crisp` scripts were written for a different working layout; set `CRISP_WORKDIR` and see `cowork/crisp/README.md`.

## Limits

- **Census blocks, not student addresses.** Where kids live comes from the 2020 Census (DHC ages by block, smoothed), calibrated so today's lines reproduce 2025-26 neighborhood enrollment by school. Moved blocks carry their old area's "capture rate" (private school, transfers, charters). Out-of-sample error is about 21-27% per school, so **any size within ~15% of a threshold is uncertain** (`build/data/backtest.md`).
- **DLI and focus-program homes are estimated**, not published: spread over the host's high school cluster (or district-wide) in proportion to Census kids. DLI by-grade counts are estimated.
- **Durability uses PSU's per-school forecast.** Each school follows its own row in PSU's July 2026 Table 5.5 through 2035-36, the end of that forecast. PSU's low/high scenarios are not used.
- **Year-by-year results are a projection, not a forecast.** Boundaries are held fixed; 2032-33 to 2035-36 are reported only.
- **Plan results are model estimates.** All plans shown are model v2 runs (calibrated, PSU 2031-32 basis); see each plan's scorecard. The solver's contiguity rule (zones "star-shaped" around the school) is stricter than necessary, and middle school is solved after K-5 rather than jointly.
- **PPS's maps were digitized** from vector PDFs (median georeferencing error ~70 ft). K-8 dashed areas and the Skyline inset are handled by rules. Our PPS A school sizes are within 5% of PPS's on average, but a few differ a lot.
- **High school** is judged on walk miles; transit time would be the right measure. Building capacities are PPS's 2025-26 school-profile functional capacities, captured second-hand (the earlier model used the 2021 LRFP).
- First-generation pages use an older model (NCES 2024-25 totals, public OSRM router) and are kept for reference.

## Sources and license

Every data source with links and licenses is in [SOURCES.md](SOURCES.md); every link is in [RESOURCES.md](RESOURCES.md). Code is MIT; the analysis, docs and results are CC BY 4.0; third-party data keeps its own license (OpenStreetMap-derived data is ODbL). See [LICENSE](LICENSE).

Copyright (c) 2026 Paul Frazier. Corrections welcome via GitHub issues.

*Built with AI: the research, data work, modeling and writing were done by AI (Claude, from Anthropic), directed and guided by Paul Frazier, a PPS parent. Best effort; it will have errors.*
