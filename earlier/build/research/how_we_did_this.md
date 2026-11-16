# How we did this

> **Built with AI.** The research, data work, modeling and writing on this site were done by AI (Claude, from Anthropic), directed and guided by Paul Frazier, a PPS parent. This is an independent analysis, not a Portland Public Schools product.

*Last updated 2026-10-15. A link tree of everything we used or read, with a few words on each.*

## The short version

We started with where kids live. We used the 2020 Census at the level of single city blocks (9,295 of them) and calibrated each block to real 2025-26 neighborhood-school enrollment. We measured real walking distances along streets and paths from every block to every school, with a local copy of the OSRM router on OpenStreetMap data. We sized every school with Portland State University's July 2026 per-school forecasts, the same forecasts PPS uses, for each year from 2027-28 to 2031-32. A solver then draws the lines. A school is at target when it is between its size floor (360 for K-5, 500 for middle, 1,100 for high school) and its building capacity. The one firm rule is to keep at least as many schools at target as PPS A every year; the solver also pushes every school toward target, then minimizes walking. Four of the five example plans keep every elementary school at target every year; Rebalanced PPS A gives up a few for fewer line changes. We checked our model against PPS's own numbers: on PPS's own lines, 58 of 62 schools land within 10% of PPS's Family Guide projections for PPS A in 2031-32 (51 in 2027-28, when PPS phases some changes in), and every miss is explained. **Every figure on this site is from our model, not from PPS**, unless it is quoted with a PPS source. PPS's own plans are shown with PPS's figures for school sizes and schools at target.

## How to read this page

- **Original:** the public link where the item lives. "Local copy only" means we have no recorded public link.
- **Local copy:** a plain-text Markdown copy kept for searching and quoting. Paths are relative to the project folder. Each copy starts with front matter that records its source link, retrieval date and a checksum of the original. The copies are unofficial text extractions and may contain errors; the original is always authoritative.
- **Labels:** **[PPS]** a PPS document · **[PSU]** Portland State's forecast for PPS · **[State]** Oregon law or rule · **[Second-hand]** a community or news source, or PPS data that someone else captured · **[Ours]** our own work.

---

## 1. PPS rightsizing documents

### 1a. PPS rightsizing web pages

All ten pages were archived on 2026-10-12. Index: `build/pps-texts/README.md`.

- **Rightsize hub page** [PPS]. Original: https://www.pps.net/about/portland-public-schools-information/rightsize · Local: `build/pps-texts/web-rightsize.md`. The landing page for the whole process. We used it to find every linked document.
- **Rightsizing Scenarios** [PPS]. Original: https://www.pps.net/about/portland-public-schools-information/rightsize/scenarios · Local: `build/pps-texts/rightsizing-scenarios-web-page.md`. The page that released PPS Status Quo, PPS A and PPS B. It links the overview and the four regional summaries.
- **How Could Your School Be Impacted?** [PPS]. Original: https://www.pps.net/about/portland-public-schools-information/rightsize/how-could-your-school-be-impacted (school list: https://view-awesome-table.com/-P3DWjCXVoIaFhxSyFlA/view/) · Local: `build/pps-texts/web-how-could-your-school-be-impacted.md`. The school-by-school lookup that links every Family Guide.
- **Frequently Asked Questions** [PPS]. Original: https://www.pps.net/about/portland-public-schools-information/rightsize/frequently-asked-questions · Local: `build/pps-texts/web-frequently-asked-questions.md`. PPS's answers on process, immersion and retention. It is also where the teachers' union agreement (MOU) is linked.
- **Rightsizing Presentations** [PPS]. Original: https://www.pps.net/about/portland-public-schools-information/rightsize/rightsizing-presentations · Local: `build/pps-texts/web-rightsizing-presentations.md`. The list of board decks, memos and resolutions from March to September 2026.
- **High School Feeder Patterns** [PPS]. Original: https://www.pps.net/about/portland-public-schools-information/rightsize/feeder-patterns · Local: `build/pps-texts/web-feeder-patterns.md`. Links the feeder-pattern PDFs in six languages (see 1e).
- **SEGC Documents** [PPS]. Original: https://www.pps.net/about/portland-public-schools-information/rightsize/segc-documents · Local: `build/pps-texts/web-segc-documents.md`. Links the two equity-audit reports on the 2023 Southeast changes.
- **Timeline** [PPS]. Original: https://www.pps.net/about/portland-public-schools-information/rightsize/timeline · Local: `build/pps-texts/web-timeline.md`. Dates for the decision process.
- **Videos** [PPS]. Original: https://www.pps.net/about/portland-public-schools-information/rightsize/videos · Local: `build/pps-texts/web-videos.md`. Six short explainer videos (transcripts in section 3).
- **Calendar** [PPS]. Original: https://www.pps.net/about/portland-public-schools-information/rightsize/calendar · Local: `build/pps-texts/web-calendar.md`. Community sessions. Only the static text was captured; events load by script.

### 1b. The scenarios (October 2026)

- **Scenarios Overview, district-wide comparison** [PPS]. Original: https://drive.google.com/file/d/1ueJVC-Jo6MRKw56Jedihc6YbVdBlSB2z/view (BoardBook copy, "District wide scenarios 10.04.26": https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505788) · Local: `build/pps-texts/scenarios-overview.md` and `build/pps-texts/boardbook-2026-10/boardbook-10-06-26-district-wide-scenarios-10-04-26.md`. Closures, receiving schools, K-8 to K-5 conversions and immersion moves for PPS A and PPS B, plus the size thresholds (360 / 500 / 1,100). It says all figures are 2031-32 projections, which is why we size schools on 2031-32 too.
- **Regional summaries (four)** [PPS]. Local copies in `build/pps-texts/regional-summary-*.md` and `build/pps-texts/boardbook-2026-10/boardbook-10-06-26-regional-summary-*.md` (same text, different files). Per-region closures, moves and sustainability measures. We used them to check the scenario structure.
  - Cleveland-Franklin: https://drive.google.com/file/d/1N60HZm5Gez3j-QxO7hhjlNw0XvvqmDRY/view · BoardBook https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505790
  - Grant-McDaniel: https://drive.google.com/file/d/15jfJajO5ydijfe3jhtV4s_qGWsuSm3YW/view · BoardBook https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505791
  - Jefferson-Roosevelt: https://drive.google.com/file/d/1fN8KvZOqKHPRX8rT4NSyM7vSr6-DUhLk/view · BoardBook https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505792
  - Wells-Lincoln: https://drive.google.com/file/d/1nvFOg4q0orwsqFQiQ11BgR2Gsau2y9RI/view · BoardBook https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505793
- **Family Guides, one per school (82)** [PPS]. Original: reached from https://www.pps.net/about/portland-public-schools-information/rightsize/how-could-your-school-be-impacted (each guide is a Google Drive PDF; every guide's own link is in its local copy's front matter and in `build/pps-texts/README.md`) · Local: `build/pps-texts/family-guide-<school>.md`. Each four-page guide (dated 2026-10-08) says what happens to the school under PPS A and PPS B, gives its capacity, and has PPS's own enrollment projections for 2027-28 to 2031-32 under "no changes", A and B. Those projections are what we calibrated against. Schools covered: Abernethy, ACCESS, Ainsworth, Alameda, Arleta, Astor, Atkinson, Beach, Beaumont, Benson, Beverly Cleary, Boise-Eliot/Humboldt, Brentwood, Bridger/Creative Science, Bridlemile, Buckman, Capitol Hill, César Chávez, Chapman, Chief Joseph, Clark, Cleveland, Creston, da Vinci, Dr. Martin Luther King Jr., Duniway, Faubion, Forest Park, Franklin, George, Glencoe, Grant, Gray, Grout, Harriet Tubman, Harrison Park, Hayhurst, Hosford, Ida B. Wells, Irvington, Jackson, James John, Jefferson, Kellogg, Kelly, Laurelhurst, Lent, Lewis, Lincoln, Llewellyn, Maplewood, Markham, Marysville, McDaniel, Metropolitan Learning Center, Mt. Tabor, Ockley Green, Odyssey, Peninsula, Richmond, Rieke, Rigler, Roosevelt, Rosa Parks, Rose City Park, Roseway Heights, Sabin, Scott, Sellwood, Sitton, Skyline, Stephenson, Sunnyside, Sunrise, Vernon, Vestal, West Sylvan, Whitman, Winterhaven, Woodlawn, Woodmere, Woodstock.
- **Attendance-boundary maps, school year 2027-28 (12 maps)** [PPS]. Originals on BoardBook (Oct 6, 2026 meeting) · Local: `build/pps-texts/boardbook-2026-10/boardbook-10-06-26-{status-quo,scenario-a,scenario-b}-attendance-boundaries-*.md` (text labels only). PPS's own lines for PPS Status Quo, PPS A and PPS B at each level. We traced them block by block (`build/data/scenario_maps/`), and our PPS baselines use those traced lines.

  | Map | K-5 | 6-8 | 9-12 | K-12 |
  |---|---|---|---|---|
  | PPS Status Quo | [14505804](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505804) | [14505802](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505802) | [14505803](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505803) | [14505805](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505805) |
  | PPS A | [14505796](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505796) | [14505794](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505794) | [14505795](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505795) | [14505797](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505797) |
  | PPS B | [14505800](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505800) | [14505798](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505798) | [14505799](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505799) | [14505801](https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14505801) |

### 1c. Board meeting materials

The BoardBook home for PPS (org 915) is https://meetings.boardbook.org/Public/Organization/915. Supplement index: `build/pps-texts/boardbook-2026-10/README.md`.

- **Oct 6, 2026 meeting agenda** [PPS]. Original: https://meetings.boardbook.org/Public/Agenda/915?meeting=769955 (supplementals: https://meetings.boardbook.org/Meeting/Supplementals/915?meeting=769955) · Local: `build/pps-texts/boardbook-2026-10/boardbook-10-06-26-agenda.md`. The scenario-release meeting and its 19 rightsizing attachments.
- **Oct 6, 2026 rightsizing slide deck** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14511742 · Local: `build/pps-texts/boardbook-2026-10/boardbook-10-06-26-boe-meeting-rightsizing-powerpoint.md`. How PPS built the scenarios, including "capped receiving schools at no more than two per closure" (p. 11), which we use in one solver option.
- **Scenario Release memo, Oct 5, 2026** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14509719 · Local: `build/pps-texts/boardbook-2026-10/boardbook-10-06-26-rightsizing-update-scenario-release-memo.md`. The written scenario description. It gives the split rules we follow (for example, Buckman 50/50 to Abernethy and Sunnyside; Maplewood 70/30 to Hayhurst and Rieke).
- **Board Q&A tracker, Oct 1, 2026** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14493920 · Local: `build/pps-texts/boardbook-2026-10/boardbook-10-06-26-supplemental-26-10-01-qa-tracker.md`. Staff answers to board questions. It confirms the PSU July 2026 forecast is PPS's enrollment baseline and links several documents below.
- **Board question tracker, Sept 14, 2026** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14421589 · Local: `build/pps-texts/boardbook-2026-10/boardbook-09-15-26-supplemental-board-question-tracker-26-09-14.md`. Earlier board questions and answers.
- **Draft rightsizing resolution, Sept 15, 2026** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14383792 · Local: `build/pps-texts/boardbook-2026-10/boardbook-09-15-26-draft-rightsizing-resolution.md`. A one-page draft resolution from a board member, read for context.
- **Sept 15, 2026 board deck** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14430171 · Local: `build/pps-texts/boardbook-09-15-26-boe-meeting-rightsizing-2.md` (extract also in `build/research/sources/board_deck_2026-09-15.txt`). PPS's decision framework and KPIs: the high-school size-range goal (slide 16) and post-modernization high-school capacities (slide 21) that we use.
- **Sept 8, 2026 committee deck, "Well-Resourced Schools"** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14374370 (Google Slides version: https://docs.google.com/presentation/d/1cb41ScRyaNDeOwDU7FgpcrxPknkgKqY57vesZi8i-_8/edit?usp=drive_link) · Local: `build/pps-texts/boardbook-2026-10/boardbook-09-08-26-tle-well-resourced-schools-rightsizing.md` and `build/pps-texts/boardbook-september-8-presentation-google-slides.md`. What PPS means by a well-resourced school, and the building-capacity minimums staff cited.
- **Sept 1, 2026 board deck** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14357211 · Local: `build/pps-texts/boardbook-09-01-26-boe-meeting-rightsizing-1.md`. Well-resourced schools and how many changes PPS expected to need.
- **Aug 4, 2026 board deck** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997425 · Local: `build/pps-texts/boardbook-08-04-26-boe-meeting-rightsizing.md`. Lessons PPS drew from the Southeast equity audit.
- **Aug 4, 2026 memo, "Rightsizing Update: Equity Audit Evaluation"** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997426 · Local: `build/pps-texts/boardbook-rightsizing-update-08-04-26-board-memo.md`. Where PPS says the 360 and 500 floors come from the state's Quality Education Model and the 1,100 high-school floor from the Jefferson dual-assignment work.
- **May 26, 2026 board deck** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997282 · Local: `build/pps-texts/boardbook-board-book-05-26-26-boe-meeting-rightsizing-1.md`. Resolution revisions and the policy factors to consider.
- **Resolution 7307, guiding principles and workplan** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997273 · Local: `build/pps-texts/boardbook-reso-7307-adopting-guiding-principles-and-workplan-in-the-rightsizing-process-for-portland.md`. The board's adopted principles for rightsizing, which we read as the rules any plan should respect.
- **Draft rightsizing guiding principles** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997246 · Local: `build/pps-texts/boardbook-draft-rightsizing-guiding-principles.md`. The draft that became Resolution 7307.
- **Resolution 7296, starting the rightsizing process (revised, and a proposed amendment)** [PPS]. Originals: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3990244 and https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3990653 · Local: `build/pps-texts/boardbook-resolution-7296-*.md`. Why the board started rightsizing: steady enrollment decline.
- **Mar 31, 2026 board work session book** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3988980 · Local: `build/pps-texts/boardbook-03-31-26-board-work-session-rightsizing-board-book.md`. Early framing; quotes the neighborhood-school assignment policy (4.10.045-P).
- **Mar 10, 2026 board materials, "Growing Great Schools"** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997004 · Local: `build/pps-texts/boardbook-03-10-26-board-materials-growing-great-schools-rightsizing-planning.md`. The first rightsizing planning update.
- **"Alternative & Focus School Overview," June 2026 committee deck** [PPS]. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997345 · Local: `build/research/sources/tle_focus_options_2026-06.txt` (plain extract, no front matter). Current immersion and focus-option pathways, and kindergarten immersion seats by language.
- **Oregon PTA school-consolidation guidance (Oct 2025)**, posted by PPS. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3991313 · Local: `build/pps-texts/boardbook-oregon-pta-school-consolidation-advisory-guidance.md`. Research and process advice on closures, read for background.
- **Denver Public Schools "Thrive Initiative" annual report**, posted by PPS. Original: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3990455 · Local: `build/pps-texts/boardbook-denver-schools-dps-dsti-annualreport-final-2.md`. Another district's consolidation report, read for background.
- **Memorandum of Understanding, PPS and Portland Association of Teachers** [PPS]. Original: https://drive.google.com/file/d/1P7FhiSZwHulEp7Q_r_iCkw_4zPpqaDTP/view · Local: `build/pps-texts/memorandum-of-understanding-pps-pat.md`. The 2025-26 furlough-day agreement over the budget shortfall. Context only.
- **Southeast equity audit: evaluation report** [PPS]. Original: https://drive.google.com/file/d/1gcq_2z1sc6yj90PJCsUc9yqrLfAVWxSz/view (BoardBook: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997427) · Local: `build/pps-texts/segc-equity-audit-evaluation-report.md`. What happened after the 2023 Southeast changes, including how immersion students responded when programs moved (pp. 48-49).
- **Southeast equity audit: school-by-school analysis** [PPS]. Original: https://drive.google.com/file/d/1xKJXsjio70jEAndFTHpr1_9FF3dQptlY/view (BoardBook: https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997428) · Local: `build/pps-texts/segc-equity-audit-school-by-school-analysis.md`. The same audit, one school at a time.

### 1d. Enrollment, lotteries and family surveys

- **Enrollment Summary, Oct 2025, by neighborhood and type of school attended** [PPS]. Original: https://www.pps.net/fs/resource-manager/view/d65fc69c-e9b5-4c13-8199-545d12deb541 · Local: `build/pps-texts/boardbook-2026-10/pps-enrollment-summary-oct-2025-capture-rates.md`. How many students in each neighborhood attend their own school, another one, or a program. We used it for focus-lottery students and the Lent-area students at Marysville (`build/data/v2/capture_2025_26.csv`).
- **PPS Data & Reporting pages** [PPS]. Originals: https://www.pps.net/departments/dataaccountability/data-and-accountability/data-strategy-and-insights/data-and-reporting and https://www.pps.net/departments/dataaccountability/data-and-accountability/data-strategy-and-insights/archives · No local copy of these pages. Where PPS posts capture-rate and enrollment reports. Two older capture-rate PDF links we found now return "not found".
- **Lottery waitlists, Sept 15, 2026 (focus options and immersion)** [PPS]. Original: https://drive.google.com/file/d/1IhkWQBAdcGROJU89JUXmluj2iqUS3Cef/view · Local: `build/pps-texts/boardbook-2026-10/pps-lottery-waitlists-2026-09-15.md`. Demand for focus and immersion seats, read for context.
- **2026-27 kindergarten lottery results, and middle/high school lottery transfer slots** [PPS]. Local copy only: `build/research/sources/k_lottery_results_2026-27.txt` and `build/research/sources/lottery_slots_ms_hs_2026-27.txt` (from PPS's Enrollment & Transfer pages; exact links not recorded). Used for focus-school seat counts and addresses (Winterhaven, da Vinci).
- **"Why They Stay and Leave," family survey summary, Jan 2026** [PPS]. Original: https://drive.google.com/file/d/1inDzPET-xRxzR8xZhCssQNMGI2JwSRbO/view · Local: `build/pps-texts/boardbook-2026-10/pps-why-they-stay-and-leave-summary-report.md`. Why families stay in or leave PPS. Background for the case for close, walkable neighborhood schools.

### 1e. Buildings, capacity and feeders

- **School Profiles 2025-26 (Power BI dashboard)** [PPS data, Second-hand capture]. Original: https://www.pps.net/departments/dataaccountability/data-and-accountability/data-strategy-and-insights/internal-school-profiles · Local: `build/pps-texts/school-profiles-2025-26/` (83 per-school text snapshots and a README). Our source for each building's current "functional capacity" (the ceiling in our size rule). The snapshots were taken by a parent-built project, not by us; spot checks match the Family Guides except Boise-Eliot/Humboldt.
- **Long-Range Facility Plan 2021, Vol 1** [PPS]. Original: https://www.pps.net/fs/resource-manager/view/84245cbd-4298-4803-8ba9-d26fb13a9c7a · Local: `build/research/sources/lrfp_2021_capacity_excerpts.txt` (excerpts only). How PPS computes functional capacity, and 2021 capacities we use where no newer figure exists.
- **High School Feeder Patterns, current** [PPS]. Original (English): https://www.pps.net/fs/resource-manager/view/b6a86fd0-fae1-4a0a-af46-72ee81348705 (also at https://resources.finalsite.net/images/v1790894228/ppsnet/f2u6fbkysoabacyo484j/PPS_High_School_Feeder_Patterns_Eng.pdf); Spanish https://www.pps.net/fs/resource-manager/view/5003be29-b005-4009-9b90-f172d52cd709; Russian https://www.pps.net/fs/resource-manager/view/f110e897-fe9d-4363-993d-94e7415e431e; Somali https://www.pps.net/fs/resource-manager/view/887f86f5-12ae-45bf-9349-2b3c2f800689; Vietnamese https://www.pps.net/fs/resource-manager/view/0bd6ff38-b4dd-426c-bbb0-edf05c6cd572; Chinese https://www.pps.net/fs/resource-manager/view/d6e584da-a6a8-44b4-80dd-7e24c1429fd6 · Local: `build/pps-texts/high-school-feeder-patterns-{en,es,ru,so,vi,zh}.md`. Which elementary and middle schools feed which high school, and the immersion pathways, after Jefferson's dual assignment ends.

### 1f. Transportation policy

Index with cited findings: `build/pps-texts/transportation/README.md`.

- **Student Transportation Service Guidelines (rev. Aug 7, 2024)** [PPS]. Original: https://resources.finalsite.net/images/v1751562292/ppsnet/thzskadliar1v7qds4yc/Service_Guidelines_Student_Transportation_2024.pdf · Local: `build/pps-texts/transportation/pps-transportation-service-guidelines-2024.md`. Who gets a bus: more than 1 mile for K-5 and 1.5 miles for middle school. Our "past the bus line" counts use these lines.
- **Supplemental Transportation Plan** [PPS]. Original: https://www.pps.net/departments/transportation/supplemental-transportation-plan · Local: `build/pps-texts/transportation/pps-supplemental-transportation-plan-web.md`. Hazard busing inside the walk zone. No hazard map is published.
- **Transportation FAQ** [PPS]. Original: https://www.pps.net/departments/transportation/frequently-asked-questions · Local: `build/pps-texts/transportation/pps-transportation-faq-web.md`. Plain-language rules, including TriMet for high schoolers.
- **Board Policy 4.10.100-P, Student Transportation Services** [PPS]. Original: https://www.pps.net/fs/resource-manager/view/d8da3d5d-1d38-40df-921d-d1ca07996e67 · Local: `build/pps-texts/transportation/pps-4-10-100-p-student-transportation-services.md`. The board policy behind the bus distances.
- **Administrative Directive 4.10.101-AD, transportation to neighborhood schools** [PPS]. Original: https://www.pps.net/fs/resource-manager/view/0217432e-56f7-4b68-81b3-281028e0d858 · Local: `build/pps-texts/transportation/pps-4-10-101-ad-transportation-neighborhood-schools.md`. How the policy is carried out.
- **Administrative Directive 4.10.049-AD, boundary changes** [PPS]. Original: https://www.pps.net/fs/resource-manager/view/c38f7930-5a61-483c-ad23-867d72b5be29 · Local: `build/pps-texts/transportation/pps-4-10-049-ad-boundary-changes.md`. PPS's own criteria for redrawing lines, including "minimize transportation times and distances."
- **PPS letter to the Legislature on HB 3014 (Feb 22, 2023)** [PPS]. Original: https://apps.oregonlegislature.gov/liz/2023R1/Downloads/PublicTestimonyDocument/53708 · Local: `build/pps-texts/transportation/pps-2023-hb3014-testimony.md`. PPS's stated support for students walking, biking and rolling to school.

---

## 2. Enrollment forecasts

- **PSU Population Research Center, *PPS Enrollment Forecasts 2026-27 to 2035-36* (July 24, 2026)** [PSU]. Original: https://www.pps.net/fs/resource-manager/view/8f9d62cd-5056-4cdc-8435-4bcba8ba86b1 (identical copy: https://drive.google.com/file/d/1YHR9m-nb55T0e8ZWdxDU3fol8tVWtXnS/view; also linked at https://resources.finalsite.net/images/v1785171463/ppsnet/ejdr22voeddvux8qwlob/PPS_Forecast_2026_27.pdf) · Local: `build/pps-texts/boardbook-2026-10/psu-prc-pps-enrollment-forecasts-2026-27-to-2035-36.md`. PPS's enrollment baseline. Table 5.5 forecasts every school and program year by year; we size every school with it. Table 5.2 is the district trend. Pages 23-24 explain PSU's method.
- **Our transcriptions of Table 5.5** [Ours, from PSU]. Local: `build/research/sources/psu_forecast_table5_5_by_school_program.json` (2025-26 and 2031-32) and `build/data/v2/psu_table5_5_by_year.csv` (every year, parsed by `build/data/v2/parse_psu_table5_5.py`). Machine-readable copies the solver reads. Check any number against the PDF.
- **PSU enrollment forecasts by grade group and school, 2025-35 (May 30, 2025, "Facilities" copy)** [PSU]. Original: https://drive.google.com/file/d/1zy_pcDNzJtzXfB011KwZDAwHCaNL_VU9/view · Local: `build/pps-texts/boardbook-2026-10/psu-prc-enrollment-forecasts-by-school-2025-35.md`. The previous year's school-level forecast. Its notes hold the only explicit immersion-allocation rule we found (for McDaniel Mandarin).

---

## 3. Board meetings and videos

No official transcripts exist. BoardBook says the official minutes are the video recordings (channel: https://www.youtube.com/@ppsboardofeducation; last posted written minutes: https://meetings.boardbook.org/Public/Minutes/915?meeting=758088). All transcripts we used are machine-made and contain errors; the video is authoritative. Every quote below cites the video and its timestamp.

We searched timestamped transcripts from Save PDX Schools (https://savepdxschools.org/transcripts/) [Second-hand] and a community caption archive [Second-hand]. We don't publish copies, because their speaker labels name board members, staff and public commenters.

| Date | Meeting | Video | What's in it for us |
|---|---|---|---|
| 2026-10-06 | Board regular meeting | https://www.youtube.com/watch?v=zOUH2Jq7Owo | The scenario release presentation. A second, unlisted upload (https://www.youtube.com/watch?v=-wwHhlqx0Us) has shifted timestamps; cite the public one. |
| 2026-09-29 | Board special meeting | https://www.youtube.com/watch?v=SPwXuNlwP_U | Bond audit and protocols; rightsizing comments. |
| 2026-09-23 | Facilities committee | https://www.youtube.com/watch?v=zfvbTie4mpE | Facilities context. The community transcript archive copy is machine-translated, so it isn't quoted here. |
| 2026-09-16 | Board retreat | https://www.youtube.com/watch?v=gw0gfK9RiDQ | Rightsizing discussion and KPIs. |
| 2026-09-15 | Board regular meeting | https://www.youtube.com/watch?v=uAf7l-ChjFo | Rightsizing KPIs (02:41:41-04:27:00), including the 70-100% "efficiently used" definition. |
| 2026-09-08 | Teaching, Learning & Enrollment committee | https://www.youtube.com/watch?v=S-pk57P6f_o | Well-resourced schools (00:04:55-01:15:00); staff on minimum building capacities. The community transcript archive copy is machine-translated, so it isn't quoted here. |
| 2026-09-01 | Board regular meeting | https://www.youtube.com/watch?v=5RMfvT-sAPU | Well-resourced schools. |
| 2026-08-04 | Board regular meeting | https://www.youtube.com/watch?v=-qhL23TOZTs | Equity-audit lessons. |

Moments we cite directly:
- PPS staff define efficiently used schools as 70-100% of capacity: https://youtu.be/uAf7l-ChjFo?t=15369
- PPS staff on minimum capacities ("our current K-5s all have the capacity for at least 360"): https://youtu.be/S-pk57P6f_o?t=3849
- The Oct 6 deck's "no more than two" receiving schools per closure: https://youtu.be/zOUH2Jq7Owo?t=5941

PPS's six explainer videos [PPS]. Short overviews of why and how PPS is rightsizing:
- "Introduction to Rightsizing": https://www.youtube.com/watch?v=K3u0UDq7DbA
- "Why do we have to Rightsize our schools?": https://www.youtube.com/watch?v=GqLIbfyd86Q
- "What is the goal of Rightsizing?": https://www.youtube.com/watch?v=N3Uk_YZ0LPU
- "What factors go into making decisions?": https://www.youtube.com/watch?v=sBOpHf1lp00
- "What is the process for making decisions?": https://www.youtube.com/watch?v=96KE5nBzjzY
- "How can the community engage in the discussion?": https://www.youtube.com/watch?v=QVi6Bfl_BnM

---

## 4. Oregon law and state documents

- **ORS 327.033 and 327.043** [State]. Original: https://www.oregonlegislature.gov/bills_laws/ors/ors327.html · Local: `build/pps-texts/transportation/ors-327-033-327-043.md`. The state rule that districts must bus elementary students living more than 1 mile from school and secondary students more than 1.5 miles.
- **ORS 332.405** [State]. Original: https://www.oregonlegislature.gov/bills_laws/ors/ors332.html · Local: `build/pps-texts/transportation/ors-332-405.md`. The board's general duty to provide transportation.
- **OAR 581-023-0040** [State]. Original: https://secure.sos.state.or.us/oard/view.action?ruleNumber=581-023-0040 (also read at https://oregon.public.law/rules/oar_581-023-0040) · Local: `build/pps-texts/transportation/oar-581-023-0040.md` (includes the Feb 2026 amendment). How the walk distance is measured, and who counts as elementary or secondary.
- **Quality Education Model prototype schools** [State]. Original: https://apps.oregonlegislature.gov/liz/2023R1/Downloads/CommitteeMeetingDocument/274502 · Local copy only of the quote, in `build/research/targets.md`. The state's 360-student elementary and 500-student middle-school prototypes that PPS's floors come from.

---

## 5. Data sources

- **US Census 2020: ages by block (DHC P12), single years by tract (PCT12), race by block (P.L. 94-171), block shapes (TIGER/Line)** [Federal]. Originals: https://api.census.gov/data/2020/dec/dhc and https://www.census.gov/geographies/mapping-files.html · Local: `build/data/raw/census/`, results in `build/data/blocks.parquet`. Where school-age kids live, split into K-5, 6-8 and 9-12, and the race counts behind our integration measure. Method: `build/data/README.md`.
- **Oregon Department of Education, Fall Membership 2025-26** [State]. Original: https://www.oregon.gov/ode/reports-and-data/students/Pages/Student-Enrollment-Reports.aspx (we used the copy in PPS Data Explorer) · Local: inside `build/data/raw/meub-pps-data/`. Enrollment by school and grade, the target we calibrate the blocks to.
- **NCES Common Core of Data, via the Urban Institute Education Data Portal** [Federal]. Originals: https://educationdata.urban.org/ and https://nces.ed.gov/ccd/ · Local: `build/routing/ccd2024.json`, `build/routing/school_points.csv`. School locations for routing, and the first-generation enrollment model.
- **City of Portland "School_Boundaries" map service** [City]. Original: https://services.arcgis.com/quVN97tn06YNGj9s/arcgis/rest/services/School_Boundaries/FeatureServer/0 · Local: `build/data/raw/boundaries/city_school_attendance_cells.geojson`, results in `build/data/boundaries/`. Current attendance areas at all three levels.
- **PPS ArcGIS attendance layer ("PPS_Boundaries_All_Grades", 2023-24 final)** [PPS]. Local copy only: `build/data/raw/boundaries/pps_boundaries_all_grades_23_24_final.geojson` (full service link not recorded). A cross-check: it matches the City layer to within 0.01% of area.
- **OpenStreetMap and OSRM** [Open data / open source]. Originals: https://www.openstreetmap.org/copyright (data license) and https://github.com/Project-OSRM/osrm-backend (router) · Local: `build/routing/` (`walk_miles.parquet`, `bike_miles.parquet`, `README.md`, `validation.md`). Walking and biking distances from every block to every school, computed on our own copy of the router. It matches the public FOSSGIS router (https://routing.openstreetmap.de/), used in our first-generation pages, with a median difference of 0.02 miles.
- **PPS Data Explorer** [Second-hand compilation of public data]. Original: https://github.com/meub/pps-data (site: https://ppsdata.info/) · Local: `build/data/raw/meub-pps-data/`. A parent-built collection of public PPS, ODE and PSU files: the school list, 2021 capacities, ODE enrollment, immersion details (PPS's "Enrollment Details for Language Immersion Schools," Oct 2025) and copies of the Oct 6 board files. It is the base of our school table.
- **Focus-option students by home catchment, 2025-26 (Google Sheet)** [**SECOND-HAND**], a community spreadsheet (not linked here). Local, public copy with counts under 10 masked for privacy: `build/pps-texts/focus-students-by-catchment-sheet-2025-26-public.md` and `build/data/v2/focus_by_catchment_2025_26_public.csv`. The model used the full counts. How many students in each neighborhood attend each focus option (ACCESS, da Vinci, Winterhaven and others). We used it only to place returning students in the "Close 2 focus options" what-if. Its first columns match PPS's Oct 2025 Enrollment Summary, but **the source of the per-program columns is not stated**, and its dollar columns are the sheet author's own estimates (not used).
- **Our derived data** [Ours]. Local: `build/data/README.md` explains each file: `schools.csv` (83 schools and programs), `blocks.parquet` (9,295 calibrated blocks), `focus_dli.csv` and `focus_dli_homes.parquet` (immersion strands and focus programs, with estimated home locations), `scenarios.json` (PPS A and PPS B in machine form, with PPS's Family Guide projections), `scenario_maps/` (our tracings of PPS's 12 maps), and `v2/` (2025-26 capacities, capture rates, implied immersion arrival shares, focus-by-catchment, PSU by year).
- **Backtest of the block model** [Ours]. Local: `build/data/backtest.md`. Tests whether Census blocks alone can predict each school's real enrollment. The answer sets our error bar: any size within about 15% of a threshold is uncertain.

---

## 6. Press and community work

### News coverage

- **OPB, Oct 5, 2026** [Second-hand]. Original: https://www.opb.org/article/2026/10/05/portland-public-schools-closures-rightsizing/ · Local copy only of quotes, in `build/research/targets.md`. Coverage of the scenario release; quoted for K-8 conversion context.
- **KATU, scenario release** [Second-hand]. Original: https://katu.com/news/local/portland-public-schools-proposes-closing-up-to-14-schools-amid-declining-enrollment · Local copy only of quotes, in `build/research/targets.md`. The receiving-school list, and "no DLI program would be eliminated."
- **KPTV interview with the PPS superintendent, Oct 6, 2026** [Second-hand]. Original: https://www.youtube.com/watch?v=vRKUxqyWvYg. Closures and the $65M shortfall in the district's own words.
- **Willamette Week, Apr 15, 2026, "PPS introduces another metric to inform school closures"** [Second-hand]. Original: https://www.wweek.com/news/schools/2026/04/15/pps-introduces-another-metric-to-inform-school-closures/ · Local copy only of quotes, in `build/research/targets.md`. A PPS spokesperson's definition of utilization.
- **Willamette Week, Dec 10, 2025, on North and Northeast enrollment balancing** [Second-hand]. Original: https://www.wweek.com/news/schools/2025/12/10/enrollment-balancing-in-north-and-northeast-portland-shows-the-consequences-of-overbuilding-high-school-capacity/ · Local copy only of quotes, in `build/research/targets.md`. Why PPS uses 1,100 as the high-school floor.
- **TriMet blog, Aug 20, 2025** [Second-hand]. Original: https://blog.trimet.org/2025/08/20/trimet-101-how-to-get-around-as-a-student/ · Local copy only of quotes, in `build/research/targets.md`. PPS high schoolers ride TriMet on their student ID, which is why walk miles are only a rough measure for high school.
- **Citizen Portal article on the scenarios** [Second-hand, AI-written]. Original: https://citizenportal.ai/articles/10621326/Oregon/School-Districts/Portland-SD-1J/Portland-school-leaders-propose-two-rightsizing-scenarios-one-with-up-to-14-school-closures · No local copy. The site blocked us, so we could not read or check it.
- **Govly meeting summaries** [Second-hand, AI-written]. Example: https://app.govly.com/public/meetings/50633 · No local copy. Summaries are public; full transcripts need a sign-in. Not used.

### Community analyses

We compared our data and results with five independent community projects. Full comparison with side-by-side number checks: `build/research/compare_resources.md`. Short public write-up: `build/research/other_models_section.md`. We link to them; the only one whose data we build on directly is PPS Data Explorer (section 5), plus the school-profile snapshots and the follow-rate trace noted below.

- **PPS Data Explorer** [Second-hand]. Original: https://ppsdata.info/ (source: https://github.com/meub/pps-data). A dashboard of enrollment, capacity, forecasts and building condition for every school. Its data is the base of our school table.
- **PPS School Explorer** [Second-hand]. Original: https://pps-explorer.codedaily.workers.dev/ (source: https://github.com/browniefed/pps-explorer). An address lookup for PPS Status Quo, PPS A and PPS B attendance areas. It traced PPS's maps independently of us, and the two tracings agree for 99.6-99.9% of kids.
- **PPS Closure Commutes** [Second-hand]. Original: https://chrisloer.github.io/pps-closures/ (maps: https://felt.com/map/PPS-school-closures-travel-time-impact-eRA1FAMvSHSebm5FQg9AcNA and https://felt.com/map/PPS-closures-travel-time-workbench-c6as0xMdQ3utb9AoiMhEBcC). How walk, bike and drive times change for each closing school's area. Its closure-area walks agree with ours within about 8-10%.
- **Right Size Portland** [Second-hand]. Original: https://rightsizepdx.com/ (explorer: https://rightsizepdx.com/rightsizing-scenario-explorer.html; source: https://github.com/southie/ppsrightsize) · Local excerpt: `build/research/follow_rate/sources/rightsizepdx_scenario_explorer.md`. Year-by-year sizes, busing and building costs, and custom scenarios. It assumes immersion programs move whole (100% follow).
- **PPS Dual Language Immersion & Rightsizing** [Second-hand]. Original: https://pps-dli-explorer.netlify.app/ (equity page: https://pps-dli-explorer.netlify.app/equity.html; source: https://github.com/jminnier/pps-dli-explorer) · Local excerpts: `build/research/follow_rate/sources/dli-explorer_*.md`. What the scenarios mean for immersion families. **It is the origin of the "80-84% follow rate"**: its own calculation from Family Guide numbers, not a PPS figure. Its snapshots of PPS's school-profile dashboard are our capacity source (1e).
- **Save PDX Schools transcripts** [Second-hand]. Original: https://savepdxschools.org/transcripts/. Searchable, speaker-labeled automated transcripts of board meetings; our primary transcript source (section 3).
- **Community transcript archive** [Second-hand]. Original: https://github.com/olivierbouwman/pps-rightsize/tree/b82a7dbd06040ca546421511838fb713d9b4acaa/transcripts/text. A caption archive of about 220 board meetings; our secondary transcript source.

---

## 7. Our research notes

- **Policy targets and scenario facts** [Ours]. Local: `build/research/targets.md` (and `targets.json`). Every size floor, ceiling, immersion and transportation rule we use, each traced to a source, plus the solver spec and the open gaps.
- **Source extracts** [Ours, from PPS]. Local: `build/research/sources/` (plain-text extracts of the Sept 1 and Sept 15 decks, Aug 4 memo, Mar 31 work session, Resolution 7307, scenario overview and regional summaries, feeder patterns, LRFP excerpts, transport guidelines, lottery sheets and the June focus-options deck, plus a crop of the PPS A 6-8 map and the Sept 15 KPI slide). Kept so quotes in `targets.md` can be rechecked offline. Original links are in the sections above.
- **Where PPS's own documents don't line up** [Ours]. Local: `build/research/pps_internal_gaps.md`. Three places where PPS's words, maps or numbers disagree (Lent-area students: Kelly vs Arleta; Buckman's lottery students; Rigler-area middle schoolers: Roseway Heights on the map vs Beaumont in the numbers), and which gaps are ours.
- **The immersion "follow rate"** [Ours]. Local: `build/research/follow_rate/report.md` (with `sources/` and `scripts/implied_follow.py`). Traces the "80-84%" to a community site's arithmetic. PPS states no rate. PPS's numbers imply about 80-83% arrive at Lent and Rigler, and the rest stay at the sending school.
- **PPS board-record findings** [Ours]. Local: `build/pps-texts/boardbook-2026-10/findings.md`. What PPS documents say about immersion follow shares and how the projections were built. PPS's "no changes" numbers equal PSU's forecast; no document explains how students were reassigned under PPS A and PPS B.
- **Transportation findings** [Ours]. Local: `build/pps-texts/transportation/README.md`. Oregon law and PPS policy on who gets a bus, each point quoted and cited.
- **Comparison with other public models** [Ours]. Local: `build/research/compare_resources.md` and `build/research/other_models_section.md`. Where our numbers agree with the five community projects, and why they differ where they do.

---

## 8. Our method and results

All figures here are our model's (model v2), on PSU's per-school forecast, not PPS's. Plan display names follow the site.

- **Method** [Ours]. Local: `build/solver/METHOD.md`. The full solver: inputs, size rules, the walking objective, exact contiguity (no islands), feeders, durability across 2027-28 to 2031-32, the v2 fixes, and known limits.
- **Plan briefs** [Ours]. Local: `build/solver/out_v2/BRIEFS.md`. One page per plan: how it works, the good, the bad, and the trade-off. It also explains why our plans can have shorter walks and more schools at target, and the catch (many schools sit just above 360, so a 9% enrollment miss hurts more).
- **Calibration against PPS's numbers** [Ours]. Local: `build/solver/out_v2/CALIBRATION.md` (data: `calibration_table.csv`). On PPS's own lines, 74 of 76 PPS Status Quo schools and 58 of 62 PPS A schools fall within 10% of PPS's Family Guide projections for 2031-32, and every miss is explained.
- **Line quality** [Ours]. Local: `build/solver/out_v2/LINES_QA.md` (referenced by METHOD.md section 9 and BRIEFS.md). Counts one-block notches and pockets: our cleaned elementary lines have 109-141 notches vs 197 under PPS A.
- **Bus need, fast proxy** [Ours]. Local: `build/solver/out_v2/BUSES.md`. Kids past the bus line under each plan, and schools that would newly need buses. PPS A adds about 1,600 kids past the line vs PPS Status Quo.
- **Walkability vs durability frontier** [Ours]. Local: `build/solver/out_v2/FRONTIER.md`. An early test of how much walking it costs to keep more schools at target. Not yet a clean result.
- **Tactical plans** [Ours]. Local: `build/solver/out_v2/TACTICAL.md`. Tries small moves at all three levels. None met all the hard rules.
- **Per-plan trade-offs** [Ours]. Local: `build/solver/out_v2/<plan>/TRADEOFFS.md`, one per plan:
  - `option2_ms460/` — "Boundary changes, balanced middle schools" (best example we modeled): spares 341 immersion students a move; 35 of 35 K-5 schools at target every year; a 460 middle-school minimum keeps elementary classes together (3 split) and fits every middle school in its building.
  - `option2/` — "Boundary changes, same closures": the same plan with PPS's 500 middle-school minimum; 12 of 13 middle schools at target, Hosford over capacity early, 13 elementary schools split between middle schools.
  - `option1_durable/` — "Redrawn K-8 lines": keeps every PPS A immersion move; best middle-school walking.
  - `option4/` — "Rebalanced PPS A": still moves more kids than PPS A, because fixing sizes takes moves.
  - `option3a/` — "Close 2 focus options: Winterhaven, da Vinci" (a what-if): best numbers, bought by closing two choice programs.
  - `option1_durable_hs/` — "Most schools that last, HS lines adjusted": tests moving whole elementary zones between high schools.
  - `option1_full.staging/` — "All lines redrawn, walkable K-12": dropped; redrawing high schools made trips longer.
  - `cap3_500_s2.staging/` — "Solver picks schools": dropped; letting the solver also choose closures didn't beat PPS A's closures with redrawn lines (middle-school walks 2.09 mi, about 1,500 more students moved) without moving more immersion students than PPS A.
  - `tactical_l/` — "Most schools last + large feeder fixes": the one tactical point that solved, with three rules broken.
- **First-generation scorecards** [Ours]. Local: `build/solver/out/compare.md`. Model v1 results, kept for the record.
- **The first-generation model** [Ours]. Local: `data/` (archived pages on the Archive page). Our earlier K-5-only model and pages (nearest walk, then balanced to 360-600). Superseded by METHOD.md.

---

## Gaps: sources we cite but couldn't trace to an original, or that are second-hand

- **Focus-students-by-catchment sheet.** Second-hand. The per-program columns have no stated source. Used only for the "Close 2 focus options" what-if.
- **"80-84% of immersion students follow a moved program."** A community site's inference from Family Guide numbers. PPS states no rate. Our model uses its own implied shares from PPS's numbers, labeled as inferred.
- **2025-26 building capacities.** PPS's numbers, but captured from PPS's dashboard by a community project, not by us. Boise-Eliot/Humboldt's 586 doesn't match the Family Guide's 632.
- **Lent-area students at Marysville (115).** The 115 is from PPS Closure Commutes. PPS's own Enrollment Summary gives 117, which we use.
- **Meeting transcripts.** All machine-made by community sites or YouTube. None is official. Two community transcript archive copies (Sept 8, Sept 23) are machine translations and must not be quoted.
- **PPS Data Explorer copies.** Second-hand copies of public files. PPS's "Enrollment Details for Language Immersion Schools" (Oct 2025) and ODE's fall membership file were read only from this repo; we have no PPS link for the immersion file.
- **PPS's 2025 utilization-model workbook.** Seen only through ppsdata.info, which says it came from a records request.
- **News quotes** (OPB, KATU, Willamette Week, TriMet). Used for context only. We keep no local copies, only the quotes in `targets.md`.
- **Lottery result and slot sheets.** PPS documents, but we did not record their exact links.
- **PPS ArcGIS boundary layer.** We kept the data but not the full service link.
- **LRFP 2021 and the June 2026 focus-options deck.** We hold only excerpts, without front matter.
- **Winterhaven and da Vinci building history.** From a search of a PPS historic-survey PDF and from Wikipedia; no links recorded, and the Winterhaven-as-Brooklyn-School point is unverified.
- **Citizen Portal and Govly.** Could not be read in full; not used.
- **PSU forecast hosts.** The pps.net and Google Drive copies are confirmed identical. The finalsite link cited on the site was not checked against them.

---

*This page and the analysis behind it were made by AI (Claude, from Anthropic), directed and guided by Paul Frazier. Every number is our model's unless a PPS source is quoted. Please check anything that matters against PPS's own documents.*
