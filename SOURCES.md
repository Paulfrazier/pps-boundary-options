# Sources, licenses and attribution

> This is an independent, best-effort analysis by a PPS parent, not an official Portland Public Schools product. Confirm anything that matters against PPS's own materials.

## Portland Public Schools (linked; text copies for checking)

The analysis cites and links each PPS document. The original PDFs are **not redistributed** here; plain-text copies of the documents we cite are kept in `build/pps-texts/`, each with its original link, for accessibility and so readers can check every quote. Numbers transcribed from them (closure lists, projections, capacities, targets) are attributed in `build/research/targets.md`, `build/data/README.md` and `build/data/scenarios.json`.

| Document | Used for | Link |
|---|---|---|
| Rightsizing scenarios site (overview + four regional PDFs, Oct 2026) | Scenario A/B closures, receivers, K-8 conversions, DLI/program moves | https://www.pps.net/about/portland-public-schools-information/rightsize/scenarios |
| October 6, 2026 Board of Education meeting materials: "Rightsizing Update: Scenario Release" memo and the **2027-28 attendance-area map PDFs** (Status Quo / A / B x K-5 / 6-8 / 9-12) | Digitized scenario boundaries (`build/data/scenario_maps/`) | BoardBook, org 915, Oct 6, 2026 Regular Meeting (item 8, Update: Rightsizing): https://meetings.boardbook.org/Public/Agenda/915?meeting=769955 (meeting ID taken from the `source_url` in `build/pps-texts/boardbook-2026-10/boardbook-10-06-26-agenda.md`; all PPS materials for the org: https://meetings.boardbook.org/Public/Organization/915 ). Map files 14505794-14505805, each at meetings.boardbook.org under `Documents/DownloadPDF/<id>?org=915` |
| Per-school Family Guides (82 PDFs) | PPS's own 2027-28 to 2031-32 projections per school under No change / A / B | https://www.pps.net/about/portland-public-schools-information/rightsize/how-could-your-school-be-impacted |
| Board decks, memos, Resolution 7307, TLE focus-options deck, equity audit | Size thresholds (360 / 500 / 1,100), KPIs, DLI and focus-option rules | Listed with links on the [How we did this](pages/how.html) page (from `build/research/how_we_did_this.md`), with text copies in `build/pps-texts/` |
| PPS School Profiles 2025-26 (Power BI report) | Building functional capacities in the current model (`build/data/v2/capacity_2025_26.csv`); Jefferson set to 1,773 after modernization (Sept 15, 2026 board deck, slide 21) | https://www.pps.net/departments/dataaccountability/data-and-accountability/data-strategy-and-insights/internal-school-profiles . **Second-hand:** captured by the pps-dli-explorer project's snapshots, archived in `build/pps-texts/school-profiles-2025-26/`; PPS's own profiles are the authority |
| Long-Range Facility Plan 2021, Vol 1 | Building functional capacities in the earlier model (v1) | https://www.pps.net/fs/resource-manager/view/84245cbd-4298-4803-8ba9-d26fb13a9c7a |
| High School Feeder Patterns | Current feeders, DLI pathways | https://resources.finalsite.net/images/v1790894228/ppsnet/f2u6fbkysoabacyo484j/PPS_High_School_Feeder_Patterns_Eng.pdf (our text copy, `build/pps-texts/high-school-feeder-patterns-en.md`, was taken from another PPS-hosted copy; same title, not byte-compared) |
| Service Guidelines - Student Transportation (2024) | Bus-eligibility distances (1 mi K-5, 1.5 mi 6-8 and 9-12; high schoolers within a mile of a TriMet stop get no yellow bus, and neighborhood high schoolers get TriMet youth passes) | https://resources.finalsite.net/images/v1751562292/ppsnet/thzskadliar1v7qds4yc/Service_Guidelines_Student_Transportation_2024.pdf |
| Enrollment Details for Language Immersion Schools, Oct 2025 | Cross-check of DLI strand counts | via the PPS Data Explorer project's `pps-data` repo (below) |

## Enrollment and forecasts

| Source | Used for | Link / license |
|---|---|---|
| **Portland State University Population Research Center**, *PPS Enrollment Forecasts 2026-27 to 2035-36* (July 2026): Table 5.5 (by school and program, to 2035-36; the basis for year-by-year sizes) and Table 5.2 (district medium forecast; used by the earlier model v1) | 2031-32 sizing basis, year-by-year school sizes 2027-28 to 2035-36, neighborhood vs. DLI split | Published by PPS: https://resources.finalsite.net/images/v1785171463/ppsnet/ejdr22voeddvux8qwlob/PPS_Forecast_2026_27.pdf ; also at https://www.pps.net/fs/resource-manager/view/8f9d62cd-5056-4cdc-8435-4bcba8ba86b1 (the copy in our text archive; same report title, not byte-compared). Table 5.5 transcribed in `build/research/sources/psu_forecast_table5_5_by_school_program.json`. Credit: Population Research Center, Portland State University |
| **Oregon Department of Education**, Fall Membership 2025-26 (sheet "School 20252026", Portland SD 1J) | Enrollment by school and grade, the calibration target | https://www.oregon.gov/ode/reports-and-data/students/Pages/Student-Enrollment-Reports.aspx (Oregon public records) |
| **NCES Common Core of Data** (school directory 2024, enrollment) via the **Urban Institute Education Data Portal** | School points (`build/routing/school_points.csv`, `ccd2024.json`), first-generation enrollment model | https://educationdata.urban.org/ (Urban Institute Education Data Portal, data from NCES CCD; US federal public data). Cite as: Urban Institute, Education Data Portal (Version 0.x), CCD; https://nces.ed.gov/ccd/ |

## Census and geography

| Source | Used for | Link / license |
|---|---|---|
| **US Census Bureau, 2020 Census Demographic and Housing Characteristics (DHC)**: P12 sex by age (blocks), PCT12 single year of age (tracts); 2020 P.L. 94-171 race (blocks); TIGER/Line 2020 blocks | Where school-age kids live (K-5 / 6-8 / 9-12 bands), race for the dissimilarity index, block geometry/centroids | https://api.census.gov/data/2020/dec/dhc , https://www.census.gov/geographies/mapping-files.html . US government work, public domain. This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau |
| **City of Portland** `School_Boundaries` feature service (PPS attendance cells, last edited 2025-11-03) | Today's K-5, 6-8 and 9-12 attendance areas (`build/data/boundaries/`) | https://services.arcgis.com/quVN97tn06YNGj9s/arcgis/rest/services/School_Boundaries/FeatureServer/0 . City of Portland open data; see the City's Open Data terms at https://www.portland.gov/ (attribution: City of Portland) |
| **pps-data** (the PPS Data Explorer project's repo, commit 80ec323, 2026-10-05) | Compiled PPS school list, LRFP 2021 capacities (earlier model), ODE/PSU/immersion files, board-meeting files | https://github.com/meub/pps-data . Code MIT-licensed; it redistributes public PPS/ODE data. Not copied here; fetched by `scripts/fetch_raw.py` |

## Street network and routing

| Source | Used for | License |
|---|---|---|
| **OpenStreetMap** (Geofabrik Oregon extract, clipped to Portland) | Walk and bike distance matrices (`build/routing/*_miles.parquet`, `validation_pairs.csv`), street lines and street-name labels on the map pages, street-following boundaries | **(c) OpenStreetMap contributors**, available under the Open Database License (ODbL) 1.0: https://www.openstreetmap.org/copyright . The derived distance matrices and street layers in this repo are offered under the ODbL |
| **OSRM** (Open Source Routing Machine, `osrm/osrm-backend` Docker image, foot and bicycle profiles) | Local routing engine that computed the matrices | BSD 2-Clause, https://github.com/Project-OSRM/osrm-backend |
| FOSSGIS `routing.openstreetmap.de` public OSRM foot router | Walk distances in the first-generation model (`cowork/`; those pages are kept offline) | Service by FOSSGIS e.V.; data (c) OpenStreetMap contributors, ODbL |

## Software and fonts

| Item | License |
|---|---|
| **Overpass** and **Overpass Mono** fonts (Google Fonts), latin subsets embedded in `pages/map.html` and in `build/map/fonts/`; loaded from Google Fonts by the other pages | SIL Open Font License 1.1, Copyright 2016 The Overpass Project Authors. Full text: [`fonts/OFL.txt`](fonts/OFL.txt) |
| Google OR-Tools (CP-SAT) | Apache 2.0 |
| pandas, NumPy, SciPy, Shapely, GeoPandas, pyproj, pyogrio, pyarrow, pdfplumber, openpyxl, requests | BSD / MIT / Apache 2.0 (see each package) |
| osmium-tool, mapshaper | GPL-3.0 / MPL-2.0 (used as command-line tools; not redistributed) |

## News coverage cited in the research notes

OPB (Oct 5 2026), KATU, Willamette Week: linked inline in `build/research/targets.md`; quoted briefly for context only.

## Reports by other organizations (public; linked and credited)

These public reports are linked to their originals. Plain-text copies are kept in `build/pps-texts/` so readers can check quotes, and each copy opens with its source link. Copyright stays with the authors.

| Report | Author | What we use it for | Original |
|---|---|---|---|
| Equity Audit Evaluation of PPS's Southeast Enrollment and Program Balancing Initiative (June 10, 2026), and its School-by-School Analysis | Dr. Terrance L. Green and Dr. Havala Hanson, for Portland Public Schools | The [Lessons from SEGC](pages/segc.html) page and the audit's size floors on [Why these sizes](pages/sizes.html) | https://drive.google.com/file/d/1gcq_2z1sc6yj90PJCsUc9yqrLfAVWxSz/view (school-by-school: https://drive.google.com/file/d/1xKJXsjio70jEAndFTHpr1_9FF3dQptlY/view); also in PPS board materials: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997427 |
| 2024 PPS Seismic Assessments, All Schools, Version 1.0 (May 15, 2024) | Holmes (structural engineers), for Portland Public Schools | Read while comparing community projects that use its seismic cost estimates; no figures used on this site | https://drive.google.com/file/d/1vN48MAzNDz1GvZ4pkSXRyAuiuNTWcnt7/view |
| Denver Schools Thrive Initiative annual report | Denver Public Schools | Background reading (from PPS's rightsizing presentations page); no figures used | https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3990455 |
| School Consolidation Advisory Guidance | Oregon PTA | Background reading (from PPS's rightsizing presentations page); no figures used | https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3991313 |

## Other PPS material we archived

Since this list was first written, the text archive in `build/pps-texts/` has grown. Each item has its source link in its front matter, and all are listed on the How we did this page:

- **October 2026 BoardBook documents** (`build/pps-texts/boardbook-2026-10/`): the scenario release, maps, regional summaries, supplemental Q&A and enrollment summary.
- **Board meeting transcripts**, timestamped. Used for research but not published here, because the speaker labels name individual board members, staff and public commenters.
- **Transportation law and policy** (`build/pps-texts/transportation/`): ORS 327.033/327.043 and 332.405, OAR 581-023-0040, PPS policy 4.10.100-P and administrative directives 4.10.049-AD and 4.10.101-AD, the 2024 service guidelines.
- **PPS School Profiles 2025-26 snapshots** (`build/pps-texts/school-profiles-2025-26/`), second-hand (see above).
- **Focus-option students by catchment, 2025-26** (`build/pps-texts/focus-students-by-catchment-sheet-2025-26-public.md`, `build/data/v2/focus_by_catchment_2025_26_public.csv`): a community spreadsheet, second-hand; used only for the Close 2 focus options what-if. Counts under 10 are masked in the public copies; the what-if used the full counts.

## Context

- **PPS family survey, "Why They Stay and Leave" summary report (Jan 6, 2026):** https://drive.google.com/file/d/1inDzPET-xRxzR8xZhCssQNMGI2JwSRbO/view. Why families stay in or leave PPS; background for the neighborhood-school and walkability arguments.
- **PPS scenario materials as text:** `build/pps-texts/` holds unofficial Markdown extractions of the Rightsizing scenarios pages and every linked document (overview, regional summaries, 82 Family Guides, feeder patterns, BoardBook presentations), each with its source link. Consult the originals.

## Related community work

Other independent analyses we compared against (details and number checks in `build/research/compare_resources.md`):

| Resource | Notes | Link |
|---|---|---|
| Portland Public Schools Data Explorer | [source repo](https://github.com/meub/pps-data), which this project also uses | https://ppsdata.info/ |
| PPS School Explorer | [source repo](https://github.com/browniefed/pps-explorer) | https://pps-explorer.codedaily.workers.dev/ |
| PPS Closure Commutes | | https://chrisloer.github.io/pps-closures/ |
| Right Size Portland | [source repo](https://github.com/southie/ppsrightsize) | https://rightsizepdx.com/ |
| PPS Dual Language Immersion & Rightsizing | [source repo](https://github.com/jminnier/pps-dli-explorer) | https://pps-dli-explorer.netlify.app/ |

## Every link

`RESOURCES.md` lists every external link this project fetched or cites, grouped by site, with the project file that references it.

## Inferred and second-hand figures

Some model inputs are not stated directly by PPS. They are flagged here so readers can weigh them:

- **DLI follow shares** (how many immersion students move with a relocated program: Lent ~0.80, Rigler ~0.83, Woodstock 0.84–0.93, Chávez ~0.89, Beaumont→Roseway ~0.90) are **implied** by PPS Family Guide enrollment projections, not stated by PPS. Derivation: `build/research/follow_rate/report.md`; values used: `build/data/v2/dli_follow.json`.
- An **80–84% follow rate** that circulated in community discussion came from a community site, not PPS. It was used only as a cross-check and is not a model input.
- **Where Winterhaven and da Vinci students live** (Close 2 focus options what-if) comes from a community spreadsheet of focus students by catchment. Its first columns match PPS's October 2025 Enrollment Summary; the per-program columns' source isn't stated.
- **2025-26 school capacities** were captured second-hand from snapshots of PPS school profiles (via the pps-dli-explorer project) and archived in `build/pps-texts/school-profiles-2025-26/`; PPS's own profiles are the authority.


*Built with AI: the research, data work, modeling and writing were done by AI (Claude, from Anthropic), directed and guided by Paul Frazier, a PPS parent. Best effort; it will have errors.*
