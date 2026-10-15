# Boundary solver: method

> **Durability horizon (current):** plans must meet or beat Scenario A's count of schools at target in **every year 2027-28 → 2031-32** (PPS's projection window); 2032-33 → 2035-36 is reported only; nothing past 2035-36 is modeled. See §7. *History:* v1 and the early v2 runs used 2031-32 → 2040-41 (PSU's district trend past 2035-36); §3b and §4 describe that older window, which configs without a `"horizon"` key still use.

Built 2026-10-12. Code: `common.py` (data), `gen_configs.py` (plan/option configs), `solve.py` (CP-SAT engine), `metrics.py` (scorecard). Python with OR-Tools 9.15 CP-SAT.

```
python gen_configs.py                     # writes configs/*.json
python metrics.py                         # baselines -> out/baselines/{today,status_quo,scenario_A,scenario_B}/
python solve.py configs/option1.json      # -> out/option1/   (add --from 6-8 to reuse the K-5 checkpoint)
```

Every output folder holds the same files: `assign_K-5.parquet`, `assign_6-8.parquet` and `assign_9-12.parquet` (idx, GEOID, school), `schools.csv` (per building), `scorecard.json` and, for solved options, `infeasibility.json` and `solve_log.txt`.

## 1. Inputs and the 2031-32 basis

- **Blocks:** the 9,295 blocks of `build/data/blocks.parquet` (idx = pps-model BL index). Kids are **neighborhood-program kids only** (`k5`, `m68`, `h912`). Each block carries its old area's capture rate.
- **Scaling to PSU 2031-32.** Each block's count is multiplied by its area's ratio *r = PSU 2031-32 neighborhood forecast / modeled 2025-26 neighborhood kids*:
  - K-5 by today's K-5 area (`es_cur`); 6-8 by today's 6-8 area (`ms_cur`). PSU forecasts each school on today's lines.
  - 9-12 by the Status-Quo 2027-28 area (`sq_hs`). PSU's 2031-32 HS numbers already include the end of Jefferson dual assignment (Jefferson 377 → 1,172 neighborhood).
  - PSU's "Neighborhood" program row is used where it exists, otherwise "Total". K-8s use the K-8 total ratio for both bands. Cesar Chavez uses its Neighborhood K-8 row (143 → 97).
  - Result: **Status Quo lines reproduce PSU's 2031-32 neighborhood numbers by construction.** District totals are K-5 13,038 (excluding Lent/Rigler DLI), 6-8 6,023, 9-12 9,261.
  - Ratios run from 0.62 (Sellwood 6-8) to 1.20 (Beach K-5).
- **Lent and Rigler K-5 areas** are whole-school Spanish DLI, so their kids follow the program (`lr_nbhd_share` = 2% are counted as neighborhood kids). PPS's own A projections imply about this much: Kelly gains ~5 from Lent's area, and Scott stays at 470. Their 6-8 and 9-12 kids are ordinary neighborhood kids.
- **Programs** (DLI strands, PISA) are fixed populations at their host building, using PSU 2031-32 program rows (`common.PROGRAMS`).
  - The Cesar Chavez K-8 Spanish program is split 273/443 K-5 and the rest 6-8, by its ODE grade mix.
  - Each config lists which building hosts which program. The Scenario A-based plans use Scenario A's placements.
  - Focus schools (Winterhaven, da Vinci, Odyssey, ACCESS, MLC, Benson) are fixed and outside the size test. Options 3a/3b can dissolve Winterhaven or da Vinci into the blocks with `dissolve_programs` (homes from `focus_dli_homes.parquet`).
- **Distances:** local-OSRM walk (and bike) miles, block centroid → school (`build/routing/*_miles.parquet`). All three levels use **walk miles** in the objective.
  - For 9-12, walk distance is only a proxy: high schoolers ride TriMet, and transit time is the right measure.
  - The scorecard also reports bike miles for 6-8 and 9-12.
- **Hard edges:** the pps-model zones are W (west of the Willamette), N (east side north of I-84) and S (east side south of I-84). A block may go to a school whose zone is in its allowed zones (`az`), or in the zone of its Today/Status-Quo school, which is an *existing* crossing. That is "no new I-84/Willamette crossings". 82 blocks straddle N/S.

## 2. Targets (hard, with slack)

| Building | Floor | Ceiling |
|---|---|---|
| K-5 | 360 | min(functional capacity, 600) |
| K-8 (Astor, Skyline) | 500, **exempt** in district-like runs | functional capacity (K-8 total) |
| 6-8 | 500 | functional capacity (85% MS rate is already in it). Harrison Park uses 890 (PPS 2025 model) instead of the 1,006 K-8-era figure |
| 9-12 | 1,100 | slide-21 capacities (Jefferson 1,773, Grant 1,935, McDaniel 1,735, Roosevelt 1,404), LRFP otherwise |

- Sizes count neighborhood kids plus hosted programs.
- Each bound has a slack variable with a huge penalty: 10,000 kid-miles per kid, which dwarfs any routing gain. A non-zero slack is therefore a **proof-of-optimization-level infeasibility report** for that school, never a silent relaxation.
- "Program-only" buildings (Lent, Rigler, Chavez and Richmond under A) have no zone. Their size is fixed by the program placement and checked by the scorecard.
- HS range (max − min) ≤ 350 is **soft**, penalized at 2 kid-miles per kid of excess.

## 3. The model (one engine, run per level)

**Variables.** x[i,s] ∈ {0,1} for block i and each candidate school s, with exactly one per block.

**Candidates.**
- K-5: the 7 nearest (walk) eligible open schools, plus the Status-Quo school if eligible.
- 6-8: per K-5 zone, the 5 nearest middle schools by kid-weighted walk among those eligible for most of the zone's kids, plus the zone's SQ and Scenario-A middle school. A K-8 zone feeds only its own K-8.
- 9-12: per 6-8 zone, the 4 nearest high schools, plus SQ and A.
- **Pruning:** a candidate is dropped when the block cannot connect to that school's building through blocks that also have it as a candidate. This removed 64 pairs at K-5.

**Objective,** in kid-miles. Weights are in the config.
- walk: 1 per kid-mile
- past a closer school: 0.25 per kid sent at least 0.25 mi further than the nearest eligible open school
- moved vs Status Quo 2027-28: 0.15 per kid
- boundary length: 3 per km of attendance-area boundary (shared Voronoi edge length from cowork `edges.json`; zero on zone lines)
- optional diversity term (off except in diversity runs): per kid of a school's kids-of-color share outside ±15 points of the district share
- split feeder: 300 each
- HS range excess and size slack, as above

**Contiguity: exact, by a distance-ordered ("star") rule.** Each school's zone must contain its building's block (root).
- A non-root block may join school s only if at least one neighbor with a *strictly smaller* geodesic potential φ_s also joins s. φ_s is the shortest-path distance from the root over blocks that have s as a candidate.
- Every chain of strictly decreasing φ_s ends at the root, so **every zone is connected: guaranteed, not repaired.**
- Every reachable block has such a neighbor (its shortest-path predecessor), so no candidate is excluded outright.
- The rule is a restriction: a zone must be "geodesically star-shaped" around its school. Each run therefore also solves the **relaxation with no contiguity**. Its bound is a valid lower bound for *any* plan, contiguous or not, and we report the gap to it.
- This formulation adds one clause per assignment variable and propagates strongly.
- **What was tried first.** Lazy separator cuts (for an island C of s: x[v,s] ≤ Σ x[N(C),s]) are exact in the limit. At 7,500 blocks the 60-second re-solves oscillated: the gap swung between 1% and 19% and islands didn't go to zero, so they were replaced. The cut machinery is still in `solve.py` as a backstop for schools without a root.
- **Adjacency fix.** pps-model `NB` leaves the rural Skyline / Sauvie / Bybee Lake area as about 35 fragments with no neighbors. Contiguity there was impossible, so `common.adjacency()` bridges each fragment to its nearest same-zone block (44 bridges, zero boundary length).

**Warm starts.**
1. Solve the relaxation from the Scenario-A map hint.
2. Greedily repair it into a star-feasible assignment (moving violators to a candidate that satisfies the rule, with geodesic-nearest as the fallback, which always satisfies it).
3. Solve the star model from that hint.

**Feeders (6-8 and 9-12).**
- Blocks are grouped by their K-5 zone (at 6-8) or their 6-8 zone (at 9-12), and group members are forced equal: clean feeders by construction.
- Contiguity uses the same star rule at **zone level**. The units are connected pieces of zones, with potentials on the zone graph.
- **Phase 2 runs only if phase 1 needs any size slack.** It lets a zone split (indicator z_g, x[i,s] − x[rep,s] ≤ z_g) at a cost of 300 per split, and uses block-level star contiguity. Every split is reported.
- A middle or high school's building block roots its zone. If two buildings share a feeder zone, only the first is rooted, and the other falls back to cuts.

**9-12 grouping (durable options).** Whole *elementary* zones go to high schools, so a middle school may split between high schools but no elementary zone does. For each middle zone p and high school h, u[p,h] = OR of its elementary zones' choices. Each u costs `ms_split` (5,000), so every extra high school a middle zone feeds is penalized, more than the durability reward per school. Last resort (phase 2): block-level assignment within elementary zones, at `split` (20,000) per split zone. "Shortest walks, sized for 2031-32 only" (`option1_2031only`) used whole middle zones at 9-12.

**Phase 2 is lexicographic** for durable runs:
- 2a minimizes only size slack, durability-count slack and splits (60 s relaxation, 180 s star model).
- 2b re-solves the full objective with splits ≤ 2a's count, warm-started from 2a without a relaxation round.
- The 2a assignment is kept if 2b ends with more slack.

**Decomposition.** Schools are linked when any block may go to both, and each connected set is solved independently. At K-5 this gives two sets: W, and N+S (linked by the 82 straddling blocks). Middle school splits into ~6 regional sets. High school is one set because of the range constraint.

**Settings.** 6 CP-SAT workers, seed 7. Relaxation 120 s, star model 300 s. Peak memory about 1.4 GB.

## 3b. Durability mode (default for every option after "Shortest walks, sized for 2031-32 only" (`option1_2031only`))

*This section describes the original (v1 / early v2) 2031-32 → 2040-41 window. Current runs use horizon `pps2031` (§7): required 2027-28 → 2031-32, per-school PSU sizes, reward for schools at target in all required years.*

"Shortest walks, sized for 2031-32 only" (`option1_2031only`) packs schools right at the 2031-32 floor. With PSU's continued decline it collapses: K-5 goes 35/35 at target in 2031-32 → 12 in 2032-33 → 9 by 2040-41. Durability mode fixes that.

- **Years and ratios.** `common.PSU_MEDIUM` holds the PSU medium district forecast (Table 5.2) for 2031-32 to 2040-41 by level, with K-5 = K-2 + 3-5. Every school at a level is scaled by the same ratio r_y = total_y / total_2031-32:
  - K-5: min 0.916, so a 360 floor needs 393 in 2031-32 to hold all ten years
  - 6-8: 0.917–1.043 (a 500 floor needs 545)
  - 9-12: min 0.883 (a 1,100 floor needs 1,246)
  - A per-area version would need PSU's per-school Table 5.5 by year. Our extract has only 2025-26 and 2031-32 (and PSU's school table stops at 2035-36), so it isn't done. Low/high scenarios (Tables 5.3/5.4) are not loaded.
- **Model.** For each countable school s and year y there's an indicator b[s,y]. b[s,y] ⇒ size_s ≥ ⌈(floor + margin)/r_y⌉ and size_s ≤ ⌊(ceiling − margin)/r_y⌋. Countable means zoned and not floor-exempt.
- **Requirement.** Σ_s b[s,y] ≥ (Scenario A's count for year y), using the same metric on the digitized A map. A slack with a penalty of 100,000 kid-miles per missing school makes any shortfall a reported infeasibility. Mode `all` (used by every current plan) requires every countable school every year.
- **Reward.** 3,000 kid-miles per school at target in all ten years (d_s ≤ b[s,y] ∀y), plus 100 per school-year. 2031-32 floors and ceilings stay hard.
- **Splits.** The split penalty is raised to 20,000 so splits are still used only for feasibility, not traded for durability.
- **9-12 grouping (durable options).** Whole *elementary* zones go to high schools, so a middle school may split between high schools but no elementary zone does. For each middle zone p and high school h, u[p,h] = OR of its elementary zones' choices. Each u costs `ms_split` (5,000), so every extra high school a middle zone feeds is penalized, more than the durability reward per school. Last resort (phase 2): block-level assignment within elementary zones, at `split` (20,000) per split zone. "Shortest walks, sized for 2031-32 only" (`option1_2031only`) used whole middle zones at 9-12.

**Phase 2 is lexicographic** for durable runs:
- 2a minimizes only size slack, durability-count slack and splits (60 s relaxation, 180 s star model).
- 2b re-solves the full objective with splits ≤ 2a's count, warm-started from 2a without a relaxation round.
- The 2a assignment is kept if 2b ends with more slack.

**Decomposition.** The per-year count spans the district, so all schools at a level are solved as one component. K-5: 9,295 blocks, 65k assignment variables, 180 s relaxation plus 600 s star model.
- **Bounds.** The rewards are negative objective terms, which makes the CP-SAT bound loose. For durable runs, read the gap as "unproven" rather than as a quality measure.

## 4. Scorecard (metrics.py)

The scorecard is the same for every plan and every level. All values use neighborhood kids on the 2031-32 basis.
- **Distance:** avg walk (and avg bike for 6-8 and 9-12); % within ½, 1 and 1½ mi (plus 2 for HS).
- **Bus eligibility:** kids over Oregon/PPS thresholds: walk > 1 mi at K-5; > 1.5 mi at 6-8, including K-8 6-8 per PPS's grade rule; > 1.5 mi at 9-12. The 9-12 figure ignores the TriMet-stop test.
- **Kids assigned to a farther school, past a closer one:** assigned at least 0.25 mi further than the nearest eligible open school at that level, with eligibility meaning no new hard-edge crossing.
- **Size:** buildings open and in range (K-8s judged on their K-8 total and listed at both K-5 and 6-8; Astor and Skyline exempt from the floor), min, max and mean utilization. Also in-range counts on the 2025-26 basis and at −9%.
- **Disruption:**
  - kids reassigned vs PPS Status Quo (2027-28, no closures); the vs-Today figure is still computed but not shown (Today archived)
  - DLI kids moved, split by "building closes" vs "program moves"
  - split feeders: a destination counts if it gets ≥5% and ≥5 kids
  - % of 6-8 zones feeding one high school
  - HS enrollment range
- **Durability** (`durability` in scorecard.json): zoned non-exempt schools at target each year of the run's horizon (current `pps2031`: 2027-28 to 2035-36, of which 2027-28 to 2031-32 required, count in all required years = `at_target_all_required_years`; older runs: 2031-32 to 2040-41, `durable_through_2040_41`), and each school's first year out of range and by how much. Program-only buildings are counted separately.
- **Equity:** dissimilarity index (kids of color vs white kids across schools at each level, Census 2020 under-18 by block from `pps-race.csv`). Also the kids-of-color share of movers vs the district share.

Baselines:
- **Today:** 2025-26 lines; 9-12 uses the pooled dual-assignment clusters, so Jefferson has no neighborhood area.
- **Status Quo 2027-28**, **PPS Scenario A** and **PPS Scenario B**: digitized PPS maps from `blocks.parquet`.

## 5. Known limits

- Census residents aren't enrollment. Any size within ~15% of a threshold is uncertain (backtest.md). Moved blocks carry their old area's capture rate.
- DLI and focus home locations are estimated, and DLI 2031-32 sizes are PSU program forecasts held at the host.
- Spanish HS DLI is regional by home address. Here it sits at its 2025-26 HS host, which matches A.
- Middle school is solved after K-5, so K-5 lines are chosen without regard to middle school feasibility. A joint model, or a K-5 re-solve with middle school feedback, could remove some splits.
- 9-12 is judged on walk miles; transit minutes would be better.

## 6. Model v2 (2026-10-12)

v2 is opt-in per config (`"model_version": "v2"`, configs in `configs/v2/`, written by `gen_configs_v2.py`; code in `v2.py` plus v2 hooks in `metrics.py` and `solve.py`). Results go to `out_v2/`. v1 configs and `out/` are untouched and still reproduce (Scenario A v1 building totals checked to within 0.001 kids, 2026-10-12). Calibration against PPS's projections is in `out_v2/CALIBRATION.md`. Labels: [PPS] stated in a PPS document, [inferred] our arithmetic on PPS numbers, [2nd-hand] from a community source, [choice] our modeling choice.

1. **Focus-lottery students (fix 1).** Sunnyside, Bridger and Buckman enroll many students from outside their areas. In-zone students (PPS Enrollment Summary Oct 2025, "own neighborhood school": Sunnyside 219, Bridger 143, Buckman 133 [PPS]) stay on the area's blocks. The rest (ODE 2025-26 enrollment minus in-zone) are a separate population, scaled by the host's PSU row by year. Placement follows each school's own PPS text when the school itself changes, and the Family Guide p. 2 footnote ("we assume that students return to their neighborhood school" [PPS]) only for schools with no change of their own:
   - Buckman closes: its students split 50/50 Abernethy/Sunnyside [PPS: Oct 6 memo, BoardBook file 14509719, p. 2]. Lottery students are a fixed 50/50; in-zone kids follow the line.
   - Sunnyside K-5 lottery students stay through grade 5, with no new admits [PPS: Sunnyside guide p. 3, "permitted to remain through 5th grade"]. The share at Sunnyside is (2032 − year)/6 for 2027-28 to 2031-32 [inferred], then 0. The rest go home. Sunnyside 6-8 lottery students go home [choice; PPS's Hosford projection leaves no room for them].
   - Bridger keeps its K-5 focus [PPS], so its K-5 lottery students stay. Its 6-8 lottery students go to Harrison Park [PPS: Bridger guide p. 3, the stated default].
   - "Home" = Census band residents in the host's 2025-26 high-school cluster, excluding the host and the Lent/Rigler areas [choice; the same rule `build/data` uses for all focus homes].
2. **Lent-area non-DLI students (fix 2).** About 117 Lent-area PPS students attend another neighborhood school (Marysville) [PPS: Enrollment Summary Oct 2025, Lent row; Closure Commutes says 115, 2nd-hand]. They sit on Lent-area blocks and are taken out of Marysville's area count. In today and Status Quo they attend Marysville. **In the Scenario A/B baselines they stay with Marysville's students at Arleta**, following PPS's stated phase-in [PPS: Marysville guide p. 3, "Avoiding multiple moves: Delaying full implementation …"]. This matches PPS's numbers (Kelly 407 vs 401, Arleta 549 vs 543). **Our options assign them by where they live**, like every other kid. Open question: PPS's Kelly projection shows no new Lent-area families after 2028-29 (`build/research/pps_internal_gaps.md` §1).
3. **DLI arrival shares (fix 3).** For each moved strand, the share that arrives at the new host is IMPLIED by PPS's Family Guide projections and PSU's strand forecast [inferred; PPS states no rate]: Atkinson→Lent 0.797–0.803, Scott→Rigler 0.812–0.825, Clark→Woodstock 0.84–0.93, Beach/James John/Sitton→Chávez ≈0.89, Beaumont→Roseway ≈0.90, Vestal and Boise-Eliot/Humboldt moves 1.0 (`build/data/v2/dli_follow.json`; `build/research/follow_rate/report.md`). Years after 2031-32 hold the 2031-32 share. Non-arrivals stay at the sending building if it still serves those grades (PPS's numbers show arrive + stay ≈ 100–112% [inferred]); otherwise they go home. A strand that doesn't move (most strands in "Boundary changes, same closures", `option2`) has no follow rate.
4. **Capacities (fix 4).** PPS 2025-26 school profiles' functional capacity (`build/data/v2/capacity_2025_26.csv`) [PPS numbers, captured 2nd-hand from pps-dli-explorer snapshots; archived in `build/pps-texts/school-profiles-2025-26/`]. Jefferson is overridden to 1,773 post-modernization [PPS: Sept 15 2026 deck slide 21]. Boise-Eliot/Humboldt's 586 vs the Family Guide's 632 is unexplained.
5. **Utilization (fix 5).** 70–100% of functional capacity is a stated PPS aim [PPS: Family Guide glossary p. 2, "Space use goal"; PPS staff, Sept 15 2026 board meeting, https://youtu.be/uAf7l-ChjFo?t=15369]. It's reported, not enforced; the ceiling stays hard at 100%.
6. **Per-school forecasts by year (fix 6).** Each area's block kids, each strand and each focus population is scaled by its own PSU July 24, 2026 Table 5.5 row, year by year from 2027-28 to 2035-36 (`build/data/v2/psu_table5_5_by_year.csv`, parsed from `build/pps-texts/boardbook-2026-10/psu-prc-pps-enrollment-forecasts-2026-27-to-2035-36.md`) [PPS/PSU]. 2036-37 to 2040-41 extend each row with the PSU medium district trend by level (Table 5.2) [inferred; PSU's school rows stop at 2035-36]. Durability checks each school's own size in each year, and the solver's per-year constraints use the same sizes.
7. **Other v2 settings.** Scenario A's 9-12 lines are kept in every option (`fixed_assign: A_hs`, because feeder splits didn't pay in v1 "Most schools at target, every year" (`option1_durable`, then named "Most schools that last to 2040-41")). Candidate costs are rebuilt after pruning unreachable candidates (a v1 bug, fixed for v2 only). Solver workers = 4, two runs at a time.
8. **Baseline vs options.** The PPS baselines follow PPS's phase-in where PPS states one (Marysville → Arleta). Status Quo and Scenario A/B follow PPS's 6-8 maps, including the Rigler-area middle schoolers in Roseway Heights, which PPS's numbers don't reflect (`pps_internal_gaps.md` §3). Options draw their own lines and assign every kid by where they live.
9. **Scorecard additions.** `durability.levels[*].schools[*].in_range_by_year` (a list aligned with `durability.years`) and `sizes_by_year`.
10. **Frontier runs** (old 2031-32 → 2040-41 window; paused/superseded by §7): "Shortest walks" (`frontier_k17`), "Balanced: 19 at target every year" (`frontier_k19`), "Balanced: 21 at target every year" (`frontier_k21`): Scenario A's schools, programs and 9-12 lines, with the same hard rule (meet or beat A's count at target every year). There's no per-school durability reward. Instead, `durability.min_durable` requires at least N schools at target in all ten years (K-5 N = 17 = A, 19, 21; 6-8 none, 7, 8). "Most schools that last to 2040-41" (`option1_durable`, reward 3,000 kid-miles per durable school) is the end point. See `out_v2/FRONTIER.md`.
11. **Optional schools (`optional_open`; used in the capstone tests).** A boolean per optional school: a closed school takes no blocks, its root block is free, and its 2031-32 floor applies only if it's open. With `cap_receivers_per_closure` (option 5 = 2; PPS deck 2026-10-06 p. 11, "Capped receiving schools at no more than two per closure", https://youtu.be/zOUH2Jq7Owo?t=5941), the blocks of a closed school's current area may go to at most 2 schools. The capstone tests also require every open school to be at target in all ten years (penalized slack per school). Buildings holding a fixed program or lottery population are never optional, and nothing is pinned to an optional building (DLI non-arrivals and lottery returners go home instead).
12. **Focus-option closures (options 3a, 3c, 3d).** Closed focus programs' students return to neighborhood schools. In option 3a (the live what-if) they return by the catchment they live in, from a per-catchment sheet of 2025-26 focus students (`build/pps-texts/focus-students-by-catchment-sheet-2025-26-public.md`; second-hand: its first columns match PPS's October 2025 Enrollment Summary, but the per-program columns' source isn't stated); 21 students who live outside PPS aren't returned. Options 3c and 3d (tests) used estimated home locations instead (`focus_dli_homes.parquet`; district- or cluster-proportional, not published). Returners are split into K-5 and 6-8 by grade. ACCESS serves grades 1-8, so its returners are 5/8 K-5 and 3/8 6-8; its TAG services aren't modeled. Odyssey is a program inside a building, so closing it changes no building.
13. **Solver budget (v2).** K-5 relaxation 180 s, first contiguity round 600 s, then up to 2 warm-started 400 s improvement rounds while 2031-32 size slack remains (an improvement round is kept only if it lowers slack). 6-8 phase 2a (feeder splits) gets 600 s; if it finds nothing, the whole-zone phase-1 plan is kept. CP-SAT's optimality gap is reported in `solve_log.txt` and is large (bounds are weak); results are good feasible plans, not proven optima.
14. **Middle→high feeders.** In the 6-8 solve, every high school a middle zone feeds (by Scenario A's fixed 9-12 lines; a destination counts at ≥5 kids of the zone's 9-12 band) costs `ms_split` = 5,000 kid-miles. At least 70% of middle zones must feed one high school (penalized slack, reported as `ms_to_one_hs_short`). PPS Scenario A has 80%; PPS's KPI target is 100%.
15. **Elementary zones nest in high-school lines.** K-5 candidates are limited to schools whose building sits in the block's own Scenario A high-school area, where the block has such a candidate. PPS's own Scenario A K-5 lines nest in 36 of 37 zones. Without this, no middle plan could reach 70% (5 of 15 at best, proven, with the earlier K-5 zones). Rebalanced PPS A uses a soft version (1 kid-mile per kid across a line) because its 1.5-mile candidate filter plus hard nesting has no contiguous plan.
16. **Tactical high-school lines (`option1_durable_hs`).** It takes the K-5 and 6-8 lines of the earlier v2 solve (no feeder rules) and solves 9-12 by whole elementary zones. A high school may differ from Scenario A's, at 2 kid-miles per kid moved. It must keep each high school in range and meet Scenario A's count at target every year (both penalized), with `ms_split` per extra high school and ≥70% of middle zones feeding one high school.
17. **Write rule and checks.** v2 solves write to `out_v2/<run>.staging/`. `run_queue.py` runs `check_exclaves.py` (every school's blocks connected on the solver adjacency; levels fixed to PPS's traced lines are exempt), writes a generic TRADEOFFS.md, renames the old folder to `<run>.prev` and swaps the new one in. Only then does it mark MANIFEST `done`.

## 7. PPS horizon and soft feeders

A config switch, `"horizon"` (`common.HORIZONS`), sets the durability window. Configs without it keep `psu2041` (2031-32 → 2040-41, all required, 2036-41 extended with the PSU district trend), so every earlier v2 result still reproduces; the earlier configs of the reruns are kept as `configs/v2/<run>_psu2041.json`. Generated by `gen_configs_v2.py` (last block).

1. **Horizon `pps2031`.** Required years 2027-28 → 2031-32: PPS's own projection window ("Estimates cover 2027-28 through 2031-32", PPS Family Guides p. 1, e.g. `build/pps-texts/family-guide-sabin.md`) [PPS]; PPS measures its targets in 2031-32. The solver requires, at every level and in each required year, at least as many zoned non-exempt schools at target as Scenario A has on the same model (penalized slack, 100,000 kid-miles per school short). Scenario A's counts, recomputed on this window [inferred: our model]: K-5 23, 23, 22, 22, 21; 6-8 10, 9, 9, 7, 7; 9-12 5, 7, 7, 8, 8. Sizes per year come from each school's own PSU July 2026 Table 5.5 row (`build/pps-texts/boardbook-2026-10/psu-prc-pps-enrollment-forecasts-2026-27-to-2035-36.md`, "Enrollment Projection by Grade Group, 2026-2035") [PSU]. 2032-33 → 2035-36 are scored and reported, not optimized. The 2036-41 extension is dropped: forecasts that far out are too uncertain. The durable reward (3,000 kid-miles) now goes to a school at target in **all required years**, plus 100 kid-miles per school-year at target in the required years. The 2031-32 floor/ceiling stays a hard (heavily penalized) bound as before.
2. **Scorecard keys under `pps2031`** (`durability`): `horizon`, `years` (2027-28 … 2035-36), `required_years`, `reported_years`; per level `at_target_zoned`, `at_target_all_required_years`, `at_target_all_years_to_2035_36` (replaces `durable_through_2040_41`, which is not written under this horizon); per school `in_range_by_year`, `in_range_all_required_years`, `in_range_all_years`; and `durability.reference` (Scenario A's counts on the same window, `short_in_required_years`, `meets_reference_every_required_year`). Baselines and `option1_durable_msfeed_off` were re-scored on this horizon without re-solving (`rescore_pps2031.py`).
3. **Middle→high feeders, soft.** Each high school a middle zone feeds (≥5 kids of its 9-12 band, by Scenario A's fixed 9-12 lines) costs `ms_split` = 200 kid-miles, i.e. ~200 per extra high school. No floor (`ms_hs_feeder.min_share` = 0). Reported: `levels.9-12.pct_ms_feeders_to_one_hs` (Scenario A: 80% [inferred: our trace of PPS's A maps]); the marginal cost of the next fix is estimated per run in TRADEOFFS.md.
4. **Walkable K-5.** No hard nesting of K-5 zones inside Scenario A's high-school lines (§6.15 is off for these runs). A tiny soft cost, 0.1 kid-mile per kid placed in a K-5 school across an A high-school line, breaks near-ties only; it was tested against no nesting at all (`_diag_nonest_pps2031`), see `out_v2/option1_durable/TRADEOFFS.md`.
5. **Solver limits.** Original v2 limits (not the halved ones): relaxation 180 s, first contiguity round 600 s, cut rounds 60 s, feeder-split phase 2a 60 s / 600 s; 4 workers, two runs at a time.
6. **Boundary changes, same closures (`option2`).** Atkinson Spanish → Lent and Scott Spanish → Rigler are necessary moves (Lent 274 and Rigler 321, below 360, if their strands stay home; both have no neighborhood area in A) [inferred: our model]. Avoided: MLK Jr Mandarin stays at MLK Jr, Beaumont Spanish 6-8 stays at Beaumont. All other strands are placed as in Scenario A. DLI recount: `dli_moves_v2.py` → `out_v2/option2/dli_moves.json`.
7. **Rebalanced PPS A (`option4`).** The K-5 candidate filter is a 2.0-mile walk cap (was 1.5 mi, infeasible with contiguity).
8. **Warm starts and phase 2.**
   - `levels.<lev>.warm_start` hints a level from another run's assignment and skips the relaxation round. Hint only, with the same rules and costs. Used for "Boundary changes, same closures" (`option2`) K-5, whose first original-limits solve stalled, and for "All lines redrawn, walkable K-12" (`option1_full`) K-5.
   - `solver.phase2_warm` starts the feeder-split search (phase 2a) from the feasible whole-zone plan instead of a fresh relaxation hint. That hint left dozens of contiguity violations, and 2a then timed out (6-8 kept its whole-zone shortfall) or came back worse than the whole-zone plan. The flag also rejects a phase 2 that doesn't reduce slack.
   - `levels.<lev>.max_splits` caps the split zones in phase 2.
   - Runs before this fix (`option1_durable`, `option2`) used the old phase 2.
9. **Walk-cap fallback (Rebalanced PPS A, `option4`).** A block left with no reachable school inside the cap after pruning gets its 3 nearest-walk schools, plus its neighbours' nearest in-cap school, as candidates (`max_walk_fallback_nearest`). On the 2.0-mile cap this affects one small block on the Columbia River edge.
10. **"All lines redrawn, walkable K-12" (`option1_full`).**
    - K-5 and 6-8 as "Redrawn K-8 lines" (`option1_durable`), without the A_hs-relative rules (the feeder penalty and the nesting cost).
    - 9-12 is redrawn from whole elementary zones. ≥75% of middle zones on one high school is near-hard (100,000 kid-miles per zone short). A soft push of 200 kid-miles per zone short of 85% applies, and nothing beyond (`parent_floor.soft_to`).
    - Elementary zones split at 9-12 only where size or durability needs it, at most 5 (`max_splits`).
    - High schools: floor 1,100, ceiling = capacity (Jefferson 1,773). Range (KPI < 350) soft. No new I-84/Willamette crossings.
11. **"Shortest walks" (`frontier_k17`), current rules.** As `option1_durable`, with no durability reward (`durable_school` = `school_year_at_target` = 0): the walk-max plan that still meets Scenario A's count in every required year. The old-rules config is `frontier_k17_psu2041.json`.
12. **Feeder-order solve and phase-2 hint.**
    - `level_order` lets a config solve K-5 → 9-12 → 6-8. "All lines redrawn, walkable K-12" (`option1_full`) uses it, so its middle zones are drawn inside its own new high-school lines (`hs_nest: {"self": true, "hard": true}`; each elementary zone takes its majority high school).
    - Phase-2 hint, finding: phase 1 satisfies the zone-level contiguity rule, but phase 2 checks the stricter block-level rule. So the whole-zone plan is not a feasible hint for phase 2a. With all variables fixed to it, CP-SAT returned INFEASIBLE (diagnostic `_diag_hint_option4`).
    - Phase-2 hint, fix: `phase2_warm` repairs it block by block (`star_repair` without groups) and turns on CP-SAT's `repair_hint` (`phase2_hint_mode: "repair"`) for the few violations left.
13. **Phase-2 warm start: not a reliable fix.** With `phase2_warm` + `repair_hint`, phase 2a still found no plan in 600 s for the 6-8 levels of `option1_durable`, `option2` (hint with 0 violations), `option4` and `option1_full`; it worked for `option1_full`'s 9-12 (4 splits) and `frontier_k17`'s 6-8 (8 splits). The old relaxation-hint path found 15 / 13 split plans for `option1_durable` / `option2`. The cause isn't known: the hint satisfies the connectivity rule, so something else in the split model rejects or ignores it. The warm start stays optional per plan.

## 8. Closeness by level

Priority: **closeness matters most for elementary, less for middle, least for high school.** How the model reflects it:

- **High school (most flexible):** every current plan keeps PPS A's traced 9-12 lines. We don't redraw them. ("All lines redrawn", which did, was dropped: its high-school trips were longer than PPS A's, 2.06 vs 1.93 mi.)
- **Middle (more flexible):** built from whole elementary zones (classmates stay together). It has a small penalty per extra high school a middle zone feeds, and PPS's 1.5-mile bus line (Transportation Service Guidelines §D.1).
- **Elementary (closeness first):** drawn for walking and size only, with PPS's 1-mile bus line.
- **What it does not do (yet):** each level is solved separately with the same walking weight (1 kid-mile per kid-mile) and the same past-a-closer-school penalty (0.25 kid-mile per kid). So no explicit rule says an elementary mile matters more than a middle-school mile.
- **Test of an explicit rule:** `option2_k5close` gives "Boundary changes, same closures" a 4× K-5 past-a-closer-school penalty (1.0 instead of 0.25; config `levels.K-5.weights`, honored by `solve.py` `_costs`), leaving 6-8 unchanged. It shows what weighting elementary closeness more costs in schools at target and kids moved.
- **Not a lever for feeders:** lowering the middle-school walking weight would not fix middle→high feeders. Elementary zones that straddle PPS A's HS lines block that at the middle level even at 10× the feeder penalty (`option1_durable/TRADEOFFS.md`, "Feeder sensitivity").

## 9. Line cleanup

The solver's boundary-length cost (3 kid-miles per km) was too weak to stop one-block trades for slightly shorter walks, so the walk redraws had more one-block notches than PPS's own lines. Cleanup method:
- **Stronger K-5 line cost.** K-5 boundary-length cost raised in rounds to 15, 30 and 45 kid-miles per km, with past-a-closer-school 1.0 kid-mile per kid. Per-level weights are honored by `solve.py` `_weights` / `_costs` via `levels.<lev>.weights`.
- **6-8 kept block for block** (`levels.6-8.fixed_run`).
- **Rule-preserving cleanup** (`smooth_v2.py`).
- **Gated swap-in** (`promote_clean.py`), driven by `clean_plan.sh`.

Line quality is measured by `lines_qa.py`. Results and criteria are in `out_v2/LINES_QA.md`. "Rebalanced PPS A" (`option4`) is not cleaned: its notches exist to fix sizes, and cleaning them moves more kids.

## Dropped: letting the solver pick which schools close

A two-stage test (`capstone2.sh`, `capstone3.sh`) let the solver choose which elementary and middle schools stay open. Stage 1 picked schools on tied pieces of the map; stage 2 redrew lines block by block. Every open school had to be at target every year, with PPS A's high-school lines. With program hosts fixed, so that no more immersion students move than in the best example we modeled (1,226), it closed 15 K-5 schools and Gray and Sellwood middle schools. Elementary kids assigned past a closer school fell to 866, but middle-school walks rose to 2.09 mi and 8,754 students were reassigned. It didn't beat PPS A's closures with redrawn lines. The earlier version moved immersion programs (1,611 students) and is ruled out by the rule that no plan moves more than PPS A's 1,567.
