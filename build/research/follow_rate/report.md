# DLI follow rate: where the "80–84%" comes from

Retrieved/checked: 2026-10-12. Labels: **[PPS]** = PPS-original document; **[2nd-hand]** = community site or repo; **[inference]** = our own arithmetic. Source copies with front matter in `sources/` (originals in `sources/originals/`); recompute with `scripts/implied_follow.py`.

## Verdict

**PPS does not state a follow rate.** The "80–84%" is the pps-dli-explorer site's own calculation, and the site says so (equity.qmd line 412: "The guides don't state a follow rate; these shares are implied by their numbers"). For each move it takes the receiving school's PPS Family Guide projection under the options (p. 4, guides dated 2026-10-08), subtracts the guide's "no changes" projection, and divides by PSU's 2026-27 forecast for the moving program, for Atkinson→Lent, Scott→Rigler and Clark→Woodstock. The arithmetic checks out, but:

- **"80–84%" covers 2027-28 only.** For 2031-32: Lent 80.3%, Rigler 82.5%, Woodstock 93.1%.
- **In PPS's numbers, students who don't arrive stay at the sending school; they don't leave PPS.** Arrive + stay is 100–112% wherever the sending school can be measured.
- **This fully explains our gap with PPS:** Rigler 544 − 505 = 39 = 223 − 184; Lent 457 − 421 = 36 = 183 − 147.

Suggested wording: "PPS's Family Guide projections imply about 80–83% of students arrive at Lent and Rigler, with the rest staying at the sending school; PPS doesn't state a rate."

## 1. pps-dli-explorer [2nd-hand]

- Repo: https://github.com/jminnier/pps-dli-explorer, commit d9d683eb31370d40a1d9659e4b212e3eb93fb9bb (2026-10-11).
- Live page: https://pps-dli-explorer.netlify.app/equity.html (retrieved with browse 2026-10-12; matches repo).

- **Line 77 (summary bullet):** "PPS's own school projections now expect only `r fol_range` of students in a moved program to follow it. The rest would stay at neighborhood schools." Renders as "80–84%".
- **Line 399 (§5):** "Their 'no changes' figures match PSU's 2026-27 forecast exactly. So we can compare a moved program's arrival with PSU's forecast for that program. In the three moves where nothing else changes at the receiving school, PPS projects that `r fol_range` of the program's students arrive. Where the guides show the sending school, the rest stay there as neighborhood students."
- **Line 412 (table note):** "Other moves (to César Chávez, Sitton and Vestal) come with boundary or grade changes and can't be separated. The guides don't state a follow rate; these shares are implied by their numbers."
- **Line 598:** asks PPS to "Publish the share of families the projections assume will follow each moved program."
- **Range:** line 48 sets `fol_range` from the min/max of the 2027-28 rows only.
- **Calculation (equity_analysis.R lines 307–336):**
  - followed = (receiving school under options − its "no changes" projection) / PSU program forecast
  - stayed = (sending school under options − PSU forecast of its other program) / PSU program forecast
  - The script errors if any guide "No changes" figure differs from the PSU school total.
- **Inputs:** [PPS] Family Guide p. 4; [PSU, prepared for PPS] 2026-27 to 2035-36 forecast, school_program rows.

## 2. Right Size Portland [2nd-hand]

- Page: https://rightsizepdx.com/rightsizing-scenario-explorer.html — byte-identical to github.com/southie/ppsrightsize at bbfa1a3c148a9098e10cab052d531d0d9f78bbc0 (sha256 1606ae0e…a1a4a).
- **D.assumptions (line 488):** "Immersion programs move with their projected program enrollment (Table 5.5 program rows); closed schools' programs move whole." = 100% follow.
- **Line 2277:** "no students are assumed to leave PPS … receiving schools' enrollment … are an upper bound."
- 2031-32 Scenario A: Rigler 544, Lent 457, César Chávez 578, Woodstock 412 (Rigler and Lent identical to ours).
- No follow, retention or attrition rate anywhere; `moveShares` covers neighborhood-area reassignment only, not immersion.

## 3. PPS documents [PPS]: no follow rate found

- **SEGC Equity Audit, p. 11** (`build/pps-texts/segc-equity-audit-evaluation-report.md`): "Students enrolled in DLI programs that moved generally followed their program … when they stayed in PPS." Also: "The Mandarin middle school DLI program is enrolled about 80% of its peak pre-relocation size (97 vs. 121) … 43% below the SEGC plan's enrollment forecast of 168." Both are post-2023 outcomes, not projection inputs.
- **SEGC School-by-School, p. 15:** "about an 86% retention rate" is about staff at Bridger; not relevant.
- **Family Guides, Regional Summaries, Scenarios Overview:** only "All figures are projections for the 2031–32 school year"; no method.
- **FAQ DLI answer:** "We look at specialized programs as full learning experiences from PK-12 … PPS will make sure every student gets the required services and support they need."
- **Board PowerPoint 2026-10-06, district-wide scenarios 2026-10-04:** nothing on follow rates or method.
- Live pps.net rightsize, FAQ and impact pages checked 2026-10-12: nothing new. Presentations and scenarios pages didn't render as text headlessly; local copies from the same day used.

## 4. Closest PPS statement [PPS speech; community transcript, NOT checked against video]

Teaching, Learning & Enrollment Committee, 2026-09-08, https://youtu.be/S-pk57P6f_o?t=2002 (33:22–34:21). Speaker: PPS staff ("Speaker 8"). Source: segment seg_000048 of the DLI explorer's transcript JSON (`sources/dli-explorer_transcript_2026-09-08_TLE.md`).

> "we do use projections … we do have to make some assumptions about how students will move through the system. What we saw in … the Southeast enrollment balancing is that when we move, for example, a program … we did not see students necessarily leave the district, but they may not have moved with the program … we will be using projections, and some of those we will track over time."

No number given.

## 5. Implied rates [inference]

From PPS Family Guide numbers (re-checked against `build/pps-texts/family-guide-*.md`) and PSU 2026-27 program rows.

| Move (scenario) | Year | PSU program | Host no-change | Host option | Arrive | Arrive % | Stay | Stay % | Arrive+Stay |
|---|---|---|---|---|---|---|---|---|---|
| Atkinson Spanish→Lent (A=B) | 2027-28 | 182 | 256 | 401 | 145 | 79.7 | – | – | – |
| | 2031-32 | 183 | 274 | 421 | 147 | 80.3 | – | – | – |
| Scott Spanish→Rigler (B; Rigler row "Options A and B") | 2027-28 | 223 | 306 | 487 | 181 | 81.2 | 49 | 22.0 | 103% |
| | 2031-32 | 223 | 321 | 505 | 184 | 82.5 | 54 | 24.2 | 107% |
| Clark Mandarin→Woodstock (A=B) | 2027-28 | 100 | 342 | 426 | 84 | 84.0 | 16 | 16.0 | 100% |
| | 2031-32 | 87 | 325 | 406 | 81 | 93.1 | 16 | 18.4 | 112% |

**César Chávez (rough):** PPS guide 527 (2031-32), 541 (2027-28). Programs moving in (PSU 2031-32): Beach 127 + Sitton 113 + James John 136 = 376. Chávez's own K-5 Spanish: PSU reports only K-8 Spanish (295); using the 2025-26 K-5 share (195/300 ≈ 65%) gives ≈192. Implied arrival (527 − 192) / 376 ≈ 89% (2027-28 ≈ 90%). Treat as roughly 85–90%; depends on the K-5 share guess.

**Pattern:** not one flat rate. Woodstock arrivals hold at ~81–84/yr while Clark's program forecast falls 100→87, so the share climbs to 93%. Arrive + stay ≥ 100% everywhere measurable. The stay share is not the share of program students living in the sending school's area (82% at Scott, 78% at Clark per the DLI explorer's equity_home_check.csv), which is far above the 22% / 16% who stay.

## 6. Implications for our model

- **To calibrate to PPS:** per-move arrival shares ≈ 0.80 Lent, 0.825 Rigler, 0.84–0.93 Woodstock, ≈ 0.89 Chávez; add the remainder to the sending school's neighborhood count rather than dropping it. This reproduces PPS's 505 and 421 exactly.
- **When citing:** say PPS projections "imply" these rates. Don't write "PPS expects only 80–84% to follow" — it reads as PPS-stated and as students lost.
- `build/research/compare_resources.md` line 284 and PLAN.md fix #3 should be reworded to match.
