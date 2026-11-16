# PPS rightsizing: policy targets and scenario facts (research, Phase 1c)

Compiled 2026-10-11. Machine-readable twin: `targets.json`. Source extracts (text pulled from the PDFs, so quotes can be re-checked offline) are in `sources/`.

How to read this. **[PPS]** means a primary PPS document (board deck, memo, resolution, scenario PDF, map, guideline, or the PSU forecast PPS publishes). **[STATE]** means Oregon statute or rule. **[3P]** means third-party (news, ppsdata.info/PPS Data Explorer). **[DEFAULT]** means no source was found and this is a proposed, clearly labeled assumption.

A key fact runs through everything below: **PPS evaluates every threshold on 2031-32 projected enrollment, not today's.** The scenario PDFs say, "All figures are projections for the 2031–32 school year unless noted." [PPS, scenarios overview, Oct 4 2026]. The solver should size schools against the PSU 2031-32 forecast, then check today's numbers too.

---

## 1. Size targets by level

### The one official table

Every scenario PDF prints the same "Sustainability thresholds" strip:

> "SUSTAINABILITY THRESHOLDS · K–5: 360 students · K–8 and middle school: 500 students · High school: 1,100 students"
> Source: [PPS] Scenario comparison PDF, https://drive.google.com/file/d/1ueJVC-Jo6MRKw56Jedihc6YbVdBlSB2z/view (linked from https://www.pps.net/about/portland-public-schools-information/rightsize/scenarios), and the four regional PDFs.

PPS states where the numbers come from:

> "We used the threshold of 360 students for elementaries and 500 students for middle schools as guided by the prototype school description in the Quality Education Model. We applied the same number for K-8s and used the 1100 students threshold we developed during the sunsetting of Jefferson dual assignment process."
> Source: [PPS] Board memo, "Rightsizing Update: Equity Audit Evaluation," Aug 4 2026, https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997426

**Where the 360 comes from:** the state's **Quality Education Model prototype school**, not a PPS staffing model. The QEM prototypes are "Elementary (360 students), Middle (500 students), and High (1,000 students)" [STATE, Oregon Legislature committee document, https://apps.oregonlegislature.gov/liz/2023R1/Downloads/CommitteeMeetingDocument/274502]. PPS kept 360 and 500 but raised the high school figure to 1,100.

These are **floors** ("schools above the sustainability threshold"). PPS publishes **no upper bound** at any level. The only ceiling in PPS's own framework is building **functional capacity** (see 1.3).

### 1.1 K-5

| Item | Value | Source |
|---|---|---|
| Floor | **360** | [PPS] threshold strip; Aug 4 memo (QEM prototype) |
| Upper bound | **None stated by PPS.** | Searched the scenario PDFs, Sept 1/15 decks, Res. 7307, and the FAQ |
| Building ceiling | Functional capacity at a 100% utilization rate (K-5 and K-8) | [PPS] LRFP 2021 (see 1.3) |
| Range KPI | Tracked but with no target: "Range of enrollment (largest - smallest) by grade level". K5 = "560 -160 =400" actual 2025-26, "557 -168 = 389" projected 2031-32 | [PPS] Sept 15 2026 deck, slide 16, https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14430171 |
| **Solver** | min 360; max = min(functional capacity, **600** [DEFAULT, carried from our earlier model]) | — |

Today's largest K-5 is 560 (Ainsworth), so 600 doesn't bind on any real school. Keep it as a sanity cap.

### 1.2 K-8 (what remains)

- Threshold: **500**, the same as middle school. PPS: "We applied the same number for K-8s" [PPS, Aug 4 memo].
- Both scenarios convert **seven K-8s to K-5**: Beverly Cleary, Laurelhurst, Sunnyside, Bridger Creative Science, César Chávez, Faubion and Vernon. The grade-level changes in the PDFs read: "Beverly Cleary 6–8 to Beaumont MS · Laurelhurst 6–8 to Mt. Tabor MS · Bridger Creative Science 6–8 to Harrison Park MS · Sunnyside Environmental 6–8 to Hosford MS · Faubion 6–8 to Ockley Green MS · Vernon 6–8 to Harriet Tubman MS · Chavez 6-8 to George · MLC becomes K-8" [PPS, scenarios overview]. OPB: "turning seven K-8 schools into K-5 schools... Several current K-8s are not listed as changing, including Astor, Skyline and Winterhaven." [3P, OPB Oct 6 2026, https://www.opb.org/article/2026/10/05/portland-public-schools-closures-rightsizing/]
- K-8s left after A or B, labeled as on the Scenario A 6-8 map: **Astor K-8 Neighborhood**, **Skyline K-8 Neighborhood**, **Winterhaven K-8 Focus/Option**, **MLC & Odyssey K-8 Focus/Option** (MLC site), plus **ACCESS 2-8 Focus/Option** [PPS, "Grade 6-8 Attendance Areas, School Year 2027-28, Scenario A", ArcGIS export dated 10/5/2026, `PPS BoardBook PDF "Scenario A - Attendance Boundaries 6-8.pdf"`].
- PSU 2031-32 forecast: Astor 418, Skyline 177, Winterhaven 310 [PPS/PSU forecast, Table 5.5, https://resources.finalsite.net/images/v1785171463/ppsnet/ejdr22voeddvux8qwlob/PPS_Forecast_2026_27.pdf]. **All of them sit below 500, and PPS leaves them alone.** A district-like run must exempt Astor and Skyline from the 500 floor, or the model has no feasible solution.

### 1.3 6-8 (middle)

| Item | Value | Source |
|---|---|---|
| Floor | **500** | [PPS] threshold strip; Aug 4 memo |
| Status quo 2031-32 | "6-8 Schools with 500 + Students: 1 in 8"; only 13% of 6-8 schools at 500+, with 7 of 15 below 400 | [PPS] Sept 1 2026 deck, slide 10, https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=14357211; Aug 4 deck, slide 17 |
| Magnitude slide | "6-8 with Enrollment 500+ in 2031-32": 15 schools → 2 at 500+; 14 schools (1 closure) → 3; 13 (2 closures) → 4; 12 (3 closures) → 8 | [PPS] Sept 1 deck, slide 12 |
| Utilization definition | "a school's enrollment divided by its functional capacity" | [3P] Willamette Week (the reporter's description, not a PPS quote), Apr 15 2026, https://www.wweek.com/news/schools/2026/04/15/pps-introduces-another-metric-to-inform-school-closures/ |
| Functional capacity method | Classrooms 500–800 sq ft = 24 students, 800–1000 = 27, >1000 = 30 → gross capacity; minus set-asides (learning center, SPED focus room, 1-2 art/music rooms, early childhood, leased rooms); × utilization rate. "the utilization rate for these configurations [K-5, K-8] is one-hundred percent." For middle and high school, "the utilization rate for these configurations is 85%." Rates are "broadly reduced for Title I schools (five-percent) and for TSI/ CSI designations (again, five-percent)." FUNCTIONAL CAPACITY ⁄ ENROLLMENT = SCHOOL UTILIZATION (sic: the arithmetic is enrollment ÷ capacity) | [PPS] Long-Range Facility Plan 2021, Vol 1, pp. 50-51, https://www.pps.net/fs/resource-manager/view/84245cbd-4298-4803-8ba9-d26fb13a9c7a |
| "Efficiently utilized" | Named as a KPI: "1. Percent of efficiently utilized schools" (Sept 15 deck, slide 17). Defined by PPS staff the same evening as 70–100% of functional capacity (see next row). | [PPS] Sept 15 deck, slide 17; Sept 15 2026 meeting video |
| Utilization band 70–100% | **A stated PPS aim** (corrected 2026-10-12; an earlier version of this file said no PPS source existed). [PPS] Family Guide glossary, p. 2, "Space use goal": "The district aims to use 70%-100% of a school's available room for students. A 'No' can mean the school is below or above that range." (every guide, e.g. `build/pps-texts/family-guide-rigler.md` lines 82-84); PPS staff, Sept 15 2026 board meeting, https://youtu.be/uAf7l-ChjFo?t=15369 (04:16:09): "we look anywhere from 70 to 100% being efficiently utilized" (checked against the video). PPS gives no research basis for the band; none was found in its board records. WW: "higher utilization rates aren't ideal because they indicate that all instructional spaces are occupied to capacity all day." | [PPS]; [3P] WW Apr 15 2026 |
| **Solver** | min 500 students; utilization ≤ 100% of functional capacity (hard); utilization ≥ 70%: **PPS aim** (Family Guide p. 2 "Space use goal"; Sept 15 2026 meeting); reported, not a hard constraint | [PPS] |

Because the 85% rate is already built into functional capacity, 100% of functional capacity is a real operating ceiling, not a theoretical one. The model keeps the 70% floor as a reported metric; it would become a rule only if the 500 floor doesn't already cover it. For a 700-seat building, 500 students is 71%, so the two floors nearly coincide.

**Middle-school functional capacities, LRFP 2021 [PPS]:** Mt. Tabor 682 · Kellogg 803 · Hosford 696 · Jackson 908 · Sellwood 683 · Roseway Heights 803 · West Sylvan 987 · Ockley Green 689 · Gray 622 · Beaumont 701 · da Vinci 714 · Tubman 732 · George 617 · Lane (now Brentwood) 770. Harrison Park was a K-8 in 2021 and has no MS row. [3P] PPS Data Explorer lists 1006 (2021) and 890 (2025 PPS utilization-model value). PPS's 2025 utilization-model workbook came out through a records request (ppsdata.info, [3P]). Its values differ slightly (Kellogg 732, Jackson 931), so Phase 1a should pick one source and say which.

**Middle-school 2031-32 status-quo forecast [PPS/PSU Table 5.5]:** Beaumont 418 · George 390 · Gray 368 · Tubman 374 · Harrison Park 417 · Hosford 374 · Jackson 515 · Kellogg 471 · Lane/Brentwood 357 · Mt. Tabor 354 · Ockley Green 436 · Roseway Heights 498 · Sellwood 350 · West Sylvan 620 · da Vinci 419. The "Middle Schools Subtotal" of 6,361 includes da Vinci.

**Back-of-envelope feasibility (ours):** 5,942 neighborhood MS students in 2031-32, plus about 1/3 of the 3,251 K-8 students in the seven converting K-8s (≈1,080), comes to ≈7,020 sixth-to-eighth graders for the 13 neighborhood middle schools left after A. That averages ≈540, just over 13 × 500 = 6,500. **The 500 floor is feasible on average but tight**, and 13 schools must all clear it. Close 2 focus options adds da Vinci's 419 and Winterhaven's ≈100 sixth-to-eighth graders, which lifts the average to ≈580.

### 1.4 9-12 (comprehensive high schools)

| Item | Value | Source |
|---|---|---|
| Floor | **1,100** | [PPS] threshold strip |
| Why 1,100 | Set in the Jefferson dual-assignment sunset work ("the 1100 students threshold we developed during the sunsetting of Jefferson dual assignment process") | [PPS] Aug 4 memo |
| Rationale quote | "ensuring that the student body of each high school stays above 1,100 by 2030–31, which district officials say is necessary to justify comprehensive programming." | [3P] WW Dec 10 2025, https://www.wweek.com/news/schools/2025/12/10/enrollment-balancing-in-north-and-northeast-portland-shows-the-consequences-of-overbuilding-high-school-capacity/ |
| HS KPIs from "Jefferson is Rising" | "% of High Schools in each scenario with enroll above 1100 students (target = 100%)"; "HS Enrollment Range (target = <350)"; "% MS feeders moving to the same HS (target = 100%)" | [PPS] Sept 15 2026 deck, slide 21 (image saved as `sources/jefferson_is_rising_kpis_slide21.png`) |
| Capacities on that slide | Jefferson 1590 (current) → 1773 (modernized), Grant 1935, McDaniel 1735, Roosevelt 1404 | same slide |
| LRFP 2021 HS functional capacities | Grant 1,686 · Franklin 1,744 · Roosevelt 1,320 · Wells-Barnett 1,872 · Cleveland 1,859 · Lincoln 1,867 · McDaniel 1,739 · Benson 2,203 · Jefferson 1,817 | [PPS] LRFP 2021, p. 122 |
| Status quo | "9-12 Schools with 1100 or more students": 100% by 2031-32. Range 1,683 (2025-26) → 375 (2031-32) | [PPS] Aug 4 deck, slide 17; Sept 15 deck, slide 16: "High Schools 2074 -391 =1683 / 1492 -1117 =375" |
| 2031-32 forecast | Cleveland 1,318 · Franklin 1,492 · Grant 1,487 · Ida B. Wells 1,457 · Jefferson 1,183 · McDaniel 1,261 · Lincoln 1,411 · Roosevelt 1,117 · (Benson 1,213, a focus school) | [PPS/PSU] Table 5.5 |
| Upper bound | **None stated.** Building capacity is the ceiling. The <350 range KPI acts as an implicit cap: max ≤ min + 350. | — |
| **Solver** | min 1,100 (hard); ≤ functional capacity (hard; use the slide's 2025 figures where given, LRFP otherwise); range ≤ 350 **soft** (status quo is already 375 in 2031-32, so a hard limit risks infeasibility) | — |

The Jefferson dual-assignment sunset is already decided (board vote Jan 2026, effective with 9th graders in 2027-28). PPS treats it as **current state** in its feeder chart: "Reflects the sunsetting of dual assignment, effective 2027-28 school year" [PPS, High School Feeder Patterns PDF, https://resources.finalsite.net/images/v1790894228/ppsnet/f2u6fbkysoabacyo484j/PPS_High_School_Feeder_Patterns_Eng.pdf]. Irvington-area students go to Grant; Peninsula and Beach Spanish DLI go to Roosevelt.

---

## 2. Dual Language Immersion (DLI)

### 2.1 What PPS says about strand size

**No PPS minimum strand size (classes per grade or students per grade) was found.** We searched the DLI department page, the scenario PDFs, the board decks (Mar 10, Mar 31, Sept 1, Sept 15), the June 2026 focus/alternative overview, the FAQ, and the SEGC equity audit (157 + 130 pp.). What PPS does say:

- "We look at specialized programs as full learning experiences from PK-12, not just single classrooms." [PPS FAQ, Sept 15 2026, https://www.pps.net/about/portland-public-schools-information/rightsize/frequently-asked-questions]
- KATU's summary of the scenario release: DLI programs "would be consolidated to provide more consistent pathways across grade levels" and "no DLI program would be eliminated." [3P, KATU, https://katu.com/news/local/portland-public-schools-proposes-closing-up-to-14-schools-amid-declining-enrollment]
- SEGC precedent: Kellogg consolidation was praised because the prior setup had "only 'one section per grade' and limited collaboration among DLI teachers" [PPS-commissioned equity audit, school-by-school volume, https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997428]. Families saw Atkinson's retained strand "as inconsistent with the district's stated rationale that immersion strands should be consolidated" [same audit, main report].

**What Scenario A actually does is a clear structural rule.** Every language ends with **exactly one elementary host and one middle-school host per high-school pathway**:

| Language / HS pathway | Today: K-5 hosts → 6-8 host(s) | Scenario A | Scenario B |
|---|---|---|---|
| Spanish / Lincoln | Ainsworth → West Sylvan | unchanged | unchanged |
| Spanish / Roosevelt | Beach, James John, Sitton, Chávez K-8 → Ockley Green, George, Chávez | **Chávez (K-5)** → **George** | same as A |
| Spanish / McDaniel | Rigler, Scott → Beaumont, Roseway Heights | **Rigler** → **Roseway Heights** | same as A |
| Spanish / Franklin | Atkinson, Lent → Kellogg | **Lent** → Kellogg | same as A |
| Mandarin / Jefferson | MLK Jr. → Tubman | **Boise-Eliot/Humboldt** → Tubman | same as A |
| Mandarin / Cleveland | Woodstock, Clark → Harrison Park | **Woodstock** → Harrison Park | same as A |
| Japanese / Grant | Richmond → Mt. Tabor | unchanged | unchanged |
| Russian / Franklin | Kelly → Lane (Brentwood) | unchanged | unchanged |
| Vietnamese / McDaniel | Rose City Park → Roseway Heights | **Vestal** → Roseway Heights | **stays at Rose City Park** |

Sources: today's pathways come from [PPS] High School Feeder Patterns PDF p. 9 and the TLE "Alternative & Focus School Overview" (June 2026, slides 7-9, https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997345). Program moves are quoted from [PPS] scenario PDFs: "Spanish: Beach, James John, and Sitton to Cesar Chavez · Atkinson to Lent · Scott to Rigler · Beaumont MS to Roseway Heights MS · Chavez 6–8 and Ockley Green MS to George MS · Vietnamese: Rose City Park to Vestal · Mandarin: Clark to Woodstock · MLK Jr. to Boise-Eliot/Humboldt". B drops the Vietnamese move. Roseway Heights hosting Spanish plus Vietnamese and Tubman hosting Mandarin also show on the A 6-8 map labels ("Roseway Heights Middle School Spanish Immersion, Vietnamese Immersion"; "Harriet Tubman Middle School Mandarin Immersion"; "George Middle School Spanish Immersion"; "Kellogg Middle School Spanish Immersion"; "Mt Tabor Middle School Japanese Immersion"; "Brentwood Middle School Russian Immersion"; "Harrison Park Middle School Mandarin Immersion"; "West Sylvan Middle School Spanish Immersion").

Spanish high-school assignment is regional by home address: "Upon completion of 8th grade Spanish DLI, students are assigned to a regional high school based on their home address." [PPS feeder PDF p. 9]. Lincoln+Wells → Lincoln; Roosevelt+Jefferson → Roosevelt; McDaniel+Grant → McDaniel; Franklin+Cleveland → Franklin.

### 2.2 Current strand sizes (PSU forecast, by program) [PPS/PSU Table 5.5]

Per-grade = program enrollment ÷ grades (6 for K-5, 3 for 6-8, 9 for Chávez K-8).

| Host | Lang | 2025-26 | /grade | 2031-32 | /grade | A/B fate |
|---|---|---|---|---|---|---|
| Ainsworth ES | Spa | 287 | 47.8 | 291 | 48.5 | stays |
| Rigler ES (whole-school) | Spa | 289 | 48.2 | 321 | 53.5 | receives Scott |
| Lent ES (whole-school) | Spa | 256 | 42.7 | 274 | 45.7 | receives Atkinson |
| Scott ES | Spa | 222 | 37.0 | 223 | 37.2 | → Rigler |
| Atkinson ES | Spa | 178 | 29.7 | 183 | 30.5 | → Lent |
| Beach ES | Spa | 155 | 25.8 | 127 | 21.2 | closes → Chávez |
| Sitton ES | Spa | 138 | 23.0 | 113 | 18.8 | → Chávez |
| James John ES | Spa | 133 | 22.2 | 136 | 22.7 | closes → Chávez |
| César Chávez K-8 | Spa | 300 | 33.3 | 295 | 32.8 | becomes K-5 host; 6-8 → George |
| MLK Jr. ES | Man | 193 | 32.2 | 196 | 32.7 | → Boise-Eliot/Humboldt |
| Woodstock ES | Man | 190 | 31.7 | 194 | 32.3 | receives Clark |
| Clark ES | Man | 91 | 15.2 | 87 | 14.5 | → Woodstock |
| Richmond ES (whole-school) | Jpn | 512 | 85.3 | 497 | 82.8 | stays |
| Kelly ES | Rus | 143 | 23.8 | 145 | 24.2 | stays |
| Rose City Park ES | Vie | 207 | 34.5 | 210 | 35.0 | A: closes → Vestal; B: stays |
| West Sylvan MS | Spa | 116 | 38.7 | 133 | 44.3 | stays |
| Kellogg MS | Spa | 201 | 67.0 | 257 | 85.7 | stays |
| George MS | Spa | 109 | 36.3 | 123 | 41.0 | receives OG + Chávez 6-8 |
| Beaumont MS | Spa | 101 | 33.7 | 145 | 48.3 | → Roseway Heights |
| Roseway Heights MS | Spa | 93 | 31.0 | 78 | 26.0 | receives Beaumont |
| Ockley Green MS | Spa | 63 | 21.0 | 34 | 11.3 | → George |
| Roseway Heights MS | Vie | 64 | 21.3 | 72 | 24.0 | stays |
| Harrison Park MS | Man | 111 | 37.0 | 98 | 32.7 | stays |
| Tubman MS | Man | 48 | 16.0 | 52 | 17.3 | stays |
| Mt. Tabor MS | Jpn | 222 | 74.0 | 210 | 70.0 | stays |
| Lane/Brentwood MS | Rus | 36 | 12.0 | 30 | 10.0 | stays |

Context [PPS TLE deck, June 2026, slide 13]: 2025-26 K "Lottery Slots" and "Enrollment" by language read Chinese 104/127, Japanese 89/104, Russian 25/25, Spanish 306/278, Vietnamese 36/52. The column order is ambiguous in the extract. K focus-option lotteries offer 26 seats per school (one class) [PPS 2026-27 K Lottery Results Summary], which is a useful marker for one class.

**Students moved by A's DLI program moves (2031-32 PSU counts):** elementary 1,275 (Beach 127, James John 136, Sitton 113, Atkinson 183, Scott 223, Clark 87, MLK 196, RCP 210); middle 179 (Beaumont 145, Ockley Green 34) plus Chávez 6-8 (≈98, estimated as 1/3 of 295). B drops RCP's 210. Some of these students move because their building closes (Beach, James John, RCP in A), not because of the program move. The Phase 4 "DLI kids moved" metric should split the two.

### 2.3 Proposed strand rule [DEFAULT, since PPS publishes none]

A first idea was "about 2 classes per grade" if PPS has no rule. Applied strictly, that fails almost every strand today (only Ainsworth, Rigler, Richmond, Kellogg and Mt. Tabor pass), so an option that keeps immersion strands in place would collapse into a plain redraw. The model uses two tiers instead:

- **Healthy strand (target, reported):** ≥ 2 classes/grade. Elementary ≥ 44 students/grade (2 × 22) averaged over K-5. Middle ≥ 40 students/grade.
- **Viable strand (hard rule for an option that keeps some immersion strands in place):** ≥ 1 full class/grade. Elementary ≥ 22 students/grade (≥ 132 K-5). Middle ≥ 20 students/grade (≥ 60 across 6-8).
- **Sole-pathway exemption:** if a strand is the only host for its language on its HS pathway (Tubman Mandarin, Lane/Brentwood Russian, Kelly Russian, Roseway Vietnamese, Richmond/Mt. Tabor Japanese), it stays even if below viable. Moving it can't create continuity, and PPS keeps all of these in both scenarios.
- **Continuity (hard, all options):** each K-5 strand feeds exactly one 6-8 strand of the same language, which feeds that language's high school (Spanish by home-address region). This matches today's chart and A.

Applying the viable rule to 2031-32 numbers: **Clark (14.5/grade), Sitton (18.8) and Beach (21.2)** fall below viable; Beach and James John close anyway. **Ockley Green MS Spanish (11.3)** falls below viable. In an option that keeps some strands in place, these still move to their pathway's surviving host, the same as A. Atkinson (30.5), Scott (37.2), James John (22.7, but its building closes) and RCP are viable where they are. In such an option, a strand whose building stays open stays put. A strand whose building closes moves to the nearest viable same-language host on its pathway, or travels with the neighborhood receiver if the receiver can hold it in range (e.g. James John → Sitton).

---

## 3. Focus options: Winterhaven and da Vinci

| | Winterhaven | da Vinci Arts |
|---|---|---|
| Grades | K-8 | 6-8 |
| Enrollment | 316 (2025-26); 310 forecast 2031-32 [PPS/PSU]; TLE deck: "Winterhaven 316" | 429 (2025-26); 419 forecast 2031-32 [PPS/PSU]; TLE deck: "da Vinci 429" |
| Building / address | 3830 SE 14th Ave [PPS lottery-slot sheet]. Built 1930. PPS historic survey calls it "Winterhaven at Brooklyn School" [3P via search of a PPS ILS PDF] | 2508 NE Everett St [PPS lottery-slot sheet]. Built as Girls Polytechnic HS, later James Monroe HS, closed 1978 [3P, Wikipedia] |
| Formerly a neighborhood school? | **Probably: the old Brooklyn School.** Its use as a neighborhood elementary and its closure date are **unverified** | **No, not an elementary or middle neighborhood school.** It was a district high school (Girls Poly/Monroe), not a K-8 attendance-area school |
| Functional capacity (LRFP 2021) | 261 (13 classrooms + 1 modular); utilization 112% (2021-22) | 714 (25 classrooms + 6 modular); utilization 63% (2021-22) |
| Admission | Lottery. 2026-27: K "Offered 26, Waitlist 70, Applications 143" [PPS K Lottery Results]; 23 sixth-grade transfer slots [PPS MS/HS lottery-slot sheet] | Lottery at 6th grade: 150 sixth-grade slots, 3 seventh, 4 eighth [PPS MS/HS lottery-slot sheet, 2026-27] |
| Where students come from (top 5) | "Hosford (45), Grout (32), Sellwood (26), Brentwood/ Lane (18), Out of District (15)" | "Ockley Green (60), Tubman (56), Roseway Heights (40), Hosford (36), Brentwood/Lane (35)" |
| Scenario A / B | **No change in either.** The A 6-8 map labels it "Winterhaven K-8 Focus/ Option" | **No change in either.** The A 6-8 map labels it "da Vinci Middle School Focus/Option" |
| Vs. 500 threshold | 310 < 500, and the threshold applies to K-8s per the Aug 4 memo | 419 < 500 |

Enrollment-origin rows come from the [PPS] TLE Committee "Alternative & Focus School Overview," June 2026, slide 18.

**What PPS has said about their size vs. 500:** nothing specific that we found. The thresholds are stated generically ("K–8 and middle school: 500 students"). No document explains why focus options under 500 are untouched. The closest statements: Res. 7307 says "Access to choice programs will be balanced with the goal of assuring well-resourced neighborhood schools across our system" [PPS, https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3997273]. OPB reports that officials "heard from families and students in support of focus options, like art at Buckman and da Vinci and environmental issues at Sunnyside." The Oregonian, quoted by Families for Equity, says "The schools that were spared include Da Vinci Middle School, an arts magnet, and Winterhaven K-8, a science magnet." [3P].

Other focus-option moves in both scenarios: Buckman (arts K-5) closes. Sunnyside loses its environmental focus status and becomes a neighborhood K-5 [3P OPB: "its status as an environmental focus option school would be 'discontinued'"]. Odyssey moves to the MLC site. The MLC 9-12 program closes ("students move to their neighborhood high school. It is not counted as a school closure" [PPS]). MLC becomes K-8. Bridger loses grades 6-8.

---

## 4. Scenarios A and B at the middle and high school levels

All changes take effect "no later than the 2027-28 school year and will be completed within three years" [PPS FAQ, Oct 1 2026]. The 6-8 map is titled "School Year 2027-28". The superintendent recommends in November, and the board votes in December 2026.

### 4.1 Closures

- **A (14):** "Beach · Buckman · Creston · Irvington · James John · Lewis · Maplewood · Marysville · Peninsula · Rose City Park · Sabin · Sellwood MS · Stephenson · Woodmere". **B (11):** the same minus Lewis, Rose City Park and Stephenson [PPS overview].
- Sellwood MS is **the only middle school closure** in both. Receivers (KATU): "Hosford for students from the Llewellyn area and Brentwood for students from the Duniway and Lewis areas." The A 6-8 map labels the Sellwood building "Sellwood School Closed".
- MLC 9-12 program closes (not counted as a closure). The Odyssey building (1849 SW 58th Ave) is shown "Odyssey Building Closed" on the A 6-8 map.

### 4.2 K-8 → K-5 conversions and middle-grade moves (identical in A and B)

| From | 6-8 goes to | HS of receiving MS |
|---|---|---|
| Beverly Cleary 6-8 | Beaumont MS | Grant |
| Laurelhurst 6-8 | Mt. Tabor MS | Grant for the Laurelhurst area; Mt. Tabor is otherwise Franklin, so the split continues (see 4.4) |
| Bridger Creative Science 6-8 | Harrison Park MS | McDaniel / Franklin split |
| Sunnyside Environmental 6-8 | Hosford MS | Cleveland |
| Faubion 6-8 | Ockley Green MS | Jefferson |
| Vernon 6-8 | Harriet Tubman MS | Jefferson |
| César Chávez 6-8 (Spanish) | George MS | Roosevelt |
| MLC | becomes K-8 (with Odyssey on site) | — |

Also: **Irvington** closes; its area goes to "Beverly Cleary for K–5 students and Beaumont for the area's middle school pathway" [3P KATU]. Today it goes to Tubman → Grant, so the Tubman/Grant split feeder goes away.

### 4.3 Middle schools with attendance-boundary changes

A and B list the same middle schools: **Beaumont, Brentwood, George, Harriet Tubman, Harrison Park, Hosford, Jackson, Kellogg, Mt. Tabor, Ockley Green, Robert Gray** [PPS overview]. Not listed: **Roseway Heights** (gains only the Beaumont Spanish program), **West Sylvan**, **da Vinci**, and **Winterhaven**. Jackson and Gray change in both, even though B keeps Stephenson open. Bridger is not a separate "6-8 school" after conversion.

**Neighborhood middle schools after A** (A 6-8 map): Beaumont, Brentwood (formerly Lane; PPS site: "Lane Middle School (Now Brentwood)"), George, Gray, Harrison Park, Hosford, Jackson, Kellogg, Mt. Tabor, Ockley Green, Roseway Heights, Tubman, West Sylvan = **13**. Add the K-8 neighborhood schools Astor and Skyline, the focus schools da Vinci (6-8), Winterhaven (K-8) and MLC & Odyssey (K-8), and ACCESS (2-8, alternative).

### 4.4 High schools

- HS with **attendance-boundary changes**, A and B alike: **Cleveland, Franklin, Jefferson, Lincoln, McDaniel, Roosevelt**. **Grant and Ida B. Wells are not listed** [PPS overview and regional PDFs]. Oddity: Lincoln gains or loses area, but its only neighbor, Wells, isn't listed. It may be the MLC HS closure or an omission; flag it for Phase 0.
- No PPS **9-12 boundary map** for either scenario was found. **The A 6-8 map shades each middle-school zone by high-school cluster** (legend: Cleveland, Franklin, Grant, Jefferson, Lincoln, McDaniel, Roosevelt, Wells-Barnett), so A's HS lines can be digitized from it. Visible on the map:
  - Tubman is now all Jefferson; the Irvington area moves to Beaumont/Grant.
  - Mt. Tabor's zone still includes a Grant-shaded Laurelhurst area alongside Franklin.
  - Harrison Park is McDaniel plus a Franklin-shaded southern piece.
  - Brentwood is Franklin plus a Cleveland-shaded western piece.
  - Hosford, which absorbs Sellwood's Llewellyn area, is all Cleveland.
  
  **Split feeders therefore persist in A** at Mt. Tabor, Harrison Park and Brentwood. This is my read of the shading, to confirm when digitizing.
- Current split feeders, per PPS [Sept 15 deck, slides 18-19]: Bridlemile K5 (Gray / West Sylvan); Bridger and Sunnyside K8 (focus students return to their neighborhood HS); Atkinson (Kellogg Spanish DLI / Harrison Park non-DLI); Woodstock (Harrison Park Mandarin / Brentwood non-DLI); Beaumont MS (Grant / McDaniel Spanish DLI); Harriet Tubman MS (Grant / Jefferson); Harrison Park MS (Franklin / McDaniel / Cleveland Chinese DLI); Hosford MS (Cleveland / Franklin); Brentwood MS (Cleveland / Franklin); Mt. Tabor MS (Grant Japanese DLI / Franklin); Ockley Green MS (Jefferson / Roosevelt Spanish DLI).

### 4.5 Official boundary maps

| Map | Status |
|---|---|
| Scenario A, Grade 6-8 Attendance Areas, SY 2027-28 | **Have**: `PPS BoardBook PDF "Scenario A - Attendance Boundaries 6-8.pdf"` (ArcGIS Pro export, "Rightsizing Model 2026.09.24 / Version: 10/5/2026 12:58 PM"). The text layer holds street and school labels only, no geometry; polygons have to be digitized. |
| Scenario A K-5, Scenario A 9-12, all Scenario B maps | **Not found** on pps.net. The scenarios page links only the overview and four regional PDFs. The "How Could Your School Be Impacted?" page loads per-school data dynamically, and it couldn't be fetched as static files. |
| Current HS feeder chart | `PPS_High_School_Feeder_Patterns_Eng.pdf` (9 pp., includes the DLI feeder chart) |

### 4.6 Stated principles relevant to lines

- **Board Policy 4.10.045-P (Student Assignment)**, as quoted to the board on Mar 31 2026: "A. A feeder pattern that allows as many students as possible to continue together from one school level to the next · B. Student body demographics · C. Compact boundaries that promote safer routes to schools and a sense of community as well as recognize and address natural and human-made barriers · D. Optimal use of existing facilities · E. Program and enrollment stability in the surrounding schools · F. Limiting the impact of boundary changes to the smallest number of students possible". The policy calls these a "non-prioritized list" that "may conflict with one another" [PPS, Mar 31 2026 work session book, https://meetings.boardbook.org/Documents/FileViewerOrPublic/915?file=3988980].
- **Res. 7307 Guiding Principles** (May 26 2026): "...maintain a sustainable portfolio of school facilities... and prioritize walkability and safe routes to schools." Workplan: "minimizes disruption for students, families, and staff, including an assessment of cohort cohesion" [PPS].
- **FAQ:** "If boundaries need to change, PPS will look at where students live, school size and space, programs, transportation, and how students move through schools from elementary to high school." [PPS FAQ, Sept 15 2026]
- **KPIs (Sept 15 deck, slide 17):** "1. Percent of efficiently utilized schools · 2. Percent of students living within 1.0 and 1.5 miles of school · 3. Number of schools with split feeders · 4. Percent of middle school feeders moving to the same high school". Balance and impact KPIs (slide 20): "Percent of focal students who will experience the change · Number of Title I and CSI/TSI schools impacted · Number of students moving to a new school or site". Slide 14 also lists "Range of enrollment (largest - smallest) by grade level".
- OPB: "She said a school's walkability was also a consideration."
- Equity audit lesson: "Families also described how new feeder patterns disrupted peer continuity" (SEGC school-by-school volume).

---

## 5. Transportation eligibility

| Rule | Text | Source |
|---|---|---|
| State mandate | "A school district is required to provide transportation for elementary school students who reside more than one mile from school and for secondary school students who reside more than 1.5 miles from school." | [STATE] ORS 327.043(2), https://www.oregonlegislature.gov/bills_laws/ors/ors327.html |
| State reimbursement | "Approved transportation costs"... "(A) Elementary school students who live at least one mile from school; (B) Secondary school students who live at least 1.5 miles from school" | [STATE] ORS 327.013(2)(a) |
| Who is "elementary" | "pupils attending a school offering only an elementary curriculum, any combination of grades K through 8"; students at a board-designated "junior high school or middle school may be considered secondary students" | [STATE] OAR 581-023-0040(1)(a)-(b), https://oregon.public.law/rules/oar_581-023-0040 (an ODE note says the rule was amended Feb 19 2026; the amended text wasn't retrieved) |
| How distance is measured (state) | "measured over the shortest practicable route on maintained public roadways... or over existing pedestrian facilities" | [STATE] OAR 581-023-0040(1)(e) |
| PPS K-5 | "For students who live more than one mile from the elementary school they attend within their school attendance boundary." | [PPS] Service Guidelines – Student Transportation, rev. 08/07/2024, §B.1, https://resources.finalsite.net/images/v1751562292/ppsnet/thzskadliar1v7qds4yc/Service_Guidelines_Student_Transportation_2024.pdf |
| PPS 6-8 | "For students who live more than one and one-half miles from the middle school they attend which is within their attendance boundary." §D.1: "within one mile... (Pre-kindergarten – 5) or within 1.5 miles for grades 6 – 8" | same |
| PPS 9-12 | "High school students who reside more than one and 1.5 miles from the school they attend which is within their attendance boundary and one mile or more from TriMet, private, or other public services." §D.1: high schoolers within 1.5 mi, or within one mile of a TriMet stop, get yellow-bus service only for hazardous walking conditions | same |
| PPS distance method | "Measurement of the most direct combination of roads, streets, highways, and public paths... from the street immediately in front of the school to the street in front of the student residence." | same §B.3 |
| PPS DLI | Native-speaker DLI students at their assigned school: >1 mi (ES) / >1.5 mi (MS). Non-native DLI students ride only as "hitchers" on existing routes | same §B.5 |
| High schoolers on TriMet | "if you're a Portland Public School (PPS) District student in grades 9-12, you can use your school ID card to get rides on TriMet, Portland Streetcar and WES Commuter Rail during the school year." | [3P] TriMet blog, Aug 20 2025, https://blog.trimet.org/2025/08/20/trimet-101-how-to-get-around-as-a-student/ |

**For the busing-cost metric:** K-5 is eligible at walk distance > 1.0 mi. 6-8 is eligible at > 1.5 mi, and that includes 6-8 students in K-8 buildings, per PPS §D.1's grade-based wording. That's stricter than OAR's school-type definition; flag it. 9-12 gets **yellow bus** only if > 1.5 mi **and** > 1.0 mi from a TriMet stop. Every other high schooler gets transit via school ID, so high-school "cost" is transit time, not bus miles.

---

## 6. Split feeders, walkability, and boundary principles: summary

PPS treats split feeders as a measured negative. Its KPIs are "Number of schools with split feeders" and "% MS feeders moving to the same HS (target = 100%)" (Jefferson KPI). Policy 4.10.045 factor A prefers "as many students as possible" continuing together. Walkability is a guiding principle (Res. 7307) and a KPI (% within 1.0 and 1.5 mi). Even so, PPS's Scenario A keeps several split feeders, apparently because DLI pathways and capacity win out. "No single factor will determine whether a school is changed or closed" [PPS FAQ].

---

## Spec for the solver

**Evaluate sizes on PSU 2031-32 projected enrollment** (primary); report 2025-26 as a check. Robustness check: −9% (per PLAN).

### Hard constraints per level

| Level | Min | Max | Notes |
|---|---|---|---|
| K-5 (neighborhood, incl. receivers) | **360** | min(functional capacity @100%, **600**) | 600 is [DEFAULT] |
| K-8 (Astor, Skyline) | **exempt** in district-like runs (PPS leaves them < 500); otherwise 500 | functional capacity | Report the shortfall; don't force it |
| 6-8 neighborhood MS (13 after A) | **500** | functional capacity @85% rate (i.e. utilization ≤ 100%) | utilization 70–100% is a stated PPS aim [PPS, Family Guide p. 2]; ≥ 70% reported, hard only if requested |
| 9-12 comprehensive (Cleveland, Franklin, Grant, Ida B. Wells, Jefferson, Lincoln, McDaniel, Roosevelt) | **1,100** | functional capacity: Jefferson 1,773 (modernized; 1,590 now), Grant 1,935, McDaniel 1,735, Roosevelt 1,404 (2025 slide); others LRFP 2021 (Cleveland 1,859, Franklin 1,744, Lincoln 1,867*, Wells 1,872) | range (max − min) ≤ 350 as **soft** (status quo is 375). *Lincoln's new building capacity is unconfirmed |
| Focus/alt (da Vinci, Winterhaven, MLC/Odyssey, ACCESS, Benson) | fixed enrollment, no boundary | — | Close 2 focus options removes da Vinci and Winterhaven and returns their students to the neighborhood |

Feeder rules: middle zones are unions of whole K-5 zones, and high zones are unions of whole middle zones. A split is allowed only when it's needed for feasibility, and every split gets reported. PPS's own A keeps splits at Mt. Tabor, Harrison Park and Brentwood, so the district-like option must allow those three.

### DLI rule

1. **Continuity (all options):** for each language and HS pathway there's exactly one K-5 host and one 6-8 host. Spanish HS assignment is by home-address region (Lincoln+Wells → Lincoln; Roosevelt+Jefferson → Roosevelt; McDaniel+Grant → McDaniel; Franklin+Cleveland → Franklin). Mandarin goes MLK/BEH → Tubman → Jefferson, and Woodstock → Harrison Park → Cleveland. Japanese goes Richmond → Mt. Tabor → Grant; Russian Kelly → Brentwood → Franklin; Vietnamese RCP or Vestal → Roseway Heights → McDaniel.
2. **Viable strand [DEFAULT]:** ≥ 22 students/grade averaged over K-5 (≥ 132 total), and ≥ 20/grade in 6-8 (≥ 60). **Healthy:** ≥ 44/grade K-5 and ≥ 40/grade 6-8 (reported).
3. **Sole-pathway exemption:** a strand that's the only host on its pathway stays regardless of size.
4. **DLI students count toward their host building's size and capacity.** Whole-school DLI buildings (Rigler, Lent, Richmond) have no neighborhood zone.
5. **Options that keep some immersion strands in place:** a strand stays in its 2025-26 building if the building stays open and the strand is viable. Otherwise it moves to the pathway's surviving or viable host, and the solver uses A's destination unless a closer viable host exists.

### Scenario-A facts the "district-like" option must replicate

1. **Closures (14):** Beach, Buckman, Creston, Irvington, James John, Lewis, Maplewood, Marysville, Peninsula, Rose City Park, Sabin, Sellwood MS, Stephenson, Woodmere. The MLC 9-12 program closes too (its students go to their neighborhood HS), and the Odyssey building closes.
2. **K-8 → K-5:** Beverly Cleary → Beaumont; Laurelhurst → Mt. Tabor; Bridger → Harrison Park; Sunnyside → Hosford (Sunnyside also loses its focus status); Faubion → Ockley Green; Vernon → Tubman; Chávez → George. MLC becomes K-8 with Odyssey.
3. **Remaining K-8s unchanged:** Astor and Skyline (neighborhood), Winterhaven (focus).
4. **Sellwood MS split:** the Llewellyn area goes to Hosford; the Duniway and Lewis areas go to Brentwood.
5. **Irvington area:** K-5 goes to Beverly Cleary; 6-8 goes to Beaumont (Grant).
6. **DLI moves:** Spanish Beach, James John and Sitton → Chávez; Chávez 6-8 and Ockley Green Spanish → George; Atkinson → Lent; Scott → Rigler; Beaumont MS Spanish → Roseway Heights; Vietnamese RCP → Vestal; Mandarin Clark → Woodstock; Mandarin MLK → Boise-Eliot/Humboldt. Ainsworth/West Sylvan, Richmond/Mt. Tabor, Kelly/Brentwood, Woodstock/Harrison Park and Tubman are unchanged.
7. **Other program moves:** Creston DHH → Glencoe; Odyssey → MLC site; Buckman's focus program ends with the closure.
8. **K-5 receivers (KATU):** Maplewood → Hayhurst + Rieke; Stephenson → Markham + Capitol Hill; Rose City Park → Scott (neighborhood); Buckman → Abernethy + Sunnyside; Creston → Atkinson; Marysville → Arleta; Woodmere → Whitman; Lewis → Duniway; Beach → Chief Joseph; James John → Sitton; Peninsula → Rosa Parks; Sabin → MLK Jr.
9. **Boundary-change lists, which bound which schools may change lines:** MS: Beaumont, Brentwood, George, Tubman, Harrison Park, Hosford, Jackson, Kellogg, Mt. Tabor, Ockley Green, Gray. HS: Cleveland, Franklin, Jefferson, Lincoln, McDaniel, Roosevelt. **Roseway Heights, West Sylvan, Grant and Ida B. Wells keep their lines in A.**
10. **Middle-school set after A:** the 13 neighborhood MS listed in 4.3 plus focus/alternative schools.
11. **Jefferson dual-assignment sunset as baseline:** Peninsula-area and Beach-Spanish → Roosevelt; Irvington → Grant; everything else in the old dual zone → Jefferson.

Scenario B is the same, except: Lewis, Rose City Park and Stephenson stay open. There's no Vietnamese move. The K-5 boundary-change list drops Capitol Hill, Duniway, Llewellyn, Markham and Scott and adds Lewis. MS and HS change lists are unchanged.

---

## Unresolved gaps

1. **No PPS DLI minimum strand size.** The rule above is a labeled default derived from A's structure and PSU program counts.
2. **The 70–100% utilization band is a stated PPS aim** (corrected 2026-10-12). Family Guide glossary p. 2, "Space use goal": "The district aims to use 70%-100% of a school's available room for students." PPS staff defined "efficiently used schools" the same way at the Sept 15, 2026 board meeting (https://youtu.be/uAf7l-ChjFo?t=15369). It applies to every school level, not just middle schools. PPS gives no research basis for it. 100% of functional capacity (85% rate for middle and high schools) is the ceiling; 70% is reported as PPS's floor for efficient use.
3. **No HS upper bound** beyond capacity and the <350 range KPI. Post-modernization capacities are published only for Jefferson, Grant, McDaniel and Roosevelt (2025 slide). Lincoln (new building), Cleveland and Wells use LRFP 2021 values.
4. **Per-school Scenario A and B projected enrollments aren't published** in the PDFs. The "How Could Your School Be Impacted?" tool is dynamic and needs a browser (/browse) to scrape.
5. **Missing maps:** no Scenario A K-5 or 9-12 maps and no Scenario B maps were found. Only the A 6-8 map exists, and A's HS clusters can be read from its shading.
6. **The Lincoln-without-Wells HS boundary-change listing** is unexplained.
7. **Winterhaven building history:** that it was once Brooklyn neighborhood school is likely but unverified.
8. **Chávez K-8's Spanish 6-8 count** isn't split out in the PSU table; ≈1/3 of 295 is my estimate.
9. **OAR 581-023-0040 was amended Feb 19 2026** and the new text wasn't retrieved. ORS 327.043's 1 / 1.5 mile mandate is unaffected.
10. **The TLE deck's DLI K "slots vs enrollment"** column order is ambiguous in the text extract.
