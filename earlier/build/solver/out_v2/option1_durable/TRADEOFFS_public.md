# Redrawn K-8 lines: trade-offs

**Basis.** Our model (v2) on PSU's per-school forecast (PSU July 2026, Table 5.5) [inferred: our model on PPS/PSU numbers, not PPS figures]. "At target" = a school between its minimum (360 K-5; 500 K-8 and 6-8; 1,100 9-12) and its building capacity (PPS 2025-26 school profiles). Required years are 2027-28 to 2031-32, PPS's projection window (PPS Family Guide p. 1: "Estimates cover 2027-28 through 2031-32"); 2032-33 to 2035-36 are reported only (last year of PSU Table 5.5). Comparisons are with PPS Scenario A ("PPS A").

**What this plan is.** PPS A's closures, programs (every immersion move kept) and high-school lines. Elementary and middle-school lines are redrawn for the shortest walks that keep every school in range and at least PPS A's at-target count every year 2027-28 to 2031-32.

**Line cleanup.** After the solve, the elementary lines were cleaned: re-solved with a higher cost on boundary length and on passing a closer school, then one-block notches moved to the school around them and small detached pieces swapped back, only where no school gets further outside its range in any year. Every rule still holds. Before/after line counts: `out_v2/LINES_QA.md`.

## Schools at target, year by year

`*` = required year. "PPS figures" = PPS's own enrollment estimates (Family Guide p. 4, guides dated 2026-10-08), counted with the same targets; PPS publishes none past 2031-32. "Our model" = PPS A's lines scored the same way as this plan. High-school lines are PPS A's in every plan, so a 9-12 difference between the two PPS A rows comes from the estimates, not the lines.

| Level | Plan | 27-28* | 28-29* | 29-30* | 30-31* | 31-32* | 32-33 | 33-34 | 34-35 | 35-36 | All required years | All years to 2035-36 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K-5 (35) | PPS A, PPS figures | 20 | 21 | 23 | 23 | 22 | — | — | — | — | 18 | — |
|  | PPS A, our model | 23 | 23 | 22 | 22 | 21 | 21 | 20 | 19 | 18 | 21 | 17 |
|  | Redrawn K-8 lines | 35 | 35 | 35 | 35 | 35 | 25 | 20 | 15 | 13 | 35 | 13 |
| 6-8 (13) | PPS A, PPS figures | 11 | 10 | 9 | 7 | 7 | — | — | — | — | 5 | — |
|  | PPS A, our model | 10 | 9 | 9 | 7 | 7 | 7 | 7 | 8 | 8 | 5 | 5 |
|  | Redrawn K-8 lines | 13 | 12 | 13 | 13 | 13 | 10 | 12 | 13 | 13 | 12 | 9 |
| 9-12 (8) | PPS A, PPS figures | 6 | 7 | 7 | 8 | 8 | — | — | — | — | 6 | — |
|  | PPS A, our model | 5 | 7 | 7 | 8 | 8 | 8 | 8 | 7 | 7 | 5 | 4 |
|  | Redrawn K-8 lines | 5 | 7 | 7 | 8 | 8 | 8 | 8 | 7 | 7 | 5 | 4 |

- Redrawn K-8 lines: meets or beats PPS A (our model) in every required year at every level.

## Walking, moves and feeders (2031-32 basis)

| Level | Measure | PPS A | Redrawn K-8 lines |
|---|---|---|---|
| K-5 | Avg walk (mi) | 0.975 | 0.947 |
|  | % within 1 mi | 62.7 | 65.7 |
|  | Assigned to a farther school, past a closer one | 1,970 | 1,285 |
|  | Over the bus line | 4,703 | 4,366 |
|  | Kids reassigned vs PPS Status Quo | 2,935 | 4,914 |
|  | Non-exempt schools in range, 2031-32 | 25 | 39 |
|  | Segregation (dissimilarity) index | 0.204 | 0.211 |
| 6-8 | Avg walk (mi) | 1.758 | 1.667 |
|  | % within 1 mi | 30.3 | 30.1 |
|  | Assigned to a farther school, past a closer one | 1,259 | 882 |
|  | Over the bus line | 2,731 | 2,661 |
|  | Kids reassigned vs PPS Status Quo | 1,972 | 2,435 |
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
| 6-8 | K-5 zones split between middle schools (ES→MS splits) | 1 | 17 |
| 9-12 | Middle zones feeding one high school (%) | 80% (12 of 15) | 47% (7 of 15) |

Bus line = 1 mi K-5, 1.5 mi 6-8/9-12 (ORS 327.043 / PPS). Assigned to a farther school, past a closer one = 0.25 mi margin, no new I-84/river crossing. Kids = neighborhood-program kids on the 2031-32 basis.

**Split feeders in this plan** (a destination counts at ≥5% and ≥5 kids):

- Middle → high: Beaumont → Grant 479, Jefferson 351, McDaniel 191; Gray → Ida B. Wells 583, Lincoln 302; Harrison Park → Franklin 311, McDaniel 209; Hosford → Cleveland 576, Franklin 118, Grant 66; Lane → Cleveland 529, Franklin 236; Mt Tabor → Franklin 280, Grant 171, McDaniel 142; Ockley Green → Jefferson 341, Roosevelt 213; Tubman → Grant 550, Jefferson 477
- Elementary → middle: Alameda → Beaumont 107, Tubman 68; Arleta → Harrison Park 10, Kellogg 123, Lane 13; Astor → Astor 131, George 9; Atkinson → Hosford 35, Kellogg 114; Beverly Cleary → Beaumont 80, Tubman 168; Bridlemile → Gray 136, West Sylvan 18; Capitol Hill → Gray 11, Jackson 152; Chapman → Gray 17, West Sylvan 189; Chief Joseph → Ockley Green 168, Tubman 13; Glencoe → Hosford 18, Mt Tabor 164; Grout → Hosford 127, Lane 22; Hayhurst → Gray 24, Jackson 124; Laurelhurst → Hosford 52, Mt Tabor 170; MLK Jr → Ockley Green 15, Tubman 111; Rosa Parks → George 85, Ockley Green 113; Scott → Beaumont 105, Roseway Heights 142; Whitman → Kellogg 30, Lane 126
- Elementary → high (high-school-age kids): Ainsworth → Lincoln 222, Ida B. Wells 35; Alameda → Grant 406, Jefferson 43; Arleta → Franklin 174, Cleveland 18; Atkinson → Franklin 188, Cleveland 6; Beverly Cleary → Grant 448, McDaniel 41, Cleveland 17; Boise-Eliot/Humboldt → Jefferson 188, Grant 23; Bridlemile → Ida B. Wells 225, Lincoln 48; Chief Joseph → Jefferson 143, Roosevelt 56; Clark → McDaniel 205, Franklin 47; Faubion → Jefferson 139, McDaniel 35; Glencoe → Franklin 182, McDaniel 62; Grout → Cleveland 233, Franklin 13; Laurelhurst → Grant 223, Franklin 24; MLK Jr → Jefferson 246, Grant 48; Rieke → Ida B. Wells 261, Lincoln 7; Scott → McDaniel 310, Grant 70; Sunnyside → Cleveland 133, Franklin 35, Grant 13; Vernon → Jefferson 217, Grant 33; Woodstock → Cleveland 79, Franklin 14

## 2031-32 size problems by school

| Plan | Schools outside their range in 2031-32 (kids short of floor / over capacity) |
|---|---|
| PPS A | Lee −106, Forest Park −102, Clark −98, Jackson −91, Grout −80, Sunnyside −80, Tubman −77, Vernon −72, Woodlawn −68, Bridger −67, Lane −52, Laurelhurst −37, Beaumont −36, Glencoe −33, Gray −28, Chapman −24, Abernethy −5, George +50 over capacity, Sitton +14 over capacity, Whitman +45 over capacity |
| Redrawn K-8 lines | none |

Focus options are not counted. Program-only buildings (no neighborhood area) are sized by program placement, not lines.

Plain-language summary of every plan: `out_v2/BRIEFS.md`.
