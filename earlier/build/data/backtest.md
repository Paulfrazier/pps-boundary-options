# Backtest: can the block model reproduce today?

Built 2026-10-12 by `scripts/04_calibrate.py` + `scripts/10_backtest_md.py`. All numbers are 2025-26 **neighborhood-program** students (school enrollment minus DLI strands, focus/lottery programs and newcomer programs where PPS/PSU publish the split; see README "Targets").

## Read this first: two different tests

1. **Final calibrated blocks vs today (the solver's input).** Each block's kids = Census-based raw count x its current area's capture factor, so blocks summed over today's lines reproduce actual neighborhood enrollment **exactly** (0.0% error at every school, every level). That is by construction, not evidence. It is the same convention the first-generation model's per-block estimate (`s` in `pps-model.json`) used.
2. **Structural backtest (the real gate).** Ignore each school's own enrollment and predict it from Census residents alone:
   - *uniform*: one district-wide capture rate per level;
   - *LOO-cluster*: the capture rate of the **other** schools in the same high-school cluster (leave-one-out) - this is the honest out-of-sample number;
   - *cross-level*: carry each block's K-5 capture factor into its 6-8 kids (and 6-8 into 9-12).
   This measures how much school-to-school variation in "who actually enrolls in the neighborhood school" exists beyond Census age counts. It bounds the error for blocks that change school, because a moved block carries its *old* area's capture factor.

## Summary

| level | areas | district capture (nbhd enrolled / Census-age residents) | MAPE uniform | MAPE LOO-cluster | MAPE cross-level | WAPE uniform | schools >15% (uniform) | final calibrated MAPE |
|---|---|---|---|---|---|---|---|---|
| K-5 | 53 | 0.50 | 21.1% | 23.2% | n/a | 19.5% | 30 | 0.0% |
| 6-8 | 23 | 0.50 | 27.1% | 34.0% | 16.9% (from K-5 factors) | 22.3% | 15 | 0.0% |
| 9-12 (7 cluster units) | 7 | 0.59 | 12.4% | n/a | 14.5% (from 6-8 factors) | 12.7% | 2 | 0.0% |

Other checks:
- K-5 raw proxy: grade-specific ages (this build) MAPE 21.1% vs all-under-18 proxy (the old `s` method) 21.4% under a uniform rate - a small improvement, not a large one.
- Old `s` (2024-25 NCES totals minus immersion estimates) vs 2025-26 neighborhood actuals: MAPE 6.6%. Biggest miss: **Hayhurst `s`=451 vs 290** - the old K5 count included the Odyssey K-8 program (ODE reports it inside Hayhurst). Old `s` sums to 14,897; new `k5` sums to 14372.
- 6-8 Rigler question: the PPS 2027-28 Status-Quo map draws the Rigler K-5 area in Roseway Heights; the City/PPS 2023-24 layer has it in Beaumont. Moving it raises MAPE (27.1% -> 28.3%) and pushes Roseway to +33%/Beaumont to -23%, so the current-layer assignment (Beaumont) is kept for calibration.

## Verdict

- Census residents alone are a weak predictor of who enrolls in each neighborhood school: capture rates run from ~0.27 (Beach, Cesar Chavez: DLI-dominated) to >1 (Bridger, Sunnyside: focus lotteries). The out-of-sample error (LOO-cluster MAPE ~23% K-5, ~34% 6-8) is the honest "model error" for any school whose population is mostly *new* territory.
- Because calibration is per area, the solver's error is concentrated in **moved blocks**: they carry their old area's capture rate. For boundary edits between similar neighborhoods this is small; for blocks moving out of DLI/focus-heavy areas (Beach, Cesar Chavez, Rigler, Lent, Sunnyside, Bridger, Buckman) it can be large - see README "Assumptions the solver must know".
- The gate passes in the sense that matters (today is reproduced exactly; total kids per level are right; cross-level carry-over of capture factors cuts the 6-8 error from 27% to 17%), **but** any school-size result within ~15% of a threshold (360 / 500 / 1,100) should be treated as uncertain.

## K-5 (53 current K-5/K-8 areas)

| school | actual nbhd 2025-26 | Census raw | capture | uniform-rate pred | err % | LOO-cluster err % | final calibrated | flag |
|---|---|---|---|---|---|---|---|---|
| Beach | 133 | 493 | 0.27 | 249 | +87 | +77 | 133 | **>15%** |
| Cesar Chavez | 88 | 324 | 0.27 | 163 | +85 | +72 | 88 | **>15%** |
| Bridger | 306 | 248 | 1.23 | 125 | -59 | -56 | 306 | **>15%** |
| Chapman | 333 | 1014 | 0.33 | 512 | +54 | +49 | 333 | **>15%** |
| Whitman | 193 | 564 | 0.34 | 284 | +47 | +56 | 193 | **>15%** |
| Sunnyside | 292 | 329 | 0.89 | 166 | -43 | -38 | 292 | **>15%** |
| Buckman | 283 | 336 | 0.84 | 169 | -40 | -43 | 283 | **>15%** |
| Marysville | 304 | 389 | 0.78 | 197 | -35 | -29 | 304 | **>15%** |
| Atkinson | 188 | 496 | 0.38 | 250 | +33 | +58 | 188 | **>15%** |
| Rosa Parks | 160 | 419 | 0.38 | 212 | +32 | +21 | 160 | **>15%** |
| Rose City Park | 210 | 545 | 0.39 | 275 | +31 | +30 | 210 | **>15%** |
| Laurelhurst | 379 | 539 | 0.70 | 272 | -28 | -21 | 379 | **>15%** |
| Ainsworth | 273 | 691 | 0.40 | 349 | +28 | +14 | 273 | **>15%** |
| Lewis | 262 | 375 | 0.70 | 189 | -28 | -30 | 262 | **>15%** |
| Abernethy | 269 | 679 | 0.40 | 343 | +27 | +34 | 269 | **>15%** |
| Lent | 256 | 369 | 0.69 | 186 | -27 | -19 | 256 | **>15%** |
| Faubion | 377 | 564 | 0.67 | 284 | -25 | -31 | 377 | **>15%** |
| Clark | 273 | 672 | 0.41 | 339 | +24 | +23 | 273 | **>15%** |
| Woodlawn | 323 | 486 | 0.67 | 245 | -24 | -36 | 323 | **>15%** |
| Woodstock | 177 | 431 | 0.41 | 217 | +23 | +26 | 177 | **>15%** |
| Alameda | 515 | 800 | 0.64 | 404 | -22 | -13 | 515 | **>15%** |
| James John | 232 | 556 | 0.42 | 281 | +21 | +10 | 232 | **>15%** |
| Boise-Eliot/Humboldt | 295 | 465 | 0.63 | 235 | -20 | -10 | 295 | **>15%** |
| Astor | 264 | 418 | 0.63 | 211 | -20 | -31 | 264 | **>15%** |
| Sitton | 207 | 489 | 0.42 | 247 | +19 | +8 | 207 | **>15%** |
| Scott | 254 | 593 | 0.43 | 299 | +18 | +15 | 254 | **>15%** |
| Glencoe | 341 | 792 | 0.43 | 400 | +17 | +41 | 341 | **>15%** |
| Arleta | 230 | 532 | 0.43 | 268 | +17 | +37 | 230 | **>15%** |
| Skyline | 139 | 231 | 0.60 | 116 | -16 | -29 | 139 | **>15%** |
| Forest Park | 264 | 604 | 0.44 | 305 | +16 | +0 | 264 | **>15%** |
| Markham | 339 | 772 | 0.44 | 390 | +15 | +11 | 339 |  |
| Rieke | 266 | 604 | 0.44 | 305 | +15 | +10 | 266 |  |
| Bridlemile | 423 | 725 | 0.58 | 366 | -13 | -32 | 423 |  |
| MLK Jr | 126 | 282 | 0.45 | 142 | +13 | +32 | 126 |  |
| Vestal | 286 | 620 | 0.46 | 313 | +9 | +6 | 286 |  |
| Creston | 219 | 474 | 0.46 | 239 | +9 | +27 | 219 |  |
| Duniway | 362 | 654 | 0.55 | 330 | -9 | -9 | 362 |  |
| Chief Joseph | 247 | 532 | 0.46 | 269 | +9 | -3 | 247 |  |
| Stephenson | 281 | 512 | 0.55 | 258 | -8 | -15 | 281 |  |
| Llewellyn | 345 | 635 | 0.54 | 320 | -7 | -7 | 345 |  |
| Beverly Cleary | 276 | 514 | 0.54 | 260 | -6 | +9 | 276 |  |
| Rigler | 291 | 545 | 0.53 | 275 | -6 | -10 | 291 |  |
| Grout | 327 | 684 | 0.48 | 345 | +6 | +8 | 327 |  |
| Kelly | 268 | 502 | 0.53 | 253 | -6 | +9 | 268 |  |
| Capitol Hill | 329 | 682 | 0.48 | 344 | +5 | -1 | 329 |  |
| Maplewood | 288 | 594 | 0.48 | 300 | +4 | -2 | 288 |  |
| Peninsula | 239 | 455 | 0.53 | 230 | -4 | -15 | 239 |  |
| Sabin | 270 | 547 | 0.49 | 276 | +2 | +21 | 270 |  |
| Lee | 251 | 486 | 0.52 | 245 | -2 | -7 | 251 |  |
| Hayhurst | 290 | 587 | 0.49 | 296 | +2 | -4 | 290 |  |
| Woodmere | 226 | 440 | 0.51 | 222 | -2 | +13 | 226 |  |
| Irvington | 259 | 509 | 0.51 | 257 | -1 | +16 | 259 |  |
| Vernon | 344 | 678 | 0.51 | 342 | -1 | -5 | 344 |  |

### K-5 schools off by more than 15% (uniform rate) and likely why (hypotheses from program/transfer patterns - not verified with PPS transfer data)
- **Beach** (+87%): Half of the building is the Spanish DLI strand; in-area kids who enroll in the DLI are not 'neighborhood' (capture 0.27).
- **Cesar Chavez** (+85%): 2/3 of the school is Spanish DLI; neighborhood program is only ~88 K-5 kids.
- **Bridger** (-59%): Creative Science focus lottery draws students from outside the area (capture >100%).
- **Chapman** (+54%): Downtown/NW: high private-school share and many Census kids in non-family housing; also feeds Ainsworth DLI.
- **Whitman** (+47%): Low capture: transfers out (charters, Lent DLI, Winterhaven/focus) in outer SE.
- **Sunnyside** (-43%): Environmental focus lottery draws from outside the area (capture ~0.9-1.2).
- **Buckman** (-40%): Arts focus option draws from outside the area.
- **Marysville** (-35%): High capture; area also feeds Lent DLI under SEGC history; small raw base.
- **Atkinson** (+33%): Half the school is Spanish DLI (not counted); transfers out to Winterhaven/Richmond/focus nearby.
- **Rosa Parks** (+32%): Transfers out (charters, Cesar Chavez DLI), plus Census undercount of churn in subsidized housing.
- **Rose City Park** (+31%): Half the school is Vietnamese DLI (not counted); transfers out.
- **Laurelhurst** (-28%): Very high neighborhood capture (affluent, popular K-8); few DLI/private drains measured.
- **Ainsworth** (+28%): Half the school is Spanish DLI; downtown private-school share.
- **Lewis** (-28%): Small, high-capture area (Sellwood/Westmoreland).
- **Abernethy** (+27%): Close-in SE with private/focus (Winterhaven, Sunnyside, Richmond) drain.
- **Lent** (-27%): Whole-school Spanish DLI: enrollment includes DLI students from outside the small area.
- **Faubion** (-25%): K-8 with high in-area capture plus transfers in (new building).
- **Clark** (+24%): Mandarin DLI not counted; outer-SE transfers out.
- **Woodlawn** (-24%): Transfers in / high capture relative to Census age counts.
- **Woodstock** (+23%): Mandarin DLI not counted; Winterhaven/da Vinci draw nearby.
- **Alameda** (-22%): High-income area with very high public-school capture and transfers in.
- **James John** (+21%): Spanish DLI strand not counted.
- **Boise-Eliot/Humboldt** (-20%): Transfers in; Census 2020 kids undercount 2025 (new housing in Eliot/Lloyd).
- **Astor** (-20%): K-8 with high capture; area is small relative to its draw.
- **Sitton** (+19%): Spanish DLI strand not counted.
- **Scott** (+18%): Spanish DLI strand not counted.
- **Glencoe** (+17%): Richmond (Japanese DLI) and focus schools draw from this area.
- **Arleta** (+17%): Transfers out (Lent DLI, charters).
- **Skyline** (-16%): Rural area, tiny Census base; K-8 draws some out-of-area students.
- **Forest Park** (+16%): High private-school share in NW hills.

## 6-8 (23 current middle areas; K-8s count their own 6-8)

| school | actual nbhd 2025-26 | Census raw | capture | uniform-rate pred | err % | LOO-cluster err % | final calibrated | flag |
|---|---|---|---|---|---|---|---|---|
| George | 249 | 803 | 0.31 | 404 | +62 | +55 | 249 | **>15%** |
| Cesar Chavez | 55 | 172 | 0.32 | 86 | +58 | +32 | 55 | **>15%** |
| Sunnyside | 193 | 164 | 1.18 | 83 | -57 | -47 | 193 | **>15%** |
| Bridger | 140 | 125 | 1.12 | 63 | -55 | -42 | 140 | **>15%** |
| Harrison Park | 308 | 914 | 0.34 | 460 | +49 | +79 | 308 | **>15%** |
| Laurelhurst | 235 | 262 | 0.90 | 132 | -44 | -52 | 235 | **>15%** |
| Faubion | 223 | 267 | 0.83 | 135 | -40 | -46 | 223 | **>15%** |
| Astor | 137 | 183 | 0.75 | 92 | -33 | -49 | 137 | **>15%** |
| Tubman | 354 | 907 | 0.39 | 457 | +29 | +42 | 354 | **>15%** |
| Beaumont | 315 | 787 | 0.40 | 396 | +26 | +34 | 315 | **>15%** |
| Sellwood | 566 | 834 | 0.68 | 420 | -26 | -33 | 566 | **>15%** |
| West Sylvan | 567 | 1396 | 0.41 | 703 | +24 | +39 | 567 | **>15%** |
| Beverly Cleary | 204 | 314 | 0.65 | 158 | -23 | -29 | 204 | **>15%** |
| Lane | 411 | 978 | 0.42 | 493 | +20 | +35 | 411 | **>15%** |
| Vernon | 195 | 325 | 0.60 | 164 | -16 | -20 | 195 | **>15%** |
| Skyline | 68 | 120 | 0.56 | 61 | -11 | -28 | 68 |  |
| Ockley Green | 397 | 873 | 0.46 | 440 | +11 | -16 | 397 |  |
| Kellogg | 330 | 586 | 0.56 | 295 | -11 | +43 | 330 |  |
| Gray | 432 | 786 | 0.55 | 396 | -8 | -2 | 432 |  |
| Mt Tabor | 208 | 382 | 0.54 | 193 | -7 | +39 | 208 |  |
| Jackson | 688 | 1272 | 0.54 | 641 | -7 | +2 | 688 |  |
| Hosford | 528 | 1094 | 0.48 | 551 | +4 | +12 | 528 |  |
| Roseway Heights | 415 | 790 | 0.53 | 398 | -4 | -8 | 415 |  |

### 6-8 schools off by more than 15% and likely why (hypotheses from program/transfer patterns - not verified with PPS transfer data)
- **George** (+62%): Most N Portland 6-8 kids attend K-8s (Astor, Cesar Chavez) or Spanish DLI; neighborhood 6-8 small.
- **Cesar Chavez** (+58%): 2/3 of the school is Spanish DLI; neighborhood program is only ~88 K-5 kids.
- **Sunnyside** (-57%): Environmental focus lottery draws from outside the area (capture ~0.9-1.2).
- **Bridger** (-55%): Creative Science focus lottery draws students from outside the area (capture >100%).
- **Harrison Park** (+49%): Recently converted from K-8; many in-area 6-8 kids in Kellogg DLI, Bridger K-8, da Vinci/Winterhaven, charters.
- **Laurelhurst** (-44%): Very high neighborhood capture (affluent, popular K-8); few DLI/private drains measured.
- **Faubion** (-40%): K-8 with high in-area capture plus transfers in (new building).
- **Astor** (-33%): K-8 with high capture; area is small relative to its draw.
- **Tubman** (+29%): Low capture; transfers out (da Vinci, Winterhaven, charters, Vernon/Faubion K-8 choices).
- **Beaumont** (+26%): Spanish DLI not counted; da Vinci draws heavily from NE.
- **Sellwood** (-26%): High capture, transfers in.
- **West Sylvan** (+24%): Spanish DLI not counted; private-school share in West Hills.
- **Beverly Cleary** (-23%): No specific explanation found; within the spread of capture rates.
- **Lane** (+20%): Russian DLI small; transfers out.
- **Vernon** (-16%): No specific explanation found; within the spread of capture rates.

## 9-12 (7 units: Jefferson's dual-assignment zones are pooled with the partner school because 2025-26 students could choose either)

| school | actual nbhd 2025-26 | Census raw | capture | uniform-rate pred | err % | LOO-cluster err % | final calibrated | flag |
|---|---|---|---|---|---|---|---|---|
| Grant | 1966 | 2472 | 0.80 | 1465 | -26 | n/a | 1966 | **>15%** |
| Roosevelt | 1238 | 2499 | 0.49 | 1481 | +20 | n/a | 1238 | **>15%** |
| Cleveland | 1336 | 2584 | 0.52 | 1531 | +15 | n/a | 1336 |  |
| McDaniel | 1389 | 2547 | 0.55 | 1509 | +9 | n/a | 1389 |  |
| Ida B. Wells | 1574 | 2449 | 0.64 | 1451 | -8 | n/a | 1574 |  |
| Franklin | 1578 | 2854 | 0.55 | 1691 | +7 | n/a | 1578 |  |
| Lincoln | 1469 | 2402 | 0.61 | 1423 | -3 | n/a | 1469 |  |

### 9-12 flags (likely causes, not verified)
- **Grant** (-26%): Transfers in and the Jefferson dual-assignment zones mostly choose Grant.
- **Roosevelt** (+20%): Transfers out (Benson, charters) and to Jefferson.
