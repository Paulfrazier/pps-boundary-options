# Boundary changes, balanced middle schools: trade-offs

**Basis.** Our model (v2) on PSU's per-school forecast (PSU July 2026, Table 5.5) [inferred: our model on PPS/PSU numbers, not PPS figures]. "At target" = a school between its minimum (360 K-5; 500 K-8 and 6-8; 1,100 9-12) and its building capacity (PPS 2025-26 school profiles). Required years are 2027-28 to 2031-32, PPS's projection window (PPS Family Guide p. 1: "Estimates cover 2027-28 through 2031-32"); 2032-33 to 2035-36 are reported only (last year of PSU Table 5.5). Comparisons are with PPS Scenario A ("PPS A").

**What this plan is.** The same closures, immersion programs and elementary lines as Boundary changes, same closures. Middle school differs: the minimum middle-school size is lowered from 500 (PPS's goal) to 460 so fewer elementary schools are split between middle schools (3 instead of 13) and no middle school is over capacity. At PPS's 500 minimum, 9 of 13 middle schools are at target every year; at 460, all 13. High school differs too, by one change to PPS A's lines (Boundary changes, same closures keeps them unchanged): the Skyline area (about 93 high-school students in 2031-32) stays at Lincoln, as today, instead of crossing the St. Johns Bridge to Roosevelt. Lincoln has room (1,407 students for 1,984 seats in 2031-32) and Roosevelt stays above its 1,100 minimum every year 2027-28 to 2031-32 (1,119 in 2031-32). It also ends Roosevelt's 2027-28 crowding (1,421 students for 1,395 seats without the change). The costs: Roosevelt falls below 1,100 from 2032-33 (1,075, then 1,027 by 2035-36, years reported but not required); the gap between the largest and smallest high school in 2031-32 grows from 362 to 424 students; and the average high-school walk rises from 1.93 to 1.98 miles, since Roosevelt is the closer school by road for the Skyline area. All figures: our model (v2) on PSU July 2026 Table 5.5; seats from PPS 2025-26 school profiles.

**Lines.** The elementary lines come from a longer re-solve that keeps Sunnyside's and Abernethy's areas entirely south of I-84. They were not put through the line cleanup: a cleanup re-solve made them worse (one more school short of its minimum, more kids sent past a closer school), so they have more one-block notches than the earlier lines (147 vs 100). Line counts: `out_v2/LINES_QA.md`.

**Middle-school minimum.** This plan uses 460, not 500, as the middle-school minimum, so its middle-school "at target" counts below use 460. Four middle schools dip below 500 in their low year: Harrison Park 461 (2030-31), Ockley Green 461 (2028-29), West Sylvan 460 (2031-32) and George 498 (2031-32). At 500, 9 of 13 are at target every year 2027-28 to 2031-32. West Sylvan falls to 443 in 2032-33, a year PPS doesn't project.

## Schools at target, year by year

`*` = required year. "PPS figures" = PPS's own enrollment estimates (Family Guide p. 4, guides dated 2026-10-08), counted with the same targets; PPS publishes none past 2031-32. "Our model" = PPS A's lines scored the same way as this plan. High-school lines are PPS A's in every plan, so a 9-12 difference between the two PPS A rows comes from the estimates, not the lines.

| Level | Plan | 27-28* | 28-29* | 29-30* | 30-31* | 31-32* | 32-33 | 33-34 | 34-35 | 35-36 | All required years | All years to 2035-36 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K-5 (35) | PPS A, PPS figures | 20 | 21 | 23 | 23 | 22 | — | — | — | — | 18 | — |
|  | PPS A, our model | 23 | 23 | 22 | 22 | 21 | 21 | 20 | 19 | 18 | 21 | 17 |
|  | Boundary changes, balanced middle schools | 35 | 35 | 35 | 35 | 35 | 21 | 19 | 15 | 13 | 35 | 13 |
| 6-8 (13) | PPS A, PPS figures | 11 | 10 | 9 | 7 | 7 | — | — | — | — | 5 | — |
|  | PPS A, our model | 10 | 9 | 9 | 7 | 7 | 7 | 7 | 8 | 8 | 5 | 5 |
|  | Boundary changes, balanced middle schools | 13 | 13 | 13 | 13 | 13 | 12 | 12 | 13 | 13 | 13 | 12 |
| 9-12 (8) | PPS A, PPS figures | 6 | 7 | 7 | 8 | 8 | — | — | — | — | 6 | — |
|  | PPS A, our model | 5 | 7 | 7 | 8 | 8 | 8 | 8 | 7 | 7 | 5 | 4 |
|  | Boundary changes, balanced middle schools | 6 | 7 | 7 | 8 | 8 | 7 | 7 | 6 | 6 | 6 | 4 |

- Boundary changes, balanced middle schools: meets or beats PPS A (our model) in every required year at every level.

## Walking, moves and feeders (2031-32 basis)

| Level | Measure | PPS A | Boundary changes, balanced middle schools |
|---|---|---|---|
| K-5 | Avg walk (mi) | 0.975 | 0.927 |
|  | % within 1 mi | 62.7 | 67.6 |
|  | Assigned to a farther school, past a closer one | 1,970 | 932 |
|  | Over the bus line | 4,703 | 4,117 |
|  | Kids reassigned vs PPS Status Quo | 2,935 | 4,867 |
|  | Non-exempt schools in range, 2031-32 | 25 | 39 |
|  | Segregation (dissimilarity) index | 0.204 | 0.213 |
| 6-8 | Avg walk (mi) | 1.758 | 1.710 |
|  | % within 1 mi | 30.3 | 28.9 |
|  | Assigned to a farther school, past a closer one | 1,259 | 1,082 |
|  | Over the bus line | 2,731 | 2,779 |
|  | Kids reassigned vs PPS Status Quo | 1,972 | 2,315 |
|  | Non-exempt schools in range, 2031-32 | 7 | 13 |
|  | Segregation (dissimilarity) index | 0.181 | 0.166 |
| 9-12 | Avg walk (mi) | 1.933 | 1.975 |
|  | % within 1 mi | 23.4 | 23.4 |
|  | Assigned to a farther school, past a closer one | 751 | 751 |
|  | Over the bus line | 4,936 | 4,936 |
|  | Kids reassigned vs PPS Status Quo | 388 | 295 |
|  | Non-exempt schools in range, 2031-32 | 8 | 8 |
|  | Segregation (dissimilarity) index | 0.180 | 0.185 |
| 9-12 | High schoolers reassigned vs PPS A | 0 | 93 |
| 9-12 | HS range, 2031-32 (largest − smallest; KPI < 350) | 362 | 424 |
| 6-8 | K-5 zones split between middle schools (ES→MS splits) | 1 | 3 |
| 9-12 | Middle zones feeding one high school (%) | 80% (12 of 15) | 40% (6 of 15) |

Bus line = 1 mi K-5, 1.5 mi 6-8/9-12 (ORS 327.043 / PPS). Assigned to a farther school, past a closer one = 0.25 mi margin, no new I-84/river crossing. Kids = neighborhood-program kids on the 2031-32 basis.

**Split feeders in this plan** (a destination counts at ≥5% and ≥5 kids):

- Middle → high: Beaumont → Grant 448, Jefferson 427; Gray → Ida B. Wells 515, Lincoln 424; Harrison Park → Franklin 108, McDaniel 310; Kellogg → Cleveland 65, Franklin 408; Lane → Cleveland 298, Franklin 545; Mt Tabor → Cleveland 31, Franklin 207, Grant 238, McDaniel 40; Ockley Green → Jefferson 306, Roosevelt 240; Roseway Heights → Grant 35, McDaniel 520; Tubman → Grant 545, Jefferson 430
- Elementary → middle: Chapman → Gray 38, West Sylvan 166; Grout → Hosford 72, Kellogg 54, Lane 24; Rosa Parks → George 72, Ockley Green 121
- Elementary → high (high-school-age kids): Ainsworth → Lincoln 220, Ida B. Wells 5; Alameda → Grant 448, Jefferson 44; Arleta → Franklin 182, Cleveland 12; Beverly Cleary → Grant 479, McDaniel 26; Boise-Eliot/Humboldt → Jefferson 223, Grant 67; Bridlemile → Ida B. Wells 218, Lincoln 51; Chief Joseph → Jefferson 125, Roosevelt 68; Clark → McDaniel 232, Franklin 17; Faubion → Jefferson 142, McDaniel 37; Glencoe → Franklin 207, McDaniel 40; Grout → Cleveland 216, Franklin 30; Laurelhurst → Grant 238, Cleveland 31; Rieke → Ida B. Wells 291, Lincoln 10; Scott → McDaniel 316, Grant 35, Jefferson 7; Sunnyside → Cleveland 173, Franklin 22; Woodstock → Cleveland 74, Franklin 14

## 2031-32 size problems by school

| Plan | Schools outside their range in 2031-32 (kids short of floor / over capacity) |
|---|---|
| PPS A | Lee −106, Forest Park −102, Clark −98, Jackson −91, Grout −80, Sunnyside −80, Tubman −77, Vernon −72, Woodlawn −68, Bridger −67, Lane −52, Laurelhurst −37, Beaumont −36, Glencoe −33, Gray −28, Chapman −24, Abernethy −5, George +50 over capacity, Sitton +14 over capacity, Whitman +45 over capacity |
| Boundary changes, balanced middle schools | none |

Focus options are not counted. Program-only buildings (no neighborhood area) are sized by program placement, not lines.

Plain-language summary of every plan: `out_v2/BRIEFS.md`.
