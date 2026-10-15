# "Why these sizes": research notes

Compiled 2026-10-14 for the site page "Why these sizes" (PPS's 360 / 500 / 1,100 school-size thresholds). Every source read for this page is saved as Markdown under `sources/` (front matter: title, source_url, retrieved 2026-10-14, publisher). Local PPS texts are cited by their `build/pps-texts/` file.


> The `sources/` text copies named below are kept locally and not published (some contain staff contact details from the PDFs). Every source here also has its public URL.

Labels: **[STATE]** Oregon state body or statute. **[PPS]** PPS document or meeting. **[AUDIT]** the PPS-commissioned SEGC equity audit. **[RESEARCH]** academic or other-state work. **[3P]** community site or news. **[2ND-HAND]** quoted from someone else's quotation and not checked against the original. **[UNVERIFIED]** not confirmed.

Page numbers: "PDF p." is the page in the PDF file; "printed p." is the number on the page. In the QEM reports they differ (2026: printed = PDF − 2; 2024: printed = PDF − 2; 2022: printed = PDF − 2).

---

## Headline

1. **PPS's numbers come from the state's cost model, not from a state size rule.** PPS: "We used the threshold of 360 students for elementaries and 500 students for middle schools as guided by the prototype school description in the Quality Education Model" [PPS, Aug 4 2026 memo]. The Quality Education Model (QEM) is the state's model for estimating how much money Oregon schools need. It prices three made-up "prototype" schools: elementary 360, middle 500, high 1,000.
2. **The QEM prototypes are averages used for costing. They are not minimum sizes.** The QEM says the prototypes "do not represent any actual schools but are composites representing an average school for its category" [STATE, QEM 2026, printed p.91]. The Legislature's research office says "Schools in Oregon are not required to adhere to the model's components" [STATE, LPRO Issue Brief, Dec 2023, p.2]. No Oregon statute or rule sets a minimum school size. The only state-law size line, ORS 327.077, gives *extra* funding to small remote schools, and it does not apply to PPS.
3. **PPS turned the averages into floors.** PPS uses them as "sustainability thresholds" and calls them a "minimum enrollment to offer stable programming" [PPS staff, Oct 6 2026]. Family Guides call them "planning goals, not ratings of school quality."
4. **PPS's own equity auditor said to go higher, and not to use the numbers as closure triggers.** The SEGC audit suggests planning floors of "approximately 450+" (K-5), "600+" (middle) and "650+" (K-8). It adds: "these numbers should not be used as automatic closure thresholds" [AUDIT, pp.145-146].
5. **The research the QEM cites gives ranges, not floors.** Cotton (1996) gives 300-400 for elementary and 400-800 for secondary. Lee & Smith (1997) put the ideal high school at 600-900. Leithwood & Jantzi (2009) recommend *upper* limits of about 300-500 (elementary) and 600-1,000 (secondary). PPS's 1,100 high-school floor is above every one of these ranges. It came from PPS's Jefferson work, not from the QEM, whose high school prototype is 1,000.

---

## (a) Third-party chart: which site, and its design

Searched all five sites (HTML, live DOM via gstack browse, JS bundles). Notes: `sources/third-party-size-charts-notes.md`.

| Site | Size/threshold chart? |
|---|---|
| **rightsizepdx.com** (Right Size Portland; github.com/southie/ppsrightsize) | **Yes, the richest.** "The sustainability threshold impact on cost per student by school size" draws the threshold as a line, plus three more threshold-based sections. |
| PPS Data Explorer (ppsdata.info; github.com/meub/pps-data) | Yes: "Schools and students at a sustainable size in 2031-32" (grouped bars). The budget page also has "Cost per student and school size", a scatter with a **"Show as a table" graph/table toggle** but no threshold line. |
| PPS Closure Commutes (chrisloer.github.io/pps-closures) | Yes: "Shorter trips, or fuller schools?", a scatter of boundary strategies (added walk minutes vs K-5 schools at 360+). |
| pps-explorer.codedaily.workers.dev | No. Boundary map only. |
| pps-dli-explorer.netlify.app | No threshold chart. |

**Which one is "the graph view"?** No site has a control literally labelled "Graph view". The likeliest matches:
- **rightsizepdx's threshold chart**: the only chart that draws the 360/500/1,100 line against schools.
- **ppsdata.info's cost-vs-size scatter**: it has the graph/table toggle.

The design spec below follows rightsizepdx and borrows the tab and table toggle from ppsdata. **Confirm with Paul.**

### Primary inspiration: rightsizepdx.com, "The sustainability threshold impact on cost per student by school size"
URL: https://rightsizepdx.com/rightsizing-scenario-explorer.html (section heading has a "Link" anchor)

- **Type:** small multiples, one panel per level (K-5 schools, K-8 schools, Middle schools (6-8), High schools (9-12)). Three panels per row on desktop; each SVG is about 390 x 240 px.
- **Axes:** x = enrollment ("students"), linear, with its own range per panel (K-5 about 150-650; HS about 500-2,300). y = cost per student in dollars ($7k-$15k for K-5). Light grey horizontal gridlines; small grey tick labels.
- **Data marks:**
  - A dark grey stepped line shows the staffing-formula cost per student at every enrollment. Solid is non-Title I; dashed (4/3) is Title I where it differs. Each step is where the formula adds a homeroom, an assistant principal or a support position.
  - Each real school is a dot at its current enrollment: **red below the threshold, green at or above**. Dots have a white 1px outline at 95% opacity.
  - Schools closing in the selected scenario get a thick dark ring.
- **Threshold drawing:**
  - A **vertical blue line (1.5px) over a pale blue band** (same blue at about 18% opacity).
  - A two-line blue label sits at the top of the line: "threshold 360: $8,226 formula" and "◇ $9,815 General Fund (actual)".
  - A filled blue dot marks where the cost curve crosses the threshold. A hollow blue diamond marks the General Fund figure.
- **Caption under each panel:** counts in one sentence (e.g. "45 schools, 157–547 students (2027-28); 38 below the threshold (red dots); 13 closing in Scenario A (ringed)…").
- **Interaction:** native SVG hover tooltips on every dot and marker (school, enrollment, $ per student, Title I, closes in A). A sticky scenario switcher (Status Quo / A / B / Custom segmented buttons) recolours and re-rings the dots.
- **Colours:**

  | Element | Colour |
  |---|---|
  | Background | #fcfcfb |
  | Gridlines | #d9d7d0 |
  | Axis text | #7a7974 |
  | Curve | #52514e |
  | Threshold | #2a78d6 |
  | Below-threshold dots | #9b2321 |
  | At-or-above dots | #1d6b2c |

  Light theme, system-ui font.

Take the idea, not the code or text: per-level panels, a threshold line with a soft band and an inline label, dots coloured by side of the line, a one-sentence count caption, and hover details.

### Secondary: ppsdata.info
- **"Schools and students at a sustainable size in 2031-32"** (https://ppsdata.info/#section-rightsizing): Plotly horizontal grouped bars.
  - Two rows: Students and Schools. Three bars each: Status quo in grey, Scenario B, Scenario A.
  - x axis 0-100%, value labels outside the bars, legend centred below.
  - Dark theme (#161b22), Nunito Sans. The full PPS measure table sits below.
- **"Cost per student and school size"** (https://ppsdata.info/budget.html#section-schools): Plotly scatter.
  - x = projected 2026-27 enrollment; y = PPS "Dollars per student" 2026-27.
  - Blue circles are not Title I; green diamonds are Title I.
  - Controls: level tabs (K-5 / K-8 / Middle / High / All), a "Mark schools" select (closing in A / B), and a collapsed "Show as a table" disclosure.
  - No threshold line.

### Tertiary: PPS Closure Commutes (chrisloer.github.io/pps-closures), "Shorter trips, or fuller schools?"
Hand-built SVG scatter, one per scenario:
- x = average added walk minutes for students who move.
- y = K-5 schools with 360+ students (or middle schools with 500+).
- Each dot is a boundary-drawing strategy, labelled, with PPS's plan ringed.

The hint line "Today about 14 of 53 K–5 neighborhood schools have 360+ K–5 students (estimate)" is their estimate [3P]. It differs from our ODE count (11 of 44); see (f).

---

## (b) Quality Education Model facts, with quotes

Landing page with every report: https://www.oregon.gov/ode/reports-and-data/taskcomm/Pages/QEMReports.aspx (`sources/ode-qem-reports-page.md`). Latest: **Quality Education Commission QEM Report 2026**, https://www.oregon.gov/ode/reports-and-data/taskcomm/Documents/Quality%20Education%20Commission%20QEM%20Report%202026.pdf (`sources/qem-2026-quality-education-commission-report.md`).

### b1. The prototypes (2026 report, PDF p.93 / printed p.91) [STATE]
> "The model developed in 1999 uses three prototype schools as a basis for generalizing the costs to operate schools statewide. The prototypes represent typical characteristics and resources of an elementary school, middle school, and high school in Oregon. The prototypes do not represent any actual schools but are composites representing an average school for its category. A research synthesis conducted by Education Northwest indicates that an effective size for elementary schools is between 300-400 students and that middle schools that are effective range from 400-800 students. The ideal high school is between 600-900 students. The prototype schools are informed by related research."
> (Footnotes 98 and 99: "Cotton, K. (1996). School Size, School Climate, and Student Performance"; "Lee, V., Smith, J. (1997). High School Size: Which Works Best and for Whom?")

The "PROTOTYPE SCHOOLS" box on the same page:

| Prototype | Size | Staffing and class-size assumptions (verbatim bullets) |
|---|---|---|
| Elementary School | **360 Students** | All-day kindergarten; Class size average of 20; 1 librarian per school; 1 school nurse per school; 1 PE and music specialist per school; 1 Family Resource staffer per school; Computers for students & staff |
| Middle School | **500 Students** | Class size average of 17.7; 1.5 additional teachers for math, English, and science; Alternative programs for special needs and students whom the system places at risk; Volunteer coordinator and community outreach worker; One counselor for every 250 students; Adequate campus security; 1 school nurse per school; 1 librarian per school; Computers for students & staff; 1 Family Resource staffer per school |
| High School | **1,000 Students** | Class size average of 20.7; 3.0 additional teachers for math, English, and science; Alternative programs; Volunteer coordinator and community outreach worker; One counselor for every 250 students; Adequate campus security; School-to-work coordinator; 1 school nurse; 1 librarian per school; 1 Family Resource staffer per school; Computers for students & staff |

Footnote 100 on the same page:
> "The QEC Status Quo Core K-12 State Funding model uses the actual staffing ratios from the base year for schools in the approximate size of the prototype schools. The Full QEM, shown here, uses the Commission's research-informed recommended ratios."

The middle-school class size changed between editions: 20.8 in the 2022 and 2024 reports, 17.7 in 2026. The SEGC audit used 20.8 (from 2024).

### b2. What the prototypes are for: adequate *funding*, at *efficiently-scaled* schools [STATE]
- QEM 2026, PDF p.93 / printed p.91: the model "provides a reasonable framework based on data, research, professional judgment, and public values, for estimating an adequate level of funding to achieve the state's quality education goals."
- QEM 2026, PDF p.94 / printed p.92 (statistical approach): the Commission analyzes data "in order to estimate the per-pupil costs of instruction in **efficiently-scaled** elementary, middle and high schools within the State of Oregon." Same wording in QEM 2024, PDF p.58 / printed p.56.
- QEM 2026, PDF p.15 / printed p.13: the model benchmarks the costs "required to provide a quality education to the average student in a prototype brick and mortar school."
- QEM 2026, Appendix B, PDF p.128 / printed p.126 (Method #2): "the model incorporates the actual observed staffing levels, student-staff service ratios for these positions in schools at or near the size of the prototype schools to determine what those per-pupil expenses are and multiplies those figures by the salary assumptions."
- QEM 2024, PDF p.10 / printed p.8: "The QEM was initially developed to estimate the base level (not optimal level) of funding required to operate a system of effective schools in Oregon in 1999."
- QEM 2012 (https://www.oregon.gov/ode/reports-and-data/taskcomm/Documents/QEMReports/2012QEMFinalReport.pdf), PDF/printed p.14, "Prototype Resource Assumptions": "The size of each school is within a range that research literature recognizes as efficient."
- QEM 2000 Final Report (https://www.oregon.gov/ode/reports-and-data/taskcomm/Documents/QEMReports/2000QEMFinalReport.pdf), PDF p.12 / printed p.5 (OCR text):
  - The prototypes were "constructed to be examples of schools in Oregon that have been structured to provide resources consistent with best, research-based practices."
  - "The size of each is at a level within a range the research literature recommends as optimal."
  - On PDF p.11 / printed p.4: "Within actual schools, educators can use the Prototype School as a benchmark for staffing and activity levels needed, but they can modify and reallocate."

**Bottom line: efficient or adequate, not minimum.**
- Every edition describes the prototypes as average, "efficiently-scaled" or "optimal-range" schools used to *price* an adequate education.
- No edition calls them a minimum, a floor or a closure standard.
- The LPRO brief is explicit: "Schools in Oregon are not required to adhere to the model's components. In Oregon, school districts have the authority to devise local budgets according to their own needs" [STATE, https://www.oregonlegislature.gov/lpro/Publications/Oregon%20Quality%20Education%20Model%20-%20Issue%20Brief%20Dec.%202023.pdf, p.2; `sources/lpro-2023-12-qem-issue-brief.md`].
- The same brief, p.2: "For 2022, the QEC defined the prototypical schools as an elementary school of 360 students, a middle school of 500 students, and a high school of 1,000 students. The prototypes for each level identify specific class sizes, staffing ratios and key positions. After staff calculates the costs of these prototype schools, they scale those costs up for the entire state."

### b3. The state itself says the prototypes are dated and too few [STATE]
- QEM 2024, PDF p.20 / printed p.18: "The Quality Education Model's costing approach relies on a set of 'prototype schools' that were established in 1999 and based on research regarding optimal school sizes for traditional brick and mortar schools within each grade band of Elementary, Middle and High School. Changes in the delivery of education, student and community needs, technological advancements, and significant demographic shifts means that these prototypes no longer fully account for the diverse conditions and communities present across Oregon."
- QEM 2024, PDF p.22 / printed p.20: "An updated QEM should incorporate additional prototype schools, adding a second high school prototype school and a virtual school prototype, account for regional differences in terms of cost impacts (rural/urban)…"
- QEM 2024, PDF p.61 / printed p.59 ("Limitation"): "Because the prototypes represent average schools, the model does not capture the variations in costs associated with the unique challenges facing different school settings, such as small rural schools and larger schools in metropolitan areas."
- QEM 2026, PDF p.99 / printed p.97: "While the AIR report recommended increasing the number of prototype schools … The commission agrees additional prototype schools should be added but it has not had the staffing capacity to do so."
- The American Institutes for Research (AIR) evaluation, as summarized by the Legislative Policy and Research Office (LPRO), Oct 22 2025 (https://olis.oregonlegislature.gov/liz/2025I1/Downloads/CommitteeMeetingDocument/310513, PDF p.8; `sources/lpro-2025-10-air-summary-310513.md`):
  - "The QEM prototypes use enrollment sizes based on decades-old research estimates." Rated "Partially follows best practice."
  - "The QEM has 3 prototypes based only on school level." Rated "Does not follow best practice."
  - The AIR report itself was not read [2ND-HAND via LPRO]. LPRO's May 28 2025 memo is at https://apps.oregonlegislature.gov/liz/2025R1/Downloads/CommitteeMeetingDocument/307317.

### b4. History: the elementary prototype was 340 until at least 2018 [STATE]
- 2004 (PDF p.42), 2012 (p.14), 2014 Vol 1 (Exhibit 5), 2016 and 2018 (Appendix A): "Elementary School—340 Students". Middle 500 and high 1,000 are unchanged throughout.
- The 2020 report text does not list prototype sizes.
- 2022 (PDF p.10 / printed p.8), 2024 and 2026: "Elementary School—360 Students".
- No report explains the change from 340 to 360. *[UNVERIFIED reason. Note: 360 = 6 grades × 3 classes × 20, matching the 20-student class-size average.]*
- The Feb 2025 QEC/ODE slides to the House Education Committee say "Elementary (360 students)" on one slide (PDF p.6) and "Elementary School—340 Students" on another (PDF p.12): https://apps.oregonlegislature.gov/liz/2025R1/Downloads/CommitteeMeetingDocument/307264.
- The 2023 committee document named in the brief (https://apps.oregonlegislature.gov/liz/2023R1/Downloads/CommitteeMeetingDocument/274502, PDF p.4) lists: "Professional judgement model based on three prototype schools Elementary (360 students), Middle (500 students), and High (1,000 students) and best practices." **Confirmed.**

### b5. Small schools in Oregon law and QEM [STATE]
- The QEM has **no small-school adjustment.** It has three average prototypes only. The 2024 report lists the missing variation for "small rural schools" as a limitation (above).
- **ORS 327.077** (`sources/ors-327-077-remote-small-schools.md`; https://www.oregonlegislature.gov/bills_laws/ors/ors327.html) is the State School Fund's "small school correction". It *adds* funding weight for:
  - **Remote small elementary schools.** For six grades, average daily membership must be "below 168", and the school must be more than 8 road miles from another elementary in the district.
  - **Small high schools.** Four grades "below 350", in a district with ADMw under 9,500.
  - PPS qualifies for neither. This is the only size line in Oregon school-finance law, and it treats small schools as legitimate but costlier, not as unsustainable.
- ODE, *The Costs of Operating Small Schools in Oregon*, Oct 25 2002 (https://www.oregon.gov/ode/reports-and-data/taskcomm/Documents/SFTF/2014.01.SFTFCostOfOperatingSmallSchoolsInOregon.pdf; `sources/ode-2002-costs-of-operating-small-schools.md`):
  - Printed p.1: "School size has a dramatic affect on per student costs for Oregon high schools, with costs per student rising rapidly as sizes fall below about 300 students." And for elementary schools, "costs rising rapidly at sizes below about 100 students."
  - Printed p.2: "It is possible to reduce the per-student operating costs by forming fewer, but larger, schools in Oregon's sparsely populated areas. There is, however, a tradeoff between the lower operating costs that are possible with larger schools and other factors that are important to families and communities—in particular, the amount of time students must spend traveling to and from school…"
  - Printed p.5: "a number of researchers have estimated that the optimal high school size is between 500 and 1,000 students, with optimal sizes for elementary and middle schools being somewhat smaller than that."
- QEM 2004 (PDF p.40 / printed p.32), citing the 2002 study: "although costs per student are dramatically higher for high schools with less than 200 students, high schools with enrollments from 500 to 2400 students cost roughly the same per student, indicating that no further cost saving from economies of scale exist at school sizes above 500."

### b6. High school: QEM 1,000 vs PPS 1,100
- The QEM high school prototype is **1,000** in every edition checked (2004-2026). The research it cites puts the "ideal high school" at **600-900** [STATE, QEM 2026, printed p.91].
- PPS's **1,100** is its own number: "the 1100 students threshold we developed during the sunsetting of Jefferson dual assignment process" [PPS, Aug 4 2026 memo, `build/pps-texts/boardbook-rightsizing-update-08-04-26-board-memo.md`, p.2].
- Willamette Week [3P, Dec 10 2025]: keeping each high school "above 1,100 by 2030–31, which district officials say is necessary to justify comprehensive programming." https://www.wweek.com/news/schools/2025/12/10/enrollment-balancing-in-north-and-northeast-portland-shows-the-consequences-of-overbuilding-high-school-capacity/ (quoted from `build/research/targets.md`; not re-read today).
- PPS's Sept 8 2026 slide: "9TH-12TH GRADE Sustainable Threshold: ~1,100 students", contrasting "PRIOR TO HS REDESIGN (2009-2011)" with "CURRENT STATE". No calculation behind 1,100 was found.
- So 1,100 is 10% above the QEM prototype and above every research range on this page.

---

## (c) PPS statements on why size matters

| # | Quote | Source |
|---|---|---|
| c1 | "We used the threshold of 360 students for elementaries and 500 students for middle schools as guided by the prototype school description in the Quality Education Model. We applied the same number for K-8s and used the 1100 students threshold we developed during the sunsetting of Jefferson dual assignment process." | [PPS] Board memo "Rightsizing Update: Equity Audit Evaluation", Aug 4 2026, p.2, https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997426 |
| c2 | "Maintaining more than 80 school sites amid declining enrollment has spread resources increasingly thin. Schools experience this through blended classrooms, an increase in itinerant staff, reduction in school-wide supports such as counselors or social workers, or courses being offered in alternate years." … "69% of K8 and 47% of middle schools falling 100 students or more below the enrollment for stable programming by 2031-32." | same memo, p.2 |
| c3 | "SUSTAINABILITY THRESHOLDS BY GRADE BAND … Comparable does not mean identical, it means every student can reach a strong, well-supported school experience." K–5: "2-3 sections per grade • Weekly arts, library and PE • Intervention and tutoring based on need • Counseling and nursing support on site". 6–8: "6-8 sections per grade • Full elective rotation: arts, world language • Intervention based on need • Counseling and nursing support on site". 9–12: "Staffing and courses that support graduation • 2+ languages, sequential arts, AP/IB/Dual Credit • 9th grade success and credit recovery • Counseling and nursing support on site" | [PPS] Sept 8 2026 "Well-Resourced Schools" deck, slide 7, https://docs.google.com/presentation/d/1cb41ScRyaNDeOwDU7FgpcrxPknkgKqY57vesZi8i-_8/edit (`build/pps-texts/boardbook-september-8-presentation-google-slides.md`) |
| c4 | "WHAT HAPPENS IF WE DON'T ACT NOW? By 2031-2032, most elementary and middle schools will face under-enrollment … 1 in 6 K-5 schools with 360+ students; 1 in 7 K-8 schools with 500+ students; 1 in 8 6-8 schools with 500+ students … STRETCHED RESOURCES LEAD TO Staff turnover, Blended classrooms, Fractured staffing, Loss of elective and student supports, Programmatic inequities across schools" | same deck, slide 5; also Sept 1 2026 deck slide 10, https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14357211 |
| c5 | Today: "SCHOOL A 200-350 STUDENTS … THE PINCH OF SHRINKING RESOURCES Blended grade bands; Arts educators split across schools; Libraries open part of the week; Limited electives for grades 6-8; Coaching and intervention reduced; Principal on duty 2-3 hours a day". Hypothetical future: "CAMPUS 1 360-500 STUDENTS SINGLE-GRADE CLASSROOMS K-5 … Single-grade classrooms; Schoolwide arts program; Libraries open more consistently; Coaching and intervention restored; Grade-level peer teams for all educators; Principals on instructional leadership" | same deck, slides 9-10 |
| c6 | Middle grades today: "28 SCHOOL SITES … ~75 SMALLEST SITE ~700 LARGEST SITE … Core subjects in blended classrooms; Elective range varies widely; Not all offer accelerated math; Coaching, intervention, climate reduced; Solo teachers, collaboration is hard; PE, arts and STEM spaces vary" | same deck, slide 11 (the "~7 / 5" text split is read as ~75) |
| c7 | "our definition of sustainable enrollment range is minimum enrollment to offer stable programming. … a minimum of 360 students. At the K-8 and middle school threshold, it's 500 students. And at the high school, the threshold is 1,100. And I do want to say this with this caveat: this is a bridge. … These were numbers that were grounded in our work through SEGC, a lessons learned process, and then also using state resources like quality education model" / "So these are numbers that we've settled on. Again, not ideal state, but it's a bridge." | [PPS] staff, Oct 6 2026 board meeting, https://youtu.be/zOUH2Jq7Owo?t=5842 (transcript checked against captions, `build/pps-texts/meeting-transcripts/findings.md` §3) |
| c8 | "we knew we couldn't get to 100% of sustainable schools. And so we then started asking ourselves: what would it look like to get to 50%? … 60%? … 70%? And that's when these numbers started emerging" | [PPS] staff, Oct 6 2026, https://youtu.be/zOUH2Jq7Owo?t=14893 |
| c9 | "If we maintain the same number of elementaries by the time we reach 2031-32, it means eight elementaries will be at or above the 360 students threshold … This is a very simplified pro way of looking at it." | [PPS] staff, Sept 1 2026, https://youtu.be/5RMfvT-sAPU?t=5612 |
| c10 | "All of our … K-5 buildings have a functional capacity that is 360 or above. … the K-8s are less than the threshold of 500. And then all of our middle schools have functional capacities of at least 500." | [PPS] staff, Sept 8 2026, https://youtu.be/S-pk57P6f_o?t=3849 |
| c11 | "School size goal: More than 360 students for K-5 schools; more than 500 for K-8 or middle schools; more than 1,100 for high schools. These are planning goals, not ratings of school quality." | [PPS] Family Guide glossary, p.2 (every guide; e.g. `build/pps-texts/family-guide-rigler.md`) |
| c12 | "Combining smaller programs can help create larger, more stable schools with more comparable programming and staffing across the city." / "Rightsizing does not change class size expectations. … Bringing together under-enrolled programs can also help schools provide more consistent access to art, physical education, music, library, counseling and other student supports." / "Schools with more stable enrollment may be better able to offer a wider range of classes, programs, activities, and student supports, while creating more stable staffing over time." / "PPS is drawing from national research, state guidance, and lessons learned from districts including Denver, Seattle, and Austin." | [PPS] Rightsizing FAQ, https://www.pps.net/about/portland-public-schools-information/rightsize/frequently-asked-questions (`build/pps-texts/web-frequently-asked-questions.md`) |
| c13 | "PPS will provide comparable, sustainable and rich academic programming at all grade spans" | [PPS] Resolution 7307 (guiding principles), `build/pps-texts/boardbook-reso-7307-…md` |
| c14 | KPI "Percent of Schools Above Threshold" (2025-26 → 2031-32): K5 Title I 18%→9%; K5 not Title I 35%→26%; K8 Title I 50%→50%; K8 not Title I 18%→9%; MS Title I 29%→0%; MS not Title I 50%→25%. Focal students in sustainable K-8 schools: poverty 35.4%→23%; historically underserved race 35.5%→24%; special education 33%→22%; multilingual 43.5%→29% | [PPS] Sept 15 2026 deck, slides 14-15, https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14430171 |

Notes:
- **Thresholds are used as floors, with inconsistent wording.** The memo and deck say "360+", which includes 360. The Family Guides say "More than 360", which excludes it. No school sits exactly on a threshold in the 2025-26 or PSU 2031-32 data, so this does not change any count today.
- **The "1 in 7" K-8 figure is ambiguous.** It matches our data only if focus-option K-8s are counted (see f).
- **No research basis was ever given** in a meeting beyond "SEGC, a lessons learned process, and … quality education model" [`findings.md`, "Not found"].
- **360 is the QEM prototype size, not a staffing-model figure.** It is sometimes described as "from PPS's staffing model"; PPS cites the Quality Education Model prototype (see `targets.md`).

---

## (d) Research on school size: brief and balanced

| Finding | Source |
|---|---|
| "Many researchers, however, indicate that an appropriate and effective size is 300-400 students for an elementary school and 400-800 students for a secondary school." Also: "There is no clear agreement among researchers and educators about what constitutes a 'small' school or a 'large' school." | [RESEARCH] Cotton, K. (1996), *School Size, School Climate, and Student Performance*, NWREL Close-Up #20, summary p.11 (PDF); definition section p.3, quoting Williams (1990). https://educationnorthwest.org/sites/default/files/SizeClimateandPerformance.pdf. **This is the "Education Northwest" synthesis the QEM cites.** |
| "Results suggest that the ideal high school enrolls between 600 and 900 students." The draft adds that students in high schools "over 2,100 students" learn "considerably less", and that size matters more in lower-SES and high-minority schools. | [RESEARCH] Lee, V. E., & Smith, J. B. (1997), *Educational Evaluation and Policy Analysis* 19(3), 205-227; ERIC EJ554778 and ED396888 (abstracts only). Cited by the QEM. |
| "The weight of evidence provided by this research clearly favors smaller schools. … Elementary schools with large proportions of such students should be limited in size to not more than about 300 students; those serving economically and socially heterogeneous or relatively advantaged students should be limited in size to about 500 students. Secondary schools … about 600 students or fewer … about 1,000 students." | [RESEARCH] Leithwood, K., & Jantzi, D. (2009), *Review of Educational Research* 79(1), 464-490, 57 post-1990 studies; ERIC EJ879147 abstract. **These are upper limits, not floors.** |
| "The best of the cost function studies suggest that sizeable potential cost savings … may exist by moving from a very small district (500 or fewer pupils) to a district with ca 2,000 – 4,000 pupils. The findings from production function studies of schools are less consistent, but there is some evidence that moderately sized elementary schools (300–500 students) and high schools (600–900 students) may optimally balance economies of size with the potential negative effects of large schools." | [RESEARCH][2ND-HAND] Andrews, Duncombe & Yinger (2002), *Economics of Education Review* 21(3), 245-262, as quoted by the Vermont Agency of Education, Mar 10 2015 brief, p.1, https://legislature.vermont.gov/Documents/2016/WorkGroups/House%20Education/Reports%20and%20Resources/W~Agency%20of%20Education~Research%20Brief%20on%20Optimal%20School%20District%20Sizes~3-10-2015.pdf. The original article was not read. |
| Oregon: per-student costs rise "rapidly" below about 300 students (high school) and about 100 (elementary). High schools from 500 to 2,400 "cost roughly the same per student". | [STATE] ODE 2002 small-schools study, printed pp.1-2; QEM 2004, printed p.32 (see b5) |
| OECD: school size is "at the heart of school effectiveness and efficiency discussions", but "the literature on this issue is quite fragmented". The review covers consolidation, "alternatives to consolidation when schools are facing declining enrolment", and the evidence on quality and efficiency. | [RESEARCH] Ares Abalde, M. (2014), *School Size Policies: A Literature Review*, OECD Education Working Papers No. 106, doi:10.1787/5jxt472ddkjl-en; abstract via https://ideas.repec.org/p/oec/eduaab/106-en.html. **Abstract only; findings not read** (OECD page returned 403). |
| The SEGC audit's own literature review (pp.141-142): "The research on school size does not support a simple conclusion that smaller schools are always better or that larger schools are always more efficient." Smaller schools give "stronger relationships, greater student visibility"; larger schools give "more staffing flexibility, more program breadth … specialists, electives, and intervention support". Effects on achievement are "mixed, modest, and highly dependent on context" (citing Luyten, Hendriks & Scheerens 2014; Egalite & Kisida 2016; Lee & Loeb 2000). | [AUDIT] `build/pps-texts/segc-equity-audit-evaluation-report.md` pp.141-142 |

**Balanced summary for the page:**
- The research mostly gives *ranges where schools tend to work well*, and often *upper* limits.
- It does not give a size below which a school fails.
- PPS's 360 sits inside the 300-400 elementary range the QEM cites. Its 500 for middle schools sits inside 400-800.
- **The cost evidence is about very small schools.** In the Oregon study, costs climb steeply only below about 100 (elementary) or 300 (high school).
- **The program-breadth argument is the real one PPS makes:** sections per grade, electives, full-time specialists. It is a staffing-arithmetic argument more than a research finding.

---

## (e) SEGC equity audit: verified

Source: *Equity Audit Evaluation of PPS Southeast Enrollment and Program Balancing Initiative*, June 10 2026, main report (`build/pps-texts/segc-equity-audit-evaluation-report.md`), https://drive.google.com/file/d/1gcq_2z1sc6yj90PJCsUc9yqrLfAVWxSz/view (linked from https://www.pps.net/about/portland-public-schools-information/rightsize/segc-documents). Page numbers are the report's own; they match the PDF.

**Verified: 450 / 600 / 650.** Exact text:

- **p.143:** "PPS should consider Oregon's QEM as an adequacy benchmark, but not as a final enrollment target. … the QEM's prototype school structure was developed as a statewide funding model using composite schools, not as a precise enrollment standard for every PPS school. … For this reason, PPS should treat QEM as a minimum adequacy floor rather than a complete contemporary model of what every well-resourced school requires."
- **p.144:**
  - On state funding: "this means PPS should not interpret the QEM prototype numbers as sufficient by themselves."
  - On attrition: "For elementary schools specifically, the median annualized loss among net declining schools was approximately 16.5 students per year, or about 82.5 students over five years. … an elementary attrition buffer of approximately 85 students … For middle schools … approximately 15.25 students per year, or about 76 students over five years … approximately 75 to 80 students … PPS may want to stress test the middle school number closer to 100 students over five years."
  - The floor itself: "Using this logic that we stated above, PPS might consider 450 students as a practical elementary planning floor."
- **p.145:**
  - "In other words, 450 is not the ideal school size target but rather a PPS planning floor that adds a five-year attrition buffer to the QEM adequacy benchmark."
  - "Similarly, for middle schools, PPS should consider 600 students as a practical planning floor."
  - "For K–8 schools, because QEM does not provide a separate K–8 prototype, PPS should consider a local planning estimate of approximately 650 students."
  - "we cannot state enough that these numbers should not be used as automatic closure thresholds. They should be used as planning ranges…"
- **p.146:** "Schools below these ranges may still be necessary, valued, and educationally strong, but they may require additional district investment, a specialized program model, or an explicit equity rationale."
- **Figure 6.1, "Deriving Planning Floors for Well Resourced Schools" (p.146):**

  | School type | QEM prototype | Buffer | Planning floor |
  |---|---|---|---|
  | Elementary | 360 | + about 85 | Approximately 450+ |
  | Middle | 500 | + about 100 | Approximately 600+ |
  | K–8 | no QEM prototype | local estimate | Approximately 650+ |

  Figure note: "Figures are preliminary planning estimates, to be refined once PPS defines its well-resourced school model."

Also noted:
- **p.141:** "these numbers should not be understood as automatic closure thresholds."
- **p.136:** "adequacy models should not be confused with practical planning floors under current funding conditions and realities. Oregon has not consistently funded schools at the level its own adequacy model identifies as necessary."

**How PPS responded.** The Aug 4 memo that reports the audit keeps 360/500 and applies 500 to K-8s. That is 150 below the audit's K-8 figure. PPS then uses the numbers as the "Schools above threshold" closure-planning KPI, which the audit said not to do. *(This is our reading of the documents; PPS has not said it rejected the audit numbers.)*

---

## (f) Data available for charts

### Files and fields (all local, clean enough to chart)

**`build/data/schools.csv`**: 83 rows.
- Neighborhood schools: 44 K-5, 14 middle (6-8), 9 K-8, 8 high (9-12). Focus or alternative schools: 8, flagged `focus_option=1`.
- Fields:
  - `name`, `level`
  - `enr_total`, `enr_k5`, `enr_68`, `enr_912`: **ODE Fall Membership 2025-26, Oct 1 2025** (sheet "School 20252026", Portland SD 1J, via the PPS Data Explorer's pps-data repository)
  - `enr_gK`…`enr_g12`
  - `forecast_2031_32_prc`: **PSU Population Research Center forecast for 2031-32**, the "Total" row of Table 5.5, https://resources.finalsite.net/images/v1785171463/ppsnet/ejdr22voeddvux8qwlob/PPS_Forecast_2026_27.pdf
  - `pps_proj_2031_32_no_change` / `_A` / `_B`: PPS Family Guide projections. They equal the PSU figure for every school except Bridlemile (PSU 408 vs PPS 413).
  - `capacity_functional_2021` (LRFP 2021), `lat`, `lon`
- For K-5 schools `enr_total = enr_k5` in every row, so whole-school counts include co-located DLI strands. PPS's threshold counts appear to use whole-school totals too.

**`build/data/v2/psu_table5_5_by_year.csv`**: the PSU Table 5.5 time series.
- Columns `y2023`…`y2035` are fall of that year, so `y2025` = 2025-26 and `y2031` = 2031-32. Check: Abernethy y2025 = 269 = ODE.
- Rows by school and program (`type` ES/MS/K8/HS, `program` Total/Neighborhood/Spanish/…).
- Use the `Total` rows: 45 ES, 15 MS, 11 K8, 9 HS, plus K12 and G28. Names are squashed ("MtTabor", "IdaBWells-Barnett").
- Good for a per-school line or slope chart, 2023-24 to 2035-36.

**`build/data/scenarios.json`** → `pps_projections_2027_28_to_2031_32`: per school `{no_change:[5 values], A:[…]|"closes", B:[…]|"closes"}` for 2027-28…2031-32 (index 4 = 2031-32), from the 82 Family Guides. Its `thresholds` key = `{k5:360, k8_and_middle:500, high:1100, space_use_goal:"70-100% of building capacity"}`.

**`build/data/v2/capacity_2025_26.csv`**: `capacity_2025_26` (PPS School Profiles "Functional Capacity", captured second-hand by pps-dli-explorer on 2026-10-09) and `capacity_lrfp_2021`. Uses "Lane"/"Sunrise" names, not "Lane (Brentwood)"/"Lee (Sunrise)".
- Check of PPS's Sept 8 claim: every K-5 (44/44) and middle school (14/14) has a 2025-26 functional capacity at or above its threshold.
- K-8s below 500: **Skyline 285**, **Sunnyside 492**.
- So in every K-5 and middle building, size is limited by enrollment, not by the building.

### Exact counts: neighborhood schools vs PPS thresholds (strictly below = "below")

| Level (threshold) | Schools | 2025-26 below (ODE) | 2025-26 at/above | 2031-32 no change below (PSU) | 2031-32 at/above |
|---|---|---|---|---|---|
| K-5 (360) | 44 | **33** | 11 | **37** | 7 |
| Middle 6-8 (500) | 14 | **8** | 6 | **12** | 2 |
| K-8 (500) | 9 | **6** | 3 | **7** | 2 |
| High 9-12 (1,100) | 8 | **1** (Jefferson 390) | 7 | **0** | 8 |

The same schools against the **SEGC floors** (450 / 600 / 650):

| Level | Below in 2025-26 | Below in 2031-32 |
|---|---|---|
| K-5 | 41 of 44 | 41 of 44 |
| Middle | 12 of 14 | 13 of 14 |
| K-8 | 9 of 9 | 9 of 9 |

Students in schools at or above PPS's threshold:

| Level | 2025-26 | 2031-32 |
|---|---|---|
| K-5 | 4,629 of 13,848 (33%) | 3,074 of 13,259 (23%) |
| Middle | 3,572 of 6,939 (51%) | 1,135 of 5,942 (19%) |
| K-8 | 1,753 of 4,215 (42%) | 1,127 of 3,846 (29%) |

Median school size:

| Level | 2025-26 | 2031-32 |
|---|---|---|
| K-5 | 295 | 296 |
| Middle | 460 | 417 |
| K-8 | 480 | 418 |

**Cross-checks against PPS's own figures:**
- K-5 2031-32: 7 of 44 = 16%, which matches PPS's "1 in 6".
- Middle 2031-32: 2 of 14 (2 of 15 with da Vinci = 13%), which matches "1 in 8" and the Aug 4 deck's "13%".
- K-8 "1 in 7" (14%) does *not* match the 9 neighborhood K-8s (2 of 9 = 22%). It matches if the focus K-8s (Winterhaven, Odyssey, ACCESS, MLC) are added: 2 of 13 = 15%. **Flag this.**
- The memo's "47% of middle schools falling 100 students or more below" matches 7 of 15 (with da Vinci) under 400 in 2031-32. Its "69% of K8" was **not reproduced**: 3 of 9 neighborhood K-8s, or 7 of 13 with focus, are under 400.

**Focus and alternative schools, not in the counts above** (2025-26 → 2031-32):

| School | Level | 2025-26 | 2031-32 |
|---|---|---|---|
| Richmond | K-5 DLI | 512 | 497 |
| Winterhaven | K-8 | 316 | 310 |
| Odyssey | K-8 | 217 | 224 |
| da Vinci | 6-8 | 429 | 419 |
| ACCESS | 1-8 | 324 | 275 |
| MLC | K-12 | 275 | 199 |
| Benson | 9-12 | 1,024 | 1,213 |
| Alliance | 9-12 | 215 | n/a |

**Sorted values, for a strip or dot chart:**
- **K-5 2025-26:**
  - Under 300: Rosa Parks 160, Whitman 193, Creston 219, Woodmere 226, Arleta 230, Peninsula 239, Chief Joseph 247, Lee/Sunrise 251, Lent 256, Irvington 259, Lewis 262, Forest Park 264, Rieke 266, Abernethy 269, Sabin 270, Stephenson 281, Buckman 283, Vestal 286, Beach 288, Maplewood 288, Hayhurst 290, Rigler 291, Boise-Eliot/Humboldt 295
  - 300-359: Marysville 304, MLK Jr 319, Woodlawn 323, Grout 327, Capitol Hill 329, Chapman 333, Markham 339, Glencoe 341, Llewellyn 345, Sitton 346
  - 360 and over: Duniway 362, Clark 363, James John 364, Atkinson 366, Woodstock 366, Kelly 411, Rose City Park 417, Bridlemile 423, Scott 477, Alameda 515, Ainsworth 565
- **K-5 2031-32 (PSU):**
  - Under 300: Rosa Parks 168 … Glencoe 296
  - 300-359: 13 schools, Boise-Eliot/Humboldt 308 … James John 352
  - 360 and over (7): Rose City Park 370, Atkinson 386, Kelly 391, Bridlemile 408, Scott 470, Alameda 492, Ainsworth 557
- **Middle schools:**

  | School | 2025-26 | 2031-32 |
  |---|---|---|
  | Beaumont | 416 | 418 |
  | George | 356 | 390 |
  | Gray | 432 | 368 |
  | Tubman | 403 | 374 |
  | Harrison Park | 420 | 417 |
  | Hosford | 528 | 374 |
  | Jackson | 688 | 515 |
  | Kellogg | 533 | 471 |
  | Lane/Brentwood | 450 | 357 |
  | Mt Tabor | 430 | 354 |
  | Ockley Green | 460 | 436 |
  | Roseway Heights | 572 | 498 |
  | Sellwood | 566 | 350 |
  | West Sylvan | 685 | 620 |

- **K-8s:**

  | School | 2025-26 | 2031-32 |
  |---|---|---|
  | Astor | 401 | 418 |
  | Beverly Cleary | 480 | 389 |
  | Bridger | 446 | 415 |
  | César Chávez | 443 | 392 |
  | Faubion | 600 | 602 |
  | Laurelhurst | 614 | 525 |
  | Skyline | 207 | 177 |
  | Sunnyside | 485 | 475 |
  | Vernon | 539 | 453 |

- **High schools:**

  | School | 2025-26 | 2031-32 |
  |---|---|---|
  | Cleveland | 1,451 | 1,318 |
  | Franklin | 1,777 | 1,492 |
  | Grant | 2,074 | 1,487 |
  | Ida B. Wells | 1,574 | 1,457 |
  | Jefferson | 390 | 1,183 |
  | Lincoln | 1,648 | 1,411 |
  | McDaniel | 1,626 | 1,261 |
  | Roosevelt | 1,418 | 1,117 |

  Jefferson rises after the dual-assignment sunset.

Data caveats:
- **Different source years.** 2025-26 is ODE membership on Oct 1 2025. 2031-32 is a PSU projection.
- **The "no change" projections already decline.** PPS's per-school model (Family Guides) differs from PSU for one school only.
- **K-8 6-8 counts are small.** The 2025-26 middle-grade counts in K-8s range from 68 (Skyline) to 235 (Laurelhurst). This matters for the audit's per-grade argument.

---

## (g) Proposed page outline: "Why these sizes"

Design system (from (a)):
- Light panels.
- Per-level small multiples with tabs (K-5 / Middle / K-8 / High).
- A blue threshold rule over a soft band, with an inline label.
- Dots red below and green at or above, with hover tooltips.
- A one-line count caption under each panel.
- A "Show as a table" disclosure under every chart.
- Put the SEGC floors on the same axis as a dashed, lighter second rule.

### 1. "Where 360, 500 and 1,100 come from"
- **Chart:** a three-row "lineage" graphic, one row per level. Each row shows the state prototype (360 / 500 / 1,000), PPS's threshold (360 / 500 / 1,100), the audit's suggested floor (450 / 600 / 650 for K-8) and the research ranges as a horizontal band. Elementary: Cotton 300-400; Leithwood-Jantzi upper limits 300-500. Secondary: Cotton 400-800; Lee & Smith 600-900 for HS.
- **Data:** the constants in (b), (d) and (e).
- **Links:**
  - QEM 2026 report, PDF p.93 / printed p.91
  - QEM reports page
  - LPRO issue brief
  - ORS 327.077
  - Aug 4 memo
- **Caveats:**
  - K-8 has no QEM prototype; PPS reused 500.
  - The HS 1,100 came from PPS's Jefferson work, not from the state.
  - The QEM elementary prototype was 340 until at least 2018; the reason for 360 is not given.

### 2. "What the state model actually is"
- **Chart:** no chart. Show the 2026 prototype box as a three-column card set (360 / 500 / 1,000 with class-size averages 20 / 17.7 / 20.7 and staffing bullets). Add a callout quoting "composites representing an average school for its category" and "not required to adhere".
- **Data:** b1, b2.
- **Caveats:**
  - The prototypes price an *adequate* education at *efficiently-scaled* schools. They are not minimums.
  - The state's own reports (2024) and the AIR evaluation (2025) call them dated: "decades-old research estimates".
  - Oregon has not funded the QEM fully, which is the audit's argument for going *higher*.

### 3. "How many schools fall below today, and in 2031-32" (the headline chart, rightsizepdx-style)
- **Chart:** a per-level dot strip (beeswarm) of every neighborhood school's enrollment.
  - x = students. Threshold rule at 360/500/1,100; dashed audit rule at 450/600/650.
  - Toggle 2025-26 (ODE) ↔ 2031-32 (PSU, no change).
  - Optional slope or connector lines between the two years.
  - Caption counts: "33 of 44 K-5 schools are below 360 today; 37 in 2031-32."
- **Data:** `schools.csv` `enr_total` and `forecast_2031_32_prc`, `level`, `focus_option`; counts in (f).
- **Caveats:**
  - These are PSU projections with no changes.
  - Focus schools are excluded (list them separately).
  - "360+" vs "more than 360" wording.
  - PPS's K-8 "1 in 7" only matches if focus K-8s are counted.
  - PPS's "69% of K8" figure was not reproduced.

### 4. "Why size matters to PPS: sections per grade"
- **Chart:** a staffing-arithmetic bar or waffle. For a given enrollment, show students per grade and the implied homerooms per grade at 20 / 25 per class.
  - K-5: 360 ÷ 6 = 60 per grade = 3 classes of 20 or about 2.4 of 25.
  - Middle: 500 ÷ 3 ≈ 167 per grade ≈ 6-8 sections.
  - Overlay PPS's slide-7 promises ("2-3 sections per grade" K-5; "6-8 sections per grade" 6-8) and the audit's arithmetic (450 → 75 per grade; 600 → 200 per grade; 650 K-8 → 72 per grade).
- **Data:** constants from c3, b1, e. Optional: per-school students per grade from `enr_gK…enr_g8`.
- **Caveats:**
  - This is arithmetic, not evidence of outcomes.
  - PPS has not published the staffing formula that links enrollment to specialists. rightsizepdx's formula curve is a third-party reconstruction [3P].
  - Class-size caps come from the PPS–PAT contract and are not in this research.

### 5. "What the research says, and doesn't"
- **Chart:** a range chart. For each level, horizontal bars for each research range: Cotton ES 300-400 / secondary 400-800; Lee & Smith HS 600-900; Leithwood & Jantzi upper limits ES 300 (disadvantaged) / 500, secondary 600 / 1,000; Andrews et al. ES 300-500, HS 600-900 [2ND-HAND]. Overlay PPS's thresholds as vertical rules.
- **Data:** (d).
- **Caveats:**
  - Most ranges are "works well" or "no larger than", not floors.
  - Effects are modest and depend on context.
  - Smaller schools tend to help low-income students.
  - The cost evidence is about very small schools (Oregon 2002: steep only below about 100 ES / 300 HS).
  - The OECD review was read as an abstract only.

### 6. "Floors or goals? What PPS's own auditor said"
- **Chart:** reuse chart 3 with three positions on a toggle (QEM/PPS floor, audit floor, no floor), showing how the count of "below" schools jumps: K-5 33 → 41 of 44 today; middle 8 → 12 of 14; K-8 6 → 9 of 9.
- **Data:** (f) counts; audit quotes pp.143-146.
- **Caveats:**
  - The audit's higher floors are "preliminary planning estimates", built for a district still shrinking.
  - The audit says explicitly "not … automatic closure thresholds" and that schools below the floors "may still be necessary, valued, and educationally strong".
  - PPS's own Family Guides call the numbers "planning goals, not ratings of school quality".
  - Staff on Oct 6: "not ideal state, but it's a bridge".

### Footer: the Oregon guidance to link
- QEM reports page: https://www.oregon.gov/ode/reports-and-data/taskcomm/Pages/QEMReports.aspx
- QEM 2026 report: https://www.oregon.gov/ode/reports-and-data/taskcomm/Documents/Quality%20Education%20Commission%20QEM%20Report%202026.pdf
- QEM 2024 report: https://www.oregon.gov/ode/reports-and-data/taskcomm/Documents/M000266%20DOE%20Quality%20Education%20Model%20Report%202024.pdf
- LPRO QEM issue brief (Dec 2023): https://www.oregonlegislature.gov/lpro/Publications/Oregon%20Quality%20Education%20Model%20-%20Issue%20Brief%20Dec.%202023.pdf
- LPRO summary of the AIR evaluation (Oct 2025): https://olis.oregonlegislature.gov/liz/2025I1/Downloads/CommitteeMeetingDocument/310513
- QEC slides naming the prototypes (2023): https://apps.oregonlegislature.gov/liz/2023R1/Downloads/CommitteeMeetingDocument/274502
- ORS 327.077 (small-school funding): https://www.oregonlegislature.gov/bills_laws/ors/ors327.html
- ODE, *The Costs of Operating Small Schools in Oregon* (2002): https://www.oregon.gov/ode/reports-and-data/taskcomm/Documents/SFTF/2014.01.SFTFCostOfOperatingSmallSchoolsInOregon.pdf

Per the kit's PPS rules, the page should also carry the AI-disclosure top link and footer note, and cite every figure.

### Open items
- Confirm with Paul which "graph view" he meant: rightsizepdx's threshold chart or ppsdata's cost-vs-size scatter with its table toggle.
- AIR's full Task 3 report (https://www.air.org/project/evaluation-oregons-quality-education-model) was not read. The prototype critique is quoted via LPRO.
- Andrews, Duncombe & Yinger (2002) and the OECD paper were not read in full.
- Why the QEM elementary prototype moved from 340 to 360 (between the 2018 and 2022 reports) is not explained in any report read.
