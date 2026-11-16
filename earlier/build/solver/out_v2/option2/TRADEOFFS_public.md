# Boundary changes, same closures: trade-offs

**Basis.** Our model (v2) on PSU's per-school forecast (PSU July 2026, Table 5.5) [inferred: our model on PPS/PSU numbers, not PPS figures]. "At target" = a school between its minimum (360 K-5; 500 K-8 and 6-8; 1,100 9-12) and its building capacity (PPS 2025-26 school profiles). Required years are 2027-28 to 2031-32, PPS's projection window (PPS Family Guide p. 1: "Estimates cover 2027-28 through 2031-32"); 2032-33 to 2035-36 are reported only (last year of PSU Table 5.5). Comparisons are with PPS Scenario A ("PPS A").

**What this plan is.** PPS A's closures, programs and high-school lines. Elementary and middle-school lines are redrawn for the shortest walks that keep every school in range and at least PPS A's at-target count every year 2027-28 to 2031-32. Two of PPS A's immersion moves are avoided: MLK Jr Mandarin stays at MLK Jr (PPS A moves it to Boise-Eliot/Humboldt) and Beaumont Spanish 6-8 stays at Beaumont (PPS A moves it to Roseway Heights). Two are kept because they're needed: without them Lent would have 274 kids and Rigler 321, both below 360. This spares 341 immersion students a program move in 2031-32 (about 326 counting only families PPS's own projections imply would have followed; inferred from the PPS Family Guide, not stated by PPS). 1,226 program students still move (PPS A 1,567).

**Lines.** The elementary lines come from a longer re-solve that keeps Sunnyside's and Abernethy's areas entirely south of I-84. They were not put through the line cleanup: a cleanup re-solve made them worse (one more school short of its minimum, more kids sent past a closer school), so they have more one-block notches than the earlier lines (147 vs 100). Line counts: `out_v2/LINES_QA.md`.

## Schools at target, year by year

`*` = required year. "PPS figures" = PPS's own enrollment estimates (Family Guide p. 4, guides dated 2026-10-08), counted with the same targets; PPS publishes none past 2031-32. "Our model" = PPS A's lines scored the same way as this plan. High-school lines are PPS A's in every plan, so a 9-12 difference between the two PPS A rows comes from the estimates, not the lines.

| Level | Plan | 27-28* | 28-29* | 29-30* | 30-31* | 31-32* | 32-33 | 33-34 | 34-35 | 35-36 | All required years | All years to 2035-36 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K-5 (35) | PPS A, PPS figures | 20 | 21 | 23 | 23 | 22 | — | — | — | — | 18 | — |
|  | PPS A, our model | 23 | 23 | 22 | 22 | 21 | 21 | 20 | 19 | 18 | 21 | 17 |
|  | Boundary changes, same closures | 35 | 35 | 35 | 35 | 35 | 21 | 19 | 15 | 13 | 35 | 13 |
| 6-8 (13) | PPS A, PPS figures | 11 | 10 | 9 | 7 | 7 | — | — | — | — | 5 | — |
|  | PPS A, our model | 10 | 9 | 9 | 7 | 7 | 7 | 7 | 8 | 8 | 5 | 5 |
|  | Boundary changes, same closures | 12 | 12 | 13 | 13 | 13 | 10 | 12 | 13 | 13 | 12 | 9 |
| 9-12 (8) | PPS A, PPS figures | 6 | 7 | 7 | 8 | 8 | — | — | — | — | 6 | — |
|  | PPS A, our model | 5 | 7 | 7 | 8 | 8 | 8 | 8 | 7 | 7 | 5 | 4 |
|  | Boundary changes, same closures | 5 | 7 | 7 | 8 | 8 | 8 | 8 | 7 | 7 | 5 | 4 |

- Boundary changes, same closures: meets or beats PPS A (our model) in every required year at every level.

## Walking, moves and feeders (2031-32 basis)

| Level | Measure | PPS A | Boundary changes, same closures |
|---|---|---|---|
| K-5 | Avg walk (mi) | 0.975 | 0.927 |
|  | % within 1 mi | 62.7 | 67.6 |
|  | Assigned to a farther school, past a closer one | 1,970 | 932 |
|  | Over the bus line | 4,703 | 4,117 |
|  | Kids reassigned vs PPS Status Quo | 2,935 | 4,867 |
|  | Non-exempt schools in range, 2031-32 | 25 | 39 |
|  | Segregation (dissimilarity) index | 0.204 | 0.213 |
| 6-8 | Avg walk (mi) | 1.758 | 1.739 |
|  | % within 1 mi | 30.3 | 27.6 |
|  | Assigned to a farther school, past a closer one | 1,259 | 1,233 |
|  | Over the bus line | 2,731 | 2,938 |
|  | Kids reassigned vs PPS Status Quo | 1,972 | 2,274 |
|  | Non-exempt schools in range, 2031-32 | 7 | 13 |
|  | Segregation (dissimilarity) index | 0.181 | 0.164 |
| 9-12 | Avg walk (mi) | 1.933 | 1.933 |
|  | % within 1 mi | 23.4 | 23.4 |
|  | Assigned to a farther school, past a closer one | 751 | 751 |
|  | Over the bus line | 4,936 | 4,936 |
|  | Kids reassigned vs PPS Status Quo | 388 | 388 |
|  | Non-exempt schools in range, 2031-32 | 8 | 8 |
|  | Segregation (dissimilarity) index | 0.180 | 0.180 |
| 9-12 | High schoolers reassigned vs PPS A | 0 | 0 |
| 9-12 | HS range, 2031-32 (largest − smallest; KPI < 350) | 362 | 362 |
| 6-8 | K-5 zones split between middle schools (ES→MS splits) | 1 | 13 |
| 9-12 | Middle zones feeding one high school (%) | 80% (12 of 15) | 40% (6 of 15) |

Bus line = 1 mi K-5, 1.5 mi 6-8/9-12 (ORS 327.043 / PPS). Assigned to a farther school, past a closer one = 0.25 mi margin, no new I-84/river crossing. Kids = neighborhood-program kids on the 2031-32 basis.

**Split feeders in this plan** (a destination counts at ≥5% and ≥5 kids):

- Middle → high: Beaumont → Grant 398, Jefferson 404, McDaniel 65; Gray → Ida B. Wells 594, Lincoln 273; Harrison Park → Franklin 197, McDaniel 342; Hosford → Cleveland 581, Grant 238; Lane → Cleveland 414, Franklin 429; Mt Tabor → Cleveland 103, Franklin 269; Ockley Green → Jefferson 433, Roosevelt 194; Roseway Heights → Grant 49, McDaniel 478; Tubman → Grant 582, Jefferson 324
- Elementary → middle: Alameda → Beaumont 161, Tubman 27; Arleta → Kellogg 119, Lane 27; Atkinson → Kellogg 119, Mt Tabor 45; Bridger → Harrison Park 44, Kellogg 22; Glencoe → Harrison Park 18, Hosford 18, Mt Tabor 147; Grout → Hosford 37, Kellogg 16, Lane 86, Mt Tabor 9; Hayhurst → Gray 41, Jackson 103; Kelly → Harrison Park 74, Kellogg 21, Lane 91; Lee → Roseway Heights 176, Tubman 10; MLK Jr → Ockley Green 56, Tubman 42; Rosa Parks → George 92, Ockley Green 99; Scott → Beaumont 17, Roseway Heights 233; Sunnyside → Hosford 66, Mt Tabor 94
- Elementary → high (high-school-age kids): Ainsworth → Lincoln 220, Ida B. Wells 5; Alameda → Grant 448, Jefferson 44; Arleta → Franklin 182, Cleveland 12; Beverly Cleary → Grant 479, McDaniel 26; Boise-Eliot/Humboldt → Jefferson 223, Grant 67; Bridlemile → Ida B. Wells 218, Lincoln 51; Chief Joseph → Jefferson 125, Roosevelt 68; Clark → McDaniel 232, Franklin 17; Faubion → Jefferson 142, McDaniel 37; Glencoe → Franklin 207, McDaniel 40; Grout → Cleveland 216, Franklin 30; Laurelhurst → Grant 238, Cleveland 31; Rieke → Ida B. Wells 291, Lincoln 10; Scott → McDaniel 316, Grant 35, Jefferson 7; Sunnyside → Cleveland 173, Franklin 22; Woodstock → Cleveland 74, Franklin 14

## 2031-32 size problems by school

| Plan | Schools outside their range in 2031-32 (kids short of floor / over capacity) |
|---|---|
| PPS A | Lee −106, Forest Park −102, Clark −98, Jackson −91, Grout −80, Sunnyside −80, Tubman −77, Vernon −72, Woodlawn −68, Bridger −67, Lane −52, Laurelhurst −37, Beaumont −36, Glencoe −33, Gray −28, Chapman −24, Abernethy −5, George +50 over capacity, Sitton +14 over capacity, Whitman +45 over capacity |
| Boundary changes, same closures | none |

Focus options are not counted. Program-only buildings (no neighborhood area) are sized by program placement, not lines.

Plain-language summary of every plan: `out_v2/BRIEFS.md`.
