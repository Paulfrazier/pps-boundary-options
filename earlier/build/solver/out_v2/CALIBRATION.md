# Calibration: model v2 vs PPS Family Guide projections

Written 2026-10-12 (models track). Data: `build/solver/out_v2/calibration_table.csv` (rebuild: `cd build/solver && ../../.venv/bin/python metrics.py --v2 today status_quo scenario_A scenario_B && ../../.venv/bin/python calibrate.py`).

**PPS numbers** are the Family Guide "How many students are expected?" tables, p. 4 of each guide (guides dated 2026-10-08, archived as `build/pps-texts/family-guide-*.md`; digitized in `build/data/scenarios.json` → `pps_projections_2027_28_to_2031_32`). PPS's "No changes" row equals the PSU PRC July 24, 2026 forecast, Table 5.5 (`build/pps-texts/boardbook-2026-10/findings.md` §b). **Ours** = building totals from our model on PPS's own traced lines (No changes (PPS Status Quo, 2027-28), PPS Scenario A, PPS Scenario B). v1 has only a 2031-32 basis. Focus/alternative schools (Winterhaven, da Vinci, Odyssey, ACCESS, MLC, Benson) are not scored.

## Verdict: calibrated (pass)

PPS measures its targets in 2031-32, so 2031-32 is the gate; 2027-28 is reported too.

| Plan | Schools scored | Within 10%, 2031-32 (v1 → v2) | Within 5%, v2 | Median abs. diff, v2 | Misses >10%, v2 2031-32 | Within 10%, v2 2027-28 |
|---|---|---|---|---|---|---|
| No changes (PPS Status Quo, 2027-28) | 76 | 74 → **74** | 74 | 0.0% | Beaumont −25%, Roseway Heights +21% | 74 |
| PPS Scenario A | 62 | 57 → **58** | 46 | 1.6% | Roseway Heights +16%, Sunnyside +19%, Atkinson +12%, Vernon −11% | 51 |
| PPS Scenario B | 65 | 59 → **61** | 50 | 1.6% | same four as A | 56 |

Every 2031-32 miss is explained below, and so is every 2027-28 miss. Mean absolute difference in PPS Scenario A fell from 5.3% (v1) to 3.4% (v2). v1's biggest PPS Scenario A misses are gone: Sunnyside +77% → +19%, Hosford +20% → +3%, Scott −12% → −4%, Rigler +8% → 0%, Lent +9% → 0%.

Plan codes in the miss tables: SQ = No changes (PPS Status Quo, 2027-28), A = PPS Scenario A, B = PPS Scenario B.

Labels: **PPS-inconsistency** = PPS's own documents disagree, so no single number can match; **our-choice** = a modeling choice of ours (stated); **timing** = PPS phases a change in over several years and our model applies it at once; **unexplained** = not traced to a cause.

## Misses in 2031-32 (the gate)

| Plan | School | Ours v2 | PPS | Diff | Category | Explanation |
|---|---|---|---|---|---|---|
| SQ | Beaumont | 313 | 418 | −25% | PPS-inconsistency | PPS's Status Quo 6-8 map (BoardBook file 14505802, dated 2026-10-03) draws the Rigler K-5 area inside Roseway Heights; PPS's numbers keep those ≈104 middle schoolers at Beaumont. We follow the map (Paul, 2026-10-12). See `build/research/pps_internal_gaps.md` §3 for the evidence. |
| SQ | Roseway Heights | 601 | 498 | +21% | PPS-inconsistency | The other side of the same Rigler-area gap. Beaumont + Roseway together: ours 914, PPS 916 (−0.2%). |
| A, B | Roseway Heights | 731 | 628 | +16% | PPS-inconsistency | Same Rigler-area gap, carried into PPS Scenario A's 6-8 map. Without the ≈104 Rigler-area kids Roseway would be ≈627 (0%). |
| A, B | Sunnyside | 280 | 235 | +19% | our-choice | Sunnyside's 2031-32 total is ours 129 own in-zone K-5 + 62 Buckman-area K-5 (the traced line; Sunnyside guide p. 3: "the area north of Burnside") + 63 Buckman lottery students (50/50, Oct 6 memo p. 2) + ≈26 Sunnyside lottery students in their last grandfathered year (Sunnyside guide p. 3: lottery students "permitted to remain through 5th grade"; 1 of 6 cohorts left in 2031-32). Our in-zone share for Sunnyside's K-5 (0.452) is a K-8-wide ratio (PPS capture report Oct 2025: 219 own-school residents; ODE 2025-26 enrollment 485), which likely overstates the K-5 in-zone count. Abernethy + Sunnyside together: ours 635, PPS 600 (+6%). PPS's year-by-year Sunnyside series (376, 343, 317, 281, 235) has the same declining shape as our phase-out (2027-28: ours 392 vs 376, +4%). |
| A, B | Atkinson | 463 | 413 | +12% | our-choice | Ours = 219 Atkinson-area + 208 Creston-area kids + 36 Spanish DLI non-arrivals who stay at Atkinson. PPS's numbers leave room for about 23 non-arrivals and no focus returners. Our returners from Sunnyside/Bridger (≈32, spread by Census residents across the Franklin cluster) and the stay share (Atkinson's stay share is not measurable from PPS's guides, `build/research/follow_rate/report.md` §5, so we use 1 − arrival share) together account for the gap. |
| A, B | Vernon | 288 | 323 | −11% | unexplained (small) | Vernon becomes K-5. Our No changes (PPS Status Quo) Vernon K-8 total matches PPS (451 vs 453), so the gap is the K-5 vs 6-8 split inside the K-8: our block grade bands come from Census age shares, PPS's from its own grade data. 35 kids; same in v1 (−10.8%). |

## Misses in 2027-28 only (timing)

PPS phases several changes in; our model applies every change in 2027-28. PPS's stated reasons: Marysville guide p. 3, "Avoiding multiple moves: Delaying full implementation ensures students previously impacted by Southeast Guiding Coalition changes do not experience multiple school moves during elementary school"; Sunnyside guide p. 3, lottery students "permitted to remain through 5th grade"; Bridger guide p. 3, "Current middle grade (6th and 7th) students would be reassigned". PPS's year-by-year rows (Family Guide p. 4) show the shape. All of these are within 10% by 2031-32 except where listed above.

| Plan | School | Ours 2027-28 | PPS 2027-28 | Diff | PPS series 2027-28 → 2031-32 | Reading |
|---|---|---|---|---|---|---|
| A, B | Arleta | 516 | 224 | +130% | 224, 536, 545, 552, 543 | Marysville merger starts 2028-29 in PPS's numbers (stated delay). |
| A | Lane (Brentwood) | 589 | 384 | +51% | 384, 586, 525, 480, 457 | Lane's new area starts 2028-29. |
| B | Lane (Brentwood) | 644 | 384 | +68% | 384, 664, 596, 542, 512 | Same. |
| A, B | Kellogg | 661 | 507 | +30% | 507, 548, 582, 556, 579 | Atkinson/Creston 6-8 kids arrive over three years. |
| A | Llewellyn | 429 | 330 | +30% | 330, 340, 367, 387, 399 | Gradual fill-in from its new area. |
| A | Hosford | 742 | 602 | +23% | 602, 747, 610, 575, 557 | Sellwood/Sunnyside middle-grade moves land in 2028-29. |
| B | Hosford | 677 | 602 | +12% | 602, 669, 540, 512, 501 | Same. |
| A, B | Tubman | 490 | 608 | −19% | 608, 546, 492, 465, 455 | PPS keeps current middle schoolers at Tubman while they finish; ours re-sorts them at once. |
| A | Duniway | 447 | 544 | −18% | 544, 517, 505, 482, 463 | Same pattern (Lewis students arrive in 2027-28 and are not re-sorted). |
| A, B | Jackson | 524 | 618 | −15% | 618, 564, 486, 428, 404 | Same pattern. |
| A, B | George | 707 | 604 | +17% | 604, 637, 669, 649, 636 | George's new 6-8 groups arrive over three years. |
| A, B | Gray | 561 | 481 | +17% | 481, 518, 551, 508, 490 | Same. |
| A, B | Roseway Heights | 766 | 655 | +17% | 655, 642, 671, 655, 628 | Not timing: the Rigler-area gap above. |
| SQ | Beaumont / Roseway Heights | 297 / 665 | 410 / 554 | −28% / +20% | | Rigler-area gap above. |


## What changed from v1 to get here (all in `build/solver/v2.py`, configs from `gen_configs_v2.py`)

1. **Fix 1, focus-lottery students** (Sunnyside, Bridger, Buckman) are a separate population. Rule (Paul, 2026-10-12): a school with a change of its own follows PPS's stated rule for it; the Family Guide p. 2 footnote ("we assume that students return to their neighborhood school") covers only schools with no change of their own.
   - Buckman closes: its enrolled students split 50/50 Abernethy/Sunnyside. Source: Oct 6 memo (BoardBook file 14509719) p. 2, "Buckman would consolidate into Abernethy and Sunnyside, with a proposed distribution of 50 percent to each." In-zone kids follow the traced line; lottery kids are a fixed 50/50. Effect: Abernethy −19% → −3%.
   - Sunnyside K-5 lottery students stay through grade 5 and none are admitted after 2026-27 (Sunnyside guide p. 3), then return home. Sunnyside 6-8 lottery students return home: the guide sends "Neighborhood 6th-8th graders" to Hosford, and PPS's Hosford projection (557) leaves no room for the lottery group (sending them to Hosford would give 669, +20%).
   - Bridger 6-8 lottery students go to Harrison Park, the guide's stated default (Bridger guide p. 3: "would be reassigned to Harrison Park Middle School or could choose to return to their neighborhood middle school").
   - Returners live where Census residents live in the host's 2025-26 high-school cluster (the same rule `build/data` uses for every focus program's homes). The first v2 pass weighted by PPS's "other neighborhood school" counts instead; those counts include DLI lottery flows and sent 43–64% of returners to Whitman (+28%) and Kellogg (+19%). With residents weighting: Whitman 0%, Kellogg +6%. Scored either way, PPS Scenario A has 58 or 59 of 62 within 10%.
2. **Fix 2, Lent-area non-DLI students** (≈117 at Marysville today; PPS capture report Oct 2025, Lent row, "other neighborhood school" 117). In the **PPS baselines** (PPS Scenario A and B) they stay with Marysville's student body and go to Arleta, following PPS's stated phase-in (Paul, 2026-10-12, revised decision 1; Marysville guide p. 3). Effect: Kelly +30% → +1.5%, Arleta −23% → +1%. In **our options** they are assigned by where they live, like every other kid.
   - **Still open (flagged):** the Marysville guide (p. 3) says "the pre-SEGC Lent neighborhood non-DLI boundary would move to Kelly", and the Kelly guide (p. 3) says Kelly "would welcome neighborhood students from Lent". Yet Kelly's projection barely moves (391 → 401 in 2031-32), even after the phase-in. Why don't Kelly's projections show any new Lent-area families after 2028-29? See `build/research/pps_internal_gaps.md` §1.
3. **Fix 3, DLI arrival shares** implied by PPS's numbers (not stated by PPS): Lent 0.80, Rigler 0.825, Woodstock 0.84–0.93, Chávez ≈0.89, Beaumont→Roseway ≈0.90 (`build/data/v2/dli_follow.json`; `build/research/follow_rate/report.md`). Effect: Rigler +8% → 0%, Lent +9% → 0%.
4. **Fix 4, capacities** from PPS 2025-26 school profiles (second-hand capture; affects in-range checks, not the sizes compared here).
5. **Fix 6, per-school PSU forecasts by year** (Table 5.5), which makes 2027-28 comparable at all.

## Caveats

- PPS doesn't publish how it built the scenario numbers (`build/pps-texts/boardbook-2026-10/findings.md` §b, "Not found"). Matching them shows that our model reproduces PPS's arithmetic. It doesn't show that either is right.
- The DLI arrival shares and the Sunnyside/Buckman/Bridger placements are fitted to or read from PPS documents. They are inputs, not independent checks.
- Options use the same population rules, so option-vs-PPS Scenario A comparisons share these assumptions.

## Per-school tables

Bold = more than 10% off. "v1 diff" and "v2 diff" are vs PPS 2031-32.

### No changes (PPS Status Quo, 2027-28)

| School | Type | v1 2031-32 | v2 2031-32 | PPS 2031-32 | v1 diff | v2 diff | v2 2027-28 | PPS 2027-28 | v2 diff 2027-28 |
|---|---|---|---|---|---|---|---|---|---|
| Abernethy | K-5 | 241 | 241 | 241 | +0.0% | +0.0% | 242 | 242 | +0.0% |
| Ainsworth | K-5 | 557 | 557 | 557 | +0.0% | +0.0% | 555 | 555 | +0.0% |
| Alameda | K-5 | 490 | 490 | 492 | -0.4% | -0.4% | 496 | 498 | -0.4% |
| Arleta | K-5 | 210 | 210 | 210 | +0.0% | +0.0% | 213 | 213 | +0.0% |
| Astor | K-8 | 419 | 419 | 418 | +0.2% | +0.2% | 413 | 412 | +0.2% |
| Atkinson | K-5 | 386 | 386 | 386 | +0.0% | +0.0% | 363 | 363 | +0.0% |
| Beach | K-5 | 287 | 287 | 287 | +0.0% | +0.0% | 284 | 284 | +0.0% |
| Beaumont | 6-8 | 313 | 313 | 418 | **-25.1%** | **-25.1%** | 297 | 410 | **-27.6%** |
| Beverly Cleary | K-8 | 394 | 394 | 389 | +1.3% | +1.3% | 436 | 430 | +1.4% |
| Boise-Eliot/Humboldt | K-5 | 309 | 309 | 308 | +0.3% | +0.3% | 315 | 314 | +0.3% |
| Bridger | K-8 | 417 | 417 | 415 | +0.5% | +0.5% | 453 | 450 | +0.7% |
| Bridlemile | K-5 | 407 | 407 | 413 | -1.5% | -1.5% | 413 | 419 | -1.4% |
| Buckman | K-5 | 239 | 239 | 239 | +0.0% | +0.0% | 244 | 244 | +0.0% |
| Capitol Hill | K-5 | 320 | 320 | 311 | +2.9% | +2.9% | 319 | 310 | +2.9% |
| Cesar Chavez | K-8 | 392 | 392 | 392 | +0.0% | +0.0% | 413 | 413 | +0.0% |
| Chapman | K-5 | 336 | 336 | 333 | +0.9% | +0.9% | 319 | 316 | +0.9% |
| Chief Joseph | K-5 | 243 | 243 | 238 | +2.1% | +2.1% | 250 | 245 | +2.0% |
| Clark | K-5 | 343 | 343 | 343 | +0.0% | +0.0% | 360 | 360 | +0.0% |
| Cleveland | 9-12 | 1318 | 1318 | 1318 | +0.0% | +0.0% | 1460 | 1460 | +0.0% |
| Creston | K-5 | 192 | 192 | 187 | +2.7% | +2.7% | 207 | 201 | +3.0% |
| Duniway | K-5 | 348 | 348 | 345 | +0.9% | +0.9% | 341 | 338 | +0.9% |
| Faubion | K-8 | 603 | 603 | 602 | +0.2% | +0.2% | 619 | 618 | +0.2% |
| Forest Park | K-5 | 258 | 258 | 258 | +0.0% | +0.0% | 260 | 260 | +0.0% |
| Franklin | 9-12 | 1492 | 1492 | 1492 | +0.0% | +0.0% | 1689 | 1689 | +0.0% |
| George | 6-8 | 389 | 389 | 390 | -0.3% | -0.3% | 390 | 391 | -0.3% |
| Glencoe | K-5 | 301 | 301 | 296 | +1.7% | +1.7% | 316 | 311 | +1.6% |
| Grant | 9-12 | 1487 | 1487 | 1487 | +0.0% | +0.0% | 1935 | 1935 | +0.0% |
| Gray | 6-8 | 366 | 366 | 368 | -0.5% | -0.5% | 425 | 427 | -0.5% |
| Grout | K-5 | 280 | 280 | 280 | +0.0% | +0.0% | 303 | 303 | +0.0% |
| Harrison Park | 6-8 | 417 | 417 | 417 | +0.0% | +0.0% | 427 | 427 | +0.0% |
| Hayhurst | K-5 | 266 | 266 | 266 | +0.0% | +0.0% | 274 | 274 | +0.0% |
| Hosford | 6-8 | 375 | 375 | 374 | +0.3% | +0.3% | 484 | 482 | +0.4% |
| Ida B. Wells | 9-12 | 1457 | 1457 | 1457 | +0.0% | +0.0% | 1524 | 1524 | +0.0% |
| Irvington | K-5 | 223 | 223 | 223 | +0.0% | +0.0% | 240 | 240 | +0.0% |
| Jackson | 6-8 | 515 | 515 | 515 | +0.0% | +0.0% | 660 | 661 | -0.2% |
| James John | K-5 | 354 | 354 | 352 | +0.6% | +0.6% | 361 | 359 | +0.6% |
| Jefferson | 9-12 | 1183 | 1183 | 1183 | +0.0% | +0.0% | 564 | 564 | +0.0% |
| Kellogg | 6-8 | 470 | 470 | 471 | -0.2% | -0.2% | 512 | 513 | -0.2% |
| Kelly | K-5 | 391 | 391 | 391 | +0.0% | +0.0% | 402 | 402 | +0.0% |
| Lane | 6-8 | 357 | 357 | 357 | +0.0% | +0.0% | 417 | 417 | +0.0% |
| Laurelhurst | K-8 | 527 | 527 | 525 | +0.4% | +0.4% | 610 | 607 | +0.5% |
| Lee | K-5 | 254 | 254 | 254 | +0.0% | +0.0% | 245 | 245 | +0.0% |
| Lent (program-only) | K-5 | 279 | 274 | 274 | +1.8% | +0.0% | 256 | 256 | +0.0% |
| Lewis | K-5 | 201 | 201 | 201 | +0.0% | +0.0% | 224 | 224 | +0.0% |
| Lincoln | 9-12 | 1411 | 1411 | 1411 | +0.0% | +0.0% | 1598 | 1598 | +0.0% |
| Llewellyn | K-5 | 312 | 312 | 312 | +0.0% | +0.0% | 312 | 312 | +0.0% |
| MLK Jr | K-5 | 337 | 337 | 337 | +0.0% | +0.0% | 337 | 337 | +0.0% |
| Maplewood | K-5 | 248 | 248 | 247 | +0.4% | +0.4% | 279 | 278 | +0.4% |
| Markham | K-5 | 345 | 345 | 347 | -0.6% | -0.6% | 310 | 312 | -0.6% |
| Marysville | K-5 | 309 | 309 | 312 | -1.0% | -1.0% | 297 | 300 | -1.0% |
| McDaniel | 9-12 | 1261 | 1261 | 1261 | +0.0% | +0.0% | 1528 | 1528 | +0.0% |
| Mt Tabor | 6-8 | 350 | 350 | 354 | -1.1% | -1.1% | 401 | 406 | -1.2% |
| Ockley Green | 6-8 | 436 | 436 | 436 | +0.0% | +0.0% | 442 | 442 | +0.0% |
| Peninsula | K-5 | 236 | 236 | 236 | +0.0% | +0.0% | 250 | 250 | +0.0% |
| Richmond (program-only) | K-5 | 497 | 497 | 497 | +0.0% | +0.0% | 504 | 504 | +0.0% |
| Rieke | K-5 | 313 | 313 | 311 | +0.6% | +0.6% | 254 | 252 | +0.8% |
| Rigler | K-5 | 327 | 327 | 321 | +1.9% | +1.9% | 312 | 306 | +2.0% |
| Roosevelt | 9-12 | 1117 | 1117 | 1117 | +0.0% | +0.0% | 1312 | 1312 | +0.0% |
| Rosa Parks | K-5 | 168 | 168 | 168 | +0.0% | +0.0% | 159 | 159 | +0.0% |
| Rose City Park | K-5 | 370 | 370 | 370 | +0.0% | +0.0% | 391 | 391 | +0.0% |
| Roseway Heights | 6-8 | 601 | 601 | 498 | **+20.7%** | **+20.7%** | 665 | 554 | **+20.0%** |
| Sabin | K-5 | 236 | 236 | 235 | +0.4% | +0.4% | 237 | 236 | +0.4% |
| Scott | K-5 | 470 | 470 | 470 | +0.0% | +0.0% | 500 | 500 | +0.0% |
| Sellwood | 6-8 | 351 | 351 | 350 | +0.3% | +0.3% | 525 | 523 | +0.4% |
| Sitton | K-5 | 309 | 309 | 311 | -0.6% | -0.6% | 331 | 333 | -0.6% |
| Skyline | K-8 | 177 | 177 | 177 | +0.0% | +0.0% | 196 | 196 | +0.0% |
| Stephenson | K-5 | 260 | 260 | 261 | -0.4% | -0.4% | 270 | 271 | -0.4% |
| Sunnyside | K-8 | 475 | 475 | 475 | +0.0% | +0.0% | 484 | 484 | +0.0% |
| Tubman | 6-8 | 374 | 374 | 374 | +0.0% | +0.0% | 457 | 457 | +0.0% |
| Vernon | K-8 | 451 | 451 | 453 | -0.4% | -0.4% | 490 | 492 | -0.4% |
| Vestal | K-5 | 282 | 282 | 279 | +1.1% | +1.1% | 297 | 294 | +1.0% |
| West Sylvan | 6-8 | 622 | 622 | 620 | +0.3% | +0.3% | 689 | 687 | +0.3% |
| Whitman | K-5 | 222 | 222 | 223 | -0.4% | -0.4% | 204 | 205 | -0.5% |
| Woodlawn | K-5 | 289 | 289 | 289 | +0.0% | +0.0% | 300 | 300 | +0.0% |
| Woodmere | K-5 | 224 | 224 | 225 | -0.4% | -0.4% | 223 | 224 | -0.4% |
| Woodstock | K-5 | 325 | 325 | 325 | +0.0% | +0.0% | 342 | 342 | +0.0% |

### PPS Scenario A

| School | Type | v1 2031-32 | v2 2031-32 | PPS 2031-32 | v1 diff | v2 diff | v2 2027-28 | PPS 2027-28 | v2 diff 2027-28 |
|---|---|---|---|---|---|---|---|---|---|
| Abernethy | K-5 | 349 | 355 | 365 | -4.4% | -2.7% | 358 | 354 | +1.1% |
| Ainsworth | K-5 | 557 | 557 | 557 | +0.0% | +0.0% | 555 | 555 | +0.0% |
| Alameda | K-5 | 490 | 490 | 493 | -0.6% | -0.6% | 496 | 498 | -0.4% |
| Arleta | K-5 | 519 | 549 | 543 | -4.4% | +1.1% | 516 | 224 | **+130.4%** |
| Astor | K-8 | 431 | 434 | 430 | +0.2% | +0.9% | 428 | 422 | +1.4% |
| Atkinson | K-5 | 395 | 463 | 413 | -4.4% | **+12.1%** | 431 | 395 | +9.1% |
| Beaumont | 6-8 | 449 | 464 | 498 | -9.8% | -6.8% | 524 | 506 | +3.6% |
| Beverly Cleary | K-5 | 451 | 451 | 484 | -6.8% | -6.8% | 492 | 503 | -2.2% |
| Boise-Eliot/Humboldt | K-5 | 505 | 505 | 512 | -1.4% | -1.4% | 516 | 521 | -1.0% |
| Bridger | K-5 | 285 | 293 | 305 | -6.6% | -3.9% | 310 | 310 | +0.0% |
| Bridlemile | K-5 | 407 | 407 | 413 | -1.5% | -1.5% | 413 | 419 | -1.4% |
| Capitol Hill | K-5 | 386 | 386 | 379 | +1.8% | +1.8% | 387 | 381 | +1.6% |
| Cesar Chavez (program-only) | K-5 | 558 | 517 | 527 | +5.9% | -1.9% | 531 | 541 | -1.8% |
| Chapman | K-5 | 336 | 336 | 333 | +0.9% | +0.9% | 319 | 316 | +0.9% |
| Chief Joseph | K-5 | 403 | 410 | 417 | -3.4% | -1.7% | 415 | 420 | -1.2% |
| Clark | K-5 | 256 | 262 | 272 | -5.9% | -3.7% | 276 | 276 | +0.0% |
| Cleveland | 9-12 | 1238 | 1238 | 1322 | -6.4% | -6.4% | 1377 | 1465 | -6.0% |
| Duniway | K-5 | 428 | 428 | 463 | -7.6% | -7.6% | 447 | 544 | **-17.8%** |
| Faubion | K-5 | 373 | 375 | 407 | -8.4% | -7.9% | 385 | 425 | -9.4% |
| Forest Park | K-5 | 258 | 258 | 258 | +0.0% | +0.0% | 260 | 260 | +0.0% |
| Franklin | 9-12 | 1543 | 1543 | 1476 | +4.5% | +4.5% | 1737 | 1686 | +3.0% |
| George | 6-8 | 673 | 673 | 636 | +5.8% | +5.8% | 707 | 604 | **+17.1%** |
| Glencoe | K-5 | 301 | 327 | 317 | -5.0% | +3.2% | 322 | 318 | +1.3% |
| Grant | 9-12 | 1487 | 1487 | 1487 | +0.0% | +0.0% | 1935 | 1935 | +0.0% |
| Gray | 6-8 | 472 | 472 | 490 | -3.7% | -3.7% | 561 | 481 | **+16.6%** |
| Grout | K-5 | 280 | 280 | 280 | +0.0% | +0.0% | 303 | 303 | +0.0% |
| Harrison Park | 6-8 | 620 | 645 | 591 | +4.9% | +9.1% | 699 | 642 | +8.9% |
| Hayhurst | K-5 | 409 | 409 | 410 | -0.2% | -0.2% | 439 | 472 | -7.0% |
| Hosford | 6-8 | 669 | 566 | 557 | **+20.1%** | +1.6% | 742 | 602 | **+23.3%** |
| Ida B. Wells | 9-12 | 1461 | 1461 | 1457 | +0.3% | +0.3% | 1529 | 1524 | +0.3% |
| Jackson | 6-8 | 409 | 409 | 404 | +1.2% | +1.2% | 524 | 618 | **-15.2%** |
| Jefferson | 9-12 | 1181 | 1181 | 1190 | -0.8% | -0.8% | 563 | 570 | -1.2% |
| Kellogg | 6-8 | 567 | 613 | 579 | -2.1% | +5.9% | 661 | 507 | **+30.4%** |
| Kelly | K-5 | 396 | 407 | 401 | -1.2% | +1.5% | 405 | 407 | -0.5% |
| Lane | 6-8 | 435 | 448 | 457 | -4.8% | -2.0% | 579 | 384 | **+50.8%** |
| Laurelhurst | K-5 | 323 | 323 | 359 | -10.0% | -10.0% | 374 | 378 | -1.1% |
| Lee | K-5 | 254 | 254 | 254 | +0.0% | +0.0% | 245 | 245 | +0.0% |
| Lent (program-only) | K-5 | 457 | 421 | 421 | +8.6% | +0.0% | 401 | 401 | +0.0% |
| Lincoln | 9-12 | 1314 | 1314 | 1331 | -1.3% | -1.3% | 1485 | 1580 | -6.0% |
| Llewellyn | K-5 | 431 | 431 | 399 | +8.0% | +8.0% | 429 | 330 | **+30.0%** |
| MLK Jr | K-5 | 377 | 377 | 383 | -1.6% | -1.6% | 373 | 376 | -0.8% |
| Markham | K-5 | 539 | 539 | 549 | -1.8% | -1.8% | 511 | 519 | -1.5% |
| McDaniel | 9-12 | 1290 | 1290 | 1281 | +0.7% | +0.7% | 1562 | 1535 | +1.8% |
| Mt Tabor | 6-8 | 554 | 574 | 546 | +1.5% | +5.1% | 657 | 645 | +1.9% |
| Ockley Green | 6-8 | 521 | 521 | 507 | +2.8% | +2.8% | 508 | 552 | -8.0% |
| Richmond (program-only) | K-5 | 497 | 497 | 497 | +0.0% | +0.0% | 504 | 504 | +0.0% |
| Rieke | K-5 | 418 | 418 | 432 | -3.2% | -3.2% | 368 | 348 | +5.7% |
| Rigler (program-only) | K-5 | 544 | 505 | 505 | +7.7% | +0.0% | 487 | 487 | +0.0% |
| Roosevelt | 9-12 | 1212 | 1212 | 1205 | +0.6% | +0.6% | 1421 | 1337 | +6.3% |
| Rosa Parks | K-5 | 464 | 472 | 472 | -1.7% | +0.0% | 492 | 481 | +2.3% |
| Roseway Heights | 6-8 | 746 | 731 | 628 | **+18.8%** | **+16.4%** | 766 | 655 | **+16.9%** |
| Scott | K-5 | 413 | 452 | 470 | **-12.1%** | -3.8% | 508 | 512 | -0.8% |
| Sitton | K-5 | 414 | 433 | 449 | -7.8% | -3.6% | 445 | 464 | -4.1% |
| Skyline | K-8 | 177 | 177 | 177 | +0.0% | +0.0% | 196 | 196 | +0.0% |
| Sunnyside | K-5 | 417 | 280 | 235 | **+77.4%** | **+19.1%** | 392 | 376 | +4.3% |
| Tubman | 6-8 | 423 | 423 | 455 | -7.0% | -7.0% | 490 | 608 | **-19.4%** |
| Vernon | K-5 | 288 | 288 | 323 | **-10.8%** | **-10.8%** | 313 | 325 | -3.7% |
| Vestal | K-5 | 492 | 494 | 500 | -1.6% | -1.2% | 506 | 507 | -0.2% |
| West Sylvan | 6-8 | 622 | 622 | 620 | +0.3% | +0.3% | 689 | 687 | +0.3% |
| Whitman | K-5 | 447 | 461 | 465 | -3.9% | -0.9% | 431 | 437 | -1.4% |
| Woodlawn | K-5 | 289 | 292 | 289 | +0.0% | +1.0% | 303 | 300 | +1.0% |
| Woodstock | K-5 | 412 | 407 | 406 | +1.5% | +0.2% | 426 | 426 | +0.0% |

### PPS Scenario B

| School | Type | v1 2031-32 | v2 2031-32 | PPS 2031-32 | v1 diff | v2 diff | v2 2027-28 | PPS 2027-28 | v2 diff 2027-28 |
|---|---|---|---|---|---|---|---|---|---|
| Abernethy | K-5 | 349 | 355 | 365 | -4.4% | -2.7% | 358 | 354 | +1.1% |
| Ainsworth | K-5 | 557 | 557 | 557 | +0.0% | +0.0% | 555 | 555 | +0.0% |
| Alameda | K-5 | 490 | 490 | 493 | -0.6% | -0.6% | 496 | 498 | -0.4% |
| Arleta | K-5 | 519 | 549 | 543 | -4.4% | +1.1% | 516 | 224 | **+130.4%** |
| Astor | K-8 | 431 | 434 | 430 | +0.2% | +0.9% | 428 | 422 | +1.4% |
| Atkinson | K-5 | 395 | 463 | 413 | -4.4% | **+12.1%** | 431 | 395 | +9.1% |
| Beaumont | 6-8 | 449 | 464 | 498 | -9.8% | -6.8% | 524 | 506 | +3.6% |
| Beverly Cleary | K-5 | 451 | 451 | 484 | -6.8% | -6.8% | 492 | 503 | -2.2% |
| Boise-Eliot/Humboldt | K-5 | 505 | 505 | 512 | -1.4% | -1.4% | 516 | 521 | -1.0% |
| Bridger | K-5 | 285 | 293 | 305 | -6.6% | -3.9% | 310 | 310 | +0.0% |
| Bridlemile | K-5 | 407 | 407 | 413 | -1.5% | -1.5% | 413 | 419 | -1.4% |
| Capitol Hill | K-5 | 320 | 320 | 311 | +2.9% | +2.9% | 319 | 310 | +2.9% |
| Cesar Chavez (program-only) | K-5 | 558 | 517 | 527 | +5.9% | -1.9% | 531 | 541 | -1.8% |
| Chapman | K-5 | 336 | 336 | 333 | +0.9% | +0.9% | 319 | 316 | +0.9% |
| Chief Joseph | K-5 | 403 | 410 | 417 | -3.4% | -1.7% | 415 | 420 | -1.2% |
| Clark | K-5 | 256 | 262 | 272 | -5.9% | -3.7% | 276 | 276 | +0.0% |
| Cleveland | 9-12 | 1314 | 1314 | 1371 | -4.2% | -4.2% | 1463 | 1480 | -1.1% |
| Duniway | K-5 | 348 | 348 | 345 | +0.9% | +0.9% | 341 | 338 | +0.9% |
| Faubion | K-5 | 373 | 375 | 407 | -8.4% | -7.9% | 385 | 425 | -9.4% |
| Forest Park | K-5 | 258 | 258 | 258 | +0.0% | +0.0% | 260 | 260 | +0.0% |
| Franklin | 9-12 | 1468 | 1468 | 1429 | +2.7% | +2.7% | 1652 | 1672 | -1.2% |
| George | 6-8 | 673 | 673 | 636 | +5.8% | +5.8% | 707 | 604 | **+17.1%** |
| Glencoe | K-5 | 301 | 327 | 317 | -5.0% | +3.2% | 322 | 318 | +1.3% |
| Grant | 9-12 | 1487 | 1487 | 1487 | +0.0% | +0.0% | 1935 | 1935 | +0.0% |
| Gray | 6-8 | 472 | 472 | 490 | -3.7% | -3.7% | 561 | 481 | **+16.6%** |
| Grout | K-5 | 280 | 280 | 280 | +0.0% | +0.0% | 303 | 303 | +0.0% |
| Harrison Park | 6-8 | 620 | 645 | 591 | +4.9% | +9.1% | 699 | 642 | +8.9% |
| Hayhurst | K-5 | 409 | 409 | 410 | -0.2% | -0.2% | 439 | 472 | -7.0% |
| Hosford | 6-8 | 626 | 522 | 501 | **+25.0%** | +4.2% | 677 | 602 | **+12.5%** |
| Ida B. Wells | 9-12 | 1461 | 1461 | 1457 | +0.3% | +0.3% | 1529 | 1524 | +0.3% |
| Jackson | 6-8 | 409 | 409 | 404 | +1.2% | +1.2% | 524 | 618 | **-15.2%** |
| Jefferson | 9-12 | 1181 | 1181 | 1190 | -0.8% | -0.8% | 563 | 570 | -1.2% |
| Kellogg | 6-8 | 567 | 613 | 579 | -2.1% | +5.9% | 661 | 507 | **+30.4%** |
| Kelly | K-5 | 396 | 407 | 401 | -1.2% | +1.5% | 405 | 407 | -0.5% |
| Lane | 6-8 | 479 | 492 | 512 | -6.4% | -3.9% | 644 | 384 | **+67.7%** |
| Laurelhurst | K-5 | 323 | 323 | 359 | -10.0% | -10.0% | 374 | 378 | -1.1% |
| Lee | K-5 | 254 | 254 | 254 | +0.0% | +0.0% | 245 | 245 | +0.0% |
| Lent (program-only) | K-5 | 457 | 421 | 421 | +8.6% | +0.0% | 401 | 401 | +0.0% |
| Lewis | K-5 | 308 | 311 | 283 | +8.8% | +9.9% | 323 | 296 | +9.1% |
| Lincoln | 9-12 | 1314 | 1314 | 1331 | -1.3% | -1.3% | 1485 | 1580 | -6.0% |
| Llewellyn | K-5 | 312 | 312 | 312 | +0.0% | +0.0% | 312 | 312 | +0.0% |
| MLK Jr | K-5 | 377 | 377 | 383 | -1.6% | -1.6% | 373 | 376 | -0.8% |
| Markham | K-5 | 345 | 345 | 347 | -0.6% | -0.6% | 310 | 312 | -0.6% |
| McDaniel | 9-12 | 1290 | 1290 | 1281 | +0.7% | +0.7% | 1562 | 1535 | +1.8% |
| Mt Tabor | 6-8 | 554 | 574 | 546 | +1.5% | +5.1% | 657 | 645 | +1.9% |
| Ockley Green | 6-8 | 521 | 521 | 507 | +2.8% | +2.8% | 508 | 552 | -8.0% |
| Richmond (program-only) | K-5 | 497 | 497 | 497 | +0.0% | +0.0% | 504 | 504 | +0.0% |
| Rieke | K-5 | 418 | 418 | 432 | -3.2% | -3.2% | 368 | 348 | +5.7% |
| Rigler (program-only) | K-5 | 544 | 505 | 505 | +7.7% | +0.0% | 487 | 487 | +0.0% |
| Roosevelt | 9-12 | 1212 | 1212 | 1205 | +0.6% | +0.6% | 1421 | 1337 | +6.3% |
| Rosa Parks | K-5 | 464 | 472 | 472 | -1.7% | +0.0% | 492 | 481 | +2.3% |
| Rose City Park | K-5 | 370 | 370 | 370 | +0.0% | +0.0% | 391 | 391 | +0.0% |
| Roseway Heights | 6-8 | 746 | 731 | 628 | **+18.8%** | **+16.4%** | 766 | 655 | **+16.9%** |
| Scott | K-5 | 253 | 292 | 301 | **-15.9%** | -3.0% | 325 | 326 | -0.3% |
| Sitton | K-5 | 414 | 433 | 449 | -7.8% | -3.6% | 445 | 464 | -4.1% |
| Skyline | K-8 | 177 | 177 | 177 | +0.0% | +0.0% | 196 | 196 | +0.0% |
| Stephenson | K-5 | 260 | 260 | 261 | -0.4% | -0.4% | 270 | 271 | -0.4% |
| Sunnyside | K-5 | 417 | 280 | 235 | **+77.4%** | **+19.1%** | 392 | 376 | +4.3% |
| Tubman | 6-8 | 423 | 423 | 455 | -7.0% | -7.0% | 490 | 608 | **-19.4%** |
| Vernon | K-5 | 288 | 288 | 323 | **-10.8%** | **-10.8%** | 313 | 325 | -3.7% |
| Vestal | K-5 | 282 | 284 | 279 | +1.1% | +1.8% | 298 | 294 | +1.4% |
| West Sylvan | 6-8 | 622 | 622 | 620 | +0.3% | +0.3% | 689 | 687 | +0.3% |
| Whitman | K-5 | 339 | 350 | 382 | **-11.3%** | -8.4% | 331 | 363 | -8.8% |
| Woodlawn | K-5 | 289 | 292 | 289 | +0.0% | +1.0% | 303 | 300 | +1.0% |
| Woodstock | K-5 | 412 | 407 | 406 | +1.5% | +0.2% | 426 | 426 | +0.0% |
