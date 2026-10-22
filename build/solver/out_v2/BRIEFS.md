# Plan briefs (model v2)

Models track, 2026-10-12 (numbers refreshed overnight after the line cleanup), for the site. One brief per plan we propose: how it works, the good, the bad, the trade-offs.

**Basis.** All figures are our model's (v2) on PSU's 2031-32 per-school forecast (PSU July 2026, Table 5.5), from each plan's `scorecard.json`, unless a row says otherwise [inferred: our model on PPS/PSU numbers, not PPS figures]. "At target" = a school between its minimum (360 K-5; 500 K-8 and 6-8; 1,100 9-12) and its building capacity (PPS 2025-26 school profiles). "Every year" = every year 2027-28 to 2031-32, PPS's projection window (PPS Family Guide p. 1). Comparisons are with PPS Scenario A ("PPS A") and PPS Status Quo (2027-28, no closures).

## Why the example plans have shorter walks AND more schools at target

**The real part.**
- **PPS A mostly reassigns whole areas.** It assigns each closing school's area to one or two nearby receivers, with few other line changes (PPS Scenario Release memo, Oct 5, 2026: Maplewood, Stephenson, Buckman and Sellwood are split between two receivers). It doesn't redraw lines across the district to balance sizes, so some receivers end up big and their neighbors small. On our model, 20 K-5 and middle schools are outside their range in 2031-32 under PPS A (`option2/TRADEOFFS.md`). PPS's own projections show the same pattern (Family Guides p. 4, 2031-32): Clark falls from 343 with no changes to 272 under PPS A (88 short of 360), Sunnyside from 475 to 235, and George reaches 636 in a 623-seat building (capacity: PPS 2025-26 school profiles).
- **The two goals point the same way.** Reassigning whole areas also assigns kids to a farther school, past a closer one: 1,970 K-5 kids under PPS A. Sending those kids to the closer school shortens their walk *and* moves them from an over-full receiver to an under-filled neighbor.
- **Size is a rule, not a side effect.** Our solver treats size as a rule and walking as the goal: the one firm rule is at least as many schools at target as PPS A, every year to 2031-32; within that, it minimizes walking. So "more schools at target" comes from redrawing every line to a size rule, not from walkability itself.

**The catch: schools are packed just above the minimum.** To get the most schools at target, the solver holds many of them only just over 360.

| K-5, 2031-32 | PPS A | Redrawn K-8 lines | Boundary changes, same closures |
|---|---:|---:|---:|
| All open K-5 schools in range, on forecast (of 41 open) | 27 | 41 | 41 |
| Within 20 kids of the 360 minimum | 2 of 35 | 22 of 35 | 22 of 35 |
| All open K-5 schools in range if enrollment comes in 9% below forecast | **25** | 16 | 15 |
| If enrollment comes in 9% low: zoned K-5 schools under 360 | 15 | 25 | 26 |
| ... total kids they are short | 1,136 | 579 | 635 |
| ... most any one school is short | 129 | 32 | 32 |

(The first and third rows count every open K-5 school, program-only and floor-exempt buildings included: `levels.K-5.schools_in_range` and `levels.K-5.schools_in_range_at_minus9pct`. The "within 20" row and the three "9% low" rows count zoned, non-exempt schools (35), from each plan's `schools.csv` 2031-32 totals × 0.91 [inferred: our model]. −9% is our own stress test, not a PPS standard: PPS plans on PSU's medium forecast, which is what every other figure here uses.)

**What this means.**
- **If PSU's forecast is right,** the example plans keep far more schools at target than PPS A.
- **If enrollment comes in about 9% low,** PPS A keeps more schools in range than the example plans, because it already lets 12 run short and keeps the rest big. But their shortfalls are shallow: every school would be within 32 kids of 360, while PPS A's short schools would be up to 129 kids under, and 1,136 short in total vs about 580 to 640.
- **After the forecast window,** the same packing shows up, a year or three later. K-5 schools at target drop below PPS A's (21, 20, 19, 18 in 2032-33 → 2035-36):
  - Rebalanced PPS A and both Boundary changes plans from 2033-34 (18 and 19 vs 20).
  - Redrawn K-8 lines from 2034-35 (15 vs 19).
  - Those years are reported, not required.
- **In short:** the example plans are better on the forecast and more fragile to a miss. A size buffer (aiming for 380 instead of 360) didn't help: that version kept only 14 of 41 open K-5 schools in range at −9%, because 380 × 0.91 = 346 is still under 360. Surviving a 9% miss needs about 396 per school.

**Costs every redraw shares.**
- The walk redraws (the current best; both Boundary changes plans; Redrawn K-8 lines) reassign about 1,900–2,000 more K-5 kids than PPS A (about 4,820–4,910 vs 2,935, vs PPS Status Quo). "Rebalanced PPS A" reassigns about 660 more (3,594).
- Middle zones feed one high school less often: 40–47% for the example plans above (33% for the focus-option what-if below), vs PPS A's 80%. Two feeder measures appear on the site: "middle zones feed one high school" is the share of middle schools whose students go to one high school; "class kept together into high school" is the share of middle schoolers who go to the high school most of their classmates go to (current best 76%, previous best 77%, PPS A 90%).
- Lines: the example plans' elementary lines are cleaner than PPS's: 141–147 one-block notches (blocks mostly surrounded by another school's area), vs 197 under PPS A, and no real pockets (PPS A has five, one of 71 blocks at Faubion). Measured by `build/solver/lines_qa.py`; before/after in `out_v2/LINES_QA.md`. "Rebalanced PPS A" is the exception (303), because cleaning its lines moves more kids.

---

## Current best: fewer DLI moves, sustainable schools (`equity_noswap_alameda_rig_hs`) — the current best

**How it works.** PPS A's 14 closures, with elementary and middle-school lines redrawn for the shortest walks under the one firm rule (at least PPS A's number of schools at target, every year to 2031-32), and no program swaps: an immersion program whose building stays open stays home. So Atkinson Spanish, Scott Spanish, MLK Jr Mandarin and Beaumont Spanish 6-8 stay put, and Lent, Rigler and Cesar Chavez stay neighborhood K-5 schools with their Spanish programs. Two targeted fixes follow the redraw: big-school relief (an elementary school over 450 kids gets a soft ceiling of 450, and moving kids off it costs less), moving at most 300 elementary kids; and Rigler-area kids who aren't in Rigler's Spanish program are counted where PPS reports they attend (105 at Scott; PPS Oct 2025 enrollment by program and residence). High-school lines are PPS A's, with one change: the Skyline area stays at Lincoln, as today, instead of crossing the St. Johns Bridge to Roosevelt (as in the previous best). Middle schools use PPS's 500 minimum.

**The good.**
- Every elementary school at target every year 2027-28 to 2031-32: 38 of 38 (PPS A 18 of 35 by PPS's own figures, 21 on our model). Middle: 12 of 13 at PPS's 500 every year, 13 of 13 in 2031-32 (PPS A 5 by PPS's own figures).
- On PPS's own dashboard measures (2031-32, our model): 97% of schools sustainable (PPS A 69%, previous best 90%), and 98% of students in sustainable schools (PPS A 81%, previous best 93%); 65% of buildings efficiently used (PPS A 53%).
- Fewest immersion students moved of any plan that closes schools: 820 (PPS A 1,567; previous best 1,226).
- Shorter elementary trips than PPS A and the previous best: 70% of K-5 kids within 1 mile (PPS A 63%, previous best 68%); 3,805 past the 1-mile bus line (PPS A 4,703, previous best 4,117); 890 assigned to a farther school, past a closer one (PPS A 1,970, previous best 932).
- Shorter middle-school walks than PPS A: 1,037 middle schoolers assigned past a closer school (PPS A 1,259, previous best 1,082); average 1.72 mi (1.76).
- Classes stay together into middle school: 4 elementary zones split between middle schools (PPS A 1, previous best 3); 97% of K-5 kids go to the same middle school as most of their class (PPS A 99%).
- Ends Roosevelt's crowding: in range every year 2027-28 to 2031-32 (1,313 in 2027-28; PPS A's lines put 1,421 students in its 1,395 seats that year). High schools at target 6, 7, 7, 8, 8 (PPS A 5, 7, 7, 8, 8). Jefferson is below 1,100 in 2027-28 to 2029-30 (563, 804, 979) in every plan, PPS A included.

**The bad.**
- More students change schools than under PPS A: 38% of K-8 students on PPS's measure (PPS A 27%); 4,818 K-5 and 2,271 middle schoolers reassigned vs PPS Status Quo (PPS A 2,935 and 1,972).
- Fewer middle schoolers go to the same high school as most of their classmates: 76% (PPS A 90%, previous best 77%), and 40% of middle zones feed one high school (PPS A 80%). The middle lines were redrawn while the high-school lines are PPS A's, apart from Skyline.
- George is over its 623 seats in 2027-28 to 2030-31 (652, 650, 649, 628); PPS's own Family Guide projects George over 623 under PPS A too (George guide p. 60). Two middle schools sit right at 500 in 2031-32 (Gray, Jackson).
- 2,830 middle schoolers past the 1.5-mi bus line (PPS A 2,731, previous best 2,779).
- High schools: the gap between the largest and smallest grows from 362 to 424 students (target under 350) and the average walk from 1.93 to 1.98 mi; Roosevelt drops below 1,100 from 2032-33, a year PPS doesn't project (as in the previous best).
- Fragile to a 9% enrollment miss: 17 of 41 open K-5 schools stay in range at −9% (PPS A 25 of 41; at forecast 41 vs 27).

**Trade-off in one line.** Every elementary school at target every year, the fewest immersion moves, and shorter elementary trips than PPS A or the previous best, at the cost of more students changing schools than PPS A and weaker middle-to-high-school feeders.

Sources: `out_v2/equity_noswap_alameda_rig_hs/scorecard.json`, `schools.csv` and `TRADEOFFS.md`; `out_v2/PPS_SCORECARD_public.md` (row "Current best: fewer DLI moves, sustainable schools"; PPS dashboard measures computed from this run's `schools.csv` and `scorecard.json` by `build/solver/pps_scorecard.py`); `out_v2/TRADEOFFS_MATRIX.json` (classmates and split counts) [our model v2 on PSU July 2026 Table 5.5, not PPS figures, except where marked].

## Boundary changes, balanced middle schools (`option2_ms460`) — the previous best

**Previous best.** This was the best example we modeled until 2026-10-22. The current best (`equity_noswap_alameda_rig_hs`, above) beats it on PPS's sustainability measures (97% of schools and 98% of students in sustainable schools in 2031-32, vs 90% and 93%), moves fewer immersion students (820 vs 1,226), and puts fewer K-5 kids past the 1-mile bus line (3,805 vs 4,117). This plan keeps every middle school in its building every year (the current best has George over its 623 seats in 2027-28 to 2030-31), but only by using a 460 middle-school minimum: at PPS's 500, 9 of its 13 middle schools are at target every year, vs 12 of 13 in the current best. It also splits one fewer elementary zone between middle schools (3 vs 4), has fewer middle schoolers past the 1.5-mi bus line (2,779 vs 2,830), keeps slightly more middle schoolers with their classmates into high school (77% vs 76%), and uses more buildings efficiently (68% vs 65%). Both reassign 38% of K-8 students on PPS's measure, and both use the same high-school lines.

**How it works.** PPS A's closures, programs and high-school lines, with one change to the high-school lines: the Skyline area (about 93 high schoolers) stays at Lincoln, as today, instead of crossing the St. Johns Bridge to Roosevelt. Elementary and middle-school lines are redrawn for the shortest walks under the one firm rule: at least PPS A's number of schools at target, every year to 2031-32. Middle schools are balanced with a minimum of 460 (PPS's goal is 500), and at most 3 elementary schools may be split between middle schools; these middle-school lines are proven best under those rules (the solver closed the optimality gap to 0%). Two immersion moves that PPS A makes are avoided:
- **MLK Jr Mandarin** stays at MLK Jr (PPS A moves it to Boise-Eliot/Humboldt).
- **Beaumont Spanish 6-8** stays at Beaumont (PPS A moves it to Roseway Heights).

Two other moves are kept because they're needed: without them, Lent would have 274 kids and Rigler 321, both below 360.

**Call-out: middle schools below PPS's 500 goal.** The middle-school minimum is 460, not PPS's 500. Four middle schools dip below 500 in their low year: Harrison Park 461 (2030-31), Ockley Green 461 (2028-29), West Sylvan 460 (2031-32) and George 498 (2031-32). So at PPS's 500, 9 of 13 middle schools are at target every year 2027-28 to 2031-32 (PPS A 5 by PPS's own figures). West Sylvan falls to 443 in 2032-33, a year PPS doesn't project. In return, only 3 elementary schools split between middle schools and no middle school is over capacity [our model].

**The good.**
- Spares 341 immersion students a program move in 2031-32, about 326 counting only families PPS's own projections imply would have followed. (These follow shares are inferred from the PPS Family Guide, not stated by PPS.)
- 35 of 35 K-5 schools at target every year (PPS A 18 by PPS's own figures, 21 on our model).
- Every school in range in 2031-32, and no middle school over capacity in any year 2027-28 to 2031-32: the fullest are Hosford 710 of 711 and Lane 763 of 763 (2027-28), and Beaumont 724 of 737 (capacity: PPS 2025-26 school profiles).
- Classes stay together: 3 elementary zones split between middle schools (PPS A 1); 97% of K-5 kids go to the same middle school as most of their class (PPS A 99%).
- Shorter walks than PPS A at both levels. K-5: 932 kids assigned to a farther school, past a closer one (PPS A 1,970); average 0.93 mi (0.98). Middle: 1,082 (PPS A 1,259); average 1.71 mi (1.76).
- Ends Roosevelt's crowding in 2027-28: PPS A's high-school lines put 1,421 students in its 1,395 seats that year; with Skyline at Lincoln, Roosevelt has 1,313 [our model].
- Sunnyside's and Abernethy's areas stay entirely south of I-84. PPS A gives Sunnyside about 21 K-5 kids from north of I-84, Buckman's old crossing (our model on PPS's Scenario A K-5 map; the Sunnyside Family Guide, p. 3, sends Buckman's area "north of Burnside" to Sunnyside).

**The bad.**
- Smaller middle schools: three run in the 460s, below PPS's 500 goal (see the call-out).
- About 4,870 K-5 and 2,315 middle schoolers reassigned vs PPS Status Quo (PPS A 2,935 and 1,972).
- 40% of middle zones feed one high school (PPS A 80%).
- Roosevelt drops below its 1,100 minimum from 2032-33 (1,075, falling to 1,027 in 2035-36), years PPS doesn't project; PPS A's lines keep it above 1,100 through 2035-36 (1,104) [our model].
- The gap between the largest and smallest high school grows from 362 to 424 students (the target is under 350), and the average high-school walk from 1.93 to 1.98 mi.
- Fragile to a 9% enrollment miss (15 of 41 open K-5 schools stay in range at −9%, vs PPS A's 25 of 41; at forecast 41 vs 27).
- 2,779 middle schoolers over the 1.5-mi bus line (PPS A 2,731).
- The elementary lines weren't cleaned after their last re-solve (a cleanup made them worse): 147 one-block notches, still fewer than PPS A's 197.

**Trade-off in one line.** Keeps two immersion programs in their buildings, keeps elementary classes together and fits every middle school in its building, with shorter walks than PPS A, by accepting middle schools of about 460 instead of 500 and more moves.

## Balanced middle schools, Sellwood open (`option2_ms460_sellwood_home`)

**How it works.** The previous best (`option2_ms460`), with one building change: Sellwood Middle stays open instead of closing as in PPS A. Elementary lines, immersion programs and high-school lines are the same as `option2_ms460`. Sellwood serves about its own neighborhood, the Duniway and Llewellyn areas plus a few Grout-area blocks, and is exempt from the 460 middle-school minimum, so the solver doesn't pull kids from farther away to fill it. The other 13 middle schools are redrawn under the same rules as `option2_ms460` (minimum 460, few elementary schools split between middle schools). Kids sent past a closer middle school count four times as heavily here as in `option2_ms460`. The middle-school lines are proven best under those rules (optimality gap 0%).

**Call-out: Sellwood is a small middle school.** About 312 middle schoolers in 2031-32, in a building with room for 683 (46% full; capacity: PPS 2025-26 school profiles). That's below PPS's 500 goal; Sellwood is left out of the at-target counts as an exempt school. At PPS's 500, 7 of the other 13 middle schools are at target every year 2027-28 to 2031-32 (`option2_ms460` 9, PPS A 5 by PPS's own figures); in their low year Lane is at 460 (2031-32), Harrison Park 461 (2030-31), Ockley Green 461 (2028-29), West Sylvan 460 (2031-32), Kellogg 467 (2030-31) and George 498 (2031-32) [our model].

**The good.**
- Sellwood-area families keep a middle school close to home: Sellwood's middle schoolers average a 1.32-mi walk.
- Shortest middle-school walks of any plan: average 1.68 mi (`option2_ms460` 1.71, PPS A 1.76); 2,754 middle schoolers past the 1.5-mi bus line (2,779; PPS A 2,731).
- Fewer moves: about 2,074 middle schoolers reassigned vs PPS Status Quo (`option2_ms460` 2,315); 6,941 K-5 and 6-8 together (7,182).
- Middle schools feed high schools a little more cleanly: 50% of middle zones feed one high school (`option2_ms460` 40%, PPS A 80%); 8 middle schools split between high schools (9; PPS A 3).
- Hosford and Lane stop running near full: Hosford 626 of 711 seats at its fullest (`option2_ms460` 710), Lane 547 of 763 (763).
- Everything at the elementary level matches `option2_ms460`: 35 of 35 K-5 schools at target every year, 932 K-5 kids past a closer school (PPS A 1,970), average walk 0.93 mi, and 341 immersion students spared a program move in 2031-32.

**The bad.**
- One more middle-school building to run, for about 312 students.
- Smaller middle schools elsewhere: six of the other 13 dip below PPS's 500 goal in their low year (see the call-out).
- 1,164 middle schoolers assigned past a closer middle school (`option2_ms460` 1,082; PPS A 1,259). About 94 of them live nearer Lane but are in Sellwood's area today and stay at Sellwood.
- 4 elementary schools split between middle schools (`option2_ms460` 3; PPS A 1).
- K-5 and high-school drawbacks are the same as `option2_ms460`, including 15 of 41 K-5 schools in range at −9% (PPS A 25).

**Trade-off in one line.** Keeps Sellwood Middle open for its neighborhood, giving the shortest middle-school walks and fewer moves than `option2_ms460`, at the cost of a half-full building and more middle schools below PPS's 500 goal.

## Boundary changes, same closures (`option2`)

**How it works.** The same closures, immersion programs and elementary lines as Boundary changes, balanced middle schools, with PPS A's high-school lines unchanged (Skyline goes to Roosevelt, as in PPS A). Middle school also differs: the minimum is PPS's 500, with no cap on elementary schools split between middle schools.

**The good.**
- 12 of 13 middle schools at target every year at 500 (balanced middle schools 9 at 500; PPS A 5 by PPS's own figures); the smallest middle school is 500.
- Everything the previous best gets at K-5: 35 of 35 at target every year; 932 kids assigned to a farther school, past a closer one; the same two immersion programs stay put.
- 2,274 middle schoolers reassigned vs PPS Status Quo (balanced middle schools 2,315; PPS A 1,972).

**The bad.**
- Hosford is over capacity in its first two years: 823 and 776 students in a 711-seat building, 2027-28 and 2028-29 (the one middle school not at target).
- 13 elementary zones split between middle schools (balanced middle schools 3, PPS A 1); 89% of K-5 kids go to the same middle school as most of their class (97%, 99%).
- Longer middle-school walks than balanced middle schools and PPS A: 1,233 assigned to a farther school, past a closer one (1,082; 1,259); average 1.74 mi (1.71; 1.76); 2,938 over the 1.5-mi bus line (2,779; 2,731).

**Trade-off in one line.** Meets PPS's 500 middle-school goal at 12 of 13 schools, at the cost of an overcrowded Hosford early, more split elementary classes and longer middle-school walks.

---

## Redrawn K-8 lines (`option1_durable`)

**How it works.** Same as above, but every immersion move in PPS A is kept.

**The good.**
- 35 of 35 K-5 and 12 of 13 middle schools at target every year.
- **Best middle-school walking of the example plans** (by kids assigned to a farther school, past a closer one): 882 middle schoolers (PPS A 1,259); average 1.67 mi (1.76).
- K-5: 1,285 assigned to a farther school, past a closer one (PPS A 1,970); average 0.95 mi.
- 47% of middle zones feed one high school (tied best of the example plans with Rebalanced PPS A).

**The bad.**
- About 4,910 K-5 kids reassigned.
- 17 elementary zones split between middle schools.
- Longer K-5 walks than the previous best (1,285 vs 932 assigned to a farther school, past a closer one).
- Fragile to a 9% enrollment miss (16 of 41 open K-5 schools stay in range at −9%; PPS A 25 of 41).

**Trade-off in one line.** The pick if middle-school walking matters most, keeping PPS's immersion plan.

## Rebalanced PPS A (`option4`)

**How it works.** PPS A's closures and programs. Lines change as little as possible from PPS Status Quo while bringing schools into range, with a 2-mile K-5 walk cap. Three schools still miss in 2031-32 (Forest Park, Jackson and Roseway Heights).

**The good.**
- Fewest K-5 moves of the example plans: 3,594 K-5 kids reassigned vs PPS Status Quo (the redraws about 4,900; PPS A 2,935).
- 33 K-5 schools at target every year.

**The bad.**
- **Moves more kids than PPS A**: 3,594 K-5 vs 2,935. PPS A leaves 20 schools out of range, and fixing them takes moves.
- K-5 walking is about PPS A's (1,838 assigned to a farther school, past a closer one).
- Three schools still miss in 2031-32: Forest Park −101 (PPS A −102; geography under the 2-mile cap), Jackson −78, Roseway Heights −35.
- Most jagged lines (303 one-block notches vs PPS A 197). Every notch it adds fixes a school's size, so cleaning the lines would move more kids (+42 to +289 K-5 kids); it is left as solved.

**Trade-off in one line.** The fewest moves that fix PPS A's sizes is still more moves than PPS A; balancing schools isn't free.

## Close 2 focus options: Winterhaven, da Vinci (`option3a`) — a what-if

**How it works.** PPS A's closures, programs and high-school lines, plus Winterhaven (K-8 STEM) and da Vinci (6-8 arts) close. Their students return to their neighborhood schools, and elementary and middle lines are redrawn under the same rules as the redraws above.
- **Where returning students live** comes from a per-catchment spreadsheet of 2025-26 focus students (`build/pps-texts/focus-students-by-catchment-sheet-2025-26-public.md`; second-hand: its first columns match PPS's October 2025 Enrollment Summary, but the per-program columns' source isn't stated).
- They cluster near their schools. Winterhaven, grades 6-8 by middle-school catchment: Hosford 45, Sellwood 26, Lane 18 (its K-5 students sit in the elementary rows). da Vinci: Ockley Green 60, Tubman 56, Roseway Heights 40 (sheet rows, 2025-26).
- 21 students who live outside PPS aren't returned to any school.

**The good.**
- 35 of 35 K-5 and **13 of 13 middle schools** at target every year (PPS A 18 / 5 by PPS's own figures; 21 / 5 on our model). The returning students fill middle schools that are short in the other plans.
- Short K-5 walks: 1,001 assigned to a farther school, past a closer one (previous best 932); average 0.93 mi. Middle: 1,044 (PPS A 1,259).

**The bad.**
- Assumes every returning student attends their neighborhood school; none leave PPS or pick another option.
- Closes two programs families chose; what happens to the buildings isn't modeled.
- 4,888 K-5 kids reassigned vs PPS Status Quo; 33% of middle zones feed one high school; 8 elementary zones split between middle schools.
- Fragile to a 9% enrollment miss (17 of 41 open K-5 schools stay in range at −9%; PPS A 25 of 41).

**Trade-off in one line.** The most schools at target and among the shortest walks, bought by closing two choice programs and assuming their families stay in PPS. It also moves the most students (7,525 K-5 and 6-8) and has the fewest middle zones feeding one high school (33%).

**Friend groups.** 93% of K-5 kids go to the same middle school as most of their class (previous best 97%, PPS A 99%); 81% of middle schoolers go to the same high school as most of their class (previous best 77%, PPS A 90%). Smallest groups split off: about 7 per grade (Vestal → Mt Tabor) and 8 per grade (Woodstock → Kellogg); Faubion splits three ways (29 / 16 / 15 per grade). [inferred: traced block by block from `option3a/assign_*.parquet` on PSU 2031-32 kids, K-5 ÷ 6 and 6-8 ÷ 3 per grade]


## PPS Scenario A (`scenario_A`)

**How it works.** PPS's own plan. It closes elementary schools and assigns each closing school's area to one or two nearby receivers, with few other line changes. Several immersion programs move with their families. Its middle and high-school lines keep most middle schools feeding one high school. Size and at-target figures below are PPS's own (Family Guide p. 4, guides dated 2026-10-08); walking, moves and feeders are our model on PPS's map, since PPS doesn't publish them.

**The good.**
- Fewer students reassigned than any example plan, on our model: 2,935 K-5 and 1,972 6-8 vs PPS Status Quo (the previous best 4,867 and 2,315; the current best 4,818 and 2,271).
- Strong feeders: 80% of middle zones feed one high school, and 90% of middle schoolers go to the high school most of their classmates go to (our model on PPS's lines). Only 3 middle schools split between high schools.
- The most robust plan to an enrollment miss: 25 of 41 open K-5 schools stay in range if enrollment comes in 9% below forecast (our stress test, not a PPS standard).

**The bad.**
- Few schools at target every year 2027-28 to 2031-32 by PPS's own figures: 18 of 35 elementary schools and 5 of 13 middle schools.
- Sizes are uneven because lines aren't rebalanced across neighbors: some schools run big while others fall short, e.g. Clark 272 and Sunnyside 235 K-5 students in 2031-32, and George 636 in a 623-seat building (PPS figures).
- Longer elementary walks on our model: 1,970 K-5 kids assigned to a farther school, past a closer one; 62.7% within a mile (PPS Status Quo 72.2%).
- Moves 1,567 immersion students to a new program site in 2031-32 (our model).
- Kids past the bus distance rise 28% over PPS Status Quo, to 7,433 (our model; `BUSES.md`).

**Trade-off in one line.** Simple reassignments and strong feeders, at the cost of uneven school sizes and longer elementary walks.

## PPS Scenario B (`scenario_B`)

**How it works.** PPS's second plan: fewer closures than A (44 open elementary buildings vs A's 41, our count), with the same approach of reassigning closing schools' areas to nearby receivers and the same middle-school lines as A (our tracing of PPS's maps). Size and at-target figures are PPS's own (Family Guide p. 4); walking, moves and feeders are our model on PPS's map.

**The good.**
- Fewer moves than A on our model: 2,305 K-5 and 1,972 6-8 reassigned vs PPS Status Quo; 1,357 immersion students move (A 1,567).
- The same strong feeders as A: 80% of middle zones feed one high school; 3 middle schools split between high schools.
- One more middle school at target every year than A by PPS's figures (6 of 13).

**The bad.**
- Fewer elementary schools at target every year 2027-28 to 2031-32 than A by PPS's own figures: 15 of 38.
- The most elementary kids assigned to a farther school, past a closer one, of any plan on our model: 2,144.
- Less robust to an enrollment miss than A: 20 of 44 open K-5 schools stay in range at −9% (our stress test).

**Trade-off in one line.** Keeps more schools open than A and moves fewer families, at the cost of more small schools.

## PPS Status Quo (`status_quo`)

**How it works.** No closures: PPS's 2027-28 lines with every school open, sized by the PSU forecast (Family Guide "No changes" row = PSU July 24, 2026, Table 5.5). It's the baseline every plan's moves are counted from.

**The good.**
- Nobody is reassigned and no immersion program moves.
- The shortest walks of any plan on our model: K-5 average 0.87 mi, 72.2% within a mile.

**The bad.**
- Few schools at target every year 2027-28 to 2031-32 by PPS's own figures: 9 of 50 elementary schools and 2 of 14 middle schools.
- Many small schools as enrollment falls: by PPS's figures several elementary schools sit near or under 200 students (e.g. Rosa Parks 159, Creston 187 at their low year).

**Trade-off in one line.** The shortest walks and no disruption, with most schools below PPS's size goals (360 for K-5, 500 for middle).

---

**Dropped, as a finding:** "All lines redrawn, walkable K-12" (`option1_full`). Redrawing high schools too didn't improve feeders (47%), and high-school trips got longer than PPS A's (2.06 vs 1.93 mi avg). The Ida B. Wells area has ~734 middle schoolers for two middle schools that need 1,000; the Grant area 445 for Beaumont's 500. PPS A has the same weak spots (`option1_full.staging/TRADEOFFS.md`).

**Dropped, as a finding:** "Shortest walks" (`frontier_k17`). It drew the shortest walks that only match PPS A's count of schools at target, to show what the extra schools at target cost in walking. Once the elementary lines of Boundary changes, same closures were re-solved, that plan beat it on nearly every measure: 932 vs 995 elementary kids sent past a closer school, 35 vs 28 elementary and 12 vs 10 middle schools at target every year, 7,141 vs 7,413 students reassigned, 1,226 vs 1,567 immersion students moved. Its one edge, fewer elementary schools split between middle schools (8 vs 13), is beaten by Boundary changes, balanced middle schools (3). So keeping more schools at target no longer costs walking.

**Dropped, as a finding:** "Solver picks schools" (`capstone_s2`, `cap3_500_s2`). Letting the solver also choose which schools close didn't beat PPS A's closures with redrawn lines. Without moving immersion programs, middle-school walks rose to 2.09 miles and about 1,600 more students moved than in Boundary changes, same closures. Its strong middle-school numbers came only from moving immersion programs: 1,611 students, more than PPS A's 1,567.
