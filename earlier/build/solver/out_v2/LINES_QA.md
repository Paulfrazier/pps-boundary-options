# Line quality check (model v2)

Models track, 2026-10-13. Measured by `build/solver/lines_qa.py` on each plan's live assignment files (`out_v2/<plan>/assign_*.parquet`), with kids = PSU 2031-32 forecast [inferred: our model].

**What is counted** (on real shared block edges only):
- **Teeth (one-block notches):** blocks whose boundary is mostly (> 50%) with another school's area.
- **Fingers:** runs of 3 or more connected thin blocks (same-school share < 60%), i.e. long one-block-wide extensions.
- **Pockets:** pieces of a school's area cut off from its building's piece and touching another school's area.
  - Not counted as pockets: the 11 Washington County blocks (GEOID 41067…, a detached part of the district), rural West Hills fragments with no real shared edge, and pieces joined only across the I-84 line (as PPS's own Buckman/Sunnyside areas).
  - Middle-school "pockets" with 0 kids are rural fragments.
- **Far pockets:** runs of 3 or more blocks whose kids walk at least 0.5 mi past a closer open school. These are size choices (a school held at its minimum), e.g. Forest Park, Faubion, Clark, Glencoe.

## Overnight cleanup, before → after (K-5, 2026-10-12/13)

Rule-preserving: every plan still meets PPS A's at-target count every year, every school stays in range, and walking did not get worse beyond small tolerances (`promote_clean.py`).

| Plan | K-5 notches | K-5 past a closer school | Kids reassigned (K-5) |
|---|---|---|---|
| Boundary changes, same closures (`option2`) | 267 → 129 → 100 | 1,111 → 1,097 → 1,095 | 4,853 → 4,923 → 4,953 |
| Redrawn K-8 lines (`option1_durable`) | 327 → 141 | 1,397 → 1,285 | 4,875 → 4,914 |
| Shortest walks (`frontier_k17`) | 257 → 109 | 1,061 → 995 | — |
| Close 2 focus options (`option3a`) | 273 → 119 | 1,025 → 1,001 | — |
| Rebalanced PPS A (`option4`) | 303 (left as solved) | 1,838 | 3,594 |
| PPS A (`scenario_A`) | 197 | 1,970 | 2,935 |

Boundary changes, same closures had a second cleanup on 2026-10-14: elementary lines re-solved with Sunnyside kept south of I-84 (PPS A sends about 21 Sunnyside kids from north of I-84), then the same notch cleanup; every rule still holds.

Rebalanced PPS A was not cleaned: every notch it has fixes a school's size, and cleaning it moved 42 to 289 more K-5 kids.

Boundary changes, same closures got new elementary lines on 2026-10-15, shared with Boundary changes, balanced middle schools: a longer re-solve that keeps Sunnyside's and Abernethy's areas entirely south of I-84. Fewer kids pass a closer school (932 vs 1,095) and far pockets drop (17 vs 20), but these lines were not cleaned: a cleanup re-solve made them worse (one school short of its minimum, 1,023 kids past a closer school), so teeth rose from 100 to 147.

## Current state, all live plans

| Plan | Level | Teeth | Fingers (>=3 thin blocks) | Pockets | Far pockets (>=0.5 mi past closer) |
|---|---|---|---|---|---|
| scenario_A | K-5 | 197 (304 kids) | 15 (53 blocks) | 5 (197 kids) | 40 (1078 kids) |
| scenario_A | 6-8 | 119 (82 kids) | 7 (24 blocks) | 5 (4 kids) | 25 (872 kids) |
| option2 | K-5 | 147 (297 kids) | 10 (33 blocks) | 0 (0 kids) | 17 (471 kids) |
| option2 | 6-8 | 111 (95 kids) | 8 (28 blocks) | 1 (0 kids) | 21 (850 kids) |
| option2_ms460 | K-5 | 147 (297 kids) | 10 (33 blocks) | 0 (0 kids) | 17 (471 kids) |
| option2_ms460 | 6-8 | 58 (61 kids) | 6 (18 blocks) | 0 (0 kids) | 22 (687 kids) |
| option1_durable | K-5 | 141 (293 kids) | 10 (31 blocks) | 0 (0 kids) | 27 (674 kids) |
| option1_durable | 6-8 | 106 (89 kids) | 6 (19 blocks) | 1 (0 kids) | 21 (567 kids) |
| frontier_k17 | K-5 | 109 (232 kids) | 13 (41 blocks) | 0 (0 kids) | 21 (503 kids) |
| frontier_k17 | 6-8 | 104 (94 kids) | 10 (33 blocks) | 1 (0 kids) | 23 (898 kids) |
| option3a | K-5 | 119 (262 kids) | 13 (42 blocks) | 0 (0 kids) | 19 (470 kids) |
| option3a | 6-8 | 109 (85 kids) | 13 (43 blocks) | 1 (0 kids) | 19 (685 kids) |
| option4 | K-5 | 303 (490 kids) | 32 (113 blocks) | 0 (0 kids) | 46 (1021 kids) |
| option4 | 6-8 | 181 (116 kids) | 18 (58 blocks) | 0 (0 kids) | 24 (1238 kids) |
