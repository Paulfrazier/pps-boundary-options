# Definitions

> Independent, best-effort analysis by a PPS parent, not an official PPS product. Confirm anything that matters against PPS's own materials.

What every number in this project means. The code that computes each one is named so you can check it.

## Who is counted

- **Neighborhood kids.** Children who live in an area and attend its neighborhood program, estimated per 2020 Census block. Block counts are split into grade bands (K-5, 6-8, 9-12) by age and calibrated so today's attendance areas reproduce 2025-26 neighborhood enrollment (ODE fall membership, PSU's neighborhood vs. DLI split). They are estimates, not student addresses. See `build/data/README.md` and `build/data/backtest.md`.
- **Program students.** Dual Language Immersion (DLI) and focus-option students. They are counted at the building that hosts their program, not by where they live, and move with the program. Lent and Rigler's areas are whole-school Spanish DLI today, so their kids follow the program. Under PPS A and B, César Chávez has no neighborhood area; its neighborhood K-5 kids go to Rosa Parks (PPS Family Guides, p. 3).
- **Basis year.** The optimizer and its scorecards size everything on **PSU's 2031-32 forecast**, as PPS does. Each school area is scaled by PSU's own ratio for that area. The first map pages use the earlier model on a roughly 2025-26 basis (see "Two model versions" below).

## Distance

- **Walk distance.** The shortest walking route on OpenStreetMap streets and paths, from each Census block's center to the school, computed with OSRM's foot profile. Freeways, rail and the river are crossed only at real bridges and overpasses. Bike distance uses OSRM's bicycle profile.
- **Average walk.** Walk distance averaged over every kid at that level, weighted by kids per block.
- **Within ½ / 1 / 1½ / 2 miles.** Share of kids whose assigned school is that close on foot (the map also shows 2 miles at every level).
- **Past busing distance.** Kids whose walk is over the distance at which Oregon law (ORS 327.043) and PPS's transportation guidelines provide a bus: more than 1 mile for K-5, more than 1.5 miles for 6-8 and 9-12. For high school we ignore PPS's extra TriMet-stop test, so this overstates yellow-bus riders there. The trade-offs table's "past the bus line" rows use this count for K-5 and 6-8 (`levels.<level>.kids_over_bus_threshold` in each scorecard).

## Kids assigned to a farther school, past a closer one

A kid counts if their assigned school is **at least 0.25 miles farther on foot than the nearest open school at their level**. The quarter-mile margin keeps near-ties from counting.

**One figure to quote.** The site's figure is the current optimizer's scorecard value: `levels.K-5.kids_past_closer_school` in each plan's `build/solver/out_v2/<plan>/scorecard.json` (model v2, 2031-32 basis, 0.25 mile margin). PPS A = **1,970** kids at K-5 (PPS Status Quo 1,861; PPS B 2,144; Redrawn K-8 lines 1,285; Boundary changes, balanced middle schools (the best example we modeled) and Boundary changes, same closures 932 each; Rebalanced PPS A 1,838; the what-if Close 2 focus options 1,001). Model v1 gave PPS A 1,997. Any other number you see for the same idea, such as 2,575 for PPS A, comes from the earlier model and is labeled as such where it appears (the archive pages and older letters).

Both model versions use the same rule. They differ in:

| | Earlier model (first map pages, letters) | Current optimizer (scorecards) |
|---|---|---|
| Kids counted | Earlier K-5 estimate, about 14,900, roughly 2025-26 | Recalibrated K-5 neighborhood kids, 2031-32 basis (fewer kids) |
| Walk distances | Public OSRM router, nearby schools only; straight line × 1.4 otherwise | Local OSRM, every block to every school |
| Which schools count as "closer" | Any open school | Open schools reachable without a new I-84 or Willamette crossing |
| PPS A (official lines) | 2,575 | 1,970 |

So the two PPS A figures measure the same idea on different populations and distance data; they should not be compared with each other or mixed in one table. Use the scorecard figure (1,970) for comparing options, and label anything else "earlier model".

## School size

- **Size target (floor).** PPS's thresholds: K-5 more than 360, K-8 and 6-8 more than 500, 9-12 more than 1,100 (PPS scenario documents; our model counts a school exactly at the threshold as at target, which changes no counts; 360 and 500 trace to the state's Quality Education Model). Astor and Skyline, which PPS keeps as small K-8s in every scenario, are exempt in our model; PPS's Family Guides still list a more-than-500 goal for both.
- **Ceiling.** The building's functional capacity (PPS School Profiles 2025-26, captured second-hand; Jefferson 1,773 after modernization; the earlier model used the 2021 Long-Range Facility Plan). PPS publishes no upper size target.
- **At target.** A school's total (neighborhood kids plus program students it hosts) is at or above its floor and at or below its ceiling.
- **Utilization.** Total students ÷ functional capacity. PPS's family guides state an aim of 70-100%.

## Durability

- **Schools at target, year by year.** Each school's size in each year from 2027-28 to 2035-36, following its own row in PSU's July 2026 forecast (Table 5.5), checked against its floor and capacity. 2027-28 to 2031-32 is the **required window** (PPS's own projection years, Family Guide p. 1); 2032-33 to 2035-36 are **reported only**. Nothing past 2035-36 is projected. It is a projection, not a forecast: boundaries are held fixed. (The earlier model v1 used one district-wide ratio to 2040-41.)
- **Durable option (design goal).** At every level and in every year 2027-28 to 2031-32, at least as many schools at target as PPS A.

## Disruption

- **Baseline.** PPS Status Quo: PPS's own 2027-28 map with no closures, which keeps every school open. Every plan is compared with it. (Today's 2025-26 lines were archived on 2026-10-12; they differ from the baseline mainly at 9-12, where the Jefferson dual assignment ends.)
- **Kids reassigned.** Kids whose assigned school differs from PPS Status Quo (2027-28, no closures).
- **DLI kids moved.** Program students whose program changes building, split into "building closes" and "program moves."
- **Split feeder.** An elementary zone sending kids to more than one middle school (or a middle zone to more than one high school), counting a destination only if it gets at least 5% and at least 5 kids.

## Diversity

- **Kids of color share.** Kids of color = Census 2020 under-18 population minus under-18 white alone, not Hispanic or Latino (tables P2 minus P4), by block (`pps-race.csv`), applied to that block's neighborhood kids. Latino children of any race count as kids of color. District average: about 42.5% at K-5 (42.8% at 6-8, 42.6% at 9-12). On the map, **Color by racial mix** fills each school's area by this share compared with the district: blue is lower, orange is higher, darkest at 25 points or more away. It counts where kids live (2020 Census residents), not who is enrolled.
- **Segregation (dissimilarity) index.** Half the sum, over schools, of the absolute difference between each school's share of all kids of color and its share of all white kids. 0 means every school matches the district mix; 1 means complete separation.
- **Within 15 points.** Schools whose kids-of-color share is within 15 percentage points of the district average.

## PPS plan lines

- **PPS A / PPS B (PPS's Scenarios A and B, official map).** Lines traced from PPS's published 2027-28 attendance-area map PDFs (BoardBook), median error about 70 feet, assigned to Census blocks. The first map pages originally used a reconstruction (closing areas merged into receivers, split schools drawn halfway); that version is superseded.

## Two model versions

- **Earlier model** (first map pages, walk tables, the "diversity challenge" figures and the first letters): K-5 only, 2020 Census blocks calibrated to 2024-25 school totals, public OSRM distances.
- **Current model** (optimizer, scorecards, dashboard, compare map v2 statistics for PPS plans): all three levels, recalibrated to 2025-26 neighborhood enrollment, PSU 2031-32 basis, local OSRM distances, official traced PPS lines.

Numbers from the two versions are not directly comparable.

## Plan names

Plans were renamed on 2026-10-12 so names say what each plan does (the best example we modeled again on 2026-10-14). If you have an older figure, this is what it was called. Plans marked * are not on the site now (archived, dropped, paused or awaiting a decision); their names are listed so older figures can be traced.

| Plan | Earlier names |
|---|---|
| Today (2025-26 lines), archived 2026-10-12 * | Today |
| PPS Status Quo (2027-28, no closures) | PPS 2027-28 lines, no closures; PPS 2027-28, no closures; No changes (PPS Status Quo, 2027-28); No changes (PPS); Status Quo 2027-28; Status Quo |
| PPS A (PPS Scenario A) | PPS Scenario A; PPS plan A |
| PPS B (PPS Scenario B) | PPS Scenario B; PPS plan B |
| Shortest walks (at least PPS A's count of schools at target every year), dropped 2026-10-15 * | Shortest walks, A's count every year; Shortest walks that still last |
| Balanced: 19 at target every year * | Balanced: 19 schools last to 2040-41 |
| Balanced: 21 at target every year * | Balanced: 21 schools last to 2040-41 |
| Redrawn K-8 lines (PPS A's closures with K-5 and middle-school lines redrawn for walking; PPS high schools) | Redrawn walkable K-8 lines, PPS high schools (full name until 2026-10-14); Redrawn K-8, PPS HS (short name until 2026-10-14); Most schools at target, every year; Most schools that last to 2040-41; Option 1-durable; Option 1 (durable); Option 1 |
| Most at target, HS lines adjusted * | Most schools that last, HS lines adjusted |
| Most at target + small feeder fixes * | Most schools last + small feeder fixes |
| Most at target + medium feeder fixes * | Most schools last + medium feeder fixes |
| Most at target + large feeder fixes * | Most schools last + large feeder fixes |
| Boundary changes, balanced middle schools (the best example we modeled: PPS A's closures with redrawn K-5 and middle-school lines, middle-school minimum 460; MLK Jr Mandarin and Beaumont Spanish 6-8 stay in their buildings) | Boundary changes, smaller middle schools; Smaller middle schools |
| Boundary changes, same closures (the same elementary lines, middle-school minimum 500) | Same closures, better lines (until 2026-10-14); Redrawn K-8, MLK Jr + Beaumont DLI stay; Redrawn K-8, 2 DLI stay; Immersion programs stay put; Immersion stays put; Option 2 |
| Close 2 focus options (Winterhaven, da Vinci), a what-if | Option 3a; Focus schools meet the size rule |
| Close 2 focus options, 1 more school open * | Option 3b; Focus schools sized, one more school open |
| Rebalanced PPS A | Rebalanced PPS A: every school in range (until 2026-10-15); Fewest moves, every school in range (until 2026-10-14); Fewest moves; Fewest moves, in range; Fewest kids moved; Option 4; "fewest moves" |
| Solver picks closures, built to last * | Option 5 |
| Shortest walks, sized for 2031-32 only * | Option 1 (2031-only); Option 1 |

The first-generation pages (no longer on the site; their files stay in the repo) used "Walk redraw A/B" and "Walk + diversity A" on an earlier model; those are not the same plans.


*Built with AI: the research, data work, modeling and writing were done by AI (Claude, from Anthropic), directed and guided by Paul Frazier, a PPS parent. Best effort; it will have errors.*
