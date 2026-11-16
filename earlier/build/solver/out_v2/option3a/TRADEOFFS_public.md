# Close 2 focus options (Winterhaven, da Vinci) — a what-if: trade-offs

**Basis.** Our model (v2) on PSU's per-school forecast (PSU July 2026, Table 5.5) [inferred: our model on PPS/PSU numbers, not PPS figures]. "At target" = a school between its minimum (360 K-5; 500 K-8 and 6-8; 1,100 9-12) and its building capacity (PPS 2025-26 school profiles). Required years are 2027-28 to 2031-32, PPS's projection window (PPS Family Guide p. 1: "Estimates cover 2027-28 through 2031-32"); 2032-33 to 2035-36 are reported only (last year of PSU Table 5.5). Comparisons are with PPS Scenario A ("PPS A").

**What this plan is.** PPS A's closures, programs and high-school lines, plus Winterhaven (K-8 STEM) and da Vinci (6-8 arts) close. Their students return to their neighborhood schools by the catchment they live in, from a per-catchment sheet of 2025-26 focus students (second-hand: its first columns match PPS's October 2025 Enrollment Summary, but the per-program columns' source isn't stated). 21 students who live outside PPS aren't returned. It assumes every returning student attends their neighborhood school. Elementary and middle lines are redrawn under the same rules as the redraws.

**Line cleanup.** After the solve, the elementary lines were cleaned: re-solved with a higher cost on boundary length and on passing a closer school, then one-block notches moved to the school around them and small detached pieces swapped back, only where no school gets further outside its range in any year. Every rule still holds. Before/after line counts: `out_v2/LINES_QA.md`.

## Schools at target, year by year

`*` = required year. "PPS figures" = PPS's own enrollment estimates (Family Guide p. 4, guides dated 2026-10-08), counted with the same targets; PPS publishes none past 2031-32. "Our model" = PPS A's lines scored the same way as this plan. High-school lines are PPS A's in every plan, so a 9-12 difference between the two PPS A rows comes from the estimates, not the lines.

| Level | Plan | 27-28* | 28-29* | 29-30* | 30-31* | 31-32* | 32-33 | 33-34 | 34-35 | 35-36 | All required years | All years to 2035-36 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K-5 (35) | PPS A, PPS figures | 20 | 21 | 23 | 23 | 22 | — | — | — | — | 18 | — |
|  | PPS A, our model | 23 | 23 | 22 | 22 | 21 | 21 | 20 | 19 | 18 | 21 | 17 |
|  | Close 2 focus options (Winterhaven, da Vinci) | 35 | 35 | 35 | 35 | 35 | 22 | 22 | 17 | 16 | 35 | 16 |
| 6-8 (13) | PPS A, PPS figures | 11 | 10 | 9 | 7 | 7 | — | — | — | — | 5 | — |
|  | PPS A, our model | 10 | 9 | 9 | 7 | 7 | 7 | 7 | 8 | 8 | 5 | 5 |
|  | Close 2 focus options (Winterhaven, da Vinci) | 13 | 13 | 13 | 13 | 13 | 11 | 12 | 13 | 13 | 13 | 11 |
| 9-12 (8) | PPS A, PPS figures | 6 | 7 | 7 | 8 | 8 | — | — | — | — | 6 | — |
|  | PPS A, our model | 5 | 7 | 7 | 8 | 8 | 8 | 8 | 7 | 7 | 5 | 4 |
|  | Close 2 focus options (Winterhaven, da Vinci) | 5 | 7 | 7 | 8 | 8 | 8 | 8 | 7 | 7 | 5 | 4 |

- Close 2 focus options (Winterhaven, da Vinci): meets or beats PPS A (our model) in every required year at every level.

## Walking, moves and feeders (2031-32 basis)

| Level | Measure | PPS A | Close 2 focus options (Winterhaven, da Vinci) |
|---|---|---|---|
| K-5 | Avg walk (mi) | 0.975 | 0.928 |
|  | % within 1 mi | 62.7 | 67.7 |
|  | Assigned to a farther school, past a closer one | 1,970 | 1,001 |
|  | Over the bus line | 4,703 | 4,156 |
|  | Kids reassigned vs PPS Status Quo | 2,935 | 4,888 |
|  | Non-exempt schools in range, 2031-32 | 25 | 39 |
|  | Segregation (dissimilarity) index | 0.204 | 0.212 |
| 6-8 | Avg walk (mi) | 1.758 | 1.657 |
|  | % within 1 mi | 30.3 | 30.3 |
|  | Assigned to a farther school, past a closer one | 1,259 | 1,044 |
|  | Over the bus line | 2,731 | 2,828 |
|  | Kids reassigned vs PPS Status Quo | 1,972 | 2,637 |
|  | Non-exempt schools in range, 2031-32 | 7 | 13 |
|  | Segregation (dissimilarity) index | 0.181 | 0.186 |
| 9-12 | Avg walk (mi) | 1.933 | 1.933 |
|  | % within 1 mi | 23.4 | 23.4 |
|  | Assigned to a farther school, past a closer one | 751 | 751 |
|  | Over the bus line | 4,936 | 4,936 |
|  | Kids reassigned vs PPS Status Quo | 388 | 388 |
|  | Non-exempt schools in range, 2031-32 | 8 | 8 |
|  | Segregation (dissimilarity) index | 0.180 | 0.180 |
| 9-12 | High schoolers reassigned vs PPS A | 0 | 0 |
| 9-12 | HS range, 2031-32 (largest − smallest; KPI < 350) | 362 | 362 |
| 6-8 | K-5 zones split between middle schools (ES→MS splits) | 1 | 8 |
| 9-12 | Middle zones feeding one high school (%) | 80% (12 of 15) | 33% (5 of 15) |

Bus line = 1 mi K-5, 1.5 mi 6-8/9-12 (ORS 327.043 / PPS). Assigned to a farther school, past a closer one = 0.25 mi margin, no new I-84/river crossing. Kids = neighborhood-program kids on the 2031-32 basis.

**Split feeders in this plan** (a destination counts at ≥5% and ≥5 kids):

- Middle → high: Beaumont → Grant 909, Jefferson 151, McDaniel 104; Gray → Ida B. Wells 567, Lincoln 292; Harrison Park → Franklin 308, McDaniel 266; Hosford → Cleveland 651, Franklin 50; Kellogg → Cleveland 41, Franklin 426; Lane → Cleveland 411, Franklin 305; Mt Tabor → Franklin 204, Grant 234, McDaniel 81; Ockley Green → Jefferson 368, Roosevelt 135; Roseway Heights → Grant 44, McDaniel 479; Tubman → Grant 75, Jefferson 644
- Elementary → middle: Arleta → Harrison Park 12, Kellogg 131, Lane 19; Capitol Hill → Gray 30, Jackson 137; Faubion → Beaumont 100, Ockley Green 75, Tubman 48; Llewellyn → Hosford 53, Lane 129; Rosa Parks → George 145, Ockley Green 75; Vernon → Beaumont 54, Tubman 133; Vestal → Harrison Park 49, Mt Tabor 18; Woodstock → Kellogg 26, Lane 66
- Elementary → high (high-school-age kids): Ainsworth → Lincoln 203, Ida B. Wells 32; Alameda → Grant 458, Jefferson 49; Arleta → Franklin 179, Cleveland 8; Beverly Cleary → Grant 421, McDaniel 46, Cleveland 18; Boise-Eliot/Humboldt → Jefferson 197, Grant 22; Bridlemile → Ida B. Wells 203, Lincoln 67; Chief Joseph → Jefferson 136, Roosevelt 58; Clark → McDaniel 212, Franklin 33; Faubion → Jefferson 137, McDaniel 64; Glencoe → Franklin 179, McDaniel 57; Grout → Cleveland 213, Franklin 21; Laurelhurst → Grant 232, Franklin 18; MLK Jr → Jefferson 231, Grant 53; Rieke → Ida B. Wells 281, Lincoln 11; Scott → McDaniel 276, Grant 49, Jefferson 11; Sunnyside → Cleveland 149, Franklin 28; Vernon → Jefferson 223, Grant 25; Woodstock → Cleveland 112, Franklin 20

## 2031-32 size problems by school

| Plan | Schools outside their range in 2031-32 (kids short of floor / over capacity) |
|---|---|
| PPS A | Lee −106, Forest Park −102, Clark −98, Jackson −91, Grout −80, Sunnyside −80, Tubman −77, Vernon −72, Woodlawn −68, Bridger −67, Lane −52, Laurelhurst −37, Beaumont −36, Glencoe −33, Gray −28, Chapman −24, Abernethy −5, George +50 over capacity, Sitton +14 over capacity, Whitman +45 over capacity |
| Close 2 focus options (Winterhaven, da Vinci) | none |

Focus options are not counted. Program-only buildings (no neighborhood area) are sized by program placement, not lines.

Plain-language summary of every plan: `out_v2/BRIEFS.md`.
