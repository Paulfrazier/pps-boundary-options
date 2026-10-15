# Bus need: fast proxy (model v2)

Models track, 2026-10-12. Proxy only: no routing, no ridership rate, no bus counts.

**Rule.** PPS buses K-5 kids who live more than 1 mile from their assigned school and middle-grade kids who live more than 1.5 miles away (PPS Board Policy 4.10.100-P; Transportation Service Guidelines, rev. Aug 2024, §D.1; `build/research/sources/pps_transport_service_guidelines_2024.txt`). High schoolers mostly get TriMet passes (§D.1, lines 86–89), so 9-12 is left out here.

**Data.** `kids_over_bus_<level>` in each run's `schools.csv` / `scorecard.json`: model v2, 2031-32 projection, Census kids by home block, walk distance to the assigned school [inferred: our model, not PPS rider counts]. **Baseline = PPS Status Quo (2027-28, no closures)** (`status_quo`; Paul 2026-10-12: Today is archived). "Newly bused school" = a school with fewer than 20 eligible kids in the baseline and 20 or more under the plan. 20 is our cut (roughly a partial busload), not a PPS number.

## Kids past the bus line

| Plan | K-5 (> 1 mi) | 6-8 (> 1.5 mi) | Total | Change vs baseline |
|---|---:|---:|---:|---:|
| PPS Status Quo (baseline) | 3,496 | 2,320 | 5,816 | — |
| PPS A | 4,702 | 2,730 | 7,433 | +1,617 (+28%) |
| PPS B | 4,376 | 2,731 | 7,106 | +1,290 (+22%) |
| Redrawn K-8 lines | 4,446 | 2,661 | 7,107 | +1,291 (+22%) |
| Boundary changes, same closures | 4,116 | 2,938 | 7,055 | +1,239 (+21%) |
| Boundary changes, balanced middle schools | 4,116 | 2,779 | 6,895 | +1,079 (+19%) |

(Today's 2025-26 lines, archived: 5,757.)

## Schools that newly need buses (baseline → plan, eligible kids)

| Plan | K-5 | 6-8 |
|---|---|---|
| PPS A | 5: Rosa Parks 0→179, Scott 7→153, Beverly Cleary 9→135, MLK Jr 0→108, Sunnyside 2→61 | 2: Beaumont 0→105, Mt Tabor 11→64 |
| PPS B | 5: Rosa Parks 0→179, Beverly Cleary 9→135, MLK Jr 0→108, Lewis 1→70, Sunnyside 2→61 | 2: Beaumont 0→105, Mt Tabor 11→64 |
| Redrawn K-8 lines | 6: Rosa Parks 0→113, Scott 7→109, Beverly Cleary 9→97, MLK Jr 0→57, Sunnyside 2→47, Bridger 0→30 | 2: Beaumont 0→239, Mt Tabor 11→122 |
| Boundary changes, same closures | 7: Beverly Cleary 9→92, Rosa Parks 0→83, Scott 7→74, Bridger 0→46, Sunnyside 2→25, Laurelhurst 0→24, MLK Jr 0→24 | 2: Beaumont 0→229, Mt Tabor 11→89 |
| Boundary changes, balanced middle schools | 7: same as Boundary changes, same closures (same elementary lines) | 2: Beaumont 0→246, Mt Tabor 11→77 |

Beaumont's 0 in the baseline follows PPS's 2027-28 map, which moves the Rigler-area 6-8 kids to Roseway Heights (PPS's own numbers keep them at Beaumont; open question for PPS).

**Caveats.** Eligible doesn't mean riding, and bus count depends on routing and bell tiers (60-minute route window, guidelines §353), so these figures are not a bus count. Immersion and focus-program transport may follow different rules; they're not separated here. Plans with closures have fewer schools (K-5: 52 in the baseline → 37 under PPS A), so the median eligible per school roughly doubles (K-5 53 → 134 under PPS A).
