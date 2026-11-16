# Northeast: Tubman / Beaumont / Grant / Jefferson (main chat, 2026-10-27)

*Analysis by AI (Claude), directed and guided by Paul. Model figures are 2031-32 PSU-forecast neighborhood kids on Census-block homes (model v2), not PPS counts. Nothing here is a solver run; the walk tests are block-level LPs and whole-area brute force (scratchpad tubman_sites.py), seconds each.*

## Bottom line
- **The NE mess comes from building feeders from elementary lines outward.** Build them from the middle school instead: Sabin (+ Irvington west of NE 15th/Knott), Boise-Eliot/Humboldt, MLK Jr and Vernon go to Tubman, then Jefferson. Beverly Cleary (+ east Irvington) and Alameda go to Beaumont (Spanish kept home), then Grant. This is `out_v2/irv_sabin_15th` (Jefferson version): Tubman 549, Beaumont 561, Grant 1,326, Jefferson 1,342, no elementary split between two middle schools. The `_grant` version reopens the split (Tubman feeds Grant 161 / Jefferson 765; Jefferson 1,181).
- **Tubman's building is in the wrong place.** On pure nearest-school, the N Flint site draws 241 middle schoolers (incl. 52 Mandarin). Every plan therefore sends Vernon's 163 about 3.0 mi there, past Beaumont at 1.5 mi. PPS's own LRFP 2021 says Tubman "is under consideration for relocation" (`pps-texts/lrfp-2021-vol2-ne-middle-sites.md`, PDF p. 101). Its play areas are in Lillis Albina Park, not on PPS land (same page). Board member La Forte raised air quality on 2026-10-06 ([04:01:33](https://youtu.be/zOUH2Jq7Owo?t=14493); community automated transcript).
- **Best district-owned sites are the Sabin and Vernon buildings.** Each pulls about 540-560 middle schoolers on nearest-school, and both cut the NE average middle-school walk from 1.42 to about 1.22 mi. Bus-eligible kids (over 1.5 mi) drop from 663 to 356 at Sabin and 394 at Vernon.

## Sites tested (Tubman's middle school moved; Beaumont, Roseway Heights, Ockley Green fixed; all at 500+ and under capacity)

| Site | Nearest-school draw | Avg walk | Over 1.5 mi |
|---|---|---|---|
| Tubman today, N Flint | 241 | 1.42 | 663 |
| Sabin building | 558 | 1.22 | 356 |
| Vernon building | 539 | 1.23 | 394 |
| MLK Jr building | 515 | 1.28 | 426 |
| Irvington building | 369 | 1.29 | 467 |
| Meek (+ Whitaker-Adams land)* | 470 | 1.31 | 515 |
| Humboldt (KairosPDX lease)* | 505 | 1.36 | 567 |

\*Straight-line distance × 1.22 (Tubman's measured walk/straight ratio). Other rows use network walk miles.

## Lot and building (LRFP 2021 Vol 2, `pps-texts/lrfp-2021-vol2-ne-middle-sites.md`)

| | Sabin | Vernon | Tubman today | Beaumont |
|---|---|---|---|---|
| Site area | 158,123 SF / 3.63 ac | 162,914 SF / 3.74 ac | 132,858 SF / 3.05 ac | 249,163 SF / 5.72 ac |
| Building | 65,769 SF, 3 levels, 1928 | 70,833 SF, 3 levels, 1931 | 87,610 SF, 2 levels, 1952 | 91,294 SF, 2 levels, 1926 |
| Classrooms / functional capacity | 31 / 610 | 25 / 579 | 33 / 732 | 34 / 701 |
| Modulars | 4 | 4 | 0 | 0 |
| Zoning | R5, CU | R2.5, CU | CM3 | R5, CU |
| Gym | cafegymatorium; "Construct a new gymnasium" listed | one small gym, 51% of standard | (not reviewed) | (not reviewed) |
| Science / arts | no music or art room | one small science room; music and art in portables | | |

Whitaker-Adams: 10.05 ac vacant since 2007 (radon and mold), CM2/R5. LRFP plans it as an athletics hub, with the note "Confirm middle school system capacity in the area before planning for this site (Ref: Board Resolution 3195)" (PDF pp. 148-149).

## Solve request (for the models chat; not queued from here)
`tubman_at_vernon`: base `irv_sabin_15th`.
- Middle school "Tubman" relocated to the Vernon building: walk from Vernon's routing node; capacity 579 (LRFP), floor 500, Mandarin 6-8 strand with it.
- Vernon K-5 closes into Sabin; Sabin capacity 610.
- Re-solve K-5 for Sabin, Vernon, MLK Jr, Woodlawn, Rigler, Irvington-area and 6-8 NE; HS fixed as in irv_sabin_15th.
- Report Sabin K-5 size, the NE 6-8 walk, over-1.5-mi counts and feeder splits.

Variant `tubman_at_sabin`: middle school in the Sabin building, capacity 610, Sabin K-5 closed (as in A).

## Update: PPS's 2022-23 Tubman siting study, Whitaker lines, Vernon (2026-10-27 pm)
- **PPS's study:** six "(Re)Siting: due diligence" volumes, Feb 2022 to Apr 2023 (`pps-texts/tubman-siting-2022-23/`). Sites in the evaluation matrix: Humboldt (+ Jefferson South Lot), Jefferson South and Main lots, Prophet ESC, 432 NE Killingsworth, Boise-Eliot, the Concordia University site, Emanuel, Meek, Irvington, Kenton, Lloyd Center, MLK Jr, N Stanton, NE Multnomah, the PBOT yard, PP&R parks (Alberta, Dawson, Irving), Sabin, Thunderbird Way, Whitaker-Adams.
- **The Vernon building was never evaluated.** "Vernon" appears only as a neighbor of Alberta Park (city-owned; rejected because it would displace amenities serving the historically Black neighborhood) and of 432 NE Killingsworth (rejected).
- **Sabin, MLK, Irvington and Boise-Eliot were rejected as co-location sites,** i.e. sharing with the existing school: "lack of available building square footage (including floor-to-area ratio maximums). Older K-8 facilities are often poorly-suited for effective middle school instruction" (v03, 2022-06-14). A full conversion of a vacated building wasn't studied.
- **PPS's program size for Tubman is 120,000 SF** (v06 cost basis; $500-600/SF hard cost). That compares with Vernon at 70,833 SF and Sabin at 65,769 SF (LRFP). A conversion would need about 50,000 SF added on a 3.6-3.7 acre lot under R2.5/R5 limits.
- **Whitaker lines** (block LP, new 778-seat school assumed): avg walk 1.29 mi, 489 over 1.5 mi. The school draws Vernon 150, Faubion 139 and Rigler 97, and feeds Jefferson 338 / McDaniel 107. Boise-Eliot/Humboldt and MLK go to Ockley Green; Irvington and most of Sabin go to Beaumont (672). The Vernon building does better: 1.23 mi, 395, Jefferson 378 / Grant 77.
- **Keeping Vernon whole:** in the Vernon swap, Vernon K-5 moves to Sabin (1.21 mi avg, 187 of 288 over 1 mi). In the Sabin swap, Sabin K-5 moves to Vernon (1.08 mi, 147 of 236 over 1 mi) and Vernon stays in its own building. A, B and D already split Vernon's K-8 by sending its 6-8 to Tubman.

## Vernon three-way split, feeders by geography (2026-10-27 pm; scratchpad rigler_path.py; base irv_sabin_15th; middle school "Tubman" in the Vernon building)
- Vernon-zone K-5 (288) goes to the nearest of King, Sabin or Rigler. Avg walk 0.93 mi, 130 over 1 mi; MLK Jr 417, Sabin 514, Rigler 469. With King and Sabin only: 1.17 mi, 172 over 1 mi, Sabin 605/621.
- East Vernon (Rigler-bound): 91 K-5, 54 in 6-8, 60 in 9-12. Their walk to Beaumont is 0.84 mi; to Tubman at Vernon 1.38; to Roseway Heights 2.70. High school: Grant 1.62, Jefferson 2.65, McDaniel 3.06. So the neighborhood strand at Rigler should go to Beaumont and then Grant, not Rigler's Spanish path (Roseway Heights/Beaumont Spanish, then McDaniel).
- Middle LP, east Vernon to Beaumont: Tubman at Vernon 539/579, Beaumont 676/737, Roseway Heights 500, Ockley Green 529; NE avg 1.24 mi. Forcing them to Tubman instead: Tubman 579 (full), their walk 1.38 mi.
- High school: 60 east-Vernon teens Jefferson to Grant gives Grant about 1,386 and Jefferson about 1,282 (base 1,326 / 1,342).
- Solve request: `tubman_at_vernon_split3` = tubman_at_vernon, with Vernon K-5 to MLK Jr / Sabin / Rigler (Rigler gets a neighborhood strand), Rigler neighborhood to Beaumont to Grant.

## Fit, ADA, and "Vernon to King + Sabin" (2026-10-27 late)
- **Fit (base irv_sabin_15th):** Sabin K-5 is 358 (237 own + 121 Irvington-west), which fits Vernon (capacity 552 model / 579 LRFP). Sabin + Vernon K-5 together is 646 and does not fit; only Sabin's own 236 + Vernon's 288 = 524 does.
- **Swap walks:** Sabin's own kids to the Vernon building average 1.08 mi, 147 over 1 mi. Irvington-west kids to the Vernon building average 1.91 mi, all 121 over 1 mi; to Beverly Cleary 1.37 mi, 115 over 1 mi; staying at Sabin 1.04 mi, 62 over 1 mi.
- **Vernon ADA:** PPS's 2020 ADA town hall notes say "Vernon: Gym isn't accessible. No elevator. Bark chips not accessible. Ramps - too steep" (`pps-texts/ada-sabin-irvington/pps-2020-ada-town-hall-listening-notes-3.md`; staff notes of community comments, 2020; not re-verified). Vernon has 3 levels (LRFP). Its targeted seismic retrofit is nearly done (bond page, Oct 2026: gym and cafeteria finishes remain). Sabin has an elevator to all floors (state register, 1995) plus a stage lift; some main-floor split levels.
- **Over 1 mi, for Sabin-own + Irvington-west + Vernon (645 K-5 kids):**

| Package | Over 1 mi | Notes |
|---|---|---|
| A: Vernon to King + Sabin; middle school in the Vernon building | 234 | Sabin 605/621, MLK Jr 417; every elementary goes to Tubman at Vernon, then Jefferson |
| B: Swap; middle school in Sabin; Sabin + Vernon K-5 in the Vernon building; Irvington-west to BC | 351 | Vernon building 524, BC 475/531 |
| C: Vernon to King / Sabin / Rigler | 192 | Conflicts with A/B Rigler-as-regional-immersion plan |
| Base (Tubman stays on N Flint) | 151 | Vernon 289 (exempt); Tubman location problem stays |

## Lead package, bus count (2026-10-27 late; scratchpad ne_plan_bus.py)
**Package:** base irv_sabin_15th.
- Vernon K-5 goes to the nearer of MLK Jr or Sabin.
- Irvington zero-busing line: north of NE Brazee and east of about NE 12th, plus north of NE Knott (`line_options` column brazee21_knott, with lon > -122.6542) goes to Sabin; the rest goes to Beverly Cleary.
- Middle school "Tubman" moves to the Vernon building. Sabin, MLK Jr and Boise-Eliot/Humboldt feed it. Beverly Cleary and Alameda feed Beaumont.
- Boise-Eliot must go to Tubman: sending it to Ockley Green leaves Tubman at 402 and puts Ockley Green at 668, over its 657 capacity.

**Sizes (2031-32 model):** Sabin 540, BC 430, MLK Jr 416, Boise-Eliot 387. Tubman at Vernon 523, Beaumont 587, Roseway Heights 554, Ockley Green 547.

**Bus-eligible neighborhood kids** (K-5 over 1 mi, 6-8 over 1.5 mi; DLI students not included):

| Plan | K-5 | 6-8 | Total | NE subset |
|---|---|---|---|---|
| Status Quo | 3,458 | 2,320 | 5,777 | 1,302 |
| PPS A | 4,819 | 2,702 | 7,520 | 2,080 |
| PPS B | 4,490 | 2,702 | 7,192 | 1,943 |
| Plan D | 4,007 | 2,607 | 6,614 | 1,727 |
| 15th line (Tubman on Flint) | 4,004 | 2,790 | 6,793 | 1,899 |
| Lead package | 4,090 | 2,641 | 6,731 | 1,833 |

**Net vs the 15th-line plan, by today's area:**

| Area | Net | Detail |
|---|---|---|
| Vernon | -63 | K-5 +83, 6-8 -146 |
| Sabin | -61 | 6-8 |
| MLK Jr | -30 | |
| Boise-Eliot | +46 | 6-8 |
| Irvington | +45 | K-5 +4, 6-8 +41 |
| Rest | about 0 | |

**Net in the areas the package changes** (Sabin, Irvington, Vernon, MLK Jr, Boise-Eliot, BC): package 507 vs Status Quo 336 (+171), A 771 (-264), B 771 (-264), D 663 (-156). The NE-wide net (vs SQ +531, A -246, B -109, D +106) also counts base-plan differences outside the package: irv_sabin_15th closes Rose City Park (+129 vs SQ/B/D) and moves Beach (+124 vs SQ/D) and Faubion (+98 vs SQ).
