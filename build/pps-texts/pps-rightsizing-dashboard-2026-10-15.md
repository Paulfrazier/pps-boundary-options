---
title: "District Rightsizing & School Boundary Proposal Dashboard (PPS, Power BI)"
source_url: "https://app.powerbi.com/view?r=eyJrIjoiZTYxZThjOWUtZDAyZS00YmFkLWI4YWUtOTZiOGUxOTAxNWMzIiwidCI6ImQwOGRmYzk0LWEyM2MtNDRlNC04YjhkLTRhYmM0MGRkYTlhZSIsImMiOjZ9"
linked_from: "pps.net Rightsize section side navigation"
publisher: "Portland Public Schools"
versions: "v1.0 Oct 14, 2026; v1.1 Oct 15, 2026 (\"Added Grade and Program Level Data\"), per the dashboard's version page"
retrieved: 2026-10-15
document_type: "Interactive Power BI report, 13 pages; text extracted from the rendered page plus a screenshot of each page"
capture_scope: "PARTIAL. Default filter selections only. Scrollable tables show only the rows visible on screen; scenario/grade-band toggles and the 'High Level Methodology' hover text were not captured."
checks: "Per-school enrollment totals match the PPS Family Guide tables (e.g. MLK Jr 376/395/389/386/383; Beaumont 506..498; Tubman 608..455; Jefferson 570..1190; Abernethy 354..365), within 1 in a cell or two."
---

# PPS Rightsizing & School Boundary Proposal Dashboard (Power BI), partial capture

Unofficial text capture of PPS's interactive dashboard, for checking figures. Each page's text is as rendered (UI labels removed); tables run together where Power BI renders cells without separators, so read them with the screenshot. Headline figures read from the pages:

- **District (p. 2):** Scenario A closes 14 schools, B 11. Share of schools sustainable in 2031-32: A 67%, B 59%, Status Quo 26%. Share of students in sustainable schools: A 80%, B 74%, Status Quo 48%; by student group (DC, historically underserved race/ethnicity, IEP, MLL) in the same table. K-8 students moved/stayed: A 27%/73%, B 24%/76%.
- **Grade bands (pp. 3-6, KPI cards; only the default scenario's cards are in the captured text below, and the other scenarios' values were read from the live dashboard by the site track, not re-checked here):** within 1 mi / 1.5 mi, % efficiently used, % sustainable 2031-32, schools closed. K-5: A 55/78, 51%, 72%, 13 closed; B 58/79, 38%, 55%, 10 closed; Status Quo 65/81, 22%, 18%. K-8: A and B 71/82; Status Quo 78/84. 6-8: A and B 28/50, 1 closed; Status Quo 30/50. 9-12: no walk figures.
- **Regions (pp. 7-10):** per-school notes on boundary and program moves, with projections.
- **p. 11:** who ends up in sustainable schools, by student group.
- **p. 13 (added Oct 15):** grade-by-grade K-8 projections per school, scenario and program (PSU-based).

PPS does not state how "within 1 mile" is measured on the captured pages (the methodology is in a hover tooltip not captured). PPS's shares run below our model's network-walk shares (K-5 Status Quo 65% vs our 72.2%; A 55% vs 62.7%; B 58% vs 65.3%; 6-8 Status Quo 30% vs 39.9%, A 28% vs 30.3%), while the changes between scenarios agree closely (K-5 Status Quo→A −10 points PPS vs −9.5 ours; →B −7 vs −6.9) [inferred: comparison by the site track, 2026-10-15].

## Page 1

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p1.png`

```text
Welcome to the District Rightsizing & School Boundary Proposal Dashboard Our Goal: Ensure every student in our district attends a school that is sustainable, safely staffed, and packed with the academic, artistic, and support programs they deserve. Quick Tips for Parents:Hover for Info: Look for the i icon next to chart headers to read short explanations of the data.Navigating the PagesDistrict Overall: High-level summary comparing the impact of all scenarios across the whole district. Building Capacity / Utilization: Shows which school buildings are operating at optimal student size. Grade-Level Pages (K-5, K-8, 6-8, 9-12): Specific enrollment projections and distance metrics for each grade band. Neighborhood Clusters: Detailed neighborhood-by-neighborhood maps, program relocations, and boundary changes. Key Definitions & GlossarySustainable SchoolA school with enough enrolled students to avoid staffing changes, sustain Arts/Music and other pathways and has dedicated Social/Emotional Support StaffUtilization RateOperating a school building within its ideal capacity (typically 70%-100%). Prevents both uncomfortable overcrowding and underused, empty classrooms. 100% does not mean every room is filled all the time. Status QuoKeeping all school boundaries, grade structures, and open buildings exactly as they are today. Serves as the baseline to compare proposed changes against doing nothing.Feeder PatternThe pathway determining which middle and high school students move to after elementary school. Shows your child's long-term academic pathway from K through 12th grade.Split FeederWhen students graduating from one elementary school split and go to two different middle schools based on home address. Explains why neighbors in the same elementary school might attend different middle schools.Students Moved vs. StayedThe percentage of students whose assigned neighborhood school changes under a scenario vs. those remaining at their current school. Helps families quickly gauge how much disruption a scenario causes in their immediate area. District Overall K-5 OverallK-8 Overall6-8 Overall9-12 Overall Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers-+ 125% Microsoft Power BI1of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 125%
```

## Page 2

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p2.png`

```text
Grade_Band_Filter ESHSK8MS 
 Scenario Number of Schools Closed % Sustainable Schools 31-32 % of Students in Sustainable Schools 31-32 % DC Students in Sustainable Schools 31-32 % Underserved Race in Sustainable Schools 31-32 % Students with IEP in Sustainable Schools 31-32 % MLL in Sustainable Schools 31-32
 Scenario A1467%80%81%83%77%87% Scenario B1159%74%76%79%71%84% Status Quo026%48%42%46%41%44%
 Actual and Projected Enrollment Actual and Projected Enrollment Click these buttons to access grade band ranges, regional impacts and school level impacts District Overall K-5 OverallK-8 Overall6-8 Overall9-12 Overall Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers 
All Students (K-8 Total)All Students (K-8 Total)Historically Underserved Race / EthnicityHistorically Underserved Race / EthnicityStudents Experiencing PovertyStudents Experiencing PovertyStudents Receiving Multilingual ServicesStudents Receiving Multilingual ServicesStudents Receiving Special Education ServicesStudents Receiving Special Education ServicesScenario Name % Moved % Stayed % Moved % Stayed % Moved % Stayed % Moved % Stayed % Moved % Stayed
Scenario A27%73%28%72%27%73%31%69%27%73%Scenario B24%76%26%74%25%75%28%72%24%76%
 Current State KPI -+ 102% Microsoft Power BI2of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 102%Page 2 of 13 Next Page Button Pressed Enter or Space
```

## Page 3

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p3.png`

```text
Scenario Name Scenario AScenario BStatus Quo Number of K-5 Schools Closed Number of K-5Schools Closed10 % of K-5 school with 360 or more students % of K-5 school with 360 or morestudentsScenarioStatus QuoTarget Goal High Level Methodology (Hover here) High Level Methodology (Hover here) K-5 Projected Enrollment with Scenario K-5 Projected Enrollment with Scenario
School 2027 2028 2029 2030 2031
Abernethy354359369368365Ainsworth555568551551557Alameda498503508503493Arleta224536545552543Atkinson395394395412413Beach00000Beverly Cleary503494496478484Boise-Eliot/Humboldt521540533533512Bridger Creative Science310304313313305Bridlemile419414414422413Buckman00000Capitol Hill313304309322314Cesar Chavez541532525528527Chapman317340335327337Chief Joseph420426424421417Clark276277279275272Creston00000Dr Martin Luther King Jr376395389386383Duniway338348345349347Faubion425423414416407
Total1616816236162041613215979
 % Students living within 1 mile58%% Students living within 1.5 miles79% % Efficiently Utilized 31-3238%% Sustainable 31-3255%% of Students in Sustainable Schools 31-3264% 
Enrollment Range 2027-2028 2028-2029 2029-2030 2030-2031 2031-2032
260 - 309810788310 - 359118888360 - 39966654Closed / Excluded910101010Less than 26021323Over 4001617181919
 District Overall K-5 OverallK-8 Overall6-8 Overall9-12 Overall Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers-+ 125% Microsoft Power BI3of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 125%Page 3 of 13 Next Page Button Pressed Enter or Space
```

## Page 4

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p4.png`

```text
Scenario Name Scenario AScenario BStatus Quo Number of K-8 Schools Closed Number of K-8Schools Closed0 % of K-8 schools with 500 or more students % of K-8 schools with 500 or more studentsScenarioStatus QuoTarget Goal High Level Methodology (Hover here) High Level Methodology (Hover here) % Students living within 1 mile71%% Students living within 1.5 miles82% K-8 Projected Enrollment with Scenario K-8 Projected Enrollment with Scenario
School 2027 2028 2029 2030 2031
Access Academy310296286278275Astor423421456439431Skyline196197190180177Winterhaven311312312311310
Total12401226124412081193
 % Efficiently Utilized 31-3240%% Sustainable 31-320%% of Students in Sustainable Schools 31-320% 
Enrollment Range 2027-2028 2028-2029 2029-2030 2030-2031 2031-2032
400 - 44911 11450 - 499  1  Closed / Excluded11111Less than 40044444
 District Overall K-5 OverallK-8 Overall6-8 Overall9-12 Overall Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers-+ 125% Microsoft Power BI4of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 125%Page 4 of 13 Next Page Button Pressed Enter or Space
```

## Page 5

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p5.png`

```text
Scenario Name Scenario AScenario BStatus Quo Number of 6-8 Schools Closed Number of 6-8Schools Closed1 % of 6-8 schools with 500 or more students % of 6-8 schools with 500 or more studentsScenarioStatus QuoTarget Goal High Level Methodology (Hover here) High Level Methodology (Hover here) % Students living within 1 mile28%% Students living within 1.5 miles50% 6-8 Projected Enrollment with Scenario 6-8 Projected Enrollment with Scenario
School 2027 2028 2029 2030 2031
Beaumont506502501490498Brentwood384664596542512DaVinci Arts430430428424419George604637669649636Harriet Tubman608546492465455Harrison Park642625614578591Hosford602669540512501Jackson618565487429405Kellogg507548582556579Mt Tabor645647599580546Ockley Green552486496491507Robert Gray481519552509491Roseway Heights655642671655629Sellwood5230000West Sylvan691652675650625
Total84488132790275307394
 % Efficiently Utilized 31-3243%% Sustainable 31-3264%% of Students in Sustainable Schools 31-3269% 
Enrollment Range 2027-2028 2028-2029 2029-2030 2030-2031 2031-2032
400 - 44911122450 - 49911333500 - 54934234Closed / Excluded 1111Less than 4001    Over 55098865
 District Overall K-5 OverallK-8 Overall6-8 Overall9-12 Overall Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers-+ 125% Microsoft Power BI5of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 125%Page 5 of 13 Next Page Button Pressed Enter or Space
```

## Page 6

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p6.png`

```text
% of 9-12 schools with 1100 or more students % of 9-12 schools with 1100 or morestudentsScenarioStatus QuoTarget Goal Scenario Name Scenario AScenario BStatus Quo Number of 9-12 Schools Closed Number of9-12 SchoolsClosed0 High Level Methodology (Hover here) High Level Methodology (Hover here) 9-12 Projected Enrollment with Scenario 9-12 Projected Enrollment with Scenario
School 2027 2028 2029 2030 2031
Benson12001216121512151213Cleveland14801501146514581371Franklin16721571151514661429Grant19381826171715801491Ida B Wells15311520149314951464Jefferson57081298811651190Lincoln15801546144213581331McDaniel15351488136313111281Roosevelt13371301125112561205
Total1284312781124491230411975
 % Efficiently Utilized 31-3278%% Sustainable 31-32100%% of Students in Sustainable Schools 31-32100% District Overall 
Enrollment Range 2027-2028 2028-2029 2029-2030 2030-2031 2031-2032
1100 - 129911234500 - 999111  Over 130077665
 K-5 OverallK-8 Overall6-8 Overall9-12 Overall Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers-+ 125% Microsoft Power BI6of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 125%Page 6 of 13 Next Page Button Pressed Enter or Space
```

## Page 7

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p7.png`

```text
Grant/McDaniel District Overall K-5 OverallK-8 Overall6-8 Overall9-12 Overall % Efficiently Utilized 31-3254%% Sustainable 31-3269%% of Students in Sustainable Schools 31-3282% Scenario Scenario AScenario BStatus Quo Number of K-5 Schools Closed Number of K-5Schools Closed2 Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers Percent of Sustainable Elementary Schools Percent of Sustainable Elementary SchoolsScenarioScenario AScenario BStatus Quo Percent of Sustainable K8 Schools Percent of Sustainable K8 SchoolsScenarioScenario AScenario BStatus Quo Percent of Sustainable Middle Schools Percent of Sustainable Middle SchoolsScenarioFifty PercentSeventy PercentStatus Quo Enrollment Ranges by ES Enrollment Ranges by ESEnrollment RangeLess than 260 s…260-309310-359360-449450 plus Enrollment Ranges by K8 Enrollment Ranges by K8 Enrollment Ranges by Middle School Enrollment Ranges by Middle SchoolEnrollment Range450-499500-549550+ 
School 2027 2028 2029 2030 2031
Alameda498503508503493Beaumont506502501490498Beverly Cleary503494496478484Clark276277279275272Grant19381826171715801491Harrison Park642625614578591Irvington00000Laurelhurst378370371361359McDaniel15361490136513151283Rigler487515510504505Rose City Park00000Roseway Heights655642671655628Scott512475479465470Sunrise246251241255257Vestal507505507507500
Total86848475825979667831
School Note
BeaumontSpanish DLI at Beaumont moves to the regional hub at Roseway Heights. The Beaumont boundary expands to include Beverly Cleary and current Irvington neighborhoods.Beverly ClearyBeverly Cleary middle grade students move to Beaumont Middle School, and the Beverly Cleary attendance boundary expands to include the Irvington neighborhood.ClarkMandarin DLI at Clark moves to Woodstock.Harrison ParkHarrison Park expands its boundary to include the Lent neighborhood and Kelly, while losing Atkinson. Middle grade students at Harrison Park move to McDaniel, Cleveland, or Franklin high schools based on the split feeder pattern.IrvingtonIrvington closes, with elementary students moving to Beverly Cleary, middle grade students moving to Beaumont Middle School, and high school aged students moving to Grant High School.LaurelhurstLaurelhurst middle grade students move to Mt. Tabor Middle School, and the Mt. Tabor boundary expands to include Laurelhurst. High school aged students from the Laurelhurst area move to Grant High School.RiglerRigler receives the Spanish DLI from Scott, and the Rigler neighborhood boundary moves completely to Scott.Rose City ParkRose City Park closes. Vietnamese DLI moves to Vestal, while middle grade VDLI students stay at Roseway Heights without middle grade changes. The Rose City Park neighborhood boundary moves 100% to Scott.Roseway HeightsRoseway Heights receives Spanish DLI from Beaumont Middle School, with all middle grade students moving to McDaniel High School when they reach high school age.ScottScott Spanish DLI moves to Rigler, and the Scott boundary expands to include the Rose City Park neighborhood boundary.VestalRose City Park VDLI moves to Vestal.
-+ 77% Microsoft Power BI7of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 77%Page 7 of 13 Next Page Button Pressed Enter or Space
```

## Page 8

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p8.png`

```text
Cleveland/Franklin District Overall K-5 OverallK-8 Overall6-8 Overall9-12 Overall % Efficiently Utilized 31-3248%% Sustainable 31-3271%% of Students in Sustainable Schools 31-3282% Scenario Scenario AScenario BStatus Quo Number of K-5 Schools Closed Number of K-5Schools Closed6 Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers Percent of Sustainable Elementary Schools Percent of Sustainable Elementary SchoolsScenarioFifty PercentSeventy PercentStatus Quo Percent of Sustainable K8 Schools Percent of Sustainable K8 SchoolsScenarioFifty PercentSeventy PercentStatus Quo Percent of Sustainable Middle Schools Percent of Sustainable Middle SchoolsScenarioFifty PercentSeventy PercentStatus Quo Enrollment Ranges by ES Enrollment Ranges by ESEnrollment RangeLess than 260 s…260-309310-359360-449450 plus Enrollment Ranges by K8 Enrollment Ranges by K8Enrollment Rangeless than 400 Enrollment Ranges by Middle School Enrollment Ranges by Middle SchoolEnrollment Rangeless than 400450-499500-549550+ 
School 2027 2028 2029 2030 2031
Abernethy354358369368365Arleta224536545552543Atkinson395394395412413Brentwood384586525480457Bridger Creative Science310304313313305Buckman00000Cleveland14651469142214041322Creston00000Duniway544517505482463Franklin16861601155615161476Glencoe318302309317316Grout308308306296293Hosford602747610575557Kellogg507548582556579Kelly407407410402401Lent401417424430421Lewis00000Llewellyn330340367387399Marysville3000000Mt Tabor645647599580546
Total1175711511112431103210769
School Note
AbernethyThe Abernethy attendance boundary expands to include approximately 50% of the Buckman neighborhood boundary.ArletaThe Arleta attendance boundary expands to include the pre-SEGC boundary from Marysville. This goes into effect for the 28-29 school year.AtkinsonAtkinson transitions its Spanish immersion program to the regional hub at Lent. The Atkinson attendance boundary expands to include 100% of the Creston boundary, with middle grade students moving to Kellogg Middle School instead of Harrison Park.BrentwoodThe Brentwood boundary expands to include the Lewis and Duniway areas, while the Kelly area moves to Harrison Park. High school aged students from the Whitman and Woodmere boundaries move to Franklin High School, and high school aged students from Woodstock, Lewis, and Duniway continue to Cleveland High School.Bridger Creative ScienceBridger middle grade students move to Harrison Park, while the K–5 program remains as a neighborhood focus/option school.BuckmanBuckman closes, with half of its attendance area assigned to Sunnyside and the other half assigned to Abernethy.ClevelandThe Cleveland boundary expands to include Sunnyside, while Woodmere and Whitman area high school aged students move to Franklin High School.CrestonCreston closes and its boundary goes 100% to Atkinson. Middle grade students then move to Kellogg Middle School and high school aged students move to Franklin High School. The Deaf and Hard of Hearing Program moves to Glencoe.DuniwayDuniway’s southern boundary area moves to Llewellyn, while Duniway expands to include the Lewis boundary. Middle grade students in this zone move to Brentwood Middle School instead of Sellwood.FranklinHigh school aged students in Sunnyside move to Cleveland High School, and all high school aged students from the Whitman and Woodmere areas move to Franklin High School. High school aged students in a portion of the Vestal area move to McDaniel High School.HosfordHosford receives the Sunnyside boundary as well as the Llewellyn area from Sellwood, while Creston middle grade students move to Kellogg. All middle grade students at Hosford move to Cleveland High School.KelloggKellogg’s boundary expands to include the Atkinson and Creston areas, with high school aged students moving to Franklin High School. Lent neighborhood students who moved to Kelly will now move to Harrison Park.KellyKelly’s boundary expands to include the Lent neighborhood, with middle grade students moving to Harrison Park Middle School and high school aged students moving to Franklin High School.LentLent receives the Spanish DLI from Atkinson, while its neighborhood area moves to Kelly.LewisLewis closes and its boundary joins the Duniway boundary.LlewellynThe Llewellyn boundary expands to include the southern portion of Duniway, with middle grade students moving to Hosford Middle School.MarysvilleMarysville closes in the 28-29 school year and the pre-SEGC Marysville boundary moves to Arleta. The previous Lent boundary moves to Kelly.Mt TaborMt. Tabor’s boundary expands to include Laurelhurst. High school aged students in Laurelhurst and Japanese DLI move to Grant High School, while high school aged students in the Glencoe area move to Franklin High School.SellwoodSellwood closes. The Llewellyn area plus a portion of the southern Duniway area move to Hosford. The remaining Duniway area and Lewis move to Brentwood, and high school aged students move to Cleveland High School.Sunnyside EnvironmentalSunnyside becomes a neighborhood-only school, allowing current out-of-neighborhood students to remain through fifth grade. Middle grade students move to Hosford. Sunnyside expands its boundary to include a portion of Buckman, and high school aged students move to Cleveland High School instead of Franklin.
-+ 77% Microsoft Power BI8of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 77%Page 8 of 13 Next Page Button Pressed Enter or Space
```

## Page 9

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p9.png`

```text
Ida B. Wells-Barnett/Lincoln District Overall K-5 OverallK-8 Overall6-8 Overall9-12 Overall % Efficiently Utilized 31-3267%% Sustainable 31-3260%% of Students in Sustainable Schools 31-3275% Scenario Scenario AScenario BStatus Quo Number of K-5 Schools Closed Number of K-5Schools Closed2 Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers Percent of Sustainable Elementary Schools Percent of Sustainable Elementary SchoolsScenarioFifty PercentSeventy PercentStatus Quo Percent of Sustainable K8 Schools Percent of Sustainable K8 SchoolsScenarioFifty PercentSeventy PercentStatus Quo Percent of Sustainable Middle Schools Percent of Sustainable Middle SchoolsScenarioFifty PercentSeventy PercentStatus Quo Enrollment Ranges by ES Enrollment Ranges by ESEnrollment RangeLess than 260 s…260-309310-359360-449450 plus Enrollment Ranges by K8 Enrollment Ranges by K8Enrollment Rangeless than 400 Enrollment Ranges by Middle School Enrollment Ranges by Middle SchoolEnrollment Range400-449450-499500-549550+ 
School 2027 2028 2029 2030 2031
Ainsworth555568551551557Bridlemile419414414422413Capitol Hill381370370387379Chapman317340335327337Forest Park261261258253259Hayhurst469448430421406Ida B Wells15311520149314951464Jackson618565487429405Lincoln15801546144213581331Maplewood00000Markham519543543554549Rieke348396422434432Robert Gray481519552509491Skyline196197190180177Stephenson00000West Sylvan691652675650625
Total83668339816279707825
School Note
Capitol HillThe Capitol Hill attendance boundary expands to include a portion of the Stephenson boundary.HayhurstThe Hayhurst attendance boundary expands to include a portion of the Maplewood area.JacksonThe Jackson boundary changes as the Maplewood area moves to Gray.LincolnHigh school aged students in the Skyline boundary move from Lincoln High School to Roosevelt High School.MaplewoodMaplewood closes, with 70% of its boundary moving to Hayhurst and 30% moving to Rieke.MarkhamThe Markham attendance boundary expands to include a portion of the Stephenson boundary.MLC K12MLC High School closes, and high school aged students move to their neighborhood high schools or Lincoln High School.Odyssey ProgramOdyssey moves to MLC.RiekeThe Rieke boundary expands to include a portion of the Maplewood boundary.Robert GrayThe Gray boundary expands to include the Maplewood area whose middle grade students used to move to Jackson.StephensonStephenson closes and merges 70% to Markham and 30% to Capitol Hill.
-+ 77% Microsoft Power BI9of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 77%Page 9 of 13 Next Page Button Pressed Enter or Space
```

## Page 10

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p10.png`

```text
Jefferson/Roosevelt District Overall K-5 OverallK-8 Overall6-8 Overall9-12 Overall % Efficiently Utilized 31-3253%% Sustainable 31-3273%% of Students in Sustainable Schools 31-3282% Scenario Scenario AScenario BStatus Quo Number of K-5 Schools Closed Number of K-5Schools Closed4 Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers Percent of Sustainable Elementary Schools Percent of Sustainable Elementary SchoolsScenarioFifty PercentSeventy PercentStatus Quo Percent of Sustainable K8 Schools Percent of Sustainable K8 SchoolsScenarioFifty PercentSeventy PercentStatus Quo Percent of Sustainable Middle Schools Percent of Sustainable Middle SchoolsScenarioFifty PercentSeventy PercentStatus Quo Enrollment Ranges by ES Enrollment Ranges by ESEnrollment Range260-309310-359360-449450 plus Enrollment Ranges by K8 Enrollment Ranges by K8Enrollment Range400-449450-499 Enrollment Ranges by Middle School Enrollment Ranges by Middle SchoolEnrollment Range450-499500-549550+ 
School 2027 2028 2029 2030 2031
Astor423421456439431Beach00000Boise-Eliot/Humboldt520540533533512Cesar Chavez541532525528527Chief Joseph420426424421417Dr Martin Luther King Jr376395389386383Faubion425423414416407George604637669649636Harriet Tubman608546492465455James John00000Jefferson57081298811651190Ockley Green552486497490507Peninsula00000Roosevelt13371301125112561205Rosa Parks481487479471472Sabin00000Sitton464459465455449Vernon325322320318323Woodlawn304320303296294
Total79508107820582888208
School Note
AstorThe Astor attendance boundary expands to include the Bybee Lake Shelter area.BeachBeach closes. The Spanish immersion program from Beach transitions to Chavez K–5, and the boundary of Beach is now included in the Chief Joseph boundary.Boise-Eliot/HumboldtMLK Jr Mandarin Immersion joins BEH.Cesar ChavezChavez expands into a dedicated school-wide K–5 Spanish DLI campus. Neighborhood K–5 students move to Rosa Parks, while middle grade neighborhood and Spanish immersion students move to George. K–5 Spanish immersion programs from Sitton, James John, and Beach consolidate at Chavez.Dr Martin Luther King JrMLK Jr.'s boundary expands to include Sabin, while Mandarin DLI moves to Boise-Eliot/Humboldt.FaubionMiddle grade students move to Ockley Green. The Faubion boundary changes, and the Bybee Lake Shelter area moves to Astor.GeorgeGeorge Middle School receives Spanish DLI programs from Chavez and Ockley Green, with its boundary expanding to include the Chavez and Peninsula neighborhoods.Harriet TubmanHarriet Tubman’s boundary expands to include Vernon, while losing the Irvington neighborhood boundary.James JohnJames John closes. Spanish DLI moves to Chavez, and the neighborhood boundary moves to Sitton.JeffersonHigh school aged students in the Bybee Lake Shelter area move from Jefferson to Roosevelt High School.Ockley GreenOckley Green’s boundary expands to include Faubion and loses the Peninsula area. Spanish DLI moves from Ockley Green to George.PeninsulaPeninsula closes and students move to Rosa Parks.RooseveltThe Roosevelt High School boundary expands to include Skyline K–8.Rosa ParksRosa Parks expands its boundary to include all of Peninsula and Cesar Chavez neighborhood zones.SabinSabin closes and students move to MLK Jr K–5.SittonSpanish immersion at Sitton moves to Chavez Spanish immersion, and the Sitton boundary expands to include the James John boundary.VernonMiddle grade students move to Tubman Middle School, while K–5 students remain at Vernon and its boundary expands to include Sabin.
-+ 77% Microsoft Power BI10of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 77%Page 10 of 13 Next Page Button Pressed Enter or Space
```

## Page 11

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p11.png`

```text
Page navigation Click to return to the District Overall Page Region All Grade_Band_Filter ESHSK8MS 
 Scenario Number of Schools Closed % Sustainable Schools 31-32 % of Students in Sustainable Schools 31-32 % DC Students in Sustainable Schools 31-32 % Underserved Race in Sustainable Schools 31-32 % Students with IEP in Sustainable Schools 31-32 % MLL in Sustainable Schools 31-32
 Status Quo026%48%42%46%41%44% Scenario B1159%74%76%79%71%84% Scenario A1467%80%81%83%77%87%
 Who ends up in Sustainable Schools? Who ends up in Sustainable Schools?OverallUnderserved RaceStudents with IEPStudents Experiencing PovertyNumber of Schools Closed-+ 102% Microsoft Power BI11of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 102%Page 11 of 13 Next Page Button Pressed Enter or Space
```

## Page 12

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p12.png`

```text
Version Control Page Initial Launch Version 1.0. Last updated October 14th, 2026.Version 1.1 Added Grade and Program Level Data - October 15, 2026 District Overall K-5 OverallK-8 Overall6-8 Overall9-12 Overall Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers-+ 125% Microsoft Power BI12of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 125%Page 12 of 13 Next Page Button Pressed Enter or Space
```

## Page 13

Screenshot: `build/pps-texts/pps-rightsizing-dashboard-2026-10-15/p13.png`

```text
Grade Level Impacts and Projections School Year 2027-2028 Program All School All School Type All Grade Level Impacts & ProjectionsThis tool illustrates grade-level enrollment projections under evaluated Rightsizing scenarios across PPS schools.Important Note on Projections: All data shown originates from enrollment projections produced by PSU’s Population Research Center. Because these figures are future projections modeled under proposed scenarios, they are estimates and may not match live or historical enrollment figures shown in other district reports.How to Use: Click the + symbol next to any Scenario name to expand and view enrollment projections broken down by specific program type within that school. District Overall 
School Name KG 1 2 3 4 5 6 7 8 Total
Abernethy          Scenario A646362575157   354Scenario B646362575157   354Status Quo424243403540   242Access Academy          Scenario A  20404445515357310Scenario B  20404445515357310Status Quo  20404445515357310Ainsworth          Scenario A8893819411386   555Scenario B8893819411386   555Status Quo8893819411386   555Alameda          Scenario A808189838283   498Scenario B808189838283   498Status Quo808189838283   498Arleta          Scenario A413742294035   224Scenario B413742294035   224Status Quo373540293735   213Astor
 K-5 OverallK-8 Overall6-8 Overall9-12 Overall Grant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ Roosevelt Web URL Link to School One Pagers-+ 125% Microsoft Power BI13of13Welcome PageDistrict OverallK-5 OverallK-8 Overall6-8 Overall9-12 OverallGrant/ McDanielCleveland/ FranklinWells/ LincolnJefferson/ RooseveltRegional KPIsVersion ControlGrade and Program Level
Report Zoomed To 125%Page 13 of 13 Next Page Button Pressed Enter or Space
```
